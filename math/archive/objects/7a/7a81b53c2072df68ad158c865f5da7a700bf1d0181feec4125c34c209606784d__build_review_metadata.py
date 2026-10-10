"""Review-owned metadata checks only: never imports, parses, compiles, or runs supplied programs."""
from pathlib import Path
import hashlib,json,math,zipfile,io
O=Path(__file__).resolve().parent
R=Path('fft_research_master_20261009/additions')
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
src=read(O/'SOURCE_INDEX.json')
a=read(R/'1845/source_excerpts/fft_green_phase24_ordering_defect/audit.json')
e=read(R/'1848/CHECK_RESULTS.json');s=read(R/'1848/SCREEN_CHECK_RESULTS.json');p=read(R/'1906_centered/precision_audit/CHECK_RESULTS.json');log=read(R/'1906_centered/precision_audit/CHECK_RUN.log')
checks={
 'method':'Reviewer-authored inert JSON/schema/count/hash/algebra checks; no supplied source execution, import, compile, or syntax parse.',
 'phase24_histogram_rows':len(a['exhaustive']),
 'phase24_histogram_totals_valid':all(sum(r['rank_distribution'].values())==r['sequences']==1<<r['n'] for r in a['exhaustive']),
 'phase24_total_binary_words':sum(r['sequences'] for r in a['exhaustive']),
 'phase24_sample_minima':[{'n':r['n'],'minimum':r['min_rank_over_every_stride_and_sample'],'joint_probability_bound':r['explicit_joint_probability_lower_bound']} for r in a['random_all_stride_audit']],
 'endpoint_result_counts':e['counts'],
 'endpoint_counts_derived_from_source_loop_ranges':{'direct_cut_ranks':3*(sum(n-1 for n in (4,8,16,32,64))+26),'exhaustive_n8_critical_minors':3*math.comb(8,3)*math.comb(8,5),'random_critical_minors':3*4*24,'coset_decompositions':3*8*(2+3+3+3+3),'consecutive_coset_ranks':3*8*(2+3+3+3+3),'moment_algebra_cases':sum(2**(m-1) for m in range(1,16))},
 'screen_result_matches_saved_log':s==read(R/'1848/SCREEN_RUN.log'),
 'screen_joint_tables_sum_to_factorial8':all(sum(v.values())==math.factorial(8) for v in s['comparisons'].values()),
 'v11_logged_test_methods':sum(l.startswith('test_') for l in (R/'1906_centered/extracted/fft_hero1_centered_v12/test_v11_regression.log').read_text().splitlines()),
 'v11_source_test_methods':sum(l.startswith('    def test_') for l in (O/src[5]['snapshot']).read_text().splitlines()),
 'precision_saved_group_lengths':{k:len(v) for k,v in p.items() if isinstance(v,list)},
 'precision_source_summary_matches_extracted_original':(R/'1906_centered/precision_audit/SOURCE_RESULT_SUMMARY.json').read_bytes()==(R/'1906_centered/extracted/fft_hero1_centered_v12/RESULT_SUMMARY.json').read_bytes(),
 'precision_source_sha256':src[6]['row']['sha256'],
 'precision_saved_result_sha256':sha((R/'1906_centered/precision_audit/CHECK_RESULTS.json').read_bytes()),
 'precision_saved_log_sha256':sha((R/'1906_centered/precision_audit/CHECK_RUN.log').read_bytes()),
 'precision_report_sha256':sha((R/'1906_centered/precision_audit/V12_PRECISION_AUDIT.md').read_bytes()),
 'precision_version_mismatch':{'required_unconditional_source_key':'source_centered_envelope','present_in_saved_result':'source_centered_envelope' in p,'current_centered_envelope_formula':'2*exp(pi/4)-1','elementary_formula_diagnostic_binary64':2*math.exp(math.pi/4)-1,'saved_centered_envelope':p['centered_envelope'],'looser_report_formula':'1+2*exp(pi*pi/32)*(exp(pi/4)-1)','looser_formula_diagnostic_binary64':1+2*math.exp(math.pi**2/32)*math.expm1(math.pi/4),'current_H0_mass_limit':'2*exp(pi/4)-1','saved_H0_mass':p['symmetric_envelope_mass'][0]['mass'],'classification':'Source/report/result version mismatch; precise generating source unlocated; no fabrication claim.'}
}
checks['endpoint_counts_match_loop_ranges']=checks['endpoint_result_counts']==checks['endpoint_counts_derived_from_source_loop_ranges']
seals=[]
for rel in ['1848/SHA256SUMS.txt','1906_centered/precision_audit/SHA256SUMS.txt']:
 manifest=R/rel
 rows=[]
 for line in manifest.read_text().splitlines():
  h,name=line.split('  ',1);target=manifest.parent/name
  rows.append({'name':name,'expected':h,'actual':sha(target.read_bytes()) if target.is_file() else None,'matches':target.is_file() and sha(target.read_bytes())==h})
 seals.append({'manifest':str(manifest),'rows':rows,'all_matches':all(r['matches'] for r in rows)})
checks['manifest_checks']=seals
archive=R/'1845/source_archives/fft_green_research_phase24_2026-10-09(1).zip'
with zipfile.ZipFile(archive) as z:
 prefix='fft_green_phase24_ordering_defect/'
 entries=[]
 for line in z.read(prefix+'SHA256SUMS.txt').decode().splitlines():
  h,name=line.split('  ',1);entries.append({'name':name,'matches':sha(z.read(prefix+name))==h})
 old=z.read(prefix+'previous_full_phase23_checkpoint.zip')
 with zipfile.ZipFile(io.BytesIO(old)) as oz:
  testnames=[n for n in oz.namelist() if '/tests/' in n and n.endswith('.py')]
  counts={n:sum(l.lstrip().startswith('def test_') for l in oz.read(n).decode().splitlines()) for n in testnames}
 checks['phase24_archive']={'path':str(archive),'sha256':sha(archive.read_bytes()),'manifest_entries':entries,'all_match':all(x['matches'] for x in entries),'nested_phase23_sha256':sha(old),'nested_phase23_test_method_counts':counts,'nested_phase23_total_static_test_methods':sum(counts.values()),'zip_members_only_read_not_extracted_or_executed':True}
(O/'EVIDENCE_RECONCILIATION.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['manifest_checks','phase24_archive']},indent=2))
