"""Additional audit-authored controls. No uploaded module imports."""
from pathlib import Path
import importlib.util,json,sys,random,math
sys.dont_write_bytecode=True
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('audit_helpers',here/'independent_checks.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
rng=random.Random(83180)
cas=0;root_evaluations=0
for n,p in [(8,17),(12,97),(16,97),(18,109),(32,193)]:
 w0=a.root(n,p)
 for s,w in [(1,3),(2,4),(3,4),(3,5),(4,6)]:
  for rep in range(5):
   while True:
    Y=[[rng.randrange(p) for _ in range(w)] for _ in range(s)]
    if a.rk(Y,p)==s:break
   lo=s*(s-1)//2;coeff=[0]*(s*(w-s)+1)
   from itertools import combinations
   for K in combinations(range(w),s):
    v=a.det([[row[k] for k in K] for row in Y],p)*a.det([[pow(w0,k*h,p) for h in range(s)] for k in K],p)
    coeff[sum(K)-lo]=(coeff[sum(K)-lo]+v)%p
   assert any(coeff)
   bad=0
   for j in range(n):
    z=pow(w0,j,p)
    M=[[sum(Y[t][i]*pow(z*pow(w0,h,p)%p,i,p) for i in range(w))%p for h in range(s)] for t in range(s)]
    d=a.det(M,p); assert d==pow(z,lo,p)*a.peval(coeff,z,p)%p
    bad+=d==0;root_evaluations+=1
   assert bad<=s*(w-s)
   cas+=1
cov=0
for n in [4,8,16,32]:
 p=998244353
 for rep in range(4):
  M=[[rng.randrange(1,p) for _ in range(n)] for _ in range(n)]
  rows=list(range(n));cols=list(range(n));rng.shuffle(rows);rng.shuffle(cols)
  left=[rng.randrange(1,p) for _ in range(n)];right=[rng.randrange(1,p) for _ in range(n)]
  N=[[left[i]*M[rows[i]][cols[j]]*right[j]%p for j in range(n)] for i in range(n)]
  assert a.moments(M)==a.moments(N);cov+=1
# Verify the recurrence from separately solved sparse systems, at multiple sizes.
rec=0
for n in [4,8,16,32,64]:
 for seed in range(3):
  terms=a.params(n,100+seed);x=[rng.randrange(a.P) for _ in range(n)]
  for t in terms:
   alpha=pow(t['denominator'],-1,a.P);w=pow(3,-((a.P-1)//n),a.P)
   z=[x[i]*pow(w,t['right_exponents'][i],a.P)%a.P for i in range(n)]
   h=0
   for j in t['order']:h=(alpha*h+z[j])%a.P
   h=h*pow(1-pow(alpha,n,a.P),-1,a.P)%a.P
   y=[0]*n
   for j in t['order']:h=(alpha*h+z[j])%a.P;y[j]=h*pow(w,t['left_exponents'][j],a.P)%a.P
   assert y==a.mv(a.component(n,t),x,a.P);rec+=1
# The source interface support branch uses raw x==0 rather than x%P==0.
p=a.P;target=[[p,1],[1,1]];middle=[[0,1],[1,1]]
assert [[x%p for x in r] for r in target]==middle
counter={'prime':p,'target':target,'middle':middle,'same_matrix_mod_p':True,'source_raw_zero_counts':[sum(x==0 for r in target for x in r),sum(x==0 for r in middle for x in r)],'source_branch_result':'excluded','qualified_fix':'Normalize modulo p before support counting, or require canonical residues.'}
result={'casoratian_spaces':cas,'casoratian_root_evaluations':root_evaluations,'two_sided_moment_covariance_controls':cov,'cyclic_recurrence_controls':rec,'noncanonical_residue_interface_counterexample':counter,'prime_998244353_trial_division_check':all(p%d for d in range(2,math.isqrt(p)+1)),'all_passed':True}
assert result['prime_998244353_trial_division_check']
output=Path(sys.argv[1]) if len(sys.argv)>1 else here/'EXTRA_RESULTS.json'
output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
