#!/usr/bin/env python3
"""Fresh exact controls. Uses no supplied verifier and reads no input files."""
from fractions import Fraction
import json
from pathlib import Path

P = 65537
G = 3
SQRT2 = next(a for a in range(2, P) if a*a % P == 2)
INV_SQRT2 = pow(SQRT2, -1, P)
COUNT = {}

def count(key, amount=1):
    COUNT[key] = COUNT.get(key, 0) + amount

def direct_mask(h, f, b, L):
    word = format(f, '0%db' % h) if h else ''
    possible = []
    for t in range(1, L+1):
        if h < 2*b+t:
            continue
        k = word[b:b+t]
        if word[:b] == '0'*b and word[b+t:2*b+t] == '0'*b and k[0] == k[-1] == '1' and '0'*b not in k:
            possible.append(t)
    assert len(possible) <= 1
    return bool(possible)

def step(state, bit, b, L):
    stage, length, zeros = state
    if stage in (2, 3):
        return state
    if stage == 0:
        if bit:
            return (3, 0, 0)
        return (1, 0, 0) if length+1 == b else (0, length+1, 0)
    if length == 0 and bit == 0:
        return (3, 0, 0)
    length += 1
    zeros = 0 if bit else zeros+1
    if zeros == b:
        t = length-b
        return (2 if 1 <= t <= L else 3, t, zeros)
    return (1, length, zeros)

def prepare(n, b, L):
    N = 1 << n
    H0 = max(0, n-L)
    states = [(0, 0, 0)] * (2*N)
    selected = [False] * (2*N)
    S = []
    for h in range(1, n+1):
        for f in range(1 << h):
            idx = (1 << h)+f
            parent = (1 << (h-1))+(f >> 1) # MSB reading trie
            states[idx] = step(states[parent], f & 1, b, L)
            selected[idx] = states[idx][0] == 2 and h >= H0
            assert selected[idx] == (h >= H0 and direct_mask(h, f, b, L))
            count('mask_nodes')
            if selected[idx]:
                S.append((h, f))
    covered = [False] * (2*N)
    A = []
    for h in range(n+1):
        for f in range(1 << h):
            idx = (1 << h)+f
            parent_flag = False if h == 0 else covered[(1 << (h-1)) + (f % (1 << (h-1)))] # low-bit trie
            if selected[idx] and not parent_flag:
                A.append((h, f))
            covered[idx] = selected[idx] or parent_flag
    return S, A, H0

def cylinder(n, h, f):
    return set(range(f, 1 << n, 1 << h))

def closure(n, S):
    seen = {(h, q, f) for h, f in S for q in range(1 << (n-h))}
    todo = list(seen)
    while todo:
        h, q, f = todo.pop()
        if h == 0:
            continue
        M = 1 << (n-h)
        for q0 in (q, q+M):
            child = (h-1, q0, f % (1 << (h-1)))
            if child not in seen:
                seen.add(child)
                todo.append(child)
    return seen

def check_structure(n, S, A, H0):
    N = 1 << n
    E = set().union(*(cylinder(n, h, f) for h, f in S)) if S else set()
    EA = set()
    for h, f in A:
        C = cylinder(n, h, f)
        assert not EA.intersection(C)
        EA.update(C)
    assert E == EA
    assert sum(1 << (n-h) for h, f in A) == len(E)
    assert set(A).issubset(S)
    C = closure(n, S)
    for j in range(H0+1):
        labels = {ell % (1 << j) for ell in E}
        predicted = {(j, q, f) for f in labels for q in range(1 << (n-j))}
        actual = {node for node in C if node[0] == j}
        assert predicted == actual
        assert len(actual) >= len(E)
        count('ancestor_depth_checks')
    count('structure_cases')
    count('explicit_ancestor_nodes', len(C))
    return E

def cyclo_sum(N, exponents):
    coeff = [0] * (N//2)
    for e in exponents:
        e %= N
        if e >= N//2:
            coeff[e-N//2] -= 1
        else:
            coeff[e] += 1
    return tuple(coeff)

def check_orthogonal(n, A):
    N = 1 << n
    rows = [(h, q, f) for h, f in A for q in range(1 << (n-h))]
    for i, (h, q, f) in enumerate(rows):
        for j, (hh, qq, ff) in enumerate(rows):
            exps = [s*(f-ff) for s in range(q, N, 1 << (n-h)) if s % (1 << (n-hh)) == qq]
            got = cyclo_sum(N, exps)
            expected = (1 << h,) + (0,)*(N//2-1) if i == j else (0,)*(N//2)
            assert got == expected
            count('cyclotomic_gram_entries')

def field_packets(n, x, embedding):
    N = 1 << n
    w = pow(G, (P-1)//N * embedding, P)
    assert pow(w, N, P) == 1 and pow(w, N//2, P) == P-1
    roots = [pow(w, j, P) for j in range(N)]
    packet = {}
    for h in range(n+1):
        scale = pow(INV_SQRT2, h, P)
        for q in range(1 << (n-h)):
            for f in range(1 << h):
                packet[h, q, f] = scale * sum(x[s]*roots[s*f % N] for s in range(q, N, 1 << (n-h))) % P
                if h:
                    a = 1 << (h-1)
                    f0, sigma = f % a, f//a
                    v = (packet[h-1, q, f0] + (1 if sigma == 0 else -1)*packet[h-1, q+(1 << (n-h)), f0]) % P
                    got = roots[q*sigma*a % N] * INV_SQRT2 * v % P
                    assert got == packet[h, q, f]
                    count('field_recurrence_values')
    count('field_input_cases')
    return packet, roots

def check_field_conversion(n, b, L, x, embedding):
    N = 1 << n
    S, A, H0 = prepare(n, b, L)
    E = check_structure(n, S, A, H0)
    p, roots = field_packets(n, x, embedding)
    y = [pow(INV_SQRT2, n, P) * sum(x[s]*roots[s*ell % N] for s in range(N)) % P for ell in range(N)]
    recovered = {}
    for h, f in A:
        M = 1 << (n-h)
        scale = pow(INV_SQRT2, n-h, P)
        for v in range(M):
            ell = f+v*(1 << h)
            got = scale * sum(roots[q*v*(1 << h) % N]*p[h, q, f] for q in range(M)) % P
            assert got == y[ell]
            recovered[ell] = got
            count('frontier_fourier_outputs')
    assert set(recovered) == E
    for h, f in S:
        M = 1 << (n-h)
        scale = pow(INV_SQRT2, n-h, P)
        for q in range(M):
            got = scale * sum(roots[-q*v*(1 << h) % N]*recovered[f+v*(1 << h)] for v in range(M)) % P
            assert got == p[h, q, f]
            count('regenerated_packet_outputs')
    a = [x[s]*roots[(s*(s-1)//2) % N] % P for s in range(N)]
    bn = [pow(INV_SQRT2, n, P)*roots[-t*(t+1)//2 % N] % P for t in range(-(N-1), N)]
    conv = [0]*(3*N-2)
    for i, ai in enumerate(a):
        for j, bj in enumerate(bn):
            conv[i+j] = (conv[i+j]+ai*bj) % P
    for ell in range(N):
        assert roots[ell*(ell+1)//2 % N] * conv[N-1+ell] % P == y[ell]
        count('chirp_fourier_outputs')
    # Independent coefficient reconstruction from 2 by 4 block products.
    B = N//2
    reconstructed = [0]*(3*N-2)
    for i in range(2):
        aa = a[i*B:(i+1)*B]
        for j in range(4):
            bb = bn[j*B:(j+1)*B]
            for u, au in enumerate(aa):
                for v, bv in enumerate(bb):
                    reconstructed[(i+j)*B+u+v] = (reconstructed[(i+j)*B+u+v]+au*bv) % P
    assert reconstructed == conv
    count('root_preserving_block_convolutions')

def recurrence_exponent_controls():
    for n in range(1, 10):
        N = 1 << n
        for h in range(1, n+1):
            M, a = 1 << (n-h), 1 << (h-1)
            for q in range(M):
                for f in range(1 << h):
                    f0, sigma = f % a, f//a
                    for s in range(q, N, M):
                        branch = ((s-q)//M) % 2
                        rhs_exponent = s*f0 + q*sigma*a + branch*sigma*(N//2)
                        assert (s*f-rhs_exponent) % N == 0
                        count('symbolic_recurrence_coefficients')

def cover_controls():
    cases = []
    for b, width in [(1, 8), (2, 10), (3, 12)]:
        Q, half = 1 << width, width//2
        pat = '1'+'0'*b+'1'
        T = {t for t in range(Q) if all(pat in format(t, '0%db' % width)[lo:hi] for lo, hi in ((0,half), (half,width)))}
        assert T
        alpha = Fraction(len(T), Q)
        uncovered = set(range(Q))
        shifts = []
        while uncovered:
            best = max(range(Q), key=lambda a: (len(uncovered.intersection({(t+a) % Q for t in T})), -a))
            newly = uncovered.intersection({(t+best) % Q for t in T})
            assert Fraction(len(newly), len(uncovered)) >= alpha
            uncovered -= newly
            shifts.append(best)
        assert all(any((u-a) % Q in T for a in shifts) for u in range(Q))
        # Exact placement check under two witnessed markers in top width bits.
        lower = 2
        n = width+lower
        for t in T:
            for u in range(1 << lower):
                ell = (t << lower)+u
                assert any(direct_mask(h, ell % (1 << h), b, width) for h in range(n-width, n+1))
                count('top_block_placement_checks')
        cases.append({'b': b, 'window': width, 'group_size': Q, 'marker_set_size': len(T), 'greedy_calls': len(shifts), 'shifts': shifts})
    return cases

def moment_controls():
    for b in range(7, 257):
        half = 1 << (b-2)
        a = half-b-1
        p = Fraction(1, 1 << (b+2))
        alpha = a*p
        q = max(a-b-2, 0)
        second = alpha + 4*max(a-b-1, 0)*p*p + q*(q+1)*p*p
        assert Fraction(1,32) <= alpha <= Fraction(1,16)
        assert second < 2*alpha
        assert alpha*alpha/second >= Fraction(1,64)
        count('exact_moment_cases')

def negative_controls():
    # Missing unit phase: n=2,h=1,q=1,f=1, input e_1.
    w = pow(G, (P-1)//4, P)
    assert w*INV_SQRT2 % P != INV_SQRT2
    # Missing odd butterfly sign: n=1,h=1,q=0,f=1, input e_1.
    assert (-INV_SQRT2) % P != INV_SQRT2
    # Incomplete q bank is insufficient for the claimed complete-q closure.
    incomplete = {(1,0,0), (0,0,0), (0,2,0)}
    falsely_predicted = {(0,q,0) for q in range(4)}
    assert {v for v in incomplete if v[0] == 0} != falsely_predicted
    # Wrong trie parent: low-bit parent differs from high-bit parent at h=2,f=1.
    assert (1 % 2) != (1 >> 1)
    # Omitting output chirp phase already fails at N=4,ell=1,input e_0.
    assert pow(w, -1, P) != 1
    return ['omitted_recurrence_phase', 'omitted_butterfly_sign', 'incomplete_q_closure', 'wrong_trie_parent', 'omitted_chirp_output_phase']

def nested_frontier_controls():
    n, b, L = 11, 3, 4
    N = 1 << n
    S, A, H0 = prepare(n, b, L)
    assert len(S) > len(A)
    E = check_structure(n, S, A, H0)
    roots = [pow(G, (P-1)//N*j, P) for j in range(N)]
    x = [(17*s*s+3*s+9) % P for s in range(N)]
    y = {ell: pow(INV_SQRT2,n,P)*sum(x[s]*roots[s*ell % N] for s in range(N)) % P for ell in E}
    p = {(h,q,f): pow(INV_SQRT2,h,P)*sum(x[s]*roots[s*f % N] for s in range(q,N,1 << (n-h))) % P for h,f in S for q in range(1 << (n-h))}
    recovered = {}
    for h,f in A:
        M = 1 << (n-h)
        for v in range(M):
            ell = f+v*(1 << h)
            got = pow(INV_SQRT2,n-h,P)*sum(roots[q*v*(1 << h) % N]*p[h,q,f] for q in range(M)) % P
            assert got == y[ell]
            recovered[ell] = got
            count('nested_frontier_fourier_outputs')
    assert set(recovered) == E
    for h,f in S:
        M = 1 << (n-h)
        for q in range(M):
            got = pow(INV_SQRT2,n-h,P)*sum(roots[-q*v*(1 << h) % N]*recovered[f+v*(1 << h)] for v in range(M)) % P
            assert got == p[h,q,f]
            count('nested_regenerated_packet_outputs')

def interval_controls():
    for n in range(4, 15):
        for b in range(1, (n-1)//2+1):
            depth = n-2*b-1
            start = 1 << (n-b-1)
            size = 1 << depth
            interval = set(range(start, start+size))
            assert all(direct_mask(n, f, b, 1) for f in interval)
            for j in range(depth+1):
                assert {f % (1 << j) for f in interval} == set(range(1 << j))
                count('interval_full_projection_checks')
            count('interval_cases')

def main():
    for n in range(3, 13):
        for b in range(1, 5):
            L = 1 << (b-1)
            S,A,H0 = prepare(n,b,L)
            E = check_structure(n,S,A,H0)
            assert sum(1 << (n-h) for h,f in S) <= (L+1)*(1 << n)//(1 << b)
            if n <= 6:
                check_orthogonal(n,A)
    # Cases chosen independently of marker syntax test the general lemma too.
    for n,H0,S in [(5,2,[(2,1),(4,5),(5,12)]), (6,3,[(3,5),(5,7),(6,39)]), (6,0,[(0,0),(6,3)]), (5,5,[(5,3),(5,17)])]:
        A = [(h,f) for h,f in S if not any(hh<h and f % (1 << hh)==ff for hh,ff in S)]
        check_structure(n,S,A,H0)
        check_orthogonal(n,A)
    for n in range(3,8):
        N = 1 << n
        b,L = (1,1) if n < 5 else (2,2)
        inputs = [[int(s==i) for s in range(N)] for i in range(N)] if N <= 16 else []
        inputs += [[(s*s+7*s+11) % P for s in range(N)], [(13*s*s*s+5*s+2) % P for s in range(N)]]
        for embedding in (1,3):
            for x in inputs:
                check_field_conversion(n,b,L,x,embedding)
    recurrence_exponent_controls()
    moment_controls()
    interval_controls()
    nested_frontier_controls()
    covers = cover_controls()
    report = {'status':'PASS', 'field_prime':P, 'sqrt2':SQRT2, 'counts':COUNT, 'covers':covers, 'negative_controls':negative_controls(), 'method':'Fresh exact implementation; no target/predecessor code read, imported, or executed. Finite controls supplement the all-size proof.'}
    Path('INDEPENDENT_CONTROLS.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','counts':COUNT},sort_keys=True))

if __name__ == '__main__':
    main()
