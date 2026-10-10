import os
import sys
import json
import subprocess
from pathlib import Path
RESULT=[]
for n,d in [(4096,1),(262144,3)]:
    for method in ['scipy','phase8','generated','hand']:
        x=subprocess.run([sys.executable,str(Path(__file__).parent/'isolated_cold.py'),
                         '--n',str(n),'--degree',str(d),'--method',method],
                         env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),
                         capture_output=True,text=True,check=True)
        obj=json.loads(x.stdout.strip().splitlines()[-1]);RESULT.append(obj)
        print(json.dumps(obj),flush=True)
    sample=RESULT[-4:]
    assert max(a['checksum'] for a in sample)-min(a['checksum'] for a in sample)<1e-8
path=Path(__file__).parent/'isolated_cold_results.json'
path.write_text(json.dumps({'description':'Each implementation started in a separate Python interpreter; all native compilation, initial transforms and 48 outputs charged.', 'results':RESULT},indent=2)+'\n')
print('saved',path)
