# Uniform one-extra-pole Prony construction

Date: 2026-10-09.

## Result and scope

For every even N=2h >= 4, the chirp moments from Phase 21 admit an exact sum of at most h+1 ordinary exponentials whose distinct, nonzero nodes avoid alpha^N=-1. Consequently the Phase 21 DFT identity admits at most h+1 admissible common-Weyl Green resolvents. Combined with the Phase 21 lower bound, the minimum pole count lies in {h,h+1} for every even N.

This report does **not** prove that the original degree-h polynomial is always squarefree or always avoids the forbidden nodes. It does not establish a faster FFT. Pole/root preparation, residues, conditioning, and applying the resolvents remain costs, and independent application of h+1 length-N solves takes quadratic work.

The extension is a self-contained deduction from elementary moment-polynomial and rational-pencil arguments. No claim of general novelty for these classical algebraic tools is intended. No uploaded executable was run.

## 1. Definitions

Set q=omega^(-1)=exp(2*pi*i/N) and c_m=q^(m(m-1)/2). Define the complex linear functional L on polynomials by L(z^m)=c_m. Only moments through index 2h-1 are needed for the result; the formula can harmlessly define later moments too.

For 0 <= n <= h, set

    R_n(z) = product_{k=0}^{n-1} (z-q^k) = sum_{j=0}^n r_(n,j) z^j,
    P_n(z) = sum_{j=0}^n (c_n/c_j) r_(n,j) z^j.

The empty product gives P_0=1. The polynomial P_h is precisely A_h in Phase 21 Section 3A. Each P_n is monic, has coefficients in Z[q], and has nonzero constant term

    P_n(0) = (-1)^n q^(n(n-1)).

Since c_(s+j)=c_s c_j q^(sj),

    L(z^s P_n) = c_s c_n R_n(q^s) = 0,  0 <= s < n.       (1)

These are formal orthogonality identities for a complex bilinear moment functional; no positivity or real-orthogonality theorem is being assumed.

## 2. Consecutive moment polynomials are coprime

Let Delta_n=det(c_(r+s))_(0<=r,s<n), with Delta_0=1. Diagonal factors and a Vandermonde factorization give

    Delta_n = q^[n(n-1)(n-2)/2]
              product_{d=1}^{n-1} (q^d-1)^(n-d).          (2)

Every factor is nonzero for n<=h. In particular, all these moment matrices are nonsingular, and P_n is the unique monic degree-n polynomial satisfying (1).

For completeness, the usual three-term argument is valid over C here. Expand zP_n in the monic basis P_0,...,P_(n+1). For k<=n-2,

    L((zP_n)P_k)=L(P_n(zP_k))=0.

The squared bilinear norms L(P_k^2)=Delta_(k+1)/Delta_k are nonzero when needed, so all coefficients below P_(n-1) vanish. Thus, for 1<=n<=h-1,

    P_(n+1) = (z-a_n)P_n - b_n P_(n-1),
    b_n = Delta_(n+1) Delta_(n-1) / Delta_n^2
        = q^(3n-3)(q^n-1) != 0.                          (3)

One explicit diagonal coefficient, not needed for coprimality, is

    a_n = q^(n-1)(q^(n+1)+q^n-1).

Also P_1=z-1. If P_h and P_(h-1) shared a root, (3), with its nonzero b_n, would propagate that common root down to P_0=1. Therefore

    gcd(P_h,P_(h-1))=1.                                  (4)

Combining (4) with P_(h-1)(0)!=0 gives

    gcd(zP_h,P_(h-1))=1.                                 (5)

No inference that P_h itself is squarefree is made.

## 3. A one-parameter recurrence of order h+1

Define

    F(z)=zP_h(z),   G(z)=P_(h-1)(z),
    B_t(z)=F(z)+tG(z).

For every complex t, B_t is monic of degree h+1. For 0<=s<=h-2, equation (1) gives

    L(z^s B_t)=L(z^(s+1)P_h)+t L(z^s P_(h-1))=0.         (6)

These are exactly the recurrence constraints on 2h available moments for an order-(h+1) recurrence. When t!=0, B_t(0)=tP_(h-1)(0)!=0.

## 4. An explicit finite parameter set always contains a valid choice

Equation (5) makes F and G coprime. If alpha is a multiple root of B_t, then G(alpha)!=0 (otherwise F(alpha)=0), and eliminating t from B_t(alpha)=B_t'(alpha)=0 yields

    W(alpha)=0,
    W(z)=F'(z)G(z)-F(z)G'(z).

Because F and G are monic of respective degrees h+1 and h-1, W has degree 2h-1 and leading coefficient 2. It is not the zero polynomial. Each root alpha of W for which G(alpha)!=0 supplies at most one bad parameter, namely t=-F(alpha)/G(alpha). Hence at most 2h-1 distinct complex parameters make B_t nonsquarefree.

The forbidden-node set E={alpha: alpha^(2h)=-1} has 2h distinct members. For alpha in E:

- If G(alpha)=0, then F(alpha)!=0 by coprimality, so alpha is a root of no B_t.
- Otherwise precisely one parameter can make it a root: t=-F(alpha)/G(alpha).

Thus at most 2h further distinct parameters produce any forbidden node. The union of the two bad-parameter sets has cardinality at most 4h-1. Consequently at least one integer

    t in {1,2,...,4h} = {1,2,...,2N}                      (7)

makes B_t squarefree and coprime to z^N+1. All candidates in (7) are nonzero, so its roots are nonzero as well. This is a uniform characteristic-zero existence proof, not an inference from experiments.

Equation (7) gives a finite algebraic selection procedure: construct each candidate and test the two polynomial gcds over the cyclotomic field Q(q). It is not a favorable complexity bound for computing all roots or for applying the DFT. One may also certify an individual candidate by a suitable finite-field reduction with nonzero resultants; a failed reduction is not evidence that the characteristic-zero candidate fails.

## 5. Exact moment and resolvent reconstruction

Choose a valid t from (7), and let alpha_1,...,alpha_(h+1) be the distinct roots of B_t. Solve the nonsingular (h+1)-node Vandermonde system

    c_m = sum_{ell=1}^{h+1} beta_ell alpha_ell^m,
    0 <= m <= h.

The right-hand sequence satisfies the B_t recurrence for every later index, because each alpha_ell is a root. Equation (6) says the chirp sequence satisfies the same recurrence for each remaining required index h+1,...,2h-1. The monic leading coefficient makes each next term uniquely determined, so

    c_m = sum_{ell=1}^{h+1} beta_ell alpha_ell^m,
    0 <= m < N.                                         (8)

For the Phase 21 Weyl shift T with T^N=-I, define

    gamma_ell=beta_ell(1+alpha_ell^N).

Every inverse exists by construction, and the finite geometric-series identity gives

    sum_{m=0}^{N-1} c_m T^m
      = sum_{ell=1}^{h+1} gamma_ell (I-alpha_ell T)^(-1).

Using the Phase 21 chirp identity,

    Fhat = (Q/sqrt(N))
           sum_{ell=1}^{h+1} gamma_ell (I-alpha_ell T)^(-1).

Zero residues, if any, may be omitted, so this is an at-most-(h+1)-pole representation. The previously proved lower bound h applies. The precise uniform conclusion is therefore

    h <= minimum admissible common-Weyl pole count <= h+1.

## 6. Independent checks and their limits

The independently authored script `independent_checks.py`:

1. Checks the defining moment identities symbolically for degrees 1 through 8.
2. Checks the explicit three-term recurrence symbolically through degree 8.
3. Constructs P_h and P_(h-1) from their defining products over a prime field, without using that recurrence to construct them.
4. Verifies consecutive coprimality, selects a t, checks B_t against its derivative and z^N+1, and verifies every required moment-recurrence equation and reconstruction.

Run:

    python independent_checks.py

The checked sizes are every even N from 4 through 130, together with 256, 512, and 1024 (67 sizes). All passed. The candidate t=1 worked in every tested reduction; **no claim that t=1 works uniformly follows**. Prime, primitive root image, candidate parameter, degrees, and results appear in `check_results.json`. The gcd entries are degrees: 0 means a constant gcd.

Finite-field checks are supplementary; the uniform proof is Sections 1-5. In the checks, p>4h and q has exact order N. The same nonzero-leading-coefficient and bad-parameter counting argument is compatible with these characteristics. A successful coprimality reduction also independently certifies the selected characteristic-zero candidate by the integral-resultant argument.

## 7. Original h-pole question remains open here

The relation

    P_h(z) = (-1)^h q^(h(h-1))
             H_h(-q^(-(h-1))z;q),
    H_h(u;q)=sum_{j=0}^h [h choose j]_q u^j,

identifies the original polynomial with a scaled Rogers-Szego polynomial. Standard positivity/real-orthogonality zero theorems cannot simply be applied at nonreal q=exp(pi*i/h). Consecutive coprimality likewise does not imply that a single polynomial is squarefree. The derivation above deliberately avoids both unsupported steps.

For primary background on the finite q-binomial/continuous-q-Hermite correspondence, see NIST DLMF, equation 18.28.16: https://dlmf.nist.gov/18.28.E16 . The standard real-q zero theory from that setting is not invoked in the proof. The required specialized recurrence and coprimality facts were proved above directly from the moments.

No counterexample to the original h-pole claim was established. No uniform h-pole proof was established. The rigorously completed useful result is the uniform h+1 construction.
