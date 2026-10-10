"""Independent exact integer checks supporting, but not replacing, symbolic bounds."""
import json, math
from pathlib import Path
out=[]
for N in range(1297,100002,2):
    d=(math.isqrt(N)+16)//13;m=N-d;r=2*(d-1)
    E=d-3+(d-1)//2;O=d-3+(d-2)//2;e=(N+1)//2
    assert d>=4 and (13*d-17)**2<N
    assert N>=7*d and m+1>=3*(d-1) and m>=4*(d-1)
    assert N-5*d+12>=(N+1)//2
    assert E+r<e and e+O+r<N
    assert (5*d-8)**2<N
    a=E+O+2+2*r;b=d-1;c=d+2*r-1
    assert (a,b,c)==(7*d-10,d-1,5*d-5)
    assert a+b+c==13*d-16
    if N in [1297,2001,10001,100001]:
        out.append({'N':N,'d':d,'m':m,'banks':2*m+2,'shifted_chirp_ranges':[[0,E+r],[e,e+O+r]],'derivative_atom_groups':[a,b,c],'coherence_condition_integer_check':(a+b+c-1)**2<N})
Path(__file__).with_name('FRESH_UNIFORM_INEQUALITY_RESULTS.json').write_text(json.dumps({'odd_orders_checked':(100001-1297)//2+1,'range':[1297,100001],'status':'PASS','examples':out},indent=2)+'\n')
print(json.dumps(out,indent=2))
