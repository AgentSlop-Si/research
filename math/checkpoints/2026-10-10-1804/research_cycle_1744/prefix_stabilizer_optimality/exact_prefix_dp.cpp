// Fresh independent control, 2026-10-10. No inherited project code.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
uint64_t rot(uint64_t x,int s,int m){uint64_t mask=(uint64_t(1)<<m)-1;return ((x<<s)|(x>>(m-s)))&mask;}
int stab(uint64_t x,int m,const vector<int>& periods){for(int s:periods) if(rot(x,s,m)==x) return m/s;return 1;}
int target(int m){int z=0,n=m;for(int p=2;p<=n;++p)while(n%p==0){z+=m-m/p;n/=p;}return z;}
int main(int argc,char**argv){int lo=argc>1?atoi(argv[1]):2, hi=argc>2?atoi(argv[2]):24;
 if(lo<2 || hi>27 || lo>hi){cerr<<"Supported exact bound: 2 <= low <= high <= 27\n";return 2;}
 for(int m=lo;m<=hi;++m){auto start=chrono::steady_clock::now();vector<int> per;for(int s=1;s<m;s++)if(m%s==0)per.push_back(s);uint32_t lim=uint32_t(1)<<(m-1); vector<uint16_t> dp(lim);vector<uint8_t> last(lim); // all represented sets contain 0, first element fixed by translation
 dp[0]=0;for(uint32_t a=1;a<lim;++a){uint16_t best=0;uint8_t at=0;for(uint32_t b=a;b;b&=b-1){int k=__builtin_ctz(b);if(dp[a^(uint32_t(1)<<k)]>=best){best=dp[a^(uint32_t(1)<<k)];at=k+1;}}dp[a]=best+stab((uint64_t(a)<<1)|1,m,per)-1;last[a]=at;}
 vector<int> order;for(uint32_t a=lim-1;a;){int x=last[a];order.push_back(x);a^=uint32_t(1)<<(x-1);}order.push_back(0);reverse(order.begin(),order.end());int check=0;uint64_t set=0;vector<int> weights;for(int x:order){set|=uint64_t(1)<<x;int h=0;for(int s=0;s<m;s++){bool ok=true;for(int y=0;y<m;y++)if(((set>>y)&1)!=((set>>((y+s)%m))&1)){ok=false;break;}h+=ok;}check+=h-1;weights.push_back(h);}
 if(check!=dp.back()){cerr<<"verification failure";return 1;}cout<<"{\"m\":"<<m<<",\"maximum\":"<<dp.back()<<",\"hierarchy\":"<<target(m)<<",\"states\":"<<lim<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"order\":[";for(int i=0;i<m;i++)cout<<(i?",":"")<<order[i];cout<<"],\"stabilizers\":[";for(int i=0;i<m;i++)cout<<(i?",":"")<<weights[i];cout<<"]}"<<endl;
 }
}
