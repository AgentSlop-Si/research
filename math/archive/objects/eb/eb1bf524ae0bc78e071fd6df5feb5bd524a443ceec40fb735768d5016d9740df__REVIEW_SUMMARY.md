# Independent Phase39 N16 exhaustive acceptance

10 October 2026. The fixed seven-Green N16 exclusion is accepted. This closes the earlier sample-only N16 obligation in Q26/S17 without changing any prior freeze. It adds no N16 quartic exhaustiveness or all-N conclusion.

The accepted source theorem is `masks/n16_supplement/N16_THEOREM_AND_CERTIFICATE.md`, SHA-256 `a4205d74030c7c86d8a16fee6fd6f3cb36cbeb2c66b7022709b58960de23185d`. The source programs were inspected only as text; none was executed, imported, compiled, or AST-parsed. This reviewer independently authored and compiled `reviewer_n16.cpp`, which uses six nested distinct-index loops rather than the owner's unranking stream. It checks only the fixed first-ten-row determinant, with an independently written product/lift routine and Gaussian determinant calculation.

Both exhaustive reviewer runs finish successfully:

- p=998244353: all10,483,200 mappings; every fixed minor nonzero; determinant product656557892.
- p=2013265921: all10,483,200 mappings; every fixed minor nonzero; determinant product86141027.

These exactly match the two owner's independently generated streams. No minor fallback, random sampling, early-success termination, or hidden mapping exclusion occurs. The six loops enumerate 16·15·16·15·14·13 mappings bijectively. The checked minor has ten columns and rows0 through9 of the prescribed four-quadratic cubic lift. Exact signed64-bit products are safe for both moduli; each product is reduced before sums. A planted exact pencil target, with known root(1,7,11), fails immediately on the first mapping, as required, so the verifier is not an always-success control.

Input matrices were independently rebuilt again from the stored integer cycle lists and displayed rational couplings using direct Green path sums. Every T and pencil entry equals the included data in both primes. The reviewer checks primality by complete trial division, root orders and generator conditions, i=zeta16^4, all Green denominators, and outer inverses. Both detA and detC match the displayed nonzero residues. The input text hashes match908e72cdd117983e6da8c979f2a2fb6e3ca15e4c11ab53ef43b809a0f5a7d3fe and7cfb3d8bd9f199ccde2ee54e8cfde5f8307deebbb5ecce24634095e768a0d92c.

The proof implication is the already accepted homogeneous-Macaulay certificate: a nonzero maximal cubic minor makes every cubic monomial a row-span combination, excluding any nonzero projective common root over the algebraic closure. The selected minor is a rational cyclotomic expression with all inverted quantities units under the valid split reduction. Nonzero reduction proves characteristic-zero nonvanishing. Every full permutation pair induces one of the exhaustively excluded local mappings. Thus no specified two-mask/two-permutation factorization exists over C for any nonzero middle projective coefficient triple. Either prime alone suffices mathematically; the second is redundant arithmetic verification.

The simultaneous generic fixed-order N4/N8/N16 openness corollary is also accepted: multiply the finitely many determinant numerators and denominator guards, all nonzero at the common displayed nine-scalar specialization. The resulting nonempty Zariski-open set is within that fixed-order parameter family. It does not classify the exceptional locus or change cycle orders freely.

Remaining limitations: no exhaustive N16 quartic statement; N32/larger sampled records retain their sample-only status; Phase38 and Phase39 are distinct; Q27's actual Fourier target fiber remains open; no universal cycle architecture, unrestricted FFT lower bound, FFT construction, implementation speed or worldwide priority claim follows. Existing theorem-level priority comparisons remain provisional.
