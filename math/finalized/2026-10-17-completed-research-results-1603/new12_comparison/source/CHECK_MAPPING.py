"""Fresh exact controls for the new comparison only. No historical code is loaded."""
import json
from pathlib import Path
import sympy as S

ROOT=Path(__file__).resolve().parents[1]
I=S.I
def norm2(z):
    return S.simplify(z*S.conjugate(z))
def mag(z):
    return S.sqrt(norm2(z))

# The legal N=16 route and weight fixture from the comparison.
N=16
tau=[4*(i//4)+(i%4+2)%4 for i in range(N)]
pi=list(range(N))
for cyc in [(0,4,8),(2,6,10)]:
    for a,b in zip(cyc,cyc[1:]+cyc[:1]): pi[a]=b
assert all(pi[tau[i]]==tau[pi[i]] for i in range(N))
w=[S.Rational(1,2)]*N
w[8]=w[10]=-S.Rational(1,2)
P=S.zeros(N)
P0=S.zeros(N)
for i in range(N):
    P[i,pi[i]]=w[i]
    P0[i,pi[i]]=S.Rational(1,2)
assert (S.eye(N)-P).det()!=0 and (S.eye(N)-P0).det()!=0
assert sum(norm2(w[i]-w[tau[i]]) for i in range(N))==0
z=(1+S.sqrt(3)*I)/2
d=[S.Integer(1)]*N
for cyc in [(0,4,8),(2,6,10)]:
    for i,power in zip(cyc,range(3)): d[i]=S.expand(z**power)
assert all(norm2(x)==1 for x in d)
E=S.simplify(sum(norm2(w[i]-S.Rational(1,2)*d[i]/d[pi[i]]) for i in range(N)))
assert E==S.Rational(3,2)
L=S.Matrix([[2,-1,1],[-1,2,-1],[1,-1,2]])
assert L.eigenvals()=={S.Integer(1):2,S.Integer(4):1}

# Mixed-amplitude, loop, parallel, reversed, zero-weight and zero-constant controls.
phases=[S.Integer(1),I,S.Rational(3,5)+S.Rational(4,5)*I,-I]
edges=[
    (0,1,S.Rational(2),S.Rational(3,10)+S.Rational(4,10)*I,S.Rational(1,3)),
    (1,0,S.Rational(1,2),-S.Rational(1,2),S.Rational(1,2)),
    (0,1,S.Rational(1,2),S.Rational(1,2),S.Rational(1,2)),
    (1,2,S.Rational(3,2),S.Integer(0),S.Rational(2,5)),
    (2,3,S.Rational(4,3),I/4,S.Integer(0)),
    (3,3,S.Integer(2),-S.Rational(1,3),S.Rational(1,3)),
    (2,0,S.Integer(1),I/5,S.Rational(1,5)),
]
direct=S.Integer(0)
constant=S.Integer(0)
pairs={}
radial_checks=0
for u,v,beta,we,c in edges:
    r,R=mag(we),mag(c)
    direct+=beta*norm2(we-c*phases[u]/phases[v])
    radial=beta*(r-R)**2
    constant+=radial
    a=beta*r*R
    sigma=we*S.conjugate(c)/(r*R) if a else S.Integer(1)
    assert S.simplify(beta*norm2(we-c*phases[u]/phases[v])-radial-a*norm2(phases[u]-sigma*phases[v]))==0
    radial_checks+=1
    if not a: continue
    if u==v:
        constant+=a*norm2(1-sigma)
        continue
    if u>v:
        u,v=v,u
        sigma=S.conjugate(sigma)
    A,Z=pairs.get((u,v),(S.Integer(0),S.Integer(0)))
    pairs[(u,v)]=(A+a,Z+a*sigma)
reduced=constant
for (u,v),(A,Z) in pairs.items():
    b=mag(Z)
    reduced+=2*(A-b)
    if b: reduced+=b*norm2(phases[u]-(Z/b)*phases[v])
assert S.simplify(direct-reduced)==0

result={
    "scope":"Fresh exact controls for comparison algebra only; no replay of accepted scientific proof",
    "all_checks_passed":True,
    "n16_route_commutes_with_tau":True,
    "n16_actual_inverse_legal":True,
    "n16_reference_inverse_legal":True,
    "n16_raw_energy":"0",
    "triangle_magnetic_eigenvalues":[1,1,4],
    "n16_attained_unit_phase_energy":"3/2",
    "n16_graph_first_eigenvalue":"0 (isolated vertices)",
    "n16_graph_first_cheeger_constant":"0 (isolated vertex subset)",
    "mixed_amplitude_edge_checks":radial_checks,
    "simple_graph_aggregation_exact":True,
    "historical_programs_executed":0,
    "new_theorem_credit":0
}
(ROOT/'publish'/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
