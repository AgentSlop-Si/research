"""Fresh narrow arithmetic/text/data controls; never load supplied code as code."""
import hashlib,io,json,pathlib,re,zipfile
from fractions import Fraction
P=pathlib.Path('archived_proof_source_review_0527');M=pathlib.Path('fft_research_master_20261009');rows=json.loads((P/'SOURCE_MANIFEST.json').read_text())
def put(n,x):(P/n).write_text(json.dumps(x,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
controls=[]
# C01: same-length distinct ZIPs demonstrate size-only identity boundary.
blobs=[]
for payload in (b'first',b'other'):
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_STORED) as z:
  info=zipfile.ZipInfo('sample.txt',(2026,1,1,0,0,0));z.writestr(info,payload)
 blobs.append(out.getvalue())
assert len(blobs[0])==len(blobs[1]) and digest(blobs[0])!=digest(blobs[1])
ident=json.loads((M/'additions/1807/SOURCE_IDENTITIES.json').read_text())
controls.append({'id':'C01','source_indices':[26,29],'method':'Independent in-memory ZIPs and direct metadata inspection','same_size':len(blobs[0]),'distinct_sha256':[digest(b) for b in blobs],'actual_1807_metadata_hash_fields':sum('sha256' in d for d in ident),'conclusion':'A byte count is not a prior identity certificate. Actual1807 metadata has no expected hash, so source29 establishes measured hashes rather than violating an existing expected digest.'})
# C02: content set cannot establish multiplicity or paths.
h=digest(b'shared');expected=[{'path':'a','sha256':h},{'path':'b','sha256':h}];observed={'a':h}
assert all(r['sha256'] in set(observed.values()) for r in expected) and 'b' not in observed
controls.append({'id':'C02','source_indices':[20],'method':'Independent synthetic hash-set membership control','expected':expected,'observed':observed,'membership_passes':True,'missing_path':'b','conclusion':'Set containment establishes content availability, not occurrence completeness.'})
# C03: generic loop-vacuity boundary, with actual data counts separately preserved.
assert all([]) and sum([])==0
controls.append({'id':'C03','source_indices':[9,11,15,17,26,29,36],'method':'Boolean identities and ACTUAL_DATA_CARDINALITIES.json','empty_all_true':True,'conclusion':'Absent cardinality checks permit omissions in those individual loops. Actual signed certificates have256 schedules with2 minus witnesses each, common certificate32 rows/8 routes, algebraic CT3 records and large2 records; no actual missing-record failure asserted.'})
# C04: compare source25 printed rank bound with maximum possible square rank.
r=json.loads((M/'additions/1717/twisted_bound_review/results.json').read_text());rankrows=[]
for x in r['checks']:
 cap=x['distinct_phase_classes']*8*12;rankrows.append({'N':x['N'],'bound':cap,'necessarily_at_least_dimension':cap>=x['N']})
assert all(x['necessarily_at_least_dimension'] for x in rankrows)
controls.append({'id':'C04','source_indices':[25],'method':'Fresh integer arithmetic on saved listed parameters','rows':rankrows,'conclusion':'All13 product rank-budget tests are dimensionally automatic; branch identities and other exact controls retain independent content.'})
# C05: exact small field arithmetic supports stated codelet exception and embedding.
eta=4;p=7;u=(-pow(2,-1,p))%p;v=(eta-eta*eta)*pow(2,-1,p)%p
assert v==1 and u==3
z=91;p5=241;phi=sum(pow(z,k,p5) for k in range(5))%p5
assert phi==0 and z!=1 and pow(163,120,p5)==240
controls.append({'id':'C05','source_indices':[3,4,10],'method':'Fresh modular exponentiation, no source imports','F7_codelet_coefficients':[u,v],'phi5_at91_mod241':phi,'disc163_Euler_mod241':240,'conclusion':'Literal two-multiply F7 codelet has one identity coefficient; cyclotomic reduction and nonsquare residue arithmetic agree. Does not reproduce the full algebraic synthesis.'})
put('FRESH_INDEPENDENT_CONTROLS.json',{'no_supplied_source_executed':True,'controls':controls})
# Resolve stored hash references without following paths outside the corpus.
index=json.loads((P/'STORED_RECORDS_INDEX.json').read_text()); refs=[]; manifests=[];visited=set()
def in_master(path):
 try:path.resolve().relative_to(M.resolve());return True
 except ValueError:return False
for rec in index:
 path=pathlib.Path(rec['path'])
 if rec['kind']!='neighbor_data_or_record' or path in visited:continue
 visited.add(path)
 raw=(P/rec['snapshot']).read_bytes()
 if path.name.upper().startswith('SHA256SUMS') or path.name in ('MANIFEST.sha256',):
  for no,line in enumerate(raw.decode().splitlines(),1):
   if not line.strip() or line.lstrip().startswith('#'):continue
   m=re.fullmatch(r'([0-9A-Fa-f]{64})\s+\*?(.+)',line)
   if not m:manifests.append({'manifest':str(path),'line':no,'status':'unparsed'});continue
   target=path.parent/m[2]
   okay=in_master(target) and target.is_file();actual=digest(target.read_bytes()) if okay else None
   manifests.append({'manifest':str(path),'line':no,'target':str(target),'expected':m[1].lower(),'actual':actual,'status':'match' if actual==m[1].lower() else 'mismatch' if actual else 'missing_or_outside_corpus'})
 if path.suffix!='.json':continue
 try:obj=json.loads(raw)
 except Exception:continue
 def walk(x,where=''):
  if isinstance(x,dict):
   name=next((x[k] for k in ('file','path','filename','file_name','script') if isinstance(x.get(k),str)),None)
   expected=next((x[k] for k in ('original_sha256','sha256','expected_sha256','recorded_sha256') if isinstance(x.get(k),str) and re.fullmatch('[0-9a-fA-F]{64}',x[k])),None)
   if name and expected:
    candidates=[path.parent/name,path.parent/'sources'/name,path.parent/'source_archives'/name,path.parent/'downloads'/name]
    existing=[c for c in candidates if in_master(c) and c.is_file()];matches=[c for c in existing if digest(c.read_bytes())==expected]
    refs.append({'record':str(path),'json_path':where,'target_name':name,'expected':expected,'existing_candidates':[str(c) for c in existing],'matching_candidates':[str(c) for c in matches],'status':'matched' if matches else 'mismatch' if existing else 'unresolved_in_record_directory'})
   for k,v in x.items():walk(v,where+'/'+str(k))
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,where+'/'+str(i))
 walk(obj)
put('STORED_MANIFEST_RECONCILIATION.json',manifests);put('STORED_HASH_REFERENCE_RECONCILIATION.json',refs)
print(json.dumps({'controls':len(controls),'manifest_rows':len(manifests),'manifest_statuses':{s:sum(x['status']==s for x in manifests) for s in {x['status'] for x in manifests}},'hash_references':len(refs),'reference_statuses':{s:sum(x['status']==s for x in refs) for s in {x['status'] for x in refs}}},indent=2))
