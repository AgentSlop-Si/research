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
typedef double fftw_complex[2]; typedef struct fftw_plan_s *fftw_plan;
fftw_plan fftw_plan_dft_1d(int,fftw_complex*,fftw_complex*,int,unsigned);
void fftw_execute_dft(const fftw_plan,fftw_complex*,fftw_complex*);
void fftw_destroy_plan(fftw_plan);
}
static constexpr unsigned FFTW_ESTIMATE_=(1u<<6); static constexpr int FFTW_FORWARD_=-1;
using C=std::complex<double>; using Clock=std::chrono::steady_clock;
static double ms(Clock::time_point t){return std::chrono::duration<double,std::milli>(Clock::now()-t).count();}
struct Term{size_t index; C value;}; struct Result{std::vector<C> v; uint64_t bf=0;};
static Result rec(size_t n,const std::vector<Term>&s){
 if(s.empty())return{}; if(n==1)return{{s[0].value},0};
 std::vector<Term> e,o;e.reserve(s.size());o.reserve(s.size());for(auto&t:s)(t.index&1?o:e).push_back({t.index>>1,t.value});
 auto E=rec(n/2,e),O=rec(n/2,o); Result R;R.v.resize(n);R.bf=E.bf+O.bf+n/2;
 constexpr double P=3.14159265358979323846; C w(1),q=std::polar(1.0,-2*P/double(n));
 bool he=!E.v.empty(),ho=!O.v.empty(); for(size_t k=0;k<n/2;k++){C u=he?E.v[k]:C{}, z=ho?w*O.v[k]:C{};R.v[k]=u+z;R.v[k+n/2]=u-z;w*=q;}return R;
}
static Result sparse_fft(size_t n,const std::vector<Term>&s){return rec(n,s);}
class FFTW {int n_;std::vector<std::array<double,2>> in_,out_;fftw_plan p_{};public:
 explicit FFTW(int n):n_(n),in_(n),out_(n){p_=fftw_plan_dft_1d(n,reinterpret_cast<fftw_complex*>(in_.data()),reinterpret_cast<fftw_complex*>(out_.data()),FFTW_FORWARD_,FFTW_ESTIMATE_);if(!p_)throw std::runtime_error("plan");}
 ~FFTW(){fftw_destroy_plan(p_);} void init(const std::vector<double>&x){for(int i=0;i<n_;i++){in_[i][0]=x[i];in_[i][1]=0;}execute();}
 void apply(const std::vector<Term>&s){for(auto&t:s){in_[t.index][0]+=t.value.real();in_[t.index][1]+=t.value.imag();}}
 void execute(){fftw_execute_dft(p_,reinterpret_cast<fftw_complex*>(in_.data()),reinterpret_cast<fftw_complex*>(out_.data()));}
 const auto&out()const{return out_;}
};
static std::vector<C> copyout(const FFTW&f){std::vector<C>x(f.out().size());for(size_t i=0;i<x.size();i++)x[i]=C(f.out()[i][0],f.out()[i][1]);return x;}
static double err(const std::vector<C>&a,const FFTW&f){double e=0;for(size_t i=0;i<a.size();i++)e=std::max(e,std::abs(a[i]-C(f.out()[i][0],f.out()[i][1])));return e;}
static double med(std::vector<double>v){std::sort(v.begin(),v.end());return v[v.size()/2];}
int main(int ac,char**av){size_t n=ac>1?std::stoull(av[1]):262144;int reps=ac>2?std::stoi(av[2]):7;std::mt19937_64 g(987654321+n);std::normal_distribution<double>d(0,1);std::uniform_real_distribution<double>dv(-.2,.2);
 std::vector<double>x(n);for(auto&z:x)z=d(g);FFTW f((int)n);f.init(x);auto cached=copyout(f);
 std::cout<<"N,k,adaptive_ms,fftw_ms,speedup,butterflies,max_err\n";
 for(size_t k=1;k<=std::min<size_t>(2048,n/4);k<<=1){std::vector<double>ta,tb;uint64_t bf=0;double mx=0;
   for(int r=0;r<reps;r++){std::vector<Term>s;s.reserve(k);size_t start=g()%n,stride=((g()%(n/2))*2+1);for(size_t j=0;j<k;j++)s.push_back({(start+j*stride)&(n-1),C(dv(g),0)});
     auto t=Clock::now();auto delta=sparse_fft(n,s);for(size_t i=0;i<n;i++)cached[i]+=delta.v[i];ta.push_back(ms(t));bf=delta.bf;
     f.apply(s);t=Clock::now();f.execute();tb.push_back(ms(t));mx=std::max(mx,err(cached,f));if(mx>5e-6)throw std::runtime_error("bad "+std::to_string(mx));}
   double a=med(ta),b=med(tb);std::cout<<n<<","<<k<<","<<std::fixed<<std::setprecision(6)<<a<<","<<b<<","<<b/a<<","<<bf<<","<<std::scientific<<mx<<"\n";}
}
