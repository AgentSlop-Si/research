"""Restore publicly included originals exactly; never run scientific programs."""
from pathlib import Path
import importlib.util, json, sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('packaging_verifier',ROOT/'verify_package.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def restore(destination):
 v.verify(ROOT)
 dest=Path(destination).resolve()
 if dest.exists():raise ValueError('Restoration destination must be new')
 ledger=json.loads((ROOT/'RESTORATION_LEDGER.json').read_text())
 originals=[]
 for row in ledger['files']:
  raw=v.decode(v.safe(ROOT,row['public_path']).read_bytes(),row['representation'])
  if v.info(raw)!={'bytes':row['restored_bytes'],'sha256':row['restored_sha256']}:raise ValueError('Original identity mismatch')
  originals.append((row,raw))
 dest.mkdir(parents=True)
 for row,raw in originals:
  out=v.safe(dest,row['logical_path']);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
  if out.read_bytes()!=raw:raise ValueError('Restoration write mismatch')
 return {'status':'PASS','original_files_restored':len(originals),'private_administrative_omissions_not_restored':True,'scientific_programs_executed':False}
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python3 -I restore_sources.py NEW_DIRECTORY')
 print(json.dumps(restore(sys.argv[1]),indent=2))
