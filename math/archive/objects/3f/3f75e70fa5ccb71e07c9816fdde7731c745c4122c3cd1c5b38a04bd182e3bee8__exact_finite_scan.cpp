#include <array>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
using namespace std;
int P,Z,inv[2048],zp[8];
int mod(long a){a%=P;return a<0?a+P:a;}
int sig[8]={2,7,5,0,6,1,3,4};int pivot[8]={3,0,0,1,0,0,0,1};
bool off(int r,int j){return r!=j&&r!=(j+1)%8&&r!=sig[j];}
int main(int argc,char**argv){P=argc>1?atoi(argv[1]):17;Z=argc>2?atoi(argv[2]):2; if(P>2048)return 2;zp[0]=1;for(int i=1;i<8;i++)zp[i]=mod(zp[i-1]*Z);if(mod(zp[7]*Z)!=1||zp[4]!=P-1)return 3;for(int a=1;a<P;a++)for(int b=1;b<P;b++)if(mod(a*b)==1){inv[a]=b;break;}
long counts[5]={}, rowsurvive[8]={};int M[8][8],A[8][8],u[8],t[4],v[8],x[8],y[8];
for(t[0]=1;t[0]<P;t[0]++)for(t[1]=1;t[1]<P;t[1]++)for(t[2]=1;t[2]<P;t[2]++)for(t[3]=1;t[3]<P;t[3]++){
 for(int r=0;r<8;r++)for(int j=0;j<8;j++)M[r][j]=mod(zp[(r*(j-j%2))%8]+(j%2?-1:1)*t[j/2]*zp[(r*(j-j%2+1))%8]);
 for(u[0]=1;u[0]<P;u[0]++) {counts[0]++;for(int j=0;j<8;j++)A[0][j]=mod(M[0][j]+u[0]*M[7][j]);bool ok=true;
  for(int j=0;j<8;j++)if(pivot[j]==0&&(!A[0][j]||!A[0][sig[j]])){ok=false;break;}if(!ok)continue;counts[1]++;
  for(int r=1;r<8&&ok;r++) {int val=-1;for(int j=0;j<8;j++)if(pivot[j]==0&&off(r,j)){
    int b=mod(A[0][sig[j]]*M[r][j]-A[0][j]*M[r][sig[j]]),c=mod(A[0][sig[j]]*M[(r+7)%8][j]-A[0][j]*M[(r+7)%8][sig[j]]);
    if(!c){if(b){ok=false;break;}}else{int q=mod(-b*inv[c]);if(val!=-1&&val!=q){ok=false;break;}val=q;}
   }if(!ok)break;if(val==-1){printf("UNDERDETERMINED t=%d,%d,%d,%d w=%d r=%d\n",t[0],t[1],t[2],t[3],u[0],r);return 5;} if(!val)ok=false;u[r]=val;if(ok)rowsurvive[r]++;
  }if(!ok)continue;counts[2]++;
  for(int r=0;r<8;r++)for(int j=0;j<8;j++)A[r][j]=mod(M[r][j]+u[r]*M[(r+7)%8][j]);
  for(int j=0;j<8&&ok;j++){int a=A[pivot[j]][j],c=A[pivot[j]][sig[j]];if(!a||!c){ok=false;break;}v[j]=mod(-a*inv[c]);for(int r=0;r<8;r++)if(off(r,j)&&mod(A[r][j]+v[j]*A[r][sig[j]])){ok=false;break;}}
  if(!ok)continue;counts[3]++;
  for(int j=0;j<8;j++){int r=(j+1)%8;y[j]=mod((A[r][j]+v[j]*A[r][sig[j]])*inv[u[r]]);r=sig[j];x[r]=mod((A[r][j]+v[j]*A[r][sig[j]])*inv[v[j]]);}
  int pu=1,pv=1;for(int j=0;j<8;j++){pu=mod(pu*u[j]);pv=mod(pv*v[j]);if(!x[j]||!y[j]||mod(A[j][j]+v[j]*A[j][sig[j]]-x[j]-y[j]))ok=false;}
  if(pu==1||pv==1)ok=false;
  if(ok){counts[4]++;printf("SOLUTION p=%d z=%d t=",P,Z);for(int a:t)printf("%d,",a);printf(" u=");for(int a:u)printf("%d,",a);printf("\n");}
 }
}
for(int r=1;r<8;r++)printf("ROW %d: %ld\n",r,rowsurvive[r]);printf("COUNTS p=%d z=%d total=%ld pivot=%ld reduced=%ld offsupport=%ld solution=%ld\n",P,Z,counts[0],counts[1],counts[2],counts[3],counts[4]);
}
