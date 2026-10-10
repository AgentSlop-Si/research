#!/usr/bin/env python3
"""Fresh static metadata check of supplemental text/math review seals."""
import runpy,pathlib,json,hashlib,collections
ns=runpy.run_path('final_review_closure_0535/audit_coverage.py');audit=ns['audit_package'];dump=ns['dump'];P=ns['P'];R=ns['R'];O=ns['O'];reg=json.loads((R/'ADDITIVE_CODE_COVERAGE.json').read_text());already={r['package'] for r in reg['rows']+reg['semantic_template_rows']}
extras=set()
def find(x):
 if isinstance(x,str) and (P/x).is_dir(): extras.add(x)
 elif isinstance(x,dict):
  for k,v in x.items():find(k);find(v)
 elif isinstance(x,list):
  for v in x:find(v)
for f in R.glob('*ACCEPTANCE*.json'):find(json.loads(f.read_text()))
extras|={'coverage_audit_20261010/review_queue1_aggregate','coverage_audit_20261010/review_queue2_complete207','coverage_audit_20261010/review_recovered_hero17_phase11','external_inventory_text_review_0225/sealed_reconciliation_0233','recovered_companion_review_0217','remaining_bank_certificates_audit_0243'}
checks=[]
for name in sorted(extras-already):
 check,bh=audit(P/name);checks.append(check)
dump('SUPPLEMENTAL_PACKAGE_INTEGRITY.json',checks)
print('SUPPLEMENTAL',len(checks),'errors',[{'directory':x['directory'],'errors':[e for e in x['entry_checks'] if not e['matches'] or not e['size_matches']],'parse_errors':x['parse_errors']} for x in checks if not x['all_entry_hashes_match']])
q1=json.loads((P/'coverage_audit_20261010/review_queue1_aggregate/COVERAGE.json').read_text());q2=json.loads((P/'coverage_audit_20261010/review_queue2_complete207/COVERAGE.json').read_text());r70=json.loads((P/'external_inventory_text_review_0225/sealed_reconciliation_0233/ITEM_RECONCILIATION.json').read_text())
print('q1row',str(q1['rows'][0])[:1400]);print('q2row',str(q2['rows'][0])[:1400])
