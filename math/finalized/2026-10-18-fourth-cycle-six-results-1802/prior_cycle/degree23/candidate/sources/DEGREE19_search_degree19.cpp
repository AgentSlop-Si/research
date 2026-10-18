#include <array>
#include <vector>
#include <iostream>
#include <fstream>
#include <cstdint>
#include <algorithm>
#include <chrono>
using namespace std;
constexpr int P=53,D=19;
using Big=__uint128_t;
constexpr Big ORDER=[]() constexpr {Big r=1;for(int i=0;i<D;i++)r*=P;return r;}();
struct F {
 array<int,D>a{};
 F(int x=0){a[0]=(x%P+P)%P;}
 bool zero()const{for(int v:a)if(v)return false;return true;}
 bool operator==(const F&o)const{return a==o.a;}
 bool operator!=(const F&o)const{return a!=o.a;}
 F operator+(const F&o)const{F z;for(int i=0;i<D;i++){int v=a[i]+o.a[i];z.a[i]=v>=P?v-P:v;}return z;}
 F operator-(const F&o)const{F z;for(int i=0;i<D;i++){int v=a[i]-o.a[i];z.a[i]=v<0?v+P:v;}return z;}
 F operator-()const{return F()-*this;}
 F operator*(const F&o)const{int c[2*D-1]={};for(int i=0;i<D;i++)for(int j=0;j<D;j++)c[i+j]+=a[i]*o.a[j];for(int i=2*D-2;i>=D;i--){c[i-D]-=12*c[i];c[i-D+1]-=c[i];}F z;for(int i=0;i<D;i++){int v=c[i]%P;z.a[i]=v<0?v+P:v;}return z;}
 F power(Big e)const{F x=*this,z(1);while(e){if(e&1)z=z*x;e>>=1;if(e)x=x*x;}return z;}
 F inverse()const{if(zero()){cerr<<"division zero\n";exit(2);}return power(ORDER-2);}
 F operator/(const F&o)const{return *this*o.inverse();}
};
ostream&operator<<(ostream&s,const F&v){s<<'[';for(int i=0;i<D;i++){if(i)s<<',';s<<v.a[i];}return s<<']';}
uint64_t rng=202610181330ULL;
uint64_t next(){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}
F randomF(){F x;for(int&i:x.a)i=next()%P;return x;}
using Poly=vector<F>;
void trim(Poly&x){while(x.size()>1&&x.back().zero())x.pop_back();}
Poly mod(Poly a,const Poly&h){for(int k=(int)a.size()-1;k>=(int)h.size()-1;k--){F c=a[k];if(c.zero())continue;for(int j=0;j<(int)h.size()-1;j++)a[k-(h.size()-1)+j]=a[k-(h.size()-1)+j]-c*h[j];}a.resize(min(a.size(),h.size()-1));if(a.empty())a={F()};trim(a);return a;}
Poly mulmod(const Poly&a,const Poly&b,const Poly&h){Poly c(a.size()+b.size()-1);for(int i=0;i<(int)a.size();i++)for(int j=0;j<(int)b.size();j++)c[i+j]=c[i+j]+a[i]*b[j];return mod(c,h);}
Poly powmod(Poly x,Big e,const Poly&h){Poly z={F(1)};while(e){if(e&1)z=mulmod(z,x,h);e>>=1;if(e)x=mulmod(x,x,h);}return z;}
bool split(const Poly&h){
 // Exact Frobenius splitting in degree 19, represented beyond uint64_t.
 return powmod({F(0),F(1)},ORDER,h)==Poly({F(0),F(1)});
}
int pm(int a,int e){int z=1;a=(a%P+P)%P;while(e){if(e&1)z=z*a%P;e>>=1;if(e)a=a*a%P;}return z;}
int G[2][2][13][13],TARGET[13][13];
int gauss(int e,int d,int a,int b){int r=(e*a%13+13)%13,l=(d*b%13+13)%13;if(r+l>=13)return 0;int w=pm(16,(e*d+13)%13),z=1;for(int i=1;i<=l;i++)z=z*(1-pm(w,r+i)+P)%P*pm(1-pm(w,i),P-2)%P;return z;}
void setup(){for(int e=0;e<2;e++)for(int d=0;d<2;d++)for(int a=0;a<13;a++)for(int b=0;b<13;b++)G[e][d][a][b]=gauss(2*e-1,2*d-1,a,b);for(int a=0;a<13;a++)for(int b=0;b<13;b++)TARGET[a][b]=pm(16,10*(a+b)*(a+b)%13);}
F moment(const array<F,14>&yp,int a,int b){int c=G[0][1][a][b]*pm(G[0][1][13-b][b],P-2)%P;return (F(TARGET[a][b])-yp[13-a-b]*F(c))*F(pm(G[1][1][a][b],P-2));}
bool line(const array<F,14>&yp,Poly&c,Poly&n){int bs[6]={1,1,1,1,2,2},as[6]={1,2,3,4,2,3};F M[6][8];for(int i=0;i<6;i++)for(int j=0;j<8;j++)M[i][j]=moment(yp,as[i]+j,bs[i]);for(int i=0;i<6;i++){int k=i;while(k<6&&M[k][i].zero())k++;if(k==6)return false;if(k!=i)for(int j=0;j<8;j++)swap(M[k][j],M[i][j]);F v=M[i][i].inverse();for(int j=i;j<8;j++)M[i][j]=M[i][j]*v;for(int k=0;k<6;k++)if(k!=i){F v=M[k][i];for(int j=i;j<8;j++)M[k][j]=M[k][j]-v*M[i][j];}}c.resize(8);n.resize(8);for(int i=0;i<6;i++){c[i]=-M[i][7];n[i]=-M[i][6];}c[7]=1;n[6]=1;return true;}
array<F,3> gate(const array<F,14>&yp,const Poly&c,const Poly&n){F U[9],V[9],E[2][2],B[2][2];for(int a=1;a<=9;a++){U[a-1]=moment(yp,a,3);V[a-1]=yp[a]*F(G[1][0][a][3]*pm(G[1][1][a][3],P-2)%P);}for(int s=0;s<2;s++)for(int j=0;j<8;j++){E[s][0]=E[s][0]+c[j]*U[s+j];E[s][1]=E[s][1]+n[j]*U[s+j];B[s][0]=B[s][0]+c[j]*V[s+j];B[s][1]=B[s][1]+n[j]*V[s+j];}return {E[0][0]*B[1][0]-E[1][0]*B[0][0],E[0][0]*B[1][1]+E[0][1]*B[1][0]-E[1][0]*B[0][1]-E[1][1]*B[0][0],E[0][1]*B[1][1]-E[1][1]*B[0][1]};}
vector<F> roots2(const array<F,3>&a){if(a[2].zero()){if(a[1].zero())return {};return {-a[0]/a[1]};}F d=a[1]*a[1]-F(4)*a[0]*a[2],s=d.power((ORDER+3)/8);if(s*s!=d)s=s*F(23);if(s*s!=d)return {};F inv=(F(2)*a[2]).inverse();if(s.zero())return {-a[1]*inv};return {(-a[1]+s)*inv,(-a[1]-s)*inv};}
int main(int argc,char**argv){setup();int limit=argc>1?stoi(argv[1]):100000;uint64_t candidates=0;auto start=chrono::steady_clock::now();for(int trial=0;trial<limit;trial++){F y=randomF();if(y.zero()){trial--;continue;}array<F,14>yp;yp[0]=1;for(int j=1;j<14;j++)yp[j]=yp[j-1]*y;Poly c,n;if(!line(yp,c,n)){cerr<<"unexpected chart failure\n";return 3;}auto q=gate(yp,c,n);for(F lam:roots2(q)){Poly h(8);for(int j=0;j<8;j++)h[j]=c[j]+lam*n[j];if(h[0].zero())continue;candidates++;if(split(h)){cout<<"{\"trial\":"<<trial<<",\"candidates\":"<<candidates<<",\"y\":"<<y<<",\"lambda\":"<<lam<<",\"H\":[";for(int j=0;j<8;j++){if(j)cout<<',';cout<<h[j];}cout<<"]}\n";return 0;}}if(trial%100==0){double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();cerr<<"trial "<<trial<<" candidates "<<candidates<<" seconds "<<seconds<<'\n';}}cerr<<"NO_SPLIT declared trials="<<limit<<" candidates="<<candidates<<'\n';return 1;}
