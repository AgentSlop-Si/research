"""Independent review code. Imports no uploaded programs; source JSON is data only."""
from pathlib import Path
import json, random, itertools, hashlib, math
import sympy as sp
BASE=Path(__file__).resolve().parent
SRC=BASE/'extracted/fft_green_research_phase29_2026-10-10(1)/fft_green_phase29_two_parameter'
CERT=SRC/'certificates'

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(a,b,p): return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]
def inv(a,p):
 n=len(a); w=[[x%p for x in row]+ident(n)[i] for i,row in enumerate(a)]
 for k in range(n):
  t=next(i for i in range(k,n) if w[i][k]);w[k],w[t]=w[t],w[k]
  v=pow(w[k][k],-1,p);w[k]=[x*v%p for x in w[k]]
  for i in range(n):
   if i!=k:
    v=w[i][k];w[i]=[(x-v*y)%p for x,y in zip(w[i],w[k])]
 b=[r[n:] for r in w];assert mul(a,b,p)==ident(n) and mul(b,a,p)==ident(n);return b

def det(a,p):
 a=[r[:] for r in a];out=1;n=len(a)
 for k in range(n):
  piv=next((i for i in range(k,n) if a[i][k]),None)
  if piv is None:return 0
  if piv!=k:a[k],a[piv]=a[piv],a[k];out=-out
  c=a[k][k];out=out*c%p;ic=pow(c,-1,p)
  for i in range(k+1,n):
   c=a[i][k]*ic%p
   for j in range(k+1,n):a[i][j]=(a[i][j]-c*a[k][j])%p
 return out%p

def rank(a,p):
 a=[r[:] for r in a];h=0
 for k in range(len(a[0])):
  piv=next((i for i in range(h,len(a)) if a[i][k]),None)
  if piv is None:continue
  a[h],a[piv]=a[piv],a[h];v=pow(a[h][k],-1,p)
  for i in range(h+1,len(a)):
   c=a[i][k]*v%p
   for j in range(k+1,len(a[0])):a[i][j]=(a[i][j]-c*a[h][j])%p
   a[i][k]=0
  h+=1
  if h==len(a):break
 return h

def components(n,seed,p,root,denoms):
 rng=random.Random(seed);out=[];spec=[]
 for d in denoms:
  order=list(range(n));rng.shuffle(order);a=ident(n)
  for k in range(n):a[order[(k+1)%n]][order[k]]=(-pow(d,-1,p))%p
  g=inv(a,p);le=[rng.randrange(n) for _ in range(n)];ri=[rng.randrange(n) for _ in range(n)]
  out.append([[pow(root,le[i]+ri[j],p)*g[i][j]%p for j in range(n)] for i in range(n)])
  spec.append({'order':order,'left_exponents':le,'right_exponents':ri,'coupling_denominator':d})
 return out,spec

def family(n,p=998244353,generator=3):
 assert sp.isprime(p);w=pow(generator,-((p-1)//n),p);assert pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in sp.factorint(n))
 seed=2800+n;aa,sa=components(n,3*seed+1,p,w,[4,5]);bb,sb=components(n,3*seed+2,p,w,[4,5]);cc,sc=components(n,3*seed+3,p,w,[4,5]);gg,sg=components(n,3*seed+4,p,w,[7]);coeff=3*pow(2,-1,p)%p
 a=[[ (aa[0][i][j]+coeff*aa[1][i][j])%p for j in range(n)]for i in range(n)];c=[[ (cc[0][i][j]+coeff*cc[1][i][j])%p for j in range(n)]for i in range(n)]
 F=[[pow(w,i*j,p) for j in range(n)]for i in range(n)];T=mul(mul(inv(a,p),F,p),inv(c,p),p)
 assert all(v for row in T for v in row)
 return T,bb+[gg[0]],{'n':n,'p':p,'root':w,'A':sa,'B':sb+sg,'C':sc}

def moment(a,s,p):
 n=len(a);iv=[[pow(x,-1,p) for x in row] for row in a];out=n**3
 for i in range(n):
  for j in range(i):
   a1=sum(pow(a[i][k]*iv[j][k]%p,s,p) for k in range(n))%p
   a2=sum(pow(a[j][k]*iv[i][k]%p,s,p) for k in range(n))%p
   out=(out+2*a1*a2)%p
 return out

def peval(a,t,p):
 r=0
 for x in a[::-1]:r=(r*t+x)%p
 return r

def pmul(a,b,p):
 out=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]=(out[i+j]+x*y)%p
 return out

MON2=[(a,b,2-a-b) for a in range(3) for b in range(3-a)]
MON4=[(a,b,4-a-b) for a in range(5) for b in range(5-a)]
POS={e:i for i,e in enumerate(MON4)}
def rows(T,G,r,c,p,anchor=3):
 def vec(i,j):return [G[1][i][j],G[2][i][j],G[0][i][j]]
 def prod(v,w):
  ans={e:0 for e in MON2}
  for i in range(3):
   for j in range(3):
    e=[0,0,0];e[i]+=1;e[j]+=1;e=tuple(e);ans[e]=(ans[e]+v[i]*w[j])%p
  return ans
 out=[]
 for i in range(1,anchor):
  for j in range(1,anchor):
   x=prod(vec(r[i],c[0]),vec(r[0],c[j]));y=prod(vec(r[i],c[j]),vec(r[0],c[0]));a=T[i][j]*T[0][0]%p;b=T[i][0]*T[0][j]%p
   q={e:(a*x[e]-b*y[e])%p for e in MON2}
   for m in MON2:
    row=[0]*15
    for e,v in q.items():row[POS[tuple(x+y for x,y in zip(m,e))]]=v
    out.append(row)
 return out

def main():
 results={'source_code_executed':False};specs=[];cases={}
 for n in (4,8,16):
  T,G,spec=family(n);specs.append(spec);p=spec['p'];c=json.loads((CERT/f'bezout_two_param_N{n}.json').read_text());a,b=c['slice_P1'],c['slice_P2'];u,v=c['bezout_U'],c['bezout_V'];x=pmul(a,u,p);y=pmul(b,v,p);z=[((x[k] if k<len(x) else 0)+(y[k] if k<len(y) else 0))%p for k in range(max(len(x),len(y)))];assert z[0]==1 and not any(z[1:])
  tq=[moment(T,s,p) for s in (1,2)];d=math.prod(v for row in G[2] for v in row)%p
  leads=[pow(d,s,p)*(moment(G[2],s,p)-tq[s-1])%p for s in (1,2)];assert leads==[a[-1],b[-1]] and all(leads)
  checked=[0,0];mu=0
  while checked[1]<2*n*n+1:
   B=[[(G[0][i][j]+c['fixed_lambda_slice']*G[1][i][j]+mu*G[2][i][j])%p for j in range(n)]for i in range(n)]
   if all(x for row in B for x in row):
    dd=math.prod(x for row in B for x in row)%p
    for s,poly in ((1,a),(2,b)):
     if checked[s-1]<s*n*n+1:
      assert peval(poly,mu,p)==pow(dd,s,p)*(moment(B,s,p)-tq[s-1])%p;checked[s-1]+=1
   mu+=1
  cases[n]={'bezout_identity':True,'identified_evaluations':checked,'leading_mu_coefficients':leads}
  (BASE/f'family_N{n}.txt').write_text(str(n)+' '+str(p)+'\n'+'\n'.join(' '.join(map(str,row)) for M in [T]+G for row in M)+'\n')
  if n==8:
   cert=json.loads((CERT/'anchored_exhaustive_N8_p998244353.json').read_text())
   for w in cert['sample_nonzero_minors']:
    m=rows(T,G,w['source_rows'],w['source_cols'],p);assert det([m[k] for k in w['selected_rows']],p)==w['determinant_modp']!=0
   cases[n]['saved_minor_witnesses']=len(cert['sample_nonzero_minors'])
 results['two_parameter_certificates']=cases
 for p,generator in ((998244353,3),(2013265921,31)):
  T,G,spec=family(4,p,generator);specs.append(spec);cert=json.loads((CERT/f'degree4_all_permutations_N4_p{p}.json').read_text());seen=set()
  for key,w in cert['pivot_witnesses'].items():
   r,c=key.split('/');r=tuple(map(int,r));c=tuple(map(int,c));assert sorted(r)==list(range(4)) and sorted(c)==list(range(4));seen.add((r,c));m=rows(T,G,r,c,p,4);assert det([m[k] for k in w['selected_rows']],p)==w['determinant_modp']!=0
  assert len(seen)==576
  planted=[[(G[0][i][j]+2*G[1][i][j]+3*G[2][i][j])%p for j in range(4)] for i in range(4)];rk=rank(rows(planted,G,range(4),range(4),p,4),p);assert rk<15
  results[f'all_N4_minors_p{p}']={'count':576,'positive_control_rank':rk}
 # Exact characteristic-zero paired-constructor control.
 z=sp.symbols('z');i=sp.I;r=sp.sqrt(2);q=(1+i)/r;t=(1-i)/r;gp=1+t*z-z*z+t*z**3;Q=1+r*z+i*z*z;P=2-2*i+2*r*z
 assert sp.simplify(sp.rem(sp.expand(gp*Q-P),z**4-1,z))==0
 assert sp.simplify(sp.resultant(Q,z**4-1,z))==8*i
 assert sp.simplify(sp.resultant(Q,P,z))==8+8*i
 Z=sp.zeros(4)
 for k in range(4):Z[(k+1)%4,k]=1
 C=sp.eye(4)+t*Z-Z**2+t*Z**3;D=sp.diag(*[sp.simplify(q**(k*k)) for k in range(4)]);F=sp.Matrix([[i**(j*k) for k in range(4)]for j in range(4)])
 assert all(sp.simplify(x)==0 for x in D*C*D-F)
 H=sp.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])
 for A in (F,H): assert A*A.applyfunc(lambda x:1/x).T==4*sp.eye(4)
 results['paired_F4']={'chirp_identity_exact':True,'rational_congruence_exact':True,'denominator_resultant':'8i','coprime_numerator_resultant':'8+8i','scope':'scalar-weighted two resolvents; exact unit-diagonal two-sum normalization not yet established'}
 results['invariant_insufficiency']={'F4_and_real_H4_both_R_equals_4I':True,'inequivalent':'All H4 cross-ratios are ±1; F4 has cross-ratio i.'}
 # v16 exhaustive cycle statistic and independent matrix checks.
 minima={}
 for n in range(2,10):
  minimum=n;winners=[]
  for perm in itertools.permutations(range(n)):
   unseen=set(range(n));zero=0
   while unseen:
    k=min(unseen);cy=[]
    while k in unseen:unseen.remove(k);cy.append(k);k=perm[k]
    zero+=sum(cy)%n==0
   rk=n-zero
   if rk<minimum:minimum=rk;winners=[perm]
   elif rk==minimum:winners.append(perm)
  assert minimum==n//2 and winners==[tuple((-j)%n for j in range(n))]
  minima[n]={'minimum':minimum,'minimizers':len(winners),'permutations':math.factorial(n)}
 results['v16_exhaustive_permutations']=minima
 checks=0
 for n,p,root in ((5,101,2),(8,97,5),(16,97,5),(25,101,2),(32,193,5),(49,197,2),(64,257,3)):
  w=pow(root,(p-1)//n,p)
  assert pow(w,n,p)==1 and all(pow(w,n//a,p)!=1 for a in sp.factorint(n))
  rng=random.Random(771+n);F=[[pow(w,j*k,p)for k in range(n)]for j in range(n)]
  for trial in range(6):
   perm=list(range(n));rng.shuffle(perm);DP=[[((pow(w,-i,p) if i==j else 0)-(1 if i==perm[j] else 0))%p for j in range(n)]for i in range(n)]
   DF=[[(F[(i-1)%n][j]-F[i][perm[j]])%p for j in range(n)]for i in range(n)]
   unseen=set(range(n));zero=0
   while unseen:
    k=min(unseen);cy=[]
    while k in unseen:unseen.remove(k);cy.append(k);k=perm[k]
    zero+=sum(cy)%n==0
   assert rank(DP,p)==rank(DF,p)==n-zero;checks+=1
 results['v16_independent_matrix_rank_checks']=checks
 (BASE/'FAMILY_SPECIFICATIONS.json').write_text(json.dumps(specs,indent=2))
 (BASE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2))
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()
