Public derivative of an independently reviewed research report. Private delivery details are omitted; all mathematical assumptions, proof, costs, review evidence and limitations are retained. Original source-report SHA-256: 5dfcf24fcd71d68fe24d9e4fe9d298042658f57d4440ca63bd62231c6df91a11.

Review date: 12 October 2026 UTC.

# Independent review: Q16 single-trial composition

Date: 2026-10-12. Verdict: **ACCEPT_BOUNDED** after independent sealed-candidate
inspection and cold replay. The candidate SHA-256 is
`6736ec94f37707bd02e53b2804fead56d2d7ff5a62ba3bbe85ad7e50f07128ac`.
Its 44 manifest payloads and 24 exact source-member bindings verify against
all five accepted dependency archives. The author checks and all 15 literal
mutations reproduce their recorded JSON exactly. The independently authored
checks also pass. No substantive theorem or implementation correction was
required; source-trust and whole-output boundaries were made explicit before
the immutable candidate was sealed.

## Scope and finding

The inspected adapter correctly composes the unchanged accepted sampler,
finite-word bucket/ranking/fiber selector, and companion amplitude estimator.
The proposed single-target probability theorem follows by a union bound on
shared seeds. No independence between isolation, interference, crowding, or
selection is necessary. The result is a bounded single-target inclusion and
absolute-amplitude guarantee under its spectral, tap, randomness, and source
antecedents. It is not full sparse recovery, accurate estimation of every
returned candidate, a complete sparse engine, a wall-time sparse-FFT result, or a novelty
claim.

The accepted dependency archive identities are sampler
`98c27330f248ac75c677700a872a1ab88e7a4985e2d5fc09c56098966ac533e2`,
collision `e4d0c49c2aef372ef719a22a6f55af1cdf2803ec4caa5f11539e497511e5b414`,
ranking/location `10797360653f5cd171ee8c61fa236f3b961018d361132dd9e23bdd0b6a6eabfc`,
amplitude `60f9168baa667446dc00be46e809b4b8c6c270613a124029b59293f387348718`,
and crowding `4205cbd515c153bbbbb0cda973d48d42eaed3ba2dc0b31c748c29b1fde8c38c9`.
Their exact local production code and proofs were inspected. Accepted tap
constructors were not executed or modified. Physical entropy quality and
source provenance cannot be verified by this adapter.

## Independent derivation of the joint event

Fix the whole signal, trusted true filter, target i, heavy set H containing i,
and all thresholds before drawing the current pair. Let s=|H|, L bound the
other-heavy l1 mass, E_H and E_R bound the respective spectral energies,
a_- <= |F_i| <= a_+, and rho=(5/64)2^-q. The exact sampler supplies a uniform
odd sigma and a conditionally uniform, independent tau, under its supplied
ideal-bit assumption.

The collision component's strict 3d/2 neighborhood has failure probability
at most alpha=min(1,4(s-1)/B). Outside it every other-heavy contribution to
the target bucket has true-filter weight at most rho, including the closed
stopband boundary. Its absolute interference is therefore at most rho L.
The remaining tail has second moment at most

    V_R = [rho^2 + (1+2rho)4/B] E_R.

Character averaging over tau proves that bound; the individual phase
characters do not need to be independent. Markov bounds the event |C_R|>eta
by V_R/eta^2. These statements concern the same seed experiment.

Let M bound the heavy protected-bucket union, with default min(B,2s).
The accepted crowding estimate for N_T=#{j:|Z_j|>=T} is

    delta_c = min(1, [(B-M)rho^2 E_H + (2+4rho+B rho^2)E_R]
                         / [(r-M+1)T^2]),

when M<=r<B and T>0, with the accepted endpoint rules otherwise. It is
essential that the bound uses true H, includes finite heavy leakage, and
counts >=T. It is not a deterministic per-seed energy assertion.

On the complement of these three bad events,

    |Z_h(i)| >= (1-rho)a_- - rho L - eta.

If this is at least T+2epsilon, where epsilon=(15/512)2^-k, the accepted
perturbed-rank theorem puts i in the complete returned fiber union. Equality
at this margin is allowed because every bucket outside the >=T set has
strictly smaller true magnitude.

The companion amplitude error for this same i is at most

    rho L + eta + rho a_+ + a_num,
    a_num=(63/512)2^-k.

The rho a_+ term is true-response bias and cannot be omitted. The estimator's
arithmetic certificate is deterministic and simultaneous for any supplied
finite index list, so the list selected from these same seeds needs no fresh
independent estimation draw. Union bound gives the claimed joint success
probability after subtracting a justified unconditional operational-abort
bound beta. Conditioning on returned successes cannot substitute for beta.

## Independent uniform constants and a growing witness

Assume s>=1, D>=1, a>0, a<=|F_i|<=Da, each heavy coefficient at most Da,
E_R<=a^2/64, r=4s, B>=64s, rho sD<=1/16, B rho^2 D^2<=1/256, and
a_num<=a/16. Choose T=a/2, eta=a/8, and M=2s. Then E_H<=sD^2a^2 and
L<=(s-1)Da. The target lower bound is at least 13a/16, whereas
T+2epsilon<=9a/16. The amplitude bound is at most a/4.

The isolation failure is at most 1/16. Since q>=10 implies rho<1/1024,

    V_R/eta^2 <= rho^2 + (1+2rho)/(16s) < 1/12.

Also 2+4rho+B rho^2<3, using D>=1, so

    delta_c <= [s/64+3/16]/(2s+1) <= 13/192 < 1/12.

Thus success is at least max(0,37/48-beta). These loose constants are
strictly nonvacuous without multiplying event probabilities.

For m divisible by four and m>=24, take q=m, B=2^(m/2), s=2^(m/4),
D=a=1, r=4s, and k=1. The accepted support guard w=16Bm+1<n holds and
all displayed small-leakage conditions hold. The rational signal
x_v=s/n when s divides v, and zero otherwise, has exactly s Fourier
coefficients equal to one at multiples of n/s. This proves a nonempty
growing spectral/input regime. Trusted tap existence here is supplied by
the accepted constructor theorem, not by newly executed tap fixtures.
The candidate count is J=4n^(3/4), not r. Existing executable fixtures
have B<=16 and do not directly exercise this B>=64s family.

## Independent execution and adversarial checks

The separately authored `independent_check.py` checks the inspected adapter
without executing source archives or the accepted constructor. Three actual
accepted endpoint-fixture traces use distinct sigma/tau pairs. Each consumes
exactly 19 ideal-tape bits, invokes the sample callback 1,282 times over 641
distinct addresses repeated in exactly the same order, prepares bucket roots
twice, and emits 256 distinct candidates and 256 amplitude/phase records.
Runtime instrumentation independently counts the root preparations rather
than trusting the wrapper's claimed counter.

There are 13 invalid-scalar preflight tests with no entropy, samples, or root
preparations consumed; four first/last sample failures across the two passes;
four bit-exception prefixes preserving exception identity; four invalid-bool
bit prefixes; and exact target-margin equality, just-above-margin, and beta=1
endpoints. Forty-five exact growing-family scalar checks and 314 varied
B/s/q/D checks independently reproduce the formulas and verify the regime.

Two negative controls make important limits concrete:

1. On the accepted n=1024,B=4 fixture, constant x_v=1/1024, sigma=1,tau=0,
   r=1,k=1 returns 256 amplitudes all exactly 1. Only F_0 is nonzero.
   Interpreting all outputs as the recovered vector incurs squared l2 error
   255. This does not contradict the single-target theorem; it shows why
   candidate aggregation/pruning and a full-vector guarantee remain open.
2. Repeating the callback with second-pass values increased by 2^-100 can
   leave the rounded buckets identical, and the wrapper succeeds. Its
   consistency comparison detects some source changes but does not prove
   that the callback describes one stable whole signal. That remains an
   explicit trust/assumption boundary.

Finite checks support the proof and API audit. They do not prove physical
randomness, all-input recovery, or uniform theorems by finite exhaustion.

## Costs and remaining obligations

The unchanged amplitude API recomputes the buckets. Every nonempty trial
therefore pays two full bucket invocations and root preparations, 2w sample
callback/decode operations, K=2m-1 bit-provider calls, top-r ranking, inverse
fiber expansion, J=rn/B explicit indices, and J individual phase evaluations
and output records. Both bucket reports are retained and paid. No single-read
or shared-root optimization is accepted merely because the seeds repeat.
On failure, consumed source prefixes and completed preparation remain paid.
Deterministic caps reject before source calls; no resource cap is silently
assigned a random failure probability.

Cold tap construction and provenance checking are separate from warm use of
trusted taps. Cold input acquisition/indexing may cost Omega(n ell); two
callbacks at the same address are not automatically free acquisitions.
Hashing/importing every vendored fixture and source-pin file, parsing and
output serialization, actual numeric widths, Python objects, and source
provider costs remain paid. Arithmetic O((B+J)polylog n) is conditional on
the declared width regime and sufficient slack; it is not an end-to-end
wall-time or completed sparse-engine statement.

Concrete entropy/source adapters, repetitions and medians, error/abort
composition across trials, aggregation/pruning, full-vector guarantees,
unitary conversion, downstream S6, and priority/novelty remain outside this
bounded acceptance. 
