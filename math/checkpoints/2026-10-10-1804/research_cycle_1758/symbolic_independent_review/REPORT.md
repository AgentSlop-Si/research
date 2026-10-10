# Independent symbolic-reduction audit

## Verdict

**PASS for the stated necessary-reduction claim.** The frozen reduction was replayed with a freshly authored checker and an independent exact implementation of Q(ζ₁₁). The resulting system is exactly the supplied 16-variable, 59-equation checkpoint. No division by an optional-zero edge was found. No nonzero constant contradiction or Fourier factorization was found or claimed.

The bare final polynomial equations are not certified as equivalent to the original factorization problem. Reconstruction must retain the nonvanishing guards described below. Some guards may be algebraically redundant; this review does not claim they form a minimal independent set or prove that any spurious component actually exists.

## What was independently checked

- Every listed input, source, report, and accepted prerequisite hash matched; both gzip files decompress to their corresponding dense certificate hashes.
- The 99-edge topology was read only as data. All 121 entries of CBA were rebuilt from endpoint-compatible paths, with target F[i,j] = ζ^(ij).
- All 3,025 two-by-two determinants were expanded directly from the rebuilt entries, including cancellation of intersecting-path terms. This recovered exactly 22 unique entries and four single-monomial minors, proving the supplied set of 63 mandatory nonzero edges.
- The 21 selected gauges lie on distinct internal diagonal coordinates: A → D₁A, B → D₂BD₁⁻¹, C → CD₂⁻¹. Each normalized edge is already mandatory. One internal gauge remains unfixed.
- All 21 gauge records and 26 Laurent monomial substitutions were replayed. Every binomial source was checked, its chosen exponent difference was ±1, and its recorded replacement annihilated the source exactly. The complete 97-equation / 52-variable intermediate system matched.
- All 36 linear pivot sources and replacements matched the current equations exactly. Every pivot denominator and Laurent normalization used only a nonzero field constant and mandatory-edge monomials.
- The complete 30-step checkpoint matched, including all 66 equations in 22 variables.
- The final generator performs another safe monomial normalization before its unsuccessful next-pivot attempt. Replaying that normalization, without committing another substitution, reproduced every final equation exactly.
- The authoritative final checkpoint has 16 variables, 59 nonzero polynomial equations, 30,694 terms total, and at most 6,271 terms in one equation.

The checker never executes or imports any inherited research or review program. It uses a restricted AST parser for coefficient expressions; canonical integer vectors with a common denominator for Q[ζ]/(1+ζ+…+ζ¹⁰); sparse edge monomials; and streamed top-level JSON items. The large certificate was processed as data without emitting its contents into the review conversation.

## Reconstruction guards

Use x₀,…,x₉₈ for the original edge coordinates.

The final active variables are:

0, 11, 22, 25, 34, 39, 41, 44, 49, 52, 55, 65, 83, 88, 91, 92.

Eight surviving coordinates are mandatory and must remain nonzero:

**39, 41, 44, 52, 83, 88, 91, 92.**

The linear phase eliminated eight further mandatory coordinates:

35, 61, 98, 96, 89, 95, 46, 48.

- Edges 35 and 61 reconstruct to explicitly verified nonzero constants; their nonvanishing is automatic.
- Edges **98, 96, 89, 95, 46, 48** yield six nonconstant guards that must be retained or checked.
- `RECONSTRUCTION_GUARDS.json` stores the exact recorded replacement expressions and reverse evaluation order.
- `FINAL_COORDINATE_GUARDS.json` expresses the six guards as polynomials entirely in the final 16 coordinates. Their term counts are respectively **2, 2, 10, 2, 10, 6**. Coefficients are exact rational vectors in the basis 1,ζ,…,ζ⁹.
- Converting these expressions to polynomial guards clears/cancels only nonzero surviving mandatory monomials and nonzero field constants. Edge 96 also uses the already-required edge-95 numerator as a rational denominator.

Two particularly small guards are, up to nonzero field scaling:

- x₉₁ − ζ⁴ ≠ 0, since x₉₅ = ζ − ζ⁵/x₉₁.
- ζ²x₃₉ + (ζ⁸−ζ⁷)x₉₁ ≠ 0, since x₉₈ is this numerator divided by x₃₉x₄₁.

Reconstruction is triangular: first process the 36 linear replacements in reverse, then the 47 Laurent/gauge records in reverse. Every dependency is available at the time it is needed, and all 99 original edge coordinates are recovered. Check the mandatory replacement guards as they are reconstructed. A proposed point of the bare final system is not a factorization certificate; it must satisfy the guards, reconstruct successfully, and be checked against the original 121 entry equations.

## Safe factor-cancellation next step

1. Retain the eight surviving-coordinate exclusions and six final-coordinate guard polynomials explicitly.
2. Factor the final equations exactly over Q(ζ₁₁), or test divisibility directly by the small certified guards and their exact factors.
3. A factor may be cancelled from an equation only when it is a nonzero field constant, a product of surviving mandatory coordinates, or is proved nonzero by one of the retained guards. If a guard factors, each of its factors is nonzero on every original solution.
4. Record exact product identities for each cancellation. Such cancellation strengthens the necessary relaxation toward the original guarded domain; it need not preserve all solutions of the *bare* relaxed polynomial system.
5. Keep optional-zero cases unless an independent argument excludes them. None of the eight optional final coordinates may be divided merely for convenience.

An alternative is to adjoin an inverse variable for the product of the surviving coordinates and guard numerators, or to use the corresponding saturation. This is a proposed next computation, not a completed contradiction, factorization, or unrestricted no-go result.

## Artifacts and reproduction

- `RECEIPT.json`: machine-readable verdict, full source hashes, counts, pivots, and canonical equation hashes.
- `check_symbolic_reduction.py`: fresh independent checker.
- `check.log`: complete successful replay log.
- `NORMALIZATION_LEDGER.json`: every safe monomial shift used during linear replay.
- `RECONSTRUCTION_GUARDS.json`: exact stage-coordinate guard expressions.
- `FINAL_COORDINATE_GUARDS.json`: final-coordinate polynomial guards.
- `SHA256SUMS.txt`: hashes binding these review artifacts.

Reproduce from the shared workspace root with:

    python research_cycle_1758/symbolic_independent_review/check_symbolic_reduction.py

All frozen inputs were preserved. Only this review directory was written.
