#!/usr/bin/env python3
"""Fresh self-contained exact controls for inherited N=3,7,9 scope.
This program does not import any project or author program.
"""
import sympy as s
import json
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
checks=[]
def ck(name,v):
 if not v:raise AssertionError(name)
 checks.append(name)
def field(n):
 z=s.Symbol('z');K=s.QQ.algebraic_field(s.CRootOf(s.cyclotomic_poly(n,z),0));return K,K.unit

def literal(n,e,d,K,q):
 R=K.poly_ring('a','b');a,b=R.gens
 M=[[R.zero for j in range(n)]for i in range(n)]
 for j in range(n):M[(j+e)%n][j]+=a;M[j][j]+=b*R.convert(q**(d*j%n),K)
 I=[[R.one if i==j else R.zero for j in range(n)]for i in range(n)];P=[r[:]for r in I];power=I
 def mul(A):return [[sum((M[i][k]*A[k][j]for k in range(n)),R.zero)for j in range(n)]for i in range(n)]
 for r in range(1,n):
  power=mul(power);P=[[P[i][j]+power[i][j]for j in range(n)]for i in range(n)]
 MP=mul(P)
 ck(f'N{n} literal inverse ({e},{d})',all(P[i][j]-MP[i][j]==((1-a**n-b**n)if i==j else 0)for i in range(n)for j in range(n)))
 return {(aa,bb):sum((P[(j+aa)%n][j]*R.convert(q**(-bb*j%n)/K(n),K)for j in range(n)),R.zero)for aa in range(n)for bb in range(n)}
def fourier(n,K,q):return {(a,b):sum((q**((-b*j-(j+a)*j)%n)for j in range(n)),K.zero)/K(n)for a in range(n)for b in range(n)}
# Reconstruct the legal N=3 construction and then recover literal branch weights.
n=3;K,q=field(n);O=[(1,1),(-1,1),(-1,-1),(1,-1)]
f=fourier(n,K,q);alpha={(1,1):K.one,(-1,1):q,(-1,-1):K.one,(1,-1):q};raw={o:literal(n,*o,K,q)for o in O}
H={}
for o,k in [((1,1),0),((1,-1),1),((-1,1),-1)]:H[o,0]=sum((f[a,0]*q**(-k*a%n)for a in range(n)),K.zero)/K(n)
H[(-1,-1),0]=K.zero
sec={}
for o in O:
 for p,poly in raw[o].items():
  for (r,l),z in poly.items():sec[o,l,p]=sec.get((o,l,p),K.zero)+z*alpha[o]**r
for e,d in O:H[(e,d),1]=f[e%n,d%n]/sec[(e,d),1,(e%n,d%n)]
for d in [1,-1]:
 H[(1,-d),2]=f[0,d%n]-H[(1,d),1]-H[(-1,d),1]
 H[(-1,-d),2]=K.zero
ck('N3 all nine amplitude coefficients',all(sum((H[o,l]*sec.get((o,l,p),K.zero)for o in O for l in range(n)),K.zero)==f[p]for p in f))
weights={o:[-sum((H[o,l]*q**(-o[0]*o[1]*j*l%n)for l in range(n)),K.zero)for j in range(n)]for o in O}
ck('N3 all four legal guards',all(1-alpha[o]**n-K.one==-K.one for o in O))
branch={p:K.zero for p in f}
for o in O:
 for j in range(n):
  for p,poly in raw[o].items():
   value=sum((z*alpha[o]**r*q**(o[0]*o[1]*j*l%n)for (r,l),z in poly.items()),K.zero)/(-K.one)
   branch[p]+=weights[o][j]*value/K(n)
ck('N3 raw literal branch weighted coefficients equal Fourier',branch==f)
print('N3 legal literal construction PASS',flush=True)
# N=7 row polynomials extracted afresh from literal numerators.
n=7;K,q=field(n);raw={o:literal(n,*o,K,q)for o in [(1,1),(-1,1)]};f=fourier(n,K,q);C=f[0,0];f={p:z/C for p,z in f.items()}
from sympy.polys.rings import ring
from sympy.polys.groebnertools import groebner
PR,x,y=ring('x,y',K,order='grevlex');eq=[]
for aa in range(2,n-1):
 expr=PR.ground_new(-f[aa,1])
 for o,parameter in [((1,1),x),((-1,1),y)]:
  end=(o[0]%n,1);endcoef=next(z for (r,l),z in raw[o][end].items()if l==1)
  h=f[end]/endcoef
  expr+=sum((h*z*parameter**(r-1) for(r,l),z in raw[o][aa,1].items()if l==1),PR.zero)
 eq.append(expr)
G=groebner(eq,PR)
ck('N7 exact literal-row ideal is the unit ideal',len(G)==1 and G[0]==PR.one)
print('N7 exact literal row unit ideal PASS',flush=True)
# N=9 forced degree-four recurrence from direct Fourier coefficients.
n=9;K,q=field(n);f=fourier(n,K,q)
A=DomainMatrix([[f[a+k,1]for k in range(4)]for a in range(1,5)],(4,4),K)
b=DomainMatrix([[-f[a+4,1]]for a in range(1,5)],(4,1),K)
ps=[r[0]for r in A.inv().matmul(b).to_list()]+[K.one]
p0,p1,p2,p3,p4=ps
ck('N9 forced recurrence all four equations',all(sum((ps[k]*f[a+k,1]for k in range(5)),K.zero)==K.zero for a in range(1,5)))
ck('N9 recurrence p3 nonzero identity',p3*(q*q+1)==K.one)
B=p1/(q*p3);AA=-p3/(1+q)
ck('N9 paired-base product forced to one',B==K.one)
res=p2-q*AA*AA-(1+q*q)*B
ck('N9 paired-base recurrence impossible',bool(res))
E=(1+q)**2*(p2-1-q*q)-q*p3*p3
ck('N9 exact displayed obstruction',E==q**5-q**4+2*q*q-2*q-3)
V=2*q**5-q**4+3*q*q-3*q+2
ck('N9 inherited all-admissible-field certificate',E*V==K(3))
print('N9 forced recurrence certificate PASS',flush=True)
out={'status':'PASS: inherited characteristic-zero N3, N7, N9 scope','checks':checks,'checks_passed':len(checks),'N7_reduced_basis':[str(p)for p in G],'scope':'N3 legal raw construction; N7 exact characteristic-zero necessary-row unit ideal; N9 exact recurrence contradiction. The all-odd-N>=11 result is independently reviewed by the general Hankel/Vandermonde proof, not by extrapolation from numerical controls.'}
Path(__file__).with_name('independent_scope_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
