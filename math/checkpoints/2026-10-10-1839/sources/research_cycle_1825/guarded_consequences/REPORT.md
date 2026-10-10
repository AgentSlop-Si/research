# Three equation-forced pivots in the guarded Fourier circuit

## Result and status

**AUTHOR-PENDING: fresh author-side exact replay passes; independent review pending.**

The accepted 12-coordinate, 55-equation necessary circuit system has a further guard-preserving, bijective rational reduction to **9 free coordinates and 52 residual equations**. All **14 original nonvanishing guards** remain; three additional, explicitly derived denominator guards are recorded, for **17 displayed guards**. Guard count is a record count, not an independence assertion.

Free coordinates:

`x0, x11, x25, x34, x41, x49, x65, x83, x92`.

Newly reconstructed coordinates are `x22, x88, x52`. Together with the accepted definitions, the reconstruction order is:

`22, 88, 52, 39, 44, 55`, followed by the accepted reconstruction of `x91`.

This is exact equivalence to the accepted **guarded necessary system**, not a proof that its solutions reconstruct an original Fourier factorization. No feasible assignment or contradiction is claimed, and no unrestricted Fourier impossibility follows. Every eventual candidate still requires prior reverse reconstruction and all original 121 entry equations.

## Accepted inputs

The prior reduction was independently replayed in:

- `research_cycle_1819/guarded_reduction_review/RECEIPT.json`
- SHA-256 `51f6adcf4c160cc5b83ae44d99f77544067f91ec915db1fcc234ae83d4f48c39`

The new certificate fixes exact hashes for that receipt and the parent `CERTIFICATE.json` and `COMPACT_BRANCH.json`. Earlier programs were read neither as executable modules nor run. Only their frozen JSON data is consumed.

Work takes place over the field K = Q(ζ), where Φ11(ζ) = 0. In particular, ζ and all its powers are nonzero.

## The forcing lemma and zero branches

Suppose a retained equation has the form

`E = v D − N = 0`,

where D and N do not involve v, and N is already nonzero on the retained guarded domain. Then D cannot vanish: the D = 0 branch would force N = 0, a contradiction. Thus every guarded solution has the unique value `v = N/D`.

Conversely, adjoining the guard D ≠ 0 and setting v = N/D makes E vanish identically. Keeping every other equation and guard evaluated at that value gives a bijection with the original guarded solution set. The new denominator guard is a logical consequence on the original variety, not a fresh restriction that excludes any solution.

The previous direct guard-product scan tested whether a coefficient was a product of existing guards. This continuation instead uses nonzero numerators forced by equations. It does not assert that the previous scan was exhaustive over this wider class of deductions.

## Three exact pivots

The equation identifiers below are the unchanged identifiers from the parent necessary system. Entry labels refer to the original matrix positions from which those residual equations arose.

### 1. Equation 58, entry (10,10): x22

The exact stored equation is

`E58 = x22 (x34 + x49) − ζ`.

Set `D22 = x34 + x49`. Since ζ ≠ 0, both D22 and x22 are nonzero at every solution. Therefore

`x22 = ζ / D22`.

This also proves an additional fixed-support consequence: the coordinate x22 cannot vanish, even though it was not one of the eight mandatory coordinate guards in the accepted starting checkpoint. The entire branch x34 + x49 = 0 is impossible for this necessary system.

### 2. Equation 36, entry (6,3): x88

Set `a = x11*x34` and `w = x0*x65`. Define the seven-term polynomial, written in grouped form,

`D88 = −ζ^7 + x41 [ζ − ζ^10 + a(ζ^7 − ζ^9 + (ζ^2−1)x83) + w(ζ^10 + a(x83−ζ^7))]`.

The exact stored equation is

`E36 = x88 D88 + ζ^10`.

Thus D88 ≠ 0 is forced, and

`x88 = −ζ^10 / D88`.

The old x88 ≠ 0 guard remains explicitly retained, even though the displayed formula also proves it.

### 3. Equation 4, entry (1,0): x52

Using the previously reconstructed x88, define the thirteen-term polynomial

`D52 = −x83 + w(−ζ^7 + ζ^6*x83)`

`      + x0*x49 [ζ^3 + (ζ^5−ζ^2)x83 + x25(−ζ^2+ζ*x83)`

`                   + (−ζ^8+ζ^7*x83)x88(1−x92−w)]`.

The exact stored equation is

`E4 = x52 D52 + ζ^4*x83`.

The original guard x83 ≠ 0 implies ζ^4*x83 ≠ 0. Hence D52 ≠ 0 is forced, and

`x52 = −ζ^4*x83 / D52`.

The old x52 ≠ 0 guard also remains explicitly retained.

## Circuit endpoint and equivalence

The three new sources, equations 58, 36, and 4, are removed because their solve identities are exact. The other 52 equations remain unchanged as references to frozen parent-stage polynomials, evaluated after the reconstruction circuit. The fourteen original guards are retained as the same references. Guards D22, D88, and D52 are added explicitly.

The three accepted definitions for x39, x44, and x55 remain unchanged. Their source identities and exact nonzero guard-product certificates are replayed again. Every denominator and numerator uses only free coordinates or earlier reconstructed coordinates. In particular, D52 can use x88 because x88 was reconstructed earlier; the inherited x44/x55 definitions can use x88 and x39 because both are available when needed.

Two directions establish equivalence:

1. Starting from any point of the accepted guarded 12-coordinate necessary system, equations E58, E36, and E4 prove all three new denominators nonzero and determine the three newly removed coordinates uniquely. The point therefore supplies a point of the nine-coordinate circuit domain.
2. Starting from a point of the nine-coordinate circuit satisfying all 52 residual equations and 17 guards, reconstruction makes E58, E36, and E4 vanish by their checked identities. The other 52 equations and all fourteen old guards are exactly the accepted necessary system's remaining conditions. This gives its unique corresponding point.

This is a statement about a rational evaluation circuit. No fully expanded nine-variable polynomial system, residual independence, or radical/ideal computation is claimed.

## Verification and bounds

`check_consequence.py` is freshly authored, standalone, and does not import the generator or any inherited program. It uses Python rational arithmetic, ordinary coefficient convolution, and descending reduction by Φ11. It verifies:

- Frozen source hashes and the accepted review chain
- The three new exact solve identities
- Their nonzero numerator identities, including the x83 guard for x52
- The grouped D22/D88/D52 formulas above
- All three inherited compact solve identities and nonzero guard-product identities
- The complete acyclic reconstruction order
- Exact preservation of the 52 residual references and all fourteen original guards
- Explicit inclusion of all three new denominator guards
- Every stored equation/guard is evaluable using available coordinates

Work is capped at 1,000,000 sparse term pairs per multiplication and 50,000 output terms. No parent residual is expanded under the rational substitutions. No Gröbner-basis search, numerical feasibility claim, or probabilistic symbolic proof is used.

Seven deliberate corruptions are independently submitted to the new checker as negative controls: altered numerator, omitted original guard, omitted derived guard, wrong source, zero field unit, missing dependency, and missing residual equation. Every corruption must be rejected. These are author-side robustness controls, not an independent review.

## Files and replay

- `CONSEQUENCE_CERTIFICATE.json`: exact rational circuit and new sparse polynomials
- `check_consequence.py`, `CHECK_RECEIPT.json`, `check.log`: standalone exact author-side replay
- `check_mutations.py`, `MUTATION_RECEIPT.json`, `mutations.log`: seven rejection controls
- `build_consequence.py`: fresh JSON-only construction script
- `REVIEW_ENTRY.json`, `SHA256SUMS.txt`: review entry and hashes

From the shared workspace root:

    python research_cycle_1825/guarded_consequences/check_consequence.py
    python research_cycle_1825/guarded_consequences/check_mutations.py

The checker requires the frozen parent data named in the certificate; the new package does not duplicate the approximately 29 MB parent polynomial store. A passing author receipt is not a substitute for independent mathematical replay.
