#!/usr/bin/env python3
"""Independent Boolean reachability and Fourier determinant checks."""
import pathlib,json,collections
R=pathlib.Path(__file__).resolve().parent
A={0,2,4,6,8,10,12,16,18,20,24,26,28};V={20,22,24,25,26,28,30}
def rev(i,n):return int(format(i,f'0{n.bit_length()-1}b')[::-1],2)
def make_cut(m):
 c={(0,'l',13*m),(2,'l',19*m)}
 for z in range(m):
  c.update((1,'x',32*z+r) for r in [24,26,28]);c.add((1,'l',32*z+21))
  if z<m-1:c.add((1,'u',32*z+31))
 for b in V:c.update((2,'x',b*m+j) for j in range(m))
 assert len(c)==12*m+1
 return c

def propagate(n,c):
 m=n//32;x=[i<13*m for i in range(n)];records=[]
 for s in range(3):
  x=[v and(s,'x',i) not in c for i,v in enumerate(x)];lo=[False]*n;up=[False]*n
  for i in range(1,n):lo[i]=(s,'l',i) not in c and(x[i-1] or lo[i-1])
  for i in range(n-2,-1,-1):up[i]=(s,'u',i) not in c and(x[i+1] or up[i+1])
  y=[(x[i] or lo[i] or up[i]) and(s,'y',i) not in c for i in range(n)];records.append({'stage':s,'input':{i for i,v in enumerate(x) if v},'output':{i for i,v in enumerate(y) if v}})
  x=[y[rev(i,n)] for i in range(n)]
 return records

def bfs(n,c):
 m=n//32;adj=collections.defaultdict(list)
 for s in range(3):
  for i in range(n):
   adj[s,'x',i].append((s,'y',i))
   if i<n-1:adj[s,'x',i].append((s,'l',i+1))
   if i>0:adj[s,'x',i].append((s,'u',i-1))
   if s<2:adj[s,'y',i].append((s+1,'x',rev(i,n)))
  for i in range(1,n):
   adj[s,'l',i].append((s,'y',i))
   if i<n-1:adj[s,'l',i].append((s,'l',i+1))
  for i in range(n-1):
   adj[s,'u',i].append((s,'y',i))
   if i:adj[s,'u',i].append((s,'u',i-1))
 seen={(0,'x',j) for j in range(13*m)};q=collections.deque(seen)
 while q:
  for v in adj[q.popleft()]:
   if v not in seen and v not in c:seen.add(v);q.append(v)
 return {i for i in range(n) if(2,'y',i) in seen}

cases=[]
for e in range(9):
 m=1<<e;n=32*m;c=make_cut(m)
 for s,k,i in c:assert 0<=s<3 and((k=='x' and 0<=i<n)or(k=='l' and 1<=i<n)or(k=='u' and 0<=i<n-1))
 rec=propagate(n,c)
 assert rec[0]['output']==set(range(13*m))
 assert {rev(i,n)%32 for i in rec[0]['output']}==A
 assert rec[1]['output']=={32*z+r for z in range(m) for r in range(21)}
 assert {rev(i,n)//m for i in rec[1]['output'] if rev(i,n)>=19*m}==V
 assert rec[2]['output']==set(range(19*m))
 assert not rec[2]['output']&set(range(19*m,n))
 assert propagate(n,set())[-1]['output']==set(range(n))
 if n<=128:assert bfs(n,c)==rec[-1]['output']
 cases.append({'N':n,'m':m,'cut_nodes':len(c),'source_width':13*m,'target_width':13*m,'gap':m-1,'reachable_target_count':0,'independent_BFS_crosscheck':n<=128})
dets=[];p=65537
for n in [64,128]:
 w=pow(3,(p-1)//n,p);assert pow(w,n,p)==1 and pow(w,n//2,p)!=1;m=n//32;W=13*m
 nodes=[pow(w,j,p) for j in range(W)];d=pow(w,19*m*sum(range(W)),p)
 for j in range(W):
  for i in range(j):d=d*(nodes[j]-nodes[i])%p
 assert d;dets.append({'N':n,'field':p,'root':w,'rows':[19*m,n],'columns':[0,W],'rank':W,'determinant':d})
out={'uniform_cut_cases':cases,'fourier_determinants':dets,'source_credit':'The uniform12m+1 cut and N64 threshold originate in newly supplied bitrev no-go source; this is independent verification.','uploaded_code_executed':False}
(R/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
