# NF-03 independent review: explicit even-length legal pencil family

Date: 11 October 2026. Review of the exact candidate proof with SHA-256
`ad435354eceb014f2e28cedc6563181505076fdc1ef9421eba14bb546e06ff2f`.

## Verdict

**Scoped ACCEPT: mathematical family, uniform quantitative envelopes, exhaustive certified preparation, and exact-rational query contract. No mandatory mathematical repair found.**

The accepted statement is: for every even integer N=2h>=4, the polynomial
B_N(z)=zP_h(z)+2^(10N^3+2)P_(h-1)(z) has h+1 distinct nonzero roots avoiding alpha^N=-1. These roots support the previously accepted common-Weyl bank identity, explicit uniform separation and nonpole bounds, and an effective certified preparation procedure taking 2^[O(p+N^7)] bit operations. Once prepared, the bank has a paid O(N^2) rational-operation application and the stated conservative polynomial bit bound, with relative output error below 2^(-p).

The same family has unscaled moment Vandermonde condition number exp(Omega(N^4)). It supplies neither useful growing-degree conditioning nor practical preparation. Acceptance does not extend to a fast FFT, a production floating-point implementation, h-pole optimality, universal t=1, or external novelty. The earlier h+1 existence theorem remains accepted independently of this review. Its finite parameter-selection rule was already effective in an algebraic sense; the new contribution under review is the particular closed-form parameter and its explicit quantitative/bit-cost contract, not first computability of the existence result.

### Component decisions

- T1, closed-form all-even legal parameter: ACCEPT.
- T2, radius, separation, nonpole, derivative, Vandermonde and residue envelopes: ACCEPT.
- T3, exp(Omega(N^4)) condition-number lower bound: ACCEPT for this unscaled family only.
- A1, finite-grid Rouché certification, root identification and complete disjoint disk selection: ACCEPT.
- A2, coefficient construction, preparation bit model, weights and residue precision: ACCEPT.
- A3, signed-shift query, endpoint ledger, relative error and exact-rational application bit cost: ACCEPT.
- I1, implemented full exhaustive grid or production numerical executor: NOT CLAIMED / NOT VALIDATED.
- W1, close all NF-03 goals or growing-degree stability: REJECT as an overextension; practical conditioned construction remains open.

The small implementation clarifications in Section 6 below instantiate slack already present in the candidate. They do not change its parameter, bounds, asymptotic cost or verdict.

## 1. Artifact and dependency audit

The reviewed local proof matches the supplied SHA-256 and the proof member of the candidate ZIP. The candidate ZIP matches SHA-256 `2c28b73941c59aee6a8697ed13d2e6db5c359d02b25f8f1ef3422c1b2370913e`. Its source ledger's eight copied-source hashes were independently checked.

The relevant accepted dependencies were inspected as inert text:

- P02 Section B, hash `f6412a2cb78457a2fddd62a6e688095cb82528b4457ad1454dbbe069179937d6`, supplies the moment polynomials, consecutive coprimality, finite bad-parameter argument, recurrence propagation and pole-count scope. R16 accepts this exact body.
- P05, hash `02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787`, is accepted at fixed-degree scope by R21. The candidate's growing-N envelopes are derived afresh and do not rely on uniformity of P05's fixed-degree constants.
- The earlier pencil extension and Phase 21 target conventions were inspected for sign, reciprocal and node conventions.

No author control script or inherited research executable was run. The independent checker in this packet imports no such program. No Sheet, GitHub repository, accepted dependency or candidate source was modified.

## 2. Algebraic family and uniform height argument

### 2.1 Nonzero bad-parameter polynomial

P_n is monic with nonzero constant term. The accepted Hankel determinants are nonzero through the required degrees, and the nonzero three-term coefficient propagates any putative common root of P_h and P_(h-1) to P_0=1. Thus F=zP_h and G=P_(h-1) are coprime.

At a multiple root of F+tG, G cannot vanish; eliminating t gives W=F'G-FG'=0. W has degree 2h-1 and leading coefficient (h+1)-(h-1)=2. Hence only finitely many t give repeated roots. At any forbidden root of z^N+1, F+tG is either a nonconstant affine polynomial in t or a nonzero constant. Consequently both resultant polynomials are nonzero, and so is their product A(t). Monicity fixes the z-degree of B_t at m=h+1 for every t: there is no hidden degree drop or root at infinity.

### 2.2 Embeddings, integers and Cauchy bound

Every embedding of Q(q) maps q to a primitive unit-modulus Nth root. The product definition gives coefficient l1 norm at most 2^n for every conjugate P_n. The phase multipliers have modulus one. The same bound holds for the bivariate coefficient norm used for B_t.

The two Sylvester dimensions are 2m-1=N+1 and m+N, individually at most 2N. Their entry-polynomial coefficient norms are at most N*2^N. The deliberately enlarged determinant bound has binary logarithm

4N log2(2N)+4N log2(N*2^N)
=4N+8N log2 N+4N^2 <=9N^2,

using log2 N<=N/2 and 4N<=N^2 for N>=4. The candidate's 10N^2 bound is therefore valid uniformly, including N=4.

The product H(t)=product_sigma sigma(A(t)) is a product of whole conjugate polynomials, not a coefficient-by-coefficient multiplication rule. It is nonzero in K[t]; its coefficients are algebraic integers fixed by the Galois group, hence ordinary integers. Its l1 norm is at most 2^(10N^3). Its leading coefficient is a nonzero integer, so Cauchy's bound needs no unavailable lower bound on one chosen complex coefficient. The proposed t_N exceeds 1+2^(10N^3) strictly. This proves both legal resultants are nonzero. B_N(0)=t_N P_(h-1)(0) excludes zero nodes separately.

### 2.3 Reversal and normalization

The proof does not require reversing B_N or assuming that its reciprocal is monic. For a nonzero constant term, z^m B_N(1/z) retains degree m, has constant term 1 and leading coefficient B_N(0), and labels reciprocal roots. The forbidden set is invariant under inversion. For even N, its resultant with z^N+1 equals that of B_N; its discriminant also equals B_N's discriminant. These identities were independently checked at symbolic t for N=4,6,8,10. They support the convention audit, not an extra hypothesis in the proof. No lower-root bound is inferred from an incorrectly normalized reciprocal polynomial.

## 3. Quantitative bounds and conditioning

### 3.1 Radius and nonzero lower radius

Each conjugate polynomial is monic with coefficient l1 norm at most 2^(L+N). Cauchy's bound is below R=2^(L+N+1). In the chosen embedding the product of root moduli is t_N, since the constant coefficient has that modulus. Removing m-1 factors bounded by R gives |alpha_i|>=t_N R^(-(m-1)), stronger than the printed lower bound. No individual root integrality assumption is needed here.

### 3.2 Discriminant and forbidden resultant

The discriminant is a nonzero algebraic integer. All of its conjugates are bounded by M_D=(2R)^(m(m-1)); its nonzero integer field norm yields |D_B|>=M_D^(-(d-1)). Isolating one squared root difference and bounding the other m(m-1)-2 factors gives

|alpha_i-alpha_j|>=(2R)^(1-Nm(m-1)/2),

which is stronger than delta. The degree in this estimate is the coefficient-field degree d=phi(N), not the degree of a splitting field. A splitting-field norm is unnecessary and would be a different bound.

The same coefficient-field norm argument applies to J=Res(B_N,z^N+1), with conjugate bound (2R^N)^m. Removing the other m-1 factors gives |1+alpha_i^N|>=(2R^N)^(-(Nm-1))>=eta. Factoring alpha_i^N+1 and bounding the other distances by 2R gives rho. These arguments justify each all-embedding lower bound before it is used.

At a root, monicity and separation imply |B_N'(alpha_i)|>=delta^(m-1)=d_0, the exact derivative hypothesis needed by the grid proof.

### 3.3 Vandermonde orientation, dimensions and resolvents

For V[k,i]=alpha_i^k, the coefficients of the Lagrange basis form rows of V^(-1), equivalently columns of (V^T)^(-1). Bounding each row's l1 norm and then the Frobenius norm gives the stated sqrt(m) factor. The weaker K_V, W_b and G_b therefore cover the inverse, vector weights and individual residues without dropping a dimension factor.

The signed cyclic shift and Weyl shift are unitary with spectrum E={tau:tau^N=-1}. Since |tau|=1 and E is inversion-invariant, |1-alpha tau|=|tau^(-1)-alpha|. This proves the resolvent/nonpole relationship in the candidate; there is no missing |alpha| multiplier.

The binary-log scales are respectively O(N^3), O(N^6), O(N^6), O(N^7), O(N^7). Exponent notation is a compact way to specify enormous values, not a fixed-word arithmetic assumption.

### 3.4 Condition-number lower bound

The z^(m-2) coefficient is t_N plus a P_h coefficient of modulus at most 2^h. Vieta's bound therefore forces M^2>=(t_N-2^h)/binom(m,2). An entry in the last row gives sigma_max(V)>=M^(m-1). The constant row gives sigma_min(V)<=sqrt(m), using the transpose, whose singular values agree with V's even for complex matrices.

The stated lower bound follows. Uniformity can be made completely explicit: t_N-2^h>=2^(L-1), binom(m,2)<=N^2, log2 N<=N/2, and m-1=N/2 imply

log2 kappa_2(V) >= (N/4)(10N^3+1-N)-N/4
= (5/2)N^4-N^2/4 >= 2N^4.

This stronger conservative consequence holds for all even N>=4. It concerns the unscaled moment coordinates only. It does not lower-bound Fourier complexity, the condition of the final unitary operator, or other node families.

## 4. Certified root grid: termination, identity and completeness

All constants A_0,d_0,r,s are explicit positive dyadics. The nearest lattice point to each root is at complex distance at most s/sqrt(2)<=s and lies in the enumerated square: the root has modulus at most R and s<1. Every enumerated center has modulus at most 2R because R is much larger than 1+sqrt(2).

For a monic polynomial with all roots of modulus at most R, the l1 norm of its Taylor coefficient vector at w is at most product_i(1+|w-alpha_i|)<=(1+|w|+R)^m<=A_0. This justifies all three Taylor estimates in the candidate. In particular, the derivative perturbation is bounded using k<=m and e<=1, and the higher terms satisfy r^k<=r^2.

At a nearest-root center the true Rouché margin is at least

(d_0/2)r-d_0 r/64-d_0 r/16=27d_0r/64>d_0r/4.

Coefficient approximation and outward modulus bounds cannot consume that margin. For an explicit conservative interpretation, let E=theta A_0=zeta, bound the approximate moduli by rational intervals of width at most zeta, and inflate by E for Taylor-coefficient uncertainty. The total possible change in the two sides is at most 2(m+1)zeta<=d_0r/256, well below d_0r/16. This accounts for complex coefficients and the full vector dimension. A literal final-interval-width-at-most-zeta implementation may instead use theta/4 and modulus widths zeta/4; that changes precision by at most a constant number of bits.

At every center use only the prescribed finite precision. Accept only a strict outward-certified inequality; reject inconclusive cases. Thus an equality or unfavorable grid point cannot trigger infinite local refinement. Every nearest-root center will be accepted by this finite test unless its root already has a retained disk.

Each certified disk has exactly one root, strictly inside. If certified disks for two different roots intersected, the two root distances plus the center distance would give a root separation less than or equal to 4r, contradicting delta>=8r. Thus greedy overlap rejection cannot eliminate the last available disk for an unrepresented root. Once m pairwise disjoint disks are retained, they contain m different roots of a degree-m polynomial, proving completeness. An exact squared-distance comparison of dyadic centers decides disk intersection, including tangency.

A root is identified by the specified q embedding, B_N and its isolating disk. A radical formula or ordering oracle is not needed. Labels can be assigned in a deterministic grid-enumeration order for a single preparation. If a later precision request must retain previous labels, rerun at smaller radius and match disks by their unique shared root neighborhoods; separation makes the match unambiguous. Alternatively, prepare once at the final required accuracy. All bank statements are invariant under a common permutation of nodes and weights.

## 5. Bit model, weights and query precision

### 5.1 Preparation

The q-polynomial degree is at most n(n-1), since the exponent phase and product coefficient exponents are both nonnegative and their maximum sum is n(n-1). For |qhat-q|<=N^(-2), the telescoping power estimate includes the factor (1+u)^(N^2)<=e<3. Therefore the stated q precision suffices uniformly. The correct embedding is obtained directly from exp(2*pi*i/N), not guessed from a cyclotomic polynomial's roots.

Machin's formula, alternating-series remainders and Taylor remainders give rational enclosures in O(b_q+1) terms. The pi enclosure must be propagated through the argument 2*pi/N as well as through the sine/cosine remainder; allocating a constant extra number of bits suffices. Exact bisection supplies modulus and normalization square roots. These standard elementary procedures justify the bit model without trusting ordinary floating-point library functions.

The square's center count is bounded by (8R/s)^2. The logarithm of 1/s is at most p+O(N^7), because log2(d_0^(-1))=O(N^7), log2 A_0=O(N^4), and min in the radius becomes max in its exponent. There is no multiplication p*N^7 in that exponent bound. The candidate's polynomial arithmetic factor S_0^20 and storage S_0^10 are amply conservative for dyadic q formation, exact rational Taylor shifts, bisection, streamed grid counters and m retained disks. The total 2^[O(p+N^7)] preparation claim passes.

### 5.2 Weights and residues

The bound ||Vtilde-V||<=H_V e follows from the telescoping power identity and a Frobenius envelope. K_V H_V e<=1/4 gives ||Vtilde^(-1)||<=4K_V/3<=2K_V by a convergent Neumann series. Rearranging the exact rational linear system then gives (BW). Its vector dimension factors are conservative: ||c-ctilde||<=sqrt(m)u_c<=m u_c.

The prescribed e and u_c each spend at most v_b/4 in (BW). Reserve the other v_b/2 for rounding the whole beta vector, rather than spending v_b/2 on every component. For example, rounding each real and imaginary component within v_b/(4m) satisfies that vector budget. This costs only O(log m) extra bits.

The gamma bound uses the exact beta bound W_b and |alphatilde|<=2R. The two displayed terms spend at most v_g/4 each; round each real/imaginary residue within v_g/4 for the remaining complex-error budget. Exact rational elimination is implementable with pivoting and reduced fractions or fraction-free elimination; determinant/minor bounds ensure polynomial operand size. Deciding zero residues is unnecessary.

For a target precision p, every tolerance has binary logarithm p+O(N^7). Taking the minimum over all preparatory and application tolerances preserves this form. One may choose a dyadic accuracy below that minimum and perform one complete preparation, avoiding any ambiguity about cross-call node labels.

### 5.3 Application and relative error

The resolvent identity gives the exact perturbation bound 2e/rho^2 and the perturbed inverse norm 2/rho. Summing both residue and root contributions over all m branches gives (AB)<=eps/4; no individual branch conditioning is ignored.

The signed wrap equation is y_0+a y_(N-1)=x_0. Substituting the ordinary forward recurrence produces exactly the printed numerator x_0-a b and denominator 1+a^N. The independent tests include complex rational a, a=0 and |a|>1; changing this sign would fail them.

For endpoint perturbations, compare the approximate endpoints/normalizer against their exact versions while holding Ctilde fixed, then compare Ctilde with C. Using ||Ctilde||<=2N, endpoint norms <=2 and exact normalizer <=1, a telescoping expansion spends at most (8N+4N+2N)a_0<=16N a_0<=eps/4. The remaining exact-scaled bank error is at most eps/(4sqrt(N))<=eps/4. Hence the operator error before final rounding is at most eps/2.

For a nonzero dyadic input with b-bit numerators and denominators, ||x||>=2^(-b). Rounding all 2N real coordinates to absolute error eps*2^(-b)/(16N) has Euclidean norm at most eps*2^(-b)*sqrt(2N)/(16N)<=eps||x||/8. The final relative error is therefore below eps. The zero input is handled separately. Since Fhat is unitary, relative-to-input norm and relative-to-exact-output norm coincide.

The recurrence uses O(Nm)=O(N^2) rational operations, not fixed-cost machine operations. Its starting constants are dyadic with O(p+N^7) bits. Within a branch, dyadic denominators share a power-of-two common multiple, and division introduces only the branch denominator 1+a^N (or its complex norm when coordinates are rationalized). Summing m branches can multiply at most m such denominators. Reduced-fraction operand lengths are O(N^2(p+b+N^7)); they need not double at every loop iteration. Schoolbook rational arithmetic, including ordinary reduced-fraction gcd work, fits the stated O(N^6(p+b+N^7)^2) conservative bound. Query input/output traffic and final rounding are included; preparation remains a separate exponential cost.

## 6. Independent evidence

The fresh script `controls/independent_checks.py` ran successfully, without importing or executing the author's or inherited scripts.

- Reproduced all 35 author-reported successful finite-field cases and all 4 bad reductions, including the exact derivative/forbidden gcd degrees. Bad reductions remain bad reductions, not characteristic-zero counterexamples.
- Added successful legal-guard/moment cases for N=66,70,98,130,258, with every attempted reduction recorded.
- Checked 88,556 exact signed-shift/endpoint target entries for every even N from 4 through 80. This uses integer exponent congruences and includes wrap signs.
- Recomputed norm polynomials for N=4,6,8 by explicit multiplication over cyclotomic automorphisms, matching every author coefficient. Added N=10, norm degree 76, coefficient l1 norm 109326625612465225655310561685891344204345703125. This is a different norm construction from the author's resultant-over-q route.
- Verified symbolic reciprocal degree, leading coefficient, constant, discriminant and forbidden-resultant identities at N=4,6,8,10.
- Checked three genuinely complex Gaussian-rational Rouché disks at nearest dyadic grid points, with the full theta coefficient-error budget deliberately used. Rational squared comparisons certify all modulus intervals. Included no-root, repeated-root and oversized-disk negative controls and a greedy duplicate-disk completeness control.
- Verified 16 exact complex-rational signed-resolvent recurrences across N=4,6,8,12, including zero and large-modulus scalar nodes.
- Checked explicit exponent ledgers at 102 lengths through N=10000 and several p values as finite arithmetic controls. Uniform validity comes from the proof above, not these finite values.

No full instance of the candidate's astronomical exhaustive grid was run. No production floating-point program, timing claim or end-to-end numerical implementation is certified. The controls corroborate the algebra and selected certificate mechanics; they are not substitutes for the all-N proof.

## 7. Existing-row action and stopping scope

Apply only the scoped acceptance described in `EXISTING_ROW_PROPOSAL.json`, if the parent chooses to update the existing workflow. Do not create a new fusion row. Preserve Q20's accepted h+1 existence result and its open h/t=1 questions. Preserve Q08's fixed-degree boundary and separate useful growing-degree conditioning from this intentionally poor explicit envelope.

The next research question remains an explicit substantially better-conditioned legal family with practical certified preparation. This review creates no Sheet or GitHub mutation and grants no publication-priority conclusion.
