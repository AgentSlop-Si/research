"""Stand-alone independent determinant checker, no project module imports."""
from itertools import combinations_with_replacement
from pathlib import Path
import json

P=998244353

def independent_root(n):
    for b in range(2, P):
        w=pow(b,(P-1)//n,P)
        if pow(w,n,P)==1 and pow(w,n//2,P)!=1:
            return w
    raise RuntimeError

def independently_rebuild_and_verify(data):
    for key,cert in data['conjugate_pair_cubic_certificates'].items():
        n=int(key)
        w=independent_root(n)
        sources=tuple(k for k in range(n) if k not in (1,n-1))
        terms=[]
        for degree in (1,2,3):
            terms.extend(m for m in combinations_with_replacement(sources,degree) if sum(m)%n==1)
        supports=[tuple(s) for s in cert['supports']]
        if len(supports)!=len(terms)+1 or len(set(supports))!=len(supports):return False
        rows=[]
        for bits in supports:
            if len(bits)>3 or any(j<0 or j>=n for j in bits):return False
            freq={k:sum(pow(w,(k*j)%n,P) for j in bits)%P for k in sources}
            row=[]
            for mon in terms:
                v=1
                for k in mon:v=v*freq[k]%P
                row.append(v)
            row.append(sum(pow(w,j%n,P) for j in bits)%P)
            rows.append(row)
        # Independent modular elimination: operate by rows; don't call graded_certificate.
        det=1
        width=len(rows)
        for j in range(width):
            pivot=next((t for t in range(j,width) if rows[t][j]),None)
            if pivot is None:return False
            if pivot !=j:
                rows[j],rows[pivot]=rows[pivot],rows[j]
                det=-det
            a=rows[j][j]
            det=det*a%P
            inv=pow(a,P-2,P)
            for t in range(j+1,width):
                ratio=rows[t][j]*inv%P
                if ratio:
                    for col in range(j,width):rows[t][col]=(rows[t][col]-ratio*rows[j][col])%P
        print(f"N={n}: independent determinant {det} (nonzero), monomials={len(terms)}, rows={len(supports)}")
        if det!=cert['determinant_mod_998244353']:return False
    return True

if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('audit_results.json').read_text())
    assert independently_rebuild_and_verify(data)
    print('Independent certificate verification PASS')
