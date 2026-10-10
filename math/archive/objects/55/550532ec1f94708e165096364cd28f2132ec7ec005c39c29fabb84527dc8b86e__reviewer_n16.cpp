// Independent fixed-minor verifier. No supplied program is compiled or imported.
#include <fstream>
#include <iostream>
#include <cstdint>
using Z=std::int64_t;
Z p,T[32][32],B[3][32][32];
Z power(Z x,Z k){Z r=1;while(k){if(k&1)r=r*x%p;x=x*x%p;k>>=1;}return r;}
Z minusmod(Z a,Z b){Z z=a-b;return z<0?z+p:z;}
Z det(Z a[10][10]){
 Z d=1;
 for(int c=0;c<10;++c){
   int h=c;while(h<10&&a[h][c]==0)++h;if(h==10)return 0;
   if(h!=c){for(int j=0;j<10;++j){Z t=a[h][j];a[h][j]=a[c][j];a[c][j]=t;}d=d? p-d:0;}
   d=d*a[c][c]%p;Z iv=power(a[c][c],p-2);
   for(int i=c+1;i<10;++i){Z v=a[i][c]*iv%p;if(v)for(int j=c+1;j<10;++j)a[i][j]=minusmod(a[i][j],v*a[c][j]%p);a[i][c]=0;}
 }
 return d;
}
void product(int r,int c,int s,int d,Z out[6]){
 out[0]=B[0][r][c]*B[0][s][d]%p;
 out[1]=(B[0][r][c]*B[1][s][d]%p+B[1][r][c]*B[0][s][d]%p)%p;
 out[2]=(B[0][r][c]*B[2][s][d]%p+B[2][r][c]*B[0][s][d]%p)%p;
 out[3]=B[1][r][c]*B[1][s][d]%p;
 out[4]=(B[1][r][c]*B[2][s][d]%p+B[2][r][c]*B[1][s][d]%p)%p;
 out[5]=B[2][r][c]*B[2][s][d]%p;
}
int main(int argc,char**argv){
 if(argc!=2)return 2;std::ifstream in(argv[1]);int n;in>>n>>p;if(n!=16)return 3;
 for(int i=0;i<n;++i)for(int j=0;j<n;++j)in>>T[i][j];
 for(int k=0;k<3;++k)for(int i=0;i<n;++i)for(int j=0;j<n;++j)in>>B[k][i][j];if(!in)return 4;
 const int pairs[4][2]={{0,1},{0,2},{0,3},{1,2}};
 const int locations[3][6]={{0,1,2,3,4,5},{1,3,4,6,7,8},{2,4,5,7,8,9}};
 Z count=0,prod=1;
 for(int r=0;r<n;++r)for(int s=0;s<n;++s)if(r!=s)
 for(int a=0;a<n;++a)for(int b=0;b<n;++b)if(a!=b)
 for(int c=0;c<n;++c)if(c!=a&&c!=b)
 for(int d=0;d<n;++d)if(d!=a&&d!=b&&d!=c){
   int cs[4]={a,b,c,d};Z A[10][10]={};
   for(int k=0;k<4;++k){int u=pairs[k][0],v=pairs[k][1];Z h[6],l[6],q[6];
     product(s,cs[u],r,cs[v],h);product(s,cs[v],r,cs[u],l);
     Z x=T[0][u]*T[1][v]%p,y=T[0][v]*T[1][u]%p;
     for(int j=0;j<6;++j)q[j]=minusmod(x*h[j]%p,y*l[j]%p);
     for(int m=0;m<3;++m)if(3*k+m<10)for(int j=0;j<6;++j)A[3*k+m][locations[m][j]]=q[j];
   }
   Z h=det(A);if(!h){std::cerr<<"ZERO "<<r<<' '<<s<<' '<<a<<' '<<b<<' '<<c<<' '<<d<<'\n';return 1;}
   ++count;prod=prod*h%p;
 }
 std::cout<<"{\"N\":16,\"prime\":"<<p<<",\"mappings\":"<<count<<",\"first_ten_minor_product\":"<<prod<<",\"all_nonzero\":true,\"enumeration\":\"six nested distinct-index loops\"}\n";
 return count==10483200?0:5;
}
