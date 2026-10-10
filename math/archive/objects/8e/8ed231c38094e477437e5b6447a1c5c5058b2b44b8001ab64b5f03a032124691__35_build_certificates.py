"""Produce independently checkable Bezout polynomial certificates."""
import json,hashlib
from pathlib import Path
from phase28_polynomial import exceptional_coupling_certificate,poly_mul,poly_add
from phase28_synthesis import P

def main():
    dest=Path(__file__).with_name('certificates')
    dest.mkdir(exist_ok=True)
    for n in (4,8,16):
        c=exceptional_coupling_certificate(n,2800+n)
        assert c['gcd']==[1] and c['verification_passes']
        fn=dest/f'bezout_N{n}.json'
        raw=(json.dumps(c,separators=(',',':'))+'\n').encode()
        fn.write_bytes(raw)
        print(fn.name,'bytes',len(raw),'SHA256',hashlib.sha256(raw).hexdigest(),
              'reduced degrees',c['reduced_degree_p1'],c['reduced_degree_p2'])

if __name__=='__main__':main()
