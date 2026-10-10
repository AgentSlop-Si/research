"""New reviewer checks, authored for this exact audit. Inputs are inert JSON/archive bytes.
No supplied program is executed, imported, compiled, AST-parsed, or copied into this checker.
Stored gate words are only counted and schema-checked; historical PASS labels remain historical.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from decimal import Decimal,localcontext
import hashlib,json,re,gzip,zipfile,io,math
O=Path(__file__).parent
E=json.load(open(O/'EVIDENCE_INDEX.json'));P=json.load(open(O/'PROVENANCE.json'))
def item(name):return next(e for e in E if e['member']==name or any(o['member']==name for o in e['occurrences']))
def raw(name):return (O/item(name)['local']).read_bytes()
def data(name):return json.loads(raw(name))
checks=[]
def record(name,value,scope):checks.append({'check':name,'result':value,'scope':scope})
# Inert per-archive manifests, resolved only within the same archive.
G={a['sha256']:a for a in json.load(open(O/'RELATED_ARCHIVE_METADATA.json'))};ac={}
def archive(h):
 if h not in ac:
  parts=G[h]['first_observed_at'].split('!');b=(Path('fft_research_master_20261009')/parts[0]).read_bytes()
  for part in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(b))as z:b=z.read(part)
  assert hashlib.sha256(b).hexdigest()==h;ac[h]=b
 return ac[h]
manifests=[]
for e in E:
 base=Path(e['member']).name.lower()
 if base not in ('sha256sums.json','sha256sums.txt','bundle_sha256.json','bundle_manifest.json','source_manifest.json'):continue
 b=(O/e['local']).read_bytes();kind='sha256';recs=[]
 try:
  if base.endswith('.txt'):
   entries=[(m.group(2),m.group(1),None) for line in b.decode().splitlines() if (m:=re.fullmatch(r'([a-f0-9]{64})\s+\*?(.+)',line))]
  else:
   d=json.loads(b)
   if base=='source_manifest.json' and isinstance(d,dict) and 'files' in d and isinstance(d['files'],list) and d['files'] and 'git_blob_sha' in d['files'][0]:
    kind='git_blob_sha1';entries=[('upstream/'+v['path'],v['git_blob_sha'],v.get('size'))for v in d['files']]
   elif isinstance(d,dict) and isinstance(d.get('files'),dict) and all(isinstance(v,str) and re.fullmatch('[a-f0-9]{64}',v)for v in d['files'].values()):entries=[(k,v,None)for k,v in d['files'].items()]
   elif isinstance(d,dict) and all(isinstance(v,str) and re.fullmatch('[a-f0-9]{64}',v)for v in d.values()):entries=[(k,v,None)for k,v in d.items()]
   elif isinstance(d,dict) and all(isinstance(v,dict)and 'sha256'in v for v in d.values()):entries=[(k,v['sha256'],v.get('bytes'))for k,v in d.items()]
   else:
    manifests.append({'manifest':e['member'],'archive_sha256':e['archive_sha256'],'status':'schema_not_in_requested_hash_manifest_formats'});continue
  with zipfile.ZipFile(io.BytesIO(archive(e['archive_sha256'])))as z:
   names=set(z.namelist());parent=str(Path(e['member']).parent)
   for name,want,size in entries:
    candidates=[name] if parent=='.' else [parent+'/'+name,name]
    match=next((n for n in candidates if n in names),None)
    if match is None:recs.append({'path':name,'status':'not_in_same_archive'});continue
    bb=z.read(match);got=hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()if kind=='git_blob_sha1'else hashlib.sha256(bb).hexdigest()
    recs.append({'path':name,'matched_member':match,'status':'match'if got==want and(size is None or size==len(bb))else'mismatch','observed_digest':got,'expected_digest':want,'bytes':len(bb)})
  manifests.append({'manifest':e['member'],'archive_sha256':e['archive_sha256'],'kind':kind,'entries':recs,'counts':dict(Counter(r['status']for r in recs))})
 except Exception as exc:manifests.append({'manifest':e['member'],'status':'read_error','error':str(exc)})
(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps(manifests,indent=2)+'\n')
record('Stored manifest actual-byte verification',{'manifests':len(manifests),'counts':dict(sum((Counter(m.get('counts',{}))for m in manifests),Counter()))},'Hashes establish byte consistency, not truth, authorship, timing, or fresh historical execution.')
# Loop cardinality and reported primitive-word budgets, without running source tests.
v4=data('v4/independent_results.json');src=data('v4/source_v4_results.json');rows=src['packed_correctness']
v4audit={'rows':len(rows),'violations':sum(r['decoder_error_normalized']>r['decoder_bound_normalized']+1e-12 for r in rows),'one_word_key_violations':sum(r['params']['descriptor_bits']*r['params']['g_used']>r['params']['word_bits']for r in rows),'table_exponent_budget_violations':sum(r['params']['descriptor_bits']*r['params']['g_used']>r['params']['gamma']*math.log2(r['N'])for r in rows),'all_lookup_miss_rows':sum(r['table_entries']==r['lookup_count']for r in rows),'total_cache_misses':sum(r['table_entries']for r in rows),'total_lookups':sum(r['lookup_count']for r in rows)}
assert all(v4['saved_data_audit'][k]==v for k,v in v4audit.items())
record('v4 stored budget audit',v4audit,'Recomputed from stored data, not new decoder/sampling trials; 15/20 keys exceed the stated one-word budget and 20/20 exceed the table exponent budget.')
counts={'guard_cases':5*7*7*4,'guard_lanes':5*7*4*sum([1,2,7,16,65,129,257]),'phase_rounding_cases':7*sum([1,2,3,5,8,17,31,64,127]),'decoder_cases':9*6*4}
assert all(v4['independent_'+k]==v for k,v in counts.items())
record('v4 loop cardinalities',counts,'Cardinality match only; historical numerical trials not repeated.')
x=data('verification/inverse_scan_checks.json')['counts'];expected={'random_words':7*6*20,'inverse_identity_vectors':sum([1,2,3,4,5,8,16])*6*20,'fft_basis_vectors':sum([1,2,4,8,16,32]),'fft_random_vectors':9*12,'dense_fourier_inverse_matrices':8};assert x==expected
record('Inverse-scan stored loop cardinalities',expected,'Does not fresh-execute random words or FFT implementation.')
g=data('verification/packed/guarded_add_results.json');assert g['block_cases']==9*4*5*4 and g['lane_sums_checked']==9*4*4*sum([1,7,32,64,129]);assert len(g['records'])==180
assert all(r['guarded_lane_bits']==(2*r['groups']*r['lane_bound']).bit_length() and r['lanes_per_64bit_word']==64//r['guarded_lane_bits'] for r in g['records'])
record('Guarded packing budget/cardinality',{'cases':g['block_cases'],'lane_sums':g['lane_sums_checked'],'records':len(g['records'])},'Checks lane-capacity inequalities and saved record counts; no wall-clock speedup inference.')
for name in ['verification/packed/transpose_results.json','verification/transpose/verify_packed_transpose.json']:
 d=data(name);rs=d.get('records',d.get('cases'));fits=sum(r.get('required_word_bits',r.get('square_bits'))<=64 for r in rs)
 record('Transpose RAM admissibility '+name,{'records':len(rs),'fit_64_bit_word':fits,'exceed_64_bit_word':len(rs)-fits,'maximum_tile_bits':max(r.get('required_word_bits',r.get('square_bits'))for r in rs)},'Packed semantic identities can use arbitrary Python integers; only bounded tiles fit a 64-bit word.')
# Exact F8 matrix identity from stored coefficients, using a narrow polynomial grammar.
zero=(F(0),)*4
one=(F(1),F(0),F(0),F(0))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def times(a,b):
 out=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[(i+j)%4]+=(-1 if i+j>=4 else 1)*x*y
 return tuple(out)
def monomial(exp):
 out=[F(0)]*4;out[exp%4]=F((-1)**(exp//4));return tuple(out)
def decode(s):
 s=s.replace(' ','');parts=re.findall(r'[+-]?[^+-]+',s);assert ''.join(parts)==s;out=[F(0)]*4
 for part in parts:
  if 'zeta'not in part:out[0]+=F(part);continue
  m=re.fullmatch(r'([+-]?)(?:(\d+)\*)?zeta(?:\*\*([123]))?(?:/(\d+))?',part);assert m,(s,part)
  sign,coeff,exp,den=m.groups();out[int(exp or 1)]+=F((-1 if sign=='-'else 1)*int(coeff or 1),int(den or 1))
 return tuple(out)
c=data('verification/f8/channel_certificate.json');A,B,C,D=[[list(map(decode,channel))for channel in c[key]]for key in ['forward_a','forward_b','backward_a','backward_b']];diag=list(map(decode,c['diagonal']));checked=0
for i in range(8):
 for j in range(8):
  y=diag[i]if i==j else zero
  for k in range(3):
   if i>=j:
    t=B[k][j]
    for u in range(j+1,i+1):t=times(t,A[k][u])
    y=plus(y,t)
   if i<=j:
    t=D[k][j]
    for u in range(i,j):t=times(t,C[k][u])
    y=plus(y,t)
  assert y==monomial(c['row_order'][i]*c['col_order'][j]);checked+=1
record('F8 exported coefficient matrix',{'entries_exactly_verified':checked,'ring':'Q[z]/(z^4+1)','certificate_sha256':item('verification/f8/channel_certificate.json')['sha256'],'parser':'whitelisted sums of rational monomials; no eval/sympify/AST'},'Fresh exact finite certificate check, independent of the supplied generator and verifier. Does not certify an all-size family or runtime improvement.')
# Independent modular rank elimination used only on freshly constructed constant matrices.
def rank(a,p):
 basis={}
 for inputrow in a:
  v=[x%p for x in inputrow]
  for j in sorted(basis):
   c=v[j]
   if c:v=[(x-c*y)%p for x,y in zip(v,basis[j])]
  nz=next((j for j,x in enumerate(v)if x),None)
  if nz is not None:
   c=pow(v[nz],-1,p);basis[nz]=[c*x%p for x in v]
 return len(basis)
inventories=[]
for p,g0 in [(998244353,3),(2013265921,31)]:
 w=pow(g0,(p-1)//8,p);assert pow(w,4,p)==p-1
 matrix=[[pow(w,i*j,p)for j in range(8)]for i in range(8)]
 hist35=Counter(rank([[matrix[i][j]for j in cols]for i in rows],p)for rows in combinations(range(8),3)for cols in combinations(range(8),5))
 hist44=Counter(rank([[matrix[i][j]for j in cols]for i in rows],p)for rows in combinations(range(8),4)for cols in combinations(range(8),4))
 assert hist35=={3:3136}and hist44=={4:4304,3:576,2:20}
 inventories.append({'prime':p,'3x5':dict(hist35),'4x4':dict(hist44)})
record('F8 exhaustive fresh minor-rank inventories',inventories,'Exact finite-field arithmetic, 16,072 newly checked matrices; modular nonzero minors support lower bounds, not an unrestricted runtime barrier.')
# Fresh exact combinatorial count reconciliation of prime-support tests.
ann=data('prime_annihilator_checks.json')
for r in ann['counts']:
 p=r['prime'];assert r['support_sets']==2**p-2;assert r['nonzero_coefficients']==sum(math.comb(p,k)*(k+1)for k in range(1,p))
record('Prime annihilator inventory counts',{'total_support_sets':sum(r['support_sets']for r in ann['counts']),'total_coefficients':sum(r['nonzero_coefficients']for r in ann['counts'])},'Counts reconciled without running all supplied polynomial tests. Prime-only vanishing criterion does not imply a runtime lower bound.')
# Fresh integer constants and high-precision numerical gap; no all-length inference.
with localcontext()as cx:
 cx.prec=80;h=24;v=math.comb(h,3);degree=math.comb(h-3,3)+3*(h-3);W=2*v**3+3*v*v*(v*degree+h);Dlt=2*v*v*(v-3*h*h);den=1<<(W-1).bit_length();m=h**3
 gap=-(1-Decimal(Dlt)/(Decimal(m)*den)).ln()/Decimal(m).ln()
 const=data('constants.json')['reduced_center_padded_h24'];assert (v,W,Dlt,den,m)==tuple(const[k]for k in ['v','W','Delta','Wstar','m']);assert abs(gap-Decimal(const['tensor_gap_high_precision']))<Decimal('1e-70')
 record('Reduced-center h24 constants',{'v':v,'W':W,'Delta':Dlt,'Wstar':den,'tensor_gap_80digit_numeric':str(gap),'claimed_5e_minus10_is_numerically_below':gap>Decimal('5e-10')},'Integer constants exact; Decimal logarithm is high-precision numerical reconciliation, not an interval proof or every-length reduction.')
# Saved words: byte hashes and metadata, never interpretation/execution of their gates.
axes=[]
for h in [23,25]:
 pair=[]
 for mode in ['baseline','carrier']:
  prefix=f'results/{mode}-{h}/';compressed=raw(prefix+'word.json.gz');decompressed=gzip.decompress(compressed);word=json.loads(decompressed);receipt=data(prefix+'receipt.json');prep=data(prefix+'transitions.bin.json');prof=data(prefix+'transitions.bin.profiles.json')
  wordhash=hashlib.sha256(decompressed).hexdigest();assert wordhash==receipt['word_sha256']==prep['word_sha256'];assert receipt['profile']==prof and receipt['prepared']==prep
  assert (word['h'],word['v'],word['R'])==(h,math.comb(h,3),prof['R']);assert len(word['frames'])+2==prep['frames'];assert len(word['ops'])==receipt['compiled']['elementary_xors'];assert 2*word['v']+word['R']==receipt['replay']['full_basis_vectors']
  mass=sum(i*c for i,c in enumerate(prof['blocks']));assert mass==prof['rank_sum']==h*prof['R']+h*(h-1)==prep['rank_mass']
  pair.append((wordhash,prof));axes.append({'h':h,'mode':mode,'compressed_sha256':hashlib.sha256(compressed).hexdigest(),'word_sha256':wordhash,'frames':len(word['frames']),'ops':len(word['ops']),'rank_mass':mass,'receipt_fields_match':True,'gates_executed':False})
 if h==23:assert pair[0][0]==pair[1][0]and pair[0][1]==pair[1][1]
 else:assert {i:b-a for i,(a,b)in enumerate(zip(pair[0][1]['blocks'],pair[1][1]['blocks']))if a!=b}=={1:2,3:2,4:1,5:-1,7:-1}
record('Binary-frame saved-word/receipt reconciliation',axes,'Exact compressed/decompressed hashes and arithmetic only; hundreds of thousands of stored XOR instructions were not replayed.')
res=data('result.json');cm={int(k):v for k,v in res['child_multiplicities'].items()};assert sum(k*v for k,v in cm.items())==res['counts']['rank_mass'];assert res['counts']['m']*res['counts']['W']-res['counts']['rank_mass']==res['counts']['deficit']
assert F(res['candidate_moment_excess_at_baseline_lower'])>0 and F(res['candidate_valid_moment_gap_lower'])>0 and F(res['valid_witness_kappa_difference'])<0
record('Candidate rejection stored rational signs',{'counts':res['counts'],'positive_moment_excess':True,'candidate_kappa_difference':res['valid_witness_kappa_difference']},'Internal arithmetic/sign consistency only; the supplied moment/assembly programs were not executed.')
summary=data('results/summary.json');wordcoverage=[]
for case in summary['cases']:
 name=f"results/t{case['t']}_r{case['r']}_s{case['start_stage']}_certificate.json";cert=data(name);n=case['real_scalar_inputs'];dim=case['dirty_lift']['full_state_dimension'];target=cert['normalized_target_matrix']
 expected=[[(j,'1')]for j in range(dim)]
 for j,row in enumerate(target):
  rr={dimidx:F(val)for dimidx,val in expected[n+j]}
  for idx,val in row:rr[idx]=F(val)
  expected[n+j]=sorted((idx,str(val))for idx,val in rr.items())
 digest=hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest();assert digest==case['dirty_lift']['full_state_matrix_sha256'];assert json.loads(json.dumps(expected))==cert['full_state_matrix']
 lengths={key:len(cert[key])for key in ['baseline_word','candidate_word']if key in cert};kinds={key:dict(Counter(op[0]for op in cert[key]))for key in lengths}
 wordcoverage.append({'case':name,'state_dimension':dim,'word_lengths':lengths,'operation_types':kinds,'target_and_stored_full_state_hash_match':True,'reported_straight_line_add_sub':case['candidate_add_sub'],'gate_words_replayed':False})
record('Two-round certificate availability and target-hash reconciliation',{'cases':wordcoverage,'baseline_words_present':sum('baseline_word'in r['word_lengths']for r in wordcoverage),'candidate_words_present':sum('candidate_word'in r['word_lengths']for r in wordcoverage)},'All ten stored target matrices match their digest; only one candidate word is supplied. Word availability/hash checks do not establish correctness of absent candidate words or recount the separate straight-line circuit cost.')
bench=data('fft130_adaptive_merge/benchmark_view_optimizer_results.json');br=[]
for scenario,vv in bench.items():
 observed=vv['sequential']['ms']/vv['adaptive']['ms'];assert abs(observed-vv['adaptive']['speedup_vs_sequential'])<1e-12
 br.append({'scenario':scenario,'stored_speedup_vs_sequential':observed,'stored_checksum_difference':vv['adaptive']['checksum_abs_diff']})
record('Optimizer benchmark ratio arithmetic',br,'Historical floating-point checksums/timings only. The shift workload slows down; exact numerical correctness and broad speedup are not certified by a checksum.')
# Radix4 count formulas from saved measurements, without running any transform.
r4=data('verification/radix4_results.json');assert r4['basis_columns_checked']==2*sum([2,4,8,16,32,64,128,256]);assert r4['random_vectors_checked']==2*8*3
for r in r4['records']:
 n=r['N'];L=n.bit_length()-1
 assert r['stage_count']==(L+1)//2 and r['permutation_words']==n*(1+2*r['stage_count'])
 if L%2==0:
  s=L//2;assert r['scan_multiplications']==9*n*s//2;assert r['scan_additions']==7*n*s//2;assert r['twiddle_data_multiplications']==3*n*s//4-n+1;assert r['twiddle_preparation_multiplications']==n-1-3*s
record('Radix4 stored work/count reconciliation',{'records':len(r4['records']),'basis_columns':r4['basis_columns_checked'],'random_vectors':r4['random_vectors_checked']},'Confirms formula bookkeeping and historical trial counts, not all-N correctness or speed.')
# Fixed positive control independently multiplied with unbounded Python integers.
ctrl=data('control_results.json');p=ctrl['prime'];assert p==257;w=pow(3,(p-1)//16,p);ii=pow(w,4,p)
leaf=[[1,1,1,1],[-1,-1,1,1],[ii,-ii,1,-1],[-ii,ii,1,-1]]
H=[[leaf[i%4][j%4]%p if i//4==j//4 else 0 for j in range(16)]for i in range(16)]
per=ctrl['middle_input_to_output_permutation'];tw=[pow(w,j*r,p)for j in range(4)for r in [1,3,0,2]]
# Product H diag(tw) P H, with P[perm[j],j]=1.
actual=[[sum(H[i][per[k]]*tw[per[k]]*H[k][j]for k in range(16))%p for j in range(16)]for i in range(16)]
expected=[[pow(w,i*j,p)for j in ctrl['column_order']]for i in ctrl['row_order']]
assert actual==expected
record('F16 stored positive-control factorization',{'prime':p,'exact_matrix_entries_checked':256,'safe_int64_upper_bound':4*256**3},'Fresh unbounded-integer matrix multiplication of fixed data, not execution of the supplied NumPy screen. This validates one control, not all screens/candidates.')
value=642620;b=value.to_bytes(8,'little');big=int.from_bytes(b,'big');assert big!=value
record('Binary profile reader endian boundary',{'example_rank_sum':value,'little_endian_bytes_hex':b.hex(),'raw_big_endian_interpretation':big},'New byte-order example for S02 L35–39. The header helper normalizes its own reads, but raw scalar/frame/transition reads require separate normalization on big-endian hosts.')
(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'method':'new reviewer arithmetic and inert metadata checks only','checks':checks,'check_groups':len(checks),'source_execution':'none','source_import_compile_AST':'none'},indent=2)+'\n')
print('Fresh groups',len(checks));print('Manifest totals',checks[0]['result']);print('F8 exact',checked)
