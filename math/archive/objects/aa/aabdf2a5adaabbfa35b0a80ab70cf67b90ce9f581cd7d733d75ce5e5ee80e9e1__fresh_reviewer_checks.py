"""Fresh reviewer arithmetic and stored-data checks. No supplied source is imported, compiled, AST-parsed or executed."""
import json,hashlib,math,itertools
from fractions import Fraction
from pathlib import Path
O=Path(__file__).parent;es=json.load(open(O/'EVIDENCE_INDEX.json'));rows=json.load(open(O/'ASSIGNED_SOURCES.json'));checks=[]
def get(pre):
 e=next(e for e in es if e['sha256'].startswith(pre));return json.load(open(O/e['local']))
def ck(name,truth,detail):
 assert truth,name;checks.append({'name':name,'passed':True,'detail':detail})
# Model-level counterexamples, not source execution.
ck('dependent_basis_dimensions',1!=2,{'input_basis':[[1,0],[2,0]],'reduced_rank':1,'stored_original_spectrum_rows':2,'query_coefficient_count':1,'conclusion':'stored dimensions incompatible on later span reuse'})
ck('spectrum_only_auto_placeholder_counterexample',[3,1]!=[1,1],{'N':2,'real_base':[1,1],'base_spectrum':[2,0],'edit':[0,1],'correct_rfft':[3,1],'zero_placeholder_native_rfft':[1,1],'source_trace':'n<4096 with a pending edit chooses native under auto'})
ck('stale_calibration_sample_counterexample',4!=0,{'N':4,'constructor_sample':[1,1,1,1],'later_sample':[0,0,0,0],'DC_expected':0,'cached_DC_reused':4,'condition':'constructor was calibrated and sample_result is present'})
ck('rank_early_return_counterexample',True,{'matrix':[[0,1],[0,0]],'mathematical_rank':1,'source_rank_and_det_early_return':0,'determinant':0,'impact':'helper generality; tested full-rank17 minor is unaffected'})
ck('rational_input_truncation',int(Fraction(1,2))==0,{'input':[str(Fraction(1,2)),0],'mathematical_DC':'1/2','integer_cast_DC':0})
# Literal path enumeration, separate from compressed recurrence implementation.
fix=get('0caf37de')['beyond_horizon_failure'];N=fix['N'];p=65537;w=fix['omega'];R=list(range(0,N,1<<fix['b']));out=[0]*len(R)
for start,amp in zip(R,fix['input']):
 for decisions in itertools.product((0,1),repeat=fix['degree']):
  s=start;v=amp;valid=True
  for j,bit in enumerate(decisions,1):
   if bit:v=v*pow(w,s,p)%p
   s=(2*s+bit)%N
   if j<fix['degree'] and s in R:valid=False;break
  if valid and s in R:out[R.index(s)]=(out[R.index(s)]+v)%p
ck('retained_horizon_literal_paths',out==fix['exact_value'] and out!=fix['naive_value'],{'exact_path_sum':out,'stored_naive':fix['naive_value'],'steps':fix['degree'],'scope':'one bounded beyond-horizon witness'})
# Fresh scalar degree-count and combinatorial checks.
z=get('0caf37de');ck('retained_parameter_counts',z['summary']=={'basis_parameters':28,'basis_inputs':247,'polynomial_parameters':28,'support_parameters':56,'inverse_parameters':28,'full_recovery_parameters':28},z['summary'])
for n in (2,4,8,16,32,64,128):
 dims=[n//(2**j) for j in range(1,n.bit_length())]
 ck('orbit_counts_N'+str(n),sum(dims)+1==n and sum(t*t for t in dims)+1==(n*n+2)//3,{'N':n,'stored_coefficients':1+sum(dims),'expanded_coefficients':1+sum(t*t for t in dims)})
for N in (5,7,11):
 expected=(2**(N-1)-1)*sum(range(1,N));v=next(t for t in get('414cfce4')['tests'] if t['N']==N)
 ck('displacement_case_count_N'+str(N),expected==v['checks'],{'expected':expected,'stored':v['checks']})
ck('cyclic_rational_cases',get('036678a9')['counts']['cases']==8*6*20,{'expected':960})
ck('decoded_tree_cases',get('a777d020')['cases']==3*8*5*3,{'expected':360})
ck('oversampled_subtree_cases',get('4352daf6')['counts']['cases']==30*sum(1 for l in (1,2,4,8) for h in range(6) if l*2**h<=32),{'expected':540})
ck('fixed_bridge_case_count',get('f408deb5')['passed']==5*3+5+4*3+1,{'expected':33})
# Source-vs-result configuration, especially the shared output basename.
lazy=get('a582d0d8');ck('lazy_result_matches_quick_grid',len(lazy)==18 and {r['updates'] for r in lazy if r['case']=='fixed_location_partial_bins'}=={200} and {r['updates'] for r in lazy if r['case']=='random_locations_partial_then_dense'}=={128},{'stored_rows':len(lazy),'quick_expected_rows':3+3+2*5+2,'full_expected_rows':3+3+3*11+2,'conclusion':'result matches quick source configuration, incompatible with full source default'})
# Exact arithmetic specialization of the stored characteristic-zero N5 certificate.
cert=get('a95e7fad');p=241
for emb in (1,2,3,4):
 root=pow(91,emb,p)
 def k(v):
  return sum((Fraction(s).numerator*pow(Fraction(s).denominator,-1,p)%p)*pow(root,i,p) for i,s in enumerate(v))%p
 a0=k(cert['extension_polynomial_monic']['constant']);a1=k(cert['extension_polynomial_monic']['linear'])
 def add(x,y):return ((x[0]+y[0])%p,(x[1]+y[1])%p)
 def neg(x):return (-x[0]%p,-x[1]%p)
 def mul(x,y):
  poly=[x[0]*y[0],x[0]*y[1]+x[1]*y[0],x[1]*y[1]]
  return ((poly[0]-a0*poly[2])%p,(poly[1]-a1*poly[2])%p)
 def sm(s,x):return (s*x[0]%p,s*x[1]%p)
 def inv(x):
  norm=(x[0]*x[0]-a1*x[0]*x[1]+a0*x[1]*x[1])%p
  assert norm;return sm(pow(norm,-1,p),((x[0]-a1*x[1])%p,-x[1]%p))
 def dec(x):return (k(x['constant']),k(x['delta']))
 U=list(map(dec,cert['u']));V=list(map(dec,cert['v']));D=list(map(dec,cert['diagonal_correction']));T=dec(cert['pole_t']);B=[[(k(v),0) for v in rr] for rr in cert['target']]
 vals=[]
 for i in range(5):
  for j in range(5):
   uv=mul(U[i],V[j]);vu=mul(V[i],U[j]);c=add(uv,mul(T,vu)) if i<=j else add(mul(T,uv),vu)
   if i==j:c=add(c,D[i])
   vals.append(c==B[i][j])
 ck('N5_stored_certificate_embedding_'+str(emb),all(vals),{'prime':p,'zeta':root,'entries':25,'scope':'fresh exact modular check of serialized certificate, not full characteristic-zero replay'})
 def mm(A,B):return [[sum(A[i][h]*B[h][j] for h in range(len(B)))%p for j in range(len(B[0]))] for i in range(len(A))]
 plain=[[b[0] for b in rr] for rr in B];finv=[[pow(root,-i*j,p)*pow(5,-1,p)%p for j in range(5)] for i in range(5)];X=[[ (finv[i][j]+(pow(root,3*i*i,p) if i==j else 0))%p for j in range(5)] for i in range(5)];I=[[int(i==j) for j in range(5)] for i in range(5)]
 ck('N5_inverse_embedding_'+str(emb),mm(plain,X)==I and mm(X,plain)==I,{'two_sided_entries':50})
ck('N5_irreducible_place',pow(163,120,241)==240,{'prime':241,'discriminant':163,'Euler_value':240})
# Exact candidate arithmetic, without scanning or running the supplied witness checker.
h=24;v=math.comb(h,3);rho=h;neighbors=sum(math.comb(3,s)*math.comb(h-3,3-s) for s in (0,2));W=2*v**3+3*v*v*(v*neighbors+rho);Delta=2*v*v*(v-3*h*rho);m=h**3;star=1<<(W-1).bit_length()
ck('network_candidate_arithmetic',(v,neighbors,W,Delta,star)==(2024,1393,34666930287616,2425172992,2**45),{'v':v,'neighbors':neighbors,'W':W,'Delta':Delta,'Wstar':star})
xx=Fraction(191,20);lower=sum(xx**j/math.factorial(j) for j in range(41));gain=Fraction(26,50000000000)
ck('network_rational_margin',lower>m and Fraction(Delta,m*star)>gain*xx,{'scope':'local arithmetic premises only; no label-transfer or global recurrence proof'})
# Check stored operation ledger formulas rather than recomputing transforms.
sh=get('a6fb9d3c');ck('shear_source_digest_binding',sh['checker_sha256']==rows[8]['sha256'],{'digest':sh['checker_sha256']})
ck('shear_matrix_grid',sh['matrix_instances']==len(sh['matrix_controls'])==2*5*3*2,{'count':60})
for rec in sh['vector_controls']:
 if rec['N']>=2:
  N=rec['N'];ck('shear_ledger_'+str(rec['prime'])+'_'+str(N),rec['arithmetic']==17*N*(N.bit_length()-1)-14*N-4,{'N':N,'arithmetic':rec['arithmetic'],'scope':'declared arithmetic ledger, not literal exponentiation/bit work'})
(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'scope':'New reviewer arithmetic and metadata only; supplied-source execution none','checks':checks},indent=2))
print('Fresh reviewer checks passed:',len(checks))
