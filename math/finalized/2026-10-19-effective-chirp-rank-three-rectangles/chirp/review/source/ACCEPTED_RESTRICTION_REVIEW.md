# Independent review: principal restriction and infinite chirp subfamily

## Verdict

**Accept the principal-restriction theorem, the exact restricted chirp family, the non-effective positive-sign generic exclusion, and the explicit infinite square-modulus exclusion, conditional only on the separately sealed N5 certificate already independently accepted.** In particular, for q odd, gcd(q,5)=1 and q≡1 modulo241, the forced chirp B_(5q²) has no representation as two Hamiltonian-cycle Green terms with arbitrary diagonal endpoint masks and legal Green denominators. The explicit sequence q=2410k+1 is valid.

This is an infinite representation obstruction for that forced feedback B. It does not exclude general Fourier algorithms, different choices of feedback A, products of Green sums, extra terms, or unmatched monomial endpoints. The generic positive-sign statement has a finite but uncomputed algebraic exceptional set and no explicit cutoff. No negative-sign generic conclusion is accepted without a separate anchor.

## Source snapshots

The final construction report is `source/FINAL_INFINITE_CHIRP_EXCLUSION.md`, SHA-256 5ad4fe5f6777685113509427cd0371d3e1b856e8cda2858c89b9a06b72ebdd12; its 19-file manifest was independently checked by reading hashes. The final report focuses on the explicit infinite family and makes no claim to compute a generic eliminant. This review additionally audits the preserved preceding draft’s positive-sign generic-curve corollary in Section3 below; it is not silently attributed to the final theorem. Both snapshots are preserved, and neither codebase is executed.

## 1. Restriction proof, including degeneracies

For row action (Wx)_i=w_i x_sigma(i), a Hamiltonian cycle satisfies W^N=rho I, rho=product w. Its inverse is (I+...+W^(N−1))/(1−rho). For a nonempty selected set S, the successive selected-to-selected arcs partition all original edges. Define the induced Hamiltonian order and each effective edge as the product on its arc. Their total product remains rho.

Between distinct selected vertices there is a unique original path of length below N; its weight equals the product of the corresponding induced arcs. The diagonal numerator is one in both inverses. Hence the principal submatrix is exactly the induced Green inverse, in the displayed ordering of S. For a singleton, the induced loop weight is rho and the equality is still 1/(1−rho). This proof has no division by any individual weight, so arbitrarily many zero edges remain valid. The effective guard is exactly the original guard.

Diagonal endpoints restrict entrywise, including zero masks. A sum of two branches therefore restricts to two allowed branches with possibly different induced orders. All induced five-cycles lie in the complete 24-by-24 universe of the preceding N5 audit. Unmatched row/column endpoint permutations do not satisfy this principal-restriction inheritance automatically.

## 2. Exact five-coordinate target

For odd N=5m, gcd(m,5)=1, take S={0,m,2m,3m,4m}, h=(N+1)/2, eta=omega^(m²), and G=G_N. Eta has exact order five and h≡3 modulo5. Direct substitution in the previously verified chirp resolvent gives

B_N[S,S] = [F(eta)−G C(eta)+NG D(eta)]/(1+NG),

with F_ab=eta^(ab), C_ab=eta^(−3(a+b)²), D_ab=eta^(−3a²)delta_ab. The three matrices are linearly independent: off-diagonal C/F ratios at (0,1) and (0,2) are distinct eta² and eta³, and D has diagonal support. Thus this block is not B5 for N>5 in characteristic zero; incorrectly identifying it with B5 would invalidate the extension. The source correctly retains the scalar family.

## 3. Gauss-sign scalar curve and generic statement

For every primitive complex additive character of odd modulus N, G_N²=epsilon_N N, epsilon_N=(−1)^((N−1)/2). The product with the opposite Gauss sum equals N by the invertible change of variables x−y,x+y. The opposite sum is epsilon_N times the original by the Jacobi-character formula. The latter was verified in the primary [Gurevich–Hadani–Howe paper, equation 3.3 and Remark 3.3](https://arxiv.org/html/0808.2447). It applies to composite odd moduli and arbitrary primitive characters, not only primes or one selected square-root sign.

Writing g=G_N gives the numerator curve H_(eta,epsilon)(g)=F−gC+epsilon*g³D. The denominator is 1+epsilon*g³. For actual complex N>=5 its magnitude cannot vanish because |NG_N|=N sqrt(N)>1. General symbolic/finite parameters need their own denominator check.

On the positive-sign curve, the joint off-support equations and all maximal augmented minors from the N5 audit are polynomial in g and multihomogeneous in ten projective direction pairs. The closed family in A1_g times (P1)^10 projects properly to A1. Its image is closed. At g0=G5(eta), g0²=5, the numerator is (1+5g0)B5; nonzero scalar multiplication of a target multiplies each off-support equation and each augmented minor by that scalar, so it preserves emptiness. The N5 exclusion therefore makes the image a proper closed subset of the line, hence finite. The union over 576 order pairs is finite, and the four possible eta embeddings give another finite union.

Consequently only finitely many odd N=5m with gcd(m,5)=1 and N≡1 modulo4 can evade this necessary principal-block obstruction, since |G_N| tends to infinity. This is a rigorous non-effective finite-exception conclusion. The elimination ideals exist, but no expanded eliminant, actual exceptional list or numerical cutoff has been computed. The proof uses [properness of projective morphisms](https://stacks.math.columbia.edu/tag/01WC), already independently checked for the N5 lift.

## 4. Explicit square-modulus CRT identity

For N=5q² with odd q coprime to5, every residue has a unique representation x=q²u+5v, u modulo5 and v modulo q². The cross term in h x² is a multiple of N. Thus

G_N = G5(eta) * sum_(v modulo q²) xi^(5h v²),

where eta=omega^(q⁴), xi=omega^5. In the second sum, write v=s+qt. Because xi has exact order q² and 2*5h is a unit modulo q, the inner t-sum vanishes unless s=0, where it equals q. Therefore G_N=q G5(eta), with no guessed sign, square-root convention, or assumption that q is prime. This is valid for every primitive supplied omega.

The actual block is consequently

C_q(eta)=[F−q g5 C+5q³ g5 D]/(1+5q³ g5), g5=G5(eta).

In particular its coefficients lie in the degree-four field Q(eta) before any reduction is attempted.

## 5. Arithmetic specialization and endpoint scope

For q≡1 modulo241, reduce Q(eta) at eta=91. Then q*g5=103, 5q³*g5=33, and the denominator is the unit34. The reduced target block is exactly the independently certified N5 target. The same closed projective necessary system therefore has empty geometric special fiber. Proper specialization, exactly as in the accepted N5 audit, excludes a characteristic-zero point, including singular-endpoint limits.

There is no illicit loss of root order here. Since 241 does not divide N, a primitive Nth root cannot simply reduce to a fifth root. The proof instead first places the restricted coefficients in Q(eta); q reduces to1 as an integer. If one works in the ambient cyclotomic field, a prime above the chosen coefficient-field prime has an appropriate residue-field extension and the primitive omega retains exact Nth order. No ambient root collapse is used or needed.

Any permitted full B_N representation would restrict to a forbidden C_q representation, by Section1. Hence the explicit infinite exclusion follows. q=2410k+1 satisfies all guards for every k>=0. The first nontrivial member of that particular simple sequence has q=2411 and N=29,064,605; no matrix of that size is constructed by this certificate. Smaller valid q can be chosen under the more general congruence statement, but the proof requires no search for them.

## 6. Independent controls

Our fresh standalone standard-library checker passes 3,906 principal restrictions, checking 67,869 entries, including reordered selected sets, singleton/full subsets, nonzero/some-zero/all-zero weights and singular endpoint masks. It also checks 72 invalid guard preservations. Fifty-seven exact Gauss-sign controls cover both signs, composite moduli and nonstandard primitive roots. Eight selected five-coordinate blocks are checked; 3,500 entries additionally agree with direct forced inverses. Twenty-four full square-CRT Gauss sums and residue bijections cover q=1,3,7,9,11,13,17,21. Every one of the 25 target entries is symbolically reduced modulo q−1 at p241, with denominator34.

These exact finite controls supplement the proofs. They do not infer complex statements from bare modular equality, nor claim an all-size application algorithm. The proper projective N5 certificate is the essential characteristic-zero exclusion input; its immutable independent seal is retained separately.

The source report and metadata are snapshotted inert. No constructor or uploaded code was imported or executed. Portable replay and file seals accompany this review.
