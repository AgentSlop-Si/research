"""Generate SHA manifest and a reproducible distributable ZIP (no pycache)."""
from pathlib import Path
import hashlib,zipfile,json
ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT.parent/'fft_dual_support_onion_gate_2026-10-09.zip'
files=sorted((f for f in ROOT.iterdir() if f.is_file() and f.name!='SHA256SUMS.txt'), key=lambda p:p.name)
manifest=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files)
(ROOT/'SHA256SUMS.txt').write_text(manifest)
files.append(ROOT/'SHA256SUMS.txt')
with zipfile.ZipFile(OUTPUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
    for p in files:z.write(p,arcname=f'{ROOT.name}/{p.name}')
with zipfile.ZipFile(OUTPUT) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
print(json.dumps({'archive':str(OUTPUT),'files':len(files),
                  'archive_bytes':OUTPUT.stat().st_size,
                  'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest()},indent=2))
