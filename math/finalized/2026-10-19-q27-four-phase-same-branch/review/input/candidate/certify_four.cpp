// Fresh four-variable all-original-window coefficient certificate, 19 Oct 2026.
#include <array>
#include <vector>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <algorithm>
#include <cstdint>
#include <string>
#include "chart_generated.h"
using namespace std;
using F=uint64_t;
const F p=1000000009ULL;
F add(F a,F b){F c=a+b;return c>=p?c-p:c;}
F sub(F a,F b){return a>=b?a-b:a+p-b;}
F mul(F a,F b){return a*b%p;}
F pw(F a,F n){F r=1;for(;n;n>>=1,a=mul(a,a))if(n&1)r=mul(r,a);return r;}
F inv(F a){if(!a)throw runtime_error("zero denominator");return pw(a,p-2);}
using Poly16=array<F,16>;
using Mat=array<Poly16,64>;
using Poly81=array<F,81>;
using Poly625=array<F,625>;
int map16[16][16],map81[81][81],index4to5[256];
vector<int> support;
int variation(array<int,4>d){int r=0;for(int k=0;k<4;k++)r+=abs(d[k]-d[(k+1)%4]);return r;}
array<int,4> digits(int n,int b){array<int,4>d{};for(int k=3;k>=0;k--){d[k]=n%b;n/=b;}return d;}
int idx(array<int,4>d,int b){int n=0;for(int v:d)n=n*b+v;return n;}
int mask(array<int,4>d){int n=0;for(int k=0;k<4;k++)n|=d[k]<<k;return n;}
array<int,4> maskdigits(int n){array<int,4>d{};for(int k=0;k<4;k++)d[k]=(n>>k)&1;return d;}
void init(){
 for(int a=0;a<16;a++)for(int b=0;b<16;b++){auto x=maskdigits(a),y=maskdigits(b);for(int k=0;k<4;k++)x[k]+=y[k];map16[a][b]=idx(x,3);}
 for(int a=0;a<81;a++)for(int b=0;b<81;b++){auto x=digits(a,3),y=digits(b,3);for(int k=0;k<4;k++)x[k]+=y[k];map81[a][b]=idx(x,5);}
 for(int a=0;a<256;a++){auto d=digits(a,4);index4to5[a]=idx(d,5);if(*max_element(d.begin(),d.end())-*min_element(d.begin(),d.end())<=2 && variation(d)<=4)support.push_back(a);}
 if(support.size()!=126)throw runtime_error("wrong support count");
}
struct Build {Mat N;F active_h;};
Build build(int active_stage,int branch,array<int,4> edges,F ii){
 F gains[2][24],h[2][3];
 for(int s=0;s<2;s++){
  for(int e=0;e<24;e++)if(e<7)gains[s][e]=1;else{F a=GAUSS[s][e-7][0],b=GAUSS[s][e-7][1];F ib=mul(ii,b);gains[s][e]=mul(add(a,ib),inv(sub(a,ib)));}
  for(int b=0;b<3;b++){h[s][b]=1;for(int j=0;j<8;j++)h[s][b]=mul(h[s][b],gains[s][8*b+j]);if(!h[s][b]||h[s][b]==1)throw runtime_error("bad frozen holonomy/guard");}
 }
 Mat A[2]{};
 for(int s=0;s<2;s++)for(int b=0;b<3;b++){
  Mat B{};
  for(int start=0;start<8;start++){
   int from=CYC[s][b][start],bits=0;F weight=1;B[8*from+from][0]=add(B[8*from+from][0],1);
   for(int len=1;len<8;len++){
    int j=(start+len)%8,e=8*b+j,to=CYC[s][b][j];weight=mul(weight,gains[s][e]);
    if(s==active_stage)for(int k=0;k<4;k++)if(e==edges[k]){if(bits&(1<<k))throw runtime_error("repeated edge");bits|=1<<k;}
    B[8*to+from][bits]=add(B[8*to+from][bits],weight);
   }
  }
  Poly16 factor{};factor[0]=1;
  for(int c=0;c<3;c++)if(c!=b){
   Poly16 next{};
   if(s==active_stage && c==branch){for(int k=0;k<16;k++)if(factor[k]){if(k)throw runtime_error("overlap in guards");next[k]=add(next[k],factor[k]);next[15]=sub(next[15],mul(factor[k],h[s][c]));}}
   else for(int k=0;k<16;k++)next[k]=mul(factor[k],sub(1,h[s][c]));
   factor=next;
  }
  for(int rc=0;rc<64;rc++)for(int u=0;u<16;u++)if(B[rc][u])for(int v=0;v<16;v++)if(factor[v]){
   if(u&v)throw runtime_error("variable overlap");A[s][rc][u|v]=add(A[s][rc][u|v],mul(B[rc][u],factor[v]));
  }
 }
 Mat N{};
 for(int r=0;r<8;r++)for(int c=0;c<8;c++)for(int j=0;j<8;j++)for(int u=0;u<16;u++)if(A[1][8*r+j][u])for(int v=0;v<16;v++)if(A[0][8*j+c][v]){
  if(u&v)throw runtime_error("stage variable overlap");N[8*r+c][u|v]=add(N[8*r+c][u|v],mul(A[1][8*r+j][u],A[0][8*j+c][v]));
 }
 return {N,h[active_stage][branch]};
}
array<Poly81,64> modulus_product(const Mat&N,const Mat&conjN){
 array<Poly81,64> H{};
 for(int rc=0;rc<64;rc++)for(int a=0;a<16;a++)for(int b=0;b<16;b++)H[rc][map16[a][b]]=add(H[rc][map16[a][b]],mul(N[rc][a],conjN[rc][15^b]));
 for(int rc=0;rc<64;rc++)for(int e=0;e<81;e++)if(H[rc][e]){auto d=digits(e,3);if(*max_element(d.begin(),d.end())-*min_element(d.begin(),d.end())>1 || variation(d)>2)throw runtime_error("H27 support failure");}
 return H;
}
array<F,256> quotient(const array<Poly81,64>&H,int a,int r,int b,int c,F h){
 Poly625 P{};
 const auto&A=H[8*r+c];const auto&B=H[8*a+b];const auto&C=H[8*r+b];const auto&D=H[8*a+c];
 for(int i=0;i<81;i++)for(int j=0;j<81;j++)P[map81[i][j]]=add(P[map81[i][j]],sub(mul(A[i],B[j]),mul(C[i],D[j])));
 // Exact ascending recurrence Q_e=P_e+h Q_(e-1), with full multiply-back.
 Poly625 wideQ{};array<F,256> Q{};
 for(int i=0;i<625;i++){
  auto d=digits(i,5);F v=P[i];bool pred=true;for(int k:d)if(k==0)pred=false;
  if(pred)v=add(v,mul(h,wideQ[i-156]));wideQ[i]=v;
  bool cubic=true;for(int k:d)if(k==4)cubic=false;
  if(!cubic && v)throw runtime_error("nonzero outer quotient coefficient");
  if(cubic){int j=idx(d,4);Q[j]=v;if(v && *max_element(d.begin(),d.end())-*min_element(d.begin(),d.end())>2)throw runtime_error("cut support failure");if(v && variation(d)>4)throw runtime_error("two-cut variation failure");}
 }
 // Multiply F*Q in all 5^4 positions, without coefficient projection.
 Poly625 back{};
 for(int j=0;j<256;j++){int i=index4to5[j];back[i]=add(back[i],Q[j]);back[i+156]=sub(back[i+156],mul(h,Q[j]));}
 if(back!=P)throw runtime_error("full polynomial division failure");
 return Q;
}
void write_vec(const vector<int>&v){cout<<'[';for(size_t k=0;k<v.size();k++){if(k)cout<<',';cout<<v[k];}cout<<']';}
int main(int argc,char**argv){try{
 init();F ii=argc>1?stoull(argv[1]):569522298ULL;if(mul(ii,ii)!=p-1)throw runtime_error("invalid Gaussian embedding");
 int only=argc>2?stoi(argv[2]):-1;int label=0,passed=0,failed=0;uint64_t windows=0;
 for(int s=0;s<2;s++)for(int br=1;br<=2;br++)for(int a=0;a<5;a++)for(int b=a+1;b<6;b++)for(int c=b+1;c<7;c++)for(int d=c+1;d<8;d++,label++){
  if(only>=0 && label!=only)continue;
  array<int,4> edges={8*br+a,8*br+b,8*br+c,8*br+d};auto z=build(s,br,edges,ii);auto zc=build(s,br,edges,p-ii);auto H=modulus_product(z.N,zc.N);
  array<vector<F>,126> basis;vector<int> rows,pivots;array<bool,256> seen{};F det=1;int wi=0;
  for(int ar=0;ar<8;ar++)for(int rr=ar+1;rr<8;rr++)for(int bc=0;bc<8;bc++)for(int cc=bc+1;cc<8;cc++,wi++){
   auto Q=quotient(H,ar,rr,bc,cc,z.active_h);windows++;for(int e=0;e<256;e++)if(Q[e])seen[e]=true;
   vector<F> row;for(int e:support)row.push_back(Q[e]);
   for(int j=0;j<126;j++)if(row[j]){
    if(basis[j].empty()){
     F pivot=row[j];det=mul(det,pivot);F reciprocal=inv(pivot);for(int k=j;k<126;k++)row[k]=mul(row[k],reciprocal);
     basis[j]=row;rows.push_back(wi);pivots.push_back(j);break;
    }else{F scale=row[j];for(int k=j;k<126;k++)row[k]=sub(row[k],mul(scale,basis[j][k]));}
   }
   // Continue through all 784 original windows after the fixed minor is full rank.
  }
  // New pivot columns need not arrive in sorted order; determinant uses listed pivot-column order.
  int inversions=0;for(size_t i=0;i<pivots.size();i++)for(size_t j=i+1;j<pivots.size();j++)if(pivots[i]>pivots[j])inversions++;
  // Recorded column order is natural support order restricted to selected pivots.
  auto sortedp=pivots;sort(sortedp.begin(),sortedp.end());if(inversions%2)det=sub(0,det);
  if(rows.size()==126)passed++;else failed++;
  cerr<<"SUPPORT label="<<label<<" absent=";for(int e:support)if(!seen[e])cerr<<e<<",";cerr<<"\n";
  cout<<"{\"label\":"<<label<<",\"stage\":"<<s<<",\"branch\":"<<br<<",\"edges\":["<<edges[0]<<','<<edges[1]<<','<<edges[2]<<','<<edges[3]<<"],\"encoded\":["<<24*s+edges[0]<<','<<24*s+edges[1]<<','<<24*s+edges[2]<<','<<24*s+edges[3]<<"],\"rank\":"<<rows.size()<<",\"windows\":";write_vec(rows);cout<<",\"columns\":";vector<int> cols;for(int j:sortedp)cols.push_back(support[j]);write_vec(cols);cout<<",\"determinant\":"<<det<<",\"prime\":"<<p<<",\"i_image\":"<<ii<<"}\n";
  cerr<<"label="<<label<<" stage="<<s<<" branch="<<br<<" rank="<<rows.size()<<" checked_windows="<<wi<<"\n";
 }
 cerr<<"SUMMARY labels="<<passed+failed<<" passed="<<passed<<" failed="<<failed<<" quotient_checks="<<windows<<"\n";
 return failed?2:0;
 }catch(exception&e){cerr<<"FATAL "<<e.what()<<'\n';return 1;}}
