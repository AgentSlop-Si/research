# Exact structured ALG-034 to theorem-parameter Q16 BUCKETS

17 October 2026. New restricted integration candidate, awaiting independent review.

## 1. Exact result and scope

The live entrypoint `ScaleAdapter.execute(raw,state,...)` executes the pinned exact structured ALG-034 producer on separately supplied original input, checks its returned exact period-four transform, normalizes it without rounding, and invokes a new certified constant-source BUCKETS backend. It returns a fully materialized immutable vector of 131,072 dyadic complex bucket values, each within 2^-464 of the same ideal Q16 BUCKETS operator used by the reviewed component.

This is a restricted genuine theorem-parameter instance. It is not a reduced fixture: beta is exactly 5/56 and every theorem provenance check in the reviewed `theorem_spec`/`WindowSpec.validate` actually runs and passes. It does not invoke or reproduce the legacy rounded tap-fold/FFT execution. The exact algebraic producer and this frequency-domain BUCKETS implementation are new backends with directly proved target correspondence. Neither is relabeled as execution of the accepted serial producer.

The full Q16 recovery algorithm, random schedules, amplification, outer all-length transfer, and that transfer's separate t<M guard are not run or closed. Its exact recovery decision threshold was not available in the pinned component sources. Section 7 supplies a separately labeled local half-threshold consequence, not a substitute for an unavailable recovery theorem. The mathematical instance is valid for every specified window/BUCKETS guard; no claim is made that every separate outer-transfer guard has been verified.

The admitted adapter input is exactly x=2^-F delta_0, at N=2^28, represented by the structured producer's canonical sparse input grammar. B_A=N, any valid odd a and phase beta_A are allowed; singleton blocks give P x=x. The producer has a larger quarter-axis family, but other family members are explicitly rejected by this adapter. No general sparse or arbitrary-input claim follows.

## 2. Sources and trust boundary

The unchanged accepted compact-window source is copied as `vendor/compact_window.py`, SHA-256 e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59. All numerical bodies and imports were inspected as text before execution. This backend executes its exact Ledger, WindowSpec/theorem_spec, Interval, Machin pi setup, outward quotient, even-power, clipping and nearest-even primitives. It never invokes its time-tap preparation or the legacy BUCKETS FFT.

The retained `vendor/buckets.py` and `vendor/paid_source.py` are inert source references here; they are not imported by the new numerical path. Their guards/formulas were read in full. The predecessor's independent bridge review and resource/contract/proof text are included as inert source references. They explicitly permit an independently certified equivalent input representation, while not treating an arbitrary compressed label as a valid source.

The exact structured producer is separately authored and pinned at `vendor/structured_producer.py`. The full source was inspected before import. Its proof belongs to the companion producer packet. This adapter uses its actual `execute`, not a supplied `ExactRun`, caller certificate or attestation. Successful source normalization therefore inherits a computed exact Fourier value bound to the caller's original sparse input.

Trusted correct Python/stdlib, correctly executing pinned sources, no concurrent caller mutation during validation, no hostile reflection/monkeypatching, and independently retained original context are assumptions. This is semantic validity, not authentication of an unknown external origin or proof of historical remote execution. Replacing both original context and claim changes the statement under test. Digests detect byte substitution, not mathematical truth.

## 3. Exact instance, precision and normalization

The exact downstream parameters are

- m=28, M=N=268,435,456
- beta_Q=5/56, beta_Q*m=5/2 >= 2
- k=2^ceil(2 beta_Q*m)=32
- B_Q=2^ceil((1/2+beta_Q)m)=131,072=4096k
- T=M/B_Q=2048, ell=8B_Q=1,048,576
- r=2m+1=57, g=T/4=512, H=3T/4=1536
- W=2r(ell-1)+1=119,537,551 < M
- P_Q=16m+16=464, rho=2^-464

Thus B_Q divides M, T>=4, the beta domain, sparse ratio, and compact-support guard hold exactly. Every odd residue 1<=sigma<M and every 0<=tau<M is admitted. The constant source makes the result independent of both; the actual call still validates and charges them.

For the fixture F=0, x=delta_0, the exact producer has B_A=N, W_in=G=1, H_A=1, A=1, K=0, and

    C = 2^(N+3m+6) = 2^268435546,
    c = N+90,
    q = 464,
    p = max(W_in,c+t+1,c+q+G+2) = N+557 = 268436013

at t=16. Its exact output is y_j=2^-14. The formal p-grid numerator is 2^(p-1-14)=2^268435998 and kappa=1-p=-268436012. They are stored as a typed common exponent and four unit numerators. No 268-million-bit precision-grid integer is constructed, nor is that exponent-only representation passed off as a literal legacy integer array.

For general admitted F, y_j=2^(-F-14), alpha=2^-F, so v_j=y_j/alpha=2^-14 exactly. Norm squared is M*2^-28=1, in particular norm>1/2. Its actual producer and requantization errors are both zero. The formal accepted serial-policy allowance still passes honestly:

    (C*2^kappa)/alpha = 2^-466 <= rho.

The adapter checks this exponent inequality against the actual specialized policy, and requires q>=464. It never constructs the huge C or p-grid integer. The second negative-sign unitary transform is R(Px)/alpha=delta_0, not the original-input Fourier transform Ux.

## 4. Same ideal BUCKETS operator, different evaluation

Let c_t be the exact coefficients of the centered 2r-fold convolution of the length-ell normalized box, with support |t|<=r(ell-1). Its discrete Fourier transform is

    Phi(a) = [sin(pi*ell*a/M)/(ell*sin(pi*a/M))]^(2r),

with the limiting value 1 at a=0 mod M. Centering cancels the box's phase; the even exponent makes Phi real, nonnegative, M-periodic and even. Let

    C_Q = sum_(a=-g)^g Phi(a),
    D_H(t) = sum_(a=-H)^H exp(2*pi*i*a*t/M),
    w_t = M*c_t*D_H(t)/C_Q.

These are the exact window quantities constructed by the pinned source. In particular C_Q>=1. The ideal reviewed BUCKETS operation for v is the B_Q-point fold/DFT of w_t*v_(sigma*t+tau), scaled by 1/sqrt(M). Since v is the positive constant 1/sqrt(M), all sigma/tau dependence disappears. Finite sum interchange and Fourier orthogonality give, for h=jT,

    bucket_j = (1/M) sum_t w_t exp(-2*pi*i*j*t/B_Q)
             = [sum_(a=-H)^H Phi(jT-a)] / C_Q.

No approximate identity or rounded-root power is used. W<M prevents support aliasing in the original signed window representation. The finite Fourier identity also holds directly with the signed support. Each ideal bucket is real and nonnegative, and bins 1 and B_Q-1 are equal by evenness.

The direct backend computes C_Q, the j=0 numerator, and the j=1 numerator by streaming Phi(a), 1<=a<=T+H=3584. It retains only the three pairs of running interval endpoints. Numerator |sin(pi*ell*a/M)| has period M/ell=256 and reflection symmetry, so 129 sine enclosures are prepared once and reused. The even power removes the discarded numerator sign. Denominators use the intended positive sin(pi*a/M), since 1<=a<=3584<M/2.

This is an algebraic evaluation of the original operator. It neither constructs an approximate different window nor silently removes the cost of an actual FFT. There is no FFT in this new path, and all needed roots/sine evaluations are explicitly paid.

## 5. Far-bin certificate and exact window delta

For every j outside {0,1,B_Q-1}, every circular distance d from jT-a to zero, |a|<=H, is at least 2T-H=5T/4 and at most M/2 after reflection. On that interval, sin(pi*d/M)>=2d/M, while the numerator sine magnitude is at most 1. Consequently

    |sin(pi*ell*d/M)/(ell*sin(pi*d/M))|
      <= M/(2*ell*d) = T/(16d) <= 1/20.

Therefore, using C_Q>=1,

    0 <= bucket_j <= (2H+1)/20^(2r) = 3073/20^114 < 2^-464.

The last comparison is checked by exact integer multiplication, 3073*2^464<=20^114. Returning exact zero at every such bin is within the original rho budget. No accumulated tail or length-M scan is needed: this one proved bound applies to each of the finitely many output bins.

The original window pass/stop delta is separately retained:

    delta_window = (2H+1)/16^r = 3073*2^-228 <= M^-4=2^-112.

This exact inequality is checked. Window approximation delta and numerical rho are distinct quantities and are never substituted for each other.

## 6. Certified three-bin numerical computation

All intervals use exact integer endpoints on the K=560 grid. The pinned Scalar setup supplies a paid finite outward Machin pi enclosure. The new ShortTaylor sine evaluator performs the same exact rational period/reflection reduction and uses the midpoint of the outward pi-angle interval. Each Taylor term is propagated by outward floor/ceiling arithmetic. The angle midpoint radius is added using the real sine 1-Lipschitz bound.

There are exactly 128 odd sine terms, through degree 255. The degree-256 Taylor polynomial has the same value because its even coefficient is zero; its remainder for |x|<=2 is at most 2^257/257!. A shared exact factorial and scaled tail ceiling are constructed once. The code checks this ceiling is <=1 on the K-grid. This fixed finite certificate justifies the smaller series count; no tolerance loop or empirical floating estimate selects it.

For a positive denominator interval, the pinned all-corner quotient encloses the exact normalized sine ratio. Intersecting with [-1,1] is justified by the normalized Dirichlet-kernel bound. The pinned even endpoint power exactly encloses power 114, including a zero-crossing interval. Clipping to [0,1] is valid. Streaming interval sums enclose the true normalizer and the two distinct numerator sums. A final outward quotient therefore encloses each true bucket.

Midpoints are rounded by signed ties-to-even to the P_Q=464 grid. Let u=2^(560-464) and let e be the maximum distance between the chosen numerator times u and either interval endpoint. The exact integer test e^2<=u^2 certifies absolute complex error <=2^-464; imaginary part is exactly zero. Three certificates are retained, with the side certificate duplicated at B_Q-1. The actual run passed all of them.

Every bin is thus within rho. Since rho<=24(m+1)M^2*rho, this satisfies the published combined BUCKETS allowance with slack. Zero producer/normalization errors introduce no additional source perturbation. The backend does not claim bit-for-bit equality with the legacy numerical implementation, only the same ideal target with the stated error guarantee.

## 7. Bucket threshold, and what is not recovered

A local explicit threshold 1/2 is valid for this one known one-sparse target. The center ideal bucket is >=1 because H>=g and Phi>=0. For every other bin, circular distance is at least T-H=g=T/4, so the same argument gives normalized sine ratio <=1/4, hence bucket_j<=3073/4^114=delta_window. After an error at most rho, center remains above 1/2 and every other bucket remains below 1/2. The actual complete output has exactly index zero above this threshold.

This proves a useful diagnostic separation for the instance. It is not claimed to be the exact decision rule of an unexecuted Q16 frequency-recovery implementation. General isolation, location recovery, amplitude estimation, probability, amplification, separate outer transfer and its t<M condition remain outside this packet. `full_recovery_executed` is always false.

## 8. Semantic binding and adversarial controls

ScaleAdapter never accepts a purported producer result. Each execution calls the pinned structured producer on original raw/state, checks nonzero exact status, N=2^28 and the returned period ((1,0),)*4, then derives alpha and source exponent from the computed result. The exact four-point transform is invertible, so this constant unit period identifies the admitted raw unit impulse within the producer's quarter-axis grammar. Every input scale and phase/state binding remains in the packet.

The prepared constant engine is reused as paid trusted state, just as an accepted prepared window/root engine may be reused. Its immutable output tuple is independent of the original caller lists. Each execute revalidates producer input and downstream sigma/tau. A verifier bounds the entire proposed packet, executes the producer again against separately supplied original arguments, reconstructs the expected complete packet from the already paid numerical engine, and compares typed canonical bytes. Claimed digests or editable flags cannot authenticate changed output values, changed source scale, substituted input, or altered policy.

This replay does not recompute numerical preparation on every call. The constructor cost is paid once, engine source/private state is trusted, and the packet includes all B output coordinates for exact comparison. Fresh ScaleAdapter construction recomputes all numerical preparation, as tested. No hostile mutation of private engine state is in the model.

## 9. Paid resources and deployment limits

The deployment domain is one fixed theorem parameter set, not an unbounded-cap theorem. The structured producer has its own finite caps/receipts. This adapter only admits its constant N=2^28 branch. The numerical path permits at most 30,000,000 metered arithmetic operations, 70,000-bit recorded numeric integers and 4,000,000 cumulative logical allocation slots. Exceeding a guard emits no successful result. Integer intermediates are bounded before shifts; binary-operation rejection can materialize a finite at-most-double-width temporary before its post-operation width check. The exact executed maximum was 63,840 bits. No claim of a strict Python peak-allocation cap or host availability is made.

The actual numerical run used 6,441,192 recorded integer operations before extended checks. It evaluated 3584 Phi terms, prepared 129 numerator sine enclosures, paid the denominator sines, the single Machin setup and shared factorial tail, maintained the normalizer/numerator intervals, certified the three bins and wrote all 131,072 outputs. Its peak recorded numeric width includes the exact integer endpoint powers and their denominator, not just the 560-bit grids. All arithmetic is charged by the pinned conservative schoolbook model; allocated slots, control/index work, copies and cumulative storage are charged as well. The observed 42-second run is not a complexity or CPU/RSS claim.

The old literal path would require an N-position source tuple, W=119,537,551 taps, 6,873,409,239 exact sliding-convolution cells, 65,536 FFT roots and 1,114,112 FFT butterflies. These are not unpaid work in the new path: the proven frequency-domain identity replaces them. New actual FFT-root preparation and butterflies are zero, while 129 sine roots and all direct scalar evaluations are explicitly charged. The full B-output allocation remains real and paid. At this p, materializing and serializing the old p-grid array would also have a 268,435,999-bit nonzero numerator at each of N positions; exponent factoring is part of the new representation, not a claim that such a literal scan was performed.

Source reads/hash/parse/import are paid on each preparation, even if a trusted module is already loaded. Numerical Meter charges actual source bytes with a deliberately oversized quadratic bound. The integration receipt additionally includes fixed 2^75 work and 2^42 storage envelopes for bounded dependency loading. The producer receipt and its declared export envelope are added. Every attempted producer invocation additionally incurs one fixed canonical/control envelope, including bounded property JSON decodes, header assembly and rejected attempts within the declared input caps. Arbitrarily oversized caller-allocated in-memory objects receive no successful resource certificate. No root/window setup is treated as an oracle or free external dependency.

Typed canonicalization permits at most 8 MiB, 500,000 nodes, depth 16, list length 131,072, dictionary length 64, string length 2048, and 4096-bit serialized integers. It checks the full tree before encoding. JSON intake bounds text and UTF-8 bytes, forbids duplicate keys/floats/nonfinite numbers, bounds each integer token and reuses the canonical-tree check. A parse can allocate a bounded 8-MiB syntax tree before post-parse structural rejection; this is explicitly covered. Unknown subclasses and serialization hooks are rejected. Each bounded export/parse/copy/compare is charged by an intentionally generous 2^90 schoolbook work / 2^44 cumulative storage envelope. Exports performed after a receipt are separate operations; callers must add the documented per-export charge or obtain a receipt with the actual count. These logical cost upper bounds are very loose, not measured machine RAM or practical operation budgets.

## 10. Minimum-size obstruction and its resolution

Write y=beta_Q*m>=2. The sparse ratio requires

    ceil(m/2+y)-ceil(2y) >= 12.

But ceil(A)-ceil(B)<=ceil(A-B), so for m<=26 the left side is <=ceil(m/2-y)<=11. Thus every instance satisfying the known outer beta*m guard and window sparse ratio needs m>=27. The witness m=27,beta=2/27 has B=65536,k=16 and W<M. A square power-of-two N, needed by this dyadic exact impulse backend, first becomes possible at m=28. Our chosen beta=5/56 minimizes T for this m while preserving the sparse guard and compactness.

This is a lower bound for these guards, not a global impossibility theorem or an arbitrary imposed resource ceiling. The old N<=4096 adapter could host none. The new restricted exact source and certified frequency-domain operator remove that deployment obstruction for this actual instance without raising a literal N-array cap or allocating an unbounded object.

## 11. Completion boundary

The independent-review target is the source-pinned restricted live exact producer -> exact normalized source -> original ideal BUCKETS operator at genuine theorem parameters, with full output, error and paid resource accounting. Its tests are fresh positive/adversarial controls, not old replayed test programs. Independent acceptance of this target would close that specific structured integration gate. It would not close arbitrary ALG-034 input deployment, general Q16 sparse recovery, all-length dispatch, randomized guarantees or any universal FFT speedup claim.
