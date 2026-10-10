# Haar–Green stages also require logarithmically many stages

Independent synthesis and proof, 9 October 2026.

## Main result

Let N=2m be a power of two. Let H_m be orthonormal binary Haar synthesis. A
Haar–Green stage is S=V_H C_a(A_1) C_b(A_2), where A_1,A_2 are real symmetric
tridiagonal matrices in possibly different coordinate orders, a,b are real,

    C_a(A)=(I+i a A)(I-i a A)^(-1),
    R_H=[[0,H_m],[H_m*,0]],
    V_H=(I+i e R_H)/sqrt(1+e^2),  e real.

The strengths a,b,e, path weights and coordinate orders may vary between
stages and with N. A word of t such stages or inverse stages, interleaved
with arbitrary unitary monomial matrices, cannot equal normalized Fourier
unless

    t >= N log_2(N)/(11N-12).                         (1)

The same conclusion holds for any flat unitary matrix and for endpoint
unitary monomials. This proves t=Omega(log N), including the uploaded strong
Haar family. No bounded-strength or bounded-degree estimate is used.

The result is a restriction on this factorization family, not a lower bound
for arbitrary Fourier arithmetic algorithms. If stages are separately
executed at Theta(N) work, it gives Omega(N log N) work for that execution.
It does not exclude algebraically compiling or fusing a whole word into
another arithmetic circuit with fewer operations, nor nonunit diagonal
scalings or different nonlocal primitives.

## 1. A tridiagonal Cayley has a linear-size unitary-gate factorization

Put T=I-i a A. Hermitian A implies T is normal and invertible:

    T*T = TT* = I+a^2 A^2.

Take QR factorizations with positive real diagonal in R:

    T=Q_- R_-,   T*=Q_+ R_+.

Then R_-*R_-=T*T=TT*=R_+*R_+. Uniqueness of the upper-triangular Cholesky
factor gives R_-=R_+=R. Therefore

    C_a(A)=T*T^(-1)=Q_+ Q_-*.                         (2)

Both T and T* are tridiagonal, hence upper Hessenberg. Left multiplication
by N-1 adjacent 2-by-2 unitary Givens rotations eliminates their subdiagonal
entries. A zero subdiagonal needs no gate. Subsequent diagonal phases make
the R diagonal positive and contribute no matrix entropy.

Thus each Q factor is a product of at most N-1 two-coordinate unitaries
and a unitary diagonal. Equation (2) realizes the entire Cayley in at most
2(N-1) two-coordinate gates. This is an exact algebraic factorization,
regardless of whether the supplied implementation uses a tridiagonal solve.
For a path in another coordinate order, conjugating by its permutation
only relabels the gates; permutations contribute zero entropy.

For context, this QR argument applies to any Hermitian tridiagonal A,
including nonconstant real path weights and arbitrary diagonal entries.
The real-strength condition is essential to this argument.

The comparison model allows arbitrary predetermined complex unitary-gate
coefficients. QR/Givens normalization can introduce square roots outside the
original input coefficient field. Only existence of this gate representation
is needed for the stage-count contradiction; this is not a claim of a
same-coefficient-field executor or free scalar-constant preparation.

## 2. The Haar involution rotation has a linear-size gate factorization

Write c=1/sqrt(1+e^2), s=e/sqrt(1+e^2). Direct block multiplication gives

    V_H = diag(H_m,I_m) [[cI_m,isI_m],[isI_m,cI_m]] diag(H_m*,I_m).  (3)

The middle factor is m independent two-coordinate rotations. Binary Haar
synthesis and analysis each use m-1 normalized sum/difference butterflies,
with coordinate permutations if needed. There is one butterfly per internal
vertex of the complete binary tree, not m log m butterflies.

Consequently V_H uses at most 3m-2 two-coordinate unitaries. Together with
two path Cayleys, each S or S^-1 uses at most

    g_N = 4(N-1)+3N/2-2 = 11N/2-6                    (4)

such gates. Scalar normalizations in (3) are part of the 2-by-2 unitary
gates; no growing or ignored nonunitary scale is present.

## 3. Self-contained entropy bound

For a unitary matrix U define

    Phi(U) = -sum_(i,j) |U_ij|^2 log_2(|U_ij|^2),

with 0 log 0=0. Identity has entropy zero; any flat N-by-N unitary has
entropy N log_2 N. Row permutations and unit-modulus row scalings preserve
Phi exactly.

Suppose a unitary gate mixes rows r,s. For column j let
p_j=|U_rj|^2+|U_sj|^2. The gate preserves p_j. Given p_j, the entropy of
these two entries is between -p_j log_2 p_j and
-p_j log_2 p_j+p_j. Thus its change has absolute value at most p_j.
Summing over j, row normalization gives sum_j p_j=2. Each gate changes
Phi by at most two bits. Therefore any exact product with G such gates and
arbitrary unitary monomials producing a flat unitary requires

    G >= N log_2 N/2.                                (5)

Combining G<=t g_N with (4)-(5) proves (1). Inverse stages have the same
gate count by reversing the gates. Strengths and permutations may be fully
N-dependent, since the decomposition count does not depend on their values.

## 4. What this changes in the uploaded phase-13 checkpoint

The new fixed-p norm theorem is sound, and the Haar construction really
escapes its norm budget. However, the checkpoint explicitly leaves open
whether its tridiagonal-solve execution can be replaced by O(N) unitary
2-register gates. Equations (2)-(4) establish precisely that representation.
The Haar replacement therefore does not escape logarithmic stage count.

This obstruction is compatible with the stage's robust cut ranks and
growing fixed-p norms: neither measures total Fourier entropy. It is also
compatible with the exact covariance and finite two-stage vetoes, but is an
all-N statement independent of those finite tests.

## Precedence and evidence

The matrix-entropy lower bound is established prior work: Nir Ailon,
[A Lower Bound for Fourier Transform Computation in a Linear Model Over
2x2 Unitary Gates Using Matrix Entropy](https://arxiv.org/abs/1305.4745), 2013.
It is reproduced above to make the application self-contained. No priority
claim is made for QR, Haar, entropy, or their combination.

Source audited: fft_green_phase13_phase_coherence/THEOREM.md, sections 1–3
and the strong-coupling control, in the user-supplied phase-13 archive.
Independent numerical identity checks and exact modular certificate checks
are supplied separately. Numerical tests support implementation consistency;
the all-N conclusion follows from the proof above.

Verification artifacts: independent_phase13_checks.py and
independent_phase13_results.json. The independently authored checker imported
no uploaded executable. It passed 20 normalized QR/Haar reconstruction cases
at N=4,8,16,32,64 with strengths 1/32,1/2,2,100; independently reproduced all
10 full-rank one-stage covariance defects through N=128; and matched all 30
uploaded two-stage diagonal-multiset mismatch certificates exactly.
