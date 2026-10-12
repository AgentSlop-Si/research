# Independent review: Q19 common phase arcs

12 October 2026. Verdict: **ACCEPT_BOUNDED_COMMON_PHASE_ARCS**.

The frozen candidate correctly extends the existing Q19 uncertainty certificate to nonconstant rationally parameterized unit-circle arcs, including genuinely phase-correlated actual weights. Every successful positive output is a uniform lower bound on both normalized Frobenius and operator error against the specified normalized Fourier matrix. The quantifier includes all real parameters in the admitted intervals, including irrational values. The analytic argument establishes that quantifier; finite controls validate the implementation and selected identities.

No candidate change was needed. This is a bounded representation and direct-energy implementation extension of the accepted theorem. It creates no new Fourier-obstruction theorem identity, does not close the full Q19 gate, and neither replaces nor dominates the earlier singleton/box implementation or its midpoint-transfer result.

## Frozen identity and provenance

- Candidate archive: `Q19_Common_Phase_Arcs_Candidate_2026-10-12.zip`
- Candidate archive SHA-256: `c09fa7651cc21617baf557457d510116ccc41e96164a36241cf1c213cc3836a3`
- New checker SHA-256: `3197ea3c05190c23225ea9e1371fa6f2d38729966ea061208452975178622317`
- Candidate proof SHA-256: `ba7fb5f0553648931be715fe3cff217fc65ff1a0e5e69ffa2b18ca167b34a414`
- Candidate manifest SHA-256: `9d27ad230af0d2cdf70aa2ddeca304248f5dbac5d6b592aedc018a0b88b7a5ef`
- Accepted P11 proof SHA-256: `9be4a2795988244f0658fc9e90c0e7181d5d02a0325a738ee2045e3b4377ddfa`

All 19 manifest payloads, 20 checksum-list entries, 22 archive files, and seal bindings were verified. Four packaged inert sourcepins match their bytes; the fifth pin, the retained historical source snapshot, also matches the locally available source. P11 proof, predecessor contract, and predecessor independent review were compared byte-for-byte with their accepted local copies. Those historical documents were read as text only. No historical research/predecessor program was executed, imported, compiled, or parsed as code.

Only the newly authored candidate checker, its newly authored controls, and this review's independently authored checker were executed. `tests/replay_frozen.py` checks the archive binding and extracts the frozen candidate into a fresh temporary directory. The author's 1,395 controls reproduce every frozen file byte-for-byte. The independent result is likewise reproduced byte-for-byte. No external write was performed.

## Independent mathematical reconstruction

### 1. Cayley geometry, sign, and chart boundary

The chart is d(t)=u(1-t²+2it)/(1+t²). Its denominator is positive for every finite real t. The identity (1-t²)²+4t²=(1+t²)² proves exact unitarity for every admitted real parameter, not only rational samples or a midpoint. The +2it orientation agrees with the implemented formula and the stated reference weights.

The real-coordinate derivative has its only finite zero at t=0. The imaginary-coordinate derivative has zeros at t=±1. Therefore the endpoint/critical-point bounds used by the candidate are exact before anchor rotation. Complex interval multiplication by the exact unit anchor gives an outward, possibly larger, rectangle. Large finite parameters remain safe rational operations. The chart has no finite pole; it omits the point -u, approached only as |t| tends to infinity. An opposite anchor includes that point at parameter zero, but the current schema does not implement chart unions or full-circle inputs.

Interval rectangles are only enclosing sets. They are never treated as a set of exactly unitary phases. Phase unitarity comes exclusively from the parameterization. Forgetting dependency during products, conjugation, and differences can enlarge the enclosure, never shrink it below the represented actual values. The self-loop simplification d_i conjugate(d_i)=1 is exact.

### 2. One global phase identity is essential

The row convention P[i,pi(i)]=w_i gives P0=D(cP_pi)D*, with w0_i=c d_i conjugate(d_pi(i)). For a fixed simultaneous selection, the single top-level phase vector supplies the same unitary D for every occurrence. Exact commuting routes imply that every ungauged resolvent (I-cP_pi)^-1 commutes with the same half-grid Pi. Layer sums retain that property. In the product, adjacent D*D factors cancel, giving T0=D S D*, where [S,Pi]=0.

The correct conclusion is [T0,D Pi D*]=0. T0 generally does not commute with Pi itself. The independent exact family deliberately verifies this distinction. Route matrices do not need to commute with one another; they need only commute with Pi. The reviewer family uses two mutually noncommuting routes to test that boundary.

The same selected coefficient is used in the actual and reference term. Coefficient uncertainty is therefore present in both networks and remains controlled by beta. There is no omitted coefficient perturbation or separate occurrence gauge. Per-occurrence phase vectors are explicitly refused by the schema.

The pinned P11 phase-gauge floor applies to every selected unitary D. Its bound is at least 1/4 for even s≥4. This is uniform over the represented arcs; choosing a shared phase does not incur an additional midpoint perturbation penalty. Arbitrary unrelated occurrence gauges would break the cancellation argument, and this implementation does not admit them.

### 3. Damping, energies, and normalization

For a weighted permutation, the operator norm is the maximum weight modulus. Independent-box corner maxima or the residual guard gamma+||e||_1≤rho establish |w_i|≤rho<1. The exact reference bound gives |w0_i|=|c|≤gamma≤rho. Thus all actual and reference inverses exist with norm at most g=1/(1-rho). Equality at the supplied rho ceiling is admitted; rho=1 is refused. These are sufficient guards, so refusal does not assert that every represented physical instance is invalid.

Raw energy uses outward bounds for |w_i-w_tau(i)|². Flat energy uses outward bounds for |w_i-w0_i|², or the exact residual identity in correlated mode. With a=max layer beta sum, A=sum beta, and B=(ag)^(m-1)g², the accepted resolvent, telescoping, and weighted Cauchy–Schwarz identities give

- ||[T,Pi]||_F ≤ B sqrt(A E_raw)
- ||T-T0||_F ≤ B sqrt(A E_flat)

For the negative-exponent normalized Fourier target, ||[U,Pi]||_F²=2N. I independently reconstructed this for every admitted dimension N=16,36,64 using integer root-of-unity multiplicities and exact cyclotomic polynomial remainders. The complex cross term is exactly zero; normalization is by sqrt(N), and the energy radicands divide by N, not N². Reversing the Fourier sign conjugates this cross term and does not change the checked norm.

The two normalized error bounds are therefore max(0,(sqrt(2)-B sqrt(A E_raw/N))/2) and max(0,1/4-B sqrt(A E_flat/N)). Operator error is at least normalized Frobenius error. All upper quantities are independent of the selected real parameters, proving the simultaneous family assertion.

### 4. Strict thresholds, rounding, and refusal

The candidate uses a lower enclosure of sqrt(2), upper enclosures of subtracted radicals, and a final downward dyadic rounding. A separate rational binary-search square-root implementation matches 600 root controls and complete certificate recomputations. Taking the maximum preserves validity. A positive floor certifies rejection; zero is inconclusive. Neither zero nor a refusal establishes Fourier equality or feasibility.

The independent one-layer threshold family has rho=1/2, beta=1, c=1/4, broad phases, and constant residual delta. Its flat floor before truncation is 1/4-4 delta. The exact controls return 1/8 at delta=1/32 and zero at delta=1/16 and 3/32. The raw floor is zero in those fixtures, so equality cannot be concealed by another positive component.

The author's two-layer interval-residual family separately certifies max(0,1/4-16 delta), giving 1/8 at delta=1/128 and inconclusion at delta=1/64. I cold-reproduced these exact outputs. These are certificate thresholds, not physical feasibility thresholds.

If A=0, all coefficient boxes are forced to zero and the network is zero. Both target error norms equal one. Every structural, phase, route, coefficient, and damping guard is checked before this result. Zero-beta late-error cases are refused.

## Fresh independent controls

`tests/independent_audit.py` and `output/INDEPENDENT_RESULTS.json` contain:

- 300 independent arc-range recomputations and 2,700 exact rational phase samples, including rotated anchors, all extrema, and near-chart-limit 63-bit parameters
- 600 independent square-root reconstructions
- 30 complete direct-energy certificate recomputations covering all s, both weight modes, precision endpoints, 1–4 layers, and up to 8 occurrences
- 24 typed refusal controls covering nearly-unit anchors, unsupported occurrence gauges, uncertain routes, routes not commuting with the required half-grid involution, or duplicate routes, coefficient corners, damping, booleans, floats, input-bit limits, and zero-beta late failures
- Exact positive/equality/beyond-threshold controls, a fully validated zero family, and exact self-loop phase cancellation
- Exact Fourier cross-term/normalization checks at N=16,36,64
- An irrational rotated phase in Q(sqrt(2),i), checked by exact ordered-field arithmetic
- Three full matrix controls in Q(sqrt(2),i), with both inverse products, actual damping, gauge commutation, exact raw/flat energies, and both squared Frobenius transfer inequalities checked

### Nontrivial correlated family

The review supplies a second, independently constructed N=16 two-layer family. Its first route shifts y by one. The second shifts x by y mod 2, leaving y fixed. Both commute with the half-grid involution, but they do not commute with each other. Constants are 1/4 and i/4; rho=1/2; both coefficients and beta are one; residuals are +1/256 and -1/256.

The anchors include both 1 and i. Eight phase coordinates have parameter intervals [-2,2], and the others are fixed. A nontrivial correlated subset chooses one shared t for four coordinates and -t for four others. Exact matrix instances are checked at t=-1/3, 1/2, and sqrt(2). No rational approximation is substituted for sqrt(2).

The exact flat energy is 1/2048. Here A=2, B=8, and the candidate certifies a common floor of 3/16 over its entire represented continuum. The fixture and certificate are embedded in `output/INDEPENDENT_RESULTS.json`. The reference product commutes with D Pi D* and has a nonzero commutator with ordinary Pi, as it should.

### Independent-occurrence-gauge counterexample

For N=16 use route tau and c=1/4 twice. The first occurrence uses D1=I. The second uses D2 with d_0=i and every other phase one. The product's commutator with the first gauge's Pi has exact squared Frobenius norm 34816/50625, which is positive. Thus separately flat occurrences cannot be declared jointly in that fixed commutant. This counterexample does not assert that every alternative gauge is impossible or that Fourier equality is attainable.

## Resource and scope disposition

Acceptance is successful-output correctness of a bounded trusted-object exact-arithmetic reference API: s in {4,6,8}, 1–4 nonempty layers, at most 8 occurrences, 64-bit written rational components, and precision 0–128. There is no hostile parser/CLI contract, stored-rational bit budget, wall-time bound, memory-allocation guarantee, streaming implementation, fixed-word arithmetic implementation, or calibrated physical-input coverage.

O(E+N+m) rational/index operations is a sound scalar-operation accounting statement with bounded layer exponents. Integer arithmetic, gcd, and bit complexity are additional. Memory includes the parsed data and retained enclosure arrays. Process failure produces no completed certificate. The candidate does not execute the network's transform on a data vector.

The accepted predecessor's midpoint transfer remains separately valid and unmodified. This direct-energy API may return a weaker floor on singleton input; no regression/domination guarantee is claimed. General uncertain routes or routes not commuting with the required half-grid involution, reference-constant uncertainty, independently gauged occurrences, full-circle/chart unions, and production integration remain open.

## Scope and remaining work

Only the bounded common-phase-arc uncertainty sub-obligation advances. The completed next-task obligation is the extension of at least one exact singleton phase to a rigorous arc while retaining every common-reference, damping, norm, and energy hypothesis. The broader Q19 research question remains open.

This implementation extension does not change the distinct NF-01, curvature, primitive-holonomy, phase-cone or projective-equivalence theorem identities. It establishes no novelty or historical-priority conclusion.

Public derivative note: private tracking references are omitted. Ambiguous “noncommuting routes” language is clarified to mean routes not commuting with the required half-grid involution, as the reviewed proof explicitly permits mutually noncommuting routes. Original report SHA-256: `658494a0d48f70326412009137c6f58271622693148e2bc007e5cfb0134aaee5`.
