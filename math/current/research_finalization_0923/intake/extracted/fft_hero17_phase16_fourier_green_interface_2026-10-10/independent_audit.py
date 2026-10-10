"""Independent Phase 16 audit. Uses direct Fourier basis evaluations.

No numerical FFT or Green black-box is used to assert matrix identity.
"""
import json
import random
from pathlib import Path

from phase16 import (nth_root, boundary_pair, rank_mod, fourier, mm, mv,
                     solve, column_band_valid, boundary_circulant_gauge,
                     harper_algebra_audit, harper_rational_witness,
                     intertwining_check)

OUT=Path(__file__).with_name('AUDIT_RESULTS.json')
SEED=20261010
RANDOM=random.Random(SEED)


def direct_bin(v,k,p,w):
    n=len(v)
    step=pow(w,(-k)%n,p)
    z=1;out=0
    for x in v:
        out=(out+x*z)%p
        z=z*step%p
    return out


def direct_bins(v,p,w):
    return [direct_bin(v,k,p,w) for k in range(len(v))]


def boundary_audit():
    primes={3:7,5:11,7:29,9:19,11:23,13:53,15:31,17:103}
    summary=[];full_transforms=0;coefficients=0
    for n,p in primes.items():
        a=(n-1)//4;b=(n-1)//2-a;w=nth_root(n,p)
        P,Q=boundary_pair(n,a,p)
        assert rank_mod(Q,p)==n
        assert column_band_valid(P,a)
        assert column_band_valid(Q,b)
        pred,h,DL,DR=boundary_circulant_gauge(n,a,p,Q)
        assert pred==Q
        # The full Fourier matrix is compared *without using phase16.fourier*.
        for j in range(n):
            e=[int(i==j) for i in range(n)]
            y=mv(P,solve(Q,e,p),p)
            z=direct_bins(e,p,w)
            assert y==z,(n,j)
            full_transforms+=1;coefficients+=n
        for _ in range(5):
            vec=[RANDOM.randrange(p) for _ in range(n)]
            y=mv(P,solve(Q,vec,p),p)
            z=direct_bins(vec,p,w)
            assert y==z
            full_transforms+=1;coefficients+=n
        summary.append({'N':n,'p':p,'a':a,'b':b,'P_nnz':sum(x!=0 for row in P for x in row),
                        'Q_nnz':sum(x!=0 for row in Q for x in row),
                        'Q_rank':rank_mod(Q,p),
                        'circulant_kernel_nnz':sum(x!=0 for x in h)})
    return summary,full_transforms,coefficients


def exhaustive_zero_count():
    # All nonzero length-16 vectors supported in {0,1,2} over GF(17).
    n,p=16,17;w=nth_root(n,p)
    pw=[pow(w,(-k)%n,p) for k in range(n)]
    trials=0;max_zeros=0;attainers=0
    for a in range(p):
        for b in range(p):
            for c in range(p):
                if a==b==c==0: continue
                zeros=sum((a+b*pw[k]+c*pw[k]*pw[k])%p==0 for k in range(n))
                assert zeros<=2,('bad Fourier polynomial zero count',a,b,c,zeros)
                trials+=1
                if zeros>max_zeros: max_zeros=zeros;attainers=0
                if zeros==max_zeros:attainers+=1
    return {'n':n,'p':p,'nonzero_triples':trials,'maximum_fourier_zeros':max_zeros,
            'attaining_vectors':attainers}


def field_exceptions():
    out=[]
    for n,a,p in [(45,11,181),(45,11,271),(49,12,197),(49,12,491),(53,13,107),(53,13,743)]:
        P,Q=boundary_pair(n,a,p)
        rank=rank_mod(Q,p)
        assert column_band_valid(P,a)
        assert column_band_valid(Q,(n-1)//2-a)
        out.append({'N':n,'a':a,'p':p,'rank_Q':rank,'nullity_Q':n-rank})
    assert [v['nullity_Q'] for v in out] == [2,0,2,0,4,0]
    return out


def harper_audit():
    primes={3:7,4:5,5:11,6:7,7:29,8:17,9:19,10:11,
            11:23,12:13,13:53,15:31,16:17}
    span=[];cert=[]
    for n,p in primes.items():
        dim,aug=harper_algebra_audit(n,p)
        span.append({'N':n,'p':p,'algebra_dim':dim,'plus_F_dim':aug,
                     'F_in_harper_algebra':dim==aug})
        if n%2:
            wit=harper_rational_witness(n,p,(n-1)//2)
            assert wit and wit[0]==(n-1)//2
            cert.append({'N':n,'p':p,'first_tested_invertible_rational_degree':wit[0],
                         'numerator_coeffs':wit[1],'denominator_coeffs':wit[2]})
    assert all(v['F_in_harper_algebra']==(v['N']%4!=0) for v in span)
    return span,cert


def intertwiner_audit():
    n,p=17,103;w=nth_root(n,p);F=fourier(n,p,w)
    assert intertwining_check(F,p,w)
    # Independent basis test: identities reconstruct each column from the first.
    for j in range(n):
        e=[int(t==j) for t in range(n)]
        assert mv(F,e,p)==direct_bins(e,p,w)
    return {'N':n,'columns_certified':n,'all_column_entries':n*n}


def main():
    summary,transforms,coeffs=boundary_audit()
    data={
      'phase':'Hero #17 Phase 16: Fourier-Green interface rigidity',
      'status':'PASS',
      'proven_results':['cyclic-window Fourier uncertainty','band-interface lower bound',
                        'boundary polynomial uniqueness','quadratic chirp normalizes Weyl shifts'],
      'not_proven':['arbitrary exact O(N) FFT','novel historical priority',
                    'all-length invertibility of boundary construction',
                    'uniform rational degree optimum for Harper'],
      'random_seed':SEED,
      'boundary_cases':summary,
      'complete_transform_trials':transforms,
      'complete_transform_coefficients_checked':coeffs,
      'exhaustive_zero_count':exhaustive_zero_count(),
      'field_sensitive_denominator':field_exceptions(),
      'harper_algebra':harper_audit()[0],
      'harper_rational_witnesses':harper_audit()[1],
      'Fourier_intertwiner':intertwiner_audit(),
      'cost_note':'P and Q have Theta(N^2) entries on boundary-balanced families; direct solve of Q is not linear time.'
    }
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('PASS: boundary full transforms',transforms,'coefficients',coeffs)
    print('PASS: exhaustive zero count',data['exhaustive_zero_count'])
    print('PASS: field-sensitive denominator ranks',[(v['N'],v['p'],v['rank_Q']) for v in data['field_sensitive_denominator']])
    print('PASS: Harper algebra classifications',len(data['harper_algebra']))
    print('PASS: Fourier intertwining',data['Fourier_intertwiner'])
    print('Wrote',OUT)
if __name__=='__main__':main()
