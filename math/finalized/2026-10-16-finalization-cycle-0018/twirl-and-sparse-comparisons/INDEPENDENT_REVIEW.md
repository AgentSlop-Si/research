# Independent review of the sparse-defect and Weyl-twirl comparison gates

16 October 2026 UTC. Repository reference: `07455df33fd8243bc0e7facb92af6c6a5830ae2a`.

## Scope and decision

**ACCEPT** the mathematical comparisons and the exact 19-cell proposal with SHA-256 `a2a14c8ae0c345c2390305f0b2bb3789955b4ce6f27548d5f5216428f11070cc`. All 19 preimages match fresh independent native reads, six stable row bindings agree, and all four action/stop mirror groups match. Eighteen cells prepend dated scoped updates while retaining full history; only overview E108 replaces its status with CLOSED. This review makes no external writes and grants no new theorem, discovery, priority, runtime, or implementation acceptance.

- **M-SPARSE-DEFECT:** complete the bounded inverse-neighborhood comparison stage and keep the parent open. Global uniform row-sparsity sharpness is an explicitly retained successor, not a consequence of single-neighborhood attainment.
- **M-WEYL-TWIRL:** its named certificate/comparison record is eligible for scope-limited closure once the accepted comparison is recorded. The canonical result is the fixed-linear certificate, moment bound and correctly charged cut calculus. Uniform coefficient construction and bounded training are expressly excluded consequences, rather than missing lemmas of that certificate. No status of Q10, F081, another Weyl record, or a constructive synthesis task follows automatically.

The exact owner stop for both records permits a primary theorem with an explicit hypothesis/formula/cost mapping, or a qualified nonmatch or identified access blocker. It does not require worldwide priority clearance. The remaining global row-sparsity successor distinguishes the sparse parent from the twirl certificate record.

## Independent source and prior-work checks

I read the live overview rows 98 and 108; Catalogue rows 47 and 48; and the corresponding `novelity breakthough` rows 81 and 91. Their stable IDs agree. These native preimages remain local and are excluded from this publication report.

I independently retrieved the five repository sources below, read their relevant complete proof/review bodies, and verified the retrieved content against the returned Git blob SHA-1. SHA-256 values are the actual repository bytes, not filenames treated as proof of identity:

- Phase20 audit: `e7413d1d591cfae89647304a88b1ca664dea9602dd86fec79a58688f346a7946`, Git blob `28212b19e78502ce5acf52a90570d42b0285d3d0`.
- Weyl expansion review: `f061a03aaeee5077e0f40d931f29a59c1debcf44253c9eb683ddfa027a9b5572`, Git blob `f0852ec11fc260c52ea3c0b5f1d427d37cf771b6`. This is the documented sanitized repository export. The historical archive identity `989383d1...` is not asserted to be byte-identical to it.
- Stable inverse-defect audit: `7f554d446354ad3a1afe464c6bb187701de452990c2c54d5cbd8bf7dce6cddef`, Git blob `32e210a98b14888fa57096b2050d1e644bc5e0b9`.
- Inverse refinement review: `2de76424c35cd9bfe1eedaad4091b56ed53a49b5fff6f5cb4b77a130fb28b12c`, Git blob `2a474abbf29b040bef68211523b7bab07b2efd3f`.
- Publication-readiness review: `d240eb54e486ad2cd768b0ca95bdd0f3164c65b4c7c31234532fb5b46ec6c4fc`, Git blob `90d0c62a1c768975cdb4ee374426fa3bb8fc8ed8`.

The original accepted REVIEW-11 record also hashes to its catalogue pin, `1868a916c240c0f20bb132bf3850376170e17a7134fb2713ee3d961cbbc5be13`. The prior full M-record inventory explicitly retains the sparse global-sharpness successor and labels the twirl record as an accepted certificate with a generic comparison remaining.

The existing stable-inverse and publication-readiness sources already cite nullity and singular-value approximation for the lower bound. Repeating that attribution alone would not finish the selected next comparison. This review instead checks the positive attaining construction and the zero-critical endpoint, keeping them distinct from global sparsity.

## Sparse-defect comparison

[Lang, *The Inverse of a Nearly-banded Matrix*](https://arxiv.org/pdf/0812.0172), Theorem 2.1, equation (3.2), and Lemma 3.3, supplies nullity, best low-rank block approximation, and a block replacement preserving invertibility in a small-error regime. Lemma 3.3 is the important additional comparator beyond the previously recorded lower-bound ingredients. Its literal hypothesis is small perturbation; its proof establishes invertibility when the replacement error is below the reciprocal inverse norm. It does not state the entire all-unitary, arbitrary-rank-budget, zero-critical-endpoint theorem in the project's formulation.

[Li–Strang, Theorem 1](https://cklixx.people.wm.edu/uinorm-note.pdf) independently supplies the rectangular complex truncated-SVD minimizer for any unitarily invariant norm, including the spectral norm used here. Its [2020 journal identity](https://journals.uwyo.edu/index.php/ela/article/view/5551) was verified. It is cited as classical approximation machinery, not as the complete inverse-pattern theorem.

Here is the independently checked substitution and derived extension. Let U be unitary, t=|I|, m=|J|, 0≤r<t, d=t−r and k=m−d. The feasible inverse-block class is empty when d>m. Otherwise nullity converts its constraint to rank M[J,I-complement]≤k. Put A=U[J,I] and C=U[J,I-complement]. Since AA*+CC*=I_m, padded singular-value lists give σ_(k+1)(C)=sqrt(1−σ_d(A)^2).

Replace C inside U by a best rank-k truncation, leaving all other entries unchanged. The full perturbation norm equals that block error. When σ_d(A)>0 it is strictly below one, so the full matrix is invertible by the unitary distance-to-singularity test. Nullity recovers the required inverse-block rank. The choice deleting the leading d left singular directions of A is exactly the accepted construction U−QQ*U P_(I-complement). This proves the mechanism match; it is a derivation from classical ingredients, not a literal quotation of Lang's full theorem. In the literal r=0 dimensional correspondence, feasibility gives m≥t and Lang's p=m−t is nonnegative. General r uses k=m−t+r and the independently stated nullity derivation, without pretending negative bandwidth is covered.

At σ_d(A)=0, a feasible inverse defines at least d independent vectors h supported in J with M*h supported in I. Since rank A<d, one nonzero such h also has U*h supported in I-complement. Invertibility makes M*h nonzero; orthogonality yields error strictly greater than one. Scaled feasible permutation matrices approach error one. Thus the infimum is one and is unattained. This endpoint proof is already accepted internally. Neither inspected Lang clause nor the following comparator states it in this exact constrained-invertible form; that is a bounded qualified nonmatch, not proof of originality.

[Li–Lim, *Generalized Matrix Nearness Problems*](https://www.stat.uchicago.edu/~lekheng/work/near.pdf), §2.1, Algorithm 1, pp. 1710–1711, treats a Frobenius-norm generalized low-rank variable problem. It does not impose the full-matrix invertibility and inverse-subblock constraint of this spectral-norm endpoint problem. The declared complex extension does not remove these metric and feasible-class differences. This is a clause-level comparison, not a claim that no other theorem in the literature can imply the result.

All-unitary spectral statements remain separate from Fourier-flat scalar bounds. The sparse-column sine bound needs 1≤s<N. Scalar global row-sparsity formulas retain their s≥1 and separate r=0 branch. Dense inverse sums, variable masks and changed coordinate frames need not satisfy the hypotheses. No finite-field operator-norm transfer, exact support-union sharpness, global uniform-sparsity optimum, or unrestricted arithmetic lower bound follows.

## Weyl-twirl comparison

[Werner, *All Teleportation and Dense Coding Schemes*](https://arxiv.org/pdf/quant-ph/0003070), Theorem 1, items 4–5, equations (5)–(6), supplies the exact finite-dimensional unitary-basis/depolarizer implication. With d=N and W=D^aS^b, trace orthogonality holds for every N, including composite N. Divide the source's sum by N² to obtain the project's twirl. For X=U*M, expanding the commutator square gives the squared Frobenius distance to the scalar multiples of U. M is fixed and linear; it need not itself be invertible or unitary. Calibration of the scalar remains a separate condition.

[Iitaka–Ebisuzaki, *Random phase vector for calculating the trace of a large matrix*](https://arxiv.org/pdf/cond-mat/0401202), equations (2)–(4), (16), and (22), gives the complex random-phase variance mechanism. Independent uniform four-phase coordinates satisfy Ez_i=Ez_i²=0 and |z_i|=1. For H=R*R, that substitution gives E(z*Hz)²=(tr H)²+tr(H²)−ΣH_ii². Combining this with the accepted residual bound ||R||_F≤2τ yields E Z²≤8τ⁴ and Var Z≤7τ⁴ for Z=||Rz||²/2. Four-phase sampling is stated as an explicit substitution, not as the continuous distribution in the paper.

The dimension-independent sample counts remain valid under fresh independent Weyl and probe samples: k≥ceil(28/ε²) per group and h≥ceil(8 log(1/δ)) groups suffice by Chebyshev and Hoeffding. These estimate the loss of a fixed candidate; they do not establish optimization convergence or protect an adaptive/stateful oracle. Finite-precision zero loss does not prove exact equality.

Each sample pays two complete candidate applications plus phase/shift/vector work. For candidate preparation P and application T, the arithmetic work is P+O(kh(T+N+log N)), with additional seed/calibration work when used. Root generation, exact sampling, coefficient representation, precision, candidate memory, data movement, and output are not free. The O(N) per-sample claim requires T=O(N), prepared admissible roots and the stated arithmetic model. It is not an end-to-end Fourier construction or bit-complexity result.

The already accepted routing correction remains intact: either charge every interstage shuffle in the same cross-rank budget or factor its residual outer permutation and transport the target cut. The N=12 half-swap counterexample still refutes uncharged routing. The parity full-rank block statement requires N=2m with m odd. The seed correction may leave the original Green grammar and must be charged in affected cuts.

## Independent controls and publication boundary

The accompanying small-control record checks the N=2 Weyl average, all 16 two-coordinate four-phase probes, a rational 3/5–4/5 positive-attainment example, and the exact zero-critical swap boundary. These supplement the written arguments; they are not a replay of historical research programs or a numerical proof of the general statements. No supplied code was executed, imported, installed or compiled. No large solver was used.

Publication may include this report, its source identities, the compact small-control result, and the exact scoped verdict. Raw native preimages, private workspace locators, complete external papers, and unrelated historical archives are excluded. The eventual spreadsheet writer must recheck current stable IDs and preimages, preserve each cell's history, formulas, links, formatting and numeric priorities, and independently verify readback. This review is not itself an external-write authorization.

The accepted additional comparison-summary prefixes in novelty P81/T81/P91/T91 prevent stale current text from saying that no primary comparison has been completed. They retain each earlier statement verbatim as dated history. Numeric novelty scores and historical priority classes are unchanged. `ACCEPTED_CELL_PREFIXES.json` provides only reviewed new text, exact cell addresses and preimage hashes; it deliberately omits the native old values.
