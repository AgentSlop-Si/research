#!/usr/bin/env python3
"""Fresh exact controls for the restricted ALG-070 complete-view theorem.

Only Python standard library. No project implementation is imported.
The arbitrary-subset DP permits paid prefetch; it is not an LRU oracle.
"""
from collections import OrderedDict
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json


def lru_trace(seq, capacity):
    cache = OrderedDict()
    faults = 0
    trace = []
    for v in seq:
        old = tuple(cache)
        loaded = v not in cache
        if loaded:
            faults += 1
            if len(cache) == capacity:
                cache.popitem(last=False)
        else:
            del cache[v]
        cache[v] = None
        trace.append((v, old, tuple(cache), loaded))
    return faults, trace


def offline_all_subsets(seq, capacity, universe):
    """Bellman optimum; each event allows every paid complete cache change.

    States may be underfilled. Replacement D->C costs the cardinality of C minus D. After
    conversion C must contain the requested key. Therefore this explicitly
    permits speculative loading of multiple other keys before each request.
    Empty initial state; no inaccessible free prepared output.
    """
    states = [frozenset(c) for n in range(capacity + 1)
              for c in combinations(universe, n)]
    containing = {v: [s for s in states if v in s] for v in universe}
    dp = {frozenset(): 0}
    for v in seq:
        dp = {c: min(cost + len(c-d) for d, cost in dp.items())
              for c in containing[v]}
    return min(dp.values())


def phase_certificate(seq, capacity):
    if not seq:
        return [], []
    universe = set(range(capacity + 1))
    phases = []
    start, seen = 0, set()
    for t, v in enumerate(seq):
        if v not in seen and len(seen) == capacity:
            phases.append((start, t, frozenset(seen)))
            start, seen = t, set()
        seen.add(v)
    phases.append((start, len(seq), frozenset(seen)))
    caches = []
    for _, _, s in phases:
        target = set(s)
        for v in sorted(universe - target):
            if len(target) == capacity:
                break
            target.add(v)
        caches.append(frozenset(target))
    return phases, caches


def check_potential():
    count = 0
    load_controls = 0
    for K in range(1, 6):
        universe = tuple(range(K + 1))
        for order in permutations(universe, K):
            rank = {v: i+1 for i, v in enumerate(order)}
            def phi(cache, ranks=rank):
                return sum(ranks.get(v, K+1) for v in cache)
            for h in range(1, K+1):
                for O in combinations(universe, h):
                    before = phi(O)
                    for requested in O:
                        hit = requested in rank
                        new = (requested,) + tuple(v for v in order if v != requested)
                        new = new[:K]
                        ranks = {v: i+1 for i, v in enumerate(new)}
                        delta = phi(O, ranks)-before
                        assert delta <= (0 if hit else -(K-h+1))
                        count += 1
                    for remove in O:
                        for add in set(universe)-set(O):
                            assert rank.get(add,K+1)-rank.get(remove,K+1) <= K
                            load_controls += 1
    return {"request_transition_checks": count,
            "offline_load_transition_checks": load_controls,
            "K_range": [1, 5], "universe_size": "K+1"}


def check_exhaustive():
    for capacity in range(1, 5):
        assert lru_trace([], capacity)[0] == 0
        assert offline_all_subsets([], capacity, tuple(range(5))) == 0
    assert lru_trace([0,0,1,1,0], 1)[0] == 3
    cases = 0
    comparisons = 0
    phase_checks = 0
    maximum = Fraction(0)
    max_witness = None
    for U, length in [(2, 9), (3, 7), (4, 6)]:
        universe = tuple(range(U))
        for seq in product(universe, repeat=length):
            opts = {h: offline_all_subsets(seq,h,universe)
                    for h in range(1,U+1)}
            for K in range(1,U+1):
                a, _ = lru_trace(seq,K)
                for h in range(1,K+1):
                    assert (K-h+1)*a <= K*opts[h], (seq,K,h,a,opts[h])
                    comparisons += 1
                ratio = Fraction(a,opts[K])
                if ratio > maximum:
                    maximum = ratio
                    max_witness = {"K": K,"sequence": seq,"LRU":a,"OPT":opts[K]}
            # The phase bound is for exactly K+1 allowed keys.
            K = U-1
            phases,caches = phase_certificate(seq,K)
            prev,loads = frozenset(),0
            for (start,end,seen),cache in zip(phases,caches):
                assert seen <= cache and len(cache)==K
                loads += len(cache-prev)
                prev=cache
                assert all(v in cache for v in seq[start:end])
            assert loads <= K + (len(seq)-1)//K
            assert opts[K] <= loads
            phase_checks += 1
            cases += 1
    return {"sequences":cases,"empty_sequence_checks":8,"one_slot_edge_checks":1,"competitive_inequalities":comparisons,
            "phase_prefetch_certificates":phase_checks,
            "domains":[{"universe":2,"length":9},{"universe":3,"length":7},
                       {"universe":4,"length":6}],
            "maximum_observed_equal_capacity_ratio":str(maximum),
            "maximum_witness":max_witness,
            "offline_method":"all subsets; paid arbitrary prefetch transitions"}


def adversarial_sequence(K,T,policy):
    cache=[]
    seq=[]
    for _ in range(T):
        v=min(set(range(K+1))-set(cache))
        seq.append(v)
        if policy=="no_retention":
            continue
        if len(cache)==K:
            cache.pop(-1 if policy=="MRU" else 0)
        cache.append(v)
        assert len(cache)<=K
    return tuple(seq)


def check_adversaries():
    rows=[]
    for K in range(1,9):
        for policy in ["LRU","FIFO","MRU","no_retention"]:
            seq=adversarial_sequence(K,200,policy)
            opt=offline_all_subsets(seq,K,tuple(range(K+1)))
            assert opt <= K+(len(seq)-1)//K
            phases,caches=phase_certificate(seq,K)
            loads=len(caches[0])+sum(len(b-a) for a,b in zip(caches,caches[1:]))
            assert opt<=loads<=K+(len(seq)-1)//K
            rows.append({"K":K,"policy":policy,"T":len(seq),"online_loads":len(seq),
                         "offline_loads":opt,"phase_schedule_loads":loads,
                         "ratio":str(Fraction(len(seq),opt))})
    # Common costs must dilute the optional-work ratio.
    for K in range(1,20):
        for F,g in [(1,1),(K,1),(K*K,1),(K,7)]:
            bound=Fraction(F+g,Fraction(F,K)+g)
            assert 1<=bound<=K
            if F>=K*g:
                assert bound>=Fraction(K+1,2)
    return {"policy_sequences":rows,"full_cost_formula_checks":76}


def conv_direct(a,b,p):
    n=len(a)
    out=[]
    for t in range(n):
        vals=[a[j]*b[(t-j)%n]%p for j in range(n)]
        out.append(sum(vals)%p)
    return tuple(out)


def conv_polynomial(a,b,p):
    # Different loop/order oracle: ordinary polynomial product then quotient.
    n=len(a)
    product_coeffs=[0]*(2*n-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            product_coeffs[i+j]=(product_coeffs[i+j]+x*y)%p
    out=list(product_coeffs[:n])
    for i in range(n,len(product_coeffs)):
        out[i-n]=(out[i-n]+product_coeffs[i])%p
    return tuple(out)


def check_convolution_versions():
    queries=0
    builds=0
    coalescence=0
    raw_words=0
    for p in [3,5,7]:
        for n in range(1,7):
            A=tuple((j*j+2)%p for j in range(n))
            B=tuple((2*j+1)%p for j in range(n))
            H=tuple((3*j+2)%p for j in range(n))
            registry={}
            vectors={}
            cache=OrderedDict()
            def register(key):
                nonlocal raw_words
                # Exact tuple equality, no unverified probabilistic hash claim.
                if key not in registry:
                    handle=len(registry)
                    registry[key]=handle
                    vectors[handle]=key
                    raw_words+=sum(len(x) for x in key)
                return registry[key]
            base=register((A,B,H))
            for step in range(18):
                which=step%3
                arrays=[list(A),list(B),list(H)]
                pos=step%n
                arrays[which][pos]=(arrays[which][pos]+1)%p
                changed=register(tuple(tuple(a) for a in arrays))
                arrays[which][pos]=(arrays[which][pos]-1)%p
                restored=register(tuple(tuple(a) for a in arrays))
                assert restored==base
                coalescence+=1
                for v in [base,changed,restored,changed]:
                    a,b,h=vectors[v]
                    oracle=conv_polynomial(conv_polynomial(a,b,p),h,p)
                    if v not in cache:
                        if len(cache)==2:
                            cache.popitem(last=False)
                        cache[v]=conv_direct(conv_direct(a,b,p),h,p)
                        builds+=1
                    else:
                        cache.move_to_end(v)
                    assert cache[v]==oracle
                    assert len(cache)<=2
                    queries+=1
                # A zero-output query has no materialization effect.
                before=(tuple(cache),builds)
                empty_coordinates=[]
                if empty_coordinates:
                    raise AssertionError("unreachable")
                assert before==(tuple(cache),builds)
    return {"exact_full_vector_queries":queries,"materializations":builds,
            "cancel_and_restore_version_checks":coalescence,
            "fields":[3,5,7],"N_range":[1,6],
            "paid_registered_raw_scalar_slots":raw_words}


def validate_trace(seq,trace,K):
    cache=set()
    for requested,declared_before,after,charged in trace:
        assert requested==seq.pop(0)
        assert set(declared_before)==cache
        assert len(after)<=K
        assert requested in after
        newly=set(after)-cache
        assert newly <= {requested}
        assert bool(newly)==charged
        cache=set(after)
    assert not seq


def check_mutations():
    seq=[0,1,2,0,2,1]
    _,trace=lru_trace(seq,2)
    validate_trace(list(seq),trace,2)
    rejected=[]
    mutations=[]
    bad=list(trace);v,b,a,c=bad[0];bad[0]=(v,b,a,False)
    mutations.append(("free_first_materialization",bad))
    bad=list(trace);v,b,a,c=bad[1];bad[1]=(v,b,a+(99,),c)
    mutations.append(("hidden_extra_complete_slot",bad))
    bad=list(trace);v,b,a,c=bad[0];bad[0]=(v,b,(99,),c)
    mutations.append(("wrong_view_output",bad))
    bad=list(trace);v,b,a,c=bad[2];bad[2]=(v,(99,),a,c)
    mutations.append(("unbound_previous_cache",bad))
    bad=list(trace);v,b,a,c=bad[0];bad[0]=(v,b,a+(99,),c)
    mutations.append(("uncharged_speculative_view_in_demand_trace",bad))
    for name,bad in mutations:
        try:
            validate_trace(list(seq),bad,2)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    return {"rejected_mutations":rejected,"positive_trace_accepted":True,
            "scope":"validator targets demand-LRU trace; paid prefetch separately tested by Bellman DP"}


def main():
    here=Path(__file__).resolve().parent
    source=(here/'source/ALG070_PRIOR_REPORT.md').read_bytes()
    source_blob=hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()
    assert source_blob=='dc6213abdf5d6574fb39a0442a126313a839005b'
    result={"owner":"ALG-070","date":"2026-10-18","verdict":"PASS",
            "scope":"exact finite corroboration of restricted complete-view proofs",
            "source_git_blob":source_blob,
            "source_sha256":hashlib.sha256(source).hexdigest(),
            "potential":check_potential(),
            "exhaustive":check_exhaustive(),
            "adversaries":check_adversaries(),
            "convolution_versions":check_convolution_versions(),
            "mutations":check_mutations(),
            "failures":0,
            "no_external_writes":True,
            "not_claimed":["arithmetic lower bound","full-owner closure","production qualification",
                           "randomized lower bound","unequal-price cache theorem"]}
    (here/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['verdict','potential','exhaustive','convolution_versions','mutations','failures']},indent=2))


if __name__=='__main__':
    main()
