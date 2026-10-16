"""Newly authored exact C10 finite-prime-field solver and differential checks.

No supplied research program is imported or executed. Root finding by enumeration
is a separately counted test oracle, not a large-field complexity claim.
"""
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib
import json
import random
import time


def mm(a, b, p):
    return tuple(sum(a[2*i+k] * b[2*k+j] for k in range(2)) % p
                 for i in range(2) for j in range(2))


def mv(a, v, p):
    return ((a[0]*v[0] + a[1]*v[1]) % p,
            (a[2]*v[0] + a[3]*v[1]) % p)


def transpose(a):
    return a[0], a[2], a[1], a[3]


def det(a, p):
    return (a[0]*a[3] - a[1]*a[2]) % p


def canonical(v, p):
    x, y = v
    assert x or y
    return (0, y * pow(x, -1, p) % p) if x else (1, 0)


def vector(key):
    return (1, key[1]) if key[0] == 0 else (0, 1)


def trim(a):
    a = list(a)
    while a and not a[-1]:
        a.pop()
    return a


def poly_gcd(a, b, p):
    a, b = trim(a), trim(b)
    while b:
        r = a[:]
        inv = pow(b[-1], -1, p)
        while len(r) >= len(b):
            d, f = len(r)-len(b), r[-1]*inv % p
            for j in range(len(b)):
                r[j+d] = (r[j+d] - f*b[j]) % p
            r = trim(r)
        a, b = b, r
    if not a:
        return []
    inv = pow(a[-1], -1, p)
    return [x*inv % p for x in a]


def evaluate(a, t, p):
    r = 0
    for c in reversed(a):
        r = (r*t + c) % p
    return r


def sequential(flags, fresh, clauses):
    k = len(flags)
    if k < 2:
        return fresh, []
    pref = list(range(fresh, fresh+k-1))
    for i in range(k-1):
        clauses.append((-flags[i], pref[i]))
    for i in range(1, k-1):
        clauses.append((-pref[i-1], pref[i]))
    for i in range(1, k):
        clauses.append((-flags[i], -pref[i-1]))
    return fresh+k-1, pref


def two_sat(n, clauses):
    """Iterative Kosaraju, with no recursion limit or pairwise flag loop."""
    adj = [[] for _ in range(2*n)]
    rev = [[] for _ in range(2*n)]
    def idx(lit):
        return 2*(abs(lit)-1) + (lit < 0)
    for a, b in clauses:
        a, b = idx(a), idx(b)
        adj[a ^ 1].append(b)
        rev[b].append(a ^ 1)
        adj[b ^ 1].append(a)
        rev[a].append(b ^ 1)
    visited = [False]*(2*n)
    order = []
    for root in range(2*n):
        if visited[root]:
            continue
        visited[root] = True
        stack = [(root, 0)]
        while stack:
            v, pos = stack[-1]
            if pos == len(adj[v]):
                order.append(v)
                stack.pop()
            else:
                w = adj[v][pos]
                stack[-1] = (v, pos+1)
                if not visited[w]:
                    visited[w] = True
                    stack.append((w, 0))
    comp = [-1]*(2*n)
    cc = 0
    for root in reversed(order):
        if comp[root] >= 0:
            continue
        comp[root] = cc
        stack = [root]
        while stack:
            v = stack.pop()
            for w in rev[v]:
                if comp[w] < 0:
                    comp[w] = cc
                    stack.append(w)
        cc += 1
    if any(comp[2*i] == comp[2*i+1] for i in range(n)):
        return None
    ans = [False] + [comp[2*i] > comp[2*i+1] for i in range(n)]
    assert all((ans[abs(a)] == (a > 0)) or
               (ans[abs(b)] == (b > 0)) for a, b in clauses)
    return ans


def solve(n, edges, p, force_all_false_if_valid=False, force_false_components=()):
    """Edges are (i,j,L) representing u_j^T L u_i=0 over prime F_p."""
    stats = Counter(n=n, m=len(edges))
    adj = [[] for _ in range(n)]
    for i, j, L in edges:
        if det(L, p):
            stats['rank_two_edges'] += 1
            A = (L[2], L[3], -L[0] % p, -L[1] % p)
            B = (A[3], -A[1] % p, -A[2] % p, A[0])
            adj[i].append((j, A))
            adj[j].append((i, B))
    component = [-1]*n
    transports = [None]*n
    count = 0
    for root in range(n):
        if component[root] >= 0:
            continue
        component[root] = count
        transports[root] = (1, 0, 0, 1)
        stack = [root]
        while stack:
            i = stack.pop()
            for j, A in adj[i]:
                if component[j] < 0:
                    component[j] = count
                    transports[j] = mm(A, transports[i], p)
                    stack.append(j)
        count += 1
    stats['components'] = count
    gcds = [[] for _ in range(count)]
    infinity = [True]*count
    occurrences = []
    crosses = []
    for i, j, L in edges:
        c, d = component[i], component[j]
        if c == d:
            A = mm(transpose(transports[j]), mm(L, transports[i], p), p)
            q = (A[0], (A[1]+A[2]) % p, A[3])
            gcds[c] = poly_gcd(gcds[c], q, p)
            infinity[c] &= q[2] == 0
            stats['internal_equations'] += 1
        elif any(L):
            assert not det(L, p)
            pivot = next(a for a in range(4) if L[a])
            r, col = divmod(pivot, 2)
            row = L[2*r:2*r+2]
            column = (L[col], L[2+col])
            def transformed_kernel(form, T):
                a = (form[0]*T[0]+form[1]*T[2]) % p
                b = (form[0]*T[1]+form[1]*T[3]) % p
                stats['point_occurrences'] += 1
                stats['point_normalization_inversions'] += b != 0
                return canonical((b, -a % p), p)
            alpha = transformed_kernel(row, transports[i])
            beta = transformed_kernel(column, transports[j])
            a = len(occurrences)
            occurrences.append((c, alpha, a))
            b = len(occurrences)
            occurrences.append((d, beta, b))
            crosses.append((a, b))
    fallback = [None]*count
    for c in range(count):
        g = gcds[c]
        if not g:
            fallback[c] = (0, 0)
            stats['unrestricted_components'] += 1
        elif infinity[c]:
            fallback[c] = (1, 0)
        elif len(g) == 2:
            fallback[c] = (0, -g[0] * pow(g[1], -1, p) % p)
        elif len(g) == 3:
            # Separately charged exact test oracle; never part of O(M log M).
            stats['quadratic_root_oracle_calls'] += 1
            for t in range(p):
                stats['root_oracle_field_candidates'] += 1
                if not evaluate(g, t, p):
                    fallback[c] = (0, t)
                    break
        if fallback[c] is None:
            stats['empty_domain_rejection'] += 1
            return None, dict(stats)
    ordered = sorted(occurrences)
    occurrence_flag = [None]*len(occurrences)
    flags = [[] for _ in range(count)]
    points = [None]
    last = None
    for c, key, occurrence in ordered:
        if (c, key) != last:
            flag = len(points)
            points.append(key)
            flags[c].append(flag)
            last = c, key
        occurrence_flag[occurrence] = flag
    clauses = [(occurrence_flag[a], occurrence_flag[b]) for a, b in crosses]
    for c in range(count):
        for flag in flags[c]:
            tag, t = points[flag]
            permitted = infinity[c] if tag else not evaluate(gcds[c], t, p)
            if not permitted:
                clauses.append((-flag, -flag))
                stats['forbidden_flags'] += 1
    fresh = len(points)
    prefixes = []
    for component_flags in flags:
        fresh, pref = sequential(component_flags, fresh, clauses)
        prefixes.append(pref)
    stats['named_flags'] = len(points)-1
    stats['auxiliary_variables'] = fresh-len(points)
    stats['variables'] = fresh-1
    stats['clauses'] = len(clauses)
    assert stats['named_flags'] <= 2*len(edges)
    assert stats['variables'] <= 4*len(edges)
    assert stats['clauses'] <= 9*len(edges)
    # Optional test-only units select an all-false component in a valid original
    # Boolean solution; they are not constraints of the input system or repair.
    test_units = [(-flag, -flag) for c in force_false_components for flag in flags[c]]
    assignment = two_sat(fresh-1, clauses + test_units)
    if assignment is None:
        stats['two_sat_rejection'] += 1
        return None, dict(stats)
    if force_all_false_if_valid:
        trial = [False]*fresh
        if all((trial[abs(a)] == (a>0)) or (trial[abs(b)] == (b>0))
               for a, b in clauses):
            assignment = trial
            stats['forced_all_false_control'] += 1
    roots = []
    for c in range(count):
        chosen = [flag for flag in flags[c] if assignment[flag]]
        assert len(chosen) <= 1
        if chosen:
            root = points[chosen[0]]
        else:
            stats['all_false_repairs'] += 1
            root = fallback[c]
            for flag in flags[c]:
                if points[flag] == root:
                    assignment[flag] = True
                    stats['named_point_repairs'] += 1
        roots.append(vector(root))
        prefix = False
        for flag, s in zip(flags[c], prefixes[c]):
            prefix |= assignment[flag]
            assignment[s] = prefix
    assert all((assignment[abs(a)] == (a > 0)) or
               (assignment[abs(b)] == (b > 0)) for a, b in clauses)
    result = [mv(transports[i], roots[component[i]], p) for i in range(n)]
    assert all(any(v) for v in result)
    assert direct_valid(result, edges, p)
    return result, dict(stats)


def direct_valid(directions, edges, p):
    for i, j, L in edges:
        a, b = directions[i]
        c, d = directions[j]
        if (c*(L[0]*a+L[1]*b)+d*(L[2]*a+L[3]*b)) % p:
            return False
    return True


def exhaustive(n, edges, p):
    pts = [(1,t) for t in range(p)] + [(0,1)]
    for candidate in product(pts, repeat=n):
        if direct_valid(candidate, edges, p):
            return candidate
    return None


def sequential_truth_checks():
    checks = 0
    for k in range(11):
        clauses = []
        fresh, pref = sequential(list(range(1,k+1)), k+1, clauses)
        assert len(pref) == max(0,k-1)
        assert len(clauses) == (0 if k<2 else 3*k-4)
        for bits in product([False, True], repeat=k):
            fixed = clauses + [(i if b else -i, i if b else -i)
                               for i,b in enumerate(bits,1)]
            exists = two_sat(fresh-1, fixed) is not None
            assert exists == (sum(bits) <= 1)
            checks += 1
    return checks


def main():
    start = time.monotonic()
    results = {'schema_version': 1, 'record_id': 'C10',
               'method': 'Newly authored exact finite-prime-field implementation; independent exhaustive original-equation evaluation',
               'scope': 'Selected bilinear projective subsystem only; no target extraction/Fourier construction replay',
               'sequential_truth_assignments': sequential_truth_checks()}
    counts = Counter()
    aggregate = Counter()
    fingerprint = hashlib.sha256()
    def check(n, edges, p, category):
        found, stats = solve(n, edges, p)
        brute = exhaustive(n, edges, p)
        assert (found is None) == (brute is None), (p,n,edges,found,brute)
        counts[category] += 1
        counts['satisfiable' if found is not None else 'unsatisfiable'] += 1
        aggregate.update(stats)
        fingerprint.update(json.dumps([p,n,edges,found is not None],separators=(',',':')).encode())
    # Exhaust every pair of arbitrary matrices on fixed parallel two-vertex edges.
    for p in (2,3):
        matrices = list(product(range(p), repeat=4))
        for A in matrices:
            for B in matrices:
                check(2, [(0,1,A),(0,1,B)], p, f'exhaustive_parallel_pairs_F{p}')
    # Exhaust every pair of loop matrices: direct joint quadratic controls.
    for p in (2,3):
        matrices = list(product(range(p), repeat=4))
        for A in matrices:
            for B in matrices:
                check(1, [(0,0,A),(0,0,B)], p, f'exhaustive_loop_pairs_F{p}')
    rng = random.Random(20261016)
    for p in (2,3,5,7):
        for _ in range(700):
            n = rng.randrange(1,5)
            edges = [(rng.randrange(n),rng.randrange(n),tuple(rng.randrange(p) for _ in range(4)))
                     for _ in range(rng.randrange(11))]
            check(n, edges, p, f'seeded_mixed_graphs_F{p}')
    special = []
    for p in (2,3,5,7):
        # xy, x(x-y), y(x-y): every pair has a root, all three do not.
        quadratics = [(0,1,0,0),(1,-1%p,0,0),(0,1,0,-1%p)]
        for selected in ((0,1),(0,2),(1,2),(0,1,2)):
            edges = [(0,0,quadratics[i]) for i in selected]
            check(1,edges,p,'tight_three_quadratic_controls')
        # Constant chart / infinity-only; repeated root including characteristic2.
        for L in ((1,0,0,0),(0,0,0,1),(1,-2%p,0,1)):
            check(1,[(0,0,L)],p,'infinity_and_repeated_root_controls')
    check(1,[(0,0,(-7%241,0,0,1))],241,'base_field_no_root_F241')
    for n in (0,1,6):
        check(n,[],2,'empty_graph_controls')
    # Direct all-false repair controls, including finite-field exhausted names.
    repair = []
    for p in (2,3,5):
        # Star names all p+1 center points, while each leaf is a free singleton name.
        edges = [(0,t+1,(0,0,-t%p,1)) for t in range(p)]
        edges.append((0,p+1,(0,0,1,0)))
        found, stats = solve(p+2,edges,p,force_false_components=(0,))
        assert found is not None and stats.get('named_point_repairs') == 1
        check(p+2,edges,p,'finite_field_exhaustion_stars')
        repair.append({'field':p,'stats':stats})
        # Exhausted named singleton and two-point restricted domains; selecting
        # allfalse before repair is intentional, although an allowed name exists.
        for L in ((0,0,0,1),(0,-1%p,0,1)):
            found,stats=solve(p+2,edges+[(0,0,L)],p,force_false_components=(0,))
            assert found is not None and stats.get('named_point_repairs') == 1
            repair.append({'field':p,'forced_named_restricted_repair':True,'stats':stats})
    # Force allfalse with no edge clauses, then reconstruct restricted roots.
    for p,L in ((2,(0,0,0,1)),(3,(1,0,0,0)),(5,(1,3,0,1))):
        found,stats=solve(1,[(0,0,L)],p,force_all_false_if_valid=True)
        assert found is not None and stats.get('all_false_repairs')==1
        repair.append({'field':p,'forced_restricted_repair':True,'stats':stats})
    stress=[]
    for m in (1000,10000,30000):
        p=100003
        edges=[(0,t+1,(0,0,-t%p,1)) for t in range(m)]
        before=time.monotonic()
        found,stats=solve(m+1,edges,p)
        assert found is not None
        assert stats['named_flags']==2*m
        assert stats['auxiliary_variables']==m-1
        assert stats['clauses']==4*m-4
        assert not stats.get('root_oracle_field_candidates')
        stress.append({'m':m,'stats':stats,'elapsed_seconds':round(time.monotonic()-before,6)})
    results.update({'status':'all_passed', 'differential_counts':dict(counts),
                    'differential_total':counts['satisfiable']+counts['unsatisfiable'],
                    'aggregate_solver_statistics':dict(aggregate),
                    'differential_fingerprint_sha256':fingerprint.hexdigest(),
                    'repair_controls':repair,'linear_encoding_stress':stress,
                    'elapsed_seconds':round(time.monotonic()-start,6),
                    'limitations':['Prime fields only in executable controls; abstract-field correctness is proved in REPORT.md.',
                                   'Root enumeration is separately counted, not a fast general root algorithm.',
                                   'No supplied code or historical target extraction was executed.',
                                   'Timing is diagnostic; exact clause/variable counts support encoding-size checks.']})
    out=Path(__file__).with_name('CHECK_RESULTS.json')
    out.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':results['status'],'differential_total':results['differential_total'],
                      'sequential_truth_assignments':results['sequential_truth_assignments'],
                      'elapsed_seconds':results['elapsed_seconds'],'output':str(out)},indent=2))


if __name__ == '__main__':
    main()
