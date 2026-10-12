Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematics, source attribution, limitations and review method are retained. Original source-report SHA-256: ae504917e9ce27987f771c6572e35bdf6dc8f285219eccf6aef320ec2a61bf44.

Review date: 12 October 2026 UTC.

# Q16 companion amplitude estimator: bounded independent acceptance

## Verdict and immutable target

**ACCEPT_BOUNDED.** The supplied-location companion estimator and its numerical
error theorem are accepted on the stated trusted-tap, stable-source and finite
representation contract. This is an additional completed component of Q16; it
does not close Q16, STR-Q1, the sparse engine or its recovery obligations.

The sole author candidate is `CANDIDATE.zip`, 411,611 bytes, SHA-256
`d6209520cebbbf6eb631216216597d017888cf0238112b0bb5e3fd4efbf43b76`.
The estimator implementation has SHA-256
`10fd34a6f24e6a74ba49e0ee427b8a527eac21729352d653826cb21fca630cfc`.
No author code or candidate ZIP byte was changed during review. Its manifest,
all seven fixtures, unchanged accepted bucket code, nested accepted window
archive were independently verified. The older constructor is read as evidence, not executed.

The new checker was written independently, imports no author test oracle,
and uses rational outward radical intervals instead of production pi/Taylor
root construction. A separate exact cyclotomic-ring computation checks the
complete Fourier identity, including every interfering frequency. Author tests
were also rerun in a separate extraction; all non-timing result fields matched.
The independent checker was then rerun from a new directory against a new
candidate extraction. See the byte-bound cold replay receipt.

## What is accepted

For every admitted trusted window, stable rational complex input, odd integer
sigma, integer tau, finite explicit list of supplied indices and integer k>=1,
the returned values simultaneously approximate

    E_i^D = exp(-2*pi*sqrt(-1)*tau*i/n) n U_{j(i)}

with exact rational certificate

    |Y_i - E_i^D| <= a <= (63/512) 2^-k < 2^-k/8.

The companion denominator is exactly 1 on the selected closed passband.
It is not the true tap response H. The accepted actual recovery statement is

    |Y_i - F_i| <= |C_i| + (5/64) 2^-q |F_i| + a.

No small value, probabilistic guarantee, measured bound or authentication of
C_i is supplied by this implementation. The exact true-response source
estimator E_i=E_i^D/H_o is well-defined, with

    H_o >= 1-(5/64)2^-q >= 1-5/65536 > 0.9999.

The companion substitution is therefore controlled but is not free. Both
interference and response bias must remain visible in every later use.

## Independent Fourier, phase, scale and routing derivation

Define F_l=sum_v x_v exp(-2*pi*sqrt(-1)*l*v/n). Fourier inversion inserts
a factor 1/n and the opposite exponential sign. Substitute that inversion
directly into the signed-support raw bucket. This gives

    n U_j = sum_l F_l exp(2*pi*sqrt(-1)*tau*l/n)
                      H_{j*n/B-sigma*l}.

With u=sigma*i mod n, d=n/B and v=floor((2u+d)/(2d)), the exact route is
j=v mod B and o=u-v*d. Its offset satisfies -d/2<=o<d/2. Thus upward half
ties, wraparound and their adjacent integers all remain in the accepted
closed passband. Symmetry of the real taps makes H_{-o}=H_o. Multiplication
by exp(-2*pi*sqrt(-1)*tau*i/n) therefore yields exactly

    E_i^D = H_o F_i + C_i,
    C_i = sum_{l != i} F_l exp(2*pi*sqrt(-1)*tau*(l-i)/n)
                           H_{j*n/B-sigma*l}.

Neither location discovery nor a magnitude decision is contained in this
index calculation. Reducing large signed inputs modulo n preserves it.
Repeated supplied indices are permitted and paid.

The primary paper uses the positive-root Fourier convention. Its Section 4.1
step 6 identifies response division after inverse translation, and Lemma 4.1
identifies the probabilistic estimation context. The equations above are a
fresh derivation in the candidate's declared negative-sign, unnormalized
units; the factor n is indispensable. They are not a claim that the paper
certifies this code's roundoff or its deterministic recovery.
Source checked 2026-10-12:
[Hassanieh, Indyk, Katabi and Price, Simple and Practical Algorithm for Sparse Fourier Transform](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf).

The independent checker exhausts 209,920 route instances over all frequencies
of all seven fixtures and five signed multipliers. It also verifies a full
1,969,152-term spectral sum for a three-impulse complex rational signal in
Q[zeta]/(zeta^(n/2)+1), using integer coefficients on the accepted tap grid.
This check proves exact equality of the direct time-domain polynomial and
the complete frequency-domain polynomial for that case. It separately
checks the desired term plus all other terms; interference is not set to zero.

## Uniform arithmetic proof and totality

Let R=w*2^A, M=nR, c=ceil(log2(w)). Each tap has modulus below 1/2 and
each complex queried sample has modulus at most sqrt(2)*2^A, so |U_j|<=R
and |nU_j|<=M without isolation, cancellation or assumptions on the unqueried
samples. Choose kappa=k+m+3. The unchanged accepted bucket theorem gives
raw error at most (15/64)2^-kappa. Exact m-bit left shifts give

    e_B <= (15/512)2^-k.

The production phase has per-coordinate error at most 2^-v, where
v=k+m+A+c+7. Its complex error is at most eta=2^(1-v). Multiplying the
two fixed-grid complex values uses exact integer products and sums. The
last coordinatewise ties-to-even rounding has complex error at most
e_out=2^-(k+4). Therefore

    |Y_i-E_i^D| <= e_B + eta(M+e_B) + e_out = a.

Since M<=2^(m+A+c), e_B<1 and M>=1, the middle term is at most
2^-(k+5). In units of 2^-k/512, the three contributions are bounded by
15, 16 and 32. Their total 63 is strictly below 64. This establishes
the all-admitted-input theorem independently of finite test success.

For the phase routine, Machin's identity has the correct angle branch.
The two alternating arctangent tails are bounded by their next terms.
At Npi=v+12 the combined raw error is smaller than 2^-4Npi; compression
to v+16 fractional bits leaves pi error below 2^-(v+16). Centering the
exponent gives an angle of magnitude below 4 and no amplification of this
pi error. The exact cosine and sine Taylor polynomials at that rational
angle have the stated factorial remainders. For N=max(32,v+12), use
(2N)!>=N^N to bound both remainders by 2^-N. The angle error plus Taylor
error plus final real rounding is strictly smaller than 2^-v. Cardinal
roots are returned exactly. All loops have explicit finite bounds, so no
unknown root oracle, adaptive numerical stopping condition or probabilistic
arithmetic abort enters this theorem.

The scalar quotient helper's formula is exact for every positive dyadic real
denominator. It uses signed quotient/remainder ties-to-even once per final
coordinate. In this estimator it is called only with numerator 2^(q+6) on
the q+6 grid, namely denominator 1. Arbitrary helper inputs are not evidence
of true-response provenance or a complex-denominator stability theorem.

## Response and interference: the essential limitations

The identity E_i^D=H_oF_i+C_i and |H_o-1|<=rho, rho=(5/64)2^-q,
immediately prove the recovery inequality. They also prove

    |Y_i-E_i| <= a + rho*M/(1-rho).

If an independently justified event supplies |E_i-F_i|<=T_i, then

    |Y_i-F_i| <= (1+rho)T_i + rho|F_i| + a.

This is deterministic event transfer. It neither produces nor certifies
independent uniform random bits or the probability of that event.

For the candidate's near set, cyclic distance and the triangle inequality
put every far term beyond n/B from the selected bucket center. The inherited
stopband bound therefore yields the stated near mass times (1+rho), plus
far mass times rho. This is a valid conditional mass bound, not an assertion
that the near set is empty. At B=4 the chosen near set may cover all other
frequencies; then the far bound is vacuous but remains correct.

Two exact accepted-fixture controls demonstrate the limitations:

* At Q=56, H_0=16777217/16777216. For x_v=1 and requested index 0,
  F_0=1024 while the tested companion output is 16777217/16384.
  Its error is exactly 1/16384, well above its arithmetic certificate.
  There are no nonzero interfering Fourier coefficients in this control.
* For sigma=7,tau=19, coordinate 4 is unqueried. A unit impulse there
  gives F_0=1, output 0 and exact C_0=-16777217/16777216. Its recovery
  error is 1. More arithmetic precision cannot remove this obstruction.

An additional exact full-spectrum control has |C_i|^2>292436.47, certified
by a rational lower endpoint. It satisfies the retained recovery bound.
This prevents a test suite restricted to artificially tiny interference.

The conditional budget helper checks the supplied nonnegative inequality;
it does not acquire or authenticate those bounds. Equality and a strict
one-bit-below failure case were tested. A recovery target may only be reported
after the input noise and coefficient bounds have independent justification.

## Trust, range, preparation, resources and failures

The Qmin=56 correction and full guarded growing family are retained. The
Window type checks structural parameters and tap magnitude; it does not
establish HIKP response provenance. The fixed fixture loader binds only the
seven accepted files to pinned hashes. A caller-created self-hash, a direct
Window constructor or a reflectively changed object cannot authenticate a
response. An explicit zero-tap structural Window control returns zero while
the report still carries the formulaic positive H lower bound. This is an
out-of-contract control illustrating the documented trust boundary, not an
admitted counterexample. Consumers must preserve this boundary.

The estimator has no prepared-cache input and prepares the inherited bucket
roots on each nonempty call. The inherited optional cache remains restricted
to unchanged constructor-created in-process objects. Ignored redundant JSON
metadata stays ignored; no new full metadata authentication is claimed.
Source stability and a single fixed whole-signal vector are assumptions, not
properties inferable from one query to each accessed address.

The exact products satisfy the declared scratch widths, and the final
numerators satisfy the declared output widths with slack. Negative values,
zero, both component endpoints, arbitrarily small rationals and half ties
are admitted. Absolute-error certification makes no relative-at-zero claim.
Dynamic-range checks were exercised up to A=128 in the new end-to-end suite,
with additional exact budget checks through A=192 and k=200.

The new bit-cost bound is conservative but valid. It charges long supplied
integers, exact scaling of all B complex buckets, per-request modular work,
on-demand rational phase preparation, exact products and final quotient
roundings. Rational temporary lengths are polynomially bounded; the stated
O(T^10) classical-arithmetic allowance is sufficient. There is no online
length-n root, response or signal bank. The dense radical/ring oracles in
this review are offline verification work, not part of the estimator cost.

The packed memory statement includes scaled buckets, every returned estimate
and phase certificate, rational scratch and the retained inherited report.
Actual Python headers, serialized/decoded input and parser objects, source
storage and output serialization remain additional. Tap construction is paid
when not already prepared, and bucket root preparation is not free. A dense
sequential source may require Omega(n*ell) acquisition or indexing work.

Invalid representation, family, precision and denominators cause deterministic
rejection. Source errors propagate. A fresh test deliberately fails the
eleventh read and confirms no success report is returned; all preparation and
the already-consumed prefix work must still be charged. Empty requests perform
no source reads. Runtime memory, interpreter or hardware limits are not an
assigned probability of failure or a guarantee of execution for arbitrarily
large finite parameters. Only successful admitted executions have outputs;
the proved mathematical invariant checks themselves have no random abort.

O((B+J)polylog n) applies to the component under logarithmic numeric/index
widths and q=O(log n), with source acquisition separately charged. J itself
must be sublinear with the necessary polylog slack. In the stated S6 regime
B,J=O(n^(1/2+beta)polylog n), beta<1/2, the exponent is preserved. This
does not establish the full S6 runtime, output normalization or recovery.

## Evidence and review qualifications

Fresh checks passed:

* 35 end-to-end cases, 315 estimates, all seven accepted fixtures
* 168 certified phases, including m=127 and huge signed exponents
* 11,340 exact real-division cases, including 264 half ties
* 209,920 exhaustive route checks and 140 exact precision-budget cases
* Every one of the 257 closed-passband offsets in the Q=56 fixture
* A complete 1,969,152-term exact spectral identity with non-small interference
* Exact constant-bias and missing-impulse controls
* Ten malformed-input rejection classes, source-prefix failure and empty input

The author's wrong-sign/scale controls compare an upper distance bound with
a threshold. A large upper bound alone is not a proof of separation. This
review strengthens those controls using strictly positive lower distances
well above the certificate. This is a test-evidence improvement, not a change
to the accepted estimator or a numerical counterexample.

The remaining gate includes discovered locations, perturbed ranking and
candidate selection, certified independent unbiased randomness, recovery
events and all outer-loop failures, median/repetition composition, unitary
normalization and downstream S6 finite-word integration. Preserve the accepted
ideal-arithmetic theorem, weak-coordinate versus all-input relative-l2
distinction and unresolved novelty/priority status. No unconditional recovery guarantee, full-engine closure or historical-priority conclusion follows.
