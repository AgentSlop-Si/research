"""Targeted independent tests of CDF sampling and pre-RNG fallback."""
from bisect import bisect_right
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from prefix_planner import plan_prefix,construct_surrogate


class NoAccessRng:
    def __getattribute__(self,name):
        raise AssertionError('fallback must not even consult RNG state')


class GivenUniforms:
    def __init__(self,values):self.values=values;self.position=0
    def random(self):
        result=self.values[self.position];self.position+=1;return result


def main():
    n=1024
    x=[complex((-1 if j%2 else 1)*(1+j%3)) for j in range(n)]
    x[777]=4096+0j
    plan=plan_prefix(x,.25,.5,max_head=1)
    assert plan.chosen.method=='sample-tail' and plan.chosen.head_size==1
    assert plan.ordered_top_indices==(777,)
    k=plan.chosen.requested_samples
    cycle=[0.,math.nextafter(0.,1.),.25,.5,.75,math.nextafter(1.,0.)]
    uniforms=[cycle[j%len(cycle)] for j in range(k)]
    rng=GivenUniforms(uniforms)
    entries,metadata=construct_surrogate(x,.25,.5,plan=plan,rng=rng)
    # Independent inverse-CDF oracle, with exact masses of integer-real input.
    tail=[j for j in range(n) if j!=777]
    cdf=[];total=0
    for j in tail:
        total+=int(abs(x[j]));cdf.append(Fraction(total))
    counts=Counter(tail[bisect_right(cdf,Fraction(u)*total)] for u in uniforms)
    expected={777:x[777]}
    for j,count in counts.items():
        expected[j]=complex(float(Fraction(total*count,k))*(1 if x[j].real>0 else -1))
    assert dict(entries)==expected
    assert rng.position==metadata['actual_draws']==k
    assert metadata['sampled_distinct_indices']==len(counts)
    assert metadata['realized_support']==len(counts)+1
    assert metadata['selection_calls_during_construction']==0
    for epsilon in (1e-300,math.nextafter(0.,1.)):
        fallback=plan_prefix([1,2,3,4],epsilon,.125,max_head=0)
        assert fallback.chosen.method=='exact-input'
        copied,info=construct_surrogate([1,2,3,4],epsilon,.125,
                                       plan=fallback,rng=NoAccessRng())
        assert copied==[(0,1+0j),(1,2+0j),(2,3+0j),(3,4+0j)]
        assert info['actual_draws']==0
    cutoff=plan_prefix([3,1],.25,.125,max_head=1)
    copied,info=construct_surrogate([3,1],.25,.125,plan=cutoff,rng=NoAccessRng())
    assert copied==[(0,3+0j)] and info['actual_draws']==0
    # Strict rejection of non-uniform-domain values is separate from asserting
    # that a caller-supplied RNG is independent/uniform (which is a precondition).
    rejected=0
    for bad in (-.01,1.,float('nan'),float('inf')):
        values=[0.]*k;values[k//2]=bad
        try:construct_surrogate(x,.25,.5,plan=plan,rng=GivenUniforms(values))
        except ValueError:rejected+=1
        else:raise AssertionError('out-of-domain RNG value accepted')
    root=Path(__file__).resolve().parent
    report={'status':'PASS','sampled_with_nonempty_head':True,
            'head_index':777,'actual_draws':k,'tail_distinct_indices':len(counts),
            'independent_inverse_cdf_output_match':True,
            'huge_budget_rng_nonaccess_cases':2,'exact_cutoff_rng_nonaccess_cases':1,
            'invalid_uniform_values_rejected':rejected,
            'source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                             for name in ('prefix_planner.py','run_audit.py')},
            'scope':'CDF/construction checks; not empirical or machine-certified probability bounds.'}
    (root/'independent_review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
