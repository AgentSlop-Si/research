#!/usr/bin/env python3
"""New independent exact audit. Does not import or execute candidate/history code."""
import hashlib
import json
from pathlib import Path
import time
import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = Path('/workspace/shared/phase_rankzero_exact_20261019_1220')
LOWER = Path('/workspace/shared/phase_rankzero_20261019_1053/PROOF.md')
LOWER_REVIEW = Path('/workspace/shared/phase_rankzero_review_20261019_1104/REVIEW.md')
start = time.perf_counter()
assertions = 0

def require(ok, label):
    global assertions
    if not ok:
        raise AssertionError(label)
    assertions += 1

def digest(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

manifest = json.loads((SOURCE / 'MANIFEST.json').read_text())
before = {'manifest': digest(SOURCE / 'MANIFEST.json'), 'candidate_files': {},
          'inherited_lower_proof': digest(LOWER), 'inherited_lower_review': digest(LOWER_REVIEW)}
for name, expected in manifest['certificate'].items():
    actual = digest(SOURCE / name)
    require(actual == expected, 'candidate hash and byte count: ' + name)
    before['candidate_files'][name] = actual
(HERE / 'SOURCE_BINDINGS_BEFORE.json').write_text(json.dumps(before, indent=2) + '\n')

# Exact field arithmetic: h^2=sqrt(2)-1 and z^2-2hz+1=0.
# The desired embedding is h>0 and Im(z)>0. Conjugation sends z to 2h-z.
h, z = s.symbols('h z', real=True)
rt = s.sqrt(2)
ii = s.I
K = s.QQ.algebraic_field(rt, ii)
gb = s.groebner([z*z-2*h*z+1, h*h-rt+1], z, h, domain=K)

def red(expr):
    return s.expand(gb.reduce(s.expand(expr))[1])

def matred(mat):
    return mat.applyfunc(red)

def conj(expr):
    return red(s.conjugate(expr).subs(z, 2*h-z))

def adj(mat):
    return mat.T.applyfunc(conj)

def assertzero(expr, label):
    require(red(expr) == 0, label)

def assertmat(left, right, label):
    require(left.shape == right.shape, label + ' shape')
    for j in range(left.rows):
        for k in range(left.cols):
            assertzero(left[j,k]-right[j,k], f'{label} [{j},{k}]')

# Explicit eight roots and normalization. No floating point enters these controls.
roots = [1, (1+ii)/rt, ii, (-1+ii)/rt, -1, (-1-ii)/rt, -ii, (1-ii)/rt]
F = s.Matrix(8, 8, lambda j,k: roots[(-j*k) % 8]/s.sqrt(8))
I8 = s.eye(8)
assertmat(adj(F)*F, I8, 'normalized Fourier unitarity')
assertmat(F.T, F, 'Fourier transpose symmetry')
require(red((adj(F*s.sqrt(8))*(F*s.sqrt(8)))[0,0]-1) != 0,
        'negative control rejects unnormalized Fourier')

zi = 2*h-z
am = [-z, roots[7]*z, 1, roots[7]]
bm = [1, roots[3]*zi, -zi, roots[3]]
A = s.diag(*(am*2))
B = s.diag(*(bm*2))
assertmat(adj(A)*A, I8, 'phase A unitarity')
assertmat(adj(B)*B, I8, 'phase B unitarity')
U = matred(F*A*F*B)
assertmat(adj(U)*U, I8, 'full U unitarity')

# Construct the orthonormal sectors directly, without importing a block formula.
columns = []
for parity, sign in [(0,1),(0,-1),(1,1),(1,-1)]:
    for index in [parity, parity+2]:
        v = s.zeros(8,1)
        v[index] = 1/rt
        v[index+4] = sign/rt
        columns.append(v)
T = s.Matrix.hstack(*columns)
assertmat(T.T*T, I8, 'sector basis orthonormality')
U_sector = matred(T.T*U*T)

alpha = (1-z)/2
beta = -(1+z)/2
gamma = roots[7]*(1+z)/2
delta = ii*roots[7]*(1-z)/2
expected_blocks = [
    s.Matrix([[alpha,beta],[beta,alpha]])*s.diag(bm[0],bm[2]),
    s.Matrix([[gamma,delta],[delta,-gamma]])*s.diag(bm[0],bm[2]),
    s.Matrix([[beta,alpha],[alpha,beta]])*s.diag(bm[1],bm[3]),
    s.Matrix([[delta,-gamma],[-gamma,-delta]])*s.diag(bm[1],bm[3]),
]
assertmat(U_sector, s.diag(*expected_blocks), 'full Fourier-to-sector identity')
for k in range(4):
    block = U_sector[2*k:2*k+2, 2*k:2*k+2]
    want_tr = 1-h if k in (0,3) else roots[7]*(1+h)
    want_det = 1 if k in (0,3) else -ii
    assertzero(s.trace(block)-want_tr, f'block {k} trace')
    assertzero(block.det()-want_det, f'block {k} determinant')

# Check the phase square roots as actual radicals, separately from quotient arithmetic.
hv = s.sqrt(rt-1)
tv = s.sqrt(2-rt)
w = s.sqrt((1+hv)/2) + ii*s.sqrt((1-hv)/2)
rho = s.sqrt(2+rt)/2 + ii*s.sqrt(2-rt)/2
zv = hv+ii*tv
def actualzero(expr, label):
    require(s.simplify(s.expand_complex(expr)) == 0, label)
actualzero(zv*s.conjugate(zv)-1, 'actual z unit modulus')
actualzero(w*s.conjugate(w)-1, 'actual w unit modulus')
actualzero(w*w-zv, 'actual w square')
actualzero(rho*s.conjugate(rho)-1, 'actual rho unit modulus')
actualzero(rho*rho-roots[1], 'actual rho square')
p = [-ii*w, s.conjugate(rho)*w, 1, s.conjugate(rho)]
q = [1, rho**3*s.conjugate(w), ii*s.conjugate(w), rho**3]
av = [-zv, roots[7]*zv, 1, roots[7]]
bv = [1, roots[3]*s.conjugate(zv), -s.conjugate(zv), roots[3]]
for k in range(4):
    actualzero(p[k]**2-av[k], f'actual P square {k}')
    actualzero(q[k]**2-bv[k], f'actual Q square {k}')

# Direct external residual E = F - P* Re(P F Q) Q*.
# Expanding the real core gives this square-phase formula exactly.
E = matred((F-adj(A)*F.applyfunc(conj)*adj(B))/2)
G = matred(adj(E)*E)
HU = matred((U+adj(U))/2)
assertmat(G, matred(B*(I8-HU)*adj(B)/2), 'direct external residual Gram')
assertmat(adj(G), G, 'direct Gram Hermitian')

upper_sq = (1+h)/4
other_sq = (3-rt-(1+rt)*h)/4
assertmat((G-upper_sq*I8)*(G-other_sq*I8), s.zeros(8),
          'exact residual Gram annihilating polynomial')
assertzero(s.trace(G)-6*upper_sq-2*other_sq, 'exact Gram multiplicity trace')
G_sector = matred(T.T*G*T)
for j in range(8):
    for k in range(8):
        if j//2 != k//2:
            assertzero(G_sector[j,k], 'direct Gram off-sector zero')
for k in range(4):
    block = G_sector[2*k:2*k+2, 2*k:2*k+2]
    want_tr = 2*upper_sq if k in (0,3) else upper_sq+other_sq
    want_det = upper_sq**2 if k in (0,3) else upper_sq*other_sq
    assertzero(s.trace(block)-want_tr, f'direct Gram block {k} trace')
    assertzero(block.det()-want_det, f'direct Gram block {k} determinant')

# Independent radical identity for the angular branches.
c = (1-h)/2
d = (1+h)/2
sin_theta = rt*d-c
assertzero(c*c+sin_theta*sin_theta-1, 'theta sine positive radical identity')
assertzero((c+sin_theta)/rt-d, 'cos(theta-pi/4)=d')
assertzero((1-c)/2-upper_sq, 'half-angle upper square')
assertzero((1-sin_theta)/2-other_sq, 'other singular square')
assertzero((4+2*rt)*c*(1-c)-1, 'candidate scalar identity')

# Destructive control: change only the sign of B's third phase and reject its spectrum.
B_wrong = s.diag(*([bm[0], bm[1], -bm[2], bm[3]]*2))
E_wrong = matred((F-adj(A)*F.applyfunc(conj)*adj(B_wrong))/2)
G_wrong = matred(adj(E_wrong)*E_wrong)
require(red(s.trace(G_wrong)-6*upper_sq-2*other_sq) != 0,
        'negative control rejects wrong B third-phase sign')

# Source immutability is checked after all original computations.
after = {'manifest': digest(SOURCE / 'MANIFEST.json'), 'candidate_files': {},
         'inherited_lower_proof': digest(LOWER), 'inherited_lower_review': digest(LOWER_REVIEW)}
for name, expected in manifest['certificate'].items():
    actual = digest(SOURCE / name)
    require(actual == expected, 'post-run candidate hash and byte count: '+name)
    after['candidate_files'][name] = actual
require(before == after, 'all bound sources unchanged throughout audit')
(HERE / 'SOURCE_BINDINGS_AFTER.json').write_text(json.dumps(after, indent=2) + '\n')

upper = s.sqrt(1+hv)/2
lower = s.sin(3*s.pi/16)
old = 1/s.sqrt(2)
result = {
    'status': 'PASS', 'independent_exact_assertions': assertions,
    'elapsed_seconds': time.perf_counter()-start,
    'upper_exact': 'sqrt(1+sqrt(sqrt(2)-1))/2',
    'upper_decimal_40_digits': str(s.N(upper,40)),
    'lower_inherited_exact': 'sin(3*pi/16), strict',
    'lower_decimal_40_digits': str(s.N(lower,40)),
    'gram_eigenvalues': [
        {'value': '(1+h)/4', 'multiplicity': 6},
        {'value': '(3-sqrt(2)-(1+sqrt(2))*h)/4', 'multiplicity': 2}],
    'other_singular_value': str(s.N(s.sqrt(other_sq.subs(h,hv)),40)),
    'interval_width': str(s.N(upper-lower,40)),
    'width_reduction_fraction': str(s.N((old-upper)/(old-lower),40)),
    'candidate_and_historical_code_executed': False,
    'global_optimum_claimed': False,
    'external_writes': False,
}
(HERE / 'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
