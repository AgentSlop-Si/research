# Frozen constructor deliverables for checkpoint20

All original bundles and seals are unchanged. This inventory is intended for preservation and later sorting, including positive controls, narrowly scoped negative results and unresolved operations. No uploaded code was executed.

## Coverage

- 13 frozen bundles; 52 files including their original seals.
- 7 report hashes are absent from the v19 manifest; 6 already appear as reviewer snapshots.
- Across all original files, 46 hashes are absent from v19. Preserve full bundles even where a report snapshot already exists.
- Comparison uses exact content hashes, not filename or assumed creation time.
- Every original payload seal, plus all six linked review payload seals, was independently rehashed by this inventory builder.
- Detailed per-file hashes, sizes and v19 matching paths are in the companion JSON.

## Reports absent from v19

6. Nonzero-mask butterfly control: `research_round_2156/joint_orbit/iteration_9_bank_interface/NONZERO_MASK_BUTTERFLY_CONTROL.md`
8. Fourier-4 positive kernel and Fourier-8 commuting chart: `research_round_2156/joint_orbit/iteration_9_bank_interface/FOURIER4_GREEN_KERNEL_AND_FOURIER8_CHART.md`
9. Fourier-8 noncommuting anchor certificate: `research_round_2156/joint_orbit/iteration_9_bank_interface/FOURIER8_NONCOMMUTING_ANCHOR_CERTIFICATE.md`
10. Root-pole cancellation and linear tree jet: `research_round_2156/joint_orbit/iteration_10_marked_tree/ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md`
11. One Schur step and two-run jet: `research_round_2156/joint_orbit/iteration_10_marked_tree/ONE_SCHUR_STEP_AND_TWO_RUN_JET.md`
12. Next-pivot tree and support reduction: `research_round_2156/joint_orbit/iteration_10_marked_tree/NEXT_PIVOT_TREE_AND_SUPPORT_REDUCTION.md`
13. Variable-bit block elimination and work: `research_round_2156/joint_orbit/iteration_11_variable_block/VARIABLE_BIT_BLOCK_ELIMINATION_AND_WORK.md`

## Complete bundle inventory

### 1. True bank-interface transport

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/BANK_INTERFACE_TRANSPORT.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/SHA256SUMS.txt`
Report SHA256: `b8db92bd7ec6f0cd910f4487fd2f03ea4f18927b7e0ef4015e0f098be96e216b`
v19 report membership: already present as an identical snapshot.

Positive Weyl transport and exact Cooley-Tukey control; negative maximum-row or maximum-column degree obstruction for a proper mixed bank. O(N) total nonzeros are not excluded.

Cost/scope boundary: The actual interface actions must satisfy the sparsity hypotheses. A larger sparse state lift does not suffice. The control exterior retains batched Fourier work.

Independent review: Accepted within the stated actual-action and mixed-bank hypotheses.
Review seal: `research_round_2156/review_bank_interface_certificate/SEALED_MANIFEST.sha256`; manifest SHA256 `a556684c983923dd056ee9c4a0abf3a475fe7180b832d4fe5699e6852a9e3d92`.

### 2. Fixed-interface exterior uniqueness

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/FIXED_INTERFACE_EXTERIOR_UNIQUENESS.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/EXTERIOR_UNIQUENESS_SHA256SUMS.txt`
Report SHA256: `44e2fec455a91c99c0de54952e9adba5535c947e5db691a8d725df075f4ac048`
v19 report membership: already present as an identical snapshot.

Both fixed Cooley-Tukey intertwining equations leave exactly scalar multiples of the known exterior; one calibration fixes the scalar.

Cost/scope boundary: Uniqueness of the operator does not rule out a cheaper factorization of that same operator. Matrix density is not an arithmetic lower bound.

Independent review: Accepted together with the batched equivalence review.
Review seal: `research_round_2156/review_batched_interface_equivalence/SEALED_MANIFEST.sha256`; manifest SHA256 `8bdf05bbc0acc25c4308320b587a8df5172a1a4f682e20aa3921fb58442965b7`.

### 3. Batched Fourier equivalence

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/BATCHED_FOURIER_EQUIVALENCE.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/BATCHED_EQUIVALENCE_SHA256SUMS.txt`
Report SHA256: `892d8abed1d33bf56970849ce710db648734598d2ca6aaf5263292ee9edf72a7`
v19 report membership: already present as an identical snapshot.

Full-active exterior is cost-equivalent to m arbitrary length-q Fourier transforms with O(N) overhead. Active-support routing gives charged partial-bank reductions.

Cost/scope boundary: Complement inverse transforms are paid. The original near-square extension in this report assumes m=rq; the opposite orientation is handled separately.

Independent review: Accepted with active-support-cover and fixed-radix scope.
Review seal: `research_round_2156/review_batched_interface_equivalence/SEALED_MANIFEST.sha256`; manifest SHA256 `8bdf05bbc0acc25c4308320b587a8df5172a1a4f682e20aa3921fb58442965b7`.

### 4. Original bank orientation addendum

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/ORIGINAL_BANK_ORIENTATION_ADDENDUM.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/ORIGINAL_ORIENTATION_SHA256SUMS.txt`
Report SHA256: `d11aa1b014b83726be5603d5af8c464ab0c9382228d07803020a39dfd6755b1d`
v19 report membership: already present as an identical snapshot.

For q=rm, packs the original q length-m bank transforms into one batch of m length-q transforms, then pays (N/r) inverse radix-r transforms and linear routing.

Cost/scope boundary: Linear additional work requires fixed radix r. No bank swap and no cheap exterior construction are supplied.

Independent review: Accepted as a separate additive theorem, including the original odd-exponent q=2m bank.
Review seal: `research_round_2156/review_original_bank_orientation/SEALED_MANIFEST.sha256`; manifest SHA256 `011bd8b2d0e78bdaf1540557c5130bb51a460e2570618bb0348960b4f0fe5d95`.

### 5. Changed interface constructions

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/CHANGING_INTERFACE_CONSTRUCTIONS.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/CHANGED_INTERFACE_SHA256SUMS.txt`
Report SHA256: `bc18b7d9be50ed6bfe0c08538047271469a77fd3109422c0ff3f9fe159f013ce`
v19 report membership: already present as an identical snapshot.

Exact interface gauge formulas, cheap constant-swap gauges, monomial-clock coset rigidity, and an admissible N=16 zero-mask butterfly construction.

Cost/scope boundary: A cheap gauge must include its bank conjugate and inverse. The finite control relocates ordinary Fourier work and gives no scalable improvement.

Independent review: Accepted within the full-bank and explicitly stated finite-control scope.
Review seal: `research_round_2156/review_changed_interface/SEALED_MANIFEST.sha256`; manifest SHA256 `f3a16b350d7be31bc404b7c8dedc17687adb46ea1343a9ef8e69eaeed5472c9c`.

### 6. Nonzero-mask butterfly control

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/NONZERO_MASK_BUTTERFLY_CONTROL.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/NONZERO_BUTTERFLY_SHA256SUMS.txt`
Report SHA256: `94b82c5cf3bd893ad5f2968772bf236eba07e849e17044a7ee5772cda72bc073`
v19 report membership: absent.

An explicit paired-Green expression for F2 with nonzero matching-edge masks; disjoint matchings can be stitched into Hamiltonian orders using zero connecting masks.

Cost/scope boundary: This is the known butterfly operation in an admissible grammar. Masks are not nonzero on every ambient edge, and no general FFT improvement follows.

Independent review: Constructor-sealed; no separate completed independent acceptance located for this exact report.

### 7. Monomial Weyl batch classification

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/MONOMIAL_WEYL_BATCH_CLASSIFICATION.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/MONOMIAL_WEYL_CLASSIFICATION_SHA256SUMS.txt`
Report SHA256: `f95505c0b0f3749d0ae218bb38e708c5eee0ac3b669f4958e63e42a8dd283c90`
v19 report membership: already present as an identical snapshot.

Monomial conjugates of both primitive Weyl generators force monomial equivalence to equal-size Fourier blocks. Promised-input coefficient recovery is linear from sparse actions, a supplied root, and one genuine calibration entry. Support consequence m*dP*dQ>=N.

Cost/scope boundary: Certifying the promise or obtaining actions/seed from a circuit is separately charged. Composite and dyadic cases allow intermediate block sizes. Sections 7-8 finite family claims remain outside the independent acceptance.

Independent review: Independent acceptance covers sections 1-6 and 9 only; sections 7-8 explicitly not independently accepted. Classical related literature cited; novelty not established.
Review seal: `research_round_2156/review_weyl_monomial_batch/SEALED_MANIFEST.sha256`; manifest SHA256 `a9bf59530bc3fa42eed4b8f855590f21e7a83a7f7475ee0ed540824587ccffd6`.

### 8. Fourier-4 positive kernel and Fourier-8 commuting chart

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/FOURIER4_GREEN_KERNEL_AND_FOURIER8_CHART.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/FOURIER4_KERNEL_SHA256SUMS.txt`
Report SHA256: `3d84a3e3eff27e0b23d076323ece07c68f543b3b7145cb4e0f96d2a842a6d6c9`
v19 report membership: absent.

Positive one-layer F4 paired-Green kernel with all cycle masks nonzero and explicit splitting/root/denominator guards. A narrow F8 commuting scalar-resolvent chart is excluded.

Cost/scope boundary: Finite kernel only; batching short cycles does not automatically give a legal full ambient Hamiltonian layer. The F8 exclusion does not cover general noncommuting layers.

Independent review: Constructor-sealed; queued for independent review.

### 9. Fourier-8 noncommuting anchor certificate

Report: `research_round_2156/joint_orbit/iteration_9_bank_interface/FOURIER8_NONCOMMUTING_ANCHOR_CERTIFICATE.md`
Original seal: `research_round_2156/joint_orbit/iteration_9_bank_interface/FOURIER8_NONCOMMUTING_ANCHOR_SHA256SUMS.txt`
Report SHA256: `adf1f838712db3e627f7c1ada4c05cdb8e35854055a96179adcfa5edbaf980f8`
v19 report membership: absent.

Eight fully specified fixed-anchor/order charts are rejected by exact projective direction gates, with positive Green controls and a complete coefficient budget.

Cost/scope boundary: No positive F8 two-layer kernel is found, and no unrestricted impossibility follows. The direction gate applies only after a target factor has been specified.

Independent review: Constructor-sealed; queued for independent review.

### 10. Root-pole cancellation and linear tree jet

Report: `research_round_2156/joint_orbit/iteration_10_marked_tree/ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md`
Original seal: `research_round_2156/joint_orbit/iteration_10_marked_tree/ROOT_POLE_CANCELLATION_SHA256SUMS.txt`
Report SHA256: `e3cd7602ca18450ed32c4e808de20fe036b61030b837511a768d22b6f3af6c7f`
v19 report membership: absent.

Exact pole-free bordered resolvent, an O(N) tree application and constant-input complete tree jet with 2N-2 coefficient slots, including the z=1 cancellation.

Cost/scope boundary: The coupled retained border inverse is unresolved. Neither coefficient extraction nor a marked scalar determinant identity is counted as a free algorithm.

Independent review: Independently accepted; review excludes later elimination stages and a fast retained inverse.
Review seal: `research_round_2156/review_marked_cycle_first_schur/SEALED_MANIFEST.sha256`; manifest SHA256 `0b6aaaf41f51c6eabcc863bc7d706211ca680449aaf41005e3432d95ec89ec3c`.

### 11. One Schur step and two-run jet

Report: `research_round_2156/joint_orbit/iteration_10_marked_tree/ONE_SCHUR_STEP_AND_TWO_RUN_JET.md`
Original seal: `research_round_2156/joint_orbit/iteration_10_marked_tree/ONE_SCHUR_TWO_RUN_SHA256SUMS.txt`
Report SHA256: `d9b0c4ac84adc5df1c04f414b7dcddd4c2384bbee82529e24e3e51f60e0bc157`
v19 report membership: absent.

One exact parity Schur step with a guarded tree pivot. A constant-input complete two-run numerator has at most 6N slots and an explicit O(N) shared quotient-state evaluator.

Cost/scope boundary: The pivot guard can fail while the full operator is invertible. Polynomial unknowns, repeated Schur closure and retained inversion remain unresolved.

Independent review: Independently accepted, including the shared quotient-state implementation and an independent exceptional-chart countercontrol.
Review seal: `research_round_2156/review_marked_cycle_first_schur/SEALED_MANIFEST.sha256`; manifest SHA256 `0b6aaaf41f51c6eabcc863bc7d706211ca680449aaf41005e3432d95ec89ec3c`.

### 12. Next-pivot tree and support reduction

Report: `research_round_2156/joint_orbit/iteration_10_marked_tree/NEXT_PIVOT_TREE_AND_SUPPORT_REDUCTION.md`
Original seal: `research_round_2156/joint_orbit/iteration_10_marked_tree/NEXT_PIVOT_SUPPORT_SHA256SUMS.txt`
Report SHA256: `a8d72bb99ddc752b35ffd5808c780c67b462ab65315946d5225f26a715389714`
v19 report membership: absent.

Exact next-pivot tree reference plus a growing-rank correction. Its explicit support permits a Woodbury reduction to N/32+1 marked coordinates; constant-input reduced-operator jets have an O(N) evaluator.

Cost/scope boundary: Only one bounded stage is proved. Ambient maps and marks remain carried; no closed shrinking family or cheap inverse is established. Formal-series guards have constant term one.

Independent review: Constructor-sealed; queued for independent review.

### 13. Variable-bit block elimination and work

Report: `research_round_2156/joint_orbit/iteration_11_variable_block/VARIABLE_BIT_BLOCK_ELIMINATION_AND_WORK.md`
Original seal: `research_round_2156/joint_orbit/iteration_11_variable_block/VARIABLE_BLOCK_SHA256SUMS.txt`
Report SHA256: `fd7bebda8cef672081412fdd92db1dcd474b1c9041d980ac7f051b94d040bcdc`
v19 report membership: absent.

Exact b-bit Schur/packet identities and finite-horizon frontier count S(N,b)=N*sum[t=b..n-1] A_b(t)/2^t+(b+1)*A_b(n), N=2^n. The specified full-frontier evaluator costs Theta(N*min(n+1,2^b)).

Cost/scope boundary: The matching lower bound belongs only to that evaluator. At b about log2(log2 N), its work remains Theta(N log N). The retained formal-series inverse and a closed smaller-state representation are unconstructed.

Independent review: Constructor-sealed; queued for independent review.

## Preservation instructions and stopping boundary

Copy the exact four files listed for each bundle, preserving their relative directory and original seal. Do not replace this with only the report: the authored verifier and frozen control output are part of the research record. The companion JSON lists all 52 source files. Reviewer bundles are separately linked and retain their independent acceptance boundaries.

The two latest constructor milestones are support reduction and variable-bit elimination. Both were sent to the latest-source reviewer for queued audit. The bounded construction is complete; the retained inverse is still unresolved, and no speedup is claimed.

The marked-cycle source was Library-discovered at 00:25 UTC, rather than part of a direct user upload. Its original ID and hash are recorded in JSON.
