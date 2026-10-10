"""Exact full-state circuit verification against an independent RN-by-RN solve."""
import json
import random
from pathlib import Path
from port_feedback import prepare_ports, closure_word, coupling_edit_word
from prior_affine_reuse import (prepare, execute, execute_scalar, expand_scalar,
                                inverse, charge, apply_t, apply_j)


def dense_inverse(matrix, p):
    """Independent test oracle, not part of the compiler or its cost claim."""
    n = len(matrix)
    work = [row[:] + [int(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if work[i][j] % p), None)
        if pivot is None:
            raise ValueError('singular oracle matrix')
        work[j], work[pivot] = work[pivot], work[j]
        factor = pow(work[j][j], -1, p)
        work[j] = [v*factor % p for v in work[j]]
        for i in range(n):
            if i != j:
                factor = work[i][j]
                work[i] = [(a-factor*b) % p for a,b in zip(work[i],work[j])]
    return [row[n:] for row in work]


def system(plan, fb):
    n, R, d, p = plan['n'], fb['batches'], fb['d'], plan['p']
    matrix = [[int(i == j) for j in range(R*n)] for i in range(R*n)]
    for i in range(n):
        for j in range(n):
            edge = sum(fb['u'][i][a]*fb['coupling'][a][b]*fb['v_rows'][b][j]
                       for a in range(d) for b in range(d)) % p
            matrix[i][(R-1)*n+j] = (matrix[i][(R-1)*n+j]-edge) % p
    for r in range(1,R):
        for i in range(n):
            matrix[r*n+i][(r-1)*n+i] = -plan['diagonal'][i] % p
            matrix[r*n+i][(r-1)*n+(i+1)%n] = -plan['weights'][i] % p
    return matrix


def expected(plan, fb, injections, initial, base, full_inverse):
    n, R, p = plan['n'], fb['batches'], plan['p']
    forcing = [0]*(R*n)
    for vertex, source in injections:
        values = apply_t(plan, initial[source*n:(source+1)*n])
        for i, value in enumerate(values):
            forcing[vertex*n+i] = (forcing[vertex*n+i]+value) % p
    solution = [sum(a*b for a,b in zip(row, forcing)) % p for row in full_inverse]
    # Independently verify every block equation, including the actual closing edge.
    lhs = [sum(a*b for a,b in zip(row,solution)) % p for row in system(plan,fb)]
    assert lhs == forcing
    result = initial[:]
    for i, value in enumerate(solution):
        result[base+i] = (result[base+i]+value) % p
    return result


def pick_feedback(plan,R,d,ports,rng):
    for _ in range(100):
        u = [[rng.randrange(plan['p']) for j in range(d)] for i in range(plan['n'])]
        coupling = [[rng.randrange(plan['p']) for j in range(d)] for i in range(d)]
        try:
            return prepare_ports(plan,R,u,coupling,ports)
        except ValueError as error:
            assert 'singular' in str(error)
    raise AssertionError('could not choose a nonsingular test')


def pick_edit(plan,fb,injections,rng):
    for _ in range(100):
        a = [rng.randrange(plan['p']) for _ in range(fb['d'])]
        b = [rng.randrange(plan['p']) for _ in range(fb['d'])]
        try:
            return coupling_edit_word(plan,fb,injections,a,b)
        except ValueError as error:
            assert 'singular' in str(error)
    raise AssertionError('could not choose a nonsingular edit')


def main():
    rng = random.Random(731111)
    cases = []
    basis_total = random_total = 0
    for p in (65537,998244353):
        for n in (2,4,8):
            plan = prepare(n,p)
            for R in (1,3):
                for d in (1,2,3):
                    for port_kind in ('coordinate','shared_krylov'):
                        ports = [(i % n,0) for i in range(d)] if port_kind == 'coordinate' else [(n-1,i) for i in range(d)]
                        fb = pick_feedback(plan,R,d,ports,rng)
                        oracle = dense_inverse(system(plan,fb),p)
                        for mode,injections in (
                                ('one_root',[(0,0)]),
                                ('independent_roots',[(r,r) for r in range(R)]),
                                ('repeated_source',[(0,0),(R-1,0),(R//2,1)])):
                            word,cost = closure_word(plan,fb,injections)
                            scalar = expand_scalar(word,p)
                            assert len(scalar) == cost['scalar_instructions'] == charge(word)['expanded_scalar_instructions']
                            edit,new,ecost = pick_edit(plan,fb,injections,rng)
                            escalar = expand_scalar(edit,p)
                            assert len(escalar) == ecost['scalar_instructions']
                            new_oracle = dense_inverse(system(plan,new),p)
                            fresh_new = prepare_ports(plan,R,new['u'],new['coupling'],ports)
                            assert new['sinv'] == fresh_new['sinv']
                            assert new['effective'] == fresh_new['effective']
                            word2,new2,ecost2 = pick_edit(plan,new,injections,rng)
                            new2_oracle = dense_inverse(system(plan,new2),p)
                            new_closure,_ = closure_word(plan,new,injections)
                            base = cost['target_base']
                            size = base+R*n
                            for coordinate in range(size):
                                initial = [int(i == coordinate) for i in range(size)]
                                want = expected(plan,fb,injections,initial,base,oracle)
                                got = execute(word,initial,p)
                                assert got == want == execute_scalar(scalar,initial,p)
                                assert got[:base] == initial[:base]
                                assert execute(inverse(word,p),got,p) == initial
                                new_want = expected(plan,new,injections,initial,base,new_oracle)
                                assert execute(edit,got,p) == new_want == execute_scalar(escalar,got,p)
                                assert execute(inverse(edit,p),new_want,p) == got
                                assert execute(new_closure,initial,p) == new_want
                                basis_total += 1
                            for _ in range(3):
                                initial = [rng.randrange(p) for i in range(size)]
                                want = expected(plan,fb,injections,initial,base,oracle)
                                assert execute_scalar(scalar,initial,p) == want
                                new_want = expected(plan,new,injections,initial,base,new_oracle)
                                assert execute_scalar(escalar,want,p) == new_want
                                second_want = expected(plan,new2,injections,initial,base,new2_oracle)
                                assert execute(word2,new_want,p) == second_want
                                random_total += 1
                            cases.append({'p':p,'n':n,'R':R,'d':d,'port_kind':port_kind,
                                          'mode':mode,'basis_vectors':size,
                                          'shared_orbit_steps':fb['shared_orbit_steps'],
                                          'unshared_orbit_steps':fb['unshared_orbit_steps'],
                                          'preparation':fb['coefficient_preparation'],
                                          'initial_cost':cost,'edit_cost':ecost})
    plan = prepare(4,65537)
    # Invertible S with a zero first pivot; a row swap is essential.
    u = [[1,0],[0,1],[0,0],[0,0]]
    fb = prepare_ports(plan,1,u,[[1,-1],[-1,1]],[(0,0),(1,0)])
    assert fb['preparation_row_swaps'] == 1
    singular_rejections = 0
    try:
        prepare_ports(plan,1,u,[[1,0],[0,1]],[(0,0),(1,0)])
    except ValueError as e:
        assert 'singular' in str(e)
        singular_rejections += 1
    else:
        raise AssertionError('singular initial loop accepted')
    fb = prepare_ports(plan,1,u,[[0,0],[0,0]],[(0,0),(1,0)])
    try:
        coupling_edit_word(plan,fb,[(0,0)],[1,0],[1,0])
    except ValueError as e:
        assert 'singular' in str(e)
        singular_rejections += 1
    else:
        raise AssertionError('singular edited loop accepted')
    invalid_rejections = 0
    for injections in ([],[(-1,0)],[(1,0)],[(0,-1)],[(0,1.5)]):
        for call in (lambda:closure_word(plan,fb,injections),
                     lambda:coupling_edit_word(plan,fb,injections,[0,0],[1,0])):
            try:
                call()
            except ValueError:
                invalid_rejections += 1
            else:
                raise AssertionError('invalid injection accepted')
    assert coupling_edit_word(plan,fb,[(0,0)],[0,0],[1,0])[0] == []
    different_root_plan = prepare(4,65537,pow(3,-1,65537))
    for call in (lambda:closure_word(different_root_plan,fb,[(0,0)]),
                 lambda:coupling_edit_word(different_root_plan,fb,[(0,0)],[0,0],[1,0])):
        try:
            call()
        except ValueError as e:
            assert 'mismatch' in str(e)
        else:
            raise AssertionError('different-root plan accepted for cached coefficients')
    # Insertion order is intentionally not register order. A pivot may contain
    # zero; only its known coefficient is inverted by the reversible compiler.
    unsorted_fb = pick_feedback(plan,3,2,[(3,0),(3,1)],rng)
    unsorted_injections = [(2,3),(0,1),(1,3)]
    unsorted_word,unsorted_cost = closure_word(plan,unsorted_fb,unsorted_injections)
    unsorted_base = unsorted_cost['target_base']
    initial = [(17*i+3)%65537 for i in range(unsorted_base+12)]
    initial[4] = 0
    unsorted_want = expected(plan,unsorted_fb,unsorted_injections,initial,unsorted_base,
                            dense_inverse(system(plan,unsorted_fb),65537))
    assert execute_scalar(expand_scalar(unsorted_word,65537),initial,65537) == unsorted_want
    edit,unsorted_new,_ = pick_edit(plan,unsorted_fb,unsorted_injections,rng)
    unsorted_new_want = expected(plan,unsorted_new,unsorted_injections,initial,unsorted_base,
                                dense_inverse(system(plan,unsorted_new),65537))
    assert execute_scalar(expand_scalar(edit,65537),unsorted_want,65537) == unsorted_new_want
    examples = []
    for n,R,d in ((32,4,2),(64,4,4),(128,8,4)):
        plan = prepare(n)
        ports = [(n-1,i) for i in range(d)]
        fb = pick_feedback(plan,R,d,ports,rng)
        for mode,injections in (('one_root',[(0,0)]),('independent_roots',[(r,r) for r in range(R)])):
            word,cost = closure_word(plan,fb,injections)
            update,new,ecost = pick_edit(plan,fb,injections,rng)
            assert cost['scalar_instructions'] == charge(word)['expanded_scalar_instructions']
            assert ecost['scalar_instructions'] == charge(update)['expanded_scalar_instructions']
            examples.append({'n':n,'R':R,'d':d,'mode':mode,
                             'preparation':fb['coefficient_preparation'],
                             'shared_orbit_steps':fb['shared_orbit_steps'],
                             'unshared_orbit_steps':fb['unshared_orbit_steps'],
                             'initial_cost':cost,'edit_cost':ecost})
    report = {'status':'PASS','cases':len(cases),'full_state_basis_vectors':basis_total,
              'edit_full_state_basis_vectors':basis_total,'random_full_states':random_total,
              'second_edit_random_states':random_total,'singular_rejections':singular_rejections,
              'invalid_injection_rejections':invalid_rejections,'pivot_swap_case':True,
              'different_root_plan_rejections':2,
              'unsorted_source_bank_and_zero_pivot_case':True,
              'scope':'Exact port-feedback reuse; first T calls and coefficient setup charged; no fresh FFT speedup.',
              'examples':examples,'cases_detail':cases}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('examples','cases_detail')},indent=2))


if __name__ == '__main__':
    main()
