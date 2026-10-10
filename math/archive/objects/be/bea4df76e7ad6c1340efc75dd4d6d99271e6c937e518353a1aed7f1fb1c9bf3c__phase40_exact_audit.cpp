// Phase 40 projective five-cycle exact audit.
// Read N p; then dense T,B0,B1,B2,B3 (five NxN matrices).
// For each ordered 2 middle rows and 5 distinct middle columns,
// calculate 5 overlapping 2x2 Fourier-equivalence quadrics;
// multiply each by 4 variables, obtain 20x20 homogeneous cubic certificate.
// Full rank excludes ALL nonzero complex projective couplings at that mapping
// after characteristic-zero lifting. No numerical floating-point arithmetic.
#include <array>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using u64=uint64_t;
static u64 P;
inline u64 add(u64 a,u64 b){auto s=a+b;return s>=P?s-P:s;}
inline u64 sub(u64 a,u64 b){return a>=b?a-b:a+P-b;}
inline u64 mul(u64 a,u64 b){return a*b%P;}
u64 power(u64 a,u64 exp){u64 v=1;while(exp){if(exp&1)v=mul(v,a);a=mul(a,a);exp>>=1;}return v;}
static constexpr int MON2[10][4]={{2,0,0,0},{1,1,0,0},{1,0,1,0},{1,0,0,1},
                                  {0,2,0,0},{0,1,1,0},{0,1,0,1},
                                  {0,0,2,0},{0,0,1,1},{0,0,0,2}};
int CUBIC_INDEX[4][10];
void init_index(){
 std::vector<std::array<int,4>> mons;
 for(int x=3;x>=0;x--)for(int y=3-x;y>=0;y--)for(int z=3-x-y;z>=0;z--){
  mons.push_back({x,y,z,3-x-y-z});
 }
 if(mons.size()!=20)std::abort();
 for(int v=0;v<4;v++)for(int t=0;t<10;t++){
  std::array<int,4> e{};
  for(int i=0;i<4;i++)e[i]=MON2[t][i]+(i==v?1:0);
  auto it=std::find(mons.begin(),mons.end(),e);
  if(it==mons.end())std::abort();
  CUBIC_INDEX[v][t]=(int)(it-mons.begin());
 }
}
struct Instance{
 int n=0;
 std::array<std::vector<u64>,5> M;
 inline u64 at(int m,int i,int j) const {return M[m][(size_t)i*n+j];}
 inline std::array<u64,10> quad(int r0,int r1,const std::array<int,5>&c,int a,int b) const{
  const u64 L=mul(at(0,0,a),at(0,1,b));
  const u64 R=mul(at(0,0,b),at(0,1,a));
  std::array<u64,10> output{};
  for(int i=0;i<4;i++)for(int j=i;j<4;j++){
   int id=0;
   if(i==0){id=j;} // x0^2, x0*x1, x0*x2, x0*x3
   else if(i==1){id=4+(j-1);} // x1^2 x1*x2 x1*x3
   else if(i==2){id=7+(j-2);} // x2^2 x2*x3
   else id=9;
   const u64 u=at(i+1,r1,c[a]),v=at(j+1,r0,c[b]);
   const u64 u2=at(j+1,r1,c[a]),v2=at(i+1,r0,c[b]);
   const u64 w=at(i+1,r1,c[b]),z=at(j+1,r0,c[a]);
   const u64 w2=at(j+1,r1,c[b]),z2=at(i+1,r0,c[a]);
   u64 left=mul(u,v),right=mul(w,z);
   if(i!=j){left=add(left,mul(u2,v2));right=add(right,mul(w2,z2));}
   output[id]=sub(mul(L,left),mul(R,right));
  }
  return output;
 }
};
template<std::size_t R> int rank20(std::array<std::array<u64,20>,R>&m){
 int row=0;
 for(int c=0;c<20;c++){
  int piv=row;while(piv<(int)R && !m[piv][c])piv++;
  if(piv==(int)R)continue;
  if(piv!=row)std::swap(m[piv],m[row]);
  u64 inv=power(m[row][c],P-2);
  for(int r=row+1;r<(int)R;r++){
   if(!m[r][c])continue;
   u64 f=mul(m[r][c],inv);
   for(int k=c+1;k<20;k++)m[r][k]=sub(m[r][k],mul(f,m[row][k]));
   m[r][c]=0;
  }
  row++;
  if(row==20)break;
 }
 return row;
}
int cert_rank(const Instance& a,int r0,int r1,const std::array<int,5>&cs, int cycle_choice=0){
 static constexpr int graphs[2][5][2]={
  {{0,1},{1,2},{2,3},{3,4},{4,0}},
  {{0,1},{1,2},{2,4},{4,3},{3,0}}
 };
 const auto& edges=graphs[cycle_choice];
 std::array<std::array<u64,20>,24> mat{};
 for(int e=0;e<5;e++){
  auto q=a.quad(r0,r1,cs,edges[e][0],edges[e][1]);
  for(int v=0;v<4;v++)for(int j=0;j<10;j++){
   mat[4*e+v][CUBIC_INDEX[v][j]]=q[j];
  }
 }
 // Exactly five quadrics times four linears: square 20x20 Macaulay matrix.
 std::array<std::array<u64,20>,20> shortmat{};
 std::copy_n(mat.begin(),20,shortmat.begin());
 return rank20(shortmat);
}
int main(int argc,char**argv){
 if(argc<2){std::cerr<<"Usage: phase40_exact_audit instance.txt [limit=0] [random_trials=0]\n";return 2;}
 std::ifstream in(argv[1]);Instance A;in>>A.n>>P;
 if(!in||A.n<5||P<100000){std::cerr<<"Bad header\n";return 2;}
 for(auto &m:A.M){m.resize((size_t)A.n*A.n);for(auto &x:m){in>>x;if(!in||x>=P){std::cerr<<"Bad matrix\n";return 2;}}}
 init_index();
 const u64 limit=argc>2?std::strtoull(argv[2],nullptr,10):0;
 const u64 trials=argc>3?std::strtoull(argv[3],nullptr,10):0;
 const bool use_rescue=argc>4?std::string(argv[4])=="rescue":false;
 u64 checked=0,failed=0,rescued=0,hash=1469598103934665603ULL;
 int minrank=20;std::array<int,7> bad{};auto start=std::chrono::steady_clock::now();
 auto check=[&](int r0,int r1,const std::array<int,5>&c){
  int rank=cert_rank(A,r0,r1,c);
  if(rank<20 && use_rescue){
   int alt=cert_rank(A,r0,r1,c,1);
   if(alt==20)rescued++;
   rank=alt;
  }
  minrank=std::min(minrank,rank);
  if(rank<20){if(failed==0)bad={r0,r1,c[0],c[1],c[2],c[3],c[4]};failed++;}
  checked++;hash=(hash^((u64)rank+checked*13))*1099511628211ULL;
 };
 const int n=A.n;
 if(trials){
  u64 x=0x9e3779b97f4a7c15ULL+P+17*n;
  auto next=[&](){x^=x<<13;x^=x>>7;x^=x<<17;return x;};
  for(u64 t=0;t<trials;t++){
   int r0=next()%n,r1=next()%n;while(r1==r0)r1=next()%n;
   std::array<int,5>c{};
   for(int i=0;i<5;i++){
    bool dup=true;while(dup){c[i]=next()%n;dup=false;for(int j=0;j<i;j++)if(c[j]==c[i])dup=true;}
   }
   check(r0,r1,c);
  }
 }else{
  for(int r0=0;r0<n;r0++)for(int r1=0;r1<n;r1++)if(r0!=r1)
   for(int c0=0;c0<n;c0++)for(int c1=0;c1<n;c1++)if(c1!=c0)
    for(int c2=0;c2<n;c2++)if(c2!=c0&&c2!=c1)
     for(int c3=0;c3<n;c3++)if(c3!=c0&&c3!=c1&&c3!=c2)
      for(int c4=0;c4<n;c4++)if(c4!=c0&&c4!=c1&&c4!=c2&&c4!=c3){
       check(r0,r1,{c0,c1,c2,c3,c4});
       if(limit && checked>=limit)goto done;
      }
 }
 done:
 const double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"N\":"<<n<<",\"prime\":"<<P<<",\"checked\":"<<checked
          <<",\"deficient\":"<<failed<<",\"rescued\":"<<rescued<<",\"minrank\":"<<minrank
          <<",\"bad\":[";
 for(int i=0;i<7;i++)std::cout<<(i?",":"")<<bad[i];
 std::cout<<"],\"rolling_hash\":\""<<std::hex<<hash<<std::dec<<"\",\"seconds\":"<<sec<<"}\n";
 return failed?1:0;
}
