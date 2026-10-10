"""Audit-authored exact periodic baseline. No uploaded code is imported.

Fits componentwise lower medians with deterministic median-of-medians selection.
Returns exact Gaussian-integer unnormalized Fourier baseline and residual.
No claim of novelty, full FFT computation, or numerical speed advantage.
"""
from math import gcd

def select(a, k):
    if not 0 <= k < len(a):
        raise ValueError('invalid selection')
    if len(a) <= 5:
        return sorted(a)[k]
    mids = []
    for start in range(0, len(a), 5):
        group = sorted(a[start:start+5])
        mids.append(group[len(group)//2])
    pivot = select(mids, len(mids)//2)
    low, equal, high = [], 0, []
    for v in a:
        if v < pivot: low.append(v)
        elif v > pivot: high.append(v)
        else: equal += 1
    if k < len(low): return select(low, k)
    if k < len(low) + equal: return pivot
    return select(high, k-len(low)-equal)

def periodic_baseline(coords):
    if not coords or any(len(v)!=2 or any(type(z)is not int for z in v) for v in coords):
        raise ValueError('nonempty Gaussian-integer input required')
    N=len(coords); q=gcd(N,4); n=N//q
    clusters=[[[] for _ in range(2)] for _ in range(q)]
    sums=[[0,0] for _ in range(q)]
    for j,pair in enumerate(coords):
        for c,z in enumerate(pair):
            clusters[j%q][c].append(z);sums[j%q][c]+=z
    med=[tuple(select(clusters[s][c],(n-1)//2) for c in range(2)) for s in range(q)]
    residual=[tuple(z-med[j%q][c] for c,z in enumerate(pair)) for j,pair in enumerate(coords)]
    roots=((1,0),(0,-1),(-1,0),(0,1))
    def spectrum_short(coordinates):
        out={}
        for t in range(q):
            re=im=0
            for s,(a,b) in enumerate(coordinates):
                u,v=roots[(4*s*t//q)%4]
                re+=a*u-b*v;im+=a*v+b*u
            out[t*n]=(re,im)
        return out
    sparse_baseline=spectrum_short([(n*a,n*b) for a,b in med])
    baseline=[sparse_baseline.get(k,(0,0)) for k in range(N)]
    return {'N':N,'q':q,'class_medians':med,'residual':residual,
            'residual_mass':sum(abs(z) for p in residual for z in p),
            'input_mass':sum(abs(z) for p in coords for z in p),
            'unnormalized_baseline':baseline,'exact_corner_spectrum':spectrum_short(sums)}

def combine_decoded_mean(fit, integer_outputs=None, denominator=1, *, failed=False):
    """Add decoded residual sample mean, preserving exact raw quarter-root bins.

    Decoder contract: integer_outputs[k]/denominator approximates F(residual)[k]
    divided by fit['residual_mass']. This adapter does not perform sampling or
    establish decoder accuracy. Return pairs/denominator are unnormalized Fhat.
    A flagged sampler failure is never treated as an accuracy-certified result.
    """
    N=fit['N'];mass=fit['residual_mass']
    if mass==0:
        return {'integer_outputs':list(fit['unnormalized_baseline']),
                'denominator':1,'exact':True,'failed':False}
    if failed:
        return {'integer_outputs':[(0,0)]*N,'denominator':1,'exact':False,'failed':True}
    if type(denominator)is not int or denominator<=0 or integer_outputs is None or len(integer_outputs)!=N:
        raise ValueError('valid N-entry rational decoder output required')
    out=[]
    for (u,v),(a,b) in zip(fit['unnormalized_baseline'],integer_outputs):
        if type(a)is not int or type(b)is not int:
            raise ValueError('integer decoder numerators required')
        out.append((denominator*u+mass*a,denominator*v+mass*b))
    for k,(a,b) in fit['exact_corner_spectrum'].items():
        out[k]=(denominator*a,denominator*b)
    return {'integer_outputs':out,'denominator':denominator,'exact':False,'failed':False}

if __name__ == '__main__':
    import itertools,random,json
    from pathlib import Path
    selection_cases=0
    for n in range(1,8):
        for a in itertools.product((-1,0,1),repeat=n):
            for k in {0,n//2,n-1}:
                assert select(list(a),k)==sorted(a)[k];selection_cases+=1
    rng=random.Random(918171);fit_cases=0
    for N in range(1,101):
        for _ in range(10):
            x=[(rng.randint(-200,200),rng.randint(-200,200)) for _ in range(N)]
            r=periodic_baseline(x);n=N//r['q']
            assert r['residual_mass']<=r['input_mass']
            for s in range(r['q']):
                for c in range(2):
                    a=sorted(x[j][c] for j in range(s,N,r['q']))
                    assert r['class_medians'][s][c]==a[(n-1)//2]
            fit_cases+=1
    examples={
        'near_constant_21':[(100,0)]*20+[(101,0)],
        'outlier_9':[(5,0)]*8+[(100,0)],
        'no_improvement_8':[(1,0)]*4+[(-1,0)]*4,
        'exact_periodic_12':[(3,4),(-2,1),(7,-3),(0,9)]*3}
    example_results={name:{k:v for k,v in periodic_baseline(x).items() if k in ('N','q','input_mass','residual_mass','class_medians')} for name,x in examples.items()}
    assert example_results['near_constant_21']['residual_mass']==1
    assert example_results['outlier_9']['residual_mass']==95
    assert example_results['no_improvement_8']['residual_mass']==8
    assert example_results['exact_periodic_12']['residual_mass']==0
    # Independent exact DFT checks over finite fields, rather than rounded roots.
    def prime(p):
        return p>=2 and all(p%d for d in range(2,int(p**.5)+1))
    modular_cases=0
    for N in range(1,21):
        p=N+1
        while not prime(p): p+=N
        def exact_order(a):
            return pow(a,N,p)==1 and all(pow(a,d,p)!=1 for d in range(1,N) if N%d==0)
        w=next(a for a in range(1,p) if exact_order(a))
        # Gaussian arithmetic represented as pairs, so no square root of -1 is needed.
        def mul(a,b): return ((a[0]*b[0]-a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0])%p)
        # Validate real baseline using a separate Nth-root transform. At q<=2, roots
        # are real. For q=4, choose the Gaussian embedding i=w**(-N/4).
        i=pow(w,3*N//4,p) if N%4==0 else 0
        x=[(rng.randint(-10,10),0) for _ in range(N)];r=periodic_baseline(x)
        h=[r['class_medians'][j%r['q']][0] for j in range(N)]
        for k,(a,b) in enumerate(r['unnormalized_baseline']):
            direct=sum(z*pow(w,j*k,p) for j,z in enumerate(h))%p
            assert direct==(a+b*i)%p
        modular_cases+=1
    adapter_cases=0
    from fractions import Fraction
    for x in examples.values():
        fit=periodic_baseline(x);N=len(x)
        numerators=[(j-2,3-j) for j in range(N)];D=7
        z=combine_decoded_mean(fit,numerators,D)
        for k,(a,b) in enumerate(z['integer_outputs']):
            for c,v in enumerate((a,b)):
                if fit['residual_mass']==0:
                    expected=Fraction(fit['unnormalized_baseline'][k][c])
                elif k in fit['exact_corner_spectrum']:
                    expected=Fraction(fit['exact_corner_spectrum'][k][c])
                else:
                    expected=Fraction(fit['unnormalized_baseline'][k][c])+Fraction(fit['residual_mass']*numerators[k][c],D)
                assert Fraction(v,z['denominator'])==expected
        if fit['residual_mass']:
            assert combine_decoded_mean(fit,failed=True)['failed']
        else:
            assert z['exact']
        adapter_cases+=1
    out={'status':'PASS','adapter_cases':adapter_cases,'selection_cases':selection_cases,'fit_cases':fit_cases,'modular_dft_lengths_checked':modular_cases,'examples':example_results,
         'algorithm':'deterministic median-of-medians; only groups of <=5 are sorted',
         'scope':'exact baseline and residual only; no approximate decoder and no uploaded code executed'}
    Path(__file__).with_name('median_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
