#!/usr/bin/env python3
"""Independent literal-matrix control. No research implementation is imported.
Only Python stdlib, exact Fraction arithmetic, and JSON mathematical inputs.
"""
from fractions import Fraction as Fr
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'WITNESS.json'

# The canonical representative modulo 1+X+X^2+X^3+X^4.
def elt(v=0):
    if isinstance(v, tuple):
        return v
    if isinstance(v, (list,)):
        assert len(v) == 4
        return tuple(Fr(x) for x in v)
    return (Fr(v), Fr(0), Fr(0), Fr(0))
Z, O, Q = elt(0), elt(1), elt([0,1,0,0])
def plus(x,y): return tuple(a+b for a,b in zip(x,y))
def neg(x): return tuple(-a for a in x)
def minus(x,y): return plus(x,neg(y))
def times(x,y):
    if x == Z or y == Z: return Z
    a = [Fr(0)]*7
    for i in range(4):
        for j in range(4): a[i+j] += x[i]*y[j]
    for d in (6,5,4):
        c = a[d]
        for k in range(4): a[d-4+k] -= c
    return tuple(a[:4])

@lru_cache(maxsize=None)
def reciprocal(x):
    assert x != Z, 'Division by zero'
    # Matrix of multiplication by x over Q, solved by rational Gaussian elimination.
    columns = [times(x, elt([int(i==j) for i in range(4)])) for j in range(4)]
    a = [[columns[j][i] for j in range(4)] + [Fr(int(i==0))] for i in range(4)]
    for k in range(4):
        pivot = next(i for i in range(k,4) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        c = a[k][k]
        a[k] = [v/c for v in a[k]]
        for i in range(4):
            if i != k:
                c = a[i][k]
                a[i] = [v-c*w for v,w in zip(a[i],a[k])]
    result = tuple(a[i][4] for i in range(4))
    assert times(x,result) == O
    return result

def power(x,n):
    if n < 0: return power(reciprocal(x),-n)
    ans = O
    while n:
        if n & 1: ans = times(ans,x)
        x = times(x,x)
        n //= 2
    return ans

def total(xs):
    ans = Z
    for x in xs: ans = plus(ans,x)
    return ans

def sigma(x,k): return total(times(elt(x[i]),power(Q,k*i)) for i in range(4))
def flat(x): return [str(c) for c in x]

def identity(n): return [[O if i==j else Z for j in range(n)] for i in range(n)]
def zeros(n): return [[Z for j in range(n)] for i in range(n)]
def mm(A,B):
    n=len(A)
    return [[total(times(A[i][k],B[k][j]) for k in range(n)) for j in range(n)] for i in range(n)]
def ma(A,B): return [[plus(a,b) for a,b in zip(x,y)] for x,y in zip(A,B)]
def ms(c,A): return [[times(c,a) for a in row] for row in A]
def mpow(A,k):
    R = identity(len(A))
    for _ in range(k): R = mm(R,A)
    return R

def inverse_and_det(M):
    n=len(M)
    A = [row[:] + eye for row,eye in zip(M,identity(n))]
    determinant = O
    for k in range(n):
        candidates = [i for i in range(k,n) if A[i][k] != Z]
        assert candidates, 'Literal branch is singular'
        pivot = candidates[0]
        if pivot != k:
            A[k], A[pivot] = A[pivot], A[k]
            determinant = neg(determinant)
        p = A[k][k]
        determinant = times(determinant,p)
        A[k] = [times(v,reciprocal(p)) for v in A[k]]
        for i in range(n):
            if i != k:
                c = A[i][k]
                if c != Z:
                    A[i] = [minus(v,times(c,w)) for v,w in zip(A[i],A[k])]
    R = [row[n:] for row in A]
    assert mm(M,R) == identity(n), 'Right inverse failure'
    assert mm(R,M) == identity(n), 'Left inverse failure'
    return R, determinant

checks = []
def check(name,condition):
    assert condition, name
    checks.append(name)

def main():
    data_bytes = SOURCE.read_bytes()
    data = json.loads(data_bytes)
    check('exactly_five_banks',len(data['banks']) == 5)
    check('cyclotomic_relation',total(power(Q,k) for k in range(5)) == Z)
    check('fifth_root_order',power(Q,5)==O and all(power(Q,k)!=O for k in range(1,5)))
    check('shifted_Phi5_Eisenstein_coefficients', [1,5,10,10,5][-1]%25 != 0 and all(c%5==0 for c in [5,10,10,5]))
    expected_alphas=[O,elt([-2,-3,-3,-1]),Q,elt([1,1,0,0]),elt([1,1,0,0])]
    expected_signs=[(1,1),(1,1),(-1,1),(1,-1),(-1,-1)]
    for i,b in enumerate(data['banks']):
        check(f'bank{i+1}_parameters',elt(b['alpha'])==expected_alphas[i] and elt(b['beta'])==O and (b['epsilon'],b['delta_sign'])==expected_signs[i])
        check(f'bank{i+1}_five_sectors_and_weights',len(b['normalized_h'])==5 and len(b['raw_weights'])==5)
    denominator_primes=set()
    denominators=set()
    for b in data['banks']:
        for v in [b['alpha'],b['beta'],b['Delta']]+b['normalized_h']+b['raw_weights']:
            for c in v: denominators.add(Fr(c).denominator)
    for d in denominators:
        m=d
        p=2
        while p*p<=m:
            if m%p==0:
                denominator_primes.add(p)
                while m%p==0:m//=p
            p+=1
        if m>1: denominator_primes.add(m)
    all_embeddings=[]
    I=identity(5)
    for conjugate in (1,2,3,4):
        q=power(Q,conjugate)
        C=times(elt(Fr(1,5)),total(power(q,-j*j) for j in range(5)))
        Gp=total(power(q,j*j) for j in range(5))
        check(f'conjugate{conjugate}_C_exact',C==sigma(elt(['-1/5',0,'-2/5','-2/5']),conjugate))
        check(f'conjugate{conjugate}_C_nonzero',C!=Z)
        check(f'conjugate{conjugate}_Gauss_product',times(times(C,elt(5)),Gp)==elt(5))
        F=[[power(q,-r*c) for c in range(5)] for r in range(5)]
        S=[[O if r==(c+1)%5 else Z for c in range(5)] for r in range(5)]
        T=[[power(q,c) if r==c else Z for c in range(5)] for r in range(5)]
        check(f'conjugate{conjugate}_clock_shift',mm(T,S)==ms(q,mm(S,T)))
        # Check Fourier C normalization directly by Weyl coefficient extraction.
        for a in range(5):
            for b in range(5):
                coefficient=times(elt(Fr(1,5)),total(times(power(q,-b*j),F[(j+a)%5][j]) for j in range(5)))
                check(f'conjugate{conjugate}_Fourier_Weyl_{a}_{b}',coefficient==times(C,power(q,4*(a+b)**2)))
        full=zeros(5)
        bank_reports=[]
        for index,bank in enumerate(data['banks']):
            eps,ds=bank['epsilon'],bank['delta_sign']
            alpha,beta,Delta=[sigma(elt(bank[k]),conjugate) for k in ('alpha','beta','Delta')]
            h=[sigma(elt(v),conjugate) for v in bank['normalized_h']]
            weights=[sigma(elt(v),conjugate) for v in bank['raw_weights']]
            check(f'c{conjugate}_b{index+1}_alpha_beta_nonzero',alpha!=Z and beta!=Z)
            check(f'c{conjugate}_b{index+1}_Delta_formula',Delta==minus(minus(O,power(alpha,5)),power(beta,5)))
            check(f'c{conjugate}_b{index+1}_Delta_nonzero',Delta!=Z)
            check(f'c{conjugate}_b{index+1}_raw_weights_nontrivial',any(w!=Z for w in weights))
            Se=mpow(S,eps%5)
            Td=mpow(T,ds%5)
            contribution=zeros(5)
            straight_phase_contribution=zeros(5)
            branch_determinants=[]
            for j in range(5):
                reconstructed=times(times(C,Delta),total(times(h[l],power(q,-eps*ds*j*l)) for l in range(5)))
                check(f'c{conjugate}_b{index+1}_weight{j}_normalization',weights[j]==reconstructed)
                coeff=times(elt(Fr(1,5)),total(times(weights[k],power(q,eps*ds*k*j)) for k in range(5)))
                # beta is 1 for this witness; include beta^ell for explicit convention.
                recovered_h=times(times(coeff,power(beta,j)),reciprocal(Delta))
                check(f'c{conjugate}_b{index+1}_h{j}_roundtrip',recovered_h==times(C,h[j]))
                M=ma(ms(alpha,Se),ms(times(beta,power(q,eps*ds*j)),Td))
                Qj=ma(I,ms(elt(-1),M))
                inverse,determinant=inverse_and_det(Qj)
                check(f'c{conjugate}_b{index+1}_branch{j}_determinant',determinant==Delta)
                # Also independent power identity (not used to obtain the inverse).
                check(f'c{conjugate}_b{index+1}_branch{j}_fifth_power',mpow(M,5)==ms(plus(power(alpha,5),power(beta,5)),I))
                contribution=ma(contribution,ms(times(elt(Fr(1,5)),weights[j]),inverse))
                branch_determinants.append(flat(determinant))
            # q^j phase instead of q^(eps*ds*j): exact reindexing of raw weights.
            for j in range(5):
                M=ma(ms(alpha,Se),ms(times(beta,power(q,j)),Td))
                inverse,_=inverse_and_det(ma(I,ms(elt(-1),M)))
                w=weights[(eps*ds*j)%5]
                straight_phase_contribution=ma(straight_phase_contribution,ms(times(elt(Fr(1,5)),w),inverse))
            check(f'c{conjugate}_b{index+1}_q_to_signed_phase_reindex',straight_phase_contribution==contribution)
            full=ma(full,contribution)
            bank_reports.append({'bank':index+1,'alpha':flat(alpha),'Delta':flat(Delta),'all_five_branch_determinants_equal_Delta':True,'two_sided_literal_inverses':True,'weight_character_roundtrip':True,'q_j_phase_reindex':True})
        for r in range(5):
            for c in range(5):
                check(f'c{conjugate}_literal_F_entry_{r}_{c}',full[r][c]==F[r][c])
        all_embeddings.append({'q_image_exponent':conjugate,'C':flat(C),'banks':bank_reports,'exact_residual_matrix':[[flat(minus(full[r][c],F[r][c])) for c in range(5)] for r in range(5)]})
    # Check the support gate needed to turn the accepted four-bank theorem into >=5.
    orientations=[(1,1),(1,-1),(-1,1),(-1,-1)]
    supports={s:{(a,b) for a in range(5) for b in range(5) if (s[0]*a)%5+(s[1]*b)%5<=4} for s in orientations}
    for missing in orientations:
        other=[s for s in orientations if s!=missing]
        covered=set().union(*(supports[s] for s in other))
        check(f'three_orientation_support_gap_{missing}',len(covered)<25)
        for t in (1,2):
            exclusive=((missing[0]*t)%5,(missing[1]*t)%5)
            check(f'exclusive_point_{missing}_{t}',exclusive in supports[missing] and exclusive not in covered)
    report={'verdict':'PASS','arithmetic':'Exact Python Fraction arithmetic in Q[X]/Phi_5(X); independent literal Gaussian matrix inversion','witness_sha256':sha256(data_bytes).hexdigest(),'control_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'all_checks':len(checks),'all_passed':True,'checked_embeddings':[1,2,3,4],'literal_signed_branches_checked':100,'additional_q_j_reindexed_branches_checked':100,'fourier_entries_checked':100,'rational_denominator_primes':sorted(denominator_primes),'embeddings':all_embeddings,'sufficiency_verdict':'Five legal banks realize the negative N=5 Fourier matrix in characteristic zero. Exactly five follows on combining with the separately accepted four-bank exclusion and the support gate checked here.','limits':['No author or prior research code executed/imported/compiled.','No positive-characteristic classification.','No runtime/FFT improvement claim.','No historical novelty claim.'],'check_names':checks}
    (HERE/'verification_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('embeddings','check_names','lower_bound_verified_hashes')},indent=2),flush=True)

if __name__=='__main__': main()
