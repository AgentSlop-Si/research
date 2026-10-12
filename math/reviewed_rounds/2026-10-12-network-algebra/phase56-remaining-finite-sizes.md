Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery details are omitted; mathematical source identity, assumptions, costs and limitations are preserved. Original source-report SHA-256: 5e7c0baeb082d6389de814f1cdc69e236660b77ee88023601045626807e96768.

# Phase56 remaining finite Fourier certificates: independent audit

Date: 2026-10-12 UTC. Original research scripts remained inert.

## Verdict

**ACCEPT SCOPED, separately at N=7, N=11, and N=13.** A newly authored outward-rounded interval checker verifies the saved finite centers and topologies, without optimizer search or executing any uploaded research program. It proves existence of exact full **negative-sign, unnormalized** Fourier matrices in the two-stage unrestricted complex Green-network model. The printed rational centers are isolating approximations, not exact Fourier factorizations.

The prior N5/N8 acceptance remains unchanged. Together these establish five finite examples, not an all-size theorem. The generic-dimension argument and finite-field Jacobian experiments remain outside this audit. No phase-only/unit-edge transfer, optimal term count, useful runtime, uniform conditioning, FFT asymptotic improvement, or novelty is accepted.

## Rigorous quantitative results

Every displayed strict bound below is checked against the exact numerator/denominator stored in the verdict, rather than obtained by rounding a diagnostic float.

| N | Stage terms | Coordinates / active / frozen | Radius r | q upper | eta upper | Strict self-map margin lower |
|---|---|---|---|---|---|---|
| 7 | 3+3 | 40 / 36 / 4 | 1e-70 | 1.287e-9 | 9.230e-100 | 9.999999987e-71 |
| 11 | 5+5 | 108 / 100 / 8 | 1e-70 | 1.040e-9 | 3.807e-99 | 9.999999989e-71 |
| 13 | 6+6 | 154 / 144 / 10 | 1e-85 | 3.214e-5 | 7.347e-124 | 9.9996e-86 |

Here eta bounds ||B f(c)|| infinity, and q bounds ||I-B J(z)|| infinity throughout the complex radius-r polydisc. The rigorous local inverse-Jacobian bounds are respectively <29.574, <343.845, and <9141.363. These are fixed active-slice derivative bounds, not general conditioning or practical stability claims.

Additional outward-rounded strict lower bounds across each entire containing rectangle:

| N | Minimum vertex-gain margin | Holonomy margin | Pole 1-h margin | Actual edge-gain margin | First-row/column M margin | Minimum outer L/R margin |
|---|---|---|---|---|---|---|
| 7 | 0.02082 | 0.4662 | 0.05223 | 0.1674 | 0.3246 | 0.3416 |
| 11 | 0.005861 | 0.1088 | 0.3863 | 0.006728 | 1.6757 | 0.004182 |
| 13 | 0.01565 | 0.0001895 | 0.5929 | 0.0003235 | 1.5839 | 0.01202 |

All term coefficients, middle masks, every M entry, and every individual outer factor are also certified nonzero. The exact per-category endpoint receipts are in results/N*_verdict.json. Full calibrated center entry residual upper bounds are <7.936e-98, <5.866e-98, and <2.452e-124. These center residuals alone are not existence proofs.

## Exact model, parameter reduction, and target map

For a saved permutation o of 0,...,N-1, define pos_o and nonzero complex vertex gains g. The gain at vertex 0 is normalized to 1. Let h be a nonzero complex holonomy, with h != 1, and a a nonzero complex coefficient. The Green entry is

G[i,j] = (g_i/g_j) * (1 if pos_o(i)>=pos_o(j), else h)/(1-h).

Define W[o[k+1],o[k]]=g_o[k+1]/g_o[k], with indices cyclic and an extra h on the closing edge. Thus (I-W)G=I. The equivalent prefix action is

(Gx)_o[k] = g_o[k] * (sum_{j<=k} x_o[j]/g_o[j] + h/(1-h) * sum_j x_o[j]/g_o[j]).

Each stage is S_s=sum_t a_st G_st, and M=S_2 D S_1. In each saved stage the first term has all g=1 and a=1; every other term has g_0=1. The middle diagonal has D_0=1. All other listed direct coordinates are independently complex, including amplitudes.

This explicit chart has T(N+1)-N-1 coordinates at depth 2: each stage contributes q holonomies and (q-1)N remaining gain/coefficient coordinates, then the mask contributes N-1. The checker derives the entire metadata sequence, verifies every cycle, validates every finite-decimal coordinate and every B entry, and selects exactly (N-1)^2 distinct active coordinates in the saved order. All omitted coordinates are fixed at their exact rational centers. No rank/dimension theorem is inferred from this count.

The chart normalization is compatible with exterior diagonal equivalence on the open set where each first coefficient is nonzero. For each stage, A_s=diag(g_s0), and S_s=a_s0 A_s S'_s A_s^-1. Consequently

M=a_10 a_20 A_2 S'_2 (A_2^-1 D A_1) S'_1 A_1^-1.

The exterior A factors and scalar factors can be absorbed into L,R. Divide the middle diagonal by its nonzero zeroth entry, and normalize each relative gain vector at vertex 0. This produces exactly the stated chart. This elementary local chart calculation is not acceptance of the separate all-depth generic-dimension/stabilizer claim.

For all 1<=i,j<N, the equation is

f_ij=M_ij M_00/(M_i0 M_0j)-exp(-2*pi*i*i*j/N)=0.

Throughout the certified rectangle, all M_i0 and M_0j remain nonzero. At the certified root set L_i=1/M_i0 and R_j=M_00/M_0j. Then (L M R)_ij=F_N[i,j] for every i,j. For i=0 or j=0, the calibration expression is identically 1, so no Fourier row or column is omitted. The checker additionally evaluates all N^2 calibrated entries and confirms compatibility with the respective interval target. The exact-root conclusion comes from the contraction argument, not mere interval overlap.

## Derivative and inverse-Jacobian proof

For the coefficient-weighted term H=aG, independently differentiated direct coordinates give

- dH/dh = a (g_i/g_j)/(1-h)^2 for every i,j, independent of the ordering branch;
- dH/da = G;
- dH/dg_v = (delta_iv-delta_jv) H_ij/g_v.

For first-stage coordinates dM=S_2 D dS_1; for second-stage coordinates dM=dS_2 D S_1; and dM/dD_v=S_2[:,v] S_1[v,:]. The implemented quotient derivative is

dY_ij=(dM_ij M_00+M_ij dM_00)/(M_i0 M_0j)-Y_ij(dM_i0/M_i0+dM_0j/M_0j).

This avoids introducing an unnecessary division by M_ij. Every one of the m^2 selected derivative entries is enclosed by 150-decimal-digit mpmath.iv arithmetic on the full rectangle containing the closed complex sup-norm polydisc. This is a fresh direct interval derivative computation, without the uploaded rational A0 or Cauchy-variation proof and without the earlier audit's forward-AD implementation.

Finite-decimal input strings are exact rationals enclosed by outward-rounded intervals. Complex upper magnitudes use |Re|+|Im|. Complex nonzero lower margins use max(distance(Re,0),distance(Im,0)). These are conservative Euclidean-modulus bounds. All interval binary endpoints are converted exactly to Fraction before the proof comparisons. Rounded float diagnostics are explicitly non-authoritative.

With T(z)=z-B f(z), the guards give holomorphicity on a neighborhood of the polydisc. The matrix inequality ||DT(z)||<=q<1 gives contraction, and eta+qr<r gives strict self-mapping. Banach's theorem supplies a unique fixed point in this active-coordinate polydisc. At every point, ||I-BJ||<1 makes BJ invertible, hence both square matrices B and J are invertible, so a fixed point solves f=0. Also J^-1=(I-(I-BJ))^-1 B gives ||J^-1||<=||B||/(1-q). Uniqueness is only within the specified active-coordinate slice and box.

## Independent semantic, derivative, and rejection controls

A separate fresh program uses 150-digit direct inverses of I-W, constructed from the directed cycle edges, to evaluate the full matrix on all inputs via its basis matrix. It independently compares that matrix to a prefix-scan implementation. It checks all 49/121/169 Fourier entries, the negative-sign Weyl shift convention, and the mismatch with the positive-sign target.

The prefix implementation carries its own scalar dual-number automatic differentiation and checks every active derivative against the direct analytic interval derivative midpoint: 1296, 10000, and 20736 entries respectively. The maximum discrepancies are below 2.139e-145, 2.085e-145, and 9.412e-144. These high-precision controls are diagnostics and do not replace the interval proof.

Each size includes ten rejection controls: wrong Fourier sign, normalized target with the same fixed outer calibration, h=1, zero vertex gain, zero middle mask, duplicate active index, invalid cycle permutation, first-row/column cancellation, a mutated last equation, and B=0. The endpoint control makes all second-stage terms identical with nonzero coefficients summing to zero and must hit the endpoint gate. B=0 must give q=1. All reject. A control rejection means this checker refuses that altered certificate; it is not an impossibility theorem. In particular normalized Fourier can be obtained by a different overall outer scaling, which this fixed-calibration convention test intentionally does not perform.

## Source binding

The original Phase56_Lightweight_Fresh.zip hash is 179a5b7de5575e7c05adf354421a70b8914fb698a3b1b81e22d38e242a737272. All 25 manifest members were rehashed, and the relevant extracted copies match the original archive bytes. Programs in the archive were not executed, imported, or compiled.

| Saved center | SHA256 |
|---|---|
| root_candidate_7_3_3.json | d725f1e37d9286c717c631b93b46e2a1ac2bf29c3ad3e19ac7406b98902c8e6f |
| root_candidate_11_5_5.json | 2be975fb485b5e435231cf0708b05fe11f55299f7ad281e7e872ed6e6f63ab0d |
| root_candidate_13_6_6.json | 46b41e17f2b703845d9b4eb0582ee25c1abc41490d39a9d6a559a3730dc5c7cc |

Each verdict binds the exact new checker hash. Original certificates and the earlier N5/N8 report are retained as inert historical evidence in the complete review archive, separately from this report-only publication.

The earlier reported q<0.001 did not follow from its displayed q=0.001+positive terms formula, and ordinary float output displayed 0.001 without outward rounding. The new exact-endpoint receipts independently establish bounds below 0.001 for these three sizes. They replace that reporting defect without changing the previously accepted N5/N8 evidence.

## Scope and remaining work

The separately accepted finite sizes are now N5, N7, N8, N11 and N13, with historical N5/N8 acceptance preserved. This is additional finite evidence, not a new all-size or generic-dimension theorem. The finite-field Jacobian experiments remain unaudited here.

Retain the explicit broader-model boundary: arbitrary independent complex edge gains, nonunit holonomies, variable coefficients, and middle/outer diagonals. Phase44's common-tree/unit-modulus-edge/equal-coefficient architecture is different. NF06's unit-edge, routed four-branch N4 slice is different. No assertion about either model's minima, coverage, or difficulty follows.

The sum counts are 6,10,12, namely N-1. Applying each supplied Green term costs O(N), so the direct finite executors use O(N^2) scalar arithmetic at these sizes. No all-N synthesis or gain generator has been obtained. This audit closes only the three saved-certificate verification gaps. Any all-size, dimension/stabilizer, priority, restricted-model compilation, conditioning, or runtime question requires separate evidence.
