// Independently authored rank reconstruction; no submitted source is linked or executed.
#include <iostream>
#include <vector>
#include <array>
#include <fstream>
#include <string>
using I=long long; using E=std::array<int,3>; I p;
I md(I x){x%=p;return x<0?x+p:x;}
I pw(I a,I b){I r=1;for(;b;b>>=1,a=a*a%p)if(b&1)r=r*a%p;return r;}
std::vector<E> mons(int d){std::vector<E> v;for(int a=d;a>=0;--a)for(int b=d-a;b>=0;--b)v.push_back({a,b,d-a-b});return v;}
int index(const std::vector<E>&v,E e){for(int k=0;k<(int)v.size();++k)if(v[k]==e)return k;throw 1;}
int rank(std::vector<std::vector<I>> a){int row=0;for(int j=0;j<(int)a[0].size()&&row<(int)a.size();++j){int k=row;while(k<(int)a.size()&&!a[k][j])++k;if(k==(int)a.size())continue;std::swap(a[k],a[row]);I z=pw(a[row][j],p-2);for(int t=j;t<(int)a[row].size();++t)a[row][t]=a[row][t]*z%p;for(k=row+1;k<(int)a.size();++k){I c=a[k][j];for(int t=j;t<(int)a[k].size();++t)a[k][t]=md(a[k][t]-c*a[row][t]%p);}++row;}return row;}
int main(int argc,char**argv){for(int f=1;f<argc;++f){std::ifstream in(argv[f]);int n;in>>n>>p;std::vector<std::vector<I>> m(4,std::vector<I>(n*n));for(auto &v:m)for(auto &x:v)in>>x;auto m2=mons(2);long count=0,bad3=0,bad4=0;int low3=10,low4=15;
 for(int r=0;r<n;++r)for(int s=0;s<n;++s)if(r!=s)for(int a=0;a<n;++a)for(int b=0;b<n;++b)if(b!=a)for(int c=0;c<n;++c)if(c!=a&&c!=b)for(int d=0;d<n;++d)if(d!=a&&d!=b&&d!=c){int cols[4]={a,b,c,d};std::vector<std::vector<I>> qs;for(auto ab:std::vector<std::array<int,2>>{{0,1},{0,2},{0,3},{1,2},{1,3}}){int u=ab[0],v=ab[1];I A=m[0][u]*m[0][n+v]%p,B=m[0][v]*m[0][n+u]%p;std::vector<I> q(6);for(int j=0;j<3;++j)for(int k=0;k<3;++k){E e={0,0,0};++e[j];++e[k];I x=A*m[j+1][s*n+cols[u]]%p*m[k+1][r*n+cols[v]]%p;I y=B*m[j+1][s*n+cols[v]]%p*m[k+1][r*n+cols[u]]%p;int t=index(m2,e);q[t]=md(q[t]+x-y);}qs.push_back(q);}
 for(int degree=3;degree<=4;++degree){auto basis=mons(degree),multipliers=mons(degree-2);std::vector<std::vector<I>> matrix;auto selected=degree==3?std::vector<int>{0,1,2,3}:std::vector<int>{0,1,4};for(int q:selected)for(E e:multipliers){std::vector<I> row(basis.size());for(int j=0;j<6;++j){E ex={e[0]+m2[j][0],e[1]+m2[j][1],e[2]+m2[j][2]};row[index(basis,ex)]=qs[q][j];}matrix.push_back(row);}int rr=rank(matrix);if(degree==3){if(rr<10)++bad3;low3=std::min(low3,rr);}else{if(rr<15)++bad4;low4=std::min(low4,rr);}}
 ++count;}
 std::cout<<"{\"N\":"<<n<<",\"p\":"<<p<<",\"mappings\":"<<count<<",\"min_cubic_rank\":"<<low3<<",\"min_quartic_rank\":"<<low4<<",\"deficient_cubic\":"<<bad3<<",\"deficient_quartic\":"<<bad4<<"}"<<std::endl;}
}
