# Field descent: arithmetic and prior-art boundary

10 October 2026. Independent supporting analysis. The all-order upper-bound review is separately accepted in `INDEPENDENT_PROOF_REVIEW.md`; this note records the arithmetic and literature boundaries.

## Established constraints before the candidate

Write K=Q(q), with q primitive of odd order N. Enlarging the field can only lower the permitted bank minimum. The accepted characteristic-zero lower bounds therefore imply M_K(7)≥8 and M_K(11)≥6. The accepted universal architecture gives M_K(N)≤2N−2, hence M_K(7)≤12 and M_K(11)≤20. The accepted complex upper bounds 8 and 14 do not themselves replace these base-field bounds.

The exact common-node criterion over an infinite field K requires a monic recurrence polynomial that is squarefree **and split into linear factors over K**. If nodes must be nonzero, its constant coefficient must also be nonzero. Having recurrence coefficients in K, or all moments in K, is insufficient. For four orientations this criterion applies only after decomposing the target into four compatible Gaussian-weighted triangular arrays; individual row decompositions cannot independently change a bank's node.

## A concrete obstruction for the frozen N7 witness

For the manuscript cubic g(t)=t³+s₂t−s₃, reduce the displayed coefficient formulas at the good prime (71,q−48). The denominator 29 is a unit, 48 has order seven, and

gbar(t)=t³+47t+15.

Evaluation at every element of F71 is nonzero, as recorded in the independent JSON certificate. A cubic without roots is irreducible. Since the monic coefficients lie in the local discrete valuation ring, a proper factor over K would have monic coefficients integral in that ring and would reduce to a proper factor. Thus g is irreducible over K.

At the separate good prime (43,q−4), the reduction is t³+21t+21 and its discriminant is 26. Euler's criterion gives 26²¹=−1 mod43. A square unit in K would reduce to a square, so the characteristic-zero discriminant is nonsquare. An irreducible separable cubic with nonsquare discriminant has splitting group S3. Consequently the frozen witness's splitting field has **degree exactly six** over K, sharpening its published upper bound of six.

This is a result about that specified cubic. It does not show M_K(7)>8 and does not exclude a different eight-bank construction.

## A concrete obstruction for the frozen N11 witness

At the accepted good prime (23,q−2), its sextic reduces to

t⁶+4t³+2t²+21t+12
 = (t−7)(t−8)(t⁴+15t³+8t²+20t+15).

The quartic has no root and no monic quadratic divisor over F23, independently enumerated in the fresh control, so it is irreducible. The factors are distinct. If the original monic sextic split over K, integrality at this good prime would force its reduction to split as well. Therefore the frozen sextic is genuinely nonsplit over K. No exact splitting-field degree is asserted here, and no other fourteen-bank construction is excluded.

## Why trace and Galois averaging do not remove the issue

The trace of an algebraic-node bank orbit is a matrix over K; the original count still includes every algebraic-node bank. The trace is not a new legal single bank. Averaging a representation over a Galois group retains extension-field nodes, and expanding the average may multiply the number of extension-field occurrences without producing K-nodes.

The elementary moment sequence (2,0,4,0) over Q illustrates the obstruction: it is the sum of the power sequences at sqrt(2) and −sqrt(2). Any representation with at most two distinct rational nodes would have a monic quadratic annihilator satisfying 4+2c₀=0 and 4c₁=0. Thus the annihilator would have to be t²−2, which does not split over Q. The sum is rational but its two-node representation does not descend.

A nonempty Zariski-open subset of an affine coefficient space over infinite K has K-points, but those points are polynomials with coefficients in K, not necessarily split polynomials. To use openness correctly for base-field bank synthesis, one can parameterize the roots in K first, establish the equations rationally in those coordinates, and then prove all remaining exclusion polynomials are nonzero. This is the candidate author's current approach.

## Directly inspected primary literature

- Bruce Reznick, *On the length of binary forms*, Theorem 2.1, Corollary 2.2 and Theorem 4.10. The author-hosted 24-page version explicitly relates constant-coefficient recurrences to decompositions over K and constructs split Sylvester forms to obtain the general field-dependent upper bound. The proof warns that a complex construction need not split over K. https://reznick.web.illinois.edu/hdfv3.pdf
- Bruce Reznick and Neriman Tokcan, *Binary forms with three different relative ranks*, Theorem 2.1. It requires pairwise distinct linear factors over K in the Sylvester criterion and gives examples whose rank changes with the field. https://arxiv.org/pdf/1608.08560
- Neriman Tokcan, *On the Waring Rank of Binary Forms*, Section 3. It distinguishes the field generated by coefficients from fields needed for decomposition and discusses splitting-field degrees for rank-three forms. https://arxiv.org/pdf/1610.09065
- Pierre Comon, Yang Qi and Konstantin Usevich, *Identifiability of an X-rank decomposition of polynomial maps*, served 26-page version, Sections 2.4 and 4.1–4.3. It identifies simultaneous shared-vector decompositions with scroll geometry and defines secant varieties using closure. Those geometric statements do not supply arithmetic splitting or remove the legal finite-node restriction. https://arxiv.org/pdf/1603.01566

The candidate's split-recurrence mechanism is closely related to classical field-dependent Sylvester/Prony methods. The four-orientation coupling and legal resolvent completion still need their own proof. This bounded comparison does not determine historical priority for the signed-bank theorem and is not an exhaustive literature review.

## Reproducibility

`fresh_field_obstructions.py` is a fresh elementary modular-arithmetic program. It neither imports nor executes any source/author program. `FROZEN_FIELD_OBSTRUCTION_RESULTS.json` contains exhaustive residue evaluations and polynomial-factor checks. The review reads mathematical source notes and inert data only. No external write or publication was performed.
