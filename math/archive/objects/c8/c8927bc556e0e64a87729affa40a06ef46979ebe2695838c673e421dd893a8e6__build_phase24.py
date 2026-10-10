"""Deterministic manifest and ZIP packaging for Phase24. No external deps."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'fft_hero1_phase24_20261010.zip'

def valid(path):
    if not path.is_file() or '__pycache__' in path.parts:return False
    if path.name=='MANIFEST.sha256':return False
    if path.suffix in ('.pyc','.pyo'):return False
    return True

files=sorted(x for x in ROOT.rglob('*') if valid(x))
lines=[]
for path in files:
    rel=path.relative_to(ROOT)
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f'{sha}  {rel.as_posix()}')
(ROOT/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
with ZipFile(OUT,'w',ZIP_DEFLATED,compresslevel=6) as zipout:
    for path in sorted(files+[ROOT/'MANIFEST.sha256']):
        zipout.write(path,arcname=str(Path(ROOT.name)/path.relative_to(ROOT)))
print('archive',OUT,'files',len(files)+1,'bytes',OUT.stat().st_size)
