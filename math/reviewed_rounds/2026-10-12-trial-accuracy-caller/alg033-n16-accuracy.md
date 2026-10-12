Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical guarantees, source history, costs and remaining limitations are retained. Original source-report SHA-256: 7e290b020fda621bdd939da44690e0cbac441f9dae7ab62a59839a48791d337f.

Review date: 12 October 2026 UTC.

# ALG-033 N16 useful-accuracy certificate: independent bounded ACCEPT

12 October 2026 UTC. This review accepts the exact sealed candidate only within
the bounded mathematical and executable scope below. The broader all-length problem remains open.

## Verdict and exact target

Candidate: `ALG033_N16_Useful_Accuracy_CANDIDATE_2026-10-12.zip`, 40,404 bytes,
SHA-256 `77f991e48d2fcee1b36cae182d7e3e19330332542ab2a983e788a881b9ea57ec`.
Its implementation is SHA-256
`cbfbf7f78aed0b3ab0769ab40aecee5ef469ac2cab61117c7fdcc99faea39e57`.
All 14 archive members had safe unique relative paths and ordinary file types;
all 13 payload manifest entries verified. No candidate edits were made.

For each fixed admitted Gaussian-dyadic input x of length 16, the reviewed
executor, using 101 actual coordinate-median rows and 707 fresh independent fair
bits drawn after x and the plan are fixed, satisfies

Pr[max_k |z[k] - (U16 x)[k]| > (7/8) ||x||_2]
<= 83194032936167791955502442852803912051140656 /
   19088056323407827075424486287615602692670648963
= approximately 0.004358433961353432 < 1/200.

Here U16[k,j] = exp(-2*pi*i*k*j/16)/4. This is a simultaneous all-output,
additive input-energy-scaled bound. It is not absolute epsilon accuracy,
per-output relative error, relative-l2 recovery, or exact DFT computation.
The tolerance remains loose, and the implementation is a dense reference.
The improvement below deterministic bounds is genuine within that stated norm;
it is not a practical efficiency or novelty finding.

## Independent mathematical reconstruction

The review constructs each block projection directly from compression followed
by conjugate phase expansion, then applies the normalized negative-sign DFT.
The independent arithmetic is the integer cyclotomic quotient Z[z]/(z^8+1).
It does not import the candidate's author checker. Both real and imaginary
input bases are checked across all 128 legal states and 16 outputs: 65,536
exact output identities. Linearity then binds the executable coefficient map
for every admitted input, rather than extrapolating from a few test vectors.

For every output k, the reconstructed error covariance is exactly
Q_k = (I - (-1)^k S8)/16. All 4,096 Gram entries, 256 zero means, and 4,096
entries of Q_k^2 = Q_k/8 check exactly. Positive semidefiniteness follows
from the explicit Gram construction. The antipodal involution, a nonzero
1/8-eigenvector, and trace 1 confirm norm 1/8; each individual error row has
squared norm 1.

Root enclosure checking uses an independent quartic-isolation argument:
a=cos(pi/8) and b=sin(pi/8) are the unique roots of 8t^4-8t^2+1 in (3/4,1)
and (0,1/2), respectively. Exact endpoint signs and monotonicity isolate them.
c=1/sqrt(2) is isolated by squaring. All sign changes and exchanges for 16
roots are checked. The maximum midpoint squared radius is 5/2^66, below
2^-58. Two roots per coefficient and 16 coefficients give the certified
uniform executed-row error eta=2^-28 times ||x||_2.

The real median is 1-Lipschitz under coordinatewise sup-norm perturbations.
Applying this to real and imaginary parts gives complex median perturbation
at most sqrt(2)*eta*||x||_2, conservatively bounded by 2*eta*||x||_2.
For m=7/8-2*eta, m^2>=3/4 exactly. Markov gives bad-row probability at most
2*(1/8)/m^2 <= 1/3 for the disk radius m/sqrt(2). A strict majority of rows
inside that disk bounds both coordinate medians, hence their complex error
by m. Independent rows give the 101-trial majority tail; an exact rational
probability-generating-function convolution independently reproduces it.
Union over 16 outputs needs no independence between outputs. The sampler is
shared across outputs without invalidating this union argument.

## Sampler boundary and original-source provenance

All 128 seven-bit tapes map bijectively to the 8 odd units a and 16 shifts beta.
Disjoint fresh IID bit blocks therefore give independent uniform row states.
There are no rejection trials in this new sampler; its ideal-source abort
probability is exactly zero. Missing, malformed, or exhausted sources do not
return a certified vector, and there is no fallback.

The original v13 source archive was separately read as inert ZIP data:
SHA-256 `465d0cf5573539887fdb93376e7dc6fba740512a92ac8121952dafc3492b51fd`,
52,521 bytes. All 20 original manifest entries verified, and its
`composite_cycle_core.py` member exactly matches the candidate's inert source
copy, SHA-256 `226e18d6cbae68b5c064a5c4a0b4aa0e7762405ecbf7613c136240ae176e610e`.
No historical research program was executed.

The historical N16 `draw_state` sampler is a different implementation: it has
128 trials, rejection probability 7/15 per trial, and positive abort probability
(7/15)^128. Conditional on success it has the same uniform state law as the
new sampler. That legacy abort is not silently set to zero: zero belongs only
to the newly implemented fixed-seven-bit bijection. No legacy sampler,
optimized decoder, or historical v13 implementation is certified here.

## API, actual aggregation, and cost controls

The complete reconstructed plan validates exact canonical scalar and nested
tuple types before RNG access. The independent suite rejects 169 invalid
plans before the first bit call, including numeric-equal subclasses/floats,
missing fields, malformed rational shapes, oversized inputs, and changed
certificate values. Input snapshotting and ordinary frozen-object mutation
protection hold. Another legal stored input is a valid newly bound plan, since
the entire domain shares the same proof. This is not a hostile-runtime or
hostile-callback defense and does not certify changed implementation bytes.

Seventeen exhaustion positions, including the final partial row, and nine
malformed bit types refuse without a vector. Zero input consumes no bits.
Sixty-four scalar median/perturbation cases and 64 mixed-tape full-execution
coordinate checks match separate sorted-order statistics.

For the declared small integer adversarial input, the all-zero tape returns
z[0] = 1132859909840/68719476736, with exact target zero and ||x||_2^2=272.
Its squared error exceeds (49/64)*272 by
1171635762754255129193/18446744073709551616 > 0.
Thus a fixed or correlated tape cannot replace the fresh independence premise.

The displayed kernel arithmetic counts are correct: 25,856 complex
coefficient/input products, 103,424 integer multiplications, 155,136 integer
additions/subtractions, and 161,600 median comparisons. There are 1,616 stored
complex row outputs. Each planning/revalidation pass invokes five integer
square roots and 51 binomial coefficients; make_plan plus execute therefore
invokes ten and 102, verified by instrumenting those functions. Numerical
accumulators have absolute value <2^71, so a signed 72-bit container suffices
for that inner arithmetic; the output denominator is at most 2^52.

These are partial arithmetic counts, not complete Python instruction,
bit-operation, memory, wall-time, serialization, or production resource bounds.
General budget/refusal certification stays open. Roots and tail arithmetic are
recomputed cold rather than supplied as free warmed setup.

Ten targeted mutations were killed: wrong normalization, Fourier sign, phase
sign, median index, missing output union factor, wrong tail threshold, biased
unit sampler, undercharged bits, wrong variance, and weakened canonical type
checks. An initial reviewer-only mutation selector touched a docstring instead
of executable code; that selector was corrected to target the exact tuple
expression. Candidate code remained unchanged throughout.

## Historical acceptance and remaining scope

The original v13 remains REFUTED, v1 remains HOLD, and the accepted v2 bounded
reference retains its original scope. Generic/all-length and Bessel execution,
optimized decoder correctness, physical entropy, complete cold bit/RAM and
production cost contracts, and matched certified FFT comparison remain OPEN.
No historical-priority, attribution or practical-speedup conclusion follows.

## Replay

Run the candidate author checker inside its extracted directory and compare
with its archived RESULTS.json. Run the independent checker as:

python independent_review.py --candidate input/ALG033_N16_Useful_Accuracy_CANDIDATE --output INDEPENDENT_RESULTS.json

The reviewer package includes exact candidate/original archives,
provenance, both replay results, and fresh controls. A separate final cold seal
records safe relocated extraction and byte-identical reruns against the final
archive bytes; it does not alter or reseal the reviewed archive afterward.
