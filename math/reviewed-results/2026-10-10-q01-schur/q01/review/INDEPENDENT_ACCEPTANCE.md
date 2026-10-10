# Independent acceptance of the Q01 finalization

10 October 2026

## Decision and immutable version

**Accepted, with no remaining blocking gap, at the stated mathematical and computational scope.** This independent consolidation review confirms the corrected canonical theorem, its pointwise composition lemma, the interpolation error instantiation, the limited Taylor alternative, and the separate unconstructed exact gate. It is not an external novelty determination or production implementation certification.

This decision binds these exact bytes:

- Final note: `Q01_FINALIZATION.md`, 11,205 bytes, SHA-256 `9ab67e663abe0cca45299dfecbca6c4852fbcd77e5c078a62292c2b8e3f2374b`.
- Final packet: `q01-consolidated-finalization-v3-20261010.zip`, 47,533 bytes, SHA-256 `a56218bc94ee41836b59b615c19e7b9b170290128a7aeb68eb1db44a0440cf31`.
- Checklist: `FINAL_REVIEW_CHECKLIST.md`, SHA-256 `aebb6f83a82376c95e43fc49f5e63055ba07ca951938e70c250790788ec22bcd`.
- Source manifest: `SOURCE_VERSIONS.json`, SHA-256 `9039fa04c38d61e48557282ea9952a1ea1cfe05375b4e4f8e056108a18ededa6`.

Two bounded clarifications were requested and verified: the final quantization bound now explicitly refers to the normalized input, and the exact transport contract now explicitly requires a supplied primitive N-th root in either field setting. Neither changes the mathematical result. The earlier frozen packets remain unchanged.

## Canonical theorem and charged computation

The canonical result correctly retains source A's literal domain N ≥ 2, n = ceil(log₂(N+1)), and a supplied integer 2 ≤ t ≤ n. Inputs have O(cn)-bit dyadic descriptions and polynomial dynamic range; separate bounded coordinate exponents are allowed. The growing word width is C(c)n with the stated integer operations and addressing. Online bounded-width arithmetic uses a fixed number of words, while larger coefficient certificates incur their multiword cost.

The guarantee is deterministic, relative Euclidean error for every represented input, with every finite dyadic output explicitly written. It does not assert coordinatewise relative accuracy, exact norm preservation, or correct rounding. Preparation, table construction, memory movement, addresses, normalization and outputs are charged. Zero and unit-length cases are accounted for.

For every supplied t=o(n), the eventual bound O(Nn/log₂(n/(t+log₂ n))) and O(N) words agree with the corrected proof. Fixed and inverse-polylogarithmic accuracy, and supplied stretched-log precision exponents, have the stated specializations. Precision-specification parsing and generation remain charged; mere computability is not treated as an efficient schedule.

The radix, distinct-stencil and explicit preparation-cap tests make the fast branch conditional. The direct fallback retains the error and O(N)-word guarantees throughout 2 ≤ t ≤ n. Higher precision has its separately priced wider-word fallback. No polynomial-accuracy sub-N-log-N saving is imported from a fixed-accuracy statement.

## Pointwise composition and interpolation constants

The composition lemma has complete compatible-domain hypotheses for the actual supplied vectors. It separates backend error, output-map coefficient error, and preprocessing error through the exact identity

    Ĉ A(v) − C V Bx = Ĉ(A(v) − Vv) + (Ĉ − C)Vv + CV(v − Bx).

Taking norms yields the three stated channel contributions cδb, γ‖V‖b, and ‖C‖‖V‖β. The analytic approximation error τ and final implementation residual η are then added. Neither A nor v(x) needs to be linear. Only the declared coefficient maps use operator norms. At zero input the hypotheses force zero supplied vectors, zero backend outputs, and zero final residual, so the proof also covers that case.

For interpolation, centered padding is isometric, U_M is unitary, the ideal output map is DB, and the represented output map is E B̃. Source A gives ‖B̃‖<3, ‖E‖<2, ‖B̃−B‖≤2ρ, and ‖E−D‖≤3ρ. Consequently ‖E B̃‖<6 and ‖E B̃−DB‖≤4ρ+9ρ=13ρ. With backend error ρ and exact padding, the prequantization error is at most 19ρ‖a‖ for a=x/R. Its norm is below 2‖a‖. The source's relative-plus-underflow quantizer bound contributes at most 3ρ‖a‖. Exact scale restoration therefore gives at most 22ρ‖x‖, with ρ=ε/1024. The revised note makes these norms unambiguous.

The review also checked the corrected source's total table/quantizer semantics, inclusion of initial rounding, coefficient certificates, reachable-state overflow safeguard, and the role of its preparation cap. The consolidation does not convert these obligations into free backend operations.

## Taylor comparison and exact gate

The Taylor section agrees with the independently accepted Taylor audit. Its factorial truncation, bounded masks, rounded coefficients, endpoint factors, and exact dyadic accumulation give

    4/R! + 12δ + 64R²2^(−q),

with R!≥16/ε, δ=ε/128, and q=ceil(log₂(512R²/ε)). The three terms are bounded by ε/4, 3ε/32 and ε/8, respectively, totaling at most 15ε/32<ε. These are pointwise backend estimates, not an operator-norm assertion about one nonlinear executed program.

The fixed-accuracy order matches interpolation. The Taylor inverse-polylogarithmic bound has denominator log log log N and is weaker than interpolation's log log N denominator. The Taylor audit does not establish the full supplied t=o(n) composite theorem. It is correctly treated as an alternative proof route and exact correction-rank diagnostic, not the first accepted project all-length theorem, a stronger accuracy result, or a new discovery count. The rank N/gcd(N,L), including N for odd lengths, restricts that exact separated correction representation alone.

Q31 remains separate. Its setting is exact scalar arithmetic with a supplied primitive N-th root, initially for dyadic lengths. The seed and intertwining identities are necessary and sufficient for the auxiliary operator to equal the unnormalized Fourier matrix, but no growing low-work transport satisfying them is supplied. Parameter/root generation, nonzero-denominator checks, transport and ordinary transpose, addressing and output costs remain obligations. Nonzero baselines are required for the sparse-Gram division formula; zero baselines use the polynomial circuit. Characteristic dividing the trace power k makes the canonical trace carrier's differential and formal Hessian vanish, so it is excluded. Nothing in the approximate composition lemma closes this exact construction gap.

## Integrity checks and review limits

All four source snapshots were independently hashed and compared byte-for-byte to their original accepted/source files:

- A, corrected interpolation: `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`.
- B, Taylor proof: `1716f38b2be430287973ea76856c3173770e873d102e4bf339d0084d4c994b77`.
- C, independent Taylor acceptance: `d1b12a9a7e3e00695e9f73e0addc8b21c6316bfe2f22ea47afc62659df161f00`.
- D, Necklace–Green theory: `8f9e1d4a0de9826fba802e885f7cff244119dffcb543153d6a25173c804eaaea`.

All 15 local source links resolve. All nine manifest digests match, and all ten ZIP file entries match the public files byte-for-byte. Inspection found no private account identifiers, private conversation links, or workspace paths in the publication text. The machine-readable companion receipt records the accepted versions and checks.

No source program was executed, imported, compiled, or parsed into an executable representation. No historical control run is claimed as rerun; this review ran no new mathematical test suite. Fresh file hashing, archive-byte comparisons, and link checks are integrity checks. Prior mathematical acceptance is retained at its stated scope. Production execution, practical crossover, formal machine verification, and external publication priority remain unverified. No remote changes were made.
