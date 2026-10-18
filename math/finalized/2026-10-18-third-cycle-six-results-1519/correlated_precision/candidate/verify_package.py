"""Verify the frozen package and the copied accepted-source pins."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for row in manifest['files']:
        assert digest(ROOT/row['path'])==row['sha256'], row['path']
    pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
    checked=[]
    for row in pins:
        assert digest(ROOT/row['local'])==row['sha256'], row['local']
        source=Path(row['source'])
        available=source.is_file()
        if available: assert digest(source)==row['sha256'], str(source)
        checked.append({'local':row['local'],'original_available':available})
    result={'status':'PASS','manifest_entries':len(manifest['files']),
            'source_pins':checked,'manifest_sha256':digest(ROOT/'MANIFEST.json')}
    (ROOT/'PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
