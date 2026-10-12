Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 84dbd828bb6239ae2b54a21780b65b942fc100212c20c4e45636450c536c40ad

---

# Independent review: Q05 noncyclic endpoint minimax

Verdict: ACCEPT the mathematical claim, for the frozen candidate identified below. No correction to the proof is required. This closes the matching-upper obligation for all finite abelian 2-groups, not only the named mixed-order family.

Reviewed 11 October 2026. The author checker was read as text but was not executed, imported, compiled, or dynamically loaded. All reviewer computation uses the independently written `check_independent.py`. No external write was performed.

## Frozen target

- Candidate ZIP: `Q05_Noncyclic_Minimax_Upper_CANDIDATE_2026-10-11.zip`
- ZIP SHA-256: `7823862a6ef13b5523afce2e37831573ab61fbeb78c724dcc8cfb9a13c298d16`
- Candidate manifest SHA-256: `b979692c72a58e0bfd79ac725aff4c85c736f366b1edf912249f2c5cc4f4bc8b`
- `PROOF.md`: `96b32a10b917a64941a161fee7d52f72905c11434ef79b9b1b48cd4e83f43d53`
- Author `checks/check_noncyclic.py`: `e799df6208dffe058839f342dcf6390aeffaad08330d19159f1e6833bab2f1c2`
- Author `results/EXACT_CONTROLS.json`: `e3ca537ae53159e508b62ce34548276fb100b69ed8c56f819252c05996571f81`

All 15 files listed in the candidate manifest were hash-verified before the independent run. The ZIP hash also matched the author's freeze message. The candidate files were not changed by this review.

## Accepted statement and reasoning

For the unnormalized character table F_G of every finite abelian 2-group G, with arbitrary independent endpoint permutations, the minimum maximum strict upper/lower corner rank is 0 at N=1, 1 at N=2 and N=4, and N/4+1 at every N>=8. This is a characteristic-zero minimax statement. The construction also supplies an upper bound over a splitting field of characteristic other than 2, without claiming the corresponding universal lower bound there.

1. Isotropic involution existence is uniform. If an element has order 2^e with e>=2, its halfway multiple a has order 2 and B(a,a)=1 because 2^(2e-2) is divisible by 2^e. Otherwise the group is elementary abelian and the diagonal map x -> B(x,x) is a homomorphism to {+1,-1}; at order at least 4 its kernel contains a nonzero element. This works for every symmetric perfect pairing, including induced pairings that are not presented in the original diagonal coordinate form.

2. The quotient is valid. A=<a> lies in K=A-perp; K has index 2. Perfectness gives K-perp=A. Therefore the radical of B restricted to K is exactly A, and Q=K/A has a symmetric perfect induced pairing and order N/4.

3. The binary-sum lift is genuinely a permutation. The low bit distinguishes the two members of A; the inner bits enumerate all A-cosets in K; the high bit distinguishes K and t+K. Arbitrary representative or lift choices may create carries into A but do not change this argument. Generators need not be involutions or a vector-space basis.

4. The cut recurrence is exact, including odd cuts. For k<=N/2, put p=floor(k/2), d=ceil(k/2). All columns in t+K survive. Their selected-row span has dimension d because the d representative characters restricted to K are distinct. That span lies in the kernel of the p pair-sums and hence equals this kernel. In the quotient by that kernel, surviving K-columns give exactly the quotient corner at cut p. At k=2p+1, the second member z_p+a survives and supplies the quotient column p. Thus r_G(k)=d+r_Q(p), rather than a shifted suffix recurrence.

5. Reflection is valid for arbitrary binary-sum lifts. Bit complementation gives x(N-1-j)=c-x(j), and simultaneous reversal is nonzero diagonal row/column equivalence. Symmetry of B equates the two corner orientations. Hence r_G(k)=r_G(N-k), which completes the second half of the cut range without imposing any additional group-linearity on the binary labels.

6. The uniform upper is immediate from the quotient column count. Even cuts satisfy r_G(2p)<=L and odd cuts satisfy r_G(2p+1)<=L+1, where L=N/4. At k=2L-1 with L>=2 the quotient corner has a single nonzero column, so equality L+1 holds. The N=4 quotient is trivial and gives (1,1,1). The base cases are correctly separated.

7. The inherited lower matches the same objective. For arbitrary independent endpoints, the critical corner has 2L-1 rows and 2L+1 columns. In a 2-group an odd-size set cannot be invariant under a nonidentity translation, giving d_H>=1. The accepted deficit estimate gives rank at least L+1. Its derivation is analytic over the complex normalized table, with exact rank subsequently transferred through cyclotomic characteristic-zero field extensions. The minimum half-square rank N/4 is a different assertion and is correctly kept separate.

These arguments hold for every group order. The finite controls below are regression evidence, not the induction premise.

## Independent controls

The reviewer implemented fresh exact arithmetic in Z[z]/(z^(M/2)+1) for power-of-two M, using division-free row elimination with integer-content normalization. No author rank routine or author constructor was called. This independently validates the characteristic-zero ranks, rather than treating modular ranks as their proxy.

- Verified all 204 author-reported characteristic-zero corner ranks for every abelian group type of orders 4, 8 and 16, directly from the sealed endpoint labels.
- Verified 2,024 corner ranks for all 28 group types of orders 4 through 64 in GF(769), a third splitting field distinct from the two author fields.
- Independently built 264 randomized recursive endpoint constructions with varied isotropic involutions, complements, quotient representatives, and arbitrary quotient-basis lifts.
- Exhausted all symmetric perfect pairing matrices for C2^2 (4 forms), C2^3 (28 forms), C4^2 (32 forms), and C2 x C4 (4 forms), with three independent constructor choices per form.
- Sampled five perfect symmetric pairings each for C2 x C8, C4 x C8, C2^2 x C8, C2 x C16, C8^2 and C2^6, with two constructor choices per form.
- These adversarial constructions passed 4,596 characteristic-zero and 8,976 finite-field corner checks, including noncanonical induced pairings and carry-producing lifts.
- Independently checked all 3,136 critical 3x5 rectangles of C2 x C4 in characteristic zero; every rank was exactly 3.

The arithmetic and control results are recorded in `RESULTS.json`; the run log is `RUN.log`. Finite-field checks remain algebraic controls only. They are not evidence for a finite-field singular-value statement or an independent universal finite-field lower theorem.

## Complexity and scope review

The supplied direct-product decomposition is an explicit input assumption. Construction of addition and pairing tables costs O(dN^2) bounded-integer operations. Quotient sizes decrease by a factor of 4, so the sum of quadratic table costs is O(N^2). Expected hash-table bookkeeping and the conservative deterministic sorting allowance are properly distinguished; O(dN^2 (log N)^3) is a conservative schoolbook deterministic bit-operation bound. O(N^2) integer-word storage, output of two N-element permutations, and O(log N) recurrence evaluation per supplied cut are consistent with the implementation. The cost of finding a black-box group decomposition is excluded, as it should be.

The proof only outputs permutations and rank certificates. Its row sums are proof operations, not authorized transform stages. The text correctly does not infer an FFT, branch, channel, separator, readout, scalar-operation, memory-bandwidth or routing-complexity improvement.

The shared profile and the inherited pointwise bounds permit the stated exact rank sums at N=8 and N=16; this review does not promote rank-sum optimality at larger N. Historical priority remains unresolved. In particular, prior digit reversal, Kronecker-Fourier structure and low-rank hierarchical ideas are not newly claimed here. No nonabelian, mixed-prime, optimal-gap or approximation-minimax extension follows.

## Scope and remaining work

Accepted conclusion: "Independent-endpoint Fourier minimax equals N/4+1 for every finite abelian 2-group of order N>=8 (bases 0,1,1 at N=1,2,4). A symmetric-pairing isotropic-quotient recursion provides the uniform upper and exact cut profile; the previously accepted critical-rectangle deficit estimate supplies the lower."

Keep separate and open: worldwide priority/theorem-level comparison with general Kronecker-Fourier literature; larger-order minimum rank sums; a universal positive-characteristic lower; optimal/approximation gap questions; nonabelian or mixed-prime groups; and transform/branch/readout complexity claims.
