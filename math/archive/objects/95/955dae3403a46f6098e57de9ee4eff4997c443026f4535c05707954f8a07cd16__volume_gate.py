"""Mathematical guardrails for complex-valued high-arity FFT circuits.

The actual Fourier circuit implementation in Phase 26 is over a prime field.
This module is a separate complex-number model used to audit the consequences
of bounded coefficients and unitary no-extra-workspace gates. It implements
known determinant/entropy ideas; it does NOT prove an unrestricted lower bound.
"""
import math
import cmath


def entropy(matrix):
    """For a complex unitary row circuit: sum -|Aij|^2 log2 |Aij|^2."""
    total=0.0
    for row in matrix:
        for z in row:
            p=abs(z)**2
            if p>1e-25:total -= p*math.log2(p)
    return total


def block_fourier_layer(n,b):
    """Apply a direct sum of normalized b-DFT gates to the n x n identity."""
    if n % b:raise ValueError('b must divide n')
    matrix=[[0j]*n for _ in range(n)]
    scale=1/math.sqrt(b)
    for start in range(0,n,b):
        for r in range(b):
            for c in range(b):
                matrix[start+r][start+c]=scale*cmath.exp(2j*math.pi*r*c/b)
    return matrix


def block_volume_toll(n,b,c_bound=1.0):
    """One complex invertible b x b gate with entries <=C in modulus:
    log(|det gate|) <= b log C + b/2 log b by Hadamard.
    This is the maximum allowed potential increase of this b-gate, not a
    scalar implementation cost and not a finite-field statement.
    """
    if b<1 or c_bound<=0:raise ValueError
    return b * (math.log(c_bound)+0.5*math.log(b))


def Fourier_target_volume(n):
    return n/2 * math.log(n)


def Fourier_target_entropy(n):
    return n * math.log2(n)


def gt3_gate_tolls(G):
    if G<2 or G&(G-1):raise ValueError('G dyadic >= 2')
    t=G.bit_length()-1; N=3*G
    two_gates=3*(G//2)*t
    three_gates=G
    volume_two=two_gates*block_volume_toll(N,2)
    volume_three=three_gates*block_volume_toll(N,3)
    entropy_two=two_gates*2
    entropy_three=three_gates*3*math.log2(3)
    return {'N':N,'two_gates':two_gates,'three_gates':three_gates,
        'volume_gate_capacity':volume_two+volume_three,
        'volume_dft_required':Fourier_target_volume(N),
        'entropy_gate_capacity':entropy_two+entropy_three,
        'entropy_dft_required':Fourier_target_entropy(N)}


def volume_lower_bound_fixed_arity(n,B,C):
    """If gates are at most B-ary, each entry has modulus <=C,
    |det(G)| <= (C sqrt(B))^B. The cap below is an upper bound on
    per-gate potential for gates with b<=B for C>=1.
    Thus it gives a lower bound on the number of gates in this restricted
    in-place model (not a lower bound on arbitrary scalar circuits).
    """
    if B<2 or C<1: raise ValueError('B>=2,C>=1')
    per_gate=block_volume_toll(n,B,C)
    return Fourier_target_volume(n)/per_gate


def shear_identity_residue(p=2013265921):
    H=[[1,1],[1,p-1]]
    L=[[1,0],[1,1]]
    D=[[1,0],[0,p-2]]
    U=[[1,1],[0,1]]
    def matmul(a,b):
        return [[sum(a[i][k]*b[k][j] for k in range(2))%p
            for j in range(2)] for i in range(2)]
    assert matmul(matmul(L,D),U)==H
    return H


def required_max_entry_for_gate_budget(n, gate_budget, max_arity):
    """Necessary coefficient-height bound for an unnormalized Fourier matrix.

    In any complex in-place factorization into <=gate_budget invertible gates,
    each supported on <=max_arity coordinates, some coefficient has modulus
    at least exp(log(n)*n/(2*budget*B))/sqrt(B). This is a deliberately
    conservative consequence of Hadamard's bound for B>=2 and C>=1.
    The actual necessary max coefficient is max(1, that value).
    """
    if n<2 or gate_budget<=0 or max_arity<2:raise ValueError
    return max(1.0,math.exp(n*math.log(n)/(2*gate_budget*max_arity)) / math.sqrt(max_arity))
