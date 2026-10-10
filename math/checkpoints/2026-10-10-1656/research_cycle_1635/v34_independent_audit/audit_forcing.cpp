#include <array>
#include <vector>
#include <iostream>
#include <fstream>
#include <cstdint>
#include <cassert>
#include <algorithm>
using namespace std;
using Bits=array<uint64_t,32>;
array<Bits,2048> permitted;
array<Bits,12> by_size;
const uint64_t highmask[6]={0xaaaaaaaaaaaaaaaaULL,0xccccccccccccccccULL,0xf0f0f0f0f0f0f0f0ULL,0xff00ff00ff00ff00ULL,0xffff0000ffff0000ULL,0xffffffff00000000ULL};

// A nonempty U is a stopping set if no row meets it exactly once.
// A seed is forcing iff its unknown complement contains no stopping set.
// Build all stopping sets, then their upward closure by Boolean zeta transform.
int exact_forcing(const array<int,11>& rows, int* witness=nullptr){
 Bits forbidden; forbidden.fill(~uint64_t(0));
 for(int r:rows) for(int w=0;w<32;w++) forbidden[w]&=permitted[r][w];
 forbidden[0]&=~uint64_t(1);
 for(int d=0;d<6;d++) for(auto& w:forbidden) w|=(w<<(1<<d))&highmask[d];
 for(int d=6;d<11;d++){
  int step=1<<(d-6);
  for(int start=0;start<32;start+=2*step)
   for(int j=0;j<step;j++) forbidden[start+step+j]|=forbidden[start+j];
 }
 for(int k=0;k<=11;k++) for(int w=0;w<32;w++){
  uint64_t feasible=~forbidden[w]&by_size[11-k][w];
  if(feasible){if(witness)*witness=2047^(64*w+__builtin_ctzll(feasible));return k;}
 }
 abort();
}

struct Run {
 vector<pair<int,int>> edges;
 vector<int> eligible;
 array<int,11> rows{},cols{};
 uint64_t hist[12]{},dualhist[12]{},joint[12][12]{};
 uint64_t patterns=0;
 bool transpose=false;
 int layer,z;
 vector<int> deleted;
 ofstream* exceptions;
 ofstream* certificates=nullptr;
 void leaf(){
  int seed;int a=exact_forcing(rows,&seed),b=transpose?exact_forcing(cols):-1;
  hist[a]++;patterns++;
  if(certificates){
   assert(a<=3);
   for(int j=0;__builtin_popcount(unsigned(seed))<3;j++) seed|=1<<j;
   uint64_t dm=0;for(int e:deleted)dm|=uint64_t(1)<<e;
   *certificates<<layer<<' '<<dm<<' '<<seed<<'\n';
  }
  if(transpose){dualhist[min(a,b)]++;joint[a][b]++;}
  if(a>=4 && z<=6){
   *exceptions<<layer<<' '<<z<<' '<<a<<' '<<b<<' '<<seed;
   for(int d:deleted)*exceptions<<' '<<d;
   *exceptions<<'\n';
  }
 }
 void enumerate(int first,int left){
  if(!left){leaf();return;}
  for(int index=first;index<=int(eligible.size())-left;index++){
   int e=eligible[index];
   auto [r,c]=edges[e];rows[r]^=1<<c;cols[c]^=1<<r;deleted.push_back(e);
   enumerate(index+1,left-1);
   deleted.pop_back();rows[r]^=1<<c;cols[c]^=1<<r;
  }
 }
};

int main(int argc,char**argv){
 for(int mask=0;mask<2048;mask++)for(int U=0;U<2048;U++)
  if(__builtin_popcount(unsigned(mask&U))!=1)permitted[mask][U/64]|=uint64_t(1)<<(U%64);
 for(int U=0;U<2048;U++)by_size[__builtin_popcount(unsigned(U))][U/64]|=uint64_t(1)<<(U%64);
 array<int,11> identity{},zero{},dense{};
 for(int j=0;j<11;j++){identity[j]=1<<j;dense[j]=2047;}
 assert(exact_forcing(identity)==0);assert(exact_forcing(zero)==11);assert(exact_forcing(dense)==10);
 int maxz=argc>1?atoi(argv[1]):5;
 bool dual=argc>2?atoi(argv[2]):false;
 bool restricted=argc>3?atoi(argv[3]):false;
 ofstream exceptional(restricted?"restricted_exceptional_masks.txt":"exceptional_masks.txt");
 ofstream certificates;
 if(restricted)certificates.open("restricted_seed_certificates.txt");
 cout<<"{\"method\":\"stopping-set upward Boolean zeta transform\",\"controls\":true,\"layers\":[";
 for(int l=0;l<3;l++){
  vector<pair<int,int>> edges;
  for(int i=0;i<33;i++){int r,c;cin>>r>>c;assert(cin);edges.push_back({r,c});}
  vector<int> eligible;
  if(restricted){int count;cin>>count;for(int i=0;i<count;i++){int e;cin>>e;eligible.push_back(e);}maxz=count;}
  else for(int e=0;e<33;e++)eligible.push_back(e);
  if(l)cout<<',';cout<<'[';
  for(int z=0;z<=maxz;z++){
   Run R;R.edges=edges;R.eligible=eligible;R.layer=l;R.z=z;R.transpose=dual;R.exceptions=&exceptional;
   if(restricted)R.certificates=&certificates;
   for(auto [r,c]:edges){R.rows[r]|=1<<c;R.cols[c]|=1<<r;}
   R.enumerate(0,z);
   if(z)cout<<',';
   cout<<"{\"deleted\":"<<z<<",\"patterns\":"<<R.patterns<<",\"histogram\":[";
   for(int k=0;k<12;k++){if(k)cout<<',';cout<<R.hist[k];}
   cout<<"],\"dual_histogram\":[";
   for(int k=0;k<12;k++){if(k)cout<<',';cout<<R.dualhist[k];}
   cout<<"],\"joint_histogram\":[";
   for(int a=0;a<12;a++){if(a)cout<<',';cout<<'[';for(int b=0;b<12;b++){if(b)cout<<',';cout<<R.joint[a][b];}cout<<']';}
   cout<<"]}"<<flush;
   cerr<<"Completed layer "<<l<<", z="<<z<<", patterns="<<R.patterns<<"\n";
  }
  cout<<']';
 }
 cout<<"]}\n";
}
