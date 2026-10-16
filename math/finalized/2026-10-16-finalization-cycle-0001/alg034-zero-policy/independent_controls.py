"""Independent exact controls. No candidate or historical program is imported."""
from fractions import Fraction
from math import comb
from pathlib import Path
from itertools import product
import hashlib
import json
import random

ROOT=Path(__file__).parent
counts={}
def check(ok,label):
    if not ok: raise AssertionError(label)
    counts[label]=counts.get(label,0)+1

def mono(n,e,v=1):
    d=n//2; e%=n; out=[0]*d
    out[e%d]=v if e<d else -v
    return out
def plus(a,b): return [x+y for x,y in zip(a,b)]
def mul(a,b):
    d=len(a); out=[0]*d
    for i,x in enumerate(a):
      if x:
       for j,y in enumerate(b):
        k=i+j; out[k%d]+=x*y*(1 if k<d else -1)
    return out
def auto(a,r):
    n=2*len(a); out=[0]*len(a)
    for i,x in enumerate(a): out=plus(out,mono(n,i*r,x))
    return out
def norm(a):
    n=2*len(a); v=mono(n,0)
    for r in range(1,n,2): v=mul(v,auto(a,r))
    return v
def lengths(n,b):
    q,r=divmod(n,b); return [q+(j<r) for j in range(b)]
def blocks(n,b,a,beta,rows):
    out=[]; start=0
    for ell in lengths(n,b):
      h=[0]*(n//2)
      for t in range(ell):
        r=a*t*(t-1)//2+(a*start+beta)*t
        x,y=rows[start+t]
        h=plus(h,plus(mono(n,r,x),mono(n,r+n//4,y)))
      out.append(h);start+=ell
    return out
def independent_blocks(n,b,a,beta,rows):
    """Separate 2N phase-exponent route, expanded before reduction."""
    out=[]; start=0
    for ell in lengths(n,b):
      full=[0]*n
      for t,(x,y) in enumerate(rows[start:start+ell]):
        E=(a*t*(t-1)+2*(a*start+beta)*t)%(2*n)
        assert E%2==0
        full[E//2]+=x;full[(E//2+n//4)%n]+=y
      out.append([full[j]-full[j+n//2] for j in range(n//2)])
      start+=ell
    return out
def projection(n,b,a,beta,rows):
    hs=blocks(n,b,a,beta,rows);out=[];s=0
    for ell,h in zip(lengths(n,b),hs):
      for t in range(ell):
        q=a*t*(t-1)//2+(a*s+beta)*t
        out.append(mul(h,mono(n,-q)))
      s+=ell
    return hs,out
def fft_unnormalized(vals):
    n=len(vals);out=[]
    for k in range(n):
      v=[0]*(n//2)
      for j,x in enumerate(vals): v=plus(v,mul(x,mono(n,-j*k)))
      out.append(v)
    return out
def energy(vals):
    z=[0]*len(vals[0])
    for x in vals:z=plus(z,mul(x,auto(x,-1)))
    return z
def ceil_log2(x): return (x-1).bit_length()
def plan(n,b,rows,t=0):
    w=max((abs(x).bit_length() for row in rows for x in row),default=0)
    hs=blocks(n,b,1,0,rows)
    masses=[sum(map(abs,h)) for h in hs if any(h)]
    if not masses:return None
    A=min(masses);K=ceil_log2(A);G=w+(n//2-1)*K
    H=min(comb(n+b-1,b),1<<(n-b));C=64*H*b*(1<<b)*n*n
    c=ceil_log2(C);Pq=16*(n.bit_length()-1)+16
    p=max(w,c+t+1,c+Pq+G+2)
    I=b+2*ceil_log2(n)+10
    return dict(A=A,K=K,G=G,W=w,H=H,C=C,c=c,Pq=Pq,p=p,I=I)

# Exhaustive small complex input encodings; independent quotient routes.
for flat in product((-1,0,1),repeat=8):
  rows=list(zip(flat[::2],flat[1::2]))
  for b,a,beta in ((3,1,0),(3,3,1),(4,1,3)):
    hs=blocks(4,b,a,beta,rows)
    check(hs==independent_blocks(4,b,a,beta,rows),'independent_phase_reduction')
    if b==4:check((not any(map(any,hs)))==(not any(flat)),'singleton_zero_equivalence')

rng=random.Random(340016)
for n,trials in ((4,40),(8,60),(16,50),(32,30)):
  for _ in range(trials):
    b=rng.randrange(3,n+1);a=rng.randrange(1,n,2);beta=rng.randrange(n)
    rows=[(rng.randrange(-7,8),rng.randrange(-7,8)) for j in range(n)]
    hs=blocks(n,b,a,beta,rows)
    check(hs==independent_blocks(n,b,a,beta,rows),'independent_phase_reduction')
    for h in hs:
      v=norm(h)
      check(not any(v[1:]),'norm_is_integer')
      check((v[0]!=0)==any(h),'norm_nonzero_iff_reduced_nonzero')
      A=sum(map(abs,h))
      check(all(sum(map(abs,auto(h,r)))==A for r in range(1,n,2)),'conjugate_l1_bound')

# Exact target energy, Fourier reflection and zero equivalence, independent of producer.
for n in (4,8,16):
 for b in sorted(set((3,n//2,n))):
  if b<3:continue
  for a,beta in ((1,0),(n-1,n//4)):
    rows=[(rng.randrange(-3,4),rng.randrange(-3,4)) for j in range(n)]
    hs,px=projection(n,b,a,beta,rows)
    e=[0]*(n//2)
    for ell,h in zip(lengths(n,b),hs):e=plus(e,[ell*v for v in mul(h,auto(h,-1))])
    check(energy(px)==e,'exact_projection_energy')
    f=fft_unnormalized(px);ff=fft_unnormalized(f)
    check(ff==[[n*z for z in px[-j%n]] for j in range(n)],'second_transform_is_reflection')
    check((not any(map(any,px)))==(not any(map(any,hs))),'projected_zero_equivalence')

# Exact kernel and near-kernel family from the source: N64 B3 a1 beta0.
n=64;b=3
for K in (0,1,2,5,16,64,1024,65536):
  rows=[(0,0)]*n;rows[0]=(1<<K,0);rows[1]=(-(1<<K)+1,0)
  hs=blocks(n,b,1,0,rows)
  check(hs[0]==mono(n,0) and not any(map(any,hs[1:])),'near_kernel_exact_reduction')
  p=plan(n,b,rows)
  check(p['A']==1 and p['K']==0 and p['G']==K+1,'near_kernel_precision_growth')
  check(p['p']-(K+1)==p['c']+p['Pq']+2,'near_kernel_linear_width')
rows=[(0,0)]*n;rows[0]=(1,0);rows[1]=(-1,0)
check(not any(map(any,blocks(n,b,1,0,rows))),'nonzero_input_exact_kernel')
# Imaginary embedding matters: S_1=i at beta=N/4; 1+i*i=0.
rows=[(0,0)]*8;rows[0]=(1,0);rows[1]=(0,1)
check(not any(map(any,blocks(8,3,1,2,rows))),'imaginary_phase_kernel')
check(any(map(any,blocks(8,3,1,0,rows))),'wrong_phase_detected')

# Sufficient precision is verified by exact integer comparisons, no producer surrogate.
cap_examples=[]
for n in (4,8,16,64,256,4096):
 for b in sorted(set((3,n//2,n))):
  if b<3:continue
  for width in (1,8,53):
    rows=[(0,0)]*n;rows[0]=((1<<width)-1,0)
    for t in (0,7,211):
      z=plan(n,b,rows,t)
      check(2*z['C']<=(1<<(z['p']-t)),'producer_accuracy_premise')
      check(z['C']<=(1<<(z['p']-z['Pq']-z['G']-2)),'delta_le_rho_mu_over_four')
      check(n<(1<<(2*z['Pq'])),'sqrtN_rho_strictly_below_one')
      # Symbolic F cancellation: Delta/mu = C*2^(W-p+(D-1)K).
      for F in (-10**30,-3,0,17,10**30):
        delta_exp=z['W']-F-z['p'];mu_exp=-F-(n//2-1)*z['K']
        check(delta_exp-mu_exp==z['G']-z['p'],'scale_exponent_cancellation')
      if z['p']+z['I']>65536:cap_examples.append(dict(n=n,b=b,width=width,t=t,p=z['p'],I=z['I']))
check(bool(cap_examples),'wrapper_sufficient_cap_can_fail')
rows=[(1,0)]+[(0,0)]*3
z=plan(4,3,rows)
check(z['p']+z['I']<=65536 and 65536+z['I']>65536,'actual_precision_cap_must_be_checked')

# A small-signal integer polynomial with A>1 catches the omitted-degree mutation.
for n in (8,16,64):
 rows=[(0,0)]*n;rows[0]=(3,0)
 z=plan(n,3,rows)
 bad_p=z['c']+z['Pq']+z['W']+2
 check(z['C']>(1<<(bad_p-z['Pq']-z['G']-2)) if bad_p-z['Pq']-z['G']-2>=0 else True,'omitted_degree_bound_detected')

result={'status':'PASS','assertions':sum(counts.values()),'counts':counts,
 'cap_examples':cap_examples[:8],
 'scope':'Exact independent algebra and policy arithmetic only; no supplied program, producer, wrapper, or Q16 executor run.',
 'controls_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
