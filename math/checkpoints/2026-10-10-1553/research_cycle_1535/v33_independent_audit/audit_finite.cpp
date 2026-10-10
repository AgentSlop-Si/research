// Independent finite certificate checker. No supplied code is linked/imported.
// All-minors algorithm: division-free first-row Laplace subset recurrence.
// Routing algorithm: perfect-matching subsets, Boolean relation composition.
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>
using U=uint64_t;
constexpr int N=11, M=1<<N;
using B=std::bitset<M>;
int main(){
 int n;U q;std::cin>>n>>q;assert(n==N&&q==1000000123ULL);
 std::array<std::array<U,N>,N> H{};
 for(auto& row:H)for(auto& x:row)std::cin>>x;
 std::array<std::array<unsigned,N>,3> adj{};
 for(int l=0;l<3;l++){int ec;std::cin>>ec;assert(ec==33);for(int e=0;e<ec;e++){int d,s;std::cin>>d>>s;assert(0<=s&&s<N&&0<=d&&d<N);adj[l][s]|=1u<<d;}}
 assert(std::cin.good());
 std::array<int,M> card{};
 std::array<std::vector<int>,N+1> subsets;
 for(int s=0;s<M;s++){card[s]=__builtin_popcount((unsigned)s);subsets[card[s]].push_back(s);}
 std::vector<U> D((size_t)M*M,0);D[0]=1;
 std::array<U,N+1> minor_count{},minor_zeros{},minor_checksum{};
 for(int s=1;s<M;s++){
   int i=__builtin_ctz((unsigned)s),srest=s&(s-1),k=card[s];
   for(int t:subsets[k]){
     U sum=0;int sign=1;
     for(int js=t;js;js&=js-1){int j=__builtin_ctz((unsigned)js);U term=H[i][j]*D[(size_t)srest*M+(t^(1<<j))]%q;sum=(sum+(sign>0?term:q-term))%q;sign=-sign;}
     D[(size_t)s*M+t]=sum;minor_count[k]++;minor_zeros[k]+=(sum==0);minor_checksum[k]=(minor_checksum[k]+sum)%q;
   }
 }
 std::array<std::vector<B>,3> relation;
 for(int l=0;l<3;l++){
   relation[l].resize(M);relation[l][0].set(0);
   for(int s=1;s<M;s++){
     int j=__builtin_ctz((unsigned)s),srest=s&(s-1);
     for(int t:subsets[card[s]-1])if(relation[l][srest].test(t)){
       unsigned choices=adj[l][j]&~(unsigned)t;
       while(choices){unsigned b=choices&-choices;choices-=b;relation[l][s].set(t|b);}
     }
   }
 }
 std::array<U,N+1> route_count{},route_failures{};
 std::array<int,N+1> min_outputs{};min_outputs.fill(M);
 for(int s=1;s<M;s++){
   int k=card[s];B reach=relation[0][s];
   for(int l=1;l<3;l++){B next;for(int t:subsets[k])if(reach.test(t))next|=relation[l][t];reach=next;}
   min_outputs[k]=std::min(min_outputs[k],(int)reach.count());
   for(int t:subsets[k]){route_count[k]++;route_failures[k]+=!reach.test(t);}
 }
 auto list=[](auto const& a){std::cout<<'[';for(int k=1;k<=N;k++){if(k>1)std::cout<<',';std::cout<<a[k];}std::cout<<']';};
 std::cout<<"{\n\"all_minors_count_by_order\":";list(minor_count);
 std::cout<<",\n\"zero_minors_by_order\":";list(minor_zeros);
 std::cout<<",\n\"minor_residue_sum_by_order\":";list(minor_checksum);
 std::cout<<",\n\"routing_terminal_pairs_by_size\":";list(route_count);
 std::cout<<",\n\"failed_routing_pairs_by_size\":";list(route_failures);
 std::cout<<",\n\"minimum_reachable_output_subsets_by_size\":";list(min_outputs);
 std::cout<<",\n\"full_determinant\":"<<D[(size_t)(M-1)*M+(M-1)]<<"\n}\n";
}
