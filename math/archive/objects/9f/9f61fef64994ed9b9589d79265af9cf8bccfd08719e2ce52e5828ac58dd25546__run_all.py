from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def run(cmd:list[str], log):
    p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log.write('$ '+' '.join(cmd)+'\n'+p.stdout+'\n')
    if p.returncode:
        raise SystemExit(p.returncode)

with (ROOT/'run_all.log').open('w') as log:
    run([sys.executable,'build_results.py'],log)
    run([sys.executable,'-m','unittest','-v','test_checkpoint.py'],log)
    run([sys.executable,'independent_verifier.py'],log)
    # Verify manifest last. The manifest excludes itself and the volatile log.
    manifest=ROOT/'MANIFEST.sha256'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            if not line.strip():continue
            want,name=line.split('  ',1)
            got=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
            if got!=want:
                raise SystemExit(f'hash mismatch: {name}')
        log.write('manifest: OK\n')
print((ROOT/'run_all.log').read_text())
