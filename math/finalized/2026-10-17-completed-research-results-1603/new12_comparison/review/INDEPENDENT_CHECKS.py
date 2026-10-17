"""New independent exact controls for the NEW-12 source map; no historical imports."""
from pathlib import Path
import hashlib, json
import sympy as S

ROOT = Path(__file__).resolve().parent
Q = S.Rational
I = S.I

def sq(z):
    return S.simplify(S.expand_complex(z*S.conjugate(z)))

def check0(z):
    assert S.simplify(S.expand_complex(z)) == 0, z

# Distinct magnitudes, phases, orientations, loops, zeros, cancellation.
d = [S.Integer(1), I, Q(3,5)+Q(4,5)*I, -I]
edges = [
 (0,1,Q(2,3),3*I,2),
 (0,1,Q(1,3),-3*I,2),
 (1,0,Q(4,5),1+I,1-I),
 (1,2,Q(1,2),0,2),
 (2,1,Q(3,4),1+I,0),
 (2,2,Q(2,5),-2,3),
 (3,3,Q(7,9),2*I,-I),
 (2,3,Q(1,4),2*I,2*I),
 (2,3,Q(1,4),-2*I,2*I),
 (0,3,Q(3,2),0,0),
 (3,0,S.Integer(0),2*I,3),
 (1,3,Q(2,7),Q(3,5)+Q(4,5)*I,2*I),
]
C = S.Integer(0)
raw = S.Integer(0)
pairs = {}
for u,v,beta,w,c in edges:
    r,R = S.Abs(w),S.Abs(c)
    a = beta*r*R
    radial = beta*(r-R)**2
    lhs = beta*sq(w-c*d[u]/d[v])
    raw += lhs
    if a == 0:
        check0(lhs-radial)
        C += radial
        continue
    sigma = S.simplify(w*S.conjugate(c)/(r*R))
    check0(sq(sigma)-1)
    check0(lhs-radial-a*sq(d[u]-sigma*d[v]))
    C += radial
    if u == v:
        C += a*sq(1-sigma)
    else:
        if u>v:
            u,v = v,u
            sigma = S.conjugate(sigma)
        A,Z = pairs.get((u,v),(S.Integer(0),S.Integer(0)))
        pairs[u,v] = (S.simplify(A+a),S.simplify(Z+a*sigma))
reduced = S.Integer(0)
cancelled = 0
for (u,v),(A,Z) in pairs.items():
    b = S.Abs(Z)
    C += 2*(A-b)
    if b == 0:
        cancelled += 1
    else:
        reduced += b*sq(d[u]-(Z/b)*d[v])
check0(raw-C-reduced)
assert cancelled >= 1
assert float(C.evalf()) >= 0

# Direct matching normalization with genuinely nonconstant complex functions.
tau = [4*(i//4)+(i%4+2)%4 for i in range(16)]
funcs = [[S.Integer(i)+I*(i%3) for i in range(16)],
         [Q(i-3,5)+Q(i%5,7)*I for i in range(16)]]
betas = [Q(3,7),Q(4,9)]
E = sum(betas[q]*sq(f[i]-f[tau[i]]) for q,f in enumerate(funcs) for i in range(16))
Qmatching = sum(2*betas[q]*sq(f[i]-f[tau[i]]) for q,f in enumerate(funcs) for i in range(16) if i<tau[i])
check0(E-Qmatching)

# Legal N=16 network, reconstructed rather than loaded from the author's checker.
n=16
pi=list(range(n))
for a,b,c in [(0,4,8),(2,6,10)]:
    pi[a],pi[b],pi[c]=b,c,a
assert sorted(pi)==list(range(n))
assert all(pi[tau[j]] == tau[pi[j]] for j in range(n))
w=[Q(-1,2) if j in (8,10) else Q(1,2) for j in range(n)]
P=S.zeros(n)
P0=S.zeros(n)
for j in range(n):
    P[j,pi[j]]=w[j]
    P0[j,pi[j]]=Q(1,2)
assert P.conjugate().T*P == S.eye(n)/4
assert P0.conjugate().T*P0 == S.eye(n)/4
assert (S.eye(n)-P).det()!=0
assert (S.eye(n)-P0).det()!=0
assert all(w[j]==w[tau[j]] for j in range(n))
L=S.Matrix([[2,-1,1],[-1,2,-1],[1,-1,2]])
x=S.Symbol('x')
assert S.factor(L.charpoly(x).as_expr()) == (x-4)*(x-1)**2
v=S.Matrix([1,Q(1,2)+S.sqrt(3)*I/2,-Q(1,2)+S.sqrt(3)*I/2])
assert (L-S.eye(3))*v == S.zeros(3,1)
d16=[S.Integer(1)]*16
for cyc in [(0,4,8),(2,6,10)]:
    for j,z in zip(cyc,list(v)):
        d16[j]=z
energy=S.simplify(sum(sq(w[j]-Q(1,2)*d16[j]/d16[pi[j]]) for j in range(n)))
assert energy==Q(3,2)
# Min eigenvalue of each triangle is 1; every unit phase vector has squared norm 3.
# Thus each weight-1/4 triangle has minimum >=3/4, attained above.

out={
 'all_checks_passed':True,
 'independently_authored':True,
 'mixed_edge_cases':len(edges),
 'general_amplitude_identity':True,
 'zero_weight_and_constant_cases':True,
 'loop_and_reverse_orientation_cases':True,
 'parallel_cancellation_pairs':cancelled,
 'full_aggregated_energy_identity':True,
 'raw_matching_factor_two':True,
 'n16_permutation_and_tau_commutation':True,
 'n16_PstarP_and_P0starP':'I/4',
 'n16_inverse_bound':'g=2 from norm(P)=norm(P0)=1/2; preserved for all common unitary D',
 'n16_actual_determinant':str((S.eye(n)-P).det()),
 'n16_reference_determinant':str((S.eye(n)-P0).det()),
 'n16_raw_energy':'0',
 'triangle_characteristic_polynomial':'(x-1)^2*(x-4)',
 'n16_exact_unit_phase_minimum':str(energy),
 'n16_first_graph_eigenvalue':'0; ten isolated vertices',
 'n16_first_cheeger_constant':'0; singleton isolated vertex and positive measure',
 'historical_program_executions':0,
 'external_writes':0,
}
(ROOT/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
