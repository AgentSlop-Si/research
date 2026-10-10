"""Produce saved, explicitly verifiable Bézout witnesses at two primes."""
import json
from pathlib import Path
import phase37_curvature as q

def run():
    folder=Path(__file__).resolve().parent
    base=folder/'certificates';base.mkdir(exist_ok=True)
    summary=[]
    for p,g in [(998244353,3),(2013265921,31)]:
        q.set_field(p,g)
        for n in (4,8,16,32,64,128):
            data=q.two_mask_gate(n,include_witness=True)
            assert data['excluded'] and data['degrees']==[2*n,2*n]
            f,h=data['polynomials_coefficients_mod_prime']
            u,v=data['bezout_coefficients_mod_prime']
            assert q.add(q.mul(u,f),q.mul(v,h))==[1]
            path=base/f'bezout_N{n}_p{p}.json'
            path.write_text(json.dumps(data,indent=2)+'\n')
            summary.append({'N':n,'prime':p,'degrees':data['degrees'],'polynomial_gcd_degree':0,
                            'leading_coefficients_mod_prime':data['leading_coefficients_mod_prime'],
                            'bezout_identity_verified':True,'certificate':path.name})
            print('saved',path.name)
    (folder/'certificate_index.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':run()
