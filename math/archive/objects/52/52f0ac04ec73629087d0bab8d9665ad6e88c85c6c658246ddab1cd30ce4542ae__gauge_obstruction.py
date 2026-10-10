"""Phase29 C4-free obstruction to reducing twiddles by row/column gauges.

For b×h stage, coefficient T[u,q] = omega^(u*q), omega primitive order b*h.
After arbitrary nonzero row/col rescalings, at most h+choose(b,2)
entries can equal one. This follows because two rows cannot agree on
more than one column; a second agreement would force b*h | (u-v)(q-q'),
whose absolute value is strictly smaller than b*h.

The routine exhaustively maximizes the number of unit entries for small b=4
by searching all root-of-unity row rephasings and the optimal column rephasing.
"""
import json,itertools
from collections import Counter

def bound(b,h):
    return max(0,b*h-(h+b*(b-1)//2))

def ordinary_ones(b,h):
    return h+b-1

def maximize_gauge_roots(b,h):
    """Exhaustive for b=4,h<=8; root-of-unity row/col phases only.
    Arbitrary complex row scalings cannot improve beyond C4 bound, but optimum
    over arbitrary scalings is not asserted here.
    """
    g=b*h
    best=-1;bestalphas=None
    for values in itertools.product(range(g),repeat=b-1):
        a=(0,)+values
        score=0
        for q in range(h):
            vals=[(a[u]+u*q)%g for u in range(b)]
            score+=max(Counter(vals).values())
        if score>best:best=score;bestalphas=a
    return dict(b=b,h=h,g=g,ordinary_ones=ordinary_ones(b,h),
                optimum_unit_entries=best,alpha_exponents=bestalphas,
                absolute_upper_bound=h+b*(b-1)//2,
                ordinary_nonunit=(b-1)*(h-1),
                optimum_nonunit=b*h-best,
                maximum_possible_gauge_saving=(b-1)*(b-2)//2,
                actual_root_gauge_saving=best-ordinary_ones(b,h))

def run():
    out=[maximize_gauge_roots(4,h) for h in (1,2,4,8)]
    for r in out:
        assert r['optimum_unit_entries']<=r['absolute_upper_bound']
        assert r['optimum_unit_entries']>=r['ordinary_ones']
    return dict(theorem='C4-free upper bound, arbitrary nonzero row/column scalings',
                stage8_upper_bound_extra_savings=21,
                stage4_upper_bound_extra_savings=3,
                finite_root_gauge_audits=out)
if __name__=='__main__':print(json.dumps(run(),indent=2))
