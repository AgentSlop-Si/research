# Guard-aware fixed-topology Fourier continuation

## Status and result

**AUTHOR-PENDING.** The author-side exact checkers pass. This work has not yet received independent review. It is a continuation of the independently accepted 16-coordinate necessary system, not a Fourier factorization and not an unrestricted complex impossibility result.

The strongest delivered reduction is a **12-free-variable, 55-equation rational-circuit system**, with **all fourteen nonvanishing constraints retained**. Its free coordinates are:

`0, 11, 22, 25, 34, 41, 49, 52, 65, 83, 88, 92`.

Four coordinates are removed safely: `91` in the expanded checkpoint, followed by `39, 44, 55` in the compact triangular branch. “55 equations” counts stored residual constraints, not algebraically independent constraints. The compact system is represented by exact polynomial evaluation and rational reconstruction circuits; it is **not** claimed to be a fully expanded 12-variable polynomial checkpoint. No comparable expanded term count is claimed.

The new transformations are equivalent to the accepted **guarded** 16-coordinate necessary system on its explicitly retained domain. No claim is made that an unchecked solution of either the bare equations or the compact equations supplies an original Fourier factorization. A proposed point must pass every guard, reconstruct all original coordinates through the prior certificates, and satisfy the original 121 entry equations.

## Accepted starting point

- Accepted receipt: `research_cycle_1758/symbolic_independent_review/RECEIPT.json`, SHA-256 `7aa78ab0122f0dacf4231937c608ee1022c793cbeefb2c29ec82356c58d76c2e`.
- Accepted necessary checkpoint: 16 variables, 59 equations, 30,694 terms; largest equation 6,271 terms.
- Eight surviving mandatory coordinates: `39, 41, 44, 52, 83, 88, 91, 92`.
- Six final-coordinate guard polynomials: original mandatory edges `98, 96, 89, 95, 46, 48`, with 2, 2, 10, 2, 10, 6 terms.
- The original review entry and frozen input files are unchanged.

## Direct guard-factor cancellation is exhausted at the starting checkpoint

All six original nonconstant guards are irreducible over Q(ζ₁₁) in the sixteen-coordinate polynomial ring. This is established by small exact certificates, rather than a large multivariate factorization:

- Guards 98, 96, and 95 are degree one in a coordinate with a nonzero field-unit leading coefficient.
- Guards 89 and 46 are linear in x25. Writing either as `a*x25+b`, its certificate gives `b=a*q+c` with a nonzero field constant `c`. Thus the coefficients are coprime and the linear polynomial is primitive and irreducible.
- Guard 48 is linear in x11. Its leading coefficient is `ζ*x34*x41*(x83−ζ^7)`. Its constant coefficient has a nonzero remainder modulo each of those three distinct linear factors, establishing primitivity and irreducibility.

An exact scan checked every starting equation against all six irreducible guards and all eight mandatory coordinate factors: **826 negative divisibility tests**. Therefore no initial equation admits a direct cancellation justified solely by a factor of one of these original guards. This is a statement about direct polynomial divisibility, not about saturation or all consequences of the equations.

## Expanded checkpoint and safe cancellations

A safe field-unit linear pivot eliminates x91 using entry `(10,2)`. The resulting expanded checkpoint has:

- 15 variables and 58 equations
- 124,465 terms total
- At most 25,534 terms in one equation
- No nonzero constant equation

The pass then makes **34 exact mandatory-monomial cancellations**, using x39 and x41. Every cancellation has a stored identity `dividend = certified_nonzero_divisor * quotient`. These cancel degrees and common monomial factors; they do not reduce the term counts in this checkpoint.

Three further exact identities normalize retained guards:

- The transformed x91 guard is divided by mandatory x39.
- The transformed edge-98 guard is divided by mandatory x39 and then mandatory x41.

The nonvanishing conditions are updated, not discarded. In particular, normalizing the x91 guard exposes a new safe x39 pivot that would be missed by testing only the unnormalized guard polynomials.

## Compact continuation without large expansion

The compact branch starts at the guarded 15-coordinate checkpoint. It solves three equations in the reconstruction order `39, 44, 55`. Each denominator is proved nonzero by an exact product identity:

- x39: nonzero field constant times the normalized x91 guard.
- x44: nonzero field constant times `x83 * g89 * g95 * g48`.
- x55: nonzero field constant times `x83 * g95`.

Here `g89`, `g95`, and `g48` are the currently retained transformed guards, not fresh assumptions. Every guard needed for a denominator depends only on free coordinates and previously reconstructed variables. The three source equations are removed because their recorded linear solve identities vanish identically after the corresponding substitution. The other 55 equations and all fourteen guards are evaluated through the exact triangular substitutions.

After reconstructing `39, 44, 55`, the earlier x91 replacement reconstructs the original sixteen-coordinate checkpoint. The existing accepted reverse-reconstruction certificates then remain applicable.

### A useful simplified core

Two of the eliminations simplify substantially. Set

`T = ζ − ζ^9*x41 + x11*x41*(x34+x49)`

`A = (ζ^9−ζ^4)/(ζ−1)` and `U = A*T−1`.

Then the certified replacements are

`x39 = U/T`,

`x91 = −U/(ζ^7−ζ^6)`.

The retained normalized x91 guard is exactly `−T`, so division by T is justified. On that domain, the retained x39 exclusion is equivalent to `U ≠ 0`. These formulas do not replace the other retained guards or the residual equations. `SIMPLIFIED_CORE.json` and the auxiliary checker verify the exact identities.

## Stopping rule and limits

The fully expanded route is bounded by 50,000 terms per polynomial, 300,000 terms per equation system, and 2,000,000 term-pair products per multiplication. It stops after testing all certified safe pivots found by the stated guard-product scan:

- x39 expansion produces 50,970 terms, above the per-polynomial limit.
- x55 crosses the 50,000-term intermediate limit.
- x44 requires a 14,969-by-375 product, above the 2,000,000 pair limit.

The compact branch records these already-certified acyclic pivots without expanding them. It does not claim an exhaustive further circuit-level pivot search. No Gröbner-basis search was launched. The earlier 15,000-term exploratory checkpoint and the first 50,000-term checkpoint are preserved separately.

## Exact verification and artifacts

All inherited research and review programs were treated only as files/data; none was imported or executed. The generator uses freshly authored exact cyclotomic arithmetic with integer coefficient vectors and rational denominators. Its own continuation scripts import only this newly authored kernel.

The standalone checker does not import the generator. It uses ordinary polynomial convolution followed by descending Φ11 reduction, distinct from the generator's cyclic-convolution field multiplication. It independently parses the frozen coefficient expressions, verifies input hashes, checks every product and substitution identity, and checks every updated guard. The auxiliary checker uses that separate checker arithmetic to verify the compact dependency order, all denominator products, the six irreducibility proofs, 826 initial negative divisibility tests, and the simplified core.

Key files:

- `CERTIFICATE.json`: all exact polynomial data and 38 committed expanded-stage events.
- `FINAL.json`: the 15-variable expanded checkpoint references and retained guards.
- `COMPACT_BRANCH.json`: strongest 12-variable, 55-equation exact rational-circuit reduction.
- `SIMPLIFIED_CORE.json`: simplified x39/x91 formulas and their exact sources.
- `GUARD_IRREDUCIBILITY.json`: the six small irreducibility certificates.
- `CHECK_RECEIPT.json`, `AUXILIARY_CHECK_RECEIPT.json`: successful author-side verification receipts.
- `check_guarded.py`, `check_auxiliary.py`: checkers; their logs are included.
- `scan_15000/`, `scan_50000/`, `compact_13/`: preserved earlier checkpoints.
- `REVIEW_ENTRY.json`, `SHA256SUMS.txt`: independent-review entry and artifact hashes.

Recheck from the shared workspace root:

    python research_cycle_1805/guarded_fourier_reduction/check_guarded.py
    python research_cycle_1805/guarded_fourier_reduction/check_auxiliary.py

The checkers inspect only frozen input data and this new certificate package. A passing author-side check is not a substitute for independent review.
