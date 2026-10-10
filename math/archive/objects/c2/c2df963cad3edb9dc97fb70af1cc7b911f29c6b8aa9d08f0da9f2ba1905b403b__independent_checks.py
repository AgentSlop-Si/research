"""Audit-authored checks. Uploaded programs are never imported or executed.
Only the uploaded JSON certificates/audit values are read as data.
Run: python3 independent_checks.py [audit-root] [output-json]
"""
from pathlib import Path
import json, sys, random, math
from itertools import combinations
BASE=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else BASE/'research/INDEPENDENT_RESULTS.json'
SOURCE=BASE/'extracted/fft_green_research_phase28_2026-10-10(1)/fft_green_phase28_internal_phase_synthesis'
P=998244353

def mm(a,b,p=P):
 return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]
def tr(a):return list(map(list,zip(*a)))
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def rref(a,p=P):
 a=[r[:] for r in a]; piv=[]; h=0
 if not a:return a,piv
 for j in range(len(a[0])):
  t=next((i for i in range(h,len(a)) if a[i][j]%p),None)
  if t is None:continue
  a[t],a[h]=a[h],a[t]; u=pow(a[h][j],-1,p); a[h]=[x*u%p for x in a[h]]
  for i in range(len(a)):
   if i!=h:
    v=a[i][j]; a[i]=[(x-v*y)%p for x,y in zip(a[i],a[h])]
  piv.append(j); h+=1
  if h==len(a):break
 return a,piv
def rk(a,p=P):return len(rref(a,p)[1])
def inv(a):
 n=len(a); r,piv=rref([row+e for row,e in zip(a,eye(n))]);assert piv[:n]==list(range(n))
 b=[row[n:] for row in r];assert mm(a,b)==eye(n);return b
def null(a,w,p):
 r,piv=rref(a,p);out=[]
 for j in range(w):
  if j in piv:continue
  v=[0]*w;v[j]=1
  for k,i in enumerate(piv):v[i]=-r[k][j]%p
  out.append(v)
 assert all(all(sum(x*y for x,y in zip(row,v))%p==0 for row in a) for v in out)
 return out
def det(a,p):
 a=[row[:] for row in a]; v=1
 for j in range(len(a)):
  k=next((i for i in range(j,len(a)) if a[i][j]%p),None)
  if k is None:return 0
  if k!=j:a[j],a[k]=a[k],a[j];v=-v
  d=a[j][j];v=v*d%p;d=pow(d,-1,p)
  for i in range(j+1,len(a)):
   t=a[i][j]*d%p
   for l in range(j,len(a)):a[i][l]=(a[i][l]-t*a[j][l])%p
 return v%p

def params(n,seed):
 # The published seed defines these integers. No uploaded code is evaluated.
 g=random.Random(seed);out=[]
 for den in [4,5]:
  order=list(range(n));g.shuffle(order)
  left=[g.randrange(n) for _ in range(n)];right=[g.randrange(n) for _ in range(n)]
  out.append({'denominator':den,'order':order,'left_exponents':left,'right_exponents':right})
 return out

def component(n,t):
 w=pow(3,-((P-1)//n),P); assert pow(w,n,P)==1 and pow(w,n//2,P)!=1
 # Solve the sparse resolvent directly, independently of distance-table formula.
 b=eye(n); order=t['order'];alpha=pow(t['denominator'],-1,P)
 for k,j in enumerate(order):b[order[(k+1)%n]][j]=(b[order[(k+1)%n]][j]-alpha)%P
 g=inv(b)
 return [[g[i][j]*pow(w,t['left_exponents'][i]+t['right_exponents'][j],P)%P for j in range(n)] for i in range(n)]
def mixer(n,seed):
 ps=params(n,seed); cs=[component(n,t) for t in ps];z=3*pow(2,-1,P)%P
 return [[(x+z*y)%P for x,y in zip(a,b)] for a,b in zip(*cs)],cs,ps

def moments(m,p=P):
 n=len(m); assert all(x%p for row in m for x in row)
 # Direct per-entry inverses, and ratio powers; independent of saved polynomials.
 im=[[pow(x,-1,p) for x in row] for row in m]; totals=[n**3,n**3]
 for i in range(n):
  for j in range(i):
   u=[m[i][k]*im[j][k]%p for k in range(n)]
   v=[m[j][k]*im[i][k]%p for k in range(n)]
   totals[0]+=2*sum(u)*sum(v)
   totals[1]+=2*sum(x*x%p for x in u)*sum(x*x%p for x in v)
 return [x%p for x in totals]
def peval(a,x,p=P):
 y=0
 for v in reversed(a):y=(y*x+v)%p
 return y
def pmul(a,b,p=P):
 out=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]=(out[i+j]+x*y)%p
 return out

def phase_checks():
 data=json.loads((SOURCE/'audit.json').read_text());reports=[]; allparams={};sample_count=0
 for record in data['certificates']:
  n=record['N'];seed=2800+n;A,_,pa=mixer(n,3*seed+1);B,(B0,B1),pb=mixer(n,3*seed+2);C,_,pc=mixer(n,3*seed+3)
  allparams[str(n)]={'A':pa,'B':pb,'C':pc}
  w=pow(3,-((P-1)//n),P);F=[[pow(w,i*j,P) for j in range(n)] for i in range(n)]
  T=mm(mm(inv(A),F),inv(C)); mt=moments(T);mb=moments(B)
  diff=(mt[0]-mb[0])%P;assert diff==record['nonzero_difference'] and diff
  report={'n':n,'trace_difference':diff,'target_entries_nonzero':True,'outer_inverses_verified':True}
  if n<=16:
   cert=json.loads((SOURCE/f'certificates/bezout_N{n}.json').read_text());p1=cert['p1_coefficients'];p2=cert['p2_coefficients']
   u=pmul(p1,cert['bezout_u']);v=pmul(p2,cert['bezout_v']);identity=[((u[k] if k<len(u) else 0)+(v[k] if k<len(v) else 0))%P for k in range(max(len(u),len(v)))]
   assert identity[0]==1 and not any(identity[1:])
   E=cert['removed_denominator_factor'];rem=[cert['removed_from_p1'],cert['removed_from_p2']]
   assert [len(p1)-1,len(p2)-1]==[n*n-rem[0],2*n*n-rem[1]] and p1[-1] and p2[-1]
   if n==16:
    assert E==[B0[5][5],B1[5][5]]
    diag=[[ (t['left_exponents'][i]+t['right_exponents'][i])%n for i in [5,6,15]] for t in pb]
    assert diag==[[7,4,4],[3,0,0]]
    # Exact cyclotomic ratio is shared, not merely accidentally equal mod p.
    assert len(set((a-b)%n for a,b in zip(*diag)))==1
    report['characteristic_zero_factor_exponents']=diag
   checked=[0,0]
   # d+1 distinct exact evaluations identify each degree<=d polynomial.
   for z in range(2*n*n+1):
    M=[[(x+z*y)%P for x,y in zip(a,b)] for a,b in zip(B0,B1)]
    assert all(x for row in M for x in row)
    obs=moments(M);D=math.prod(x for row in M for x in row)%P
    for s,poly in enumerate([p1,p2],1):
     if z>s*n*n:continue
     lhs=peval(poly,z)* (pow(peval(E,z),rem[s-1],P) if E else 1)%P
     rhs=pow(D,s,P)*(obs[s-1]-mt[s-1])%P
     assert lhs==rhs,(n,s,z)
     checked[s-1]+=1;sample_count+=1
   report.update({'degree_certificates':[len(p1)-1,len(p2)-1],'polynomial_identifying_evaluations':checked,'bezout_identity':True})
  reports.append(report)
  print('phase',n,'passed',flush=True)
 return reports,allparams,sample_count

def root(n,p):
 assert (p-1)%n==0
 fac=[q for q in range(2,n+1) if n%q==0 and all(q%d for d in range(2,math.isqrt(q)+1))]
 for a in range(2,p):
  w=pow(a,(p-1)//n,p)
  if all(pow(w,n//q,p)!=1 for q in fac):return w
 raise AssertionError

def stage(n,r,rng,p):
 # Sum r independently generated rank-one separated matrices + arbitrary diagonal.
 a=[[rng.randrange(0,p) for _ in range(n)] for _ in range(r)]
 b=[[rng.randrange(0,p) for _ in range(n)] for _ in range(r)]
 c=[[rng.randrange(0,p) for _ in range(n)] for _ in range(r)]
 e=[[rng.randrange(0,p) for _ in range(n)] for _ in range(r)]
 d=[rng.randrange(p) for _ in range(n)]
 return [[d[i] if i==j else sum(a[t][i]*b[t][j] if i>j else c[t][i]*e[t][j] for t in range(r))%p for j in range(n)] for i in range(n)]
def mv(a,x,p):return [sum(v*y for v,y in zip(row,x))%p for row in a]
def perm(x,q):
 y=[0]*len(x)
 for i,j in enumerate(q):y[j]=x[i]
 return y
def sparse_witness(n,r1,r2,p,seed,zero=False):
 rng=random.Random(seed);s=2*r1+1;w=s+r2; S1=stage(n,r1,rng,p);S2=stage(n,r2,rng,p)
 if zero:S1=[[0]*n for _ in range(n)]
 q=list(range(n));rng.shuffle(q);omega=root(n,p)
 # Only the right tail of first w output rows needs annihilating.
 Y=null(tr([row[w:] for row in S2[:w]]),w,p)[:s];assert len(Y)==s and rk(Y,p)==s
 forbidden=bad=valid=0;first=None
 for j in range(n-s+1):
  J=list(range(j,j+s)); X=null([[row[k] for k in J] for row in S1[:j]+S1[j+s:]],s,p);assert X
  hit=bool(set(q[j:j+s])&set(range(w)))
  PF=[[sum(y[i]*pow(omega,i*k,p) for i in range(w))%p for k in J] for y in Y]
  singular=det(PF,p)==0
  forbidden+=hit;bad+=singular
  if hit or singular:continue
  valid+=1;v=[0]*n;v[j:j+s]=X[0]
  got=mv(S2,perm(mv(S1,v,p),q),p)
  projected=mv(Y,got[:w],p);assert not any(projected)
  projected_f=mv(PF,X[0],p);assert any(projected_f)
  if first is None:first={'start':j,'input':X[0],'fourier_projection':projected_f}
 assert forbidden<=s*w and bad<=s*r2 and valid>=n+1-s*(s+2*r2+1)>0
 return {'n':n,'r1':r1,'r2':r2,'prime':p,'zero_first_stage':zero,'valid_witness_positions':valid,'guaranteed_positions':n+1-s*(s+2*r2+1),'forbidden':forbidden,'singular':bad,'first':first}

def defect(R,C,n):
 return min(min(sum(x>t for x in R)+sum(x<=t for x in C),sum(x<=t for x in R)+sum(x>t for x in C)) for t in range(-1,n))
def outside(start,w,n):return int(start>0)+int(start+w<n)
def boundary_rank_checks():
 p=12289;rng=random.Random(47392);cnt=0;strict=0
 for n in [8,16,32]:
  for rep in range(5):
   ranks=[rng.randrange(1,3) for _ in range(3)];ss=[stage(n,r,rng,p) for r in ranks]
   qs=[]
   for _ in range(2):q=list(range(n));rng.shuffle(q);qs.append(q)
   # Build columns using directly multiplied matrices and explicit permutations.
   M=tr([mv(ss[2],perm(mv(ss[1],perm(mv(ss[0],e,p),qs[0]),p),qs[1]),p) for e in eye(n)])
   invq=[0]*n
   for i,j in enumerate(qs[1]):invq[j]=i
   for w in range(1,n+1):
    for i in sorted(set([0,(n-w)//2,n-w])):
     for j in sorted(set([0,(n-w)//2,n-w])):
      R=[invq[k] for k in range(i,i+w)];C=qs[0][j:j+w]
      k=defect(R,C,n);bound=outside(j,w,n)*ranks[0]+outside(i,w,n)*ranks[2]+ranks[1]+k
      observed=rk([row[j:j+w] for row in M[i:i+w]],p)
      assert observed<=bound
      cnt+=1;strict+=bound<2*ranks[0]+2*ranks[2]+ranks[1]+k
 return {'matrix_window_tests':cnt,'strictly_smaller_boundary_budgets':strict}

def expectation_checks():
 cases=0
 for n in range(2,10):
  for w in range(1,min(4,n//2)+1):
   sets=list(combinations(range(n),w));num=sum(max(a)<min(b) or max(b)<min(a) for a in sets for b in sets)
   assert num==2*math.comb(n,2*w);cases+=1
 return cases

if __name__=='__main__':
 phases,parameters,evaluations=phase_checks()
 witness=[]
 # Exact threshold N=18 and non-dyadic cases are included.
 for n,p in [(18,109),(24,97),(32,12289),(64,12289)]:
  for seed in range(4):witness.append(sparse_witness(n,1,1,p,100+seed,seed==0))
 for n,r1,r2,p in [(40,2,1,241),(48,1,2,193),(64,2,2,12289)]:
  for seed in range(3):witness.append(sparse_witness(n,r1,r2,p,300+seed,seed==0))
 ranks=boundary_rank_checks();expect=expectation_checks()
 result={'phase28':phases,'polynomial_identifying_evaluations':evaluations,'explicit_cycle_gauges':parameters,'sparse_boundary_witnesses':witness,'boundary_rank_checks':ranks,'exhaustive_ordered_subset_counts':expect,'all_passed':True}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'phase_lengths':len(phases),'polynomial_identifying_evaluations':evaluations,'sparse_witness_cases':len(witness),'boundary_rank_checks':ranks,'ordered_subset_cases':expect,'all_passed':True},indent=2))
