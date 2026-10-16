# Independent review of rectangle cost and monomial centralizer gates

16 October 2026 UTC. Source baseline: `0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4` in AgentSlop-Si/research.

## Decisions

**ACCEPT** the mathematical comparisons and the exact 23-cell proposal with SHA-256 `4ace65a86e5c33f39812bd3ca9b868e258786b2e0fb778564e5e66ad4c7b9e08`. All 23 preimages match fresh independent native CellData; six stable-ID row bindings and four action/stop mirror groups agree. Twenty-two updates retain the complete prior string after an explicit history marker. Only overview E68 changes status. This acceptance is a review outcome, not an external-write receipt; eventual application requires a fresh unchanged-preimage check.

- **M-RECTANGLE-TILING:** finish the named endpoint-incidence comparison as a bounded qualified nonmatch. Keep the parent **TO RESEARCH**, priority 42. Its owner expressly retains the higher-rank incidence optimum for general nonsquare composite lengths.
- **ALG-MONOMIAL-CENTRALIZER:** the owned classification/comparison record is eligible for **CLOSED**, priority 42 unchanged. The complex theorem is a consequence of the primary full monomial stabilizer classification after scalar normalization and equal-side specialization. The primitive-root arbitrary-field statement retains its accepted algebraic proof; it is not claimed as the literal field domain of the complex primary theorem.

Neither decision establishes historical originality, a faster FFT, finite-word stability, production readiness, or closure of adjacent gauge/architecture records. The second owner excludes the full dense commutant, unrelated gauges, free routing and unrestricted runtime conclusions; it does not promise those as successors. These exclusions therefore do not keep its completed monomial record open.

## Independently checked sources and ownership

Fresh native reads established the stable-ID bindings in Research overview rows 93 and 68, Catalogue rows 50 and 26, and novelity breakthough rows 76 and 51. The operative stop condition permits an exact primary-theorem hypothesis/formula/cost mapping, or a qualified nonmatch or specific access blocker. It does not require global novelty clearance.

The retrieved Phase7 rectangle audit is 8,943 bytes, SHA-256 `ed3a259cc88ecb2cf12092f612aabaeb917885fe84147cf2feb99802d1fd32c4`, Git blob `58be131bc82c3ccc7dfb15b435d01bd9edd17942`. The historical `795e4df8...` identity in its filename is not its sanitized repository-byte hash. The retrieved Phase16 audit is 15,593 bytes, SHA-256 `6b83dab44ee74f9cd3c905a2b16b78d38a208a7ed5efffcc4430428e098cd88a`, Git blob `280fb6351d66981fe27181f9baec69c587090e85`. Both complete relevant proof bodies were independently read and the returned Git blob identities were recomputed from the bytes.

The existing Delvaux–Van Barel Lemma 11 subgroup-block construction comparison was already recorded. This review does not present it as new progress. The public source [TW477](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW477.pdf) was independently inspected; its title is *Rank-deficient submatrices of Kronecker products of Fourier matrices*. The present new comparison concerns the endpoint objective and its feasible class.

## Rectangle endpoint comparison

[Alman–Guan–Padaki, *Smaller Low-Depth Circuits for Kronecker Powers*, v1](https://arxiv.org/pdf/2211.05217v1), section 1 and equation (1.1), defines synchronous linear-circuit size as the sum of nonzeros in its sparse matrix factors. In depth two this is a sum of outer products with cost equal to the total support sizes of the two vectors. Theorem 1.4 gives an exponent below 1.5 for powers of any fixed square matrix; Theorem 1.6 gives exponent 1.443 for Walsh–Hadamard matrices. These are circuit upper bounds with arbitrary field coefficients. They are not exact disjoint-rectangle optimization theorems.

Here is the independently checked map. Extending each rank-one Fourier tile by zero produces one outer product, with exactly a+b nonzero factor entries for an a-by-b tile. Thus the endpoint objective agrees with wire count for this particular implementation. The converse fails: a general outer-product decomposition may overlap and cancel, and a summand need not equal the restriction of the target on its support. Consequently a minimum over all such factorizations is at most the tiling minimum, and a tiling lower bound gives no general circuit lower bound.

The target domain also matters. A fixed-base tensor Fourier power has a product indexing group, whereas cyclic F_(q^n) has the cyclic indexing group. They must not be silently identified. The Walsh–Hadamard construction is useful evidence that the broader character-table circuit model permits savings, but is not a cyclic-all-length theorem supplied to this record. No latest-best or implementation-performance claim is made.

The accepted exact tiling proof survives this comparison. A nonempty rank-one rectangle has rows in an H-coset and columns in an annihilator coset. If |H|=d, its dimensions satisfy a<=d and b<=N/d. Thus

    a+b = ab(1/a+1/b) >= (ab/N)(d+N/d)
        >= (ab/N) min_(e|N)(e+N/e).

Disjoint coverage sums ab to N². All products of the H-cosets and annihilator cosets form N disjoint tiles, attaining N(d+N/d). This establishes the accepted exact objective and its square/prime specializations at the literal no-sharing scope. It does not settle higher-rank nonsquare-composite tilings.

Retain the source's other guards: complex spectral norm and characteristic-zero prime full-spark arguments do not automatically transfer to arbitrary finite fields; the literal historical tile loop has an extra zero-addition per tile unless first-term initialization is used; a floating MILP status is not an exact proof certificate; roots, representation, storage and data movement are not made free by an incidence formula.

## Monomial centralizer comparison

[Tadej, *Defect and equivalence of unitary matrices. The Fourier case*, versioned source](https://arxiv.org/pdf/1310.8119v2), Theorem 4.23(c), equation (197), printed pages 56–57, gives the full complex unitary-monomial stabilizer as character shifts combined with paired group automorphisms. Lemma 4.22 and Corollary 4.8 supply its completeness; Lemma 4.9 specializes the pairing to inverse automorphisms for a cyclic indexing group. The adjacent discussion explicitly identifies the involutive-automorphism condition for permutation similarities. This is broader complex symmetry machinery from which the owned equal-side commutant is obtained, not a literal statement over arbitrary fields.

The following explicit specialization was independently checked. Use F_(i,j)=omega^(ij), with omega of order N, and Q e_j=a_j e_tau(j). Set b=tau(0). From column zero of FQ=QF,

    a_j/a_0 = omega^(b tau(j)).

Over C these ratios have unit modulus. Therefore Q/a_0 is unitary monomial, and commutation is equivalent to the stabilizer pair S=T=Q/a_0 fixing F under S F T*. This normalization is necessary before invoking the primary unitary stabilizer theorem. Scalar normalization of F itself does not change its commutant.

For N>=2, the entry equations reduce to

    i(tau(j)-b) + b tau(j) - j tau^(-1)(i) = 0 mod N.

Taking j=0 gives b²=0. Taking j=1 gives an affine inverse with slope u=tau(1)-b. Since tau is bijective, u is a unit. Comparing inverse slopes and tau's first difference yields u²=1. Substituting tau(j)=uj+b then gives 2ub=0, equivalently 2b=0. The weights become a_j=a_0 omega^(ubj). Conversely these congruences make every entry commute. N=1 is the separate scalar case. For odd N only b=0 is admitted; for even N the additional b=N/2 is allowed exactly when 4 divides N.

This derivation agrees with the source's accepted all-N algebraic proof and makes the equal-side specialization explicit. It uses only a field, nonzero monomial weights, and a primitive Nth root, so the accepted algebraic statement survives outside C. The extension is credited to the accepted proof rather than falsely ascribed to Tadej's unitary setting. No complex norm or conjugate-transpose argument is imported into a noncomplex field. The alternative Fourier sign convention yields the same centralizer because 2ub=0.

This closes the specified comparison without promising full dense-commutant classification, arbitrary gauge/routing invariance, free coefficient construction, or a new algorithm. The common-gauge architecture applications and finite F4 certificate remain in their own records.

## Exact accepted native proposal

The accepted target cells are:

- Research overview: C68, E68, F68, J68, P68, Q68; C93, F93, J93, P93, Q93.
- Catalogue: AE26, AF26, AE50, AF50.
- novelity breakthough: P51, T51, Y51, Z51; P76, T76, Y76, Z76.

All edits are limited to `userEnteredValue`. No targeted cell has rich-text runs, and no formula, priority, row identity, accepted theorem text, link run, format, validation or note is changed. Existing dynamic catalogue hyperlinks in novelty R51/R76 and rich source links in overview I68/I93 are outside the write set. Historical notes can retain their historical wording without being mistaken for the current cell prefix. `ACCEPTED_CELL_PREFIXES.json` records reviewed new text and preimage hashes without exposing the native old values. The conditional status delta is one more closed record and one fewer open record, subject to unrelated concurrent changes and a fresh complete count.

## Independent controls and publication boundary

An independently authored standard-library integer checker examined all 872 permutations for N=2 through 6, comparing the direct forced-weight commuting equations with the affine classification. All passed. It also checked all 5,213 nonempty subset rectangles at those lengths, verifying the subgroup envelope and exact integer incidence inequality whenever the rank-one divisibility test holds. These small controls supplement the written proofs; they are not a replay of historical source programs, a production test, or a substitute for a uniform argument.

The versioned primary papers were independently read through accessible PDF text. Screenshot attempts for the Tadej theorem pages returned cache-miss errors, so no visual-facsimile or local primary-PDF byte verification is claimed. The algebra above was independently derived to avoid relying on extraction of conjugate bars or permutation conventions.

No supplied research program was executed, imported, installed or compiled; no solver or denied-network bypass was used. No external write was made. Raw native preimages and complete third-party papers are excluded from this publication directory. The final cell reviewer must bind a proposal to fresh unchanged native preimages, preserve full dated history and all unaffected formulas/formatting/links/priorities, and verify the eventual readback.
