#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cmath>
#include <complex>
#include <cstdint>
#include <cstring>
#include <deque>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <bit>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

extern "C" {
typedef double fftw_complex[2];
typedef struct fftw_plan_s *fftw_plan;
fftw_plan fftw_plan_dft_r2c_1d(int n, double *in, fftw_complex *out, unsigned flags);
void fftw_execute_dft_r2c(const fftw_plan p, double *in, fftw_complex *out);
void fftw_destroy_plan(fftw_plan p);
}
static constexpr unsigned FFTW_ESTIMATE_ = (1u << 6);

using Clock = std::chrono::steady_clock;
using C = std::complex<double>;
using Vec = std::vector<double>;
using Spec = std::vector<C>;

static double ms_since(Clock::time_point t0) {
    return std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
}

struct Timings {
    double fingerprint_ms=0, lookup_ms=0, relation_ms=0, fft_ms=0, reconstruct_ms=0, cache_ms=0;
    double total() const { return fingerprint_ms+lookup_ms+relation_ms+fft_ms+reconstruct_ms+cache_ms; }
    void add(const Timings& o){ fingerprint_ms+=o.fingerprint_ms; lookup_ms+=o.lookup_ms; relation_ms+=o.relation_ms; fft_ms+=o.fft_ms; reconstruct_ms+=o.reconstruct_ms; cache_ms+=o.cache_ms; }
};

class FFTWBackend {
    struct PlanEntry {
        int n{};
        Vec scratch_in;
        std::vector<std::array<double,2>> scratch_out;
        fftw_plan plan{};
        explicit PlanEntry(int n_) : n(n_), scratch_in(n_), scratch_out(n_/2+1) {
            plan = fftw_plan_dft_r2c_1d(n, scratch_in.data(), reinterpret_cast<fftw_complex*>(scratch_out.data()), FFTW_ESTIMATE_);
            if(!plan) throw std::runtime_error("FFTW plan creation failed");
        }
        ~PlanEntry(){ if(plan) fftw_destroy_plan(plan); }
        PlanEntry(const PlanEntry&)=delete; PlanEntry& operator=(const PlanEntry&)=delete;
    };
    std::unordered_map<int, PlanEntry*> plans_;
public:
    ~FFTWBackend(){ for(auto &kv:plans_) delete kv.second; }
    Spec rfft(const Vec& x) {
        int n=(int)x.size();
        auto it=plans_.find(n);
        if(it==plans_.end()) it=plans_.emplace(n,new PlanEntry(n)).first;
        Spec out(n/2+1);
        fftw_execute_dft_r2c(it->second->plan, const_cast<double*>(x.data()), reinterpret_cast<fftw_complex*>(out.data()));
        return out;
    }
};

static inline uint64_t mix64(uint64_t z){
    z ^= z >> 30; z *= 0xbf58476d1ce4e5b9ULL;
    z ^= z >> 27; z *= 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static uint64_t hash_bytes(const Vec& x) {
    // Word-at-a-time non-cryptographic fingerprint. Exact hits are still
    // verified with memcmp, so collisions affect speed only, never correctness.
    const uint64_t* p=reinterpret_cast<const uint64_t*>(x.data());
    uint64_t h=0x9e3779b97f4a7c15ULL ^ mix64((uint64_t)x.size());
    for(size_t i=0;i<x.size();i+=4){
        uint64_t a=p[i];
        uint64_t b=(i+1<x.size()?p[i+1]:0x243f6a8885a308d3ULL);
        uint64_t c=(i+2<x.size()?p[i+2]:0x13198a2e03707344ULL);
        uint64_t d=(i+3<x.size()?p[i+3]:0xa4093822299f31d0ULL);
        h ^= mix64(a + 0x9e3779b97f4a7c15ULL);
        h ^= std::rotl(mix64(b),17); h ^= std::rotl(mix64(c),33); h ^= std::rotl(mix64(d),49);
        h = h*0x9ddfea08eb382d69ULL + 0x632be59bd9b4e019ULL;
    }
    return mix64(h);
}

static bool bit_equal(const Vec& a,const Vec& b){
    return a.size()==b.size() && std::memcmp(a.data(),b.data(),a.size()*sizeof(double))==0;
}

static std::pair<double,double> signature(const Vec& a){
    long double s=0,q=0;
    for(double v:a){s+=v; q+=(long double)v*v;}
    return {(double)s,(double)q};
}
static bool similar_sig(std::pair<double,double>a,std::pair<double,double>b){
    auto close=[](double x,double y){return std::abs(x-y)<=1e-7+1e-10*std::max(std::abs(x),std::abs(y));};
    return close(a.first,b.first)&&close(a.second,b.second);
}

static std::vector<uint64_t> as_bits(const Vec& x){
    std::vector<uint64_t> b(x.size()); std::memcpy(b.data(),x.data(),x.size()*8); return b;
}

static int cyclic_right_shift(const Vec& base,const Vec& target){
    if(base.size()!=target.size()) return -1;
    const int n=(int)base.size(); if(n==0) return -1;
    auto a=as_bits(base), p=as_bits(target);
    std::vector<int> pi(n);
    for(int i=1,j=0;i<n;i++){ while(j&&p[i]!=p[j]) j=pi[j-1]; if(p[i]==p[j]) j++; pi[i]=j; }
    int j=0;
    for(int i=0;i<2*n-1;i++){
        uint64_t v=a[i%n];
        while(j&&v!=p[j]) j=pi[j-1];
        if(v==p[j]) j++;
        if(j==n){ int start=i-n+1; if(start<n) return (n-start)%n; j=pi[j-1]; }
    }
    return -1;
}

static Spec shifted_spectrum(const Spec& base,int n,int shift){
    Spec out(base.size());
    C omega=std::exp(C(0,-2.0*M_PI*shift/n)), phase(1,0);
    for(size_t k=0;k<out.size();k++){ out[k]=base[k]*phase; phase*=omega; }
    return out;
}
static Spec sparse_spectrum(const Spec& base,int n,const std::vector<std::pair<int,double>>& edits){
    Spec out=base;
    for(auto [pos,d]:edits){
        if(pos==0){ for(auto &z:out) z+=d; continue; }
        C omega=std::exp(C(0,-2.0*M_PI*pos/n)), phase(1,0);
        for(auto &z:out){ z += d*phase; phase*=omega; }
    }
    return out;
}

struct Entry { uint64_t h{}; Vec input; Spec spectrum; std::pair<double,double> sig; };

enum class Mode { HashOnly, Exact, Structural };

class AdaptiveFFT {
    FFTWBackend& fft_;
    std::deque<Entry> cache_;
    size_t max_refs_=3;
    int max_sparse_=1;
public:
    Timings times;
    std::unordered_map<std::string,size_t> stats;
    explicit AdaptiveFFT(FFTWBackend& f,size_t refs=3,int sparse=1):fft_(f),max_refs_(refs),max_sparse_(sparse){}
    void clear(){cache_.clear(); times={}; stats.clear();}
    Spec run(const Vec& x,Mode mode){
        auto all0=Clock::now(); (void)all0;
        uint64_t h=0;
        if(mode!=Mode::HashOnly || true){ auto t=Clock::now(); h=hash_bytes(x); times.fingerprint_ms+=ms_since(t); }
        if(mode==Mode::HashOnly){
            auto t=Clock::now(); auto y=fft_.rfft(x); times.fft_ms+=ms_since(t); stats["fft"]++; return y;
        }
        {
            auto t=Clock::now();
            for(auto it=cache_.rbegin();it!=cache_.rend();++it){
                if(it->h==h && bit_equal(it->input,x)){
                    Spec y=it->spectrum; times.lookup_ms+=ms_since(t); stats["exact"]++; return y;
                }
            }
            times.lookup_ms+=ms_since(t);
        }
        if(mode==Mode::Structural){
            auto t=Clock::now();
            auto xs=signature(x);
            for(auto it=cache_.rbegin();it!=cache_.rend();++it){
                if(it->input.size()!=x.size()) continue;
                if(max_sparse_>0){
                    std::vector<std::pair<int,double>> edits; edits.reserve(max_sparse_+1);
                    // sampled reject matching Python engine's spirit
                    bool promising=true; int sampled=0;
                    for(int q=0;q<16 && q<(int)x.size();q++){
                        size_t idx=(size_t)q*(x.size()-1)/std::max(1,15);
                        if(x[idx]!=it->input[idx] && ++sampled>max_sparse_){promising=false;break;}
                    }
                    if(promising){
                        for(size_t i=0;i<x.size();i++) if(x[i]!=it->input[i]){
                            edits.push_back({(int)i,x[i]-it->input[i]});
                            if((int)edits.size()>max_sparse_) break;
                        }
                        if(!edits.empty() && (int)edits.size()<=max_sparse_){
                            times.relation_ms+=ms_since(t); auto r=Clock::now(); auto y=sparse_spectrum(it->spectrum,(int)x.size(),edits); times.reconstruct_ms+=ms_since(r); stats["sparse"]++; return y;
                        }
                    }
                }
                if(similar_sig(xs,it->sig)){
                    int shift=cyclic_right_shift(it->input,x);
                    if(shift>=0){ times.relation_ms+=ms_since(t); auto r=Clock::now(); auto y=shifted_spectrum(it->spectrum,(int)x.size(),shift); times.reconstruct_ms+=ms_since(r); stats["shift"]++; return y; }
                }
            }
            times.relation_ms+=ms_since(t);
        }
        auto tf=Clock::now(); auto y=fft_.rfft(x); times.fft_ms+=ms_since(tf); stats["fft"]++;
        auto tc=Clock::now();
        Entry e{h,x,y,signature(x)}; cache_.push_back(std::move(e)); while(cache_.size()>max_refs_) cache_.pop_front();
        times.cache_ms+=ms_since(tc);
        return y;
    }
};

struct Rank2Result { bool ok=false; int rank=0; Vec b0,b1; std::vector<std::array<double,2>> c; };
static bool close_val(double a,double b,double tol=2e-12){return std::abs(a-b)<=tol*(1+std::abs(b));}
static Rank2Result detect_rank2(const std::vector<Vec>& rows,double tol=2e-12){
    Rank2Result r; if(rows.empty()) return r; size_t n=rows[0].size();
    int p0=-1,p1=-1;
    for(const auto& row:rows){
        if(row.size()!=n) return {};
        if(r.rank==0){
            auto it=std::max_element(row.begin(),row.end(),[](double a,double b){return std::abs(a)<std::abs(b);});
            if(it==row.end() || std::abs(*it)<=tol){ r.c.push_back({0,0}); continue; }
            r.b0=row; p0=(int)std::distance(row.begin(),it); r.rank=1; r.c.push_back({1,0}); continue;
        }
        if(r.rank==1){
            double alpha=row[p0]/r.b0[p0]; bool good=true;
            for(size_t j=0;j<n;j++) if(!close_val(alpha*r.b0[j],row[j],tol)){good=false;break;}
            if(good){r.c.push_back({alpha,0});continue;}
            r.b1=row; double best=0; for(size_t j=0;j<n;j++){double d=r.b0[p0]*r.b1[j]-r.b0[j]*r.b1[p0]; if(std::abs(d)>std::abs(best)){best=d;p1=(int)j;}}
            double scale=*std::max_element(r.b0.begin(),r.b0.end(),[](double a,double b){return std::abs(a)<std::abs(b);}) * *std::max_element(r.b1.begin(),r.b1.end(),[](double a,double b){return std::abs(a)<std::abs(b);});
            (void)scale; if(std::abs(best)<=1e-14) return {}; r.rank=2; r.c.push_back({0,1}); continue;
        }
        double det=r.b0[p0]*r.b1[p1]-r.b0[p1]*r.b1[p0];
        double a=(row[p0]*r.b1[p1]-row[p1]*r.b1[p0])/det;
        double b=(r.b0[p0]*row[p1]-r.b0[p1]*row[p0])/det;
        bool good=true; for(size_t j=0;j<n;j++) if(!close_val(a*r.b0[j]+b*r.b1[j],row[j],tol)){good=false;break;}
        if(!good) return {}; r.c.push_back({a,b});
    }
    r.ok=r.rank>0; return r;
}

static std::vector<Spec> reconstruct_rank2(FFTWBackend& fft,const Rank2Result& r,Timings& tm){
    auto tf=Clock::now(); Spec f0=fft.rfft(r.b0), f1; if(r.rank==2) f1=fft.rfft(r.b1); tm.fft_ms+=ms_since(tf);
    auto tr=Clock::now(); std::vector<Spec> out(r.c.size(),Spec(f0.size()));
    for(size_t i=0;i<out.size();i++) for(size_t k=0;k<f0.size();k++) out[i][k]=r.c[i][0]*f0[k]+(r.rank==2?r.c[i][1]*f1[k]:C(0));
    tm.reconstruct_ms+=ms_since(tr); return out;
}

static double max_err(const Spec&a,const Spec&b){double e=0; for(size_t i=0;i<a.size();i++) e=std::max(e,std::abs(a[i]-b[i])); return e;}
static Vec random_vec(size_t n,std::mt19937_64&r){std::normal_distribution<double>d; Vec x(n); for(auto &v:x)v=d(r); return x;}

struct RowResult { std::string impl,case_name; size_t n,count; double ms,speedup; Timings tm; std::unordered_map<std::string,size_t> stats; };

static double median(std::vector<double> v){std::sort(v.begin(),v.end()); return v[v.size()/2];}

template<class F> static double bench(F&& f,int reps=7){ std::vector<double> t; t.reserve(reps); f(); for(int i=0;i<reps;i++){auto s=Clock::now(); f(); t.push_back(ms_since(s));} return median(t); }

int main(int argc,char**argv){
    std::cout<<std::fixed<<std::setprecision(6);
    FFTWBackend fft; std::mt19937_64 rng(10082026);

    // correctness: exact, shift, sparse, rank-2
    for(int n:{64,1024,4096}){
        Vec x=random_vec(n,rng); auto fx=fft.rfft(x); AdaptiveFFT eng(fft); auto a=eng.run(x,Mode::Structural); auto b=eng.run(x,Mode::Structural); if(max_err(fx,b)>1e-9) return 2;
        Vec sh=x; std::rotate(sh.begin(),sh.end()-7,sh.end()); auto fs=fft.rfft(sh); auto got=eng.run(sh,Mode::Structural); if(max_err(fs,got)>2e-7) {std::cerr<<"shift err\n";return 3;}
        Vec sp=x; sp[n/3]+=0.125; eng.clear(); eng.run(x,Mode::Structural); auto gs=eng.run(sp,Mode::Structural); auto esp=fft.rfft(sp); if(max_err(gs,esp)>2e-7){std::cerr<<"sparse err\n";return 4;}
    }
    {
        size_t n=4096,m=32; Vec b0=random_vec(n,rng),b1=random_vec(n,rng); std::uniform_int_distribution<int>di(-3,3); std::vector<Vec> rows(m,Vec(n));
        for(auto&row:rows){double a=di(rng),b=di(rng);for(size_t j=0;j<n;j++)row[j]=a*b0[j]+b*b1[j];}
        auto r=detect_rank2(rows); if(!r.ok||r.rank!=2) return 5; Timings tm; auto out=reconstruct_rank2(fft,r,tm); if(max_err(out[7],fft.rfft(rows[7]))>2e-7)return 6;
    }
    std::cout<<"TESTS PASSED\n";
    std::cout<<"impl,case,n,count,total_ms,speedup_vs_baseline,fingerprint_ms,lookup_ms,relation_ms,fft_ms,reconstruct_ms,cache_ms,exact,shift,sparse,fft\n";

    for(size_t n:{4096ul,16384ul,65536ul,262144ul}){
        const size_t count=12; Vec x=random_vec(n,rng);
        std::vector<Vec> exact(count,x), shifts, sparse, unrelated; shifts.reserve(count); sparse.reserve(count); unrelated.reserve(count);
        for(size_t i=0;i<count;i++){Vec s=x; size_t sh=(i*97+13)%n; std::rotate(s.begin(),s.end()-sh,s.end()); shifts.push_back(std::move(s)); Vec p=x;p[(i*7919+17)%n]+=0.125*(i+1);sparse.push_back(std::move(p));unrelated.push_back(random_vec(n,rng));}
        std::vector<std::pair<std::string,std::vector<Vec>*>> cases={{"exact_repeat",&exact},{"shift_stream",&shifts},{"sparse_stream",&sparse},{"unrelated",&unrelated}};
        for(auto &[cn,inputs]:cases){
            double base=bench([&]{for(auto &v:*inputs){volatile auto z=fft.rfft(v);(void)z;}},5);
            for(auto [name,mode]:std::vector<std::pair<std::string,Mode>>{{"hash_only",Mode::HashOnly},{"exact_cache",Mode::Exact},{"structural",Mode::Structural}}){
                std::vector<double> vals; Timings medtm; std::unordered_map<std::string,size_t> st;
                for(int rep=0;rep<5;rep++){
                    AdaptiveFFT e(fft); if(cn!="exact_repeat" && mode==Mode::Structural) e.run(x,mode); // seed structural reference
                    auto s=Clock::now(); for(auto &v:*inputs){auto z=e.run(v,mode); volatile double q=z[0].real();(void)q;} double elapsed=ms_since(s);
                    vals.push_back(elapsed); if(rep==2){medtm=e.times;st=e.stats;}
                }
                double t=median(vals);
                std::cout<<name<<','<<cn<<','<<n<<','<<count<<','<<t<<','<<(base/t)<<','<<medtm.fingerprint_ms<<','<<medtm.lookup_ms<<','<<medtm.relation_ms<<','<<medtm.fft_ms<<','<<medtm.reconstruct_ms<<','<<medtm.cache_ms<<','<<st["exact"]<<','<<st["shift"]<<','<<st["sparse"]<<','<<st["fft"]<<"\n";
            }
        }
    }

    // Low-rank family: baseline vs detection+2 FFTs vs known basis (2 FFTs + reconstruction)
    for(size_t n:{4096ul,16384ul,65536ul}){
        size_t m=128; Vec b0=random_vec(n,rng),b1=random_vec(n,rng); std::uniform_int_distribution<int>di(-3,3); std::vector<Vec> rows(m,Vec(n)); std::vector<std::array<double,2>> coeff(m);
        for(size_t i=0;i<m;i++){coeff[i]={(double)di(rng),(double)di(rng)};for(size_t j=0;j<n;j++)rows[i][j]=coeff[i][0]*b0[j]+coeff[i][1]*b1[j];}
        double base=bench([&]{for(auto &v:rows){volatile auto z=fft.rfft(v);(void)z;}},3);
        Timings dettm; double det=bench([&]{dettm={};auto td=Clock::now();auto r=detect_rank2(rows);dettm.relation_ms+=ms_since(td);auto o=reconstruct_rank2(fft,r,dettm);volatile double q=o[0][0].real();(void)q;},3);
        Timings ktm; double known=bench([&]{ktm={};Rank2Result r;r.ok=true;r.rank=2;r.b0=b0;r.b1=b1;r.c=coeff;auto o=reconstruct_rank2(fft,r,ktm);volatile double q=o[0][0].real();(void)q;},3);
        std::cout<<"rank2_detect,low_rank_family,"<<n<<','<<m<<','<<det<<','<<(base/det)<<",0,0,"<<dettm.relation_ms<<','<<dettm.fft_ms<<','<<dettm.reconstruct_ms<<",0,0,0,0,2\n";
        std::cout<<"known_basis,low_rank_family,"<<n<<','<<m<<','<<known<<','<<(base/known)<<",0,0,0,"<<ktm.fft_ms<<','<<ktm.reconstruct_ms<<",0,0,0,0,2\n";
    }
    return 0;
}
