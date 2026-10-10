"""Fresh exact algebra and integer boundary checks for constant-eight refinement."""
from pathlib import Path
import json,math
import sympy as s
Q=s.Matrix([[0,s.sqrt(7),s.sqrt(35)],[s.sqrt(7),0,s.sqrt(5)],[s.sqrt(35),s.sqrt(5),0]])
M=8*s.eye(3)-Q
minors=[s.simplify(M[:j,:j].det()) for j in [1,2,3]]
assert minors==[8,57,66]
examples=[]
for N in range(1025,100002,2):
    d=math.isqrt(N)//8;m=N-d;r=2*(d-1)
    E=d-3+(d-1)//2;O=d-3+(d-2)//2;e=(N+1)//2
    assert d>=4 and N>=64*d*d
    assert N>=7*d and m>=4*(d-1) and m+1>=3*(d-1)
    assert N-5*d+12>=(N+1)//2 and m>=(N-1)//2
    assert E+r<e and e+O+r<N
    a=E+O+2+2*r;b=d-1;c=d+2*r-1
    assert (a,b,c)==(7*d-10,d-1,5*d-5)
    assert a<=7*d and b<=d and c<=5*d
    coord=[E+O+2,d-1,d]
    assert coord==[3*d-6,d-1,d]
    if N in [1025,1297,1601,10001,100001]:
        examples.append({'N':N,'d':d,'banks':2*m+2,'derivative_groups':[a,b,c],'coordinate_exclusion_groups':coord,'shifted_chirp_ranges':[[0,E+r],[e,e+O+r]]})
out={'status':'PASS','principal_minors':[int(v) for v in minors],'boundary_threshold':1025,'odd_orders_checked':(100001-1025)//2+1,'range':[1025,100001],'examples':examples}
Path(__file__).with_name('FRESH_CONSTANT_EIGHT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
