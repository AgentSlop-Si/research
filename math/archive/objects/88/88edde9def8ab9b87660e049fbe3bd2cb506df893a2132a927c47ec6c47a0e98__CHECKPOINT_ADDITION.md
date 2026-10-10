# Endpoint rank checkpoint addition

Source: `fft_optimal_endpoint_rank_gate_2026-10-09(1).zip`, Library ID `[private-id]`, version 0, 500406 bytes, SHA256 `0aab4233b4ccf709ace8cca81fbe6e8d0f3645e9227b4c8c60e91efd2fe59bc5`.

Accepted over C: for dyadic N>=8, the exact minimum quasiseparable rank of a Fourier matrix over arbitrary independent input and output permutations is N/4+1. Double bit reversal attains it. Its exact cut-rank recurrence and parity-dependent total-rank formula are correct, and its total is asymptotically optimal with leading term N^2/6.

Independent bounded addition: at every odd cut k, rank is at least ceil(k(N-k)(N+1)/N^2); at even cuts it is at least ceil(k(N-k)/N). These bounds match bit reversal pointwise for N=8 and N=16, proving exact minimum upper-right total ranks 14 and 48. They do not settle finite-size total optimality for larger N.

The older two-stage natural/affine-input theorem N<=9r^2+7r retains its original endpoint restriction. The new one-matrix optimum does not broaden that theorem. At r=1, the prior N<=16 result is necessary-filter sharpness, not factorization existence. Arbitrary input permutations still require actual Fourier submatrix ranks.

For common-coordinate-order products, q(product)<=sum q(factors), so s stages each of rank at most r require sr>=N/4+1. Uncharged interstage permutations or differently ordered stage representations prevent applying this deduction directly. Rank is not an arithmetic-cost lower bound.

Independent standard-library checks passed across GF(257), GF(12289), GF(65537), including 435 direct cuts, all 9,408 critical N=8 minors, 288 random larger critical minors, 672 coset identities, and rational/profile formulas through N=32,768. The characteristic-zero lower bound is established by proof, not inferred from these fields.

The N=8 screens were also independently reproduced over GF(12289): interval-window 15,728 survivors; subset 31,384; optimized support 15,728 with identical survivor set; first-trace uncertainty 40,320. Thus none improves the previous window filter at this size. The uploaded standalone subset script has a sibling-import portability issue, avoided in the independent checker.

No uploaded code was executed or imported. All source manifest entries and the nested prior archive hash were verified. No new exact fresh-arbitrary-input FFT evaluator, fully charged complexity improvement, unrestricted circuit lower bound, or novelty claim follows.
