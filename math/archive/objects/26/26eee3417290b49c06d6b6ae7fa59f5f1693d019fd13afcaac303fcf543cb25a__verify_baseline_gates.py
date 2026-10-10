"""Auditor-authored controls. Does not read/import any uploaded program."""
import itertools,json,math,random
from functools import lru_cache
from pathlib import Path
R=random.Random(20261010)
def rank(a,p):
 a=[r[:] for r in a]; n=len(a);m=len(a[0]) if n else 0;k=0
 for j in range(m):
  q=next((q for q in range(k,n) if a[q][j]%p),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];v=pow(a[k][j],-1,p);a[k]=[x*v%p for x in a[k]]
  for q in range(n):
   if q!=k:
    v=a[q][j];a[q]=[(x-v*y)%p for x,y in zip(a[q],a[k])]
  k+=1
  if k==n:break
 return k

def moment(x,y):
 return sum(a*b*(1 if i+j>=5 else -1 if i+j==4 else 0) for i,a in enumerate(x) for j,b in enumerate(y))
verts=[]
for a in range(6):
 x0=2*a*(11-a);lo=16*max(0,11-a-8);hi=2*((a*a)//4+((11-a)**2)//4);bounds=[(lo,hi),(0,36),(0,20),(0,10)];V=set()
 for free in range(4):
  fixed=[i for i in range(4) if i!=free]
  for bits in itertools.product(range(2),repeat=3):
   v=[0]*4
   for i,z in zip(fixed,bits):v[i]=bounds[i][z]
   v[free]=110-x0-sum(v)
   if bounds[free][0]<=v[free]<=bounds[free][1]:V.add((x0,*v,11))
 verts.append(sorted(V))
assert list(map(len,verts))==[8,10,10,12,12,11]
mt=[[max(moment(x,y) for x in V for y in W) for W in verts] for V in verts]
assert max(map(max,mt))==3377 and 4*3377<121**2
@lru_cache(None)
def profiles(n,k):
 if k<0 or k>n:return frozenset()
 if n==1:return frozenset([(k,)])
 ans=set()
 for a in range(max(0,k-n//2),min(k,n//2)+1):
  for u in profiles(n//2,a):
   for v in profiles(n//2,k-a):ans.add((2*a*(k-a),*(x+y for x,y in zip(u,v))))
 return frozenset(ans)
P=profiles(32,11);assert len(P)==617;assert max(moment(x,y) for x in P for y in P)==3377
# Independent integer grid discrepancy, all unsigned coordinate-bit maps.
disc=[]
for n in [32,64]:
 m=n.bit_length()-1;survivors=[];minmax=n*n;best=[]
 for sig in itertools.permutations(range(m)):
  perm=[sum(((j>>sig[t])&1)<<t for t in range(m)) for j in range(n)]
  maximum=0
  for k in range(n+1):
   count=0
   for l in range(n+1):
    if l:count+=perm[l-1]<k
    maximum=max(maximum,abs(n*count-k*l))
  if maximum<=2*n:survivors.append(list(sig));assert sum(perm[j]<11 for j in range(21))==9
  if maximum<minmax:minmax=maximum;best=[list(sig)]
  elif maximum==minmax:best.append(list(sig))
 disc.append(dict(n=n,total=math.factorial(m),survivors=survivors,min_max_numerator=minmax,denominator=n,minimizers=best))
assert len(disc[0]['survivors'])==5 and not disc[1]['survivors'];assert disc[1]['min_max_numerator']==135
# Exact finite-field F8 tricharacter rectangle control, F32 sharp witness.
p=97;w=pow(5,12,p);assert pow(w,8,p)==1 and pow(w,4,p)!=1
F=[[pow(w,i*j,p) for j in range(8)] for i in range(8)];cases=0
for I in itertools.combinations(range(8),3):
 for J in itertools.combinations(range(8),5):assert rank([[F[i][j] for j in J] for i in I],p)==3;cases+=1
profiles8={}
for name,O in [('natural',list(range(8))),('parity',[0,2,4,6,1,3,5,7])]:
 profiles8[name]=[rank([[F[i][j] for j in O[k:]] for i in O[:k]],p) for k in range(1,8)]
assert profiles8['natural']==[1,2,3,4,3,2,1] and profiles8['parity']==[1,2,3,2,3,2,1]
w32=pow(5,3,p);W=[0,2,4,8,10,12,16,18,20,24,28];assert rank([[pow(w32,i*j,p) for j in W] for i in W],p)==5
# Raw forward/backward F4 leaf, two displayed coefficient choices.
raw=0
for p,g in [(97,5),(257,3),(17,3)]:
 ii=pow(g,(p-1)//4,p);assert ii*ii%p==p-1
 a=[0,-1,-ii,-1];b=[1,1,-1,1];c=[1,-1,-1,0];e=b;d=[-1,-3,3,-3];rows=[0,2,1,3];cols=[1,3,0,2]
 for j in range(4):
  x=[int(t==j) for t in range(4)];f=[];s=0
  for i in range(4):s=(a[i]*s+b[i]*x[i])%p;f.append(s)
  u=[0]*4;s=0
  for i in range(3,-1,-1):s=(c[i]*s+e[i]*x[i])%p;u[i]=s
  out=[(f[i]+u[i]+d[i]*x[i])%p for i in range(4)];assert out==[pow(ii,rows[i]*cols[j],p) for i in range(4)];raw+=1
# New recurrence-extension checker, arbitrary Q with Q0=1, arbitrary full states.
def conv(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c
def invseries(q,n,p):
 h=[1]
 for i in range(1,n):h.append(-sum(q[j]*h[i-j] for j in range(1,min(i,len(q)-1)+1))%p)
 return h
fusion=0
for L in [1,2,4,8,16]:
 for k in range(1,L+1):
  for H in [2,4,8]:
   q=[1]+[R.randrange(97) for _ in range(k)];q[-1]=q[-1] or 1;v=[R.randrange(97) for _ in range(L)];qv=conv(q,v,97);num=qv[:L];tail=qv[L:];h=invseries(q,H*L,97)
   target=(conv(num,h,97)+[0]*(H*L))[:H*L];ext=(conv(tail,h,97)+[0]*(H*L))[:(H-1)*L];got=v+[(-x)%97 for x in ext];assert got==target;fusion+=1
# Guarded bounded-word sum controls.
guards=0
for U in [1,3,8,17]:
 for G in [1,2,3,8,31,256]:
  q=(2*U*G).bit_length();s=64//q
  for mode in ['min','max','random']:
   rows=[[(-U if mode=='min' else U if mode=='max' else R.randrange(-U,U+1)) for _ in range(s)] for _ in range(G)]
   total=sum(sum((v+U)<<(q*j) for j,v in enumerate(row)) for row in rows);assert total<1<<64
   assert [((total>>(q*j))&((1<<q)-1))-G*U for j in range(s)]==[sum(row[j] for row in rows) for j in range(s)];guards+=1
eta=1/4+1/512+1/(2*512**2);assert 5*eta<math.sqrt(2-2/math.sqrt(32))
res={'status':'PASS','source_programs_executed':False,'F32_vertices':list(map(len,verts)),'F32_moment_table':mt,'F32_profiles':len(P),'F32_sharp_rank':5,'bit_coordinate_discrepancy':disc,'F8_rectangle_cases':cases,'F8_profiles':profiles8,'raw_F4_basis_cases':raw,'arbitrary_recurrence_macro_checks':fusion,'strict_64bit_guard_cases':guards,'five_stage_margin':math.sqrt(2-2/math.sqrt(32))-5*eta,'scope':'Finite controls support explicitly checked symbolic proofs; they are not execution of uploaded tests, whole-archive approval, numerical-stability certification or general FFT improvement.'}
Path(__file__).with_name('BASELINE_GATE_CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
