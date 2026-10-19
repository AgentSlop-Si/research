#!/usr/bin/env python3
"""Independently audit field-choice receipts, fixed seed/cap, and every PRNG draw.
The discovery gate/splitting prefix is source-bound, not independently rerun here.
"""
import argparse,hashlib,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parent;m=runpy.run_path(str(R/'literal_review.py'))
require=m['require'];P,D=53,31

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);args=ap.parse_args();c=args.candidate
 tests=json.loads((c/'FIELD_SEARCH.json').read_text())['tests']
 expected=[(1,k) for k in range(1,53)]+[(2,k) for k in range(1,12)]
 require([(r['linear'],r['constant']) for r in tests]==expected,'63 lexicographic modulus candidates')
 tested=[]
 for row in tests:
  h=[row['constant'],row['linear']]+[0]*29+[1];a=[0,1]
  first=m['ppow'](a,P,h)
  for k in range(D):a=m['ppow'](a,P,h)
  gcd=m['pgcd'](h,m['polyadd'](first,[0,1],-1))
  irreducible=a==[0,1] and gcd==[1]
  require(a==row['final_frobenius'] and gcd==row['gcd'] and irreducible==row['irreducible'],'modulus family exact Frobenius/gcd')
  tested.append({'linear':row['linear'],'constant':row['constant'],'irreducible':irreducible})
 require([r['irreducible'] for r in tested]==[False]*62+[True],'first tested irreducible modulus')
 scope=json.loads((c/'SEARCH_SCOPE.json').read_text());amend=json.loads((c/'SEARCH_SCOPE_AMENDMENT.json').read_text())
 require(scope['seed']==202610192024 and scope['cap_nonzero_cross_nodes']==100000,'frozen seed/cap')
 require(amend['seed_unchanged']==scope['seed'] and amend['nonzero_cross_node_cap_unchanged']==scope['cap_nonzero_cross_nodes'],'representation-only amendment')
 require(amend['support_search_started'] is False and amend['extension_inversion_started'] is False,'amendment recorded before search/inversion')
 chronology=json.loads((c/'DISCOVERY_CHRONOLOGY.json').read_text())
 for name,h in chronology['preflight_hashes'].items():require(sha(c/name)==h,'preflight hash binding')
 ledger_raw=(c/'PREFIX_LEDGER.jsonl').read_bytes();ledger=[json.loads(line) for line in ledger_raw.splitlines()]
 seed=scope['seed'];state=seed;mask=(1<<64)-1;draws=zeroes=nodes=candidates=hits=0
 for row in ledger:
  require(row['rng_before']==state,'PRNG initial state for row')
  y=[]
  for k in range(D):
   state ^= (state<<13)&mask;state ^= state>>7;state ^= (state<<17)&mask
   state &= mask;y.append(state%P);draws+=1
  require(state==row['rng_after'],'PRNG final state for row')
  if row.get('zero_draw'):
   require(y==[0]*D,'zero-node skip');zeroes+=1;continue
  require(row['trial']==nodes and row['y']==y,'sequential nonzero cross nodes')
  nodes+=1
  for root in row['gate_roots']:
   require(len(root['H'])==8 and all(len(a)==D and all(type(v) is int and 0<=v<P for v in a) for a in root['H']),'canonical prefix polynomial')
   require(root['nonzero_constant']==any(root['H'][0]),'nonzero-constant gate')
   candidates+=root['nonzero_constant'];hits+=root['fully_splits']
  require(row['cumulative_candidates']==candidates,'prefix candidate count')
  require(row['hit']==any(r['fully_splits'] for r in row['gate_roots']),'hit flag')
  if row['hit']:require(row is ledger[-1],'stop on first reported hit')
 require(nodes==1114 and draws==34534 and zeroes==0 and candidates==1117 and hits==1,'exact first-hit counts')
 last=ledger[-1];hit=next(r for r in last['gate_roots'] if r['fully_splits'])
 candidate=json.loads((c/'NONSTABLE_CANDIDATE.json').read_text());cert=json.loads((c/'DEGREE31_LITERAL_CERTIFICATE.json').read_text())
 require(candidate['trial']==1113 and candidate['y']==last['y']==cert['y']==cert['z'],'witness node binding')
 require(candidate['H']==hit['H']==cert['H'] and candidate['lambda']==hit['lambda'],'witness polynomial binding')
 replay=json.loads((c/'FIRST_HIT_REPLAY.json').read_text())
 require(replay['verdict']=='PASS' and replay['full_failed_prefix_and_first_hit_reexecuted'],'candidate prefix replay claim')
 runs=replay['runs'];require([r['nonzero_node_limit'] for r in runs]==[1113,1114] and [r['exit_code'] for r in runs]==[1,0],'prefix replay boundary')
 first_raw=b'\n'.join(ledger_raw.splitlines()[:-1])+b'\n'
 require(hashlib.sha256(first_raw).hexdigest()==runs[0]['prefix_sha256'],'failed-prefix bytes')
 require(sha(c/'PREFIX_LEDGER.jsonl')==runs[1]['prefix_sha256']==chronology['prefix_sha256'],'first-hit prefix bytes')
 require(sha(c/'NONSTABLE_CANDIDATE.json')==runs[1]['candidate_output_sha256'],'replayed candidate bytes')
 # Bind inherited acceptance without executing any accepted old witness.
 v=json.loads((c/'sources/DEGREE29_REVIEW_VERDICT.json').read_text())
 require(v['verdict']=='ACCEPT_SCOPE_LIMITED','inherited acceptance')
 for key,name in [('candidate_report_sha256','REPORT.md'),('review_report_sha256','DEGREE29_REVIEW_INDEPENDENT_REVIEW.md'),('arithmetic_sha256','DEGREE29_REVIEW_ARITHMETIC.json')]:
  require(sha(c/'sources'/name)==v[key],'accepted predecessor byte binding')
 lower=(c/'sources/ACCEPTED_LOWER_REVIEW.md').read_text()
 require('for every characteristic-53 field and every legal beta' in lower and 'at least seven distinct nonzero effective alpha nodes' in lower,'inherited field-uniform lower theorem text')
 out={'verdict':'PASS','modulus_candidates_independently_checked':tested,'modulus_family_amendment':amend,
      'seed':seed,'cap_nonzero_nodes':100000,'nonzero_nodes':nodes,'coefficient_draws':draws,
      'zero_nodes_skipped':zeroes,'recurrence_candidates':candidates,'first_hit_zero_based_trial':1113,
      'prng_prefix_independently_reexecuted':True,'all_gate_and_split_results_independently_reexecuted':False,
      'candidate_full_prefix_replay_receipt_bound':True,'first_hit_not_premise_of_literal_theorem':True,
      'prefix_sha256':sha(c/'PREFIX_LEDGER.jsonl'),'candidate_sha256':sha(c/'NONSTABLE_CANDIDATE.json'),
      'certificate_sha256':sha(c/'DEGREE31_LITERAL_CERTIFICATE.json'),'inherited_lower_theorem_byte_bound':True,
      'inherited_old_witnesses_executed':False,
      'source_hashes':{name:sha(c/name) for name in ['SEARCH_SCOPE.json','SEARCH_SCOPE_AMENDMENT.json','FIELD_SEARCH.json','DISCOVERY_CHRONOLOGY.json','PREFIX_LEDGER.jsonl','FIRST_HIT_REPLAY.json','SEARCH_RESOURCE.json']}}
 (R/'PROVENANCE_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: all 63 field candidates; 34,534 PRNG draws; 1,114-node first-hit ledger; inherited acceptance binding.')
if __name__=='__main__':main()
