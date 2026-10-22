# Independent review: C10 prime-field selected-system cost contract

21 October 2026 UTC. Verdict: ACCEPTED in the bounded scope below, against the exact frozen author v3 bytes. The substantive theorem and corrected ledger pass independent mathematical review and fresh exact controls. No supplied research program was executed or imported; no repository, native workbook, or other external state was changed.

## Decision and boundary

The accepted bounded completion is the prime-field root/representation/bit-cost specialization of the already accepted selected projective row-system solver. It includes deterministic base-field and algebraic-closure decision, and a constructive common quadratic output field with the explicit witness and field-discovery charges below.

The entire C10 owner remains open. Column compatibility, supported-entry scales, legal Green parameters and denominators, fixed endpoint integration, full two-Green factorization, concrete target preparation/extraction, and Fourier-application complexity are not solved here. This is not historical novelty, a lower bound, or a faster Fourier algorithm. Earlier accepted obligations must not receive duplicate completion credit.

## Authoritative input and source verification

The mathematical input is N nonnegative vertices and M selected directed bilinear equations u_j^T L_e u_i=0. The matrices have canonical F_p coefficients, and p is a supplied promised prime. Endpoint indices are valid; hence N=0 forces M=0. Loops, parallel equations, disconnected graphs, rank-zero and rank-one matrices, repeated roots, and p=2 are admitted.

I independently fetched the following three actual files through the connected GitHub read interface, at the exact commits below. I compared their complete returned text to the author's inert source snapshots, recomputed SHA256 and Git blob identities, and read the full relevant proofs. The source register was separately hash-checked. A hash-named filename was not treated as evidence of its contents.

- Original accepted reduction: commit 0339a31eb6109f0b96074ab8321f8653641e7530; 8,526 bytes; SHA256 93b237e0e3d425cc126df06c60d686ec644159fa31e035df38dc7bfa849f4835; Git blob 7bd7146ab8d8257f0b973bf9ccb7a3b1408e7fb8. https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/93/93b237e0e3d425cc126df06c60d686ec644159fa31e035df38dc7bfa849f4835__REVIEW.md
- Accepted sorting/sequential-2SAT report: commit 228288f489fef7bd534275a54d4c4c2c842cff38; 14,656 bytes; SHA256 72a2777bd409eea831567306c9c920332f99febb73d5c767bfbbab7606539a76; Git blob 279f4862ba9c36265ee4e4c5e82cf30a77a41208. https://github.com/AgentSlop-Si/research/blob/228288f489fef7bd534275a54d4c4c2c842cff38/math/finalized/2026-10-16-research-finalization-1749/c10/REPORT.md
- Its independent acceptance: same commit; 11,719 bytes; SHA256 f8536528b7637caa0eac54e069e5f70a06559f349aa99a77508ab7d9fbfa7230; Git blob 2f96d325f1b8ef4d95da4ec9bd1dcc9c6fa6c427. https://github.com/AgentSlop-Si/research/blob/228288f489fef7bd534275a54d4c4c2c842cff38/math/finalized/2026-10-16-research-finalization-1749/independent_review/INDEPENDENT_REVIEW.md

The owner's retained open-record snapshot is provenance, not mathematical evidence. It is not included in this review's source set.

## Common quadratic field: independent proof audit

Every rank-two edge has invertible transport J L_e. Reverse propagation can use its adjugate; this is projectively the inverse even in characteristic two. A spanning forest expresses each u_i as T_i z_C with T_i invertible over F_p. Every internal equation becomes one homogeneous binary quadratic over F_p. Its component's domain is summarized by the finite-chart gcd and a separate infinity bit. Every cross-component nonzero matrix has rank one, so its equation is a positive disjunction of equality to two points defined over F_p.

For odd p choose eta with eta^((p-1)/2)=-1. Then X^2-eta is irreducible and E=F_p[alpha]/(alpha^2-eta) is a field, represented uniquely by two residues. A degree-two polynomial with discriminant Delta has roots in E: zero and square discriminants require only F_p; for nonsquare Delta, Euler multiplicativity gives that Delta/eta is square, so sqrt(Delta)=r alpha with r in F_p. Linear roots are already in F_p. The same fixed eta works for every component.

For p=2, X^2+X+1 has no binary root and defines F4. It is the only irreducible monic quadratic over F2. Evaluating its four represented elements suffices to find the finite root of any nonconstant polynomial of degree at most two. No division by two or binary nonsquare is required.

The accepted 2SAT reconstruction now uses points in this one E. A true named flag selects its F_p point. An all-false component selects any allowed point in E. If this is a named base point, exactly its flag is turned on and sequential prefix auxiliaries are recomputed. If its alpha coefficient is nonzero, it equals no named F_p point. The repair preserves every positive cross clause, every genuine forbidden-name unit, and at-most-one. It does not require an unnamed-point search, even when all base-field projective points are named.

Thus a closure-feasible selected system has some solution wholly in this common E; conversely E embeds over F_p into an algebraic closure, so an E-solution is a closure solution. Transported vectors are nonzero because each T_i remains invertible over E. Every original equation can then be evaluated directly in a single field.

This is existential. It does not say that every particular closure solution has degree at most two. For example, a one-vertex system with no equations admits [1:beta] for beta of degree three over F_p; that particular projective point is not in P1(F_(p^2)). It also admits [1:0], which is the required bounded-field witness. The accepted v3 wording expressly retains this distinction.

## Complete deterministic decision ledger

Let b=ceil(log2(p+1)), ell=ceil(log2(N+M+2)). With elementary b-bit modular multiplication/remainder costing O(b^2), and nonzero inversion via a^(p-2) costing O(b^3), the corrected bound is

D = O((N+M+1)(b^2+ell) + M b^3 + M log2(M+1)(b+ell)).

This is valid in the report's specified bit-cost, record-random-access model. It is not claimed for every bit-addressed RAM or Turing-machine memory model. Record accesses/copies charge their ell-bit index and field payload, rather than silently costing one.

The phase audit gives:

1. Reading, rank tests, graph/forest construction, all transport products and internal substitutions require O(N+M+1) bounded-field arithmetic and index work. Adjugate reverse transports introduce no N-term inversion charge.
2. Every polynomial gcd has degree at most two, so each update uses a bounded number of divisions. At most O(M) such divisions contribute O(M b^3). There are at most min(N,M) restricted components.
3. The at-most-2M named point occurrences lie in F_p. Canonicalization is either the unique infinity tag or y/x, with one certified nonzero inversion. Equality of keys is exactly projective equality. This adds O(M b^3), not an unpriced inversion oracle.
4. Deterministic comparison sorting charges O(M log(M+1)(b+ell)) for keys, component identifiers, copying and comparison. Occurrence references prevent repeated global dictionary searches in clause construction. A comparison sort with linear auxiliary records exists; no randomized dictionary is needed for the theorem.
5. Named membership checks, at most 4M variables and 9M clauses, implication-graph construction, SCCs, and assignment/repair all have O(N+M) graph/index work with the stated bit charge. Matching a repaired base point can use one scan of each component's names, totaling O(M); no hidden pairwise search is required.
6. A base-field quadratic is nonempty iff Delta=0 or Euler's test returns 1, for odd p. This costs O(b^3) per needed component. Binary evaluation at 0 and 1 is constant. Closure decision needs only a nonconstant chart gcd or allowed infinity, with no root extraction or supplied eta.
7. The added +1 explicitly covers the prime descriptor, initialization and decision bit when N=M=0. Storage, including fixed registers, is O((N+M+1)(b+ell)) bits beyond a retained target oracle.

No coefficient growth is hidden: every intermediate is reduced modulo p, including transport coefficients and polynomial summaries. Prime verification is not inferred from a nonsquare test. Untrusted primality adds the actual P_prime; unreduced or oversized integer inputs add their actual reading/reduction costs.

## Witness, root algorithm, field discovery and output

The report uses the classical Tonelli-Shanks loop, not a square-root oracle or the faster algorithms in the cited paper. I checked Algorithm 1 in J.-C. Schlage-Puchta, “On Shanks' Algorithm for Modular Square Roots,” https://arxiv.org/pdf/1105.1456, and independently audited the stated operation count.

For p-1=2^s q, initialization takes at most 6b modular products. The loop maintains c of exact order 2^m, t of order at most 2^(m-1), and r^2=d t. When t is not 1, its least exponent i obeys 1<=i<m. The update cancels the top order-two part of t and decreases m to i. The work in that loop is i+(m-i-1)+1+2=m+2 products. The distinct m values are drawn from s,...,2, giving the stated conservative total 6b+s(s+5)/2. Exponent and loop-control costs fit O(b^3+s^2 b^2). Zero radicands bypass the nonzero-square loop; invalid eta is an auxiliary-input error, not UNSAT.

If W is the actual number of required quadratic component roots, W<=min(N,M). Supplied eta is certified once at O(b^3); root construction, needed coefficient inversions, and a cached eta inverse add

O(b^3 + W(b^3+s^2 b^2)).

The binary branch has no eta and O(1+W) setup/root work; the displayed common upper-bound notation may use s=0 at p=2.

Constructing E from its certified degree-two polynomial is only a constant-size descriptor with O(b)-bit coefficients. Multiplication uses a bounded number of base products. Reconstruction and direct checking of all original equations cost O((N+M)(b^2+ell)), already absorbed in D. Row-coordinate payload is O(Nb), and total output with field descriptor and decision bit is O((N+1)b). It consists of nonzero pairs, not implicitly normalized coordinates. Requested canonical normalized output adds O(N b^3); the extension inverse uses the nonzero norm a^2-eta b^2, and binary inversion is constant-size. Additional sequential root scratch is O(b); storing all coordinates remains within the solver's stated linear storage.

Consequently the supplied-nonsquare witness bound is

S_B^bit + O(M E_B^bit) + D + O(b^3 + W(b^3+s^2 b^2)).

No supplied eta is needed for either decision. When odd-p witness construction is requested without eta, independent uniform F_p* trials have success probability one half; b-bit rejection sampling has constant expected retries. Charging all tests yields Las Vegas expected O(b^3) setup. A deterministic scan has an explicitly retained conservative O(p b^3) surcharge. The theorem does not assert unconditional deterministic polylogarithmic nonresidue discovery. Supplied and discovered field setup are not silently interchanged.

Target extraction remains S_B^bit + O((N+1)ell+b+M E_B^bit+M b^2), subsumed by the combined bound above. These are same-model bit costs. Scalar S_B/E_B values cannot replace them. Target field/root-of-unity construction, power-table setup, entry representations, and possible M=Theta(N^3) selection costs are not newly bounded.

## Fresh independent exact controls

The reviewer authored independent_controls.py from the displayed mathematics. It does not execute, import, compile, or parse any author research/checker program. The original-equation brute-force oracle is separately implemented from the forest/gcd/2SAT reduction. The tiny-field enumeration and Python data structures are validation devices, not a claimed implementation of the asymptotic bit model. Complexity acceptance comes from the explicit algorithm/phase proof above.

Normal Python and python -O independently completed with identical JSON result bytes. All correctness checks use explicit exceptions, so optimization cannot remove them. Results include:

- 30,080 exact base/closure decisions on 15,040 complete selected systems. These include every ordered pair of 2-by-2 matrices on one-vertex loop systems and two-vertex parallel-edge systems over F2 and F3, plus seeded mixed graphs and bounded F5/F7 cases. Closure answers are compared against exhaustive original-equation assignments in F4/F9/F25/F49 as appropriate.
- 19,781 directly verified nonzero original-system witnesses, including 12 additional forced-all-false complete-graph controls. The latter explicitly cover unrestricted components with every base point named, finite repeated-root domains and infinity-only domains. Across all successful runs, 17,766 all-false components, 14 named-point repairs and 1,183 genuinely nonbase all-false components were exercised.
- A nonbase component adjacent to a forced named base point, independent irreducible components, rank-one loops, rank-two forests, zero equations, empty/isolated systems, repeated roots, and the tight three-quadratic obstruction.
- 16,124 base/closure degree-two domain checks through F13; 1,659 strict-extension domains; 258,121 canonical projective equivalence comparisons through F19; 76,125 Euler tests and 75,958 base inversions through prime 997; 371 extension inversions.
- 47,765 successful nonzero Tonelli calls across all test families, with exact loop product counts, maintained invariants and the global budget checked. There are 668 invalid-eta certificate rejections and one explicit auxiliary-error-path test.
- 241 simultaneous irreducible component polynomials over F241, all with roots represented in the same eta=7 field, including the source example alpha^2=7 with 7^120=240 modulo 241.

Finite tests are controls, not proofs for all primes or graph sizes. They do not rerun target extraction, original N3/N5 target constructions, arbitrary-field composita, or any full Fourier factorization. The author's separate narrow counts are not relabeled as these independent whole-system checks.

## Review corrections and final integration guard

The initial v1 ledger vanished at N=M=0; that was a real omitted fixed-cost case. The author preserved v1 and issued v2 with the +1, fixed storage/extraction overhead and complete-output accounting. I checked every v2 manifest payload and the full diff. The author then preserved v2 and issued v3 with the requested existential common-field wording and total binary s notation. I inspected the exact v2-to-v3 diff, recomputed the report and manifest hashes, and verified every manifest payload of all three versions. These precision changes do not alter the proved algorithm.

A separately pinned reviewer proposal was prepared while the author was temporarily unavailable. It is now superseded by the author's verified v3 and is non-authoritative: it is not an additional theorem or a replacement source. The accepted author REPORT.md has SHA256 2a0d28168c92d2738985d57a879e79879d5112d493a86a26943f90aeda973447, and its complete v3 MANIFEST.json has SHA256 ebe8cbde5ecc6fa51e5915e0f107ec7bc927fc40a7d146bbf3a57f8c465d3214. The accompanying acceptance record binds these exact bytes to this review and the fresh controls.

Only the named prime-field root/representation/bit-cost obligation is accepted as completed by this final byte-bound review. No parent status, protected history, old accepted text, native cell, score or publication count is implicitly changed by this mathematical review. A sanitized export and separately authorized, verified integration are distinct operations.
