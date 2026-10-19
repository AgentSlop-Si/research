#!/usr/bin/env python3
"""Documentary integrity only; no scientific program is imported or executed."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())
def main():
 seal=read('SEAL.json');allow=read('PRESERVATION_ALLOWLIST.json');manifest=read('MANIFEST.json')
 for n,k in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITIONS.json','owner_dispositions_sha256')]:assert sha(ROOT/n)==seal[k],n
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
 assert not any(p.is_symlink() for p in ROOT.rglob('*'))
 assert actual==set(allow['files']),'allowlist file set'
 assert {e['path'] for e in manifest['files']}==actual-{'MANIFEST.json','SEAL.json'}
 for e in manifest['files']:
  p=ROOT/e['path'];assert sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],e['path']
 binds=read('COPY_BINDINGS.json')
 for e in binds['files']:
  p=ROOT/e['public_path'];assert e['transformation']=='EXACT_COPY'
  assert sha(p)==e['public_sha256']==e['source_sha256']
  assert p.stat().st_size==e['public_bytes']==e['source_bytes']
 assert len({e['public_path'] for e in binds['files']})==len(binds['files'])
 for s in binds['source_sets']:
  p=ROOT/s['public_prefix']/s['manifest'];assert sha(p)==s['manifest_sha256']
  es=json.loads(p.read_text()) if p.suffix=='.json' else {x.split(None,1)[1].removeprefix('./'):x.split(None,1)[0] for x in p.read_text().splitlines() if x}
  assert len(es)==s['payload_entries']
  for n,h in es.items():assert sha(p.parent/n)==h,n
 a=read('FINAL_ACCEPTANCE.json')['results'];assert set(a)=={'chirp','rectangle'}
 expected={'chirp':'a3c758d9016ac5bbc7c78d1133e135d7714a81adf14e8dbc541d18ed7aab7b38','rectangle':'ef02706ac4265a67e5ff56f7f4d7bcfe41c987caf17e3cb0885f896d84bff1d5'}
 for k,e in a.items():
  assert e['independently_accepted'] and not e['owner_closure']
  assert e['accepted_proof_sha256']==expected[k]
  for f in ['accepted_proof','review','candidate_manifest','review_manifest']:assert sha(ROOT/e[f+'_path'])==e[f+'_sha256']
 v=read(a['rectangle']['verdict_path']);assert v['verdict']=='ACCEPT' and v['candidate_report_sha256']==expected['rectangle']
 assert sha(ROOT/a['rectangle']['verdict_path'])==a['rectangle']['verdict_sha256']
 assert expected['chirp'] in (ROOT/a['chirp']['review_path']).read_text()
 assert 'Accept the explicit cutoff' in (ROOT/a['chirp']['review_path']).read_text()
 d=read('OWNER_DISPOSITIONS.json');assert d['owner_closures']==d['priority_changes']==d['canonical_claim_count_changes']==0
 for owner,pr in [('M-CHIRP-LOWER',34),('M-RECTANGLE-TILING',42)]:
  e=d['owners'][owner];assert e['status']=='TO RESEARCH' and e['priority']==pr and not e['owner_closure']
 neg=d['owners']['M-CHIRP-LOWER']['preserved_negative_epsilon'];assert not neg['accepted_result_reopened'] and neg['independent_report_sha256']=='d89108b404074f6b3d995407b61b30acb57aa07069e736b29bf53025292d3c4b'
 assert not read('OMISSIONS.json')['omitted_manifest_declared_source_files']
 assert read('PROJECTION_DISCLOSURE.json')['privacy_projected_files']==0
 assert not seal['scientific_reruns_during_packaging'] and not seal['external_writes'] and not seal['prior_packets_modified']
 bad=re.compile(r'https?://docs\.google\.com/spreadsheets|libfile_[A-Za-z0-9]+|file_000000[0-9a-f]+|Bearer\s+[A-Za-z0-9_.-]+',re.I)
 for p in ROOT.rglob('*'):
  if p.is_file() and p.name!='verify_package.py':assert not bad.search(p.read_text()),str(p)
 t=(ROOT/'README.md').read_text()
 for x in ['2^(2^534)','both real signs','4820k-5','62/957','124/2749461','5/5746','3757','not necessary','priority 34','priority 42']:assert x in t,x
 print(json.dumps(dict(status='PASS',public_files=len(actual),exact_copy_bindings=len(binds['files']),frozen_source_sets=len(binds['source_sets']),independent_scientific_acceptances=2,owner_closures=0,privacy_projections=0,scientific_programs_executed=False,external_writes=False),indent=2))
if __name__=='__main__':main()
