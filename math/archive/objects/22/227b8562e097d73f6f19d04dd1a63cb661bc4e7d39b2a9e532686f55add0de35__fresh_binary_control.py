"""Independent binary-field control, no predecessor or ring-control imports."""
import json,pathlib,time
HERE=pathlib.Path(__file__).resolve().parent
def bits(indices):return sum(1<<i for i in indices)
def rem(a,b):
 while a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
 return a
def bgcd(a,b):
 while b:a,b=b,rem(a,b)
 return a
class Field:
 def __init__(self,f):self.f=f;self.calls=0
 def mul(self,a,b):
  self.calls+=1;r=0
  while b:
   if b&1:r^=a
   b>>=1;a<<=1
   if a&256:a^=self.f
  return r
 def pow(self,a,n):
  r=1
  while n:
   if n&1:r=self.mul(r,a)
   a=self.mul(a,a);n>>=1
  return r
 def inv(self,a):
  assert a;r=self.pow(a,254);assert self.mul(a,r)==1;return r
def trim(A):
 while A and not A[-1]:A.pop()
 return A
def pmod(A,B,F):
 A=A[:];inv=F.inv(B[-1])
 while A and len(A)>=len(B):
  t=F.mul(A[-1],inv);shift=len(A)-len(B)
  for j,b in enumerate(B):A[j+shift]^=F.mul(t,b)
  trim(A)
 return A
def pgcd(A,B,F):
 while B:A,B=B,pmod(A,B,F)
 inv=F.inv(A[-1]);return [F.mul(x,inv) for x in A]
def evaluate(A,x,F):
 y=0
 for a in reversed(A):y=F.mul(y,x)^a
 return y
def run():
 start=time.perf_counter();out=[]
 for name,indices in [('good',[8,5,4,3,0]),('bad',[8,7,6,4,2,1,0])]:
  f=bits(indices);F=Field(f);x=2
  # Rabin degree-eight irreducibility certificate.
  assert F.pow(x,256)==x and bgcd(F.pow(x,16)^x,f)==1
  assert F.pow(x,17)==1 and x!=1
  # Multiplicative Gaussian formula, independent of q-Pascal construction.
  H=[1]
  for k in range(1,9):H.append(F.mul(H[-1],F.mul(1^F.pow(x,9-k),F.inv(1^F.pow(x,k)))))
  derivative=[H[k] if k%2 else 0 for k in range(1,9)];trim(derivative)
  d_gcd=pgcd(H,derivative,F)
  cluster_gcd=pgcd(H,[1]+[0]*16+[1],F)
  roots=[j for j in range(17) if evaluate(H,F.pow(x,j),F)==0]
  assert d_gcd==[1]
  assert roots==([] if name=='good' else [6,11])
  assert len(cluster_gcd)-1==len(roots)
  out.append({'factor':name,'modulus_bits':f,'modulus_nonzero_degrees':indices,'H_coefficients_as_binary_polynomials':H,'ordinary_derivative_gcd':d_gcd,'cluster_gcd':cluster_gcd,'cluster_root_indices':roots,'field_multiplications':F.calls})
 result={'controls':out,'elapsed_seconds':time.perf_counter()-start}
 (HERE/'BINARY_FIELD_CONTROL.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':run()
