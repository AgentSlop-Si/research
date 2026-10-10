# Primary-source prior-art comparison

F132 and its all-length extension are supported proof-level syntheses of established tabulation and stable Fourier interpolation mechanisms. No inspected primary source literally establishes the entire same finite-word/cold/all-input relative-l2 contract; worldwide novelty remains unresolved.

Read-only comparison dated 10 October 2026. Original uploaded code was not executed. The exact all-length theorem is in THEOREM_AND_PROOF.md.

## PA-ALG-01: Josh Alman
[Faster Walsh-Hadamard Transform and Matrix Multiplication over Finite Fields using Lookup Tables](https://arxiv.org/pdf/2211.04643)

Exact constant-field Kronecker transforms already attain the logarithmic saving by fully enumerated small-block tables. Section 5 separately discusses packed word-RAM permutation costs. F132 uses the same established mechanism, with rounded complex states, normwise stability, and O(r) paid gathering/output for each r-coordinate block.

Inspection: Sections 1, 3 and 5; Lemma 3.1, Theorem 3.2, word-RAM permutation discussion. Disposition: Mechanism precedent established; not a literal complex relative-l2 theorem or priority clearance.

## PA-ALG-02: Ryan Williams
[Matrix-Vector Multiplication in Sub-Quadratic Time (Some Preprocessing Required)](https://people.csail.mit.edu/rrw/mat-vec3.pdf)

Finite-semiring matrix-vector multiplication with preprocessing is an established general tabulation setting. Its superquadratic preprocessing and dense-matrix query problem do not supply F132’s cold, near-linear Fourier setup or numerical error contract. Calling the finite-alphabet table principle itself new would be incorrect.

Inspection: Theorems 1.1–1.2 and discussion of block lookup preprocessing. Disposition: General finite-state/tabulation precedent established; model-specific F132 corollary still needs its proof.

## PA-ALG-03: Lyubashevsky, Micciancio, Peikert and Rosen
[SWIFFT: A Modest Proposal for FFT Hashing](https://people.csail.mit.edu/cpeikert/pubs/fft_impl.pdf)

The paper explicitly tabulates initial finite-field FFT levels on binary inputs. This is a direct FFT implementation precedent, not only a matrix-multiplication analogy. It does not assert the cold all-input rounded-complex norm theorem, repeated re-quantization, or its growing accuracy/radix schedule.

Inspection: Section 3, binary-input lookup tables for initial FFT iterations. Disposition: FFT-specific lookup reuse is established prior art.

## PA-ALG-04: Martin Fürer
[How Fast Can We Multiply Large Integers on an Actual Computer?](https://arxiv.org/pdf/1402.1811)

The O(n) log-RAM integer-multiplication result partitions n input bits into roughly n/log n complex coefficients. N independently represented Fourier coefficients may contain Theta(N log N) bits. Substituting that aggregate input size does not directly imply an O(N log N/log log N) N-coordinate DFT.

Inspection: Log-RAM model and Section 4.1/Theorem 1 integer multiplication comparison. Disposition: Relevant word-cost precedent; previously alleged direct subsumption is not justified.

## PA-ALG-05: Chan, Jin, Vassilevska Williams and Xu
[Faster Algorithms for Text-to-Pattern Hamming Distances](https://arxiv.org/pdf/2310.13174)

Lemma 2.2 gives deterministic O(n log p) word-RAM convolution over F_p; Appendix B repairs an earlier packed-convolution argument and uses bit tricks and tables. Exact modular convolution is not a complex DFT with relative-l2 accuracy. This strengthens the required finite-field packing comparison without proving subsumption.

Inspection: Lemma 2.2 and Appendix B model, statement and proof architecture. Disposition: Important modern comparator; model and target differ.

## PA-ALG-06: Dutt and Rokhlin
[Fast Fourier Transforms for Nonequispaced Data](https://epubs.siam.org/doi/10.1137/0914081)

Oversampled/analytic Fourier interpolation with O(N log N+N log(1/epsilon)) arithmetic work is classical. The new all-length result composes that established idea with F132 and proves its specific separated-grid operator norm, finite-state coefficient tables and cold word costs. The interpolation principle is not claimed new.

Inspection: Primary publisher abstract, scope, complexity and bibliography. Disposition: Classical all-length compiler mechanism; exact new composition proved locally.

## PA-ALG-07: Potts, Steidl and Tasche
[Numerical Stability of Fast Trigonometric Transforms: A Worst Case Study](https://www-user.tu-chemnitz.de/~potts/paper/stabfinal.pdf)

Normwise FFT stability through sparse unitary factorizations and careful twiddle preparation is established. The paper explicitly distinguishes stable generation from recurrences whose errors grow with length. F132’s accuracy guarantee should be credited as an application of this tradition, with additional finite-alphabet and paid-table accounting.

Inspection: Sections 2–3, twiddle precomputation and normwise stability Theorems 3.3/3.6. Disposition: Stability mechanism classical; no tabulated sub-N-log-N theorem claimed by this source.

## PA-ALG-08: Potts and Tasche
[Numerical Stability of Nonequispaced Fast Fourier Transforms](https://www-user.tu-chemnitz.de/~potts/paper/nfftstabil.pdf)

The paper explicitly uses dyadic oversampling, localized windows and truncated evaluation. Its displayed generic Euclidean bounds include dimension-dependent factors; they cannot simply be substituted as a dimension-free epsilon contract. Our separated-grid Schur argument supplies the needed bound for this special all-length compiler.

Inspection: Algorithm 2.1, equations (2.5)/(2.6), sampling separation and stability discussion. Disposition: Close primary comparator; avoids importing a looser error norm.

## PA-ALG-09: Potts and Tasche
[Uniform error estimates for nonequispaced fast Fourier transforms](https://arxiv.org/pdf/1912.09746)

Uniform NFFT window-error analysis has an extensive existing literature. A new fast Fourier claim must distinguish interpolation error, arithmetic error, relative energy accuracy and word complexity. This source reinforces that the window approximation itself is an established research area, rather than evidence of priority for the proposed composition.

Inspection: Primary abstract, window-family framework and uniform-error scope. Disposition: Background comparator; no complete theorem-matched subsumption asserted.

## PA-ALG-10: AMD rocFFT maintainers
[Bluestein Design Document](https://rocm.docs.amd.com/projects/rocFFT/en/docs-6.3.0/design/bluestein.html)

Bluestein’s chirp-convolution reduction is standard. The new negative derivation concerns applying an l2-only approximate FFT contract to its kernel spectrum: an allowed error can amplify by Theta(sqrt N). It is not a claim that the classical identity is incorrect or that all implementations suffer that error.

Inspection: Chirp definition, convolution embedding and FFT reduction. Disposition: Identity classical; black-box precision obstruction derived independently.

## What remains novel only at the project level

The dyadic proof accounts for input normalization, underflow, complete finite alphabets, table outputs, scale-dependent twiddles, all movement and the precision/radix boundary. The new derivation extends it to every integer length using a dimension-free spectral interpolation bound and finite offset tables. The sharp Bluestein example explains why an apparently easier black-box reduction did not establish that extension. These are concrete completed derivations, not claims to have invented their classical ingredients.

No global first-discovery claim follows from these comparisons. The general finite-alphabet compiler idea is especially close to known Four-Russians reasoning; publication value must rest on a demonstrably useful, previously unstated contract or application, not the lookup-table headline.

## Remaining checks

- Obtain an external algorithms/numerical-analysis review of whether the full finite-word theorem is already a standard corollary of a general stable circuit-tabulation result.
- Check model conventions for multiplication, division, memory addressing and coefficient generation against any claimed comparator.
- Formalize the complete eager-table executor and interval coefficient certificates; no asymptotic-runtime production implementation has been validated.
- Distinguish mathematical asymptotic usefulness from crossover sizes and real hardware speed.
