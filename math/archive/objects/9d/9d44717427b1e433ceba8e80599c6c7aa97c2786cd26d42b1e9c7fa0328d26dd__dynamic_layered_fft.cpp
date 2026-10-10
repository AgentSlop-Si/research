#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

extern "C" {
typedef double fftw_complex[2];
typedef struct fftw_plan_s *fftw_plan;
fftw_plan fftw_plan_dft_r2c_1d(int n, double *in, fftw_complex *out, unsigned flags);
void fftw_execute_dft_r2c(const fftw_plan p, double *in, fftw_complex *out);
void fftw_destroy_plan(fftw_plan p);
}
static constexpr unsigned FFTW_ESTIMATE_ = (1u << 6);
using C = std::complex<double>;
using Clock = std::chrono::steady_clock;

static double ms_since(Clock::time_point t0) {
    return std::chrono::duration<double, std::milli>(Clock::now()-t0).count();
}

static bool is_pow2(size_t n){ return n && ((n & (n-1))==0); }
static unsigned ilog2_pow2(size_t n){ unsigned r=0; while((size_t(1)<<r)<n) ++r; return r; }
static size_t bit_reverse(size_t x, unsigned bits){
    size_t y=0;
    for(unsigned i=0;i<bits;i++){ y=(y<<1)|(x&1); x>>=1; }
    return y;
}

class FFTWReal {
    int n_;
    std::vector<double> scratch_;
    std::vector<std::array<double,2>> out_;
    fftw_plan plan_{};
public:
    explicit FFTWReal(int n):n_(n),scratch_(n),out_(n/2+1){
        plan_=fftw_plan_dft_r2c_1d(n_, scratch_.data(), reinterpret_cast<fftw_complex*>(out_.data()), FFTW_ESTIMATE_);
        if(!plan_) throw std::runtime_error("fftw plan failed");
    }
    ~FFTWReal(){ if(plan_) fftw_destroy_plan(plan_); }
    void run(const std::vector<double>& x){
        fftw_execute_dft_r2c(plan_, const_cast<double*>(x.data()), reinterpret_cast<fftw_complex*>(out_.data()));
    }
    const std::vector<std::array<double,2>>& out() const { return out_; }
};

struct UpdateStats {
    uint64_t butterflies=0;
    uint64_t complex_outputs=0;
    double ms=0;
};

class LayeredDynamicFFT {
    size_t n_;
    unsigned L_;
    std::vector<double> input_;
    std::vector<std::vector<C>> stage_; // stage 0 bit-reversed leaves; stage L full DFT
    std::vector<std::vector<C>> tw_;    // tw_[s][j], s>=1
    std::vector<int> mark_;
    int epoch_=1;
public:
    explicit LayeredDynamicFFT(const std::vector<double>& x):n_(x.size()),L_(ilog2_pow2(x.size())),input_(x),stage_(L_+1,std::vector<C>(n_)),tw_(L_+1),mark_(n_,0){
        if(!is_pow2(n_)) throw std::invalid_argument("N must be power of two");
        for(size_t i=0;i<n_;++i) stage_[0][bit_reverse(i,L_)] = C(x[i],0.0);
        constexpr double PI=3.141592653589793238462643383279502884;
        for(unsigned s=1;s<=L_;++s){
            size_t len=size_t(1)<<s, half=len>>1;
            tw_[s].resize(half);
            for(size_t j=0;j<half;++j) tw_[s][j]=std::polar(1.0,-2.0*PI*double(j)/double(len));
            auto &prev=stage_[s-1]; auto &cur=stage_[s];
            for(size_t block=0;block<n_;block+=len){
                for(size_t j=0;j<half;++j){
                    C u=prev[block+j]; C v=prev[block+j+half]*tw_[s][j];
                    cur[block+j]=u+v; cur[block+j+half]=u-v;
                }
            }
        }
    }
    const std::vector<double>& input() const { return input_; }
    const std::vector<C>& spectrum() const { return stage_[L_]; }

    UpdateStats add_deltas(const std::vector<std::pair<size_t,double>>& edits){
        auto t0=Clock::now();
        std::vector<size_t> dirty;
        dirty.reserve(edits.size());
        ++epoch_; if(epoch_==0){ std::fill(mark_.begin(),mark_.end(),0); epoch_=1; }
        for(auto [idx,delta]:edits){
            if(idx>=n_) throw std::out_of_range("edit idx");
            input_[idx]+=delta;
            size_t p=bit_reverse(idx,L_);
            stage_[0][p] += C(delta,0.0);
            if(mark_[p]!=epoch_){ mark_[p]=epoch_; dirty.push_back(p); }
        }
        UpdateStats st;
        for(unsigned s=1;s<=L_;++s){
            size_t len=size_t(1)<<s, half=len>>1;
            ++epoch_; if(epoch_==0){ std::fill(mark_.begin(),mark_.end(),0); epoch_=1; }
            std::vector<size_t> butterflies; butterflies.reserve(dirty.size());
            for(size_t idx:dirty){
                size_t block=idx & ~(len-1);
                size_t local=idx-block;
                size_t j=local % half;
                size_t key=block+j; // first output position identifies butterfly
                if(mark_[key]!=epoch_){ mark_[key]=epoch_; butterflies.push_back(key); }
            }
            auto &prev=stage_[s-1]; auto &cur=stage_[s];
            std::vector<size_t> next; next.reserve(butterflies.size()*2);
            for(size_t key:butterflies){
                size_t block=key & ~(len-1);
                size_t j=key-block;
                C u=prev[key]; C v=prev[key+half]*tw_[s][j];
                cur[key]=u+v; cur[key+half]=u-v;
                next.push_back(key); next.push_back(key+half);
            }
            st.butterflies += butterflies.size();
            st.complex_outputs += 2*butterflies.size();
            dirty.swap(next);
        }
        st.ms=ms_since(t0);
        return st;
    }
};

static double max_err_half(const LayeredDynamicFFT& inc, const FFTWReal& ref){
    const auto &a=inc.spectrum(); const auto &b=ref.out();
    double e=0;
    for(size_t k=0;k<b.size();++k){
        C z(b[k][0],b[k][1]); e=std::max(e,std::abs(a[k]-z));
    }
    return e;
}

static uint64_t predicted_nodes(size_t n,size_t k){
    // Upper bound on dirty complex outputs across radix-2 stages.
    uint64_t total=0;
    for(size_t width=2;width<=n;width<<=1){
        uint64_t v=std::min<uint64_t>(n, uint64_t(k)*uint64_t(width));
        total += v;
    }
    return total;
}

int main(int argc,char**argv){
    std::vector<size_t> Ns={65536,262144};
    int reps=9;
    if(argc>1) Ns={size_t(std::stoull(argv[1]))};
    if(argc>2) reps=std::stoi(argv[2]);
    std::mt19937_64 rng(0xDA70BEEF1234ULL);
    std::normal_distribution<double> normal(0.0,1.0);
    std::uniform_real_distribution<double> delta(-0.25,0.25);
    std::cout << "N,k,inc_ms,fftw_ms,speedup,dirty_outputs,predicted_upper,max_err\n";
    for(size_t n:Ns){
        std::vector<double> x(n); for(double &v:x) v=normal(rng);
        LayeredDynamicFFT inc(x);
        FFTWReal fftw((int)n); fftw.run(inc.input());
        double initial_err=max_err_half(inc,fftw);
        if(initial_err>1e-7) throw std::runtime_error("initial correctness failure err="+std::to_string(initial_err));
        std::vector<size_t> ks;
        for(size_t k=1;k<=std::min<size_t>(4096,n/2);k<<=1) ks.push_back(k);
        for(size_t k:ks){
            std::vector<double> inc_times, fftw_times; std::vector<uint64_t> dirty_counts; double maxe=0;
            inc_times.reserve(reps); fftw_times.reserve(reps);
            for(int r=0;r<reps;++r){
                std::vector<std::pair<size_t,double>> edits; edits.reserve(k);
                // Deterministic distinct indices spaced by an odd stride; random start.
                size_t start=(size_t)(rng()%n), stride=(size_t)((rng()%(n/2))*2+1);
                std::vector<char> used; // avoid O(N) clear: k small; use modular unique sequence if n power-of-two & stride odd.
                for(size_t j=0;j<k;++j){ size_t idx=(start+j*stride)&(n-1); edits.push_back({idx,delta(rng)}); }
                auto st=inc.add_deltas(edits); inc_times.push_back(st.ms); dirty_counts.push_back(st.complex_outputs);
                auto t=Clock::now(); fftw.run(inc.input()); fftw_times.push_back(ms_since(t));
                maxe=std::max(maxe,max_err_half(inc,fftw));
                if(maxe>2e-6) throw std::runtime_error("correctness failure n="+std::to_string(n)+" k="+std::to_string(k)+" err="+std::to_string(maxe));
            }
            auto median=[](std::vector<double> v){ std::sort(v.begin(),v.end()); return v[v.size()/2]; };
            auto medi_u=[](std::vector<uint64_t> v){ std::sort(v.begin(),v.end()); return v[v.size()/2]; };
            double ti=median(inc_times), tf=median(fftw_times);
            std::cout<<n<<","<<k<<","<<std::fixed<<std::setprecision(6)<<ti<<","<<tf<<","<<(tf/ti)<<","<<medi_u(dirty_counts)<<","<<predicted_nodes(n,k)<<","<<std::scientific<<maxe<<"\n";
        }
    }
}
