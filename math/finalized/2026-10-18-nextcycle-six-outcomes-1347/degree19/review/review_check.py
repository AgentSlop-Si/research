#!/usr/bin/env python3
"""Independent degree-19 inert-certificate review. Arithmetic and literal-power method adapted from the byte-bound degree-17 independent reviewer. No candidate code is imported or run."""
import hashlib, json, math, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
IN=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'inputs'
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT
P,D,N=53,19,13
HMOD=[12,1]+[0]*17+[1]
Z=(0,)*D; O=(1,)+(0,)*(D-1)
def trim(a):
 a=[x%P for x in a]
 while a and not a[-1]:a.pop()
 return a
def pa(a,b,sgn=1):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=sgn*x
 return trim(c)
def pm(a,b):
 if not a or not b:return []
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%P
 return trim(c)
def pdiv(a,b):
 a=trim(a); b=trim(b);assert b
 q=[0]*max(0,len(a)-len(b)+1);lead=pow(b[-1],-1,P)
 while len(a)>=len(b):
  k=len(a)-len(b);v=a[-1]*lead%P;q[k]=v
  for j,x in enumerate(b):a[k+j]=(a[k+j]-v*x)%P
  a=trim(a)
 return trim(q),a
def pgcd(a,b):
 while b:a,b=b,pdiv(a,b)[1]
 return trim([x*pow(a[-1],-1,P) for x in a])
def ppow(a,n):
 r=[1]
 while n:
  if n&1:r=pdiv(pm(r,a),HMOD)[1]
  a=pdiv(pm(a,a),HMOD)[1];n>>=1
 return r
def padded(a):return tuple(a)+((0,)*(D-len(a)))
def const(n):return (n%P,)+(0,)*(D-1)
def add(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def sub(a,b):return tuple((x-y)%P for x,y in zip(a,b))
def sc(a,n):return tuple(x*n%P for x in a)
def mul(a,b):
 if a==Z or b==Z:return Z
 if not any(a[1:]):return sc(b,a[0])
 if not any(b[1:]):return sc(a,b[0])
 # Integer convolution, carry-free because 19*52^2 < 2^16.
 aa=sum(x<<(16*i) for i,x in enumerate(a));bb=sum(x<<(16*i) for i,x in enumerate(b));cc=aa*bb
 c=[(cc>>(16*i))&65535 for i in range(2*D-1)]
 # Reduce u^k = -u^(k-D+1)-12u^(k-D), largest degree first.
 for k in range(2*D-2,D-1,-1):c[k-D+1]-=c[k];c[k-D]-=12*c[k]
 return tuple(x%P for x in c[:D])
def powf(a,n):
 r=O
 while n:
  if n&1:r=mul(r,a)
  a=mul(a,a);n>>=1
 return r
def inv(a):
 assert a!=Z
 r0,r1=HMOD[:],trim(list(a));t0,t1=[],[1]
 while r1:
  q,r=pdiv(r0,r1);r0,r1=r1,r;t0,t1=t1,pa(t0,pm(q,t1),-1)
 assert len(r0)==1
 result=padded(pdiv(trim([v*pow(r0[0],-1,P) for v in t0]),HMOD)[1])
 assert mul(a,result)==O
 return result
def fsum(xs):
 s=Z
 for x in xs:s=add(s,x)
 return s
def gcoef(e,d,a,b):
 r=e*a%N;l=d*b%N
 if r+l>=N:return 0
 g=1
 for i in range(1,r+1):g=g*(1-pow(16,e*d*(l+i)%N,P))*pow((1-pow(16,e*d*i%N,P))%P,-1,P)%P
 return g

def main():
 data_bytes=(IN/'DEGREE19_LITERAL_CERTIFICATE.json').read_bytes()
 assert hashlib.sha256(data_bytes).hexdigest()=='b10199e01e9e7775c78bf34b6cac41ce8d1e90280a013f0a2b21b4c1dcd9a09e'
 data=json.loads(data_bytes)
 assert data['field_modulus_ascending']==HMOD and data['degree']==D and data['characteristic']==P
 assert all(P%k for k in range(2,math.isqrt(P)+1))
 assert all(D%k for k in range(2,math.isqrt(D)+1))
 # Complete prime-polynomial field proof precedes every extension inverse.
 frob=[0,1];remainders=[]
 for i in range(D):frob=ppow(frob,P);remainders.append(frob)
 assert D*52**2 < 65536
 assert frob==[0,1] and pgcd(HMOD,pa(remainders[0],[0,1],-1))==[1]
 assert pow(16,N,P)==1 and all(pow(16,i,P)!=1 for i in range(1,N))
 # Differential arithmetic tests against ordinary convolution/long division.
 basis=[tuple(int(i==j) for i in range(D)) for j in range(D)]
 rng=random.Random(202610181335)
 pairs=[(a,b) for a in basis for b in basis]+[(tuple(rng.randrange(P) for _ in range(D)),tuple(rng.randrange(P) for _ in range(D))) for _ in range(100)]
 for a,b in pairs:assert mul(a,b)==padded(pdiv(pm(list(a),list(b)),HMOD)[1])
 def elem(a):assert isinstance(a,list) and len(a)==D and all(type(x)is int and 0<=x<P for x in a)
 for a in [data['y'],data['z']]+data['roots']+data['H']:elem(a)
 assert len(data['matrix'])==N and all(len(r)==N for r in data['matrix'])
 for row in data['matrix']:
  for a in row:elem(a)
 roots=list(map(tuple,data['roots']));h=list(map(tuple,data['H']))
 assert len(roots)==len(set(roots))==7 and Z not in roots and len(h)==8 and h[-1]==O and h[0]!=Z
 product=[O]
 for r in roots:
  c=[Z]*(len(product)+1)
  for i,a in enumerate(product):c[i]=sub(c[i],mul(a,r));c[i+1]=add(c[i+1],a)
  product=c
 assert product==h
 frob_roots=[powf(r,P) for r in roots];assert set(frob_roots)!=set(roots) and any(any(a[1:]) for a in h)
 y,z=tuple(data['y']),tuple(data['z']);assert y==z and any(y[1:])
 # Direct exact Frobenius periods, beyond merely nonbase coordinates.
 orbit_lengths=[]
 for node in roots+[y,z]:
  orbit=[];v=node
  while v not in orbit:
   orbit.append(v);v=powf(v,P)
  assert v==node and len(orbit)==D
  orbit_lengths.append(len(orbit))
 gamma=sum(pow(16,-t*t%N,P) for t in range(N))*pow(N,-1,P)%P;assert gamma==7
 gamma_inv=pow(gamma,-1,P);ninv=pow(N,-1,P)
 for a in range(N):
  for b in range(N):
   target_coefficient=sum(pow(16,(-(t+a)*t-b*t)%N,P) for t in range(N))*ninv%P
   assert target_coefficient==gamma*pow(16,10*(a+b)**2%N,P)%P
 banks=data['banks'];assert len(banks)==16
 supports={};total=[[Z]*N for _ in range(N)];nonzero=[];inverse_hashes=[];bank_hashes=[];power_tables=[]
 for bi,bank in enumerate(banks):
  e,d=bank['epsilon'],bank['delta'];assert type(e)is int and type(d)is int and e in (-1,1) and d in (-1,1) and type(bank['beta'])is int and bank['beta']==1
  assert len(bank['amplitudes'])==len(bank['weights'])==N
  for a in [bank['alpha'],bank['guard']]+bank['amplitudes']+bank['weights']:elem(a)
  alpha=tuple(bank['alpha']);assert alpha!=Z;supports.setdefault((e,d),[]).append(alpha)
  aps=[O]
  for k in range(N):aps.append(mul(aps[-1],alpha))
  power_tables.append(aps)
  guard=sc(aps[N],-1);assert guard!=Z and guard==tuple(bank['guard']);gi=inv(guard)
  weights=list(map(tuple,bank['weights']));amps=list(map(tuple,bank['amplitudes']))
  for j in range(N):assert weights[j]==mul(sc(guard,gamma),fsum(sc(amps[b],pow(16,-e*b*j%N,P)) for b in range(N)))
  for b in range(N):assert amps[b]==sc(mul(gi,fsum(sc(weights[j],pow(16,e*b*j%N,P)) for j in range(N))),ninv*gamma_inv)
  B=[[Z]*N for _ in range(N)]
  for j,w in enumerate(weights):
   diag=[pow(16,(e*d*j+d*r)%N,P) for r in range(N)]
   power=[[O if r==c else Z for c in range(N)] for r in range(N)]
   geometric=[[Z]*N for _ in range(N)]
   for k in range(N):
    geometric=[[add(geometric[r][c],power[r][c]) for c in range(N)] for r in range(N)]
    power=[[add(mul(alpha,power[(r-e)%N][c]),sc(power[r][c],diag[r])) for c in range(N)] for r in range(N)]
   lam=add(aps[N],O)
   assert all(power[r][c]==(lam if r==c else Z) for r in range(N) for c in range(N))
   V=[[mul(gi,geometric[r][c]) for c in range(N)] for r in range(N)]
   for r in range(N):
    for c in range(N):
     target=O if r==c else Z
     assert sub(sc(V[r][c],1-diag[r]),mul(alpha,V[(r-e)%N][c]))==target
     assert sub(sc(V[r][c],1-diag[c]),mul(alpha,V[r][(c+e)%N]))==target
     B[r][c]=add(B[r][c],sc(mul(w,V[r][c]),ninv))
   inverse_hashes.append(hashlib.sha256(json.dumps(V,separators=(',',':')).encode()).hexdigest());last=V
  nonzero.append(sum(x!=Z for row in B for x in row));assert nonzero[-1]>0
  for a in range(N):
   for b in range(N):
    weyl=sc(fsum(sc(B[(t+a)%N][t],pow(16,-b*t%N,P)) for t in range(N)),ninv)
    assert weyl==sc(mul(aps[e*a%N],amps[b]),gamma*gcoef(e,d,a,b))
  total=[[add(total[r][c],B[r][c]) for c in range(N)] for r in range(N)]
  bank_hashes.append(hashlib.sha256(json.dumps(B,separators=(',',':')).encode()).hexdigest())
  print('bank',bi+1,'passes all literal and Weyl identities',flush=True)
 assert {k:len(v) for k,v in supports.items()}=={(1,1):7,(-1,1):1,(1,-1):1,(-1,-1):7}
 assert set(supports[(1,1)])==set(supports[(-1,-1)])==set(roots)
 assert supports[(-1,1)]==[y] and supports[(1,-1)]==[z]
 control=[0,0,0]
 for r in range(N):
  for c in range(N):
   target=const(pow(16,-r*c%N,P));assert total[r][c]==target==tuple(data['matrix'][r][c])
   control[0]+=sc(total[r][c],N)!=target
   control[1]+=total[r][c]!=const(pow(16,r*c%N,P))
   control[2]+=add(total[r][c],sc(last[r][c],ninv))!=target
 assert control==[169,144,91]
 ranks=[]
 for b in range(N):
  A=[[sc(power_tables[i][bank['epsilon']*a%N],gcoef(bank['epsilon'],bank['delta'],a,b)) for i,bank in enumerate(banks)] for a in range(N)]
  for a in range(N):assert fsum(mul(A[a][i],tuple(banks[i]['amplitudes'][b])) for i in range(16))==const(pow(16,10*(a+b)**2%N,P))
  k=0
  for c in range(16):
   piv=next((r for r in range(k,N) if A[r][c]!=Z),None)
   if piv is None:continue
   A[k],A[piv]=A[piv],A[k];ii=inv(A[k][c]);A[k]=[mul(x,ii) for x in A[k]]
   for r in range(k+1,N):
    a=A[r][c]
    if a!=Z:A[r]=[sub(x,mul(a,y)) for x,y in zip(A[r],A[k])]
   k+=1
   if k==N:break
  ranks.append(k)
 assert ranks==[13,9,11,12,13,13,13,13,13,13,12,11,9]
 sufficient=[2,3,5,7,11,13,17,19];modulus=math.prod(sufficient);assert modulus==9699690
 assert next(d for d in range(2,modulus) if math.gcd(d,modulus)==1)==23
 result={'verdict':'PASS','certificate_sha256':hashlib.sha256(data_bytes).hexdigest(),'field_order':P**D,'field_order_bits':(P**D).bit_length(),'field_irreducibility':{'frobenius_remainders':remainders,'gcd_X53_minus_X':[1]},'arithmetic_crosschecks':len(pairs),'banks':16,'allocation':[7,1,1,7],'guards':16,'distinct_nonzero_same_sign_roots':7,'support_factorization_coefficients':8,'frobenius_root_images':frob_roots,'parameter_frobenius_orbit_lengths':orbit_lengths,'nonbase_cross_nodes':True,'nonstable_same_sign_supports':True,'branch_power_identities':208,'branch_power_scalar_equalities':208*N*N,'literal_branch_inverses':208,'inverse_product_identities':416,'inverse_scalar_equalities':416*N*N,'weights_forward_checks':208,'amplitudes_inverse_checks':208,'bank_weyl_equalities':16*N*N,'full_sector_equalities':N*N,'sector_ranks':ranks,'fourier_entry_equalities':N*N,'target_mismatches':0,'nonzero_bank_entries':nonzero,'negative_controls':{'omitted_one_over_13':control[0],'opposite_fourier_sign':control[1],'last_weight_plus_one':control[2]},'inverse_sha256':inverse_hashes,'bank_sha256':bank_hashes,'sufficient_divisors':sufficient,'remaining_gcd_modulus':modulus,'next_unclassified_degree':23,'next_degree_field_order':P**23,'next_degree_order_bits':(P**23).bit_length(),'next_degree_exceeds_uint128':P**23>=2**128,'method':'Independent carry-free integer-convolution field multiplication, polynomial Euclidean inverse, full matrix geometric-power inverse, literal left/right inverse checks, all raw banks, independent Weyl extraction and sector rank calculation.'}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'ARITHMETIC.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['inverse_sha256','bank_sha256','field_irreducibility','frobenius_root_images']},indent=2))
if __name__=='__main__':main()
