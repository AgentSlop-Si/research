"""Independent exact tests. python verify.py writes RESULTS.json.

No tests constitute a worst-case faster-FFT proof. Test-data preparation,
dense DFT/reference work, and matrix ranks are not fast-path operations.
"""
from __future__ import annotations
import json, random, time, hashlib
from pathlib import Path
from fiber_fft import (Field, Roots, sparse_fft, direct_dft, dense_fft_reference,
 berlekamp_massey, recover_fiber, certified_fiber_fft, make_fiber_signal,
 precondition, generate_preconditioned_input, undo_precondition_output,
 sparse_diagonal_shift_solve, certified_aggregate_fft)

FIELDS=[(65537,3),(998244353,3)]
RNG=random.Random(20261010)

def wr(p,g,n):return pow(g,(p-1)//n,p)
def arithmetic(c):return c['add']+c['mul']+c['inv']
def qshape(n):q=1<<((n.bit_length()-1)//2);return q,n//q

def rank(a,p):
 a=[r.copy() for r in a];i=0
 for j in range(len(a[0])):
  pivot=next((k for k in range(i,len(a)) if a[k][j]%p),None)
  if pivot is None:continue
  a[i],a[pivot]=a[pivot],a[i];v=pow(a[i][j],-1,p)
  a[i]=[v*x%p for x in a[i]]
  for k in range(i+1,len(a)):
   c=a[k][j]
   if c:a[k]=[(v-c*w)%p for v,w in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i

def clean(z):
 z=z.copy();z.pop('output',None);return z

def check_sparse_fft():
 cases=entries_checked=0
 for p,g in FIELDS:
  for n in [1,2,4,8,16,32,64,128]:
   w=wr(p,g,n)
   for size in sorted({0,1,min(3,n),n//2,n}):
    support=RNG.sample(range(n),size);x=[0]*n
    for j in support:x[j]=RNG.randrange(1,p)
    for sign in [1,-1]:
     f=Field(p);roots=Roots(n,w,f)
     y=sparse_fft([(j,x[j]) for j in support],n,sign,roots)
     z=direct_dft(x,pow(w,sign,p),p)
     assert y==z,(p,n,size,sign)
     cases+=1;entries_checked+=n
 return dict(cases=cases,entries_checked=entries_checked)

def check_fiber_recovery():
 accepted=rejected=prefix_spoofs=0
 for p,g in FIELDS:
  for m in [4,8,16,32,64,128]:
   w=wr(p,g,m)
   for b in sorted({1,max(1,m//4),m//2}):
    for r in sorted({0,1,b}):
     if r>b:continue
     support=RNG.sample(range(m),r);amps=[RNG.randrange(1,p) for _ in support]
     y=[sum(a*pow(w,(-h*u)%m,p) for h,a in zip(support,amps))%p for u in range(m)]
     modes=recover_fiber(y,b,Roots(m,w,Field(p)),1)
     assert modes is not None and dict(modes)==dict(zip(support,amps))
     accepted+=1
     if 2*b<m:
      yy=y.copy();yy[-1]=(yy[-1]+1)%p
      modes=recover_fiber(yy,b,Roots(m,w,Field(p)),1)
      assert modes is None,(p,m,b,r,'forged prefix accepted')
      prefix_spoofs+=1
    # r=b+1 with generic nonzero coefficients must reject (grid has unique expansion).
    supp=RNG.sample(range(m),b+1)
    y=[sum((h+2)*pow(w,(-h*u)%m,p) for h in supp)%p for u in range(m)]
    assert recover_fiber(y,b,Roots(m,w,Field(p)),1) is None
    rejected+=1
 return dict(accepted=accepted,rejected=rejected,forged_prefixes_rejected=prefix_spoofs)

def check_full_transforms():
 cases=entries_checked=atoms=0;examples=[]
 for p,g in FIELDS:
  for n in [4,8,16,32,64,128,256,512,1024,2048,4096]:
   w=wr(p,g,n);q,m=qshape(n);b=min(max(1,n.bit_length()-1),m//2)
   for case in range(3):
    modes=[]
    for t in range(q):
     rr=RNG.randrange(b+1) if case<2 else b
     supp=RNG.sample(range(m),rr)
     modes.append([(h,RNG.randrange(1,p)) for h in supp])
    x=make_fiber_signal(n,p,w,modes)
    for green in [False,True]:
     xx=generate_preconditioned_input(x,Roots(n,w,Field(p))) if green else x
     z=certified_fiber_fft(xx,p,w,b,green=green)
     assert z['accepted'],(p,n,case,green,z)
     ref=direct_dft(xx,w,p) if n<=64 else dense_fft_reference(xx,w,p)
     assert z['output']==ref,(p,n,case,green)
     assert z['K']==sum(map(len,modes))
     cases+=1;entries_checked+=n
     if case==2 and green and n>=256:examples.append(clean(z))
  # Entire atomic basis of the fiber-coordinate representation at small sizes.
  for n in [4,8,16,32,64]:
   w=wr(p,g,n);q,m=qshape(n)
   for t in range(q):
    for h in range(m):
     modes=[[] for _ in range(q)];modes[t]=[(h,1)]
     x=make_fiber_signal(n,p,w,modes)
     z=certified_fiber_fft(x,p,w,1)
     assert z['accepted'] and z['output']==direct_dft(x,w,p)
     atoms+=1;entries_checked+=n
 return dict(random_cases=cases,atomic_inputs=atoms,entries_checked=entries_checked,examples=examples)

def check_dense_full_rank_family():
 out=[]
 for p,g in FIELDS:
  for m in [4,8,16,32,64]:
   n=m*m;w=wr(p,g,n);b=min(n.bit_length()-1,m//2)
   # Complex diagonal dominance does NOT imply finite-field noncancellation.
   # Choose a finite test coefficient explicitly; generation is not fast-path work.
   for attempt in range(256):
    diagonal=2*b+attempt
    modes=[[(t,diagonal)]+[((t+j)%m,1) for j in range(1,b)] for t in range(m)]
    x=make_fiber_signal(n,p,w,modes);ref=dense_fft_reference(x,w,p)
    if all(x) and all(ref):break
   else:raise AssertionError('No dense modular control found')
   result=certified_fiber_fft(x,p,w,b)
   assert result['accepted'] and result['output']==ref
   matrix=[[x[t+m*u] for u in range(m)] for t in range(m)]
   rr=rank(matrix,p)
   assert rr==m and all(x) and all(ref),(p,n,rr,sum(v!=0 for v in x),sum(v!=0 for v in ref))
   out.append(dict(p=p,N=n,M=m,b=b,K=m*b,input_nonzeros=n,output_nonzeros=n,fiber_matrix_rank=rr,diagonal=diagonal,test_generation_attempts=attempt+1))
 return out

def check_fallback_and_corruption():
 generic=fallback=late=0
 for p,g in FIELDS:
  for n in [16,64,256,1024]:
   w=wr(p,g,n);q,m=qshape(n);b=1
   for _ in range(4):
    x=[RNG.randrange(p) for _ in range(n)]
    z=certified_fiber_fft(x,p,w,b,fallback=True)
    assert not z['accepted'] and z['fallback']
    assert z['output']==dense_fft_reference(x,w,p)
    generic+=1
   modes=[[(t%m,t+1)] for t in range(q)]
   x=make_fiber_signal(n,p,w,modes)
   # Corrupt only the final raw coordinate; all first 2b samples remain intact.
   x[-1]=(x[-1]+1)%p
   z=certified_fiber_fft(x,p,w,b,fallback=True)
   assert not z['accepted'] and z['failure_fiber']==q-1
   assert z['output']==dense_fft_reference(x,w,p);late+=1
  for n in [4,8,16,32]:
   w=wr(p,g,n)
   for j in range(n):
    x=[0]*n;x[j]=1
    z=certified_fiber_fft(x,p,w,1,fallback=True)
    assert not z['accepted'] and z['output']==direct_dft(x,w,p)
    fallback+=1
 return dict(generic_dense_cases=generic,late_corruptions=late,ordinary_basis_fallbacks=fallback)

def check_green_identity():
 cases=0;denominator_rejections=0
 for p,g in FIELDS:
  for n in [4,8,16,32,64,128,256]:
   w=wr(p,g,n);f=Field(p);r=Roots(n,w,f)
   for _ in range(3):
    x=[RNG.randrange(p) for _ in range(n)]
    px=precondition(x,r);fx=dense_fft_reference(x,w,p)
    fp=dense_fft_reference(px,w,p)
    lfx=[((7+pow(w,k,p))*fx[k]+2*fx[(k-1)%n])%p for k in range(n)]
    assert fp==lfx
    assert generate_preconditioned_input(px,r)==x
    assert undo_precondition_output(lfx,r)==fx
    cases+=1
  for diag,b in [([0,1],1),([1,1],-1)]:
   try:sparse_diagonal_shift_solve(diag,b,[1,2],Field(p))
   except ZeroDivisionError:denominator_rejections+=1
   else:raise AssertionError('Invalid denominator not rejected')
 return dict(cases=cases,denominator_rejections=denominator_rejections)

def check_profiles():
 """Integer support accounting; ratios are measured, not asymptotic proof."""
 out=[];p=998244353;g=3
 for n in [256,1024,4096,16384,65536,262144]:
  w=wr(p,g,n);q,m=qshape(n);b=min(n.bit_length()-1,m//2)
  modes=[]
  for t in range(q):modes.append([(t,2*b)]+[((t+j)%m,1) for j in range(1,b)])
  # Fast independent data generation by dense inverse fiber transforms.
  eta=pow(w,q,p);x=[0]*n
  for t in range(q):
   coeff=[0]*m
   for h,a in modes[t]:coeff[h]=a
   y=dense_fft_reference(coeff,pow(eta,-1,p),p)
   for u,a in enumerate(y):x[t+q*u]=a
  result=certified_fiber_fft(x,p,w,b)
  assert result['accepted'] and result['output']==dense_fft_reference(x,w,p)
  bf=Field(p);br=Roots(n,w,bf)
  base=sparse_fft(list(enumerate(x)),n,1,br)
  assert base==result['output']
  out.append(dict(N=n,b=b,K=result['K'],new_arithmetic=arithmetic(result['count']),
   baseline_arithmetic=bf.c.arithmetic,ratio=arithmetic(result['count'])/bf.c.arithmetic,
   new_word_proxy=result['count']['word'],baseline_word_proxy=bf.c.word,
   old_theorem_MK=q*m*b,old_theorem_K_squared=(q*b)**2))
 return out


def check_aggregate():
 accepted=rejected=full_heavy=0;records=[]
 for p,g in FIELDS:
  for n in [16,64,256,1024,4096]:
   w=wr(p,g,n);q,m=qshape(n)
   for setting in ['one_heavy','all_light','zero']:
    modes=[]
    for t in range(q):
     rr=m if setting=='one_heavy' and t==q-1 else (0 if setting=='zero' else min(2,m//2))
     supp=RNG.sample(range(m),rr)
     modes.append([(h,RNG.randrange(1,p)) for h in supp])
    x=make_fiber_signal(n,p,w,modes);K=sum(map(len,modes))
    for green in [False,True]:
     xx=generate_preconditioned_input(x,Roots(n,w,Field(p))) if green else x
     z=certified_aggregate_fft(xx,p,w,K,green=green)
     assert z['accepted'] and z['output']==dense_fft_reference(xx,w,p)
     assert z['K']==K and len(z['heavy_fibers'])<=K//(z['threshold']+1)
     accepted+=1
     if setting=='one_heavy':
      assert q-1 in z['heavy_fibers'];full_heavy+=1;records.append(clean(z))
     if K>0:
      zz=certified_aggregate_fft(xx,p,w,K-1,green=green,fallback=True)
      assert not zz['accepted'] and zz['output']==dense_fft_reference(xx,w,p)
      assert len(zz['heavy_fibers'])<=(K-1)//(zz['threshold']+1)+1
      rejected+=1
   xx=[RNG.randrange(p) for _ in range(n)]
   z=certified_aggregate_fft(xx,p,w,q,fallback=True)
   assert not z['accepted'] and z['output']==dense_fft_reference(xx,w,p)
   rejected+=1
 return dict(accepted=accepted,rejected_with_correct_fallback=rejected,             completely_dense_fiber_controls=full_heavy,examples=records)

def main():
 results={'status':'Exact certified structured-input FFT; NOT an unrestricted sub-NlogN algorithm',
          'model':'Unit-cost exact prime-field arithmetic; supplied primitive root; word proxy separately counted',
          'seed':20261010,'groups':{}}
 tests=[('pruned_transform',check_sparse_fft),('mode_recognition',check_fiber_recovery),
        ('end_to_end',check_full_transforms),('dense_full_rank',check_dense_full_rank_family),
        ('fallback',check_fallback_and_corruption),('green',check_green_identity),
        ('operation_profiles',check_profiles),('aggregate_budget',check_aggregate)]
 for name,fn in tests:
  results['groups'][name]=fn();print(name,'PASS',flush=True)
 results['passed_groups']=len(tests)
 path=Path(__file__).with_name('RESULTS.json')
 path.write_text(json.dumps(results,indent=2)+'\n')
 print('SHA256',hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':main()
