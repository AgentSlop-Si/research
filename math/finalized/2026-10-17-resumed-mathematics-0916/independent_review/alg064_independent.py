"""Fresh output verifier. Reads inert output data, imports no author program."""
import json, hashlib
from fractions import Fraction as F
from pathlib import Path
from math import factorial
ROOT=Path(__file__).parent
Z=(F(0),F(0));O=(F(1),F(0))
def decode(v):
 if isinstance(v,dict) and set(v)=={'numerator','denominator'}:return F(v['numerator'],v['denominator'])
 if isinstance(v,list):return [decode(x) for x in v]
 if isinstance(v,dict):return {k:decode(x) for k,x in v.items()}
 return v
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def scale(a,c):return a[0]*c,a[1]*c
def nu(a):return abs(a[0])+abs(a[1])
def atan_recip(q,target):
 s=F(0);k=0
 while True:
  s+=F((-1)**k,(2*k+1)*q**(2*k+1));k+=1
  err=F(1,(2*k+1)*q**(2*k+1))
  if err<=target:return s,err

def rnd(v,b):
 s=v*(1<<b);return F((s.numerator*2+s.denominator)//(2*s.denominator),1<<b)

def oracle(x,eps):
 n=len(x);S=sum(nu(a) for a in x);p=1
 while F(1,1<<p)>min(F(1,n),eps/(3072*n*(S+1))):p+=1
 rho=F(1,1<<p)
 # arctan(1/2)+arctan(1/3)=pi/4: a different exact pi identity from author.
 a,ea=atan_recip(2,rho/1024);b,eb=atan_recip(3,rho/1024)
 pir=4*(a+b);pi=rnd(pir,p+10);pie=4*(ea+eb)+abs(pi-pir)
 degree=0
 while F(4**(degree+1),factorial(degree+1))>rho/128:degree+=1
 rem=F(4**(degree+1),factorial(degree+1))
 values=[]
 for k in range(n):
  kk=k if 2*k<=n else k-n;theta=F(2*kk,n)*pi;assert abs(theta)<4
  term=O;node=O
  for j in range(1,degree+1):term=scale(mul(term,(F(0),theta)),F(1,j));node=add(node,term)
  node=(rnd(node[0],p+8),rnd(node[1],p+8))
  # Taylor Lagrange remainder per real/imag component, pi angle error, final rounding.
  radius=2*pie+2*rem+F(1,1<<(p+8));assert radius<=rho
  power=O;v=Z
  for a in x:v=add(v,mul(a,power));power=mul(power,node)
  values.append(v)
 bound=3*n*S*rho
 assert bound<=eps/1024
 return values,bound,p

def main():
 import sys
 path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'reports'/'alg064'/'OUTPUT_VECTORS.json'
 raw=decode(json.loads(path.read_text()));print(type(raw), (list(raw)[:4] if isinstance(raw,dict) else len(raw)))
 cases=raw['cases'] if isinstance(raw,dict) else raw
 count=0;maxp=0;names=[]
 for case in cases:
  x=case['raw_dyadic_input'];eps=case['epsilon'];outputs=case['outputs'];ref,err,p=oracle(x,eps)
  assert len(outputs)==len(x)
  for y,z in zip(outputs,ref):
   dist2=(y[0]-z[0])**2+(y[1]-z[1])**2
   assert dist2<=(eps-err)**2,case['name']
   count+=1
  maxp=max(maxp,p);names.append(case['name'])
 out={'status':'PASS','author_output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cases':len(cases),'all_output_entries':count,'max_oracle_fraction_bits':maxp,'oracle':'Independent exact rational arctan(1/2)+arctan(1/3) pi certificate, Taylor exponential node enclosure and direct power sums; no author code executed/imported','case_names':names}
 (ROOT/'ALG064_OUTPUT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
