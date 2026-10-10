#!/usr/bin/env python3
"""Independently authored exact-integer stress checks, not uploaded execution.

Proof is in STREAMING_ROBUST_SYNTHESIS.md. These checks test bookkeeping,
adversarial orders and boundaries; finite tests do not replace its proof.
"""
import itertools
import json
import random
from pathlib import Path


def robust_select(values, mu=0, bscale=2, tie='first', rng=None, verify=True):
    reps=[]
    counts=[]
    bad=0
    good=0
    decrements=0
    max_occupied=0
    for n,z in enumerate(values,1):
        is_bad=abs(z-mu)>bscale
        bad+=is_bad
        good+=not is_bad
        matching=[j for j,c in enumerate(reps) if (z-c)**2<=4*bscale*bscale]
        if matching:
            j=matching[0] if tie=='first' else matching[-1] if tie=='last' else rng.choice(matching)
            counts[j]+=1
        elif len(reps)<5:
            reps.append(z)
            counts.append(1)
        else:
            decrements+=1
            pairs=[(c,h-1) for c,h in zip(reps,counts) if h>1]
            reps=[c for c,h in pairs]
            counts=[h for c,h in pairs]
        max_occupied=max(max_occupied,len(reps))
        if verify:
            assert len(reps)==len(counts)<=5
            assert all(h>0 for h in counts)
            assert all(abs(reps[i]-reps[j])>2*bscale for i in range(len(reps)) for j in range(i))
            near=[h for c,h in zip(reps,counts) if abs(c-mu)<=3*bscale]
            far=[h for c,h in zip(reps,counts) if abs(c-mu)>3*bscale]
            assert len(near)<=3
            assert sum(far)+2*decrements<=bad
            assert sum(near)>=good-4*decrements
            # Each full decrement consumes 5 old counts and discards 1 arrival.
            assert sum(counts)==n-6*decrements
            if 4*bad<n:
                assert near
                assert max(near)>max(far,default=0)
    chosen=None if not counts else reps[max(range(len(counts)),key=lambda j:counts[j])]
    if 4*bad<len(values):
        assert chosen is not None and abs(chosen-mu)<=3*bscale
    return chosen, decrements, max_occupied


def one_counter(values,bscale=1):
    candidate=None
    count=0
    for z in values:
        if count==0:
            candidate=z
            count=1
        elif abs(z-candidate)<=2*bscale:
            count+=1
        else:
            count-=1
    return candidate


def main():
    rng=random.Random(9012026)
    exhaustive=0
    dec_cases=0
    max_dec=0
    # Exhaust all short words. Includes exact ±B, ±2B, ±3B boundaries.
    alphabet=(-8,-6,-4,-2,0,2,4,6,8)
    for length in range(1,7):
        for values in itertools.product(alphabet, repeat=length):
            _,d,_=robust_select(values)
            exhaustive+=1
            dec_cases+=bool(d)
            max_dec=max(max_dec,d)
    # All permutations of a designed full-counter cancellation multiset.
    # Here mu=0,B=2. Stored -5,0,5 are near; ±12 are far.
    ordered_cases=0
    for seq in itertools.permutations((-12,-5,0,5,12,2)):
        robust_select(seq)
        ordered_cases+=1
    random_cases=0
    certified_cases=0
    full_slots=0
    for it in range(16000):
        length=rng.choice((7,11,15,19,23,31,47,63,95,127))
        # Sometimes hit or exceed the proved boundary to exercise decrement accounting.
        b=rng.randrange(length//3+1) if it%3==0 else rng.randrange((length-1)//4+1)
        good=[rng.choice((-2,-1,0,1,2)) for _ in range(length-b)]
        bad=[rng.choice((-20,-12,-7,-6,-5,-3,3,5,6,7,12,20)) for _ in range(b)]
        seq=good+bad
        rng.shuffle(seq)
        if it%5==0:
            # Correlate order with signs while retaining bad/good counts.
            seq.sort(reverse=bool(it%2))
        for tie in ('first','last','random'):
            _,d,occupied=robust_select(seq,tie=tie,rng=rng)
            random_cases+=1
            certified_cases+=4*b<length
            dec_cases+=bool(d)
            max_dec=max(max_dec,d)
            full_slots+=occupied==5
    # Strong bad-first and bad-last cases with exact boundary good points.
    adversarial=0
    for repeat in range(1,61):
        bad=[-20,-5,5,20]*repeat
        good=[-2]*(8*repeat+1)+[2]*(8*repeat+1)
        for seq in (bad+good, good+bad, good[::2]+bad+good[1::2]):
            for tie in ('first','last'):
                robust_select(seq,tie=tie)
                adversarial+=1
    witness=(-2,-1,-1,1,1,1,10)
    assert one_counter(witness)==10
    assert sum(abs(z)<=1 for z in witness)==5
    result={
        'status':'pass',
        'arithmetic':'exact Python integers; no uploaded modules',
        'exhaustive_short_sequences':exhaustive,
        'designed_permutations':ordered_cases,
        'randomized_order_and_tie_cases':random_cases,
        'random_cases_in_proved_below_quarter_regime':certified_cases,
        'adversarial_bad_first_or_last_cases':adversarial,
        'cases_with_full_decrement':dec_cases,
        'cases_reaching_five_slots':full_slots,
        'maximum_observed_decrement_events':max_dec,
        'one_counter_counterexample':{'samples':list(witness),'target':0,'B':1,'good':5,'returned':10},
        'checked_invariants':[
            'representatives pairwise farther than 2B',
            'at most three representatives within 3B of target',
            'surviving far mass + 2D <= bad samples',
            'near mass >= good samples - 4D',
            'total counter mass = processed samples - 6D',
            'largest counter near whenever bad < processed/4'
        ],
        'scope':'Finite invariant checks support the separate all-size proof; no statistical performance or floating stability claim.'
    }
    path=Path(__file__).with_name('streaming_check_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
