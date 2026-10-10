# Independent review of the guarded Fourier reduction

## Verdict

**PASS, within the stated guarded necessary-system scope.** The new reduction is independently verified as equivalent to the accepted guarded 16-coordinate, 59-equation checkpoint. No original Fourier factorization, contradiction, or unrestricted complex no-go follows from this review.

The verified outputs are:

- An expanded checkpoint with **15 variables, 58 equations, 124,465 terms**, and at most **25,534 terms** in one equation.
- An exact triangular rational-evaluation circuit with **12 free variables and 55 residual equation constraints**.
- **All fourteen nonvanishing constraints retained.** No optional-zero component was discarded through an uncertified division.
- Four valid eliminations: **x91**, then **x39, x44, x55**.
- **34 exact mandatory-coordinate cancellations** and **three exact guard-normalization identities**.
- Six independently verified original-guard irreducibility proofs and **826 certified initial nondivisibility statements**.
- Independently checked simplified x39/x91 formulas, with the necessary guard conditions maintained.

The twelve free coordinates are `0, 11, 22, 25, 34, 41, 49, 52, 65, 83, 88, 92`. The number 55 counts stored residual constraints; algebraic independence is not asserted.

## Frozen input and independence

The review entry is `research_cycle_1805/guarded_fourier_reduction/REVIEW_ENTRY.json`, SHA-256 `06ff76f081c8fdba74e9bc77a2036247e4515b0e57930117ea85504e616b97e7`.

The accepted predecessor receipt is `research_cycle_1758/symbolic_independent_review/RECEIPT.json`, SHA-256 `7aa78ab0122f0dacf4231937c608ee1022c793cbeefb2c29ec82356c58d76c2e`.

Every file in the new entry manifest, every source and review-artifact hash listed by the accepted predecessor, and the compressed/decompressed certificate identities were checked. Frozen hashes were checked again at the end. All inherited files remain unchanged.

`check_independent.py` was freshly authored for this review. It imports only Python standard-library modules, never an inherited research or review program. It uses exact rational coefficient vectors in the basis `1,zeta,...,zeta^9`, direct polynomial convolution followed by monic Phi_11 reduction, rational Gaussian elimination for field inverses, and a restricted arithmetic AST parser for the accepted predecessor's coefficient strings. All 223 distinct content-addressed polynomials across the reviewed certificate pools were parsed canonically and their addresses checked.

The accepted predecessor's 59 equations and fourteen guards were independently loaded and compared term by term to the new starting point. This review relies on the prior accepted topology/reconstruction result; it does not rerun that prior research program or pretend to re-prove its whole history.

## Exact expanded-stage replay

The source equation for x91 is entry `(10,2)`. Its identity is exactly

`source = (zeta^7-zeta^6)*x91 - numerator`.

The denominator `zeta^7-zeta^6` is a nonzero element of Q(zeta). The checker independently recomputed all 59 equation substitutions, including the source equation's zero result, and all fourteen guard substitutions. For every polynomial P, it checked the recorded denominator power m and the exact identity represented by `D^m P(x91=N/D)`. Removing the identically zero source leaves 58 equations.

Each of the 34 cancellations was checked as the exact polynomial identity `dividend = divisor * quotient`. Every divisor was the currently retained mandatory-coordinate guard, specifically x39 or x41. No zero factor was silently discarded.

The three guard normalizations were replayed in their actual order:

1. Divide the transformed x91 guard by the retained x39 guard.
2. Divide the transformed edge-98 guard by the retained x39 guard.
3. Divide that edge-98 quotient by the retained x41 guard.

The checker required current-state references at each step and exact product equality. Divisor guards remain present, so these updates preserve the nonvanishing domain in both directions. The final equation and guard dictionaries match `FINAL.json` exactly. The term and variable counts were recomputed from the resulting polynomials.

## Compact circuit audit

For each compact definition, the checker proved the source polynomial identity `P = D*x - N` in the parent fifteen-coordinate polynomial ring. It also independently checked the full numerator/denominator dependency set and the denominator product certificate. The following denominator identities hold exactly:

- x39: `D39 = (1-zeta) * normalized_guard_x91`.
- x44: `D44 = (zeta^4+zeta^5+zeta^6) * x83 * g89 * g95 * g48`.
- x55: `D55 = zeta * x83 * g95`.

All three field constants are nonzero. Here the guard symbols refer to the **currently retained transformed guards**, exactly as stored in the parent checkpoint.

The dependency graph is acyclic:

- x39 depends on `11, 34, 41, 49`.
- x44 depends on `0, 11, 25, 34, 39, 41, 49, 65, 83, 88, 92`.
- x55 depends on `0, 11, 25, 34, 39, 41, 44, 49, 65, 83, 88, 92`.

Every guard factor used to establish a denominator's nonvanishing depends only on free coordinates and previously reconstructed coordinates. Thus there is no circular assumption that a later, still-undefined variable makes an earlier denominator nonzero.

The source equations removed are entry `(8,6)` for x39, `(0,5)` for x44, and `(0,8)` for x55. Under their recorded substitutions, their numerators cancel identically. The checker verifies that the remaining dictionary consists of exactly all other 55 parent equations, and that the guard dictionary retains exactly all fourteen parent guards. Composing the proven polynomial identities with this acyclic rational evaluation map preserves them on the domain where the denominators are nonzero.

### What is and is not a checked identity

The checked result is an **exact rational circuit system**: evaluate the three definitions in order, then evaluate every stored residual polynomial and every guard at the reconstructed coordinates.

The review does **not** claim that all 55 composed residuals were expanded into twelve-variable polynomials. It does not assert equality to any additional unprovided simplified twelve-variable equations, nor a term count, factorization, cancellation, or independence result for such a system. The compact source identities and denominator identities were checked symbolically; the residual composition semantics are exact by construction and were verified by complete reference/dependency accounting.

This establishes a bijective correspondence between the guarded fifteen-coordinate checkpoint and the guarded circuit solutions: projection gives the twelve free coordinates, and the unique three certified linear solves give the inverse. The separately checked x91 reconstruction similarly connects to the accepted guarded sixteen-coordinate checkpoint.

## Original guards and irreducibility

The six starting guard polynomials are exactly the accepted final-coordinate numerators for mandatory edges 98, 96, 89, 95, 46, and 48. Their proofs were verified without invoking a factorization routine:

- g98, g96, and g95 are linear in the selected coordinate with nonzero field-unit leading coefficient.
- g89 and g46 are linear in x25. In each case, the certificate's exact identity `b = a*q + c` has nonzero field constant c. Therefore their two coefficients are coprime.
- g48 is linear in x11. Its leading coefficient is exactly `zeta*x34*x41*(x83-zeta^7)`. The checker verifies all three distinct monic linear factors, the complete leading-coefficient product, and a nonzero remainder of the constant coefficient modulo each factor.

Each polynomial is primitive and degree one over the fraction field of the remaining polynomial coordinates. Gauss's lemma establishes irreducibility over Q(zeta) in the full sixteen-coordinate polynomial ring.

## Exact compressed certificates for 826 negative tests

Instead of large symbolic remainder expansions, the independent checker produced **exact finite-field nondivisibility witnesses**, recorded in `NONDIVISIBILITY_WITNESSES.json`. There are 59 initial equations times fourteen allowed factors: eight mandatory coordinates and six original irreducible guards.

All 826 pairs are witnessed using only fifteen points over F_1013, with `zeta -> 114`. The checker verifies that 1013 is prime, that 114 is a nontrivial eleventh root satisfying Phi_11, that every relevant coefficient denominator is invertible modulo 1013, and that each divisor's lexicographic leading coefficient has nonzero residue. At the recorded point, the divisor evaluates to zero and the equation evaluates to the recorded nonzero residue. The second g95 point is needed for some pairs; there is no random acceptance criterion.

Why this proves a characteristic-zero statement: work in the coefficient ring localized at the chosen residue place. All coefficients of the dividend and divisor lie in this ring. The divisor's leading coefficient is a unit there. If the divisor divided the dividend over Q(zeta), single-divisor polynomial long division would produce the quotient within this localized ring, since every division is by that unit. Reducing the identity modulo the residue place would force the dividend to vanish at every zero of the divisor. The recorded nonzero value contradicts that implication. Thus each witness proves genuine nondivisibility over Q(zeta), not merely a heuristic failed modular factorization.

`verify_negative_witnesses.py` is a separate, small, freshly authored verifier that uses only integer modular arithmetic and the frozen certificate data. It rechecks the saved witness file, all fifteen points, all 826 distinct pairs, all field-denominator conditions, and the leading-coefficient unit condition. It also passes.

Together with the six irreducibility proofs, these negative tests exhaust direct cancellation by factors justified solely by the initial fourteen guards. They do not establish saturation, radicality, or the absence of further consequences from the equations.

## Simplified x39/x91 formulas and the domain nuance

The checker independently establishes

`T = zeta - zeta^9*x41 + x11*x41*(x34+x49)`,

`A = (zeta^9-zeta^4)/(zeta-1)`,

`U = A*T - 1`,

`x39 = U/T`,

`x91 = -U/(zeta^7-zeta^6)`.

It checks the explicit coefficient formulas, the nonzero field denominators, the exact cross-multiplied x39 identity, and the x91 identity both before and after composition. The parent normalized x91 guard is exactly `-T`, so the cancellation by T is authorized.

An important distinction is retained: the **normalized** x91 exclusion supplies `T != 0`, while the **original reconstructed coordinate** x91 is nonzero because the retained x39 exclusion is equivalent to `U != 0` on that domain. One cannot discard the x39 exclusion after writing the simplified formulas. All fourteen constraints remain in force, including the other original reconstruction guards.

## Boundaries and unverified operational claims

- No candidate factorization or contradiction is delivered.
- A future candidate must satisfy every guard, reconstruct through the accepted certificates, and satisfy all original 121 entry equations.
- No expanded twelve-variable residual checkpoint, exhaustive further circuit-pivot search, saturation calculation, Groebner computation, or algebraic-independence claim was reviewed or inferred.
- The author's stated failed expansion attempts and their particular resource-limit counts are operational logs. This review intentionally did not rerun the expensive failed searches. They are unnecessary for the accepted identities or circuit equivalence. The author does not claim an exhaustive new compact-level pivot search.
- The first development run of the fresh checker assumed the solved source was omitted from the equation-transform list. The actual certificate includes its verified zero transform. That reviewer schema assumption was corrected; the development failure files are preserved and are not a mathematical defect in the certificate. The completed run passes every check.

## Artifacts and replay

- `RECEIPT.json`: independent verdict, claims, scope, source hashes, and checker hash.
- `EVENT_REPLAY.json`: all 38 expanded-stage events.
- `CIRCUIT_REPLAY.json`: exact compact definitions, all residual and guard references, and identity scope.
- `NONDIVISIBILITY_WITNESSES.json` and `.json.gz`: complete exact negative certificates.
- `check_independent.py`, `check.log`: complete fresh exact checker and passing log.
- `verify_negative_witnesses.py`, `witness_check.log`: standalone saved-witness verification and passing log.
- `CHECKER_DEVELOPMENT_FAILURE.json`, `CHECKER_DEVELOPMENT_check.log`: preserved development-run record.
- `SHA256SUMS.txt`, `REVIEW_ENTRY.json`: frozen review artifact hashes and entry point.

Run from the workspace root:

```sh
python research_cycle_1819/guarded_reduction_review/check_independent.py
python research_cycle_1819/guarded_reduction_review/verify_negative_witnesses.py
```

The main verifier writes a newly timed receipt and replay files, so a rerun changes the receipt's runtime and hash; the mathematical input hashes remain pinned. `SHA256SUMS.txt` describes the delivered run.
