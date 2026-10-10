#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <utility>
#include <vector>
using P=std::pair<int,int>;
std::vector<P> baseline(int n){std::vector<P>s;for(int m=1;m<n;m*=2)for(int i=0;i<n;i++)if(!(i&m))s.push_back({i,i|m});return s;}
bool full(const std::vector<P>&s,int n,bool reverse){std::array<uint32_t,64>a;for(int i=0;i<n;i++)a[i]=1u<<i; if(!reverse){for(auto [i,j]:s)a[i]=a[j]=a[i]|a[j];}else{for(auto it=s.rbegin();it!=s.rend();it++){auto[i,j]=*it;a[i]=a[j]=a[i]|a[j];}}for(int i=0;i<n;i++)if(a[i]!=(1u<<n)-1)return false;return true;}
int main(int argc,char**argv){int n=argc>1?std::stoi(argv[1]):16;int rew=argc>2?std::stoi(argv[2]):2;bool rev=argc>3;auto start=std::chrono::steady_clock::now();auto orig=baseline(n);std::vector<P>pairs;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)pairs.push_back({i,j});uint64_t total=0,success=0;std::ofstream wit("results/topology_witnesses_"+std::to_string(n)+"_"+std::to_string(rew)+(rev?"_reverse":"")+".jsonl");for(int d=0;d<(int)orig.size();d++){auto s=orig;s.erase(s.begin()+d);if(rew==0){total++;if(full(s,n,rev))success++;continue;}for(int p=0;p<(int)s.size();p++){P op=s[p];for(P np:pairs){if(np==op)continue;s[p]=np;if(rew==1){total++;if(full(s,n,rev)){success++;wit<<"{\"delete\":"<<d<<",\"replace\":[["<<p<<","<<np.first<<","<<np.second<<"]]}\n";}continue;}for(int q=p+1;q<(int)s.size();q++){P oq=s[q];for(P nq:pairs){if(nq==oq)continue;s[q]=nq;total++;if(full(s,n,rev)){success++;wit<<"{\"delete\":"<<d<<",\"replace\":[["<<p<<","<<np.first<<","<<np.second<<"],["<<q<<","<<nq.first<<","<<nq.second<<"]]}\n";}}s[q]=oq;}}s[p]=op;}}double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"{\"n\":"<<n<<",\"baseline_calls\":"<<orig.size()<<",\"candidate_calls\":"<<orig.size()-1<<",\"replacements\":"<<rew<<",\"direction\":\""<<(rev?"reverse":"forward")<<"\",\"labeled_schedules\":"<<total<<",\"full_support_schedules\":"<<success<<",\"elapsed_seconds\":"<<elapsed<<"}\n";}
