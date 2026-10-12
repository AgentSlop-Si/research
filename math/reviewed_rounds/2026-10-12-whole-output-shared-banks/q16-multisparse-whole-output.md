# Independent review: Q16 two-stage multi-sparse whole output

Date: 2026-10-12. This document records the review reasoning; the final verdict
is effective only for the immutable candidate hash and successful cold replay
recorded in REVIEW_VERDICT.json. No historical executable was run and no external
write was performed.

## Scope and result

The bounded composition is mathematically sound under its complete declared
source, spectral separation, trusted arithmetic and ideal-bit assumptions.
The new wrapper executes orchestration against trusted callbacks; it does not
supply or independently execute the complete accepted HIKP backend. That
separation is essential to the acceptance. Q16 remains progressed/open.

The genuine new scope is multi-sparse heavy-support recovery, including all
false-candidate removal and all returned amplitudes, in a stable observed signal
with a small Fourier tail. It is not recovery of the full nonzero spectrum when
that tail is nonzero, recovery of an unspecified clean signal under varying
measurement noise, exact amplitudes, or an all-input relative-to-tail theorem.

## Independent probability and error audit

Fix the whole signal and heavy set H, with s>=2, amplitudes in [a,Da], and
nonheavy squared Fourier energy at most a^2/64, before the full ideal bit tape.
The inherited discovery theorem gives each fixed heavy inclusion probability
at least 37/48. Independent seed blocks bound its omission from all t discovery
lists by (11/48)^t; the union over the s heavies costs s, without assuming any
independence between different heavies.

For every fixed estimation index i, including a false candidate, at most s
heavy competitors have to be excluded. The accepted strict radial event has
probability at most 4/B per competitor, so the union costs at most 1/16.
Outside this event their actual-filter leakage is at most rho*s*Da. Since every
coefficient has magnitude at most Da, the self-response bias adds at most
rho*Da. The stronger rho*(s+1)*D<=1/16 therefore pays both terms.
The nonheavy interference excludes i itself. Conditional phase orthogonality
and the accepted true-filter bounds give second moment at most
[rho^2+(1+2rho)*4/B]*E_tail. Markov at a/8 costs less than 1/12. Neither this
bound nor its combination with the heavy event assumes independence within a
trial. Together with arithmetic error at most a/16, each fresh estimate has
complex error at most a/4 with failure probability at most 7/48.

Conditioning on the complete discovery history in the ideal, all-success
experiment fixes the adaptive union C while leaving every fresh estimation
seed independent. This legitimate history conditioning is distinct from
conditioning on operational success. For each fixed i in C the number of bad
estimates is dominated by Binomial(u,7/48). With u odd, its majority tail is
b_u. The all-candidate union costs |C|<=min(n,tJ), not s. Averaging over the
discovery history is valid. Reusing discovery estimates or seed blocks would
not justify this argument.

A strict majority of estimates in the complex a/4 ball puts both coordinate
medians within a/4 of the corresponding true coordinate. The resulting
complex radius is sqrt(2)*a/4. An independent three-record example shows that
this loss is real: two good errors (a/4,0),(0,a/4), plus one bad error
(a/4,a/4), have coordinate median (a/4,a/4). Using a/4 as the final complex
radius would be wrong.

All heavy candidates are strictly above the a/2 magnitude threshold. Every
nonheavy coefficient has magnitude at most a/8, and
(a/2-a/8)^2 - (sqrt(2)*a/4)^2 = a^2/64 > 0.
Thus every false candidate is strictly below threshold. The inclusive exact
squared-magnitude test has no equality loophole on the good event. Correct
heavy inclusion plus simultaneous median accuracy gives precisely H as the
returned support, and the complete squared Fourier-vector error is at most
s*a^2/8+E_tail, including omitted tail coordinates.

The final failure bound is

    min(1, s*(11/48)^t + min(n,tJ)*b_u + beta).

Beta must be a separately justified unconditional bound for any abort in a
coupling to the full ideal tape; it is added once. It is not an empirical
success rate or permission to condition away bad seeds. Source hangs and
arbitrary correlated bits are not covered by supplying an invented beta.

## API and execution boundary

An early API ambiguity was corrected before sealing. The accepted single_trial
routine draws its own seed, while this new wrapper draws seeds and passes them
to discover(sigma,tau,r). The callback contract now specifies the two unchanged
accepted location and supplied-location calls at that seed, with the repeated
bucket consistency check. It is not claimed to invoke the old seed-drawing
wrapper unchanged. The new little-endian seed map differs from the predecessor's
MSB-first map, but independently enumerates the same product-uniform affine
pairs and consumes exactly 2m-1 physical bit-provider calls per trial.
Malformed callables now reject before entropy consumption.

Output shape checks do not authenticate trusted taps, the full source, numerical
certificates, spectral hypotheses or actual provider behavior. Numerical widths
and backend source preflight are external prerequisites to these new callback
contracts. The wrapper's backend count fields are required successful-backend
counts, not measured HIKP counts. The retained B=4 tap fixture is inert context only; no new complete HIKP
backend replay is claimed or performed.

## Costs and comparator

Each of t discovery calls still pays both bucket/root preparations, 2w sample
callbacks and all J=4sn/B individual phase/amplitude records, although those
amplitudes are discarded. Fresh estimation adds u bucket/root preparations,
uw callbacks and u|C| phase records. Total successful counts are (t+u)(2m-1)
physical bit calls, (2t+u)w sample calls, 2t+u roots and tJ+u|C| phases.
The inherited arithmetic widths and cold Q>=56 tap construction remain paid.

The new sort/deduplicate work is charged on every discovery round, not once.
Exact rational record checks, two coordinate sorts per candidate, squared
thresholds, 2u|C| stored coordinates, seed traces, all possible |C| output
records, allocations, parsing, hashing and serialization remain paid. The
pooled set can reach n; only the good-event output count is s. Source acquisition
or indexing can cost Omega(n*ell), and arbitrary address-dependent provider
work is not hidden in callback counts. Every failed prefix remains spent.
The full ledger is conservative and does not claim an executable timeout,
constant-bit real arithmetic, measured RSS or a production speed advantage.

The equal-access dense certified DFT comparator is legitimate: uniform absolute
coordinate error at most a/4 permits deterministic thresholding on the same
spectral promise, with the stronger s*a^2/16+E_tail squared-error target. All
roots, precision, n input reads, storage and dense arithmetic are paid. It is
not implemented or benchmarked here. The old exact two-sample cardinal method
continues to dominate its old one-sparse subdomain, but cannot identify general
members of this new multi-sparse domain.

## Independent evidence

The source-binding checker reads accepted archives as inert bytes and verifies
eight document/fixture members against their archive hashes and the candidate
copies. It does not execute their Python files.

Fresh exact geometric controls enumerate 10,922 bad subsets to check binomial
majority tails, prove the strict squared threshold gap, show the necessary
sqrt(2) loss, and expose both success-conditioning and reused-seed failures.
Exact cyclotomic-ring DFTs at n=16,32,64 verify a whole Gaussian-rational source
with heavy support {n/8,5n/8}, unit heavy coefficients and a 1/16 DC tail. Its
heavy frequencies are non-cardinal. The independent Parseval checks use the
unnormalized factor n correctly. These algebraic controls do not execute the
large admitted HIKP backend or expand the theorem to the small test dimensions.

The newly authored wrapper is independently checked on a non-cardinal-compatible
two-heavy spectral example with a nonzero DC tail. Sixty bounded controls cover
exact medians, all-candidate pruning, scaled threshold equality, numerical/type
and resource preflight, malformed backend records, original exception identity
and precise bit prefixes. All 2,730 possible affine pairs for m<=6 are independently
exhausted. Twelve literal mutations of only the new wrapper are killed, including
false-support union size, lost repetition powers, omitted beta, reused estimation
seeds, median errors, threshold scaling/strictness and a missing discovery pass.
An initially clipped probability control was strengthened with a nonvacuous
case so that dropping beta is actually detected. Test counts are bounded evidence,
not the proof of the uniform theorem or certification of a real entropy source.

## Scope and remaining work

The accepted scope is a bounded conditional whole-output composition. Its exact spectral gap, unknown heavy set, fresh second-stage seeds, whole candidate-union multiplier, companion bias, vector-error units, global unconditional abort condition and complete costs are essential. The theorem is proved, but accepted-backend integration for this new loop is not executed. The earlier raw top-two obstruction, cardinal-only one-sparse repair and its stronger two-sample baseline remain valid.

The broader Q16 construction remains open. Concrete entropy and stable-source certification,
a directly wired and independently executed accepted backend, broader noisy/tail
regimes, all-input relative-error recovery, unitary/downstream S6 integration,
performance and primary priority remain open. No novelty upgrade or general full-engine validation follows from this review.

Derivative note: private tracking/integration instructions are omitted or restated as mathematical scope. Complete proof, model, evidence, costs, source limitations and open obligations are preserved. Original report SHA-256: `6b2666c70883b182911955c7a1cb31b55344d22560554e94cdcb318704588c06`.
