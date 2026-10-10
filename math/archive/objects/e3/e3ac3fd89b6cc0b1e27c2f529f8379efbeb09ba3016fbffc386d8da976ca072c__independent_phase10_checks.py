import sys,json,hashlib,random
from pathlib import Path
import numpy as np
from unittest.mock import patch
root=Path('two_research_updates_2247/unpacked/fft_phase10_aot')
hashes=json.loads((root/'SHA256SUMS.json').read_text())['files']
for fn,sha in hashes.items():
    assert hashlib.sha256((root/fn).read_bytes()).hexdigest()==sha,fn
sys.path.insert(0,str(root))
from algebra_fft import AlgebraFFT
from two_edit_engine import prepare_two

def conv(a,b):
    n=len(a)
    return [sum(int(a[j])*int(b[(i-j)%n]) for j in range(n)) for i in range(n)]
def expr(a,b,c,d):
    parts=[conv(conv(a,a),b),conv(a,b),conv(b,b),conv(c,d)]
    return np.asarray([sum(v[i] for v in parts) for i in range(len(a))],dtype=np.int64)
rng=random.Random(202610082250)
cases=0;maxerr=0.
with patch('ctypes.CDLL',side_effect=AssertionError('Shipped native code must not load')):
    for n in [2,3,7,16,31,64]:
        for trial in range(20):
            arrays=[[rng.randrange(-4,5) for _ in range(n)] for _ in range(4)]
            eng=AlgebraFFT(n)
            a,b,c,d=[eng.signal(x) for x in arrays]
            node=eng.add(eng.mul(a,a,b),eng.mul(a,b),eng.mul(b,b),eng.mul(c,d))
            plan=prepare_two(eng,node,a,b)
            pa,pb=rng.randrange(n),rng.randrange(n)
            if trial%3==0:pb=pa
            da,db=rng.randrange(-3,4),rng.randrange(-3,4)
            aa,bb=arrays[0].copy(),arrays[1].copy()
            aa[pa]+=da;bb[pb]+=db
            truth=expr(aa,bb,*arrays[2:])
            got=plan.update(pa,da,pb,db,backend='numpy')
            err=float(np.max(np.abs(got-truth)))
            maxerr=max(maxerr,err)
            assert err<1e-8,(n,trial,err)
            qs=[0,n-1,0,n//2]
            part=plan.update(pa,da,pb,db,indices=qs,backend='numpy')
            assert np.max(np.abs(part-truth[qs]))<1e-8
            cases+=1
    eng=AlgebraFFT(4)
    a=eng.signal([1,0,0,0])
    bad=eng.add(eng.scale(a,2**53),a,eng.scale(a,-2**53))
    assert bad==eng.zero
    collapse=eng.evaluate_time(bad).tolist()
print(json.dumps(dict(hashes_verified=len(hashes),two_edit_numpy_cases=cases,partial_checks=cases,max_absolute_error=maxerr,
    cancellation_expression='(2^53)*A + A - (2^53)*A',exact_expected=[1,0,0,0],actual=collapse,shipped_native_code_loaded=False),indent=2))
