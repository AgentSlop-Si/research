# Q13 / STR-Q2: bounded rank-two structural execution gate

Date: 12 October 2026. Status: **contract and mathematical design, with fresh finite controls; not an accepted metered executor.**

## Result and scope correction

The next useful task is an independently audited **bounded structural rank-at-most-two executor** that discovers an unknown common phase, returns a fully checked witness, and computes every Fourier output with paid preparation, rejection and interruption behavior. It is not another existence proof of rank-two recognition.

The current Q13 and STR-Q2 records already accept the general-rank exact membership theorem, its cyclic-window extension, a bounded general-rank dense reference, and the later bounded unknown-phase rank-at-most-one structural executor. The rank-two theorem is therefore already covered. What remains useful is to realize the fixed-rank linear-work route in an exact bounded program with the complete accounting and all-phase output contract. This is implementation/accounting progress built from established results, not a new Prony theorem or a historical-priority claim.

A concrete audit control also rules out an incorrect simplification: a genuine rank-two signal can have **four distinct canonical common phases**, with all four roots of the degree-four phase filter valid. Acquisition must return any verified witness; it must not promise an identifiable original phase or assume at most two candidates.

## 1. Exact bounded interface

Proposed standalone target:

- Resident, unmutated, exact built-in record with keys `N`, `p`, `omega`, `x`; integer headers and coordinates exclude booleans and subclasses.
- `3 <= N <= 512`; supplied prime `5 <= p <= 65537`; `N` divides `p-1`; `x` is a length-`N` list of canonical residues modulo `p`.
- `omega` is a supplied canonical residue checked to have exact order `N`. If `omega=None` is supported, it means an explicit request for the already established deterministic, fully charged root-search preparation. It must never silently trigger an uncharged search. A supplied-root-only first implementation is acceptable if that restriction is explicit and the optional-search gate remains open.
- Budget is an exact integer, with a documented finite maximum such as the rank-one executor's 20,000,000 named-event cap. Neither the domain rectangle nor a default cap promises completion.
- The target family is

  `x[j] = omega^(a*j*j) * sum(c[l] * omega^(b[l]*j), l=1..s)`,

  with `0 <= s <= 2`, distinct `b[l]` modulo `N`, and nonzero coefficients. The empty representation is zero.
- Canonical phase range is `0 <= a < L`, `L=N/gcd(2,N)`. The even half-shift changes both phase and all frequencies, as in the accepted source. Canonical range removes a universal alias, not every signal-dependent ambiguity.
- `N=2` is deliberately outside this new rank-two gate: rank two is then the trivial full-rank family. Existing rank-one acceptance for `N=2` remains unchanged.

Completed `MEMBER` returns a checked root, one canonical witness with sorted distinct frequencies and all `N` positive-sign unnormalized values

`X[k] = sum(x[j] * omega^(k*j), j=0..N-1)`.

`NONMEMBER` means rejection of the complete rank-at-most-two baseline family, not failure of one phase or one recovery attempt, and returns no transform. `INVALID` is detected malformed/out-of-domain input. `LIMIT` is indeterminate and may precede detection of invalidity. No partial root, representation or transform is published on `LIMIT`; output publication is a paid terminal event. Zero is accepted only after complete parameter and raw-input validation. There is no dense DFT fallback hidden inside acceptance.

This interface is not automatically a drop-in replacement for the legacy general-rank API. Changes to that API, dispatcher or accepted rank-one entry point are separate integration work.

## 2. Explicit quartic acquisition filter

Read all raw entries. For nonzero input choose a deterministic nonzero center `c`, for example the first. All subscripts below are modulo `N`. Put `z=x[c]`, `u=x[c-1]`, `v=x[c+1]`, `U=x[c-2]`, `V=x[c+2]`.

The accepted cyclic determinant at rank two expands to

`E(t) = z^3 - 2*z*u*v*t + (u^2*V + U*v^2)*t^3 - z*U*V*t^4`.

There is no quadratic term. This is the direct determinant of the three-by-three matrix with entries `x[c+i-j]*t^((i-j)*(i-j-1)/2)`. Its constant coefficient `z^3` is nonzero. Consequently its degree is at most four even with wrapped/repeated coordinates, and every true common phase satisfies `E(omega^(-2*a))=0`.

Scan **every** one of the `L` canonical phase points, in increasing phase order, charging all evaluations. Since those points are distinct and `E` is nonzero, at most `min(4,L)` phases survive. Do not infer membership from vanishing, and do not discard this original nonzero polynomial if its reduction modulo `t^L-1` happens to vanish.

This is only the `r=2` specialization of the already accepted cyclic eliminant, not a new general phase-elimination theorem. For a fixed rank, a direct complete grid scan is already linear in `N`; there is no discrete-log oracle or generic polynomial-root oracle in this design.

## 3. Fixed-size recovery, including cancellation and small lengths

For each surviving phase `a`, obtain the first four periodic dechirped moments

`y[j] = x[j mod N] * omega^(-a*j*j)`, for `j=0,1,2,3`.

For `N=3`, the fourth moment is a valid periodic reuse, not an extra observation. Let

`Delta = y[0]*y[2] - y[1]^2`.

If `Delta=0`, a genuine nonzero rank-at-most-two sequence at this phase must actually have one mode. Require `y[0] != 0`, scan the whole supplied root grid for `lambda=y[1]/y[0]`, and require a matching node. Take its amplitude to be `y[0]` and verify every original coordinate. If `y[0]=0`, reject this phase. A zero recovery prefix never licenses zero acceptance for nonzero raw input.

If `Delta != 0`, compute the inverse of `Delta` once and reuse it to recover

`S = (y[0]*y[3] - y[1]*y[2]) / Delta`,

`P = (y[1]*y[3] - y[2]^2) / Delta`.

Scan all `N` grid nodes for roots of `q(Z)=Z^2-S*Z+P`. Require two distinct roots `lambda1,lambda2`, with canonical frequencies `b1,b2`. Recover

`c1 = (y[1]-y[0]*lambda2)/(lambda1-lambda2)`,

`c2 = y[0]-c1`.

Require nonzero coefficients, then reconstruct and compare **all `N` original coordinates**, accumulating a mismatch flag rather than treating a matching prefix as evidence of membership. Continue to the next filtered phase after any failure. Only exhausting all filtered phases proves `NONMEMBER`.

Why this is complete: for a genuine two-mode sequence,

`Delta = c1*c2*(lambda1-lambda2)^2 != 0`.

The recovered `S,P` are the node sum and product. This argument allows `y[0]=0`, singular one-by-one prefixes and cancellation; it does not assume every raw sample is nonzero. A genuine nonzero one-mode sequence has nonzero `y[0]`, zero `Delta`, and its unique node belongs to the supplied grid. Final raw reconstruction is sound for arbitrary input, including false eliminant roots. These are classical two-node Prony/Vandermonde identities.

One may reuse a separately paid accepted rank-one fast path before this route. If it rejects, its entire attempted work must be added; its rejection does not reject the rank-two family. The simpler first implementation can handle one- and two-mode cases together as above. Either choice needs an explicit ordering policy and ledger.

## 4. All-output work without a dense fallback

For the first fully verified witness define the shared Gauss row

`G_a(c) = sum(omega^(a*j*j+c*j), j=0..N-1)`.

Reuse the accepted all-phase rank-one orbit construction. Set

`d=gcd(2*a,N)`, `K=N/d`, `c0=(-a*K) mod d`.

The row vanishes outside `c = c0 mod d`. Compute its seed at `c0` by a paid `N`-term direct sum, then traverse the permitted coset using

`G_a(c+2*a) = omega^(-a-c) * G_a(c)`.

There are `K-1` recurrence steps. Initialize all `N` row entries, including the zeros. The shift-by-`K` cancellation proves the support restriction; shift by one proves the recurrence. No nonzero-seed hypothesis or guessed support parity is required for the algorithm's correctness.

For each `k`, write

`X[k] = c1*G_a(k+b1) + c2*G_a(k+b2)`

with the obvious one-mode and empty-sum versions. All indices are modulo `N`. The construction covers odd and even lengths, composite lengths, zero phase, nonunit phase, and affine support cosets. It uses the same primitive-`N`-root baseline family and positive transform sign as Q13.

The separately accepted Phase43/44 certificate implementation is relevant comparative evidence, but has a primitive-`2N`-root family and different sign convention. It is not silently substituted for this API; for example `N=4,p=5` is a valid baseline grid without a primitive eighth root in the field.

## 5. Paid model and achievable bound

The claimed target is a **named exact-field/data-event ledger**, not an unqualified CPU, bit-complexity, physical-memory or wall-clock result. A completion certificate must pin the final source and specify its events before runtime comparisons.

Required paid stages are:

1. Record/header/range checks, complete raw reads, actual primality trial work, and supplied-root order validation/table writes. Invalidity detected late retains the spent prefix.
2. Optional root discovery only when requested: all candidates, failed partial tables and modular exponentiation internals. Its output root defines the returned DFT coordinate ordering.
3. Nonzero-center selection, all five cyclic lookups, every quartic coefficient operation and write.
4. Exactly `L` phase-filter visits, including every nonroot and every returned candidate. Straight Horner evaluation has four field multiplications and four additions per phase before its comparison and data/index events.
5. Each attempted phase's moment reads, dechirping, fixed-size solve, checked inversions and modular-exponentiation internals; a full `N`-point node scan on every route that reaches that stage. Straight quadratic evaluation uses two multiplications and two additions per node. The rank-one scan is also paid in full.
6. Amplitude recovery and all `N` raw reconstructions/comparisons for every candidate reaching verification, successful or not. With direct root-table synthesis and `s<=2`, a simple schedule uses `N*(s+1)` multiplications and `N*s` additions, plus the reads, indices and comparisons.
7. Gauss support/gcd preparation, `N`-term seed, `K-1` recurrence steps, row initialization/writes, and all mixture-output arithmetic, reads and writes. An ordinary two-mode mixture uses two multiplies and one add per output after the row exists.
8. Final witness, root and complete output materialization/publication. Denial of the last output write or the final publication event must withhold the whole public mathematical result.

The quartic has at most four candidates. Each uses at most two scalar inversions, so at most eight such inversions occur before acceptance/rejection, excluding any optional preliminary rank-one call. Fermat inversion requires `O(log p)` actual metered field multiplications rather than one free operation. All storage can remain `O(N)` field entries, with at most four small candidate records. No `N`-by-`N` transform matrix is needed.

For supplied-root completed calls, the resulting target bounds are

- `O(N+log p)` field additions/multiplications, including boundedly many inversion internals;
- `O(N+sqrt(p)+log p)` complete named work when the stated primality validation is included;
- `O(N)` live field-array storage.

Optional deterministic root discovery has its separate worst-case `O(p*(N+log p))` named work; no linear cold-request bound in `N` alone follows. Constant-degree polynomial and classical recovery arithmetic already imply these field bounds from accepted theory. The **open obligation is source-bound implementation and exact prefix accounting**, not discovery of these asymptotics. The present fresh checker deliberately does not supply a production budget meter. In particular, its rank-two mathematical routine calls the inverse of `Delta` twice; it is not an implementation of the proposed two-inversion-per-candidate ceiling. That target requires caching `Delta^(-1)` and reusing it for both `S` and `P`, followed by one inverse of the node difference.

## 6. Exact identifiability and full-verification controls

### Four canonical phases can all be genuine

Take `N=8`, `p=17`, `omega=2`, and

`x=(2,0,2,0,2,0,2,0)`.

For each `a=0,1,2,3`, choose frequencies `-2*a` and `4-2*a` modulo eight, both with coefficient one. These give the same raw vector. At odd indices their sum vanishes. At `j=2m`, multiplication by the chirp gives

`2*omega^(4*a*m*(m-1)) = 2`,

because `m*(m-1)` is even. The same parity argument works over the complex numbers with any primitive eighth root; it is not an accidental finite-field cancellation.

Equivalently, even phases use dechirped frequencies `0,4`; odd phases use `2,6`. Every witness is genuinely rank two because the raw signal has both zero and nonzero coordinates, whereas a nonzero one-mode chirp has none of its coordinates zero.

At center zero the quartic is `E(t)=8*(1-t^4)`. Its four canonical phase points are `1,13,16,4`, and all are roots and valid phases. The positive unnormalized DFT is `(8,0,0,0,8,0,0,0)` modulo 17. Thus the degree-four candidate bound is attained in number of genuine canonical phases for this instance. This is a sharpness/identifiability control, not a claim that phase ambiguity is a new phenomenon or an obstruction to any-witness acquisition.

### Vanishing and a valid prefix do not establish membership

On the same grid, take

`x=(1,1,1,1,2,1,1,1)`.

At center zero, `E(t)=1-2*t+2*t^3-t^4`, with filtered canonical phases zero and two. Both have a valid short recovery prefix; both fail full raw reconstruction at index four. Independently computed complete dechirped Fourier supports have size eight at **every** canonical phase, so this is a true rank-at-most-two nonmember. An implementation that accepts the quartic or prefix alone fails this small control.

## 7. Fresh evidence and explicit stopping condition

`chirp_rank2_fresh_check.py` is a newly authored mathematical design checker. It imports no uploaded, archived or repository source programs. It compares the specialization against complete explicit-family enumeration, checks the expanded quartic against the direct six-term determinant, and checks Gauss-mixture outputs against direct DFT sums. Its own test code is not an independent review of a future metered executor. Exact counts and source binding are recorded in `chirp_rank2_fresh_results.json`. The completed run passed 279,668 exhaustive raw-vector decisions on the four stated grids, 51,797 direct-determinant identity points, 36,854 accepted direct-DFT output coordinates, and 870 structured cases covering every canonical phase at lengths 8, 12, 16, 32 and 512 (including `p=65537` at the last endpoint). It found and rejected 112,182 false phase-filter roots across the exhaustive controls. The four-phase ambiguity has all four exact witnesses recorded. These finite checks are evidence for the specialization, not a substitute for the proof or the missing meter audit.

The next gate closes only when a pinned bounded executor and a separately authored reviewer establish all of the following:

- exhaustive small-field agreement with an independent family/Fourier-support oracle;
- all-canonical-phase rank-two mixtures, including cancellation, leading zeros, periodic `N=3`, repeated/absent node rejection, false eliminant roots and the four-phase ambiguity above;
- all-output equality at odd/even/composite lengths, nonunit phases and hard bounds;
- complete preparation, attempted/rejected-candidate and terminal-output ledger predictions, with actual arithmetic calls reconciled to counts;
- every-unit interruption controls for representative success, rejection, invalid and optional-search routes, plus exact hard-boundary final-write/publication withholding;
- explicit distinctions among `INVALID`, `NONMEMBER` and `LIMIT`, and a verifier that independently checks the mathematical witness/output rather than trusting telemetry.

A precise counterexample to these hypotheses or a demonstrated resource/accounting blocker is a valid stopping result and must be reported rather than relabeled acceptance. Passing the present mathematical controls alone does not close that gate. General-rank optimized integration, `min(B,H)`, blocked/Toeplitz kernels, bit/process-memory qualification, numerical robustness, optimized-FFT speed and historical priority stay separate.

## Sources and provenance

1. Current [Q13 research-queue row](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1877766156&range=A16), [STR-Q2 continuation row](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1152106829&range=A5), and [ALG-CHIRP-ELIM catalogue row](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001001&range=A5), read from the 12 October 2026 live snapshot. The Q13/STR-Q2 01:03 UTC update supersedes their supplied-odd-only historical description. Snapshot SHA256 `57a577ea5637e6449bd9e7edb44efec312fcfa092369a1424d4516a174163ec7`.
2. *Exact recognition of common quadratic chirps*, working note v3, 11 October 2026, Sections 1–3, 6, Appendix B and C. Read as inert text; SHA256 `b4fccb71cfed1822001cc7d7763df4a8e8d83083972f102a75bb93f974d4c2c0`. This supplies the already accepted general theorem, cyclic filter, dense-reference distinction and classical-attribution boundaries.
3. [Published independent unknown-rank-one review](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-supplement/q13-unknown-rank-one.md), especially Sections 2–5 and 7. Exact recovered text SHA256 `eb7d25c5eec91af5c366d625bb28f5665b5019bfbd8fd4f831bf9c9074210c45`.
4. [Published independent Phase43/44 certificate review](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-supplement/even-chirp-complete-certificate.md). Exact recovered text SHA256 `f58b92a90d08c412b17466d98cb36ec303e2fe2acfc9e85771d352240d9772dc`. It documents the distinct stronger-root family and is not counted as closing baseline Q13 integration.

No historical-priority conclusion is drawn from this gate. No live workbook or repository change was performed by this audit.
