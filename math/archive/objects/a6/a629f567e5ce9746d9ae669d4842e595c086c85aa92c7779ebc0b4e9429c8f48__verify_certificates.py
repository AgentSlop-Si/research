"""Independently check the saved exact modular polynomial Bézout witnesses.
Can optionally regenerate their underlying complex Green two-mask circuit.
"""
import argparse,json
from pathlib import Path
import phase37_curvature as q

def verify(regenerate=False):
    root=Path(__file__).resolve().parent
    listing=json.loads((root/'certificate_index.json').read_text())
    checked=0
    for row in listing:
        p=row['prime'];g=3 if p==998244353 else 31
        q.set_field(p,g)
        dat=json.loads((root/'certificates'/row['certificate']).read_text())
        f,h=dat['polynomials_coefficients_mod_prime']
        u,v=dat['bezout_coefficients_mod_prime']
        n=row['N']
        assert [len(f)-1,len(h)-1]==[2*n,2*n]
        assert f[-1] and h[-1]
        assert q.add(q.mul(u,f),q.mul(v,h))==[1]
        assert q.gcd_poly(f,h)==[1]
        assert dat['N']==n and dat['prime']==p
        if regenerate:
            generated=q.two_mask_gate(n,include_witness=True)
            assert generated['polynomials_coefficients_mod_prime']==[f,h]
            assert generated['cycle_orders']==dat['cycle_orders']
            assert json.loads(json.dumps(generated['plaquettes']))==dat['plaquettes']
        checked+=1
    return checked

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--regenerate',action='store_true')
    opt=a.parse_args()
    print('certificates passing exact Bezout checks:',verify(opt.regenerate))
