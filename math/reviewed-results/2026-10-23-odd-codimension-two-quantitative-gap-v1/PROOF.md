# Uniform relative separation at odd inverse codimension two

Date: 2026-10-23 UTC. Separate strengthening candidate, pending independent review. Owner M-SPARSE-DEFECT remains TO RESEARCH. No exact optimum, optimal lower-bound constant, historical novelty, full-budget classification, or Fourier/FFT improvement is claimed.

## 1. Result in the original unrestricted matrix model

Let F[j,k]=N^(-1/2) exp(-2 pi i jk/N), and let Delta(N,s) be the infimum of ||M-F||_2 over invertible complex N-by-N matrices M for which every row of M^(-1) has at most s nonzero entries. The norm is the spectral/operator 2-norm. Supports, complex coefficients, and conditioning are unrestricted. The accepted E_REVIEW.md, Sections 1-4, binds this exact original model.

Put

    g=(sqrt(3)-1)/2.

**Theorem.** For every odd integer N>=3,

    Delta(N,N-2)^2
      >= 2/N + g^2/[sqrt(N)+g sqrt(N/(N-2))]^2
      >= (9-4 sqrt(3))/N.                              (1.1)

Since 9-4 sqrt(3)=2.0717967697...>2, this is a uniform relative separation from the inherited squared floor 2/N. In norm terms,

    Delta(N,N-2)/sqrt(2/N)
      >= sqrt((9-4 sqrt(3))/2)>1.01779.                 (1.2)

The sharper first bound has a squared lower-bound coefficient tending to

    2+g^2=3-sqrt(3)/2=2.1339745962... .

This is an asymptotic statement about the proved lower bound, not the unknown optimum or an asserted asymptotic formula for Delta.

Every distinct odd semiprime N=pq is included. The accepted semiprime classification already proves strict nonsharpness at this budget. The new result makes that separation quantitatively bounded away from the floor by a universal relative constant in the original simultaneous inverse-row-sparsity problem. The exact N=3 optimum remains inherited, not counted as new.

## 2. Two-column obstruction without row regularity

Let C be any N-by-N matrix having exactly two nonzero entries in each column, each of modulus N^(-1/2). Write T_i for its two-element column supports. No row regularity or prescribed phases are assumed.

There are two cases:

**Case I.** Some T_i and T_j intersect in exactly one row. Then

    |(C* C)[i,j]|=1/N.                                 (2.1)

**Case II.** No two supports intersect in exactly one row. Distinct supports are then disjoint. If there are r distinct supports, 2r<=N, so oddness gives r< N/2. The N columns distributed among these r supports force at least three columns to have the same support T.

For those three columns the three-by-three Gram G is positive semidefinite, has rank at most two, diagonal 2/N, and trace 6/N. Cauchy-Schwarz on its eigenvalues gives

    tr(G^2)>=(tr G)^2/2=18/N^2.

Its diagonal contributes 12/N^2. Thus its six ordered off-diagonal squared moduli sum to at least 6/N^2, and at least one pair satisfies

    |(C* C)[i,j]|>=1/N,    T_i=T_j.                    (2.2)

The distinction between the two cases is useful: the coefficient-error terms in the eventual stability identity see only T_j minus T_i. They see one position in Case I and no positions in Case II.

This is a global row-column incidence argument. It covers arbitrary irregular row degrees and arbitrary phases; no root-sum separation or rounding of approximate cyclotomic cancellation is needed.

## 3. Exact original-model stability identities

Fix an admissible M with s=N-2, and put

    B=M^(-1), E=M-F, rho=||E||_2,
    q=(N-2)/N, a^2=2/N, epsilon=rho^2-a^2.

Pad the actual support of each row b_i of B to any set S_i of exactly N-2 positions, without changing any coefficient of B. Define

    A[j,i]=F[j,i] 1_(j in S_i),
    C=F-A, Y=q B-A*, H=rho^2 I-E E*.

Then H is positive semidefinite, the support of row Y_i is contained in S_i, and the support T_i of column C_i is the two-element complement of S_i. In particular Y_i vanishes on T_i. Each C_i has norm sqrt(2/N), but only one or zero of its entries can contribute to the cross terms below.

Write x_i=||b_i||_2>0 and z_i=(b_i F)_i. The equality b_i E=e_i-b_i F and unitarity of F give

    b_i H b_i* =2 Re(z_i)-1-(q-epsilon)x_i^2.

Since b_i is supported on S_i and the restricted Fourier column has squared norm q,

    ||Y_i||^2=q^2 x_i^2+q-2q Re(z_i).

Hence the exact identity

    q b_i H b_i*+||Y_i||^2=q epsilon x_i^2             (3.1)

holds for every row, including rows whose actual support is smaller than N-2.

Define

    P=q epsilon B B*,
    Q=q B H B*+Y Y*,
    K=C* C-a^2 I.

The inherited one-row bound, or the calculation in Section 4, gives epsilon>=0. Thus P and Q are positive semidefinite. Formula (3.1) gives the equality of their individual diagonal entries, not merely their traces:

    P[i,i]=Q[i,i]=q epsilon x_i^2.                     (3.2)

Positive semidefinite Cauchy-Schwarz therefore implies

    |(P-Q)[i,j]|<=2q epsilon x_i x_j,
    ||Y_i||<=sqrt(q epsilon) x_i.                     (3.3)

Substitute A*=qB-Y and use B E=I-BF to obtain the exact matrix identity

    K=P-Q+Y C+C* Y*.                                  (3.4)

All matrices here remain in the original coordinates. No common support, binary-coefficient inverse, prescribed condition number, or Fourier-submatrix ansatz has been substituted for the original admissible class.

## 4. Inverse-row norm control

Cauchy-Schwarz on S_i gives Re(z_i)<=sqrt(q) x_i. Consequently

    rho^2 >= ||b_i E||^2/x_i^2
           =1+x_i^(-2)-2 Re(z_i)/x_i^2
           >=a^2+(x_i^(-1)-sqrt(q))^2.

This proves epsilon>=0 and, if epsilon<q,

    x_i <=1/[sqrt(q)-sqrt(epsilon)].                  (4.1)

For this case set

    u=sqrt(q epsilon)/[sqrt(q)-sqrt(epsilon)].

Then (3.3) gives |(P-Q)[i,j]|<=2u^2 and ||Y_i||<=u for all i.

## 5. Localizing the mask obstruction

Apply Section 2 to the padded complementary mask C.

In Case I, T_i and T_j share one position. Row Y_i vanishes on T_i, so its product with C_j has at most the one surviving entry on T_j minus T_i. Thus

    |(Y C)[i,j]|<=||Y_i||/sqrt(N)<=u/sqrt(N).

Similarly |(C* Y*)[i,j]|<=u/sqrt(N). Equations (2.1) and (3.4) give

    1/N<=2u^2+2u/sqrt(N).

Writing v=sqrt(N)u yields 1<=2v^2+2v, hence

    v>=g=(sqrt(3)-1)/2.                               (5.1)

In Case II, choose the pair from (2.2). Its supports are identical. Both cross terms vanish exactly, since Y_i and Y_j vanish on that common support. Equations (2.2) and (3.4) therefore imply

    1/N<=2u^2,
    v>=1/sqrt(2)>g.

Thus (5.1) holds in either case. Substituting u and rearranging gives

    sqrt(epsilon)
      >=g/[sqrt(N)+g/sqrt(q)].                        (5.2)

If epsilon>=q, the square of the right side of (5.2) is strictly smaller than q, so the resulting lower bound on epsilon is automatic. We have proved the first inequality in (1.1) for every admissible M, with no assumption that rho<1. Taking the infimum preserves it; no compactness or attainment argument is used.

For N>=3 we have 1/sqrt(q)<=sqrt(N). Therefore

    g/[sqrt(N)+g/sqrt(q)]
      >=g/[sqrt(N)(1+g)]
      =(2-sqrt(3))/sqrt(N).

Adding a^2=2/N gives

    rho^2 >= [2+(2-sqrt(3))^2]/N
            =(9-4 sqrt(3))/N,

as required.

## 6. Scope, attribution, controls, and stop

Only flat entry magnitudes and unitarity of F are used. The same proof consequently applies to every flat unitary target of odd order, with the same original inverse-row admissibility definition. This is an immediate extension of the proved argument, not a support classification or a claimed novelty theorem for complex Hadamard matrices.

The earlier separately sealed packet semiprime_quantitative_codim2_20261023 gives a weaker polynomial correction using a sharp relaxed mask operator-defect lemma. It is unchanged. The present packet instead localizes to two columns and improves the correction to order 1/N, establishing uniform relative separation. The sharpness of that earlier relaxed mask lemma does not make either inverse-row lower bound sharp. No optimizer or matching upper bound is proved here.

The full semiprime cycle classification is not being silently promoted to a full-budget quantitative result. For other nonexceptional budgets, controlling approximate long root sums and propagating approximate cycles remains unresolved. This packet stops at the odd codimension-two family and its original-model coefficient-stability mechanism. No generic exponentially small cyclotomic-height bound is offered as progress.

Fresh self-authored controls check the integer support dichotomy, the Gram lower certificates, exact stability identities evaluated numerically, arbitrary complex inverse coefficients, padded smaller supports, both obstruction cases, and negative controls. No historical scientific script was run. Numerical checks do not replace the proof; exact counts and tolerances are in RESULTS.json. The frozen source copies, report, controls, and outputs are hash-bound by MANIFEST.json and SOURCE_BINDINGS.json. Independent review is required before acceptance. No external state was changed.
