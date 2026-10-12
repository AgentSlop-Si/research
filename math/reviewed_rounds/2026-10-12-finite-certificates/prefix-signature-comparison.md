Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted. Mathematical assumptions, classical attribution, evidence depth and remaining work are retained. Original source-report SHA-256: ae11e20fca0d89595b233c854b64808e6410d54c2a619d5014c11f4106e41179.

# Independent review of the uniform target factorization comparison

12 October 2026 UTC. Verdict: **ACCEPT as a bounded implication comparison.** No mathematical repair is required. This review neither reopens the accepted PREFIX certificates nor closes a historical-priority gate.

The archive reviewed is `Prefix_Uniform_Target_Factorization_Comparison_2026-10-12.zip`, SHA-256 `3a1a5d18045ff3f84229caa168c697a408f0188459c07336dee3acc81cfdbda3`. All eight archive members match the corresponding local packet files; all seven manifest payload hashes and all sixteen inherited input fingerprints verify. The accepted uniform theorem remains a dependency, not a theorem proved by the present small controls.

## Main finding

For every prime r ≥ 5, the two displayed signatures are genuine unique-product signatures of the same group D8 × C3 × Cr and the same ordered type (2,2,2,3,r), with minimum length r + 9. Under the specified last-coordinate-fast flattening, their scores are respectively 76r − 24 and 70r − 24, and their generated proper-prefix stabilizers are respectively C4 × C3 × Cr and the whole group. This is a symbolic family argument, not extrapolation from small primes.

The separation refutes precisely the assertion that group, minimum signature length and ordered block type determine fixed-decoder prefix optimality or full escape. It does not exclude more informative reductions or establish historical novelty. Fresh primary-body text supports the report's CHS01 and Sands08 hypothesis distinctions. EFK remains partially read through inherited evidence, with its remaining body and equality comparison open.

## Definitions and symbolic verification

Use left translation throughout. For an order x of N elements, let T_j be its first j elements, S_j its setwise stabilizer, Z(x) = Σ from j = 1 to N of (|S_j| − 1), and B(x) = ⟨S_j : 1 ≤ j < N⟩. Since S_N = G, the equivalent identity Z(x) = Σ from j = 1 to N − 1 of |S_j| is valid. The empty prefix is absent and the full prefix is excluded from B. Changing either convention would invalidate this comparison.

Write D8 = ⟨u,v : u⁴ = v² = 1, vu = u⁻¹v⟩. With products evaluated from left to right and the last coordinate varying fastest, the signatures are

- α_D = ([1,v],[1,u],[1,u²]);
- β_D = ([1,u²],[1,u],[1,v]).

For α_D, the products are v^a u^(b+2d), where a,b,d are binary. The reflection parity determines a, and b+2d runs bijectively over the four rotation exponents. For β_D, the products are u^(2a+b)v^d, again a bijection. No commutation or block-permutation theorem for nonabelian signatures has been assumed.

The resulting orders are

- α_D: (1,u²,u,u³,v,u²v,u³v,uv);
- β_D: (1,v,u,uv,u²,u²v,u³,u³v).

A stabilizer acts freely on its prefix, so its order divides the prefix size and 8. Odd proper prefixes therefore have trivial stabilizer. The even proper stabilizers for α_D are ⟨u²⟩, ⟨u⟩ and ⟨u²⟩, at sizes 2,4,6. For β_D they are ⟨v⟩, ⟨uv⟩ and ⟨u²v⟩. In particular, the fourth β_D prefix is not a subgroup: it has size four and stabilizer of size two. The sixth-prefix assertion also follows from the complement of {u³,u³v}. Thus Z(α_D) = 12, B(α_D) = ⟨u⟩, Z(β_D) = 10 and B(β_D) = D8. The latter follows already from v and uv generating D8.

Let K = C3 × Cr, with generators c,t, and append ([1,c,c²],[1,t,…,t^(r−1)]) to each D8 signature. Central direct-product coordinates give uniqueness on G immediately. Both signatures have length 2+2+2+3+r = r+9. The prime-factor lower bound for |G| = 2³·3·r is exactly r+9. The minimum-length assertion is therefore exact.

### Product identity

For a fibre order on H × K, let n = |H| and m = |K|. Write a proper-prefix position as j = qm+s. If 0 < s < m, the fibre over the next H element is the unique fibre with intermediate cardinality. Any stabilizing left translation must fix that H element, so its H component is the identity. Its K component is exactly a stabilizer of the inner s-prefix. If s = 0 and 1 ≤ q < n, the stabilizer is S_q(H) × K. These assertions do not need commutativity of H or K.

Summing proper-prefix stabilizer sizes gives

Z(H × K, fibre order) = n Z(K, inner order) + m Z(H, outer order).

The first complete fibre is still a proper prefix because n > 1; it supplies the full K factor to B. All proper checkpoint projections supply exactly the outer proper-prefix stabilizers, and intermediate positions supply no H projection. Consequently B = B(H, outer order) × K. This also verifies both inclusions, rather than only exhibiting generators.

For the displayed K order, the two completed Cr checkpoints have stabilizer Cr, and the 3(r−1) other proper prefixes have trivial stabilizer. Hence Z_K = 2r + 3(r−1) = 5r−3. With n = 8 and m = 3r, the product identity proves

Z(α) = 8(5r−3) + 3r·12 = 76r−24;
Z(β) = 8(5r−3) + 3r·10 = 70r−24.

Also B(α) = ⟨u⟩ × K, of order 12r and index two in G, whereas B(β) = G. The score gap is 6r > 0. None of these calculations uses the uniform optimum theorem. Identifying α as an unrestricted optimizer and β as a full-escape optimizer does use the accepted theorem, correctly bound by the candidate.

## Relation to the accepted result

The accepted statement hash `160249458b37b8940e28d983054587ddcd1c39e90fcb54871f3e7b7d4ae2994a` and acceptance archive hash `e7c6b2feb2d5d044fccfce0dbcd854820e17fc5585921f83db4323ba0c15de21` verify unchanged. The original author theorem hash remains `3a5fd5e8b3dae6a854d65b3e523e86d3927a8b316db322241e884446d7a158a1`.

Retain the accepted sharp full-escape maximum, the unrestricted maximum and the complete unrestricted recursive maximal-subgroup right-coset classification. Retain the labeled count recurrence with coefficients 2,4,6 and r!, counting actual subgroups and actual element orders. There is no additional representative multiplier, translation quotient or automorphism quotient. The comparison does not classify or count all full-escape maximizers. The remaining distinct-odd-prime family after the accepted p = 3 slice is 5 ≤ p < r.

No graph search, affine-invariant state check, completed finite-case certificate or optimizer-count enumeration was rerun. The fresh controls use D8 as permutations of four points and verify only the two new signature orders, the normal-subset obstruction, exact affine coefficient arithmetic and source integrity.

## Primary source audit

### GVS03 and BDW11

[González Vasco, Rötteler and Steinwandt, 2003](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/On-Minimal-Length-Factorizations-of-Finite-Groups.pdf), Definition 2.1 and Remark 2.2 on PDF page 2, define ordered unique-product signatures and their sum-of-block-sizes length, with the prime-factor lower bound. Proposition 3.1 on page 3 supplies solvable-group attainment by composition-series transversals. The witnesses satisfy that general definition directly. This source's existence/length result does not impose the prefix objective.

[Baumeister and de Wiljes, 2011 preprint](https://arxiv.org/pdf/1104.4503), page 2, uses a first-coordinate-fast mixed-radix decoder. Its cover convention also imposes polynomial length in the logarithm of group size. The candidate explicitly uses the general GVS03 signature definition; it must not additionally claim the length r+9 family is a uniformly polylogarithmic cryptographic cover. Algorithm 5.2 and Theorem 5.4 on page 6 require abelian G and every chosen combination of local blocks to be a signature of U. Remark 5.5 includes the degenerate U=G construction. Theorems 5.11 and 5.15 on pages 8–9 impose their respective subgroup and non-proper-translate hypotheses for individual factor periods. These distinctions are correctly respected. The polynomial-length clarification is useful source hygiene, not a repair of the comparison.

### CHS01

[Corrádi, Hermann and Szabó, 2001](https://acta.hu/download.phtml?id=2624), printed page 530, defines F-simulation using an equal-size subgroup in a Fitting class containing abelian groups and overlap greater than (p+1)|A|/(2p). The stricter threshold is |A|−δ, where δ is 2 for even size and p−1 otherwise. Theorem 1 on pages 532–533 requires normalized, conjugation-invariant factor subsets; prime-size or simulated factors yield the Fitting-class conclusion, and the stricter condition yields normal-subgroup partial products after a suitable factor reordering. Lemma 3 on page 531 forces abelianness when all normalized normal factors have prime size.

Here uvu⁻¹ = u²v is absent from {1,v}, so the normal-subset premise fails. More generally, Lemma 3 precludes applying its all-prime normal-factor premise to this nonabelian G. Even the inherited abelian C24 witness satisfies the hypotheses while separating fixed flattenings. That witness establishes a decoder mismatch, not a counterexample to CHS01. The candidate's distinction is valid.

### Sands08

[Sands, 2008](https://ieja.net/files/papers/volume-3/Volume-3--2008/5-V3-2008.pdf), printed page 84, globally restricts groups to finite abelian groups and normalizes factors. Theorem 1, pages 86–87, requires a direct product of cyclic or simulated nonsubgroup subsets that is a direct factor of prime index. It recovers a unique normalized complementary factor, a prime-order subgroup generated by a successor or distortion element. The proof and global conventions substantiate the candidate's reading.

The target G is nonabelian. Independently, the inherited C24 example concerns A={0,…,7}, formed as the direct sum of the three cyclic nonsubgroup factors {0,4},{0,2},{0,1}; its index is three. Its Sands complement {0,8,16} differs from the trivial B of the natural flattened element order. Thus the two subgroup-recovery objects genuinely differ. No historical novelty follows merely from that difference.

### Rendering limit

The fresh selected primary text was readable. The CHS screenshot produced a reference without an image payload available for inspection, and the Sands screenshot failed. This review therefore makes no new rendered-page verification claim and supplies no invented PDF byte hashes. Full third-party texts are not redistributed.

## EFK and the remaining gate

The EFK reading remains inherited, not freshly verified against a complete primary body in this review. The pinned earlier audit credits Theorem 2.1's statement and principal incidence double count at printed page 325, the allowed empty-base specialization at page 326, and Theorem 5.1 and proof at page 331. Its source ledger also records the Section 4 opening and a Theorem 6.1 excerpt. Do not revert to describing Theorem 2.1 as wholly unread.

The unresolved targets remain the complete definitions and Lemma 2.1 around page 324, most of Section 4 around pages 328–330, Proposition 5.1's proof, the complete Corollary 6.1 and Section 6 ending, and full rendered-page inspection. These are source/equality-comparison gaps, not defects in the independently accepted PREFIX theorem. EFK is the 1992 article; the publisher's later online date does not replace its publication year. The [publisher DOI](https://doi.org/10.1017/S0963548300000377) remains the source reference.

The candidate correctly labels the empty-base reduction as its own tested substitution into the inherited conditional theorem. With A₀ empty, A_j=T_j and F={T₁,…,T_(N−1)}, only equal-rank incidences occur and the resulting loading is Σ_(j<N)|S_j|=Z. The two new orders give loadings 76r−24 and 70r−24, both greater than N=24r for every prime r≥5. Thus the needed budget fails. The empty-base specialization itself is not forbidden. This invalidates that direct substitution only; another incidence construction remains possible.

The separate threshold identity is also correct. For d_i=(1,1,2,4), e_b=(1,2) and f_c=(1,r−1), the weighted sum over thresholds below the prime valuations of |S_j| telescopes to |S_j|. Removing the zero threshold gives |S_j|−1. Summing over all j, including N, yields the displayed Z identity. Each threshold requires its divisor 2^i3^b r^c to divide j, so its count is at most N/(2^i3^b r^c). The sum of those individual caps is 176r−100. The weighted deficit Δ is therefore exactly 176r−100−Z, and recovering the accepted bounds requires Δ≥100r−76, or Δ≥106r−76 under B=G. Separate rank caps establish only Δ≥0. This is a valid quantified missing step, not an attribution of an unproved compatibility inequality to EFK.

The remaining primary EFK body and equality-comparison obligations remain open.

## Scope and remaining work

The bounded implication comparison is accepted. All previously accepted PREFIX mathematics and original empty/full-prefix conventions are preserved. It adds no worldwide-priority finding or general-family extension.

Accepted conclusion:

“Accepted uniform p=3 theorem on D8 × C3 × Cr for every prime r≥5. A verified same-group, same ordered-type minimum-length-signature pair has scores 76r−24 and 70r−24 under one specified flattening, with proper B and B=G respectively. This separates signature length/type from prefix optimality; CHS01 and Sands08 have verified hypothesis/object mismatches. No exact classical derivation was established by this bounded comparison. EFK Theorem 2.1 is partially read, but remaining-body/equality coverage and worldwide priority remain unresolved.”

Retain attribution of transversal constructions, compatible local branching and factorial/product counting. “Not supplied by the inspected statements” must not be upgraded to “absent from the literature.” The next source task is the named missing primary EFK pages and an explicit incidence/equality reduction, not more undirected keyword searching.

## Trust boundary

This is independent project review, not external peer review or formal proof-assistant certification. The reviewer inspected source text, proved the product and score identities symbolically, and wrote fresh comparison-only controls. The complete sealed review archive is preserved separately and contains research inputs and bounded source metadata, with no third-party full texts.
