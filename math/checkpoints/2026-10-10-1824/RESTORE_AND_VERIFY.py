#!/usr/bin/env python3
"""Verify preserved bytes and optionally restore original source names; execute no research code."""
import argparse, hashlib, json, pathlib, gzip
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def safe(root, rel):
    path=pathlib.PurePosixPath(rel)
    if path.is_absolute() or '..' in path.parts or not path.parts: raise ValueError('Unsafe relative path')
    dest=root.joinpath(*path.parts)
    if dest.is_symlink() or not dest.resolve().is_relative_to(root.resolve()): raise ValueError('Unsafe destination')
    return dest
def source_bytes(base, row):
    src=safe(base,row['object_path']);data=src.read_bytes()
    if row.get('object_encoding')=='gzip':
        assert len(data)==row['stored_bytes'] and hashlib.sha256(data).hexdigest()==row['stored_sha256']
        data=gzip.decompress(data)
    elif row.get('object_encoding') not in (None, 'identity'):
        raise ValueError('Unsupported object encoding')
    assert len(data)==row['source_bytes'] and hashlib.sha256(data).hexdigest()==row['source_sha256']
    return data
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--restore-to',type=pathlib.Path,help='New nonexistent directory for original source paths')
    a=p.parse_args();base=pathlib.Path(__file__).resolve().parent
    sums=base/'SHA256SUMS'
    if sums.exists():
        for line in sums.read_text().splitlines():
            h,name=line.split(None,1);assert sha(safe(base,name.strip()))==h,name
    manifest=json.loads((base/'SOURCE_MANIFEST.json').read_text())
    for row in manifest['files']:
        source_bytes(base,row)
    if a.restore_to:
        if a.restore_to.exists():raise ValueError('Refusing to overwrite an existing destination')
        a.restore_to.mkdir(parents=True)
        for row in manifest['files']:
            dst=safe(a.restore_to,row['source_path']);dst.parent.mkdir(parents=True,exist_ok=True)
            with dst.open('xb') as f:f.write(source_bytes(base,row))
            assert sha(dst)==row['source_sha256']
    print(json.dumps({'status':'PASS','source_names':manifest['source_files'],'unique_content_objects':manifest['unique_content_objects'],'research_programs_executed':False,'restored':bool(a.restore_to)}))
if __name__=='__main__':main()
