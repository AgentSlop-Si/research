#!/usr/bin/env python3
"""Independent exact-math audit. Does not import or execute archive source.
This deliberately dense reference checker is not an implementation of the
claimed linear-time recognizers. Run: python3 audit/independent_checks.py
"""
import ast, hashlib, itertools, json, math, pathlib, random
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'extracted/hero17_shear_gauge'
RNG=random.Random(211517)
COUNT={}
def count(k,n=1):COUNT[k]=COUNT.get(k,0)+n

def prime(p):return p>1 and all(p%d for d in range(2,math.isqrt(p)+1))
def field(n):
 p=n+1
 while not prime(p):p+=n
 for w in range(2,p):
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0):return p,w
 raise AssertionError('root')
def dft(x,w,p):
 n=len(x);out=[]
 for h in range(n):
  step=pow(w,-h,p);v=1;s=0
  for z in x:s=(s+z*v)%p;v=v*step%p
  out.append(s)
 return out
def idft(x,w,p):return [z*pow(len(x),-1,p)%p for z in dft(x,pow(w,-1,p),p)]
def solve(mat,b,p):
 n=len(b);a=[[v%p for v in row]+[b[i]%p] for i,row in enumerate(mat)]
 for j in range(n):
  i=next((i for i in range(j,n) if a[i][j]),None)
  if i is None:return None
  a[j],a[i]=a[i],a[j];iv=pow(a[j][j],-1,p);a[j]=[v*iv%p for v in a[j]]
  for i in range(n):
   if i!=j:
    v=a[i][j];a[i]=[(a[i][k]-v*a[j][k])%p for k in range(n+1)]
 return [row[-1] for row in a]
def polyprod(factors,p):
 c=[1]
 for f in factors:
  z=[0]*(len(c)+len(f)-1)
  for i,a in enumerate(c):
   for j,b in enumerate(f):z[i+j]=(z[i+j]+a*b)%p
  c=z
 return c
def rows_to_x(rows):return [rows[t][u] for u in range(len(rows[0])) for t in range(len(rows))]
def x_to_rows(x,q):return [[x[t+q*u] for u in range(len(x)//q)] for t in range(q)]
def G(z,L,p):return (L%p if z%p==1 else (1-pow(z,L,p))*pow(1-z,-1,p)%p)
def B(z,L,d,p):
 if not L:return 0
 if z%p==1:return math.comb(L+d-1,d)%p
 s=sum(math.comb(L+j-1,j)*pow(1-z,j,p) for j in range(d))%p
 return (1-pow(z,L,p)*s)*pow(pow(1-z,d,p),-1,p)%p

def params(m,p,w,g):
 # omega^j occupy distinct cosets of <omega^Q> when j<Q.
 return [(a,pow(w,j,p)) for j,a in enumerate(RNG.sample(range(m),g))]
def make_orbits(q,m,p,w,par):
 eta=pow(w,q,p);spec=[[RNG.randrange(1,p) for _ in range(m)] for _ in par]
 bases=[idft(z,eta,p) for z in spec]
 rows=[[sum(pow(mu,t,p)*bases[j][(u-a*t)%m] for j,(a,mu) in enumerate(par))%p for u in range(m)] for t in range(q)]
 return rows,spec

def recover(rows,p,w,g):
 q=len(rows);m=len(rows[0]);eta=pow(w,q,p)
 if q<2*g or m<g:return None
 C=[dft(row,eta,p) for row in rows[:2*g]];chars=[]
 for h in range(m):
  coeff=solve([[C[i+j][h] for j in range(g)] for i in range(g)],[-C[i+g][h] for i in range(g)],p)
  if coeff is None:return None
  chars.append(coeff+[1])
 trace=[-c[-2]%p for c in chars];F=dft(trace,eta,p);im=pow(m,-1,p)
 par=[((-h)%m,z*im%p) for h,z in enumerate(F) if z]
 if len(par)!=g:return None
 spec=[[0]*m for _ in par]
 for h in range(m):
  nodes=[mu*pow(eta,-a*h,p)%p for a,mu in par]
  val=solve([[pow(lam,t,p) for lam in nodes] for t in range(g)],[C[t][h] for t in range(g)],p)
  if val is None:return None
  for j,v in enumerate(val):spec[j][h]=v
 for t in range(2*g):
  if any(sum(spec[j][h]*pow(mu*pow(eta,-a*h,p)%p,t,p) for j,(a,mu) in enumerate(par))%p!=C[t][h] for h in range(m)):return None
 return par,spec

def full_orbit_output(q,m,p,w,par,spec):
 return [sum(spec[j][k%m]*G(mu*pow(w,-k-q*a*(k%m),p)%p,q,p) for j,(a,mu) in enumerate(par))%p for k in range(q*m)]
def scalar_recurrence(par,h,eta,p):return polyprod([[1,-mu*pow(eta,-a*h,p)%p] for a,mu in par],p)
def make_green(rows,p,w,par,events):
 q=len(rows);m=len(rows[0]);eta=pow(w,q,p);g=len(par)
 C=[dft(row,eta,p) for row in rows]
 for t in range(2*g,q):
  for h in range(m):
   co=scalar_recurrence(par,h,eta,p)
   C[t][h]=(m*events.get((t,h),0)-sum(co[l]*C[t-l][h] for l in range(1,g+1)))%p
 return [idft(row,eta,p) for row in C]
def detect_green(rows,p,w,g,budget):
 rec=recover(rows,p,w,g)
 if rec is None:return None
 q=len(rows);m=len(rows[0]);eta=pow(w,q,p);par,spec=rec
 C=[dft(row,eta,p) for row in rows];events={}
 for t in range(2*g,q):
  for h in range(m):
   co=scalar_recurrence(par,h,eta,p)
   r=(C[t][h]+sum(co[l]*C[t-l][h] for l in range(1,g+1)))%p
   if r:events[t,h]=r*pow(m,-1,p)%p
 if len(events)>budget:return None
 return par,spec,events

def full_green_output(q,m,p,w,par,spec,events):
 out=full_orbit_output(q,m,p,w,par,spec);eta=pow(w,q,p);g=len(par)
 for (t,h),c in events.items():
  lam=[mu*pow(eta,-a*h,p)%p for a,mu in par]
  weights=[pow(z,g-1,p)*pow(math.prod((z-v)%p for i,v in enumerate(lam) if i!=j)%p,-1,p)%p for j,z in enumerate(lam)]
  for s in range(q):
   k=h+m*s;z=pow(w,-k,p)
   out[k]=(out[k]+m*c*pow(z,t,p)*sum(weights[j]*G(z*lam[j]%p,q-t,p) for j in range(g)))%p
 return out

def gauge_vote(c0,c1,eta,p):
 m=len(c0);logs={pow(eta,t,p):t for t in range(m)};votes={}
 for h in range(m):
  for k in range(h+1,m):
   if math.gcd(k-h,m)!=1 or not c0[h]*c0[k]*c1[h]*c1[k]%p:continue
   r0=c1[h]*pow(c0[h],-1,p)%p;r1=c1[k]*pow(c0[k],-1,p)%p
   log=logs.get(r1*pow(r0,-1,p)%p)
   if log is None:continue
   a=-log*pow(k-h,-1,m)%m;mu=r0*pow(eta,a*h,p)%p
   votes[a,mu]=votes.get((a,mu),0)+1
 if not votes:return None
 best=max(votes,key=votes.get)
 return best if votes[best]*2>sum(votes.values()) else None

def check_gauged_newton(q,m,p,w,d):
 eta=pow(w,q,p);a=RNG.randrange(m);mu=RNG.randrange(1,p)
 first_spec=[RNG.randrange(1,p) for _ in range(m)];initial=[idft(first_spec,eta,p)]
 if d>1:initial.append(initial[0][:])
 while len(initial)<d:initial.append([RNG.randrange(p) for _ in range(m)])
 events={}
 for t in range(max(d,2),q):
  if RNG.randrange(3)==0:events[t,RNG.randrange(m)]=RNG.randrange(1,p)
 rows=[r[:] for r in initial]
 for t in range(d,q):
  row=[]
  for u in range(m):
   forcing=sum(c*pow(eta,h*u,p) for (tt,h),c in events.items() if tt==t)
   row.append((forcing+sum((-1)**(j+1)*math.comb(d,j)*rows[t-j][u] for j in range(1,d+1)))%p)
  rows.append(row)
 raw=[[pow(mu,t,p)*rows[t][(u-a*t)%m]%p for u in range(m)] for t in range(q)]
 vote=gauge_vote(dft(raw[0],eta,p),dft(raw[1],eta,p),eta,p);assert vote==(a,mu)
 init=[dft(r,eta,p) for r in rows[:d]];forward=[[sum((-1)**(j-i)*math.comb(j,i)*init[i][h] for i in range(j+1))%p for h in range(m)] for j in range(d)]
 out=[]
 for k in range(q*m):
  h=k%m;z=mu*pow(w,-k-q*a*h,p)%p
  v=sum(forward[j][h]*pow(z,j,p)*B(z,q-j,j+1,p) for j in range(d))
  v+=sum(m*c*pow(z,t,p)*B(z,q-t,d,p) for (t,hh),c in events.items() if hh==h)
  out.append(v%p)
 assert out==dft(rows_to_x(raw),w,p)
 count('gauge_full_vectors');count('gauge_full_bins',q*m)

def compositions(D,g):
 if g==1:yield (D,);return
 for a in range(1,D-g+2):
  for rest in compositions(D-a,g-1):yield (a,)+rest

def confluent_reference(q,m,p,w,par,mults):
 D=sum(mults);g=len(par);eta=pow(w,q,p);columns=[(j,r) for j in range(g) for r in range(mults[j])]
 A=[[RNG.randrange(1,p) for _ in range(m)] for col in columns]
 C=[]
 for t in range(q):C.append([sum(A[c][h]*math.comb(t,r)*pow(mu*pow(eta,-a*h,p)%p,t,p) for c,(j,r) in enumerate(columns) for a,mu in [par[j]] if t>=r)%p for h in range(m)])
 events={}
 for t in range(2*D,q):
  if RNG.randrange(2):events[t,RNG.randrange(m)]=RNG.randrange(1,p)
 co_by_h=[polyprod([[1,-mu*pow(eta,-a*h,p)%p] for (a,mu),d in zip(par,mults) for _ in range(d)],p) for h in range(m)]
 for t in range(2*D,q):
  for h in range(m):C[t][h]=(m*events.get((t,h),0)-sum(co_by_h[h][l]*C[t-l][h] for l in range(1,D+1)))%p
 rows=[idft(c,eta,p) for c in C]
 # Recover all poles and multiplicities from a fresh exact Hankel trace.
 pilot=[dft(r,eta,p) for r in rows[:2*D]];char=[]
 for h in range(m):
  c=solve([[pilot[r+s][h] for s in range(D)] for r in range(D)],[-pilot[r+D][h] for r in range(D)],p)
  assert c is not None;char.append(c+[1])
 ft=dft([-c[-2]%p for c in char],eta,p)
 ar=[((-h)%m,rho*pow(m,-1,p)%p) for h,rho in enumerate(ft) if rho]
 assert len(ar)==g
 candidates=[]
 for ds in compositions(D,g):
  ps=[(a,rho*pow(d,-1,p)%p) for (a,rho),d in zip(ar,ds)]
  if all(polyprod([[-mu*pow(eta,-a*h,p)%p,1] for (a,mu),d in zip(ps,ds) for _ in range(d)],p)==char[h] for h in range(m)):candidates.append((ps,ds))
 assert len(candidates)==1
 ps,ds=candidates[0];assert sorted((a,mu,d) for (a,mu),d in zip(ps,ds))==sorted((a,mu,d) for (a,mu),d in zip(par,mults))
 # Derive partial-fraction weights by fitting D initial impulse coefficients.
 weights=[]
 for h in range(m):
  co=co_by_h[h];imp=[]
  for v in range(q):imp.append((1 if v==0 else -sum(co[l]*imp[v-l] for l in range(1,min(v,D)+1)))%p)
  poles=[mu*pow(eta,-a*h,p)%p for a,mu in par]
  green_cols=[(j,r) for j,d in enumerate(mults) for r in range(1,d+1)]
  mat=[[math.comb(v+r-1,r-1)*pow(poles[j],v,p)%p for j,r in green_cols] for v in range(D)]
  wt=solve(mat,imp[:D],p);assert wt is not None
  for v in range(q):assert sum(wt[c]*math.comb(v+r-1,r-1)*pow(poles[j],v,p) for c,(j,r) in enumerate(green_cols))%p==imp[v]
  weights.append(wt)
 out=[]
 for k in range(q*m):
  h=k%m;z=pow(w,-k,p);poles=[mu*pow(eta,-a*h,p)%p for a,mu in par]
  val=sum(A[c][h]*pow(z*poles[j]%p,r,p)*B(z*poles[j]%p,q-r,r+1,p) for c,(j,r) in enumerate(columns))
  for (t,hh),c in events.items():
   if h==hh:val+=m*c*pow(z,t,p)*sum(weights[h][i]*B(z*poles[j]%p,q-t,r,p) for i,(j,r) in enumerate(green_cols))
  out.append(val%p)
 assert out==dft(rows_to_x(rows),w,p)
 count('confluent_full_vectors');count('confluent_full_bins',q*m)

def main():
 # Parse source only. Uploaded Python is never imported or run.
 trees={f.name:ast.parse(f.read_text()) for f in SRC.glob('*.py')}
 tests={n:sum(isinstance(z,(ast.FunctionDef,ast.AsyncFunctionDef)) and z.name.startswith('test_') for z in ast.walk(t)) for n,t in trees.items() if n.startswith('test_')}
 manifest=json.loads((SRC/'MANIFEST.json').read_text())
 verified=[]
 for rec in manifest['files']:
  b=(SRC/rec['path']).read_bytes();assert len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256'];verified.append(rec['path'])
 count('source_test_definitions',sum(tests.values()));count('source_manifest_entries',len(verified))
 for p in (17,97):
  for z in range(p):
   for L in range(0,10):
    assert G(z,L,p)==sum(pow(z,t,p) for t in range(L))%p;count('geometric_kernel_checks')
    for d in range(1,5):
     assert B(z,L,d,p)==sum(math.comb(t+d-1,d-1)*pow(z,t,p) for t in range(L))%p;count('binomial_kernel_checks')
 configs=[(4,4),(6,5),(6,6),(8,8),(8,9),(12,12),(16,16)]
 for q,m in configs:
  p,w=field(q*m);eta=pow(w,q,p)
  for g in range(1,min(3,q//2,m)+1):
   for rep in range(5):
    par=params(m,p,w,g);rows,spec=make_orbits(q,m,p,w,par);recovered=recover(rows,p,w,g);assert recovered is not None
    rp,rs=recovered;assert sorted(par)==sorted(rp)
    assert full_orbit_output(q,m,p,w,rp,rs)==dft(rows_to_x(rows),w,p)
    count('orbit_full_vectors');count('orbit_full_bins',q*m)
    events={(t,RNG.randrange(m)):RNG.randrange(1,p) for t in range(2*g,q) if RNG.randrange(2)}
    grown=make_green(rows,p,w,par,events);cert=detect_green(grown,p,w,g,len(events));assert cert is not None
    cp,cs,ce=cert;assert ce==events
    assert full_green_output(q,m,p,w,cp,cs,ce)==dft(rows_to_x(grown),w,p)
    count('green_full_vectors');count('green_full_bins',q*m)
    if events:assert detect_green(grown,p,w,g,len(events)-1) is None;count('tight_budget_rejections')
  for d in range(1,min(q,4)+1):
   for rep in range(5):check_gauged_newton(q,m,p,w,d)
  for g in range(1,min(3,q//2,m)+1):
   for rep in range(10):
    raw=[[RNG.randrange(p) for _ in range(m)] for _ in range(q)]
    cert=detect_green(raw,p,w,g,0)
    if cert is None:count('dense_rejections')
    else:
     cp,cs,ce=cert;assert full_green_output(q,m,p,w,cp,cs,ce)==dft(rows_to_x(raw),w,p);count('dense_accepted_exact')
 # Adversarial gauge errors, including zero C1 values and composite M.
 for m in (5,6,8,9,10,12,15,16):
  q=m;p,w=field(q*m);eta=pow(w,q,p)
  for rep in range(40):
   a=RNG.randrange(m);mu=RNG.randrange(1,p);c0=[RNG.randrange(1,p) for _ in range(m)];c1=[mu*pow(eta,-a*h,p)*c0[h]%p for h in range(m)]
   e=(m-1)//4
   for h in RNG.sample(range(m),e):c1[h]=RNG.randrange(p)
   assert gauge_vote(c0,c1,eta,p)==(a,mu);count('adversarial_gauge_recoveries')
 # Degeneracy excludes actual structured signals; do not call rejection error.
 q=m=4;p,w=field(16)
 assert recover([[0]*m for _ in range(q)],p,w,1) is None;count('degenerate_pilot_rejections')
 par=[(0,1),(1,1)];rows,spec=make_orbits(q,m,p,w,par)
 assert recover(rows,p,w,2) is None;count('degenerate_pilot_rejections')
 # Universal basis fixed ahead of raw input. Direct reference recovery/evaluation.
 for m in (2,3,4,5,6,8):
  n=m*m;p,w=field(n);eta=pow(w,m,p);par=[(j,pow(w,j,p)) for j in range(m)]
  for rep in range(4):
   x=[RNG.randrange(p) for _ in range(n)];rows=x_to_rows(x,m);C=[dft(r,eta,p) for r in rows];spec=[[0]*m for _ in range(m)]
   for h in range(m):
    lam=[mu*pow(eta,-a*h,p)%p for a,mu in par];assert len(set(lam))==m
    co=solve([[pow(z,t,p) for z in lam] for t in range(m)],[C[t][h] for t in range(m)],p);assert co is not None
    for j,z in enumerate(co):spec[j][h]=z
   bases=[idft(s,eta,p) for s in spec]
   rebuilt=[[sum(pow(mu,t,p)*bases[j][(u-a*t)%m] for j,(a,mu) in enumerate(par))%p for u in range(m)] for t in range(m)]
   assert rows_to_x(rebuilt)==x
   assert full_orbit_output(m,m,p,w,par,spec)==dft(x,w,p)
   assert recover(rows,p,w,m) is None # Q<2g, independently explicit.
   count('universal_full_vectors');count('universal_full_bins',n)
 for q,m in ((8,8),(10,9),(12,12)):
  p,w=field(q*m)
  for mults in ((2,),(3,),(2,1),(1,2),(2,2)):
   if 2*sum(mults)>q:continue
   for rep in range(3):confluent_reference(q,m,p,w,params(m,p,w,len(mults)),mults)
 # Explicit full-rank union and pilot limitations, with exhaustive gauge check.
 q=m=8;p,w=field(64);eta=pow(w,q,p);par=[(0,1),(1,w)]
 witness_rows,witness_specs=make_orbits(q,m,p,w,par)
 assert solve(witness_rows,[1]+[0]*(q-1),p) is not None
 C=[dft(r,eta,p) for r in witness_rows];minimum={d:q*m for d in (1,2,3)}
 for a in range(m):
  for mu in range(1,p):
   D=[[C[t][h]*pow(mu,-t,p)*pow(eta,a*h*t,p)%p for h in range(m)] for t in range(q)]
   for d in minimum:
    modes=sum(sum((-1)**j*math.comb(d,j)*D[t-j][h] for j in range(d+1))%p!=0 for t in range(d,q) for h in range(m))
    minimum[d]=min(minimum[d],modes)
 assert min(minimum.values())>q
 COUNT['exhaustive_single_gauge_candidates']=m*(p-1)
 witness={'n':q*m,'q':q,'m':m,'p':p,'omega':w,'orbits':par,'raw':rows_to_x(witness_rows),'rank':m,'minimum_events_over_every_gauge_by_order':minimum,'comparison_budget':q}
 event={(2*len(par),0):1};grown=make_green(witness_rows,p,w,par,event)
 assert grown!=witness_rows and recover(grown,p,w,2) is not None
 assert detect_green(grown,p,w,2,1) is not None
 assert full_orbit_output(q,m,p,w,par,witness_specs)!=dft(rows_to_x(grown),w,p)
 COUNT['strict_green_extension_witnesses']=1
 q=m=4;p,w=field(16);eta=pow(w,q,p);c0=[1]*m;c1=[pow(eta,h*h,p) for h in range(m)]
 assert gauge_vote(c0,c1,eta,p) is None
 b0=idft(c0,eta,p);b1=idft(c1,eta,p);pilotfail=[[(b0[u]+t*(b1[u]-b0[u]))%p for u in range(m)] for t in range(q)]
 assert all((pilotfail[t][u]-2*pilotfail[t-1][u]+pilotfail[t-2][u])%p==0 for t in range(2,q) for u in range(m))
 witness['missing_identifiable_pilot']={'n':16,'q':4,'p':p,'omega':w,'raw':rows_to_x(pilotfail),'order':2,'events':0,'C0':c0,'C1':c1,'gauge_recovery':None}
 (ROOT/'audit/EXPLICIT_WITNESSES.json').write_text(json.dumps(witness,indent=2)+'\n')
 # Exact no-ambiguity support counts for the smallest clean family.
 q=m=2;p,w=field(4);eta=pow(w,q,p);seen=set()
 for a in range(m):
  for mu in range(1,p):
   for spec in itertools.product(range(1,p),repeat=m):
    base=idft(spec,eta,p);x=tuple(rows_to_x([[pow(mu,t,p)*base[(u-a*t)%m]%p for u in range(m)] for t in range(q)]));seen.add(x)
 assert len(seen)==m*(p-1)*(p-1)**m;COUNT['tiny_clean_family_exact_count']=len(seen);COUNT['tiny_all_input_count']=p**(q*m)
 result={'status':'PASS','counts':COUNT,'source_tests_by_file':tests,'independence':'No uploaded Python imported or executed; dense reference formulas, finite exact tests, and static AST/manifest inspection only.','not_claimed':['Source runtime regression reproduced','Benchmark against FFT/NTT','Numerical stability','Universal sub-NlogN algorithm','Formal verification','Literature novelty']}
 (ROOT/'audit/CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
