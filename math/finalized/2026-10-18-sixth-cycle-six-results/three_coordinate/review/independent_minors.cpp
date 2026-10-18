// Independent review: Boolean interpolation from direct Green inverses;
// ascending constant-term division; fixed, not greedily chosen, determinants.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <map>
#include <string>
#include <chrono>
using namespace std; using Z=long long; const Z p=1000000009;
Z md(Z v){v%=p;return v<0?v+p:v;} Z powr(Z a,Z n){Z b=1;while(n){if(n&1)b=b*a%p;a=a*a%p;n/=2;}return b;} Z inv(Z a){assert(a);return powr(a,p-2);}
using Mat=array<Z,64>; using Num=array<Mat,8>; using Poly=array<Z,125>;
int cyc[2][3][8],ab[2][17][2]; array<int,3>E[125]; int bitindex[8],conv[27][27]; vector<pair<int,int>> wp;
Z inversions=0,entrychecks=0,quotients=0,jetchecks=0,minorchecks=0;
Mat times(const Mat&a,const Mat&b){Mat c{};for(int i=0;i<8;i++)for(int j=0;j<8;j++)for(int k=0;k<8;k++)c[8*i+j]=(c[8*i+j]+a[8*i+k]*b[8*k+j])%p;return c;}
Mat invert(const Mat&a,Z expected){array<array<Z,16>,8>T{};for(int i=0;i<8;i++)for(int j=0;j<8;j++){T[i][j]=a[8*i+j];T[i][8+j]=(i==j);}Z det=1;
 for(int k=0;k<8;k++){int r=k;while(r<8&&!T[r][k])r++;assert(r<8);if(r!=k){swap(T[k],T[r]);det=md(-det);}Z v=T[k][k];det=det*v%p;Z iv=inv(v);for(int j=0;j<16;j++)T[k][j]=T[k][j]*iv%p;for(int i=0;i<8;i++)if(i!=k){v=T[i][k];for(int j=0;j<16;j++)T[i][j]=md(T[i][j]-v*T[k][j]);}}
 assert(det==expected);Mat b{};for(int i=0;i<8;i++)for(int j=0;j<8;j++)b[8*i+j]=T[i][8+j];auto c=times(a,b),d=times(b,a);for(int i=0;i<64;i++){assert(c[i]==Z(i/8==i%8)&&d[i]==Z(i/8==i%8));entrychecks+=2;}inversions++;return b;
}
struct Guard{int mask;Z h;}; struct Model{Num coef;vector<Guard> guards;array<Z,6> h;};
Model interpolate(array<int,3>L,Z ii){Model out;Z gain[2][24];int edgevar[2][24];for(int s=0;s<2;s++)for(int e=0;e<24;e++){gain[s][e]=1;edgevar[s][e]=-1;if(e>=7){Z a=ab[s][e-7][0],b=ab[s][e-7][1];gain[s][e]=md(a+b*ii)*inv(md(a-b*ii))%p;}for(int v=0;v<3;v++)if(L[v]==24*s+e)edgevar[s][e]=v;}
 for(int s=0;s<2;s++)for(int b=0;b<3;b++){Z h=1;int mask=0;for(int j=0;j<8;j++){h=h*gain[s][8*b+j]%p;int v=edgevar[s][8*b+j];if(v>=0)mask|=1<<v;}assert(h&&h!=1);out.h[s*3+b]=h;if(mask)out.guards.push_back({mask,h});}
 for(int point=0;point<8;point++){Mat stage[2]{};for(int s=0;s<2;s++){Z D=1;for(int b=0;b<3;b++){Mat A{};for(int j=0;j<8;j++)A[9*j]=1;Z h=1;for(int j=0;j<8;j++){int e=8*b+j,v=edgevar[s][e];Z w=gain[s][e];if(v>=0&&!(point&(1<<v)))w=0;h=h*w%p;int r=cyc[s][b][j],c=cyc[s][b][(j+7)%8];A[r*8+c]=md(A[r*8+c]-w);}Z d=md(1-h);assert(d);D=D*d%p;auto G=invert(A,d);for(int k=0;k<64;k++)stage[s][k]=(stage[s][k]+G[k])%p;}
 for(Z&v:stage[s])v=v*D%p;}out.coef[point]=times(stage[1],stage[0]);}
 for(int v=0;v<3;v++)for(int mask=0;mask<8;mask++)if(mask&(1<<v))for(int k=0;k<64;k++)out.coef[mask][k]=md(out.coef[mask][k]-out.coef[mask^(1<<v)][k]);return out;
}
Poly quotient(Poly a,Guard g){Poly q{};auto e=E[bitindex[g.mask]];int delta=bitindex[g.mask];for(int id=0;id<125;id++){q[id]=a[id];bool ge=true;for(int t=0;t<3;t++)if(E[id][t]<e[t])ge=false;if(ge)q[id]=(q[id]+g.h*q[id-delta])%p;}
 for(int id=0;id<125;id++){bool overflow=false;for(int t=0;t<3;t++)if(e[t]&&E[id][t]==4)overflow=true;if(overflow)assert(q[id]==0);Z v=q[id];bool ge=true;for(int t=0;t<3;t++)if(E[id][t]<e[t])ge=false;if(ge)v=md(v-g.h*q[id-delta]);assert(v==a[id]);}return q;}
Z determinant(vector<vector<Z>>A){int n=A.size();Z d=1;for(int c=0;c<n;c++){int r=c;while(r<n&&!A[r][c])r++;if(r==n)return 0;if(r!=c){swap(A[r],A[c]);d=md(-d);}Z v=A[c][c];d=d*v%p;Z iv=inv(v);for(int r=c+1;r<n;r++){Z m=A[r][c]*iv%p;for(int j=c+1;j<n;j++)A[r][j]=md(A[r][j]-m*A[c][j]);}}return d;}
struct Rec{array<int,3>L;int n;Z d;vector<int>w,c;};bool readrec(istream&f,Rec&r){if(!(f>>r.L[0]))return false;f>>r.L[1]>>r.L[2]>>r.n>>r.d;r.w.resize(r.n);r.c.resize(r.n);for(auto&v:r.w)f>>v;for(auto&v:r.c)f>>v;assert(f);return true;}
int family(const Rec&r){if(r.L[0]/24==r.L[2]/24){if(r.L[0]%24/8==r.L[2]%24/8)return 46;return 41;}for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)if(r.L[i]/24==r.L[j]/24&&r.L[i]%24/8==r.L[j]%24/8)return 56;return 52;}
void constraints(const Poly&q,const Rec&r,const Model&m){for(int id=0;id<125;id++){auto e=E[id];if(e[0]>3||e[1]>3||e[2]>3)assert(q[id]==0);for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)if(r.L[i]/24==r.L[j]/24&&r.L[i]%24/8==r.L[j]%24/8&&((e[i]==0&&e[j]==3)||(e[i]==3&&e[j]==0)))assert(q[id]==0);}
 if(r.n!=41&&r.n!=52)return;int a=-1,b=-1,c=-1;for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)if(r.L[i]/24==r.L[j]/24&&((r.n==52)||(r.L[i]%24/8==r.L[j]%24/8))){a=i;b=j;}assert(a>=0);c=3-a-b;
 int ba=(r.L[a]/24)*3+(r.L[a]%24)/8,bb=(r.L[b]/24)*3+(r.L[b]%24)/8,bc=(r.L[c]/24)*3+(r.L[c]%24)/8;
 Z aa=inv(m.h[ba]),bbv=inv(m.h[r.n==41?bc:bb]);Z powersA[4]={1,aa,aa*aa%p,aa*aa%p*aa%p},powersB[4]={1,bbv,bbv*bbv%p,bbv*bbv%p*bbv%p};Z jets[7][3]{};
 for(int id=0;id<125;id++)if(q[id]){auto e=E[id];int block=r.n==41?e[a]-e[b]+3:e[c];int u=r.n==41?e[b]:e[a],v=r.n==41?e[c]:e[b];assert(block>=0&&block<7);Z coeff=q[id];jets[block][0]=(jets[block][0]+coeff*powersA[u]%p*powersB[v])%p;if(u)jets[block][1]=(jets[block][1]+coeff*u%p*powersA[u-1]%p*powersB[v])%p;if(v)jets[block][2]=(jets[block][2]+coeff*v%p*powersA[u]%p*powersB[v-1])%p;}
 for(auto&arr:jets)for(Z v:arr){assert(!v);jetchecks++;}
}
void check(const Rec&r,const Model&plus,const Model&minus,bool negative){array<array<Z,27>,64>H{};for(int a=0;a<8;a++)for(int b=0;b<8;b++){int id=9*((a&1)+(b&1))+3*(((a>>1)&1)+((b>>1)&1))+((a>>2)&1)+((b>>2)&1);for(int k=0;k<64;k++)H[k][id]=(H[k][id]+plus.coef[a][k]*minus.coef[7^b][k])%p;}
 vector<vector<Z>>minor;for(int w:r.w){int rr=w/28,cc=w%28;auto[a,b]=wp[rr];auto[c,d]=wp[cc];Poly P{};for(int i=0;i<27;i++)for(int j=0;j<27;j++){int id=conv[i][j];P[id]=md(P[id]+H[a*8+c][i]*H[b*8+d][j]-H[a*8+d][i]*H[b*8+c][j]);}Poly q=P;for(auto g:plus.guards)q=quotient(q,g);constraints(q,r,plus);vector<Z>row;for(int c:r.c)row.push_back(q[25*(c/16)+5*((c/4)%4)+(c%4)]);minor.push_back(row);quotients++;}
 Z actual=determinant(minor);if(actual!=r.d){cerr<<"BAD determinant "<<r.L[0]<<','<<r.L[1]<<','<<r.L[2]<<" got "<<actual<<" expected "<<r.d<<'\n';abort();}assert(actual);minorchecks++;if(negative){minor[1]=minor[0];assert(determinant(minor)==0);}
}
int main(){ifstream ch("REVIEW_CHART.txt");for(int s=0;s<2;s++){for(auto&b:cyc[s])for(int&j:b)ch>>j;for(auto&pair:ab[s])for(int&j:pair)ch>>j;}assert(ch);for(int i=0;i<125;i++)E[i]={i/25,(i/5)%5,i%5};for(int m=0;m<8;m++)bitindex[m]=25*(m&1)+5*((m>>1)&1)+((m>>2)&1);for(int i=0;i<27;i++)for(int j=0;j<27;j++)conv[i][j]=25*(i/9+j/9)+5*((i/3)%3+(j/3)%3)+i%3+j%3;for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)wp.emplace_back(i,j);
 ifstream f("REVIEW_MINORS_PRIMARY.txt"),g("REVIEW_MINORS_CONJUGATE.txt");Rec a,b;int count=0,negative=0;map<int,int>counts;auto start=chrono::steady_clock::now();while(readrec(f,a)){assert(readrec(g,b)&&a.L==b.L&&a.n==b.n&&a.n==family(a));auto pos=interpolate(a.L,569522298),neg=interpolate(a.L,430477711);bool control=counts[a.n]==0;check(a,pos,neg,control);check(b,neg,pos,control);if(control)negative+=2;counts[a.n]++;count++;if(count%500==0)cerr<<count<<" verified; seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<'\n';}assert(!readrec(g,b)&&count==5744);ofstream out("INDEPENDENT_MINORS.json");out<<"{\n  \"result\": \"PASS\",\n  \"labels\": "<<count<<",\n  \"fixed_minor_checks\": "<<minorchecks<<",\n  \"full_polynomial_quotient_checks\": "<<quotients<<",\n  \"direct_green_inversions\": "<<inversions<<",\n  \"inverse_entry_comparisons\": "<<entrychecks<<",\n  \"jet_comparisons\": "<<jetchecks<<",\n  \"duplicate_row_controls\": "<<negative<<",\n  \"seconds\": "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n}\n";cout<<"PASS "<<count<<" labels, "<<minorchecks<<" fixed minors.\n";
}
