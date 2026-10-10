"""Independent Phase25 controls. Repeat with `python audit.py`."""
from __future__ import annotations
import json,random,time
from pathlib import Path
from phase25_affine import *
from phase25_twisted import *


def reference_fft(x:list[int])->list[int]:
    """Independent exact iterative radix-2 FFT, only for audit comparison."""
    n=len(x);w=root(n)
    y=[v%P for v in x]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit;bit>>=1
        j^=bit
        if i<j:y[i],y[j]=y[j],y[i]
    length=2
    while length<=n:
        wm=pow(w,n//length,P)
        for s in range(0,n,length):
            v=1
            for k in range(length//2):
                a=y[s+k];b=v*y[s+k+length//2]%P
                y[s+k]=(a+b)%P
                y[s+k+length//2]=(a-b)%P
                v=v*wm%P
        length*=2
    inv=pow(sqrt_mod(n),-1,P)
    return [v*inv%P for v in y]


def main():
    records=[]
    for n in (16,64,256,1024,4096,16384):
        rng=random.Random(20261009+n)
        z=rng.randrange(1,P)
        # Both two-run orders, including degenerate roots.
        methods=[]
        for method,order,runs in (
          ('zigzag',zigzag_order(n),affine_runs_zigzag(n)),
          ('twisted',twisted_order(n),twisted_runs(n))):
            for zz in (z,root(n),0):
                actual=fourier_affine_geometric(n,zz,runs)
                expected=reference_fft(permuted_geometric_input(order,zz))
                if actual!=expected:raise AssertionError((n,method,zz))
            methods.append(method)
        alpha,beta=2,3
        if n<=16384:
            x=[rng.randrange(P) for _ in range(n)]
            inv=TwistedGreenSumInverse.create(n,alpha,beta)
            if len(inv.updates)!=4:raise AssertionError('not four updates')
            if inv.apply(twisted_green_sum_apply(n,alpha,beta,x))!=x:
                raise AssertionError('twisted inverse')
        W=successor_of_order(twisted_order(n));Z=cyclic_shift_successor(n)
        commute=permutation_difference_rank([W[Z[i]] for i in range(n)],
                                             [Z[W[i]] for i in range(n)])
        if commute!=n-2:raise AssertionError('wrong rank')
        rows={"n":n,"orders_checked":methods,"exact_fft_controls_per_order":3,
              "twisted_green_inverse_checked":n<=16384,
              "green_noncommuting_rank":commute,
              "twisted_crosscut_edges":crosscut_edge_count(n,twisted_order(n)),
              "twisted_corner_updates":4,
              "hidden_cross_edges":hidden_cut_edge_counts(n),
              "hidden_cut_rank_upper_bound":5,
              "spectral_error_floor_bound":round(hidden_cut_spectral_error_floor(n),7)}
        records.append(rows)
        print('size',n,'FFT exact controls passed; commutator rank',commute,
              'inverse check',n<=16384,flush=True)
    out={'status':'PASS','field_modulus':P,'experiments':records,
         'note':'Finite field controls. Does not establish sub-NlogN FFT or numeric stability.'}
    Path(__file__).with_name('audit.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':main()
