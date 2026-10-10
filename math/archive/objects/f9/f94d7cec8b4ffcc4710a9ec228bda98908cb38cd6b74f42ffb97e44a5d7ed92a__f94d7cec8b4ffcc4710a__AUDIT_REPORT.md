# Sealed independent audit: HERO17 tensor, fiber, phase and coset recognition

Audit date: 9 October 2026 UTC. Source checkpoint labels itself 10 October 2026.

## Verdict

The selected-split exact finite-field tensor and fiber algorithms are sound under the stated input, prime-field and supplied-root contracts. Their deterministic recognition costs are charged, their accepted transforms produce all N coefficients, and maximal ordinary fiber-matrix rank does not invalidate the sparse-fiber proof. The inherited common-quadratic-chirp engine correctly handles the full quadratic-parameter quotient, zero input, nonunit phases and even lengths.

**One important coverage correction:** the shipped fused dispatcher recognizes its chosen CRT split and its single default fiber divisor. It does not recognize the union over all eligible divisors. A concrete N=12 counterexample is given below. This is a missed fast-path opportunity, not an incorrect accepted output.

**One important fusion boundary:** the archive still uses the original factorial permutation eliminant. The prior master’s polynomial Toeplitz eliminant and growing-rank corollary are not integrated. In particular, the whole shipped fused callable must not inherit the standalone tensor/fiber O(rN) growing-rank bound.

No universal O(N), unrestricted sub-N-log-N DFT, arbitrary integer-multiplication, finite-precision-stability, or publication-priority claim is established. No uploaded Python was executed or imported.

## 1. Materials and audit method

Read as data: RESEARCH.md, README.md, CHAIN_CHECKPOINT.md, tensor_union.py, fiber_union.py, fast_vandermonde.py, phase_union_general.py, coset_union.py, fused_fft.py, test_hero17.py and independent_audit.py in the extracted HERO17 tensor/fiber archive. Graph convolution is covered by a separate audit.

Compared against the existing common-chirp audit, ELIMINANT_EXTENSION.md and GROWING_RANK_CHIRP_COROLLARY.md under the prior master. Provenance records their hashes without modifying them.

The attached independent_checks.py is newly authored standard-library code. It uses a separately written dynamic BM, Gaussian moment recovery, generic subset-DP polynomial determinants, direct finite-field DFTs and explicit full-vector oracles. It does not import any uploaded module. Its tests validate mathematical identities and independently reconstructed mechanisms; they are not execution regressions of the supplied implementation, do not reproduce the supplied 27-test claim, and do not measure optimized FFT performance. Supplied test logs remain attributed evidence only.

## 2. CRT tensor recognition and transform

For N=AB, gcd(A,B)=1, the input permutation j=u e_A+v e_B and output permutation k=sB+tA give

    omega^(-jk)=(omega^B)^(-us) (omega^A)^(-vt).

Both maps are bijections. Thus the permuted transform is F_A X F_B^T. Exact row elimination in tensor_union.py constructs X=sum_l f_l g_l^T: new normalized residual rows have zeroes at previous pivots, and earlier rows may be padded with zero coefficients. A later pivot need not be numerically to the right of all earlier pivots; the triangular zero-at-previous-pivots invariant is sufficient. At the first independent row beyond the bound, rejection is valid.

For actual rank s<=r, raw recognition costs O((1+r)N) field work and at most r scalar inversions. Direct short transforms and materialization cost O(r(A²+B²)+rN+N). A²+B²<=C N therefore gives O((1+r)N), uniformly for feasible r. Matrix rank is preserved by the invertible short DFTs.

The dispatcher checks A²+B²<=4N. Standalone tensor transform entry points do not impose that guard; their accepted unbalanced instances retain O(r(A²+B²+N)), not automatically O(rN).

Every integer polynomial P respects the CRT ring decomposition: P(j)=e_A P(u)+e_B P(v) mod N. Consequently omega^{P(j)} has CRT rank one, and sums of r independently parameterized polynomial phases have rank at most r. This is exact ring algebra and does not require the polynomial to be quadratic or its coefficients to be supplied to the recognizer.

## 3. Fiber recognition: soundness, completeness and accounting

Write N=QM, eta=omega^Q, y_t[u]=x[t+Qu]. A fiber is accepted precisely when it has at most r distinct eta-character modes.

For M>=3r, an s-mode sequence with nonzero coefficients has a nonsingular s-by-s Hankel factorization V diag(c) V^T. At least 2s samples identify its degree-s recurrence. Prefix linear complexity cannot decrease, so the supplied bounded BM safely rejects before a proposed order above r. It caches the inverse of the previous nonzero discrepancy and performs at most r order-increasing inversions per fiber. The recurrence coefficient list must be reversed to obtain the ascending node polynomial; the source does so. Its exact M-root scan requires all s distinct admissible roots. The full-coordinate reconstruction check gives deterministic soundness.

For nodes z_i, let P(z)=product_i(z-z_i), Q_i=P/(z-z_i). The coefficient dot product with moments satisfies

    sum_j [z^j]Q_i(z) y_j = sum_l c_l Q_i(z_l) = c_i P'(z_i).

Thus fast_vandermonde.py’s amplitude formula is correct, including arbitrary distinct nodes, with O(s²) arithmetic and s scalar inversions. Its live auxiliary storage is O(s), not O(s²): it constructs the quotients sequentially. Distinct-node testing costs O(s²), already included.

When M<3r the source computes the entire short fiber spectrum and counts its nonzero coefficients. This is an exact membership test, including zero rows and the N=M=1 endpoint.

Orthogonality gives, for k=h+sM,

    X[k]=M sum_t sum_{(h',c) in R_t, h'=h} c omega^(-kt).

A detected mode contributes exactly Q output updates. With K=sum_t |R_t|, output work is O(N+QK), at most O(N+rQ²). No uncharged global FFT, mode oracle or precomputed input-dependent table appears.

An explicit uniform ledger is

    O(N+rN+Qr²+rQ²) field additions/multiplications,
    O(Qr) scalar inversions,
    O(N) live field-element storage for 1<=r<=M.

If M>=3r, Qr²<=rN. If M<3r, the direct branch costs QM²=NM<3rN, and its storage is linear. For a fixed Q²<=C N and r_eff=min(r,M), the whole fiber branch therefore admits O((1+r_eff)N) arithmetic, O(Qr_eff) inversions and O(N) space. Recognition on rejected inputs has the same bound. Arbitrary independent labels across rows are allowed, so Q distinct character rows with nonzero amplitudes have full row rank when Q<=M while remaining one-mode per fiber.

## 4. Complete common-chirp phase coverage

Let r>=1, N>=3r. A nonzero s<=r character sum cannot have r consecutive zero samples. The interior interval of eligible centers has N-2r>=r entries, so a nonzero promised vector has a nonzero center. The source explicitly handles all-zero input first.

For the (r+1)-square Hankel phase determinant, the unique minimum exponent is the reversal permutation. After dividing by t^{(r+1)r(r-1)/2}, the eliminant has degree at most D=binom(r+2,3) and nonzero constant coefficient (-1)^{r(r+1)/2}x_center^{r+1}. This proof works in the supplied prime field even when D>=p. At the true quadratic phase, t=omega^{-2a}, its Hankel matrix differs from the dechirped rank-r matrix by invertible diagonal factors, so the eliminant vanishes.

The canonical phase range has L=N/gcd(2,N) elements. For even N, replacing a by a+N/2 adds the linear frequency N/2 since j²=j mod 2. Hence the omitted parameters are exactly redundant representations, not missed chirps. The map a to omega^{-2a} is injective on the retained range; at most min(D,L) candidates survive. Every candidate is individually dechirped, recurrence-tested, root-scanned, solved and fully verified. Returning the first verified representation is sufficient; uniqueness is not claimed.

The shipped construction remains O((r+1)!r²) for its eliminant, O(ND) for the scan, and O(min(D,L)(Nr+r³)) for candidate verification. It is O_r(N) for fixed r, not uniformly O(rN).

The Gauss evaluator is also correct at all transform lengths. With d=gcd(a,N), m=N/d, the row vanishes unless d divides the linear parameter. Odd m uses completion of squares. For m=2q, only parameters of parity q survive; the base linear parameter q mod 2 and the shift solved modulo q give the stated exponent. The m=1 and m=2 branches avoid invalid inverses modulo one. These are exact identities, independent of numerical approximation.

## 5. Coset reduction and root/model obligations

The support scan finds the largest divisor d of N for which all nonzero indices lie in one class u mod d. Equivalently, this is the smallest affine subgroup coset containing the support. There are O(N) divisibility/sample checks and at most O(log N) strict gcd reductions, since each new divisor is at most half the preceding one.

With y[t]=x[u+dt], eta=omega^d,

    X[k]=omega^(-uk) Y[k mod (N/d)].

If support shrinks further than a originally promised coset, restriction of a common quadratic chirp to a shorter arithmetic progression is still a common quadratic chirp with at most the same number of character modes. Some modes may merge or cancel. Thus the maximal-divisor choice preserves this promised family. Zero and singleton inputs are explicitly supported. For the short-coset branch, the literal source uses modular pow inside direct summation: uniformly in growing r this has O(M² log M) modular-multiplication cost rather than a literal O(M²). A length-M root table removes that extra factor; fixed-r O_r(N) is unaffected either way, and the combined polynomial-chirp ledger below already dominates this small branch.

Both root-table implementations validate exact order in O(N) multiplications, including N=1. They do not prove that p is prime. Primality/certification, the field and the primitive root are supplied premises; prime/root construction from a bare length N is not an online guarantee. A fixed field only supports N dividing p-1. “Every length” means every positive N with suitable supplied field/root data, not one universal fixed field.

The word-RAM interpretation additionally requires p=N^{O(1)}, word-sized exact input residues, addressing/modular multiplication/reduction contracts, and bounded-word indices. Integer gcd/inverses and scalar field inversions must be charged. With O(log N) word cost per inverse, fiber inversion overhead is O(Qr log N), absorbed by O(rN) when Q²<=C N; tensor needs O(r log N). No bit-complexity theorem for unrestricted-size inputs or stable floating-point equality recognizer follows. The trusted-certificate entry points accept externally constructed dataclasses; only certificates returned by the verified raw recognizers carry the stated membership guarantee.

## 6. Verified default-divisor counterexample

Take N=12, F_13, primitive root omega=2, r=1, and

    x=[1,2,1,8,1,6,1,11,1,5,1,7].

At Q=2, the even fiber is 1 and the odd fiber is 2*4^u, so each fiber has one character. Q²<=N. The exact direct DFT agrees with the independent Q=2 evaluator.

The default choose_q returns Q=3. Its first fiber is [1,8,1,5], whose successive ratios begin 8 and 5 in F_13, so it is not one character. The selected CRT split is (3,4), and its matrix has rank 2. All samples are nonzero, so support gcd is 1. A rank-one common quadratic chirp would have constant x[j+2]x[j]/x[j+1]²; the first two values are 10 and 3, so no such chirp exists. Therefore all three branches of the shipped r=1 dispatcher reject this valid alternate-Q one-mode input.

The source’s per-specified-Q theorem remains correct. Its default dispatcher must be described as a selected-split union. Trying a fixed constant number of public alternatives preserves the linear bound. Trying every divisor must include the number and cost of those attempts; it is not a free completeness repair.

## 7. Independent checks completed

All checks passed; details are in independent_results.json.

- 118,617 exhaustive raw row-membership vectors across F_7^3/r=1, F_5^4/r=1 and F_7^6/r=2; 613 accepted, no disagreement with the full direct-spectrum oracle.
- 591 raw sparse-fiber cases across diverse lengths, every eligible divisor in the finite test list, zero rows and small-row endpoints.
- 30 arbitrary-factor CRT transform/rank-invariance cases.
- 9 maximal-row-rank one-mode fiber cases.
- 1,341 common-chirp cases covering every a at each tested N=3..30 and allowed r=1..3.
- 820 all-phase Gauss rows and 22,140 row entries at N=1..40.
- 160 degree-independent bounded-square-multiplier polynomial-phase cases, described in EXTENSION_AND_FUSION.md.
- 44 independent Vandermonde-formula cases.
- 62,481 explicitly checked direct-DFT bins, in addition to the Gauss-row and exhaustive spectral-membership oracle entries.
- The explicit selected-divisor coverage counterexample.

Finite tests support, but do not replace, the proofs and charged ledgers. Runtime in the JSON is an unoptimized diagnostic only.

## 8. Recommended acceptance wording

Accept the fixed-r exact tensor/fiber/coset fast paths under their selected-split and supplied-field/root hypotheses. Accept the standalone uniform tensor/fiber growing-rank corollary and separately budgeted fusion proved in EXTENSION_AND_FUSION.md. Do not describe the source dispatcher as a complete union over all divisors, as already using the master’s Toeplitz eliminant, or as universally sub-N-log-N. Retain explicit fallback/nonmembership and no-priority qualifications. Bounded primary-source context is in PRIOR_ART.md.

## 9. Cross-check of the separate graph audit’s bounded extension

The graph auditor proposed testing bounded ordinary rank of the merged coefficient matrix C[t,h] after the original surviving-state guard fails. I independently checked the algebra and accounting of that proposal. Its active frequency columns number H<=min(K_x,K_y)<=min(r_x,r_y)Q. Rank-d row elimination costs O(dN); each resulting basis row remains supported within those H columns. Evaluating its length-M character sum at every internal coordinate costs O(MH), so all d basis rows and all explicit outputs cost O(dMH+dN)<=O(d min(r_x,r_y)N+dN). This is a valid additional structured output test, not permission to bypass raw-input recognition or to call generic dense output cheap.

I also checked the proposed strict-escape family Q=M=s², labels 0<=h<s. Put x label h at row a=h+s v with coefficient eta^{h floor((h+v)/s)}, and put y label h with coefficient 1 at row b=(s-1)h+w, for 0<=v,w<s. The y-row intervals overlap at most twice. For a matching pair, a+b=s(h+v)+w, so each fixed label reaches every target row exactly once, and the x coefficient cancels the carry factor. Hence C[t,h]=M for h<s, rank(C)=1, while the nonzero state count is S=sQ. This eventually escapes every fixed original S<=C Q guard using one-mode x fibers and at-most-two-mode y fibers. The separate graph audit owns its executable checks and complete convolution deliverable; this note records an independent mathematical cross-check only.
