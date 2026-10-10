# Sparse time-surrogate Fourier approximation: prior-art check

Checked 9 October 2026. This is a bounded primary-source search, not an exhaustive novelty certification.

## Verdict

I did not locate a paper stating exactly the proposed package: arbitrary fresh complex input, magnitude-proportional time sampling, a simultaneous additive max-bin guarantee, and all outputs computed through a sparse-input FFT in O(N log log N) for inverse-polylogarithmic accuracy. This absence does **not** establish novelty.

The sampler itself is an exact specialization of established randomized matrix multiplication / empirical sparsification. The fast evaluation stage is established pruned FFT computation. The package should presently be described as a straightforward composition of known ingredients, with novelty unverified.

There is also an important competing result: classical sparse Fourier algorithms already imply **O(N) output-all computation at the proposed error scale for sufficiently spread-out time inputs**, including constant-magnitude inputs. Requiring all bins to be written does not make sparse-spectrum approximation irrelevant: absent entries can be filled with zero.

## 1. Identical importance-sampling estimator

Drineas, Kannan and Mahoney, *Fast Monte Carlo Algorithms for Matrices I: Approximating Matrix Multiplication*, SIAM J. Comput. 36(1), 132–157 (2006), Section 4 and Lemmas 3–4, sample column-row products with replacement and reweight by inverse sampling probability. Optimal probabilities for their mean-square criterion are proportional to the product of column and row Euclidean norms. See the [author-hosted paper](https://www.stat.berkeley.edu/~mmahoney/pubs/matrix1_SICOMP.pdf).

**Specialization (our deduction):** take A=F, the unitary DFT, and B=x, a single column. Every column of F has norm one, so their probabilities become p_j=|x_j|/||x||_1, and their estimator is exactly F y with y=(1/k) sum_t (x_{J_t}/p_{J_t}) e_{J_t}. The paper is written for real matrices; the complex extension is immediate by realification or the same second-moment computation. Its stated main error theorem is Frobenius-norm based, not the desired sharpened max-bin bound. The latter follows separately from bounded-coordinate concentration and a union bound.

## 2. Established empirical sparsification principle

Barman, *Approximating Nash Equilibria and Dense Subgraphs via an Approximate Version of Carathéodory's Theorem* (2014 preprint; later SIAM publication), Theorem 2, gives a convex-combination approximation using O(p gamma²/epsilon²) sampled atoms in the p norm. The paper explicitly traces the principle to Maurey's lemma and work by Pisier and Carl. [Primary preprint](https://arxiv.org/pdf/1406.2296).

**Application (our deduction):** represent F x/||x||_1 as a convex combination of phase-rotated Fourier columns. Realify C^N to R^(2N), and take p proportional to log N. This recovers the O(epsilon^-2 log N) support scale for max-coordinate approximation. Direct Hoeffding concentration adds the log(1/failure_probability) dependence. Neither the phase handling nor the finite-coordinate union bound supplies a substantial new mechanism.

## 3. Established sparse-input FFT evaluation

The [official FFTW pruned-transform documentation](https://fftw.org/pruned.html) explicitly gives O(N log K) arithmetic complexity when K inputs are nonzero, as well as the transposed selected-output situation. It cites Sorensen and Burrus, *Efficient computation of the DFT with only a subset of input or output points*, IEEE Transactions on Signal Processing 41(3), 1184–1200 (1993), and Duhamel–Vetterli's 1990 review. The documentation also warns that arithmetic savings need not translate into comparable implementation speedups.

For the proposed theorem, use O(N log(K+2)) to cover K=0 or 1, and include the O(N) fresh-input scan and output writes. The probabilistic surrogate does not change the fact that the evaluation kernel is a known exact transform of a sparse input.

## 4. Sparse-spectrum competition must be included

Hassanieh–Indyk–Katabi–Price, *Simple and Practical Algorithm for Sparse Fourier Transform*, SODA 2012, [Theorem 4.4 and Section 4.2](https://www.cs.utexas.edu/~ecprice/papers/sparse-fft-soda.pdf), give, after unitary rescaling,

    ||X-Xtilde||_infinity² <= c||X_tail(k)||_2²/k + eta²||X||_1²,
    runtime O(sqrt(N k log(N/eta)/c) log N), success 1−1/N.

N is a power of two. Access is through indexed time samples. Unlisted outputs are zero; support need not equal k. Use the proven Section 4 algorithm, not the Section 5 heuristic. Eta is filter precision.

**Derived comparison:** set tau=||x||_1/(sqrt(N)||x||_2), k≥2c/(epsilon²tau²), eta≤epsilon*tau/sqrt(2N), and constant c. Parseval and ||X||_1≤sqrt(N)||x||_2 give the proposed tolerance. For constant tau and inverse-polylogarithmic epsilon, reconstruction costs sqrt(N)*polylog(N); adding input scanning and one dense zero-fill gives O(N).

This deduction requires no spectral sparsity, but does **not** settle arbitrary low-tau inputs: k may reach N. Fixed polynomial failure targets follow by increasing repetition constants in the concentration proof; arbitrary failure targets need explicit amplification accounting. This is a proof adaptation, not a quoted theorem. No defensible novelty claim remains for the constant-tau headline alone.

## 5. Related results that are not the same theorem

- Nakos, Song and Wang, *(Nearly) Sample-Optimal Sparse Fourier Transform in Any Dimension; RIPless and Filterless* (2019), Theorem 1.1: O(k log k log N) time-domain samples, O-tilde(N) reconstruction time, O(k)-sparse output, max error at most ||X_tail(k)||_2/sqrt(k), probability 1−1/poly(N). It assumes a polynomially bounded signal-to-noise parameter and discusses knowing a noise scale. This confirms that max-bin sparse-recovery guarantees are standard, but its stated soft-linear runtime does not by itself beat O(N log log N). [Primary paper](https://arxiv.org/pdf/1909.11123).
- Chen, Moore and Russell, *Small-Bias Sets for Nonabelian Groups: Derandomizing the Alon–Roichman Theorem* (2013), recalls that random sets of size O(log |G|/epsilon²) make all nontrivial representation averages small. For cyclic G, this is the same all-character concentration phenomenon for a uniform target distribution. It does not supply the arbitrary signed/complex input algorithm or its output-all runtime. [Primary preprint](https://arxiv.org/abs/1304.5010).

## Research implications

1. Cite the estimator and pruned FFT as established tools. An exact-title search is not evidence that their composition is a new research contribution.
2. State the error scale prominently: epsilon||x||_1/sqrt(N) is not per-bin relative error and is not an l2-relative Fourier guarantee.
3. Compare to the SODA 2012 max-bin theorem, including its additive precision term, output materialization, time-sample access, probability, and the tau-dependent regime.
4. A defensible new contribution would need an independently substantial advance: stronger scale, a provable optimality result for a clearly specified model, improved dependence in an unresolved input regime, or demonstrated end-to-end computational benefit with honest baselines. None is established by this literature check.
