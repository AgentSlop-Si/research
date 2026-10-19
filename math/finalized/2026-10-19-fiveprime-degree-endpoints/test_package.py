#!/usr/bin/env python3
"""Reproducible adversarial export controls in temporary copies only."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
BASE=Path(__file__).resolve().parent
def write(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def reseal(root):
    rows=[{'path':str(p.relative_to(root)),'bytes':len(p.read_bytes()),'sha256':digest(p)}
          for p in sorted(root.rglob('*')) if p.is_file() and str(p.relative_to(root)) not in ['MANIFEST.json','SEAL.json']]
    write(root/'MANIFEST.json',{'scope':'Exact exported endpoint proof and independent review; no native state','files':rows})
    write(root/'SEAL.json',{'manifest_sha256':digest(root/'MANIFEST.json'),'manifest_entries':len(rows),
                          'source_ledger_sha256':digest(root/'SOURCE_LEDGER.json'),
                          'final_acceptance_sha256':digest(root/'FINAL_ACCEPTANCE.json')})
def change(root,name,key,value):
    p=root/name;obj=json.loads(p.read_text());obj[key]=value;write(p,obj)
def invoke(root):
    return subprocess.run([sys.executable,str(root/'verify_package.py')],capture_output=True,
                          env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
def main():
    good=invoke(BASE);assert good.returncode==0,good.stderr.decode()
    actions=[
      ('missing_exact_report',lambda r:(r/'candidate/REPORT.md').unlink()),
      ('corrupted_exact_report',lambda r:(r/'candidate/REPORT.md').write_text((r/'candidate/REPORT.md').read_text()+'\nAltered proof.\n')),
      ('full_classification_overclaim',lambda r:change(r,'CLAIM_SCOPE.json','full_classification_claim',True)),
      ('owner_closure',lambda r:change(r,'OWNER_DISPOSITIONS.json','status','CLOSED')),
      ('priority_change',lambda r:change(r,'OWNER_DISPOSITIONS.json','priority',43)),
      ('score_change',lambda r:change(r,'OWNER_DISPOSITIONS.json','score_change',True)),
      ('false_complete_provenance_replay',lambda r:change(r,'SCIENTIFIC_REPLAY.json','complete_original_provenance_replayed',True)),
      ('source_ledger_drift',lambda r:change(r,'SOURCE_LEDGER.json','purpose','Changed provenance description')),
      ('undisclosed_omitted_binding_reinsertion',lambda r:(r/'candidate/SOURCE_BINDINGS.json').write_text('[]\n')),
      ('private_native_file_injection',lambda r:(r/'NATIVE_CELLDATA.json').write_text('{}\n'))]
    results=[]
    for label,mutate in actions:
        with tempfile.TemporaryDirectory(prefix='endpoint-package-negative-') as temp:
            copy=Path(temp)/'public';shutil.copytree(BASE,copy)
            mutate(copy);reseal(copy)
            run=invoke(copy);assert run.returncode!=0,label
            results.append({'name':label,'top_manifest_and_seal_recomputed':True,'rejected':True})
    print(json.dumps({'status':'PASS','positive_package_check_passed':True,'negative_controls':results,
                      'original_export_unchanged':True,'external_writes':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
