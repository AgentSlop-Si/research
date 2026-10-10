# Primary comparison and novelty dispositions

Date: 10 October 2026. Comparison means the stated portions of primary texts were read, not that all related literature has been exhausted. Mathematical correctness, practical performance, and priority are separate questions. No supplied software was run.

## F015: certified growing-fiber Fourier algorithm

### Exact surviving theorem

For N=2^k, Q=2^floor(k/2), M=N/Q, supplied roots in an exact field, cap b≤M/2: identify and completely verify at most b modes in each of Q raw strided M-fibers, then return every Fourier coefficient. The charged bound is O(N log(b+2)+Qb²), space O(N). The aggregate-budget sibling allows heavy fibers by paying ordinary transforms against an actual discovered mode count, including one final over-budget fiber on rejection. These are structured-input success-or-rejection theorems, not all-input exact speedups. Original source inspected: novelty_catalogue_0825/master/fft_research_master_20261009/additions/0155_material_coverage_and_new_results/reviews/review_growing_fiber/source/THEORY.md, §§1–10.

### Primary comparators read beyond abstracts

1. FFTW authors, *Pruned FFTs*, https://fftw.org/pruned.html. Opening discussion and the first-K-output construction state the O(N log K) arithmetic savings and input/output duality, and distinguish arithmetic savings from measured performance. This directly precedes F015's pruning lemma. The source does not supply F015's blind per-fiber recognition and rejection contract. Its engineering caution agrees with the project's lack of a measured speed win.

2. Briani–Cuyt–Lee, *A hybrid Fourier-Prony method* (2017), https://arxiv.org/pdf/1706.04520, §§3–5, equations (9)–(16). The method uses shifted undersampled DFTs and short exponential-recovery problems to resolve collisions, including a Hankel-based count and a Vandermonde recovery step. These are close classical mechanisms. F015's exact supplied-grid root scan, full N-entry verification, arbitrary violating-input rejection budget, and growing b cost are not stated in those sections. The paper discusses noise sensitivity rather than proving F015's exact-field all-size rejection theorem. This is a precise difference in the inspected text, not evidence of novelty elsewhere.

3. Bringmann et al., *Traversing the FFT Computation Tree for Dimension-Independent Sparse Fourier Transforms*, https://arxiv.org/html/2107.07347, §2 and Theorem 1, plus §§3 and 5. The exact recovery result is deterministic, oracle-input, globally k-sparse in the final Fourier domain, and near quadratic in k up to its explicit subpolynomial/polylog factors. Its base side length is a power of two; exact complex arithmetic is the declared model. F015 instead permits a dense final spectrum with sparse internal strided fibers, reads all data, and certifies rejection. Applying global sparsity recovery to each fiber remains a comparator but does not produce F015's stated N log b+Qb² bound without the separately classical pruning/certification steps. No conflict with that paper's restricted conditional non-equispaced-transform lower bound follows.

### Second-pass disposition

F015 remains a correct, useful recognition/pruning package with a project-relative growing-budget improvement. “Fourier plus Prony,” “discover modes,” and “prune the FFT” cannot be advertised as new ideas. The credible candidate increment is the complete charged interface for sparse intermediate fibers, including synthesis sharing and the aggregate rejection ledger. Priority for that exact interface is unresolved. Numerical robustness, root/field discovery, finite-bit cost and hardware crossover remain open, not implicitly granted by the exact-field proof.

The same proof mechanism now improves FUS-05 recognition on dyadic lengths (STRUCTURED_THEOREMS.md S2). Application to arbitrary fresh dense x stays O(Nr) or an ordinary FFT alternative; faster recognition does not speed a different operator application for free.

## F016: all-length Gaussian weak-error approximation

### Target contract, not a stronger substitute

The existing F016 theorem has per-fixed-input probability 1−N^(−c), weak unitary coordinate error C_alpha N^(−alpha)||x||₂ for fixed alpha<1/2, ideal supplied-constant arithmetic, and O(N log log N) work with dense output. It is neither relative per-bin error nor relative-l2 error. No binary64 implementation theorem was previously established. Source inspected: novelty_catalogue_0825/master/fft_research_master_20261009/additions/2020_2027/gaussian_crosscheck/GAUSSIAN_ALL_LENGTH_AUDIT.md, Gaussian identity, rough padding, complexity, and random quantifier sections.

### Primary HIKP comparison

Hassanieh–Indyk–Katabi–Price, *Simple and Practical Algorithm for Sparse Fourier Transform*, https://people.csail.mit.edu/haitham/Papers/sFFT.pdf, §3 and §4.2, especially Lemma 4.3 and Theorem 4.4: the actual theorem is pointwise l∞/l2, with an additional Fourier-l1 leakage term. This already dominates the dyadic weak-accuracy headline after normalization and dense zero filling. The paper also explicitly discusses general n after Lemma 3.6, predicting only a totient-factor runtime loss. However, Claim 3.7 and the displayed inner loop require B dividing n; those lines do not detail the prime-length bucket construction. This limits how mechanically one can quote a complete all-length implementation from the inspected text, and it also precludes claiming that general lengths were conceptually absent from prior work.

S6 proves an explicit alternative transfer using only the fully stated dyadic primitive, centered interpolation, and sparse scatter. The transfer is a research-cycle derivation, not a assertion that its exact form was already published.

### Other primary comparators

- Nakos–Song–Wang, *Nearly Sample-Optimal Sparse Fourier Transform in Any Dimension; RIPless and Filterless*, https://arxiv.org/html/1909.11123, Theorem 1.1 and §1.5. It allows arbitrary integer side length, has an l∞/l2 guarantee, near-linear time with unspecified polylog factors in the shorthand, and a polynomial signal-to-noise bound. This is substantial all-length weak-accuracy prior art; its displayed theorem alone does not give O(N) dense output at every alpha<1/2. Numerical rounding is assumed negligible. Do not equate its sample complexity with runtime or erase its SNR premise.
- Kapralov, *Sparse Fourier Transform in Any Constant Dimension with Nearly-Optimal Sample Complexity in Sublinear Time*, https://arxiv.org/html/1604.00845, the stated power-of-two model, Lemma 10.1 and Corollary 10.2. The semi-equispaced primitive approximates selected bins with a charged sparse-input and output-transform cost. It is directly relevant filtering/interpolation technology, but the inspected statement uses dyadic side length and does not by itself supply F016's arbitrary-length Gaussian arithmetic contract.

### Revised disposition

The general weak-approximation headline has strong classical antecedents. The dyadic case was already non-novel. This cycle's explicit all-length O(N) fusion removes O(N log log N) at the same weak scale as a compelling performance headline for F016 within the inherited ideal-arithmetic scope. The HIKP general-n remark further narrows any plausible originality claim. What remains potentially worth retaining is a specialized Gaussian/Green derivation, a transparent all-length implementation/model account, or a future genuine numerical robustness result. None is priority-cleared.

Do not upgrade S6 to a certified fixed-word theorem: its sparse recovery engine still carries the original mathematical arithmetic assumptions. The new interpolation coefficients are certified, but that is not a certificate for every arithmetic step in the sparse engine.

## FUS-04 through FUS-08

- FUS-04: paid scalar balancing and finite template compilation are classical perturbation/tabulation interfaces. The non-Fourier instantiation and coefficient/certificate cost remain the concrete follow-on.
- FUS-05: exact Prony, partial fractions, input pruning, and Fourier orthogonality account for the theorem. The raw-input contract is useful; neither full operator rank nor number of rank-one summands is a runtime lower bound.
- FUS-06: Batenkov–Diederichs–Goldman–Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*, https://arxiv.org/html/1909.01927, §2.3, Theorems 2.2–2.3 and Corollary 2.1, gives the multiplicity-by-exponent profile for clustered unit-circle nodes, not merely the smallest singular value. The full relevant theorem statements and divided-difference appendix were freshly read. Accordingly, the full-profile extension in S3 is explicitly a classical confluent-coordinate result specialized to the guarded RS family, not a newly discovered spectral principle. Unit-circle growing-bandwidth estimates and our fixed-degree complex-root asymptotics must not be conflated.
- FUS-07: the early-exit criterion is Pythagoras plus a paid projector and energy calculation. Its value is executable certification on a concrete accepted family.
- FUS-08: finite-orbit interpolation supplies arbitrary finite-probe counterexamples. Retain as a verification warning. It does not say the actual tabulator is wrong or establish a runtime lower bound.

## Decisive remaining gaps

1. Identify an explicit non-Fourier numerical circuit for S1 with efficiently certified envelopes and genuinely few scaled templates.
2. Implement the eager, bounded-budget S2 recognizer and validate arithmetic counts separately from runtime.
3. For RS, compute constants for one guarded family and compare actual prescribed weight sensitivity to worst-case moment sensitivity.
4. Produce a numerical implementation theorem for the HIKP engine plus sparse all-length transfer, or transparently keep the ideal arithmetic model.
5. Examine whether HIKP's general-length divisor adaptation is specified in a companion or subsequent primary paper. No negative search is a novelty proof.
6. Search theorem-level intermediate-fiber recognition/aggregate-budget antecedents before promoting F015 as externally original.
