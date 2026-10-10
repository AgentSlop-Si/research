// Authored independently for this review: coefficient expansion and row-echelon rank.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
using namespace std;using I=int64_t;
#ifndef AUDIT_PRIME
#define AUDIT_PRIME 998244353
#endif
constexpr I p=AUDIT_PRIME;
I pw(I a,I b){I r=1;while(b){if(b&1)r=r*a%p;a=a*a%p;b>>=1;}return r;}
I sub(I a,I b){a-=b;return a<0?a+p:a;}
int main(int argc,char**argv){
 if(argc!=4)return 2;ifstream in(argv[1]);int n;I ip;in>>n>>ip;if(n>16||ip!=p)return 3;
 I T[16][16],G[4][16][16];for(int i=0;i<n;i++)for(int j=0;j<n;j++)in>>T[i][j];for(int k=0;k<4;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)in>>G[k][i][j];if(!in)return 4;
 vector<array<int,4>> m2,m3;vector<array<int,3>>trip;
 for(int a=0;a<=2;a++)for(int b=0;b<=2-a;b++)for(int c=0;c<=2-a-b;c++)m2.push_back({a,b,c,2-a-b-c});
 for(int a=0;a<=3;a++)for(int b=0;b<=3-a;b++)for(int c=0;c<=3-a-b;c++)m3.push_back({a,b,c,3-a-b-c});
 int slots[4][10],qslot[4][4];
 for(int a=0;a<4;a++)for(int b=0;b<10;b++){auto e=m2[b];e[a]++;for(int k=0;k<20;k++)if(e==m3[k])slots[a][b]=k;}
 for(int a=0;a<4;a++)for(int b=0;b<4;b++){array<int,4>e={0,0,0,0};e[a]++;e[b]++;for(int k=0;k<10;k++)if(e==m2[k])qslot[a][b]=k;}
 I L[16][16][4];for(int i=0;i<n;i++)for(int j=0;j<n;j++){L[i][j][0]=G[1][i][j];L[i][j][1]=G[2][i][j];L[i][j][2]=G[3][i][j];L[i][j][3]=G[0][i][j];}
 for(int a=0;a<n;a++)for(int b=0;b<n;b++)for(int c=0;c<n;c++)if(a!=b&&a!=c&&b!=c)trip.push_back({a,b,c});
 ofstream stream(argv[2],ios::binary),details(argv[3]);int hist[21]={};long count=0;
 for(auto r:trip)for(auto c:trip){
  I M[36][20]={};int row=0;
  for(int i=0;i<3;i++)for(int k=i+1;k<3;k++)for(int j=0;j<3;j++)for(int l=j+1;l<3;l++){
   I A=T[i][l]*T[k][j]%p,B=T[i][j]*T[k][l]%p,q[10]={};
   for(int a=0;a<4;a++)for(int b=0;b<4;b++){
    I x=A*(L[r[i]][c[j]][a]*L[r[k]][c[l]][b]%p)%p;
    I y=B*(L[r[i]][c[l]][a]*L[r[k]][c[j]][b]%p)%p;
    int z=qslot[a][b];q[z]=(q[z]+sub(x,y))%p;
   }
   for(int a=3;a>=0;a--){for(int b=0;b<10;b++)M[row][slots[a][b]]=q[b];row++;}
  }
  int rank=0;
  for(int col=0;col<20;col++){
   int pivot=rank;while(pivot<36&&!M[pivot][col])pivot++;if(pivot==36)continue;
   for(int j=col;j<20;j++)swap(M[rank][j],M[pivot][j]);I v=pw(M[rank][col],p-2);
   for(int j=col;j<20;j++)M[rank][j]=M[rank][j]*v%p;
   for(int i=rank+1;i<36;i++){I f=M[i][col];if(f)for(int j=col+1;j<20;j++)M[i][j]=sub(M[i][j],f*M[rank][j]%p);}
   rank++;
  }
  hist[rank]++;stream.put((char)rank);count++;
  if(rank!=20)details<<r[0]<<","<<r[1]<<","<<r[2]<<"/"<<c[0]<<","<<c[1]<<","<<c[2]<<" "<<rank<<"\n";
  if(count%1000000==0)cerr<<"checked "<<count<<"\n";
 }
 cout<<"N "<<n<<" prime "<<p<<" cases "<<count<<"\n";for(int i=0;i<=20;i++)if(hist[i])cout<<"rank "<<i<<" count "<<hist[i]<<"\n";return 0;
}
