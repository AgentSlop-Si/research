"""Build SHA-256 manifest and reproducible ZIP for the joint-orbit experiment."""
import hashlib
import json
from pathlib import Path
import zipfile

DIR=Path(__file__).resolve().parent
DEST=DIR.parent/'fft_joint_galois_stability_research_2026-10-09.zip'
FILES=[
    'README.md','RESEARCH.md','RESULTS_SUMMARY.md','NEXT_GATE.md',
    'orbit_stability.py','modular_audit.py','experiment.py','precision_audit.py',
    'joint_measurement_audit.py','tests/test_stability.py',
    'audit_results.json','precision_results.json','joint_measurement_results.json',
    'run_output.txt','precision_output.txt','joint_output.txt','tests_output.txt',
    'package.py'
]

def run():
    hashes={}
    for name in FILES:
        p=DIR/name
        if not p.is_file():
            raise FileNotFoundError(p)
        hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    manifest={'title':'Joint Galois orbit stability audit','date':'2026-10-09','status':'restricted stability/precision theorem; NOT a new FFT algorithm','sha256':hashes}
    (DIR/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in FILES+['MANIFEST.json']:
            z.write(DIR/name,arcname='fft_joint_orbit_stability/'+name)
    with zipfile.ZipFile(DEST) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(FILES)+1
        for name,digest in hashes.items():
            assert hashlib.sha256(z.read('fft_joint_orbit_stability/'+name)).hexdigest()==digest
    print('ZIP:',DEST)
    print('FILES:',len(FILES)+1)
    print('BYTES:',DEST.stat().st_size)
    print('SHA256:',hashlib.sha256(DEST.read_bytes()).hexdigest())

if __name__=='__main__':run()
