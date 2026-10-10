"""Exact product, relation, cold/warm, and one-parent comparison audit."""
import importlib.util
import json
from pathlib import Path
from random import Random

from multiparent import (Ledger, SeedCache, baseline_batch, make_seed_cache,
                        polynomial_batch, secant_batch, signed_patch)

ROOT = Path(__file__).resolve().parent


def digits(value, n):
    return list(value.to_bytes(n, 'little'))


def integer(value):
    return int.from_bytes(bytes(value), 'little')


def assert_products(pairs, result):
    for (a,b), out in zip(pairs, result['outputs']):
        assert len(out) == 2*len(a)
        assert integer(out) == integer(a)*integer(b)
        assert all(0 <= v < 256 for v in out)
    assert len(result['outputs']) == len(pairs)
    assert result['counts']['full_output_digit_writes'] == 2*len(pairs)*len(pairs[0][0])


def summary(result):
    return {k:v for k,v in result.items() if k != 'outputs'}


def affine_pairs(n, q, both=False, descending=False):
    rng = Random(7123+n+q)
    da = [rng.randrange(1,8) for _ in range(n)]
    db = [rng.randrange(1,8) for _ in range(n)]
    a0 = [rng.randrange(1,15) for _ in range(n)]
    b0 = [rng.randrange(1,15) for _ in range(n)]
    fixed_b = [rng.randrange(1,256) for _ in range(n)]
    pairs = []
    for i in range(q):
        t = q-1-i if descending else i
        a = [u+t*v for u,v in zip(a0,da)]
        b = [u+t*v for u,v in zip(b0,db)] if both else list(fixed_b)
        assert max(a+b) < 256
        pairs.append((a,b))
    return pairs


def main():
    rows = []
    product_checks = 0
    for n in (1, 16, 64, 1024):
        pairs = affine_pairs(n, 12)
        baseline = baseline_batch(pairs)
        secant = secant_batch(pairs)
        poly = polynomial_batch(pairs)
        for result in (baseline, secant, poly):
            assert_products(pairs, result)
            product_checks += len(pairs)
        assert secant['counts']['seed_multiplications'] == 2
        assert secant['residual_supports'] == [0]*10
        assert poly['degrees'] == [1,0]
        assert poly['counts']['seed_multiplications'] == 2
        # Every coordinate and every actual signed-numeric difference is dense.
        pair_supports = []
        for i in range(len(pairs)):
            for j in range(i+1,len(pairs)):
                coordinate = sum(u != v for u,v in zip(pairs[i][0],pairs[j][0]))
                delta = integer(pairs[j][0])-integer(pairs[i][0])
                numeric = sum(v != 0 for v in delta.to_bytes(n,'little'))
                assert coordinate == numeric == n
                pair_supports.append(numeric)
        rows.append(dict(case='same_B_dense_first_zero_second', n=n, queries=len(pairs),
                         baseline=summary(baseline), secant=summary(secant),
                         polynomial=summary(poly),
                         all_pair_first_difference_support_min=min(pair_supports)))

    for descending in (False, True):
        pairs = affine_pairs(64, 12, both=True, descending=descending)
        result = polynomial_batch(pairs)
        assert_products(pairs,result)
        product_checks += len(pairs)
        assert result['degrees'] == [1,1]
        assert result['counts']['seed_multiplications'] == 3
        assert result['schedule'][3:] == ['polynomial']*9
        rows.append(dict(case='both_affine_descending' if descending else 'both_affine',
                         n=64,queries=12,result=summary(result)))

    pairs = [(digits(2**40+1234567*i+5329*i*i+77*i**3,8),
              digits(2**39+2323*i+91*i*i,8)) for i in range(12)]
    result = polynomial_batch(pairs)
    assert_products(pairs,result)
    product_checks += len(pairs)
    assert result['degrees'] == [3,2]
    assert result['counts']['seed_multiplications'] == 6
    rows.append(dict(case='cubic_times_quadratic',n=8,queries=12,result=summary(result)))

    pairs = affine_pairs(64, 12)
    pairs = [(digits(integer(a)+10*(i%3),64),b) for i,(a,b) in enumerate(pairs)]
    result = secant_batch(pairs,max_patch=1)
    assert_products(pairs,result)
    product_checks += len(pairs)
    assert max(result['residual_supports']) == 1
    assert result['counts']['seed_multiplications'] == 2
    rows.append(dict(case='signed_sparse_second_difference',n=64,queries=12,result=summary(result)))

    warm_rows=[]
    for mode,both,seeds in ((secant_batch,False,2),(polynomial_batch,True,3)):
        pairs = affine_pairs(64,12,both=both)
        cache,creation = make_seed_cache(pairs,seeds)
        cold = mode(pairs)
        warm = mode(pairs,cache=cache)
        assert cold['outputs'] == warm['outputs']
        assert_products(pairs,warm)
        product_checks += len(pairs)
        assert warm['counts'].get('seed_multiplications',0)==0
        assert creation['counts']['seed_multiplications'] == cold['counts']['seed_multiplications']
        warm_rows.append(dict(mode=mode.__name__,seed_creation=creation,
                              cold=summary(cold),warm=summary(warm)))

    rng=Random(61913)
    fixed_b=[rng.randrange(256) for _ in range(32)]
    pairs=[([rng.randrange(256) for _ in range(32)],list(fixed_b)) for _ in range(12)]
    adversaries=[]
    for mode in (secant_batch,polynomial_batch):
        result=mode(pairs)
        assert_products(pairs,result)
        product_checks+=len(pairs)
        assert result['counts']['seed_multiplications']==len(pairs)
        adversaries.append(dict(mode=mode.__name__,result=summary(result)))

    # Exact same target integers as the original fixed-modulus one-parent graph.
    previous=ROOT.parent/'fft_route_barriers_research'/'correction_graph.py'
    previous_comparison=None
    if previous.exists():
        spec=importlib.util.spec_from_file_location('previous_correction_graph',previous)
        module=importlib.util.module_from_spec(spec)
        import sys
        sys.modules[spec.name]=module
        spec.loader.exec_module(module)
        nhex,q=128,8
        ah=[[i+1]*nhex for i in range(q)]
        bh=[rng.randrange(1,16) for _ in range(nhex)]
        old_base=module.run(ah,bh,base=16,graph=False,numeric_patches=True)
        old_graph=module.run(ah,bh,base=16,graph=True,numeric_patches=True)
        def pack_hex(v): return [v[j]+16*v[j+1] for j in range(0,len(v),2)]
        pairs=[(pack_hex(a),pack_hex(bh)) for a in ah]
        result=secant_batch(pairs)
        assert_products(pairs,result)
        product_checks+=q
        assert result['outputs']==[pack_hex(out) for out in old_graph['outputs']]
        assert result['outputs']==[pack_hex(out) for out in old_base['outputs']]
        assert old_graph['counts']['fresh_products']==q
        assert min(old_graph['correction_supports'])==nhex
        previous_comparison=dict(n_hex=nhex,n_bytes=nhex//2,queries=q,
            original_baseline_scalar_arithmetic=old_base['total_arithmetic'],
            original_graph_scalar_arithmetic=old_graph['total_arithmetic'],
            original_graph_fresh_products=old_graph['counts']['fresh_products'],
            original_all_pair_support_min=min(old_graph['correction_supports']),
            multi_parent=summary(result),
            caution='Models differ: do not add opaque seed calls to old scalar counts or infer a wall-clock ratio.')

    # Focused carry boundaries, including signed residuals through long carries.
    carry_cases=0
    for n in (1,3,32):
        for v in (-(256**n-1),-257,-1,0,1,257,256**n-1):
            c=Ledger()
            patch=signed_patch([v],n+2,c)
            assert sum(sign*digit*256**j for j,sign,digit in patch)==v
            carry_cases+=1
    for length in (1,2,3):
        pairs=[(digits(i+1,2),digits(7-i,2)) for i in range(length)]
        result=polynomial_batch(pairs)
        assert_products(pairs,result)
        product_checks+=length

    invalid=0
    def rejects(fn):
        nonlocal invalid
        try: fn()
        except (ValueError,TypeError): invalid+=1
        else: raise AssertionError('invalid call accepted')
    pairs=affine_pairs(3,8)
    cache,_=make_seed_cache(pairs,2)
    rejects(lambda:secant_batch([],max_patch=2))
    rejects(lambda:secant_batch(pairs,max_patch=-1))
    rejects(lambda:polynomial_batch(pairs,max_degree=4))
    rejects(lambda:polynomial_batch(pairs,max_degree=True))
    rejects(lambda:signed_patch([-255,1],1,Ledger()))
    rejects(lambda:secant_batch([([256],[0])]))
    rejects(lambda:secant_batch([([True],[0])]))
    changed=[(list(a),list(b)) for a,b in pairs]
    changed[0][0][0]^=1
    rejects(lambda:secant_batch(changed,cache=cache))
    rejects(lambda:secant_batch(pairs,cache=SeedCache(4,cache.entries)))
    a,b,p=cache.entries[0]
    rejects(lambda:secant_batch(pairs,cache=SeedCache(3,((a,b,p[:-1]),))))
    changed=[(list(a),list(b)) for a,b in pairs]
    changed[2][1][0]^=1
    rejects(lambda:secant_batch(changed))
    all_cache,_=make_seed_cache(pairs,3)
    rejects(lambda:secant_batch(pairs,cache=all_cache))

    payload=dict(status='PASS',exact_product_comparisons=product_checks,
        signed_carry_checks=carry_cases,invalid_calls_rejected=invalid,
        rows=rows,warm=warm_rows,unrelated_adversaries=adversaries,
        original_one_parent_same_targets=previous_comparison,
        model='Opaque paid M(8n) seed multiplications plus explicit word/digit/carry/output work; no FFT breakthrough.')
    (ROOT/'audit.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:payload[k] for k in ('status','exact_product_comparisons','signed_carry_checks','invalid_calls_rejected')},indent=2))
    if previous_comparison:
        print(json.dumps({k:v for k,v in previous_comparison.items() if k!='multi_parent'},indent=2))


if __name__=='__main__':
    main()
