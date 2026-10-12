Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: 316e2e045daa16f5c2d6a01417ddddba91bf2cbbd7482f445b9155f58dff3f3a.

# Independent review: Q16 finite-word HIKP window component

## Disposition

ACCEPT WITH EXPLICIT ERRATUM the finite dyadic coefficient/companion-response component on the stated guarded, growing dyadic family. Acceptance is of the independently corrected statement below, bound to the unchanged v1 candidate by SOURCE_BINDING.json and EXPLICIT_ERRATUM.json. This is a partial numerical-interface closure. Q16::flat-window-engine and STR-Q1 remain OPEN for the complete finite-word sparse engine. P05 §S6/R18's accepted ideal-arithmetic result, historical Gaussian/Green qualifications, and existing priority status do not change.

The review found and requested two small corrections. Before the first seal, the query comparisons were changed to shifts and the bit cost of reducing an unusually long supplied index was charged explicitly. After that seal, this reviewer found that the stated minimum Q=57 must be Q=56. The present independent review supplies the correction and proves the cap inequality on the complete valid domain. There is no author v2 in this accepted packet: the original v1 proof still contains its Q=57 typo and is retained unchanged. No program change is needed. Acceptance therefore applies to the source-bound implementation together with this explicit reviewer erratum, not to the uncorrected wording as written.

No original archived program was run. Only the inspected newly authored candidate and new independent verification programs were executed.

## 1. Primary-source conventions and scope

I independently opened HIKP's SODA paper and checked Definition 3.3, §4.1, and the offset and estimation formulas. The relevant passband is |i|≤n/(2B), with small response outside |i|≤n/B. The estimation offset is in the passband, and estimation divides by the actual filter response. The source also uses a global response bound in its analysis. The candidate supplies that bound explicitly, rather than relying only on a pass/stop definition. [HIKP, Simple and Practical Algorithm for Sparse Fourier Transform](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf).

I separately checked arXiv:1201.2501v2, dated 6 April 2012: its Definition 2.3 has a clipped companion response, while Claim 7.2 and Lemma 7.3 connect the continuous Gaussian/box construction, discrete periodization, and finite support. Its unitary convention would use G=√n h for the candidate's raw taps. Its width parameters correspond to B′=B/2 and α=1/2 here. The candidate correctly derives its own normalization and finite-bit costs; it does not import an ideal-real-arithmetic operation count as a bit bound. [HIKP, Nearly Optimal Sparse Fourier Transform, v2](https://arxiv.org/pdf/1201.2501v2).

The source inspection used the web PDF text extraction. Screenshot retrieval failed with a cache error, and no primary PDF byte hash is asserted. The source URLs, explicit arXiv version, and checked sections are sufficient for this source comparison; they are distinct from the exact candidate-byte binding below. Raw source text is not republished in this review.

## 2. Uniform family, normalization, and analytic bounds

The accepted domain is integer n=2^m, B=2^b with 2≤b≤m, q≥10, L=8Bq, and w=2L+1<n. The returned coefficients have p=q+ceil(log₂w)+6 fractional bits. The response convention is the unnormalized sum H_i=Σ_t h_t exp(-2πiti/n). Exact symmetry makes the response real; a later bucket implementation must use this normalization or explicitly account for a conversion.

The support guard ensures distinct residues, including at the two ends of the symmetric interval. It excludes any hidden wrapped-support or duplicated-tap interpretation. The ideal infinite time kernel is

f(t)=exp(-t²/(16B²q)) sin(3πt/(2B))/(πt), with f(0)=3/(2B).

Multiplying the continuous Gaussian by the inverse transform of the box [-3/(4B),3/(4B)] gives the candidate's erf difference with argument scale 4πB√q. This independently fixes the 2π factors and amplitude. The transform is a convolution of a nonnegative unit-mass Gaussian density and a height-one box, so its value R lies in [0,1]. The pass and stop boundaries are each at least 1/(4B) from the corresponding box edge; the erfc bound therefore gives the claimed exponentially small errors.

The Gaussian majorant of the sinc gives an ℓ¹ tail below 3 exp(-4q)<3·2^(-5q) after truncation at L. Poisson summation applies because the product is Schwartz. For centered |ξ|≤1/2 and B≥4, nonzero frequency aliases are at least |j|/4 away from a box edge. Summing their nonnegative tails gives the claimed bound below 4·2^(-144q). These bounds apply to every frequency, including the cyclic Nyquist coordinate. They are not inferred from the finite tests.

For q≥10, truncation, aliasing, and the pass/stop Gaussian tails fit inside Δ/16, where Δ=2^-q. Quantizing all w possible taps with absolute error at most 2^-p adds no more than w·2^-p≤Δ/64 to any unnormalized Fourier response. Thus the actual dyadic tap response satisfies the declared pass/stop/global bounds with 5Δ/64. Symmetric coefficients are quantized together, so imaginary cancellation is exact mathematically.

The companion response D is exactly one in the passband and zero in the stopband. In transition, its grid and certified absolute error give |D-R|≤Δ/64; clipping cannot worsen this. Consequently |D-H|<Δ globally. This is an approximation contract, not a claim that a finite supported vector has an exactly flat Fourier plateau. The actual passband denominator is at least 1-5Δ/64>0.9999. Replacing it by the companion value one in an estimator still incurs the stated perturbation and must be paid by the future recovery proof.

For fixed d≥1 and 0<γ<1, q=dm+10 and dyadic B within a constant factor of n^γ give a nontrivial growing sparse family. The support guard holds eventually. The sublinear preparation claim is confined to this logarithmic-precision, sublinear-B regime (also allowing fixed polylogarithmic factors), rather than every allowed finite parameter triple.

## 3. Finite arithmetic, totality, and costs

The inspected code uses integer endpoints with directed floor and ceiling. Its multiply and positive-denominator divide enclose endpoint extrema. Integer square roots enclose both input endpoints. Exact periodic reduction handles sine zeros and half-integer extrema. The signed nearest-even routine handles negative ties correctly, and the final quantization acceptance test checks the whole interval using exact integer inequalities.

The Machin π series has a rigorously bounded alternating tail. The coefficient exponential is range-reduced before its alternating series and then squared with outward rounding. Reduced sine arguments are bounded in magnitude by π/2. The response uses either a certified erfc saturation interval or a Taylor interval in an overlapping bounded region; refining cannot leave a gap between the two branches. Taylor remainders and the fixed saturation widths remain well below the relevant output grids. No floating-point library transcendental value is used as proof evidence.

The totality argument's giant precision cap is conservative but valid. In checking its radius induction, one may use the stronger radius-at-most-one-half invariant: the final majorant is far below one-half, which keeps every interval denominator separated from zero and justifies the stated 8U amplification factor. The fixed analytic remainder terms are separately budgeted, rather than mistaken for machine rounding that vanishes with increased W.

The actual minimum Q is 56, attained by m=10,b=2,q=10,p=26. The review independently proves the cap exponent inequality for every Q≥1. With Wmax=2^18 Q²,

log₂(129(Wmax+1)) < 26+2Q,

so the exponent is bounded above by -229376Q²+6162Q+29, which is less than -2Q-20. This covers the full valid domain Q≥56. Exact checks for Q=1 through 100000 supplement this algebra, and include Q=56 explicitly. EXPLICIT_ERRATUM.json records the exact correction; no mathematical dependency requires a source-code change.

The preparation charge O(Q^8+wQ^5), context/scratch storage O(Q²), and stored-tap charge O(wp) are conservative in the stated classical bit model. Cached roots have only the fixed q and π arguments at each precision; the cached precision levels form a geometric series. Integer powering in the Machin preparation and context creation are included in the looser context bound. After context preparation, a transition query costs O(Q^5). Canonical-coordinate pass/stop comparisons use shifts, with O(m+q) output/comparison work; longer integer-index reduction is separately charged. Requesting all n responses is not free.

The constructor stores a sparse coefficient list, not a length-n zero array or precomputed response bank. The Python object overhead is explicitly distinguished from packed mathematical storage. The exhaustive author DFT tests are dense verification work, not secretly required online preparation. Multiprecision scratch may use O(log²n) bits on the highlighted family; this is not a binary64 or constant-word production theorem.

## 4. Fresh independent verification

The exact sealed candidate code was copied into a separate replay directory. Its four complete author test cases reproduce all mathematical output fields and coefficient hashes; elapsed times were excluded from comparison. The primitive result file is byte-identical. The replay checks 30,720 frequency coordinates, with the full positive transition sets, and the reported exact primitive controls.

My independent interval verifier does not import the candidate implementation. It uses a different π identity, π=4(arctan(1/2)+arctan(1/3)), and exact rational alternating tails. Exponentials use a positive-term series for exp(x), a certified reciprocal, and squaring. Its erf reference uses a positive-term series for exp(z²)erf(z), a geometric tail bound, and an independently enclosed exp(-z²). The verifier uses 512-bit outward dyadic intervals throughout.

The actual dyadic Fourier response is independently checked with the real even-tap formula and a certified fixed-point cosine recurrence, rather than the author's FFT. For a midpoint c̄∈[-1,1], floor rounding introduces at most one ulp per recurrence step. The Chebyshev second-kind bound |U_j(c̄)|≤j+1 gives accumulated error at most t(t-1)/2 ulps. The derivative bound |T′_t|≤t² adds at most t² times the certified cosine-input error. The implemented t²(e+1) bound therefore encloses each cosine, without the spurious exponential blowup of a naive interval recurrence.

Results:

- All 5,572 stored nonnegative candidate taps independently satisfy their stated coefficient-error contract.
- Three fresh regimes add 3,843 tap checks: (m,b,q)=(10,2,10), (11,3,15), and (13,2,80). The middle case has w=1921<n=2048; the last has p=99 and Q=202.
- All 1,024 frequencies in the smallest case pass by exact symmetry and 513 independent half-spectrum enclosures. The other six regimes each have 28 additional direct spectral checks, including pass/stop boundaries and transition centers.
- 289 additional response queries pass comparison both to the independent erf reference at the promised response-grid accuracy and to the actual dyadic DFT at error below Δ. These include every nonnegative transition offset, with endpoints, for the two smaller fresh regimes.
- The response is tested at signed, periodic, Nyquist, exact pass/stop boundary, and 10,000-bit wrapped-index inputs. These agree exactly after reduction.
- 219 valid parameter combinations and 1,851 rejected combinations verify the explicit domain guard and exact precision/denominator arithmetic. A separate 65,682-case signed rational RNE sweep verifies half-grid error, tie parity, and odd symmetry.

These are rigorous finite checks plus a reviewed uniform analytic proof. They are not an inference of an asymptotic theorem from a small sweep, a random-generator test, or a recovery-success experiment.

## 5. Scope and remaining work



“An independently reviewed finite dyadic Gaussian/box HIKP coefficient-and-companion-response constructor is available for an explicit growing guarded family, with uniform support/response bounds, positive denominator margin, and paid preparation/storage/bit costs. The complete finite-word sparse engine and downstream transfer arithmetic remain open; accepted ideal-arithmetic and priority qualifications are unchanged.”

Only this classical coefficient-and-companion-response component is accepted. It adds no historical-priority claim or independent theoretical discovery.

The next obligation is a source-bound raw-product, exact modular-index, folding, and bucket-FFT implementation consuming these taps under the selected normalization. It must charge input conversion, twiddle preparation, product/addition/FFT rounding and range. Then come perturbed location/selection and estimation, independent unbiased randomness, every abort, and the S6 output/interpolation arithmetic. Neither the companion's exact-one branch nor this denominator margin removes those obligations.

There is no new generic exact-Fourier complexity claim, deterministic all-input recovery guarantee, proof of source-code absence, or closure of the complete finite-word Q16/STR-Q1 gate.

## Reproduction and binding

SOURCE_BINDING.json verifies the immutable first candidate archive, all 20 payloads, manifest, CRC, and exact member set. EXPLICIT_ERRATUM.json binds the Q=56 correction to that same v1 archive and proof hash. No successor candidate is asserted, and the executed constructor bytes remain unchanged. COLD_REPLAY_BINDING.json records the exact mathematical replay match. Independent results and executable checks are retained in the complete review packet, separately from this report-only publication. REVIEW_MANIFEST.json and the external review seal bind the final review payloads.
