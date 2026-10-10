# Theorem dependencies and proof obligations

Private editorial map • 10 October 2026

## Logical order

1. Integer Gaussian coefficients, reciprocity, q-Lucas, and the formal generating function supply the common starting point.
2. Maximal pole-weight extraction gives the separated local coefficient, Theorem 1. Keeping the next regular degree at the shared root gives the overlap coefficient, Theorem 2.
3. The classical Hermite discriminant and formal simple-root lifting turn those coefficients into the exact ordinary-discriminant expansions. Galois conjugacy and monic integer division give the normalized cyclotomic quotients.
4. The integer cyclotomic bridge, Lemma 3, converts one nonzero reduced quotient into characteristic-zero squarefreeness at order dp. Applied directly to Theorem 1, it yields the separated content criterion.
5. The finite q-binomial half-sum identity gives reciprocal parameters, Lemma 4. Hermite differential equations, or the known hook-Wronskian congruence, give paired-good selection, Lemma 5. Together with Theorem 2 and Lemma 3 these imply the paired-residue criterion, Theorem 6.
6. Theorem 1's local model at the moving nodes −q^j gives the cluster-resultant order. The full integer product factorization, a good lower residue component, cyclotomic ramification, and the integral power basis imply Theorem 7's rational-content valuation. This branch does not use Theorems 2 or 6.
7. Exact fixed-base arrays feed the two sufficient criteria. Individual modular certificates close only their named p|d exceptions. The optional scalar-bank result additionally depends on the separate accepted rank, annihilator, and resonance classification.

## What must appear as proof rather than an assertion

- Local models: a formal coefficientwise pole bound, not an informal analytic limit or a numerical root plot.
- Overlap: why the t^b and t^(b+d) regular coefficients are precisely the only contributors at order A+1; why the explicit τ is defined.
- Discriminant: all n roots accounted for; every cross-cluster factor and sign retained; why the remainder is even.
- Quotient: division in Z[q] before reduction or upper-root specialization; the Q_d normalization included.
- Residue selection: nonzero in a product of fields means at least one component, not a unit in the whole product. For the overlap case, both inverse residual guards are required before one of the two J polynomials is selected.
- Characteristic p: no zero-root exception, no illegal logarithmic derivative, and τ≠1 deduced from the reciprocal relation.
- Valuation: an integral lower bound at every upper prime plus a constructed upper prime with equality; only then take the minimum and floor.
- Finite inputs: full exact arrays and canonical remainders, not only the reported content integers. Do not extrapolate to uncomputed bases.

## Status and priority distinction

The local and arithmetic statements in MANUSCRIPT_OUTLINE.md are supported by the accepted proof and audit files listed in SOURCE_MAP.md. This package performs editorial synthesis and spot-checks of primary-source statements; it does not replace those independent audits or claim a new independent mathematical verification.

The following are established antecedents or standard tools: q-Lucas, classical Hermite limits and discriminants, the quasi-Laguerre ordinary-discriminant formula, the identified hook-Wronskian congruence, cyclotomic polynomial identities, the integral power basis, and cyclotomic ramification. The fixed-root coefficient with its full normalization, its combined arithmetic use, and the reciprocal-pair application remain candidates for a contribution pending the priority gate.

## Minimal manuscript assembly plan

- Opening: state Theorems 1 and 2 together, then two arithmetic consequences without a novelty adjective.
- Main proof section: share the formal expansion machinery and discriminant bookkeeping.
- Arithmetic section: state the quotient bridge once, then separate the paired and valuation branches.
- Attribution remarks: place the quasi-Laguerre and hook-Wronskian reductions beside the corresponding lemmas.
- Examples and supplement: present finite content inputs, exceptional certificates, and hypothesis-failure examples.
- Optional appendix: retain the motivating restricted scalar-bank application only if it helps the intended audience.

No mathematical theorem should depend on a publication-significance judgment or a failed literature search. Completing the older full-text comparisons is required for originality language, not for the validity of the already accepted private proof record.
