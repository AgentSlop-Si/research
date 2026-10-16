# M-CONJUGATED-FEEDBACK and ALG-035: named comparison gates

Date: 16 October 2026. Repository baseline: `0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4`. Workbook: `1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU`. Mode: local candidate for independent review, no external writes.

## Disposition and exact scope

Two previously unfinished **source-specific comparisons** reach a proposed stopping point through explicit formula/hypothesis maps and qualified nonmatches. This is not closure of either research record. M-CONJUGATED-FEEDBACK remains TO RESEARCH at priority 34; ALG-035 remains TO RESEARCH at priority 12. No new theorem, implementation, replay, worldwide-priority or unrestricted lower-bound acceptance is proposed. In the earlier remaining-gate inventory, M-CONJUGATED-FEEDBACK's primary gate is constructive mathematical work and its comparison is secondary. Only that secondary named comparison is completed here; its primary gate remains open. ALG-035's inventory comparison had no named theorem selected until this pass.

The live owners are Catalogue 109 / novelty 154 / overview 223 and Catalogue 165 / novelty 203 / overview 291. Their current action explicitly requests the comparisons below. Their stop permits an exact primary-theorem hypothesis/formula/cost mapping or qualified nonmatch. These comparisons therefore do not replace the harder accepted-scope successors with easier mathematical tasks. The construction and precision successors remain open and are made explicit in the proposed leading text.

All six complete live owner rows, their notes and full accepted-scope/history fields were inspected. All five linked research bodies, including ALG-035's supplemental theorem and independent audit, were read in full as inert text. Relevant REVIEW-10 and REVIEW-17 per-ID outcomes were also read. Five repository bodies were fetched at the stated baseline. `SOURCE_BINDINGS.json` records exact export hashes, Git blob identities and locators. The Phase5 audit's historical name begins `470f9e5e…`; its published sanitized export is `d96fdb7f…`. These are different identities, not a new recovery claim.

No supplied program was executed, imported, installed or parsed as code. No numerical solver, new experiment, benchmark or external mutation was used. The algebra below compares statements; already accepted identities are not counted as new proof.

## 1. M-CONJUGATED-FEEDBACK

### Accepted owner scope, preserved

The pinned review assumes an invertible A and C, J²=I over characteristic different from two, nonzero λ with λ²≠1, and legal Cayley denominators. It proves the conjugated-involution feedback equivalence; the direct-Cayley commutator condition; and an explicit even-N cheap noncommuting closure control. The control is excluded from Fourier by a cut-rank bound for even N≥12. N=10 remains a threshold equality, not an exclusion.

The existing remaining obligation is simultaneous Fourier compatibility, paired-Green membership of A and B, and uniformly cheap setup. A five-factor supplied B representation proves no exclusion of all alternative two-Green representations. Those statements remain unchanged.

### Named primary matrix-function comparison

[Higham's author manuscript, Functions of Matrices (2006)](https://eprints.maths.manchester.ac.uk/310/1/fm_final.pdf), § 1 interpolation definition (4) and Facts 1, 2, 5, 6, formulates matrix functions through the Hermite interpolation polynomial, with similarity invariance and diagonalizable evaluation. This is the exact classical functional-calculus result used here. Its complex-matrix formulation supplies neither a cheap similarity constructor nor a finite-field numerical theorem.

The following substitution and algebra are this report's owner-specific mapping. Put H=CJC⁻¹ and K=BA=λH. Then H²=I and

    P+ = (I+H)/2,    P− = (I−H)/2.

These are complementary algebraic spectral projectors: P±²=P±, P+P−=0, P++P−=I, and K=λP+−λP−. They need not be orthogonal projectors. If J is nonscalar, the minimal polynomial is (z−λ)(z+λ), whose roots are distinct under the owner's guards. Scalar J is the already-retained degree-one branch.

Take f(z)=z/(1−z). The pole is outside the two-point spectrum because λ²≠1. Interpolation gives

    f(K) = [λ/(1−λ)]P+ − [λ/(1+λ)]P−
         = (K+λ²I)/(1−λ²)
         = C[(λJ+λ²I)/(1−λ²)]C⁻¹.

Since B=KA⁻¹, the actual transfer is

    (I−BA)⁻¹B = f(K)A⁻¹ = CΔC⁻¹A⁻¹.

The right-hand A⁻¹ cannot be commuted past the other factors. This identifies the accepted resolvent formula as a two-point functional-calculus specialization; it supplies no extra admissible-factor theorem. The same polynomial equalities can be checked algebraically in the owner's allowed fields, but the complex numerical comparison is not transferred there.

The Cayley formula has the same rational-functional-calculus nature: for U=(I+aW)(I−aW)⁻¹, lawful denominator, a≠0 and characteristic≠2,

    U+I=2(I−aW)⁻¹,
    W=a⁻¹(U−I)(U+I)⁻¹.

Thus polynomial/rational commutation properties apply under those guards. The previously accepted direct ansatz's noncommuting-order failure and zero-parameter exceptions are not reclassified as a new theorem in this comparison.

### Schur comparison: a specific applicability failure

[Davies–Higham (2003)](https://eprints.maths.manchester.ac.uk/156/1/paper.pdf), eqs (1.1)–(1.4) and Algorithm 5.1, uses similarity, reordered Schur blocks and Sylvester recurrences. Algorithm 5.1 requires f analytic on a closed convex set whose interior contains the spectrum, and derivative evaluation. Its stated dense cost depends on the eigenvalue distribution, roughly 28n³ to n⁴/3 flops. Scalar Parlett recurrence has repeated-eigenvalue failures; block treatment separates spectra. The paper also discusses amplification by an ill-conditioned similarity.

For the owner's concrete nonscalar λ=2 control, the spectrum is {−2,2}. Every convex set containing these points contains1. Therefore **f(z)=z/(1−z) fails Algorithm 5.1's stated convex analytic-domain hypothesis**, despite being well-defined on the spectrum. This is a qualified nonmatch to that particular generic algorithm, not a rejection of the feedback identity or of all matrix-function methods.

One may instead use the entire polynomial p(z)=(z+λ²)/(1−λ²), because the supplied annihilator proves p(K)=f(K). That substitution repairs the analytic-domain issue but does not discover K, verify unknown closure for free, or construct Fourier-compatible A/B. Its linear degree already makes a general Schur reduction unnecessary once the exact relation and actions are supplied. No claim that the expensive generic algorithm is a lower bound on structured evaluation follows.

### Full cost and hidden-oracle check

The original accepted evaluator is

    Tx = (Bx + B A Bx)/(1−λ²).

It uses two B actions, one A action and O(N) vector arithmetic after the plans and the exact closure certificate are supplied. It does not require applying A⁻¹ or C during each evaluation. Conversely, directly applying CΔC⁻¹A⁻¹ requires all inverse/conjugation actions, their preparation and coefficient access. Cheap forward A alone supplies none of those inverse costs. A general dense Schur representation also has dense input/storage/setup work; the generic comparison provides no O(N) structured constructor.

For a target F, the formal rearrangement A=F⁻¹CΔC⁻¹ embeds the target inverse and is not a paid construction algorithm. In contrast, the accepted explicit control defines its cycles, permutation, U, Z and C=UZ without Fourier data; it is a genuine cheap noncommuting control, but its own cut-rank certificate prevents Fourier equality in the stated N≥12 range. These two cases must not be conflated.

Disposition: the named classical matrix-function/Schur comparison is complete as an exact algebraic match and a specific algorithm/constructor nonmatch. It establishes no historical priority for the combined architectural control. The remaining Fourier compatibility, paired-Green membership, setup and numerical/bit-cost questions remain open. Further comparison work must name a genuinely different theorem or construction rather than replay this one.

## 2. ALG-035

### Accepted owner scope, preserved

For Q=KM, the complete phase summaries are an invertible coordinate change. Their shared exact aggregate is the already-attributed mixed-radix Cooley–Tukey endpoint with O(Q log Q) scalar work and O(Q) storage under supplied root/phase contracts. Creating and then undoing summaries cannot be treated as free. No new fast exact algorithm was established by removing the separate Green scans.

The audit distinguishes three maps: the normalized local summary transfer has singular values1; the physical raw-input-block map into its M selected Fourier outputs has singular values1/√K; and the complete normalized-summary synthesis z=D/√M→U_Qx is unitary. For s<M phase rows the unbiased fixed-subset estimator is (M/s)E_S, with exact operator error max(1,M/s−1) and mean-square error (M−s)||x||²/s under uniform sampling. The full-frame endpoint s=M is exact before separate Gaussian-filter/rounding biases. Determinant claims retain their input-basis and explicit-intermediate restrictions.

These results and the Cooley–Tukey, rank, sampling and bounded-coefficient attributions are already accepted. They receive no new completion credit here. The named unfinished comparison is whether a sparse-Fourier recovery theorem supplies the owner's exact all-input endpoint or bypasses its stated rank/error limitation.

### Named sparse-recovery source and contract

[Nakos–Song–Wang, arXiv:1909.11123v1](https://arxiv.org/pdf/1909.11123v1), Theorem 1.1, § 1.5, Algorithm 3 and Theorem A.16, gives frequency-sparse recovery with normalized-DFT error ||X−y||∞≤||X₋ₖ||₂/√k, O(k)-sparse output and polynomially high probability for each fixed input. It uses O(k log k log Q) time-coordinate samples and O(Q log³Q log k) stated arithmetic time, supplied noise-scale/SNR information, and neglects FFT roundoff. One-dimensional arbitrary Q is included. Version 1 prints μ=||X₋ₖ||₂/k in A.16 but uses /√k in the algorithm and surrounding derivation; its informal SNR wording also differs. This comparison is conditional on the explicit algorithm convention μ=||X₋ₖ||₂/√k>0 and polynomial R*≥||X||∞/μ. It does not silently repair the source or admit zero-tail cases.

### Exact-target nonmatch

Write X=U_Qx and E_k=||X₋ₖ||₂. A nonzero allowed error E_k/√k is not the exact identity y=X required for arbitrary x by the complete-frame record. Generic inputs have E_k>0 for k<Q. Substituting k=Q produces μ=0, so the stated positive-noise/SNR interface does not supply an exact all-input limit. An exact sparse special case or a separately implemented dense fallback would need its own source and costs. Neither is silently imported.

The frame parameter s counts selected phase subspaces per block. The recovery parameter k counts allowed output frequencies. They are different resources. No equation k=s or k=sK follows from either theorem, and no source-bound compiler from NSW queries/decoder to s selected Green phase rows is supplied.

### Norm/scale map, with quantifiers kept separate

The following are deductions for comparison, not new accepted sampling theorems.

1. The sparse-recovery inequality alone yields

       ||X−y||₂/||x||₂ ≤ √(Q/k) E_k/||x||₂.

   Thus a target relative-l₂ tolerance ε requires an additional tail inequality E_k≤ε√(k/Q)||x||₂ if it is to follow from this particular conversion. This is a sufficient inference, not a necessary condition on the algorithm's actual error. On a flat-magnitude spectrum, the converted upper bound is √((Q−k)/k), so obtaining ε through this bound needs k≥Q/(1+ε²). This does not lower-bound NSW runtime or refute its stronger sparse-recovery interpretations.

2. For the already-accepted uniform phase-subset estimator, RMS relative-l₂ error≤ε is exactly the condition (M−s)/s≤ε², or s≥M/(1+ε²). This is an expectation statement. It is not a high-probability guarantee, and constant s cannot make that RMS error vanish as M grows. The fixed-subset operator error remains at least1 whenever s<M.

3. For an illustrative Q-length weak per-bin scale with fixed 0<α<1/2, E_k≤||x||₂ and k=ceil(Q^(2α)) imply error≤Q^−α||x||₂ when the comparator interface is admitted. This does not answer the exact ALG-035 target or transfer the original-N padded/weighted Gaussian contract. Also, the direct conversion to relative-l₂ gives Q^(1/2−α), which does not tend to zero. A weak all-bin norm bound must not be called exactness or useful vanishing relative-l₂ accuracy merely because its scalar multiplier shrinks.

4. The unitary synthesis's fixed-rank spectral error concerns one fixed linear operator acting uniformly on all inputs. NSW's output support, thresholds and decoder depend on data; a k-sparse output is not a fixed rank-k linear input-output map. Its per-fixed-input probability does not assert one seed works on every input. Therefore the accepted local/global rank-deficiency argument cannot simply be applied to that nonlinear recovery algorithm. Conversely, NSW does not supply the per-block pathwise rank deficit, retained-measurement grammar and absence of extra information needed to substitute into the separate Gaussian compressed-input obstruction. The dimensional count cannot be transferred from the output sparsity label alone.

### Paid work and remaining gate

The exact frame evaluator pays summary formation/recovery, both transform-axis banks, twiddles, roots/phase access, storage and all Q outputs. The recovery comparison has a different input-access and output contract. Exposing its sparse answer as all Q explicit bins adds O(Q) writes/storage. Obtaining the required noise information is not certified as free preparation. The source's repeat-until random-shift runtime is controlled on its high-probability analysis event, not by a deterministic cap supplied here. Its given arithmetic upper bound supplies no o(Q log Q) exact circuit, finite-word precision proof, fair-bit/abort contract or production speed comparison. Comparing these upper bounds is not a universal speed ordering.

Unitarity of the exact frame controls exact conditioning, not twiddle generation, phase-integer overflow, floating arithmetic, all-length FFT error or Gaussian pre/postweight effects. The owner's numerical successor remains open. The generic separate-scan bill is O(Q log Q+QM); its reduction to O(Q log Q) outside the joint-identity execution requires the intended M=O(log Q) regime. The full joint evaluator and the historical separate scans are not silently equated.

Disposition: the named NSW comparison is complete as a qualified approximation/interface/quantifier/cost nonmatch to the exact phase-frame target. The cheaper global input-independent output-only Fourier circuit and certified numerical realization remain unsupplied. This comparison does not reopen or recount the complete-bank collapse, fixed-rank proof, finite-population identities or determinant gate as new work.

## 3. Minimal exact local proposal

`NATIVE_CELL_PROPOSAL.json` contains fourteen prefix-only edits: Catalogue AE/AF, overview P/Q/F, and novelty Y/Z for each selected stable ID. The F overlay prevents the finished named comparison from remaining the leading task. Each edit includes its exact current preimage and the full replacement text formed by prepending the new block to unchanged history. No statuses, scores, proof/novelty fields, formulas, notes, links, validation or formatting are to change.

Application requires independent acceptance, a fresh exact-preimage read and report publication. A changed preimage must be reconciled rather than overwritten. No native write is part of this candidate. The independent reviewer should check the source-version guards, λ=2 analytic-domain mismatch, positive-noise endpoint restriction, nonuniform/fixed-linear distinction, the actual remaining owner obligations, and exact history preservation before authorizing the proposed narrow update.
