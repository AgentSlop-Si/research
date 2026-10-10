# Independent audit: equation-forced denominator eliminations

## Verdict

**PASS within the accepted guarded necessary-system scope.** The frozen author certificate gives a bijection from the accepted **12-free-coordinate, 55-residual circuit** to a **9-free-coordinate, 52-residual circuit**. All fourteen original nonvanishing guards remain, and the three new denominator guards are consequences of the original equations. No zero-denominator component of the accepted guarded solution set has been discarded.

The nine free coordinates are **x0, x11, x25, x34, x41, x49, x65, x83, x92**. The new solves are **x22, x88, x52**, followed by the unchanged **x39, x44, x55** solves and accepted **x91** restoration. The consequence **x22 ≠ 0** is valid.

This is neither a feasible Fourier factorization nor a contradiction. It is not a sufficiency result for the original 121 Fourier entry equations. Counts describe stored constraints and guards; they do not assert algebraic independence or dimension.

## Frozen inputs and independence

Accepted predecessor receipt:

- `research_cycle_1819/guarded_reduction_review/RECEIPT.json`
- SHA-256 `51f6adcf4c160cc5b83ae44d99f77544067f91ec915db1fcc234ae83d4f48c39`

Frozen author review entry:

- `research_cycle_1825/guarded_consequences/REVIEW_ENTRY.json`
- SHA-256 `9e691093a9cd9ff23218d5f44b107e4cc2d1d16ea5589185fda2fb9736674a22`

Frozen consequence certificate:

- SHA-256 `44ace9f92adb7784f862705c29974fe4eb3faadf6ab38131934da950cf636a2b`

Frozen author report:

- SHA-256 `1cc0969a6b5003a9ca5502d6e8b09d30ea1ee58a216eaaa63f8a58ae4b3f4a82`

The checker independently pins the author-provided freeze hashes, verifies every file and byte count in the review entry, verifies the complete `SHA256SUMS.txt` coverage, checks author receipt bindings, and rechecks all source hashes listed by the accepted predecessor. All frozen file hashes are checked again at completion. The source hash map is retained in the independent receipt.

`check_independent.py` was written from scratch for this audit. It imports only Python standard-library modules. **No author or inherited research/review program was run or imported.** Their programs were hashed as provenance bytes, not used to compute this result. JSON records alone supply input polynomials. The predecessor's already accepted reduction is the trust boundary; its complete earlier algebraic history is not claimed to have been re-proved here.

The checker validates all 202 distinct inherited content-addressed polynomials, containing 376,648 stored terms, plus six new polynomials. It checks canonical rational coefficient encoding, strictly ordered nonnegative exponent vectors, absence of stored zero terms, content hashes, and reference consistency. Coefficients are exact rational vectors in the basis 1, ζ, …, ζ⁹. Multiplication uses direct convolution and descending monic reduction by Φ11. Arithmetic self-tests verify Φ11(ζ)=0 and ζ¹¹=1. The coefficient-field interpretation uses the Eisenstein proof for Φ11(t+1) at 11.

## Exact equations and nonvanishing proofs

All identities below were checked coefficient by coefficient in the full parent polynomial ring, before any rational substitution.

1. Equation 58, entry (10,10):

   E58 = x22 D22 − ζ, with D22 = x34 + x49.

   Hence x22 = ζ/D22. Because ζ is nonzero, D22=0 would force ζ=0. The same identity proves x22≠0. No assumption on x34 or x49 individually is needed.

2. Equation 36, entry (6,3):

   E36 = x88 D88 + ζ¹⁰.

   Hence x88 = −ζ¹⁰/D88. The numerator is the nonzero field constant −ζ¹⁰, encoded canonically as 1+ζ+⋯+ζ⁹. Thus D88=0 is impossible on the predecessor solution set.

3. Equation 4, entry (1,0):

   E4 = x52 D52 + ζ⁴ x83.

   Hence x52 = −ζ⁴ x83/D52. The exact retained original guard named x83 is the coordinate polynomial x83 itself. It is already available as a free coordinate and required nonzero. Therefore this numerator is nonzero, and D52=0 is impossible on the guarded predecessor solution set. The proof does not extend to the omitted unguarded x83=0 domain, and no such extension is claimed.

The independently reconstructed grouped formulas in the frozen report also agree exactly with the stored seven-term D88 and thirteen-term D52. With a=x11*x34 and w=x0*x65, these are:

D88 = −ζ⁷ + x41[ζ−ζ¹⁰ + a(ζ⁷−ζ⁹+(ζ²−1)x83) + w(ζ¹⁰+a(x83−ζ⁷))].

D52 = −x83 + w(−ζ⁷+ζ⁶*x83)
      + x0*x49[ζ³+(ζ⁵−ζ²)x83+x25(−ζ²+ζ*x83)
      +(−ζ⁸+ζ⁷*x83)x88(1−x92−w)].

The zero-branch argument is exact: for E=vD−N=0, nonzero N forces both D≠0 and v≠0. This uses an equation together with retained guards, rather than merely assuming D is generically nonzero.

## Dependency order and inherited reconstruction

The complete new dependencies are:

- x22: 34, 49
- x88: 0, 11, 34, 41, 65, 83
- x52: 0, 25, 49, 65, 83, 88, 92

In particular, x52 uses x88 only after x88 is defined. Neither its numerator's guard proof nor any new denominator proof depends circularly on the variable being solved.

The three inherited definitions are exactly unchanged as records. Their source equations and all three guard-product identities were independently re-proved:

- D39 = (1−ζ) * normalized_guard_x91
- D44 = (ζ⁴+ζ⁵+ζ⁶) * x83 * g89 * g95 * g48
- D55 = ζ * x83 * g95

Each scalar is nonzero in Q(ζ), each factor remains among the fourteen original guards, and each factor's variables are available at the relevant reconstruction step. The guard named x91 here is the accepted transformed guard, not a circular demand to evaluate the as-yet unreconstructed coordinate x91.

The checker also re-proves the final accepted x91 source identity and verifies its numerator only uses the reconstructed fifteen coordinates. Its denominator ζ⁷−ζ⁶ is a nonzero field constant. Earlier reverse reconstruction remains delegated to the accepted predecessor theorem.

## Exact correspondence of solution sets

Forward direction: take a solution of the accepted 12-coordinate guarded circuit. Its reconstructed fifteen-coordinate point satisfies the three retained source equations above. Their nonzero numerators force D22, D88, and D52 nonzero and determine the three coordinates uniquely. Project onto the nine listed free coordinates. Evaluating the new definitions recovers x22 and x88, then x52; evaluating the unchanged inherited definitions recovers the same remaining coordinates. Every retained residual and guard therefore holds.

Reverse direction: start with a nine-coordinate assignment in the new rational circuit domain satisfying its 52 residual conditions and 17 guards. Each definition is well-defined in order. The three new exact solve identities restore E58=E36=E4=0. The remaining 52 residual references are exactly all the other accepted 55 residuals, with no replacements. The fourteen old guards are exactly preserved. Thus this reconstruction is a solution of the accepted 12-coordinate circuit. Projection and reconstruction are inverses because every solve is unique.

The checker additionally accounts for the full fifteen-coordinate parent: precisely six distinct source equations, three new and three inherited, are removed from its 58-equation dictionary. Every other equation remains. No substituted residual has been expanded, cancelled, or asserted equivalent to an unprovided polynomial. Circuit composition and complete dictionary/dependency accounting are sufficient for the correspondence proved here.

## Mutation controls

The independent checker rejects **18 deliberate corruptions**, recorded in `MUTATION_CONTROLS.json`. These include rehashed numerator and denominator coefficient changes, a missing numerator guard factor, a zero numerator scalar, missing original and derived guards, an incorrect derived-guard reference, wrong source label/reference, a missing dependency, an invalid reconstruction order, dropped/replaced residuals, an incomplete free-coordinate list, an altered inherited pivot, a changed source hash claim, and unhashed polynomial tampering.

The main certificate file's frozen hash pin is deliberately bypassed for these in-memory semantic trials. Rehashed polynomial mutations reach and fail the exact source-identity check, so their rejection is not merely a consequence of a stale content address. Original files remain unchanged. The author's separate seven-control receipt was hash-bound but its checker was not executed or used as proof.

## Replay and scope

From the workspace root:

    python research_cycle_1828/forced_denominator_review/check_independent.py

Review artifacts:

- `check_independent.py`: fresh independent checker
- `check.log`: successful run output
- `RECEIPT.json`: exact verdict, checks, source hashes, and checker hash
- `MUTATION_CONTROLS.json`: independent negative-control results
- `REVIEW_ENTRY.json` and `SHA256SUMS.txt`: review artifact bindings

No Sheet or GitHub write was made. No further theoretical reduction, feasibility search, Gröbner computation, or unrestricted impossibility claim is part of this review.
