# Independent review: order-5q proper q-multiple endpoints

Date: 2026-10-19 UTC. Verdict: **PASS**, for the exact statement below. No proof repairs are required.

## Accepted scope and frozen binding

For every prime q>5, N=5q, every primitive Nth root zeta, and every arbitrary binary N-by-N matrix R, define D[r,c]=R[r,c] zeta^(rc). Neither square Gram can equal dI when d is one of 2q, 3q, 4q. Either Gram would imply the other because D is square and d>0.

This review accepts only these three endpoint exclusions. It does not claim a complete order-5q classification, resolve 4q<d<5q or d<=q, extend to other orders, establish historical novelty, improve an FFT, or close an owner item. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No external writes were performed.

The audited candidate is `fiveq_endpoints_20261019_1815`:

- REPORT.md SHA-256: c14ab1fc4ed3325972cfb7fc8ae1474ed705dae8dde725b397f9323aa6fc94bf
- MANIFEST.json SHA-256: 74d010baa9add435eae553526c372ca958dc979772bf1c0df624b342c2f9e42c
- verify_endpoints.py SHA-256: 41bd5634cf97a0b9ef7c4aa42045d6d03ecaacbc9a69be7726c7fd61acf3df91

All 18 manifest-bound files and the manifest seal were checked. All four frozen accepted-source copies matched their original local source paths. The full candidate was copied to `frozen_author_packet` without editing it. A separate clean copied rerun reproduced all 18 manifest-bound files byte for byte; both candidate and independent RUN.stderr files were empty. See AUTHOR_PACKET_INTEGRITY.json and AUTHOR_RERUN.json.

## Symbolic proof audit

1. **Both Grams and both degrees.** If D*D=dI with d>0, D is invertible and D*=dD^(-1), hence DD*=dI; the converse is identical. The diagonal entries of both identities are exactly the row and column support counts because each supported entry has modulus one. Column regularity in coverage is therefore available and has not been assumed separately.

2. **Original phase is preserved.** The stated e_5 and e_q are orthogonal idempotents modulo 5q. They sum to 1, so multiplication of actual CRT row and column indices gives rc=e_5 au+e_q bv modulo 5q. Thus zeta^(rc)=alpha^(au) beta^(bv) literally. Alpha and beta have the required orders for every primitive choice of zeta. There is no rephasing or change of Fourier target.

3. **Primitive binary cancellation is valid.** If both row coordinates differ, the two nonzero character multipliers permute the corresponding prime coordinates. Since alpha beta=zeta, the products alpha^i beta^j with i<4, j<q-1 span Q(zeta); their number is phi(5q), so they are a basis. Reduction gives the stated four-corner relation. It expresses epsilon[u,v] as an integer sum A[u]+B[v]. Two varying integer arrays would give range at least two on the full Cartesian product, impossible for a binary array. One coordinate is therefore constant. The zero subset is exactly a union of full q-lines or a union of full five-fibers, including empty/full degeneracies. Undoing multiplier permutations preserves these kinds of cycles.

4. **Coverage uses arbitrary supports.** For a supported (r,c), precisely q+4 rows agree with r in at least one CRT coordinate, counting r once. Since d=kq>=2q>q+4 for q>=7, at least one of the d supporting rows of column c differs in both coordinates. Its orthogonal overlap contains c; primitive binary cancellation supplies a full cycle through c contained in S_r. This works separately at every supported entry and does not assume any global support pattern.

5. **Canonical geometry and size equation.** Defining A_r and B_r to be all full lines/fibers makes the obtained union canonical. The union consists of ell_r disjoint lines, plus (5-ell_r) additional points for each of f_r full fibers. Hence d=ell_r q+(5-ell_r)f_r. Every full line contributes q distinct entries, so ell_r<=k. Because k<5 the support is proper, and f_r=q would make it full. Thus 0<=ell_r<=k<5 and 0<=f_r<q are both justified before arithmetic is used. No accidental extra cycle is omitted.

6. **The f=0 branch is handled correctly.** At an endpoint, q divides (5-ell_r)f_r. Here 1<=5-ell_r<=5 and q is prime >5, so q divides f_r. Its established range forces f_r=0, and the degree equation then gives ell_r=k. This includes pure-line supports from the start. The argument does not transplant an interior nonempty-fiber or singleton-fiber claim to an endpoint.

7. **No common-group support is assumed.** After arithmetic, A_(a,b) is an arbitrary k-element subset and can vary with both a and b. There is no step identifying A values across a first-coordinate group, or imposing a shared assignment/permutation. The next step works on the actual five independently chosen sets with a common b.

8. **The final order-5 obstruction has the correct factor.** With b fixed, different rows a,a' have overlap (A_(a,b) intersect A_(a',b)) times the entire q-coordinate. Beta contributes 1, so their exact row Gram is q times a binary fifth-root subset sum. Its vanishing means the intersection is either empty or all five coordinates, by Phi_5. The latter is impossible because its size is at most k<5. Hence all five k-element sets are pairwise disjoint. Their union would have size 5k>5. This excludes each of k=2,3,4 without additional regularity or support assumptions.

9. **The smallest prime is safe.** At q=7, the three degrees are 14,21,28 and the exceptional row count is 11. Coverage therefore applies. The canonical ranges are ell<=k<=4 and f<7, and gcd(7,5-ell)=1. The final universe still has exactly five coordinates. There is no q=7 equality, strict-inequality, or partner-selection exception.

10. **Scope is not silently broadened.** The proof deliberately excludes k=1 and k=5 from its contradiction. At k=1, five disjoint singleton line sets are possible; at k=5 a full fifth-root overlap vanishes. These are correctly represented by positive divisor controls. The earlier accepted middle/upper results are provenance bindings, not black-box endpoint assumptions. Bibliographic novelty/priority was not independently researched and is not part of this PASS; the elementary cancellation proof is self-contained.

## Independently authored exact controls

`check_endpoints_independently.py` was authored independently before inspecting the candidate checker. It imports only the Python standard library. It uses direct integer polynomial division by Phi_(5q)(X)=Phi_q(X^5)/Phi_q(X), rather than evaluating roots numerically. Row and column Gram signs are their actual respective signs, and diagonal polynomial remainders are also verified. No historical checker is imported or executed by this independent program.

The final run passed:

- 37,950 actual-index CRT phase products at q=7,11,13,17,19,23.
- 1,350 exact coverage bounds across all original rows at those primes and all three k values.
- 169,500 full original-index Gram entries, including both orientations and diagonals, at q=7,11,13. Positive controls at d=1,5,q,5q use contiguous row groups and arithmetic-progression column groups, a different valid divisor-mask construction from the candidate's CRT-diagonal controls. Negative controls cover all three endpoints and include both constant group line sets and line sets changed by b-dependent permutations of the five row coordinates. Both row/column degree counts hold; both Grams fail. Every distinct-b row overlap vanishes, isolating the needed same-b obstruction.
- 67,394 actual canonical mixed-cycle supports at q=7,11, with maximal line/fiber sets recomputed from the support rather than assumed. The only endpoint supports are the 10 two-line, 10 three-line, and 5 four-line choices, all with zero full fibers.
- 495 endpoint degree equations for all primes 7<=q<1000, allowing ell=0,...,5 and f=0,...,q. Only (ell,f)=(k,0) occurs. Scope guards retain mixed solutions at composite q=9 and smaller q=3, demonstrating why the coprimality argument cannot be applied without its hypotheses.
- 34,816 complete binary corner assignments at q=7,11. Exact polynomial coordinates and full rank modulo 1,000,003 independently certify the rational CRT basis at each test prime; full modular rank implies full rational rank. The valid binary kernel arrays are precisely 158 and 2,078, respectively, matching the parallel-cycle count 2^5+2^q-2. Every accepted array was checked at every primitive choice of zeta, giving 86,912 exact zero controls. All 119,820 one-entry toggles were nonzero.
- 6,024 exact fixed-b pair sums across q=7,11,13,17,19,23 and k=1,...,5. Zero occurs exactly for empty or full-five intersections. A separate combinatorial search gives maximum disjoint collections floor(5/k), which are below five for the three excluded k values. The k=1 and k=5 controls guard the proper endpoint boundaries.

These are exact finite controls supporting the symbolic all-prime proof. They are not an exhaustive arbitrary-square-mask search or a substitute for the proof.

## Candidate checker and packaging audit

The candidate checker was also read in full. Its actual-index polynomial arithmetic, Gram orientation, diagonal checks, regular negative masks, arbitrary five-row enumeration, canonical support enumeration, and source hashing agree with its stated scope. Its 406,250 arbitrary five-row tuples are exactly twice [10^5+10^5+5^5], with q=7 and q=11. Its 4,500 exact order-5 pair checks are twice [10 row pairs times (10^2+10^2+5^2)]. No square-mask exhaustiveness is claimed.

No mathematical gap, false positive construction, hidden common-group assumption, cancellation mismatch, or scope inflation was found. No repairs are required for the frozen proof.
