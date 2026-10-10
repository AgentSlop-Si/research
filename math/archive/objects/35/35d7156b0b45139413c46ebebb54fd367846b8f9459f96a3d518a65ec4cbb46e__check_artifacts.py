"""Reviewer-authored inert artifact consistency checks. Never loads supplied code."""
import pathlib,json,hashlib,csv,io,math,zipfile,datetime
out=pathlib.Path('fusion_phase_source_review_0408');master=pathlib.Path('fft_research_master_20261009')
rows=json.loads((out/'INPUT_ROWS.json').read_text());ev=json.loads((out/'EVIDENCE_MANIFEST.json').read_text()); checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def evpath(n):return next((out/'evidence').glob(f'{n:03d}_*'))
def data(n):return json.loads(evpath(n).read_text())
def check(name,ok,details): checks.append({'check':name,'passed':bool(ok),'details':details})
# Check manifests as data, containing each entry within its manifest directory.
mc=[]
for e in ev:
 p=pathlib.Path(e['path']);name=p.name
 if name not in ['MANIFEST.sha256','SHA256SUMS.txt','SHA256SUMS.json']:continue
 raw=(out/e['snapshot']).read_text();entries=[]
 if name.endswith('.json'):
  d=json.loads(raw)
  entries=[(x['name'],x['sha256']) for x in d['artifacts']] if 'artifacts' in d else [(k,v['sha256']) for k,v in d.items()]
 else:
  for line in raw.splitlines():
   if not line.strip():continue
   h,n=line.split(maxsplit=1);entries.append((n.lstrip('* '),h))
 for n,h in entries:
  target=p.parent/n
  contained=target.resolve().is_relative_to(p.parent.resolve())
  exists=contained and target.is_file();actual=sha(target.read_bytes()) if exists else None
  mc.append({'manifest':str(p),'name':n,'expected':h,'actual':actual,'status':'match' if actual==h else 'absent_from_extracted_tree' if not exists else 'MISMATCH'})
(out/'EMBEDDED_MANIFEST_CHECKS.json').write_text(json.dumps(mc,indent=2))
check('embedded manifests of available exact files',not any(x['status']=='MISMATCH' for x in mc),{'entries':len(mc),'matched':sum(x['status']=='match' for x in mc),'absent_from_extracted_tree':[x for x in mc if x['status']=='absent_from_extracted_tree']})
# Compare each original read target and canonical representative to frozen identity.
orig=[]
for r in rows:
 for kind,p in [('code_bytes',pathlib.Path(r['local_content'])),('master_representative',master/r['representative_path'])]:
  orig.append({'kind':kind,'path':str(p),'sha256':sha(p.read_bytes()),'expected_sha256':r['sha256'],'size_bytes':p.stat().st_size,'matches':sha(p.read_bytes())==r['sha256']})
(out/'ORIGINAL_SOURCE_MANIFEST.json').write_text(json.dumps(orig,indent=2))
# Exact arithmetic on archived coefficients only; no supplied functions.
for n in [98,99,97]:
 c=data(n);p=c['prime'];terms={}
 for left,right in [(c['bezout_u'],c['p1_coefficients']),(c['bezout_v'],c['p2_coefficients'])]:
  for i,a in enumerate(left):
   for j,b in enumerate(right):terms[i+j]=(terms.get(i+j,0)+a*b)%p
 ok=terms.get(0)==1 and all(v==0 for k,v in terms.items() if k)
 check(f"saved Bezout N={c['n']}",ok,{'snapshot':str(evpath(n).relative_to(out)),'degrees':[len(c['p1_coefficients'])-1,len(c['p2_coefficients'])-1],'nonzero_leading_coefficients':all(c[k][-1]%p for k in ['p1_coefficients','p2_coefficients']),'boundary':'Verifies coefficient identity only; does not rebuild the defining matrix polynomials or prove their characteristic-zero degrees.'})
# Source/output schema consistency without executing source.
ann=data(103)
check('annihilator saved-output completeness for current script', 'bitrev_all_widths' in ann,{'source_sha256':rows[39]['sha256'],'source_lines':'30-39 unconditionally append bitrev_all_widths before writing at line 62','saved_result_sha256':sha(evpath(103).read_bytes()),'missing_keys':['bitrev_all_widths'] if 'bitrev_all_widths' not in ann else [],'existing_counts':{k:len(v) for k,v in ann.items() if isinstance(v,list)},'impact':'Existing result sections retained; no stored result for added all-width sweep; no theorem invalidation inferred.'})
# Stored numerical negative results preserved, not rerun.
b=list(csv.DictReader(io.StringIO(evpath(71).read_text())))
unst=[{'n':int(r['n']),'blocks':int(r['blocks']),'decoder_error':r['decoder_error']} for r in b if r['recurrence_stable_binary64']=='0']
check('v14 saved stability summary matches rows',len(unst)==data(68)['binary64_unstable_rows'],{'rows':len(b),'unstable':unst,'boundary':'Archived numerical failures; no fresh numerical execution.'})
d=data(73);summary=d['summary']
check('v14 summary counts',summary['decoder_cases']==len(d['decoder_checks']) and summary['covariance_cases']==len(d['covariance_checks']) and summary['finite_field_cases']==len(d['finite_field_certificate']) and summary['robust_diagnostic_cases']==len(d['robust_diagnostics']),summary)
ph=data(33)
check('phase27 archived arithmetic',all(c['affine_gap']['checked']==c['n']**2//2 and c['rank_two_trap_difference']==2 and c['dense_trap_nonzero_formula']==c['n']**2-3*c['n']+4 and c['exact_graph_gap']['exact_positive_pivots']==c['n'] for c in ph['finite_instance_certificates']),{'sizes':[c['n'] for c in ph['finite_instance_certificates']],'full_pivot_sequence_stored':False,'boundary':'Counts/formulas checked; archived pivot hashes not independently recomputed.'})
check('phase28 saved trace differences',all((c['trace2_target']-c['trace2_middle'])%data(95)['field_prime']==c['nonzero_difference'] and c['nonzero_difference']!=0 for c in data(95)['certificates']),{'count':len(data(95)['certificates'])})
suite=data(86);check('phase5 stored suite all six successful',len(suite)==6 and all(x['returncode']==0 for x in suite),{'scripts':[x['script'] for x in suite]})
check('v15 finite-field scope',[(r['q'],r['basis_vectors_checked']) for r in data(133)['records']]==[(56,56),(119,119),(136,24),(238,24)],{'all_passed':data(133)['all_passed'],'boundary':'Only first two lengths have all-basis coverage; last two are partial-basis plus six dense vectors.'})
check('source-comparison extra keys provenance',True,{'source_lines':'32 builds base summary','additional_saved_keys':[k for k in data(118) if k in ['unique_member_hash_count','unique_byte_new_hash_count']],'boundary':'Saved SOURCE_COMPARISON includes postprocessed counts beyond literal extractor output; not evidence the shown script alone wrote every field.'})
# Named inherited archive identities and requested dependencies from contained members.
archive_checks=[]
archive_paths=[master/'additions/2020_2027/hero1_phase14/original/fft_hero1_phase14_20261010.zip',master/rows[27]['representative_path'].rsplit('/',1)[0]/'prior_phase4_bundle.zip',master/rows[39]['representative_path'].rsplit('/',1)[0]/'prior_checkpoint_full.zip']
for ap in archive_paths:
 if not ap.exists():archive_checks.append({'path':str(ap),'exists':False});continue
 raw=ap.read_bytes();ar={'path':str(ap),'sha256':sha(raw),'size':len(raw),'selected_members':[]}
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for zi in z.infolist():
   if pathlib.PurePosixPath(zi.filename).name in ['unit_step_core.py','mixedradix.py','composite_cycle_core.py','exact_batch.py','prior_checkpoint_full.zip','test_twisted_gate.py']:
    b=z.read(zi);h=sha(b);dest=out/'dependencies'/h;dest.parent.mkdir(exist_ok=True);dest.write_bytes(b)
    ar['selected_members'].append({'name':zi.filename,'sha256':h,'bytes':len(b),'snapshot':str(dest.relative_to(out)),'inspection':'identity only; no additional full-review credit'})
 archive_checks.append(ar)
(out/'ARCHIVE_DEPENDENCY_IDENTITIES.json').write_text(json.dumps(archive_checks,indent=2))
(out/'ARTIFACT_CHECKS.json').write_text(json.dumps({'method':'Independent reviewer metadata and integer arithmetic only. Uploaded source never run/imported/compiled/parsed.','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks},indent=2))
print('Artifact checks',[(c['check'],c['passed']) for c in checks]);print('Manifests',len(mc),'mismatch',sum(x['status']=='MISMATCH' for x in mc),'missing',sum(x['status']=='absent_from_extracted_tree' for x in mc));print('Archives',json.dumps(archive_checks,indent=2))
