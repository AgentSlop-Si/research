# Exact structured ALG-034 producer at theorem scale

17 October 2026. Fresh candidate. This proof concerns the new exact producer in
`structured_producer.py`; independent final review is a separate step.

## 1. Precisely what changes

The accepted serial implementation had N<=64; its adapter had N<=4096. The
accepted all-length mathematics is not invalidated by these deployment caps.
Increasing them and materializing every root, polynomial, source value and
large fixed-point numerator would not be a practical integration.

This packet instead supplies a NEW, restricted exact backend. It accepts an
unambiguously encoded family on which the target is computed exactly with
integer additions and fourth roots of unity. It does not claim to execute the
accepted serial recurrence, or to reproduce that recurrence's rounded output.
The output contract is the same ideal target, with the stronger error bound
zero. Backend identifiers explicitly distinguish the two implementations.

The supported family is:

* N=2^m, 2<=m<=64 and m even;
* B_A=N, hence all balanced longer-first blocks have length one;
* ordinary valid ALG-034 state: a is an odd residue, 0<a<N, and 0<=beta_A<N;
* a canonical exact complex dyadic vector with support in
  {0,N/4,N/2,3N/4};
* each Cartesian numerator has at most 1024 magnitude bits, metadata at most
  128 bits, and at most four explicitly listed nonzero coordinates.

An unsupported input receives an explicit rejection. This code is not a
general arbitrary-input deployment, a fast implementation of the full serial
algorithm, or full sparse recovery. The existing small general backend remains
a separate already-accepted option. This packet neither modifies it nor imports
or executes its historical Python.

The shared integration fixture is N=2^28=268435456 and x=delta_0. The adapter
worker's distinct constant-source BUCKETS backend uses beta_Q=5/56,
B_Q=131072, k=32, r=57 and P_Q=464. Its numerical/window proof, complete legal
guard verification and actual 131072-bin output belong to the companion
adapter packet. Nothing in this producer proof substitutes for that work.

## 2. Canonical input and original-context binding

The exact built-in input dictionary is

    {schema: ALG034_SPARSE_DYADIC_V1, N, F, entries}

and each entry is [j,u,v]. It denotes x_j=(u+i v)2^-F; unlisted coordinates
are exactly zero. Indices must be strictly increasing residues in the admitted
four-point support, and listed coordinates must be nonzero. For nonzero input,
at least one Cartesian numerator must be odd. Zero is represented by empty
entries and F=0. These conditions give a unique representation of each vector:
the support and coordinate ordering are fixed, and removing the greatest common
power of two from the integer components uniquely fixes F. Zero has its own
unique convention. No duplicate-entry summation or omitted-coordinate callback
is accepted. A separately supplied state has exactly N,B,a,beta fields.

Validation checks exact Python builtin types, rejecting bool as an integer,
floats, tuple-for-list coercions, duplicate or zero support, noncanonical common
powers of two, bad phase state and unsupported support/lengths. It copies the
input into immutable tuples before arithmetic. The trusted execution model is
correct Python/stdlib/integer arithmetic, unmodified source, no interpreter
tampering and no concurrent caller mutation during validation. This is not a
sandbox for hostile Python object reflection.

An ExactRun contains immutable tuples and bytes. Decoding its context or packet
creates independent mutable copies. A later caller mutation therefore does not
change the run. The raw hash labels the exact encoding; no proof relies on
collision resistance for semantic equality.

`verify(raw,state,t,q,packet,p)` takes independently retained original context,
validates bounded packet grammar and recomputes the entire exact producer. It
compares the full canonical packet, not merely a digest. Thus an accepted packet
equals a newly computed correct result for that supplied original context.
Recomputing every editable digest and policy for an alternative input still
fails against the original supplied raw input. It does not authenticate an
unknown outside source or attest that an earlier remote process ran.

## 3. The exact target computation

Every balanced block has length one because B_A=N. Its relative position is
t=0 and its embedding phase is one. The compression/expansion map therefore
satisfies P_(a,beta) x=x for every admitted a and beta; no block-length factor
is introduced.

Write c_l for the raw complex integer at index lN/4, with missing c_l=0. For
the negative-sign unitary DFT,

    (U_N P x)_j = 2^(-F-m/2) sum_(l=0)^3 c_l (-i)^(j l).

Since m is even, 1/sqrt(N)=2^(-m/2) is exactly dyadic. The four sums are Gaussian
integers and depend only on j modulo four. The code forms them by exact
Cartesian products with the four roots (1,0),(0,-1),(-1,0),(0,1), and exact
integer additions. Hence the returned four-row period and value_exponent
=-F-m/2 specify every one of the N exact target values. No transcendental
function, root approximation, hidden N-vector or tolerance test is used.

The four-point Fourier matrix is invertible. Therefore nonzero canonical input
cannot produce an all-zero period. The code also checks this invariant. Because
P is the identity on the entire supported family, the projected-zero case is
exactly the original-zero case: no distinct nonzero projected-zero input exists
here. The zero branch emits no normalized source and no declared precision.

If W is the largest raw Cartesian numerator bit length, a Cartesian component
of the period has magnitude less than 4*2^W, so its bit length is at most W+2.
All arithmetic is exact. The backend's target error is exactly zero, not an
empirical floating-point agreement or a serial-error certificate assumed from
a caller.

## 4. Exact specialization of the unchanged precision policy

The accepted all-length policy is retained as an additional mathematical grid
and error-budget specification. Its original source is the accepted report at

https://github.com/AgentSlop-Si/research/blob/acd8db5e6ad4660fb63ce1f2c63ee45577d454f0/math/finalized/2026-10-16-research-finalization-1458/all_length_policy/REPORT.md

with SHA-256
7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062.
The accepted bounded implementation and proof in the provided completion packet
were read as data, not run.

For dyadic N>=4, L=lcm(2N,4)=2N and Phi_(2N)(X)=X^N+1, so D=N. A singleton
block with integer value u+i v has polynomial u+v X^(N/2), already of degree
less than N and therefore already reduced. It is nonzero exactly when the
coordinate is nonzero. Its original aggregated mass is |u|+|v|, because the two
exponents are distinct. Unlisted blocks have zero polynomial. Thus finding the
minimum nonzero block mass A, breaking ties by original block index, requires
only the at most four entries, and is exactly the full policy's selection.

Let K=ceil(log2 A), computed as bit_length(A-1), and

    G=W+(N-1)K.

Since B_A=N,

    H=min(binomial(2N-1,N),2^(N-N))=1,
    C=64 H N 2^N N^2 = 2^(N+3m+6),
    c=ceil(log2 C)=N+3m+6.

It would be pointless to construct the enormous binomial or C to learn these
identities. The exact symbolic representation C_factor=(1,c) is part of the
declared schema and denotes precisely 1*2^c. It is not a floating estimate or
an arbitrary caller-supplied C.

For t>=0 and q>=m, the selected p is exactly

    max(W,c+t+1,c+q+G+2),

unless the caller supplies a larger valid p. Default q=16m+16. All expressions
are evaluated on exact bounded-width metadata integers. The formal output grid
has kappa=W-F-p and common_left_shift=p-W-m/2. The code checks that the latter
is nonnegative, so the exact formal grid numerator at frequency j is

    period[j mod 4] * 2^(p-W-m/2).

Multiplying by 2^kappa gives exactly period[j mod 4]*2^(-F-m/2), as required.
The data structure stores the common shift rather than that integer's expanded
binary digits. It is therefore an exact compressed p-grid representation;
it does not claim to be an allocated array of p-bit fixed-point cells.

Its maximum formal numerator bit length is at most p+2-m/2<=p+1, safely within
p+I for I=N+2m+10. The actual exact backend never performs the serial algorithm's
large intermediate products, so it does not claim those products were computed
or that their storage was paid. The original serial range theorem is not
needed for the direct zero-error proof. The displayed accepted-serial radius
C*2^kappa is an independently derived permissible bound; zero error satisfies
it and all weaker required producer error budgets automatically.

## 5. Concrete N=2^28 execution

For raw input F=0, entries=[[0,1,0]], and state
N=B_A=268435456,a=1,beta_A=0, t=16,q=464:

    W=A=G=H=1, K=0, D=268435456, L=536870912,
    c=268435546,
    p=p_min=268436013,
    I=268435522,
    kappa=-268436012,
    common_left_shift=268435998,
    maximum formal numerator bits=268435999.

The returned period is ((1,0),(1,0),(1,0),(1,0)) and value_exponent=-14. Thus
y_j=2^-14 exactly for every j. Its squared norm is N*2^-28=1. The formal radius
C*2^kappa is 2^-466, below the downstream rho=2^-464 even without using the
actual zero error. The second exact transform is U_N y=delta_0, equivalently
R P x with R[j]=(-j mod N), and alpha=1 on this fixture. The downstream input
is a genuine norm-one vector whose ideal Fourier target is one-sparse, hence
within k=32. The source is synthetic and explicitly constructed; it is not
misrepresented as the user's external data.

The receipt records only 155 metered integer operations and 30 bits for the
widest metered data integer. The enormous formal grid numerator is never
created. Its scale description is exact mathematics, not an uncharged
decompression step. Any future consumer insisting on expanded N rows or p-bit
integers must explicitly pay and resource-check that expansion. The companion
adapter instead consumes the constant family through a new proven interface.

## 6. Work, memory and failure contract

The production source imports only dataclasses, hashlib and json. It contains no
network, file reads, dynamic import, eval, exec, subprocess, floating arithmetic,
special-function call or historical dependency. It does not loop to N, B_A, p,
D or a support radius. The only arithmetic loops visit at most four entries and
four output residues. The only materialized power primitive has exponent <=64;
the production path never uses it to expand p or C. The fixture uses 1<<28 only
to construct its length metadata.

Input length metadata has at most 65 bits under m<=64; original F,t,q and caller
p have at most 128 bits; raw Cartesian numerators at most 1024 bits; period sums
at most 1026 bits. Selected p is itself rechecked at 128 bits. A large p denotes
a large number of formal fractional bits; it remains a small metadata integer.
The canonical serializer admits only the declared exact types, at most 512
tree visits and depth 16, lists<=128, dictionaries<=64, 4096-bit serialized
integers and a conservatively charged 65536-byte output bound. The producer's
own output is substantially smaller. All untrusted packet serialization checks
run before replay.

Each metered integer operation is charged

    128*(sum(operand and output magnitude widths)+8)^2

schoolbook bit-work units. This bounds integer addition, subtraction,
multiplication, division, shift, modulo and width extraction, including copying
the result. Each result's bits and explicitly allocated slots are counted.
The source contains a bounded number of unmetered sign, branch, comparison,
index and validation operations. Let E be metered operations + allocated slots
+ serialized bytes + 1024, and V be maximum metered width + bit_length(E)+32.
The receipt charges 4096 E V^2 additional control/serialization work and
4096 E V cumulative logical storage, on top of produced integer bits. This
conservative envelope covers exact metadata formulas, list/dict/string scans,
fixed-function SHA-256 work, decimal conversion, copies, and counters. The
reserved 16 KiB ledger serialization is charged before the ledger is formed.
Instrumented data width does not purport to measure interpreter objects or
SHA-256 machine registers.

The public packet() method is a separate export operation, bounded in work by
2^70 bit units and storage by 2^42 bits. These fixed oversized bounds dominate
the <=512-node, <=64 KiB, <=4096-bit serialization domain, and are explicitly
advertised in every receipt. They are NOT paid merely by calling execute.
Semantic verify pays its own full execute, both bounded serializations and
comparison, and one such packet export. If both an original execute and verify
are used, their receipts are added. Source-file load/pinning by a composition
wrapper, downstream validation and output construction, and future exports are
separate costs and must be added by that wrapper. Tests and their independent
oracle are not claimed as production runtime.

For the fixture, producer total_bit_work_upper=906559206400 and cumulative
storage_upper_bits=11622335881. These deliberately loose formal bounds are not
peak resident memory or a promise of this many bytes being necessary. The
measured fresh producer execution in the test process took about 0.004 seconds;
the entire test process, including 64 dense small-N oracles, used about 14 MiB
maximum RSS on this host. Measurements are observations, not machine-independent
guarantees. Full checked results carry the exact observed values.

Every resource, unsupported-structure, grammar, precision or invariant failure
raises an exception before a successful ExactRun is returned. MemoryError or
host interruption similarly produces no certificate. There is no catch that
converts failure to numerical success, no approximate-zero normalization, and
no policy retry. A rejection does not prove an input mathematically impossible;
it delineates this deliberately restricted implementation.

## 7. Fresh checks and what they establish

`checks.py` uses only this fresh module and the Python standard library. It runs:

* 64 deterministic four-axis complex-input cases at N=4,16,64,256, compared
  coordinate-by-coordinate with a separately written full-N direct Fourier
  sum using explicit quadrant cases;
* independent small-domain construction of the exact C expression and expanded
  p-grid numerators, checking grid alignment and formal stored range;
* the actual N=2^28 compact producer and paid semantic replay;
* an N=2^64 case with 1024-bit raw components, large negative F and p=2^120,
  confirming no precision-sized integer allocation;
* original-zero handling, canonical grammar, width/resource caps, support and
  phase restrictions, and too-small p/q failures;
* altered output period, scale and formal grid, fabricated attestation fields,
  oversized packet lists and input substitution;
* a wholly self-consistent alternative-input packet, with freshly recomputed
  policy and hash, rejected against the retained original context;
* immutable-run behavior under changes to caller inputs and decoded copies.

These controls supplement the algebraic proof; they are not the proof of a
general N transform or of downstream recovery. The separate adapter packet
must establish its own window enclosures, legal theorem guards, complete bucket
output, arithmetic receipt and source binding. No claim of finished arbitrary-
input deployment, full stream/recovery implementation, or novelty is made here.
