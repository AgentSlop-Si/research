# Next exact Fourier construction gate

The latest theorem makes a genuine architectural decision:

**Stop exploring real positive or projectively-positive Green sums separated by only one complex diagonal phase mask.** Unitarity alone forces their mask phases to be real-collinear, regardless of phase spread. This restriction includes non-affine positive-weight cycle permutations and arbitrary complex outer monomial gauges. It is a hard exact obstruction at all N>=3.

**Surviving possible constructions:**

1. At least one aggregate stage has **essential projective phase frustration**, witnessed by a non-positive-real anchored cross-ratio. This must come from genuinely complex weight holonomy or destructive interference, not removable endpoint phases.
2. Alternatively, introduce >=2 **independent internal complex phase masks** between real positive mixing stages; then the single-mask theorem does not apply.
3. For either route, solve the **full** quadratic Veronese/Segre feasibility system from the prior archive with admissible nonzero gauges, not merely the commutator determinant or graph cuts.
4. Test exact Weyl covariance `M S = Delta M`, plus the Fourier first-column seed. Verify on basis and random field vectors at N=4,8,16,32.
5. Derive one parameter **length-doubling recurrence** that produces the exact matrices with O(N) charged input-independent coefficient generation and O(N) sequential application. Without a uniform recurrence, finite-size equality is not an FFT complexity advance.

Fast exact small-instance pretest: on any nonzero aggregate matrix `A`, compute its anchored ratios `A_ij A_00 / (A_i0 A_0j)`. If every one is real positive and the same holds for the other stage, reject immediately for N>=3. The dense check is O(N^2), for research-scale candidates only.

**No proposed construction has passed this full gate.**
