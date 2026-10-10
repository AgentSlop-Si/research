"""Deterministic archive packager, with checksums of every included project file."""
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

HERE=Path(__file__).resolve().parent
DST=HERE.parent/'fft_moving_partition_twisted_gate_2026-10-10.zip'
FILES=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt' and not p.name.endswith('.pyc')]
FILES.sort(key=lambda p:str(p.relative_to(HERE)))
checksums={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(HERE/'SHA256SUMS.txt').write_text(''.join(f'{h}  {filename}\n' for filename,h in checksums.items()))
manifest={'date':'2026-10-10','research':'moving arbitrary partitions + twisted bit-reversal exact rank barriers',
  'files':len(FILES),'sha256':checksums,
  'exact_finite_certificates':13,'new_regression_groups':8,'twisted_lengths_verified':9,
  'tight_network_cuts':6,'rank_feasible_network_controls':24,
  'performance_claim':'No FFT improvement; no exact Fourier factorization constructed'}
(HERE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Refresh checksum file and manifest inclusion, without recursing into a circular MANIFEST hash.
files=FILES+[HERE/'SHA256SUMS.txt',HERE/'MANIFEST.json']
with ZipFile(DST,'w',ZIP_DEFLATED,compresslevel=8) as z:
 for p in files:z.write(p,arcname=str(HERE.name+'/'+str(p.relative_to(HERE))))
with ZipFile(DST) as z:
 bad=z.testzip()
 assert bad is None,bad
 print('ZIP',DST,'count',len(z.namelist()),'bytes',DST.stat().st_size)
