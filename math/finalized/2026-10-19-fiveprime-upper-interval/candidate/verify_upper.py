#!/usr/bin/env python3
"""Self-authored exact controls for 3q<d<4q, q>5 prime.

No historical scripts, floating arithmetic, external dependencies, or square-mask
census are used. Every root sum uses original indices and integer coefficients.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNTS = Counter()


def write(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def positions(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask -= low


class OriginalFourier:
    def __init__(self, q):
        self.q, self.n = q, 5*q
        self.e5 = q*pow(q, -1, 5)
        self.eq = 5*pow(5, -1, q)
        n = self.n
        assert (self.e5+self.eq)%n == 1
        assert self.e5*self.eq%n == 0
        assert self.e5*self.e5%n == self.e5%n
        assert self.eq*self.eq%n == self.eq%n
        self.indices = [[self.index(a,b) for b in range(q)] for a in range(5)]
        assert sorted(sum(self.indices, [])) == list(range(n))
        for r in range(n):
            for c in range(n):
                assert (r*c-self.e5*(r%5)*(c%5)-self.eq*(r%q)*(c%q))%n == 0
                COUNTS['original_CRT_phase_products'] += 1

    def index(self, a, b):
        return (a*self.e5+b*self.eq)%self.n

    def support(self, baseline, fibers):
        return sum(1 << self.index(u,v) for u in range(5) for v in range(self.q)
                   if u in baseline or v in fibers)

    def root_sum(self, support, difference):
        # alpha=zeta^e5, beta=zeta^eq. The original monomial zeta^k is
        # alpha^(k mod5) beta^(k modq). Eliminate alpha^4 and beta^(q-1).
        q = self.q
        grid = [[0]*q for _ in range(5)]
        for c in positions(support):
            exponent = difference*c % self.n
            grid[exponent%5][exponent%q] += 1
        return tuple(grid[a][b]-grid[a][q-1]-grid[4][b]+grid[4][q-1]
                     for a in range(4) for b in range(q-1))

    def fibers(self, support):
        return [sum((support>>self.index(u,v))&1 for u in range(5))
                for v in range(self.q)]


def transpose(rows, n):
    answer = [0]*n
    for r, mask in enumerate(rows):
        for c in positions(mask):
            answer[c] |= 1<<r
    return answer


def check_full_mask(F, rows, d, valid, label):
    cols = transpose(rows, F.n)
    assert all(mask.bit_count()==d for mask in rows+cols)
    report = {'q':F.q, 'N':F.n, 'degree':d, 'label':label,
              'row_and_column_regular':True, 'expected_equality':valid,
              'gram_counts':{}, 'nonzero_witnesses':{}}
    for orientation, supports in [('row',rows), ('column',cols)]:
        tally = Counter()
        for r in range(F.n):
            for s in range(F.n):
                difference = r-s if orientation=='row' else s-r
                common = supports[r]&supports[s]
                remainder = F.root_sum(common,difference)
                COUNTS['full_Gram_entries'] += 1
                if r==s:
                    assert remainder == (d,)+(0,)*(4*(F.q-1)-1)
                    tally['diagonal_correct'] += 1
                    continue
                kind = ('order_q' if difference%5==0 else
                        'order_5' if difference%F.q==0 else 'primitive')
                zero = not any(remainder)
                tally[kind+('_zero' if zero else '_nonzero')] += 1
                if valid:
                    assert zero, (label,orientation,r,s,remainder)
                if not zero and orientation not in report['nonzero_witnesses']:
                    report['nonzero_witnesses'][orientation] = {
                        'original_indices':[r,s], 'character_order_type':kind,
                        'difference_mod_N':difference%F.n,
                        'common_original_support':list(positions(common)),
                        'exact_basis_remainder':list(remainder)}
        if not valid:
            assert tally['primitive_nonzero']>0
            if orientation=='row':
                assert tally['order_q_nonzero']==0
        report['gram_counts'][orientation]=dict(tally)
    if F.q==7 and not valid:
        report['original_index_binary_rows'] = [format(x,f'0{F.n}b')[::-1] for x in rows]
    return report


def positive_mask(n, d):
    quotient=n//d
    assert d*quotient==n
    return [sum(1<<c for c in range(n) if c%quotient==r//d) for r in range(n)]


def negative_mask(F, twisted):
    rows=[0]*F.n
    for a in range(5):
        A={a,(a+1)%5,(a+2)%5}
        for b in range(F.q):
            special=((a+1)*b+a)%F.q if twisted else b
            rows[F.index(a,b)]=F.support(A,{special})
    return rows


def mixed_cycle_controls(F):
    q=F.q
    degree_types={d:set() for d in range(3*q+1,4*q)}
    q7_examples=[]
    for ell in range(4):
        for A_tuple in combinations(range(5),ell):
            A=set(A_tuple)
            for B_bits in range((1<<q)-1):
                B=set(positions(B_bits))
                mask=F.support(A,B)
                d=mask.bit_count()
                assert d==ell*q+(5-ell)*len(B)
                # Check maximal/canonical cycle sets, not merely a representation.
                actual_lines={u for u in range(5)
                              if all((mask>>F.index(u,v))&1 for v in range(q))}
                actual_fibers={v for v in range(q)
                               if all((mask>>F.index(u,v))&1 for u in range(5))}
                assert actual_lines==A and actual_fibers==B
                COUNTS['canonical_mixed_cycle_supports'] += 1
                if d in degree_types:
                    assert B
                    degree_types[d].add((ell,len(B)))
                    if q==7 and d==3*q+2 and len(B)>1 and A_tuple==tuple(range(ell)) and B==set(range(len(B))):
                        q7_examples.append({'ell':ell,'fiber_count':len(B),'degree':d,
                                            'original_support':list(positions(mask)),
                                            'minimum_total_fibers_with_other_rows_nonempty':q-1+len(B),
                                            'available_fibers':q})
    for d, types in degree_types.items():
        assert d>q+4
        expected={(ell,f) for ell in range(4) for f in range(q)
                  if ell*q+(5-ell)*f==d}
        assert types==expected
        singles=[ell for ell in range(4) if 5+ell*(q-1)==d]
        assert singles==([3] if d==3*q+2 else [])
        COUNTS['interval_degree_reductions'] += 1
    # Enumeration-free packing statement used by the proof: q nonempty
    # disjoint subsets of q fibers all have size one. Each possible violation
    # would require at least q-1+f fibers.
    for f in range(2,q+1):
        assert q-1+f>q
        COUNTS['mixed_fiber_packing_obstructions'] += 1
    for r in range(F.n):
        exceptional={s for s in range(F.n) if s%5==r%5 or s%q==r%q}
        assert len(exceptional)==q+4 and r in exceptional
        COUNTS['coverage_exceptional_row_counts'] += 1
    return {'q':q, 'types_before_disjointness':
            {str(d):[list(t) for t in sorted(types)] for d,types in degree_types.items()},
            'forced_degree_after_disjointness':3*q+2,
            'q7_mixed_shapes_at_residual_degree':q7_examples}


def overlap_controls(F):
    q=F.q
    triples=[set(x) for x in combinations(range(5),3)]
    counts=Counter()
    witnesses={}
    for A in triples:
        for C in triples:
            h=len(A&C)
            assert h in (1,2,3)
            for v in range(q):
                r=F.support(A,{v})
                for w in range(q):
                    common=r&F.support(C,{w})
                    f=F.fibers(common)
                    if v!=w:
                        assert f[v]==f[w]==3
                        assert all(f[t]==h for t in range(q) if t not in (v,w))
                        for db in range(1,q):
                            rem=F.root_sum(common,F.index(0,db))
                            assert (not any(rem))==(A==C)
                            COUNTS['same_group_balance_checks'] += 1
                    else:
                        assert f[v]==5
                        assert all(f[t]==h for t in range(q) if t!=v)
                    for da in range(1,5):
                        for db in range(1,q):
                            diff=F.index(da,db)
                            rem=F.root_sum(common,diff)
                            zero=not any(rem)
                            assert zero==(A==C and v!=w)
                            COUNTS['primitive_overlap_checks'] += 1
                            key=('equal' if A==C else 'different')+'_baselines_'+('same' if v==w else 'different')+'_fibers'
                            counts[key+('_zero' if zero else '_nonzero')] += 1
                            witness_key=f'h{h}_'+('same' if v==w else 'different')+'_fibers'
                            if not zero and witness_key not in witnesses:
                                witnesses[witness_key]={'A':sorted(A),'C':sorted(C),
                                    'special_fibers':[v,w], 'fiber_counts':f,
                                    'original_difference':diff,
                                    'common_original_support':list(positions(common)),
                                    'exact_basis_remainder':list(rem)}
    return {'q':q,'classification_counts':dict(counts),
            'exact_zero_condition':'A=C and v!=w', 'nonzero_certificates':witnesses}


def partner_controls(q):
    counts=Counter()
    if q==7:
        maps=permutations(range(q))
        kind='all permutations'
    else:
        maps=([(m*b+s)%q for b in range(q)] for m in range(1,q) for s in range(q))
        kind='all affine permutations'
    for perm in maps:
        assert len(set(perm))==q
        counts['permutations'] += 1
        inverse={v:b for b,v in enumerate(perm)}
        for b in range(q):
            for special in range(q):
                choices=set(range(q))-{b,inverse[special]}
                assert len(choices)>=q-2>0
                assert all(bp!=b and perm[bp]!=special for bp in choices)
                counts[f'{len(choices)}_eligible_rows'] += 1
                COUNTS['partner_selection_checks'] += 1
    return {'q':q,'scope':kind,'counts':dict(counts)}


def main():
    bindings=json.loads((ROOT/'SOURCE_BINDINGS.json').read_text())
    for b in bindings:
        data=(ROOT/b['copy']).read_bytes()
        assert len(data)==b['bytes'] and sha256(data).hexdigest()==b['sha256']
    positives=[]; negatives=[]; mixed=[]; overlaps=[]; partners=[]
    for q in [7,11,13,17,19,23]:
        F=OriginalFourier(q)
        if q in [7,11,13,17]:
            for d in [1,5,q,F.n]:
                positives.append(check_full_mask(F,positive_mask(F.n,d),d,True,'divisor_control'))
            for twisted in [False,True]:
                negatives.append(check_full_mask(F,negative_mask(F,twisted),3*q+2,False,
                                  'distinct_affine_maps' if twisted else 'common_fiber_map'))
        if q in [7,11]:
            mixed.append(mixed_cycle_controls(F))
            overlaps.append(overlap_controls(F))
            partners.append(partner_controls(q))
    write('POSITIVE_CONTROLS.json',positives)
    write('NEGATIVE_CONTROLS.json',negatives)
    write('MIXED_CYCLE_CONTROLS.json',mixed)
    write('OVERLAP_CERTIFICATES.json',overlaps)
    write('PARTNER_CONTROLS.json',partners)
    result={'status':'PASS','counts':dict(COUNTS),'source_bindings_checked':len(bindings),
            'positive_parameters':[[x['q'],x['degree']] for x in positives],
            'negative_parameters':[[x['q'],x['degree'],x['label']] for x in negatives],
            'arithmetic':'Exact integer original-index cyclotomic rational-basis reduction',
            'floating_point_used':False,'external_writes':False,
            'scope':'Finite corroboration of a symbolic theorem; no exhaustive square-mask search'}
    write('RESULTS.json',result)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
