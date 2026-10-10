"""Rebuild a reproducible source/receipt ZIP after tests pass."""
from __future__ import annotations
from pathlib import Path
import zipfile,hashlib,subprocess,tempfile,sys,json

DIR=Path(__file__).resolve().parent
ZIP=DIR.parent/'fft_hero1_phase18_20261010.zip'

def files():
    return sorted((f for f in DIR.rglob('*') if f.is_file()
                   and '__pycache__' not in f.parts and f.name!='MANIFEST.sha256'),
                  key=lambda f:str(f.relative_to(DIR)))

def run():
    allfiles=files()
    lines=[]
    for f in allfiles:
        sha=hashlib.sha256(f.read_bytes()).hexdigest()
        lines.append(f'{sha}  {f.relative_to(DIR)}')
    (DIR/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for file in sorted(files()+[DIR/'MANIFEST.sha256']):
            z.write(file,arcname=f'{DIR.name}/{file.relative_to(DIR)}')
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None
        with tempfile.TemporaryDirectory(prefix='phase18_clean_') as tmp:
            z.extractall(tmp)
            cwd=Path(tmp)/DIR.name
            result=subprocess.run(['sha256sum','-c','MANIFEST.sha256'],cwd=cwd,
                                  capture_output=True,text=True)
            assert result.returncode==0,(result.stdout,result.stderr)
            t=subprocess.run([sys.executable,'-m','unittest','-q','test_phase18'],cwd=cwd,
                             capture_output=True,text=True)
            assert t.returncode==0,t.stderr
            test_result=t.stderr.splitlines()[-3:]
    out={'archive':str(ZIP),'size_bytes':ZIP.stat().st_size,
         'sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),
         'files':len(files())+1,'source_hashes_all_ok':True,
         'clean_extraction_phase18_tests_ok':True,'clean_test_receipt':test_result}
    print(json.dumps(out,indent=2))
    return out
if __name__=='__main__':run()
