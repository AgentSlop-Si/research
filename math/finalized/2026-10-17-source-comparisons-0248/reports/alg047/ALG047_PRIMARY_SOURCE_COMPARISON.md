# ALG047 ordered Weyl pair source comparison

Date: 17 October 2026  
Repository baseline: AgentSlop-Si/research, commit 26eb7017276591988762f27e2d1c23e739bcf3e4  
Scope: the exact Fourier-symbol separation rank for one fixed independent ordered pair of Weyl lines at odd prime length.

## Result

The rank-one versus rank-N dichotomy has a precise primary-source derivation. Gurevich and Hadani supply the Weyl-symbol algebra and quadratic Cayley kernel; Gurevich, Hadani and Howe identify the positive, unnormalized Fourier operator with the Weyl element and give its scalar. After the coordinate and normalization changes below, the repository tensor follows. Removing two invertible diagonal phases leaves an all-ones matrix or a permuted Fourier matrix.

Neither selected source states the repository's ordered-pair rank dichotomy as a named theorem. The appropriate attribution is **an elementary fixed-pair consequence of the cited classical formulas**, with the rank reduction and compatible-pair classification written out here. This is stronger than merely listing related literature and weaker than a claim that the entire repository result appears verbatim in a source.

The selected passages do not supply the repository's rational-degree statement or a finite-coefficient-field transfer theorem. Those are kept distinct. This comparison does not close the broader record, change its priority, establish historical novelty, or turn product count into an arithmetic-operation lower bound.

## Retained repository evidence

The [independent review](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/archive/objects/48/48aa7789ccad0f2c0bcadb36adc63345438e39e076c8bcf8582eaad60803a1b5__INDEPENDENT_REVIEW.md) has SHA256 48aa7789ccad0f2c0bcadb36adc63345438e39e076c8bcf8582eaad60803a1b5. Its complete proof and guards were read.

The review identifies the v22 source archive by SHA256 e1d30f08aa720c4e492a0e268b343d08d52bd80ecb126ab3fbe6c27097f36906. That exact archive was recovered from the retained v25 → v24 → v23 → v22 nesting and hash-checked before reading its RESEARCH.md. The proof file has SHA256 74f35b38e525cc0df6496931fe88c51fc81e046dc7796ceb2a6c738146202122. The two unchanged texts are retained under source_snapshot. No supplied research program or bytecode was executed.

The v22 proof contains the Fourier symbol in §2, rank dichotomy in Theorem 3.1, compatible pair classification in §4, and explicit factor entries in §5. Its §6 recurrence/minor argument is superseded for this comparison by the independent review's stronger tail-polynomial proof and its finite-field warning. The present task does not reopen the accepted scoped correctness decision.

## Primary source locations

### Gurevich and Hadani 2006

[The Geometric Weil Representation, math/0610818v1](https://arxiv.org/pdf/math/0610818v1), printed pages 6–7, Eq. (1.2.2), Eq. (1.2.3), Theorem 1.2.1 and the following restriction to V: the inverse symbol is dim(H)^−1 Tr(Aπ(h^−1)); operator composition becomes twisted convolution. Printed page 9, Eq. (2.1.1), gives the kernel

    K_g(z) = ν(g) ψ(ω(κ(g)z,z)/4),
    κ(g) = (g+I)(g−I)^−1,
    ν(g) = G^(2r) q^(−2r) χ(det(κ(g)+I)),

for g−I invertible. Here the paper's N is renamed r, half the phase-space dimension, to avoid confusing it with transform length. For this comparison r=1 and q=N. The source has complex-valued representations of a group defined over a finite field. [Source](https://arxiv.org/html/math/0610818v1)

### Gurevich Hadani and Howe 2008

[Quadratic reciprocity and the sign of the Gauss sum via the finite Weil representation, 0808.2447v3](https://arxiv.org/pdf/0808.2447v3), §1.1 and §1.2.1, printed pages 2–3, fix ω((t,b),(t′,b′))=tb′−bt′ and π(t,0)f(x)=f(x+t), π(0,b)f(x)=ψ(bx). Section 2.1 and Theorem 2.4, printed page 5, use the positive unnormalized DFT and state

    F_N = C_N ρ_N(w),
    w = [[0,1],[-1,0]],
    C_N = i^((N−1)/2) sqrt(N),

for the standard character ψ(x)=exp(2πix/N). The theorem covers odd N and states independence from the chosen linearization. The rank argument below only uses its odd-prime specialization. The introductory matrix has the opposite sign; the theorem's matrix agrees with the displayed Schrödinger action and Egorov identity. [Source](https://arxiv.org/pdf/0808.2447v3#page=5)

## Conventions and normalization

All exponents below are in F_N, where N is an odd prime; fractions mean modular inverses. The repository uses

    X e_j = e_(j+1),    Z e_j = omega^j e_j,
    F[i,j] = omega^(ij),
    D_(a,b) = omega^(ab/2) X^a Z^b,
    sigma((a,b),(c,d)) = bc−ad.

The matrix product AB applies B first. The phrase "ordered pair" is essential.

Let R=diag(−1,1). A repository direction u=(a,b) corresponds to source coordinates Ru=(−a,b). In the function model, Xf(x)=f(x−1). The Heisenberg group law therefore gives

    π(t,b) = psi(−tb/2) π(t,0)π(0,b),
    π(−a,b) = omega^(ab/2) X^a Z^b = D_(a,b),
    ω(Ru,Rv) = sigma(u,v).

Consequently the source multiplication law becomes exactly

    D_u D_v = omega^(sigma(u,v)/2) D_(u+v).

There is no extra conjugation or sign change of the central character in this map.

Use the quotient-V symbol normalization throughout:

    Ahat(u) = N^−1 Tr(A D_(−u)),
    A = sum_(u in F_N²) Ahat(u) D_u.

The trace can be cyclically reordered, so this agrees with the review's Tr(D_(−u)A). The source's center-equivariant description over H requires a center average: summing the same symbol against π(h) over H contributes N identical terms for each V-coordinate. Thus the equivalent group synthesis is N^−1 sum_H Ahat(h)π(h). A literal unnormalized sum over H cannot be combined with the stated trace inverse. The restriction-to-V formula after Theorem 1.2.1 and the normalized convolution in Eq. (1.2.3) fix the convention used here. This explicitly avoids carrying a spurious factor N from the printed group-sum notation.

In repository coordinates, positive Fourier satisfies

    F X F^−1 = Z,    F Z F^−1 = X^−1,
    J = [[0,−1],[1,0]] = R^−1 w R.

The opposite sign of J and the source w is therefore a coordinate change, not a negative-sign DFT. For the source's w, det(w−I)=2, so its Cayley kernel applies at every odd prime, including 3. The 2006 representation's uniqueness exception at F_3 in dimension two does not invalidate this Fourier comparison: the 2008 theorem fixes the Weyl-element operator independently of linearization, and the direct trace calculation below also handles N=3.

## Deriving the Fourier symbol

Since w²=−I, direct algebra gives κ(w)=−w. At z=Ru=(−a,b),

    ω(κ(w)z,z) = −a²−b².

The source quadratic kernel therefore has the repository phase omega^(−(a²+b²)/4). Its normalization is also compatible. In dimension two,

    ν(w) = G²/N² · χ(2) = χ(−2)/N,

using G²=χ(−1)N. For the standard complex character, Theorem 2.4 and Tr(F)=G give

    C_N ν(w) = G/N = gamma.

Equivalently Tr(ρ_N(w))=χ(−2), as follows from the source character formula, so G=C_Nχ(−2). This is an exact scalar identity; it does not identify gamma with N^−1/2 without its phase.

The numerical expression for C_N above is explicitly tied to the standard character. For a different primitive omega, or for a different coefficient field, use the exact trace normalization rather than importing that complex scalar unchanged. Independently of the Weil linearization, the repository matrix definitions give

    Fhat(a,b)
      = N^−1 sum_j omega^(j²+(a−b)j−ab/2)
      = gamma omega^(−(a²+b²)/4),
    gamma = N^−1 sum_j omega^(j²).

The last step completes the square. This confirms both sign and scalar and connects the general primitive-root version directly to the retained proof.

## Deriving the exact ordered pair rank

Fix nonzero u=(a,b), v=(c,d) with ad−bc nonzero. Let

    A = sum_m alpha_m D_(mu),
    B = sum_n beta_n D_(nv).

The map (m,n) → mu+nv is bijective. Thus each Fourier symbol coordinate comes from exactly one pair of line coefficients, and the product coefficient is

    (AB)hat(mu+nv) = alpha_m beta_n omega^(sigma(u,v)mn/2).

For the positive Fourier target, remove that ordered-product cocycle:

    T[m,n] = Fhat(mu+nv) omega^(−sigma(u,v)mn/2).

Expanding its quadratic form yields

    T[m,n] = gamma
             omega^(−(a²+b²)m²/4)
             omega^(−(c²+d²)n²/4)
             omega^(−k mn/2),
    k = u dot v + sigma(u,v).

The first and second phases are nonzero diagonal scalings, and gamma is nonzero under the retained guards. Hence T has the same rank as M[m,n]=omega^(−k mn/2).

* If k=0, M is the nonzero all-ones matrix, of rank one.
* If k is nonzero, multiplication m → −km/2 permutes F_N. Thus M is a row permutation of F. Its columns are independent: they form a Vandermonde matrix at the N distinct points 1,omega,...,omega^(N−1). Its rank is N.

This proves the exact dichotomy, with no intermediate rank, from the source formula plus elementary linear algebra. It does not use a prime-Fourier full-spark theorem.

The same argument also proves that the **minimum number of products on this one fixed ordered pair** is exactly rank(T). Every product supplies one outer product after removing the cocycle, giving the lower inequality. Conversely every rank decomposition T=sum_(s=1)^r alpha^(s)(beta^(s))^T yields r line-operator products whose sum is F, giving the upper inequality. The directions must remain fixed throughout this statement; allowing a different pair for each summand changes the model.

## Compatible directions and exposed factor

The scalar equation k=0 becomes

    (a+b)c + (b−a)d = 0.

Since u is nonzero, all nonzero solutions have

    v = t(a−b,a+b),    t nonzero,
    det(u,v) = t(a²+b²).

Therefore an independent compatible pair exists exactly when u is anisotropic, a²+b² nonzero. Its partner has norm 2t²(a²+b²), also nonzero. On reversing the pair, k becomes u dot v−sigma(u,v)=−2sigma(u,v), nonzero. Compatibility is not order-invariant.

In the compatible case all entries of T are nonzero, so its two vectors are unique up to reciprocal nonzero scalar factors. With

    L_u = sum_m omega^(−(a²+b²)m²/4)D_(mu),

one gets F=L_u(gamma L_v). This coefficient classification is an elementary consequence of the rank-one expression, rather than an additional theorem found in the two selected passages.

The retained proof then gives a direct entry calculation. For a nonzero a,

    L_u[i,j] = omega^(−(a−b)² i²/(4a²))
               omega^((a²+b²)ij/(2a²))
               omega^(−(a+b)² j²/(4a²)).

For an anisotropic u, the middle coefficient is nonzero, so L_u is obtained from the positive Fourier matrix by an invertible diagonal factor on each side and a row permutation. Applying or undoing these endpoints costs O(N) once their parameters are supplied; consecutive phases can also be prepared in O(N) field work. If a=0, completing a one-variable Gauss square instead gives a diagonal factor. Two independent directions cannot both be vertical, so every compatible pair contains at least one nonvertical Fourier-equivalent factor.

This is a reduction under the specified separately evaluated representation. It supplies no unrestricted scalar-operation lower bound and no faster Fourier primitive. The cited primary formulas carry no operation-cost theorem that would change that boundary.

## Repository extensions kept separate

### Finite phase space and finite coefficient fields

The finite field F_N indexing the source group is not the field of matrix coefficients. The selected classical sources use complex-valued representations. The repository also permits a coefficient field K with characteristic not dividing 2N, a supplied primitive Nth root omega, and nonzero gamma.

The latter scope is justified directly by the retained algebra: Tr(D_(−u)D_v)=N delta_(u,v) makes the symbol map nondegenerate; completing the square gives the symbol; and the Vandermonde determinant proves the residual Fourier rank. No complex positivity or arbitrary transfer of Fourier minors is needed. This elementary extension is not presented as a statement already quoted from the selected sources. Root construction, bit cost and numerical stability remain separate.

Primality cannot be dropped just because the 2008 Fourier/Weil identity covers odd composite lengths. For example, at N=9, u=(1,0), v=(4,1) have unit determinant 1 but k=3. The residual matrix omega^(−3mn/2) has rank 3, neither 1 nor 9. The nonzero-k step needs k invertible, which is automatic over prime-length F_N but not over Z/NZ for composite N.

### Rational degree

The independent review proves the stronger guarded statement deg(q)+deg(p) >= N−1 for

    L_u = q(C)^−1 p(C),    C=D_u,    a²+b² nonzero,

with q(C) invertible and ordinary one-sided polynomial representatives in this specified generator. It is not a consequence explicitly supplied by either selected primary passage.

To see the separate mechanism, put Q=a²+b² and a_r=omega^(−Qr²/4). If d=deg(q) and e=deg(p) are below N−1, the cyclic coefficient equations for r=e+1,...,N−1 give

    0 = a_r sum_(j=0)^d q_j omega^(−Qj²/4) (omega^(Qr/2))^j.

The inner sum is a nonzero polynomial of degree d, at N−1−e distinct nodes, so d>=N−1−e. The cases d or e at least N−1 are immediate. This proof extends to the guarded field K and avoids the original v22 argument's unsupported finite-field full-spark transfer. The inverse guard remains essential to interpreting a rational representation. Laurent supports, varying generators and general shared evaluators are outside this argument.

Thus this pass resolves a primary-source mapping for the fixed-pair rank ingredient, while leaving any distinct historical attribution search for the rational-degree refinement outside its closure. It does not establish that the refinement is new.

## Fresh controls and their limits

Run `python3 check_conventions.py` in this directory. CHECK_RESULTS.json records a fresh successful execution. The checker imports only the Python standard library and no supplied program.

It checks the source/repository operator map, all Weyl coefficients and cocycle pairs at N=3,5,7 over suitable prime coefficient fields. It independently constructs the dephased tensors and row-reduces all 2,544 independent ordered pairs: 368 are compatible and have rank one; all others have rank N. Every compatible pair's reversed-order failure is checked. The N=9 example is an exact composite guard control. A separately labelled floating-point check corroborates the standard complex scalar at primes through 19; the written identity, not that numerical check, establishes the scalar generally.

These finite controls corroborate signs, normalization and hypotheses. The symbolic derivation is the proof. The previously accepted full repository replay and the rational-degree tests are not represented as newly replayed here.

## Bounded disposition

The ordered fixed-pair rank comparison is mapped to primary formulas with an explicit hypothesis, sign, scalar, cocycle and linear-algebra bridge. It is appropriate to append this result to ALG047's owner history while preserving its current status and priority. The broader restricted-resolvent attribution, arbitrary multiline factors, varying-pair sums and shared evaluation questions are not closed by this packet.
