"""Exact basis audit and a charged same-target related-query comparator."""
from collections import Counter
import json
from pathlib import Path
import random
import sys
from rational_reuse import (prepare_rational, solve_band, apply_band,
                            generate_related_pair, verified_output, Counted)
from fixed_kernel import prepare
from operators import prepare_sparse, horner_c
from prior_exact_arithmetic import PrimeField, CyclotomicField

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'fft_qweyl_resolvent_research'))
from fast_hc import prepare_fast, apply_hc


def total(count):
    return sum(count.values())


def main():
    cases = []
    basis = mixed = singular = rejected = 0
    fields = [(PrimeField(65537), n) for n in (4,8,16,32)]
    fields += [(PrimeField(998244353), n) for n in (4,8,16,32)]
    fields += [(CyclotomicField(n), n) for n in (4,8)]
    rng = random.Random(20261009)
    for field,n in fields:
        q = field.root(n)
        kernel = prepare(field,n,q)
        sparse = prepare_sparse(field,n,q)
        # 2 can itself have dyadic root order in a finite field: choose safely.
        shift = next(field.integer(v) for v in range(2,100)
                     if field.power(field.integer(v),n) != field.one)
        plan = prepare_rational(field,n,q,shift)
        vectors = [[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
        vectors += [[field.integer(rng.randrange(-5,6)) for _ in range(n)] for _ in range(3)]
        for index,x in enumerate(vectors):
            y,_ = horner_c(field,sparse,kernel.kernel,x)
            xq,yq,counts = generate_related_pair(field,plan,x,y)
            truth,_ = horner_c(field,sparse,kernel.kernel,xq)
            assert yq == truth
            assert apply_band(field,plan.source,xq) == x
            assert apply_band(field,plan.target,yq) == y
            checked,detail = verified_output(field,plan,x,y,xq)
            assert checked == yq and detail['expensive_transform_calls']==0
            if index < n: basis+=1
            else: mixed+=1
        for bad_shift in (field.one,q):
            try: prepare_rational(field,n,q,bad_shift)
            except ValueError: singular+=1
            else: raise AssertionError('singular root shift accepted')
        bad=list(xq);bad[0]=field.add(bad[0],field.one)
        try: verified_output(field,plan,x,y,bad)
        except ValueError: rejected+=1
        else: raise AssertionError('wrong relation accepted')
        cases.append(dict(field=getattr(field,'p',f'Q(zeta_{n})'),n=n,
                          preparation=plan.preparation,pair_online=counts,
                          verified_online=detail))
    benchmark=[]
    field=PrimeField(998244353)
    for n in (32,64,128,256):
        eta=field.root(2*n);q=field.mul(eta,eta)
        fast=prepare_fast(field,n,eta)
        x=[field.integer(rng.randrange(-100,101)) for _ in range(n)]
        y,anchor=apply_hc(field,fast,x)
        plan=prepare_rational(field,n,q,field.integer(2))
        queries=16
        related=Counter(fast.preparation)
        related.update(plan.preparation);related.update(anchor['field_operations'])
        baseline=Counter(fast.preparation);baseline.update(anchor['field_operations'])
        # Both workloads generate the same related inputs. Charge their common
        # grading/source-solver preparation to the fresh-transform baseline too.
        baseline.update(plan.grading['preparation'])
        baseline.update(plan.source.preparation)
        baseline['neg'] += 1
        last_x,last_y=x,y
        supports=[]
        for _ in range(queries):
            current_x,source_count=solve_band(field,plan.source,last_x)
            current_y,detail=verified_output(field,plan,last_x,last_y,current_x)
            truth,fresh=apply_hc(field,fast,current_x)
            assert current_y==truth
            # Query input generation is included in BOTH competing workloads.
            related.update(source_count);related.update(detail['field_operations'])
            baseline.update(source_count);baseline.update(fresh['field_operations'])
            supports.append(sum(a!=b for a,b in zip(current_x,last_x)))
            last_x,last_y=current_x,current_y
        benchmark.append(dict(n=n,additional_queries=queries,
                              cold_graph_field_operations=total(related),
                              cold_fresh_field_operations=total(baseline),
                              graph_ledger=dict(related),fresh_ledger=dict(baseline),
                              minimum_changed_coordinates=min(supports),
                              all_outputs_materialized=True,
                              complete_relation_verification_charged=True,
                              baseline_extra_root='supplied primitive 2N-th root'))
    report=dict(status='PASS',cases=cases,full_basis_vectors=basis,mixed_vectors=mixed,
                singular_shift_rejections=singular,bad_relation_rejections=rejected,
                comparisons=benchmark,
                model='Exact field arithmetic; related-query anchor and all preparation paid; not CPU timings.')
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))


if __name__=='__main__': main()
