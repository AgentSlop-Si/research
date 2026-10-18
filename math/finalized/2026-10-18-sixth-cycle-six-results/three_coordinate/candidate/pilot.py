"""Fresh exact finite-field diagnostics; never interpreted as characteristic-zero exclusion."""
import json,itertools,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHART=json.loads((ROOT/'sources/CHART.json').read_text())
p=1000000009
imag=569522298
ZERO=(0,0,0)
def add(a,b,sgn=1):
 c=a.copy()
 for e,v in b.items():
  c[e]=(c.get(e,0)+sgn*v)%p
  if not c[e]:del c[e]
 return c
def scale(a,v):return {e:x*v%p for e,x in a.items() if x*v%p}
def mul(a,b):
 c={}
 for e,v in a.items():
  for f,w in b.items():
   g=tuple(e[k]+f[k] for k in range(3));c[g]=(c.get(g,0)+v*w)%p
 return {e:v for e,v in c.items() if v}
def mon(e,v=1):return {e:v%p}
def mm(A,B):
 return [[sum_poly(mul(A[r][k],B[k][c]) for k in range(8)) for c in range(8)] for r in range(8)]
def sum_poly(ps):
 a={}
 for b in ps:a=add(a,b)
 return a
def branch(s,b,label,im):
 stage=CHART['stages'][s];cycle=stage['cycles'][b];weights=[]
 for j in range(8):
  edge=b*8+j
  if edge<7:v=1
  else:
   a,bb=stage['gaussian_pairs'][edge-7];v=(a+im*bb)*pow((a-im*bb)%p,-1,p)%p
  e=list(ZERO)
  if (s,edge) in label:e[label.index((s,edge))]=1
  weights.append(mon(tuple(e),v))
 h={ZERO:1}
 for w in weights:h=mul(h,w)
 d=add({ZERO:1},h,-1)
 H=[[{} for j in range(8)]for i in range(8)]
 for a in range(8):
  val={ZERO:1};H[cycle[a]][cycle[a]]=val
  for ell in range(1,8):
   j=(a+ell)%8;val=mul(weights[j],val);H[cycle[j]][cycle[a]]=val
 return H,d
def numerator(label,im):
 stages=[];active=[];allguards=[]
 for s in range(2):
  bs=[branch(s,b,label,im)for b in range(3)]
  A=[[{}for j in range(8)]for i in range(8)]
  for b,(H,d) in enumerate(bs):
   allguards.append(d)
   if len(d)>1:active.append(d)
   other={ZERO:1}
   for bb,(_,dd)in enumerate(bs):
    if bb!=b:other=mul(other,dd)
   for r in range(8):
    for c in range(8):A[r][c]=add(A[r][c],mul(H[r][c],other))
  stages.append(A)
 return mm(stages[1],stages[0]),active,allguards
def divide_binomial(P,d):
 lead=max(d);lc=d[lead];R=P.copy();Q={}
 while R:
  e=max(R)
  if not all(e[k]>=lead[k]for k in range(3)):break
  f=tuple(e[k]-lead[k]for k in range(3));v=R[e]*pow(lc,-1,p)%p;Q[f]=v
  R=add(R,mul(mon(f,v),d),-1)
 assert not R,('nonexact division',R)
 return Q
def system(label,all_windows=False):
 N,active,guards=numerator(label,imag);Nc,_,_=numerator(label,-imag)
 Nt=[[{tuple(1-e[k]for k in range(3)):v for e,v in Nc[r][c].items()}for c in range(8)]for r in range(8)]
 Q=[]
 rowpairs=list(itertools.combinations(range(8),2))if all_windows else [(0,r)for r in range(1,8)]
 for a,r in rowpairs:
  for b,c in rowpairs:
   P=add(mul(mul(N[r][c],N[a][b]),mul(Nt[r][c],Nt[a][b])),mul(mul(N[r][b],N[a][c]),mul(Nt[r][b],Nt[a][c])),-1)
   q=P
   for d in active:q=divide_binomial(q,d)
   check=q
   for d in active:check=mul(check,d)
   assert check==P
   Q.append(q)
 F={ZERO:1}
 for d in active:F=mul(F,d)
 return Q,F,guards
def rank(polys,extra=None):
 cols=sorted(set().union(*(q.keys()for q in polys),extra.keys()if extra else set()))
 rows=[[q.get(e,0)for e in cols]for q in polys];R=[];piv=[];chosen=[]
 for j,row in enumerate(rows):
  for r,k in zip(R,piv):
   a=row[k]
   if a:row=[(v-a*w)%p for v,w in zip(row,r)]
  k=next((k for k,v in enumerate(row)if v),None)
  if k is None:continue
  a=pow(row[k],-1,p);row=[v*a%p for v in row]
  R.append(row);piv.append(k);chosen.append(j)
 if extra is None:return len(R),len(cols),chosen,[cols[k]for k in piv]
 row=[extra.get(e,0)for e in cols]
 for r,k in zip(R,piv):
  a=row[k]
  if a:row=[(v-a*w)%p for v,w in zip(row,r)]
 return len(R),len(cols),not any(row)
def kind(L):
 ss=[s for s,e in L]
 if len(set(ss))==1:
  cnt=sorted([sum(e//8==b for s,e in L)for b in range(3)],reverse=True)
  return 'same_stage_'+''.join(map(str,cnt))
 pair=[(s,e)for s,e in L if ss.count(s)==2]
 return 'mixed_same_branch_pair'if pair[0][1]//8==pair[1][1]//8 else'mixed_different_branch_pair'
def main():
 reps=[[(0,16),(0,17),(0,18)],[(0,8),(0,9),(0,7)],[(0,8),(0,9),(0,16)],[(0,8),(0,9),(1,7)],[(0,7),(0,8),(1,7)],[(0,8),(0,16),(1,8)]]
 out=[]
 for L in reps:
  st=time.time();Q,F,guards=system(L)
  tests=[];power={ZERO:1}
  for k in range(4):
   tests.append([k,*rank(Q,power)]);power=mul(power,F)
  mult=[mul(q,mon(e))for e in [ZERO,(1,0,0),(0,1,0),(0,0,1)]for q in Q]
  result={'label':L,'kind':kind(L),'base':tests,'affine_F':rank(mult,F),'seconds':time.time()-st}
  out.append(result);print(json.dumps(result),flush=True)
 (ROOT/'PILOT.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
