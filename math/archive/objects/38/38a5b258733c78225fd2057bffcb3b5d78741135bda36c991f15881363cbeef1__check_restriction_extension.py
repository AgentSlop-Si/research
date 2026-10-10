"""New exact checks for Green principal restriction and the square-modulus chirp family."""
from pathlib import Path
import json,math
from sympy import isprime,primitive_root,factorint
p=65537

def I(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def add(A,B):return [[(a+b)%p for a,b in zip(x,y)]for x,y in zip(A,B)]
def sub(A,B):return [[(a-b)%p for a,b in zip(x,y)]for x,y in zip(A,B)]
def mul(A,B):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)]for row in A]
def diag(v):return [[v[i]if i==j else 0 for j in range(len(v))]for i in range(len(v))]
def inv(A):
 n=len(A);M=[row[:]+eye for row,eye in zip(A,I(n))]
 for j in range(n):
  k=next(k for k in range(j,n)if M[k][j])
  M[j],M[k]=M[k],M[j];v=pow(M[j][j],-1,p);M[j]=[a*v%p for a in M[j]]
  for k in range(n):
   if k!=j:
    v=M[k][j];M[k]=[(a-v*b)%p for a,b in zip(M[k],M[j])]
 return [row[n:]for row in M]
def Wmat(w,sigma):return [[w[i]if j==sigma[i]else 0 for j in range(len(w))]for i in range(len(w))]
def prod(v):
 r=1
 for a in v:r=r*a%p
 return r

def induced(w,sigma,S):
 rows=[];weights=[];lengths=[]
 for s in S:
  j=s;v=1;length=0
  while True:
   v=v*w[j]%p;j=sigma[j];length+=1
   if j in S:break
  rows.append(S.index(j));weights.append(v);lengths.append(length)
 assert sorted(rows)==list(range(len(S)))and sum(lengths)==len(w)
 assert prod(weights)==prod(w)
 seen=[];j=0
 while j not in seen:seen.append(j);j=rows[j]
 assert j==0 and len(seen)==len(S)
 return weights,rows,lengths

def green_controls():
 global p;p=65537;cases=[]
 for n in(5,6,7,9,12,16,25):
  cycles=[list(range(n)),[0]+list(range(2,n,2))+list(range(1,n,2))[::-1]]
  for order,cyc in enumerate(cycles):
   assert sorted(cyc)==list(range(n));sigma=[0]*n
   for i,j in zip(cyc,cyc[1:]+cyc[:1]):sigma[i]=j
   ss=[k*n//5 for k in range(5)];S=[ss[i]for i in(2,0,4,1,3)]
   for mode in('nonzero','two_zero','all_zero'):
    w=[2]*n
    if mode=='two_zero':w[1]=0;w[-2]=0
    if mode=='all_zero':w=[0]*n
    rho=prod(w);assert(1-rho)%p
    ww,rr,ll=induced(w,sigma,S);G=inv(sub(I(n),Wmat(w,sigma)));GG=inv(sub(I(5),Wmat(ww,rr)))
    assert [[G[i][j]for j in S]for i in S]==GG
    for mask in(False,True):
     left=[i+2 for i in range(n)];right=[3*i+1 for i in range(n)]
     if mask:left[S[1]]=0;right[S[3]]=0
     full=mul(diag(left),mul(G,diag(right)))
     local=mul(diag([left[i]for i in S]),mul(GG,diag([right[i]for i in S])))
     assert [[full[i][j]for j in S]for i in S]==local
    cases.append(dict(N=n,order=order,edge_mode=mode,selected=S,induced_permutation=rr,effective_weights=ww,arc_lengths=ll,cycle_product=rho,guard=(1-rho)%p))
 # Invalid denominator remains invalid; it is not silently admitted.
 n=7;sigma=[(i+1)%n for i in range(n)];w=[1]*n;S=[0,1,3,4,6];ww,rr,ll=induced(w,sigma,S)
 failed=[]
 for den in(sub(I(n),Wmat(w,sigma)),sub(I(5),Wmat(ww,rr))):
  try:inv(den);failed.append(False)
  except StopIteration:failed.append(True)
 assert failed==[True,True]
 return dict(prime=65537,cases=cases,Green_restriction_entries_checked=25*len(cases),endpoint_restriction_entries_checked=50*len(cases),singular_endpoint_checks=len(cases),invalid_original_and_induced_guards_rejected=True)

def gauss(n,omega):
 h=(n+1)//2;a=1;r=pow(omega,h,p);values=[]
 for j in range(n):values.append(a);a=a*r%p;r=r*omega%p
 assert a==1
 assert values==[pow(omega,h*j*j,p)for j in range(n)]
 G=sum(values)%p;Gm=sum(pow(a,-1,p)for a in values)%p
 assert G*Gm%p==n%p
 eps=1 if n%4==1 else-1;assert G*G%p==eps*n%p
 return G

def pick_field(n):
 global p
 invalid=[]
 for k in range(2,201):
  pp=k*n+1
  if not isprime(pp):continue
  p=int(pp);generator=int(primitive_root(p));omega=pow(generator,(p-1)//n,p)
  assert pow(omega,n,p)==1 and all(pow(omega,n//int(q),p)!=1 for q in factorint(n))
  G=gauss(n,omega);guard=(1+n*G)%p
  if not guard:invalid.append(dict(prime=p,omega=omega,G=G,feedback_guard=0));continue
  return omega,G,invalid
 raise AssertionError('No bounded diagnostic field found')

def block_check(n,omega,G):
 m=n//5;h=(n+1)//2;eta=pow(omega,m*m,p);assert pow(eta,5,p)==1 and eta!=1
 den=(1+n*G)%p;assert den
 fullblock=[];family=[]
 for a in range(5):
  row=[];expected=[]
  for b in range(5):
   i,j=a*m,b*m
   row.append((pow(omega,i*j,p)-G*pow(omega,(-h*(i+j)**2)%n,p)+(n*G*pow(omega,(-h*i*i)%n,p)if i==j else 0))*pow(den,-1,p)%p)
   expected.append((pow(eta,a*b,p)-G*pow(eta,(-3*(a+b)**2)%5,p)+(n*G*pow(eta,(-3*a*a)%5,p)if a==b else 0))*pow(den,-1,p)%p)
  fullblock.append(row);family.append(expected)
 assert fullblock==family
 g5=sum(pow(eta,3*j*j,p)for j in range(5))%p;assert g5*g5%p==5%p
 den5=(1+5*g5)%p
 differs=None
 if den5:
  B5=[[(pow(eta,a*b,p)-g5*pow(eta,(-3*(a+b)**2)%5,p)+(5*g5*pow(eta,(-3*a*a)%5,p)if a==b else 0))*pow(den5,-1,p)%p for b in range(5)]for a in range(5)]
  differs=fullblock!=B5
  assert differs==(n!=5)
 return dict(N=n,prime=p,omega=omega,eta=eta,G=G,g5=g5,epsilon=1 if n%4==1 else-1,feedback_guard=den,B5_guard=den5,block_differs_from_B5=differs,entries_checked=25)

def chirp_controls():
 global p
 general=[];squares=[];guard_exceptions=[]
 for m in(1,3,7,9,11,13,17,19,21):
  n=5*m;omega,G,bad=pick_field(n);guard_exceptions+=bad;general.append(block_check(n,omega,G))
 for q in(1,3,7,9,11,13):
  n=5*q*q;omega,G,bad=pick_field(n);guard_exceptions+=bad;case=block_check(n,omega,G)
  h=(n+1)//2;xi=pow(omega,5,p);small=sum(pow(xi,5*h*v*v,p)for v in range(q*q))%p
  assert small==q%p and G==q*case['g5']%p
  case.update(q=q,square_Gauss_factor=small,primitive_N_root_keeps_order=True);squares.append(case)
 # A deliberately resonant finite-field N5 case retains the failed target guard.
 p=31;root=pow(int(primitive_root(p)),6,p);bad=[]
 for j in range(1,5):
  omega=pow(root,j,p);G=gauss(5,omega)
  if(1+5*G)%p==0:
   F=[[pow(omega,i*k,p)for k in range(5)]for i in range(5)];A=diag([pow(omega,3*k*k,p)for k in range(5)])
   try:inv(add(inv(F),A));raise AssertionError('Resonant inverse incorrectly exists')
   except StopIteration:pass
   bad.append(dict(prime=p,N=5,omega=omega,G=G,feedback_guard=0))
 assert len(bad)==2
 return dict(general_odd_m_cases=general,square_modulus_cases=squares,diagnostic_field_guard_exceptions=guard_exceptions,deliberate_resonances=bad)

def modular_family_controls():
 global p;p=241;out=[]
 for k in(0,1,2,7,241):
  q=2410*k+1;n=5*q*q
  assert q%2==1 and q%5==1 and q%241==1 and n%241==5
  for exponent in(1,2,3,4):
   eta=pow(91,exponent,p);g5=sum(pow(eta,3*j*j,p)for j in range(5))%p
   assert g5*g5%p==5 and(1+5*q**3*g5)%p==(1+5*g5)%p!=0
   block=[[(pow(eta,a*b,p)-q*g5*pow(eta,(-3*(a+b)**2)%5,p)+(5*q**3*g5*pow(eta,(-3*a*a)%5,p)if a==b else 0))*pow((1+5*q**3*g5)%p,-1,p)%p for b in range(5)]for a in range(5)]
   base=[[(pow(eta,a*b,p)-g5*pow(eta,(-3*(a+b)**2)%5,p)+(5*g5*pow(eta,(-3*a*a)%5,p)if a==b else 0))*pow((1+5*g5)%p,-1,p)%p for b in range(5)]for a in range(5)]
   assert block==base
   out.append(dict(k=k,q=q,N=n,eta_residue=eta,g5_residue=g5,denominator_residue=(1+5*g5)%p,entries_checked=25))
 return out

result=dict(status='PASS',Green_restriction=green_controls(),chirp_family=chirp_controls(),explicit_modular_family=modular_family_controls(),scope='Principal restriction and explicit square-modulus congruence family; no ambient large Fourier matrices constructed.')
Path(__file__).with_name('RESTRICTION_EXTENSION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],Green_cases=len(result['Green_restriction']['cases']),Green_entries=result['Green_restriction']['Green_restriction_entries_checked'],endpoint_entries=result['Green_restriction']['endpoint_restriction_entries_checked'],general_chirp_cases=len(result['chirp_family']['general_odd_m_cases']),square_chirp_cases=len(result['chirp_family']['square_modulus_cases']),explicit_modular_cases=len(result['explicit_modular_family']),deliberate_resonances=len(result['chirp_family']['deliberate_resonances'])),indent=2))
