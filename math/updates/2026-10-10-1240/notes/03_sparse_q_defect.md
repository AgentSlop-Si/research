# HERO17 Phase 21 independent mathematical and cost audit

Date: 10 October 2026. Scope: the reciprocal q-factorial kernel spectrum, raw-input sparse-q-defect evaluator, and Green-character Hankel multiplication in the Phase 21 archive.

## Conclusion

The constructive result is valid in its stated exact-field setting. For odd N and a supplied primitive 2N-th root, the specified reciprocal q-factorial kernel has a complete, explicit O(N) spectrum evaluator. A fresh length-N coefficient vector whose q-recurrence defect has k nonzero coefficients has a complete length-2N padded transform in O((k+1)N), including a scan that finds its defects.

This is a structured-input result. It does not give a linear-time transform of arbitrary fresh inputs. The arbitrary-input forcing polynomial contains N−1 independent coefficients; evaluating that forcing remains a Fourier evaluation problem. Applying the associated full-rank Hankel chart to a general vector still uses ordinary transforms.

The submitted seven-row operation table is reproducible by independent closed-form accounting. At N=243, its proposed method costs 25,487 and its power-of-two comparator costs 25,475: the proposal loses by 12 operations under that convention. Two qualifications are required: the executable omits inverse radix-3 scalar negations from its ledger, and its actual fast fallback is limited to radix-2/3-smooth lengths. Neither qualification invalidates the recurrence theorem.

## Mathematical evidence and provenance

The proof certificate, implementation text and benchmark definitions were inspected. Only a newly written standard-library verifier was executed. It reconstructs recurrence propagation, direct monomial-sum oracles, mixed-radix decimation-in-frequency transforms and a separate radix-2 convolution. The original archive's 15 manifest entries passed their source integrity check; those checks are provenance, not extra mathematical tests. The public portable verifier uses only the selected numerical comparison table and does not require the original archive.

Original archive and mathematical source hashes are recorded in SOURCE_MANIFEST.json. Historical predecessor claims are not reaccepted by inclusion in the source lineage.

## Why the recurrence works

Put L=2N, q=eta^8, rho=eta^2, phi_t=product from j=1 through t of (1−q^j), and h_t=rho^(t²)/phi_t. Because N is odd, gcd(8,2N)=2, so q has order N; every phi_t for 0≤t<N is nonzero. Also rho=q^(4^−1 mod N). The adjacent-coefficient ratio gives

    (1−q^t) h_t = eta^(4t−2) h_(t−1),  1≤t<N.

Consequently the polynomial H(z)=sum h_t z^t satisfies

    H(z)−H(qz) = eta² z H(eta⁴ z) − eta^(−2) h_(N−1) z^N.

The final term cancels the degree-N boundary term; omitting it changes the polynomial identity. At z=eta^j, this becomes

    Y_(j+8) = Y_j − eta^(j+2)Y_(j+4) + eta^(Nj−2)h_(N−1).

The step j→j+4 has exactly two cycles of length N. Two direct Horner values per cycle give the seeds at 0,4 and 1,5. Each remaining value is assigned once, in 2N−4 updates. No cyclic linear system is solved, and no recurrence pivot can become singular. Direct seeds also remove any need to assume uniqueness from periodic recurrence constraints alone. The independent controls check every closing equation as well as the forward propagation.

The four Horner evaluations, root table, q-factorial preparation, and output materialization each take O(N). Root-order validation by exponentiation also fits this bound. The supplied source factors the integer 2N by trial division; that is not free integer work, but is O(sqrt(N)) trial divisions and does not spoil the O(N) word-operation bound. This is not a bit-complexity or numerical-stability statement.

## Singular cases and setup contract

- N must be odd and at least 3. Even N can reduce the order of q and changes the orbit structure; the source explicitly rejects it. N=3 works, including its two length-3 orbits.
- The field characteristic must not divide 2N. The field must contain the supplied primitive 2N-th root. In the prime-field implementation, p is assumed prime and 2N must divide p−1.
- The source validates the root order but does not certify primality. For example, N=3, p=91, eta=12 passes the order and congruence tests, but 1−q has gcd 13 with 91. This is outside the theorem's hypotheses and would invalidate the denominator/dimension arguments. A production boundary needs a trusted prime-field object or a prime certificate; the audit does not treat a composite modulus as a theorem counterexample.
- The Green chart further assumes nonzero alpha and beta, delta=1−alpha^N−beta^N nonzero, and nonzero gamma=N^−1 sum q^(−t²). The odd-order quadratic Gauss factor is nonzero in the admitted field setting; the code checks it. These extra chart restrictions are unnecessary for the standalone kernel-spectrum and sparse-defect theorems.
- Prime/root search and primality certification are excluded from the source's supplied-root arithmetic model. All test searches are setup for the verifier, not evidence that search is O(N). The power-of-two comparator additionally assumes its own primitive padding root is supplied. The test fields support both sets of roots.

## Raw-input sparse defects and the dense-input boundary

For a raw vector a, define

    r_t=(1−q^t)a_t−eta^(4t−2)a_(t−1),  1≤t<N.

The same polynomial coefficient comparison adds R(z)=sum r_t z^t to the right-hand side. Its spectral recurrence therefore subtracts R(eta^j). A complete scan finds all defects with four source-ledger operations per position; positions are not supplied by the caller. Each nonzero coefficient contributes a full length-2N geometric progression. Four direct seeds and 2N−4 recurrence updates then materialize every output.

For a fixed support of size k, a_0 and the k defect values determine all N coefficients because 1−q^t is nonzero. The corresponding linear space, allowing zero values on the chosen support, has dimension k+1. Requiring every chosen value to be nonzero gives a subset of that space. Taking a union over supports does not change the fact that the method exploits a restricted defect pattern.

For unrestricted a, the map (a_1,…,a_(N−1))→(r_1,…,r_(N−1)), at fixed a_0, is lower triangular with nonzero diagonal. Thus every forcing coefficient can vary independently. This is an exact explanation of the restriction of this architecture, not a lower bound for all Fourier algorithms.

The default source threshold is k≤3. Above it, the code scans first and then invokes an ordinary transform. Changing the threshold to grow as N would remove the claimed fast worst-case fallback: the direct sparse-forcing route can be quadratic. With fixed threshold, the actual implementation is O(N log N) for N=3^m. More generally, source mixed_ntt chooses radix 2, then 3, and otherwise the entire remaining size. For N=5^m it uses a direct N-point butterfly after the initial split, costing 4N²+3N field operations for the forward transform. Calling this a prime-radix fallback, or promising the implemented O(N log N) bound at every bounded-prime-factor length, is too broad. A general small-prime factor planner would repair that implementation limitation.

## Hankel application and what is actually saved

With diagonal factors A_a=phi_a alpha^(−a), B_b=phi_b beta^(−b), the chart has entries delta gamma A_a B_b h_(a+b) when a+b<N, and zero otherwise. Reverse and scale the input using v_j=B_(N−1−j)x_(N−1−j). For the linear convolution c=h*v,

    (Wx)_a=delta gamma A_a c_(N−1+a).

Padding to 2N avoids wraparound because the convolution length is 2N−1. The recurrence prepares the fixed kernel spectrum in O(N), but a general v still requires a forward transform, pointwise products, and an inverse transform. All output diagonal factors and inverse normalization are included in the source field ledger. The nonzero antidiagonal makes this chart full rank; that does not make its action a complete Fourier transform. This audit verifies the displayed weight formula and its application; the earlier Phase 20 derivation identifying those weights with Green operators is not rederived here.

The first query saves one kernel transform relative to a same-length, unprepared three-transform convolution. On subsequent queries, a conventional algorithm also caches the fixed kernel spectrum and uses two transforms. The source methods themselves recompute the spectrum on each apply call; repeated-query caching is an available implementation optimization, not automatic behavior of those calls.

## Exact ledger reconstruction and the qualification

Let P(e)=bit_length(e)−1+popcount(e) for e>0, and V(d)=P(d)+sum P(d/f) over distinct prime divisors f of d. For N=3^m, direct enumeration of the source loops gives:

    Common mixed preparation C = 13N+7+V(2N)+2P(N)
    Kernel recurrence K = 14N−17
    One mixed transform T = 3N+(20/3)Nm
    Chart online work = 2T+5N
    Proposed first-query total = C+K+2T+5N
    Same-length three-transform total = C+3T+5N

For S=the least power of two at least 2N−1, the comparator has common preparation

    C2 = S+12N+3+V(N)+V(S)+2P(N)

and total C2+(9/2)S log2(S)+S+3N. These formulas reproduce every submitted total without executing submitted code.

| N | Proposed ledger | Same-length three transforms | Power-of-two three transforms |
|---:|---:|---:|---:|
| 9 | 597 | 635 | 951 |
| 27 | 2,135 | 2,395 | 2,306 |
| 81 | 7,434 | 8,720 | 10,998 |
| 243 | 25,487 | 30,931 | 25,475 |
| 729 | 86,087 | 107,245 | 116,491 |
| 2,187 | 287,297 | 365,317 | 528,514 |
| 6,561 | 949,238 | 1,227,004 | 1,163,477 |

The proposed ledger beats the same-length comparator in all seven cases and the specified power-of-two comparator in six. It does not beat every conventional implementation, and a least-length padding choice is not an optimal arithmetic circuit. Both submitted NTT implementations still charge trivial multiplications that could be optimized. These are operation ledgers, not measured runtimes.

The specific accounting discrepancy is phase21.py line 197: the inverse transform evaluates −plan.three_const without incrementing the addition/subtraction ledger. It does this once per radix-3 recursive node, N−1 times. Elsewhere, such as the odd boundary term, field negation is charged through minus(0,x). With negation charged consistently, the literal submitted executable totals are larger by N−1 for both mixed methods. At N=243 they become 25,729 and 31,173; the power-of-two total stays 25,475. At N=6,561 the proposed literal total becomes 955,798.

This is easily repairable without any extra field operation: retain the positive three_const and swap the two inverse center+asym and center−asym output assignments. The existing two additions/subtractions then supply the required signs. That repaired schedule realizes the original table, including the 12-operation loss. Alternatively, preparing one cached negative constant adds one operation. The audit distinguishes these choices and does not silently call the current source fully charged.

For the source sparse path, online arithmetic is 20N−25+6kN, and preparation is V(2N)+2N+2 when 3 divides N, or V(2N)+2N otherwise. These include defect detection, seeds, boundary scalars, residual accumulation, and propagation. They exclude integer indexing, comparisons, reads, and writes as numerical entries. The source actually performs O(N) input reads and output writes, so those costs do not alter the asymptotic theorem. It is inaccurate to imply that literal I/O operations appear in the scalar-operation totals. The independent verifier separately checks exactly 2N output assignments and, in its implementation, 6N raw-coefficient accesses. Its character update carries r_t eta^(jt) directly, an equivalent two-operation progression rather than the source's three-operation progression; functional checks do not pretend to reproduce identical instruction traces.

## Independent controls

All independent controls passed:

- 2,736 kernel bins checked by direct monomial sums, over 16 odd lengths through N=243, with both eta and eta^−1 orientations; also checked against the fresh mixed transform.
- 61,378 complete sparse-transform bins checked through N=6,561, with zero through three defects, including zero initial coefficients, the all-zero input, and checks of all recurrence closing equations.
- All 343 raw vectors in F7³ tested exhaustively, covering 2,058 output bins.
- Every convolution coefficient and every chart output compared using recurrence preparation, conventional mixed transforms, and the independent radix-2 transform at all seven benchmark sizes. Direct Hankel sums checked all rows through N=243 and 20 rows per larger size, 420 direct rows in total.
- An N=6,561 dense input had 6,560 nonzero defects. The forced dense recurrence agrees with the ordinary transform, while the source's default decision rule correctly selects its ordinary fallback. This verifies correctness without claiming that dense forcing is fast.
- A missing-forcing negative control changed 14 of 18 bins; invalid lengths and nonprimitive roots were rejected by the verifier. Composite-modulus and non-2/3-smooth examples document the setup and fallback boundaries. The inverse-output-swap repair identity passed 300 field cases.

Reproduction: see REPRODUCE.md. The portable independent_controls.py writes INDEPENDENT_RESULTS.json beside itself in a disposable working copy. Its small-prime searches and deliberately forced dense recurrence are audit work, not part of the claimed fast algorithm. The source hashes, portable verifier hash, numerical results, and operation-count distinctions accompany this note.

## Classical ingredients and unresolved originality

Coefficient-shift generating-function identities, constant-order recurrence propagation, geometric-progressions for sparse spectral contributions, and Toeplitz/Hankel reduction to convolution are established mathematical ingredients. The specific specialization can still be useful as a fully explicit structured-kernel preparation method. This audit establishes correctness and boundaries; it does not establish historical priority.

The source's cited Garoufalidis–Koutschan paper proves preservation of q-holonomicity under root-of-unity twisting and rational substitutions. It is relevant context, but its abstract alone does not prove that this exact specialization is already present: https://arxiv.org/abs/1201.3353. A dedicated prior-art search would be needed for a novelty claim.

OpenAI Math problem 130 separately documents a uniform all-length exact complex DFT and convolution bound O(N(log N)^(1−10^−13)), with root-order selection and scalar preparation included and the chosen root supplied. Its unrestricted exact-complex model differs from these prime-field experiments; Phase 21 does not improve that general-transform result: https://github.com/openai/math/blob/main/lean/docs/130.md.

## Recommended status

Accept as a verified structured-kernel O(N) preparation theorem and an input-adaptive sparse-q-defect transform, with the field/root assumptions stated. Preserve the arbitrary-input obstruction, both comparator baselines, the N=243 loss, first-query versus cached-query distinction, and absence of numerical/bit-complexity guarantees. Qualify the current implementation ledger and fallback range as above. Leave unrestricted exact linear-time DFT and historical originality unproved.
