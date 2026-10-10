"""Exact finite-field checks of cyclic-shift Vandermonde displacement rank.
This tests algebraic identities, not a runtime lower bound or FFT speedup.
"""
import itertools, json
from pathlib import Path

def rank(a,p):
    a=[row[:] for row in a]; r=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]%p),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][j],-1,p); a[r]=[(x*inv)%p for x in a[r]]
        for i in range(r+1,len(a)):
            c=a[i][j]; a[i]=[(x-c*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r

def main():
    results=[]
    for N,p in [(5,11),(7,29),(11,23)]:
        zeta=next(z for z in range(2,p) if pow(z,N,p)==1)
        count=0
        for mask in range(1,1<<(N-1)):
            zs=[pow(zeta,j,p) for j in range(1,N) if mask>>(j-1)&1]
            for B in range(1,N):
                V=[[pow(z,r,p) for z in zs] for r in range(B)]
                for t in range(1,B+1):
                    defect=[[(V[r][s]*pow(z,t,p)-V[(r+t)%B][s])%p
                             for s,z in enumerate(zs)] for r in range(B)]
                    expected=[[0 if r+t<B else
                               (pow(z,B,p)-1)*pow(z,r+t-B,p)%p for z in zs]
                              for r in range(B)]
                    assert defect==expected
                    assert rank(defect,p)==min(t,len(zs))
                    count+=1
        results.append(dict(N=N,field_prime=p,root=zeta,checks=count))
    out=dict(status='passed',arithmetic='exact modular integers',tests=results,
             total=sum(x['checks'] for x in results),
             limitation='Finite test cases supplement the proof; no operation-count lower bound.')
    Path(__file__).with_name('displacement_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
