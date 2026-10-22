#!/usr/bin/env python3
"""Fresh finite corroboration of the ALG-042 affine-cover obstruction.

Authored independently for this task. Standard library only. No repository
program is imported or executed; no source file is read by these tests.
The all-size proof is THEOREM.md, not a conclusion inferred from these tests.
"""
import itertools
import json
import random


def has_zero_run(x, n, b):
    return '0' * b in format(x, '0%db' % n)


def witness(n, b, maps):
    d = (b + 1) // 2
    assert len(maps) < 1 << d
    digitmask = (1 << d) - 1
    invs = [pow(a, -1, 1 << d) for a, c in maps]
    prefix = 0
    branch_counts = []
    for m in range(0, n - d + 1, d):
        bad = {(-inv * ((a * prefix + c) >> m)) & digitmask
               for (a, c), inv in zip(maps, invs)}
        assert len(bad) <= len(maps)
        v = next(v for v in range(1 << d) if v not in bad)
        prefix += v << m
        branch_counts.append((1 << d) - len(bad))
    mask = (1 << n) - 1
    outputs = [(a * prefix + c) & mask for a, c in maps]
    assert all(not has_zero_run(y, n, b) for y in outputs)
    return prefix, min(branch_counts, default=1 << d)


def literal_marker(ell, n, b, L):
    for h in range(max(n-L, 0), n+1):
        bits = format(ell & ((1 << h)-1), '0%db' % h)
        for t in range(1, L+1):
            if h < 2*b+t:
                continue
            # rev_t(k) has the same endpoint/run predicate as k itself.
            middle = bits[b:b+t]
            if (bits[:b] == '0'*b and bits[b+t:2*b+t] == '0'*b
                    and middle[0] == middle[-1] == '1'
                    and '0'*b not in middle):
                return True
    return False


def main():
    out = {'status': 'PASS', 'proof_status': 'finite corroboration only'}

    # Exhaust the carry formula and bijection at many lower prefixes,
    # with higher bits deliberately set to all ones as an independence test.
    count = 0
    for n in range(1, 6):
        N = 1 << n
        for d in range(1, min(n, 3)+1):
            for m in range(0, n-d+1, d):
                for P in range(1 << m):
                    for a in range(1, N, 2):
                        for c in range(N):
                            images = []
                            for v in range(1 << d):
                                high = ((1 << (n-m-d))-1) << (m+d)
                                x = P + (v << m) + high
                                actual = (((a*x+c) % N) >> m) & ((1 << d)-1)
                                formula = (a*v + ((a*P+c) >> m)) % (1 << d)
                                assert actual == formula
                                images.append(actual)
                                count += 1
                            assert sorted(images) == list(range(1 << d))
    out['exhaustive_block_formula_evaluations'] = count

    # Every interval placement, including terminal partial aligned blocks.
    windows = 0
    for n in range(1, 130):
        for b in range(1, n+1):
            d = (b+1)//2
            for start in range(n-b+1):
                m = ((start+d-1)//d)*d
                assert start <= m and m+d <= start+b <= n
                windows += 1
    out['all_window_placement_checks'] = windows

    # Exhaust families, checking both a returned witness and the stronger
    # count of simultaneous avoidance points by an independent enumeration.
    families = 0
    for n, b, max_k in [(3, 3, 3), (4, 3, 2)]:
        N = 1 << n
        maps = [(a,c) for a in range(1,N,2) for c in range(N)]
        masks = []
        for a,c in maps:
            mask = sum(1 << x for x in range(N)
                       if not has_zero_run((a*x+c)%N,n,b))
            masks.append(mask)
        d = (b+1)//2
        q,r = divmod(n,d)
        for k in range(max_k+1):
            for ids in itertools.combinations(range(len(maps)),k):
                selected = [maps[j] for j in ids]
                x,_ = witness(n,b,selected)
                common = (1 << N)-1
                for j in ids:
                    common &= masks[j]
                assert common & (1 << x)
                assert common.bit_count() >= ((1 << d)-k)**q * (1 << r)
                families += 1
    out['exhaustive_map_families_and_count_bounds'] = families

    # Literal source-marker containment and affine-image versus inverse-map
    # direction on deliberately small toy parameters outside b>=7.
    marker_counts = []
    rng = random.Random(420221026)
    cover_checks = 0
    for b in range(1,4):
        L = 1 << (b-1)
        for n in range(L+2*b, L+2*b+3):
            N = 1 << n
            E = {x for x in range(N) if literal_marker(x,n,b,L)}
            assert E and all(has_zero_run(x,n,b) for x in E)
            marker_counts.append({'n':n,'b':b,'L':L,'size_E':len(E)})
            k = (1 << ((b+1)//2))-1
            for _ in range(10):
                forward = [(rng.randrange(N//2)*2+1,rng.randrange(N)) for i in range(k)]
                inverse = [(pow(a,-1,N),(-pow(a,-1,N)*c)%N) for a,c in forward]
                x,_ = witness(n,b,inverse)
                actual_union = {(a*y+c)%N for a,c in forward for y in E}
                assert x not in actual_union
                cover_checks += 1
    out['toy_literal_marker_cases'] = marker_counts
    out['direct_affine_image_cover_checks'] = cover_checks

    # Valid source parameters b>=7, L+2b<=n. These use exact big integers,
    # not exhaustive universe enumeration; the all-size proof remains primary.
    large = []
    for b in range(7,13):
        L = 1 << (b-1)
        d = (b+1)//2
        k = (1 << d)-1
        for tail in [0,1,d-1]:
            n = L+2*b+tail
            N = 1 << n
            maps = [(rng.getrandbits(n)|1,rng.getrandbits(n)) for _ in range(k)]
            x,branches = witness(n,b,maps)
            # Every exact marker has a b-zero run. Direct no-run scanning
            # is sufficient here; exhaustive marker syntax is tested above.
            assert all('0'*b not in format((a*x+c)%N, '0%db'%n) for a,c in maps)
            large.append({'n':n,'b':b,'L':L,'d':d,'maps':k,
                          'min_available_block_digits':branches,
                          'witness_hex':hex(x)})
    out['admissible_parameter_cases'] = large

    # The strict inequality k<2^d matters to this construction: all possible
    # translations modulo 2^d jointly forbid every first-block digit.
    b,n = 7,78
    d = (b+1)//2
    bad = {(-c) % (1 << d) for c in range(1 << d)}
    assert bad == set(range(1 << d))
    out['boundary_control_k_equals_2_to_d'] = 'first-block greedy guarantee correctly fails'

    # Nonunits break the conditional block permutation. This is why the
    # theorem is restricted to source permutations/odd-affine maps.
    assert len({(2*v)%16 for v in range(16)}) == 8
    out['negative_control_even_multiplier'] = 'detected nonbijection'

    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
