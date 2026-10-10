"""Exact full-register basis audit: source, all arbitrary targets, and dirty w."""
import hashlib
import json
import random
from pathlib import Path
from prior_affine_reuse import (prepare,execute,execute_scalar,expand_scalar,
    charge,inverse,apply_t,apply_k,anchor_word)
from terminal_anchor import (terminal_anchor_word,scalar_count,difference_word,
                             difference_scalar_count)


def expected(plan,batches,initial,support):
    n,p=plan['n'],plan['p']
    result=initial[:]
    source=[initial[j] if j in support else 0 for j in range(n)]
    for r in range(batches):
        transformed=apply_t(plan,source)
        for i,value in enumerate(transformed):
            result[(2+r)*n+i]=(result[(2+r)*n+i]+value)%p
        source=apply_k(plan,source)
    return result


def main():
    rows=[]
    basis_count=random_count=0
    rng=random.Random(20261009)
    for prime in (65537,998244353):
        for n in (2,4,8,16):
            plan=prepare(n,prime)
            supports=[list(range(n)),[0],[n-1],sorted({0,n//2,n-1}),[]]
            for batches in (1,2,4):
                for support in supports:
                    word=terminal_anchor_word(plan,batches,support)
                    scalar=expand_scalar(word,prime)
                    backwards=inverse(word,prime)
                    difference=difference_word(plan,batches,support)
                    difference_scalar=expand_scalar(difference,prime)
                    difference_backwards=inverse(difference,prime)
                    count=charge(word)
                    assert len(scalar)==count['expanded_scalar_instructions']==scalar_count(n,batches,support)
                    assert len(difference_scalar)==difference_scalar_count(n,batches,support)
                    assert all(not (n<=gate[1]<2*n) for gate in word)
                    size=(batches+2)*n
                    for coordinate in range(size):
                        initial=[int(i==coordinate) for i in range(size)]
                        wanted=expected(plan,batches,initial,set(support))
                        got=execute(word,initial,prime)
                        assert got==wanted
                        assert execute_scalar(scalar,initial,prime)==wanted
                        assert execute(difference,initial,prime)==wanted
                        assert execute_scalar(difference_scalar,initial,prime)==wanted
                        assert execute(difference_backwards,wanted,prime)==initial
                        assert execute(backwards,got,prime)==initial
                        assert got[:2*n]==initial[:2*n]
                        basis_count+=1
                    for _ in range(3):
                        initial=[rng.randrange(prime) for _ in range(size)]
                        wanted=expected(plan,batches,initial,set(support))
                        assert execute_scalar(scalar,initial,prime)==wanted
                        assert execute_scalar(difference_scalar,initial,prime)==wanted
                        random_count+=1
                    rows.append({'prime':prime,'n':n,'batches':batches,'support':support,
                                 'full_state_basis_vectors':size,'scalar_instructions':len(scalar),
                                 'difference_scalar_instructions':len(difference_scalar),
                                 'charge':count,'all_checks_passed':True})
    comparisons=[]
    for n,batches in ((32,4),(64,4),(128,8)):
        plan=prepare(n)
        old=charge(anchor_word(plan,batches))['expanded_scalar_instructions']
        new=charge(terminal_anchor_word(plan,batches))['expanded_scalar_instructions']
        sparse_support=sorted({0,n//4,n//2,3*n//4,n-1})
        sparse=charge(terminal_anchor_word(plan,batches,sparse_support))['expanded_scalar_instructions']
        difference=charge(difference_word(plan,batches))['expanded_scalar_instructions']
        difference_sparse=charge(difference_word(plan,batches,sparse_support))['expanded_scalar_instructions']
        assert old-new==6*(batches-1)*(n-1)
        assert old-difference==2*(batches-1)*(8*n-7)
        comparisons.append({'n':n,'batches':batches,'prior_first_anchor_dense':old,
                            'terminal_anchor_dense':new,'terminal_anchor_sparse':sparse,
                            'difference_dense':difference,'difference_sparse':difference_sparse,
                            'sparse_support':sparse_support,
                            'terminal_dense_instructions_saved':old-new,
                            'difference_dense_instructions_saved':old-difference})
    report={'status':'PASS','cases':len(rows),'full_state_basis_vectors':basis_count,
            'random_full_states':random_count,'comparisons':comparisons,'cases_detail':rows,
            'scope':'Exact target-difference compiler and sparse projected-source specialization; no fresh arbitrary FFT speed claim.',
            'unchanged_baseline_sha256':hashlib.sha256(Path(__file__).with_name('prior_affine_reuse.py').read_bytes()).hexdigest()}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases_detail'},indent=2))


if __name__=='__main__':
    main()
