import sympy as S,json,time
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
from sympy.polys.groebnertools import groebner
z=S.Symbol('z');root=S.CRootOf(z**4+1,3);K=QQ.algebraic_field(root);Z=K.unit
R,*v=ring('t0,t1,t2,t3,w',K,order='grevlex');t0,t1,a,b,w=v
E=[]
for f in json.load(open('adjacent_anchor_construction_0304/reduced_resultants.json')):
 E.append(R.from_dict({tuple(ex):sum(K(num)/K(den)*Z**j for j,(num,den) in enumerate(cs))for ex,cs in f}))
def numsub(f,idx,n,d):
 deg=f.degree(v[idx]);out=R.zero
 for e,c in f.items():
  ee=list(e);power=ee[idx];ee[idx]=0
  out+=R.from_dict({tuple(ee):c})*n**power*d**(deg-power)
 return out

def split(f,idx):
 const=R.zero;lin=R.zero
 for e,c in f.items():
  ee=list(e);power=ee[idx];ee[idx]=0
  assert power<2
  if power:lin+=R.from_dict({tuple(ee):c})
  else:const+=R.from_dict({tuple(ee):c})
 return -const,lin

def out(name,f):
 print(name,'terms',len(f),'degree',max(map(sum,f),default=0),flush=True)
 print('  ',f,flush=True)

def clean(f,guards):
 for d in guards:
  if d and not d.is_ground:
   while f and not f.rem(d):f=f.exquo(d)
 return f.monic() if f else f
N1,D1=split(E[2],1);out('t1 numerator',N1);out('t1 denominator',D1)
S1=[numsub(f,1,N1,D1) for f in E]
Nw,Dw=split(S1[4],4)
common=Nw.gcd(Dw);Nw=Nw.exquo(common);Dw=Dw.exquo(common)
out('w numerator',Nw);out('w denominator',Dw);out('w cancelled',common)
S2=[clean(numsub(f,4,Nw,Dw),[D1,Dw,common]) for f in S1]
N0,D0=split(S2[3],0);common0=N0.gcd(D0);N0=N0.exquo(common0);D0=D0.exquo(common0)
out('t0 numerator',N0);out('t0 denominator',D0);out('t0 cancelled',common0)
S3=[clean(numsub(f,0,N0,D0),[D1,Dw,D0,common,common0]) for f in S2]
RR,A,B=ring('a,b',K,order='grevlex')
FF=[]
for j,f in enumerate(S3):
 ff=RR.from_dict({(e[2],e[3]):c for e,c in f.items()});FF.append(ff);out('FINAL'+str(j),ff)
print('GROEBNER START',time.time(),flush=True)
G=groebner([f for f in FF if f],RR,method='buchberger');print('GROEBNER DONE',time.time(),len(G),flush=True)
for g in G:out('G',g)
