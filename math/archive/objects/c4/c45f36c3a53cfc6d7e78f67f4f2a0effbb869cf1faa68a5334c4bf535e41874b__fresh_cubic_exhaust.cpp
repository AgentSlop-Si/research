// Independently authored bounded certificate verifier; consumes only fresh reconstructed matrices.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <algorithm>
#include <numeric>
#include <cstdint>
using I=long long;
I P; I mod(I x){x%=P;return x<0?x+P:x;} I power(I a,I n){I r=1;for(;n;n>>=1,a=a*a%P)if(n&1)r=r*a%P;return r;}
using Exp=std::array<int,3>; using Quad=std::array<I,6>;
std::vector<Exp> mon(int d){std::vector<Exp> o;for(int a=d;a>=0;--a)for(int b=d-a;b>=0;--b)o.push_back({a,b,d-a-b});return o;}
std::vector<Exp> m2=mon(2),m3=mon(3),m4=mon(4),m1=mon(1);
std::vector<std::vector<int>> lift(int d){auto u=mon(d-2),v=mon(d);std::vector<std::vector<int>> out;for(auto e:u){std::vector<int> row;for(auto f:m2){Exp g={e[0]+f[0],e[1]+f[1],e[2]+f[2]};row.push_back(std::find(v.begin(),v.end(),g)-v.begin());}out.push_back(row);}return out;}
Quad product(std::array<I,3> a,std::array<I,3> b){Quad out{};for(int i=0;i<3;++i)for(int j=0;j<3;++j){Exp e={0,0,0};++e[i];++e[j];int k=std::find(m2.begin(),m2.end(),e)-m2.begin();out[k]=mod(out[k]+a[i]*b[j]);}return out;}
struct Cert {int rank;unsigned mask;I determinant;};
Cert certificate(const std::vector<Quad>& qs,int d){int cols=(d==3?10:15);static const auto l3=lift(3),l4=lift(4);const auto &loc=(d==3?l3:l4);I a[18][15]={};int ids[18];int rows=0;for(auto q:qs)for(auto m:loc){for(int k=0;k<6;++k)a[rows][m[k]]=q[k];ids[rows]=rows;++rows;} int r=0;unsigned mask=0;I det=1;std::vector<int> selected;
 for(int c=0;c<cols && r<rows;++c){int s=r;while(s<rows&&!a[s][c])++s;if(s==rows)continue;if(s!=r){for(int j=0;j<cols;++j)std::swap(a[s][j],a[r][j]);std::swap(ids[s],ids[r]);}mask|=1U<<ids[r];selected.push_back(ids[r]);det=det*a[r][c]%P;I inv=power(a[r][c],P-2);for(int i=r+1;i<rows;++i){I x=a[i][c]*inv%P;if(x)for(int j=c+1;j<cols;++j)a[i][j]=mod(a[i][j]-x*a[r][j]);a[i][c]=0;}++r;}
 int inversions=0;for(int i=0;i<(int)selected.size();++i)for(int j=i+1;j<(int)selected.size();++j)inversions+=selected[i]>selected[j];if(inversions%2)det=mod(-det);return {r,mask,det};
}
std::vector<int> unpack(I code,int n,int k){std::vector<int> avail(n);std::iota(avail.begin(),avail.end(),0);std::vector<int> out;for(int i=0;i<k;++i){I suffix=1;for(int j=i+1;j<k;++j)suffix*=n-j;int a=code/suffix;code%=suffix;out.push_back(avail[a]);avail.erase(avail.begin()+a);}return out;}
int main(int argc,char**argv){if(argc!=4)return 2;std::ifstream f(argv[1]);int n;f>>n>>P;std::vector<std::vector<I>> T(n,std::vector<I>(n));std::vector<std::vector<std::array<I,3>>> B(n,std::vector<std::array<I,3>>(n));for(auto&r:T)for(auto&x:r)f>>x;for(int k=0;k<3;++k)for(int i=0;i<n;++i)for(int j=0;j<n;++j)f>>B[i][j][k];if(!f)return 3;I requested=std::stoll(argv[2]);I columns=I(n)*(n-1)*(n-2)*(n-3),total=I(n)*(n-1)*columns;I checks=requested?std::min(requested,total):total;bool exhaustive=checks==total;
 std::ofstream w(std::string(argv[3])+"_exceptions.csv");w<<"mapping,r0,r1,c0,c1,c2,c3,cubic_rank,cubic_row_mask,cubic_det\n";I bad3=0,bad4=0;int min3=10,min4=15;I determinant_product=1;unsigned common_mask=1023;I nondefault_masks=0;I step=total/2+1;while(std::gcd(step,total)!=1)++step;
 for(I t=0;t<checks;++t){I index=exhaustive?t:((__int128)t*step+17)%total;auto rs=unpack(index/columns,n,2);auto cs=unpack(index%columns,n,4);std::vector<Quad> q;for(auto pair:std::vector<std::array<int,2>>{{0,1},{0,2},{0,3},{1,2}}){int a=pair[0],b=pair[1];auto l=product(B[rs[1]][cs[a]],B[rs[0]][cs[b]]),r=product(B[rs[1]][cs[b]],B[rs[0]][cs[a]]);I x=T[0][a]*T[1][b]%P,y=T[0][b]*T[1][a]%P;Quad z;for(int k=0;k<6;++k)z[k]=mod(x*l[k]%P-y*r[k]%P);q.push_back(z);}auto a=certificate({q[0],q[1],q[2],q[3]},3);bad3+=a.rank!=10;min3=std::min(min3,a.rank);determinant_product=determinant_product*a.determinant%P;nondefault_masks+=a.mask!=common_mask;if(a.mask!=common_mask || a.rank!=10){w<<index<<','<<rs[0]<<','<<rs[1];for(int x:cs)w<<','<<x;w<<','<<a.rank<<','<<a.mask<<','<<a.determinant<<'\n';}}
 std::cout<<"{\"N\":"<<n<<",\"prime\":"<<P<<",\"checked_distinct_mappings\":"<<checks<<",\"possible_mappings\":"<<total<<",\"exhaustive\":"<<(exhaustive?"true":"false")<<",\"min_cubic_rank\":"<<min3<<",\"deficient_cubic\":"<<bad3<<",\"maximal_minor_product\":"<<determinant_product<<",\"default_minor_row_mask\":"<<common_mask<<",\"nondefault_minor_count\":"<<nondefault_masks<<",\"sample_step\":"<<step<<"}\n";
 return (bad3||bad4)?1:0;
}
