"""Restore exact selected source trees; does not execute scientific code."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode=True
from verify_package import verify, decode, info, path, require

def restore(root,destination):
    root=Path(root).resolve(); destination=Path(destination).resolve()
    require(not destination.exists(),'Output directory must not already exist')
    verify(root)
    files=json.loads((root/'COPY_BINDINGS.json').read_text())['files']
    destination.mkdir(parents=True)
    for row in files:
        data=decode((root/row['public_path']).read_bytes(),row['representation'])
        require(info(data)=={'bytes':row['source_bytes'],'sha256':row['source_sha256']},'Decoded source mismatch')
        output=path(destination,row['logical_path']); output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('xb') as f: f.write(data)
        require(output.read_bytes()==data,'Restored source write mismatch')
    return {'status':'PASS','source_files_restored':len(files),'scientific_programs_executed':False}

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: python restore_sources.py OUTPUT_DIRECTORY')
    print(json.dumps(restore(Path(__file__).resolve().parent,sys.argv[1]),indent=2))
