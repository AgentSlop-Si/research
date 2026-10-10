"""Create deterministic research ZIP and SHA-256 manifest, then verify extraction."""
from pathlib import Path
import hashlib,json,zipfile,tempfile,subprocess,sys
BASE=Path(__file__).resolve().parent
OUT=BASE.parent/'fft_boolean_orbit_recovery_research_2026-10-09.zip'
FILES=[
 'README.md','RESEARCH.md','NEXT_GATE.md','orbit_recovery.py',
 'cyclotomic_interpolation.py','independent_modular_certificate.py',
 'run_audit.py','audit_results.json','modular_certificate.json',
 'tests/test_orbit.py','package.py'
]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={f:sha(BASE/f) for f in FILES}
(BASE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for f in FILES+['MANIFEST.json']:
  z.write(BASE/f,arcname=f)
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='fft_orbit_fresh_') as td:
  z.extractall(td)
  root=Path(td)
  checked=json.loads((root/'MANIFEST.json').read_text())
  assert checked==manifest
  assert all(sha(root/f)==h for f,h in checked.items())
  r=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=td,capture_output=True,text=True)
  assert r.returncode==0,r.stdout+'\n'+r.stderr
  r2=subprocess.run([sys.executable,'run_audit.py'],cwd=td,capture_output=True,text=True)
  assert r2.returncode==0,r2.stdout+r2.stderr
  r3=subprocess.run([sys.executable,'independent_modular_certificate.py'],cwd=td,capture_output=True,text=True)
  assert r3.returncode==0,r3.stdout+r3.stderr
  print('Fresh extraction tests:',r.stderr.splitlines()[-1],flush=True)
  print('Fresh exact audits: PASS, PASS',flush=True)
  print('ZIP member checksums:',len(checked),'matched',flush=True)
print('Archive size:',OUT.stat().st_size,'bytes')
print('SHA256:',sha(OUT))
print('Path:',OUT)
