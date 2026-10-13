# Independent review of the bounded rank-two CHIRP design

Date: 12 October 2026 UTC.

**Verdict: the proposed mathematical route and next-gate scope are sound. This is a reviewed design, not acceptance of a metered rank-two executor.** No production implementation, exact runtime ledger, interruption proof, or optimized-FFT comparison is delivered by this review.

## 1. Scope and source binding

Reviewed `chirp_rank2_next_gate.md`, SHA-256 `a62329f96a9ecfe41689f412bb2b6de2abe3fd8a9d650250ed6664a3c0ac9055`, against these exact definitions:

- *Exact recognition of common quadratic chirps*, working note v3, Sections 1–3, 6–7 and the stated classical-attribution boundaries; source SHA-256 `b4fccb71cfed1822001cc7d7763df4a8e8d83083972f102a75bb93f974d4c2c0`.
- The published [unknown-rank-one independent review](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-supplement/q13-unknown-rank-one.md), recovered text SHA-256 `eb7d25c5eec91af5c366d625bb28f5665b5019bfbd8fd4f831bf9c9074210c45`.
- The published [Phase43/44 independent certificate review](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-supplement/even-chirp-complete-certificate.md), recovered text SHA-256 `f58b92a90d08c412b17466d98cb36ec303e2fe2acfc9e85771d352240d9772dc`.
- The current Q13/STR-Q2 records extracted in `chirp_source_rows.txt`; the accepted unknown-rank-one scope supersedes the earlier supplied-odd-only description.

The family is precisely the baseline primitive-N-root family

`x[j] = omega^(a*j*j) * sum(c[l]*omega^(b[l]*j))`, with at most two distinct modes and nonzero listed coefficients; zero has the empty representation.

The proposed domain is `3<=N<=512`, supplied prime `5<=p<=65537`, `N|(p-1)`, with exact-order-N root validation. The output transform has the positive, unnormalized sign. The stronger primitive-2N-root certificate family and its negative-sign transform are not interchangeable with this interface. In particular, `N=4,p=5` is an admitted baseline grid without an order-eight field root.

The author checker and results were inspected as inert text. This reviewer executed only the newly written `chirp_rank2_independent_check.py`, which uses the Python standard library and independent direct Fourier-support sums. No author, archive, historical or repository implementation was imported or executed. The independent counts below are separate from the author's larger self-check counts; the latter are not relabeled independent evidence.

## 2. Quartic necessity and candidate completeness

For a nonzero center `c`, put `z=x[c]`, `u=x[c-1]`, `v=x[c+1]`, `U=x[c-2]`, `V=x[c+2]`, with cyclic indices. Direct expansion of the three-by-three determinant gives

`E(t)=z^3-2*z*u*v*t+(u^2*V+U*v^2)*t^3-z*U*V*t^4`.

The constant `z^3` is nonzero. The degree bound is four even when coordinates wrap or repeat, including N=3. At `t=omega^(-2*a)`, multiplication of raw entries by the triangular exponents removes the quadratic dependence up to nonzero row/column factors. A genuine two-mode or one-mode dechirp has determinant zero. Thus every true canonical phase is retained.

This implication is one-way. A local determinant zero does not prove that the entire signal has at most two modes. The proposal correctly requires a complete canonical grid scan, then independent recovery and full raw reconstruction for each candidate attempted. The phase points for `0<=a<N/gcd(2,N)` are distinct, so at most four candidates survive the original nonzero polynomial. A zero remainder modulo `t^L-1` does not erase this original certificate or authorize rejection.

A negative decision must exhaust every filtered candidate. A failed solve, missing grid node, failed reconstruction, or rank-one fast-path rejection eliminates only the relevant route or phase. Budget exhaustion is indeterminate, never a negative membership certificate.

## 3. Rank-one, zero, cancellation and short-length behavior

For a genuine two-node dechirp,

`Delta=y[0]*y[2]-y[1]^2=c1*c2*(lambda1-lambda2)^2`,

which is nonzero under the stated distinct-node and nonzero-amplitude assumptions. This holds even when `y[0]=0`; cancellation at the first sample therefore must not force rejection of a rank-two candidate. The formulas for the node sum `S`, product `P`, and two amplitudes in the proposal are correct.

When Delta is zero, a genuine nonzero member at that phase must have one node, and its `y[0]` is nonzero. Testing its forced ratio on the full N-root grid and then reconstructing all raw entries is complete and sound. If Delta and y[0] both vanish, that phase can be rejected for a nonzero raw vector. A zero prefix is not permission to accept zero.

For N=3, the fourth moment is periodic reuse of index zero. Both the model and dechirp are N-periodic under this baseline exponent convention, so the reuse is valid. Excluding N=2 from this new gate is explicit and sensible because rank two is the full family there. It does not withdraw the accepted rank-one N=2 result.

Zero acceptance must follow full record, raw-coordinate, prime and root validation. An invalid root or composite modulus must not be accepted merely because all coordinates vanish.

## 4. Independently verified counterexamples and controls

The fresh reviewer script establishes agreement with a different membership oracle: dechirp at every canonical phase, compute the complete normalized inverse Fourier spectrum, and count its nonzero entries. Fourier invertibility is justified by `N|(p-1)`.

- All 343 raw vectors over `N=3,F7,omega=2` agree: 271 members.
- All 625 raw vectors over `N=4,F5,omega=2` agree: 177 members.
- These checks cover 2,274 nonzero-vector canonical-phase decisions, 86 genuine one-mode phases and 516 genuine two-mode phases.
- Direct three-by-three determinant expansion agrees with the quartic in 5,514 point checks, including wrapped small lengths.
- Direct Gauss sums check every phase on N=3,4,5,6,8,12,16,32 at the fields recorded in the results: 86 rows and 1,574 coordinate-level support/recurrence checks.

### Necessary filter plus plausible prefix still fails

For `N=8,p=17,omega=2`, take

`x=(1,1,1,1,2,1,1,1)`.

The quartic coefficients are `(1,15,0,2,16)` modulo 17, and only canonical phases zero and two survive. At phase zero, the first four moments suggest the rank-one witness `(b,c)=(0,1)`. At phase two, they suggest the rank-two witness `((0,7),(4,11))`. Both witnesses reconstruct every raw coordinate except index four.

The complete dechirped spectra have support size eight at all four canonical phases. Hence this is a true rank-at-most-two nonmember, not merely one failed phase. The example independently confirms the proposed full-raw-verification obligation and exposes an implementation that accepts the quartic or the four-sample recovery alone.

### Four genuine canonical phases

On the same grid, `x=(2,0,2,0,2,0,2,0)` has valid rank-two witnesses at all four canonical phases: even phases have frequencies 0 and 4, odd phases have frequencies 2 and 6, all coefficients one. Independent complete spectra and resynthesis verify every witness. No nonzero rank-one chirp can represent this vector because it has both zero and nonzero entries.

The parity identity in the design also proves the same ambiguity over the complex numbers. It is not a finite-field artifact. The universal even half-shift quotient does not remove signal-dependent ambiguity. Returning any fully checked canonical witness is the correct contract; recovering a unique original phase is unsupported.

## 5. All-output mathematics and accounting boundary

For the accepted witness, the proposed Gauss row obeys

`d=gcd(2*a,N)`, `K=N/d`, `c0=(-a*K) mod d`,

with support contained in `c=c0 mod d` and recurrence

`G_a(c+2*a)=omega^(-a-c)*G_a(c)`.

Translation by K proves the support restriction, translation by one proves the recurrence, and the additive step has order K. Thus one N-term seed and K-1 recurrence steps reach the entire permitted coset; initialized zeros supply all other entries. A nonzero-seed assumption is unnecessary for correctness. The proposed positive-sign mixture shift `G_a(k+b)` is correct. Direct controls cover zero/nonunit phases and odd/even/composite lengths.

The promised accounting must pay for complete input validation, primality trial work, root preparation, optional requested discovery, all L filter visits, rejected phase work, full grid scans on reached routes, inversions and exponentiation internals, all reached N-entry reconstructions, row initialization, all transform arithmetic and writes, and terminal publication. Rejection cannot discard spent work. Denying the last write or publication must withhold the whole mathematical result.

The eight-inversion upper bound requires one cached inverse of Delta for both S and P, followed by one inverse of the node difference, for each of at most four candidates. This reviewer requested that explicit clarification. The final design now contains it and states that its unmetered mathematical checker separately calls inverse(Delta) twice. Consequently the checker itself does not realize the proposed two-inversion-per-candidate ceiling. This is a resolved documentation precision issue, not a mathematical failure.

The stated supplied-root target bounds are achievable for this fixed-rank schedule: `O(N+log p)` field additions/multiplications, `O(N+sqrt(p)+log p)` named work with trial primality validation, and `O(N)` live field-array storage. These are design-level bounds. Optional root discovery is separately charged and does not give a linear cold-request bound in N alone. None of these statements measures all Python instructions, bit complexity, operating-system memory, wall-clock time, or speed against an optimized FFT.

## 6. Open implementation obligations and publication wording

The following remain necessary before an executor acceptance verdict:

1. Pin a concrete source, exact standalone input/output contract, finite budget bounds and named events. Decide supplied-root-only versus explicitly requested optional root discovery.
2. Produce complete-route ledger formulas, including failed candidates, invalid prefixes, zero input and optional search. Reconcile actual arithmetic calls to those counts.
3. Independently verify witness and every transform entry; use an oracle not derived from the producer's claimed telemetry.
4. Run every-unit interruption controls through representative success, rejection, late invalidity and discovery routes. Verify final-write and final-publication withholding at hard bounds.
5. Include absent/repeated grid nodes, singular prefixes, cancellation, N=3 periodic reuse, both explicit adversaries above, and all-phase hard-boundary mixture/output tests.
6. Preserve `INVALID`, `NONMEMBER` and `LIMIT` semantics and full output atomicity. Never treat a failed route or a finite budget as global nonmembership.

Recommended publication characterization: **independently checked rank-two mathematical design and sharply specified next implementation/accounting gate**. The rank-two recognition theorem is already a specialization of the accepted general-rank source. This review adds bounded independent controls and checks the proposed executor contract; it does not establish a new Prony theorem, a historical-priority result, or a completed rank-two production integration.

## 7. Reproducibility

Run `python chirp_rank2_independent_check.py` in the directory containing that file. It rewrites only `chirp_rank2_independent_results.json` and imports no other local program.

Reviewer script SHA-256: `5f6c692978bc6638ae80d27c8eb02fc4d40a5d2b03f39212692414e658ad48cd`.

Reviewer results SHA-256: `d03d98dae8c887de5f48c68408770dbb0724a43e615dd70f2143467a42876787`.

Author mathematical checker inspected, not executed: SHA-256 `b7497288aa1976f4a778c2d8d934ba419e979818ff73214353758da6456ef506`; inspected author results SHA-256 `c5aa9ec4ea6c33cbb54d9ffeae2063b3d2b5a97621595c4ceb73e294edfe8892`.

No live workbook or repository write was performed by this review.
