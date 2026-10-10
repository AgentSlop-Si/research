// Exact projective full-minor certificate for five complex-gauged Hamiltonian Green terms.
// Tests seven selected 2x2 minors of an ordered 3x4 window; homogeneous degree 3,
// 5 variables => 35 columns. Full modular rank 35 excludes ALL complex Green
// coefficients and internal nonzero diagonal gauges/permutations for that window.
#include <bits/stdc++.h>
using namespace std;
using u32=uint32_t;using u64=uint64_t;
#ifndef MODULUS
#define MODULUS 998244353u
#endif
constexpr u32 MOD=MODULUS;
constexpr int Q=5, MAXN=16, DEGDIM=35, QUAD_DIM=15, KEYSPACE=1024;
u32 T[MAXN][MAXN],G[Q][MAXN][MAXN];
int N=8, idx2[KEYSPACE], idx3[KEYSPACE], ex2[QUAD_DIM][Q], ex3[DEGDIM][Q];
vector<array<uint8_t,3>> rowtriples;
vector<array<uint8_t,4>> colquads;
inline u32 mul(u32 a,u32 b){return (u64)a*b%MOD;}
inline u32 sub(u32 a,u32 b){return a>=b?a-b:a+MOD-b;}
u32 powmod(u32 a,u32 e){u32 r=1;while(e){if(e&1)r=mul(r,a);a=mul(a,a);e>>=1;}return r;}
inline int key(int a,int b,int c,int d,int e){return ((((a*4+b)*4+c)*4+d)*4+e);}
void prepare(){
 fill(idx2,idx2+KEYSPACE,-1);fill(idx3,idx3+KEYSPACE,-1);
 int z=0;
 for(int a=0;a<=2;a++)for(int b=0;b<=2-a;b++)for(int c=0;c<=2-a-b;c++)for(int d=0;d<=2-a-b-c;d++){
  int e=2-a-b-c-d;
  int v[5]={a,b,c,d,e};copy(v,v+Q,ex2[z]);idx2[key(a,b,c,d,e)]=z++;
 }assert(z==QUAD_DIM);
 z=0;
 for(int a=0;a<=3;a++)for(int b=0;b<=3-a;b++)for(int c=0;c<=3-a-b;c++)for(int d=0;d<=3-a-b-c;d++){
  int e=3-a-b-c-d;
  int v[5]={a,b,c,d,e};copy(v,v+Q,ex3[z]);idx3[key(a,b,c,d,e)]=z++;
 }assert(z==DEGDIM);
 for(int a=0;a<N;a++)for(int b=0;b<N;b++)if(b!=a)for(int c=0;c<N;c++)if(c!=a&&c!=b)
  rowtriples.push_back({(uint8_t)a,(uint8_t)b,(uint8_t)c});
 for(int a=0;a<N;a++)for(int b=0;b<N;b++)if(b!=a)for(int c=0;c<N;c++)if(c!=a&&c!=b)
  for(int d=0;d<N;d++)if(d!=a&&d!=b&&d!=c)
    colquads.push_back({(uint8_t)a,(uint8_t)b,(uint8_t)c,(uint8_t)d});
}
void coeff(int row,int col,u32 v[Q]){for(int k=0;k<Q;k++)v[k]=G[k][row][col];}
void product(const u32 v[Q],const u32 w[Q],u32 out[QUAD_DIM]){
 fill(out,out+QUAD_DIM,0);
 for(int a=0;a<Q;a++)for(int b=0;b<Q;b++){
  int e[Q]={0,0,0,0,0};e[a]++;e[b]++;
  int k=idx2[key(e[0],e[1],e[2],e[3],e[4])];
  u32 c=mul(v[a],w[b]);out[k]+=c;if(out[k]>=MOD)out[k]-=MOD;
 }
}
struct RankResult {int rank;array<uint8_t,DEGDIM> witnesses;};
RankResult check(const array<uint8_t,3>& rs,const array<uint8_t,4>& cs){
 u32 basis[DEGDIM][DEGDIM]={{0}}, inv[DEGDIM]={0};
 bool occupied[DEGDIM]={0};
 array<uint8_t,DEGDIM> chosen{};int rank=0,rowindex=0;
 const int selected_pairs[7][4]={
    {0,1,0,1}, {0,1,0,2}, {0,1,0,3}, {0,2,1,2},
    {0,2,2,3}, {1,2,0,1}, {1,2,0,3}
 };
 for(int qidx=0;qidx<7;qidx++){
  const int i=selected_pairs[qidx][0],ii=selected_pairs[qidx][1];
  const int j=selected_pairs[qidx][2],jj=selected_pairs[qidx][3];
  const u32 a=mul(T[i][jj],T[ii][j]),b=mul(T[i][j],T[ii][jj]);
  u32 v1[Q],v2[Q],v3[Q],v4[Q],p1[QUAD_DIM],p2[QUAD_DIM],quad[QUAD_DIM];
  coeff(rs[i],cs[j],v1);coeff(rs[ii],cs[jj],v2);
  coeff(rs[i],cs[jj],v3);coeff(rs[ii],cs[j],v4);
  product(v1,v2,p1);product(v3,v4,p2);
  for(int k=0;k<QUAD_DIM;k++)quad[k]=sub(mul(a,p1[k]),mul(b,p2[k]));
  for(int var=0;var<Q;var++){
   u32 r[DEGDIM]={0};
   for(int k=0;k<QUAD_DIM;k++){
     int e[Q];copy(ex2[k],ex2[k]+Q,e);e[var]++;
     int p=idx3[key(e[0],e[1],e[2],e[3],e[4])];r[p]=quad[k];
   }
   for(int p=0;p<DEGDIM;p++)if(occupied[p] && r[p]){
     u32 factor=mul(r[p],inv[p]);
     for(int c=p;c<DEGDIM;c++)r[c]=sub(r[c],mul(factor,basis[p][c]));
   }
   int pivot=0;while(pivot<DEGDIM&&!r[pivot])pivot++;
   if(pivot<DEGDIM){
     assert(!occupied[pivot]);occupied[pivot]=true;
     memcpy(basis[pivot],r,sizeof(r));inv[pivot]=powmod(r[pivot],MOD-2);
     chosen[rank]=(uint8_t)rowindex;rank++;
   }
   rowindex++;
   if(rank==DEGDIM)return {rank,chosen};
  }
 }
 return {rank,chosen};
}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: rectangular_audit matrices.bin ranks.bin [begin] [end] [witnesses.bin]\n";return 2;}
 ifstream in(argv[1],ios::binary);u32 mod=0,n=0;
 in.read((char*)&mod,4);in.read((char*)&n,4);
 if(!in||mod!=MOD||(n!=4&&n!=8&&n!=16)){cerr<<"invalid input header\n";return 2;}
 N=n;
 for(int i=0;i<N;i++)for(int j=0;j<N;j++)in.read((char*)&T[i][j],4);
 for(int k=0;k<Q;k++)for(int i=0;i<N;i++)for(int j=0;j<N;j++)in.read((char*)&G[k][i][j],4);
 if(!in){cerr<<"truncated input\n";return 2;}
 prepare();
 const size_t size=rowtriples.size()*colquads.size();
 if(argc>=5 && string(argv[3])=="--indices"){
    ifstream ids(argv[4],ios::binary);
    ofstream out(argv[2],ios::binary);
    if(!ids||!out){cerr<<"cannot open sample input/output\n";return 2;}
    unsigned long long hist[DEGDIM+1]={0};
    unsigned long long total=0;
    u64 id=0;
    while(ids.read((char*)&id,sizeof(id))){
        if(id>=size){cerr<<"sample index out of range\n";return 2;}
        auto result=check(rowtriples[id/colquads.size()],colquads[id%colquads.size()]);
        hist[result.rank]++;out.put((char)result.rank);total++;
    }
    if(!ids.eof()){cerr<<"truncated sample indices\n";return 2;}
    cout<<"N="<<N<<" indexed samples="<<total<<" ranks:";
    for(int k=0;k<=DEGDIM;k++)if(hist[k])cout<<" "<<k<<":"<<hist[k];
    cout<<"\n";
    return 0;
 }
 const size_t begin=(argc>=4?stoull(argv[3]):0),end=(argc>=5?stoull(argv[4]):size);
 if(begin>end||end>size){cerr<<"invalid audit range, max "<<size<<"\n";return 2;}
 ofstream out(argv[2],ios::binary);if(!out){cerr<<"cannot open ranks output\n";return 2;}
 ofstream wit; if(argc>=6){wit.open(argv[5],ios::binary);if(!wit){cerr<<"cannot open witness output\n";return 2;}}
 unsigned long long hist[DEGDIM+1]={0};
 for(size_t k=begin;k<end;k++){
   auto res=check(rowtriples[k/colquads.size()],colquads[k%colquads.size()]);
   hist[res.rank]++;out.put((char)(res.rank));
   if(wit)wit.write((char*)res.witnesses.data(),DEGDIM);
 }
 out.close();if(wit)wit.close();
 cout<<"N="<<N<<" begin="<<begin<<" end="<<end<<" count="<<(end-begin)<<" ranks:";
 for(int r=0;r<=DEGDIM;r++)if(hist[r])cout<<" "<<r<<":"<<hist[r];
 cout<<"\n";
 return 0;
}
