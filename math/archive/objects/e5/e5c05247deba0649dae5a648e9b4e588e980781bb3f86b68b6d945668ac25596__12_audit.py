"""Reproducible deterministic Phase 19 exact and numerical controls."""
import json,random
from field_core import P,eye,dft,matmul,inverse,monomial,cyclic_operators,add,defect_count,reflection
from joint_gate import gate,audit_outer,vertex_signatures
from harper_monomial import no_single_harper_sandwich,allowed_symmetries
from stable_green import example
from spectral_green import complex_nonnormal_control,complex_nonnormal_nondominant_control
from green_product_audit import reject_fixed_green_product
from near_resonance import audit as resonant_control


def random_invertible(n,rng):
    # invertible by construction: upper triangular, nonzero diagonal.
    A=[[0]*n for _ in range(n)]
    for i in range(n):
        A[i][i]=rng.randrange(1,P)
        for j in range(i+1,n):A[i][j]=rng.randrange(1,P)
    return A


def positive(n):
    rng=random.Random(191900+n);F=dft(n)
    A=random_invertible(n,rng)
    perm=list(range(n));rng.shuffle(perm)
    q=[rng.randrange(1,P) for _ in range(n)]
    C=monomial(q,perm)
    # Solve A C B=F for B to create a genuine nontrivial middle-gauge control.
    B=matmul(inverse(C),matmul(inverse(A),F))
    out=audit_outer(A,B)
    assert out['status']=='possible',out
    assert out['perm']==perm
    found=monomial(out['q'],out['perm'])
    M=matmul(A,matmul(found,B))
    assert defect_count(M)==(0,0)
    # A solution is only recovered up to common scalar, calibrated by column 1.
    i=next((j for j in range(n) if M[j][1]),None)
    alpha=F[i][1]*pow(M[i][1],-1,P)%P
    M=[[alpha*x%P for x in row] for row in M]
    assert M==F
    return {'n':n,'permutation_recovered_exactly':True,'same_mask_solves_both_dualities':True,
            'scalar_calibration_recovers_all_Fourier_entries':True,
            'number_of_candidate_permutations':out['candidate_permutations']}


def one_equation_trap(n):
    F=dft(n);T,V=cyclic_operators(n)
    B=add(eye(n),[[2*T[i][j]%P for j in range(n)] for i in range(n)])
    inverse(B)  # ensure invertible
    M=matmul(F,B)
    assert defect_count(M)[0]==0
    assert defect_count(M)[1]>0
    # Independently: any C that makes F*C*B=F must equal B^-1; B^-1 is NOT monomial.
    out=audit_outer(F,B)
    assert out['status']=='impossible',out
    return {'n':n,'first_duality_defect':0,
            'second_duality_defect':defect_count(M)[1],
            'joint_gate_excludes_every_monomial':True,'reason':out['reason']}


def dual_ambiguity(n):
    F=dft(n);J=reflection(n)
    C=add([[3*e%P for e in row] for row in eye(n)],[[5*e%P for e in row] for row in J])
    M=matmul(F,C)
    assert defect_count(M)==(0,0)
    assert M!=F
    assert [M[i][1] for i in range(n)]!=[F[i][1] for i in range(n)]
    return {'n':n,'both_duality_defects_zero':True,'column_one_calibration_rejects':True}


def full_audit():
    return {'field_prime':P,
            'positive_joint_monomial_controls':[positive(n) for n in (8,16,32)],
            'one_equation_false_positive_controls':[one_equation_trap(n) for n in (8,16,32)],
            'dual_commutant_controls':[dual_ambiguity(n) for n in (8,16,32)],
            'fixed_green_product_joint_gate':[reject_fixed_green_product(n,seed) for n in (8,16,32,64) for seed in (0,1,2)],
            'harper_cycle_symmetries':[allowed_symmetries(n) for n in (4,8)],
            'harper_middle_monomial_obstructions':[no_single_harper_sandwich(n) for n in (8,16,32)],
            'near_resonant_green_norm_escapes':[resonant_control(n) for n in (8,16,32,64,128,256)],
            'stable_noncommuting_green_products':[example(n) for n in (16,32,64)],
            'spectrally_conditioned_non_DD_green':[complex_nonnormal_control(n) for n in (8,16,32,64,128,256)],
            'spectrally_conditioned_nonnormal_non_DD_green':[complex_nonnormal_nondominant_control(n) for n in (8,16,32,64,128,256)]}

if __name__=='__main__':
    print(json.dumps(full_audit(),indent=2))
