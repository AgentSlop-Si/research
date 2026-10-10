#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

// Fresh finite-field row elimination. Input is little-endian uint32 row-major.
// This implementation is independent of every supplied source executable.
uint64_t power(uint64_t a, uint64_t e, uint64_t p) {
  uint64_t b=1;
  while(e) { if(e&1) b=b*a%p; a=a*a%p; e>>=1; }
  return b;
}
int main(int argc,char**argv) {
  if(argc!=5) return 2;
  const int m=std::stoi(argv[2]), n=std::stoi(argv[3]);
  const uint64_t p=std::stoull(argv[4]);
  std::vector<uint32_t> a(size_t(m)*n);
  std::ifstream in(argv[1],std::ios::binary);
  in.read(reinterpret_cast<char*>(a.data()),a.size()*4);
  if(size_t(in.gcount())!=a.size()*4) throw std::runtime_error("size mismatch");
  int r=0, swaps=0; uint64_t det=1;
  std::vector<int> pivots;
  for(int c=0;c<n && r<m;++c) {
    int q=r; while(q<m && a[size_t(q)*n+c]==0) ++q;
    if(q==m) continue;
    if(q!=r) { for(int j=c;j<n;++j) std::swap(a[size_t(q)*n+j],a[size_t(r)*n+j]); ++swaps; }
    uint64_t pivot=a[size_t(r)*n+c]; det=det*pivot%p;
    uint64_t inverse=power(pivot,p-2,p);
    for(int i=r+1;i<m;++i) {
      uint64_t f=uint64_t(a[size_t(i)*n+c])*inverse%p;
      if(f) for(int j=c+1;j<n;++j) {
        uint64_t subtraction=f*a[size_t(r)*n+j]%p;
        a[size_t(i)*n+j]=(uint64_t(a[size_t(i)*n+j])+p-subtraction)%p;
      }
      a[size_t(i)*n+c]=0;
    }
    pivots.push_back(c); ++r;
  }
  if(swaps&1) det=(p-det)%p;
  std::cout << "{\"rank\":"<<r<<",\"determinant\":";
  if(m==n) std::cout<<(r==m?det:0); else std::cout<<"null";
  std::cout<<",\"pivots\":[";
  for(size_t i=0;i<pivots.size();++i) { if(i) std::cout<<","; std::cout<<pivots[i]; }
  std::cout<<"]}\n";
}
