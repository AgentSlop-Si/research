"""Independent v2 byte/data audit. No NTT code, original generator, or oracle is executed."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
ROOT=Path('/workspace/scratch/928904ebc9b0');V1=ROOT/'paid_ntt_contract_1546';V2=ROOT/'paid_ntt_contract_v2_1622';OUT=ROOT/'paid_ntt_contract_v2_audit_1627'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def check_manifest(base):
    files=read(base/'FILES_SHA256.json')
    for f in files:
        p=base/f['file'];assert p.stat().st_size==f['bytes'] and digest(p)==f['sha256']
    return len(files)
expected={'PAID_NTT_CONTRACT.md':'0cefd28b3548a2368ca87b6429b4775aff7e8e16d28913dfaaf4c2a324ca2301','PROTOCOL.json':'e97f0f3da08ed17804169262fb8f31872032f53ab708091419af4b2eec28f3dd','FILES_SHA256.json':'def2f742943cc2a50b15c785cf1a14b4605f9a93a6d48e3ed9e029688be676ff'}
for f,h in expected.items():assert digest(V2/f)==h
assert digest(ROOT/'paid_ntt_contract_audit_1613/INDEPENDENT_PROTOCOL_REVIEW.md')=='ff43683d04cf5493afc84196938bcfcb695374ec284f84501b66d56a40f1f0f2'
result={'bound_v2_pins':expected,'original_review_pin':'PASS','v1_manifest_files_verified':check_manifest(V1),'v2_manifest_files_verified':check_manifest(V2)}
accepted=['SOURCE_IDENTITIES.json','CORPUS_MANIFEST.json','corpus_inputs.bin','MODULUS_ROOT_CERTIFICATE.json','STATIC_COUNTS.csv']
assert all((V1/f).read_bytes()==(V2/f).read_bytes() for f in accepted)
result['unchanged_accepted_files']=accepted
for s in read(V2/'SOURCE_IDENTITIES.json')['sources']:
 p=Path(s['path']);assert len(p.read_bytes())==s['bytes'] and digest(p)==s['sha256']
result['recovered_sources_still_pinned']='PASS'
old_orders=read(V1/'PAIRED_ORDER.json')['orders'];new_orders=read(V2/'PAIRED_ORDER.json')['orders'];assert old_orders==new_orders
result['all_48_algorithm_order_records_unchanged']=True
corpus=(V2/'corpus_inputs.bin').read_bytes();manifest=read(V2/'CORPUS_MANIFEST.json');index={(r['n'],r['case']):r for r in manifest['vectors']}
pools=read(V2/'FIXTURE_POOLS.json')['pools'];assert [r['n'] for r in pools]==[2**e for e in range(1,19)]
poolindex={}
for pool in pools:
 n=pool['n'];assert pool['cases']==[f'dense_{i}' for i in range(8)]
 slices=[]
 for i,s in enumerate(pool['source_slices']):
  assert s['case']==f'dense_{i}'
  entry=index[n,s['case']]
  assert s['offset_bytes']==entry['offset_bytes'] and s['length_bytes']==entry['length_bytes']==4*n
  slices.append(corpus[s['offset_bytes']:s['offset_bytes']+s['length_bytes']])
 assert len(slices)==8
 payload=b''.join(slices);assert len(payload)==pool['serialized_bytes']==32*n
 assert sha256(payload).hexdigest()==pool['sha256'];poolindex[n]=pool
result['all_18_fixture_pool_byte_pins_verified']=True
expanded=read(V2/'EXPANDED_PILOT_TRIALS.json');trials=expanded['trials'];assert len(trials)==768
expected_rows=[]
for order in new_orders:
 session=order['session'];block=order['block']
 for K in ([1,64] if session==0 else [64,1]):
  for mode in (['plan-cold','warm'] if session==0 else ['warm','plan-cold']):
   for position,a in enumerate(order['algorithm_order']):
    expected_rows.append((session,block,8192,K,mode,a,position))
for i,(trial,expected_row) in enumerate(zip(trials,expected_rows)):
 assert trial['trial_id']==i
 assert tuple(trial[k] for k in ['session','block','n','K','mode','algorithm','order_position'])==expected_row
 K=trial['K'];warm=trial['mode']=='warm'
 assert trial['fixture_H']==K and trial['independent_fixture'] is True
 assert trial['fixture_pool_sha256']==poolindex[8192]['sha256']
 assert trial['useful_seed_hex']=='243F6A8885A308D3'
 assert trial['warmup_seed_hex']==('243F6A8885A308D3' if warm else None)
 assert trial['warmup_cases']==([f'dense_{j}' for j in range(4)] if warm else [])
 assert trial['useful_case_sequence']==[f'dense_{j%8}' for j in range(K)]
 assert len(set((trial['session'],trial['block'],trial['n'],trial['K'],trial['mode'],trial['algorithm']) for trial in trials))==768
result['expanded_manifest_exact_nesting_cases_seeds_H_and_ownership']='PASS'
result['counts']={'batches':len(trials),'useful_calls':sum(len(t['useful_case_sequence']) for t in trials),'discarded_warmup_calls':sum(len(t['warmup_cases']) for t in trials),'nested_warm_intervals':sum(t['mode']=='warm' for t in trials)}
assert result['counts']=={'batches':768,'useful_calls':24960,'discarded_warmup_calls':1536,'nested_warm_intervals':384}
counts=Counter((t['K'],t['mode'],t['algorithm']) for t in trials);assert len(counts)==16 and set(counts.values())=={48}
result['per_condition_algorithm_paired_observations']=48
result['no_ntt_or_generator_or_oracle_execution']=True
result['no_performance_measurements']=True
(OUT/'V2_INDEPENDENT_DELTA_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
