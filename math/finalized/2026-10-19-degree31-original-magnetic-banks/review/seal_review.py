#!/usr/bin/env python3
import argparse,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent

def record(path):
 b=path.read_bytes()
 return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def write(name,obj): (R/name).write_text(json.dumps(obj,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);a=ap.parse_args();c=a.candidate
 expected_manifest='6f2ecfb4e0ffb7a719f4d0558bbead83e8f6535a5cf1c0fe7b87e14efe19333a'
 if record(c/'MANIFEST.json')['sha256']!=expected_manifest:raise RuntimeError('candidate final manifest changed')
 manifest=json.loads((c/'MANIFEST.json').read_text());snap=R/'candidate_snapshot';snap.mkdir(exist_ok=True)
 for row in manifest['files']:
  source=c/row['path'];actual=record(source)
  if any(actual[k]!=row[k] for k in actual):raise RuntimeError('candidate manifest mismatch '+row['path'])
  dest=snap/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
 shutil.copy2(c/'MANIFEST.json',snap/'MANIFEST.json')
 if record(c/'DEGREE31_LITERAL_CERTIFICATE.json')['sha256']!='20ff3730c3b42568062d6da7151939c23ffd0abdf1bd6a8d79c1abfb905de5ad':raise RuntimeError('literal witness changed')
 literal=json.loads((R/'LITERAL_REVIEW.json').read_text())
 for name in ['LITERAL_REVIEW.json','ARITHMETIC_REVIEW.json','PROVENANCE_REVIEW.json','IMPLEMENTATION_REVIEW.json','COLD_REPLAY.json']:
  if json.loads((R/name).read_text())['verdict']!='PASS':raise RuntimeError('review receipt not PASS')
 binding={'verdict':'PASS','candidate_manifest_entries_verified':len(manifest['files']),
          'candidate_manifest_sha256':record(c/'MANIFEST.json')['sha256'],
          'candidate_report_sha256':record(c/'REPORT.md')['sha256'],
          'candidate_certificate_sha256':record(c/'DEGREE31_LITERAL_CERTIFICATE.json')['sha256'],
          'candidate_operation_ledger_sha256':record(c/'OPERATION_LEDGER.md')['sha256'],
          'source_pins_sha256':record(c/'SOURCE_PINS.json')['sha256'],
          'snapshot':'candidate_snapshot','snapshot_preserves_manifest_bytes':True,
          'all_source_copy_local_paths_verified_during_review':True,
          'historical_accepted_scientific_programs_executed':False}
 write('CANDIDATE_BINDING.json',binding)
 verdict={'verdict':'ACCEPT_SCOPE_LIMITED','date_utc':'2026-10-19',
          'theorem':'B(F_(53^31))=16 in the original N13 free-cross-singleton signed-resolvent grammar, allowing arbitrary legal beta and raw weights',
          'field_modulus':'u^31+2u+11 over F53','field_order_bits':178,'allocation':[7,1,1,7],
          'candidate_certificate_sha256':binding['candidate_certificate_sha256'],
          'candidate_manifest_sha256':binding['candidate_manifest_sha256'],
          'candidate_report_sha256':binding['candidate_report_sha256'],
          'review_report_sha256':record(R/'INDEPENDENT_REVIEW.md')['sha256'],
          'review_receipts':{n:record(R/n)['sha256'] for n in ['LITERAL_REVIEW.json','ARITHMETIC_REVIEW.json','PROVENANCE_REVIEW.json','IMPLEMENTATION_REVIEW.json','COLD_REPLAY.json','CANDIDATE_BINDING.json']},
          'banks':16,'branch_inverses':208,'both_inverse_orders':416,'inverse_entry_equalities':70304,
          'raw_and_amplitude_equalities':416,'bank_Weyl_equalities':2704,'full_sector_equalities':169,
          'target_entries':169,'target_mismatches':0,'standalone_cold_replay':'byte-identical receipt',
          'fresh_cpp_ubsan':'PASS, 1062 products, eleven powers, one inverse',
          'lower_bound':'Inherited accepted field-uniform theorem; no old witness or lower-minor computation rerun',
          'seed':202610192024,'cap_nonzero_cross_nodes':100000,'first_hit_zero_based_trial':1113,
          'prefix_prng_independently_reexecuted':True,'prefix_gate_split_arithmetic_independently_reexecuted':False,
          'candidate_complete_failed_prefix_replay_bound':True,'first_hit_not_required_for_theorem':True,
          'transfer':'31 divides d implies B(F_(53^d))=16','general_field_classification':False,
          'owner_closure':False,'priority_change':False,'FFT_or_novelty_claim':False,
          'scientific_correction_required':False,'external_writes':False,'additional_agents_created':False}
 write('VERDICT.json',verdict)
 rows=[]
 for path in sorted(R.rglob('*')):
  if not path.is_file() or '__pycache__' in path.parts or path.name=='MANIFEST.json' and path.parent==R:continue
  rows.append({'path':str(path.relative_to(R)),**record(path)})
 write('MANIFEST.json',{'files':rows,'excludes':['root MANIFEST.json','Python caches','temporary compiler binaries']})
 for row in json.loads((R/'MANIFEST.json').read_text())['files']:
  if any(record(R/row['path'])[k]!=row[k] for k in ('bytes','sha256','git_blob_sha1')):raise RuntimeError('review readback mismatch')
 print(json.dumps({'verdict':'ACCEPT_SCOPE_LIMITED','candidate_files_verified':len(manifest['files']),
                   'review_files_sealed':len(rows),'review_manifest_sha256':record(R/'MANIFEST.json')['sha256'],
                   'review_report_sha256':record(R/'INDEPENDENT_REVIEW.md')['sha256'],
                   'verdict_sha256':record(R/'VERDICT.json')['sha256']},indent=2))
if __name__=='__main__':main()
