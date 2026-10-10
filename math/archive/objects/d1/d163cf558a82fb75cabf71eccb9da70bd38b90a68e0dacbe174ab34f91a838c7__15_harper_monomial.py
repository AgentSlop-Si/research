"""Exact finite-field witnesses and graph-audit of the Harper monomial centralizer.
Uniform theorem proved over C in THEOREM.md. Tests are finite controls only.
"""
from itertools import permutations
from field_core import P,eye,add,cyclic_operators,matmul,inverse,dft,monomial,reflection


def allowed_symmetries(n):
    T,V=cyclic_operators(n)
    v=[V[i][i] for i in range(n)]
    ok=[]
    for p in permutations(range(n)):
        if any(v[p[i]]!=v[i] for i in range(n)):continue
        # Coordinate permutation must preserve nonzero offdiagonal pattern.
        if any(not T[p[i]][p[(i+1)%n]] for i in range(n)):continue
        ok.append(p)
    assert set(ok)=={tuple(range(n)),tuple((-i)%n for i in range(n))}
    return {'n':n,'v_preserving_cycle_automorphisms':len(ok),'only_identity_reflection':True}


def no_single_harper_sandwich(n):
    T,V=cyclic_operators(n);H=add(T,V);F=dft(n);J=reflection(n)
    assert matmul(H,F)==matmul(F,H)
    assert matmul(H,J)==matmul(J,H)
    A=add(H,[[(-7 if i==j else 0)%P for j in range(n)] for i in range(n)])
    B=add(H,[[(-11 if i==j else 0)%P for j in range(n)] for i in range(n)])
    # If F=(H-7I)^-1 C (H-11I)^-1, then C=(H-7I)F(H-11I).
    # C must be monomial for this candidate, but it has multiple nonzeros per row.
    inverse(A);inverse(B) # prove proposed rational stages are defined mod p
    C=matmul(A,matmul(F,B))
    nnz=[sum(v!=0 for v in row) for row in C]
    assert any(k!=1 for k in nnz)
    return {'n':n,'H_commutes_F':True,'H_commutes_J':True,
            'candidate_middle_row_nonzero_min':min(nnz),
            'candidate_middle_row_nonzero_max':max(nnz),'middle_monomial_impossible_for_pair':True}
