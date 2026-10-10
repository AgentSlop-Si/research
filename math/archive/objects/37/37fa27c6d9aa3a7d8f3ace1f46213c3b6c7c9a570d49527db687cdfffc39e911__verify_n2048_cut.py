#!/usr/bin/env python3
"""Read constructor certificate as inert JSON; independently verify its separator."""
import json,pathlib,collections,hashlib
R=pathlib.Path(__file__).resolve().parent
path=R/'CONSTRUCTOR_N2048_CUT.json';data=json.loads(path.read_text())
n=data['N'];depth=data['stages'];I=data['I'];J=data['J']
assert n==2048 and depth==4 and I==list(range(683)) and J==list(range(1365,2048))
names={'input':'x','output':'y','lower_state':'l','upper_state':'u'}
cut=[(s,names[k],i) for s,k,i in data['removed_nodes']];assert len(cut)==len(set(cut))==676
cut=set(cut)
for s,k,i in cut:
 assert 0<=s<depth and ((k in ('x','y') and 0<=i<n) or(k=='l' and 1<=i<n) or(k=='u' and 0<=i<n-1))
rev=[int(format(i,'011b')[::-1],2) for i in range(n)]
adj=collections.defaultdict(list)
for s in range(depth):
 for i in range(n):
  adj[s,'x',i].append((s,'y',i))
  if i<n-1:adj[s,'x',i].append((s,'l',i+1))
  if i>0:adj[s,'x',i].append((s,'u',i-1))
  if s<depth-1:adj[s,'y',i].append((s+1,'x',rev[i]))
 for i in range(1,n):
  adj[s,'l',i].append((s,'y',i))
  if i<n-1:adj[s,'l',i].append((s,'l',i+1))
 for i in range(n-1):
  adj[s,'u',i].append((s,'y',i))
  if i>0:adj[s,'u',i].append((s,'u',i-1))
def reach(removed):
 seen={(0,'x',j) for j in J if (0,'x',j) not in removed};q=collections.deque(seen)
 while q:
  for v in adj[q.popleft()]:
   if v not in seen and v not in removed:seen.add(v);q.append(v)
 return seen
reachable=reach(cut);target={(depth-1,'y',i) for i in I};assert not reachable&target
# Negative mutation control: deleting nothing leaves every target reachable.
assert target<=reach(set())
# Record essentiality of each selected node: not needed for upper bound, useful control.
essential=0
for v in cut:
 if reach(cut-{v})&target:essential+=1
p=65537
assert all(p%d for d in range(2,257))
omega=pow(3,(p-1)//n,p)
assert pow(omega,n,p)==1 and pow(omega,n//2,p)!=1
z=[pow(omega,j,p) for j in J];det=1
for j in range(len(z)):
 for i in range(j):det=det*(z[j]-z[i])%p
assert det
out={'field':p,'primitive_root':omega,'fourier_block_determinant':det,'N':n,'stages':depth,'I_half_open':[0,683],'J_half_open':[1365,2048],'cut_vertices':676,'reachable_target_vertices':0,'empty_cut_reaches_all_targets':True,'individually_essential_cut_vertices':essential,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'verification':'Independent directed adjacency and breadth-first reachability; no maxflow implementation or uploaded code executed','mathematical_conclusion':'Every represented four-stage repeated-bit-reversal order-one quasiseparable product has selected block rank at most676; target Fourier block has Vandermonde rank683.'}
(R/'N2048_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
