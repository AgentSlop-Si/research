"""Fast, independent arithmetic verification of saved Bezout identities."""
from pathlib import Path
import json, hashlib
from phase28_polynomial import poly_mul,poly_add,poly_trim
from phase28_synthesis import P

def main():
    base=Path(__file__).with_name('certificates')
    for n in (4,8,16):
        path=base/f'bezout_N{n}.json'
        raw=path.read_bytes();cert=json.loads(raw)
        assert cert['n']==n and cert['prime']==P
        assert cert['nonzero_reduced_leading_coeffs']
        assert cert['gcd']==[1]
        assert len(cert['p1_coefficients'])-1==cert['reduced_degree_p1']
        assert len(cert['p2_coefficients'])-1==cert['reduced_degree_p2']
        combined=poly_add(poly_mul(cert['bezout_u'],cert['p1_coefficients']),
                          poly_mul(cert['bezout_v'],cert['p2_coefficients']))
        assert combined==[1]
        print(f'N={n}: verified Bezout identity, degrees '
              f'{cert["reduced_degree_p1"]}/{cert["reduced_degree_p2"]}; '
              f'SHA256={hashlib.sha256(raw).hexdigest()}')
if __name__=='__main__':main()
