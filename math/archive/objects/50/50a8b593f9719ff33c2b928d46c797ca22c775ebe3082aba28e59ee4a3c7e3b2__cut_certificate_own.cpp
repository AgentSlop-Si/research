// Independently authored exact finite-field rank and vertex-capacity flow checker.
#include <vector>
#include <array>
#include <iostream>
#include <queue>
#include <algorithm>
#include <cstdint>
using namespace std; using ll=long long;
ll powm(ll a,ll b,ll p){ll r=1;for(;b;b>>=1,a=a*a%p)if(b&1)r=r*a%p;return r;}
pair<int,ll> rankdet(vector<vector<ll>> a,ll p){int n=a.size(),r=0;ll d=1;for(int j=0;j<n;j++){int k=r;while(k<n&&!a[k][j])k++;if(k==n)continue;if(k!=r){swap(a[k],a[r]);d=(p-d)%p;}ll piv=a[r][j];d=d*piv%p;ll v=powm(piv,p-2,p);for(int k=r+1;k<n;k++){ll t=a[k][j]*v%p;if(t)for(int c=j;c<n;c++)a[k][c]=(a[k][c]-t*a[r][c]%p+p)%p;}r++;}return {r,r==n?d:0};}
struct Flow{struct E{int to,rev,cap;};vector<vector<E>>g;vector<int>lev,it;Flow(int n):g(n),lev(n),it(n){};void edge(int a,int b,int c){E x{b,(int)g[b].size(),c},y{a,(int)g[a].size(),0};g[a].push_back(x);g[b].push_back(y);}bool bfs(int s,int t){fill(lev.begin(),lev.end(),-1);queue<int>q;q.push(s);lev[s]=0;while(q.size()){int v=q.front();q.pop();for(auto&e:g[v])if(e.cap&&lev[e.to]<0)lev[e.to]=lev[v]+1,q.push(e.to);}return lev[t]>=0;}int dfs(int v,int t,int f){if(v==t)return f;for(int&i=it[v];i<(int)g[v].size();i++){auto&e=g[v][i];if(e.cap&&lev[e.to]==lev[v]+1){int a=dfs(e.to,t,min(f,e.cap));if(a){e.cap-=a;g[e.to][e.rev].cap+=a;return a;}}}return 0;}int maxflow(int s,int t){int a=0,v;while(bfs(s,t)){fill(it.begin(),it.end(),0);while((v=dfs(s,t,1000000)))a+=v;}return a;}};
int main(){int n;cin>>n;vector<vector<int>>perms(3,vector<int>(n));for(auto&r:perms)for(auto&x:r)cin>>x;vector<array<vector<int>,4>> sets(n);vector<array<int,4>>ds(n);vector<array<int,2>>ranks(n);vector<array<ll,2>>dets(n);
for(int mask=1;mask<n;mask++){for(int j=0;j<n;j++)sets[mask][0].push_back(__builtin_parity((unsigned)(j&mask))==0);for(int s=1;s<4;s++)for(int j=0;j<n;j++)sets[mask][s].push_back(sets[mask][s-1][perms[s-1][j]]);for(int s=0;s<4;s++){ds[mask][s]=0;for(int j=1;j<n;j++)ds[mask][s]+=sets[mask][s][j]!=sets[mask][s][j-1];}}
for(int f=0;f<2;f++){ll p=f?65537:12289,w=f?282:8340;vector<ll>wp(n);wp[0]=1;for(int j=1;j<n;j++)wp[j]=wp[j-1]*w%p;for(int mask=1;mask<n;mask++){vector<int>R,C;for(int j=0;j<n;j++){if(!sets[mask][3][j])R.push_back(j);if(sets[mask][0][j])C.push_back(j);}vector<vector<ll>>a;for(int i:R){vector<ll>r;for(int j:C)r.push_back(wp[(i*j)%n]);a.push_back(r);}auto rd=rankdet(a,p);ranks[mask][f]=rd.first;dets[mask][f]=rd.second;}}
vector<vector<int>>flows(16,vector<int>(n));vector<int>best(16,-999),arg(16,0);
auto id=[n](int s,int t,int j){return s*8*n+t*n+j;};int nodes=32*n+2,src=nodes-2,sink=nodes-1,inf=10000;
for(int J=1;J<16;J++){Flow base(nodes);for(int s=0;s<4;s++){for(int j=0;j<n;j++){base.edge(id(s,0,j),id(s,1,j),1);base.edge(id(s,2,j),id(s,3,j),1);base.edge(id(s,1,j),id(s,2,j),inf);}if(!(J&(1<<s))){for(int j=1;j<n;j++){base.edge(id(s,4,j),id(s,5,j),1);base.edge(id(s,1,j-1),id(s,4,j),inf);base.edge(id(s,5,j),id(s,2,j),inf);if(j+1<n)base.edge(id(s,5,j),id(s,4,j+1),inf);}for(int j=0;j<n-1;j++){base.edge(id(s,6,j),id(s,7,j),1);base.edge(id(s,1,j+1),id(s,6,j),inf);base.edge(id(s,7,j),id(s,2,j),inf);if(j)base.edge(id(s,7,j),id(s,6,j-1),inf);}}}for(int s=0;s<3;s++)for(int j=0;j<n;j++)base.edge(id(s,3,perms[s][j]),id(s+1,0,j),inf);
 for(int mask=1;mask<n;mask++){Flow flow=base;for(int j=0;j<n;j++){if(sets[mask][0][j])flow.edge(src,id(0,0,j),inf);if(!sets[mask][3][j])flow.edge(id(3,3,j),sink,inf);}int value=flow.maxflow(src,sink);flows[J][mask]=value;int budget=0;for(int s=0;s<4;s++)if(!(J&(1<<s)))budget+=ds[mask][s];if(value>budget||ranks[mask][0]!=ranks[mask][1])return 3;int gap=ranks[mask][0]-value;if(gap>best[J])best[J]=gap,arg[J]=mask;}
 cerr<<"flow subset "<<J<<" done\n";
}
cout<<"{\"parity\":[";for(int m=1;m<n;m++){if(m>1)cout<<",";cout<<"{\"mask\":"<<m<<",\"boundaries\":[";for(int s=0;s<4;s++){if(s)cout<<",";cout<<ds[m][s];}cout<<"],\"rank\":["<<ranks[m][0]<<","<<ranks[m][1]<<"],\"det\":["<<dets[m][0]<<","<<dets[m][1]<<"]}";}cout<<"],\"subsets\":[";for(int J=1;J<16;J++){if(J>1)cout<<",";cout<<"{\"J_bits\":"<<J<<",\"best\":"<<best[J]<<",\"first_mask\":"<<arg[J]<<",\"flows\":[";for(int m=1;m<n;m++){if(m>1)cout<<",";cout<<flows[J][m];}cout<<"]}";}cout<<"]}\n";}
