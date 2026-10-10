"""Safely materialize source data for the independent audit. Never executes it."""
from pathlib import Path, PurePosixPath
import hashlib, stat, zipfile
BASE=Path(__file__).resolve().parent
archive=BASE/'original/fft_hero1_phase14_20261010.zip'
assert archive.stat().st_size==9352867
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='2f09f244ad60479aa4e61320ad9f6584c3ae08e3e18c447793583045a7940f04'
target=BASE/'extracted'
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert sum(x.file_size for x in z.infolist())==9842778
    for x in z.infolist():
        p=PurePosixPath(x.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in x.filename
        assert not (x.flag_bits&1) and not stat.S_ISLNK(x.external_attr>>16)
        if x.is_dir(): continue
        assert p.parts[0]=='fft_hero1_phase14'
        out=target/Path(*p.parts)
        out.parent.mkdir(parents=True,exist_ok=True)
        data=z.read(x)
        if out.exists(): assert out.read_bytes()==data, f'Refusing to overwrite changed file: {out}'
        else: out.write_bytes(data)
print('Verified source bytes materialized for static integrity reads only; no uploaded code executed.')
