# PR622 repacking comparison audit

12 October 2026 UTC. Original archive unchanged. Bounded source comparison and fresh exact arithmetic only; no supplied program was imported or executed. Independent mathematical review accepts the bounded profile comparison; it does not claim a second numerical reconstruction.

## Result

The candidate archive's corrected comparison is supported. For the stated native-complex moment model, the threshold ordering is **PR623 > candidate > PR624**. Eight fresh strict rational moment checks establish this numerical ordering from the exact recorded profiles. This does not certify any owner map, full upstream pipeline, all-size compiler, practical FFT speedup, integer-multiplication kappa, or algorithmic originality.

The candidate improves its pinned PR622 profile but is surpassed by a directly comparable published PR623 profile. Its corrected README already withdraws its earlier novelty/current-best implications. Keep that correction prominent; do not present the finite repacking as a new complete FFT algorithm.

## Exact sources

Candidate: [FFT_PR622_Repacking_Candidate_2026-10-13.zip](sources/FFT_PR622_Repacking_Candidate_2026-10-13.zip), SHA-256 afb3280fda31e1a26e72d4dabf7870b9433ceef366114e66151be5e85ef4a05a. Inspected README, PR623_PR624_COMPARISON.json, candidate PROFILE.json and baseline EXPECTED.json as data. The candidate's owner maps and full provider/replay pipeline are outside this audit.

[PR623](https://github.com/CrocSwap/integer-mult-bounds/pull/623) uses a changed owner allocation and ck/jp8 dispatch on the same PR622 construction. Its author describes a fresh replay but explicitly retains conditional algorithmic assumptions. The complete pinned [EXPECTED.json](https://github.com/jeremykothe2/integer-mult-bounds/blob/e39a615ca601ce5d62abeb24f3fcdb8644ca1005/research/complex-571-cold14-k492b/data/EXPECTED.json) was retrieved at commit e39a615ca601ce5d62abeb24f3fcdb8644ca1005. Its Git blob SHA-1 is 8fe7f49fac1d8fe96f8ecd19b51ce94be28288d0; file SHA-256 is 4dbca2078028cb0d88fa34c35c4ec4ab2a05ad2ec742d9ea615733938aca236d.

[PR624](https://github.com/CrocSwap/integer-mult-bounds/pull/624) retains the PR622 dispatch, records an owner-repacking improvement, and explicitly acknowledges PR623's stronger reported result. Its full [EXPECTED.json](https://github.com/jeremydiviney/integer-mult-bounds/blob/036753ed33d4e620932262646e3d02a1927256a6/research/complex-571-cold14-k492/data/EXPECTED.json) was retrieved at commit 036753ed33d4e620932262646e3d02a1927256a6. Git blob SHA-1 ffc5ad2aa36839e24544bfc045fbe60f80ac270d; file SHA-256 d249fc437bdb85f551a18c650222f5ca3d67974db74b23b4829cc8baeac2655c.

Both pinned files' complete `global` objects match the archived comparison. Source authors' replay claims were read, not independently rerun. No assertion that the current unpinned branch has remained unchanged is required.

## Numerical theorem

For a nonnegative finite rank profile H supported on integers 1<=r<73, define

Phi_H(b) = sum_r H[r]*(r/73)^(1-b)/7168.

All four recorded profiles (PR622 baseline, candidate, PR623, PR624) have rank mass 520704, live stock 7168 and dimension 73, hence deficit 2560. In particular Phi_H(0)<1. Each term is strictly increasing in b and at least one term is present; Phi_H tends to infinity as b tends to infinity. Thus each profile has a unique real threshold Phi_H(b_H)=1.

The candidate-minus-baseline profile is exactly e_1-4e_3+2e_16-e_21, which preserves rank mass. Fresh rational enclosures give:

- PR622 baseline threshold lies strictly between 0.001638101302431117748332 and 0.001638101302431117748333.
- Candidate threshold lies strictly between 0.001638113483700526508299 and 0.001638113483700526508300.
- PR623 has Phi<1 at 0.001638169876460961469484, above the candidate's upper endpoint.
- PR624 has Phi<1 at 0.001638104468552563164027 but Phi>1 at the candidate's lower endpoint.
- The candidate has Phi>1 at the PR623 tested saving.

These signs prove PR623's threshold exceeds the candidate's, which exceeds PR624's. Merely comparing feasible lower bounds would not prove threshold ordering; the additional cross-profile signs supply the required upper comparisons. The numbers here are native-complex moment savings b. The kappa quantities in the PR titles are different parameters and are not substituted for b.

## Independent rational arithmetic

`pr622_moment_comparison_check.py` reads only JSON members of the candidate ZIP and the two pinned EXPECTED files. It verifies the source Git blob hashes, comparison equality, profile delta and four rank masses. It then reconstructs every moment interval without importing the archive's moment engine.

Write each term as r*H[r]/(73*7168) times exp(b*log(73/r)). To bound log(x), reduce x by powers of two into [1,2] and use the positive atanh expansion with z=(x-1)/(x+1). Ninety terms have upper tail at most 2*z^181/(181*(1-z²)). Bound log(2) the same way. Outward rounding on the rational grid 10^-70 preserves each enclosure.

For 0<=t<1/100, retain exp(t)'s Taylor polynomial through degree 25. Its remaining positive tail is at most [t^26/26!]/[1-t/27]. Evaluating the lower polynomial at the lower endpoint and the polynomial plus tail at the upper endpoint gives exact Fraction enclosures. Every reported sign is strict against rational endpoints, not inferred from a displayed decimal.

Reproduce with:

python pr622_moment_comparison_check.py sources/FFT_PR622_Repacking_Candidate_2026-10-13.zip sources/PR623_pinned_EXPECTED.json sources/PR624_pinned_EXPECTED.json

The result file records full rational bounds for all eight comparisons. The supplied moment program, optimizers, pickle, owner verifiers and upstream software were not run.

## Status boundary

This closes only the pinned-source and numerical-profile comparison under the separate independent mathematical review. Candidate map legality, claimed preserved local semantics, the fresh full admission/invoice/assembly pipeline, and all conditional Fourier/bit transfers remain unaccepted in this audit. The original corrected author status is preserved. For the stated novelty objective, retain a low priority unless a distinct question requires the finite packing certificate.

## Independent review

`pr622_independent_review.md` accepts the monotonicity argument, rational tail bounds and threshold comparison. The eight exact numerical evaluations are the fresh checker's results; the reviewer did not perform a second numerical reconstruction. Owner-map and full algorithm claims remain outside scope.
