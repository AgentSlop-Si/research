"""Exact rank-d cycle closure and rank-one coupling edits, without clean scratch.

All coefficient arithmetic is counted. The emitted scalar circuit charges every
first T call. This is a reuse compiler, not a faster fresh Fourier transform.
"""
from prior_feedback import Counted, add_j_word, rank_one_add
from prior_affine_reuse import add_t_word


def dot(c, x, y):
    value = c.mul(x[0], y[0])
    for a, b in zip(x[1:], y[1:]):
        value = c.add(value, c.mul(a, b))
    return value


def mm(c, a, b):
    columns = list(zip(*b))
    return [[dot(c, row, col) for col in columns] for row in a]


def mv(c, a, v):
    return [dot(c, row, v) for row in a]


def invert(c, a):
    """Counted, pivoted Gauss-Jordan; even zero-factor eliminations are charged."""
    d = len(a)
    work = [row[:] + [int(i == j) for j in range(d)]
            for i, row in enumerate(a)]
    swaps = 0
    for k in range(d):
        pivot = next((i for i in range(k, d) if work[i][k]), None)
        if pivot is None:
            raise ValueError('singular port closure')
        if pivot != k:
            work[pivot], work[k] = work[k], work[pivot]
            swaps += 1
        reciprocal = c.inv(work[k][k])
        work[k] = [c.mul(v, reciprocal) for v in work[k]]
        for i in range(d):
            if i == k:
                continue
            factor = work[i][k]
            work[i] = [c.sub(v, c.mul(factor, w))
                       for v, w in zip(work[i], work[k])]
    return [row[d:] for row in work], swaps


def jt(c, plan, v):
    n = plan['n']
    return [c.add(c.mul(plan['diagonal'][i], v[i]),
                  c.mul(plan['weights'][(i-1) % n], v[(i-1) % n]))
            for i in range(n)]


def kt(c, plan, v):
    return [v[0]] + [c.add(v[i], c.mul(plan['weights'][i-1], v[i-1]))
                     for i in range(1, plan['n'])]


def j_action(c, plan, v):
    n = plan['n']
    return [c.add(c.mul(plan['diagonal'][i], v[i]),
                  c.mul(plan['weights'][i], v[(i+1) % n]))
            for i in range(n)]


def validate_matrix(matrix, rows, cols, name, p):
    if len(matrix) != rows or any(len(row) != cols for row in matrix):
        raise ValueError('invalid ' + name + ' dimensions')
    return [[int(v) % p for v in row] for row in matrix]


def prepare_ports(plan, batches, u, coupling, ports):
    """ports[l]=(coordinate,shift) means V_l=(J^T)^shift e_coordinate.

    Closure: z_0=b_0+U coupling V^T z_last, z_r=b_r+J z_(r-1).
    Common-coordinate ports share both transpose Krylov walks. No T is called.
    """
    n, p, d = plan['n'], plan['p'], len(ports)
    if not isinstance(batches, int) or batches < 1 or d < 1:
        raise ValueError('positive batch and port counts required')
    if any(not isinstance(j, int) or not isinstance(s, int)
           or not 0 <= j < n or s < 0 for j, s in ports):
        raise ValueError('invalid observation port')
    u = validate_matrix(u, n, d, 'U', p)
    coupling = validate_matrix(coupling, d, d, 'coupling', p)
    c = Counted(p)
    h = batches - 1
    group_limits = {}
    for j, s in ports:
        group_limits[j] = max(group_limits.get(j, 0), h+s)
    walks = {}
    for j, limit in group_limits.items():
        left = [[int(i == j) for i in range(n)]]
        row = [[plan['kernel'][j-i] if i <= j else 0 for i in range(n)]]
        for _ in range(limit):
            left.append(jt(c, plan, left[-1]))
            row.append(kt(c, plan, row[-1]))
        walks[j] = (left, row)
    v_rows = [walks[j][0][s] for j, s in ports]
    a_rows = [walks[j][0][h+s] for j, s in ports]
    rows = [[walks[j][1][h-r+s] for r in range(batches)] for j, s in ports]
    g = mm(c, a_rows, u)
    glambda = mm(c, g, coupling)
    schur = [[c.sub(int(i == j), glambda[i][j]) for j in range(d)]
             for i in range(d)]
    sinv, swaps = invert(c, schur)
    factor = mm(c, coupling, sinv)
    effective = mm(c, u, factor)
    steps = sum(group_limits.values())
    assert dict(c.count) == {
        'mul':steps*(3*n-1)+2*n*d*d+4*d*d*d,
        'add':steps*(2*n-1)+(n-1)*d*d+2*d*d*(d-1)+n*d*(d-1),
        'sub':d*d+2*d*d*(d-1), 'constant_inverse':d}
    return {'n':n, 'p':p, 'q':plan['q'], 'batches':batches, 'd':d, 'u':u,
            'coupling':coupling, 'ports':list(ports), 'v_rows':v_rows,
            'a_rows':a_rows, 'rows':rows, 'g':g, 'sinv':sinv,
            'effective':effective, 'coefficient_preparation':dict(c.count),
            'preparation_row_swaps':swaps, 'shared_orbit_steps':steps,
            'unshared_orbit_steps':sum(h+s for j,s in ports),
            'generated_orbit_field_elements':2*n*sum(v+1 for v in group_limits.values())}


def layout(plan, feedback, injections):
    n, R = plan['n'], feedback['batches']
    if feedback['n'] != n or feedback['p'] != plan['p'] or feedback['q'] != plan['q']:
        raise ValueError('plan and feedback mismatch')
    if not injections:
        raise ValueError('at least one injection required')
    if any(not isinstance(vertex, int) or not isinstance(source, int)
           or not 0 <= vertex < R or source < 0 for vertex, source in injections):
        raise ValueError('invalid injection')
    banks = 1 + max(source for vertex, source in injections)
    return banks, (banks+1)*n


def port_functionals(plan, feedback, injections, c):
    n = plan['n']
    functionals = []
    for port_rows in feedback['rows']:
        values = {}
        for vertex, source in injections:
            for i, value in enumerate(port_rows[vertex]):
                index = source*n+i
                values[index] = c.add(values.get(index, 0), value)
        functionals.append(values)
    return functionals


def closure_word(plan, feedback, injections):
    """Add all closed-loop solutions to arbitrary targets; preserve all sources."""
    n, p, R = plan['n'], plan['p'], feedback['batches']
    banks, base = layout(plan, feedback, injections)
    c = Counted(p)
    functionals = port_functionals(plan, feedback, injections, c)
    word = []
    for r in reversed(range(1, R)):
        word.extend(add_j_word(plan, base+(r-1)*n, base+r*n, -1))
    for vertex, source in injections:
        word.extend(add_t_word(plan, source*n, base+vertex*n))
    rank_costs = []
    for ell in range(feedback['d']):
        vector = [row[ell] for row in feedback['effective']]
        correction, cost = rank_one_add(p, functionals[ell], base, vector)
        word.extend(correction)
        rank_costs.append(cost)
    for r in range(1, R):
        word.extend(add_j_word(plan, base+(r-1)*n, base+r*n))
    baseline = 3*len(injections)*n*(n+1)//2+2*(R-1)*(6*n-3)
    return word, {'source_banks':banks, 'target_base':base,
                  'ADD_T_calls':len(injections), 'feedback_extra_ADD_T_calls':0,
                  'acyclic_scalar_instructions':baseline,
                  'rank_one_corrections':rank_costs,
                  'scalar_instructions':baseline+sum(x['scalar_instructions'] for x in rank_costs),
                  'source_pivot_constant_inverses':sum(x['source_pivot_inverse'] for x in rank_costs),
                  'scalar_expansion_constant_inverses':len({g[3] for g in word if g[0]=='shear' and g[3]}),
                  'coefficient_preparation':dict(c.count)}


def coupling_edit_word(plan, feedback, injections, a, b):
    """Update coupling by a*b^T using one global rank-one ADD and zero T calls.

    Return the new prepared state for further edits. Coefficient preparation is
    charged, including updating its small inverse and effective U factor.
    """
    n, p, R, d = plan['n'], plan['p'], feedback['batches'], feedback['d']
    banks, base = layout(plan, feedback, injections)
    if len(a) != d or len(b) != d:
        raise ValueError('invalid edit vector dimensions')
    a, b = [x % p for x in a], [x % p for x in b]
    c = Counted(p)
    z = mv(c, feedback['sinv'], mv(c, feedback['g'], a))
    theta = c.sub(1, dot(c, b, z))
    if theta == 0:
        raise ValueError('singular edited port closure')
    reciprocal = c.inv(theta)
    v = [dot(c, b, col) for col in zip(*feedback['sinv'])]
    lambdaz = mv(c, feedback['coupling'], z)
    alpha = [c.mul(c.add(x,y), reciprocal) for x,y in zip(a,lambdaz)]
    direction = mv(c, feedback['u'], alpha)
    vector = []
    for r in range(R):
        vector.extend(direction)
        if r+1 < R:
            direction = j_action(c, plan, direction)
    functionals = port_functionals(plan, feedback, injections, c)
    functional = {}
    for ell, values in enumerate(functionals):
        for i, value in values.items():
            functional[i] = c.add(functional.get(i,0), c.mul(v[ell], value))
    word, rank_cost = rank_one_add(p, functional, base, vector)
    # Keep the next closure compiler ready; no d^3 inversion or dense refactor.
    new_coupling = [[c.add(feedback['coupling'][i][j], c.mul(a[i],b[j]))
                     for j in range(d)] for i in range(d)]
    new_sinv = [[c.add(feedback['sinv'][i][j],
                      c.mul(c.mul(z[i],v[j]), reciprocal))
                 for j in range(d)] for i in range(d)]
    root_direction = vector[:n]
    new_effective = [[c.add(feedback['effective'][i][j], c.mul(root_direction[i],v[j]))
                      for j in range(d)] for i in range(n)]
    m, q = len(injections), len({source for vertex,source in injections})
    assert dict(c.count) == {
        'mul':7*d*d+2*d+2*n*d+2*n*(R-1)+d*q*n,
        'add':6*d*d-2*d-1+n*(2*d+R-2)+d*n*(m+q),
        'sub':1, 'constant_inverse':1}
    new = dict(feedback)
    new.update(coupling=new_coupling, sinv=new_sinv, effective=new_effective)
    # These report the current edit, not a fresh-inverse preparation claim.
    new['last_edit_preparation'] = dict(c.count)
    return word, new, {'source_banks':banks, 'target_base':base, 'theta':theta,
                       'ADD_T_calls':0, 'rank_one_correction':rank_cost,
                       'scalar_instructions':rank_cost['scalar_instructions'],
                       'source_pivot_constant_inverses':rank_cost['source_pivot_inverse'],
                       'scalar_expansion_constant_inverses':len({g[3] for g in word if g[0]=='shear' and g[3]}),
                       'coefficient_preparation':dict(c.count)}
