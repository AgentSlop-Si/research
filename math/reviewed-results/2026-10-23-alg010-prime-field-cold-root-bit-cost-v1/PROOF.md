# ALG-010: paid prime-field cold realization

23 October 2026 UTC. Candidate for independent review, not self-acceptance.

## Scoped outcome

The selected open root-acquisition/bit-cost child now has a complete concrete
interface, proof and fresh implementation for prime fields. This is a standard
finite-field realization of the accepted first-order algorithm, **not a new
Fourier mechanism or asymptotic discovery**. The original exact relation family,
finite boundary, all-coordinate verification and singular recovery are retained.
The accepted cyclic-hypergeometric comparison is neither reopened nor repeated.
ALG-010 remains open at priority 42 for its broader fields, prescribed-root
acquisition when not supplied, numerical stability, complete-interface priority,
and unrelated acceleration/integration obligations.

The deterministic supplied-root bound is

    T_prime(p) + O(N b^2 + b^3) bit operations,

where b is the bit length of the supplied prime p. It includes full input
validation, root validation, parameter discovery, accepted or rejected input,
all singular work and complete output encoding. O(N) modular work plus at most
six inversions, each by Fermat powering, gives this bound. No field-operation
count is renamed bit time.

If the caller explicitly permits any primitive Nth root and requires that root
be returned, elementary Las Vegas acquisition adds expected O(b^3) bit work and
at most 4b expected independent unbiased random bits. It has **no finite
deterministic worst-case runtime**. Every failed candidate is charged. Capped
search returns ROOT_LIMIT, never mathematical infeasibility or family DECLINE.
A preassigned root is never silently replaced by a random root.

The reference actually validates primality by exact trial division; its
T_prime(p)=O((1+sqrt(p)) b^2) cost can dominate and is exponential in b. There is
no practical-speed claim. A caller-supplied certified-prime context may replace
that stage only with its own paid construction, validation and provenance;
this implementation does not claim to construct or verify a faster certificate.

## 1. Exact live scope and sources

The native Research overview row 53 was read in full on 23 October 2026. It
says the named cyclic-hypergeometric comparison is complete, retains ALG-010 as
TO RESEARCH at 42, and explicitly leaves root acquisition and bit complexity
open. `sources/LIVE_ROW.json` records that read. The repository main was freshly
compared with 019b4052fdb5e0753ed248683a2c09a80590f3d3 and was identical.

Original accepted algorithm:
https://github.com/AgentSlop-Si/research/blob/019b4052fdb5e0753ed248683a2c09a80590f3d3/math/archive/objects/95/952f1d290c9b71058687de0c663a58ec7883b0465edf12cf72496e1fcce7b2d6__952f1d290c9b7105__README.md

Its recovered bytes have SHA-256
952f1d290c9b71058687de0c663a58ec7883b0465edf12cf72496e1fcce7b2d6.
The exact completed comparison and independent review are retained as inert
text in `sources/COMPARISON.md` and `sources/INDEPENDENT_COMPARISON.md`, with
SHA-256 c3d56d36ea643d193f5c533ca52e371056ee86e61a8feeb3355fc06c6b39a231 and
a86f115b66978f190f0dfd631f0f91355b4099a598a831b65b07f14bf77befe5.
Their immutable locations and all source metadata are in SOURCE_BINDINGS.json.
No historical scientific program was executed or imported.

## 2. Input, field, root and output contracts

Input consists of N=2^n>=4, an integer p, and all N canonical residues
x_i in {0,...,p-1}. We require p prime and N | p-1. This is an explicit
specialization of the original supplied exact field, not a result for arbitrary
fields or characteristic-zero bit representations. Primality is actually
checked before field inversion in the reference. Noncanonical residues,
floats, booleans, bad shape, incompatible p and invalid roots are malformed
input, not a negative mathematical completion certificate.

One of two explicitly different root interfaces is selected:

1. **Prescribed/supplied q.** Read the canonical residue q, build Q_i=q^i for
   0<=i<=N, and require Q_N=1 and Q_(N/2)!=1. These conditions are equivalent
   to exact order N because N is a power of two. The exact supplied q is used.
2. **Any primitive root permitted.** Supply independent unbiased random bits;
   acquire and return an exact root q by Section 3. The family tested and the
   output transform are defined by this returned q. This interface does not
   recover an independently prescribed unavailable root, compute a discrete
   logarithm, or silently permute a canonical Fourier output.

On ACCEPT, output all N canonical values

    y_k = sum_(i=0)^(N-1) q^(ki) x_i in F_p,

and the exact q. ACCEPT occurs exactly when a nonzero quadruple
(p0,p1,r0,r1) in F_p^4 satisfies

    (p0+p1 q^i)x_i + (r0+r1 q^i)x_(i+1) = 0,  0<=i<N-1.

The parameters are discovered, not supplied. Exact zero coordinates, vanishing
bands, finite nonperiodic boundaries and singular transformed systems remain
included. No regular-ratio promise or periodic closure is substituted.
On DECLINE, the relation system has rank four; no transform is returned.
There is no general-FFT fallback in this implementation. A whole-input
always-output application must add its separate full fallback cost.

`encode_result` implements a concrete caller-known-p,N wire format. R is one
byte for ROOT_LIMIT; D followed by q denotes DECLINE; A followed by q and every
y_k denotes ACCEPT. Each residue occupies ceil(b/8) big-endian bytes. Thus an
accepted encoded result has exactly 1+(N+1)ceil(b/8) bytes. Diagnostic operation
counters are separate from the mathematical output and can be disabled; they
are not output-sized cached transforms.

## 3. Root acquisition, entropy and failures

Write m=(p-1)/N. Obtain a uniform nonzero residue a by drawing b independent
bits and rejecting values outside 1,...,p-1. Compute q=a^m. Then q^N=1.
Accept if q^(N/2)!=1. Because F_p^* is cyclic, a->a^m is a surjection onto the
N-element root subgroup with equal-size fibers. Exactly N/2 of those roots
have order N. Hence exactly half of the nonzero candidates succeed, regardless
of the odd part or 2-adic valuation of p-1. Factoring p-1 or finding a generator
of all F_p^* is unnecessary.

A candidate's two powers use O(b) modular multiplications in total; allowing
O(b^3) bits per candidate is conservative. All failures do the same paid work.
There are exactly two expected nonzero candidates. A raw b-bit draw succeeds
with probability (p-1)/2^(b+1)>=1/4, so the expected number of raw draws is at
most four and the expected bit consumption is at most 4b. Each rejected raw
draw incurs its comparison and generation cost. The random-bit supplier's
actual cost is additionally charged, not assumed to be a physical entropy
oracle with zero setup cost. The stated bound models one bit operation per
supplied unbiased bit; a different provider adds its full tariff.

Unbounded acquisition is Las Vegas: zero error and almost-sure termination,
with geometric tails, not a deterministic bound. With only a T-candidate cap,
T>=1, failure probability is exactly 2^(-T); the number of raw rejection draws
is still unbounded. With only a D-raw-draw cap, failure probability is
(1-(p-1)/2^(b+1))^D <= (3/4)^D; deterministic work is O(D b^3), entropy is at
most Db, and the status may be ROOT_LIMIT. If both caps are supplied, these
separate exact tail equalities no longer describe the combined stop; the union
bound 2^(-T)+(3/4)^D is valid. Caps are never treated as evidence that no root
exists or that x is outside the relation family. The controls use deterministic
scripted/pseudorandom draws to test branches; they do not establish physical
entropy quality.

An alternative deterministic enumeration of nonzero a would terminate because
half the candidates succeed, but it has O(p b^3) worst-case cost and is not the
reference's chosen acquisition policy. No deterministic polynomial-time
primitive-root discovery theorem is claimed here.

## 4. Preserved algebra and complete recognition

For each source index 0<=i<N-1 form

    [x_i, q^i x_i, x_(i+1), q^i x_(i+1)].

Streaming exact elimination keeps at most three normalized pivot rows. A
fourth independent row proves rank four and DECLINE without normalizing that
fourth row. Otherwise back substitution gives a nonzero kernel quadruple.
Every source equation is rechecked during a full residual pass. Thus all
finite-boundary inputs are accepted exactly, including rank below three.
Elimination is adaptive rational arithmetic, not a fixed linear circuit.

Let D=diag(q^i) and (Sx)_i=x_(i+1 mod N). With the original positive-sign F,

    L=p0 I+p1 D+r0 S+r1 DS,
    F L=J F,
    (Jy)_k=(p0+r0 q^(-k))y_k+(p1+r1 q^(-k-1))y_(k+1).

The full cyclic residual u=Lx vanishes at indices 0,...,N-2. Its actual last
entry is retained, and (Fu)_k=u_(N-1)q^(-k) is constructed and charged. The
nonsingular solve of Jy=Fu determines the desired transform. A homogeneous
periodic formula would be wrong when the last residual is nonzero.

Both source and target operators have nullity at most one. If a cyclic upper
band is nonzero as a polynomial, it has at most one zero among the N distinct
root powers. Starting just after that zero, if present, leaves N-1 nonzero
path edges. Otherwise any start works. Express each coordinate as

    z_i=alpha_i t+beta_i

by those path equations and impose the final cyclic equation. A nonzero final
coefficient determines t. A zero coefficient with zero forcing leaves the
nonzero kernel alpha (its starting coordinate is one); inconsistent forcing
is excluded for the actual transformed source by similarity. If the upper band
is identically zero, the nonzero diagonal polynomial has at most one zero,
and the diagonal solve has at most one free coordinate. No edge that may be
zero is ever inverted.

If J is singular, obtain its particular solution y0 and nonzero kernel h, and
obtain a nonzero source kernel v by the same linear solve for L. Choose j with
v_j!=0. Since F is invertible, Fv=c h for c!=0. Fourier orthogonality gives

    sum_k q^(-kj)h_k = N v_j/c !=0.

The equality sum_k q^(-kj)y_k=N x_j therefore determines the unique missing
scalar. Both kernel solves, weighted sums, scalar inversion and the complete
final correction/output pass are paid. This is source-input side information,
not reconstruction from a smaller measurement set. All formulas remain exact
in F_p because N divides p-1 and is invertible modulo p.

## 5. Constant inversion count and full bit ledger

For nonzero d_1,...,d_s, form prefix products P_0=1,
P_i=P_(i-1)d_i. Invert P_s once, then walk backward. If z=P_i^(-1), emit
z P_(i-1)=d_i^(-1) and replace z by z d_i=P_(i-1)^(-1).
This gives every inverse with one inversion and 3s modular multiplications in
the simple reference. This is classical simultaneous inversion (Montgomery's
trick); no novel inversion mechanism is claimed.

All cyclic path denominators are known before traversal, so this operation
can be used legally without altering the source family or its costs:

- Discovery uses at most three pivot inversions, including rejected inputs.
- A nonsingular target cycle uses one batched path inversion and at most one
  closing-scalar inversion. A diagonal target needs at most one batch.
- A singular target uses one batch and no closing-scalar inversion.
- Its singular source-kernel solve uses one further batch, never a nonsingular
  closing inversion.
- The final source anchor uses one inversion.

Thus the complete evaluator uses at most six inversions. Empty batches cost
zero and do not invert one gratuitously. Each inversion uses repeated-squaring
power a^(p-2), requiring fewer than 2b modular multiplications. All other
post-root field work, equality tests, storage accesses and full output writes
are O(N). The generous implementation audit bound add+mul<=200N+20b includes
its Fermat powers and all supplied-root evaluator arithmetic; it excludes
primality and optional acquisition, which have their own explicit tariffs.
For an explicit loose derivation: discovery has at most 26(N-1)+24
non-inversion additions/products; the root table and four operator/residual/
forcing preparations add 13N. A nonsingular cycle needs at most 10N+4
non-inversion operations, while a singular cycle or source-kernel pass needs
at most 8N+4. The singular anchor and complete correction use at most 7N+2.
The six inversions add fewer than 12b products. Diagonal branches cost less.
Thus the displayed 200N+20b envelope dominates every branch for N>=4,b>=3.
These bounds follow from the loops, not from the finite tests.

Use schoolbook b-bit addition/comparison O(b), and multiplication followed by
exact remainder O(b^2). All stored field values have at most b bits; raw products
have at most 2b bits, so coefficient growth is controlled rather than assumed.
The fixed number of Fermat inversions costs O(b^3). N<=p-1 implies log N<=b;
O(log N)-bit indexing and each represented-word read/write are charged,
not treated as free. We use the inherited random-access index model with
bit-length charges for these operations, not a claim about an arbitrary
sequential-tape simulation. All loop addresses have O(log N) bits; the anchor
weights are generated successively by w<-w q^(-j), not by a free vector oracle.
These index/data-movement costs are subsumed by O(Nb^2). The O(N) live field arrays and bounded-index
arrays require O(Nb) bits. Binary input/output encoding costs O(Nb); all N
inputs are validated even if discovery later declines. No dense matrix or
lookup table of possible input transforms is prepared.

Consequently the deterministic supplied-root total is

    T_input_decode + T_prime(p) + T_setup + O(Nb^2+b^3),

where canonical fixed-width input decoding and ordinary array setup are
O(Nb), and output encoding is already included. If the caller starts with
unbounded integers, rationals, an extension-field encoding or a different
oracle, its conversion costs are extra and this canonical input bound does
not apply silently. This implementation rejects rather than truncates them.
Root validation costs N modular products in the actually used power table;
root construction is not hidden in that validation.

The reference's deterministic primality check divides by every odd integer
through floor(sqrt(p)), with the even case separate. Its worst-case
O((1+sqrt(p))b^2) bit charge is stated, including successful prime inputs and
composite rejection. Repeating the evaluator repeats this validation; no
amortized prime cache is assumed. A changed validated-context API could reuse
it only with the initial cost explicitly assigned to its lifecycle.

For t nonzero root candidates and d raw draws, the mathematical acquisition
without diagnostic counters adds O(t b^3+d b) bit operations
under the ideal supplied-bit tariff, plus provider setup/tariff. This per-run
bound accounts for every failure, including a limited search. Expected
acquisition restores T_prime(p)+O(Nb^2+b^3); it does not give a worst-case claim.
The implementation's diagnostic counters consume logarithmic additional bits
in t,d if retained, and increment/serialization work must be charged for very
long runs. For the actual uncapped diagnostic reference, conservatively add
O((t b+d) log(t b+d+2)) counter-increment work and O(log(t b+d+2))
counter storage bits. This is not omitted from a per-run worst-case bound.
These diagnostics are not required by the mathematical algorithm. The capped
variant fixes their widths from its cap. This distinction does not affect the
expected bound because geometric tails have finite logarithmic moments.

An always-output fallback is deliberately absent. Adding a generic direct
DFT costs O(N^2 b^2) bits in addition to all failed fast-path work; a separate
radix-2 finite-field implementation can instead be charged at its full
O(N log N b^2) modular/encoding work, with its own source and implementation
verification. Neither fallback is executed or certified here. No improvement
for arbitrary fresh inputs follows.

## 6. Attribution and what remains open

The inherited comparison attributes regular periodic q-ratio Fourier formulas
to Au-Yang and Perk; the present work does not repeat that comparison. Streaming
fixed-width elimination, square-and-multiply powering, finite-field cyclicity,
rejection sampling and simultaneous inversion are standard. This packet's
contribution is a complete bounded engineering/bit-cost realization of the
already accepted raw-input theorem, with the missing acquisition/failure and
encoding distinctions made explicit. It carries no new historical-priority,
algorithmic-novelty or practical-speed claim.

For standard arithmetic attribution, Victor Shoup's *A Computational
Introduction to Number Theory and Algebra*, version 2.5, Section 3.4
(printed pages 65-67) explicitly gives repeated-squaring inversion in cubic
bit time; its cyclic-group results provide the elementary group background.
https://www.shoup.net/ntb/ntb-v2_5.pdf

Classical simultaneous inversion is expressly reviewed as Montgomery's trick
in Section 2.1 of *Efficient Methods for Simultaneous Homomorphic Inversion*.
https://cic.iacr.org/p/2/1/36/pdf
The algebra above independently proves exactly the version used here; this
citation is attribution, not reliance on a homomorphic arithmetic model.

Remaining ALG-010 duties include characteristic-zero/extension-field
representations, fixed unavailable-root acquisition beyond the explicit
any-root contract, floating-point recognition and stability, complete-interface
historical priority, caller/fallback integration and broader acceleration.
No whole-owner closure, general numerical theorem or unrestricted FFT result
is proposed. The selected prime-field child should not be assigned again
without a changed contract or demonstrated defect after independent acceptance.

## 7. Fresh controls and review boundary

`python -B fresh_controls.py` uses only the new executor and new dense/rank
oracles. It does not import or execute historical scientific code. The fresh
checks pass 1,577 raw inputs: 1,257 exact full outputs, 320 rank-four declines,
811 singular recoveries, 876 nonzero finite-boundary cases, and 46,068 output
coordinates. They include all 625 vectors in F_5^4, zero/basis/mode vectors,
generated degree-one recurrences and random rejections through N=256.

Further checks cover all 624 nonzero coefficient quadruples in F_5^4 as cyclic
systems, full primitive-root candidate populations at six (p,N) pairs, exact
scripted rejection-draw/candidate-limit behavior, nine malformed inputs, and
round-trip fixed-width output encoding for every accepted vector. The maximum
observed inversion count is six, matching the proved bound. These controls
corroborate the all-size algebra; they are not a theorem by finite census,
a physical-entropy certification, a performance benchmark or independent
scientific acceptance. The final accepted-ready stopping condition is this
paid represented-field interface and its proof, not ALG-010 parent closure.
