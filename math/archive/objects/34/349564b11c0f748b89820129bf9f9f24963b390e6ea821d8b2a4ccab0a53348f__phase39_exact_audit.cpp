// Phase 39: exact two-parameter, two-mask Green-versus-DFT certificate.
// Read N p and T,G0,G1,G2 dense matrices (each N rows of N integers).
// Test ALL ordered 2-row/4-column mappings if --limit 0; else first limit.
// Optional --kind cubic (4 quadratic minors x 3 variables -> rank 10),
// or quartic (3 quadratic minors x 6 quadratics -> rank 15).
// Integer modular arithmetic only; no floating point.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using u64=uint64_t;
static u64 P;
inline u64 add(u64 a,u64 b){u64 s=a+b;return s>=P?s-P:s;}
inline u64 sub(u64 a,u64 b){return a>=b?a-b:a+P-b;}
inline u64 mul(u64 a,u64 b){return (a*b)%P;}
u64 power(u64 a,u64 exp){u64 v=1;while(exp){if(exp&1)v=mul(v,a);a=mul(a,a);exp>>=1;}return v;}
struct Instance{
 size_t n;
 std::array<std::vector<u64>,4> mats;
 inline u64 val(int m,size_t i,size_t j)const{return mats[m][i*n+j];}
 std::array<u64,6> quad(int r0,int r1,const std::array<int,4>& c,int a,int b) const {
   // T[0,a]*T[1,b]*B[r1,c[a]]*B[r0,c[b]]
   // - T[0,b]*T[1,a]*B[r1,c[b]]*B[r0,c[a]]
   std::array<u64,3> x,y,z,w;
   for(int s=0;s<3;s++){
     x[s]=val(1+s,r1,c[a]);y[s]=val(1+s,r0,c[b]);
     z[s]=val(1+s,r1,c[b]);w[s]=val(1+s,r0,c[a]);
   }
   const u64 L=mul(val(0,0,a),val(0,1,b));
   const u64 R=mul(val(0,0,b),val(0,1,a));
   auto qmul=[](const std::array<u64,3>& u,const std::array<u64,3>& v){
     return std::array<u64,6>{mul(u[0],v[0]),add(mul(u[0],v[1]),mul(u[1],v[0])),
       add(mul(u[0],v[2]),mul(u[2],v[0])),mul(u[1],v[1]),
       add(mul(u[1],v[2]),mul(u[2],v[1])),mul(u[2],v[2])};};
   const auto X=qmul(x,y),Y=qmul(z,w);
   std::array<u64,6> out{};
   for(int s=0;s<6;s++)out[s]=sub(mul(L,X[s]),mul(R,Y[s]));
   return out;
 }
};

static constexpr int CUBIC_MON[3][6]={{0,1,2,3,4,5},{1,3,4,6,7,8},{2,4,5,7,8,9}};
// Degree-four indexing is generated programmatically below.
int quartic_index[6][6];
void make_quartic_index(){
 const int quad[6][3]={{2,0,0},{1,1,0},{1,0,1},{0,2,0},{0,1,1},{0,0,2}};
 int out[15][3],idx=0;
 for(int i=4;i>=0;i--)for(int j=4-i;j>=0;j--){out[idx][0]=i;out[idx][1]=j;out[idx][2]=4-i-j;idx++;}
 if(idx!=15){std::abort();}
 for(int a=0;a<6;a++)for(int b=0;b<6;b++){
   int x0=quad[a][0]+quad[b][0],x1=quad[a][1]+quad[b][1];
   int pos=0;while(pos<15 && (out[pos][0]!=x0 || out[pos][1]!=x1))pos++;
   if(pos==15)std::abort();
   quartic_index[a][b]=pos;
 }
}

template<std::size_t M,std::size_t K>
int rank(std::array<std::array<u64,K>,M>& mat){
 int r=0;
 for(int col=0;col<(int)K;col++){
   int pivot=r;
   while(pivot<(int)M && !mat[pivot][col])pivot++;
   if(pivot==M)continue;
   if(pivot!=r)std::swap(mat[pivot],mat[r]);
   const u64 inverse=power(mat[r][col],P-2);
   for(int row=r+1;row<(int)M;row++){
     if(!mat[row][col])continue;
     u64 f=mul(mat[row][col],inverse);
     for(int k=col+1;k<(int)K;k++)mat[row][k]=sub(mat[row][k],mul(f,mat[r][k]));
     mat[row][col]=0;
   }
   r++;
   if(r==K)break;
 }
 return r;
}

int cubic_rank(const Instance& inst,int r0,int r1,const std::array<int,4>& cols){
 const int edges[4][2]={{0,1},{0,2},{0,3},{1,2}};
 std::array<std::array<u64,10>,12> mat{};
 for(int e=0;e<4;e++){
   const auto f=inst.quad(r0,r1,cols,edges[e][0],edges[e][1]);
   for(int var=0;var<3;var++)for(int j=0;j<6;j++){
     mat[e*3+var][CUBIC_MON[var][j]]=f[j];
   }
 }
 return rank(mat);
}
int quartic_rank(const Instance& inst,int r0,int r1,const std::array<int,4>& cols){
 const int edges[3][2]={{0,1},{0,2},{1,3}};
 std::array<std::array<u64,15>,18> mat{};
 for(int e=0;e<3;e++){
   const auto f=inst.quad(r0,r1,cols,edges[e][0],edges[e][1]);
   for(int var=0;var<6;var++)for(int j=0;j<6;j++){
     mat[e*6+var][quartic_index[var][j]]=f[j];
   }
 }
 return rank(mat);
}

int main(int argc,char**argv){
 if(argc<2){std::cerr<<"Usage: "<<argv[0]<<" instance.txt [limit=0] [cubic|quartic]\n";return 2;}
 std::ifstream in(argv[1]);if(!in){std::cerr<<"Missing instance\n";return 2;}
 Instance a;in>>a.n>>P; if(a.n<4 || P<=a.n){std::cerr<<"Invalid N/p\n";return 2;}
 for(auto& m:a.mats){m.resize(a.n*a.n);for(auto&v:m){in>>v;if(!in || v>=P){std::cerr<<"Bad matrix data\n";return 2;}}}
 make_quartic_index();
 const u64 limit=argc>2?std::strtoull(argv[2],nullptr,10):0;
 const u64 random_count=argc>4?std::strtoull(argv[4],nullptr,10):0;
 const std::string kind=argc>3?argv[3]:"cubic";
 if(kind!="cubic" && kind!="quartic"){std::cerr<<"Invalid kind\n";return 2;}
 uint64_t checked=0,fail=0,hash=1469598103934665603ULL;
 int minrank=100;std::array<int,6> firstbad{};
 auto start=std::chrono::steady_clock::now();
 const int n=(int)a.n;
 if(random_count){
  u64 rng=0x9e3779b97f4a7c15ULL + P + 13*a.n;
  auto next_rand=[&](){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;};
  for(u64 trial=0;trial<random_count;trial++){
    int r0=next_rand()%n,r1=next_rand()%n;
    while(r1==r0)r1=next_rand()%n;
    std::array<int,4> cols{};
    for(int c=0;c<4;c++){
      cols[c]=next_rand()%n;
      bool repeat;
      do{
        repeat=false;
        for(int prev=0;prev<c;prev++)if(cols[c]==cols[prev])repeat=true;
        if(repeat)cols[c]=next_rand()%n;
      }while(repeat);
    }
    int rr=kind=="cubic"?cubic_rank(a,r0,r1,cols):quartic_rank(a,r0,r1,cols);
    int full=kind=="cubic"?10:15;
    if(rr<minrank)minrank=rr;
    if(rr!=full){if(fail==0)firstbad={r0,r1,cols[0],cols[1],cols[2],cols[3]};fail++;}
    checked++;hash=(hash^((u64)rr+13*checked))*1099511628211ULL;
  }
  goto done;
 }
 for(int r0=0;r0<n;r0++)for(int r1=0;r1<n;r1++)if(r0!=r1){
 for(int c0=0;c0<n;c0++)for(int c1=0;c1<n;c1++)if(c0!=c1){
 for(int c2=0;c2<n;c2++)if(c2!=c0 && c2!=c1){
 for(int c3=0;c3<n;c3++)if(c3!=c0 && c3!=c1 && c3!=c2){
  std::array<int,4> col{c0,c1,c2,c3};
  int rr=(kind=="cubic")?cubic_rank(a,r0,r1,col):quartic_rank(a,r0,r1,col);
  int full=(kind=="cubic")?10:15;
  if(rr<minrank)minrank=rr;
  if(rr!=full){if(fail==0)firstbad={r0,r1,c0,c1,c2,c3};fail++;}
  checked++;hash=(hash^((u64)rr+13*checked))*1099511628211ULL;
  if(limit && checked>=limit)goto done;
 }}}}
 done:
 auto elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"N\":"<<n<<",\"prime\":"<<P<<",\"kind\":\""<<kind
  <<"\",\"checked\":"<<checked<<",\"deficient\":"<<fail
  <<",\"minimum_rank\":"<<minrank<<",\"first_bad\":[";
 for(int j=0;j<6;j++)std::cout<<(j?",":"")<<firstbad[j];
 std::cout<<"],\"rolling_hash\":\""<<std::hex<<hash<<std::dec<<"\",\"seconds\":"<<elapsed<<"}\n";
 return fail?1:0;
}
