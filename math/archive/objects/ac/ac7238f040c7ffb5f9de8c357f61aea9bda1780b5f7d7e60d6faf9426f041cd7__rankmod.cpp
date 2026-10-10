#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cstdint>
#include <chrono>
#include <fstream>
#include <algorithm>
#include <iostream>
using namespace std;
static inline int inverse(int a,int p){int64_t x=1,b=a,e=p-2;while(e){if(e&1)x=x*b%p;b=b*b%p;e>>=1;}return (int)x;}
int main(int argc,char**argv){
 if(argc<5){cerr<<"rankmod <raw_int32_bin> rows cols prime\n";return 1;}
 const int rows=atoi(argv[2]),cols=atoi(argv[3]),p=atoi(argv[4]);
 ifstream f(argv[1],ios::binary);if(!f.good()){cerr<<"file missing";return 1;}
 vector<int32_t>a((size_t)rows*cols);f.read((char*)a.data(),a.size()*sizeof(int32_t));
 if(f.gcount()!=long(a.size()*sizeof(int32_t))){cerr<<"short matrix";return 1;}
 int rank=0,det=1,sgn=1;vector<int>pivs;
 const auto start=chrono::steady_clock::now();
 for(int c=0;c<cols && rank<rows;c++){
  int pivot=rank;while(pivot<rows && a[(size_t)pivot*cols+c]%p==0)pivot++;
  if(pivot==rows)continue;
  if(pivot!=rank){for(int j=0;j<cols;j++)swap(a[(size_t)rank*cols+j],a[(size_t)pivot*cols+j]);sgn=-sgn;}
  int v=a[(size_t)rank*cols+c]%p; if(v<0)v+=p;
  det=(int)((int64_t)det*v%p);
  const int inv=inverse(v,p);
  for(int j=c;j<cols;j++)a[(size_t)rank*cols+j]=(int)((int64_t)a[(size_t)rank*cols+j]*inv%p);
  for(int i=rank+1;i<rows;i++){
    int alpha=a[(size_t)i*cols+c];if(!alpha)continue;
    int32_t*row=&a[(size_t)i*cols]; const int32_t*pp=&a[(size_t)rank*cols];
    for(int j=c+1;j<cols;j++){
      int64_t z=(int64_t)row[j]-(int64_t)alpha*pp[j];
      z%=p;if(z<0)z+=p;row[j]=(int32_t)z;
    }
    row[c]=0;
  }
  pivs.push_back(c); rank++;
 }
 const auto secs=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<"rank="<<rank<<" full_rows="<<rows<<" det="<<(rank==rows?(det*sgn%p+p)%p:0)<<" secs="<<secs<<"\n";
 cout<<"pivots=";for(size_t j=0;j<pivs.size();j++){if(j)cout<<",";cout<<pivs[j];}cout<<"\n";
}
