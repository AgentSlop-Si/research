# Independent acceptance: cubic-field singleton minimum is thirteen

14 October 2026. Verdict: **INDEPENDENT ACCEPT, precisely scoped**.

## Accepted statement

Let K = F23[u]/(u³ + 13u² + 13u + 13), N = 11, q = 13, S e_t = e_(t+1 mod 11), T e_t = 13^t e_t, and F[k,t] = 13^(-kt). Count only physical banks of the original form

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
        (I - alpha S^epsilon - beta 13^(epsilon delta j) T^delta)^(-1),
    Delta = 1 - alpha^11 - beta^11 != 0.

All parameters and weights belong to K; signs independently equal +1 or -1. Among representations with exactly one effective alpha node in each cross-sign orientation (-,+) and (+,-), the minimum number of physical banks is **exactly 13**. The two cross nodes are free to differ.

This equality combines two separately accepted gates with identical N, q, field, target, original bank grammar and effective-cross-singleton condition:

1. The present fresh literal audit proves a legal thirteen-bank upper witness.
2. The independently sealed parameter/cubic-obstruction review excludes every representation with at most twelve physical banks, allowing arbitrary legal beta, raw weights, zero/repeated alpha nodes and cancellations.

The upper witness's beta = 1 restriction is a construction choice, not a restriction on the minimum's domain. No unrestricted-orientation optimum, classification of all thirteen-bank supports, characteristic-zero lift, novelty claim or FFT runtime improvement follows.

## 1. Exact witness and source binding

The independently reviewed full source witness has SHA-256

    6ede4dadd9284e70885047614749592dfd5ae7958b7f0a361aec1a27a178f2bf

and is copied unchanged as SOURCE_WITNESS.json. Its standalone original-grammar raw certificate is copied as dependencies/RAW_CERTIFICATE.json, SHA-256

    33d742797218c51381783b4128615e702280051f6bcd1ce47207fbbadf92c580.

The orientation allocation in (++,-+,+-,--) order is (5,1,1,6):

- ++ nodes: 3, 21, u, 13 + 20u + 14u², 20 + 2u + 9u².
- -+ node: 15.
- +- node: 7.
- -- nodes: 6, 7, 12, 13, 17, 19.

Every beta is 1. The five ++ nodes are exactly the distinct nonzero roots of

    h15(t) = t^5 + 12t^4 + 17t³ + 14t² + t + 14
           = (t-3)(t-21)(t³ + 13t² + 13t + 13).

The last three are u, u^23 and u^529. The cubic has no root among all 23 base-field residues, and hence is irreducible. Its quotient is the field of 12,167 elements. The element 13 has exact multiplicative order 11. These facts are freshly checked rather than inferred from candidate pass flags.

All thirteen orientation/alpha pairs are distinct, all thirteen denominators are nonzero, and all thirteen bank matrices are nonzero. Thus there are exactly thirteen counted physical banks, and exactly one effective node in each cross orientation. The two cross nodes 15 and 7 are intentionally different.

## 2. Independent literal audit

Only the newly authored independent_verify.py ran. Candidate and historical programs were not executed, imported or compiled. Input JSON was read as inert proposed data. The checker uses standard-library tuple-based finite-field arithmetic and direct monic-polynomial reduction.

For each bank and phase j, the reviewer constructs the original matrix I - alpha S^epsilon - beta 13^(epsilon delta j) T^delta entry by entry, then independently obtains its inverse by Gaussian elimination. It does not use candidate inverse matrices or a geometric-series inverse formula to do so.

All checks pass:

- 143 freshly computed literal inverses.
- 286 separate left and right inverse-product identities.
- All 143 supplied raw phase weights applied with the original 1/11 normalization.
- All thirteen reconstructed bank matrices equal their source matrices and are nonzero.
- Every one of the 121 aggregate entries equals the directly generated literal target exactly.
- All 1,573 bank Weyl coefficients agree with independently word-counted expansions.
- All 143 raw phase weights recovered independently from the literal bank matrices and compared entrywise.
- All eleven full sector systems checked, with ranks 11, 7, 9, 10, 11, 11, 11, 11, 11, 10, 8.
- A separate direct 121-by-143 literal branch system and its augmented system each have rank 110, agreeing with the sum of sector ranks.

All literal matrices and inverse matrices are retained in outputs/LITERAL_BRANCHES.json. The independently recovered raw weights, bank matrices and Weyl coefficients are retained in outputs/BANKS_AND_RAW_WEIGHTS.json. No unverified symbolic construction step is required to establish the upper bound.

### Independent raw recovery

For any literal bank matrix B, extract

    c_B(a,b) = (1/11) sum_t B[(t+a) mod 11,t] 13^(-bt).

The checker verifies that coefficient extraction and Weyl reconstruction are inverse transforms. With s = [delta b]_11, the pure-T coefficient gives

    v_b = Delta c_B(0,b) / beta^s,
    w_j = sum_b v_b 13^(-epsilon b j).

The witness has beta = 1, so this recovery involves no zero division. Every recovered raw weight equals the supplied value. This recovery uses bank matrices obtained from fresh literal inversions, not source amplitudes.

For supplementary coefficient checks, the checker enumerates all binary words through length eleven; each T preceding S contributes 13^(epsilon delta). All mixed degree-eleven coefficients vanish. This yields the complete ordered word factors. The pure coefficient above and alpha powers reconstruct every bank Weyl coefficient, and all source sector amplitudes and equations match.

## 3. Matching lower-bound gate

The independently accepted lower-bound report is copied unchanged as dependencies/LOWER_BOUND_REVIEW.md with verified SHA-256

    6efdb0388067482e6ecca30f8592530dbfbd9a19f6f94ab1a81f9b6c6dc2b55d.

Its independent result file is copied as dependencies/LOWER_BOUND_RESULTS.json with verified SHA-256

    836868a8836c4491e4f8cd33986f3304f3092afd4953c449678417e3c58ee279.

That review was produced separately in parameter_cubic_lower_bound. Its accepted scope explicitly matches the domain stated above. The current reviewer checks that statement and its source hashes and uses it as an independently accepted dependency; the upper-bound checker does not claim to recompute the complete lower-bound proof.

The accepted lower-bound argument establishes at least five distinct nonzero same-sign nodes on either side over every extension. At most twelve physical banks would therefore force (5,1,1,5). Over F23³ its complete parameter gate forces both singleton nodes to 15 and both same-sign supports to the roots of h15. A literal linear functional annihilates every resulting bank for arbitrary legal beta and raw weights but takes value 14 on F. Thus all representations with at most twelve banks are excluded, not merely a selected support with beta = 1.

The thirteen-bank witness avoids that obstruction by using the opposite cross node 7 and six -- nodes. There is no conflict between the accepted lower bound and the accepted witness.

## 4. Deterministic falsification controls

Twenty independent rejection controls pass:

- Delete each of the thirteen banks separately.
- Increase one raw phase weight by one.
- Omit the 1/11 factor.
- Reverse the target Fourier exponent.
- Corrupt one literal inverse entry.
- Reverse the phase exponent of either cross bank separately.
- Admit alpha = 0, beta = 1 despite its zero denominator and singular literal matrix.

All outcomes and exact discrepancy counts are saved in outputs/MUTATION_CONTROLS.json. These controls supplement the exact identities; they do not broaden the theorem's scope.

The candidate also reports failures of two alternative support patterns with opposite cross nodes 10 and 12. Those negative cases are outside this upper-witness review and are not independently accepted here.

## 5. Cold replay and limits

The reviewer source and immutable witness were copied into an otherwise empty cold_workspace directory. Running that copy with isolated Python reproduces all six deterministic output files byte for byte. REPLAY_VERIFICATION.json records the comparisons; execution timings are excluded from byte equality. No source program, cached scientific module or historical executable is needed.

From the extracted review directory, reproduce with

    python3 -I independent_verify.py

The raw arithmetic run takes approximately two to three seconds; exact elapsed times are retained. That is computation time, not total review or reasoning time. Model-token usage is unavailable. There were no unexpected arithmetic exceptions or assertion failures.

No external service was written. All evidence and this acceptance were saved locally. The accepted conclusion is the exact thirteen-bank minimum in the fixed N = 11, q = 13, F23³ free-cross-singleton architecture stated above, and no broader one.
