"""Fresh exact controls for complementary sectors and triangular support."""
from pathlib import Path
import json
O=Path(__file__).resolve().parent

def root(n,p):
 for w in range(2,p):
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0):return w
 raise ValueError('root')
def inverse(A,p):
 n=len(A);B=[r[:]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  k=next((k for k in range(j,n) if B[k][j]%p),None)
  if k is None:return None
  B[j],B[k]=B[k],B[j];v=pow(B[j][j],-1,p);B[j]=[x*v%p for x in B[j]]
  for i in range(n):
   if i==j:continue
   v=B[i][j]
   B[i]=[(x-v*y)%p for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B]
def mm(A,B,p):return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p for j in range(len(B[0]))] for i in range(len(A))]
def subtract(A,B,p):return [[(a-b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]

records=[];entries=0;weyltests=0;sparsesigns=0;negative=None
for n,p in [(3,7),(5,61),(9,19),(15,31),(21,43)]:
 w=root(n,p)
 for K in range(1,n+1):
  if n%K:continue
  M=n//K;q=pow(w,M,p)
  for a,b in [(2,3),(1,2),(2,1),(0,2)]:
   d=(1-pow(b,K,p))%p;c=pow(a,K,p);Delta=(pow(d,M,p)-pow(a,n,p))%p
   if not Delta:continue
   G=[]
   for j in range(K):
    Q=[[(int(i==t)*(1-b*pow(q,i+j,p))-a*int(i==(t+1)%n))%p for t in range(n)] for i in range(n)]
    Z=inverse(Q,p);assert Z is not None;G.append(Z)
   D=[[(d*int(i==j)-c*int(i==(j+K)%n))%p for j in range(n)] for i in range(n)]
   DI=inverse(D,p);assert DI is not None
   # Verify the polynomial inverse, including d=0/c=0.
   formula=[[sum(pow(d,M-1-t,p)*pow(c,t,p)*int(i==(j+t*K)%n) for t in range(M))*pow(Delta,-1,p)%p for j in range(n)] for i in range(n)]
   assert formula==DI
   sectors=[]
   for ell in range(K):
    R=[[sum(pow(q,-j*ell,p)*G[j][i][t] for j in range(K))*pow(K,-1,p)%p for t in range(n)] for i in range(n)]
    coeff=[1]
    for r in range(K-ell-1):
     coeff.append(coeff[-1]*a*(1-pow(q,r+ell+1,p))*pow((1-pow(q,r+1,p))%p,-1,p)%p)
    P=[[sum(coeff[r]*int(i==(t+r)%n) for r in range(K-ell))*pow(b,ell,p)*pow(q,t*ell,p)%p for t in range(n)] for i in range(n)]
    assert mm(DI,P,p)==R;entries+=n*n;sectors.append(R)
    for aa in range(n):
     for bb in range(n):
      value=sum(pow(w,-bb*t,p)*R[(t+aa)%n][t] for t in range(n))*pow(n,-1,p)%p
      allowed=bb==M*ell and aa%K<=K-1-ell
      if not allowed:assert value==0
      if a%p and b%p and d and allowed:assert value!=0
      weyltests+=1
   modes=sorted(set([0,1%K,K-1]));amplitudes=[2+r for r in range(len(modes))]
   weights=[sum(g*pow(q,-ell*j,p) for ell,g in zip(modes,amplitudes))%p for j in range(K)]
   # Raw positive-mode DFT amplitudes have u=-ell, not u=ell.
   for u in range(K):
    g=sum(weights[j]*pow(q,-u*j,p) for j in range(K))*pow(K,-1,p)%p
    expected=sum(a for ell,a in zip(modes,amplitudes) if (-ell)%K==u)%p
    assert g==expected;sparsesigns+=1
   Rw=[[sum(weights[j]*G[j][i][t] for j in range(K))*pow(K,-1,p)%p for t in range(n)] for i in range(n)]
   comb=[[sum(g*sectors[ell][i][t] for ell,g in zip(modes,amplitudes))%p for t in range(n)] for i in range(n)]
   assert Rw==comb
   if K>2 and a%p and b%p and negative is None and sectors[1]!=sectors[K-1]:negative={'N':n,'K':K,'p':p,'alpha':a,'beta':b,'claim':'Using positive raw-mode label directly as sector label changes the operator.'}
   records.append({'N':n,'K':K,'p':p,'alpha':a,'beta':b,'d':d,'max_allowed_support':n*(K+1)//2})
# Odd composite Fourier support, independently from direct trace sums.
gauss=[]
for n,p in [(3,7),(5,11),(7,29),(9,19),(11,23),(13,53),(15,31),(21,43),(25,101)]:
 w=root(n,p);gm=sum(pow(w,-j*j%n,p) for j in range(n))%p;gp=sum(pow(w,j*j%n,p) for j in range(n))%p
 assert gm*gp%p==n%p
 for a in range(n):
  for b in range(n):
   direct=sum(pow(w,(-t*t-(a+b)*t)%n,p) for t in range(n))*pow(n,-1,p)%p
   predicted=gm*pow(n,-1,p)*pow(w,(a+b)**2*pow(4,-1,n)%n,p)%p
   assert direct==predicted and direct
 gauss.append({'N':n,'p':p,'full_fourier_weyl_support':n*n,'Gauss_product':gm*gp%p})
# Characteristic two sanity control: F4 with w=x, x^2+x+1=0, N=3.
def mul4(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return c
def pow4(a,k):
 v=1
 for _ in range(k):v=mul4(v,a)
 return v
Gminus=0;Gplus=0
for j in range(3):Gminus^=pow4(2,(-j*j)%3);Gplus^=pow4(2,j*j%3)
assert mul4(Gminus,Gplus)==1
assert negative
res={'exact_cases':len(records),'sector_matrix_entries':entries,'weyl_support_coefficients_checked':weyltests,'raw_mode_sign_checks':sparsesigns,'wrong_sign_negative_control':negative,'composite_and_prime_gauss_cases':gauss,'GF4_N3_gauss_product':1,'cases':records,'policy':'All code independently authored. No supplied programs executed/imported/AST-parsed. Finite controls supplement proofs.'}
(O/'fresh_sector_extension_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='cases'},indent=2))
