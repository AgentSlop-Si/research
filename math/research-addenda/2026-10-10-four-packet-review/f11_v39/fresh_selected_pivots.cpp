// Fresh exact occurrence checker for all selected quartic unit pivots.
// The certificate is inert binary arrays prepared with allow_pickle=False.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Word=__uint128_t;
struct Pivot{Word key;uint32_t owner;};
template<class T>vector<T> load(string path,size_t n){vector<T>x(n);ifstream f(path,ios::binary);f.read(reinterpret_cast<char*>(x.data()),sizeof(T)*n);assert(f && f.peek()==EOF);return x;}
int main(int argc,char**argv){
 assert(argc==2);string root=argv[1];const int N=1663740;
 auto hi=load<uint32_t>(root+"/pivot_hi.bin",N);auto lo=load<uint64_t>(root+"/pivot_lo.bin",N);auto rounds=load<int8_t>(root+"/rounds.bin",N);
 vector<Pivot> pivots;pivots.reserve(N);
 for(int i=0;i<N;i++){
   Word v=(Word(hi[i])<<64)|lo[i],x=v;array<int,12> e;
   for(int j=11;j>=0;j--){e[j]=(x&127)-1;x>>=7;}
   assert(x==0&&is_sorted(e.begin(),e.end()));array<int,3> layer{};
   for(int edge:e){assert(edge>=0&&edge<99);layer[edge/33]++;}
   assert((layer==array<int,3>{4,4,4}));assert(rounds[i]>=0&&rounds[i]<=2);pivots.push_back({v,uint32_t(i)});
 }
 sort(pivots.begin(),pivots.end(),[](const Pivot&a,const Pivot&b){return a.key<b.key;});
 for(int i=1;i<N;i++)assert(pivots[i-1].key!=pivots[i].key);
 ifstream f(root+"/selected_paths.txt");vector<array<int,3>> paths[78];
 for(auto &ps:paths){int n;f>>n;assert(n>=1&&n<=3);for(int i=0;i<n;i++){array<int,3>a;for(int&e:a)f>>e;assert(f);ps.push_back(a);}}
 vector<Word> terms;terms.reserve(21770715);vector<unsigned> own(N);uint64_t cross=0;int col=0;
 for(int a=0;a<78;a++)for(int b=a;b<78;b++)for(int c=b;c<78;c++)for(int d=c;d<78;d++,col++){
   for(const auto &pa:paths[a])for(const auto &pb:paths[b])for(const auto &pc:paths[c])for(const auto &pd:paths[d]){
     array<int,12> es;copy(pa.begin(),pa.end(),es.begin());copy(pb.begin(),pb.end(),es.begin()+3);copy(pc.begin(),pc.end(),es.begin()+6);copy(pd.begin(),pd.end(),es.begin()+9);sort(es.begin(),es.end());
     Word key=0;for(int e:es)key=(key<<7)|(e+1);terms.push_back(key);
     auto it=lower_bound(pivots.begin(),pivots.end(),key,[](const Pivot&a,Word b){return a.key<b;});
     if(it!=pivots.end() && it->key==key){
       if(it->owner==unsigned(col))own[col]++;
       else{assert(rounds[col]<rounds[it->owner]);cross++;}
     }
   }
   if(col%300000==0)cerr<<"columns="<<col<<" terms="<<terms.size()<<"\n";
 }
 assert(col==N&&terms.size()==21770715);for(unsigned n:own)assert(n==1);
 sort(terms.begin(),terms.end());uint64_t unique=1;for(size_t i=1;i<terms.size();i++)unique+=terms[i]!=terms[i-1];assert(unique==19337020);
 cout<<"COLUMNS "<<col<<"\nTERMS "<<terms.size()<<"\nDISTINCT_EDGE_MONOMIALS "<<unique<<"\nUNIT_PIVOTS "<<N<<"\nCROSS_COLUMN_PIVOT_OCCURRENCES "<<cross<<"\nALL_CROSS_OCCURRENCES_STRICTLY_EARLIER 1\nALL_PIVOTS_DISTINCT 1\nALL_OWN_COEFFICIENTS_ONE 1\n";
}
