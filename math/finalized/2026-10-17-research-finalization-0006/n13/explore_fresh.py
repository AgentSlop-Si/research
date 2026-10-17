import json,itertools,time
from pathlib import Path
P=53;N=13;Q=16
OUT=Path(__file__).resolve().parent

def G(e,d,a,b):
 r=e*a%N;l=d*b%N
 if r+l>=N:return 0
 w=pow(Q,e*d%N,P);v=1
 for j in range(1,l+1):v=v*(1-pow(w,r+j,P))*pow((1-pow(w,j,P))%P,-1,P)%P
 return v

def f(a,b):return pow(Q,10*(a+b)**2%N,P)
def solve(M,B):
 a=[[x%P for x in r]+[v%P] for r,v in zip(M,B)];r=0;ps=[];n=len(M[0])
 for c in range(n):
  p=next((k for k in range(r,len(a)) if a[k][c]),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];iv=pow(a[r][c],-1,P);a[r]=[x*iv%P for x in a[r]]
  for k in range(len(a)):
   if k!=r and a[k][c]:
    v=a[k][c];a[k]=[(x-v*y)%P for x,y in zip(a[k],a[r])]
  ps.append(c);r+=1
  if r==len(a):break
 if any(not any(row[:n]) and row[n] for row in a):return None,r
 v=[0]*n
 for row,c in zip(a,ps):v[c]=row[n]
 return v,r

def trim(a):
 a=[x%P for x in a]
 while len(a)>1 and not a[-1]:a.pop()
 return a

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%P
 return trim(c)
def sub(a,b):return trim([(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def rem(a,b):
 a=trim(a);bi=pow(b[-1],-1,P)
 while len(a)>=len(b) and a!=[0]:
  c=a[-1]*bi%P;off=len(a)-len(b)
  for i,v in enumerate(b):a[off+i]=(a[off+i]-c*v)%P
  a=trim(a)
 return a

def ppow(a,n,m):
 r=[1]
 while n:
  if n&1:r=rem(mul(r,a),m)
  a=rem(mul(a,a),m);n//=2
 return r

def split(H,d):return H[0]!=0 and ppow([0,1],P**d,H)==[0,1]
def v(y,a,b):return (f(a,b)-pow(y,13-a-b,P)*G(-1,1,a,b)*pow(G(-1,1,13-b,b),-1,P))*pow(G(1,1,a,b),-1,P)%P

def family(y):
 pairs=[(1,a) for a in range(1,5)]+[(2,a) for a in (2,3)]
 E=[[v(y,a+j,b) for j in range(8)] for b,a in pairs]
 base,r=solve([r[:6] for r in E],[-r[7] for r in E]);delta,_=solve([r[:6] for r in E],[-r[6] for r in E]);assert r==6
 return base+[0,1],delta+[1,0]

def gate(y,z,B,D):
 U=[0]*10;V=[0]*10
 for a in range(1,10):
  U[a]=(f(a,3)-pow(y,10-a,P)*G(-1,1,a,3)*pow(G(-1,1,10,3),-1,P))*pow(G(1,1,a,3),-1,P)%P
  V[a]=pow(z,a,P)*G(1,-1,a,3)*pow(G(1,1,a,3),-1,P)%P
 rows=[]
 for s in (1,2):
  ee=[sum(h[j]*U[s+j] for j in range(8))%P for h in (B,D)]
  ff=[sum(h[j]*V[s+j] for j in range(8))%P for h in (B,D)]
  rows.append((ee,ff))
 R=sub(mul(rows[0][0],rows[1][1]),mul(rows[1][0],rows[0][1]))
 return R,rows

def peval(a,x):
 s=0
 for c in a[::-1]:s=(s*x+c)%P
 return s

def quotient(H):return [rem([0]*a+[1],H)+[0]*7 for a in range(13)]
def full(y,z,H,K):
 RH=quotient(H);RK=quotient(K);ans=[]
 for b in range(13):
  M=[]
  for a in range(13):
   M.append([G(1,1,a,b)*x%P for x in RH[a][:7]]+[G(-1,1,a,b)*pow(y,-a%13,P)%P,G(1,-1,a,b)*pow(z,a,P)%P]+[G(-1,-1,a,b)*x%P for x in RK[-a%13][:7]])
  sol,rank=solve(M,[f(a,b) for a in range(13)])
  if sol is None:return None
  ans.append({'b':b,'rank':rank,'solution':sol})
 return ans

if __name__=='__main__':
 t=time.time();fam={y:family(y) for y in range(1,P)};cs={};stats={'pairs':0,'gates_zero':0,'eligible_by_d':{d:0 for d in (2,3,4)}}
 for y,z in itertools.product(range(1,P),repeat=2):
  B,D=fam[y];R,rows=gate(y,z,B,D);stats['pairs']+=1;stats['gates_zero']+=R==[0]
  c=[]
  for l in range(P):
   if peval(R,l):continue
   E=[peval(x[0],l) for x in rows];F=[peval(x[1],l) for x in rows]
   if F==[0,0] and E!=[0,0]:continue
   H=[(a+l*b)%P for a,b in zip(B,D)]
   ds=[d for d in (2,3,4) if split(H,d)]
   if ds:
    for d in ds:stats['eligible_by_d'][d]+=1
    c.append({'lambda':l,'H':H,'degrees':ds})
  cs[y,z]=c
 print('STATS',stats,'elapsed',time.time()-t,flush=True)
 witnesses=[]
 for y,z in itertools.product(range(1,P),repeat=2):
  for h,k in itertools.product(cs[y,z],cs[z,y]):
   ds=set(h['degrees'])&set(k['degrees'])
   if not ds:continue
   sol=full(y,z,h['H'],k['H'])
   if sol:
    w={'y':y,'z':z,'positive':h,'negative':k,'degrees':sorted(ds),'sectors':sol};witnesses.append(w)
    print('WITNESS',y,z,h['lambda'],k['lambda'],ds,flush=True)
    (OUT/'FIRST_WITNESS.json').write_text(json.dumps(w,indent=2))
    if 2 in ds:break
  if witnesses and 2 in witnesses[-1]['degrees']:break
 out={'stats':stats,'witnesses':witnesses,'eligible':{f'{y},{z}':v for (y,z),v in cs.items() if v},'elapsed_seconds':time.time()-t}
 (OUT/'EXPLORATION.json').write_text(json.dumps(out,indent=2));print('DONE',len(witnesses),'elapsed',time.time()-t,flush=True)
