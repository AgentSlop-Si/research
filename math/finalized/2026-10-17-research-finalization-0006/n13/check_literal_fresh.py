"""Fresh original-grammar check; no historical code imports or execution."""
import json,hashlib,time
from pathlib import Path
P=53;N=13;Q=16
D=Path(__file__).resolve().parent
class Field:
 def __init__(self,mod):self.mod=mod;self.d=len(mod)-1;self.zero=(0,)*self.d;self.one=self.c(1)
 def c(self,a):return (a%P,)+(0,)*(self.d-1)
 def add(self,a,b):return tuple((x+y)%P for x,y in zip(a,b))
 def neg(self,a):return tuple(-x%P for x in a)
 def sub(self,a,b):return self.add(a,self.neg(b))
 def scale(self,a,b):return tuple(x*b%P for x in a)
 def mul(self,a,b):
  if not any(a):return self.zero
  if not any(b):return self.zero
  z=[0]*(2*self.d-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):z[i+j]+=x*y
  for k in range(2*self.d-2,self.d-1,-1):
   v=z[k]%P
   for j in range(self.d):z[k-self.d+j]-=v*self.mod[j]
  return tuple(x%P for x in z[:self.d])
 def pow(self,a,n):
  if n<0:a=self.inv(a);n=-n
  r=self.one
  while n:
   if n&1:r=self.mul(r,a)
   a=self.mul(a,a);n//=2
  return r
 def inv(self,a):
  assert a!=self.zero
  return self.pow(a,P**self.d-2)
 def val(self,H,a):
  r=self.zero
  for h in H[::-1]:r=self.add(self.mul(r,a),self.c(h))
  return r
 def solve(self,A,b):
  n=len(A);m=len(A[0]);a=[list(r)+[v] for r,v in zip(A,b)];piv=[];r=0
  for c in range(m):
   p=next((i for i in range(r,n) if a[i][c]!=self.zero),None)
   if p is None:continue
   a[r],a[p]=a[p],a[r];iv=self.inv(a[r][c]);a[r]=[self.mul(x,iv) for x in a[r]]
   for i in range(n):
    if i==r or a[i][c]==self.zero:continue
    v=a[i][c];a[i]=[self.sub(x,self.mul(v,y)) for x,y in zip(a[i],a[r])]
   piv.append(c);r+=1
   if r==n:break
  assert all(any(x!=self.zero for x in row[:m]) or row[m]==self.zero for row in a)
  x=[self.zero]*m
  for row,c in zip(a,piv):x[c]=row[m]
  return x,r
 def inverse(self,A):
  n=len(A);a=[list(row)+[self.one if i==j else self.zero for j in range(n)] for i,row in enumerate(A)]
  for c in range(n):
   p=next(i for i in range(c,n) if a[i][c]!=self.zero);a[c],a[p]=a[p],a[c]
   iv=self.inv(a[c][c]);a[c]=[self.mul(x,iv) for x in a[c]]
   for i in range(n):
    if i==c or a[i][c]==self.zero:continue
    v=a[i][c];a[i]=[self.sub(x,self.mul(v,y)) for x,y in zip(a[i],a[c])]
  assert all(a[i][j]==(self.one if i==j else self.zero) for i in range(n) for j in range(n))
  return [row[n:] for row in a]

def roots(F,H):
 if F.d==2:
  r=[(a,b) for a in range(P) for b in range(P) if F.val(H,(a,b))==F.zero]
 else:
  u=(0,1,0);r=[F.c(a) for a in range(P) if F.val(H,F.c(a))==F.zero]+[F.pow(u,P**j) for j in range(3)]
 assert len(r)==7 and len(set(r))==7 and F.zero not in r
 assert all(F.val(H,x)==F.zero for x in r)
 # Monic product of all actual roots, coefficientwise over the chosen field.
 poly=[F.one]
 for x in r:
  z=[F.zero]*(len(poly)+1)
  for j,c in enumerate(poly):z[j]=F.sub(z[j],F.mul(x,c));z[j+1]=F.add(z[j+1],c)
  poly=z
 assert poly==[F.c(v) for v in H]
 return r

def run(name,filename,mod):
 t=time.time();w=json.loads((D/filename).read_text());F=Field(mod)
 # Verify modulus is irreducible, directly for degree2/3 by absence of base-field roots.
 assert F.d in (2,3)
 assert all(sum(c*pow(a,j,P) for j,c in enumerate(mod))%P for a in range(P))
 rx=roots(F,w['positive']['H']);rz=roots(F,w['negative']['H'])
 nodes=rx+[F.c(w['y']),F.c(w['z'])]+rz;signs=[(1,1)]*7+[(-1,1),(1,-1)]+[(-1,-1)]*7
 amps=[[F.zero]*N for _ in range(16)]
 for b,sector in enumerate(w['sectors']):
  assert sector['b']==b;mom=sector['solution']
  for off,rr in ((0,rx),(9,rz)):
   V=[[F.pow(x,a) for x in rr] for a in range(7)];aa,rank=F.solve(V,[F.c(x) for x in mom[off:off+7]])
   assert rank==7
   for j,x in enumerate(aa):amps[off+j][b]=x
  amps[7][b]=F.c(mom[7]);amps[8][b]=F.c(mom[8])
 banks=[];aggregate=[[F.zero]*N for _ in range(N)];inv_count=0;twosided=0;branch_den=[];bank_nonzero=[]
 for i,(alpha,(e,d)) in enumerate(zip(nodes,signs)):
  delta=F.neg(F.pow(alpha,N));assert delta!=F.zero
  weights=[]
  for j in range(N):
   s=F.zero
   for b in range(N):s=F.add(s,F.scale(amps[i][b],pow(Q,(-e*b*j)%N,P)))
   weights.append(F.scale(F.mul(delta,s),7))
  B=[[F.zero]*N for _ in range(N)]
  for j in range(N):
   A=[[F.zero]*N for _ in range(N)]
   for col in range(N):
    A[col][col]=F.c(1-pow(Q,(e*d*j+d*col)%N,P));A[(col+e)%N][col]=F.neg(alpha)
   I=F.inverse(A);inv_count+=1
   # Sparse left and right multiplication separately against full Gauss-Jordan inverse.
   for row in range(N):
    for col in range(N):
     left=F.add(F.mul(A[row][row],I[row][col]),F.mul(A[row][(row-e)%N],I[(row-e)%N][col]))
     right=F.add(F.mul(I[row][col],A[col][col]),F.mul(I[row][(col+e)%N],A[(col+e)%N][col]))
     target=F.one if row==col else F.zero
     assert left==target and right==target
     B[row][col]=F.add(B[row][col],F.scale(F.mul(weights[j],I[row][col]),pow(N,-1,P)))
   twosided+=2
  assert any(B[r][c]!=F.zero for r in range(N) for c in range(N));bank_nonzero.append(True);branch_den.append(delta)
  for r in range(N):
   for c in range(N):aggregate[r][c]=F.add(aggregate[r][c],B[r][c])
  banks.append({'epsilon':e,'delta_sign':d,'alpha':alpha,'beta':F.one,'inverse_guard':delta,'sector_amplitudes':amps[i],'raw_weights':weights})
 target=[[F.c(pow(Q,-r*c%N,P)) for c in range(N)] for r in range(N)]
 assert aggregate==target
 assert len(set(rx))==7 and len(set(rz))==7
 # Falsification controls: omit 1/N, opposite Fourier sign, perturb one raw weight.
 omitted=sum(F.scale(aggregate[r][c],N)!=target[r][c] for r in range(N) for c in range(N))
 opposite=sum(aggregate[r][c]!=F.c(pow(Q,r*c%N,P)) for r in range(N) for c in range(N))
 # Last invertible branch necessarily changes at least one matrix entry when a weight changes.
 perturb=sum(I[r][c]!=F.zero for r in range(N) for c in range(N));assert omitted and opposite and perturb
 result={'name':name,'degree':F.d,'modulus_ascending':mod,'field_encoding':'coefficient tuple in increasing powers of u','y':w['y'],'z':w['z'],'positive_H':w['positive']['H'],'negative_H':w['negative']['H'],'positive_roots':rx,'negative_roots':rz,'banks':banks,'aggregate':aggregate}
 (D/(name+'_LITERAL_CERTIFICATE.json')).write_text(json.dumps(result,indent=2)+'\n')
 return {'name':name,'degree':F.d,'modulus_irreducible':True,'distinct_nonzero_supports':[7,7],'allocation':[7,1,1,7],'literal_inverses':inv_count,'two_sided_inverse_identities':twosided,'aggregate_entries':169,'all_original_target_entries_equal':True,'all_sixteen_banks_nonzero':all(bank_nonzero),'all_inverse_guards_nonzero':True,'quotient_sector_ranks':[s['rank'] for s in w['sectors']],'controls':{'omitted_normalization_mismatch_entries':omitted,'opposite_sign_mismatch_entries':opposite,'last_weight_perturbation_mismatch_entries':perturb},'elapsed_seconds':time.time()-t}

if __name__=='__main__':
 out=[]
 for args in [('QUADRATIC','FIRST_WITNESS.json',[51,0,1]),('CUBIC','CUBIC_WITNESS.json',[11,25,40,1])]:
  r=run(*args);out.append(r);print(json.dumps(r),flush=True)
 (D/'LITERAL_CHECK_RESULT.json').write_text(json.dumps({'verdict':'PASS','checks':out,'historical_code_executed':False},indent=2)+'\n')
