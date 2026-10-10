# HERO0 Phase 6: exact sparse global phase support

Audit: 9 October 2026 UTC. The source's 10 October date is its research label. This is a bounded mathematical and implementation audit. Uploaded programs were read as data, never executed, imported, or compiled. The master and Library were not modified.

## Verdict

Accept the adaptive recognition theorem and exact Green reconstruction for the stated restricted class, with the model and implementation corrections below. The class is genuinely larger than a fixed-dimensional global exponential family: it has K r independent coefficients, and already its one-mode stratum can have maximal ordinary Hankel rank. Its support is recovered from fresh raw input rather than supplied as input-dependent advice.

This construction does not establish an arbitrary-input exact sub-N-log-N FFT. The family is a finite union of proper subspaces when r<M, and generic inputs have full global phase support under every chirp in the proposed finite library. The complete r=M bank returns the already-audited ordinary-FFT endpoint.

Three corrections are essential:

1. The source's claimed fully charged numerical operation totals are incomplete. A plain unmetered sum forms every Green-cycle seed, omitting at least r(Q-1) additions. Modular exponentiation, inverse/setup work, integer indexing, comparisons, storage and output writes are also not represented by the displayed addition-plus-multiplication total. The asymptotic theorem survives when these are charged under its declared arithmetic/RAM assumptions.
2. The shipped exact and complex executors return a rejection result. They do not call the full-FFT fallback described in the algorithmic prose. An exact ordinary-FFT wrapper can be supplied in a compatible field/length model, with both rejection and fallback work charged.
3. The entropy lower bound is inherited, including within this project. It is the same two-coordinate unitary matrix-entropy argument already audited in Phase16, and the underlying published result is due to Ailon. It is not a new route closure or a lower bound for general nonunitary arithmetic.

## 1. Provenance and independently generated evidence

Source: `../original/fft_hero0_phase6_sparse_phase_support_2026-10-10.zip`.

- Library identity: `[private-id]`
- Backing identity: `[private-id]`, version 0
- Exact size: 94,306 bytes
- SHA-256: `0eda6f3c099d736e3ee2439c531cdfcc6b83f672ea3a2ff9dcb5afeda5d4cd5e`
- 23 outer files; all 22 entries in the supplied checksum manifest verify
- The 63,652-byte `prior_phase5_bundle.zip` is byte-identical to the previously audited Phase5 upload: SHA-256 `25e1d0329da56504d8e3ff855ce11a63c2dcef0a41e69a6879f7e17a06130878`. Its 22-member inventory is inherited, not a new source

The unchanged archive, safe extraction and complete per-member hashes are preserved. Extraction screened absolute/traversal/backslash paths, symlinks, encryption and excessive member expansion. `../SOURCE_MANIFEST.json` records the bytes; `PROVENANCE.json` records prior-source mappings. Prior reports needed for this bounded comparison are copied read-only under `prior_evidence/`.

The independently authored `independent_checks.py` uses direct finite-field DFT definitions rather than any uploaded FFT implementation. It checks recognition, complete-mode synthesis, the Green difference equation, its antiperiodic closure, and every accepted output against an independent direct Fourier sum. It exercises zero inputs, arbitrary inputs, shared supports, disjoint per-block supports, support appearing only near the end, cap rejection, full support, and several even composite non-power-of-two lengths.

The saved run establishes:

- 15,000 exhaustive cases over F5, Q=4, covering every input, both unit slopes, every beta and all caps
- 1,476 additional exact cases over nine length/factor/field configurations, Q=8 through 128
- 6,192 accepted cases, 10,284 correctly rejected cases and 55,716 exact output entries
- 108 exact maximal-Hankel-rank witnesses with their determinant formula
- All-chirp constant-input controls and an explicit one-mode separation witness against every rank-one common quadratic chirp at Q=16
- The source coverage bound, a small exact quotient refinement, 100 numerical unitary-gate entropy diagnostics, and an analytic floating-recognition counterexample

The exact counts and witnesses are in `CHECK_RESULTS.json`. The numerical entropy checks are diagnostics; the entropy proof supplies the general result. These tests do not establish a complexity theorem by timing, certify floating arithmetic, or validate the uploaded executables by execution.

Portable replay: with Python 3 and NumPy, run `python3 audit/independent_checks.py` from any copy of this complete supplement. The checker locates its source data relative to its own path. It rewrites only `audit/CHECK_RESULTS.json`; output is deterministic. `PAYLOAD_SHA256.json` seals every other payload file and is itself excluded from its manifest.

## 2. Exact model and identity

Let Q=KM, K>=M>=2, Q even, a a unit modulo Q, and beta fixed. Let zeta have exact order Q. Work over C with supplied exact constants and exact equality, or over a field with characteristic not dividing 2Q and the required root. Put

`s[b,t] = zeta^(a*t*(t-1)/2 + (a*M*b+beta)*t)`

and `D[b,r] = sum_t s[b,t] x[b*M+t] zeta^(K*r*t)`.

Block Fourier inversion gives

`x[b*M+t] = s[b,t]^(-1)/M * sum_r D[b,r] zeta^(-K*r*t)`.

For a global support S, this is zero off S in every block, while D[b,r] is otherwise unrestricted. Each active mode is precisely the prior Green row with beta shifted to beta+rK. Consequently the unnormalized Fourier transform satisfies

`F_Q x = (1/M) sum_(r in S) F_Q P_r x`.

This is inherited complete-frame algebra applied to a newly recognized sparse-column family. The new execution improvement is avoiding all inactive rows and avoiding a full Q log M analysis just to determine their inactivity.

For completeness, let B be the negative-exponent K-transform of one mode's block coefficients. Its forcing is

`f[k] = B[k mod K] - zeta^(-M*(k+beta)-a*M*(M-1)/2) B[(k+a*M) mod K]`.

The output satisfies `Y[k] - zeta^(-k-beta)Y[k+a] = f[k]`. Along k=a*j, the gauge is `g[j]=zeta^(a*j*(j-1)/2+beta*j)`. Since Q is even and a is odd, g[Q]=-1. Thus the seed is one-half of the complete gauged forcing sum, followed by a prefix scan. This proves the exact all-output decoder, including its required characteristic and parity. The source's modular implementation is narrower: powers of two only, over its specific prime/root pair. Our broader even-composite algebra checks do not turn that implementation into a general-length NTT.

No odd-Q certificate is claimed here. The earlier complex decoder's half-root parity twist is a separate definition that must not be silently omitted in a finite-field extension.

## 3. Recognition, fresh input and rejection charges

Maintain the union S of modes discovered so far. For every block, compute the coefficients indexed by S and reconstruct every coordinate. In exact arithmetic, a successful certificate proves that every coefficient outside S is zero. On failure, a full length-M transform necessarily reveals a previously unseen nonzero coefficient. Any newly discovered mode is zero in every earlier block, including earlier failed blocks whose complete spectra were then stored.

This proves all three needed facts:

- Accepted support and coefficients are exact; no probabilistic membership test or supplied support advice is used
- A successful input of true support size r triggers at most r full short transforms, including zero for the zero vector
- With cap R, rejection occurs after at most R+1 full short transforms, even when a single failing block introduces many new modes

The recognized chirp a,beta and factorization are fixed or supplied length-dependent parameters. The theorem does not discover a favorable chirp for free. Searching a list of chirps pays for every trial, even though each trial reads the same raw input. Synthesizing sparse test inputs is not the recognizer's preprocessing and cannot substitute for its full raw-input certificate.

For accepted input, an explicit charged ledger is

`O(Q + r*Q + r*K*log K + (r+1)*M*log M)`.

It includes root-table preparation from a supplied primitive root, all dechirping, O(rM) coefficient/reconstruction work per block, at most r discoveries, storage/zero filling of at most Kr coefficients, all r decoders, accumulation, normalization and writing Q outputs. O(Q) field-word storage suffices: Kr<=Q, the Q-power table and one Q-output row at a time. The complex prototype's M-by-M phase table also fits because M²<=Q.

On rejection at cap R, before any decoder executes, the bound is

`O(Q + R*Q + (R+1)*M*log M)`.

With M=Theta(log Q), accepted work is O((r+1)Q), and worst-case recognition at cap R is O((R+1)Q). Therefore constant r gives linear work and r=O(log log Q) gives O(Q log log Q). More generally the same uniform ledger proves accepted work o(Q log Q) for any r=o(log Q). This remains a restricted-class theorem: the allowed dimension rK=o(Q) in that regime.

An ordinary exact fallback, when independently available in the same root/field/length model, adds O(Q log Q) only after rejection. With R<=M=Theta(log Q), worst-case wrapped work stays O(Q log Q). The source code explicitly returns None or `accepted=False`; no shipped end-to-end fallback should be reported. A fixed finite dispatcher of such branches pays the sum of all preceding recognition costs before the accepted branch or fallback. Testing many decompositions or growing lists of parameters is additional work.

The chosen factorization is essential. There is no promise that arbitrary lengths admit M=Theta(log Q), and padding an arbitrary length/input does not preserve sparse support or identify its original Fourier output with a padded transform for free. The result supplies no new all-length exact theorem.

## 4. Source counters and arithmetic-model obligations

In `phase6_exact.py` line 153, `sum(terms)` bypasses the addition counter. Each r-row execution requires at least r(Q-1) additions just for these sums. On the supplied r=2 benchmarks this increases the displayed count by almost two operations per input, before any other omissions. The source's 26.95–28.50 range becomes at least 28.94–30.50 in the saved cases after that correction alone. `CHECK_RESULTS.json` records each corrected lower total.

The primitive-root and inverse modular exponentiations and the NTT stage-power computations are also outside the addition/multiplication total. A separate `roots` counter increments once per stage power, not once per field multiplication in that power. Index arithmetic, comparisons, allocations, memory traffic and explicit writes are likewise distinct from that field-operation total. Accordingly neither “every operation counted” nor the displayed number as an end-to-end work certificate is warranted.

These omissions do not break the asymptotic bound under the stated suitable-root model. A length-Q table costs Q-1 field multiplications; one M inverse and setup add their declared costs; stage powers via repeated squaring cost O(log² length) per short transform, dominated by the transform/scan work at growing Q. The setup term involving log p must remain explicit if scalar inversion is implemented by exponentiation and p is allowed arbitrarily large. Taking p=Q^O(1), or separately charging inversions in the exact field model, makes the usual absorption clear. This is not a uniform prime/root discovery theorem, nor a bit-complexity bound. The shipped fixed 31-bit field has finitely many supported roots and cannot itself demonstrate an unbounded asymptotic family.

The source's own saved Python timings are slower than its NTT oracle in every listed case. They are source-reported observations, not independent practical benchmarks or comparisons with optimized FFT libraries.

## 5. Coverage, Hankel rank and strict distinctions

For a fixed S, the invertible blockwise analysis map gives dimension K|S|. Thus for r<M, searching any finite collection of slopes, shifts and supports cannot cover generic C^Q input: each candidate is a proper linear subspace. Over F_p the source union bound is valid:

`Pr[covered] <= min(1, Q*phi(Q)*sum_(j=0)^r binom(M,j)*p^(-K*(M-j)))`.

The explicit minimum with one avoids treating a loose upper bound as a probability. At p=2013265921,Q=256,M=16,r=2, its base-10 logarithm is about -2077.47922467, verifying the source's stated inequality.

A small bounded refinement is available. Replacing beta by beta+cK just permutes all global mode labels; only K beta representatives are needed. Also every <=r support lies inside an r-element support. Hence for 0<=r<=M,

`Pr[covered] <= min(1, K*phi(Q)*binom(M,r)*p^(-K*(M-r)))`.

The example's refined logarithm is about -2078.68334465. This strengthens the same architecture-specific coverage gate, not a Fourier arithmetic lower bound.

For even K, the central-block witness with one active mode has x[j]=0 for j>=Q/2 and x[Q/2-1] nonzero. Reversing the columns of its square Q/2 Hankel matrix makes it triangular, so its determinant is `(-1)^(h*(h-1)/2)*x[h-1]^h`, h=Q/2. The determinant is therefore a nonzero polynomial in the independent block-mode coefficients. Over C, jointly absolutely continuous coefficients give full Hankel rank almost surely; coordinate nonvanishing is likewise generic. These probability-one assertions do not transfer verbatim to finite fields. The modular witnesses establish exact examples.

High ordinary Hankel rank alone does not separate this class from the prior common-quadratic-chirp family, since a quadratic chirp can itself have high ordinary Hankel rank. A stronger bounded comparison uses actual coordinates and dimension:

- When K is a multiple of M, the constant vector has full global Phase6 support for every unit a and every beta. Indeed b→b+K/M multiplies the local chirp by zeta_M^(a*t), cyclically shifting its nonempty local Fourier support through every mode. The constant vector is rank-one in the prior common-chirp model (zero quadratic and linear phase). Thus the sparse Phase6 union with r<M does not include that older rank-one class.
- Conversely a fixed Phase6 support space has dimension Kr. A finite union of common-chirp spaces of coefficient dimension at most s cannot cover it over C when Kr>s. The analogous finite-field counting statement holds when the corresponding union-size bound is below p^(Kr); one must not use infinite-field measure language over a fixed finite field. Our explicit F17,Q=16,M=4 witness with D[:,0]=(1,2,3,5) belongs to Phase6 but to none of the 256 one-character quadratic/linear phase choices. This proves an exact finite-field rank-one noninclusion in the other direction.

Thus the two rank-one families are genuinely distinct, while no unproved general inclusion between all existing structured dispatch branches is asserted. The simultaneous HERO17 shear/trace audit uses interleaved, balanced fibers, unknown shears/scales, dense trace-visible orbits and optional sparse residuals. Its gauges and nondegeneracy conditions differ. The safe fusion is a fixed, fully charged union dispatcher in compatible fields/lengths, not a claim that either recognizer subsumes the other.

## 6. Entropy, precision and relation to Phase5

For a Q-wire unitary state matrix, a unitary mixer on two coordinates changes the matrix entropy by at most two bits. A column's two-row mass is fixed and its binary split entropy lies between zero and one; the total mass of those two rows is two. Identity has entropy zero, normalized Fourier has Q log2 Q, so at least (Q/2)log2 Q such mixers are required. The radix-two network attains the bound.

This is a revalidation of the known restricted model, already present in `prior_evidence/PHASE16_AND_EARLIER_AUDIT.md`. The external primary reference is [Nir Ailon, 2013, A Lower Bound for Fourier Transform Computation in a Linear Model Over 2x2 Unitary Gates Using Matrix Entropy](https://arxiv.org/abs/1305.4745). It does not cover arbitrary nonunitary arithmetic, free global gates, or qubit-operation counts. No publication novelty is inferred.

The exact finite-field recognizer uses equality. The complex prototype uses a tolerance and cannot certify exact membership. An explicit counterexample requires no roundoff: take x=(atol/2)e_0. Since its magnitude is below `atol*(1+max|x|)`, every block accepts the empty support and the returned output is zero, although the true global support contains all M modes. Its true normalized Fourier coefficients have magnitude atol/(2 sqrt Q), all nonzero. This is consistent with a small absolute-error behavior, but disproves mathematical exactness of that accepted floating input.

No complete residual, precision, working-range or exact-support-gap contract is supplied. Earlier int64 phase overflow and floating root-generation caveats remain. The modular executable returns unnormalized Fourier values; the complex executable returns normalized values. Those are equivalent only after explicitly supplying/charging the corresponding normalization in a model where it exists. Finite-field algebra does not supply complex magnitude/error estimates or a finite-bit implementation of exact complex equality.

The Phase5 measurement deficit gate does not refute this detector: it reads and checks raw input and only promises a restricted family. The full-bank determinant and entropy gates also cannot be applied as if its input carried Q independent free coordinates after restriction to a Kr-dimensional subspace. Conversely the new raw-input recognizer does not defeat those properly scoped measurement-only obstructions or turn the separate alpha<1/2 conditional approximate theorem into an exact transform.

## 7. Disposition and next exact gate

Preserve Phase6 as an independently audited structured exact fast path, with complete rejection charges, the source-counter correction, strict precision caveats and inherited entropy attribution. Its one-mode high-Hankel examples and unknown-support recognition are useful additions to the project. Its global sparse-support mechanism does not resolve generic input.

The next exact target remains a concrete globally executable contraction for full-support data, with an exact all-output identity and fully charged roots/constants, coefficient preparation, input inspection, arithmetic, indices, memory, exceptional paths and writes. The already-known complete-bank collapse cannot be relabeled as a new speedup. This audit does not certify the source's passing reference to a 2026 external exact-FFT result, launch broad architecture search, or claim practical speed, bit-complexity improvement or unrestricted lower bounds.
