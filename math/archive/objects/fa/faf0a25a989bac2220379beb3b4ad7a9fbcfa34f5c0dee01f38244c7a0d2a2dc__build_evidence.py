"""Reviewer-authored metadata-only evidence inventory. Never loads supplied Python."""
from pathlib import Path
import json,hashlib,shutil,zipfile
O=Path('chirp_phase_source_review_0357');B=Path('fft_research_master_20261009/additions')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,obj):(O/name).write_text(json.dumps(obj,indent=2)+'\n')
identities=[]
for group in ['1906_chirp','1908','1910']:
 for p in sorted((B/group).rglob('*')):
  if not p.is_file():continue
  data=p.read_bytes();relative=p.relative_to(B);copy=O/'evidence_snapshots'/relative;copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(data)
  identities.append({'path':str(p),'snapshot':str(copy.relative_to(O)),'sha256':sha(data),'bytes':len(data),'kind':'assigned_source' if p.suffix=='.py' else ('archive_bytes_only' if p.suffix=='.zip' else 'supporting_evidence'),'coverage_credit_from_hashing':False})
save('EVIDENCE_IDENTITIES.json',identities)
manifests=[]
for group,name,complete in [('1906_chirp','SHA256SUMS',True),('1906_chirp/chirp_audit','SHA256SUMS',True),('1908','SHA256SUMS.txt',True),('1908','APPROVED_SUPPLEMENT_SHA256SUMS.txt',False),('1910','SHA256SUMS.txt',True)]:
 root=B/group;p=root/name;rows=[]
 for line in p.read_text().splitlines():
  if not line.strip():continue
  expected,s=line.split(None,1);s=s.lstrip('*');f=root/s;canonical=str(f.relative_to(root));data=f.read_bytes()
  rows.append({'relative_path':canonical,'expected_sha256':expected,'actual_sha256':sha(data),'match':expected==sha(data)})
 names={r['relative_path'] for r in rows};present={str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f!=p and '__pycache__' not in f.parts and f.suffix!='.pyc'}
 manifests.append({'manifest':str(p),'sha256':sha(p.read_bytes()),'entries':rows,'all_hashes_match':all(r['match'] for r in rows),'full_current_package_manifest':complete,'unlisted_files':sorted(present-names),'listed_but_absent':sorted(names-present)})
save('MANIFEST_CHECKS.json',manifests)
# Open only known archive bytes to identify exact dependency members. No extract/import/exec.
Z=B/'1910/sources';expect=json.loads((B/'1910/PROVENANCE_VERIFICATION.json').read_text())['archive_hashes'];zs={};ares=[]
for name,h in expect.items():
 p=Z/name;z=zipfile.ZipFile(p);zs[name]=z;assert sha(p.read_bytes())==h
 ares.append({'archive':str(p),'sha256':h,'crc_bad_member':z.testzip(),'member_count':len(z.infolist()),'uncompressed_bytes':sum(i.file_size for i in z.infolist())})
v12=zs['offset_class_v12_original.zip'];manifest=next(n for n in v12.namelist() if n.endswith('/MANIFEST.sha256'));prefix=manifest.rsplit('/',1)[0]+'/'
entries=[]
for line in v12.read(manifest).decode().splitlines():
 h,s=line.split(None,1);s=s.lstrip('*');data=v12.read(prefix+s);entries.append({'member':prefix+s,'sha256':sha(data),'expected_sha256':h,'match':sha(data)==h,'inspection':'hash_only_not_source_read'})
member_refs=[('offset_class_v12_original.zip',prefix+'unit_step_core.py'),('v9_prior_original.zip','fft_unit_step_chirp_v9/prototype.py'),('v11_prior_original.zip','fft_all_length_fused_fp_v11/unit_step_core.py'),('offset_class_v12_original.zip',prefix+'v11_fused_reference.py'),('v11_prior_original.zip','fft_all_length_fused_fp_v11/prototype.py')]
member_ids=[{'archive':a,'member':m,'sha256':sha(zs[a].read(m)),'bytes':len(zs[a].read(m)),'full_source_inspection':False,'new_coverage_credit':False} for a,m in member_refs]
save('DEPENDENCY_IDENTITIES.json',{'local_imports':[{'importing_source':'test_eliminant_extension.py','module':'eliminant_extension','sha256':'e5a16a36790bd9eaa59857542b6cad1404cc35a6a67ca74ffa9370c47f713db0','resolution':'intended adjacent file, bytes verified, not dynamically imported'},{'importing_source':'self_test_checker.py','module':'check_bitrev','sha256':'7e61ae8680e03027c0c2eab49eeaf30bfd696cb8a1a8eaf51fc76794afb3f77f','resolution':'intended adjacent file, bytes verified, not dynamically imported'}],'external_dependencies':[{'module':'numpy','stored_version':'2.3.5 for 1908; unrecorded in 1910 results','current_runtime_imported':False,'dependency_closure_reviewed':False},{'module':'Python standard library','stored_version':'3.12.14 for 1908; not independently executed','current_runtime_stdlib_used_only_for_metadata':True}],'subprocess_targets':[{'source':'verify_and_rerun.py','target':'chirp_audit/independent_checker.py','sha256':'127e177eb721583d6fdcd7020c64db59dad0cf5aa62861ed0eb206ae4bcab00b'},{'source':'verify_and_rerun.py','target':'eliminant_extension/test_eliminant_extension.py','sha256':'43766d08eaaceeee1ae0994d69a6c6c6dc80cd0d52dafaf7335c9a309a9d057c'}],'archives':ares,'v12_manifest_entries':entries,'dependency_members':member_ids,'core_three_way_byte_identity':len({x['sha256'] for x in member_ids[:3]})==1,'reference_two_way_byte_identity':member_ids[3]['sha256']==member_ids[4]['sha256'],'archive_hash_reads_are_not_source_coverage':True})
# Reconcile saved counters/identities only, without recomputing program outcomes.
c=json.loads((B/'1906_chirp/chirp_audit/independent_results.json').read_text());e=json.loads((B/'1906_chirp/eliminant_extension/test_results.json').read_text());br=json.loads((B/'1908/checks/checks.json').read_text());summary=json.loads((B/'1908/checks/summary.json').read_text());tests=json.loads((B/'1908/checks/self_tests.json').read_text());off=json.loads((B/'1910/audit/independent_results.json').read_text())
rows=br['results'];bad=[]
for r in rows:
 n,t,p=r['n'],r['t'],r['prime'];upper=min(n*n,n+t*(4*n-6))
 if r['rank']!=upper or r['upper_bound']!=upper:bad.append([n,t,p,'rank_metadata'])
 if r['gauges']['gauge_rank']!=6*t+(t-1)*n:bad.append([n,t,p,'gauge_metadata'])
 if r['gauges']['jacobian_nullity']!=5*n*t-r['rank']:bad.append([n,t,p,'nullity_metadata'])
 if len(r['finite_difference_columns'])!=30:bad.append([n,t,p,'fd_count'])
 for idx in r['rank_certificate']['pivot_columns']:
  if not 0<=idx<5*n*t:bad.append([n,t,p,'pivot_column_range'])
 full=r['saved_full_rank_minor_determinant']
 if full is not None:
  w=json.loads((B/f'1908/inputs/WITNESS_N{n}_T{t}.json').read_text());cert=w['certificates_by_field'][str(p)]
  if full!=cert['full_rank_minor_det_mod_prime']:bad.append([n,t,p,'saved_determinant_metadata'])
save('STORED_RESULT_RECONCILIATION.json',{'scope':'Stored data/counter and identity reconciliation only. No supplied source executed, imported, compiled, parsed or translated to rerun its algorithms.','chirp_checker_identity_matches':c['checker_sha256']==sha((B/'1906_chirp/chirp_audit/independent_checker.py').read_bytes()),'chirp_note_identity_matches':c['source_sha256']==sha((B/'1906_chirp/chirp_audit/source/RESEARCH (2).md').read_bytes()),'chirp_gauss_row_count_matches':c['all_gauss_phases']['rows']==sum(range(1,81)),'chirp_gauss_bin_count_matches':c['all_gauss_phases']['bins']==sum(n*n for n in range(1,81)),'chirp_exhaustive_vectors':sum(x['vectors'] for x in c['exhaustive_membership']),'extension_stored_test_groups':e['test_groups_run'],'extension_stored_counts':{k:v for k,v in e.items() if isinstance(v,(int,bool))},'bitrev_stored_detailed_rows':len(rows),'bitrev_stored_summary_rows':summary['rank_checks'],'bitrev_rank_gauge_metadata_errors':bad,'bitrev_stored_self_tests':len(tests['tests']),'bitrev_worst_dot_bound':1440*(65537-1)**2,'signed_int64_limit':2**63,'bitrev_loaded_witness_parameter_range':[1,12288],'offset_covariance_parameters_all_in_claimed_regime':all(x['Q']>=x['M']**2 for x in off['exact_covariance_certificates']),'offset_numerical_states':sum(x['states'] for x in off['numerical_all_state_lift_operator_checks']),'offset_results_log_byte_identical':(B/'1910/audit/independent_results.json').read_bytes()==(B/'1910/audit/independent_run.log').read_bytes(),'no_stored_result_error_established':not bad})
print('Evidence snapshots',len(identities),'all manifests match',all(m['all_hashes_match'] for m in manifests),'all complete manifest sets match',all(not m['unlisted_files'] and not m['listed_but_absent'] for m in manifests if m['full_current_package_manifest']),'bitrev metadata errors',bad,'dependency members',member_ids)
