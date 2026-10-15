# Independent full-record review: M-CHORD

Date: 2026-10-14 UTC. Reviewer scope: original complete theorem record, not only its geometric dependency. No external writes and no historical program execution.

## Current verdict

The original Theorems A, B and C, local sharpness, and restricted scalar-polynomial bridge consequence are mathematically valid at their stated scope. Closing the full canonical M-CHORD record as **Closed (proved, attributed)** is appropriate once the actual revised manuscript integrates the primary attribution and the explicit complete-line/n=5 treatment and passes final text review. At this review checkpoint that artifact review is still pending. Historical/worldwide originality is not established and must remain explicitly unresolved. The broader two-stage Fourier/Green construction problem is separate and remains open.

## Exact record and identity

- Original archive: `../chord_finalize_1508/FFT_CHORD_RIGIDITY_BRIDGE_THEORY_2026-10-10.zip`; SHA256 `09b5042686dcac4f2e3f1ce87e0f53278bcbb5e61ff8989c7289a274616bb3c7`.
- Original theorem: `../chord_finalize_1508/original/fft_cycle_chord_20261010/THEOREM.md`; SHA256 `d3d598c9091a718ce1405a131ccbb82b0186814c2a7bad9661d99c9d5b6d319b`.
- All ZIP members were read only as bytes/text and hashed; CRC and declared member digests match. No uploaded/source checker was run, imported, compiled, or parsed as code.
- Source table snapshot: `../closure_audit_1410/PLAIN_ROWS.json`; SHA256 `20249cc853e0063e74fbfc7c681c966e71f70ae5301baa709d49c76fcfce1cba`.
- In that snapshot M-CHORD is Catalogue row 37, novelty-register row 59, and overview row 76. Some historical links still name novelty row 75. Stable-ID live resolution is required before a later table update; this review makes no table write.
- The source row's remaining mathematical-publication gate is manuscript integration in Section 0, Theorem A Step 5 and references. Its finite-field/general-runtime exclusions are permanent boundaries, not proof defects to erase.

## Primary attribution and incidence scope

Heineken, *Regelmässige Vielecke und ihre Diagonalen*, L'Enseignement Mathématique 8 (1962), 275–278, DOI https://doi.org/10.5169/seals-37967, supplies the incidence argument. The unnumbered conclusion is on p. 278; its proof is Eqs. (1)–(9), pp. 276–278, and finite/nonvertex exclusions are on p. 275. Independently retrieved publisher text explicitly allows real line parameters without restricting them to the segment interval. Its algebra uses distinct endpoints and nonparallel lines, so it applies to side-lines as well as diagonals. The manuscript must identify this as a proof-level extension rather than a verbatim broader theorem statement. For n=5, three different lines through a finite nonvertex point would need six distinct polygon endpoints, which is impossible. Infinite intersections of parallel lines and original vertices remain excluded.

Publisher extraction: https://www.e-periodica.ch/cntmng?bot=1&pid=ens-001%3A1962%3A8%3A%3A93 . Full text retrieval succeeded; attempted PDF screenshots failed with cache-miss errors. `HEINEKEN_WEB_EXTRACTION.json` is a web-tool text record, not PDF bytes or a visual-facsimile verification.

Tao, *An uncertainty principle for cyclic groups of prime order*, arXiv:math/0308286v6, https://arxiv.org/pdf/math/0308286v6, Lemma 1.3 on p. 3 with proof on pp. 3–4 supplies the prime full-minor result. Tao explicitly attributes that result to Chebotarëv. Therefore the appropriate wording is Chebotarëv's theorem, with Tao's proof as the checked source. This does not attribute the project-specific sandwich result to Tao, Heineken, or a newly established first discoverer.

## Independent proof audit

1. **Normal form and determinant.** Primitive-affine step coprime to n makes the n parameters distinct. Nonzero monomial gauges only change nonzero column factors and effective edge weights. The coefficient matrix taking (1,t,t²) to h(t)=(1-at,t(1-bt)) has rank two even when a or b vanishes. Direct expansion gives det(h(t),h(u))=(u-t)[1-b(t+u)+abtu]. No division by an edge weight is necessary.

2. **Geometry reduction.** For b nonzero set z=1/b. Two different dependent unordered pairs cannot have the same product because their sums would then also agree. Comparing the conjugate pair equations forces a=conjugate(z). The equation z+conjugate(z)tu=t+u is equivalent to membership in the complete real line through t and u. Rank two on every three distinct parameter columns excludes a proportionality class of three nonzero vectors, so different dependent pairs are endpoint-disjoint. Their common point is finite and cannot be a polygon vertex. The verified incidence corollary thus limits these pairs to two.

3. **Routing and zero-vector branch.** A Hamiltonian cycle of length at least three cannot use both orientations of the same unordered pair. Each canceled nonzero target needs one dependent pair, hence at most two outputs jointly vanish. If h(t0)=0 then a=b=t0⁻¹ and h(t)=(1-t/t0)(1,t); all remaining columns are pairwise independent. Only the zero target with zero incoming weight can cancel. The b=0 case has pairwise-independent columns. These branches establish Theorem A without losing zero weights.

4. **Local sharpness.** Pairs (0,2) and (1,3) in any odd n>=5 have distinct endpoint products, hence nonparallel lines. Their intersection is nonzero because no pair is antipodal. The given a,z,b formulas are therefore defined and make two dependent pairs. A zero vector would contradict these two disjoint pairs, so the canceling weights are nonzero. The two directed edges embed in a Hamiltonian cycle; all other right weights and an unused left weight may be zero. This gives exactly two joint zeros and both denominator guards equal to one. Only the local bound is shown sharp.

5. **Global bound.** Summing the n adjacent-pair union inequalities gives n(n-2)<=2 nnz(T), proving the stated ceiling bound. This requires every corresponding frequency triple to satisfy the primitive-affine condition.

6. **Prime hybrid.** On any three columns, the three involved frequency rows form an invertible Fourier minor. Multiplication by the rank-two row coefficient matrix therefore gives rank two. With no zero column, nonzero proportionality classes have size at most two, yielding at most floor(p/2) disjoint dependent pairs, each used at most once by the Hamiltonian routing. With a zero column, every other pair must be independent and only its zero target can cancel. Thus every weak pair has support union at least ceil(p/2). Combining g strong and p-g weak inequalities and dividing by two proves Theorem C exactly. This is a complete replacement for relying on an unspecified predecessor propagation lemma.

7. **Bridge.** Noncommutative multiplication gives A M D=(A+B)B⁻¹C⁻¹(C+D)=(A+B)(CB)⁻¹(C+D). The order K=CB is essential. Row-support degrees are at most 3,4,3. For a scalar polynomial of degree L>=0, the support union of K⁰,...,Kᴸ gives nnz(XP_L(K)Y)<=9n sum_(r=0)^L4^r. Comparing with the strong density bound proves 4^(L+1)>=1+(n-2)/6. This is a polynomial-degree condition, not a count of unshared arithmetic work or a barrier to unrestricted exact solves.

## Counterexample and exclusions

A fresh, independently written direct F19 matrix multiplication reproduces the source counterexample for n=9, primitive root 4. Joint-zero columns are [5,7,8], support union is 6<7, and both weighted-cycle inverse guards are 1. See `FRESH_F19_COUNTERCONTROL.json`. It was produced without executing any historical program.

Do not extend the near-full result to arbitrary finite fields, even lengths, repeated/nonunit progression parameters, arbitrary non-affine composite-frequency triples, or right permutations containing two-cycles. Do not claim global density sharpness, an unrestricted fast-solve lower bound, a two-layer impossibility, a new FFT algorithm, or worldwide priority. The complete proved theorem record can be closed without pretending those different questions have been settled.

## Remaining finalization check

Inspect the actual revised artifact and its hash. Confirm the Heineken extension and n=5 argument appear where the dependency is used; references and Chebotarëv/Tao attribution are precise; A/B/C/bridge statements and guards are preserved; the prime weak-pair proof is explicit; finite-field controls are not represented as all-size proof; historical originals remain preserved; and no unsupported novelty assertion was introduced. Until this check is recorded, manuscript integration remains the only closure gate identified here.
