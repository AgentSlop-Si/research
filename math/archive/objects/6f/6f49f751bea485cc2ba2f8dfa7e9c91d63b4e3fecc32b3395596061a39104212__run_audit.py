from pathlib import Path
import json,random
from exact_fields import PrimeField,CyclotomicField,fourier,mv,mm,inverse
from scan_fft import Gates,scan,scan_fft,inverse_scan_matrix,inverse_support_lower_bound


def identity(f,n):return [[f.one if i==j else f.zero for j in range(n)] for i in range(n)]


def main():
    rng=random.Random(20261009);basis=mixed=scan_checks=word_checks=0;rows=[]
    cases=[(PrimeField(p),n) for p in (97,65537) for n in (2,4,8,16,32)]
    cases += [(CyclotomicField(n),n) for n in (4,8)]
    for f,n in cases:
        q=f.root(n);F=fourier(f,n)
        for j in range(n):
            x=[f.zero]*n;x[j]=f.one
            y,info=scan_fft(f,n,q,x)
            assert y==[row[j] for row in F];basis+=1
            assert info['one_way_scans']==2*(n.bit_length()-1)
            assert sum(info['field_operations'].values())==n+3+(n.bit_length()-1)*(13*n//2-4)
        for _ in range(3):
            x=[f.integer(rng.randrange(97)) for _ in range(n)]
            y,info=scan_fft(f,n,q,x)
            assert y==mv(f,F,x);mixed+=1
        inverse_F=inverse(f,F)
        assert all(v!=f.zero for row in inverse_F for v in row)
        assert inverse_support_lower_bound(n)<=info['one_way_scans']
        rows.append(dict(n=n,field=getattr(f,'p',f'Q(zeta_{n})'),
                         proved_ordinary_scan_lower_bound=inverse_support_lower_bound(n),
                         executed_scan_count=info['one_way_scans'],ledger=info))

    # Independent explicit matrix composition with internal shuffled layouts.
    f=PrimeField(97)
    for n in (2,4,8,16):
        for trial in range(18):
            t=rng.randrange(1,6);whole=identity(f,n)
            for _ in range(t):
                a=[rng.randrange(97) for _ in range(n)]
                b=[rng.randrange(1,97) for _ in range(n)]
                forward=bool(rng.randrange(2));B=inverse_scan_matrix(f,a,b,forward)
                columns=[]
                for j in range(n):
                    e=[0]*n;e[j]=1;columns.append(scan(Gates(f),e,a,b,forward))
                S=[list(row) for row in zip(*columns)]
                assert mm(f,B,S)==identity(f,n);scan_checks+=1
                permutation=list(range(n));rng.shuffle(permutation)
                P=[[int(j==permutation[i]) for j in range(n)] for i in range(n)]
                whole=mm(f,whole,mm(f,B,P))
            supports=[sum(v!=0 for v in row) for row in whole]
            assert max(supports)<=min(n,2**t)
            assert min(supports)<=min(n,2**(t-1))
            word_checks+=1
    report=dict(status='PASS',full_fourier_basis_vectors=basis,mixed_full_outputs=mixed,
                individual_scan_inverse_checks=scan_checks,internally_shuffled_products=word_checks,
                cases=rows,
                scope='Ordinary invertible one-state scan products with arbitrary internal permutations; not a general FFT lower bound.')
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
