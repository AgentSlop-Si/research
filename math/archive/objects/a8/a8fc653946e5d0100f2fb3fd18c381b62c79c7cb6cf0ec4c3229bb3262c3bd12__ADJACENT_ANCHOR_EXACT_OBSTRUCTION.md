# Exact obstruction for the exported adjacent-anchor chart

## Result

**The entire exported guarded 12-variable, 40-equation adjacent-anchor chart is empty over every characteristic-zero field containing a primitive eighth root of unity.** No exact Fourier-8 factorization is claimed.

A slightly stronger, precisely bounded statement is proved. For the same adjacent anchor and the same fixed support pair, the necessary off-support equations cannot hold if just

\[
u_0\ne0,\qquad B_1B_5B_6\ne0,\qquad B_j=(UM)_{0j}.
\]

Equivalently, every surviving solution of the necessary equations must lie on the boundary `u0*B1*B5*B6=0`. Other edge variables and all four anchor ratios may even be zero in this algebraic statement. In the exported chart, these four assumptions are already among the guards: `u0`, `a_1`, `a_5`, and `a_6`.

This **does not reject the whole adjacent-anchor diagonal orbit** without the pivot assumptions. It does not cover `u0=0` or any of `B1=0`, `B5=0`, `B6=0`. It does not cover other support orders, a free first layer, arbitrary endpoint permutations, or general two-layer Fourier-8 kernels. It supplies no growing-size complexity lower bound.

## Exact setup

Let `z` be abstract with `z^4+1=0`; all calculations take place in

\[
K=\mathbb Q[z]/(z^4+1).
\]

No numerical embedding of `z` is used by the independent verifier. Write

- `pi(j)=j+1 (mod 8)`;
- `sigma=[2,7,5,0,6,1,3,4]` as an image list;
- `M=F8 T K_adj`, with
  `M[r,2a]=z^(2ar)+t_a z^((2a+1)r)` and
  `M[r,2a+1]=z^(2ar)-t_a z^((2a+1)r)`;
- `U=I+diag(u)P_pi`, and `w=u0`.

The adjacent anchor uses pairs `(0,1),(2,3),(4,5),(6,7)`. The second support order remains `[0,2,5,1,7,4,6,3]`; the first is `[0,1,2,3,4,5,6,7]`.

For the five columns `J={1,2,4,5,6}`, the exported pivot is row 0. Put

\[
B_j=M_{0j}+wM_{7j}.
\]

For an off-support row `r` (outside `{j,pi(j),sigma(j)}`), define

\[
\begin{aligned}
b_{rj}&=B_{\sigma(j)}M_{rj}-B_jM_{r,\sigma(j)},\\
c_{rj}&=B_{\sigma(j)}M_{r-1,j}-B_jM_{r-1,\sigma(j)}.
\end{aligned}
\]

Here `r` ranges from 1 through 7, so no wrap convention is needed in `r-1`. The original necessary minor is exactly

\[
h_{rj}=b_{rj}+u_rc_{rj}.
\]

Thus two necessary minors in one row imply the exact resultant identity

\[
R_{r;j,k}=b_{rj}c_{rk}-b_{rk}c_{rj}
=c_{rk}h_{rj}-c_{rj}h_{rk}=0.
\]

There is **no division by `c_rj` or by a coefficient used to solve for a row variable**. In particular, no hidden linear-equation pivot exception is being discarded.

## Twenty generators and the only cancellations

Use every column pair among the following eligible columns for each row:

| Row | Eligible columns from J |
|---|---|
| 1 | 2, 4, 6 |
| 2 | 4, 5, 6 |
| 3 | 1, 4, 5 |
| 4 | 1, 2, 5, 6 |
| 5 | 1, 6 |
| 6 | 1, 2 |
| 7 | 2, 4, 5 |

This gives 20 resultants. Each is a nonzero cyclotomic scalar times an exported generator `f_i` times the following explicitly canceled factors:

- `w` for every row-1 resultant;
- `B6` for column pair `(4,6)`;
- `B1` for column pair `(1,5)`;
- `B5` for column pair `(2,5)`;
- no further polynomial factors.

When two rules apply, both factors occur. The standard-library verifier reconstructs all 20 resultants directly from `M`, and checks every full factorization identity, including its exact nonzero scalar. The scalar coefficient vectors are recorded in `VERIFICATION_REPORT.json`.

Therefore, if the 40-equation interface has a guarded solution, every `f_i` vanishes.

## Exact unit-ideal certificate

`EXACT_UNIT_CERTIFICATE.json` is a proof DAG in five variables

\[
(t_0,t_1,t_2,t_3,w).
\]

It contains the 20 initial generators and the retained intermediate polynomial identities needed to derive the constant 1. Every later node is an explicit polynomial linear combination of earlier nodes, over the exact field `K`. The independent verifier evaluates all these combinations and checks that the final polynomial is exactly `1`.

The verified certificate retains **57 nodes and 575 combination terms**. This is a finite algebraic contradiction: an evaluation sending all generators to zero would also send the certified constant 1 to zero.

The discovery computation used exact symbolic algebra and a newly authored Buchberger-style proof recorder. The final check requires **only Python's standard library**, including rational arithmetic and a separate 4-by-4 exact coefficient inversion routine. It does not invoke a Gröbner-basis oracle, trust a solver's status, or execute/import a predecessor program.

A six-resultant subset was also found to have unit ideal in a modular probe. The final characteristic-zero certificate uses all 20 generators. No six-generator characteristic-zero claim is needed for the theorem.

## Denominators, embeddings, scales, endpoints, and zero edges

- The theorem is stated in **characteristic zero**. Rational denominators and cyclotomic scalar divisions are explicitly represented and checked in the certificate. No positive-characteristic extrapolation is made from it.
- Because verification is in the abstract cyclotomic field, the proof holds under every embedding of `Q(zeta8)` into a characteristic-zero extension. It is not tied to one approximate complex root.
- The only canceled variable/pivot factors are `w`, `B1`, `B5`, `B6`, all guarded nonzero in the supplied interface. There is no assumption on an unlisted resultant coefficient.
- The remaining endpoint-scale guards, `1-product(u)`, and `product(c)-product(a)` are **not used**. The contradiction arises before scale restoration and invertibility checks. Hence failure cannot be repaired by changing the recovered endpoint scales inside this chart.
- In particular, there is no candidate to reconstruct as `Q0=diag(1/x)U` and `Q1=V diag(1/y)`, and no omission of the required actual-second-factor scaling `2Q0,2Q1` can affect the contradiction.
- The theorem permits zeros in the other seven row-edge variables. It requires `u0!=0`; the boundary `u0=0` remains unresolved here. All first-anchor connecting weights may still be the legal sparse zeros described in the predecessor proof.
- Full-edge second factors can also lie on a zero-pivot boundary, so even requiring every edge nonzero does not turn this result into a whole adjacent-diagonal-orbit obstruction.

## Verification and independent controls

Run from any working directory:

    python3 adjacent_anchor_construction_0304/verify_exact_certificate.py
    python3 adjacent_anchor_construction_0304/verify_positive_controls.py

The first program:

1. Independently regenerates all 20 Fourier row-resultant identities.
2. Checks the entire exact certificate and its final constant 1.
3. Checks field/polynomial arithmetic positive controls and a perturbed-final negative control.
4. Independently regenerates and compares **all 88 coefficient polynomials** of the supplied interface, including all 40 zero equations; it also checks that every minor used is one of those zero equations.

The second program manufactures four separate **non-Fourier** exact paired-Green sums with all branch edges nonzero. For each, it verifies the 40 equations, column directions, scale restoration, and dense inverse-sum matrix identity, and rejects an entry-perturbed control. These are controls, not Fourier solutions.

The builder generated 79 intermediate nodes and retained 57, in approximately 50 seconds in this environment. Certificate verification uses large exact rational coefficients; coefficient solving and verification are not claimed to be free or uniformly constant-bit-cost. The certificate JSON is about 11 MB.

## Supplemental finite-field exploration

An independent exhaustive scan found no guarded solution over `F17` with `z=2` or over `F41` with `z=3`. The scan tested respectively `16^5=1,048,576` and `40^5=102,400,000` assignments of the four nonzero anchor ratios and `u0`; the other row variables were forced by exact linear equations. All candidates died by row 3, before scale restoration. These calculations are supplemental field-specific checks and are not used to infer the characteristic-zero theorem.

No numerical root-finding was used in this continuation. Earlier numerical probes and failed or interrupted symbolic probes are not proof evidence.

## Preservation and artifacts

Predecessor files were read as text/JSON only. Their programs were neither executed nor imported. `SOURCE_SHA256SUMS_BEFORE.txt` and `SOURCE_SHA256SUMS_AFTER.txt` agree.

The ZIP package includes the exact supplied interface JSON as read-only audit data, so its standard-library checker is self-contained after extraction. Run `python3 verify_exact_certificate.py` there. No predecessor executable is included.

Primary deliverables:

- `ADJACENT_ANCHOR_EXACT_OBSTRUCTION.md`: this proof, scope, guards, and limitations.
- `EXACT_UNIT_CERTIFICATE.json`: exact portable algebraic certificate.
- `verify_exact_certificate.py`: independent standard-library checker.
- `VERIFICATION_REPORT.json`, `verification.log`: exact verification record.
- `verify_positive_controls.py`, `POSITIVE_CONTROLS.json`: manufactured exact controls.
- `build_full_certificate.py`, `all_row_resultants.json`, `resultants_all.py`: optional discovery/reproduction artifacts; they require SymPy.
- `PACKAGE_SHA256SUMS.txt`: package manifest.

The other scripts and logs are exploratory records; their non-results are not theorem statements. The uncompleted six-generator characteristic-zero probe and the unsaturated first-three-rows probe were stopped once the full exact certificate was established.
