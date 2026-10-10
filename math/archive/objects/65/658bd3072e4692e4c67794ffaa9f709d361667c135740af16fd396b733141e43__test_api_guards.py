#!/usr/bin/env python3
"""Fast post-change safety/ownership tests without paying calibration costs."""
import json
from pathlib import Path
import numpy as np
import adaptive_fft as af

def error(f,kind):
    try:f()
    except kind:return
    raise AssertionError('Expected '+str(kind))

n=4096;x=np.zeros(n,np.uint8)
p=af.BinaryFFTPlan(n,method='codelet8')
assert p.calibration_count==0 and p.calibration['elapsed_ms']==0
assert np.all(p.execute(x)==0)
random_x=np.random.default_rng(917).integers(0,2,n,dtype=np.uint8)
np.testing.assert_allclose(p.execute(random_x),np.fft.fft(random_x),atol=2e-9,rtol=2e-11)
assert p.calibration_count==0
unaligned=np.ndarray((n,),np.complex128,buffer=bytearray(n*16+1),offset=1)
assert unaligned.flags.c_contiguous and not unaligned.flags.aligned
error(lambda:p.execute(x,out=unaligned),ValueError)
for invalid in [4096.,True,8,4095]:error(lambda v=invalid:af.get_plan(v),ValueError)
for dt in [np.float64,np.int64,np.float32]:error(lambda d=dt:p.execute(x.astype(d)),TypeError)
out=np.full(n,4+3j,np.complex128);bad=x.copy();bad[-1]=255
error(lambda:p.execute(bad,out=out),ValueError);assert np.all(out==4+3j)
error(lambda:p.execute(np.zeros(8192,np.uint8)[::2]),ValueError)
error(lambda:p.execute(out.view(np.uint8)[:n],out=out),ValueError)
saved=p.execute(x);p.execute(np.ones(n,np.uint8));assert np.all(saved==0)
assert p.execute(x,out=out) is out
p.close();p.close();error(lambda:p.execute(x),RuntimeError)
# Length validation must occur even when a same-length cache entry exists.
cp=af.get_plan(16)
error(lambda:af.get_plan(16.),ValueError)
assert af.get_plan(16) is cp
oldcount=cp.calibration_count
for _ in range(20):cp.execute(np.ones(16,np.uint8))
assert cp.calibration_count==oldcount
cp.close();replacement=af.get_plan(16);assert replacement is not cp
assert not replacement.closed
af.clear_plan_cache();assert not replacement.closed;replacement.close()
result={'passed':True,'checks':['aligned output required','integer length validated before cache','no implicit dtype conversion','binary validation before output writes','reject noncontiguous input and overlapping buffers','outputs independently owned','out buffer reuse','double close safe','closed plan rejection','closed cached plan replaced','clear cache preserves held references','explicit fixed method skips calibration','normal execution never retunes']}
Path(__file__).with_name('api_guard_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
