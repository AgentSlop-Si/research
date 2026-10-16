# Independent review: binary-index rank-one Fourier comparison

Date: 16 October 2026. Verdict: **ACCEPT the completed bounded primary-source comparison.**

Accepted comparison report SHA-256: `24e123e2f6784f5d852731b674575d1e5a0620afb7aad72ff793488ab6b5afdc`.

The review independently checked the research statement, its prior scoped review, and the primary sources cited in the comparison. The accepted result is a qualified interface nonmatch and precise classical relationship, not a new correctness milestone or historical-priority claim.

## Findings

1. Dolgov–Khoromskij–Savostyanov, Algorithm 2 and Theorem 3, give rank- and accuracy-conditioned work on compressed QTT representations. The estimate does not pay for checking every raw coordinate or materializing every output. Exact use retains true ranks; truncation with positive tolerance is approximate. The complex QR/SVD framework does not automatically transfer to a finite field or an odd residue ring.
2. Savostyanov's rank-one-output subclass is narrower than all binary-index rank-one inputs. The stated sign, normalization and bit-order mapping is correct. Rank one at input alone cannot justify uniformly rank-one Fourier intermediates or output.
3. The ordinary even/odd split, specialized to x_(2q+b)=a_0(b)t_q, gives X_k=(a_0(0)+a_0(1)omega^k)T_(k mod N/2). Reusing the common child transform reproduces the research suffix recurrence. This is correctly identified as an algebraic specialization rather than a claim that the historical paper explicitly states the complete raw-certificate package.
4. The cold ledger remains 6N−7+2d multiplications, 2N−2 additions and one inversion for accepted nonzero N>=2, plus every raw comparison and O(N) word work/storage. The 2N−2 suffix states, paid root preparation and separate zero/N=1 cases are consistent. Unit-pivot and principal-root conditions remain essential in a residue ring.
5. The older comparison leads receive substantive dispositions: binary tensor rank does not imply a short finite recurrence or small total rational degree; a nonzero field-valued factored product may have N monomial terms; all-output evaluation has K=N for the pruned-FFT interface. These are qualified nonmatches, with overlapping subclasses preserved.
6. Camps–Van Beeumen–Yang's rank-growth discussion is correctly limited to the proposed tensor-product route. It is not treated as a lower bound against every explicit-output evaluator.

The exact witness x=(1,2,3,6) gives positive order-four DFT (12,−2−4i,−4,−2+4i). Its output binary unfolding determinant is −32+32i, confirming that input rank one and output rank one are distinct conditions. Fresh finite checks support the audit but do not replay or replace the previously accepted proof.

## Scope conclusion

The selected theorem, exact hypothesis/formula mapping, cost comparison and disposition of the older leads satisfy the recorded comparison task. No outstanding assigned implementation action was identified in the complete research statement. The numerical residual path is explicitly optional and conditional on paid outward rounding; fallback is optional external work. Those limitations remain, rather than being claimed implemented.

The accepted proof, scientific assessment and historical-priority qualification are unchanged. This review establishes no unrestricted-input FFT improvement, worldwide priority, numerical implementation, production readiness or optimized runtime superiority.

Primary sources and precise locators are provided in the accepted comparison report.
