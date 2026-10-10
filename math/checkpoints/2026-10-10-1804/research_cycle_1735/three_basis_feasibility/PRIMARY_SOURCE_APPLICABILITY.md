# Primary-source applicability and bounded conclusion

10 October 2026. Bounded literature pass. Only the three specified accepted files were read for the local mechanism. No accepted file was modified.

## Outcome first

The most useful applicable result is ordinary consecutive-row Fourier/Vandermonde full spark, valid at composite orders as well as primes. A further ordinary-frequency annihilator turns the precise three-basis problem into this elementary setting. The companion STRUCTURED_INTERVAL_ELIMINATION.md gives a complete candidate guard proof for d≥4 and N≥16d−19; it awaits independent review. No generic three-basis full-spark assertion is used. The next step is proof review, not a broader literature search or optimization of the coherence constant.

## 1. Prime Fourier minors: exact theorem, narrower scope

T. Tao, “An uncertainty principle for cyclic groups of prime order,” Mathematical Research Letters 12 (2005), 121–127, Theorem 1.1 and Lemma 1.3.

Primary text: https://arxiv.org/pdf/math/0308286

For prime p, every square submatrix of the p-point Fourier matrix is nonsingular. Equivalently, every nonzero complex function f on Z/pZ satisfies |supp f|+|supp f̂|≥p+1. Thus the union of the coordinate and Fourier bases has every set of at most p atoms independent. Diagonal multiplication gives the same conclusion for coordinate versus one chirp-Fourier basis. This theorem says nothing by itself about adding all three bases: a dependence involving three component vectors is not a two-representation uncertainty identity.

It does not hold for arbitrary composite orders. Therefore importing it as an all-odd result, or applying it directly to a mixed Fourier/chirp submatrix, would be invalid.

## 2. The directly applicable all-order theorem

B. Alexeev, J. Cahill and D. G. Mixon, “Full Spark Frames,” Lemma 2, Theorems 4, 5 and 9.

Primary text: https://arxiv.org/pdf/1110.3548

Lemma 2: a rectangular Vandermonde matrix is full spark exactly when its bases are distinct. Consequently, selecting L consecutive rows of an N-point DFT gives a full-spark L×N matrix for every N. Any s distinct characters that vanish at s consecutive positions have all coefficients zero. Starting the row interval elsewhere only multiplies columns by nonzero factors. This is exactly the theorem used after ordinary-frequency elimination in our companion note.

For prime-power N, Theorem 9 additionally characterizes full-spark row sets by balanced counts modulo every divisor of N: each residue class contains floor(|M|/d) or ceil(|M|/d) chosen indices. The paper gives an N=10 counterexample to sufficiency for general composite N. These stronger row-pattern results are unnecessary for the candidate proof, which retains genuinely contiguous zero windows.

## 3. Achanta et al.: one missing row is conditional

H. K. Achanta et al., “The spark of Fourier matrices: Connections to vanishing sums and coprimeness,” Digital Signal Processing 61 (2017), 76–85, DOI 10.1016/j.dsp.2016.07.008.

Primary publisher text: https://www.sciencedirect.com/science/article/pii/S1051200416300938

For 1≤n<K<N and the K-row selection M={0,…,K}\{n}, the exact criterion is: the selected DFT rows fail to be full spark iff there are K distinct Nth roots whose elementary symmetric n-product sum vanishes. Equivalently use the (K−n)-product sum. This follows by taking the monic polynomial with those roots: its coefficient of z^n must vanish; conjugation on unit-circle roots makes the two formulations equivalent. The publisher abstract and introduction confirm this criterion and emphasize that one-hole sets can fail; the 2017 paper corrects errors in its preliminary conference version.

The accessible publisher rendering loses some displayed formulas, so no finer corrected semigroup criterion is imported here. This result does not directly treat mixed chirp/Fourier atoms. More importantly, the coordinate-functional argument can use the longer of its two contiguous zero intervals, avoiding one-hole criteria altogether.

## 4. Quadratic-chirp pairs and three-basis support uncertainty

V. Fiorentino and S. Weigert, “Uncertainty relations for the support of quantum states,” Journal of Physics A 55 (2022), 495305, Theorem 3 and equation (31).

Primary text: https://arxiv.org/pdf/2209.09817

Theorem 3 proves the sharp support-sum bound s_j(ψ)+s_k(ψ)≥p+1 for any pair in the standard complete prime-dimensional MUB set, whose bases have entries p^(-1/2)ω^(ax²+bx), together with the coordinate basis. This includes our fixed coordinate/Fourier/quadratic-chirp triple at prime order, up to indexing and phases. It is a theorem about standard MUBs, not all arbitrary pairs of unbiased bases.

Equation (31) gives s_0(ψ)+s_1(ψ)+s_2(ψ)≥3(p+1)/2 by summing pair inequalities. Its three sparsities describe three expansions of the same vector ψ. Our needed independence statement excludes f+g+h=0, where f,g,h are three different vectors sparse in different bases. The support inequality therefore does not directly provide the required three-block independence. It also has no stated arbitrary-composite-order extension.

## 5. Complete MUB unions are not automatically full spark

K. Blanchfield, “Orbits of mutually unbiased bases,” Section 6.

Primary text: https://arxiv.org/pdf/1310.4684

The standard complete prime-dimensional MUB set contains one invariant vector per basis for a phase-point involution, placing N+1 such vectors in an (N+1)/2-dimensional eigenspace. Hence sufficiently large subcollections of those vectors are dependent. Theorem 3 additionally gives N dependent vectors from distinct standard bases when the prime dimension is N=3k+2, with an orthogonality relation to an Alltop-orbit vector.

These results prevent promoting pairwise unbiasedness to full spark of an entire MUB union. They do not exhibit a dependence in our specified three bases with our particular two chirp intervals, ordinary interval, and terminal coordinate interval. Therefore they are a warning about an invalid inference, not an obstruction to the structured lemma proved here.

## 6. Explicit composite obstruction and why structure escapes it

The following is an elementary calculation, not a claim imported from a source. If N=ab, the indicator of the subgroup H={0,b,2b,…,(a−1)b} has coordinate support a and Fourier support b. Expanding it in those two bases gives a dependence using a+b atoms. At N=s² this uses 2s atoms. Thus arbitrary-support linear-size independence cannot hold uniformly over odd composite N even for two of our bases.

Those Fourier supports are subgroup progressions, rather than the long consecutive zero windows retained in the present method. The new lemma never invokes arbitrary-support composite uncertainty. Its elimination is performed before the all-order Vandermonde step, and its final distinct-frequency condition is explicit.

## Stopping point

A suitable bounded question has now changed from “find a three-basis full-spark theorem” to “independently verify the additional ordinary annihilator and every guard in STRUCTURED_INTERVAL_ELIMINATION.md.” If that review succeeds, the accepted incidence and physical-row arguments yield the proposed linear saving over a splitting field. No claim of historical novelty, optimal bank count, base-field attainment, or FFT running time follows from this search.
