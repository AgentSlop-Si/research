"""Fresh author checker. Reads formal certificates only; executes no historical code."""
import itertools,json,pathlib,resource,time,copy,hashlib
import sympy as s
resource.setrlimit(resource.RLIMIT_CPU,(240,240))
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
ROOT=pathlib.Path(__file__).resolve().parent
z=s.symbols('z');I=s.eye(8);start=time.time();counts={}
def count(k,n=1):counts[k]=counts.get(k,0)+n
def cyc(order,weights):
 M=s.zeros(8)
 for j in range(8):M[order[(j+1)%8],order[j]]=weights[j]
 return M
def adj(M):return M.T.subs(z,1/z)
def clean(M):return M.applyfunc(s.expand)
def K(M):return clean((2*I-M)*(I-M).inv())
M1=cyc(range(8),[1]*7+[-1]);M2=cyc([0,1,3,4,5,6,2,7],[z,1,1,1,1,1,1/z,-1])
assert M1**8==-I and M2**8==-I;count('prefix_cycle_identities',2)
A=K(M1);B=K(M2);Ls={}
for e,f in itertools.product([-1,1],repeat=2):
 T=clean((A if e==1 else A.inv())*(B if f==1 else B.inv()))
 Ls[e,f]=clean(adj(T)*T);count('prefix_grams')

def validate(rec):
 e,f=rec['signs'];aa=rec['A'];bb=rec['B'];assert len(aa)==len(bb)==4 and 0 in aa and 1 in bb
 assert sorted(aa+bb)==list(range(8))
 L=Ls[e,f];G=clean(rec['scale_den']*z**rec['scale_z']*L)
 ps=[]
 for m in rec['minors']:
  assert len(m['R'])==len(set(m['R']))==3 and set(m['R'])<=set(aa)
  assert len(m['C'])==len(set(m['C']))==3 and set(m['C'])<=set(bb)
  det=s.Poly(s.expand(G.extract(m['R'],m['C']).det()),z,domain=s.QQ)
  assert not det.is_zero
  valuation=min(x[0] for x,c in det.terms());assert valuation==m['valuation']
  norm=s.Poly(det.as_expr()/z**valuation,z,domain=s.QQ).monic()
  claimed=s.Poly(s.sympify(m['p'],locals={'z':z}),z,domain=s.QQ)
  assert norm==claimed;ps.append(norm.as_expr())
 assert len(ps)==len(rec['bezout'])
 bez=[s.sympify(b,locals={'z':z}) for b in rec['bezout']]
 assert s.expand(sum(u*p for u,p in zip(bez,ps)))==1
 assert rec['gcd']=='1'
 return len(ps)
cert=json.loads((ROOT/'CUT_CERTIFICATES.json').read_text())
assert len(cert['certificates'])==80
seen=set()
for rec in cert['certificates']:
 key=tuple(rec['signs']),tuple(rec['A']);assert key not in seen;seen.add(key)
 count('normalized_minor_identities',validate(rec));count('bezout_identities');count('separating_cuts')
assert len(seen)==80
# Enumerate cyclic orders up to rotation; each has a balanced contiguous cut separating 0 and 1.
for tail in itertools.permutations(range(1,8)):
 order=(0,)+tail
 windows=[set((order+order)[j:j+4]) for j in range(8)]
 assert any(0 in w and 1 not in w for w in windows);count('cycle_order_cut_controls')
# Exact nonuniform, zero-weight and degenerate-coefficient Möbius controls.
coeffs=[(2,-1,1,-1),(0,1,3,2),(3,0,1,2),(2,1,4,2),(1,2,1,0)]
weights_cases=[[2,s.Rational(1,2),1,1,1,1,1,-1],[0,2,3,4,5,6,7,-1],[s.I,2,-1,s.Rational(1,2),1,1,1,s.I]]
for order in [list(range(8)),[0,3,6,1,4,7,2,5]]:
 for weights in weights_cases:
  Q=cyc(order,weights)
  for a,b,c,d in coeffs:
   N=a*I+b*Q;D=c*I+d*Q
   if not N.det() or not D.det():count('guarded_singular_cases');continue
   C=N*D.inv();F=D*N.inv();assert C*F==I
   H=F.conjugate().T*F
   for j in range(8):
    aa=(order+order)[j:j+4];bb=[k for k in order if k not in aa]
    assert F.extract(aa,bb).rank()<=1 and F.extract(bb,aa).rank()<=1
    assert H.extract(aa,bb).rank()<=2;count('mobius_cross_rank_controls')
# New class is beyond both previous mechanisms in an explicit allowed example.
Q=cyc(range(8),[2,s.Rational(1,2),1,1,1,1,1,-1])
C=(2*I-Q)*(I-Q).inv();F=C.inv();H=F.T*F
assert len(set(H.diagonal()))>1
coeffC=[s.Rational(3,2)]+[s.Rational(1,2)]*7
coeffF=[s.Rational(129,257)]+[-s.Rational(2**(7-k),257) for k in range(1,8)]
assert C==sum((coeffC[k]*Q**k for k in range(8)),s.zeros(8))
assert F==sum((coeffF[k]*Q**k for k in range(8)),s.zeros(8))
assert all(coeffC) and all(coeffF);count('full_support_nonconstant_diagonal_controls')
# Rank route cannot silently extend to arbitrary rational functions.
P=cyc(range(8),[1]*8);F2=I+2*P**2
assert F2.det()!=0 and (F2.T*F2).extract(range(4),range(4,8)).rank()==4
count('higher_degree_rank_cap_countercontrols')
# Nonmonomial separator is a true boundary: T S I=I with S=T^-1.
T=(A*B).subs(z,1);S=T.inv();assert T*S==I
assert any(sum(v!=0 for v in S.row(r))>1 for r in range(8));count('general_separator_countercontrols')
# Not every balanced cut is covered: mixed sign L has rank two at this unseparated cut.
assert Ls[-1,1].subs(z,1).extract([0,1,2,7],[3,4,5,6]).rank()==2
count('unseparated_cut_countercontrols')
# Deliberate tampering must fail.
mutations=[]
r=copy.deepcopy(cert['certificates'][0]);r['minors'][0]['p']='1';mutations.append(r)
r=copy.deepcopy(cert['certificates'][0]);r['bezout'][0]='0';mutations.append(r)
r=copy.deepcopy(cert['certificates'][0]);r['minors'][0]['valuation']+=1;mutations.append(r)
r=copy.deepcopy(cert['certificates'][0]);r['minors'][0]['R'][0]=1;mutations.append(r)
r=copy.deepcopy(cert['certificates'][0]);r['signs']=[1,1];mutations.append(r)
for r in mutations:
 try:validate(r)
 except (AssertionError,s.PolynomialError,ValueError):count('tamper_controls_rejected')
 else:raise AssertionError('tamper accepted')
result={'result':'PASS','role':'fresh author verification, not independent acceptance','historical_code_executed':False,'external_writes':0,'checks':counts,'elapsed_seconds':round(time.time()-start,3),'certificate_sha256':hashlib.sha256((ROOT/'CUT_CERTIFICATES.json').read_bytes()).hexdigest(),'limits':{'cpu_seconds':240,'address_space_bytes':2*1024**3,'external_wall_seconds':300}}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
