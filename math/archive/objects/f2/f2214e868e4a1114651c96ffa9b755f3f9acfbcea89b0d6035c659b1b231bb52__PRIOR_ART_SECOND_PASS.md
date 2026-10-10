# Second-pass primary-source comparison

10 October 2026. Scope: the all-length deterministic represented-input relative-Euclidean Fourier theorem, with cold tables, explicit output, and Θ(log N)-bit word operations. The manuscript is mathematically supported after internal second-pass review. Publication novelty, optimality in the word model, and practical benefit remain unresolved. Negative search results do not establish novelty.

## 1. Alman: the closest complete tabulation mechanism

Josh Alman, *Faster Walsh-Hadamard Transform and Matrix Multiplication over Finite Fields using Lookup Tables*, arXiv:2211.04643, November 2022 / SOSA 2023. Primary source: https://arxiv.org/pdf/2211.04643

Read §§1.1–1.2, Lemma 3.1, Theorem 3.2 and its complete table/depth proof, and §5. The paper enumerates every short finite-field block, charges construction, and uses the block as a macrostep in a tensor recursion, obtaining N log N/log log N bit operations for constant-field transforms. This directly precedes the finite-state mechanism and the headline saving.

Its §5 matters: packed word-RAM WHT has an O(N) baseline and permutation overhead, so the bit bound cannot be relabeled an additional word-RAM improvement. Our theorem pays O(r) movement for r separately represented complex states and adds quantization/stability. It is a numerical-contract adaptation of an established strategy, not a newly invented tabulation principle. No theorem-matched subsumption is established by this comparison.

## 2. Chan–Jin–Vassilevska Williams–Xu: exact word-RAM convolution

*Faster Algorithms for Text-to-Pattern Hamming Distances*, arXiv:2310.13174. Primary source: https://arxiv.org/pdf/2310.13174

Read Lemma 2.2 and Appendix B, especially the prior incomplete packing reduction, Corollary B.4, the two-level DFT reduction and short-transform lookup. Lemma 2.2 gives deterministic O(n log p) convolution over F_p for p polynomially bounded in n on logarithmic-bit words. Appendix B explicitly accounts for finding suitable smooth extension-field transform orders, packing and lookup preprocessing.

This is a stronger model comparator than a generic reference to finite-field FFTs: it already combines word operations, short DFT tables and cold arithmetic preparation. It is nevertheless exact modular convolution, not a complex normwise Fourier map. A finite-field convolution guarantee does not produce accurate complex phases without a separate reduction and error proof. Its warning about an earlier incomplete packing argument is directly relevant to any proposed packed backend.

## 3. Fürer: count coefficients and total bits separately

Martin Fürer, *How Fast Can We Multiply Large Integers on an Actual Computer?*, arXiv:1402.1811. Primary source: https://arxiv.org/pdf/1402.1811

Read the log-RAM definition, §§4.1–4.2, Theorems 1–2 and §5. Multiplication and division of logarithmic-size words are explicit unit-cost instructions. The O(n) integer-multiplication result processes n aggregate input bits, partitioned into about n/log n complex coefficients, and pays one word operation per short numerical multiplication.

Replacing its aggregate bit variable by N log N gives O(N log N), not the present N log N/log log N coordinate bound. Thus a previously suggested direct subsumption is invalid. Conversely, this paper firmly precedes the machine-model use of guarded O(log N)-bit numerical arithmetic. It does not certify novelty of a different Fourier contract.

## 4. Harvey–van der Hoeven–Lecerf: finite-point short transforms and Kronecker substitution

*Even faster integer multiplication*, February 2015 manuscript / Journal of Complexity 2016. Author-hosted primary source: https://www.texmacs.org/joris/mul/mul.pdf

Read §2.6, §§3.1–3.4, Proposition 3.6, Propositions 3.7–3.8 and the short-transform convolution construction. The paper provides fixed-point error accounting, root preparation, composition of short complex transforms and conversion of their convolution to exact integer multiplication by Kronecker substitution. It studies bit complexity and integer multiplication, with a distinct error normalization.

This is a substantive antecedent for the new packed-block candidate: local numerical transforms accelerated by packed integer arithmetic are established. The proposed replacement must still prove its local relative-l2 normalization, unsigned carry bounds, signed-complex handling, complete word width and O(r) data movement. The paper is not being cited as already proving the precise all-length contract, nor is our packing mechanism being claimed novel.

## 5. Cherniavskii–Gribanov–Malyshev–Pardalos: all-length finite-word DFT baseline

*Delta-modular ILP Problems of Bounded Codimension, Discrepancy, and Convolution*, arXiv:2405.17001v5, 14 June 2025. Primary source: https://arxiv.org/pdf/2405.17001

New comparator added in this pass. Read §1.4, Theorem 18 and Appendix B, including cyclic Cooley–Tukey and arbitrary-length Bluestein error analysis. Theorem 18 treats rational complex inputs and finite abelian groups supplied by a basis, with O(n(log n+γ+log(1/ε))) rational operations and polynomial-in-n amplification of an absolute sup-norm input accuracy.

This is a close finite-word, arbitrary-length numerical baseline. After imposing the precision needed to turn its absolute bound into the present relative-energy target, it supplies ordinary N log N-scale work; it does not state a cold tabulated sub-N-log-N result. Its broader group domain and its different error normalization must be preserved in any comparison. It rules out describing finite-word all-length Fourier error analysis itself as new.

## 6. Potts–Tasche: localized oversampled interpolation and stability

*Numerical Stability of Nonequispaced Fast Fourier Transforms*. Author-hosted primary source: https://www-user.tu-chemnitz.de/~potts/paper/nfftstabil.pdf

Read Algorithm 2.1, window/truncation estimates, the sampling-separation discussion in §3 and the normwise roundoff analysis in §5. Oversampling, compactly truncated evaluation windows and stability controlled by sampling geometry are prior art. The new manuscript's source and target grids have fixed separation, and its Schur tail proof gives a dimension-independent spectral error for this particular compiler. That proof is still necessary when substituting an l2-only FFT routine.

A generic dimension-dependent NFFT error statement is not enough to justify the desired precision. The use of localization or oversampling alone is not a novelty claim. A thorough comparison with the larger NFFT window literature remains appropriate before any priority assertion about the exact kernel or separated-grid estimate.

## 7. SWIFFT: direct FFT lookup precedent

Lyubashevsky, Micciancio, Peikert and Rosen, *SWIFFT: A Modest Proposal for FFT Hashing*. Author-hosted primary source: https://people.csail.mit.edu/cpeikert/pubs/fft_impl.pdf

Read §3's binary-input FFT implementation, including tabulation of initial FFT iterations and parallel instruction use. This is an FFT-specific lookup precedent with concrete finite-field parameters, not merely a dense-matrix analogy. It does not state repeated floating quantization for arbitrary dyadic inputs or the present growing-block, relative-l2 theorem. The common lookup concept is therefore established, while the numerical contract must be proved separately.

## 8. Williams: finite-semiring matrix-vector preprocessing

Ryan Williams, *Matrix-Vector Multiplication in Sub-Quadratic Time (Some Preprocessing Required)*. Author-hosted primary source: https://people.csail.mit.edu/rrw/mat-vec3.pdf

Read Theorems 1.1–1.2 and the block lookup construction. Finite-semiring matrix-vector acceleration with explicit preprocessing already works on pointer machines and logarithmic-word RAMs. Its dense-matrix, superquadratic-preprocessing setting is not a cold near-linear Fourier algorithm. It establishes a general tabulation precedent, not the desired normwise transform bound.

## 9. Exact-complex Fourier work: maintain the model boundary

Official OpenAI Math #130 scope document: https://github.com/openai/math/blob/main/lean/docs/130.md

Read the current primary scope statement and its linked exact/uniform formalization descriptions. The uniform theorem is an exact-complex-register result with supplied Fourier root and unrestricted complex coefficients; the source expressly separates conditioning and bit-complexity questions. The approximate finite-word manuscript neither subsumes that theorem nor supplies its missing stability analysis. Its nonlinear quantization, finite input description and word multiplication are essential. This source is contextual comparison, not a foundation of our proof.

## Disposition and exact remaining question

The complete present upper bound survived proof/model audit. Its broad mechanisms have substantial primary precedents. What has not been established is whether this precise normalized complex all-input relative-l2/cold-word contract was previously stated or is an immediate corollary of a published finite-precision or packed-word compiler. Nor have we established that N log N/log log N is the strongest known word-RAM upper bound for this accuracy contract. The packed microkernel is being reviewed separately and receives no priority label.

Publication-level next step: have algorithms and numerical-analysis specialists compare the full finite-word theorem, not its title, against stable finite-precision transform compilation and packed-word arithmetic. An internal proof acceptance and a literature search are different kinds of evidence.
