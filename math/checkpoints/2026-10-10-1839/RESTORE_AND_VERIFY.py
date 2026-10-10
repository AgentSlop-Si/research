#!/usr/bin/env python3
"""Restore verified repository-export source bytes; never execute or import those sources."""
import argparse, gzip, hashlib, json, os
from pathlib import Path, PurePosixPath

def safe_relative(value):
    if not isinstance(value,str) or not value or '\\' in value or ':' in value or '\x00' in value:
        raise ValueError('Unsafe path')
    p=PurePosixPath(value)
    if p.is_absolute() or any(x in ('','.','..') for x in value.split('/')):
        raise ValueError('Unsafe path: '+value)
    return p

def digest(data):return hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--destination', help='New, nonexistent directory for exact source reconstruction')
    ap.add_argument('--verify-only', action='store_true', help='Check all reconstructed bytes without writing them')
    args=ap.parse_args()
    if bool(args.destination)==bool(args.verify_only):ap.error('Choose exactly one of --destination or --verify-only')
    package=Path(__file__).resolve().parent
    manifest=json.loads((package/'SOURCE_MANIFEST.json').read_text())
    destination=None
    if args.destination:
        destination=Path(args.destination)
        if destination.exists() or destination.is_symlink():raise ValueError('Destination must not exist')
        destination.mkdir(parents=True,exist_ok=False)
        destination=destination.resolve()
    seen=set();total=0
    for item in manifest['files']:
        source=safe_relative(item['source_path']);storage=safe_relative(item['storage_path'])
        if str(source) in seen:raise ValueError('Duplicate source path')
        seen.add(str(source))
        packed=package.joinpath(*storage.parts)
        if packed.is_symlink() or not packed.resolve().is_relative_to(package):raise ValueError('Unsafe stored member')
        data=packed.read_bytes()
        if digest(data)!=item['stored_sha256'] or len(data)!=item['stored_bytes']:raise ValueError('Stored data mismatch')
        if item['restoration']=='gzip_decompress':data=gzip.decompress(data)
        elif item['restoration']!='copy':raise ValueError('Unknown restoration method')
        if digest(data)!=item['source_sha256'] or len(data)!=item['source_bytes']:raise ValueError('Restored data mismatch')
        if destination is not None:
            target=destination.joinpath(*source.parts)
            target.parent.mkdir(parents=True,exist_ok=True)
            if not target.parent.resolve().is_relative_to(destination):raise ValueError('Unsafe destination')
            with target.open('xb') as f:f.write(data)
            os.chmod(target,0o644)
            if digest(target.read_bytes())!=item['source_sha256']:raise ValueError('Written bytes mismatch')
        total+=len(data)
    if len(seen)!=manifest['source_files'] or total!=manifest['logical_source_bytes']:raise ValueError('Manifest count mismatch')
    print(json.dumps({'status':'PASS','source_files':len(seen),'restored_source_bytes':total,'research_programs_executed_or_imported':False,'restored':destination is not None},indent=2))
if __name__=='__main__':main()
