"""Phase 28: exact two-sided monomial equivalence and Green Fourier synthesis.

For fixed invertible A,B,C and N-point Fourier matrix F, test whether
F=A D1 P1 B P2 D2 C with two invertible diagonal masks and two permutations.
Work over F_998244353, N a power of 2, and perform dense inversion only as
an OFFLINE feasibility test, never as an alleged sub-NlogN executor.

Core invariant: for a nowhere-zero matrix M, h_s(i,j) =
  (sum_k (M_ik/M_jk)^s)*(sum_k (M_jk/M_ik)^s).
All row-pair h_s are invariant under arbitrary nonzero diagonal row/column
scalings and column permutation; a row permutation only relabels the pairs.
Use row/column graph vertex fingerprint to recover permutations when unique;
verify exact scales and ALL entries. Collisions yield INCONCLUSIVE.
"""
from __future__ import annotations
from collections import Counter
import os
from dataclasses import dataclass
from random import Random
from typing import Sequence

P=int(os.environ.get("PHASE28_PRIME", "998244353"))
PRIMITIVE=int(os.environ.get("PHASE28_GENERATOR", "3"))


def inverse(a:int)->int:
    return pow(a%P,-1,P)


def matmul(a:list[list[int]],b:list[list[int]])->list[list[int]]:
    n=len(a)
    assert len(b)==n and all(len(r)==n for r in a+b)
    bt=list(zip(*b))
    return [[sum(a[i][k]*bt[j][k] for k in range(n))%P for j in range(n)] for i in range(n)]


def invert(a:list[list[int]])->list[list[int]]:
    n=len(a)
    augmented=[[x%P for x in row]+[int(i==j) for j in range(n)]
               for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if augmented[i][j]),None)
        if pivot is None: raise ValueError('singular matrix')
        augmented[j],augmented[pivot]=augmented[pivot],augmented[j]
        invp=inverse(augmented[j][j])
        augmented[j]=[(x*invp)%P for x in augmented[j]]
        for i in range(n):
            if i==j:continue
            factor=augmented[i][j]
            if factor:
                augmented[i]=[(x-factor*y)%P for x,y in zip(augmented[i],augmented[j])]
    return [r[n:] for r in augmented]


def fft_matrix(n:int)->list[list[int]]:
    if n<2 or n&(n-1) or (P-1)%n:raise ValueError('unsupported n')
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    wt=[pow(omega,k,P) for k in range(n)]
    return [[wt[i*j%n] for j in range(n)] for i in range(n)]


def permuted_scaled(matrix:list[list[int]], rows:list[int],cols:list[int],
                    left:list[int],right:list[int])->list[list[int]]:
    n=len(matrix)
    if (sorted(rows)!=list(range(n)) or sorted(cols)!=list(range(n)) or
            len(left)!=n or len(right)!=n):raise ValueError('invalid permutation/scalings')
    return [[left[i]*matrix[rows[i]][cols[j]]*right[j]%P for j in range(n)] for i in range(n)]


def transpose(a:list[list[int]])->list[list[int]]:
    return [list(col) for col in zip(*a)]


def row_pair_moments(matrix:list[list[int]], powers=(1,2)) -> list[list[tuple[int,...]]]:
    """O(len(powers)*N^3) field operations + O(N^2) batched modular inverses.

    Every matrix entry must be nonzero. Compute distinct unordered row pairs.
    """
    n=len(matrix)
    if any(x%P==0 for row in matrix for x in row):
        raise ValueError('zero entry: support-aware fallback required')
    # One inverse of each entry; offline cost O(N^2 log P). Can batch instead.
    vals=[x%P for row in matrix for x in row]
    pref=[1]*(n*n+1)
    for i,x in enumerate(vals): pref[i+1]=pref[i]*x%P
    invtotal=inverse(pref[-1]);invvals=[0]*(n*n)
    for i in range(n*n-1,-1,-1):
        invvals[i]=invtotal*pref[i]%P
        invtotal=invtotal*vals[i]%P
    invmat=[invvals[i*n:(i+1)*n] for i in range(n)]
    h=[[() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            # ratio_k = M_ik/M_jk
            v=[matrix[i][k]*invmat[j][k]%P for k in range(n)]
            u=[matrix[j][k]*invmat[i][k]%P for k in range(n)]
            key=[]
            for s in powers:
                key.append(sum(pow(a,s,P) for a in v)%P *
                           (sum(pow(a,s,P) for a in u)%P)%P)
            h[i][j]=h[j][i]=tuple(key)
    return h


def vertex_fingerprints(h:list[list[tuple[int,...]]])->list[tuple]:
    n=len(h)
    return [tuple(sorted(h[i][j] for j in range(n) if j!=i)) for i in range(n)]


def rowpair_multiset(h:list[list[tuple[int,...]]])->Counter:
    n=len(h)
    return Counter(h[i][j] for i in range(n) for j in range(i+1,n))


@dataclass
class Report:
    status:str
    reason:str
    row_perm:list[int]|None=None
    col_perm:list[int]|None=None
    left:list[int]|None=None
    right:list[int]|None=None


def equivalence_test(target:list[list[int]],middle:list[list[int]],powers=(1,2))->Report:
    """Test target = DL P_L middle P_R DR. `excluded` is rigorous in F_p.

    `recovered` includes full exact matrix verification. `inconclusive` means
    collision of necessary signatures prevented exhaustive permutation recovery.
    """
    n=len(target)
    if n!=len(middle) or any(len(r)!=n for r in target+middle):
        raise ValueError('matrix shapes')
    tzero=sum(x==0 for row in target for x in row)
    bzero=sum(x==0 for row in middle for x in row)
    if tzero!=bzero:
        return Report('excluded','zero-entry count mismatch (monomial invariant)')
    if tzero:
        return Report('inconclusive','matching zero counts; need support graph matching')
    ht=row_pair_moments(target,powers)
    hb=row_pair_moments(middle,powers)
    if rowpair_multiset(ht)!=rowpair_multiset(hb):
        return Report('excluded','row-pair projective moment multiset mismatch')
    htc=row_pair_moments(transpose(target),powers)
    hbc=row_pair_moments(transpose(middle),powers)
    if rowpair_multiset(htc)!=rowpair_multiset(hbc):
        return Report('excluded','column-pair projective moment multiset mismatch')

    fr_t=vertex_fingerprints(ht); fr_b=vertex_fingerprints(hb)
    fc_t=vertex_fingerprints(htc);fc_b=vertex_fingerprints(hbc)
    if Counter(fr_t)!=Counter(fr_b) or Counter(fc_t)!=Counter(fc_b):
        return Report('excluded','row/column vertex fingerprints mismatch')
    if len(set(fr_t))!=n or len(set(fc_t))!=n:
        return Report('inconclusive','repeated fingerprints: permutation matching not unique')
    row_by_sig={s:i for i,s in enumerate(fr_b)}
    col_by_sig={s:j for j,s in enumerate(fc_b)}
    rp=[row_by_sig[s] for s in fr_t]
    cp=[col_by_sig[s] for s in fc_t]
    mid=[[middle[rp[i]][cp[j]] for j in range(n)] for i in range(n)]
    left=[target[i][0]*inverse(mid[i][0])%P for i in range(n)]
    right=[target[0][j]*inverse(mid[0][j])%P*inverse(left[0])%P for j in range(n)]
    for i in range(n):
        for j in range(n):
            if target[i][j]%P !=left[i]*mid[i][j]*right[j]%P:
                return Report('excluded','unique signature matching fails exact scalar reconstruction')
    return Report('recovered','complete monomial-equivalence certificate verified',rp,cp,left,right)


def random_cycle(n:int,rng:Random)->list[int]:
    order=list(range(n));rng.shuffle(order)
    successor=[0]*n
    for k in range(n): successor[order[k]]=order[(k+1)%n]
    return successor


def green_matrix(succ:list[int],alpha:int)->list[list[int]]:
    n=len(succ)
    d=inverse(1-pow(alpha,n,P))
    out=[[0]*n for _ in range(n)]
    for col in range(n):
        j=col;val=d
        for _ in range(n):
            out[j][col]=val
            j=succ[j];val=val*alpha%P
    return out


def green_sum(n:int,seed:int, complex_gauges:bool=True)->list[list[int]]:
    rng=Random(seed)
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[pow(omega,j,P) for j in range(n)]
    ans=[[0]*n for _ in range(n)]
    for t,alpha in enumerate((inverse(4),inverse(5))):
        mat=green_matrix(random_cycle(n,rng),alpha)
        left=[roots[rng.randrange(n)] if complex_gauges else 1 for _ in range(n)]
        right=[roots[rng.randrange(n)] if complex_gauges else 1 for _ in range(n)]
        coeff=1 if t==0 else 3*inverse(2)%P
        for i in range(n):
            for j in range(n):
                ans[i][j]=(ans[i][j]+coeff*left[i]*mat[i][j]*right[j])%P
    return ans


def green_triple_fourier_test(n:int,seed:int,powers=(1,2)) -> Report:
    a=green_sum(n,seed*3+1)
    b=green_sum(n,seed*3+2)
    c=green_sum(n,seed*3+3)
    target=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
    return equivalence_test(target,b,powers=powers)

if __name__=='__main__':
    for n in (8,16,32,64):
        r=green_triple_fourier_test(n,2800+n)
        print(n,r.status,r.reason)


def ratio_correlation(matrix:list[list[int]])->list[list[int]]:
    """C(M)=M (M^{Hadamard -1})^T, over F_p; requires all entries != 0.

    Under M -> D_left P_left M P_right D_right,
    C -> D_left P_left C P_left^-1 D_left^-1 (similarity).
    """
    n=len(matrix)
    if any(len(r)!=n for r in matrix):raise ValueError('matrix must be square')
    if any(not x for row in matrix for x in row):
        raise ValueError('type-II/projective gate requires nonzero entries')
    inv=[[inverse(x) for x in row] for row in matrix]
    return matmul(matrix,transpose(inv))


def ratio_trace_invariants(matrix:list[list[int]])->dict[str,int]:
    """Return trace(C^2), trace(C^3), and type-II defect rank-free bit.

    Trace(C)=N^2 always and does not discriminate. The higher moments do.
    """
    n=len(matrix)
    c=ratio_correlation(matrix)
    square=matmul(c,c)
    cube=matmul(square,c)
    return {'trace2':sum(square[i][i] for i in range(n))%P,
            'trace3':sum(cube[i][i] for i in range(n))%P,
            'type_II':int(all(c[i][j]==(n if i==j else 0) for i in range(n) for j in range(n)))}


def trace2_from_row_moments(matrix:list[list[int]])->int:
    n=len(matrix)
    pair=row_pair_moments(matrix,powers=(1,))
    total=sum(pair[i][j][0] for i in range(n) for j in range(i+1,n))%P
    return (n**3+2*total)%P


def green_triple_trace_certificate(n:int,seed:int)->dict:
    """A single scalar certificate that excludes ALL D1,P1,P2,D2 for fixed A,B,C.

    Supports a Zariski-open generic theorem as the 2nd Green-term scalar
    couplings of A, B and C vary, with paths/individual gauges held fixed.
    """
    a=green_sum(n,seed*3+1)
    b=green_sum(n,seed*3+2)
    c=green_sum(n,seed*3+3)
    target=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
    x=trace2_from_row_moments(target)
    y=trace2_from_row_moments(b)
    return {'N':n,'seed':seed,'p':P,'trace2_target':x,'trace2_middle':y,
            'nonzero_difference':(x-y)%P,
            'excludes_all_internal_diagonal_masks_and_permutations':x!=y}


def green_components(n:int,seed:int)->tuple[list[list[int]],list[list[int]]]:
    """Same two random cycles and phase gauges as green_sum, sans 2nd weight.

    B(z)=B0+z*B1. At z=3/2, this equals green_sum(n,seed).
    """
    rng=Random(seed)
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[pow(omega,j,P) for j in range(n)]
    result=[]
    for alpha in (inverse(4),inverse(5)):
        g=green_matrix(random_cycle(n,rng),alpha)
        left=[roots[rng.randrange(n)] for _ in range(n)]
        right=[roots[rng.randrange(n)] for _ in range(n)]
        result.append([[left[i]*g[i][j]*right[j]%P for j in range(n)] for i in range(n)])
    return result[0],result[1]
