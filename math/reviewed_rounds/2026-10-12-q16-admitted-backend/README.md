# Reviewed Q16 admitted-instance backend execution

12 October 2026 UTC.

[Independent numerical refinement, full-output and cold-execution review](q16-admitted-backend-execution.md).

A freshly authored semantic refinement of the accepted HIKP numerical interfaces now executes the two-stage whole-output loop on two complete admitted Gaussian-rational inputs. This is finite execution evidence beyond the earlier theorem and trusted-callback contract. The earlier report remains a dated account of its then-unexecuted backend.

Both inputs use n=32768, B=128, q=10, w=20481, p=31, Q=66, s=2, a=D=1, k=1 and source bounds A=0, ell=21. The heavy pairs are non-cardinal: {4096,20480} and {12288,28672}. Their 1/16 tails lie at 0 and 8192. The new backend receives the complete fixed source provider, cold taps, plan and bit provider, without known-support or expected-output callbacks. The returned supports are exactly those pairs, each returned amplitude is exactly one, and the complete squared Fourier-vector error is 1/256 from the omitted tail.

The independent review checks all 10,241 cold taps against separately derived exact nearest-even values, 38,464 rounding cases, 91 separately enclosed roots, 512 actual bucket coordinates, 30 supplied-index estimates and 31 malformed/cap/source/rank controls. The full length 32768 exact algebraic dense DFT reads every coordinate and checks every Fourier output. Fresh isolated cold execution reproduces both positive runs and included negative controls with the deterministic outputs unchanged apart from labels/timings/RSS observations. Historical programs remain inert; these are new executables with reviewed semantic refinements.

The new constructor attempts W=16Q once. Its successful finite cases do not inherit a general refine-to-Wmax totality guarantee. Source bounds A=0, ell=21 remain explicit. Actual true-filter response, companion bias, input conversion, phase signs, rounding, exact n scaling and nearest-cell ties are retained.

The original t=2,u=3 tape fails, returning 42 records with 40 false positives. That failed output and paid counters remain retained and rejected. The positive study uses t=2,u=19 and a disclosed deterministic SHAKE256 label selected after the pilot failure. This is not an unbiased sample of random successes. The inherited ideal-IID theorem separately gives a formal failure bound about 0.5661134592 when beta is formally zero; this is neither the fixed tape’s success probability nor an operational abort or entropy certification.

Each positive recovery actually makes 609 bit attempts and 471,063 source calls, 23 bucket/root preparations, 1,472 bucket roots, 10,304 bucket FFT butterflies and 4,096 discarded discovery amplitudes. The two candidate unions contain 3,965 and 3,968 indices; actual phase records are 79,431 and 79,488, with 150,670 and 150,784 median-coordinate records. All false-candidate, sort, threshold and full-output work is charged. Source calls exceed the dense comparator’s 32,768 input reads, so no sublinear query or speed advantage is shown. The complete driver and separately metered negative/reviewer work have additional counts; partial interval-operation and measured-RSS diagnostics are not a complete bit-instruction or production-performance certificate.

Q16 remains open for general provider/entropy certification, a justified operational abort model, uniform executable refinement and totality, broader tail/noise and all-input relative recovery, unitary/downstream S6, practical performance and historical priority. The earlier cardinal one-sparse restriction, raw top-two obstruction and exact two-sample baseline remain valid on their original domains. No novelty or broad-gate closure is claimed.

Earlier: [Q11 two-call recovery refinement](../2026-10-12-q11-two-call-recovery/README.md). Prior scientific reports and repository visibility/licensing remain unchanged.

## Later uniform overlap proof

Read the [full b=23 Rogers–Szegő overlap review](../2026-10-12-b23-overlap/README.md), with original normalization, exact local/annulus certificates and remaining general-scope limits.
