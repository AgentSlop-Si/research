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
#include <utility>
#include <vector>

extern "C" {
typedef double fftw_complex[2];
typedef struct fftw_plan_s *fftw_plan;
fftw_plan fftw_plan_dft_1d(int n, fftw_complex *in, fftw_complex *out, int sign, unsigned flags);
void fftw_execute_dft(const fftw_plan p, fftw_complex *in, fftw_complex *out);
void fftw_destroy_plan(fftw_plan p);
}
static constexpr unsigned FFTW_ESTIMATE_ = (1u << 6);
static constexpr int FFTW_FORWARD_ = -1;
using C = std::complex<double>;
using Clock = std::chrono::steady_clock;
static double elapsed_ms(Clock::time_point t0){return std::chrono::duration<double,std::milli>(Clock::now()-t0).count();}
static bool is_pow2(size_t n){return n && !(n&(n-1));}

struct Term { size_t index; C value; };
struct SparseResult {
    std::vector<C> values;
    uint64_t butterflies = 0;
    uint64_t written = 0;
};

// Input-pruned radix-2 DIT FFT.  The support list contains only nonzero input
// coordinates in this node, indexed 0..n-1.  Empty subtrees are never visited.
static SparseResult sparse_fft_rec(size_t n, const std::vector<Term>& support){
    if(support.empty()) return {};
    if(n==1){
        SparseResult r; r.values.assign(1, support.front().value); r.written=1; return r;
    }
    std::vector<Term> ev, od;
    ev.reserve(support.size()); od.reserve(support.size());
    for(const auto &t:support){
        if(t.index&1) od.push_back({t.index>>1,t.value});
        else ev.push_back({t.index>>1,t.value});
    }
    SparseResult E=sparse_fft_rec(n/2,ev);
    SparseResult O=sparse_fft_rec(n/2,od);
    SparseResult R;
    R.values.resize(n);
    R.butterflies=E.butterflies+O.butterflies+n/2;
    R.written=E.written+O.written+n;
    constexpr double PI=3.141592653589793238462643383279502884;
    C w(1,0), step=std::polar(1.0,-2.0*PI/double(n));
    const bool haveE=!E.values.empty(), haveO=!O.values.empty();
    for(size_t k=0;k<n/2;++k){
        C u=haveE?E.values[k]:C(0,0);
        C v=haveO?(w*O.values[k]):C(0,0);
        R.values[k]=u+v;
        R.values[k+n/2]=u-v;
        w*=step;
    }
    return R;
}

static SparseResult sparse_fft(size_t n, std::vector<Term> support){
    if(!is_pow2(n)) throw std::invalid_argument("N power of two required");
    // Combine duplicate coordinates so k means actual support size.
    std::sort(support.begin(),support.end(),[](auto&a,auto&b){return a.index<b.index;});
    std::vector<Term> c; c.reserve(support.size());
    for(auto &t:support){
        if(t.index>=n) throw std::out_of_range("support index");
        if(!c.empty() && c.back().index==t.index) c.back().value+=t.value;
        else c.push_back(t);
    }
    c.erase(std::remove_if(c.begin(),c.end(),[](const Term&t){return t.value==C(0,0);}),c.end());
    return sparse_fft_rec(n,c);
}

class FFTWComplex {
    int n_;
    std::vector<std::array<double,2>> in_, out_;
    fftw_plan plan_{};
public:
    explicit FFTWComplex(int n):n_(n),in_(n),out_(n){
        plan_=fftw_plan_dft_1d(n_,reinterpret_cast<fftw_complex*>(in_.data()),reinterpret_cast<fftw_complex*>(out_.data()),FFTW_FORWARD_,FFTW_ESTIMATE_);
        if(!plan_) throw std::runtime_error("fftw plan failed");
    }
    ~FFTWComplex(){if(plan_)fftw_destroy_plan(plan_);}
    void run_sparse(size_t n,const std::vector<Term>& s){
        std::fill(in_.begin(),in_.end(),std::array<double,2>{0,0});
        for(auto&t:s){in_[t.index][0]+=t.value.real();in_[t.index][1]+=t.value.imag();}
        fftw_execute_dft(plan_,reinterpret_cast<fftw_complex*>(in_.data()),reinterpret_cast<fftw_complex*>(out_.data()));
    }
    const auto& out()const{return out_;}
};

static double maxerr(const std::vector<C>& a,const std::vector<std::array<double,2>>& b){
    double e=0; for(size_t i=0;i<a.size();++i)e=std::max(e,std::abs(a[i]-C(b[i][0],b[i][1]))); return e;
}
static double median(std::vector<double> v){std::sort(v.begin(),v.end());return v[v.size()/2];}

int main(int argc,char**argv){
    size_t n=argc>1?std::stoull(argv[1]):65536; int reps=argc>2?std::stoi(argv[2]):7;
    if(!is_pow2(n)) throw std::invalid_argument("N power of two");
    std::mt19937_64 rng(0x51A45EEDULL+n);
    std::uniform_real_distribution<double> dv(-1.0,1.0);
    FFTWComplex fftw((int)n);
    std::cout<<"N,k,pruned_ms,fftw_ms,speedup,butterflies,written,max_err\n";
    for(size_t k=1;k<=std::min<size_t>(4096,n/2);k<<=1){
        std::vector<Term> s; s.reserve(k);
        size_t start=rng()%n, stride=((rng()%(n/2))*2+1);
        for(size_t j=0;j<k;++j)s.push_back({(start+j*stride)&(n-1),C(dv(rng),0)});
        // Correctness warmup.
        auto got=sparse_fft(n,s); fftw.run_sparse(n,s); double err=maxerr(got.values,fftw.out());
        if(err>5e-6) throw std::runtime_error("correctness err "+std::to_string(err));
        std::vector<double> tp,tf; tp.reserve(reps);tf.reserve(reps); uint64_t butterflies=got.butterflies,written=got.written;
        for(int r=0;r<reps;++r){
            auto t0=Clock::now(); auto z=sparse_fft(n,s); tp.push_back(elapsed_ms(t0));
            volatile double sink=z.values[(r*997u)%n].real(); (void)sink;
            t0=Clock::now(); fftw.run_sparse(n,s); tf.push_back(elapsed_ms(t0));
        }
        double a=median(tp),b=median(tf);
        std::cout<<n<<","<<k<<","<<std::fixed<<std::setprecision(6)<<a<<","<<b<<","<<(b/a)<<","<<butterflies<<","<<written<<","<<std::scientific<<err<<"\n";
    }
}
