#!/usr/bin/env python3
"""Fresh review controls. Candidate tests are not imported.

Only the frozen candidate constructor/executor is exercised, against direct
integer-exponent and formal-coefficient references developed for this review.
"""
import hashlib
import importlib.util
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('frozen_operator', HERE.parent / 'candidate' / 'operator_cores.py')
CAND = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAND)
RNG = random.Random(202610181757)
OUT = {'coefficient_controls': [], 'cut_rank_controls': [], 'applications': [],
       'mask_controls': [], 'negative_controls': [], 'counts': {}}
COUNTS = OUT['counts']

def count(key, n=1):
    COUNTS[key] = COUNTS.get(key, 0) + n

def bits(n):
    return [i // 2 if i % 2 == 0 else n - 1 - i // 2 for i in range(n)]

def physical(code, positions):
    value = 0
    for i, position in enumerate(positions):
        if (code >> i) & 1:
            value += 2 ** position
    return value

def g(t, root, n, p):
    return pow(root, -(t * (t + 1) // 2) % (2 ** n), p)

def primitive(n, p, embedding=1):
    assert all(p % d for d in range(2, math.isqrt(p) + 1))
    N = 2 ** n
    assert (p - 1) % N == 0
    for a in range(2, p):
        z = pow(a, (p - 1) // N, p)
        if pow(z, N, p) == 1 and pow(z, N // 2, p) != 1:
            return pow(z, embedding, p)
    raise AssertionError('No supplied test root')

def gauss_rank(rows, p):
    # Streaming independent elimination, reducing incoming rows by prior pivots.
    pivots = {}
    for incoming in rows:
        row = [int(v) % p for v in incoming]
        for col, previous in pivots.items():
            if row[col]:
                fac = row[col]
                for c in range(col, len(row)):
                    row[c] = (row[c] - fac * previous[c]) % p
        at = next((i for i, v in enumerate(row) if v), None)
        if at is not None:
            inv = pow(row[at], p - 2, p)
            pivots[at] = [(v * inv) % p for v in row]
            pivots = dict(sorted(pivots.items()))
    return len(pivots)

def unfold_rows(n, k, p, w, kind, mask=None):
    before, after = bits(n)[:k], bits(n)[k:]
    for lp in range(2 ** k):
        ell_left = physical(lp, before)
        for sp in range(2 ** k):
            s_left = physical(sp, before)
            row = []
            for lc in range(2 ** (n-k)):
                ell = ell_left + physical(lc, after)
                accept = mask is None or (ell >> (n-mask[0])) in mask[1]
                for sc in range(2 ** (n-k)):
                    source = s_left + physical(sc, after)
                    entry = g(ell-source, w, n, p) if kind == 'C' else pow(w, ell*source % (2**n), p)
                    row.append(entry if accept else 0)
            yield row

class Metered(int):
    multiplications = 0
    additions = 0
    def __mul__(self, other):
        Metered.multiplications += 1
        return Metered(int(self) * int(other))
    __rmul__ = __mul__
    def __add__(self, other):
        Metered.additions += 1
        return Metered(int(self) + int(other))
    __radd__ = __add__
    def __mod__(self, p):
        return Metered(int(self) % p)

def independent_core_check(n, p, embedding):
    w = primitive(n, p, embedding)
    Metered.multiplications = Metered.additions = 0
    pure_constant_multiplications = 0
    def account_pure_constants(frame, event, argument):
        nonlocal pure_constant_multiplications
        if event == 'call' and frame.f_code is CAND.prepare.__code__:
            return
        if event == 'call' and frame.f_code.co_name == 'mul' and frame.f_code.co_filename == CAND.__file__:
            if not isinstance(frame.f_locals['a'], Metered) and not isinstance(frame.f_locals['b'], Metered):
                pure_constant_multiplications += 1
    sys.setprofile(account_pure_constants)
    try:
        cores, bill = CAND.prepare(n, Metered(w), p)
    finally:
        sys.setprofile(None)
    observed_multiplications = Metered.multiplications + pure_constant_multiplications
    assert observed_multiplications == bill['multiplications']
    bridge = next(k for k in range(1,n+1) if (k+1)//2 >= n-k)
    assert bridge == bill['bridge']
    ranks = [1] + [2 * 2 ** min((k+1)//2,n-k) - 1 for k in range(1,n)] + [1]
    assert bill['ranks'] == ranks
    slot_count = 0
    for k, core in enumerate(cores, 1):
        old_radius, new_radius = (ranks[k-1]-1)//2, (ranks[k]-1)//2
        expected = {}
        position = bits(n)[k-1]
        for old in range(-old_radius, old_radius+1):
            for ellbit in (0,1):
                for sourcebit in (0,1):
                    delta = ellbit-sourcebit
                    for new in range(-new_radius,new_radius+1):
                        if k < bridge:
                            target = old + delta * 2**position if k%2 else old
                            if new != target:
                                continue
                            future = delta * 2**position
                            value = g(future,w,n,p) * pow(w,-old*future % (2**n),p) % p
                        elif k == bridge:
                            future = delta * 2**position + new * 2**((k+1)//2)
                            value = g(future,w,n,p) * pow(w,-old*future % (2**n),p) % p
                        else:
                            target = delta + 2*new if k%2 else delta * 2**(n-k) + new
                            if old != target:
                                continue
                            value = 1
                        expected[(old,ellbit,sourcebit,new)] = value
        actual = {(a,l,s,b):int(v) for a,l,s,b,v in core}
        assert len(actual) == len(core), 'duplicate transition'
        assert actual == expected, (n,k)
        slot_count += len(core)
    assert slot_count == bill['scalar_core_slots']
    A,M=2**(bridge//2),2**(n-bridge)
    exact_prep_multiplications=9*n-1+3*sum(ranks[:bridge-1])-(bridge-1)+2*(A-1)*(4*M-1)+12*M
    assert observed_multiplications == exact_prep_multiplications
    assert bill['bridge_table_slots'] == (2*A-1)*(4*M-1)
    count('independent_core_coefficients', slot_count)
    # Recontract via backward row vectors; do not invoke candidate evaluate.
    samples = [(a,b) for a in range(2**n) for b in range(2**n)] if n <= 5 else [(RNG.randrange(2**n),RNG.randrange(2**n)) for _ in range(41)]
    for ell,source in samples:
        right = {0:1}
        for k in range(n,0,-1):
            position = bits(n)[k-1]
            left = {}
            for a,l,s,b,v in cores[k-1]:
                if l == ((ell>>position)&1) and s == ((source>>position)&1) and b in right:
                    left[a] = (left.get(a,0) + int(v)*right[b]) % p
            right = left
        assert right.get(0,0) == g(ell-source,w,n,p)
        count('backward_pair_contractions')
    OUT['coefficient_controls'].append({'n':n,'p':p,'embedding':embedding,'slots':slot_count,'metered_multiplications':observed_multiplications})
    return [[(a,l,s,b,int(v)) for a,l,s,b,v in core] for core in cores],bill,w

def reference_intermediate(n,k,bridge,x,w,p):
    before,after = bits(n)[:k],bits(n)[k:]
    j,m = (k+1)//2,n-k
    radius = 2**min(j,m)-1
    expected = []
    feasible = 0
    dead_nonzero = 0
    for op in range(2**k):
        outprefix = physical(op,before)
        for source_tail in range(2**m):
            source_suffix = physical(source_tail,after)
            for state in range(-radius,radius+1):
                total = 0
                if k < bridge:
                    low_source = outprefix % (2**j) - state
                    ok = 0 <= low_source < 2**j
                    if ok:
                        for source_prefix in range(2**k):
                            source_head = physical(source_prefix,before)
                            if source_head % (2**j) == low_source:
                                total += x[source_head+source_suffix] * g(outprefix-source_head,w,n,p)
                else:
                    output_middle = source_suffix // (2**j) + state
                    ok = 0 <= output_middle < 2**m
                    output = outprefix + output_middle * 2**j
                    for source_prefix in range(2**k):
                        source_head = physical(source_prefix,before)
                        total += x[source_head+source_suffix] * g(output-source_head-source_suffix,w,n,p)
                total %= p
                expected.append(total)
                feasible += int(ok)
                dead_nonzero += int(not ok and total != 0)
    return expected,feasible,dead_nonzero

def application_check(n,p,kind):
    cores,bill,w = independent_core_check(n,p,3)
    N = 2**n
    x = [RNG.randrange(p) for _ in range(N)] if kind == 'random' else [int(i == N//3) for i in range(N)]
    selected = [N-1,0,N//2,N-1] + list(range(1,N,3))
    tracked = [[(a,l,s,b,Metered(v)) for a,l,s,b,v in core] for core in cores]
    Metered.multiplications = Metered.additions = 0
    seen = []
    def observe(k,actual):
        if n <= 7:
            expected,feasible,dead = reference_intermediate(n,k,bill['bridge'],x,w,p)
            assert actual == expected, (n,k)
            assert feasible == N * 2**min((k+1)//2,n-k)
            seen.append({'stage':k,'slots':len(expected),'feasible':feasible,'nonzero_dead':dead})
            count('independent_intermediate_values',len(expected))
    y,ledger = CAND.apply_dense(tracked,n,x,p,selected,observe)
    observed_mul,observed_add = Metered.multiplications,Metered.additions
    expected = [sum(x[s]*g(ell-s,w,n,p) for s in range(N))%p for ell in selected]
    assert y == expected
    assert observed_mul == ledger['multiplications'] == N//2*bill['scalar_core_slots']
    assert observed_add == ledger['additions'] == observed_mul
    assert ledger['zero_initializations'] == N*sum(bill['ranks'][1:])
    assert ledger['peak_two_frontier_slots'] == N*max(a+b for a,b in zip(bill['ranks'][:-1],bill['ranks'][1:]))
    # Explicitly verify Fourier conversion and recurrence-generated diagonals.
    in_diagonal,out_diagonal=[],[]
    a,b,ra,rb=1,1,1,w
    for s in range(N):
        in_diagonal.append(a);out_diagonal.append(b)
        assert a == pow(w,s*(s-1)//2%N,p)
        assert b == pow(w,s*(s+1)//2%N,p)
        a,b=a*ra%p,b*rb%p
        ra,rb=ra*w%p,rb*w%p
    cx,_=CAND.apply_dense(cores,n,[a*b%p for a,b in zip(x,in_diagonal)],p,selected)
    fft=[v*out_diagonal[ell]%p for ell,v in zip(selected,cx)]
    direct=[sum(x[s]*pow(w,ell*s%N,p) for s in range(N))%p for ell in selected]
    assert fft==direct
    OUT['applications'].append({'n':n,'p':p,'input':kind,'selected_count_with_duplicates':len(selected),'arithmetic_multiplications':observed_mul,'arithmetic_additions':observed_add,'peak_frontier_slots':ledger['peak_two_frontier_slots'],'zero_initializations':ledger['zero_initializations'],'intermediates':seen})

def rank_check(n,p,embedding):
    w=primitive(n,p,embedding)
    for k in range(1,n):
        j,m=(k+1)//2,n-k
        actual={kind:gauss_rank(unfold_rows(n,k,p,w,kind),p) for kind in ('C','F')}
        assert actual['C']==min(2**(j+1)-1,2**(m+1)-1,2**(n-j))
        assert actual['F']==4**min(j,m)
        OUT['cut_rank_controls'].append({'n':n,'p':p,'embedding':embedding,'cut':k,**actual})
        count('exact_full_unfolding_ranks',2)

def mask_check(n,k,K,headers,p):
    assert k//2>=K
    w=primitive(n,p,5)
    j,m=(k+1)//2,n-k
    mask=(K,set(headers))
    actual={kind:gauss_rank(unfold_rows(n,k,p,w,kind,mask),p) for kind in ('C','F')}
    assert actual['C']==min(2**(j+1)-1,2**(m+1)-1,2**(n-j))
    assert actual['F']==4**min(j,m)
    before=bits(n)[:k]
    prefix_count=sum((physical(op,before)>>(n-K)) in headers for op in range(2**k))
    assert prefix_count*2**K==len(headers)*2**k
    bridge=next(s for s in range(1,n+1) if (s+1)//2>=n-s)
    frontier_count=None
    if k<bridge:
        feasible=0
        for op in range(2**k):
            outprefix=physical(op,before)
            if (outprefix>>(n-K)) not in headers:
                continue
            a=outprefix%(2**j)
            for state in range(-(2**j-1),2**j):
                if 0<=a-state<2**j:
                    feasible+=2**m
        assert feasible*2**K==len(headers)*2**n*2**j
        frontier_count=feasible
    OUT['mask_controls'].append({'n':n,'cut':k,'K':K,'headers':headers,'accepted_prefixes':prefix_count,'prebridge_feasible_entries':frontier_count,**actual})
    count('exact_masked_ranks',2)

for n in range(1,7):
    independent_core_check(n,193,1)
    rank_check(n,193,5)
for n in (7,8):
    independent_core_check(n,769,5)
    rank_check(n,769,3)
for n in (10,13,18):
    independent_core_check(n,786433,7)
for n in range(1,10):
    application_check(n,12289,'random')
for n in (2,4,7):
    application_check(n,769,'impulse')
for args in [(5,2,1,[1],193),(6,3,1,[0],193),(7,4,2,[0,3],769),(8,4,2,[1],769),(8,5,2,[0,1,3],769)]:
    mask_check(*args)
# Characteristic-three finite-field nonzero-form fraction, exhaustive all dense inputs.
n,p,w=1,3,2
for x0 in range(p):
    for x1 in range(p):
        cores,_=CAND.prepare(n,w,p)
        y,_=CAND.apply_dense(cores,n,[x0,x1],p)
        assert y==[(x0*g(ell,w,n,p)+x1*g(ell-1,w,n,p))%p for ell in range(2)]
count('small_characteristic_complete_inputs',9)
# n=2 optimal two-state constructor, separately from the uniform width-three code.
p,n=17,2;w=primitive(n,p)
for ell in range(4):
    for source in range(4):
        low=(ell&1)-(source&1);high=(ell>>1)-(source>>1)
        value=g(low,w,n,p)*g(2*high,w,n,p)*pow(p-1,(low%2)*high%2,p)%p
        assert value==g(ell-source,w,n,p)
count('optimal_exception_pairs',16)
# Exact all-size exponent/rank/storage controls, with a range different from candidate.
for n in range(1,1501):
    W=2**((n+1)//3)
    bridge=next(k for k in range(1,n+1) if (k+1)//2>=n-k)
    A,M=2**(bridge//2),2**(n-bridge)
    rs=[1]+[2*2**min((k+1)//2,n-k)-1 for k in range(1,n)]+[1]
    slots=4*sum(rs[:bridge-1])+4*rs[bridge-1]*rs[bridge]+4*sum(rs[bridge+1:])
    assert W//2<=A<=W and W//2<=M<=W
    assert W*W<=slots<=16*W*W+32*W
    closed_form=(16*W*W+8*W-4*n-24 if n%3==0 else 16*W*W+16*W-4*n-24 if n%3==1 else 8*W*W+8*W-4*n-24)
    assert slots==closed_form
    assert sum(rs[1:])<=16*W
    count('all_size_ledger_controls')
# Targeted negative controls.
try:
    CAND.prepare(4,primitive(3,193),193)
    raise AssertionError('imprimitive root accepted')
except ValueError:
    OUT['negative_controls'].append('Wrong root order rejected')
assert gauss_rank(unfold_rows(2,1,17,primitive(2,17),'C'),17)==2
OUT['negative_controls'].append('Uniform width-three n=2 is not the minimum')
assert gauss_rank(unfold_rows(5,3,193,primitive(5,193),'F'),193)==16
OUT['negative_controls'].append('DFT width cannot inherit convolution width seven')
cores,ledger=CAND.prepare(5,primitive(5,193),193)
x=list(range(32));y,_=CAND.apply_dense(cores,5,x,193)
w=primitive(5,193)
assert y!=[sum(x[s]*pow(w,ell*s%32,193) for s in range(32))%193 for ell in range(32)]
OUT['negative_controls'].append('Unscaled convolution is not the DFT')
assert any(z['nonzero_dead'] for a in OUT['applications'] for z in a['intermediates'])
OUT['negative_controls'].append('A dead suffix state is not generally a zero scalar')
OUT['summary']={k:len(OUT[k]) for k in ('coefficient_controls','cut_rank_controls','applications','mask_controls','negative_controls')}
OUT['summary'].update(COUNTS)
serialized=json.dumps(OUT,indent=2,sort_keys=True)+'\n'
(HERE/'INDEPENDENT_RESULTS.json').write_text(serialized)
print(json.dumps(OUT['summary'],sort_keys=True))
print('sha256='+hashlib.sha256(serialized.encode()).hexdigest())
