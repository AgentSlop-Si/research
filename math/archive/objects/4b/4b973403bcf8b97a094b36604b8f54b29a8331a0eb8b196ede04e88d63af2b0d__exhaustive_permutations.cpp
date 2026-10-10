// Exact Phase 38 resultant audit. Independent of Python's polynomial gcd.
// Usage: ./exhaustive_permutations instance.txt [max_checks=0 for exhaustive]
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
using u64 = uint64_t;
using poly3 = struct {u64 x0, x1, x2;};
static u64 P;
inline u64 add(u64 a,u64 b){u64 s=a+b;return s>=P?s-P:s;}
inline u64 sub(u64 a,u64 b){return a>=b?a-b:a+P-b;}
inline u64 mul(u64 a,u64 b){return (a*b)%P;}
inline u64 sq(u64 a){return (a*a)%P;}
inline u64 res(poly3 f,poly3 g){
    // Sylvester resultant of quadratic polynomials f=x0+x1*x+x2*x^2.
    u64 x=sub(mul(f.x2,g.x0),mul(f.x0,g.x2));
    u64 y=sub(mul(f.x2,g.x1),mul(f.x1,g.x2));
    u64 z=sub(mul(f.x1,g.x0),mul(f.x0,g.x1));
    return sub(sq(x),mul(y,z));
}
struct audit {
  size_t n; std::vector<u64> T,G,H;
  u64 v(const std::vector<u64>& m,size_t i,size_t j)const {return m[i*n+j];}
  poly3 quad(size_t r0,size_t r1,size_t c0,size_t cj,size_t j)const{
    // target anchor rows 0,1; columns 0,j (j in {1,2})
    // T[1,j]*T[0,0]*B[r1,c0]*B[r0,cj]
    // minus T[1,0]*T[0,j]*B[r1,cj]*B[r0,c0]
    u64 x0=v(G,r1,c0), x1=v(H,r1,c0);
    u64 y0=v(G,r0,cj), y1=v(H,r0,cj);
    u64 z0=v(G,r1,cj), z1=v(H,r1,cj);
    u64 w0=v(G,r0,c0), w1=v(H,r0,c0);
    u64 L=mul(v(T,1,j),v(T,0,0));
    u64 R=mul(v(T,1,0),v(T,0,j));
    return {sub(mul(L,mul(x0,y0)),mul(R,mul(z0,w0))),
            sub(mul(L,add(mul(x0,y1),mul(x1,y0))),mul(R,add(mul(z0,w1),mul(z1,w0)))),
            sub(mul(L,mul(x1,y1)),mul(R,mul(z1,w1)))};
  }
};
int main(int argc,char**argv){
 if(argc<2){std::cerr<<"Usage: "<<argv[0]<<" instance.txt [max_checks (0=all)]\n";return 2;}
 std::ifstream in(argv[1]); if(!in){std::cerr<<"Cannot open\n";return 2;}
 audit a;in>>a.n>>P;
 for(auto* m:{&a.T,&a.G,&a.H}){
  m->resize(a.n*a.n);
  for(auto&v:*m){in>>v; if(!in || v>=P) {std::cerr<<"Invalid instance\n";return 3;}}
 }
 const auto n=a.n;
 u64 limit=argc>=3?std::strtoull(argv[2],nullptr,10):0;
 u64 random_count=argc>=4?std::strtoull(argv[3],nullptr,10):0;
 u64 checked=0,nonzero=0,zero=0,hash=1469598103934665603ULL;
 double elapsed=0;
 auto st=std::chrono::steady_clock::now();
 if (random_count){
   u64 rng=0x9e3779b97f4a7c15ULL + 71*n + P;
   auto next_rand=[&](){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;};
   for(u64 z=0;z<random_count;z++){
      size_t r0=next_rand()%n,r1=next_rand()%n;
      while(r1==r0)r1=next_rand()%n;
      size_t c0=next_rand()%n,c1=next_rand()%n,c2=next_rand()%n;
      while(c1==c0)c1=next_rand()%n;
      while(c2==c0||c2==c1)c2=next_rand()%n;
      auto det=res(a.quad(r0,r1,c0,c1,1),a.quad(r0,r1,c0,c2,2));
      ++checked;if(det)++nonzero;
      else {++zero;if(zero<=3)std::cerr<<"ZERO: "<<r0<<","<<r1<<" / "<<c0<<","<<c1<<","<<c2<<"\n";}
      hash^=det;hash*=1099511628211ULL;
   }
   goto done;
 }
 for(size_t r0=0;r0<n;r0++)for(size_t r1=0;r1<n;r1++)if(r0!=r1){
   for(size_t c0=0;c0<n;c0++){
    std::vector<poly3> f(n),g(n);
    for(size_t c=0;c<n;c++)if(c!=c0){
      f[c]=a.quad(r0,r1,c0,c,1);
      g[c]=a.quad(r0,r1,c0,c,2);
    }
    for(size_t c1=0;c1<n;c1++)if(c1!=c0){
     for(size_t c2=0;c2<n;c2++)if(c2!=c0 && c2!=c1){
      u64 det=res(f[c1],g[c2]);
      ++checked;
      if(det)++nonzero;
      else {++zero;if(zero<=3)std::cerr<<"ZERO: "<<r0<<","<<r1<<" / "<<c0<<","<<c1<<","<<c2<<"\n";}
      hash^=det;hash*=1099511628211ULL;
      if(limit && checked>=limit) goto done;
     }
    }
   }
 }
 done:
 elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count();
 std::cout<<"{\"N\":"<<n<<",\"prime\":"<<P<<",\"checked\":"<<checked
   <<",\"nonzero_resultants\":"<<nonzero<<",\"zero_resultants\":"<<zero
   <<",\"rolling_hash\":\""<<std::hex<<hash<<std::dec<<"\",\"elapsed_seconds\":"<<elapsed<<"}"<<std::endl;
 return zero?1:0;
}
