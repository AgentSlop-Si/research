"""Reproducible release package with whole-extract verification."""
from __future__ import annotations
import hashlib,zipfile,tempfile,subprocess,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ZIP=ROOT.parent/'fft_bidirectional_macro_shuffle_research_2026-10-09.zip'
CONTENTS=[
 'README.md','RESEARCH.md','NEXT_GATE.md',
 'exact_scan_macro.py','ordering_dp.py','analytic_certificate.py',
 'reference_ntt.py','unitary_control.py','benchmark.py',
 'run_audit.py','package.py','tests/test_exact_macros.py',
 'benchmark_results.json','audit_results.json',
]

def main():
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in CONTENTS}
    manifest=''.join(f'{sha}  {name}\n' for name,sha in hashes.items())
    (ROOT/'SHA256SUMS.txt').write_text(manifest)
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in CONTENTS+['SHA256SUMS.txt']:
            archive.write(ROOT/name,arcname='fft_bidirectional_macro_research/'+name)
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        with tempfile.TemporaryDirectory(prefix='scan-fft-fresh-') as where:
            archive.extractall(where)
            folder=Path(where)/'fft_bidirectional_macro_research'
            checks=[]
            for name,sha in hashes.items():
                assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==sha,name
                checks.append(name)
            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
            tests=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=folder,env=env,check=True,capture_output=True,text=True)
            audit=subprocess.run([sys.executable,'run_audit.py'],cwd=folder,env=env,check=True,capture_output=True,text=True)
            assert 'Ran 14 tests' in (tests.stdout+tests.stderr)
            assert 'EXACT_AUDIT_OK' in audit.stdout
            print('archive',ZIP)
            print('bytes',ZIP.stat().st_size)
            print('sha256',hashlib.sha256(ZIP.read_bytes()).hexdigest())
            print('zip_crc', 'PASS')
            print('source_sha256', f'{len(checks)}/{len(hashes)} PASS')
            print('fresh_unittest', '14/14 PASS')
            print('fresh_exact_audit', audit.stdout.strip().replace('\n','; '))

if __name__=='__main__':main()
