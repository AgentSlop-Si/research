"""Independent analytic spectral and corner-entry checks; standard library only."""
from fractions import Fraction
from pathlib import Path
import math
import json

out=[]
for n in (8,16,32,64,128):
    c=math.cos(math.pi/(n+1))
    lo,hi=3-2*c,3+2*c
    k=(1/lo+1/(lo+1))/(1/hi+1/(hi+1))
    a,b=1,7
    for _ in range(2,n+1):
        a,b=b,7*b-4*a
    smallest=float(Fraction(2**(n-1),4*b))
    assert k<45/11
    out.append({'n':n,'kappa2_from_spectrum':k,
                'exact_corner_magnitude_as_float':smallest})
print(json.dumps(out,indent=2))
(Path(__file__).resolve().parent/'spectral_recomputed.json').write_text(json.dumps(out,indent=2)+'\n')
