// Independently authored exhaustive Phase29 anchored-Macaulay checker.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
using namespace std;
using I=int64_t;
I p;I pw(I a,I b){I r=1;while(b){if(b&1)r=r*a%p;a=a*a%p;b>>=1;}return r;}
I sub(I a,I b){a-=b;return a<0?a+p:a;}
int main(int argc,char**argv){
 if(argc!=4)return 2;ifstream in(argv[1]);int n;in>>n>>p;if(n!=8)return 3;
 I T[8][8],G[3][8][8];for(int i=0;i<n;i++)for(int j=0;j<n;j++)in>>T[i][j];for(int k=0;k<3;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)in>>G[k][i][j];if(!in)return 4;
 vector<array<int,3>> mon2,mon4,trip;
 for(int a=0;a<=2;a++)for(int b=0;b<=2-a;b++)mon2.push_back({a,b,2-a-b});
 for(int a=0;a<=4;a++)for(int b=0;b<=4-a;b++)mon4.push_back({a,b,4-a-b});
 int slots[6][6],qslot[3][3];
 for(int a=0;a<6;a++)for(int b=0;b<6;b++){array<int,3> e;for(int k=0;k<3;k++)e[k]=mon2[a][k]+mon2[b][k];for(int k=0;k<15;k++)if(e==mon4[k])slots[a][b]=k;}
 for(int a=0;a<3;a++)for(int b=0;b<3;b++){array<int,3>e={0,0,0};e[a]++;e[b]++;for(int k=0;k<6;k++)if(e==mon2[k])qslot[a][b]=k;}
 I L[8][8][3];for(int i=0;i<8;i++)for(int j=0;j<8;j++){L[i][j][0]=G[1][i][j];L[i][j][1]=G[2][i][j];L[i][j][2]=G[0][i][j];}
 for(int a=0;a<n;a++)for(int b=0;b<n;b++)for(int c=0;c<n;c++)if(a!=b&&a!=c&&b!=c)trip.push_back({a,b,c});
 ofstream stream(argv[2],ios::binary),details(argv[3]);int hist[16]={0},count=0;
 for(auto r:trip)for(auto c:trip){
  I M[24][15]={};int row=0;
  for(int i=1;i<3;i++)for(int j=1;j<3;j++){
   I A=T[i][j]*T[0][0]%p,B=T[i][0]*T[0][j]%p,q[6]={};
   for(int a=0;a<3;a++)for(int b=0;b<3;b++){
    I x=A*(L[r[i]][c[0]][a]*L[r[0]][c[j]][b]%p)%p;
    I y=B*(L[r[i]][c[j]][a]*L[r[0]][c[0]][b]%p)%p;
    int k=qslot[a][b];q[k]=(q[k]+sub(x,y))%p;
   }
   for(int a=0;a<6;a++){for(int b=0;b<6;b++)M[row][slots[a][b]]=q[b];row++;}
  }
  int rank=0;
  for(int col=0;col<15;col++){
   int pivot=rank;while(pivot<24&&!M[pivot][col])pivot++;if(pivot==24)continue;
   for(int j=col;j<15;j++)swap(M[rank][j],M[pivot][j]);I v=pw(M[rank][col],p-2);
   for(int j=col;j<15;j++)M[rank][j]=M[rank][j]*v%p;
   for(int i=rank+1;i<24;i++){I f=M[i][col];if(f)for(int j=col+1;j<15;j++)M[i][j]=sub(M[i][j],f*M[rank][j]%p);}
   rank++;
  }
  hist[rank]++;stream.put((char)rank);count++;
  if(rank!=15)details<<r[0]<<r[1]<<r[2]<<"/"<<c[0]<<c[1]<<c[2]<<" "<<rank<<"\n";
 }
 cout<<"cases "<<count<<"\n";for(int i=0;i<=15;i++)if(hist[i])cout<<"rank "<<i<<" count "<<hist[i]<<"\n";
 return 0;
}
