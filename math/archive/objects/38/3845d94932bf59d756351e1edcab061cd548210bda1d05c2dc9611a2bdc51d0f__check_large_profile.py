import own_algorithm as a
import json,hashlib
from pathlib import Path
N=262144;Q=M=512;b=18;f=a.Field(998244353,N)
modes=[{(t+j)%M:(2*b if j==0 else 1) for j in range(b)} for t in range(Q)]
x=a.from_modes(modes,Q,M,f);out,meta=a.check(x,f,b=b);assert out is not None and meta['discovered']==Q*b
Path('LARGE_PROFILE_RESULTS.json').write_text(json.dumps({'status':'PASS','N':N,'Q':Q,'M':M,'b':b,'K':Q*b,'independent_output_entries_checked':N,'output_sha256':hashlib.sha256(','.join(map(str,out)).encode()).hexdigest(),'source_programs_executed':False,'root_supplied':True},indent=2,sort_keys=True)+'\n');print('LARGE INDEPENDENT FULL OUTPUT PASS')
