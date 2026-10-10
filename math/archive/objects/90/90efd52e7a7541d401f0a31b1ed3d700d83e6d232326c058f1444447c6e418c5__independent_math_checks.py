"""Fresh reviewer-authored mathematical witnesses, no imports/exec/AST of supplied programs.
Generic exact matrix arithmetic checks specifications through dense matrix identities,
not the supplied recursive evaluator, gate interpreter, FFT, or recurrence solver.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, math, itertools
O=Path(__file__).parent;checks=[]
def record(name,condition,detail):
 checks.append({'check':name,'passed':bool(condition),'detail':detail})
 if not condition:raise AssertionError(name)
p=97
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n):return [[0]*n for _ in range(n)]
def add(a,b):return [[(u+v)%p for u,v in zip(x,y)] for x,y in zip(a,b)]
def scale(a,c):return [[u*c%p for u in x] for x in a]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b)))%p for j in range(len(b[0]))] for i in range(len(a))]
def power(a,k):
 z=eye(len(a))
 for _ in range(k):z=mul(z,a)
 return z
def poly(a,coeff):
 z=zero(len(a));term=eye(len(a))
 for c in coeff:z=add(z,scale(term,c));term=mul(term,a)
 return z
def inverse(a):
 n=len(a);w=[row[:]+e for row,e in zip(a,eye(n))]
 for j in range(n):
  r=next(i for i in range(j,n) if w[i][j]);w[j],w[r]=w[r],w[j]
  c=pow(w[j][j],-1,p);w[j]=[u*c%p for u in w[j]]
  for i in range(n):
   if i!=j:
    c=w[i][j];w[i]=[(u-c*v)%p for u,v in zip(w[i],w[j])]
 return [r[n:] for r in w]
def rank(a):
 a=[r[:] for r in a];row=0
 for j in range(len(a[0])):
  hit=next((i for i in range(row,len(a)) if a[i][j]),None)
  if hit is None:continue
  a[row],a[hit]=a[hit],a[row];c=pow(a[row][j],-1,p);a[row]=[v*c%p for v in a[row]]
  for i in range(row+1,len(a)):
   c=a[i][j];a[i]=[(u-c*v)%p for u,v in zip(a[i],a[row])]
  row+=1
 return row
def diag(vals):return [[v if i==j else 0 for j in range(len(vals))] for i,v in enumerate(vals)]
def jmat(n,sign=1):return [[1 if j==i+1 else sign%p if i==n-1 and j==0 else 0 for j in range(n)] for i in range(n)]
def family(q,n,r,sign=1):
 J=jmat(n,sign);z=eye(n)
 for a in range(r):z=mul(z,add(eye(n),scale(J,pow(q,a,p))))
 return mul(z,diag([pow(q,-r*i,p) for i in range(n)]))
for n in (2,4,8,16):
 q=pow(5,(p-1)//n,p);assert pow(q,n,p)==1 and pow(q,n//2,p)==p-1
 U=diag([pow(q,-i,p) for i in range(n)]);W=zero(n)
 for i in range(n-1):W[i][i+1]=(q-pow(q,-i,p))%p
 W[-1][0]=-q*pow(n,-1,p)%p;C=add(U,W);B=[row[:] for row in W];B[-1][0]=0
 A=[[int(i==j+1) for j in range(n)] for i in range(n)];factorial=[1]
 for k in range(1,n):factorial.append(factorial[-1]*(1-pow(q,k,p))%p)
 t=[pow(x,-1,p) for x in factorial];T=[[t[i-j] if i>=j else 0 for j in range(n)] for i in range(n)]
 H=poly(C,t);gamma=diag([(-1)**j*pow(q,j*(j-1)//2,p)%p for j in range(n)])
 F=[[pow(q,i*j,p) for j in range(n)] for i in range(n)]
 record('qweyl_boundary_'+str(n),mul(U,W)==scale(mul(W,U),q) and power(C,n)==zero(n) and power(add(U,B),n)==eye(n) and mul(mul(T,B),inverse(T))==C,{'field':p,'N':n,'all_matrix_entries':n*n})
 record('full_fourier_factorization_'+str(n),mul(mul(mul(diag(factorial),H),T),gamma)==F,{'field':p,'N':n,'entries':n*n,'method':'Explicit powers and dense matrix contractions, no FFT'})
 R=mul(diag([pow(q,i,p) for i in range(n)]),W);D=mul(R,add(eye(n),scale(C,-1)))
 record('grading_covariance_'+str(n),mul(R,C)==scale(mul(C,R),pow(q,-1,p)) and mul(H,R)==mul(D,H) and power(R,n)==eye(n) and power(D,n)==eye(n),{'N':n,'field':p})
 S=mul(inverse(add(eye(n),scale(A,-1))),diag([pow(q,i,p) for i in range(n)]));K=scale(mul(diag([pow(q,i,p) for i in range(n)]),B),-1);K[-1][0]=pow(n,-1,p)
 record('resolvent_covariance_'+str(n),mul(H,S)==mul(K,H) and power(S,n)==eye(n) and power(K,n)==eye(n),{'N':n,'field':p})
 for lam in (1,q,2):
  resolver=poly(C,[pow(lam,-j-1,p) for j in range(n)])
  record('resolvent_inverse_'+str(n)+'_'+str(lam),resolver==inverse(add(scale(eye(n),lam),scale(C,-1))),{'N':n,'lambda':lam,'method':'Finite nilpotent polynomial compared with generic Gauss-Jordan inverse'})
 aggregate=zero(n)
 for j in range(n):
  lam=pow(q,j,p);hval=sum(v*pow(lam,k,p) for k,v in enumerate(t))%p
  aggregate=add(aggregate,scale(inverse(add(scale(eye(n),lam),scale(C,-1))),lam*hval*pow(n,-1,p)))
 record('full_resolvent_sum_'+str(n),aggregate==H,{'N':n,'poles':n,'field':p})
 for r in (1,2,4,8):
  if 2*r>n:continue
  tail=mul(power(C,n-r),poly(C,t[n-r:]));rk=rank(tail)
  record('tail_rank_'+str(n)+'_'+str(r),rk==r,{'N':n,'r':r,'rank':rk,'method':'Dense Gaussian rank of full tail, no block FFT'})
 # Direct block products verify each closed decimation level independently.
 size=n;r=1
 while size>=4:
  h=size//2;P=family(q,h,r,1);M=family(q,h,r,-1)
  record('decimation_block_closure_'+str(n)+'_'+str(r),mul(P,M)==family(q,h,2*r) and mul(M,inverse(M))==eye(h),{'N':n,'level_dimension':size,'filter_degree':r,'half':h})
  size//=2;r*=2
 # Closed graph solved by generic block Gaussian elimination, not gate execution.
 J=add(eye(n),C);Rcount=3;observed=0;u=[2*(i+1)%p for i in range(n)];Jn=power(J,Rcount-1)
 beta=sum(Jn[observed][i]*u[i] for i in range(n))%p
 if beta==1:u=[0]*n;beta=0
 big=eye(n*Rcount)
 for b in range(1,Rcount):
  for i in range(n):
   for j in range(n):big[b*n+i][(b-1)*n+j]=-J[i][j]%p
 for i in range(n):big[i][(Rcount-1)*n+observed]=(big[i][(Rcount-1)*n+observed]-u[i])%p
 forcing=[[(3*i+7)%p] for i in range(n*Rcount)];actual=mul(inverse(big),forcing)
 w=[]
 for b in range(Rcount):
  block=forcing[b*n:(b+1)*n]
  w.append(block if b==0 else add(block,mul(J,w[-1])))
 scalar=w[-1][observed][0]*pow(1-beta,-1,p)%p;response=[[x] for x in u];want=[]
 for b in range(Rcount):want.extend(add(w[b],scale(response,scalar)));response=mul(J,response)
 record('rank_one_feedback_gaussian_'+str(n),actual==want,{'N':n,'banks':Rcount,'matrix_dimension':n*Rcount,'field':p,'method':'Generic block-system inverse versus closed rank-one formula'})
# Exact small finite-exponential boundary negative control with rational numbers.
U=[[Q(1),Q(0)],[Q(0),Q(-1)]];W=[[Q(0),Q(-2)],[Q(1,2),Q(0)]]
def qm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
correction=qm(W,U);record('finite_q_exponential_product_counterexample',correction[1][0]/4==Q(1,8),{'N':2,'difference_on_e0':['0','1/8'],'method':'Exact rational cross term WU/4'})
# JA+RG coefficient identity depends only on intersection size of two triples.
coefs=[(Q(1-s,2) if s%2==0 else Q(0))+Q(s-1,2) for s in range(4)]
# RG contributes (intersection_size-1)/2 for every pair, including the diagonal.
record('reduced_network_intersection_identity',coefs==[0,0,0,1],{'intersection_sizes':[0,1,2,3],'JA_plus_RG_coefficients':list(map(str,coefs)),'scope':'Scalar coefficient identity, not a full tensor proof'})
# Independent IEEE arithmetic witnesses, no supplied implementation called.
old=1e16;new=1.;difference=new-old;answer=old+difference
record('snapshot_cancellation_witness',answer==0. and new==1.,{'old_cache':old,'new_state':new,'subtracted_delta':difference,'replayed_answer':answer})
small=1e-200;large=1e200;scaled=small/large
record('native_mixed_range_scaling_witness',scaled==0. and small/math.sqrt(2)>0.,{'small_component':small,'large_component':large,'scaled_component':scaled,'true_two_point_unitary_imaginary_component':small/math.sqrt(2),'deduced_static_effect':'For input [large+i*small,0], global scaling loses a representable imaginary output even in zero-only mode; supplied C++ not run.'})
record('native_abi_capacity_witness',8*8 < 2*8*8,{'N':8,'float64_input_output_bytes_each':64,'native_required_bytes_each':128,'basis':'S31 raw-pointer closure accepts dtype/strides unchecked; pointer memory was not dereferenced.'})
# Prime length leaves only radices1,N; demonstrate per-plan memory guard feasibility.
n=1009;qcount=3;budget=16
record('no_sample_phase_budget_counterexample',16*qcount>budget,{'N':n,'bins':[0,1,2],'max_plan_bytes':budget,'smallest_phase_payload':16*qcount,'static_effect':'S19 falls back to radix N and still constructs 48-byte phase array, above16-byte budget.'})
# Median deterministic domination used in the document follows from an order statistic.
median_cases=0
for v in itertools.product((-2,-1,0,1,2),repeat=5):
 m=sorted(v)[2];bound=sum(math.prod(v[i]**2 for i in subset) for subset in itertools.combinations(range(5),3))
 assert abs(m)**6<=bound;median_cases+=1
record('median_moment_pointwise_domination',median_cases==3125,{'rows':5,'tested_real_vectors':median_cases,'inequality':'|median(z)|^6 <= sum over 3-subsets of product z_i^2','scope':'Finite illustration plus order-statistic reasoning; independence factors expectation and gives binomial variance bound.'})
# Exact exhaustive CountSketch local identity over fourth roots, with K=2,M=2.
phases=[1,-1,1j,-1j];A=[[2+1j,-3+2j],[4-2j,1+3j]];error=[]
for shifts in itertools.product(range(2),repeat=2):
 for signs in itertools.product(phases,repeat=2):
  # Form a compressed spectrum directly from local spectral coordinates.
  Z=[sum(signs[u].conjugate()*A[u][(s+shifts[u])%2] for u in range(2)) for s in range(2)]
  error.append(signs[0]*Z[(-shifts[0])%2]-A[0][0])
variance=sum(abs(e)**2 for e in error)/len(error);predicted=sum(abs(v)**2 for v in A[1])/2
record('local_sketch_exact_state_census',sum(error)==0 and math.isclose(variance,predicted),{'states':len(error),'mean_error':str(sum(error)/len(error)),'variance':variance,'predicted_variance':predicted,'method':'Direct frequency-domain random-variable enumeration; no supplied FFT/decoder'})
(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'source_execution':'none','supplied_import_compile_AST':'none','method':'Fresh independently authored dense mathematics and primitive arithmetic witnesses','checks':checks},indent=2))
print(json.dumps({'checks':len(checks),'all_passed':all(c['passed'] for c in checks)},indent=2))
