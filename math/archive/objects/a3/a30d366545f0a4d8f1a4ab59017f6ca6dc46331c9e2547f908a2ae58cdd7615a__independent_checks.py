#!/usr/bin/env python3
"""Fresh independent audit checks, authored 2026-10-10.
Uses only Python's standard library. Never loads any supplied research program.
These checks corroborate, but do not replace, REPORT.md's proof.
"""
from collections import Counter, deque
from itertools import combinations, permutations
from math import factorial
from random import Random
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent

def radius(n):
    r, p = 0, 1
    while p <= n:
        r, p = r + 1, p * 3
    return r

def graph(pi, sigma):
    n = len(pi)
    edges = [(j, p[j]) for p in (pi, sigma) for j in range(n)]
    adj = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(edges):
        adj[u].append((v, eid)); adj[v].append((u, eid))
    assert all(len(a) == 4 for a in adj)
    return edges, adj

def bfs(adj, root):
    dist = {root: 0}; parent = {}; queue = deque([root])
    while queue:
        u = queue.popleft()
        for v, eid in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; parent[v] = (u, eid); queue.append(v)
    return dist, parent

def ball_data(edges, adj, root, r):
    dist, parent = bfs(adj, root)
    vs = {v for v in dist if dist[v] <= r}
    es = {i for i, (u, v) in enumerate(edges) if u in vs and v in vs}
    tree = {parent[v][1] for v in vs if v != root}
    return vs, es, tree, dist, parent

def outgoing(pi, sigma, s):
    return sum(p[j] not in s for p in (pi, sigma) for j in s)

def certificate(pi, sigma):
    n = len(pi); edges, adj = graph(pi, sigma)
    r = radius(n)
    vs, es, tree, dist, parent = ball_data(edges, adj, 0, r)
    surplus = sorted(es - tree)
    assert len(surplus) >= 2
    selected = surplus[:2]; s = {0}; te = set()
    for eid in selected:
        for u in edges[eid]:
            while u != 0:
                s.add(u); u, pe = parent[u]; te.add(pe)
    assert len(te) == len(s) - 1
    assert not te.intersection(selected)
    internal = sum(u in s and v in s for u, v in edges)
    out = outgoing(pi, sigma, s)
    assert len(s) <= 4*r + 1
    assert 2*len(s) <= n
    assert internal >= len(s) + 1
    assert out == 2*len(s) - internal <= len(s) - 1
    return {'S': sorted(s), 'outgoing': out, 'method': 'bicyclic',
            'radius': r, 'surplus_edge_ids': selected, 'tree_edge_ids': sorted(te)}

def partitions(n, lo=1):
    if n == 0:
        yield ()
    for k in range(lo, n+1):
        for tail in partitions(n-k, k):
            yield (k,) + tail

def representative(parts):
    p=[]; start=0
    for k in parts:
        p.extend(range(start+1,start+k)); p.append(start); start += k
    return tuple(p)

def class_size(n, parts):
    z=1
    for k, mult in Counter(parts).items():
        z *= k**mult * factorial(mult)
    return factorial(n)//z

def witness(pi, sigma):
    n=len(pi)
    for k in range(1, n//2+1):
        for c in combinations(range(n), k):
            s=set(c)
            if outgoing(pi,sigma,s) <= k-1:
                return c
    return None

results={'description':'Independent exact-arithmetic checks; no supplied code loaded.'}
# Exact integer threshold checks, including large powers where floor logarithms jump.
for n in range(34,1000001):
    assert 2*(4*radius(n)+1) <= n
for k in range(4,1001):
    for n in (3**k-1,3**k,3**k+1):
        assert 2*(4*radius(n)+1) <= n
results['threshold']={'all_integers':[34,1000000], 'power_boundaries_k':[4,1000],
 'N33_bound':4*radius(33)+1,'N34_bound':4*radius(34)+1}
for n in range(842,1000001):
    assert (4*radius(n)+1)**2 < n
for k in range(7,1001):
    for n in (3**k-1,3**k,3**k+1):
        assert (4*radius(n)+1)**2 < n
assert (4*radius(841)+1)**2 == 841
results['composite_fourier_threshold']={'all_integers':[842,1000000], 'power_boundaries_k':[7,1000],
 'B841':4*radius(841)+1,'B842':4*radius(842)+1,'strict_bound_fails_at':841,
 'additional_initial_interval':[626,728]}
assert [n for n in range(1,842) if (4*radius(n)+1)**2 < n] == list(range(626,729))
# Relaxed incidence-deficit enumeration: zero, one, or two deficits at arbitrary levels.
profiles=0
for r in range(1,25):
    best=None
    for positions in [()] + [(i,) for i in range(r)] + list(combinations(range(r),2)) + [(i,i) for i in range(r)]:
        q=Counter(positions); a=4-q[0]; total=1+a
        for d in range(1,r):
            a=3*a-q[d]; total += a
        best=total if best is None else min(best,total); profiles += 1
    assert best == 3**r
results['deficit_profiles']={'radii':[1,24], 'profiles':profiles, 'minimum':'3**r at every tested radius'}
# Exhaustive pair enumeration modulo conjugacy of the FIRST permutation only.
# Since the second permutation ranges over all n!, this covers every ordered pair.
exhaustive=[]; ball_checks=0
for n in range(1,8):
    pairs=bad=weighted=weighted_bad=0; first_bad=None
    for parts in partitions(n):
        pi=representative(parts); weight=class_size(n,parts)
        for sigma in permutations(range(n)):
            pairs += 1; weighted += weight
            if witness(pi,sigma) is None:
                bad += 1; weighted_bad += weight
                if first_bad is None: first_bad={'pi':pi,'sigma':sigma}
            if n <= 5:
                edges,adj=graph(pi,sigma)
                for root in range(n):
                    for r in (1,2,3):
                        vs,es,tree,_,_=ball_data(edges,adj,root,r)
                        surplus=len(es)-len(tree)
                        if surplus <= 1:
                            assert len(vs) >= 3**r
                        ball_checks += 1
    assert weighted == factorial(n)**2
    exhaustive.append({'N':n,'canonical_first_pairs':pairs,'labelled_pairs_covered':weighted,
                       'pairs_without_cut':bad,'labelled_pairs_without_cut':weighted_bad,
                       'first_failure_below_claimed_range':first_bad})
results['exhaustive_pairs_N1_to_7']=exhaustive
results['multigraph_ball_checks_N1_to_5']=ball_checks
rng=Random(202610100430)
certs=[]
for n in (34,35,36,37,40,79,80,81,82,242,243,244,626,728,729,841,842,1000,2186,2187):
    identity=tuple(range(n)); cycle=tuple((j+1)%n for j in range(n)); reverse=tuple((j-1)%n for j in range(n))
    cases=[('two_loop_colors',identity,identity),('root_loops',identity,cycle),
           ('same_direction_parallel',cycle,cycle),('opposite_direction_parallel',cycle,reverse)]
    for t in range(25):
        a=list(range(n)); b=list(range(n)); rng.shuffle(a); rng.shuffle(b)
        cases.append((f'random_{t}',tuple(a),tuple(b)))
    for name,pi,sigma in cases:
        cert=certificate(pi,sigma)
        certs.append({'N':n,'case':name,'pi':pi,'sigma':sigma,'certificate':cert})
results['constructive_tests']={'count':len(certs),'seed':202610100430,'N_values':sorted({x['N'] for x in certs}),
                              'maximum_witness_size':max(len(x['certificate']['S']) for x in certs)}
# Exact inverse-cut-rank check over GF(101); no numerical tolerances.
def rank_mod(a,p=101):
    a=[list(row) for row in a]
    if not a: return 0
    rows,cols=len(a),len(a[0]); rank=0
    for j in range(cols):
        pivot=next((i for i in range(rank,rows) if a[i][j]%p),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        t=pow(a[rank][j]%p,-1,p); a[rank]=[(x*t)%p for x in a[rank]]
        for i in range(rows):
            if i != rank:
                t=a[i][j]%p; a[i]=[(x-t*y)%p for x,y in zip(a[i],a[rank])]
        rank += 1
        if rank == rows: break
    return rank

def inverse_mod(a,p=101):
    n=len(a); aug=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if aug[i][j]%p),None)
        if pivot is None: return None
        aug[j],aug[pivot]=aug[pivot],aug[j]
        t=pow(aug[j][j]%p,-1,p); aug[j]=[(x*t)%p for x in aug[j]]
        for i in range(n):
            if i != j:
                t=aug[i][j]%p; aug[i]=[(x-t*y)%p for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]

rank_checks=0
for n in range(2,10):
    count=0
    while count<30:
        a=[[rng.randrange(101) for _ in range(n)] for _ in range(n)]
        ai=inverse_mod(a)
        if ai is None: continue
        count+=1
        for mask in range(1,2**n-1):
            s=[j for j in range(n) if mask>>j&1]; sc=[j for j in range(n) if not(mask>>j&1)]
            assert rank_mod([[a[i][j] for j in s] for i in sc]) == rank_mod([[ai[i][j] for j in s] for i in sc])
            rank_checks+=1
results['exact_GF101_inverse_cut_rank_checks']=rank_checks
(OUT/'graph_certificates.json').write_text(json.dumps(certs,indent=2)+'\n')
(OUT/'checks_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
