Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 7c77cb25b336bd9c96751d7683e370e21b3c5509c6b3ceb95631c3c3d9d8ee80

---

# Phase 56 finite Green-network certificate audit

Audit date: 2026-10-11 UTC. Read-only external work; local evidence and fresh audit programs only.

## Decision

**ACCEPT SCOPED, N=5 and N=8.** Freshly authored independent interval/automatic-differentiation code verifies existence of the full negative-sign, unnormalized Fourier matrices in the saved two-stage networks, with respectively 2+2 and 3+4 Green terms. These are isolated complex root certificates, not exact equality at the printed rational centers.

**REPAIR comparison and reporting language.** The seven-versus-twelve N=8 comparison changes the edge-gain model. It is not a lower-bound refutation, an optimization inside the old restricted architecture, a phase-only construction, or an asymptotic speedup. The original certificate diagnostics also round a strict bound to `0.001`; that rounded display is not a rigorous upper bound. Fresh exact-rational endpoint receipts below replace it for the two audited sizes.

**Not independently accepted here:** the N=7,11,13 root certificates; finite-field Jacobian rank experiments; all-size/generic dimension theorem; novelty or performance claims. The archives for these claims exist, but this bounded audit did not replay them. No Supers site or leaderboard was accessed, and no track qualification is claimed.

## Source recovery and exact coverage




- `Phase56_Lightweight_Fresh.zip`, Library `[private reference omitted]`, backing file `[private reference omitted]`, 812345 bytes, SHA256 `179a5b7de5575e7c05adf354421a70b8914fb698a3b1b81e22d38e242a737272`.
- `Phase56_Green_FFT_Research.zip`, Library `[private reference omitted]`, backing file `[private reference omitted]`, 832758 bytes, SHA256 `525d953c1e68f52980da62125286802063a6c3ecc0abcb6f3a18107fc4591e71`.
- `Phase56_Theorems.md`, Library `[private reference omitted]`, SHA256 `de2d028094611802a644484c122f07949d0643948aad1e11248ee0f211e25986`.
- `Phase56_Proof_Verifier.py`, Library `[private reference omitted]`, SHA256 `27dd77e01642b7f2b5288c11292a7564c442b6e6836b9f0484a07dea59e915a1`.
- `Phase56_Research_Start_Here.md`, Library `[private reference omitted]`, SHA256 `5b1f6a065fceabbb245c27834126f3ec01ccf63b5392e87f8f3bef9954d3b4be`.

All 25 lightweight manifest entries match. The lightweight archive has 26 files including its manifest. All common entries in the complete archive are byte-identical; the complete archive adds the previous Phase55 ZIP. The three standalone text/code documents are byte-identical to the corresponding archive members. The Phase55 nested archive was not inspected or executed. A repository search for `Phase56` in AgentSlop-Si/research returned no hits; this is only a bounded search result, not proof of repository-wide absence.

Fully read as inert text: Phase56 theorem (13405 bytes), checkpoint (2930), verifier (10122), README (1265), matrix-free numerical checker (2961), all five saved certification receipts. Fully parsed and used as data: N5 and N8 root JSON, including every center coordinate, topology, active index and preconditioner entry. N7/11/13 root files were integrity-hashed but their numerical claims were not independently checked. No original research program was executed, imported, compiled, or used as an audit dependency.


## Mathematical contract verified

For each saved cycle order, vertex gains g_i are nonzero and holonomy h is nonzero and not 1. The Green entry is

G_ij = (g_i/g_j) [1 if pos(i)>=pos(j), otherwise h] / (1-h).

This is (I-W)^(-1), where W carries each vertex to its successor with gain g_successor/g_predecessor and multiplies the closing edge by h. Each stage is an unrestricted complex linear combination of such independent cycles. With nonzero middle diagonal D, M=S2 D S1. All outer calibrations are nonzero complex diagonals.

The checked target is f_ij=M_ij M_00/(M_i0 M_0j)-exp(-2 pi i i j/N)=0 for every 1<=i,j<N, with all required denominators nonzero. At a root, L_i=1/M_i0 and R_j=M_00/M_0j give L M R=F_N entrywise, including the zeroth row and column. Since this is a matrix identity, it acts correctly on every complex input vector at this fixed N.

The exact root may have arbitrary complex amplitudes. This is essential, not a phase-only guarantee. For example the N8 center's varying middle-mask magnitudes range approximately 1.829 to 8.349, vertex-gauge magnitudes 0.163 to 50.558, and holonomy magnitudes 0.038 to 3.035. These are diagnostics, not interval gates; strict nonzero/pole margins are certified separately.

## Independent certificate method

`fresh_interval_audit.py` is newly written. It imports only standard Python modules and installed mpmath 1.3.0. It reads source JSON, validates parameter/index shapes and cycle permutations, and reconstructs the holomorphic equations independently using forward automatic differentiation. It does not call, import, or copy the source's analytical Jacobian, rational A0 construction, or Cauchy-domain proof.

All finite-decimal centers and preconditioner entries are interpreted as exact rational numbers enclosed by `mpmath.iv` at 150 decimal digits. Active complex coordinates vary within a radius-r complex sup-norm polydisc; the evaluator uses real/imaginary rectangles containing that polydisc. It checks nonzero gains, coefficients, holonomies, all masks, every 1-h pole distance, and first-row/column denominators throughout that rectangle.

The interval derivative encloses J(z) throughout the domain. The code computes eta >= ||B f(c)||_infinity and q >= sup_z ||I-B J(z)||_infinity, using complex taxicab absolute-value upper bounds. Every interval endpoint is converted from its exact binary representation to Python Fraction. The final comparisons q<1 and eta+q*r<r are exact rational comparisons. The JSON receipts retain numerator and denominator, not just floating diagnostics.

These strict inequalities make z -> z-Bf(z) a contraction mapping the closed complex polydisc into itself. Because I-BJ(c) has norm below 1, B is nonsingular. Its unique fixed point in the selected active-coordinate polydisc therefore solves f=0. Inactive parameters remain fixed at their exact recorded rational centers. This does not claim uniqueness in the full parameter space.

### N5 result

- Source root `root_candidate_5_2_2.json`, SHA256 `446b85e6d550702c434ff02fd22b63b2e658c1c08bdbbed17b1fb612809fcb5e`.
- 16 complex equations; 18 total coordinates; 16 active; 2 frozen.
- r=1e-70; q<1.200e-10; eta<5.245e-99.
- Unpreconditioned residual taxicab upper <2.770e-98.
- Minimum certified gain/coefficient/mask/pole margin >0.11105.
- Minimum certified first-row/column margin >0.14041.
- Strict self-mapping margin >9.9999999987e-71.

### N8 result

- Source root `root_candidate_8_3_4.json`, SHA256 `9add27f83b6c0866fef4ce37961f5d960f61234df502b9a35790d50b744f20ee`.
- 49 complex equations; 54 total coordinates; 49 active; 5 frozen.
- r=1e-70; q<6.224e-11; eta<2.393e-93.
- Unpreconditioned residual taxicab upper <9.172e-94.
- Minimum certified gain/coefficient/mask/pole margin >0.03521.
- Minimum certified first-row/column margin >0.83545.
- Strict self-mapping margin >9.9999999993e-71.

Full exact results: `FRESH_CERTIFICATE_N5.json` and `FRESH_CERTIFICATE_N8.json`. Both positive checks were rerun against the final audit program.

### Independent semantic and rejection controls

`fresh_network_control.py` builds I-W directly and applies each Green by a fresh complex Gaussian solve, on every basis input. It does not use the entry formula or prefix implementation. After calibration, max full-Fourier entry errors are about 1.60e-14 (N5) and 9.33e-15 (N8); the full negative-sign Weyl shift errors are about 1.60e-14 and 1.14e-14. These floating checks confirm the operator convention but do not prove existence.

Four rigorous negative controls reject: wrong Fourier sign at N5 and N8 (self-mapping fails); a holonomy changed to 1 (pole gate fails); and an active center changed to 123 (contraction fails). The altered sources are in-memory controls only; original artifacts are unchanged. See `NEGATIVE_CONTROLS.json` and `FRESH_NETWORK_CONTROLS.json`.

## Reconciliation with accepted finite kernels

The previously accepted relevant record is Incoming `PHASE44-FULL-F8-20261011`. Its original theorem is Library `[private reference omitted]` (`FFT_Phase44_Theorems.md`, 14516 bytes, all 155 lines read in this audit). Its historical source hash is `d71dfe4c5ad7ba1d92091e4399e2a75440bf6bcb18f0f18b0b1c3933e8ad11b4`; archive Library `[private reference omitted]`, historical SHA256 `6858d1cb943d2fb5ba55e50bdc41576e48acb3dbe52626fb32d8911a24ab2759`. The frozen Incoming row identifies accepted independent review SHA256 `2ebae7f1f40e60a4a50cd17fb4319511e0a719fe5d4ee70e2d9f3967366a53b1`. These historical hashes were read from the frozen record; its full archive was not independently materialized or rehashed here.

Phase44 used four sums of three Green terms, unit-modulus internal edge choices with a common tree gauge per stage, equal term coefficients, and arbitrary nonzero complex interstage diagonals. Phase56 has two stages and seven terms, but permits independent complex vertex gains, nonunit holonomies and variable complex coefficients. Thus Phase56 is a new verified finite representation in the broader architecture. It does not contradict Phase44's restricted-model minimum depth for generic local expressivity, nor prove a smaller representation within Phase44's constrained family. Neither result proves a minimum number of terms for F8 alone.

- Row39 C09: a separate accepted F16 certificate, 24 branch occurrences and 384 endpoint parameters. It is not the still-open F16 membership in Phase44's specific family.
- Row50 M-F8-EXACT / F060: a separate normalized F8 three-stage separated-generator-order1 certificate, historical review hash `73f74388461972c5fdfac25d22b00ad56834907f95c676b2f33d3174426fc2e4`. No equivalence of this model and Phase56 was assumed.
- Row52 M-FOURIER4-GREEN / F060: small F4 kernels in distinct architectures.
- Row94 M-N4-GAUGE-RECURSION / F060,F125: finite N4 existence and gauge recursion, not all-length synthesis.

## Original-source repairs and limits

1. The theorem's table labels q as `<1e-3`, while its explicit final q formula is `1e-3 + Bmax*1e-45 + positive variation`. That particular displayed formula is strictly greater than 1e-3. The verifier correctly tests a looser q<1/2 sufficient for existence. Its receipt converts the rational q to an ordinary float, displaying `0.001`; that rounded text must not be treated as an outward-rounded upper bound. The fresh N5/N8 checks establish much smaller strict bounds directly.
2. A source comment and assertion error text mention `1e-5` for I-BA0, although the actual integer condition `maximum*1000<denom` proves `<1e-3`. The executable condition and theorem's main proof are consistent at 1e-3; the stale comment is a reporting repair.
3. The N=7,11,13 saved receipts remain source claims in this audit. Their root hashes are respectively `d725f1e37d9286c717c631b93b46e2a1ac2bf29c3ad3e19ac7406b98902c8e6f`, `2be975fb485b5e435231cf0708b05fe11f55299f7ad281e7e872ed6e6f63ab0d`, and `46b41e17f2b703845d9b4eb0582ee25c1abc41490d39a9d6a559a3730dc5c7cc`.
4. Each term costs O(N) given its order and gains. The five listed examples use T=N-1, so the obvious extrapolated executor costs O(N^2). No all-N existence theorem, uniform gain generator, conditioning bound, sub-N-log-N algorithm, bit-complexity improvement, or production timing follows.
5. The gauge-count theorem concerns generic matrices, not a Fourier-specific lower bound. It was read and screened, not promoted as independently accepted in this bounded pass.

## Next action and stopping point


No Sheet or GitHub writes, no browser work, no Supers access, no original uploaded-code execution, and no publication or novelty promotion occurred.
