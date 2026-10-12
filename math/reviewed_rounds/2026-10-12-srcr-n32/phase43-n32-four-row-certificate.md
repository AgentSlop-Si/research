Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, source identity and limitations are retained. Original source-report SHA-256: 268eceaf82ff766a85b5fdcd240ad662dfa3698b037127d9f3dcd2282e93c54b.

# PHASE43 N32 independent review: bounded ACCEPT

Date: 2026-10-12 UTC. Reviewer: a separate reviewer from the candidate author.
Gate: PHASE43::N32-certificate.

## Verdict

ACCEPT the source-pinned, fixed-slice, four-row existence certificate, and ACCEPT the full-DFT outer-monomial exclusion throughout the same componentwise box. This closes the bounded saved-N32 certificate gate only. It is not a full transform construction, a global two-stage obstruction, or an original unit-D-model solution.

The candidate archive has SHA256 e1fb5f77cd06f30aa4594b2a24989e93fc6fe47db86ef170ce582950fcbcfdd5. All 65 manifest-listed files and all 66 archive members, including the manifest, were verified against the untouched source directory. All 39 inert original-source member copies were independently compared byte-for-byte with the original Phase43 Green archive. The original archive, report and earlier review match their pinned SHA256 values. The source center hash is 4f3abfe82126ba7742352478b237f134df5494c5557e4b9f45b1262ee6661fe7.

No original source executable was run or imported. No center fitting, Newton center replacement, phase reduction, or change of frozen values was performed. The intact candidate ZIP is embedded in this review packet; the original failed-box records remain available there. Replays were confined to a labeled extraction.

## Independent numerical verification

1. A fresh extraction passed the author manifest verifier before replay. The author interval checker, at 60 digits, reproduced q = 0.09659777815371481 and normalized self-map = 0.5253564195051077. Exact dyadic/rational comparisons prove q < 1/10 and self-map < 53/100.
2. A separately authored checker, `independent_path_checker.py`, uses 70-digit outward intervals and an independent entrywise directed-path derivative. It imports no candidate program and uses no numerical linear algebra library or optimizer. It independently proves q < 0.104 (display value 0.10349495449521169) and normalized self-map < 0.529 (display value 0.5289679494270313).
3. These independent enclosures are slightly wider than the author's rank-one resolvent derivative enclosures. The independent q bound does not itself establish q < 0.1; that tighter figure is supported by the cold-replayed, mathematically audited author computation. Both methods establish the same existence and uniqueness claim, and both prove self-map < 0.53.
4. All 192 saved decimal tokens, the ordered 186-variable selection, the exact radius list, and the six frozen coordinates 80, 89, 104, 107, 109, 123 are checked. Radii range exactly from 2.1e-12 through 4.28e-11. Frozen coordinates do not receive interval radii.
5. The graph orders are independently regenerated from the source's fixed seeds. A separate union-find forest calculation reconstructs chord edges 31 through 95 in each layer. Every recorded physical source-to-target edge is checked.

All printed floating-point numbers above are diagnostics. Exact interval endpoints and comparison results are in the JSON records.

## Model and derivative conventions

There are two stages, each summing exactly three branches with coefficient 1. Every directed edge gain is exp(i theta), with the tree-edge angles zero. Thus all gains have modulus exactly 1. For the source convention, edge j runs from c[j-1] to c[j], including the wrapping edge j=0. The original `Edge` declaration was checked: its fields are cycle, target, source, weight, explaining the source constructor argument order.

The model is M = S2 D S1, with D[0]=1 and D[k]=exp(x[160+k] + i x[129+k]) for 1<=k<=31. This is the expanded admissible model allowing nonzero complex interstage entries. The certificate proves existence of a D within the stated box, not existence for every independently prescribed D. |D[1]| > 2.53 throughout the box, so this cannot be transferred to a unit-modulus relative diagonal or to the original unit-D product model.

For a branch let z=exp(i sum theta), and let P(b,a) be the directed path from b to a of length less than 32. Then

G[a,b] = exp(i sum over P(b,a) theta)/(1-z).

This follows from W^32=z I and the finite geometric-series inverse. For edge k, direct differentiation gives

dG[a,b]/dtheta_k = i G[a,b] (1_{k in P(b,a)} + z/(1-z)).

The independent checker uses that formula entrywise, then ordinary matrix products to propagate through S2 D S1. The author checker uses dG=G(dW)G and the corresponding rank-one propagation. They are the same exact derivative. Separate finite-field controls verify the inverse identity and equality of both derivative formulas in all six actual branch orders at two primes, totaling 393,216 exact entry-derivative comparisons. A reversed source/target derivative fails the controls.

The target is exp(-2 pi i rj/32). Equations are Q[r,j]=M[r,j]M[0,0]-target[r,j]M[0,j]M[r,0] for r=1,2,3 and j=1,...,31. The 93 real parts precede the 93 imaginary parts, in row-major order. All selected columns of the real Jacobian use that same order. A positive-sign target control has a rigorously nonzero equation over the full box.

## Analytic proof and guards

Let h be the exact radius vector, H=diag(h), B the fixed exact-decimal preconditioner, and x0 the exact saved center in the selected coordinate slice. With T(x)=x-BQ(x), both interval computations verify every row of

sum_j sup |(I-B DQ(x))_ij| h_j/h_i < 1

and the corresponding self-map bound

sup |(BQ(x0))_i|/h_i + sum_j sup |(I-B DQ(x))_ij| h_j/h_i < 1.

The box is closed and convex in 186 real dimensions. The mean-value inequality in the H-weighted infinity norm proves strict contraction and strict self-mapping. Banach's theorem supplies a unique fixed point. At any point in the box, the norm bound implies B DQ is invertible by the Neumann-series criterion. Since B is square, B is invertible; therefore every fixed point satisfies Q=0. Uniqueness is on this fixed-frozen-coordinate slice, not in all 192 coordinates.

The interval boxes contain the exact decimal centers and radii; decimal parsing and every operation are outward enclosed. The model is smooth on a neighborhood of the box because the guards hold strictly. All six |1-z| > 2/5; all first-row chart entries have modulus > 8/5; all first-column chart entries have modulus > 16/5; every one of the 1,024 matrix entries is nonzero. Interstage exponentials and edge gains are nonzero by both parameterization and interval evaluation. Division is only performed after its relevant guard; the author uses no hidden log-Jacobian division in this certificate.

At the exact root, input scaling b_j=1/M[0,j] and output scaling a_r=M[0,0]/M[r,0] give (diag(a) M diag(b))[r,j]=exp(-2 pi i rj/32) for exactly rows r=0,1,2,3 and all j. The chart guards make these calibrations invertible. This explicitly chooses the unnormalized DFT convention, including row 0 and column 0 equal to 1. It does not assert literal equality of the uncalibrated physical matrix.

## Full-DFT exclusion and permutations

The independently evaluated same-box modulus of

R = M[4,1] M[0,0] / (M[0,1] M[4,0])

is rigorously inside (0.773632,0.773633); the independent display enclosure is [0.7736321933872579,0.7736328576226579]. In particular it is strictly below 1 everywhere in the box.

Suppose M were obtained from any full Fourier matrix by independent row and column permutations and nonzero row and column diagonal scalings. The four diagonal factors in R cancel. The remaining ratio is a four-entry Fourier cross ratio, of the form omega^((p(4)-p(0))(q(1)-q(0))), whose modulus is 1. This contradicts the strict same-box modulus bound. The argument does not assume that the anchor row/column stay fixed under permutations and does not require enumeration of permutations. It also works for normalized or positive-sign Fourier matrices, though the accepted interpolation target is specifically the negative-sign unnormalized one.

Thus no matrix anywhere in the certified box is outer-monomially equivalent to a full 32-point DFT. In particular, four-row success must not be promoted to full-transform success.

## Earlier attempts and controls

The original ratio-system uniform-radius 1e-12 attempt and the cleared-equation uniform-radius 1e-10 attempt were both cold-replayed and retained. The first has q approximately 0.272838403011 but fails self-mapping. Its exact center correction lower bound exceeds (1+q)r, which rigorously excludes a root in that smaller fixed-slice box. The second has q approximately 2.704634338080; its sufficient contraction test is inconclusive and does not exclude roots.

The exact comparison audit was rerun after both replays. Eight fail-closed proof-data controls reject a repeated selected coordinate, changed frozen index, changed center decimal, reversed cycle, reversed source/target edge, changed chord, zero radius, and malformed preconditioner dimension. These supplement the independent model computation; they do not replace the interval proof.

## Scope and remaining work

The bounded saved-N32 certificate is independently accepted: source-pinned guarded four-row existence in the expanded nonunit complex-interstage model, with same-box full-DFT outer-monomial exclusion. No full-transform or broader-model conclusion follows.

Keep accepted N8/N16 evidence, including corrected N16 radius 5e-13. Preserve the inherited one-layer obstruction's restricted scope, the distinction between submersion and target attainment, and every original-model limitation. No all-length synthesis, FFT speedup, uniform parameter generation, stability or bit-complexity guarantee, or worldwide novelty claim follows. A full DFT would require a genuinely different region/model and an all-row certificate; this box gives a negative answer for that goal.

## Reproduction and archive layout

Python 3.12.14 and mpmath 1.3.0 were used. The following reproduction commands refer to the complete review archive, retained separately from this report-only publication:

- `python independent_path_checker.py`
- `python exact_controls.py`
- In `author_cold/phase43_n32_guarded_0156`, replay `guarded_componentwise.py --radius componentwise --dps 60`, `guarded_interval.py --radius 1e-12 --dps 60`, `guarded_polynomial.py --radius 1e-10 --dps 60`, then `exact_audit.py`.

The candidate's embedded manifest describes its original outputs; output timings in the replay extraction necessarily differ after execution. The untouched embedded original candidate ZIP preserves that original manifest and every original byte. The outer review manifest binds the actual replay extraction, independently authored checker, controls, logs, and review.
