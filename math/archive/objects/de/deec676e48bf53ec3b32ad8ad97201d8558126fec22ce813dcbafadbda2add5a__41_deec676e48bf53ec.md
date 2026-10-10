# Independent Green-fusion audit

2026-10-09. Scope: the cycle mixer, path-Green Fourier bridge, inverse error bound, literal field-operation accounting, and comparison with the prior Green audit. Supplied Python was read as data only; none was imported, compiled, or executed. No external browsing was needed.

## Verdict

The principal new mathematics checks out. This checkpoint adds an explicit dense growing-condition cycle mixer and an explicit diagonal-plus-rank-two Fourier conjugate of path-Green operators. The target inverse bound 73/18 is valid and dimension-independent. These are useful primitives and conditional error-transport results; they do not construct a faster arbitrary-input exact Fourier transform. No consequential mathematical error was found in the reviewed claims.

## 1. Cycle mixer: exact norms, density, and limitations

For a unit-modulus weighted full N-cycle M with M^N=-I,

- (I-M)^-1 = (1/2) sum_{j=0}^{N-1} M^j.
- K = I+(I-M)^-1 = (3/2)I+(1/2)sum_{j=1}^{N-1}M^j.
- K^-1 = [(2^(N-1)+1)I - sum_{j=1}^{N-1}2^(N-1-j)M^j]/(2^N+1).

Powers 0 through N-1 occupy distinct positions in each row/column, so all entries are nonzero over C, with no cancellation in their absolute column sums. Thus exactly

||K||_1=(N+2)/2,  ||K^-1||_1=2^N/(2^N+1),
κ_1(K)=(N+2)2^(N-1)/(2^N+1).

These include N=1, where K=3/2 and κ_1=1. Independent exact rational matrices verified these formulas, density, and inverse products for N=1,2,3,4,8,12,16. The spectral formula also follows directly from |(2-e^{iθ})/(1-e^{iθ})|^2=2+[4sin²(θ/2)]^-1. Hence κ_2 is Θ(N), with the stated even-N formula and κ_2=1 at N=2. The growing 1-condition is a real escape from the prior constant-condition family restriction, not a counterexample to the universal product-condition inequality.

The affine conjugacy FM=Mhat F is correct for the stated positive-exponent Fourier convention. Odd b,c and a=1 mod 4 give full cycles on dyadic lengths; the total edge exponent gives M^N=Mhat^N=-I. Applying rational functions to this intertwining identity is legitimate when their denominators are invertible. Independent exact finite-field dense matrices verified the source/target mixer and inverse identities for N=2,4,8,16 and three distinct descriptor choices per length.

Static source accounting confirms signed-cycle cold cost 3N+1; affine preparation 2N+log2(N)+4; prepared forward 5N+1; and prepared inverse 6N+1 field calls. Inversion is counted as one field call, not one bit operation. The full-cycle routine really executes two N-step recurrences; there is no hidden Fourier call.

The finite-field qualifications are essential: characteristic two fails, 2^N+1=0 makes K singular, and complex density does not transfer to all finite fields. Exact inverse outputs for signed-cycle basis inputs have Θ(N)-bit denominators and Θ(N²) aggregate expanded rational size. O(N) field calls therefore do not establish bounded-word O(N) time. Growing κ_2 also makes any floating-point stability claim a separate task.

## 2. Path-Green bridge and 73/18

For T=tridiag(-1,3,-1), the missing cyclic wrap edges yield exactly

H_{kl}=(3-q^k-q^-k)δ_{kl}+(q^l+q^-k)/N,

where H=FTF^-1. Thus H is diagonal plus rank at most two. The supplied Woodbury factors have the right order and signs. The path source solve is an ordinary paid tridiagonal solve; the Fourier-side solve uses two paid global sums and a 2-by-2 correction. Neither action obtains Fx from x.

For S=T^-1+(T+I)^-1 and K=FSF^-1,

S^-1=T/2+I/4-(T+I/2)^-1/8,
K^-1=H/2+I/4-(H+I/2)^-1/8.

Independent exact rational matrices confirmed the source identity at N=1,2,3,4,8,16. Independent complex dense calculations at N=4,8,16,32 confirmed the Fourier formula, Woodbury identities for shifts 0,1/2,1, and inverse identity, to errors below 7e-15. These floating checks corroborate the algebra; they are not certified floating error bounds.

The analytic infinity bound is sound. Let A0=3+α and g_k=(A0-q^k-q^-k)^-1>0. With t=average(g_k), c=average(q^k g_k), symmetry gives real c and A0t-2c=1. The Woodbury correction matrix is R=[[1+c,t],[t,1+c]], so

||R^-1||_∞=1/(1+c-t)=2/[1+(A0-2)t]≤2.

Since g_max≤1/(1+α), ||D^-1A||_∞≤2g_max and ||BD^-1||_∞=t≤g_max,

||(H+αI)^-1||_∞≤g_max+4g_max².

Consequently ||H||_∞≤7 and ||(H+I/2)^-1||_∞≤22/9 give

||K^-1||_∞≤7/2+1/4+(22/9)/8=73/18.

The bound is conservative. Independently recomputed norms of K^-1 were approximately 2.834122, 3.112895, 3.245671, and 3.310447 at N=4,8,16,32.

Static source counts independently reproduce all bridge table entries:

- Common preparation: 43N+31
- Source S: 9N-6
- Target K: 19N+12
- Source S^-1: 12N-5
- Target K^-1: 21N+8

These include counted integer embeddings as defined in that module. They do not account for the bit cost of representing arbitrary exact field elements. The implemented bridge deliberately restricts to dyadic N≥4 and rejects unsupported modular pivots; the broad mathematical identity should not be mistaken for implementation coverage at other lengths.

## 3. Error transport and the no-raw-gain lemma

The conditional residual theorem is a direct induced-norm argument. Its finite-word extension correctly includes source/root/quantization error e, head-evaluation error ζ, and target-inverse error τ:

error ≤ R{[ε L_box(r_tilde)+L_box(e)]/sqrt(N)+ζ}+τ.

The decoder success probability carries over on its success event. No finite-word implementation follows merely from this exact-field identity: coefficient storage, quantization and rounding bounds, and actual certified target application remain missing.

The cycle no-raw-gain lemma is also valid. The unique degree-<N polynomial representation of f(M)^-1 and f(Mhat)^-1 has the same coefficients; disjoint unit-modulus power supports give equal source 1-norm and target infinity norm. Therefore R||Dx||_1≥||x||_1, and R L_box(Dx)≥L_box(x)/sqrt(2). The composition statement is valid with the product of individual inverse norm bounds. It does not rule out a useful small residual after removing a cheaply transformed head, or an analysis exploiting correlated errors.

The reported near-structured example is deliberately synthesized by solving from a one-entry dominant filtered vector. Its improvement is conditional structure, not evidence that arbitrary dense inputs can be transformed into small residuals. The approximation script injects artificial bounded decoder errors rather than implementing the decoder. The README states these limitations accurately.

## 4. What changed relative to the prior audit

The prior audit's inverse-support and bounded-condition obstructions remain intact in their stated families. New contributions within this supplied sequence are:

1. A concrete dense/inverse-dense O(N)-field mixer outside the fixed bounded-condition family, plus explicit Fourier-side compatibility.
2. The paid rank-two Fourier-side path-Green solve and its uniform error-transport constant.
3. A slightly stronger original-family estimate κ_1(S)≤29/7 instead of 17/4. This follows from positive G=(2T+I)^-1, column sums ≤1/3 and diagonal ≥1/7, giving ||S^-1||_1≤58/21 and ||S||_1≤3/2. Exact rational checks agree.
4. The varying-rank-one-gauge detector properly extends the previous fixed-gauge detector. Its recurrence H_i=G_i H_{i-1}B_i^-1 and terminal H=I test are correct; the dense O(tN³) audit is not a fast evaluator or a universal novelty test.

The original gauge addition undercount was already identified in the prior independent audit. Its correction here is confirmation, not a newly discovered mathematical advance. The determinant obstruction in the prior audit still applies to its original fixed S, phase/permutation-only no-gain setting; it should not be generalized to the new cycle family or to unrestricted compensated products.

## Evidence and reproducibility

Auditor-written, self-contained checker: green_audit/check_green_fusion_independent.py. Output: green_audit/independent_results.json. It uses only standard-library arithmetic and does not import uploaded production code. The uploaded independent-review execution totals remain author-reported; this audit independently establishes the mathematics and stated static costs instead of claiming those suites were rerun.

Reviewed SHA-256 values match the supplied independent review:

- resolvent_escape.py: 5a5ad7fb7adc6f586addbbe0948f950f0b917b9f785f1ec1be4809d36a046cc2
- green_bridge.py: e35d36462a6314ff7c491a4cae4fab3c05e6e2b0b8d1189dc054a06a28a7429f
- verify_review.py: 42d1db6d9d3aa5715403b671e35434d3568fe4875a21e0c38bb5b89b5783803a

Next decisive work: exhibit and fully charge a uniformly generated short word of admissible mixers and permutations that equals the Fourier matrix, or prove an obstruction for that enlarged class. Alternatively, complete a finite-word residual integration with certified source and target errors for an explicitly stated structured/approximate problem. Neither task is completed by this checkpoint.

## Bounded extension: two forward cycle stages are excluded

A further independently verified spectral gate rules out two forward cycle-K stages at every dyadic N≥8, even with arbitrary unitary factors between and outside them and arbitrary nonzero global scalars. Since each K has squared singular values f(c)=(5-4c)/(2-2c), scalar-unitarity would require all reverse-paired products f(c)f(-c)=4+9/[4(1-c²)] to be equal. They are not equal at these lengths. The proof and numerical corroboration are in TWO_STAGE_GATE.md and green_audit/two_stage_gate_checks.json. N=2,4 are exceptions to this gate. Coordinate-dependent gains, inverse-stage primitives, and three or more forward stages remain outside the conclusion. This strengthens the current candidate search by a constant-stage exclusion; it is not a universal or asymptotic FFT lower bound.
