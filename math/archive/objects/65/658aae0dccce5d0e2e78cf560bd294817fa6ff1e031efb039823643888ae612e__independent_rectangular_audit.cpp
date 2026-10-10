// Independently authored seven-minor cubic-rank audit. Reads matrix data only.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
#include <stdexcept>
#include <omp.h>
using U=uint32_t; using W=uint64_t;
constexpr U P=998244353;
U add(U a,U b){U z=a+b;return z>=P?z-P:z;}
U sub(U a,U b){return a>=b?a-b:a+P-b;}
U mul(U a,U b){return W(a)*b%P;}
U power(U a,U n){U z=1;for(;n;n>>=1,a=mul(a,a))if(n&1)z=mul(z,a);return z;}
struct Input {int n;U T[16][16]{};U G[5][16][16]{};};
struct Basis {
 std::vector<std::array<int,2>> pair;
 int triple[5][5][5]{};
 Basis(){
  for(int i=0;i<5;i++)for(int j=i;j<5;j++)pair.push_back({i,j});
  int z=0;
  for(int i=0;i<5;i++)for(int j=i;j<5;j++)for(int k=j;k<5;k++){
   std::array<int,3> p{i,j,k};do{triple[p[0]][p[1]][p[2]]=z;}while(std::next_permutation(p.begin(),p.end()));++z;
  }
  if(z!=35||pair.size()!=15)throw std::runtime_error("basis size");
 }
};
int matrix_rank(U A[35][35]){
 int row=0;
 for(int col=0;col<35&&row<35;col++){
  int pivot=row;while(pivot<35&&!A[pivot][col])++pivot;
  if(pivot==35)continue;
  if(pivot!=row)for(int j=col;j<35;j++)std::swap(A[pivot][j],A[row][j]);
  U inverse=power(A[row][col],P-2);
  for(int j=col+1;j<35;j++)A[row][j]=mul(A[row][j],inverse);
  A[row][col]=1;
  for(int i=row+1;i<35;i++)if(A[i][col]){
   U factor=A[i][col];A[i][col]=0;
   for(int j=col+1;j<35;j++)A[i][j]=sub(A[i][j],mul(factor,A[row][j]));
  }
  ++row;
 }
 return row;
}
int certificate(const Input& X,const Basis& basis,const std::array<int,3>& rows,const std::array<int,4>& cols){
 constexpr int minors[7][4]={{0,1,0,1},{0,1,0,2},{0,1,0,3},{0,2,1,2},{0,2,2,3},{1,2,0,1},{1,2,0,3}};
 U M[35][35]{};int line=0;
 for(auto& e:minors){
  int i=e[0],h=e[1],j=e[2],l=e[3];
  U alpha=mul(X.T[i][l],X.T[h][j]),beta=mul(X.T[i][j],X.T[h][l]);
  U quadratic[15]{};
  for(int z=0;z<15;z++){
   int u=basis.pair[z][0],v=basis.pair[z][1];
   U positive=mul(X.G[u][rows[i]][cols[j]],X.G[v][rows[h]][cols[l]]);
   U negative=mul(X.G[u][rows[i]][cols[l]],X.G[v][rows[h]][cols[j]]);
   if(u!=v){
    positive=add(positive,mul(X.G[v][rows[i]][cols[j]],X.G[u][rows[h]][cols[l]]));
    negative=add(negative,mul(X.G[v][rows[i]][cols[l]],X.G[u][rows[h]][cols[j]]));
   }
   quadratic[z]=sub(mul(alpha,positive),mul(beta,negative));
  }
  for(int variable=0;variable<5;variable++,line++)
   for(int z=0;z<15;z++)M[line][basis.triple[basis.pair[z][0]][basis.pair[z][1]][variable]]=quadratic[z];
 }
 return matrix_rank(M);
}
int main(int argc,char**argv){
 if(argc<3){std::cerr<<"input output [indices_file | first_count]\n";return 2;}
 Input X;U p,n;std::ifstream f(argv[1],std::ios::binary);f.read((char*)&p,4);f.read((char*)&n,4);
 if(!f||p!=P||(n!=4&&n!=8&&n!=16))throw std::runtime_error("header");X.n=n;
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)f.read((char*)&X.T[i][j],4);
 for(int k=0;k<5;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)f.read((char*)&X.G[k][i][j],4);
 if(!f)throw std::runtime_error("truncated matrices");char extra;if(f.read(&extra,1))throw std::runtime_error("trailing matrices");
 std::vector<std::array<int,3>> rows;std::vector<std::array<int,4>> cols;
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j)for(int k=0;k<n;k++)if(k!=i&&k!=j)rows.push_back({i,j,k});
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j)for(int k=0;k<n;k++)if(k!=i&&k!=j)for(int l=0;l<n;l++)if(l!=i&&l!=j&&l!=k)cols.push_back({i,j,k,l});
 W total=W(rows.size())*cols.size();std::vector<W> indices;
 if(argc>=4&&std::string(argv[3]).find_first_not_of("0123456789")!=std::string::npos){
  std::ifstream in(argv[3],std::ios::binary);W id;while(in.read((char*)&id,8)){if(id>=total)throw std::runtime_error("case index");indices.push_back(id);}if(!in.eof())throw std::runtime_error("indices");
 }else{W count=argc>=4?std::stoull(argv[3]):total;if(count>total)throw std::runtime_error("count");for(W k=0;k<count;k++)indices.push_back(k);}
 Basis basis;std::vector<unsigned char> output(indices.size());double start=omp_get_wtime();
 #pragma omp parallel for schedule(static)
 for(size_t k=0;k<indices.size();k++){
  W id=indices[k];output[k]=certificate(X,basis,rows[id/cols.size()],cols[id%cols.size()]);
 }
 W hist[36]{};for(auto r:output)hist[r]++;
 std::ofstream out(argv[2],std::ios::binary);out.write((char*)output.data(),output.size());
 std::cout<<"N="<<n<<" cases="<<indices.size()<<" seconds="<<omp_get_wtime()-start;
 for(int r=0;r<=35;r++)if(hist[r])std::cout<<" rank"<<r<<"="<<hist[r];std::cout<<"\n";
}
