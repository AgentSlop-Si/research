"""Independent Phase 26 controls. Never import or execute submitted programs.

Python 3 standard library, with optional NumPy for explicitly numerical SVD
controls. The mathematical proofs and exact-field checks do not need NumPy.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import time

HERE = Path(__file__).resolve().parent
P = 998244353


def integer_root(v, degree):
    assert v >= 1 and degree >= 1
    low, high = 0, 1 << ((v.bit_length() + degree - 1) // degree)
    while low + 1 < high:
        mid = (low + high) // 2
        if mid ** degree <= v:
            low = mid
        else:
            high = mid
    return high if high ** degree <= v else low


def centered(v, n):
    v %= n
    return min(v, n-v)


def character_cut(n, h):
    assert n >= 4 and n & (n-1) == 0 and 0 < h < n
    left = [i for i in range(n) if (h*i) % n < n//2]
    right = [i for i in range(n) if (h*i) % n >= n//2]
    return left, right


def exact_character(n, steps):
    """Construct a strict witness by the proof's exact integer pigeonholes."""
    steps = sorted({a % n for a in steps if a % n})
    assert steps
    r = integer_root(n-1, len(steps))
    boxes = {}
    for j in range(n):
        box = tuple(r * ((j*a) % n) // n for a in steps)
        if box in boxes:
            h = j-boxes[box]
            shifts = [centered(h*a, n) for a in steps]
            assert 0 < h < n and all(r*t < n for t in shifts)
            return h, r, shifts
        boxes[box] = j
    raise AssertionError("Pigeonhole collision missing")


def cycle_edges(order):
    return list(zip(order, order[1:] + order[:1]))


def crossings(order, left):
    left = set(left)
    return sum(u not in left and v in left for u, v in cycle_edges(order))


def zigzag(n, a):
    assert n >= 8 and a % 2 == 0 and math.gcd(a//2, n//2) == 1
    return [(a*t) % n for t in range(n//2)] + [(n-1-a*t) % n for t in range(n//2)]


def rank(matrix, p=P):
    a = [[v % p for v in row] for row in matrix]
    if not a:
        return 0
    found = 0
    for col in range(len(a[0])):
        pivot = next((k for k in range(found, len(a)) if a[k][col]), None)
        if pivot is None:
            continue
        a[found], a[pivot] = a[pivot], a[found]
        ip = pow(a[found][col], -1, p)
        for k in range(found+1, len(a)):
            if a[k][col]:
                scale = a[k][col]*ip % p
                a[k][col:] = [(x-scale*y) % p for x,y in zip(a[k][col:], a[found][col:])]
        found += 1
        if found == len(a):
            break
    return found


def inverse(matrix, p):
    n = len(matrix)
    a = [[v % p for v in row] + [int(i == j) for j in range(n)] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot = next((k for k in range(col,n) if a[k][col]), None)
        if pivot is None:
            raise ValueError("singular")
        a[col], a[pivot] = a[pivot], a[col]
        inv = pow(a[col][col], -1, p)
        a[col] = [v*inv % p for v in a[col]]
        for k in range(n):
            if k != col and a[k][col]:
                scale = a[k][col]
                a[k] = [(x-scale*y) % p for x,y in zip(a[k],a[col])]
    return [row[n:] for row in a]


def weighted_solve(order, gamma, rhs, p=P):
    """Independent reverse-path closed form at order[0], then propagation."""
    n = len(order)
    first = order[0]
    numerator = rhs[first] % p
    coefficient = gamma[first] % p
    for vertex in reversed(order[1:]):
        numerator = (numerator + coefficient*rhs[vertex]) % p
        coefficient = coefficient*gamma[vertex] % p
    if coefficient == 1:
        raise ValueError("singular weighted cycle")
    out = [0]*n
    out[first] = numerator*pow((1-coefficient) % p, -1, p) % p
    previous = first
    for vertex in order[1:]:
        out[vertex] = (rhs[vertex] + gamma[vertex]*out[previous]) % p
        previous = vertex
    return out


def denominator(order, gamma, p):
    n = len(order)
    out = [[int(i == j) for j in range(n)] for i in range(n)]
    for u,v in cycle_edges(order):
        out[v][u] = (out[v][u]-gamma[v]) % p
    return out


def block(matrix, left, right):
    return [[matrix[i][j] for j in right] for i in left]


def stage_apply(stage, x, p=P):
    terms, diagonal = stage
    out = [0]*len(x)
    for order, gamma, left, right in terms:
        rhs = [u*v % p for u,v in zip(x,right)]
        sol = weighted_solve(order,gamma,rhs,p)
        out = [(old + l*v) % p for old,l,v in zip(out,left,sol)]
    return [u*v % p for u,v in zip(out,diagonal)]


def circuit(stages, x, p=P):
    for stage in stages:
        x = stage_apply(stage,x,p)
    return x


def cut_of_operator(executor, n, left, right):
    columns=[]
    for j in right:
        e=[0]*n
        e[j]=1
        v=executor(e)
        columns.append([v[i] for i in left])
    return [list(row) for row in zip(*columns)]


def permute(values, mapping):
    out=[0]*len(values)
    for i,j in enumerate(mapping):
        out[j]=values[i]
    return out


def conjugate(stage, mapping):
    terms, diagonal=stage
    return ([( [mapping[j] for j in order], permute(gamma,mapping),
               permute(left,mapping), permute(right,mapping))
              for order,gamma,left,right in terms], permute(diagonal,mapping))


def make_stage(orders, rng, allow_zero=False):
    n=len(orders[0])
    def diagonal():
        return [rng.randrange(0 if allow_zero else 1,P) for _ in range(n)]
    terms=[]
    for order in orders:
        gamma=diagonal()
        assert math.prod(gamma) % P != 1
        terms.append((order,gamma,diagonal(),diagonal()))
    return terms,diagonal()


def coarse(n, q, d=1, b=2, improved=True):
    r=integer_root(n-1,d*q)
    if improved:
        return d*q*((n-1)//r) + q*(b//2),r
    return (2*d*q*n+r-1)//r+b*q,r


def recursive_dft(values, root, p=P):
    n=len(values)
    if n==1:
        return values[:]
    even=recursive_dft(values[::2],root*root%p,p)
    odd=recursive_dft(values[1::2],root*root%p,p)
    powers=[pow(root,k,p) for k in range(n//2)]
    return [(even[k]+powers[k]*odd[k])%p for k in range(n//2)] + [(even[k]-powers[k]*odd[k])%p for k in range(n//2)]


def weyl_defects(executor, values):
    n=len(values)
    root=pow(3,(P-1)//n,P)
    transformed=executor(values)
    shifted=executor(values[-1:]+values[:-1])
    modulated=[v*pow(root,j,P)%P for j,v in enumerate(transformed)]
    second=executor([v*pow(root,j,P)%P for j,v in enumerate(values)])
    shifted_output=transformed[1:]+transformed[:1]
    return [sum(x!=y for x,y in zip(shifted,modulated)),sum(x!=y for x,y in zip(second,shifted_output))]


def run():
    start=time.monotonic()
    results={"status":"RUNNING", "implementation":"independently authored; no submitted code imported or executed"}
    archive=HERE/"source_archives/fft_green_research_phase26_2026-10-10.zip"
    archive_hash=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert archive_hash == "b3b03e9c84728cc4c9e9d258967fd8092f637d32f4a0aa6ecf27e1c6ea9c206e"
    results["source_archive_sha256"]=archive_hash

    identities=0
    for n in (4,8,16,32,64,128):
        for h in range(1,n):
            left,right=character_cut(n,h)
            assert len(left)==len(right)==n//2
            left=set(left)
            for a in range(n):
                cross=sum((j+a)%n in left for j in right)
                assert cross==centered(h*a,n)
                identities+=1
    results["exact_translation_boundary_identities"]=identities
    print("Exact boundary identities:",identities,flush=True)

    pigeonholes=0
    for n, max_s in ((8,4),(16,4),(32,3)):
        for s in range(1,max_s+1):
            for steps in itertools.combinations(range(1,n),s):
                h,r,shifts=exact_character(n,steps)
                assert r**s < n <= (r+1)**s
                assert all(t <= (n-1)//r for t in shifts)
                pigeonholes+=1
    rng=random.Random(2026100926)
    for n in (64,128,256,1024):
        for _ in range(50):
            steps=rng.sample(range(1,n),rng.randrange(1,9))
            exact_character(n,steps)
            pigeonholes+=1
    roots=0
    for exponent in (8,32,64,128,256,1024):
        for degree in (1,2,3,7,16,31,128,2048):
            v=(1<<exponent)-1
            r=integer_root(v,degree)
            assert r**degree <= v < (r+1)**degree
            roots+=1
    strict_regression={"n":16,"steps":[1,2,8],"r":2,"source_first_accepted_h":1,
                       "source_max_shift":8,"strict_requirement":"r*max_shift < n",
                       "exact_pigeonhole_witness":exact_character(16,[1,2,8])[0]}
    assert 8 < 16/2+1e-12 and not 2*8 < 16
    results.update(pigeonhole_cases=pigeonholes,large_integer_root_cases=roots,
                   floating_tolerance_counterexample=strict_regression)
    print("Pigeonhole controls:",pigeonholes,"; exact-root controls:",roots,flush=True)

    strengthened=0
    magnitudes=range(1,5)
    for tail in itertools.permutations(range(1,8)):
        order=[0,*tail]
        edges=cycle_edges(order)
        for mask in range(16):
            steps=[a for a in magnitudes if mask & (1<<(a-1))]
            allowed={v%8 for a in steps for v in (a,-a)}
            bridges=sum((v-u)%8 not in allowed for u,v in edges)
            for h in range(1,8):
                left,_=character_cut(8,h)
                cap=sum(centered(h*a,8) for a in steps)+bridges//2
                assert crossings(order,left)<=cap
                strengthened+=1
    # The Hamiltonian/no-directed-2-cycle hypothesis really matters.
    permutation=[7,2,1,4,3,6,5,0]
    bad_cross=sum(i>=4 and permutation[i]<4 for i in range(8))
    assert bad_cross==2 > centered(1,8)
    results["strengthened_hamiltonian_cut_cases"]=strengthened
    results["non_hamiltonian_negative_control"]={"permutation":permutation,"crossings":2,"invalid_cap_if_hypothesis_dropped":1}
    print("Strengthened Hamiltonian cut controls:",strengthened,flush=True)

    inverse_cases=0
    rank_cases=0
    for p in (2,3,97,P):
        for n in (8,16):
            for trial in range(8):
                order=list(range(n));rng.shuffle(order)
                gamma=[rng.randrange(p) for _ in range(n)]
                gamma[trial % n]=0  # Include zero weights and all characteristics.
                a=denominator(order,gamma,p)
                ainv=inverse(a,p)
                for j in range(n):
                    e=[int(i==j) for i in range(n)]
                    assert weighted_solve(order,gamma,e,p)==[row[j] for row in ainv]
                    inverse_cases+=1
                for h in range(1,n):
                    left,right=character_cut(n,h)
                    ra=rank(block(a,left,right),p)
                    assert rank(block(ainv,left,right),p)==ra<=crossings(order,left)
                    nonzero_cross=sum(u in right and v in left and gamma[v]%p != 0 for u,v in cycle_edges(order))
                    assert ra==nonzero_cross
                    rank_cases+=1
    for n in (8,16,32):
        try:
            weighted_solve(list(range(n)),[1]*n,[1]*n)
        except ValueError:
            pass
        else:
            raise AssertionError("singular cycle was accepted")
    results.update(weighted_inverse_columns=inverse_cases,weighted_inverse_block_ranks=rank_cases)
    print("Weighted inverse controls:",inverse_cases,"columns and",rank_cases,"cut ranks",flush=True)

    concrete=[]
    for n in (32,64,128,256,512,1024,4096,16384):
        orders=[zigzag(n,a) for a in (2,n//2+2,n//2+6)]+[list(range(n))]
        left,right=character_cut(n,2)
        edge_counts=[crossings(order,left) for order in orders]
        assert edge_counts==[3,3,11,2]
        concrete.append({"n":n,"crossings":edge_counts,"two_stage_cap":38})
    n=256
    orders=[zigzag(n,a) for a in (2,n//2+2,n//2+6)]+[list(range(n))]
    rng_source=random.Random(260027)
    stages=[make_stage(orders,rng_source) for _ in range(2)]
    left,right=character_cut(n,2)
    actual=rank(cut_of_operator(lambda x:circuit(stages,x),n,left,right))
    assert actual==38
    results["concrete_cut_counts"]=concrete
    results["reproduced_source_seed_260027_rank"]=actual
    print("Source-seed weighted N=256 candidate rank:",actual,flush=True)

    row_mapping=list(range(n));rng.shuffle(row_mapping)
    col_mapping=list(range(n));rng.shuffle(col_mapping)
    inverse_col=[0]*n
    for i,j in enumerate(col_mapping):inverse_col[j]=i
    rows=[row_mapping[j] for j in left]
    cols=[inverse_col[j] for j in right]
    left_scale=[rng.randrange(1,P) for _ in range(n)]
    right_scale=[rng.randrange(1,P) for _ in range(n)]
    def outer_monomial(x):
        x=[u*v%P for u,v in zip(x,right_scale)]
        y=permute(circuit(stages,permute(x,col_mapping)),row_mapping)
        return [u*v%P for u,v in zip(y,left_scale)]
    outer_rank=rank(cut_of_operator(outer_monomial,n,rows,cols))
    assert outer_rank==actual
    results["arbitrary_outer_monomial_rank_transfer"]={"n":n,"rank":outer_rank,"row_column_sets_need_not_be_complements":True}

    conjugations=[]
    for n in (16,32,64):
        orders=[zigzag(n,2),list(range(n))]
        stages=[make_stage(orders,rng) for _ in range(3)]
        p1=[(3*j+7)%n for j in range(n)]
        p2=[(5*j+11)%n for j in range(n)]
        composition=[p2[p1[j]] for j in range(n)]
        normal=[conjugate(stages[0],composition),conjugate(stages[1],p2),stages[2]]
        def original(x):
            return stage_apply(stages[2],permute(stage_apply(stages[1],permute(stage_apply(stages[0],x),p1)),p2))
        for _ in range(5):
            x=[rng.randrange(P) for _ in range(n)]
            assert original(x)==circuit(normal,permute(x,composition))
        h,r,_=exact_character(n,[30,15,10,5,2,1])
        left,right=character_cut(n,h)
        inverse_mapping=[0]*n
        for i,j in enumerate(composition):inverse_mapping[j]=i
        columns=[inverse_mapping[j] for j in right]
        observed=rank(cut_of_operator(original,n,left,columns))
        edgecap=sum(crossings(term[0],left) for stage in normal for term in stage[0])
        assert observed<=edgecap
        conjugations.append({"n":n,"rank":observed,"edge_cap":edgecap})
    results["three_stage_two_affine_permutation_checks"]=conjugations

    fourier=[]
    for n in (8,16,32,64,128,256):
        w=pow(3,(P-1)//n,P)
        assert pow(w,n,P)==1 and pow(w,n//2,P)!=1
        left,right=character_cut(n,2)
        observed=rank([[pow(w,i*j,P) for j in right] for i in left])
        assert observed==n//2
        fourier.append({"n":n,"rank":observed})
    results["exact_alternating_quarter_fourier_ranks"]=fourier

    thresholds=[]
    for exponent in (32,64,128,256):
        n=1<<exponent
        original=next(q for q in range(1,exponent+1) if coarse(n,q,improved=False)[0]>=n//4)
        improved=next(q for q in range(1,exponent+1) if coarse(n,q)[0]>=n//4)
        thresholds.append({"exponent":exponent,"source_first_nonexcluded":original,"strengthened_first_nonexcluded":improved})
    assert [t["source_first_nonexcluded"] for t in thresholds]==[6,11,18,32]
    results["necessary_only_coarse_thresholds"]=thresholds

    # Tiny independent all-balanced-cut control: character cuts need not find
    # the best common cut. This is not a test of the large source instances.
    n=16
    orders=[]
    for seed in (1900+100*n,1901+100*n):
        order=list(range(n));random.Random(seed).shuffle(order);orders.append(order)
    orders.append(list(range(n)))
    character_best=min(sum(crossings(order,character_cut(n,h)[0]) for order in orders) for h in range(1,n))
    all_best=min(sum(crossings(order,(0,*rest)) for order in orders) for rest in itertools.combinations(range(1,n),n//2-1))
    assert all_best<=character_best
    results["tiny_common_cut_scope_control"]={"n":n,"character_min":character_best,"all_balanced_min":all_best}

    non_affine=[]
    for n,expected in ((128,63),(256,124),(512,248),(1024,501)):
        orders=[]
        for seed in (1900+100*n,1901+100*n):
            order=list(range(n));random.Random(seed).shuffle(order);orders.append(order)
        all_orders=orders+[list(range(n))]
        minimum=min(sum(crossings(order,character_cut(n,h)[0]) for order in all_orders) for h in range(1,n))
        assert minimum==expected
        seeded=random.Random(19100+n)
        stages=[]
        for order in orders:
            gamma=[seeded.randrange(1,P) for _ in range(n)]
            diagonal=[seeded.randrange(1,P) for _ in range(n)]
            stages.append(([(order,gamma,[1]*n,[1]*n)],diagonal))
        x=[seeded.randrange(P) for _ in range(n)]
        root=pow(3,(P-1)//n,P)
        reference=weyl_defects(lambda v:recursive_dft(v,root),x)
        candidate=weyl_defects(lambda v:circuit(stages,v),x)
        assert reference==[0,0] and candidate==[n,n]
        non_affine.append({"n":n,"best_character_crossings":minimum,"reference_weyl_defects":reference,"sampled_candidate_weyl_defects":candidate})
    results["independently_reproduced_non_affine_controls"]=non_affine

    try:
        import numpy as np
    except ImportError:
        results["numerical_svd_controls"]="SKIPPED: NumPy absent; not needed by exact checks"
    else:
        numerical=[]
        for n in (16,32,64,128):
            row=np.arange(0,n,2)[:,None]
            col=np.arange(n//2)[None,:]
            s=np.linalg.svd(np.exp(-2j*np.pi*row*col/n)/np.sqrt(n),compute_uv=False)
            deviation=float(np.max(abs(s-1/np.sqrt(2))))
            assert deviation<3e-13
            numerical.append({"n":n,"max_error_from_one_over_sqrt_two":deviation})
        results["numerical_svd_controls"]=numerical
    results["source_error_floor_N256_rank38"]=math.sqrt(26/90)
    results["status"]="PASS"
    results["elapsed_seconds"]=round(time.monotonic()-start,3)
    (HERE/"CHECK_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2),flush=True)


if __name__ == "__main__":
    run()
