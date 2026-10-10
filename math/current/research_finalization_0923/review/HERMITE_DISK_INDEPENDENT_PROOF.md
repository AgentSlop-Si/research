# Independent review: quasi-Hermite discriminant exclusion

Date: 10 October 2026. Status: **accepted**, with the stronger statement below proved independently in this review. This is an internal mathematical review, not external peer review or worldwide priority certification.

## Precise theorem

Let A be a positive integer and let He_A be the monic probabilists' Hermite polynomial, characterized by He_0=1, He_1=y and He_(A+1)=y He_A−A He_(A−1). Define

J_(A+1)(y;τ)=y He_A(y)−τ He_A'(y)=He_(A+1)(y)+A(1−τ)He_(A−1)(y).

1. Every nonreal parameter τ for which J has a multiple root satisfies

   |1−τ|² > (A+1)/A.

2. The only real bad parameter is τ=0 when A is odd, and τ=−1/A when A is even. The corresponding zero at y=0 has multiplicity two and three, respectively.

3. Consequently J is squarefree whenever |1−τ|≤sqrt((A+1)/A) and τ≠0. In particular the originally proposed closed unit disk centered at 1 is valid. For even A, τ=0 may also be included.

The radius is a proved sufficient exclusion radius, not asserted optimal.

## Independent proof

Hermite orthogonality gives distinct real zeros. By parity, write the positive zeros as r_1,...,r_k and δ=A mod 2. Then, for z=y² away from the poles,

f(z)=He_A'(y)/(y He_A(y))=δ/z+Σ_j 2/(z−r_j²).

All residues are positive. In particular

Im f(z)=−Im z [δ/|z|²+Σ_j 2/|z−r_j²|²],

and, for real z away from the poles, f'(z)<0.

Suppose τ≠0 and y is a nonzero multiple root of J. He_A(y) cannot vanish, since its zeros are simple and J(y)=−τ He_A'(y) at such a zero. Thus f(z)=1/τ and f'(z)=0. The second assertion follows by differentiating J=y He_A(y)[1−τ f(y²)] at its root.

The Hermite differential equation He_A''−y He_A'+A He_A=0 and J'=0 give

0=1+Aτ+(1−τ)y²/τ.

The parameter τ=1 gives He_(A+1), which is squarefree. For σ=1−τ≠0, the equation is

z=(2A+1)−Aσ−(A+1)/σ.

If τ is nonreal, the Stieltjes formula f(z)=1/τ implies that Im z and Im τ have the same nonzero sign. On the other hand,

Im z=Im τ [A−(A+1)/|σ|²].

The bracket must be positive, proving |σ|²>(A+1)/A.

If τ is real and nonzero, f(z) is real. The imaginary-part identity forces z real, where f'(z)<0. Thus a nonzero multiple root is impossible.

It remains to check y=0 and τ=0. For odd A, He_A has a simple zero at zero; hence J(0;τ)=−τ He_A'(0) vanishes only when τ=0. Then y He_A has a double zero at zero and all its other zeros are simple. For even A, He_A(0)≠0 and

J'(0;τ)=(1+Aτ)He_A(0).

Therefore zero is multiple exactly at τ=−1/A. Using He_A''(0)=−A He_A(0) and He_A''''(0)=A(A−2)He_A(0), its cubic coefficient is −(A+1)He_A(0)/3, which is nonzero. At τ=0, y He_A is squarefree for even A. These facts prove the classification and disk consequence.

## Application and remaining guards

If the half-order Rogers–Szegő parameter satisfies 1/τ+1/conj(τ)=1 with τ≠0, then |τ−1|=1, so Disc J is automatically nonzero in characteristic zero for every A≥1. This removes precisely that guard. It does not remove g≠0, Disc U≠0, Res(F,U)≠0, or any finite-characteristic exclusion in the underlying local-cluster theorem. The half-order identity and its Rogers–Szegő normalization are the algebra lead's separate responsibility; this review establishes the entire analytic-polynomial implication.

### Final fusion addendum: independently accepted prime-order corollary

The reviewer subsequently read and rederived §§2–3 of the prior `diagonal_chirp_classification_0246/CLASSIFICATION.md` and checked the half-order q-product circle identity in the new algebra manuscript. The following stronger fused scope is now **accepted**, rather than left conditional on an uninspected statement:

- For every d≡3 mod4, b=(d−1)/2, and every primitive complex d-th root ω, H_b(z;ω) has exactly the simple shared root −1 with z^d+1. Hence for U=H_b/(z+1), both U(−1)≠0 and Res(z^d+1,U)≠0 are automatic. Only Disc U remains as a residual squarefreeness guard.
- If d is prime, H_b is squarefree. Thus every prime d≡3 mod4 and every A≥1 satisfy the local overlap splitting and leading ordinary-discriminant formulas without any residual guard. In particular ord_(Phi_d) Disc H_(Ad+b)=dA(A−1)/2+A.

The resonance proof was checked at the level of its matrix congruence. In the principal embedding, the continuous-q-Hermite Jacobi matrix is J=DRD with R real symmetric irreducible zero-diagonal and D diagonal phases. Both real and imaginary parts of D^(-2) are positive. A real nonzero eigenvalue would imply Rv=tD^(-2)v and contradict imaginary parts of the quadratic form. In odd dimension, the kernel of R is one-dimensional and the coefficient of t in det(R−tD^(-2)) is a nonzero real factor times v_0^T D^(-2)v_0, proving a simple zero. Substituting back gives exactly the simple resonant root; algebraic Galois invariance, not an assumption that Galois maps preserve absolute values, covers every primitive embedding.

The prime squarefreeness proof uses the integral identity D_b(q)=(q−1)^(b(b−1)/2)E_b(q), E_b(1)=Π_(j=1)^b j^j, obtained by the Hermite degeneration. If E_b vanished at a primitive prime-order d-th root, Phi_d would divide E_b, making d divide E_b(1), impossible for b<d. This proof was inspected rather than inferred from recorded finite tests.

The standalone disk theorem still removes only its own guard. The stronger corollary comes from explicitly combining it with these two independently checked prior theorems. It does not establish all-composite squarefreeness or replace finite-characteristic pairing arguments.

## Checks and provenance

The derivation above is independent, not inferred from numerical testing. Fresh self-authored symbolic checks computed small-A discriminants; the first cases are 4τ, 4(2τ+1)^3, 432τ(3τ²+2τ+3)^2 and 27648(4τ+1)^3(2τ²+3)^2 for A=1,2,3,4. Exploratory Newton calculations through A=100 found no disk counterexample, but were non-exhaustive and are not proof evidence. No supplied research program was executed, imported, compiled, or AST-parsed.

## Novelty disposition

**Specialized synthesis/application; priority unresolved.** The Stieltjes-ratio sign argument, Hermite differential equation, and Hermite–Laguerre parity reduction are classical machinery. The established quasi-Laguerre discriminant formula already describes this polynomial family after a quadratic pullback. The concrete possible contribution is the useful explicit exclusion region and its removal of a Rogers–Szegő local-discriminant guard. No global originality claim follows from bounded searches.

Primary sources checked or identified:

- NIST DLMF §18.2(vi), classical simple real zeros and interlacing: https://dlmf.nist.gov/18.2#vi (relevant statement inspected).
- Sawa–Uchida, *Discriminants of classical quasi-orthogonal polynomials, with combinatorial and number-theoretic applications*: https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf ; preprint https://arxiv.org/pdf/1802.00605v1 . The quasi-Laguerre formula and the exact parity reduction in the prior corpus are close antecedents; no priority certification is asserted.
- A 2025 work titled *Zeros of linear combinations of Laguerre polynomials* surfaced during search. Full primary-text comparison remains outstanding and must be resolved before stronger novelty language.
