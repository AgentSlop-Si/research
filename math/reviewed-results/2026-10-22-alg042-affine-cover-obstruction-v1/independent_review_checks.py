#!/usr/bin/env python3
"""Independent finite audit. No candidate code is imported or executed.

The main checks use direct full-universe enumeration and direct digit trials,
not the candidate's modular-inverse digit constructor.
"""
import hashlib
import itertools
import json
import random


def zeros(y, n, b):
    mask = (1 << b) - 1
    return any(((y >> s) & mask) == 0 for s in range(n - b + 1))


def strong(y, n, d):
    return all(((y >> m) % (1 << d)) != 0
               for m in range(0, n - d + 1, d))


def direct_trial(n, b, maps, high_ones=False):
    d = (b + 1) // 2
    B = 1 << d
    x = 0
    minimum = B
    for m in range(0, n - d + 1, d):
        good = []
        for v in range(B):
            new = x + (v << m)
            if all(((a * new + c) % (1 << (m+d))) >> m
                   for a, c in maps):
                good.append(v)
        assert len(good) >= B - len(maps)
        minimum = min(minimum, len(good))
        x += good[-1] << m
    r = n % d
    if high_ones:
        x += ((1 << r) - 1) << (n-r)
    assert all(not zeros((a*x+c) % (1 << n), n, b) for a,c in maps)
    return x, minimum


def literal_cylinders(n,b):
    L = 1 << (b-1)
    E = set()
    cylinders = 0
    for h in range(max(0,n-L),n+1):
        for t in range(1,min(L,h-2*b)+1):
            for k in range(1 << t):
                word = format(k, '0%db' % t)
                if word[0] != '1' or word[-1] != '1' or '0'*b in word:
                    continue
                prefix = '0'*b + word[::-1] + '0'*b
                free = h-2*b-t
                for suffix in range(1 << free):
                    f = (int(prefix,2) << free) + suffix
                    cylinders += 1
                    for ell in range(f,1 << n,1 << h):
                        assert zeros(ell,n,b)
                        E.add(ell)
    return E,cylinders


def main():
    rng = random.Random(913772451)
    out = {'status':'PASS','basis':'all-size proof primary; independent controls corroborate'}
    # Enumerate every output word instead of checking interval algebra.
    implication = 0
    for n in range(1,15):
        for b in range(1,n+1):
            d = (b+1)//2
            for y in range(1 << n):
                assert not strong(y,n,d) or not zeros(y,n,b)
                implication += 1
    out['exhaustive_word_implications'] = implication

    # All maps, all input words, all complete digit positions, signed integer
    # representatives and every high-bit continuation occur in these checks.
    carries = 0
    for n in range(1,7):
        N = 1 << n
        for a0 in range(1,N,2):
            for c0 in range(N):
                a,c = a0-N,c0-N
                for x in range(N):
                    y = (a*x+c) % N
                    for d in range(1,min(n,3)+1):
                        for m in range(0,n-d+1,d):
                            P = x % (1 << m)
                            v = (x >> m) % (1 << d)
                            predicted = (a*v + (a*P+c)//(1 << m)) % (1 << d)
                            assert predicted == (y >> m) % (1 << d)
                            carries += 1
    out['signed_representative_carry_checks'] = carries

    # Exhaustive families evaluated by direct masks, with a second count for
    # the stronger block condition, not merely the zero-run condition.
    families = 0
    minima = []
    for n,b,maxk in [(3,3,3),(4,3,3),(5,4,3)]:
        N = 1 << n
        d = (b+1)//2
        entries = set()
        for a in range(1,N,2):
            for c in range(N):
                good = sum(1 << x for x in range(N) if not zeros((a*x+c)%N,n,b))
                block = sum(1 << x for x in range(N) if strong((a*x+c)%N,n,d))
                entries.add((good,block))
        entries = sorted(entries)
        for k in range(maxk+1):
            lower = ((1 << d)-k)**(n//d) * (1 << (n%d))
            minimum_good = N
            minimum_block = N
            for chosen in itertools.combinations(entries,k):
                good = block = (1 << N)-1
                for gm,bm in chosen:
                    good &= gm
                    block &= bm
                assert block.bit_count() >= lower
                assert block & ~good == 0
                minimum_good = min(minimum_good,good.bit_count())
                minimum_block = min(minimum_block,block.bit_count())
                families += 1
            minima.append({'n':n,'b':b,'k':k,'distinct_mask_pairs':len(entries),
                           'claimed_lower':lower,'minimum_avoidance':minimum_good,
                           'minimum_strong_block_count':minimum_block})
    out['exhaustive_distinct_mask_families'] = families
    out['exact_family_minima'] = minima

    # Actual source cylinders generated outwards from reversed allowed words,
    # rather than reusing a marker membership predicate.
    source_cases = []
    for b in range(1,5):
        n = (1 << (b-1)) + 2*b
        E, cylinders = literal_cylinders(n,b)
        assert E
        k = (1 << ((b+1)//2))-1
        N = 1 << n
        for _ in range(12):
            maps = [(2*rng.randrange(N//2)+1,rng.randrange(N)) for _ in range(k)]
            inverse = [(pow(a,-1,N),-pow(a,-1,N)*c) for a,c in maps]
            x,_ = direct_trial(n,b,inverse,high_ones=True)
            assert all(x not in {(a*y+c)%N for y in E} for a,c in maps)
        source_cases.append({'n':n,'b':b,'cylinders':cylinders,'E_size':len(E)})
    out['literal_source_cylinders'] = source_cases

    # Boundary-sized families with deliberately distinct first-block
    # exclusions. Large signed representatives and arbitrary top bits test
    # quotient conventions. Random families independently exhaust n<=12.
    small = 0
    for n in range(3,13):
        N = 1 << n
        for b in range(1,n+1):
            d = (b+1)//2
            k = (1 << d)-1
            lower = ((1 << d)-k)**(n//d) * (1 << (n%d))
            for _ in range(12):
                maps = [(2*rng.randrange(N//2)+1-N,rng.randrange(-N,N)) for _ in range(k)]
                x,_ = direct_trial(n,b,maps,high_ones=True)
                count = sum(all(not zeros((a*y+c)%N,n,b) for a,c in maps) for y in range(N))
                assert count >= lower
                small += 1
    out['random_full_universe_count_checks'] = small
    large = []
    for b in range(7,13):
        L = 1 << (b-1)
        d = (b+1)//2
        B = 1 << d
        for remainder in range(d):
            n = L+2*b
            n += (remainder-n) % d
            N = 1 << n
            maps = [(rng.getrandbits(n)|1, c + (rng.getrandbits(n)<<d)) for c in range(B-1)]
            # All a == 1 mod B force B-1 distinct first-block exclusions.
            maps = [((a//B)*B+1,c) for a,c in maps]
            x,minimum = direct_trial(n,b,maps,high_ones=True)
            assert minimum == 1
            large.append({'n':n,'b':b,'k':B-1,'remainder':remainder,
                          'witness_sha256':hashlib.sha256(str(x).encode()).hexdigest()})
    out['adversarial_admissible_cases'] = large

    # Deliberately broken arguments, with explicit counterexamples.
    assert ((3*1)//2)%2 != 0  # dropping the prefix carry at m=1 fails
    assert strong(33,6,3) and zeros(33,6,4)  # over-large digit size
    assert len({(2*v)%16 for v in range(16)}) == 8
    assert {(-c)%16 for c in range(16)} == set(range(16))
    reverse3 = lambda x: int(format(x,'03b')[::-1],2)
    assert 0%2 == 4%2 and reverse3(0)%2 != reverse3(4)%2
    out['negative_controls'] = {
        'carry_omission':'a=3, P=1, m=1 changes the next output digit',
        'digit_size_too_large':'n=6, b=4, d=3, x=33 has nonzero aligned blocks but a four-zero run',
        'even_multiplier':'2v modulo 16 is not a permutation',
        'strict_family_size':'16 shifts forbid every first four-bit digit',
        'bit_reversal':'3-bit reversal separates x=0 and x=4 modulo 2 despite equal input prefixes'
    }
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
