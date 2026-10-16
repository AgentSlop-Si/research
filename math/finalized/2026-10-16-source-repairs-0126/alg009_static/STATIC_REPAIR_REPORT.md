# ALG-009 legacy resonance predicate: separate static repair candidate

Date: 2026-10-16 UTC.

## Disposition

The requested predicate agrees exactly with the complete accepted resonance audit and its recovered historical review. A separately preserved source candidate now rejects a candidate for the **at-most-one-direct-pole-repair policy** exactly when

    g = gcd(N, delta) > 1 and alpha^(N/g) = 1.

This repairs the identified legacy predicate in a separate source copy. It is not an executed historical implementation, an applied production repair, a complete cost audit, a full current-dispatcher audit, or closure of the ALG-009 owner. The model-matched Kaltofen–Yang 2007 comparison is a separate artifact and is not established by this source repair. No spreadsheet, GitHub, Library, or other external writes were performed.

## Owner and accepted evidence read first

The current research owner is ALG-009, priority 42. The complete current owner records were read before the repair. Native spreadsheet snapshots and their private document link are intentionally absent from this publication package. Historical physical-row references in older reports reflect earlier ordering. Current owner status is open for historical attribution / primary-source comparison; accepted scoped correctness is not reopened.

Full accepted audit: `ALG009_RESONANCE_BOUNDARY_AUDIT.md`, SHA-256 `6b2292a9094f5566d5ffeaaf0f6ad40aa2f701e5fcea2e536cfa7d36bd1bc210`.

Full recovered historical review: `PHASE20_AUDIT.md`, SHA-256 `4e6b45aeab8f22872d9cb6ea37cb74b2c06b55492ac53c8fa1991ac7d60678e9`.

Both documents explicitly prescribe this exact correction, distinguish safe over-rejection from wrong accepted output, and retain separate root, Green-domain, degeneracy, raw-certification and cost conditions.

## Exact source and change

Original member: `resultant_gate.py`, 9,158 bytes, SHA-256 `4a1c07d1d6933a399871655eef547451fe8cb24fd026ab70b733b45bda9d8038`.

Fresh reads confirm this member is byte-identical in:

- Phase20 archive SHA-256 `c20b633a0e8a7be1ee81ab65765a15e3fb77a39d3315c7139cef5d88aa1333c3`
- Phase24 archive SHA-256 `6d16fea8f12c8f090e20e1b04a85152f9a9a5891f2e424c018a35d55a82f7006`

The original workspace and archive bytes were left unchanged. The candidate is `corrected/resultant_gate.py`, 9,201 bytes, SHA-256 `09ef37694af956394b82f55bf366e121849cbaf7f4d89caff5527aad9a142ef4`. `resonance_guard.patch` is the exact unified diff. One comment/predicate block is replaced; every other byte matches the original. Both files were parsed as syntax trees without compiling, evaluating or importing them.

Old guard:

    if pow(alpha,n,p)==1 and gcd(d,n)!=1:continue

New guard:

    resonance_gcd=gcd(d,n)
    if resonance_gcd>1 and pow(alpha,n//resonance_gcd,p)==1:continue

No copied dependency, decoder, fallback or hybrid file was changed.

## Why the corrected predicate is exact

Assume a field, a primitive Nth root omega, alpha nonzero, and 1 <= delta < N. Put g=gcd(N,delta) and m=N/g. The homomorphism k mod N -> omega^(delta*k) has g elements in its kernel and image of order m. The image comprises every mth root of unity, since it already supplies m distinct roots of a degree-m polynomial. Thus the equation 1-alpha*omega^(delta*k)=0 has a solution exactly when alpha^m=1, and then has exactly g solutions.

Consequently the number of Fourier poles is g when alpha^m=1 and zero otherwise. The policy allows zero or one pole, so it rejects precisely g>1 and alpha^m=1. For g=1, the unchanged decoder repairs its possible single pole by a direct Fourier dot. For g>1, a nonresonant candidate requires no direct pole repairs and must not be rejected merely because alpha^N=1. Genuine multipole cases remain declined by this branch.

This is an exact pole-budget test, not a complete recognizer of the two-defect family. It says nothing by itself about resultant nondegeneracy, full support, engine construction or fallback availability. The all-field proof supplies the mathematical result; finite testing does not establish an all-size theorem on its own.

## Preserved source contract and safeguards

- The source's N>=8 and p>55 size guard remains before its eight-probe indexing. The theorem additionally assumes a prime field, exact-order root and valid engine. The patch does not add runtime validation that the old function never had.
- Delta is still scanned only in 1,...,N-1; alpha==0 is still rejected.
- An identically zero resultant is still declined. Degree/interpolation witness checks, trivial-factor checks and the degree-45 candidate cap are unchanged.
- Specialized gcd must still be linear. Higher-degree gcds remain a gate decline, not proof of nonmembership.
- Later Hankel tests remain filters. The full raw time-domain scan is unchanged and still requires one or two nonzero defects. The existing zero-defect decline is preserved.
- The decoder continues to divide at every nonpole and obtain each allowed pole coordinate directly from the input. Full-output controls below are independent mathematical reconstructions, not source execution.
- The supplied Nth root alone is insufficient for the literal complete engine. Green diagonals must be nonzero under its constructor, its recurrence denominators must be invertible, and fallback requires compatible 2Nth roots plus its power-of-two convolution roots. The GF73 control is only a residual-gate control. The GF97 control is explicitly in the valid complete-engine domain.
- The untouched shared-probe hybrid can still index eight powers before its downstream size checks. Its N>=8 restriction remains mandatory; this patch does not close the separate early-hybrid-guard task.

## Fresh independent mathematical checks

`independent_predicate_checker.py` is newly authored standard-library-only code. It neither reads nor imports any supplied or patched research source. Its result is `CHECK_RESULTS.json`.

The predicate sweep covers all primes from 3 through 257, all 2<=N<=64 dividing p-1, every 1<=delta<N, and every alpha in the field: 326 field/length grids, 649,025 triples, including 644,364 nonzero-alpha triples. Direct enumeration of all Fourier denominators agrees with the gcd formula in every case. There are zero corrected false admissions or false rejections; the old predicate has 48,662 false rejections and no false admissions relative to the pole budget. These are predicate counts, not certified fast-path instances. Small fields and lengths in this sweep test the mathematical identity; they do not expand the source branch's domain. Alpha zero is included as a supplemental identity check and remains disallowed by the source gate.

Further controls reconstruct polynomial Hankel determinants using signed permutations, monic polynomial gcds using a fresh Euclidean implementation, and the padded 6x6 Sylvester determinant using its 720 signed terms:

1. GF73/N8, omega=alpha=10: nonzero witness T(2)=62; two linear-gcd candidate orientations at deltas 2 and 6; no poles; full residual outputs match direct DFT. Delta 4 has a higher-degree gcd and is declined.
2. GF97/N8, omega=alpha=33: T(2)=48; the same two accepted orientations and higher-gcd decline; every residual output matches. Independent dense Green solves give x=(9,4,77,15,38,66,80,65), and Fx=(63,68,58,32,54,33,13,42), agreeing at all eight outputs with direct DFT. Generator 21, compatible 16th root 79 and convolution length 16 are checked.
3. The distinct historical GF97/N8 witness, omega=alpha=64, r=(1,50,64,96,22,33,50,75): T(2)=95, linear candidates at deltas 2 and 6, all outputs correct. Unlike the two newer controls, this witness has constant gcd at delta 4; the checker records that distinction.
4. A coprime one-pole application control requires exactly one direct repair and returns the complete DFT. A genuine two-pole control has poles 0 and 4 and is declined.
5. A newly constructed N16 inverse-Fourier-character perturbation leaves all eight probes unchanged while changing bin 8. The full raw-defect certificate rejects it.
6. Forty-six evaluations establish the zero-input resultant as identically zero within the degree bound; zero support remains declined. Fresh-checker domain validation rejects small length, too-small/composite field, nonprimitive root, invalid delay and zero alpha. These domain checks do not claim newly implemented historical guards.

Development note: the first fresh checker run applied the newer witnesses' delta-4 quadratic-gcd expectation to the distinct historical witness and failed that overstrong test assertion. Direct fresh polynomial calculation showed gcd=[1] there. The expectation was corrected to an empty higher-degree list; no candidate-source edit resulted. Subsequent final checks passed.

## What remains open

1. Execution-based validation of the supplied or patched historical program has not occurred in this packet. It needs the separately requested approval and must be reported separately if later obtained. This static candidate must not be called an executed or production-validated implementation.
2. The complete printed arithmetic proxy remains incomplete. The gcd/exponentiation, newly rebuilt root tables, pruned negations, fixed algebra, backend setup and fallback accounting are not repaired here. The shorter exponent preserves the scoped fixed-degree O(N) arithmetic argument, but no corrected benchmark total, timing or bit-complexity claim is made.
3. The hybrid's separate early N>=8 guard/restricted domain and full current-dispatcher coverage are unchanged.
4. The named model-matched prior-theorem comparison, including Kaltofen–Yang 2007, is outside this repair; any qualified comparison outcome must be read from its own evidence and independent review. No novelty upgrade, new discovery, canonical-count change or entire-owner closure follows from this static repair.

## Reproduction boundary

The only executable file intended for this packet's present check is the newly authored independent checker. Original and corrected historical sources are inert review material. Run the checker with Python's standard library only; it prints deterministic JSON. Do not execute or import the historical source copies absent separate authorization.
