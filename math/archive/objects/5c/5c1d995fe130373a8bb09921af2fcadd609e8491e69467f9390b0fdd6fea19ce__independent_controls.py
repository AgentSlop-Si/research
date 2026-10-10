"""Fresh independently authored controls. Reads data/text only; never imports or evaluates supplied source."""
import json,pathlib,hashlib,re,math,itertools,io,zipfile
from fractions import Fraction
P=pathlib.Path(__file__).parent
manifest=json.loads((P/'SOURCE_MANIFEST.json').read_text())
stored=json.loads((P/'STORED_OUTPUTS_INDEX.json').read_text())
checks=[]
def result(cid,title,evidence):
 checks.append({'id':cid,'title':title,'status':'PASS','evidence':evidence,'supplied_program_invoked':False})
# Pure logical countermodel: a universal check over an empty returned vector,
# followed by comparisons produced from an empty zip, supplies no dimension evidence.
returned=()
dimension=16
logical_seed=all(v==1 for v in returned)
residuals=[a-b for a,b in zip(returned,returned)]
assert logical_seed and len(residuals)==0 and len(returned)!=dimension
result('C01','Empty-vector universal predicates do not certify an N-vector',{'N':dimension,'returned_length':len(returned),'vacuous_seed_predicate':logical_seed,'residual_count':len(residuals),'valid_output_shape':False,'scope':'Logical control for source57 path; source callback not executed.'})
# Only regex line recognition, not syntax parsing, AST construction or execution.
omissions=[]
for i in (6,7,53,77):
 r=manifest[i-1];lines=(P/'sources'/r['sha256']).read_text().splitlines()
 main=next(j for j,line in enumerate(lines,1) if "__name__" in line and "__main__" in line)
 methods=[{'line':j,'name':re.search(r'def (test_\w+)',line)[1]} for j,line in enumerate(lines,1) if re.search(r'^\s+def test_\w+',line)]
 after=[m for m in methods if m['line']>main]
 assert after
 logs=[]
 for st in stored:
  if st['archive_sha256'] not in [o.get('archive_sha256') for o in r['occurrences']]:continue
  if not st['member_name'].endswith(('.txt','.log')):continue
  t=(P/st['snapshot']).read_text(errors='replace')
  found=[m['name'] for m in after if m['name'] in t]
  if found:logs.append({'member':st['member_name'],'hash':st['sha256'],'appended_methods_named':found})
 omissions.append({'source_index':i,'main_guard_line':main,'total_textually_identified_test_methods':len(methods),'methods_defined_later':after,'historical_logs_naming_later_methods':logs})
result('C02','Direct main guards precede eleven appended tests across four files',omissions)
assert sum(len(x['methods_defined_later']) for x in omissions)==11
# Mathematical order counterexample for source29's root check.
p,n,g=17,4,1
w=pow(g,(p-1)//n,p)
assert (p-1)%n==0 and pow(w,n,p)==1 and w==1
result('C03','Nth-root test is weaker than exact-order test',{'p':p,'n':n,'generator':g,'w':w,'satisfies_checked_power_equation':True,'actual_order':1,'required_order':n,'scope':'Custom generator boundary; defaults not contradicted.'})
# Float mass cancellation, without invoking NumPy or the supplied planner.
tiny=2.0**-54
assert (1.0+tiny)-1.0==0.0
exact=(Fraction(1)+Fraction(1,2**54))-Fraction(1)
assert exact>0
result('C04','Subtracting head mass can erase a nonzero floating tail',{'head':1,'tail_exact':str(exact),'double_total_minus_head':(1.0+tiny)-1.0,'scope':'Validates numerical information loss at source24; does not execute planner or invalidate ideal-arithmetic bound.'})
def get(tail):
 row=next(r for r in stored if r['member_name']==tail or r['member_name'].endswith('/'+tail))
 return json.loads((P/row['snapshot']).read_bytes()),row
# Direct Leibniz determinant, rank by exhaustive minors, suitable only tiny matrices.
def determinant(a,p):
 n=len(a);total=0
 for permutation in itertools.permutations(range(n)):
  sign=(-1)**sum(permutation[i]>permutation[j] for i in range(n) for j in range(i+1,n))
  total+=sign*math.prod(a[i][permutation[i]] for i in range(n))
 return total%p
def small_rank(a,p):
 for size in range(min(len(a),len(a[0])) ,0,-1):
  for rows in itertools.combinations(range(len(a)),size):
   for cols in itertools.combinations(range(len(a[0])),size):
    if determinant([[a[i][j] for j in cols] for i in rows],p):return size
 return 0
def summatrix(mats,p):
 return [[sum(a[i][j] for a in mats)%p for j in range(len(mats[0][0]))] for i in range(len(mats[0]))]
w,record=get('witness_n4096.json')
p=w['q'];root=w['root'];n=w['N']
assert pow(root,n,p)==1 and pow(root,n//2,p)!=1
F=[[pow(root,i*j,p) for j in w['cols']] for i in w['rows']]
assert F==w['exact_dft_block']
matrices=[w['exact_green1_block'],w['exact_green2_block']]
ranks=[small_rank(m,p) for m in matrices]
assert ranks==[w['green1_rank'],w['green2_rank']]==[1,1]
assert small_rank(summatrix(matrices,p),p)==w['sum_green_rank']==2
assert determinant(F,p)==w['dft_minor']==23964 and small_rank(F,p)==3
details=[{'member':record['member_name'],'hash':record['sha256'],'dft_determinant':23964,'green_ranks':ranks,'sum_rank':2}]
for tail in ['witness_n841_prime_square.json','witness_p29.json']:
 w,record=get(tail)
 if 'modular_sample' in w:
  sample=w['modular_sample'];p=sample['q'];root=sample['root'];order=sample['root_order'];multiplier=w['grid']['frequency_multiplier']
  rr=w['rectangle']['rows'];cc=w['rectangle']['cols'];mats=sample['green_blocks'];claimed=sample['dft_minor_det'];poly=w['exact_fourier_minor']
 else:
  sample=w['finite_field_sample'];p=sample['field_prime'];root=sample['primitive_p_root'];order=w['prime_length'];multiplier=1
  rr=w['rectangle']['rows'];cc=w['rectangle']['cols'];mats=[v['separated_block'] for v in sample['green_samples']];claimed=sample['dft_minor_det_nonzero'];poly=w['fourier_minor_cyclotomic']
 F=[[pow(root,multiplier*i*j,p) for j in cc] for i in rr]
 det=determinant(F,p);assert det==claimed and det!=0
 coeff={}
 for a in itertools.permutations(range(3)):
  exponent=sum(rr[k]*cc[a[k]]*multiplier for k in range(3))%order
  sign=(-1)**sum(a[i]>a[j] for i in range(3) for j in range(i+1,3))
  coeff[exponent]=coeff.get(exponent,0)+sign
 coeff={str(k):v for k,v in coeff.items() if v}
 assert coeff==poly['nonzero_coefficients']
 prime=w.get('grid',{}).get('prime_factor',order)
 if order==prime:
  nonzero=len({coeff.get(str(k),0) for k in range(order)})>1
 else:
  nonzero=any(len({coeff.get(str(r+k*prime),0) for k in range(prime)})>1 for r in range(prime))
 assert nonzero
 ranks=[small_rank(m,p) for m in mats];sr=small_rank(summatrix(mats,p),p)
 assert max(ranks)<=1 and sr<=2
 details.append({'member':record['member_name'],'hash':record['sha256'],'dft_determinant':det,'green_ranks':ranks,'sum_rank':sr,'cyclotomic_coefficients_recomputed':True,'nonzero_characteristic_zero_remainder':True})
result('C05','Three stored Fourier/Green block witnesses independently reconciled',{'witnesses':details,'scope':'Verifies stored small blocks/determinants and selected polynomial coefficients; not reconstruction of omitted full parent Green operators.'})
x=Fraction(11,28);taylor=sum(x**k/math.factorial(k) for k in range(9));upper=taylor+x**9/math.factorial(9)/(1-x/10)
assert upper<Fraction(741,500)
gram=Fraction(741**2,259**2);assert gram<Fraction(41,5)
result('C06','Uniform-frame rational scalar constant checked independently',{'exp_upper':str(upper),'gram_condition_bound':str(gram),'below_8_2':True,'scope':'Scalar constant only, not all-size matrix perturbation proof.'})
def archive_at(year):
 data=io.BytesIO()
 with zipfile.ZipFile(data,'w') as z:
  entry=zipfile.ZipInfo('same.txt',(year,1,1,0,0,0));z.writestr(entry,b'identical payload')
 return data.getvalue()
a,b=archive_at(2000),archive_at(2001)
assert a!=b
with zipfile.ZipFile(io.BytesIO(a)) as za,zipfile.ZipFile(io.BytesIO(b)) as zb:assert za.read('same.txt')==zb.read('same.txt')
result('C07','ZIP metadata affects reproducibility independently of payload',{'payloads_identical':True,'archive_sha256_a':hashlib.sha256(a).hexdigest(),'archive_sha256_b':hashlib.sha256(b).hexdigest(),'scope':'Synthetic metadata control for source75, no original packaging executed.'})

# Count totals derived directly from finite index sets, not from source execution.
totals=[]
def count_check(suffix, fields):
 doc,row=get(suffix)
 for key,expected in fields.items():
  assert doc[key]==expected,(suffix,key,doc[key],expected)
 totals.append({'member':row['member_name'],'hash':row['sha256'],'expected_counts':fields})
count_check('fft_global_reuse/audit_results.json',{'cases':18,'basis_columns':3*sum(2**k for k in range(1,7)),'matrix_entries':3*sum(4**k for k in range(1,7))})
sizes=[2,4,8,16,32,64]
rcounts=[len({1,min(2,n),min(4,n),n//2,n}) for n in sizes]
count_check('fft_qweyl_fusion_research/results.json',{'cases':4*sum(rcounts),'basis_vectors':4*sum(n*r for n,r in zip(sizes,rcounts))})
count_check('fft_sparse_surrogate_bridge/graph/results.json',{'cases':2*4*3*5,'full_state_basis_vectors':2*sum([2,4,8,16])*sum([3,4,6])*5,'random_full_states':2*4*3*5*3})
count_check('FIELD_JOINT_RESULTS.json',{'exact_basis_entries':sum(n*n for n in [48,80,96,192,384]),'exact_frame_joint_entries':sum(n*n for n in [48,80,96,192,384])})
count_check('FIELD_SLOPE_RESULTS.json',{'exact_matrix_entries':sum(n*n for n in [48,80,96,192,384,384])})
count_check('fft_exact_recovery_research/results.json',{'integer_product_cases':5*5*6+1+4})
cert,record=get('polynomial_audit.json')
assert sorted(c['N'] for c in cert['certificates'])==[8,16]
totals.append({'member':record['member_name'],'actual_certificate_sizes':[8,16],'scope':'Expected records are present in actual archived input, despite verifier permitting an empty list.'})
result('C08','Archived totals and required polynomial-record presence reconcile',totals)

(P/'INDEPENDENT_CONTROLS.json').write_text(json.dumps({'controls':checks,'count':len(checks),'supplied_execution':False},indent=2)+'\n')
print(json.dumps({'passed_controls':len(checks),'stored_witnesses_reconciled':len(details),'direct_run_omitted_methods':11}))
