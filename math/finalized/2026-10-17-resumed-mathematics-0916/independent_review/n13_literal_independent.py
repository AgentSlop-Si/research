"""Fresh, separate literal verifier. Imports only this cycle's self-authored verifier."""
import json, hashlib
from pathlib import Path
import n13_independent as own
P=53;N=13;Q=16
BASE=Path(__file__).parent
w=json.loads((BASE/'N13_ENUMERATION.json').read_text())['full_sector_witnesses'][0]
H=w['H'];D=7
ZERO=(0,)*D;ONE=(1,)+(0,)*(D-1)
def elt(n):return (n%P,)+(0,)*(D-1)
def add(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def neg(a):return tuple((-x)%P for x in a)
def sub(a,b):return add(a,neg(b))
def sc(a,n):return tuple(x*n%P for x in a)
def mul(a,b):
 if not any(a[1:]):return sc(b,a[0])
 if not any(b[1:]):return sc(a,b[0])
 c=[0]*(2*D-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 for k in range(2*D-2,D-1,-1):
  z=c[k]%P
  for j in range(D):c[k-D+j]-=z*H[j]
 return tuple(x%P for x in c[:D])
def power(a,n):
 z=ONE
 while n:
  if n&1:z=mul(z,a)
  a=mul(a,a);n//=2
 return z
def inv(a):
 assert a!=ZERO
 if not any(a[1:]):return elt(pow(a[0],-1,P))
 z=power(a,P**D-2);assert mul(z,a)==ONE;return z
def ev(h,a):
 z=ZERO
 for c in reversed(h):z=add(mul(z,a),elt(c))
 return z
u=(0,1,0,0,0,0,0); roots=[];x=u
for k in range(D):roots.append(x);x=power(x,P)
assert x==u and len(set(roots))==D and ZERO not in roots
assert all(ev(H,a)==ZERO for a in roots)
# Multiply actual root factors in the field.
factors=[ONE]
for a in roots:
 out=[ZERO]*(len(factors)+1)
 for i,c in enumerate(factors):out[i]=sub(out[i],mul(c,a));out[i+1]=add(out[i+1],c)
 factors=out
assert factors==[elt(x) for x in H]
V=[[power(a,k) for a in roots] for k in range(D)]
Z=[row[:]+[ONE if i==j else ZERO for j in range(D)] for i,row in enumerate(V)]
for k in range(D):
 t=next(i for i in range(k,D) if Z[i][k]!=ZERO);Z[k],Z[t]=Z[t],Z[k]
 ci=inv(Z[k][k]);Z[k]=[mul(ci,x) for x in Z[k]]
 for i in range(D):
  if i!=k:
   c=Z[i][k];Z[i]=[sub(x,mul(c,y)) for x,y in zip(Z[i],Z[k])]
VI=[r[D:] for r in Z]
for i in range(D):
 for j in range(D):
  s=ZERO
  for k in range(D):s=add(s,mul(V[i][k],VI[k][j]))
  assert s==(ONE if i==j else ZERO)
banks=[]
for e,d,nodes in [(1,1,roots),(-1,1,[elt(w['y'])]),(1,-1,[elt(w['y'])]),(-1,-1,roots)]:
 for a in nodes:banks.append({'epsilon':e,'delta':d,'alpha':a,'beta':ONE,'amplitudes':[]})
for sect in w['sectors']:
 s=sect['solution']; amps=[]
 for off in (0,9):
  aa=[]
  for row in VI:
   v=ZERO
   for c,t in zip(row,s[off:off+7]):v=add(v,sc(c,t))
   aa.append(v)
  amps.append(aa)
 vals=amps[0]+[elt(s[7]),elt(s[8])]+amps[1]
 for bank,a in zip(banks,vals):bank['amplitudes'].append(a)
for bank in banks:
 a=bank['alpha'];e=bank['epsilon'];guard=neg(power(a,13));bank['guard']=guard;assert guard!=ZERO
 ww=[]
 for j in range(N):
  v=ZERO
  for b,amp in enumerate(bank['amplitudes']):v=add(v,sc(amp,pow(Q,(-e*b*j)%13,P)))
  ww.append(sc(mul(guard,v),7))
 bank['raw_weights']=ww
# Literal cyclic-bidiagonal inverse by backward substitution from its unique zero diagonal.
# This is independent of the author's Gauss-Jordan inversion strategy.
def inverse_branch(alpha,e,d,j):
 diag=[(1-pow(Q,(e*d*j+d*t)%13,P))%P for t in range(N)]
 t0=next(t for t,v in enumerate(diag) if v==0);assert diag.count(0)==1
 ai=inv(alpha);M=[[ZERO]*N for _ in range(N)]
 for col in range(N):
  x=[ZERO]*N; t=(t0-e)%N;x[t]=neg(ai) if col==t0 else ZERO
  for step in range(N-1):
   v=sc(x[t],diag[t])
   if t==col:v=sub(v,ONE)
   nt=(t-e)%N;x[nt]=mul(ai,v);t=nt
  for r in range(N):M[r][col]=x[r]
 for r in range(N):
  for c in range(N):
   left=sub(sc(M[r][c],diag[r]),mul(alpha,M[(r-e)%N][c]))
   right=sub(sc(M[r][c],diag[c]),mul(alpha,M[r][(c+e)%N]))
   expect=ONE if r==c else ZERO
   assert left==expect and right==expect
 return M
aggregate=[[ZERO]*N for _ in range(N)];branch_count=0;nonzero=0;altered=None
for bi,bank in enumerate(banks):
 bm=[[ZERO]*N for _ in range(N)]
 for j,weight in enumerate(bank['raw_weights']):
  M=inverse_branch(bank['alpha'],bank['epsilon'],bank['delta'],j);branch_count+=1
  for r in range(N):
   for c in range(N):bm[r][c]=add(bm[r][c],sc(mul(weight,M[r][c]),pow(13,-1,P)))
  if bi==15 and j==12:altered=M
 assert any(v!=ZERO for row in bm for v in row);nonzero+=1
 for r in range(N):
  for c in range(N):aggregate[r][c]=add(aggregate[r][c],bm[r][c])
expected=[[elt(pow(Q,(-r*c)%13,P)) for c in range(N)] for r in range(N)]
assert aggregate==expected
wrong_sign=sum(aggregate[r][c]!=elt(pow(Q,r*c%13,P)) for r in range(N) for c in range(N))
wrong_norm=sum(sc(aggregate[r][c],13)!=expected[r][c] for r in range(N) for c in range(N))
perturbed=sum(add(aggregate[r][c],sc(altered[r][c],pow(13,-1,P)))!=expected[r][c] for r in range(N) for c in range(N))
assert wrong_sign and wrong_norm and perturbed
cert={'modulus_ascending':H,'roots':roots,'banks':banks,'aggregate':aggregate,'y':w['y'],'lambda':w['lambda']}
(BASE/'N13_LITERAL_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
receipt={'status':'PASS','method':'independent root/Frobenius product, field Vandermonde solve, zero-diagonal cyclic backward branch inversion, both-sided sparse multiplication, all-entry literal sum','degree':7,'roots':len(roots),'banks':len(banks),'branches':branch_count,'two_sided_inverse_identities':2*branch_count,'nonzero_banks':nonzero,'target_entries':169,'negative_controls':{'wrong_sign_mismatches':wrong_sign,'missing_average_mismatches':wrong_norm,'altered_weight_mismatches':perturbed},'scope':'exact fixed N13 original signed bank grammar; inherited universal lower bound needed to infer exact16; no unrestricted allocations or runtime claim'}
(BASE/'N13_LITERAL_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
