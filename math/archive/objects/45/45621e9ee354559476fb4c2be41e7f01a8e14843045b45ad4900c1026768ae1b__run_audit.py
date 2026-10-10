"""Focused full-prefix objective, construction, and metadata checks."""
from fractions import Fraction
import json
import math
from pathlib import Path
import random
from prefix_planner import plan_prefix, construct_surrogate


class NoDraws:
    def random(self):
        raise AssertionError('this branch must not draw randomness')


class RepeatedDraw:
    def __init__(self):
        self.calls = 0
    def random(self):
        self.calls += 1
        return 0.0


def independent_oracle(x, epsilon, delta, cap):
    mags = [Fraction(math.hypot(complex(v).real,complex(v).imag)) for v in x]
    order = sorted((j for j,a in enumerate(mags) if a),key=lambda j:(-mags[j],j))
    total, m = sum(mags,Fraction(0)),len(order)
    factor = 4*Fraction(math.log(4*len(x))-math.log(delta))/Fraction(epsilon)**2
    rows = []
    for s in range(min(m,cap)+1):
        tail = sum((mags[j] for j in order[s:]),Fraction(0))
        if not total or tail <= Fraction(epsilon)*total:
            k = 0
        else:
            value = factor*tail**2/total**2
            k = (value.numerator+value.denominator-1)//value.denominator
        support = min(m,s+k)
        draws = 0 if s+k >= m else k
        rows.append((support,draws,s,k,tail))
    return order[:min(m,cap)],min(rows)


def rejects(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('invalid or stale input was accepted')


def main():
    rng = random.Random(109)
    cases = 0
    for n in [1,2,4,8,16,32,64]:
        for trial in range(4):
            x = [complex(rng.choice([0,0,1,1,2,3,5]),rng.choice([0,0,1,-1]))
                 for _ in range(n)]
            epsilon,delta = rng.choice([0.125,0.25,0.6,0.9]),0.125
            for cap in sorted({0,1,n//4,n//2,n,n+3}):
                plan = plan_prefix(x,epsilon,delta,max_head=cap)
                order, expected = independent_oracle(x,epsilon,delta,cap)
                assert list(plan.ordered_top_indices) == order
                got = plan.chosen
                assert (got.support_upper_bound,got.actual_draws_if_chosen,
                        got.head_size,got.requested_samples,got.residual_mass)==expected
                assert len(plan.candidates)==plan.cap+1
                entries,meta = construct_surrogate(x,epsilon,delta,plan=plan,rng=rng)
                assert meta['realized_support']==len(entries)<=meta['support_upper_bound']
                assert meta['actual_draws']==got.actual_draws_if_chosen
                assert meta['selection_calls_during_construction']==0
                if got.method == 'exact-input':
                    assert dict(entries)=={j:v for j,v in enumerate(x) if v}
                cases += 1
    # A cutoff tie rho=epsilon must use zero samples and preserve the stored head.
    x = [3,1]
    plan = plan_prefix(x,0.25,0.125,max_head=1)
    assert plan.chosen.method=='head-only' and plan.chosen.head_size==1
    entries,meta = construct_surrogate(x,0.25,0.125,plan=plan,rng=NoDraws())
    assert entries==[(0,3+0j)] and meta['requested_samples']==meta['actual_draws']==0
    # Exact fallback precedes RNG use, even for an astronomically large budget.
    exact = plan_prefix([1,2,3,4],1e-300,0.125,max_head=0)
    _,exact_meta = construct_surrogate([1,2,3,4],1e-300,0.125,plan=exact,rng=NoDraws())
    assert exact_meta['requested_samples']>10**500
    assert exact_meta['actual_draws']==0 and exact_meta['copied_nonzeros']==4
    # All-zero input also validates parameters, produces no draws, and copies nothing.
    zero = plan_prefix([0]*8,0.5,0.125)
    entries,zero_meta = construct_surrogate([0]*8,0.5,0.125,plan=zero,rng=NoDraws())
    assert entries==[] and zero_meta['actual_draws']==zero_meta['copied_nonzeros']==0
    # Draw count is distinct from coalesced support: all samples may hit one index.
    sample = plan_prefix([1]*1024,0.9,0.5,max_head=0)
    generator = RepeatedDraw()
    entries,sample_meta = construct_surrogate([1]*1024,0.9,0.5,plan=sample,rng=generator)
    assert sample.chosen.method=='sample-tail'
    assert sample_meta['actual_draws']==generator.calls==sample_meta['requested_samples']
    assert sample_meta['realized_support']==sample_meta['sampled_distinct_indices']==1
    assert sample_meta['actual_draws']>1 and sample_meta['copied_nonzeros']==0
    # Full prefixes strictly improve a geometric grid on its missed head-only cutoff.
    compressible = [10]*3+[1/61]*61
    prefix_plan = plan_prefix(compressible,.1,.125,max_head=4)
    geometric = min((c for c in prefix_plan.candidates if c.head_size in (0,1,2,4)),
                    key=lambda c:(c.support_upper_bound,c.actual_draws_if_chosen,c.head_size))
    assert prefix_plan.chosen.head_size==3 and prefix_plan.chosen.support_upper_bound==3
    assert geometric.support_upper_bound==4
    # BFPRT tie order and extreme rank positions: verify against a full-sort oracle.
    selection_checks = []
    for family in [list(range(1024)),list(reversed(range(1024))),[1]*1024]:
        for cap in [1,17,128,1000]:
            checked = plan_prefix(family,0.6,0.125,max_head=cap)
            order,_ = independent_oracle(family,0.6,0.125,cap)
            assert list(checked.ordered_top_indices)==order
            selection_checks.append(dict(checked.selection_stats))
    invalid = 0
    for epsilon,delta in [(0,.5),(1,.5),(-1,.5),(math.nan,.5),(.5,0),(.5,1),(.5,math.inf),(None,.5)]:
        rejects(lambda:plan_prefix([0]*4,epsilon,delta)); invalid += 1
        rejects(lambda:construct_surrogate([0]*8,epsilon,delta,plan=zero,rng=NoDraws())); invalid += 1
    for cap in [-1,1.5,True]:
        rejects(lambda:plan_prefix([1]*4,.5,.5,max_head=cap)); invalid += 1
    for values in [[],[1,2,3],[math.inf,0],[complex(0,math.nan),0]]:
        rejects(lambda:plan_prefix(values,.5,.5)); invalid += 1
    for values,epsilon,delta in [([1,3],.25,.125),([3,1],.3,.125),([3,1],.25,.2),([3,1,0,0],.25,.125)]:
        rejects(lambda:construct_surrogate(values,epsilon,delta,plan=plan,rng=NoDraws())); invalid += 1
    report = {'status':'PASS','all_prefix_oracle_cases':cases,
              'focused_selection_cases':len(selection_checks),
              'invalid_or_stale_rejections':invalid,
              'cutoff_metadata':meta,'zero_metadata':zero_meta,
              'exact_fallback':{'requested_budget_decimal_digits':len(str(exact_meta['requested_samples'])),
                                'actual_draws':exact_meta['actual_draws'],
                                'copied_nonzeros':exact_meta['copied_nonzeros']},
              'coalescing_metadata':sample_meta,'selection_counts':selection_checks,
              'strict_geometric_improvement':{'full_prefix_support':3,'geometric_support':4},
              'scope':'Deterministic BFPRT and exact all-prefix optimum for the implemented numeric objective; not probability or floating-point certification.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='selection_counts'},indent=2))


if __name__=='__main__':
    main()
