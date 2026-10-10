#!/usr/bin/env python3
import hashlib,json,sys,zipfile
from pathlib import Path
r=Path(__file__).resolve().parent
results=[]
for name in ['ACFF_THEORY.md','HERO0_PHASE7.zip']:
    a=r/'source/new'/name;b=r/'source/prior'/name;x=a.read_bytes();y=b.read_bytes()
    assert x==y
    row={'name':name,'byte_identical':True,'size_bytes':len(x),'sha256':hashlib.sha256(x).hexdigest()}
    if name.endswith('.zip'):
        with zipfile.ZipFile(a) as za,zipfile.ZipFile(b) as zb:
            ma={i.filename:hashlib.sha256(za.read(i)).hexdigest() for i in za.infolist() if not i.is_dir()}
            mb={i.filename:hashlib.sha256(zb.read(i)).hexdigest() for i in zb.infolist() if not i.is_dir()}
            assert ma==mb
            row.update(member_count=len(ma),member_content_identical=True,members=ma)
    results.append(row)
out={'status':'PASS','changed_claims':False,'source_code_executed':False,'files':results}
p=Path(sys.argv[1]) if len(sys.argv)>1 else r/'COMPARISON_RESULTS.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
