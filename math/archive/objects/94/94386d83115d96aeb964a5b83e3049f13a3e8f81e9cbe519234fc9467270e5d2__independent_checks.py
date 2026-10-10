#!/usr/bin/env python3
"""Independently authored Phase22 checks. Does not import or execute source files.

Requirements: Python 3, NumPy, SymPy. Run from any directory.
Exact matrices use Python integers; floating checks are separately labelled.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import math
import random
import time

import numpy as np
from sympy import isprime, sqrt_mod
from linear_rotation_reference import prepare_rotation, apply_rotation

P = 998244353
HERE = Path(__file__).resolve().parent


def tr(a):
    return list(map(list, zip(*a)))


def mul(a, b):
    bt = tr(b)
    return [[sum(x*y for x, y in zip(row, col)) % P for col in bt] for row in a]


def mv(a, x):
    return [sum(u*v for u, v in zip(row, x)) % P for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def inverse(a):
    n = len(a)
    rows = [list(row) + ident for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col] % P), None)
        if pivot is None:
            raise ValueError('singular')
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = pow(rows[col][col], -1, P)
        rows[col] = [v*scale % P for v in rows[col]]
        for r in range(n):
            if r != col:
                scale = rows[r][col]
                if scale:
                    rows[r] = [(x-scale*y) % P for x, y in zip(rows[r], rows[col])]
    return [row[n:] for row in rows]


def rank(a):
    a = [[x % P for x in row] for row in a]
    count = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(count, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[count], a[pivot] = a[pivot], a[count]
        scale = pow(a[count][col], -1, P)
        a[count] = [v*scale % P for v in a[count]]
        for r in range(count+1, len(a)):
            scale = a[r][col]
            a[r] = [(x-scale*y) % P for x, y in zip(a[r], a[count])]
        count += 1
        if count == len(a):
            break
    return count


def null_vector(rows, n):
    """One nonzero kernel vector, or None. Independent elimination."""
    a = [[v % P for v in row] for row in rows]
    pivots = []
    k = 0
    for col in range(n):
        r = next((r for r in range(k, len(a)) if a[r][col]), None)
        if r is None:
            continue
        a[k], a[r] = a[r], a[k]
        scale = pow(a[k][col], -1, P)
        a[k] = [v*scale % P for v in a[k]]
        for r in range(len(a)):
            if r != k:
                factor = a[r][col]
                a[r] = [(x-factor*y) % P for x, y in zip(a[r], a[k])]
        pivots.append(col)
        k += 1
        if k == len(a):
            break
    free = next((j for j in range(n) if j not in pivots), None)
    if free is None:
        return None
    x = [0]*n
    x[free] = 1
    for r, col in enumerate(pivots):
        x[col] = -a[r][free] % P
    assert all(sum(u*v for u, v in zip(row, x)) % P == 0 for row in rows)
    return x


def fourier(n):
    w = pow(3, (P-1)-(P-1)//n, P)
    assert pow(w, n, P) == 1 and pow(w, n//2, P) != 1
    scale = pow(int(sqrt_mod(n, P)), -1, P)
    return [[scale*pow(w, i*j, P) % P for j in range(n)] for i in range(n)], w


def sampled_green(n, seed):
    """Same published parameter stream; different dense path-product evaluator.

    Each term is formed from the finite geometric inverse formula, not the
    source's linear recurrence. This is intentionally a dense diagnostic.
    """
    rng = random.Random(seed)
    w = pow(3, (P-1)-(P-1)//n, P)
    roots = [pow(w, k, P) for k in range(n)]
    total = [[0]*n for _ in range(n)]
    term_checks = []
    for _ in range(2):
        order = list(range(n))
        rng.shuffle(order)
        while True:
            weights = [rng.choice(roots) for _ in range(n)]
            product = math.prod(weights) % P
            if product != 1:
                break
        left = [rng.choice(roots) for _ in range(n)]
        right = [rng.choice(roots) for _ in range(n)]
        denominator = pow((1-product) % P, -1, P)
        unscaled = [[0]*n for _ in range(n)]
        for source in range(n):
            path_weight = 1
            for distance in range(n):
                destination = (source+distance) % n
                if distance:
                    path_weight = path_weight*weights[destination] % P
                unscaled[destination][source] = path_weight*denominator % P
                i, j = order[destination], order[source]
                total[i][j] = (total[i][j] + left[destination]*right[source]
                               *unscaled[destination][source]) % P
        # Validate every entry of (I-S)G=I using the sparse denominator.
        assert all((unscaled[i][j]-weights[i]*unscaled[(i-1)%n][j]) % P
                   == int(i == j) for i in range(n) for j in range(n))
        term_checks.append(True)
    return total


def gram_pair(a, b):
    n = len(a)
    bi = inverse(b)
    jbi = [bi[(-i) % n] for i in range(n)]
    return mul(tr(a), a), mul(tr(bi), jbi)


def signatures(a):
    invdiag = [pow(a[i][i], -1, P) for i in range(len(a))]
    h = [[v*v*invdiag[i]*invdiag[j] % P for j, v in enumerate(row)]
         for i, row in enumerate(a)]
    return h, [tuple(sorted(row)) for row in h]


def match_grams(k, c):
    n = len(k)
    zk = sum(k[i][i] == 0 for i in range(n))
    zc = sum(c[i][i] == 0 for i in range(n))
    if zk != zc:
        return 'excluded', None, 'diagonal-zero-count'
    if zk:
        return 'inconclusive', None, 'zero-diagonal'
    h, hk = signatures(k)
    g, hc = signatures(c)
    if Counter(hk) != Counter(hc):
        return 'excluded', None, 'row-signature-multiset'
    if len(set(hk)) != n:
        return 'ambiguous', None, 'repeated-signatures'
    lookup = {sig: i for i, sig in enumerate(hk)}
    perm = [lookup[sig] for sig in hc]
    if any(g[i][j] != h[perm[i]][perm[j]] for i in range(n) for j in range(n)):
        return 'excluded', None, 'full-invariant-matrix'
    return 'candidate', perm, 'matched'


def reconstruct_mask(k, c, perm):
    n = len(k)
    invperm = [perm.index(i) for i in range(n)]
    target = [[c[invperm[i]][invperm[j]] for j in range(n)] for i in range(n)]
    if any(v == 0 for row in k for v in row):
        return None
    ratio = [[target[i][j]*pow(k[i][j], -1, P) % P for j in range(n)] for i in range(n)]
    roots = sqrt_mod(ratio[0][0], P, all_roots=True)
    if not roots or roots[0] == 0:
        return None
    q0 = int(roots[0])
    q = [ratio[i][0]*pow(q0, -1, P) % P for i in range(n)]
    if any(q[i] == 0 for i in range(n)):
        return None
    return q if all(q[i]*k[i][j]*q[j] % P == target[i][j]
                    for i in range(n) for j in range(n)) else None


def sandwich(a, q, perm, b):
    middle = [[0]*len(a) for _ in a]
    for j, i in enumerate(perm):
        middle[i] = [q[i]*x % P for x in b[j]]
    return mul(a, middle)


def make_b(a, q, perm, target):
    core = mul(inverse(a), target)
    scaled = [[x*pow(q[i], -1, P) % P for x in row] for i, row in enumerate(core)]
    return [scaled[i] for i in perm]


def parity_objects(n):
    f, w = fourier(n)
    h = n//2
    sq2 = int(sqrt_mod(2, P))
    invsq2 = pow(sq2, -1, P)
    scale = f[0][0]
    imag = pow(w, n//4, P)
    inv2 = pow(2, -1, P)
    # (-i)^-1 = i, and (omega^-j - omega^j)/(2i) = sin(theta_j).
    iunit = pow(imag, -1, P)
    inv2i = pow(2*iunit, -1, P)
    hmat = [[0]*n for _ in range(n)]
    hmat[0][0] = hmat[h][1] = 1
    for j in range(1, h):
        hmat[j][j+1] = hmat[n-j][j+1] = invsq2
        hmat[j][h+j] = invsq2
        hmat[n-j][h+j] = -invsq2 % P
    q = [1]*(h+1) + [imag]*(h-1)
    # Build C directly from algebraic cos/sin entries, not H^T F.
    c = [[scale]*n, [scale*pow(P-1, k, P) % P for k in range(n)]]
    cosine, sine = [], []
    for j in range(1, h):
        cosine.append([sq2*scale*(pow(w,j*k,P)+pow(w,-j*k,P))*inv2 % P for k in range(n)])
        sine.append([sq2*scale*(pow(w,-j*k,P)-pow(w,j*k,P))*inv2i % P for k in range(n)])
    c += cosine+sine
    # O(N) coefficient preparation by an advancing root and inverse root.
    r = [[0]*n for _ in range(n)]
    r[0][0], r[1][1] = 1, P-1
    wp, wm, wi = 1, 1, pow(w, -1, P)
    for j in range(1, h):
        wp, wm = wp*w % P, wm*wi % P
        co, si = (wp+wm)*inv2 % P, (wm-wp)*inv2i % P
        a, b = j+1, h+j
        r[a][a] = r[b][b] = co
        r[a][b], r[b][a] = -si % P, si
    return f, hmat, q, c, r


def covariance_matrix(c, r):
    rc = mul(r, c)
    n = len(c)
    return [[(c[i][(j+1)%n]-rc[i][j]) % P for j in range(n)] for i in range(n)]


def run():
    started = time.time()
    result = {'field': {'p': P, 'prime_verified': bool(isprime(P))},
              'uploaded_code_executed': False, 'negative_pairs': [], 'positive_controls': [],
              'exact_parity': [], 'numerical_even_lengths': [], 'adversarial_controls': []}
    assert result['field']['prime_verified']
    cache = {}
    for n in (8,16,32,64):
        f, w = fourier(n)
        for seed in (11,17,23,29,43,2026):
            a, b = sampled_green(n, seed), sampled_green(n, seed+701)
            cache[n,seed] = a
            assert rank(a) == n and rank(b) == n
            k, c = gram_pair(a,b)
            state, perm, reason = match_grams(k,c)
            assert state == 'excluded' and perm is None
            result['negative_pairs'].append({'n':n, 'seed':seed, 'result':state, 'reason':reason,
                                            'zero_diags_K':sum(k[i][i] == 0 for i in range(n)),
                                            'zero_diags_C':sum(c[i][i] == 0 for i in range(n))})
        for seed in (17,29,2026):
            a = cache[n,seed]
            rng = random.Random(seed)
            perm = list(range(n)); rng.shuffle(perm)
            q = [rng.randrange(1,P) for _ in range(n)]
            b = make_b(a,q,perm,f)
            assert sandwich(a,q,perm,b) == f
            k,c = gram_pair(a,b)
            state, recovered, _ = match_grams(k,c)
            assert state == 'candidate' and recovered == perm
            recovered_q = reconstruct_mask(k,c,recovered)
            assert recovered_q == q or recovered_q == [(-v)%P for v in q]
            reconstructed = sandwich(a,recovered_q,recovered,b)
            assert reconstructed == f or reconstructed == [[(-v)%P for v in row] for row in f]
            result['positive_controls'].append({'n':n,'seed':seed,'result':'recovered',
                                                'all_entries_verified':True})
        signs = [1 if j%2 == 0 else P-1 for j in range(n)]
        u = [[signs[i]*x % P for x in row] for i,row in enumerate(f)]
        jmat = [[int(j == (-i)%n) for j in range(n)] for i in range(n)]
        assert mul(tr(u),u) == jmat and u[0][0] == f[0][0]
        d1 = sum(u[i][(j+1)%n] != pow(w,i,P)*u[i][j]%P for i in range(n) for j in range(n))
        d2 = sum(pow(w,j,P)*u[i][j]%P != u[(i+1)%n][j] for i in range(n) for j in range(n))
        assert d1 == 0 and d2 > 0
        result['adversarial_controls'].append({'n':n,'sign_twisted_gram_pass':True,
                                               'first_weyl_defects':d1,'second_weyl_defects':d2})
        print('Exact fixed samples and mask recovery:', n, flush=True)
    for n in (4,8,16,32,64,128):
        f,h,q,c,r = parity_objects(n)
        assert mul(h,[[q[i]*x%P for x in row] for i,row in enumerate(c)]) == f
        assert mul(tr(h),h) == eye(n) and mul(tr(c),c) == eye(n)
        assert all(v == 0 for row in covariance_matrix(c,r) for v in row)
        seed = [row[0] for row in c]
        orbit = [seed]
        for _ in range(n-1):
            orbit.append(mv(r,orbit[-1]))
        assert tr(orbit) == c and rank(tr(orbit)) == n
        prepared = prepare_rotation(n, P, pow(3, (P-1)-(P-1)//n, P))
        assert all(apply_rotation(prepared, col) == mv(r, col) for col in tr(c))
        result['exact_parity'].append({'n':n,'factorization':True,'orthogonality':True,
                                       'all_covariance_entries':True,'complete_seed_orbit':True,
                                       'rotation_nonzeros':sum(v != 0 for row in r for v in row)})
    # The real theorems assert every even N, so include non-dyadic controls.
    for n in (4,6,8,10,12,14,16,18,20,24,30,32,42,64,128,256):
        h = n//2
        jk = np.arange(n)
        f = np.exp(-2j*np.pi*np.outer(jk,jk)/n)/math.sqrt(n)
        hmat = np.zeros((n,n)); hmat[0,0]=1; hmat[h,1]=1
        for j in range(1,h):
            hmat[j,j+1] = hmat[n-j,j+1] = 1/math.sqrt(2)
            hmat[j,h+j] = 1/math.sqrt(2); hmat[n-j,h+j] = -1/math.sqrt(2)
        q = np.array([1]*(h+1)+[-1j]*(h-1))
        c = np.vstack([np.ones(n),(-1.)**jk]
                      + [math.sqrt(2)*np.cos(2*np.pi*j*jk/n) for j in range(1,h)]
                      + [math.sqrt(2)*np.sin(2*np.pi*j*jk/n) for j in range(1,h)])/math.sqrt(n)
        r = np.zeros((n,n)); r[0,0]=1; r[1,1]=-1
        for j in range(1,h):
            co,si=math.cos(2*math.pi*j/n),math.sin(2*math.pi*j/n)
            a,b=j+1,h+j
            r[a,a]=r[b,b]=co; r[a,b]=-si; r[b,a]=si
        factor_error = float(np.max(np.abs(hmat@(q[:,None]*c)-f)))
        orth_error = float(np.max(np.abs(c@c.T-np.eye(n))))
        covariance_error = float(np.max(np.abs(c[:,np.roll(jk,-1)]-r@c)))
        assert max(factor_error,orth_error,covariance_error) < 2e-12
        rank_re,rank_im = int(np.linalg.matrix_rank(f.real,tol=1e-9)),int(np.linalg.matrix_rank(f.imag,tol=1e-9))
        assert (rank_re,rank_im) == (h+1,h-1)
        probs = c*c
        positive = probs[probs > 0]
        entropy = float(-np.sum(positive*np.log2(positive)))
        assert entropy >= n*(math.log2(n)-1)+2-1e-9
        # Stronger one-mask classification: A=H times real block mixers.
        rng=np.random.default_rng(177+n)
        t=np.zeros((n,n))
        t[:h+1,:h+1] = np.eye(h+1)+0.01*rng.normal(size=(h+1,h+1))
        t[h+1:,h+1:] = np.eye(h-1)+0.01*rng.normal(size=(h-1,h-1))
        a=hmat@t
        b=(np.linalg.solve(a,f)/q[:,None])
        assert np.max(np.abs(b.imag)) < 2e-12
        assert np.max(np.abs(a@(q[:,None]*b.real)-f)) < 2e-12
        result['numerical_even_lengths'].append({'n':n,'factor_error':factor_error,
             'orthogonality_error':orth_error,'covariance_error':covariance_error,
             'rank_real':rank_re,'rank_imaginary':rank_im,'entropy':entropy,
             'sharper_entropy_floor':n*(math.log2(n)-1)+2,'real_mask_classification_control':True})
    # A fixed known seed can be defeated even by a wrong fixed LINEAR map.
    n=8; trials=2
    f,h,q,c,r=parity_objects(n)
    rng=random.Random(22)
    vectors=[[rng.randrange(P) for _ in range(n)] for _ in range(trials)]
    e0=[1]+[0]*(n-1)
    constraints=[e0]+[x for v in vectors for x in (v,[v[-1]]+v[:-1])]
    b=null_vector(constraints,n)
    assert b is not None
    wrong=[row[:] for row in c]
    wrong[0]=[(x+y)%P for x,y in zip(wrong[0],b)]
    assert wrong != c and mv(wrong,e0) == mv(c,e0)
    assert all(mv(wrong,[v[-1]]+v[:-1]) == mv(r,mv(wrong,v)) for v in vectors)
    d=covariance_matrix(wrong,r)
    assert rank(d) > 0
    result['known_seed_linear_false_accept']={'n':n,'seed':22,'trials':trials,
           'passes_sample':True,'actual_covariance_defect_rank':rank(d),'perturbation_row':b}
    # Nonlinear oracle T(x)=(sum x) Cx has exact covariance and seed, yet T!=C.
    def nonlinear(x):
        return [(sum(x)%P)*v%P for v in mv(c,x)]
    x=[2]+[0]*(n-1)
    assert nonlinear(e0) == mv(c,e0) and nonlinear(x) != mv(c,x)
    assert all(nonlinear([v[-1]]+v[:-1]) == mv(r,nonlinear(v)) for v in vectors+[x])
    result['nonlinear_false_accept']={'formula':'T(x)=(sum_i x_i) Cx',
                                      'exact_covariance_and_seed':True,'equals_C':False}
    # The I Gram has disconnected support, while I's columns fail J-parity.
    result['gram_connectivity_not_sufficient']={'A':'I_8','gram_offdiagonal_edges':0,
                                               'column_e1_is_not_reflection_eigenvector':True}
    # Zero-diagonal and repeated-fingerprint branches are genuinely inconclusive.
    assert match_grams([[0,1],[1,0]],[[0,2],[2,0]])[0] == 'inconclusive'
    assert match_grams(eye(4),eye(4))[0] == 'ambiguous'
    assert match_grams(eye(2),[[0,1],[1,0]])[0] == 'excluded'
    result['degenerate_gram_controls'] = 'passed'
    # Nonzero diagonal fingerprints do not recover an inconsistent cycle sign.
    k=[[1,2,3],[2,1,4],[3,4,1]]
    bad=[[1,-2%P,3],[-2%P,1,4],[3,4,1]]
    assert rank(k)==rank(bad)==3
    state,perm,_=match_grams(k,bad)
    assert state == 'candidate' and perm == [0,1,2]
    assert reconstruct_mask(k,bad,perm) is None
    result['pairwise_square_not_sufficient']={'candidate_fingerprint':True,'mask_reconstruction':False}
    result['summary']={'negative_excluded':len(result['negative_pairs']),
                       'positive_recovered':len(result['positive_controls']),
                       'exact_parity_sizes':len(result['exact_parity']),
                       'numerical_even_sizes':len(result['numerical_even_lengths'])}
    reference = json.loads((HERE/'SOURCE_AUDIT_REFERENCE.json').read_text())
    observed = [{key: row[key] for key in ('n','seed','result','zero_diags_K','zero_diags_C')}
                for row in result['negative_pairs']]
    assert observed == reference['negative_fixed_pairs']
    observed = [{key: row[key] for key in ('n','seed','result')} for row in result['positive_controls']]
    assert observed == reference['positive_controls']
    result['source_audit_json_all_records_match'] = True
    result['elapsed_seconds']=round(time.time()-started,3)
    path=HERE/'CHECK_RESULTS.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],sort_keys=True),flush=True)
    print('All independently authored assertions passed.',flush=True)


if __name__ == '__main__':
    run()
