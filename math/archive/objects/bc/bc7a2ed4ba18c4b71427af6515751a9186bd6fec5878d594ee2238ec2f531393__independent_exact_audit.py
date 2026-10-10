#!/usr/bin/env python3
"""Independent exact audit. Supplied programs are never imported or executed.

The certificate is verified as integer polynomial identities after global
clearing of rational denominators. The cyclotomic relation is applied by signed
exponent reduction in a sixth formal variable, not numerical root evaluation.
SymPy is used only in independent small arithmetic and manufactured matrix
controls, and to solve a 4 by 4 scalar proportionality system.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from math import gcd, lcm
import hashlib, json, sys, time
import sympy as sp
sys.set_int_max_str_digits(0)
OUT=Path(__file__).resolve().parent
SRC=Path('adjacent_anchor_construction_0304')
PRE=Path('fourier8_orbit_independent_audit_0312')
ORIGINAL=Path('fourier8_kernel_construction_0249')
START=time.monotonic()
REPORT={'status':'RUNNING','method':'Exact denominator-cleared integer polynomial arithmetic modulo z^4+1; no supplied program executed or imported; no Groebner oracle.'}

def dump(name,obj):
 (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def log(s):
 print(s,flush=True)
def sha(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()
def seal_sources():
 return {str(p):sha(p) for root in (SRC,PRE,ORIGINAL) for p in sorted(root.rglob('*')) if p.is_file()}
def verify_manifest(root,name):
 entries=[]
 for line in (root/name).read_text().splitlines():
  if not line.strip(): continue
  h,n=line.split(maxsplit=1); n=n.lstrip('*')
  p=Path(n); p=p if p.is_absolute() else root/p
  assert sha(p)==h,('manifest mismatch',str(p))
  entries.append(str(p))
 return len(entries)

# Sparse integer polynomials; first exponent is z, remaining exponents are
# t/u variables. A polynomial is represented by one denominator, not a field
# element at each monomial. Every object is canonical and coefficients are ints.
class P:
 __slots__=('n','a','d')
 def __init__(self,n,a=None,d=1):
  assert isinstance(d,int) and d!=0
  a={tuple(k):int(v) for k,v in (a or {}).items() if v}
  assert all(len(k)==n+1 and 0<=k[0]<4 and all(isinstance(e,int) and e>=0 for e in k) for k in a)
  g=abs(d)
  for v in a.values(): g=gcd(g,abs(v))
  if d<0: g=-g
  self.n=n; self.a={k:v//g for k,v in a.items()}; self.d=d//g
 def __bool__(self): return bool(self.a)
 def __eq__(self,q):
  if isinstance(q,int): q=P.const(self.n,q)
  return isinstance(q,P) and self.n==q.n and self.d==q.d and self.a==q.a
 @staticmethod
 def const(n,q):
  q=Fraction(q);return P(n,{(0,)*(n+1):q.numerator},q.denominator)
 @staticmethod
 def var(n,j):
  k=[0]*(n+1); k[j+1]=1; return P(n,{tuple(k):1})
 @staticmethod
 def zpow(n,k):
  return P(n,{(k%4,)+(0,)*n:(-1)**(k//4)})
 def __neg__(self): return P(self.n,{k:-v for k,v in self.a.items()},self.d)
 def __add__(self,q):
  if not isinstance(q,P): q=P.const(self.n,q)
  assert self.n==q.n
  d=lcm(self.d,q.d); a={k:v*(d//self.d) for k,v in self.a.items()}
  for k,v in q.a.items(): a[k]=a.get(k,0)+v*(d//q.d)
  return P(self.n,a,d)
 __radd__=__add__
 def __sub__(self,q): return self+-q
 def __rsub__(self,q): return -self+q
 def __mul__(self,q):
  if not isinstance(q,P): q=P.const(self.n,q)
  assert self.n==q.n
  return P(self.n,imul(self.a,q.a),self.d*q.d)
 __rmul__=__mul__
 def __pow__(self,k):
  assert isinstance(k,int) and k>=0
  r=P.const(self.n,1); p=self
  while k:
   if k&1:r=r*p
   p=p*p;k//=2
  return r
 def lift(self,n):
  assert n>=self.n
  return P(n,{k+(0,)*(n-self.n):v for k,v in self.a.items()},self.d)
 def coeff(self,m):
  return [Fraction(self.a.get((j,)+tuple(m),0),self.d) for j in range(4)]
 def size(self): return len({k[1:] for k in self.a})
 def serial(self):
  return [[list(m),[[v.numerator,v.denominator] for v in self.coeff(m)]] for m in sorted({k[1:] for k in self.a})]

def imul(a,b):
 c={}
 for k,v in a.items():
  for l,w in b.items():
   z=k[0]+l[0]; h=(z%4,)+tuple(i+j for i,j in zip(k[1:],l[1:]))
   c[h]=c.get(h,0)+(v*w if z<4 else -v*w)
 return {k:v for k,v in c.items() if v}

def parse(raw,n,integer_coeffs=False):
 a={};seen=set();d=1
 for mon,coeff in raw:
  assert len(mon)==n and all(type(e)is int and e>=0 for e in mon)
  m=tuple(mon);assert m not in seen;seen.add(m)
  assert 1<=len(coeff)<=4
  for j,q in enumerate(coeff):
   if integer_coeffs:
    assert type(q)is int; q=Fraction(q)
   else:
    assert len(q)==2 and all(type(i)is int for i in q) and q[1]>0
    q=Fraction(*q)
   if q:a[(j,)+m]=q;d=lcm(d,q.denominator)
 return P(n,{k:q.numerator*(d//q.denominator) for k,q in a.items()},d)

def matrix_mul(A,B):
 n=len(A); m=len(B);p=len(B[0]);zero=P.const(A[0][0].n,0)
 return [[sum((A[i][k]*B[k][j] for k in range(m) if A[i][k] and B[k][j]),zero) for j in range(p)] for i in range(n)]

def scalar_between(R,G):
 # Recover a scalar from one nonzero coefficient by rational linear algebra.
 m=max(k[1:] for k in G.a)
 columns=[(P.zpow(G.n,j)*G).coeff(m) for j in range(4)]
 mat=sp.Matrix(4,4,lambda i,j:sp.Rational(columns[j][i].numerator,columns[j][i].denominator))
 rhs=sp.Matrix([sp.Rational(v.numerator,v.denominator) for v in R.coeff(m)])
 ss=list(mat.inv()*rhs)
 s=P(G.n,{(j,)+(0,)*G.n:int(v.p) for j,v in enumerate(ss) if v},1) if all(v.q==1 for v in ss) else sum((P.zpow(G.n,j)*Fraction(int(v.p),int(v.q)) for j,v in enumerate(ss)),P.const(G.n,0))
 assert s and R==s*G,'resultant factorization does not hold coefficientwise'
 return s

def check_node_identity(target,combination,known):
 terms=[];D=target.d
 for ref,mult in combination:
  p=known[ref];den=p.d*mult.d;D=lcm(D,den);terms.append((p,mult,den))
 acc={k:-v*(D//target.d) for k,v in target.a.items()}
 for p,mult,den in terms:
  f=D//den
  for k,v in imul(p.a,mult.a).items(): acc[k]=acc.get(k,0)+v*f
 residual={k:v for k,v in acc.items() if v}
 return not residual, D.bit_length(),len(residual)

def small_arithmetic_controls():
 z,x,y=sp.symbols('z x y'); mod=sp.Poly(z**4+1,z)
 def sym(p):
  return sum(sp.Rational(v,p.d)*z**k[0]*x**k[1]*y**k[2] for k,v in p.a.items())
 controls=[]
 for s in [13,29,43,71]:
  a=P(2,{(s%4,1,0):s,(3,0,2):-s-2,(0,0,0):1},s+3)
  b=P(2,{(2,0,1):s+1,(1,2,0):-3,(0,0,0):s-1},s+7)
  for name,c,expr in [('sum',a+b,sym(a)+sym(b)),('product',a*b,sym(a)*sym(b)),('cube',a**3,sym(a)**3)]:
   exact=sp.Poly(sp.expand(expr-sym(c)),z,domain=sp.QQ.frac_field(x,y)).rem(sp.Poly(z**4+1,z,domain=sp.QQ.frac_field(x,y)))
   assert exact.is_zero
   controls.append({'seed':s,'operation':name,'passed':True})
 assert P.zpow(2,4)==-1 and P.zpow(2,8)==1
 assert (P.zpow(2,3)-P.zpow(2,1))**2==2
 assert (1+P.zpow(2,2))*(1-P.zpow(2,2))==2
 # Eisenstein at 2 after z -> z+1 proves irreducibility over Q.
 es=sp.Poly(((z+1)**4+1).expand(),z).all_coeffs()
 assert es==[1,4,6,4,2] and all(int(c)%2==0 for c in es[1:]) and int(es[-1])%4!=0
 return controls

def build_interface_and_resultants(interface,cert):
 n=12;one=P.const(n,1);zero=P.const(n,0)
 t=[P.var(n,j) for j in range(4)];u=[P.var(n,j+4) for j in range(8)]
 pi=[(j+1)%8 for j in range(8)]
 order=[0,2,5,1,7,4,6,3];sigma=[None]*8
 for a,b in zip(order,order[1:]+order[:1]):sigma[a]=b
 assert sigma==[2,7,5,0,6,1,3,4]
 assert [interface['pi'][str(j)] for j in range(8)]==pi
 assert [interface['sigma'][str(j)] for j in range(8)]==sigma
 assert interface['anchor_pairs']==[[2*j,2*j+1] for j in range(4)]
 assert interface['order_0']==list(range(8)) and interface['order_1']==order
 assert interface['variables']==['t0','t1','t2','t3']+['u'+str(j) for j in range(8)]
 F=[[P.zpow(n,r*c) for c in range(8)] for r in range(8)]
 T=[[((t[i//2] if i%2 else one) if i==j else zero) for j in range(8)] for i in range(8)]
 K=[[zero for _ in range(8)] for _ in range(8)]
 for a in range(4):
  i=2*a;K[i][i]=one;K[i][i+1]=one;K[i+1][i]=one;K[i+1][i+1]=-one
 M=matrix_mul(matrix_mul(F,T),K)
 # Independently cross-check the closed column formula against matrix products.
 for r in range(8):
  for a in range(4):
   assert M[r][2*a]==P.zpow(n,2*a*r)+t[a]*P.zpow(n,(2*a+1)*r)
   assert M[r][2*a+1]==P.zpow(n,2*a*r)-t[a]*P.zpow(n,(2*a+1)*r)
 U=[[one if i==j else (u[i] if i==pi[j] else zero) for j in range(8)] for i in range(8)]
 A=matrix_mul(U,M)
 support=[{j,pi[j],sigma[j]} for j in range(8)]
 piv=[min(set(range(8))-support[j]) for j in range(8)]
 assert piv==[interface['pivot_rows'][str(j)] for j in range(8)]
 a=[A[piv[j]][j] for j in range(8)];c=[A[piv[j]][sigma[j]] for j in range(8)]
 H=[[c[j]*A[i][j]-a[j]*A[i][sigma[j]] for j in range(8)] for i in range(8)]
 fresh={**{'a_'+str(j):a[j] for j in range(8)},**{'c_'+str(j):c[j] for j in range(8)}}
 fresh.update({f'h_{i}_{j}':H[i][j] for i in range(8) for j in range(8)})
 sinv=[sigma.index(i) for i in range(8)]
 for i in range(8):
  fresh['diag_'+str(i)]=u[pi[i]]*a[sinv[i]]*H[i][i]+c[i]*u[pi[i]]*H[i][sinv[i]]-a[sinv[i]]*H[pi[i]][i]
 assert set(fresh)==set(interface['polynomials'])
 for k,p in fresh.items():assert p==parse(interface['polynomials'][k],n,True),('interface polynomial',k)
 expected_zero=[f'h_{i}_{j}' for j in range(8) for i in range(8) if i not in support[j] and i!=piv[j]]+[f'diag_{i}' for i in range(8)]
 assert interface['zero_equations']==expected_zero and len(expected_zero)==40
 for k in ['a_1','a_5','a_6']:assert k in interface['nonzero_polynomial_guards']
 assert 'u0' in interface['nonzero_variable_guards']
 J=[j for j in range(8) if piv[j]==0]
 assert J==[1,2,4,5,6]
 B=A[0]
 for j in range(8):assert B[j]==M[0][j]+u[0]*M[7][j]
 rows=[];selected=[];minors=set();factors=[];raw=[]
 for r in range(1,8):
  eligible=[j for j in J if r not in support[j]]
  rows.append({'row':r,'eligible_columns':eligible})
  bc={}
  for j in eligible:
   b=B[sigma[j]]*M[r][j]-B[j]*M[r][sigma[j]]
   cc=B[sigma[j]]*M[r-1][j]-B[j]*M[r-1][sigma[j]]
   assert b+u[r]*cc==H[r][j]
   assert f'h_{r}_{j}' in expected_zero
   bc[j]=(b,cc);minors.add(f'h_{r}_{j}')
  for j,k in combinations(eligible,2):
   b,cj=bc[j];bk,ck=bc[k];R=b*ck-bk*cj
   assert R==ck*H[r][j]-cj*H[r][k]
   f=parse(cert['inputs'][len(selected)],5).lift(n)
   cancelled=[];g=one
   if r==1:g=g*u[0];cancelled.append('u0')
   if (j,k)==(4,6):g=g*B[6];cancelled.append('B6')
   if (j,k)==(1,5):g=g*B[1];cancelled.append('B1')
   if (j,k)==(2,5):g=g*B[5];cancelled.append('B5')
   s=scalar_between(R,g*f)
   # Removing any claimed factor or changing the sign produces a false identity.
   assert R!=-(s*g*f)
   assert R!=s*g*(f+Fraction(1,101))
   if cancelled:assert R!=s*f
   selected.append([r,j,k]);raw.append(R)
   factors.append({'index':len(selected)-1,'row':r,'columns':[j,k],'cancelled_factors':cancelled,'nonzero_scalar':s.serial()[0][1],'resultant_terms':R.size(),'generator_terms':f.size()})
 assert len(selected)==20
 published=json.loads((SRC/'VERIFICATION_REPORT.json').read_text())
 assert selected==published['selected_minors']
 assert [q['nonzero_scalar'] for q in factors]==published['normalization_scalars']
 log('PASS: all 88 interface polynomials and all 20 complete resultant factorizations regenerated from F8 T K_adj')
 return {'interface_polynomials':88,'zero_equations':40,'rows':rows,'selected_resultants':selected,'distinct_used_minors':sorted(minors),'factorizations':factors,'necessary_nonzero_factors':['u0','B1','B5','B6'],'no_other_divisors':True,'perturbed_generator_factorizations_rejected':20,'sign_reversed_factorizations_rejected':20}

def verify_certificate(cert):
 assert cert['field']=='Q[z]/(z^4+1)' and cert['variables']==['t0','t1','t2','t3','w']
 assert cert['source_resultant_indices']==list(range(20))
 inputs=[parse(v,5) for v in cert['inputs']]
 stored=json.loads((SRC/'all_row_resultants.json').read_text())
 assert len(inputs)==len(stored)==20
 for p,r in zip(inputs,stored):assert p==parse(r,5)
 known={};combs={};summaries=[];leaves=[];count=0;monomial_count=0
 for key in sorted(cert['nodes'],key=int):
  idx=int(key);node=cert['nodes'][key];p=parse(node['polynomial'],5)
  assert set(node)=={'polynomial','combination'}
  if idx<20:
   assert node['combination']==[] and p==inputs[idx]
   leaves.append(idx);bits=p.d.bit_length()
  else:
   assert node['combination'],'derived node with no justification'
   comb=[]
   for ref,raw in node['combination']:
    assert type(ref)is int and ref<idx and ref in known,'unknown or non-earlier dependency'
    q=parse(raw,5);assert q,'zero multiplier'
    comb.append((ref,q));monomial_count+=q.size()
   count+=len(comb);combs[idx]=comb
   ok,bits,res=check_node_identity(p,comb,known)
   assert ok,('node identity failed',idx,res)
  known[idx]=p
  summaries.append({'id':idx,'polynomial_monomials':p.size(),'combination_entries':len(node['combination']),'cleared_denominator_bits':bits,'passed':True})
  log(f'PASS: node {idx}, {p.size()} monomials, {len(node["combination"])} combination entries, elapsed {time.monotonic()-START:.2f}s')
 assert len(known)==57 and count==575
 final=cert['final_node'];assert final in known and known[final]==1
 ancestors=set()
 def visit(i):
  if i in ancestors:return
  ancestors.add(i)
  for j,_ in combs.get(i,[]):visit(j)
 visit(final);assert ancestors==set(known),'unneeded retained nodes'
 controls=[]
 # Structural and arithmetic adversarial checks on copies, never frozen inputs.
 assert known[leaves[0]]+Fraction(1,17)!=inputs[leaves[0]]
 controls.append({'control':'perturbed leaf polynomial','detected':True})
 first=min(combs)
 ok,_,_=check_node_identity(known[first]+Fraction(1,17),combs[first],known)
 assert not ok;controls.append({'control':'perturbed intermediate target','node':first,'detected':True})
 changed=list(combs[first]);ref,q=changed[0];changed[0]=(ref,q+Fraction(1,19))
 ok,_,_=check_node_identity(known[first],changed,known)
 assert not ok;controls.append({'control':'perturbed intermediate multiplier','node':first,'detected':True})
 ok,_,_=check_node_identity(P.const(5,0),combs[final],known)
 assert not ok;controls.append({'control':'final target changed from 1 to 0','detected':True})
 # Every node's verified equality rejects addition of 1 to its RHS.
 for idx,comb in combs.items():
  ok,_,_=check_node_identity(known[idx]+1,comb,known)
  assert not ok
 controls.append({'control':'each derived node target changed by +1','nodes':len(combs),'all_detected':True})
 return {'field':'Q[z]/(z^4+1)','input_generators':len(inputs),'retained_nodes':len(known),'derived_nodes':len(combs),'retained_input_leaves':leaves,'combination_entries':count,'multiplier_monomials':monomial_count,'final_node':final,'final_polynomial':'1','all_retained_nodes_reach_final':True,'nodes':summaries,'negative_controls':controls}


def manufactured_controls():
 pi=[(j+1)%8 for j in range(8)];sigma=[2,7,5,0,6,1,3,4]
 support=[{j,pi[j],sigma[j]} for j in range(8)];piv=[min(set(range(8))-q) for q in support]
 def investigate(u,v,x,y,label,expect_guarded):
  I=sp.eye(8);U=I.copy();V=I.copy()
  for j in range(8):U[pi[j],j]=u[pi[j]];V[sigma[j],j]=v[j]
  assert U.det()!=0 and V.det()!=0
  X=sp.diag(*x);Y=sp.diag(*y)
  M=U.inv()*X+Y*V.inv();A=U*M
  assert U*M*V==U*Y+X*V
  a=[A[piv[j],j] for j in range(8)];c=[A[piv[j],sigma[j]] for j in range(8)]
  H=sp.Matrix(8,8,lambda i,j:c[j]*A[i,j]-a[j]*A[i,sigma[j]])
  off=[H[i,j] for j in range(8) for i in range(8) if i not in support[j] and i!=piv[j]]
  si=[sigma.index(i) for i in range(8)]
  diagonal=[u[pi[i]]*a[si[i]]*H[i,i]+c[i]*u[pi[i]]*H[i,si[i]]-a[si[i]]*H[pi[i],i] for i in range(8)]
  assert len(off)==32 and all(q==0 for q in off+diagonal)
  pivotzeros=[j for j in range(8) if a[j]==0 or c[j]==0]
  rowR=0
  for r in range(1,8):
   eligible=[j for j in [1,2,4,5,6] if r not in support[j]]
   B=A[0,:]
   bc={j:(B[sigma[j]]*M[r,j]-B[j]*M[r,sigma[j]],B[sigma[j]]*M[r-1,j]-B[j]*M[r-1,sigma[j]]) for j in eligible}
   for j,k in combinations(eligible,2):
    assert bc[j][0]*bc[k][1]-bc[k][0]*bc[j][1]==0;rowR+=1
  entry={'label':label,'not_fourier':True,'equations_passed':40,'row_resultants_passed':rowR,'zero_pivot_columns':pivotzeros,'zero_u_edges':[j for j in range(8) if u[j]==0],'zero_v_edges':[j for j in range(8) if v[j]==0]}
  if expect_guarded:
   assert all(u) and all(v) and all(x) and all(y) and not pivotzeros
   assert all(H[pi[j],j]!=0 and H[sigma[j],j]!=0 for j in range(8))
   assert sp.prod(c)-sp.prod(a)!=0
   assert [-a[j]/c[j] for j in range(8)]==v
   assert [-H[i,si[i]]/a[si[i]] for i in range(8)]==x
   assert [H[pi[j],j]/(c[j]*u[pi[j]]) for j in range(8)]==y
   Q0=sp.diag(*[1/q for q in x])*U;Q1=V*sp.diag(*[1/q for q in y])
   assert Q0.inv()+Q1.inv()==M
   assert (2*Q0).inv()+(2*Q1).inv()==M/2
   entry['full_guarded_reconstruction_passed']=True
   rejects=[]
   for r,j in [(0,3),(1,6),(5,2),(6,7)]:
    Mp=M.copy();Mp[r,j]+=sp.Rational(1,137);Ap=U*Mp
    ap=[Ap[piv[j],j] for j in range(8)];cp=[Ap[piv[j],sigma[j]] for j in range(8)]
    Hp=sp.Matrix(8,8,lambda i,j:cp[j]*Ap[i,j]-ap[j]*Ap[i,sigma[j]])
    residuals=[Hp[i,j] for j in range(8) for i in range(8) if i not in support[j] and i!=piv[j]]
    residuals += [u[pi[i]]*ap[si[i]]*Hp[i,i]+cp[i]*u[pi[i]]*Hp[i,si[i]]-ap[si[i]]*Hp[pi[i],i] for i in range(8)]
    assert any(q!=0 for q in residuals)
    rejects.append({'entry':[r,j],'increment':'1/137','rejected':True})
   entry['matrix_perturbations']=rejects
  return entry
 results=[]
 for seed in [29,31,43,47]:
  u=[sp.Rational(seed+3*j+1,seed+83) for j in range(8)]
  v=[sp.Rational(-seed-2*j-1,seed+97) for j in range(8)]
  x=[sp.Rational(seed+j+2,j+3) for j in range(8)]
  y=[sp.Rational(2*seed+j+1,j+5) for j in range(8)]
  results.append(investigate(u,v,x,y,'full-edge seed '+str(seed),True))
  log('PASS: fresh non-Fourier full-edge matrix control seed '+str(seed))
 x=[sp.Rational(j+2,j+3) for j in range(8)];y=[sp.Rational(j+4,j+5) for j in range(8)]
 results.append(investigate([sp.Rational(0)]*8,[sp.Rational(0)]*8,x,y,'all cycle edges zero',False))
 u=[sp.Rational(j+1,j+13) for j in range(8)];v=[sp.Rational(-j-1,j+17) for j in range(8)]
 u[0]=0;u[5]=0;v[2]=0
 results.append(investigate(u,v,x,y,'mixed zero edges including u0=0',False))
 assert results[-2]['zero_pivot_columns']==list(range(8))
 return results


def main():
 before=seal_sources();dump('SOURCE_SEALS_BEFORE.json',before)
 manifest_counts={str(SRC/'PACKAGE_SHA256SUMS.txt'):verify_manifest(SRC,'PACKAGE_SHA256SUMS.txt'),str(PRE/'SHA256SUMS.txt'):verify_manifest(PRE,'SHA256SUMS.txt'),str(ORIGINAL/'SHA256SUMS.txt'):verify_manifest(ORIGINAL,'SHA256SUMS.txt')}
 interface=json.loads((SRC/'ADJACENT_ANCHOR_ORBIT_SYSTEM.json').read_text())
 assert (SRC/'ADJACENT_ANCHOR_ORBIT_SYSTEM.json').read_bytes()==(ORIGINAL/'ADJACENT_ANCHOR_ORBIT_SYSTEM.json').read_bytes()
 cert=json.loads((SRC/'EXACT_UNIT_CERTIFICATE.json').read_text())
 REPORT['arithmetic_controls']=small_arithmetic_controls()
 REPORT['resultants']=build_interface_and_resultants(interface,cert)
 dump('RESULTANT_AUDIT.json',REPORT['resultants'])
 REPORT['certificate']=verify_certificate(cert)
 dump('CERTIFICATE_AUDIT.json',REPORT['certificate'])
 log('PASS: exact proof DAG final constant equals 1; beginning fresh matrix controls')
 REPORT['manufactured_controls']=manufactured_controls()
 after=seal_sources();assert before==after,'frozen inputs changed'
 dump('SOURCE_SEALS_AFTER.json',after)
 REPORT.update(status='PASS',seconds=time.monotonic()-START,source_file_count=len(before),manifest_entries_verified=manifest_counts,source_files_unchanged=True,scope='No solution of the necessary Fourier off-support minors where u0*B1*B5*B6 != 0, in characteristic zero. This excludes the exported guarded chart only; zero-pivot and u0=0 boundaries remain open.')
 dump('AUDIT_RESULTS.json',REPORT)
 dump('FRESH_CONTROLS.json',{'arithmetic':REPORT['arithmetic_controls'],'certificate_negative':REPORT['certificate']['negative_controls'],'manufactured_exact_matrices':REPORT['manufactured_controls']})
 log('ALL AUDIT CHECKS PASSED in %.2fs'%REPORT['seconds'])
if __name__=='__main__':main()
