// Fresh characteristic-zero-lift minor generator; finite-field algebra is not by itself root exclusion.
#include <array>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <cassert>
#include <chrono>
#include "chart_data.hpp"
using namespace std;
using ll=long long;
const ll MOD=1000000009;
ll IM=569522298;
ll norm(ll x){x%=MOD;return x<0?x+MOD:x;}
ll pw(ll x,ll n){ll r=1;for(;n;n>>=1,x=x*x%MOD)if(n&1)r=r*x%MOD;return r;}
struct Poly {array<ll,8>a{};};
using Mat=array<Poly,64>;
using P=array<ll,125>;
array<array<int,3>,125>exp5;
array<array<int,3>,27>exp3;
array<int,8>idx5,idx3;
int sum33[27][27],sum88[8][8];
void init(){for(int i=0;i<125;i++)exp5[i]={i/25,(i/5)%5,i%5};for(int i=0;i<27;i++)exp3[i]={i/9,(i/3)%3,i%3};for(int i=0;i<8;i++){idx5[i]=25*(i&1)+5*((i>>1)&1)+((i>>2)&1);idx3[i]=9*(i&1)+3*((i>>1)&1)+((i>>2)&1);}for(int i=0;i<27;i++)for(int j=0;j<27;j++)sum33[i][j]=25*(exp3[i][0]+exp3[j][0])+5*(exp3[i][1]+exp3[j][1])+exp3[i][2]+exp3[j][2];for(int i=0;i<8;i++)for(int j=0;j<8;j++)sum88[i][j]=idx3[i]+idx3[j];}
Poly mul(const Poly&a,const Poly&b){Poly c;for(int i=0;i<8;i++)if(a.a[i])for(int j=0;j<8;j++)if(b.a[j]){assert(!(i&j));c.a[i|j]=(c.a[i|j]+a.a[i]*b.a[j])%MOD;}return c;}
void add(Poly&a,const Poly&b){for(int k=0;k<8;k++)a.a[k]=(a.a[k]+b.a[k])%MOD;}
Mat mm(const Mat&A,const Mat&B){Mat C;for(int r=0;r<8;r++)for(int c=0;c<8;c++)for(int k=0;k<8;k++)add(C[r*8+c],mul(A[r*8+k],B[k*8+c]));return C;}
struct Guard {int mask;ll h;};
struct Model {Mat N;vector<Guard>active;array<ll,6>frozen;};
Model build(const array<int,3>&L,ll im){Model out;array<Mat,2>A;
 for(int s=0;s<2;s++){
  array<Mat,3>B;array<Poly,3>d;
  for(int b=0;b<3;b++){
   array<ll,8>w;array<int,8>m{};ll h=1;int mask=0;
   for(int j=0;j<8;j++){int edge=8*b+j;ll v=1;if(edge>=7){ll a=pairs[s][edge-7][0],bb=pairs[s][edge-7][1],den=norm(a-im*bb);assert(den);assert(norm(a+im*bb));v=norm(a+im*bb)*pw(den,MOD-2)%MOD;}w[j]=v;h=h*v%MOD;for(int t=0;t<3;t++)if(L[t]==s*24+edge){m[j]=1<<t;mask|=m[j];}}
   assert(h&&h!=1);out.frozen[s*3+b]=norm(1-h);d[b].a[0]=1;d[b].a[mask]=norm(d[b].a[mask]-h);if(mask)out.active.push_back({mask,h});
   for(int start=0;start<8;start++){int col=cycles[s][b][start];B[b][col*8+col].a[0]=1;ll v=1;int mk=0;for(int len=1;len<8;len++){int j=(start+len)%8;v=v*w[j]%MOD;mk|=m[j];B[b][cycles[s][b][j]*8+col].a[mk]=v;}}
  }
  for(int b=0;b<3;b++){Poly other;other.a[0]=1;for(int c=0;c<3;c++)if(c!=b)other=mul(other,d[c]);for(int k=0;k<64;k++)add(A[s][k],mul(B[b][k],other));}
 }
 out.N=mm(A[1],A[0]);return out;
}
P divide(P a,const Guard&g){P q{};int delta=idx5[g.mask];auto e=exp5[delta];ll inv=pw(norm(-g.h),MOD-2);for(int i=124;i>=0;i--)if(a[i]){for(int k=0;k<3;k++)assert(exp5[i][k]>=e[k]);int j=i-delta;ll v=a[i]*inv%MOD;q[j]=v;a[i]=0;a[j]=norm(a[j]-v);}for(ll v:a)assert(!v);return q;}
struct Basis {vector<array<ll,64>>rows;vector<int>piv,windows;ll det=1;bool push(array<ll,64>r,int w){for(int j=0;j<(int)rows.size();j++){ll v=r[piv[j]];if(v)for(int k=0;k<64;k++)r[k]=norm(r[k]-v*rows[j][k]);}int k=0;while(k<64&&!r[k])k++;if(k==64)return false;ll pivot=r[k];det=det*pivot%MOD;ll inv=pw(pivot,MOD-2);for(ll&v:r)v=v*inv%MOD;rows.push_back(r);piv.push_back(k);windows.push_back(w);return true;}};
vector<pair<int,int>>windowpairs;
string family(array<int,3>L){int s0=L[0]/24,s1=L[1]/24,s2=L[2]/24;if(s0==s2){int b0=(L[0]%24)/8,b1=(L[1]%24)/8,b2=(L[2]%24)/8;if(b0==b2)return "same_branch_300";return "same_stage_210";}int i=(s0==s1)?0:1;return ((L[i]%24)/8==(L[i+1]%24)/8)?"mixed_same_branch_pair":"mixed_different_branch_pair";}
bool accepted(array<int,3>L){if(L[0]/24!=L[2]/24)return false;int a=L[0]%24,b=L[1]%24,c=L[2]%24;return (a==7&&b>=8&&b<=15&&c>=16)||(a>=8&&c<=15);}
int main(int argc,char**argv){init();if(argc>1)IM=stoll(argv[1]);assert(IM*IM%MOD==MOD-1);for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)windowpairs.push_back({i,j});int n=0,fail=0;auto start=chrono::steady_clock::now();vector<int>coords;for(int s=0;s<2;s++)for(int e=7;e<24;e++)coords.push_back(s*24+e);
 for(int i=0;i<34;i++)for(int j=i+1;j<34;j++)for(int k=j+1;k<34;k++){
  array<int,3>L={coords[i],coords[j],coords[k]};if(accepted(L))continue;string fam=family(L);int target=fam=="same_branch_300"?46:fam=="same_stage_210"?41:fam=="mixed_same_branch_pair"?56:52;auto M=build(L,IM),C=build(L,MOD-IM);
  array<array<ll,27>,64>H{};for(int pos=0;pos<64;pos++)for(int a=0;a<8;a++)for(int b=0;b<8;b++)H[pos][sum88[a][b]]=(H[pos][sum88[a][b]]+M.N[pos].a[a]*C.N[pos].a[7-b])%MOD;
  Basis basis;int tested=0;
  for(int rpair=0;rpair<28&&(int)basis.rows.size()<target;rpair++)for(int cpair=0;cpair<28&&(int)basis.rows.size()<target;cpair++){
   auto[a,r]=windowpairs[rpair];auto[b,c]=windowpairs[cpair];P P0{};for(int u=0;u<27;u++)for(int v=0;v<27;v++){int id=sum33[u][v];P0[id]=norm(P0[id]+H[r*8+c][u]*H[a*8+b][v]-H[r*8+b][u]*H[a*8+c][v]);}
   P q=P0;for(auto g:M.active)q=divide(q,g);array<ll,64>row{};for(int id=0;id<125;id++)if(q[id]){auto e=exp5[id];assert(e[0]<4&&e[1]<4&&e[2]<4);row[16*e[0]+4*e[1]+e[2]]=q[id];}basis.push(row,rpair*28+cpair);tested++;
  }
  bool ok=(int)basis.rows.size()==target;if(!ok)fail++;n++;
  cout<<"{\"label\":["<<L[0]<<","<<L[1]<<","<<L[2]<<"],\"family\":\""<<fam<<"\",\"rank\":"<<basis.rows.size()<<",\"target\":"<<target<<",\"determinant\":"<<basis.det<<",\"windows_tested\":"<<tested<<",\"windows\":[";for(int t=0;t<(int)basis.windows.size();t++)cout<<(t?",":"")<<basis.windows[t];cout<<"],\"columns\":[";for(int t=0;t<(int)basis.piv.size();t++)cout<<(t?",":"")<<basis.piv[t];cout<<"]}"<<endl;
  if(n%100==0)cerr<<n<<" checked, "<<fail<<" failed, seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 }
 cerr<<"FINAL checked="<<n<<" failed="<<fail<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;assert(n==5744);return fail?2:0;
}
