// Reviewer authored: exhaustive ordered projective witness gate, no source code copied.
#include <iostream>
#include <vector>
#include <array>
#include <cstdint>
using u64=uint64_t;using poly=std::array<u64,3>;
u64 p;
u64 mul(u64 a,u64 b){return a*b%p;}
u64 sub(u64 a,u64 b){return (a+p-b)%p;}
poly product(u64 a,u64 b,u64 c,u64 d){return {mul(a,c),(mul(a,d)+mul(b,c))%p,mul(b,d)};}
u64 resultant(const poly&a,const poly&b){u64 x=sub(mul(a[2],b[0]),mul(a[0],b[2]));u64 y=sub(mul(a[2],b[1]),mul(a[1],b[2]));u64 z=sub(mul(a[1],b[0]),mul(a[0],b[1]));return sub(mul(x,x),mul(y,z));}
int main(){int n;std::cin>>n>>p;std::vector<std::vector<u64>> T(n,std::vector<u64>(n)),A=T,B=T;for(auto*M:{&T,&A,&B})for(auto&r:*M)for(auto&v:r)std::cin>>v;
 u64 checked=0,zeros=0;std::vector<std::array<int,5>> exceptions;
 for(int r=0;r<n;r++)for(int s=0;s<n;s++)if(r!=s)for(int c=0;c<n;c++){
  std::vector<poly> f(n),g(n);
  for(int d=0;d<n;d++)if(d!=c){auto aa=product(A[s][c],B[s][c],A[r][d],B[r][d]);auto bb=product(A[s][d],B[s][d],A[r][c],B[r][c]);
   u64 z1=mul(T[1][1],T[0][0]),w1=mul(T[1][0],T[0][1]),z2=mul(T[1][2],T[0][0]),w2=mul(T[1][0],T[0][2]);
   for(int k=0;k<3;k++){f[d][k]=sub(mul(z1,aa[k]),mul(w1,bb[k]));g[d][k]=sub(mul(z2,aa[k]),mul(w2,bb[k]));}}
  for(int d=0;d<n;d++)if(d!=c)for(int e=0;e<n;e++)if(e!=c&&e!=d){checked++;if(!resultant(f[d],g[e])){zeros++;exceptions.push_back({r,s,c,d,e});}}
 }
 std::cout<<"{\"N\":"<<n<<",\"prime\":"<<p<<",\"checked\":"<<checked<<",\"zeros\":"<<zeros<<",\"exceptions\":[";
 for(size_t k=0;k<exceptions.size();k++){if(k)std::cout<<",";auto a=exceptions[k];std::cout<<"["<<a[0]<<","<<a[1]<<","<<a[2]<<","<<a[3]<<","<<a[4]<<"]";}std::cout<<"]}\n";
}
