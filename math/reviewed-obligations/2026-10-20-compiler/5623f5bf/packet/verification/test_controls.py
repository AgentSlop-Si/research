#!/usr/bin/env python3
"""Cold temporary-copy negative controls; no source/compiler execution."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
H = lambda b: hashlib.sha256(b).hexdigest()
def dump(p, value):
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def change(root,name,fn):
    p=root/name; x=read(p); fn(x); dump(p,x)
def reseal(root):
    files=sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                 if p.is_file() and p.relative_to(root).as_posix() not in {'MANIFEST.json','SEAL.json'})
    rows=[]
    for name in files:
        b=(root/name).read_bytes();rows.append({'path':name,'bytes':len(b),'sha256':H(b)})
    dump(root/'MANIFEST.json',rows)
    s=read(root/'SEAL.json');s['manifest_sha256']=H((root/'MANIFEST.json').read_bytes());s['files']=len(rows)
    dump(root/'SEAL.json',s)
def run(root):
    return subprocess.run([sys.executable,'-B',str(root/'verify_packet.py')],capture_output=True,text=True)
def ledger(root,fn):
    change(root,'UNPRICED_LEDGER.json',fn)
def setrow(field,value):
    return lambda x:x['widths'][0].__setitem__(field,value)
def mutate_duplicate_key(root):
    p=root/'UNPRICED_LEDGER.json'
    p.write_text(p.read_text().replace('"pilot_completed": false,','"pilot_completed": false,\n  "pilot_completed": true,',1))
def mutate_symlink(root):
    p=root/'evidence/INDEPENDENT_REVIEW.md';p.unlink();p.symlink_to('../REPORT.md')

CASES=[
 ('zero complete cost',True,lambda r:ledger(r,setrow('complete_program_cost',0))),
 ('false complete cost',True,lambda r:ledger(r,setrow('complete_program_cost',False))),
 ('false completion claim',True,lambda r:ledger(r,lambda x:x.__setitem__('pilot_completed',True))),
 ('completion numeric zero',True,lambda r:ledger(r,lambda x:x.__setitem__('pilot_completed',0))),
 ('changed width',True,lambda r:ledger(r,setrow('width',33))),
 ('boolean width',True,lambda r:ledger(r,setrow('width',True))),
 ('float width',True,lambda r:ledger(r,setrow('width',2.0))),
 ('string width',True,lambda r:ledger(r,setrow('width','2'))),
 ('float priority',True,lambda r:ledger(r,lambda x:x.__setitem__('priority_unchanged',32.0))),
 ('boolean priority',True,lambda r:ledger(r,lambda x:x.__setitem__('priority_unchanged',True))),
 ('closed parent status',True,lambda r:ledger(r,lambda x:x.__setitem__('parent_status_unchanged','DONE'))),
 ('duplicate JSON key',True,mutate_duplicate_key),
 ('nonstandard NaN JSON',True,lambda r:ledger(r,setrow('complete_program_cost',float('nan')))),
 ('changed original report identity',True,lambda r:change(r,'SOURCE_IDENTITIES.json',lambda x:x['selected_sources'][1].__setitem__('sha256','0'*64))),
 ('pre-correction substituted for accepted manifest',True,lambda r:change(r,'SOURCE_IDENTITIES.json',lambda x:x['unrecovered_accepted_bodies'][0].__setitem__('sha256','d42781f8737b83c1e886eb70560128169ae39aa057da7f43325d12bfb868d060'))),
 ('boolean source byte length',True,lambda r:change(r,'SOURCE_IDENTITIES.json',lambda x:x['selected_sources'][0].__setitem__('bytes',True))),
 ('changed projected report',True,lambda r:(r/'REPORT.md').write_bytes((r/'REPORT.md').read_bytes()+b'x')),
 ('changed sealed review',True,lambda r:(r/'evidence/INDEPENDENT_REVIEW.md').write_bytes((r/'evidence/INDEPENDENT_REVIEW.md').read_bytes()+b'x')),
 ('changed verdict completion',True,lambda r:change(r,'VERDICT.json',lambda x:x.__setitem__('pilot_completed',True))),
 ('extra private capture',True,lambda r:(r/'private_capture.json').write_text('{}\n')),
 ('missing nested evidence',True,lambda r:(r/'evidence/FROZEN_PACKET_RESULTS.json').unlink()),
 ('unexpected empty directory',False,lambda r:(r/'extra').mkdir()),
 ('symlink evidence',False,mutate_symlink),
 ('manifest duplicate entry',False,lambda r:change(r,'MANIFEST.json',lambda x:x.append(copy.deepcopy(x[0])))),
 ('manifest traversal path',False,lambda r:change(r,'MANIFEST.json',lambda x:x[0].__setitem__('path','../REPORT.md'))),
 ('manifest boolean byte length',False,lambda r:change(r,'MANIFEST.json',lambda x:x[0].__setitem__('bytes',True))),
 ('seal float file count',False,lambda r:change(r,'SEAL.json',lambda x:x.__setitem__('files',float(x['files'])))),
 ('seal float priority',False,lambda r:change(r,'SEAL.json',lambda x:x.__setitem__('priority',32.0))),
 ('seal false hash',False,lambda r:change(r,'SEAL.json',lambda x:x.__setitem__('manifest_sha256','0'*64))),
 ('nonallowlisted private locator in README',True,lambda r:(r/'README.md').write_text((r/'README.md').read_text()+'\nhttps://docs.google.com/spreadsheets/example\n')),
]

def main():
    with tempfile.TemporaryDirectory(prefix='compiler_public_controls_') as tmp:
        base=Path(tmp)/'baseline';shutil.copytree(ROOT,base)
        baseline=run(base)
        if baseline.returncode!=0:
            raise RuntimeError('baseline failed: '+baseline.stdout+baseline.stderr)
        results=[]
        for i,(name,do_reseal,mutate) in enumerate(CASES):
            r=Path(tmp)/('case_'+str(i));shutil.copytree(ROOT,r)
            mutate(r)
            if do_reseal:reseal(r)
            outcome=run(r)
            results.append({'mutation':name,'resealed':do_reseal,'detected':outcome.returncode!=0})
        result={'schema_version':1,'scope':'PUBLIC_PACKET_CHECKS_ONLY','baseline_passed':True,'all_controls_detected':all(r['detected'] for r in results),'control_count':len(results),'controls':results}
        print(json.dumps(result,indent=2,ensure_ascii=False))
        return 0 if result['all_controls_detected'] else 1
if __name__=='__main__':
    raise SystemExit(main())
