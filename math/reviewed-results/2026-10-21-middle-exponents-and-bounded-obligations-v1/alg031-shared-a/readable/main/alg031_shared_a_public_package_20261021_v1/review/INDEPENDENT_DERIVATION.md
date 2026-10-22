# ALG-031 shared quadratic coefficient: independent derivation

Status: ACCEPTED at the bounded shared-a concentration scope against candidate v2. The requested wording-only repair was verified as an exact single-sentence change; all candidate v2 members were rehashed. Candidate v1 and its historical HOLD remain preserved. ALG-031 owner closure is not accepted.

## Original-source binding

Read verbatim source bytes under `../proof/sources/`:

- DECODER.md: SHA256 `958a37ab8f0db835a83a62135b8b704533cce88f0f774667799da681b20d126a`, 9129 bytes.
- REPETITION.md: SHA256 `0554f98e8eb0cdca57a5100d0a60e4f0a85c2613aaf723c0fbceec7d6b347638`, 9534 bytes.
- AFFINE_RESONANCE.md: SHA256 `504e7f01540b55df9a65692fe6d79e87fee014e7b08ab7f50f0bf499239aad55`, 7967 bytes.

The catalogue is the existing capture at [private historical scope-capture locator omitted]. Its historical acceptance is the exact evaluator of the natural sketch, not exact or accurate original DFT recovery. It leaves stronger concentration, shared multi-seed computation, stability, and bit complexity open. A new bounded concentration theorem must not silently close the owner or those other obligations.

No supplied research program was executed. The control program in this review directory was written independently for this review.

## 1. Exact original model, not a substitute decoder

Take an odd prime M, integers 1 <= K <= M and N=KM, complex input x fixed independently of all fresh pairs, and nonzero a in F_M. Let e_L(v)=exp(2 pi i v/L). The same a is used in every repetition. In repetition j, sample b_j,d_j independently and uniformly from ALL of F_M, independently across repetitions, and put s_{j,r}=b_j+d_j r modulo M.

Define

Y_r(s)=sum_{t=0}^{M-1} x_{rM+t} e_M(a t^2+s t),
H_s(m)=sum_{u=0}^{M-1} e_M(-a u^2-s u)e_N(-m u),
F_r(m)=sum_{t=0}^{M-1} x_{rM+t}e_N(-m t),
gamma_r(m)=e_K(-mr).

The ORIGINAL decoded sample is

Xhat_m = N^(-1/2) sum_r gamma_r(m) Y_r(s_r)H_{s_r}(m),

and the true unitary DFT is X_m=N^(-1/2)sum_r gamma_r(m)F_r(m).

This uses the K ordinary original sketches and the original raw adjoint. It is not a new decoder or input-adaptive procedure.

## 2. Why fixing a is valid, and what is actually independent

For any distinct r,r' in {0,...,K-1}, the determinant r'-r is nonzero in F_M. Thus (b,d) -> (b+dr,b+dr') is a bijection of F_M^2. Each slope is uniform, and pairs of distinct slopes are independent. They are generally NOT jointly independent for K>2.

Uniform-s orthogonality gives E_s[Y_r(s)H_s(m)]=F_r(m), for this fixed a, including off-grid frequencies. Indeed only t=u remains after averaging e_M(s(t-u)). Hence each centered block term has mean zero, and pairwise independence kills cross-block covariance. The resulting conditional identity is

V_m := E_{b,d}|Xhat_m-X_m|^2
= (1/N) sum_r [ (1/M) sum_{s in F_M}|Y_r(s)|^2|H_s(m)|^2 - |F_r(m)|^2 ].

This is not the original source's uniform-whole-seed identity (M-1)||x||_2^2/N. Fixing a removes a character-orthogonality step from that older proof. The new identity is proved independently and can differ, for example flat x at DC has V_0=0 when a is nonzero.

If a is randomly selected ONCE from nonzero residues, the same statement holds after conditioning on a; all following bounds are uniform in its value. One must condition before applying an independent-repetition tail bound. Distinct repeats are independent conditional on a because each output vector is a deterministic function of its own fresh (b_j,d_j) and the fixed input. No independence across output bins is asserted or needed.

## 3. Integer-grid and off-grid chirp bounds

At alias m=qK, H_s(m) is a complete nondegenerate quadratic Gauss sum. For every odd prime M and a!=0, |H_s(qK)|^2=M. This includes M=3; no M>=17 restriction from the old median obstruction is needed for this Gauss identity.

Consequently,

V_{qK} = [M||x||_2^2 - sum_r |F_r(qK)|^2]/N <= M||x||_2^2/N.

For a general m=qK+p, 0<=p<K, put alpha=p/K. Apply exact trigonometric interpolation to the M-point integer-grid transform of the sequence u -> e_M(-a u^2). With

D_M(v)=sum_{u=0}^{M-1}e_M(vu),
Lambda_M(alpha)=(1/M)sum_{ell=0}^{M-1}|D_M(alpha-ell)|,

integer shifts q+s merely permute weights and integer-grid values. Therefore

|H_s(m)| <= sqrt(M) Lambda_M(alpha).

This bound uses complex roots and ordinary absolute value. It is not a probability statement over arbitrary coefficient fields.

The elementary uniform envelope is Lambda_M(alpha) <= 1+H_{M-1}, where H_n=sum_{j=1}^n 1/j. Proof: order the M circular distances delta_i of alpha from the integer grid. Then delta_i >= (i-1)/2, because an arc of radius delta contains at most floor(2delta)+1 integer points. Each normalized weight is at most 1. For i>=2, use |sin(pi v)|<=1 and sin(pi delta_i/M)>=2delta_i/M to obtain |D_M(v)|/M <=1/(2delta_i)<=1/(i-1). Summing proves the claim. At alpha=0, Lambda_M(0)=1 exactly, by character orthogonality.

Parseval gives (1/M)sum_s|Y_r(s)|^2=||x_r||_2^2. Thus

V_m <= M Lambda_M(p/K)^2 ||x||_2^2/N,

and uniformly V_m <= M L^2||x||_2^2/N, for L=max_{0<=p<K}Lambda_M(p/K), or safely L=1+H_{M-1}. For aliases only, take L=1 and count only the M aliases in the subsequent union bound. The all-bin theorem must not use L=1 without a separate proof.

## 4. Exact repetition and median guarantee

Assume x!=0, epsilon>0, 0<delta<1, rho=||x||_2^2/||x||_1^2, and

p_star=2 M L^2 rho/epsilon^2 < 1/4.

One repeat has probability at most p_star of complex error greater than epsilon||x||_1/sqrt(2N), by the exact conditional second moment and Markov's inequality. Set h=(R+1)/2 for odd positive R. If fewer than h samples are bad at one bin, a strict majority of both their real and imaginary coordinates lie within that radius of the true coordinates. Each odd-sample coordinate median therefore has component error at most that radius, giving complex error at most epsilon||x||_1/sqrt(N).

Independence ACROSS repetitions, conditional on the shared a, implies

P(at least h bad samples at a fixed bin | a)
<= binom(R,h) p_star^h
<= 2^R p_star^(R/2) = (4p_star)^(R/2).

The first inequality is a union bound over size-h witness subsets, not a claim that all block terms or bins are independent. A union bound over the N frequencies gives

P(max_m |median_j Xhat_{j,m}-X_m| > epsilon||x||_1/sqrt(N))
<= N(4p_star)^(R/2).

Thus any positive odd R >= 2 log(N/delta)/log(1/(4p_star)) suffices. The x=0 case is exact without this rho definition. For a set of B designated bins, replace N in the union prefactor by B and use a bound valid for those bins.

This is a per-fixed-input, diffuse-input, complex l_infinity guarantee at the specified l_1/sqrt(N) scale. It is NOT a simultaneous-over-all-inputs statement, a relative-l_2 guarantee, an exact DFT algorithm, or an arbitrary-input small-R guarantee. It does not contradict the spike obstructions in the original REPETITION.md.

## 5. Whole-algorithm accounting and required exclusions

For each of R samples:

- Draw two independent uniform F_M residues (count these as random residue draws, not an unproved deterministic bit-cost claim).
- Form the K sketches using O(N) exact scalar work.
- Run the original affine decoder at O(N log(2K)) scalar work, including chirp seed/table construction, guarded indexing, nonunit-slope handling, and output production.
- Retain its N outputs for aggregation.

The decoder must allow d=0, since the sampler includes it. In the prime case every other d is a unit. The original decoder's d=0 specialization costs O(N+K log K), and its general worst-case bound remains O(N log(2K)). Sharing a does NOT by itself justify sharing the expensive per-repeat convolutions or decreasing the charged R-fold total. Its recurrence retains the finite boundary e_K(-p)-1 at non-alias p.

Using deterministic linear-time selection separately for real and imaginary coordinates costs O(RN) ordered-real comparisons/selection work, additional to field arithmetic. A sorting implementation may instead charge O(N R log R). A simple implementation stores RN outputs and uses O(RN+M+K) additional scalar storage, plus the input and final N-vector. The candidate also provides valid lower-memory p-batching: retain RK sketches, form one shared length-M H_0,p table, and process all R repeats for that p, retaining RM sample outputs until their medians are selected. The shift by Kb preserves p. This uses O(RK+RM+M+K) auxiliary scalar storage plus the input and final output, without dropping any R-fold convolution charge. No faster joint multi-seed decoder is established.

The conservative total is O(RN log(2K)) exact scalar arithmetic plus O(RN) median-selection work, O(R) random-residue draws, and full N-output storage/writes. Suitable primitive roots, nonzero invertible FFT scales, and N^(-1/2) are supplied as in the original exact-complex model. Root/field discovery, exact-real comparison bit costs, RNG bit costs, finite-precision stability, and hardware speed are not proved here.

The retained result is a bounded shared-a concentration theorem. It does not prove a joint multi-seed computation gain, an unrestricted FFT speedup, all-prime/composite/dyadic extension, or whole-owner closure.

## 6. Fresh independent controls and negative boundaries

`fresh_exact_controls.py` constructs original centered block polynomials in a primitive Nth root and reduces all variance identities modulo Phi_N using exact integer coefficients. It ran 54 cases and 768 output bins: M in {3,5,7}, K in {1,2,M}, a in {1,M-1}, with mixed integer, spike, and flat inputs. It verifies uniform-s unbiasedness, pairwise-affine covariance cancellation, and the alias variance identity. It additionally checks 1,488 exact interpolation identities and 90 exact prime Gauss identities. Normal and optimized runs produced identical outputs, with explicit runtime checks rather than removable assertions. These finite controls supplement, not replace, the all-size proof.

Two explicit exclusions:

1. Restricting d to nonzero residues breaks pairwise slope independence: for blocks r=0 and r=1, s_0=s_1 becomes impossible, whereas independent uniform slopes agree with probability 1/M. Such a restricted sampler needs a new proof; it cannot inherit this one.
2. Reusing b as well as a can fail forever. At M=3, K=1, a=1, b=0, x=e_0 and alias q=0, each normalized output is Z=sum_u e_3(-u^2)=-i sqrt(3). The true normalized output is 1, so |Z-1|=2 for every number of repetitions, regardless of fresh d. This is an exact counterexample to interpreting the theorem as arbitrary shared-seed concentration.

The odd-prime and unit-a guards are real: for M=2,a=1 the complete chirp transform has magnitudes 0 and 2 rather than sqrt(2); for composite M, nonzero need not mean invertible and the distinct-block determinant need not be invertible.

## Hold checkpoint against the first author freeze

Reviewed candidate MANIFEST.json SHA256: 30723b5eab7f1be01c1e7eccb2f881923d16dc4e1c778a6377c23a33d69b8db0. Reviewed REPORT.md SHA256: 022c8ad34d92e5bf26274b72fdcd2afd37e56728af2b6dafedd788c9be3e00c6. All ten member hashes, three original source Git blob SHA1s, and the retained catalogue hash matched.

The only requested repair is the final sentence of REPORT section 1. Current wording: “The source's broader finite-field exact-evaluation contract alone does not provide complex order comparisons for coordinate medians.” DECODER.md explicitly states exact arithmetic over complex roots of unity; attributing a finite-field theorem to the original is unsupported. Replace with: “A broader pure field-operation contract alone does not provide the complex order comparisons required for coordinate medians.” Equivalent source-faithful wording is acceptable.

No mathematical correction is required. Recheck the revised REPORT and MANIFEST, confirm no other scope changes, and then seal bounded acceptance. Do not repeat the completed controls merely because this attribution sentence changes.

Additional independently derived exclusion: for M=3, K=2, a=1, x=(1,1,1,-1,-1,-1), and m=K, using uniform b but d only in {1,2} gives exact variance 9/2, exceeding the unrestricted-pair alias bound M||x||_2^2/N=3. This shows why excluding d=0 can invalidate the actual bound, not just the pairwise-independence proof. The candidate correctly includes d=0, so this is not a repair request.

## Final bounded acceptance against v2

The exact requested replacement is present, and no other REPORT sentence changed. Only REPORT.md, MANIFEST.json, and MANIFEST.sha256 differ from v1. All ten v2 member hashes pass; v1 hashes still match the prior frozen pins. Unchanged candidate and reviewer controls were not rerun for this wording-only repair.

Accepted v2 REPORT.md SHA256: 2210ef76037e978063de6b821729cc41e9963c5eacd63c8359f839f1a88e0ac0. Accepted v2 MANIFEST.json SHA256: 19a761368ed0ce546fe8a1b1f4befb207aa2ae8cb538a9b70e67da89345d3590.

The accepted theorem is precisely the original adjoint decoder with one shared fixed nonzero a, odd prime M, 1<=K<=M, fresh independent uniform b,d over all of F_M in every repetition, a fixed input independent of those seeds, and odd-sample coordinate medians. With L=max_p Lambda_M(p/K) or L=1+H_{M-1}, rho=||x||_2^2/||x||_1^2, and p_star=2ML^2rho/epsilon^2<1/4, simultaneous failure is at most N(4p_star)^(R/2). The explicit sufficient odd R and complete O(RN log(2K)) scalar charge, plus O(RN) ordered-real selection work, are accepted. The sharper alias-only variance and M-bin union bound are accepted only on those aliases.

This acceptance closes only that bounded seed-reuse question. Stability, bit complexity, field/root discovery, exact comparison representation, stronger all-bin concentration, arbitrary-input guarantees, dyadic/composite extensions, other shared-seed dependencies, genuinely faster joint computation, novelty, production speed, native source-comparison obligations, and whole-owner closure are not accepted. No external state was changed.
