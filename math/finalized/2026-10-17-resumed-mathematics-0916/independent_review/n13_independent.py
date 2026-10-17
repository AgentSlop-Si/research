"""Fresh independent verifier, authored 2026-10-17; imports no research code."""
import json, hashlib
from pathlib import Path
P=53; N=13; Q=16

def trim(a):
 a=[x%P for x in a]
 while len(a)>1 and not a[-1]: a.pop()
 return a

def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=x
 return trim(c)

def neg(a):return [(-x)%P for x in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)

def rem(a,b):
 a=trim(a[:]); b=trim(b[:]); inv=pow(b[-1],-1,P)
 while len(a)>=len(b) and a!=[0]:
  d=len(a)-len(b); c=a[-1]*inv%P
  for j,x in enumerate(b):a[d+j]=(a[d+j]-c*x)%P
  a=trim(a)
 return a

def ppower(a,n,m):
 z=[1]
 while n:
  if n&1:z=rem(mul(z,a),m)
  a=rem(mul(a,a),m); n//=2
 return z

def gcd(a,b):
 while b!=[0]:a,b=b,rem(a,b)
 return [(x*pow(a[-1],-1,P))%P for x in a]

def solve(a,b):
 m=len(a); n=len(a[0]); z=[a[i][:]+[b[i]%P] for i in range(m)]; piv=[];r=0
 for c in range(n):
  t=next((i for i in range(r,m) if z[i][c]%P),None)
  if t is None:continue
  z[r],z[t]=z[t],z[r];k=pow(z[r][c]%P,-1,P);z[r]=[v*k%P for v in z[r]]
  for i in range(m):
   if i!=r:
    k=z[i][c]%P
    if k:z[i]=[(x-k*y)%P for x,y in zip(z[i],z[r])]
  piv.append(c);r+=1
  if r==m:break
 if any(not any(row[:n]) and row[n] for row in z):return None,r
 x=[0]*n
 for i,c in enumerate(piv):x[c]=z[i][n]
 return x,r

# G is reconstructed by a Pascal recurrence, not copied product code.
GB={}
for w in (Q,pow(Q,-1,P)):
 d={(0,0):1}
 for n in range(1,13):
  for k in range(n+1):d[n,k]=(d.get((n-1,k-1),0)+pow(w,k,P)*d.get((n-1,k),0))%P
 GB[w]=d

def G(e,d,a,b):
 r=e*a%N; l=d*b%N
 return GB[pow(Q,e*d%N,P)].get((r+l,l),0) if r+l<N else 0

def f(a,b):return pow(Q,10*(a+b)**2%N,P)
def v(a,b,y):return (f(a,b)-pow(y,13-a-b,P)*G(-1,1,a,b)*pow(G(-1,1,13-b,b),-1,P))*pow(G(1,1,a,b),-1,P)%P

def affine(y):
 rows=[(b,a) for b in (1,2) for a in range(b,13-b-7)]
 assert rows==[(1,1),(1,2),(1,3),(1,4),(2,2),(2,3)]
 a=[[v(x+j,b,y) for j in range(6)] for b,x in rows]
 c,r=solve(a,[-v(x+7,b,y) for b,x in rows]);s,r2=solve(a,[-v(x+6,b,y) for b,x in rows])
 assert r==r2==6 and c is not None and s is not None
 return c+[0],s+[1]

def irreducible7(h):
 x=[0,1]; a=ppower(x,P,h)
 if gcd(h,sub(a,x))!=[1]:return False
 for k in range(6):a=ppower(a,P,h)
 return a==x

def sectors(h,y):
 powers=[ppower([0,1],r,h)+[0]*7 for r in range(13)];powers=[x[:7] for x in powers]
 answers=[]
 for b in range(13):
  mat=[]
  for a in range(13):
   mat.append([G(1,1,a,b)*c%P for c in powers[a]]+[G(-1,1,a,b)*pow(y,-a%13,P)%P,G(1,-1,a,b)*pow(y,a,P)%P]+[G(-1,-1,a,b)*c%P for c in powers[-a%13]])
  sol,rank=solve(mat,[f(a,b) for a in range(13)])
  if sol is None:return None
  assert all(sum(t*u for t,u in zip(row,sol))%P==f(a,b) for a,row in enumerate(mat))
  answers.append({'b':b,'rank':rank,'solution':sol})
 return answers

def main():
 pairs=0; irreducible=[];witnesses=[]
 for y in range(1,53):
  c,s=affine(y)
  for lam in range(53):
   pairs+=1;h=[(a+lam*b)%P for a,b in zip(c,s)]+[1]
   if irreducible7(h):
    irreducible.append([y,lam]);ss=sectors(h,y)
    if ss is not None:witnesses.append({'y':y,'lambda':lam,'H':h,'sectors':ss})
 result={'independent':True,'pairs':pairs,'irreducible_pairs':irreducible,'full_sector_witnesses':witnesses,'pinned_affine':affine(1),'scope':'y=z in F53*, lambda in F53, shared H monic irreducible degree7, allocation (7,1,1,7), beta=1; quotient-sector check only; raw operator verification pending'}
 Path(__file__).with_name('N13_ENUMERATION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'pairs':pairs,'irreducible':len(irreducible),'witnesses':len(witnesses),'first_witness':witnesses[:1]},indent=2))
if __name__=='__main__':main()
