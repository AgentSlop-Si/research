#!/usr/bin/env python3
"""Fresh independent controls. Never imports or executes constructor programs.
Reads constructor JSON only as data and independently recomputes its certificates.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd
import hashlib, json, itertools
from pathlib import Path
OUT=Path(__file__).resolve().parent
SRC=Path('research_round_2156/joint_orbit/iteration_9_bank_interface')
CLOSURE=Path('coverage_audit_20261010/LATEST_SOURCE_REVIEW_CLOSURE.json')
Z=(F(0),)*4; O=(F(1),F(0),F(0),F(0)); zeta=(F(0),F(1),F(0),F(0))
def q(x):
 if isinstance(x,(list,tuple)): return tuple(F(y) for y in x)
 return (F(x),F(0),F(0),F(0))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
 v=[F(0)]*7
 for i in range(4):
  for j in range(4): v[i+j]+=a[i]*b[j]
 for i in range(6,3,-1): v[i-4]-=v[i]
 return tuple(v[:4])
def power(a,n):
 assert n>=0
 ans=O
 while n:
  if n&1: ans=mul(ans,a)
  a=mul(a,a); n//=2
 return ans
def det(A): return sub(mul(A[0][0],A[1][1]),mul(A[0][1],A[1][0]))
def adj(A): return [[A[1][1],neg(A[0][1])],[neg(A[1][0]),A[0][0]]]
def mm(A,B):
 return [[reduce(add,(mul(x,y) for x,y in zip(row,col)),Z) for col in zip(*B)] for row in A]
def ms(A,B): return [[sub(x,y) for x,y in zip(a,b)] for a,b in zip(A,B)]
def ident(n): return [[O if i==j else Z for j in range(n)] for i in range(n)]
def parse(A): return [[q(x) for x in row] for row in A]
def flat(A): return [x for row in A for x in row]
def prop(a,b):
 assert len(a)==len(b)
 piv=next((i for i,x in enumerate(b) if x!=Z),None)
 if piv is None: return all(x==Z for x in a)
 return a[piv]!=Z and all(mul(x,b[piv])==mul(y,a[piv]) for x,y in zip(a,b))
def serial(v):
 if isinstance(v,F): return int(v) if v.denominator==1 else str(v)
 if isinstance(v,dict): return {str(k):serial(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)): return [serial(x) for x in v]
 return v
def perm(order):
 p=[None]*len(order)
 for a,b in zip(order,order[1:]+order[:1]): p[a]=b
 return p
def invp(p): return [p.index(i) for i in range(len(p))]
def transition(B,i,k,j,pi,sigma):
 ip=invp(pi); A,C=B[i][j],B[i][sigma[j]]; bb,D=B[ip[i]][j],B[ip[i]][sigma[j]]
 E,G=B[k][j],B[k][sigma[j]]; ff,H=B[ip[k]][j],B[ip[k]][sigma[j]]
 return [[sub(mul(A,H),mul(C,ff)),sub(mul(bb,H),mul(D,ff))],
         [sub(mul(C,E),mul(A,G)),sub(mul(D,E),mul(bb,G))]]
def rank2(H): return 2 if det(H)!=Z else (1 if any(x!=Z for x in flat(H)) else 0)
def bilinear_L(H): return [[neg(H[1][0]),neg(H[1][1])],H[0]]
def quadratic(Ti,Tk,H):
 Tkt=[list(row) for row in zip(*Tk)]; M=mm(mm(Tkt,bilinear_L(H)),Ti)
 return [M[0][0],add(M[0][1],M[1][0]),M[1][1]]
def triples(pi,sigma):
 ip,jp=invp(pi),invp(sigma)
 return [(i,k,j) for i in range(8) for k in range(i+1,8) for j in range(8)
         if j not in {i,ip[i],jp[i],k,ip[k],jp[k]}]
def butterfly(anchor):
 K=[[Z]*8 for _ in range(8)]
 pairs=[(j,j+1) for j in range(0,8,2)] if anchor=='adjacent' else [(j,j+4) for j in range(4)]
 for a,b in pairs:
  K[a][a]=K[a][b]=K[b][a]=O; K[b][b]=neg(O)
 assert mm(K,K)==[[q(2) if i==j else Z for j in range(8)] for i in range(8)]
 # Check the stipulated legal matching-mask realization, not merely K^2.
 G0=ident(8); G1=ident(8)
 for a,b in pairs: G0[a][b]=q(F(1,2)); G1[b][a]=q(F(-1,3))
 T0=[[mul(q(2),x) for x in row] for row in G0]; T1=[]
 diag=[0]*8
 for a,b in pairs: diag[a]=-1;diag[b]=-3
 T1=[[mul(q(diag[i]),x) for x in G1[i]] for i in range(8)]
 assert [[add(x,y) for x,y in zip(a,b)] for a,b in zip(T0,T1)]==K
 return K

def audit_anchor():
 data=json.loads((SRC/'FOURIER8_NONCOMMUTING_ANCHOR_CONTROLS.json').read_text())
 orders={name:perm(v) for name,v in data['orders'].items()}
 fourier=[[power(zeta,(i*j)%8) for j in range(8)] for i in range(8)]
 answers=[]; exact_transition_count=0; quadcount=0
 for case in data['cases']:
  pi,sigma=[orders[n] for n in case['orders']]
  assert [pi[sigma[i]] for i in range(8)] != [sigma[pi[i]] for i in range(8)]
  B=mm(fourier,butterfly(case['anchor'])) # actual target is B/2; homogeneous gate permits this scale
  ts=triples(pi,sigma); assert ts==[tuple(x['triple']) for x in case['equation_sources']]
  edges=[transition(B,*t,pi,sigma) for t in ts]
  for H,record in zip(edges,case['equation_sources']):
   assert rank2(H)==record['rank']; assert prop(flat(H),flat(parse(record['transition'])))
   exact_transition_count+=1
  T=[parse(x) for x in case['tree_transforms']]
  roots=[]
  for v,path in enumerate(case['forest_paths']):
   # Verify supplied path backward identifies its root, then forward products.
   cur=v
   for ei,rev in reversed(path):
    a,b,_=ts[ei]; assert cur==(a if rev else b); cur=b if rev else a
   root=cur; roots.append(root); cur=root; product=ident(2)
   for ei,rev in path:
    a,b,_=ts[ei]; H=edges[ei]; assert det(H)!=Z
    assert cur==(b if rev else a); cur=a if rev else b
    product=mm(adj(H) if rev else H,product)
   assert cur==v and det(T[v])!=Z and prop(flat(product),flat(T[v]))
  qmap={}
  for ei,((i,k,j),H) in enumerate(zip(ts,edges)):
   if roots[i]==roots[k]:
    cc=quadratic(T[i],T[k],H)
    if any(x!=Z for x in cc): qmap[ei]=cc
  assert len(qmap)==case['nonzero_internal_quadratics']
  assert set(qmap)=={r['edge'] for r in case['internal_quadratics']}
  assert len(set(roots))==case['rank_two_components']
  for record in case['internal_quadratics']:
   assert record['edge'] in qmap
   assert prop(qmap[record['edge']],[q(x) for x in record['coefficients']]);quadcount+=1
  for axrecord in case['axis_guard_checks']:
   er=axrecord['exhaustive_monomial_quadratic']['edge'];root=axrecord['root']
   assert prop(qmap[er],[q(x) for x in axrecord['exhaustive_monomial_quadratic']['coefficients']])
   for candidate in axrecord['candidates']:
    axis=candidate['axis'];viol=candidate['violated_internal_edge']
    if viol is not None: assert qmap[viol][0 if axis==0 else 2]!=Z
    assert candidate['zero_base_rows']==[i for i in range(8) if roots[i]==root and T[i][0][axis]==Z]
  result={'anchor':case['anchor'],'orders':case['orders'],'equations':len(ts),'rank_counts':{r:sum(rank2(H)==r for H in edges) for r in range(3)},'forest_components':len(set(roots))}
  cert=case['certificate']
  if cert:
   for vertex,path in cert['tree_paths'].items(): assert path==case['forest_paths'][int(vertex)]
   for edge,record in cert['source_edges'].items():
    assert tuple(record['triple'])==ts[int(edge)]
    assert prop(flat(edges[int(edge)]),flat(parse(record['transition'])))
   returns=[]
   for ei,record in zip(cert['return_edges'],cert['return_matrices']):
    i,k,j=ts[ei]; assert det(edges[ei])!=Z
    R=mm(mm(adj(T[k]),edges[ei]),T[i]); given=parse(record)
    assert prop(flat(R),flat(given));returns.append(given)
   determinant=det(ms(mm(*returns),mm(*reversed(returns))))
   assert determinant==q(cert['commutator_determinant']) and determinant!=Z
   result.update(verdict='REJECT_DIRECTION_SYSTEM',certificate_kind='nonzero_commutator_determinant',determinant=determinant,return_edges=cert['return_edges'])
  else:
   # Independently select pure monomial quadratics and eliminate axes; no generic root solver or source verdict trusted.
   pure=[(ei,cc,next(i for i,x in enumerate(cc) if x!=Z)) for ei,cc in qmap.items() if sum(x!=Z for x in cc)==1]
   assert pure
   ei,cc,term=pure[0]; possible=[1] if term==0 else ([0] if term==2 else [0,1])
   checks=[]
   for axis in possible:
    root=roots[ts[ei][0]]
    violations=[e for e,c in qmap.items() if roots[ts[e][0]]==root and c[0 if axis==0 else 2]!=Z]
    badrows=[i for i in range(8) if roots[i]==root and T[i][0][axis]==Z]
    checks.append({'axis':axis,'violating_equations':violations,'zero_base_rows':badrows})
    assert violations or badrows
   directional=all(x['violating_equations'] for x in checks)
   result.update(verdict='REJECT_DIRECTION_SYSTEM' if directional else 'REJECT_BASE_GUARD_ONLY',certificate_kind='monomial_quadratic_and_exhaustive_axes',initial_equation=ei,initial_coefficients=cc,axis_checks=checks)
   if not directional:
    assert case['anchor']=='halves' and case['orders']==['natural','bit_reverse']
    assert possible==[0,1] and all(not x['violating_equations'] for x in checks)
    assert checks[0]['zero_base_rows']==[1,3,5,7] and checks[1]['zero_base_rows']==[0,2,4,6]
  answers.append(result)
 # Positive controls from geometric cyclic inverses, no source matrix used.
 controls=[]
 for names in [x['orders'] for x in data['positive_controls']]:
  pi,sigma=[orders[n] for n in names]
  gs=[]
  for p,w in [(pi,2),(sigma,3)]:
   G=[[Z]*8 for _ in range(8)]
   for j in range(8):
    k=j
    for t in range(8): G[k][j]=q(F(w**t,1-w**8));k=p[k]
   gs.append(G)
  B=[[add(x,y) for x,y in zip(a,b)] for a,b in zip(*gs)]
  Q0=ident(8);Q1=ident(8)
  for j in range(8):Q0[pi[j]][j]=q(-2);Q1[sigma[j]][j]=q(-3)
  assert mm(Q0,gs[0])==ident(8) and mm(Q1,gs[1])==ident(8)
  assert mm(mm(Q0,B),Q1)==[[add(x,y) for x,y in zip(a,b)] for a,b in zip(Q0,Q1)]
  count=0
  for i,k,j in triples(pi,sigma):
   H=transition(B,i,k,j,pi,sigma); L=bilinear_L(H);u=[[O],[q(-2)]]
   assert mm(mm([[O,q(-2)]],L),u)==[[Z]];count+=1
  # Scale completion with U=Q0,V=Q1,x=y=1 verifies all entries, including off-support.
  controls.append({'orders':names,'equations_satisfied':count,'full_inverse_identity':True,'linear_scale_completion_all_64_entries':True,'guards':[-255,-6560]})
 return {'cases':answers,'all_source_transitions_recomputed':exact_transition_count,'all_nonzero_internal_quadratics_recomputed':quadcount,'positive_controls':controls,'field':'Q[z]/(z^4+1), exact Fraction coefficients','constructor_code_imported_or_executed':False}

# Independent sparse finite-field matrix engine.
def smm(A,B,p):
 C=[]
 for row in A:
  c={}
  for k,x in row.items():
   for j,y in B[k].items(): c[j]=(c.get(j,0)+x*y)%p
  C.append({j:x for j,x in c.items() if x})
 return C
def sadd(A,B,p):return [{j:(a.get(j,0)+b.get(j,0))%p for j in a.keys()|b.keys() if (a.get(j,0)+b.get(j,0))%p} for a,b in zip(A,B)]
def mono(A):
 n=len(A);return all(len(x)==1 for x in A) and len({next(iter(x)) for x in A})==n
def SI(n):return [{i:1} for i in range(n)]
def transpose(A,p,scale=1):
 B=[{} for _ in A]
 for i,row in enumerate(A):
  for j,x in row.items(): B[j][i]=x*scale%p
 return B
def root(p,n):
 for x in range(1,p):
  if pow(x,n,p)==1 and all(pow(x,n//d,p)!=1 for d in range(2,n+1) if n%d==0):return x
 raise ValueError((p,n))
def diago(values):return [{i:x} for i,x in enumerate(values)]
def srows_equal(A,B):return A==B

def fstage(d,w,p):
 # F_d=C2*C1, two sums of nonsingular monomials (including padding).
 half=pow(2,-1,p)
 if d==1:return ([{0:half}],[{0:half}],[{0:half}],[{0:half}])
 if d==2:
  return (diago([1,p-1]),[{1:1},{0:1}],diago([half]*2),diago([half]*2))
 assert d==4
 D1=diago([1,p-1,1,p-1]); X1=[{1:1},{0:1},{3:1},{2:1}];R=[{0:1},{2:1},{1:1},{3:1}]
 return (smm(D1,R,p),smm(X1,R,p),diago([1,1,p-1,-w%p]),[{2:1},{3:w},{0:1},{1:1}])
def lift_small(A,groups,n):
 B=[{} for _ in range(n)]
 for group in groups:
  for i,row in enumerate(A): B[group[i]]={group[j]:x for j,x in row.items()}
 assert all(B);return B

def bank_case(a,m,b,p,check_layers=True,nonzero_extension=False):
 n=a*m*b;w=root(p,n);pw=[pow(w,k,p) for k in range(n)]
 P=[{} for _ in range(n)]; Q=[{} for _ in range(n)]
 for r0 in range(a):
  for t2 in range(b):
   for r1 in range(m):
    row=(r0*b+t2)*m+r1
    for r2 in range(b):Q[row][r0+a*r1+a*m*r2]=pw[(a*r1*t2+a*m*r2*t2)%n]
   for t1 in range(m):
    col=(r0*b+t2)*m+t1
    for t0 in range(a):P[t2+b*t1+b*m*t0][col]=pw[(r0*(t2+b*t1)+m*b*r0*t0)%n]
 B=[{block*m+j:pw[(a*b*i*j)%n] for j in range(m)} for block in range(a*b) for i in range(m)]
 target=[{j:pw[(i*j)%n] for j in range(n)} for i in range(n)]
 assert smm(smm(P,B,p),Q,p)==target
 # Inverse Fourier block via conjugating root exponents and transposition.
 def invunitary(A,d):
  invvalues={pw[t]:pw[(-t)%n] for t in range(n)}
  return transpose([{j:invvalues[x] for j,x in row.items()} for row in A],p,pow(d,-1,p))
 Pi,Qi=invunitary(P,a),invunitary(Q,b)
 assert smm(P,Pi,p)==SI(n) and smm(Q,Qi,p)==SI(n)
 S=[{(i-1)%n:1} for i in range(n)]; Sm=[{(i+1)%n:1} for i in range(n)];D=diago(pw)
 acts=[smm(smm(Q,S,p),Qi,p),smm(smm(Q,D,p),Qi,p),smm(smm(Pi,D,p),P,p),smm(smm(Pi,Sm,p),P,p)]
 assert all(mono(A) for A in acts)
 result={'N':n,'a':a,'m':m,'b':b,'prime':p,'primitive_root':w,'full_bank_identity':True,'all_four_actual_actions_monomial':True,'support_product':n}
 if check_layers and a in [1,2,4] and b in [1,2,4]:
  gp=[[((r0*b+t2)*m+t1) for r0 in range(a)] for t2 in range(b) for t1 in range(m)]
  gq=[[((r0*b+r2)*m+r1) for r2 in range(b)] for r0 in range(a) for r1 in range(m)]
  pa=[lift_small(X,gp,n) for X in fstage(a,pow(w,n//a,p),p)]
  qb=[lift_small(X,gq,n) for X in fstage(b,pow(w,n//b,p),p)]
  Dp=diago([pw[(r0*(t2+b*t1))%n] for r0 in range(a) for t2 in range(b) for t1 in range(m)])
  Dq=diago([pw[(a*r1*t2)%n] for r0 in range(a) for t2 in range(b) for r1 in range(m)])
  Rq=[{} for _ in range(n)];Rp=[{} for _ in range(n)]
  for r0 in range(a):
   for r2 in range(b):
    for r1 in range(m):Rq[(r0*b+r2)*m+r1]={r0+a*r1+a*m*r2:1}
  for t0 in range(a):
   for t2 in range(b):
    for t1 in range(m):Rp[t2+b*t1+b*m*t0]={(t0*b+t2)*m+t1:1}
  pairs=[(smm(pa[0],Dp,p),smm(pa[1],Dp,p)),(smm(Rp,pa[2],p),smm(Rp,pa[3],p)),(smm(qb[0],Rq,p),smm(qb[1],Rq,p)),(smm(Dq,qb[2],p),smm(Dq,qb[3],p))]
  assert all(mono(x) for pair in pairs for x in pair)
  layers=[sadd(*pair,p) for pair in pairs]
  assert smm(layers[1],layers[0],p)==P and smm(layers[3],layers[2],p)==Q
  result.update(exact_exterior_layers=4,nonsingular_monomial_summands=8,zero_mask_guards=[1]*8)
 return result

def audit_banks():
 cases=[]
 for a,b,m in itertools.product([1,2,4],[1,2,4],[1,2,4,8,16]):cases.append(bank_case(a,m,b,65537))
 for a,m,b,p in [(3,3,1,109),(1,3,3,109),(3,3,3,109),(2,3,2,97),(3,2,2,97),(2,2,3,97)]:cases.append(bank_case(a,m,b,p,False))
 # Every affine/character block over composite 4,6,8 passes the sufficient identity.
 counts={}
 for m,p in [(4,17),(6,13),(8,17)]:
  w=root(p,m);Fmat=[{j:pow(w,i*j,p) for j in range(m)} for i in range(m)]
  Finv=[{j:pow(w,(-i*j)%m,p)*pow(m,-1,p)%p for j in range(m)} for i in range(m)]
  count=0
  for a in range(m):
   if gcd(a,m)!=1:continue
   for b in range(m):
    for c in range(m):
     U=[{} for _ in range(m)]
     for j in range(m):U[(a*j+b)%m][j]=pow(w,c*j,p)
     assert mono(smm(smm(Fmat,U,p),Finv,p));count+=1
  counts[m]=count
 return {'mixed_radix_cases':cases,'composite_affine_character_positive_cases':counts,'scope':'All four actions use the specified orientations Q S Q^-1, Q D Q^-1, P^-1 D P, P^-1 S^-1 P; not an assertion about P conjugating both standard generators.'}

def audit_f4():
 records=[]
 for p in [17,41,73,89,97,113,137,193,233,241,257]:
  for chi in range(1,p):
   if pow(chi,4,p)!=p-1:continue
   i=chi*chi%p;a=pow(chi,-1,p);h=(chi+a)%p
   roots=[r for r in range(p) if (r*r+h*r+i)%p==0]
   rec={'prime':p,'chi':chi,'root_count':len(roots)}
   if len(roots)==2:
    r,s=roots;A=(a-s)*pow((r-s)%p,-1,p)%p;B=(r-a)*pow((r-s)%p,-1,p)%p
    guards=[(1-pow(t,4,p))%p for t in roots]
    assert r and s and A and B and all(guards) and guards[0]*guards[1]%p==8*i%p
    c=[(A*pow(r,t,p)+B*pow(s,t,p))%p for t in range(4)]
    assert c==[pow(chi,(-t*t)%8,p) for t in range(4)]
    assert all(pow(chi,u*u+v*v,p)*c[(u-v)%4]%p==pow(i,u*v,p) for u in range(4) for v in range(4))
    rec.update(guards=guards,endpoint_coefficients=[A,B],exact_F4=True)
   records.append(rec)
 # Explicit F25=F5[t]/(t²-2) repeated-root branch: chi=2t, i=3, h=t, r=s=2t.
 def a25(a,b):return ((a[0]+b[0])%5,(a[1]+b[1])%5)
 def m25(a,b):return ((a[0]*b[0]+2*a[1]*b[1])%5,(a[0]*b[1]+a[1]*b[0])%5)
 def p25(a,n):
  x=(1,0)
  for _ in range(n):x=m25(x,a)
  return x
 chi=(0,2);ii=p25(chi,2);h=a25(chi,p25(chi,7));rr=(0,2)
 assert p25(chi,4)==(4,0) and p25(chi,8)==(1,0) and ii==(3,0) and h==(0,1)
 assert a25(m25(h,h),m25((1,0),ii))==(0,0) # h²-4i=h²+i in char5
 roots=[(u,v) for u in range(5) for v in range(5) if a25(a25(m25((u,v),(u,v)),m25(h,(u,v))),ii)==(0,0)]
 assert roots==[rr] and p25(rr,4)==(4,0)
 ranks=[]
 for p in [17,97,113,193,241,257]:
  ch=root(p,16);w=ch*ch%p;c=[pow(ch,(-t*t)%16,p) for t in range(8)]
  M=[[c[(k-j)%8] for j in range(5)] for k in range(3,8)]
  vand=1
  nodes=[pow(w,j,p) for j in range(5)]
  for j in range(5):
   for k in range(j+1,5):vand=vand*(nodes[k]-nodes[j])%p
  fact=1
  for k in range(3,8):fact=fact*pow(ch,(-k*k)%16,p)%p
  for j in range(5):fact=fact*pow(ch,(-j*j)%16,p)*pow(w,3*j,p)%p
  A=[row[:] for row in M];dd=1
  for col in range(5):
   pivot=next(r for r in range(col,5) if A[r][col]);
   if pivot!=col:A[col],A[pivot]=A[pivot],A[col];dd=-dd
   x=A[col][col];dd=dd*x%p
   for r in range(col+1,5):
    k=A[r][col]*pow(x,-1,p)%p
    A[r]=[(u-k*v)%p for u,v in zip(A[r],A[col])]
  assert dd==vand*fact%p and dd
  ranks.append({'prime':p,'chi':ch,'determinant':dd,'vandermonde_factor_verified':True})
 return {'all_primitive_eighth_roots_in_11_prime_fields':records,'split_positive_cases':sum(r.get('exact_F4',False) for r in records),'missing_split_cases':sum(r['root_count']==0 for r in records),'repeated_root_extension_control':{'field':'F5[t]/(t²-2)','chi':[0,2],'i':[3,0],'h':[0,1],'r_equals_s':[0,2],'discriminant':0,'root_count':1,'rejected_by_required_distinctness_guard':True,'individual_Green_guard':2},'F8_commuting_vandermonde_controls':ranks}

def main():
 closure=json.loads(CLOSURE.read_text()); inputs={str(CLOSURE):hashlib.sha256(CLOSURE.read_bytes()).hexdigest()}
 for item in closure['pending_separate_audits']:
  for member in item['members']:
   f=Path(member['path']); actual=hashlib.sha256(f.read_bytes()).hexdigest();assert actual==member['sha256'];inputs[str(f)]=actual
  f=Path(item['manifest']);actual=hashlib.sha256(f.read_bytes()).hexdigest();assert actual==item['manifest_sha256'];inputs[str(f)]=actual
 dependency=Path('research_round_2156/projective_row_gate/PROJECTIVE_CONSISTENCY_GATE.md');inputs[str(dependency)]=hashlib.sha256(dependency.read_bytes()).hexdigest()
 results={'inputs_sha256':inputs,'independence':{'source_programs_imported':False,'source_programs_executed':False,'source_programs_used_as_algorithm_text':False,'source_JSON_used_as_untrusted_certificate_data':True},'F8_anchor':audit_anchor(),'monomial_sections_7_8':audit_banks(),'F4_and_commuting_F8':audit_f4(),'all_assertions_passed':True}
 (OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(serial(results),indent=2)+'\n')
 print(json.dumps({'all_assertions_passed':True,'anchor_cases':len(results['F8_anchor']['cases']),'source_transitions_recomputed':results['F8_anchor']['all_source_transitions_recomputed'],'mixed_radix_cases':len(results['monomial_sections_7_8']['mixed_radix_cases']),'F4_split_controls':results['F4_and_commuting_F8']['split_positive_cases']}))
if __name__=='__main__':main()
