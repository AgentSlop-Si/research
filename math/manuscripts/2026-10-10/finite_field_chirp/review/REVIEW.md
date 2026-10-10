# Independent review of the assembled finite field chirp manuscript

10 October 2026 UTC

## Verdict

PASS SCOPED MANUSCRIPT PROOF. No blocking mathematical, cost-accounting, source-identity, or scope error was found in the sealed standalone manuscript. The assembled text preserves the supplied-prime-field theorem accepted in the earlier independent review, gives its proofs explicitly, and does not acquire a stronger theorem merely through editorial consolidation.

The reviewed manuscript is `research_cycle_2224/chirp_manuscript/MANUSCRIPT.md`, 53,351 bytes, SHA-256 `d2cc285240a3d035238ba4ef9537b138106b54e4bccce71e16d416112338e4f1`. This verdict also covers its embedded rejection/cost appendix and claim/proof/citation concordance. The separate appendix files agree after the documented heading-level adjustment.

This is a fresh local mathematical review of this editorial object, with newly written exact controls. It is not journal peer review, production certification, a benchmark, optimized bit-complexity certification, or historical-priority clearance. No author packet file was changed. No inherited research program or author packaging checker was imported or executed. No external write, new fusion, theorem extension, or ranking change was performed.

## Reviewed identities

An independent read-only verifier checked the entire sealed packet rather than trusting its success flag. All 112 identity, receipt, original-source, appendix, and local-link checks passed. All 27 packet files are pinned in `SEALED_INPUT_VERIFICATION.json`.

The decisive earlier identities are unchanged:

- 2020 author proof: `research_cycle_2020/recognizer_unification/REPORT.md`, 28,692 bytes, SHA-256 `670fc97d4969b0130ba7b99661de1092c6989272c717d3c8dade17771eb4a11c`.
- 2033 independent review: `research_cycle_2033/recognizer_review/REVIEW.md`, 15,374 bytes, SHA-256 `5caac961c8ef5120c55fa024063080e0d87b67e8cc5847387f239221cb6d3cbb`.
- The 2033 receipt binds exactly that author proof, review, historical checker, and saved results. Every corresponding preserved copy is byte-identical to its pinned original.
- Author manifest: SHA-256 `be3ec2e701d0f25db5a9cb95dd68a3a16029271d3322e4760018f7bfb0037b06`.

The older proof's pending-review header and the manuscript packet's pre-review sealing statements remain historical facts about their creation. This separate, later receipt supplies scoped acceptance of the sealed manuscript; neither older object was silently rewritten.

The D06 discrepancy remains correctly disclosed. The available variant is 13,619 bytes with actual SHA-256 `8bb0ccc144506e968df1a9999300e3e42d060dc055b9e7f6a1049e1b36753b0f`, not the historical 13,647-byte object named by `e871250b94c9a5823adacee7da26bb6d4477af0758c684aa8c8ff9e34be21f89`. The Gauss proof in the current manuscript is self-contained and agrees with the exact reviewed P1 derivation. Its correctness does not require resolving that historical byte mismatch.

## Eliminant and ring arithmetic

Theorem 1 and Sections 3–4 are correct under their stated assumptions.

A nonzero exponential sum on s distinct nonzero nodes cannot vanish on s consecutive coordinates: the corresponding square Vandermonde is invertible. The interior interval has N−2r at least r entries. Therefore a nonzero member has an eligible nonzero center whenever N is at least 3r. Rejecting a nonzero vector with no such center is justified.

For f(d)=d(d−1)/2, all exponents are nonnegative integers, and f(d)=0 exactly at d=0,1. Thus A(0) is lower bidiagonal, E(0)=x_c^(r+1), and every leading determinant of order k has constant coefficient x_c^k. This is a uniform nonvanishing assertion at any eligible nonzero center, with no generic-position hypothesis.

The permutation exponent is sum(i²)−sum(i sigma(i)). Reversal maximizes it at D=r(r+1)(r+2)/6. Hence degree at most D is correct; equality is not asserted. Extending a partial row–column matching to a full permutation also justifies the square-minor degree observation. No requirement D<p or interpolation at D+1 field points has appeared.

At z=omega^(−2a), the exact entry becomes y_(c+i−j) times omega^[a c²+a(2c+1)(i−j)]. The extra factor separates into nonzero row and column factors. The dechirped Toeplitz matrix factors through s nodes, so every true phase is an eliminant root. The canonical phase grid has L=N/gcd(2,N) distinct points; its reduction in the even case follows from j²−j being even.

The candidate bound min(D,L) applies to the original nonzero polynomial. A zero reduction modulo z^L−1 forces D at least L and retains every phase. It does not permit rejection or use of a root bound for a zero reduced polynomial.

In the truncated ring, all leading determinants are units. Schur-complement ratios e_k have constant coefficient x_c. The nonsymmetric paired-predictor updates are simultaneous old-vector updates; their defining equations and determinant product are preserved. Therefore no legal input with a nonzero center encounters a nonunit pivot. Such a failure would be implementation failure or invalid arithmetic, not family nonmembership.

Newton inversion g←g(2−eg) squares the residual in arbitrary characteristic and divides by no field two. All series inverses start from one cached x_c inverse. The O(r²) ring-operation count, O(r) reciprocals, Karatsuba exponent kappa=log_2(3), and linear-workspace recursive arithmetic give T(r)=r²(D+1)^kappa field additions/multiplications, one scalar inversion, and O(r(D+1)) live coefficients.

## Candidate decisions and scope

Section 5 uses the standard finite-field recurrence mechanism correctly. BM's order cannot decrease as more prefix samples are required. True s-term sums have nonsingular leading s-square moment matrices, so 2t samples suffice when s≤t. A finite-prefix BM order need not equal the polynomial degree on arbitrary inputs; the manuscript explicitly checks equality.

For the connection polynomial C(z)=product(1−lambda_l z), a grid root omega^v represents lambda=omega^(−v), not omega^v. The amplitude formula gamma=−lambda Q(rho)/C'(rho) has the correct sign and factor. Distinct grid roots, derivative guards, and nonzero listed amplitudes are checked. Full-vector synthesis supplies soundness for arbitrary prefixes; order zero is accepted only after scanning every raw coordinate.

The all-length branch also decides the same fixed-phase family. A genuine member has the stated rank and nonsingular leading block. On acceptance, solving the first s samples and checking every monic-recurrence residual forces equality at all subsequent coordinates by induction. Omitting zero recovered weights preserves that representation. Its leading-rank test is not used as a stand-alone acceptance criterion.

Every true phase survives and passes its complete test. A failed phase removes only that phase; complete candidate exhaustion proves final nonmembership. These statements apply to every valid-contract input, not just generic vectors or successful recognitions.

The theorem remains restricted to complete canonical-residue vectors over a supplied certified prime field, N dividing p−1, a supplied exact-order-N root, and 1≤r≤floor(N/3). Only the dyadic branch uses Fourier pruning. The general-field validity of the determinant identity does not extend the complete recognizer theorem to all fields. No supplied support, free root discovery, compressed-input access, floating-point tolerance, or stability guarantee is introduced.

## Complete cost and rejection ledger

The exact H and B ledgers agree with the 2020 proof and 2033 scoped review.

The dyadic phase scan reduces coefficients modulo z^L−1 and prunes a transform of support at most min(D+1,L). The input-parity recursion has at most min(2^d,h) active nodes at depth d, and summing their combine work gives O(N[1+log(h+1)]). Sequential/depth-first workspaces justify O(N) transform space.

All retained phases, including failures and a final rejection, receive the full O(N log(r+2)+r²) sparse-candidate budget. Thus

H=T(r)+D+N log(min(D+1,L)+2)+C_*[N log(r+2)+r²]+Nr+N.

The resulting uniform envelope O(Nr³ log(r+2)+r^(2+3kappa)) is correct. The O(r^5) candidate polynomial term is absorbed by r^(2+3kappa). Scalar inversions are separately O(1+C_*r), not free operations. Peak field storage is O(N+r(D+1)), not a sum over candidate workspaces.

For arbitrary lengths, the integer-binomial identity in Section 7 has the right signs, including negative a−j. The block lengths are O(s+1); a final partial block is charged. Both full-grid evaluation and all recurrence residuals cost O(N(s+1)^(kappa−1)). Horner phase evaluation and dense prefix work then yield B and O(Nr^(2+kappa)+r^(2+3kappa)). This proof uses no extra transform roots.

The sparse-first attempt costs A whether it succeeds or fails. Equal caps give S_r contained in C_r; unequal caps retain the explicit union and unabsorbed A term. min(B,H) is legitimate because those branches decide the same family with the same output contract; min(A,B) is not inferred for all chirps.

A completed REJECT supplies a membership decision, not a DFT or a promised succinct negative witness. A wrapper pays the full recognition attempt plus its backend. The stated backends are dyadic O(N log N) or same-field all-length O(N^kappa). A budget abort remains UNKNOWN. Validation, root-table preparation, raw traffic, accepted output, optional prime certification, integer gcd/inverses, and field inversions retain their declared charges. The word/bit conversions remain parameterized. The slowly growing rank corollary concerns additions/multiplications unless its additional costs also satisfy the desired total model.

## Gauss conventions and fresh vector application

Section 8's row formulas are correct. d=gcd(a,N), m=N/d, A=a/d, and xi=omega^d produce support only at multiples of d and the factor d in G_a(dw)=dT(w). Odd m uses the modular inverse of 4A modulo m. For m=2q, translation by q gives the parity condition w≡q mod 2. The shift u=((w−w0)/2)A^(−1) modulo q yields exponent −Au²−w0u; changing the lift by q leaves the phase unchanged. The a=0 and q=1 cases avoid an inverse modulo one. All halves are integer halves on even numerators.

The positive-sign unnormalized output uses G_a(k+u_l). Phase-zero output scatters N gamma_l at −u_l. The fresh-vector operator formula uses the reflected index −i−u_l and the factor N. Its O(N(s+1)) cost applies after sparse recognition and must be paid again for each fresh vector.

A chirp certificate generally gives a dense convolution-type operator, not the sparse-shift application bound. At odd length and unit phase, its Gauss kernel is diagonally equivalent to a Fourier matrix with root omega^(−(2a)^(−1)); that root is primitive and the common Gauss factor is nonzero. The resulting linear-time implication is correctly described as an implication, not a lower bound.

## Attribution and unresolved comparisons

I independently reopened the four primary classical references used by the manuscript and inspected their relevant passages. Attribution is appropriately limited:

- Massey explicitly credits Berlekamp and treats shortest recurrence synthesis over fields; the monotonic order and Section III synthesis/uniqueness statements support the cited classical ingredient. [Massey author archive](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf).
- Peter–Plonka Theorem 2.1 gives recurrence/root/coefficient reconstruction over its displayed complex-domain setting; Section 5 specializes sparse-vector recovery. The manuscript supplies its own finite-field argument instead of claiming that source already states the present every-input contract. [Peter–Plonka author manuscript](https://na.math.uni-goettingen.de/pdf/Operator_Prony_revised2.pdf).
- Gutknecht–Hochbruck Section 2 gives paired nonsymmetric predictors, pivot updates, and Algorithm 1. The centered truncated-ring unit guarantee is separately proved here, not attributed to their real/complex presentation. [Gutknecht–Hochbruck author version](https://people.math.ethz.ch/~mhg/pub/mhg-published/GutH95-NM70-laLSnHTs.pdf).
- FFTW documents the classical pruning savings and distinguishes arithmetic count from practical speed. The manuscript also proves its own dyadic tree bound. [FFTW pruning documentation](https://fftw.org/pruned.html).

I compared the literature discussion and concordance to the preserved R2 access ledger. The complete Derin text is still uninspected, the Applebaum comparison is still passage-level rather than a complete-paper read, and Lindsay's original Theorem 5B is still indirect through Agostini–Améndola–Ranestad. This review did not resolve those access/comparison gaps. It does not upgrade an abstract or indexed passage to theorem-level exclusion. The manuscript correctly distinguishes moment/sample/ordinate/complex-chirp and finite-field-vector interfaces, recognizes shared-parameter elimination as an established framework, and leaves precise priority unresolved.

No worldwide novelty, optimality, new general Toeplitz/Prony/FFT kernel, unrestricted Fourier improvement, or noisy-recognition result follows from this review. The remaining literature gaps are comparison and priority gaps, not missing lemmas in this finite-field proof.

## Fresh exact controls

Only the newly written `independent_exact_checks.py` was run. It uses standard-library exact arithmetic, independent polynomial/permutation constructions, a direct all-phase DFT-support oracle, and separate BM and Hankel candidate tests. Historical adversarial vectors were reused as openly identified input data, not as inherited executable logic.

All controls passed:

- 60 ring determinant/permutation comparisons, including predictor invariants and unit-leading-minor constants, for r=1 through 4 over p=2,3,5,7,17. Small-characteristic algebra controls do not broaden the recognizer contract.
- 1,354 all-length Hankel recognizer decisions and 814 dyadic BM recognizer decisions against the direct-DFT oracle, totaling 2,168. This includes all 625 vectors of F_5^4, and structured/arbitrary cases through N=16 and r=3.
- 1,250 exhaustive sparse decisions, caps 1 and 2 on all F_5^4 vectors.
- 522 accepted-certificate dense outputs checked against direct DFTs; 429 completed nonempty candidate-exhaustion paths.
- 220 explicit true-phase eliminant-root checks.
- 820 Gauss-row comparisons, all phases for each N=1 through 40, including zero and nonunit phases and the parity/modulo-one endpoints.
- 122 blocked-grid identities, 22 same-field fallback identities, 4 fresh sparse-operator identities, and 20 odd one-chirp Fourier equivalences.
- Explicit accepted/rejected zero-reduced eliminants, false and zero prefixes, an impulse, off-grid/repeated-root cases, chirp-only and unequal-cap sparse-only inputs.

The checker deliberately uses elementary arithmetic rather than the optimized kernels. These finite controls corroborate signs, indexing, guards, and exact decisions; they neither prove uniform complexity nor measure the claimed runtime. The all-parameter claims were assessed by the mathematical proof review above.

## Disposition

The sealed manuscript may be described as independently reviewed for its stated exact supplied-prime-field proof and complete recognition ledger. No mandatory correction was identified. Preserve its field/root/cap contract, separate inversion/integer costs, dyadic-only pruning improvement, paid failed attempts/fallback, recognition/application distinction, unresolved priority comparisons, and D06 provenance qualification in subsequent use.

The packet should remain byte-stable. `REVIEW_RECEIPT.json` binds this review, the fresh checker/results, the independent seal verification, and the exact sealed manuscript. A later manuscript edit requires a new delta review and new binding before this verdict is applied to the edited bytes.
