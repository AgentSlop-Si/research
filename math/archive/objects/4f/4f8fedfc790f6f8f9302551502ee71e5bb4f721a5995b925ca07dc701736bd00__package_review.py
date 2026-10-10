"""Reviewer packaging and independent replay; never imports uploaded programs."""
from pathlib import Path
import hashlib,json,zipfile,tempfile,shutil,subprocess,os,ast,sys
P=Path(__file__).parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=[]
for d in ['research_round_0118/review_all_subsets_rigidity','research_round_0118/review_bruhat_v23']:
 d=Path(d);m=d/'SEALED_MANIFEST.json';data=json.loads(m.read_text());assert H(m)==(d/'SEALED_MANIFEST.sha256').read_text().split()[0]
 for name,h in data['files'].items():assert H(d/name)==h,(d,name)
 old.append(dict(path=str(d),manifest_sha256=H(m),files_verified=len(data['files'])))
a=P/'projective_source/ORIGINAL_ARCHIVE.zip'
assert H(a)=='5eac4f25f89289545280f3d6575a1096cf443a52e3237111f66cecc909c92e76'
with zipfile.ZipFile(a) as z:assert z.testzip() is None;assert len(z.infolist())==16
coverage=[]
for d in ['projective_source','tensor_source','outer_source']:
 for f in sorted((P/d).iterdir()):
  if f.suffix=='.zip':continue
  row=dict(path=str(f.relative_to(P)),sha256=H(f),bytes=f.stat().st_size,text_coverage='complete',source_execution=False)
  if f.suffix=='.py':
   tree=ast.parse(f.read_text());row['static_imports']=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))];row['program_acceptance']='Static inspection only; no uploaded implementation execution'
  coverage.append(row)
manifest={line.split()[1]:line.split()[0] for line in (P/'tensor_source/MANIFEST_v19_TEXT_SNAPSHOT.sha256').read_text().splitlines()}
known={row['sha256'] for row in coverage}|{'cf7570b1afd956fded5c5353fb01b0716a2c73c480ebcd64c1f51a8363d9b962'}
missing=[dict(name=name,sha256=h,status='dependency-pending') for name,h in manifest.items() if h not in known]
(P/'SOURCE_COVERAGE.json').write_text(json.dumps(dict(files=coverage,tensor_v24_manifest_missing=missing,proof_acceptance=dict(projective='Accepted fixed-stage Theorems I-IV; inherited Green origin of reference matrix not reconstructed',outer='Accepted for pinned predecessor affine layout by fresh exact reconstruction',tensor='Main source proof pending; narrow odd-prime structural consequences independently established'),novelty='No publication-wide novelty accepted'),indent=2)+'\n')
snapshots=json.load(open('coverage_audit_20261010/CURRENT_VERSION_TEXT_SNAPSHOTS.json'))
ids={'[private-id]','[private-id]','[private-id]','[private-id]'}
prov=dict(projective=dict(library_file_id='[private-id]',sha256=H(a),original_path='coverage_library_recovery/FFT/FFT_PROJECTIVE_GAUGE_RIGIDITY_2026-10-10.zip',crc='PASS',members=16),complete_text_snapshots=[x for x in snapshots if x['library_file_id'] in ids],prior_review_seals=old,layout_sha256=H(P/'outer_source/AFFINE_LAYOUT.json'),later_mutations_used=False,source_programs_executed=False)
(P/'PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n')
# Replay fresh reviewer code in a separate directory; source code is only copied as inert evidence.
res=[]
with tempfile.TemporaryDirectory(prefix='companion_review_replay_') as td:
 T=Path(td)
 for name in ['projective_source','tensor_source','outer_source']:shutil.copytree(P/name,T/name)
 for name in ['check_projective_independent.py','check_outer_independent.py','check_tensor_independent.py']:shutil.copy2(P/name,T/name)
 for prog,out in [('check_projective_independent.py','PROJECTIVE_INDEPENDENT_RESULTS.json'),('check_outer_independent.py','OUTER_INDEPENDENT_RESULTS.json'),('check_tensor_independent.py','TENSOR_INDEPENDENT_RESULTS.json')]:
  r=subprocess.run([sys.executable,str(T/prog)],env={**os.environ,'OPENBLAS_NUM_THREADS':'1'},capture_output=True,text=True,check=True)
  (P/(prog.removesuffix('.py')+'.log')).write_text(r.stdout+r.stderr)
  assert H(T/out)==H(P/out),out
  res.append(dict(script=prog,output=out,byte_identical=True,sha256=H(P/out)))
(P/'PORTABILITY.json').write_text(json.dumps(dict(status='PASS',replays=res,python=sys.version,numpy_required=True,exact_and_numeric_byte_identical_on_tested_environment=True),indent=2)+'\n')
print('Prior seals intact; source coverage and provenance written; all three isolated replays byte-identical.')
