# Independent review: Q2 canonical Weyl-displacement obstruction

Date: 18 October 2026. Scope: Q2-DENSE-TORUS-20261013, proposed canonical same-generator displacement route for the actual cyclic inverse boundary.

## Decision

The mathematical theorem is accepted in its stated narrow scope. For every integer m≥4, every primitive complex m-th root q, and the actual prescribed λ=2^(-4-m ceil(log₂(2m))), both F and F⁻¹ have rank-m displacements relative to each canonical Weyl generator U and Q. Here F=I−T_(m−1)…T_0 is precisely the source's ordered cyclic boundary.

This rejects the proposed uniformly bounded-rank interface for those two same-generator equations. It does not reject arbitrary two-generator displacement equations, other representations, or a cold O(N) inverse. It proves no arithmetic lower bound. Exact cold O(N) inversion remains OPEN; the retained ledger is O(N^(3/2)) cold, O(N) warm, O(N) exact scalars and words, without a unit-cost bit claim. No historical implementation, uniform Fourier theorem, priority claim, or parent closure is certified.

A minor initial output reproducibility discrepancy was corrected before acceptance: the first frozen CHECK_RESULTS.json contains a verified-primality status field that the first frozen script checks but does not emit. All computational values otherwise match. The original version is preserved in author_v1/ and its actual replay in replay_v1/. The corrected version is preserved in author_v2/ and its successful, byte-for-byte replay in replay_v2/. Report, ledger, source bindings, source report, and every JSON value are unchanged; the correction makes the asserted primality result emitted by the script. The final disposition/binding file records the verified corrected input hashes.

## Source and frozen input verification

All six original author file lengths and SHA256 hashes were verified against the original frozen manifest at the first review read. A later review-staging mistake copied the corrected v2 CHECK_RESULTS.json into author_v1/. Packaging detected that discrepancy. The exact original v1 results were then reconstructed from the preserved original replay plus the final primality field displayed in the complete initial source read; the recovered 2,160 bytes match the original frozen SHA256 f436df642228829a13c63c227eaf935750b666c64c2562fbfc28c20e8a833f87 exactly. This is a hash-verified reconstruction, not a claim that the original results file was continuously retained. The wrongly staged v2 copy, prior review/disposition, and prior review manifest are preserved in provenance_correction/. Both restored author_v1/ and accepted author_v2/ now match their respective frozen input manifests. The authoritative accepted mathematical input remains author_v2/; no mathematical decision or v2 byte changed. The local source copy is 20,050 bytes, SHA256 675e7c52bee2bc37f1253b9633fb3091e16c174b6853cc9321a6c742eddca1d3. Independently computing Git's blob hash gives 6699b54831c182d8131dc4a9dfbd202dfa3d4e70. A fresh read-only GitHub fetch at commit 22e4fbdff0dd655d4cac7408964142fd2476686d returns that same blob for the controlling report.

Source: [pinned paid-inverse report](https://github.com/AgentSlop-Si/research/blob/22e4fbdff0dd655d4cac7408964142fd2476686d/math/finalized/2026-10-16-mathematical-development-1221/q2/REPORT.md).

The family, phase q^(−c), row direction, coefficient schedule, product order, boundary location, and noncommuting factorization S=L⁻¹(M+λL)M⁻¹ agree with the source. In particular, no scalar or reordered monodromy has been substituted.

## All-size proof review

1. With W=U⁻¹+Q, the cyclic determinant has exactly its diagonal and full-cycle contributions, giving det(xI−W)=x^m−2 and W^m=2I. The defining relations QU=q⁻¹UQ and QU⁻¹=qU⁻¹Q are correctly oriented.
2. Differentiating the actual ordered product at zero gives the stated sum. Iterating WU=q⁻¹UW+(1−q⁻¹)I and summing primitive-root phases kills the noncommuting part for m>2. The result is C₁=E′(0)=2m·4^(−m)(W⁻¹−I). No generic-parameter inference is used.
3. For X=U,Q, [W,X] is |1−q| times a unitary matrix up to phase. Consequently σ_min([C₁,X])≥(m/2)4^(−m)|1−q|≥2·4^(−m), using ||W||₂≤2 and |1−q|≥2sin(π/m)≥4/m. The lower bound is uniform over all primitive embeddings.
4. On |z|≤r=1/(8m), ||H_a||₂≤5/4 ensures analytic factors. The logarithmic estimate gives ||E(z)||₂≤2^(−m)e^(1/4)<2^(1−m). Matrix-valued Cauchy bounds and λ<r/2 give ||[J(λ),X]||₂<512m²2^(−m)λ².
5. The fixed schedule obeys λ≤1/[16(2m)^m]≤1/[256m²2^m]. The middle step is exactly m^(m−2)≥16, true for every m≥4. Its equality at m=4 is harmless because the analytic remainder bound is strict. Hence the perturbation norm is strictly below the uniform first-order lower singular value at the actual λ.
6. The actual complex row norm satisfies ||T_a||₂≤(2+λ)/(4+3λ)<1/2, so ||E||₂<1 and F is invertible. The identity [F⁻¹,X]=−F⁻¹[F,X]F⁻¹ preserves rank. Multiplying by X⁻¹ identifies each commutator rank with its corresponding displacement rank.

As an independent quantitative cross-check, the same argument can retain e^(1/4)<4/3 instead of the looser bound 2. It then yields

    σ_min(F−XFX⁻¹) > (2/3) λ4^(−m),
    σ_min(F⁻¹−XF⁻¹X⁻¹) > [(2/3) λ4^(−m)]/(1+2^(−m))²,

for both X=U,Q and all m≥4. These explicit positive margins follow from the same valid bounds and are not needed to repair the author's proof.

Simultaneous conjugation of a matrix and its displacement generator preserves rank. That observation supports the report's basis-change statement; it does not cover independently chosen left/right generators or a genuinely different displacement equation.

## Independent fresh controls

The reviewer-owned independent_controls.py imports neither author code nor historical programs. It constructs the original full L directly from coordinates and constructs M=P⁻¹LP by permuting both row and column indices. For m=3,4,5,6,8,10,12 over F14401 it checks all primitive m-th-root embeddings, totaling 22 cases. A primitive N=m² root is independently produced and its exact order validated.

All 22 cases verify the exact first-variation identity using a formal truncated series through degree two, plus nonzero determinants for all four F/F⁻¹ displacements. For one root at every tested size, the full source K equals the row-block construction, the full Schur boundary equals D_(m−1)F, and det K=(∏det D_a)det F. These are transcription controls, not all-size proof substitutes.

The separate m=2 guard control works in F79²=F79[i]/(i²+1). The polynomial is independently checked irreducible, i has exact order four, and q=i² has exact order two. At the actual λ=1/256=25, β=1, and both row blocks have rank one. Independent permutation-sum determinants give det K=39 and det L=det M=2. Direct construction gives det S=69 and verifies S·(MK⁻¹L)=I. Thus the full transform is invertible although the row executor is unavailable. No complex analytic rank statement is extrapolated to this finite field.

The root-order contract, scalar denominator requirements, s≠0, 1−β^m≠0, and full invertibility remain logically distinct. The determinant boundary criterion is used only when the row blocks are invertible.

## Cost and stopping boundary

The paid setup/warm/storage ledger matches the pinned source: coefficient/root preparation remains charged, E formation costs 10m³+m² scalar additions/multiplications, F formation costs m² subtractions, dense LU remains paid, and the warm scalar count is 32N+m with O(N) additional word work and all N outputs. These counts do not turn warm access into a cold O(N) theorem and do not bound exact scalar representation lengths.

This review executed only fresh sibling copies and reviewer-owned controls. It made no repository, spreadsheet, or other external writes. The scoped mathematical acceptance does not broaden any source-register status or close the parent problem.
