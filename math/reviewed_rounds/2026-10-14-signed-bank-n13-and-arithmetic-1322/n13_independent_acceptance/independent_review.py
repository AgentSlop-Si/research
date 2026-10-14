#!/usr/bin/env python3
"""Fresh N13 reviewer. Candidate files are inert JSON/text; none are executed.

Independent routes: left multiplication in the Weyl algebra; scalar determinant
interpolation with formal degree bound; fixed-last-coefficient recurrence census;
fresh literal inversions from raw certificate parameters and weights.
"""
import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

P, N, Q = 53, 13, 16
COUNTS = {"witness_inversions": 0, "control_inversions": 0,
          "two_sided_inverse_products": 0, "scalar_minor_determinants": 0,
          "degree7_polynomials": 0, "degree7_root_evaluations": 0}

def clean(a):
    a = [v % P for v in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]

def padd(a, b):
    return clean([(a[k] if k < len(a) else 0) + (b[k] if k < len(b) else 0)
                  for k in range(max(len(a), len(b)))])

def pmul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i+j] += u*v
    return clean(c)

def value(a, x):
    return sum(c*pow(x, j, P) for j, c in enumerate(a)) % P

def determinant(a):
    a = [r[:] for r in a]
    d = 1
    for k in range(len(a)):
        j = next((j for j in range(k, len(a)) if a[j][k] % P), None)
        if j is None:
            return 0
        if j != k:
            a[k], a[j] = a[j], a[k]
            d = -d
        d = d*a[k][k] % P
        iv = pow(a[k][k], -1, P)
        for i in range(k+1, len(a)):
            f = a[i][k]*iv % P
            for j in range(k+1, len(a)):
                a[i][j] = (a[i][j]-f*a[k][j]) % P
            a[i][k] = 0
    return d

def inverse(a):
    n = len(a)
    # Row-operation matrix, kept separate from the input coefficient matrix.
    a = [r[:] for r in a]
    v = [[int(i == j) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = next((r for r in range(k, n) if a[r][k]), None)
        assert pivot is not None, "singular literal matrix"
        a[k], a[pivot] = a[pivot], a[k]
        v[k], v[pivot] = v[pivot], v[k]
        factor = pow(a[k][k], -1, P)
        a[k] = [factor*x % P for x in a[k]]
        v[k] = [factor*x % P for x in v[k]]
        for r in range(n):
            if r == k:
                continue
            factor = a[r][k]
            a[r] = [(x-factor*y) % P for x, y in zip(a[r], a[k])]
            v[r] = [(x-factor*y) % P for x, y in zip(v[r], v[k])]
    assert a == [[int(i == j) for j in range(n)] for i in range(n)]
    return v

def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) % P
             for col in zip(*b)] for row in a]

def linear_image(a, v):
    return [sum(x*y for x, y in zip(row, v)) % P for row in a]

def rank(a):
    a = [r[:] for r in a]
    k = 0
    for col in range(len(a[0])):
        j = next((r for r in range(k, len(a)) if a[r][col]), None)
        if j is None:
            continue
        a[k], a[j] = a[j], a[k]
        factor = pow(a[k][col], -1, P)
        a[k] = [x*factor % P for x in a[k]]
        for r in range(k+1, len(a)):
            factor = a[r][col]
            a[r] = [(x-factor*y) % P for x, y in zip(a[r], a[k])]
        k += 1
        if k == len(a):
            break
    return k

def interpolate(xs, ys):
    # Full Lagrange formula; no polynomial division or symbolic elimination.
    out = [0]
    for i, x in enumerate(xs):
        term, divisor = [1], 1
        for j, y in enumerate(xs):
            if i == j:
                continue
            term = pmul(term, [-y, 1])
            divisor = divisor*(x-y) % P
        coefficient = ys[i]*pow(divisor, -1, P) % P
        out = padd(out, [coefficient*z for z in term])
    return out

def coefficients():
    assert all(P % k for k in range(2, math.isqrt(P)+1))
    assert [k for k in range(1, N+1) if pow(Q, k, P) == 1] == [N]
    f = [[pow(Q, -r*t, P) for t in range(N)] for r in range(N)]
    weyl = [[sum(f[(t+a) % N][t]*pow(Q, -b*t, P) for t in range(N))
             * pow(N, -1, P) % P for b in range(N)] for a in range(N)]
    gamma = weyl[0][0]
    assert gamma == 7
    target = [[x*pow(gamma, -1, P) % P for x in row] for row in weyl]
    assert all(target[a][b] == pow(Q, pow(4, -1, N)*(a+b)**2, P)
               for a in range(N) for b in range(N))
    D = {}
    for e, d in itertools.product((1, -1), repeat=2):
        z = pow(Q, e*d, P)
        level = {(0, 0): 1}
        D[e, d, 0, 0] = 1
        # Left multiplication: U U^r V^ell + V U^r V^ell.
        for degree in range(1, N+1):
            following = {}
            for (r, ell), c in level.items():
                following[r+1, ell] = (following.get((r+1, ell), 0)+c) % P
                following[r, ell+1] = (following.get((r, ell+1), 0)
                                       + c*pow(z, r, P)) % P
            level = following
            for (r, ell), c in level.items():
                D[e, d, r, ell] = c
        assert all(D[e, d, r, N-r] == int(r in (0, N)) for r in range(N+1))
    def G(e, d, a, b):
        r, ell = e*a % N, d*b % N
        return D[e, d, r, ell] if r+ell < N else 0
    # Reflection is checked entry by entry without changing q or gamma.
    reflection_checks = 0
    for e, d in itertools.product((1, -1), repeat=2):
        for a, b in itertools.product(range(N), repeat=2):
            assert G(e, d, a, b) == G(-e, -d, -a, -b)
            assert target[a][b] == target[-a % N][-b % N]
            reflection_checks += 1
    moments, triples = {}, {}
    for b in range(1, 7):
        corner = G(-1, 1, N-b, b)
        assert corner and target[N-b][b] == 1
        assert all(G(e, d, N-b, b) == 0 for e, d in ((1,1),(1,-1),(-1,-1)))
        moments[b], triples[b] = [], []
        for a in range(b, N-b):
            den = G(1, 1, a, b)
            assert den and G(1, -1, a, b) == 0 and G(-1, -1, a, b) == 0
            u = target[a][b]*pow(den, -1, P) % P
            v = G(-1, 1, a, b)*pow(corner*den % P, -1, P) % P
            power = N-a-b
            polynomial = [u]+[0]*power
            polynomial[power] -= v
            moments[b].append(clean(polynomial))
            triples[b].append([u, v, power])
    return f, weyl, gamma, target, G, moments, triples, reflection_checks

def recurrence_rows(moments, degree):
    rows, labels = [], []
    for b in moments:
        for j in range(len(moments[b])-degree):
            rows.append(moments[b][j:j+degree+1])
            labels.append([b,j])
    return rows, labels

def literal_bank(e, d, alpha, beta, weights, which):
    assert e in (-1,1) and d in (-1,1)
    delta = (1-pow(alpha, N, P)-pow(beta, N, P)) % P
    assert delta
    total = [[0]*N for _ in range(N)]
    branches = []
    identity = [[int(i == j) for j in range(N)] for i in range(N)]
    for j, weight in enumerate(weights):
        a = [[int(r == t) for t in range(N)] for r in range(N)]
        for t in range(N):
            a[(t+e) % N][t] = (a[(t+e) % N][t]-alpha) % P
            a[t][t] = (a[t][t]-beta*pow(Q, e*d*j+d*t, P)) % P
        inv = inverse(a)
        COUNTS[which+"_inversions"] += 1
        assert mm(a, inv) == identity and mm(inv, a) == identity
        COUNTS["two_sided_inverse_products"] += 2
        branches.append(inv)
        for r, t in itertools.product(range(N), repeat=2):
            total[r][t] = (total[r][t]+weight*pow(N,-1,P)*inv[r][t]) % P
    return delta, total, branches

def extract(bank):
    return [[sum(bank[(t+a) % N][t]*pow(Q,-b*t,P) for t in range(N))
             *pow(N,-1,P) % P for b in range(N)] for a in range(N)]

def amplitudes(e, d, beta, delta, weights, gamma):
    return [pow(beta, d*b % N, P)*pow(N*delta*gamma % P,-1,P)
            *sum(w*pow(Q,e*b*j,P) for j,w in enumerate(weights)) % P
            for b in range(N)]

def paid_schedule(raw, vector):
    # Constants below are preprocessing. The operation counts refer only to
    # applying the prepared schedule to this input vector.
    bank_outputs = []
    multiplications = additions = 0
    for bank in raw:
        e,d,alpha,beta = bank['epsilon'],bank['delta_sign'],bank['alpha'],bank['beta']
        assert alpha
        order = [(-e*s) % N for s in range(N)]
        inv_alpha = pow(alpha,-1,P)
        b = [-inv_alpha*vector[t] % P for t in order]
        multiplications += N
        branch_outputs = []
        for j,weight in enumerate(bank['raw_weights']):
            a = [(1-beta*pow(Q,e*d*j+d*t,P))*inv_alpha % P for t in order]
            product = math.prod(a) % P
            assert (1-product) % P
            closure_inverse = pow((1-product) % P,-1,P)
            weighted = weight*pow(N,-1,P) % P
            closure = b[0]
            for s in range(1,N):
                closure = (a[s]*closure+b[s]) % P
                multiplications += 1
                additions += 1
            x = [0]*N
            x[0] = closure*closure_inverse % P
            multiplications += 1
            for s in range(N-1):
                x[order[s+1]] = (a[s]*x[order[s]]+b[s]) % P
                multiplications += 1
                additions += 1
            branch_outputs.append([weighted*c % P for c in x])
            multiplications += N
        bank_outputs.append([sum(column) % P for column in zip(*branch_outputs)])
        additions += N*(N-1)
    result = [sum(column) % P for column in zip(*bank_outputs)]
    additions += N*(len(raw)-1)
    return result,multiplications,additions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    f, weyl, gamma, target, G, moments, triples, reflections = coefficients()
    rows6, labels6 = recurrence_rows(moments, 6)
    rows7, labels7 = recurrence_rows(moments, 7)
    assert (len(rows6), len(rows6[0]), len(rows7), len(rows7[0])) == (9,7,6,8)
    fresh_minors = []
    for ids in (list(range(7)), [0,1,2,3,4,5,7]):
        matrix = [rows6[i] for i in ids]
        # Leibniz's formula gives this rigorous degree bound, independent of
        # cancellations. Exhaust all 7! column assignments to obtain the bound.
        bound = max(sum(len(matrix[r][perm[r]])-1 for r in range(7))
                    for perm in itertools.permutations(range(7)))
        assert bound < P
        vals = []
        for y in range(P):
            vals.append(determinant([[value(v,y) for v in row] for row in matrix]))
            COUNTS["scalar_minor_determinants"] += 1
        poly = interpolate(list(range(bound+1)), vals[:bound+1])
        assert all(value(poly,y) == vals[y] for y in range(P))
        assert len(poly)-1 == 39
        fresh_minors.append({"row_indices":ids,"formal_degree_bound":bound,
                             "coefficients_ascending":poly,"values":vals})
    census = []
    for y in range(1,P):
        r6 = [[value(p,y) for p in row] for row in rows6]
        assert rank(r6) == 7
        r7 = [[value(p,y) for p in row] for row in rows7]
        coefficient6 = [r[:6] for r in r7]
        det = determinant(coefficient6)
        assert det, "fixed last free coefficient unavailable"
        inv = inverse(coefficient6)
        members = []
        for last in range(P):
            rhs = [(-r[7]-last*r[6]) % P for r in r7]
            first = linear_image(inv,rhs)
            poly = first+[last,1]
            assert linear_image(r7,poly) == [0]*6
            roots = [x for x in range(1,P) if value(poly,x) == 0]
            assert len(roots) < 7
            COUNTS["degree7_polynomials"] += 1
            COUNTS["degree7_root_evaluations"] += P-1
            members.append({"coefficient_t6":last,"polynomial_ascending":poly,
                            "distinct_nonzero_roots":roots})
        census.append({"y":y,"degree6_augmented_rank":7,
                       "degree7_first6_coefficient_minor":det,"members":members})

    # Comparison starts here. Candidate scripts remain inert source bytes.
    candidate = json.loads((root/"sources/GATE.json").read_text())
    baseline = json.loads((root/"sources/BASELINE.json").read_text())
    assert candidate["target"] == f and candidate["target_weyl"] == weyl
    assert candidate["moment_polynomials"] == {str(k):v for k,v in moments.items()}
    assert candidate["moment_triples"] == {str(k):v for k,v in triples.items()}
    assert candidate["degree6_rows"] == rows6 and candidate["degree6_row_labels"] == labels6
    assert candidate["degree7_rows"] == rows7 and candidate["degree7_labels"] == labels7
    assert len(candidate["degree6_augmented_maximal_minors"]) == 2
    for fresh, supplied in zip(fresh_minors,candidate["degree6_augmented_maximal_minors"]):
        assert all(fresh[k] == supplied[k] for k in supplied)
    bezout = [0]
    assert len(candidate["minor_bezout"]) == 2
    for fresh, coefficient in zip(fresh_minors,candidate["minor_bezout"]):
        bezout = padd(bezout,pmul(fresh["coefficients_ascending"],coefficient))
    assert bezout == [1] and candidate["minor_gcd"] == [1]
    assert len(candidate["census"]) == 52
    for fresh, supplied in zip(census,candidate["census"]):
        assert fresh["y"] == supplied["y"]
        assert not supplied["degree6"]["consistent"]
        assert supplied["degree7"]["rank"] == 6 and supplied["degree7"]["consistent"]
        assert len(supplied["degree7_enumeration"]) == 53
        ours = {tuple(m["polynomial_ascending"]):m["distinct_nonzero_roots"] for m in fresh["members"]}
        theirs = {tuple(m["polynomial_ascending"]):m["distinct_nonzero_roots"] for m in supplied["degree7_enumeration"]}
        assert ours == theirs
        assert supplied["degree7_split_members"] == []
    assert candidate["split_degree7_members"] == []
    max_roots = max(len(m["distinct_nonzero_roots"]) for c in census for m in c["members"])
    assert max_roots == 6

    total = [[0]*N for _ in range(N)]
    raw = baseline["raw_certificate"]
    assert len(raw) == 24
    prescribed = [(1,1,x) for x in range(1,12)]+[(-1,1,1),(1,-1,1)]+[(-1,-1,x) for x in range(1,12)]
    witness_report, fresh_bank_matrices = [], []
    grouped = {}
    for i, (bank, (e,d,alpha)) in enumerate(zip(raw,prescribed)):
        assert (bank["epsilon"],bank["delta_sign"],bank["alpha"],bank["beta"]) == (e,d,alpha,1)
        weights = bank["raw_weights"]
        assert len(weights) == N and all(isinstance(w,int) and 0 <= w < P for w in weights)
        delta, literal, branches = literal_bank(e,d,alpha,1,weights,"witness")
        amp = amplitudes(e,d,1,delta,weights,gamma)
        assert bank["denominator"] == delta and bank["sector_amplitudes"] == amp
        assert baseline["literal_banks"][i]["bank"] == literal
        assert baseline["literal_banks"][i]["inverses"] == branches
        actual_coeff = extract(literal)
        assert all(actual_coeff[a][b] == gamma*amp[b]*pow(alpha,e*a % N,P)*G(e,d,a,b) % P
                   for a,b in itertools.product(range(N),repeat=2))
        nonzero_entries = sum(x != 0 for row in literal for x in row)
        assert nonzero_entries and any(amp)
        assert baseline["deletion_mismatch_counts"][i] == nonzero_entries
        grouped.setdefault((e,d,alpha),[0]*N)
        grouped[e,d,alpha] = [(u+v) % P for u,v in zip(grouped[e,d,alpha],amp)]
        for r,t in itertools.product(range(N),repeat=2):
            total[r][t] = (total[r][t]+literal[r][t]) % P
        witness_report.append({"index":i,"signs":[e,d],"alpha":alpha,"beta":1,
                               "denominator":delta,"nonzero_matrix_entries":nonzero_entries,
                               "sector_amplitudes":amp})
        fresh_bank_matrices.append(literal)
    assert total == f == baseline["aggregate"]
    effective = {str((e,d)):sum(ee==e and dd==d and any(v) for (ee,dd,a),v in grouped.items())
                 for e,d in itertools.product((1,-1),repeat=2)}
    assert effective == {"(1, 1)":11,"(1, -1)":1,"(-1, 1)":1,"(-1, -1)":11}
    sector_ranks = []
    for b in range(N):
        matrix = [[pow(a,e*r % N,P)*G(e,d,r,b) % P for e,d,a in prescribed] for r in range(N)]
        rhs = [target[r][b] for r in range(N)]
        assert linear_image(matrix,[w["sector_amplitudes"][b] for w in witness_report]) == rhs
        sector_ranks.append(rank(matrix))
        assert baseline["sectors"][b]["matrix"] == matrix and baseline["sectors"][b]["target"] == rhs
        assert baseline["sectors"][b]["rank"] == sector_ranks[-1]
    assert sector_ranks == [13]*13
    # Verify the separately claimed paid cyclic-solve schedule on a full
    # basis. Counts deliberately charge all scalar multiplications/additions.
    schedule_receipts = []
    for t in range(N):
        basis = [int(k==t) for k in range(N)]
        result,muls,adds = paid_schedule(raw,basis)
        assert result == [row[t] for row in f]
        assert muls == 12168 and adds == 11531
        schedule_receipts.append({"basis_index":t,"multiplications":muls,"additions":adds})
    inverse2 = pow(2,-1,N)
    assert all(pow(Q,-r*t,P) == pow(Q,-inverse2*r*r,P)*pow(Q,inverse2*(r-t)**2,P)
               *pow(Q,-inverse2*t*t,P) % P for r,t in itertools.product(range(N),repeat=2))

    controls = []
    for e,d in itertools.product((1,-1),repeat=2):
        for alpha,beta in ((0,2),(2,0),(2,3)):
            weights = [(j*j+3*j+7) % P for j in range(N)]
            delta, literal, unused = literal_bank(e,d,alpha,beta,weights,"control")
            amp = amplitudes(e,d,beta,delta,weights,gamma)
            coeff = extract(literal)
            assert all(coeff[a][b] == gamma*amp[b]*pow(alpha,e*a % N,P)*G(e,d,a,b) % P
                       for a,b in itertools.product(range(N),repeat=2))
            controls.append({"epsilon":e,"delta_sign":d,"alpha":alpha,"beta":beta,"denominator":delta,
                             "all_169_original_bank_coefficients_pass":True})
    # Positive recurrence and padding controls ensure the rejection checker
    # recognizes an actual <=6-node moment family, including repeated/zero nodes.
    padding_controls = []
    for nodes in ([2,3,5],[2,2,3],[0,2,3],list(range(1,7))):
        support = sorted(set(nodes)-{0})
        h = [1]
        for x in support:
            h = pmul(h,[-x,1])
        h = [0]*(6-len(support))+h
        seq = [sum((i+1)*pow(x,k,P) for i,x in enumerate(nodes)) % P for k in range(1,12)]
        assert all(sum(h[j]*seq[s+j] for j in range(7)) % P == 0 for s in range(5))
        padding_controls.append({"nodes":nodes,"padded_annihilator":h,"passed":True})
    control_counts = {"omit_normalization":sum(N*total[r][t] % P != f[r][t] for r,t in itertools.product(range(N),repeat=2)),
                      "reverse_target":sum(total[r][t] != pow(Q,r*t,P) for r,t in itertools.product(range(N),repeat=2)),
                      "one_raw_weight_plus_one":None}
    damaged = raw[0]["raw_weights"][:]
    damaged[0] = (damaged[0]+1) % P
    # First inverse is already freshly checked; perturbing w_0 adds inv_0/N.
    e,d,a = prescribed[0]
    branch = [[int(r==t) for t in range(N)] for r in range(N)]
    for t in range(N):
        branch[(t+e) % N][t] = (branch[(t+e) % N][t]-a) % P
        branch[t][t] = (branch[t][t]-pow(Q,d*t,P)) % P
    perturbation = inverse(branch)
    control_counts["one_raw_weight_plus_one"] = sum(x != 0 for row in perturbation for x in row)
    assert all(control_counts.values())
    assert baseline["omit_normalization_mismatches"] == control_counts["omit_normalization"]
    assert baseline["reverse_target_mismatches"] == control_counts["reverse_target"]
    bindings = [{"path":str(p.relative_to(root)),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in sorted((root/"sources").iterdir()) if p.is_file()]
    summary = {"verdict":"ACCEPT within the stated N13/q16 characteristic-53 singleton-cross grammar",
               "N":N,"p":P,"q":Q,"gamma":gamma,"minor_degrees":[39,39],
               "minor_formal_degree_bounds":[m["formal_degree_bound"] for m in fresh_minors],
               "bezout_combination":bezout,"all_extension_physical_lower_bound":16,
               "base_field_physical_lower_bound":18,"base_field_physical_upper_bound":24,
               "witness_effective_allocation":effective,"witness_nonzero_physical_banks":24,
               "witness_target_entries_verified":N*N,"sector_ranks":sector_ranks,
               "reflection_checks":reflections,"census_count":len(census),"split_degree7_members":0,
               "maximum_degree7_nonzero_roots":max_roots,
               "paid_schedule":{"basis_vectors_checked":13,"multiplications_per_application":12168,
                                "additions_per_application":11531,"preprocessing_excluded":True,
                                "chirp_identity_entries_checked":169},
               "falsification_controls":control_counts,"counts":COUNTS,
               "limitations":["No exact optimum","No unrestricted cross-support lower bound",
                              "No other q or characteristic","No novelty or arithmetic speed claim"]}
    outputs = {"SUMMARY.json":summary,"FRESH_MINORS.json":fresh_minors,"FRESH_CENSUS.json":census,
               "FRESH_WITNESS.json":{"banks":witness_report,"aggregate":total,"sector_ranks":sector_ranks},
               "PAID_SCHEDULE.json":schedule_receipts,
               "CONTROLS.json":{"arbitrary_beta_controls":controls,"padding_controls":padding_controls},
               "SOURCE_BINDINGS.json":bindings}
    for name, data in outputs.items():
        (out/name).write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    (out/"TIMING.json").write_text(json.dumps({"elapsed_seconds":time.monotonic()-started},indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True,indent=2))

if __name__ == "__main__":
    main()
