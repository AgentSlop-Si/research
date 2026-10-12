Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical statements, source attribution, review method and remaining limitations are retained. Original source-report SHA-256: 096a2cb3f320c3e4602b80b47d3bcdcc113add7e24191f745e2e3be97ab1ecf1.

Review date: 12 October 2026 UTC.

Review-scope note: the proof below does not import the separate collision or sampler reviews as premises. Those components are now independently accepted in their own stated scopes. Their acceptance does not itself establish the useful target margins, unconditional abort composition, repetitions or full recovery required here.

# Independent review: Q16 actual-filter energy and crowding

Review date: 2026-10-12. Verdict: **ACCEPT_BOUNDED**. The sealed candidate inventory, author cold
replay, and separate reviewer checks all passed. This accepts the
actual-filter crowding lemma and scalar helper on their explicit antecedents.
Full sparse recovery and downstream S6 remain open.
No correction to the candidate theorem or implementation was required.

## 1. Reviewed object, dependencies, and trust boundary

The exact candidate identity is recorded in `REVIEW_VERDICT.json` and the
external acceptance seal. `CANDIDATE.zip` is an unchanged copy of that author
archive. The complete inventory and payload hashes are checked before safe
extraction. Source archives remain data: no accepted constructor, bucket,
selector, source provider, or accepted archive checker is executed.

The reviewer read the candidate proof, pure exact-rational production helper,
author checker, mutation runner, artifact verifier, cost and source ledgers,
and the relevant source proofs/review statements. The three dependencies are:

- True window: `60518ee0ac6d10ed796dff586da7ac414dab7c2a78b9634c1cead6ec13826e98`.
- Bucket arithmetic: `2bb05ebd459e4102bee28917c2d80fb5904b4666027b328bebad4e3e0d5e8c39`.
- Ranking/location: `10797360653f5cd171ee8c61fa236f3b961018d361132dd9e23bdd0b6a6eabfc`.

`SOURCE_BINDINGS.json` additionally identifies exact proof/review members and
nested candidate hashes. The window's Qmin=56 correction is retained. Its
signed symmetric dyadic taps, not a structurally valid arbitrary replacement,
provide the global bound |H|≤1+ρ, closed stopband |H_a|≤ρ for cyclic distance
at least d=n/B, and closed passband H_o≥1−ρ for |o|≤d/2, where
ρ=(5/64)2^−q. The exact companion value one does not make H equal to one.
The accepted negative-sign transform uses F=DFT_n(x) and Z=nU.

The new module uses only Python integers and Fraction and performs no source
reads, sampling, spectrum discovery, network calls, or external writes. Its
energy and heavy-set arguments are caller-supplied antecedents, not certified
statistics. A helper returning a number does not authenticate those inputs.

## 2. Independent derivation: deterministic energy and operator norm

For the true rational folds f_a=∑_{t≡a (mod B)}h_t x_(σt+τ), finite DFT
orthogonality gives exactly

    ∑_j |Z_j|² = n² B ∑_a |f_a|².

Cross terms within each fold remain. Applying Cauchy–Schwarz separately to
those coherent sums, using distinct support addresses, and then using
||F||²=n||x||² gives the bound K||F||² with

    K=nB max_a ∑_{t≡a (mod B)}|h_t|².

The displayed K is attained by choosing x equal to the real taps along one
maximizing fold and zero elsewhere. Thus it is the exact squared operator
norm, including the zero-window case. This argument remains valid for every
allowed seed, and the extremizer is a finite rational signal.

At a positive threshold T, the count N_T of buckets satisfying |Z_j|≥T obeys
N_T T²≤∑|Z_j|². Therefore energy strictly below (r+1)T² certifies N_T≤r.
At equality, r+1 buckets of magnitude exactly T invalidate a non-strict
certificate. T=0 counts all B buckets, even for the zero vector; r=B makes
the crowding failure event empty. The helper handles these endpoints explicitly.

The accepted n=1024,B=4,q=10 fixture has

    K=349017932929351/549755813888,

about 635, whereas its phase coefficient is approximately 2.0003052. This
supplies an actual-filter counterexample to confusing phase-averaged energy
with an identical per-seed bound. The reviewer independently attains K with
the rational maximizing-fold signal.

## 3. Independent derivation: phase moment and exact center count

Substituting Fourier inversion into the true bucket formula gives

    Z_j=∑_l F_l exp(2πiτl/n) H_(jd−σl).

For each fixed odd σ, uniform τ on all n residues cancels exactly the
l≠v cross terms when |Z_j|² is averaged. It is enough that τ be uniform
conditional on σ; σ itself need not be uniform. The coefficients F and H
and the threshold must be fixed relative to those current phases. Uniform
individual phase marginals are not a replacement for the stated character
average, and independence among the individual characters is not needed.

An equally spaced cyclic grid has one center strictly within distance d of
u when d divides u, and two otherwise. All remaining centers have distance
at least d, including the equality boundary where the stopband applies.
Because d is a power of two and σ is odd, d|σl precisely when d|l. Hence

    ∑_j |H_(jd−σl)|²
    ≤ g(l)(1+ρ)²+(B−g(l))ρ²
    = g(l)(1+2ρ)+Bρ²,

where g(l)=1+1_{d∤l}. Summing the diagonal phase moment proves the weighted
bound, and bounding g by two gives C||F||² for C=2+4ρ+Bρ². Applying Markov to
the nonnegative energy at threshold (r+1)T² proves the full-energy bound.

The factor two is not removable merely because frequencies have one nearest
bucket. A half-cell frequency sees two closed-passband responses, whose
squared sum is at least 2(1−ρ)². At the accepted endpoint this is strictly
larger than the proposed one-center constant 1+4ρ+Bρ². Closing the protected
radius from <d to ≤d would instead give three centers at an exact center;
that is a different geometry and cannot retain the one/two count.

## 4. Independent derivation: tail-aware crowding

Fix A before the seeds. For a fixed σ, let K_σ(A) be the union of the one/two
centers strictly within d of the transformed heavy frequencies. Write its
actual cardinality as s and a certified upper bound as M. The candidate uses

    M=min(B,∑_{l∈A}(1+1_{d∤l}))≤min(B,2|A|).

This set may depend on σ and remains fixed while averaging τ. Outside it,
every heavy-coordinate true filter weight has magnitude at most ρ. Exact
phase averaging cancels heavy-heavy, tail-tail off-diagonal, and heavy-tail
cross terms. It follows that

    E_τ ∑_{j∉K_σ(A)} |Z_j|² ≤ (B−s)ρ² E_A+C E_R.

If N_T>r, at least r−s+1 of those unprotected buckets reach T. Conditional
Markov therefore yields the ratio with actual s, for s≤r<B. Crucially, one
must not separately replace B−s by B−M, since that decreases the numerator.
Instead the complete ratio

    f(s)=((B−s)a+b)/(r−s+1),  a=ρ²E_A, b=C E_R,

is nondecreasing: its derivative has numerator (B−r−1)a+b≥0. Thus s≤M≤r
justifies replacing s by M in the ratio as a whole. Averaging over any allowed
σ law gives exactly the candidate bound

    min(1, ((B−M)ρ²E_A+C E_R)/((r−M+1)T²)).

The proof covers overlap among protected neighborhoods, s strictly below M,
M=r, r=B−1, empty A, zero tail, and zero heavy energy. It does not require
independence between protected centers, collisions, or crowding and target
success. The optional weighted tail coefficient and positive-gap deterministic
heavy-spill alternative also follow from the same argument.

Heavy leakage cannot be dropped. Independently evaluating the accepted
endpoint taps at the four centers gives

    H_0=16777217/16777216,
    H_d=H_(3d)=−1/33554432,
    H_(2d)=−1/8388608.

For constant rational x=1, the only nonzero Fourier coordinate is F_0=n,
yet all four true buckets are nonzero. At T=n/33554432, all four satisfy the
closed threshold, for every seed. Deleting the heavy term would falsely predict
zero failure with zero spectral tail and only one selected/protected bucket.

## 5. Independent tests, negative controls, and cold replay

`independent_check.py` and `adversarial_check.py` are separately written
reviewer checkers. They import only the inspected candidate scalar helper.
Their exact results are in the accompanying result files. The checks include:

- 20,480 single-coordinate center-geometry cases and 2,304 protected unions
- 27,776 actual-count monotonicity comparisons and 8,556 tail scalar cases
- 2,288 exact spectral/time-bucket identities in dyadic cyclotomic rings
- 496 exact fold-Parseval cases and 180 weighted full phase moments
- 304 scalar endpoint cases and 13 malformed-input rejections
- Nine direct primal-space phase averages on the pinned n=1024 actual taps
- 1,728 exact probability cases and 72 restricted phase moments on n=8
- 1,232 exact threshold equalities in those probability cases

The n=8 probability probes use explicitly described toy response arrays that
satisfy the global/stopband envelope. They are algebraic checks of the lemma,
not claimed examples of the accepted HIKP constructor. Their comparisons use
exact signs of a+b√2, with no floating threshold or sampled probability.
Likewise the toy signed-tap cyclotomic checks verify identities, not window
construction. Actual accepted-fixture tests are identified separately.

Twelve literal production-code mutations are killed independently: one
center for off-grid coordinates; deleting 4ρ; changing r+1; non-strict energy
certification; deleting heavy leakage; the wrong tail denominator; protecting
only one center; losing wraparound; dropping n from n²; replacing squared
fold energy by absolute values; dropping n from K; and summing rather than
maximizing fold operator weights.

Additional exact controls reject closed-for-strict protection with unchanged
counts, >T in place of ≥T, a τ-adaptive signal that cancels the random phases,
and conditioning away seed-dependent failures. In the latter example two
characters have unconditional squared mean two, but mean four after retaining
only constructive phases. Such conditioning cannot preserve the original
moment bound without an additional argument.

The author checker, author mutation runner, and artifact inventory are cold
replayed only after code inspection. Sealed results are compared as exact parsed JSON
with rerun outputs. Reviewer result reproduction and complete archive readback
are recorded separately. Finite tests supplement the proof; they do not prove
all parameter values by exhaustion, certify entropy quality, establish a
working recovery loop, or measure a sparse online runtime.

## 6. Composition and cost qualifications

The accepted location theorem uses both N_T≤r and target magnitude at least
T+2ε, with ε=(15/512)2^−k in F units. The candidate supplies a bound for the
first bad event. A separately established target-failure probability combines
by union bound; no independence is needed. True-H interference and bias remain,
and crowding alone does not establish the target margin or recovered support.
No pair-collision or sampler candidate is used as an accepted premise here.

A current fixed signal, fixed A, and seeds with conditional uniform τ are
required. Sigma-measurable choices can sometimes be analyzed conditionally,
but that does not authorize a τ-adaptive A or reuse the separate fixed-A
collision result outside its quantifiers. Prior adaptive history is harmless
only when the current conditional seed law and signal/set relationship meet
the stated fresh-trial assumptions.

Successful execution must cover every seed, or separately justified
unconditional abort probabilities must be charged. A value-dependent source
failure cannot be removed by conditioning on returned results. Repetition,
median/voting, candidate aggregation/pruning, output error, unitary conversion,
and downstream S6 are not supplied by this lemma.

The scalar Fraction bounds are conservative with actual intermediate widths
paid. The protected-set routine sorts and deduplicates only explicitly supplied
indices and does not scan n frequencies. Empty-input costs still include
ordinary validation/setup; use |A|+1 when expressing a literal bound including
zero. The operator-helper specialization uses accepted tap/index widths;
for generic raw helper inputs their actual serialized widths must also be paid.

Exact true folds differ from the accepted routine's rounded intermediate
folds. Recomputing them from rational samples can have denominator growth;
the candidate explicitly charges this optional path and does not present it
as an O(B polylog n) online replacement. Energies, norms, and A are not free
spectral discoveries. Retain all accepted tap preparation, root preparation,
source acquisition/indexing, numeric widths, parse/hash costs, abort-prefix
work, raw reports, and J=rn/B explicitly emitted locations. Nothing here
establishes a sublinear wall-time claim or eliminates a possible dense source
acquisition cost.

## 7. Attribution and remaining scope

The reviewer independently reopened the [HIKP primary paper](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf)
on 2026-10-12. Section 4.1 describes the bucket/location setting, and Lemma 4.2
uses a crowding bound and a target event to justify location. The new candidate's
exact constants, true-dyadic-window assembly, and finite-word interface are
local derivations. Parseval, Cauchy–Schwarz, character orthogonality, and Markov
are classical. No priority or novelty upgrade follows.

Independent bounded acceptance covers actual-filter phase-energy and >=T crowding bounds, including the tail-aware heavy-leakage refinement, exact deterministic energy/operator norm and endpoint-safe scalar helpers. Full recovery, all-input relative-l2 guarantees and downstream S6 remain open. Concrete
entropy/source evidence, useful target/interference parameters, finite-word
repetitions and outer composition, every abort, and all existing scope/cost
qualifications remain. 
