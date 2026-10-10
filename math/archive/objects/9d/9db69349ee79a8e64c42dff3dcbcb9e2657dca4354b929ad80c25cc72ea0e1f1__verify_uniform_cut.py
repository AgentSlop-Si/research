"""Independent graph/BFS audit of the uploaded 32-position cut recipe.
Only source JSON is read as data. No uploaded source code is executed/imported.
"""
from collections import deque
from pathlib import Path
import json,hashlib
BASE=Path(__file__).parent;SRC=BASE/'source'

def rev(i,m):
 out=0
 for _ in range(m):out=(out<<1)|(i&1);i>>=1
 return out

def graph(n):
 sn=4*n-2;g=[[] for _ in range(3*sn)]
 def node(s,k,i):
  return s*sn+({'input':0,'output':n,'lower':2*n-1,'upper':3*n-1}[k])+i
 for s in range(3):
  for i in range(n):g[node(s,'input',i)].append(node(s,'output',i))
  for i in range(1,n):
   g[node(s,'input',i-1)].append(node(s,'lower',i));g[node(s,'lower',i)].append(node(s,'output',i))
   if i>1:g[node(s,'lower',i-1)].append(node(s,'lower',i))
  for i in range(n-1):
   g[node(s,'input',i+1)].append(node(s,'upper',i));g[node(s,'upper',i)].append(node(s,'output',i))
   if i<n-2:g[node(s,'upper',i+1)].append(node(s,'upper',i))
  if s<2:
   for i in range(n):g[node(s,'output',i)].append(node(s+1,'input',rev(i,n.bit_length()-1)))
 return g,node

def walk(g,starts,cut):
 seen=set(starts)-cut;q=deque(seen)
 while q:
  for v in g[q.popleft()]:
   if v not in seen and v not in cut:seen.add(v);q.append(v)
 return seen

results=[]
for n in [32,64,128,256,512,1024,2048,4096,8192]:
 m=n//32;g,node=graph(n)
 recipe=[(0,'lower',13*m),(2,'lower',19*m)]
 recipe += [(1,'input',32*z+r) for z in range(m) for r in [24,26,28]]
 recipe += [(1,'lower',32*z+21) for z in range(m)]
 recipe += [(1,'upper',32*z+31) for z in range(m-1)]
 recipe += [(2,'input',b*m+u) for b in [20,22,24,25,26,28,30] for u in range(m)]
 cut={node(*v) for v in recipe};assert len(cut)==len(recipe)==12*m+1
 starts={node(0,'input',j) for j in range(13*m)}
 reach=walk(g,starts,cut);target={node(2,'output',i) for i in range(19*m,n)};assert not(reach&target)
 assert len(walk(g,starts,set())&target)==13*m
 y0={i for i in range(n) if node(0,'output',i) in reach};y1={i for i in range(n) if node(1,'output',i) in reach};y2={i for i in range(n) if node(2,'output',i) in reach}
 assert y0==set(range(13*m));assert y1=={32*z+r for z in range(m) for r in range(21)};assert y2==set(range(19*m))
 assert {rev(a,5) for a in range(13)}=={0,2,4,6,8,10,12,16,18,20,24,26,28}
 assert {rev(a,5) for a in range(21) if rev(a,5)>=19}=={20,22,24,25,26,28,30}
 for a in range(32):
  for b in range(m):assert rev(a*m+b,n.bit_length()-1)==32*rev(b,m.bit_length()-1)+rev(a,5)
 results.append({'N':n,'m':m,'cut_size':len(cut),'Fourier_minor_size':13*m,'gap':m-1,'disconnected':True,'empty_cut_reaches_all_targets':True,'stage_output_counts':[len(y0),len(y1),len(y2)]})

def det(a,p):
 a=[r[:] for r in a];res=1;n=len(a)
 for j in range(n):
  k=next((k for k in range(j,n) if a[k][j]%p),None)
  if k is None:return 0
  if k!=j:a[j],a[k]=a[k],a[j];res=-res
  res=res*a[j][j]%p;iv=pow(a[j][j],p-2,p)
  for k in range(j+1,n):
   t=a[k][j]*iv%p;a[k]=[(x-t*y)%p for x,y in zip(a[k],a[j])]
 return res%p
mods=[]
for name in ['NETWORK_CERTIFICATE_N64.json','NETWORK_CERTIFICATE_N128.json']:
 data=json.loads((SRC/name).read_text());n=data['n']
 for q in data['primes']:
  p=q['prime'];w=q['primitive_root'];assert all(p%d for d in range(2,int(p**0.5)+1));assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
  a=[[pow(w,i*j,p) for j in data['columns']] for i in data['rows']];d=det(a,p);assert d==q['determinant'] and d!=0
  mods.append({'source_json':name,'N':n,'prime':p,'root':w,'minor_size':len(a),'determinant':d})
out={'all_passed':True,'uniform_cut_cases':results,'reconstructed_source_minor_determinants':mods,'uploaded_code_executed':False,'evidence_boundary':'The uniform recipe and symbolic argument are inherited from the new upload; graph/BFS and determinant checks are independently authored.'}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
