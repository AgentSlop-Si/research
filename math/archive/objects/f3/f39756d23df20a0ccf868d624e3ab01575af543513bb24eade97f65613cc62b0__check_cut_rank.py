"""Fresh standard-library control; imports/reads no supplied project program or data."""
from itertools import permutations
import json
from pathlib import Path

S = {0, 1, 2, 3}
pi = (1, 2, 3, 4, 5, 6, 7, 0)
sigma = (2, 7, 5, 0, 6, 1, 3, 4)
z = (0, 1, 0, 0)
one = (1, 0, 0, 0)
zero = (0, 0, 0, 0)

def add(a, b):
    return tuple(x+y for x,y in zip(a,b))

def neg(a):
    return tuple(-x for x in a)

def mul(a, b):
    c = [0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j] += x*y
    for k in range(6,3,-1):
        c[k-4] -= c[k]
    return tuple(c[:4])

def power(k):
    a = one
    for _ in range(k % 8):
        a = mul(a,z)
    return a

edges = {name: [(j,p[j]) for j in sorted(S) if p[j] not in S]
         for name,p in [('pi',pi),('sigma',sigma)]}
assert edges == {'pi': [(3,4)], 'sigma': [(1,7),(2,5)]}
D = zero
for p in permutations(range(4)):
    a = one
    for r,c in enumerate(p):
        a = mul(a,power((r+4)*c))
    if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4)) % 2:
        a = neg(a)
    D = add(D,a)
v = one
for i in range(4,8):
    for j in range(i+1,8):
        v = mul(v,add(power(j),neg(power(i))))
assert v == D == (-4,4,-4,0)
assert all((j//2)*2 in S and (j//2)*2+1 in S for j in S)
result = {
    'status': 'PASS',
    'support_maps': {'pi': pi, 'sigma': sigma},
    'cut': sorted(S),
    'outgoing_edges': edges,
    'inverse_sum_cross_rank_upper_bound': 3,
    'fourier_cross_rank': 4,
    'fourier_block_determinant_basis_1_z_z2_z3': D,
    'vandermonde_product_agrees': D == v,
    'supplied_programs_executed_or_imported': False,
    'scope': 'Finite exact control; all-field rank proof is in CUT_RANK_PROOF.md.'
}
Path(__file__).with_name('CUT_RANK_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
