# Independent Q16 admitted-instance backend review

## Verdict and exact boundary

ACCEPT, BOUNDED: a freshly authored semantic refinement of the accepted HIKP
numerical interfaces has now executed the two-stage whole-output loop on two
complete, genuinely admitted multisparse inputs, with independent arithmetic,
full-output, provenance, cost and isolated cold-replay checks. The immutable
candidate identity is recorded separately in REVIEW_VERDICT.json.

This is not execution of unchanged historical binaries, a uniformly total new
constructor, a general replacement source API, an empirical random-success
estimate, or closure of Q16. No historical executable was imported or run by
this review. No external publication, provider certification, performance or
novelty upgrade is included.

The accepted predecessor archive is pinned at SHA-256
7ec5198033740119f648ae48990184baa7cfd5068ede682e7016e8345748043b.
It explicitly accepted callback orchestration while excluding executed backend
integration. This review addresses that missing execution evidence within the
finite scope below, rather than silently treating the old wrapper as a backend.

## Genuine admitted scope

Both full vectors have n=32768, B=128, q=10, w=20481, p=31 and Q=66.
Their heavy count is s=2, a=D=1, k=1; source bounds are A=0, ell=21.
All whole-output numerical and spectral hypotheses hold. The initial source is
`x_v=1/(16n)+[v even](2/n)i^(v/2)`, with heavy spectrum {n/8,5n/8}; multiplying
by i^v gives the second source with heavy spectrum {3n/8,7n/8}. The respective
1/16 tails are at zero and n/4, so squared tail energy is 1/256.
Neither heavy pair is cardinal. The backend is given only the complete fixed
source provider, taps, plan and bit provider; it is not given the known support
or an expected-output callback.

The small historical B=4 fixture is used only as inert fidelity context. It is
not substituted for the admitted B=128 execution. The exact small-dimensional
algebraic examples in the predecessor are likewise not used to establish this
execution claim.

## Numerical refinement audit

The new constructor preserves the accepted Gaussian-sinc formula, outward
interval enclosures, signed nearest-even grid p, exact reflection and distinct
support. Every one of its 10241 stored taps equals a separately derived unique
exact nearest-even value. The independent construction uses 256-bit intervals,
different Taylor lengths/range reduction, and its own Machin enclosure. Its
compact tap-array hash is
aefba98442ddc5e3fea4c2416039a2c75a7e652131aa4c3dda818a8e1392cd5b.
This establishes actual tap fidelity, not merely structural acceptance or a
caller-generated self-hash.

Fresh interval roots differ algorithmically from historical exact-rational
Taylor roots. The accepted numerical proofs require their requested dyadic
grid and per-coordinate error at most one grid unit; they do not require the
same rounded numerator. Inspection verifies those enclosing certificates,
negative signs and exact cardinal branches. The accepted input conversion,
folding, product rounding, bucket output grid, exact n scaling, nearest-cell
ties, phase correction, final output grid and companion denominator are preserved.
The true-response bias remains explicit; the exact response is never asserted
to be identically one.

The new cold constructor tries W=16Q once. Successful certified finite cases are
accepted; the inherited refine-to-Wmax totality theorem is not attributed to this
new executable. The A=0,ell=21 source limitation is also explicit. These are
material boundaries, not merely implementation details.

Independent arithmetic controls passed against the frozen backend hash:
- 38464 signed nearest-even cases.
- 91 separately enclosed bucket/phase root cases.
- 512 actual bucket coordinates across four seeds and both source forms,
  checked by separate exact rational folding and all 128 direct DFT sums.
- 30 supplied-index estimates, including noncardinal phases and route boundaries,
  checked against independently enclosed actual-filter, inverse-phase targets.
- 31 independent malformed-plan, cap, bit/source prefix, exception-identity and
  rank/fiber controls. The four rank/fiber controls additionally inspect every
  one of the 32768 possible indices; their synthetic bucket input is only a unit
  control, never offered as full-backend evidence.

The numerical reference comparisons are against the actual filter expression,
not against an expected support oracle. All separate arithmetic controls and
full execution evidence are bound to the frozen new source bytes.

## Complete outputs, dense comparator and negative cases

The author and reviewer cold processes both return precisely
(4096,1,0),(20480,1,0) on the first input and
(12288,1,0),(28672,1,0) on the shifted input. Returned support is checked as an
ordered unique list, not merely converted to a dictionary that could hide
duplicates. Every amplitude is exact for these instances; complete squared
vector error is 1/256 because the tail is omitted.

The reference comparator is an actual full length-n radix-two DFT over
Q[z]/(z^(n/2)+1), z=exp(-2pi i/n). The sign embedding i=-z^(n/4), exact
monomial rotations and reductions, rational additions and complete butterfly
traversal were checked. It reads every source coordinate and has no expected
spectrum input. Only after this full transform does the driver compare all
32768 coefficients with the independently derived complete spectrum. The
reviewer separately reconstructed every expected coefficient and checked the
complete dense-output hash, all source bytes and all source-address traces.
This is an exact algebraic comparator with paid term/bit representation costs;
it is not a production FFT benchmark or a generic complexity improvement.

The initial t=2,u=3 tape of small affine multipliers fails: it returns 42
records, including 40 false positives. The full output and work counters are
retained, and the complete-output oracle rejects it. The later positive study
uses t=2,u=19 and a disclosed deterministic SHAKE256 label chosen after that
pilot failure. This sequence is openly documented, not presented as an unbiased
sample of successful randomness.

Full-output controls also reject dropping a heavy, adding a false positive,
corrupting an amplitude, and duplicating returned records. Actual changed-source
replay fails after both discovery passes and all 2048 phase records; the source
exception preserves its original identity and spent prefix. A bad bit fails on
the eighth attempt. Undersized caps fail before any bit/source call.

## Actual work and independent accounting

For each positive run, actual counts are 609 bit attempts, 471063 source calls,
23 bucket passes and root preparations, 1472 prepared bucket roots, 10304 bucket
FFT butterflies and 4096 discarded discovery amplitudes. Candidate union sizes
are 3965 and 3968. Hence actual phase records are respectively 79431 and 79488,
with 150670 and 150784 real median-coordinate records stored. All candidate
fibers, union sorts/visits and threshold checks are paid, including false candidates.
These executed parameters require 471063>32768 source calls per recovery;
no sublinear read count or speed advantage is demonstrated. There are 80813
and 80849 noncardinal root calls, so execution is not confined
to cardinal fast paths.

Each positive dense comparator reads 32768 coordinates and evaluates 245760
butterflies/root-monomial products, 40959 actual monomial terms and 81918 rational
coefficient additions. Actual maximum polynomial support is two and scalar
width is 19 bits for these structured witnesses; these are observations, not
uniform all-input bounds. The full integration driver invokes the dense
comparator six times, including three output mutations and the failed-tape test,
so verification also pays 196608 dense input reads and 1474560 butterflies.

The main process meter excludes separately metered negative controls; it is
not mislabeled as all attempted work. Across both positive runs and its retained
negative executions, the driver pays 1126484 backend source attempts, 56 bucket
root preparations, 175971 phase records and 1429 bit attempts. Other independent
review tests incur additional verification work. Cold construction separately
pays all 10241 taps, all contexts/series/squarings/factorial checks, storage,
source generation, hashing, parsing and serialization. The selected interval
quadratic tally is only partial accounting, not a complete bit-instruction count.

## Provenance and cold replay

Read-only provenance checks passed all six accepted top-archive hashes and 106
nested archive/member paths. Historical source copies were verified as inert
bytes. The new backend SHA is
8cd506f31a6bbfb0007b319d89b449d5f3949ee4c79ce6231949adc9c331af09;
the full integration driver SHA is
74425a9d05509bb54ede38057c81c02aa7377b7a1a347661d3dd69913d319cf3.

The reviewer copied only these new executables into a separate empty runtime
directory, started a fresh process, regenerated all cold taps without a fixture,
and completed both full runs and all included negative controls with exit code
zero. Every deterministic result equals the author result after removing only
labels, timings and process-RSS observations. The independent cold run took
261.72 seconds with observed peak RSS 50220 KiB; those observations do not
establish production performance. The successful cold result SHA is
fcd40f84a3fa0450977e4286d8ce0ef9c02694e4995c3c29add9c29ab8cecccc.

## Probability and remaining obligations

The inherited ideal-bit theorem separately gives the exact formal bound
3034359625537178072416013899/5359984957120804898281095168, about 0.5661134592,
when beta is formally set to zero. This number is not the success probability
of the fixed tape, not an empirical estimate, and not a justified real abort
bound. Freshly consumed blocks of a fixed deterministic tape do not certify IID
entropy. The failed tape concretely demonstrates that distinction.

Q16 remains progressed/open. General stable-source adapters and physical entropy,
a justified operational abort model, uniform executable refinement/totality,
broader tails/noise and all-input relative recovery, unitary/downstream S6
integration, priority and practical performance are outside this acceptance.

Derivative note: the source-vector formula is marked as literal mathematical text to prevent its indicator from rendering as a link. Complete bounded execution scope, failed tape, accounting and remaining obligations are preserved. Original report SHA-256: `a27e9f6c1220eb7b8d82cbf3d92076bf19b10ade7136e73f98de2b1eb7d76afd`.
