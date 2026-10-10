// Phase 30: independent native exact finite-field Macaulay-rank verifier.
// Reads target + four Green matrices written by Python; enumerates every
// ordered 3-row/3-col mapping at N=8; exact modulo 998244353 only.
// A full degree-three row span means NO nonzero projective pencil vector
// solves the selected 3x3 scaled rank-one equations over characteristic zero.
#include <bits/stdc++.h>
using namespace std;
using u32=uint32_t; using u64=uint64_t;
#ifndef PHASE30_MOD
#define PHASE30_MOD 998244353
#endif
const u32 MOD=PHASE30_MOD;
u32 target[16][16], G[4][16][16];
int N=8;
int idx2[256],idx3[256], exponent2[10][4], exponent3[20][4];
vector<array<int,3>> triples;
inline u32 mul(u32 a,u32 b){return (u64)a*b%MOD;}
inline u32 sub(u32 a,u32 b){return a>=b?a-b:a+MOD-b;}
u32 powmod(u32 a,u32 e){u32 z=1;while(e){if(e&1)z=mul(z,a);a=mul(a,a);e>>=1;}return z;}
inline int key(int a,int b,int c,int d){return ((a*4+b)*4+c)*4+d;}
void prepare(){
 fill(idx2,idx2+256,-1);fill(idx3,idx3+256,-1);
 int k=0;
 for(int a=0;a<=2;a++)for(int b=0;b<=2-a;b++)for(int c=0;c<=2-a-b;c++){
   int d=2-a-b-c; exponent2[k][0]=a;exponent2[k][1]=b;exponent2[k][2]=c;exponent2[k][3]=d;idx2[key(a,b,c,d)]=k++;}
 assert(k==10);k=0;
 for(int a=0;a<=3;a++)for(int b=0;b<=3-a;b++)for(int c=0;c<=3-a-b;c++){
   int d=3-a-b-c; exponent3[k][0]=a;exponent3[k][1]=b;exponent3[k][2]=c;exponent3[k][3]=d;idx3[key(a,b,c,d)]=k++;}
 assert(k==20);
 for(int i=0;i<N;i++)for(int j=0;j<N;j++)if(i!=j)for(int k=0;k<N;k++)if(k!=i && k!=j)triples.push_back({i,j,k});
 assert(triples.size()==(size_t)N*(N-1)*(N-2));
}
void quad(const u32 v[4], const u32 w[4],u32 q[10]){
 fill(q,q+10,0);
 for(int a=0;a<4;a++)for(int b=0;b<4;b++){
 int e[4]={0,0,0,0};e[a]++;e[b]++;
 int z=idx2[key(e[0],e[1],e[2],e[3])];
 u32 t=mul(v[a],w[b]);q[z]+=t;if(q[z]>=MOD)q[z]-=MOD;
 }
}
inline void coeff(int row,int col,u32 v[4]){
  v[0]=G[1][row][col];v[1]=G[2][row][col];
  v[2]=G[3][row][col];v[3]=G[0][row][col];
}
struct Result {u32 rank,det;array<uint8_t,20> selected;};
Result check(const array<int,3>& rs,const array<int,3>& cs){
 u32 basis[20][20]={{0}}, inv[20]={0};
 bool occupied[20]={0};
 u32 det=1;
 array<uint8_t,20> selected{};
 int rank=0, rowIndex=0;
 for(int i=0;i<3;i++)for(int ip=i+1;ip<3;ip++)
 for(int j=0;j<3;j++)for(int jp=j+1;jp<3;jp++){
   u32 a=mul(target[i][jp],target[ip][j]);
   u32 b=mul(target[i][j],target[ip][jp]);
   u32 v1[4],v2[4],v3[4],v4[4],p1[10],p2[10],q[10];
   coeff(rs[i],cs[j],v1);coeff(rs[ip],cs[jp],v2);
   coeff(rs[i],cs[jp],v3);coeff(rs[ip],cs[j],v4);
   quad(v1,v2,p1);quad(v3,v4,p2);
   for(int k=0;k<10;k++) q[k]=sub(mul(a,p1[k]),mul(b,p2[k]));
   // multiply by degree-1 monomials ordered reverse index (3,2,1,0)
   for(int var=3;var>=0;var--){
     u32 r[20]={0};
     for(int k=0;k<10;k++){
       int e[4]={exponent2[k][0],exponent2[k][1],exponent2[k][2],exponent2[k][3]};e[var]++;
       r[idx3[key(e[0],e[1],e[2],e[3])]]=q[k];
     }
     // full reduction against all existing pivots, in coordinate order
     for(int p=0;p<20;p++)if(occupied[p] && r[p]){
       u32 factor=mul(r[p],inv[p]);
       for(int c=p;c<20;c++)r[c]=sub(r[c],mul(factor,basis[p][c]));
     }
     int pivot=0;while(pivot<20 && !r[pivot])pivot++;
     if(pivot<20){
       assert(!occupied[pivot]);occupied[pivot]=true;
       memcpy(basis[pivot],r,sizeof(r));inv[pivot]=powmod(r[pivot],MOD-2);
       det=mul(det,r[pivot]);selected[rank]=rowIndex;rank++;
     }
     rowIndex++;
     if(rank==20){
        // det of selected ORIGINAL rows at *ordered* columns = product
        // of elimination pivots times sign of pivot-column sequence.
        // The selected rows in insertion order give a pivot permutation.
        // We need to record pivot sequence separately for parity (below).
        // No determinant is saved here; we only certify nonzero rank.
        return {(u32)rank,0,selected};
     }
   }
 }
 return {(u32)rank,0,selected};
}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: audit matrix.bin ranks.bin [begin] [end]"<<endl;return 2;}
 ifstream in(argv[1],ios::binary);if(!in){cerr<<"missing matrix";return 2;}
 u32 prime=0,n=0;in.read((char*)&prime,4);in.read((char*)&n,4);
 if(prime!=MOD||(n!=8&&n!=16)){cerr<<"header error\n";return 2;}
 N=(int)n;
 for(int i=0;i<N;i++)for(int j=0;j<N;j++)in.read((char*)&target[i][j],4);
 for(int g=0;g<4;g++)for(int i=0;i<N;i++)for(int j=0;j<N;j++)in.read((char*)&G[g][i][j],4);
 if(!in){cerr<<"truncated matrix input";return 2;}
 prepare();
 size_t all=triples.size()*triples.size();
 size_t begin=(argc>3?stoull(argv[3]):0);
 size_t end=(argc>4?stoull(argv[4]):all);
 if(begin>end||end>all){cerr<<"invalid range";return 2;}
 ofstream out(argv[2],ios::binary);if(!out){cerr<<"cannot create output";return 2;}
 vector<unsigned long long> hist(21,0);
 for(size_t i=begin;i<end;i++){
   Result r=check(triples[i/triples.size()],triples[i%triples.size()]);
   hist[r.rank]++;
   out.put((char)r.rank);
 }
 out.close();
 cout<<"n="<<N<<" begin="<<begin<<" end="<<end<<" checked="<<(end-begin)<<" ranks:";
 for(int k=0;k<=20;k++)if(hist[k])cout<<" "<<k<<":"<<hist[k];
 cout<<"\n";
 return 0;
}
