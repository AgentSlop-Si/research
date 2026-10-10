#!/usr/bin/env python3
"""Independent exact review of route lifting, bank folding, and the N16 gate.

Standard library only. No constructor or uploaded code is imported or run.
"""
import argparse
import json
from pathlib import Path
import random

P = 998244353
LABELS = [(axis, c, sign) for axis in ('H', 'V')
          for c in (0, 1) for sign in (-1, 1)]


def inv(x):
    assert x % P
    return pow(x, -1, P)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    bt = list(zip(*b))
    return [[sum(x*y for x, y in zip(row, col)) % P for col in bt] for row in a]


def sub(a, b):
    return [[(x-y) % P for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, t):
    return [[x*t % P for x in row] for row in a]


def determinant(a):
    b = [row[:] for row in a]
    n = len(b)
    out = 1
    for c in range(n):
        pivot = next((r for r in range(c, n) if b[r][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            b[pivot], b[c] = b[c], b[pivot]
            out = -out
        t = b[c][c]
        out = out*t % P
        it = inv(t)
        for r in range(c+1, n):
            q = b[r][c]*it % P
            if q:
                b[r] = [(x-q*y) % P for x, y in zip(b[r], b[c])]
    return out % P


def pivots(a):
    b = [row[:] for row in a]
    row = 0
    answer = []
    for c in range(len(b[0])):
        pivot = next((r for r in range(row, len(b)) if b[r][c]), None)
        if pivot is None:
            continue
        b[pivot], b[row] = b[row], b[pivot]
        b[row] = [x*inv(b[row][c]) % P for x in b[row]]
        for r in range(row+1, len(b)):
            q = b[r][c]
            if q:
                b[r] = [(x-q*y) % P for x, y in zip(b[r], b[row])]
        answer.append(c)
        row += 1
        if row == len(b):
            break
    return answer


def solve(a, rhs):
    n = len(a)
    b = [row[:] + [v] for row, v in zip(a, rhs)]
    for c in range(n):
        pivot = next(r for r in range(c, n) if b[r][c])
        b[pivot], b[c] = b[c], b[pivot]
        t = inv(b[c][c])
        b[c] = [v*t % P for v in b[c]]
        for r in range(n):
            if r != c:
                t = b[r][c]
                b[r] = [(x-t*y) % P for x, y in zip(b[r], b[c])]
    return [row[-1] for row in b]


def cover(a, b, label):
    axis, c, sign = label
    out = []
    for x in range(a):
        for y in range(b):
            if axis == 'H':
                out.append(((x+sign*(2*y+c)) % a)*b+y)
            else:
                out.append(x*b+(y+sign*(2*x+c)) % b)
    return out


def splice(p):
    seen = set()
    reps = []
    for v in range(len(p)):
        if v in seen:
            continue
        reps.append(v)
        w = v
        while w not in seen:
            seen.add(w)
            w = p[w]
        assert w == v
    q = p[:]
    if len(reps) > 1:
        for j, v in enumerate(reps):
            q[v] = p[reps[(j+1) % len(reps)]]
    return q, reps


def green(p, weights):
    n = len(p)
    product = 1
    for w in weights:
        product = product*w % P
    guard = (1-product) % P
    assert guard
    out = [[0]*n for _ in range(n)]
    for source in range(n):
        dest, value = source, inv(guard)
        visited = set()
        for _ in range(n):
            assert dest not in visited
            visited.add(dest)
            out[dest][source] = value
            dest = p[dest]
            value = value*weights[dest] % P
        assert dest == source
    # Full inverse test by sparse left multiplication.
    for source, dest in enumerate(p):
        for c in range(n):
            assert (out[dest][c]-weights[dest]*out[source][c]) % P == int(dest == c)
    return out


def root(n):
    assert (P-1) % n == 0
    z = pow(3, (P-1)//n, P)
    assert pow(z, n, P) == 1
    if n > 1:
        assert pow(z, n//2, P) == P-1
    return z


def fourier(n):
    z = root(n)
    return [[pow(z, i*j, P) for j in range(n)] for i in range(n)]


def bank(a, b, active):
    f = fourier(b)
    out = [[0]*(a*b) for _ in range(a*b)]
    for x in range(a):
        block = f if x in active else eye(b)
        for i in range(b):
            out[x*b+i][x*b:x*b+b] = block[i]
    return out


def projection(a, b):
    return [((v//(2*b)) % a)*b+(v % (2*b)) % b for v in range(4*a*b)]


def qleft(a, pi, n):
    out = [[0]*len(a[0]) for _ in range(n)]
    for v, row in enumerate(a):
        out[pi[v]] = [(x+y) % P for x, y in zip(out[pi[v]], row)]
    return out


def qright(a, pi):
    return [[row[v] for v in pi] for row in a]


def route_tests():
    rows = []
    dense = []
    for rectangular in (False, True):
        for r in range(1, 6):
            m = 1 << r
            a, b = ((2*m, m) if rectangular else (m, m))
            n = a*b
            pi = projection(a, b)
            support_sum, rank_bound_sum = 0, 0
            for label in LABELS:
                ts, tl = cover(a, b, label), cover(2*a, 2*b, label)
                ps, cs = splice(ts)
                pl, cl = splice(tl)
                assert all(pi[tl[v]] == ts[pi[v]] for v in range(4*n))
                ends = [(pi[pl[v]], ps[pi[v]]) for v in range(4*n)]
                support = sum(x != y for x, y in ends)
                support_bound = len(cl)+4*len(cs)
                rank_bound = len(cl)+len(cs)-2
                assert support <= support_bound
                support_sum += support_bound
                rank_bound_sum += rank_bound
                if n <= 16:
                    d = [[0]*(4*n) for _ in range(n)]
                    for v, (x, y) in enumerate(ends):
                        d[x][v] = (d[x][v]+1) % P
                        d[y][v] = (d[y][v]-1) % P
                    actual_rank = len(pivots(d))
                    assert actual_rank <= min(n-1, rank_bound)
                    tau = inv(3)
                    gs = green(ps, [tau]*n)
                    gl = green(pl, [tau]*(4*n))
                    lhs = sub(qleft(gl, pi, n), qright(gs, pi))
                    rhs = scale(mul(mul(gs, d), gl), tau)
                    assert lhs == rhs
                    ws = [v+2 for v in range(n)]
                    wl = [ws[v] for v in pi]
                    gws = green(ps, ws)
                    gwl = green(pl, wl)
                    weighted_d = [[ws[i]*x % P for x in row] for i, row in enumerate(d)]
                    assert sub(qleft(gwl, pi, n), qright(gws, pi)) == mul(mul(gws, weighted_d), gwl)
                    dense.append({'N':n,'label':label,'defect_support':support,
                                  'defect_rank':actual_rank,'rank_bound':rank_bound,
                                  'scalar_resolvent_full_entries':n*4*n,
                                  'weighted_resolvent_full_entries':n*4*n})
            if rectangular:
                assert support_sum == 12*m*(3*r+8)
                assert rank_bound_sum == 18*m*(r+3)-16
            else:
                assert support_sum == 8*m*(3*r+7)
                assert rank_bound_sum == 4*m*(3*r+8)-16
            rows.append({'N':n,'shape':'rectangle' if rectangular else 'square',
                         'support_bound_sum':support_sum,'rank_bound_sum':rank_bound_sum})
    n = 16
    bad_tau = root(4*n)
    assert pow(bad_tau, n, P) != 1 and pow(bad_tau, 4*n, P) == 1
    return {'structural_cases':rows,'full_resolvent_cases':dense,
            'guard_counterexample':{'N':n,'tau':bad_tau,'small_inverse_exists':True,'large_inverse_exists':False}}


def folding_tests():
    local = []
    for m in (1, 2, 4, 8, 16, 32, 64):
        fm, fl = fourier(m), fourier(2*m)
        plus = [[(fl[i][j]+fl[i+m][j]) % P for j in range(2*m)] for i in range(m)]
        minus = [[(fl[i][j]-fl[i+m][j]) % P for j in range(2*m)] for i in range(m)]
        expected_plus = [[2*fm[i][j//2] % P if j % 2 == 0 else 0 for j in range(2*m)] for i in range(m)]
        expected_minus = [[2*pow(root(2*m),i,P)*fm[i][j//2] % P if j % 2 else 0 for j in range(2*m)] for i in range(m)]
        assert plus == expected_plus and minus == expected_minus
        s = [[(2*int(j == 2*i)-int(j % m == i)) % P for j in range(2*m)] for i in range(m)]
        minor = [[row[2*j] for j in range(m)] for row in s]
        det = determinant(minor)
        assert det == pow(2,m-1,P)
        naive = sub(plus, [[fm[i][j % m] for j in range(2*m)] for i in range(m)])
        assert naive == mul(fm,s)
        assert len(pivots(naive)) == m
        local.append({'m':m,'even_minor_determinant':det,'folding_defect_rank':m})
    global_rows = []
    for a,b in [(2,2),(4,2),(4,4),(8,4),(8,8)]:
        n = a*b
        active = set(range(a//2))
        lifted = active | {x+a for x in active}
        pi = projection(a,b)
        assert all(((v//(2*b)) in lifted) == ((pi[v]//b) in active) for v in range(4*n))
        delta = sub(qleft(bank(2*a,2*b,lifted),pi,n),qright(bank(a,b,active),pi))
        rank = len(pivots(delta))
        assert rank == b*len(active) == n//2
        fourier_delta = sub(qleft(fourier(4*n),pi,n),qright(fourier(n),pi))
        fourier_delta_rank = len(pivots(fourier_delta))
        assert fourier_delta_rank == n
        global_rows.append({'a':a,'b':b,'N':n,'active_small':sorted(active),
                            'active_large':sorted(lifted),'global_bank_defect_rank':rank,
                            'unnormalized_global_Fourier_defect_rank':fourier_delta_rank})
    return {'local':local,'global':global_rows}


def hierarchical_step(a, b, label, ps):
    n = a*b
    ts = cover(a,b,label)
    tl = cover(2*a,2*b,label)
    pi = projection(a,b)
    eta = [0]*n
    for v in range(n):
        eta[ts[v]] = ps[v]
    hsmall = sum(x != y for x,y in zip(ps,ts))
    preliminary = []
    for w in tl:
        x,y = divmod(w,2*b)
        newx,newy = divmod(eta[(x % a)*b+(y % b)],b)
        preliminary.append((newx+a*(x//a))*(2*b)+newy+b*(y//b))
    assert sum(x != y for x,y in zip(preliminary,tl)) == 4*hsmall
    assert all(pi[preliminary[v]] == ps[pi[v]] for v in range(4*n))
    seen = set()
    selected = []
    lengths = []
    for v in range(4*n):
        if v in seen:
            continue
        w, members = v, []
        while w not in seen:
            seen.add(w)
            members.append(w)
            w = preliminary[w]
        assert w == v and len(members) % n == 0
        selected.append(min(t for t in members if pi[t] == 0))
        lengths.append(len(members))
    assert len(selected) <= 4
    selected.sort()
    pl = preliminary[:]
    if len(selected) > 1:
        for j,v in enumerate(selected):
            pl[v] = preliminary[selected[(j+1) % len(selected)]]
    assert all(pi[pl[v]] == ps[pi[v]] for v in range(4*n))
    assert len(splice(pl)[1]) == 1
    hlarge = sum(x != y for x,y in zip(pl,tl))
    assert hlarge <= 4*hsmall+4
    return pl, {'small_N':n,'label':label,'small_edits':hsmall,'large_edits':hlarge,
                'premerge_cycle_lengths':lengths,'premerge_cycle_count':len(selected),
                'exact_quotient':True,'hamiltonian':True}


def hierarchical_tests():
    rows = []
    for rectangular in (False,True):
        a,b = ((4,2) if rectangular else (2,2))
        ps = [splice(cover(a,b,label))[0] for label in LABELS]
        for level in range(4):
            lifted = []
            for label,p in zip(LABELS,ps):
                newp,row = hierarchical_step(a,b,label,p)
                row.update({'base_shape':'rectangle' if rectangular else 'square','level':level+1})
                rows.append(row)
                lifted.append(newp)
            ps = lifted
            a,b = 2*a,2*b
    margins = []
    for n0,d0,coefficient in [(1<<17,7936,752),(1<<18,11264,15344)]:
        # Multiply the loss inequality by three to stay integral.
        for level in range(65):
            n = n0*4**level
            three_loss = 3*d0*4**level+16*(4**level-1)
            margin = 3*n//16-three_loss
            assert margin == coefficient*4**level+16 > 0
        margins.append({'seed_N':n0,'seed_loss_bound':d0,
                        'rational_margin_formula':f'{coefficient}*4^level+16',
                        'levels_checked':65})
    return {'instances':rows,'threshold_margin_controls':margins,
            'scope':'A new quotient-compatible splice family, not the original minimum-representative family or a Fourier coefficient lift.'}


def seed_templates(n):
    k = n.bit_length()-1
    m = 1 << (k//2)
    a, b = ((2*m,m) if k % 2 else (m,m))
    permutations = [splice(cover(a,b,label))[0] for label in LABELS]
    greens = [green(p,[inv(j+2)]*n) for j,p in enumerate(permutations)]
    return permutations,greens


def layer(greens, coefficients):
    n = len(greens[0])
    return [[sum(coefficients[t][i]*greens[t][i][j] for t in range(8)) % P
             for j in range(n)] for i in range(n)]


def outer_gate(greens, prefix, target):
    gx = [mul(g,prefix) for g in greens]
    rows = []
    for i in range(len(prefix)):
        template = [g[i] for g in gx]
        columns = pivots(template)
        assert len(columns) == 8
        equations = [[template[j][c] for j in range(8)] for c in columns]
        coeff = solve(equations,[target[i][c] for c in columns])
        residuals = [(sum(coeff[j]*template[j][c] for j in range(8))-target[i][c]) % P
                     for c in range(len(prefix))]
        failures = [c for c,v in enumerate(residuals) if v]
        row = {'row':i,'pivot_columns':columns,'pivot_determinant':determinant(equations),
               'outer_coefficients':coeff,'failure_columns':failures,'residuals':residuals}
        if failures:
            selected = columns+[failures[0]]
            minor = [[line[c] for c in selected] for line in template+[target[i]]]
            det = determinant(minor)
            assert det
            row.update({'augmented_columns':selected,'augmented_minor':minor,'augmented_determinant':det})
        rows.append(row)
    return rows


def seed_tests():
    # Deterministic primality verification validates the modular field.
    assert P > 2 and P % 2
    assert all(P % d for d in range(3, int(P**0.5)+1, 2))
    z = root(16)
    assert z == 929031873 and pow(z,8,P) == P-1
    ps,gs = seed_templates(16)
    assert len({tuple(p) for p in ps}) == 6
    b = bank(4,4,{0,1})
    ones = [[1]*16 for _ in range(8)]
    h = layer(gs,ones)
    prefix = mul(mul(h,b),h)
    det_prefix = determinant(prefix)
    assert det_prefix == 195063167
    target = fourier(16)
    rejected = outer_gate(gs,prefix,target)
    assert all(len(row['failure_columns']) == 8 for row in rejected)
    assert rejected[0]['augmented_determinant'] == 750393234
    rng = random.Random(348196)
    supplied = [[[rng.randrange(1,P) for _ in range(16)] for _ in range(8)] for _ in range(3)]
    hs = [layer(gs,c) for c in supplied]
    generated_prefix = mul(mul(hs[1],b),hs[0])
    assert determinant(generated_prefix)
    generated = mul(hs[2],generated_prefix)
    accepted = outer_gate(gs,generated_prefix,generated)
    assert all(not row['failure_columns'] for row in accepted)
    assert all(accepted[i]['outer_coefficients'] == [supplied[2][j][i] for j in range(8)] for i in range(16))
    changed = [row[:] for row in generated]
    changed[0][0] = (changed[0][0]+1) % P
    assert outer_gate(gs,generated_prefix,changed)[0]['failure_columns']
    def covariance_failures(a):
        return [(i,j) for i in range(16) for j in range(15) if (a[i][j+1]-pow(z,i,P)*a[i][j]) % P]
    assert not covariance_failures(target) and all(row[0] == 1 for row in target)
    twice = scale(target,2)
    assert not covariance_failures(twice) and all(row[0] != 1 for row in twice)
    diagnostics = []
    for n in (4,8,16,32,64):
        perms, greens = seed_templates(n)
        ranks = [len(pivots([g[i] for g in greens])) for i in range(n)]
        assert all(r == min(8,n) for r in ranks)
        diagnostics.append({'N':n,'distinct_cycles':len({tuple(p) for p in perms}),'row_template_ranks':ranks})
    return {'prime':P,'root16':z,'cycles':ps,'pole_denominators':list(range(2,10)),
            'parameters':384,'green_occurrences':24,'fixed_inner_entries':256,'free_outer_entries':128,
            'fixed_prefix_determinant':det_prefix,'fixed_prefix_rejection_rows':rejected,
            'generated_product_control':{'all_256_entries_pass':True,'all_128_outer_entries_recovered':True,'all_384_supplied_entries_nonzero':True},
            'seed_guard_control':'2F16 passes all 240 successor equations and fails all 16 seed equations.',
            'diagnostics':diagnostics,'scope':'Only the all-ones inner prefix is excluded; the 384-variable family remains open.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',default='VERIFIED_RESULTS.json')
    args = parser.parse_args()
    result = {'status':'PASS','field':P,'route':route_tests(),'folding':folding_tests(),
              'hierarchical':hierarchical_tests(),'seed':seed_tests()}
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','route_structural_cases':len(result['route']['structural_cases']),
                      'full_resolvent_cases':len(result['route']['full_resolvent_cases']),
                      'global_bank_cases':len(result['folding']['global']),
                      'hierarchical_instances':len(result['hierarchical']['instances']),
                      'N16_first_augmented_minor':result['seed']['fixed_prefix_rejection_rows'][0]['augmented_determinant']},sort_keys=True))


if __name__ == '__main__':
    main()
