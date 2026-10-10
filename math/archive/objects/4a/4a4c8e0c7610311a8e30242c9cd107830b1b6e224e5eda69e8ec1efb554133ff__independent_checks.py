"""Independent exhaustive acceptance/output check, deliberately tiny field."""
from itertools import product
from pathlib import Path
import hashlib,json,sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'fft_qlinear_recurrence_research'))
from exact_fields import PrimeField,fourier,mv
from extended_recurrence import try_extended_fourier


def main():
    f=PrimeField(5);n=4;q=f.root(n);F=fourier(f,n)
    E=[[0]*n for _ in range(n)]
    for i in range(n):
        E[i][i]=f.neg(f.power(q,i))
        if i+1<n:E[i][i+1]=f.neg(f.mul(f.power(q,i),f.sub(f.power(q,i+1),1)))
    accepted=declined=0;paths={}
    for raw in product(range(5),repeat=n):
        x=list(raw);image=mv(f,E,x);expected=mv(f,F,x)
        for cap in (0,1):
            promised=(sum(v!=0 for v in x)<=2*cap or any(
                sum(f.sub(a,f.mul(shift,b))!=0 for a,b in zip(image,x))<=cap
                for shift in range(5)))
            y,meta=try_extended_fourier(f,n,q,x,max_defects=cap)
            assert meta['accepted']==promised,(x,cap,meta)
            if promised:
                assert y==expected,(x,cap,y,expected)
                accepted+=1
                branch=meta.get('target',{}).get('branch',meta['path'])
                paths[branch]=paths.get(branch,0)+1
            else:
                assert y is None;declined+=1
    result=dict(status='PASS',exhaustive_input_cap_pairs=accepted+declined,
                accepted=accepted,declined=declined,paths=paths,
                source_sha256=hashlib.sha256((ROOT/'extended_recurrence.py').read_bytes()).hexdigest())
    (ROOT/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
