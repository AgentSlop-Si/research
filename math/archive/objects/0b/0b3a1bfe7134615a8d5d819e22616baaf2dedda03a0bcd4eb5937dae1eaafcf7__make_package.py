"""Create integrity-checked, self-contained ZIP from this research folder."""
from pathlib import Path
import hashlib, json, zipfile
b=Path(__file__).resolve().parent
zip_path=b.parent/'fft_parity_affine_depth_no_go_2026-10-10.zip'
manifest={
  'checkpoint_date':'2026-10-10',
  'original_goal':'Sub-N log N exact fresh-input FFT using global sharing',
  'proven_results':['Complex parity-block Fourier rank oracle',
                    'Exact deficient parity-pair count',
                    'GF2-affine semiseparable depth lower bound',
                    'Heterogeneous stage-rank/bit-budget no-go'],
  'testing':'10 new test groups passed; modular corroboration in two primes',
  'prior_checkpoint_SHA256': hashlib.sha256((b/'prior_checkpoint_full.zip').read_bytes()).hexdigest(),
  'caution':'No faster FFT construction and no unrestricted FFT lower bound.'
}
(b/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
files=sorted(p for p in b.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name!='SHA256SUMS.txt')
contents=[f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(b).as_posix()}' for p in files]
(b/'SHA256SUMS.txt').write_text('\n'.join(contents)+'\n')
files.append(b/'SHA256SUMS.txt')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in sorted(files):
        z.write(p,arcname=f'{b.name}/{p.relative_to(b).as_posix()}')
assert zipfile.ZipFile(zip_path).testzip() is None
print('ZIP',zip_path,'files',len(files),'bytes',zip_path.stat().st_size)
