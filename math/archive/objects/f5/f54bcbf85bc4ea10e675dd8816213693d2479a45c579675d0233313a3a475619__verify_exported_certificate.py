# Independent verifier of the newly generated raw coefficients, no package imports.
import json
from pathlib import Path
from sympy import QQ,sympify,Poly,Symbol
K=QQ.cyclotomic_field(8)
file=Path(__file__).with_name('channel_certificate.json')
c=json.loads(file.read_text())
def dec(x):
    if isinstance(x,list):return [dec(v) for v in x]
    p=Poly(sympify(x,locals={'zeta':Symbol('zeta')}),Symbol('zeta'),domain=QQ)
    return sum((K.convert(coeff)*K.unit**power[0] for power,coeff in p.terms()),K.zero)
a,b,v,e,d=[dec(c[name]) for name in ('forward_a','forward_b','backward_a','backward_b','diagonal')]
for col in range(8):
    output=[K.zero]*8
    for channel in range(3):
        state=K.zero
        for row in range(8):
            state=a[channel][row]*state+(b[channel][row] if row==col else K.zero)
            output[row]+=state
        state=K.zero
        for row in range(7,-1,-1):
            state=v[channel][row]*state+(e[channel][row] if row==col else K.zero)
            output[row]+=state
    output[col]+=d[col]
    target=[K.unit**((r*c['col_order'][col])%8) for r in c['row_order']]
    assert output==target,(col,output,target)
print('SAVED_EXACT_CERTIFICATE_VERIFIED: 64/64 entries in Q(zeta_8)')
