# Bounded prior-art comparison: two precise hypothesis checks

Verified 19 October 2026. **Cited comparisons confirmed, with limits. Historical novelty remains unresolved.**

This audit independently checked the decisive passages in accessible source texts. It checks attribution and applicability, not the correctness of the two supplied mathematical results. It does not repeat the earlier broad literature searches or certify historical priority. The accompanying JSON contains 11 stable-ID comparison cards and five explicit unread-source gaps.

## 1. Exact statements under comparison

### Binary masks with prescribed Fourier phases

Let q>3 be prime, N=3q, ζ a primitive N-th root, and R an N×N binary matrix. The target is the classification of positive integers d for which

D[r,c]=R[r,c]ζ^(rc),  D*D=dI,

namely d∈{1,3,q,3q}. The phases are fixed at each position. The claim concerns attainable degrees, not classification of every support pattern, all semiprimes, or unrestricted weighing matrices.

### Continuous q-Hermite at primitive prime-power roots

The supplied target concerns P_n(X;q)=H_n(X/2|q), with P_0=1, P_1=X and P_(n+1)=XP_n−(1−q^n)P_(n−1), and the corresponding Gaussian Rogers–Szegő family. Here p is odd, q has exact order p^s, and the combined squarefreeness range is 0≤n<min(3p,p^s). The additional third-block degrees are 2p<n<3p for s≥2; n=2p was an earlier boundary input.

The local calculations take place in K=Q_p(q), normalized by v(q−1)=1. The comparison concerns the family-specific residual expansions and root distances, and the resulting **ordinary** polynomial discriminant valuation. Neither the polynomial family nor general Newton, Hensel, or discriminant theory is claimed as new.

## 2. Fourier comparison: confirmed distinctions

The cancellation ingredient is established prior work. Lam–Leung’s Theorem 3.3 and Corollary 3.4 give the two-prime cycle structure and explicitly credit earlier work of de Bruijn. Applying this to binary overlap supports does not identify their cardinality with the full row degree. [Lam–Leung, pp. 7–8](https://arxiv.org/pdf/math/9511209v1).

The spectral-set comparison is genuine but conditional: Malikiosis–Kolountzakis require characters orthogonal on one common set. Their theorem gives divisor cardinalities at order 3q. A general entry mask instead has row-pair-dependent intersections, so an additional reduction is needed. [Theorem 1.2 and §2](https://arxiv.org/pdf/1612.01328v2).

Herr–Wiegand likewise retain all entries in a Cartesian selection J×K. Their primitive-set results do not themselves quantify over arbitrary binary entry masks. [Definition 1.1 and Theorems 2.1, 2.6](https://arxiv.org/pdf/1909.13145v4).

The broader complex weighing-matrix class permits nondivisor weights: Egan’s displayed order-5, weight-4 cubic-root example and direct-sum rule give order 15, weight 4. This supports the distinction between free phases and prescribed Fourier phases. Egan is a later survey reproducing a construction attributed to Berman. [Example 3.5 and Proposition 3.11](https://arxiv.org/pdf/2309.07522v2).

**Disposition:** the global compatibility argument for arbitrary fixed-phase masks is the item requiring further attribution checking. These source mismatches do not prove that an undiscovered structural reduction or another result cannot imply the classification.

## 3. q-Hermite comparison: confirmed distinctions

The terminal identity H_N=2T_N and the complete-N-block factorization apply when N=ord(q). At the target degrees n<N, that factorization leaves H_n unchanged. [Atakishiyeva–Atakishiyev–Koornwinder, (2.7)–(2.8)](https://arxiv.org/pdf/0811.4100v2).

Spiridonov–Zhedanov explicitly distinguish positive real recurrence theory from complex coefficients. Their degree-N zero formula and simplicity condition occur in (2.4)–(2.10); Theorem 1 gives orthogonality weights. It should not be described as a lower-degree simplicity theorem. [Askey–Wilson paper](https://arxiv.org/pdf/q-alg/9605034v2).

Their positive q-ultraspherical systems have a different recurrence and restricted real parameters. Those positivity hypotheses do not directly include the continuous q-Hermite degeneration at unit-modulus q. [q-Ultraspherical paper, (1)–(6)](https://arxiv.org/pdf/q-alg/9605033v1).

Ismail–Witte’s explicit Rogers–Szegő product (5.17) is a q-discriminant. Its nonvanishing does not certify ordinary squarefreeness. The paper also treats ordinary and generalized discriminants; the mismatch applies to the cited product, not to every topic in the paper. [Definitions (1.7)–(1.9), normalization (4.20), and (5.13)–(5.17)](https://arxiv.org/pdf/math/0012259v2).

The local consequences are established tools. Once the relevant primitive Newton side exists, irreducibility follows from Corollary 1.16. Once the integral residual with simple roots exists, Hensel lifting applies. Neither reference establishes the family-specific input. [Guàrdia–Montes–Nart](https://arxiv.org/pdf/0807.2620v2); [Conrad’s expository notes, Theorems 9.1–9.2](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf).

For the squarefree third-block polynomials, the cluster discriminant formula is applicable and uses established root-distance bookkeeping. The first formula in Theorem 16.2 does not require semistability. Its separate minimal-model formula does, with an additional residue-field-size hypothesis; no minimal-model conclusion is invoked here. [Dokchitser–Dokchitser–Maistret–Morgan, §16](https://link.springer.com/article/10.1007/s00208-021-02319-y).

**Disposition:** the possible family-specific contribution is the explicit residual/valuation calculation and the root configuration it establishes. No historical novelty claim follows merely because these cited passages do not supply that calculation.

## 4. Publication safeguards and remaining gaps

Use: “No directly subsuming result was found in the inspected statements.” Avoid “first,” “previously unknown,” “the existing literature cannot imply this,” or a claim that all degrees below the root order have been covered.

Preserve the following qualifications:

- A non-Cartesian fixed-Fourier example at order 8 can refute a universal block-decomposition assertion. It cannot rule out a special order-3q reduction.
- References to the “additional” or “third-block” work describe the scope of the supplied results, not historical priority.
- Irreducibility and discriminant consequences are conditional on the established side or cluster picture. They are not replacement proofs of the family-specific estimates.
- A source opened for a few pertinent passages has not thereby been exhaustively excluded.

Five originals remain unread in this audit: de Bruijn (1953), Berman (1978), Bond–Glickfield–Herr (2019), Zhedanov’s *Gauss sums and orthogonal polynomials* (1997), and Ismail’s *Difference equations and quantized discriminants for q-orthogonal polynomials* (2003). The first four are identified through inspected later references or the preceding comparison; the last was previously located through its publisher record. Earlier retrieval failures are evidence of a coverage limit, not evidence of absence. Full details and links are in the JSON gap records.

Other adjacent papers screened in the preceding searches were not independently re-audited here. Equivalent formulations, unindexed work, historical books, and results requiring an additional reduction remain outside any claim of exhaustion.

## 5. Safe release boundary

The accompanying files contain original summaries, limited mathematical comparison, source locators, and public bibliographic links. They contain no downloaded full papers, extensive quotations, private native-document identifiers, owner data, or executable table mutations. No external write or publication was performed.
