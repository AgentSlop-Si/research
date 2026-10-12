Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 466bd452430ddc36c47684ecc132cfa37d7a0b7d3da57d77a48801e0782abcaa

---

# Independent bounded review: Phase44 direct compiler obstruction

Review date: 2026-10-11 UTC. Target ID: PHASE44-FULL-F8-20261011.

## Verdict

ACCEPT SCOPED. The supplied report proves that a universal replacement of one unrestricted circulant factor by one equal-three-Green, unit-edge Hamiltonian stage, with arbitrary invertible complex diagonal masks on both sides, is impossible. The exact counterexample is the invertible circulant 2I+X8.

No mathematical repair is required for this bounded claim. Prefer “universal one-circulant-to-one-stage compiler” or “direct substitution of an arbitrary circulant factor” in status cells to avoid using “generic” without specifying its meaning. This review does not close a literature comparison or establish any global four-stage impossibility or novelty claim.

Reviewed candidate report SHA256: 7b0931603089f260a149471705b4e8fc29dcc455db8ad75cdd87f43c3abd85f6.
Reviewed candidate manifest SHA256: 0078fc745eb9907659a77d9f6e7c971a1bb35e6e60a0816939998af45b760285.
Both exact supplied pins and all 9 manifest entries match, including file lengths.

## Independent proof

Let W be a weighted Hamiltonian-cycle permutation matrix with every edge magnitude one and cycle holonomy h not equal to one. Then W is unitary, W^N=hI, and I-W is invertible. Put G=(I-W)^(-1). Conjugate transpose gives

    I-W* = -W*(I-W),
    G* = -(I-W)^(-1)W = -GW,
    G+G* = G(I-W) = I.

The geometric identity

    (I-W)(I+W+...+W^(N-1)) = (1-h)I

also gives G=(I+W+...+W^(N-1))/(1-h). A Hamiltonian cycle has no fixed vertex under a power k with 0<k<N, so each W^k in that range has zero diagonal. Therefore every diagonal entry of G is 1/(1-h). Taking the diagonal of G+G*=I shows that the real part of this number is 1/2.

For the equal-coefficient sum S=G0+G1+G2, it follows that

    S+S*=3I,
    diag(S)=c(1,...,1),
    c=sum_t 1/(1-h_t),
    Re(c)=3/2.

In particular c is nonzero. Write S=(3/2)I+iH with H Hermitian. Hence S is normal, invertible, and every eigenvalue has real part 3/2.

Now suppose C=ASB, where A and B are arbitrary invertible complex diagonal matrices and C has constant diagonal d. Entry j,j gives a_j b_j c=d. If d=0 this is impossible. Otherwise AB=(d/c)I and B=(d/c)A^(-1), so

    C=(d/c) A S A^(-1).

This is a scalar multiple of a similarity, not an assumption that either mask is unitary. Its spectrum is (d/c) times the spectrum of S and is consequently collinear. Diagonal masks with arbitrary amplitudes do not defeat this argument because constant target diagonal forces their entrywise product to be scalar. The condition is necessary only; collinearity is not asserted to be sufficient.

For the cyclic shift X8 e_j=e_(j+1 mod 8), let C=2I+X8. Its diagonal is constantly 2 and its characteristic polynomial is (z-2)^8-1. Thus det(C)=255 and its spectrum contains 1, 3, and 2+i. These three points are noncollinear. Therefore C cannot equal ASB for any admissible S and invertible diagonal A,B.

The proof permits arbitrary Hamiltonian orders and arbitrary unit edge phases. It therefore excludes the replacement in every fixed Phase44 stage, including the more restricted committed common-tree gauge. Simultaneous permutation similarity preserves both stage properties, so allowing it does not help. The proof does not cover independent left and right permutations.

## Exact independent controls

The fresh reviewer program independent_controls.py was authored for this review. It imports only standard Python modules and installed SymPy 1.14.0. It reads candidate files for integrity verification only. Neither the candidate verify_invariant.py nor any original uploaded research program was executed, imported, compiled, or used as a dependency.

All controls pass in exact complex rational arithmetic:

- 24 independent Hamiltonian cycles grouped into 8 three-term stages at N=2,3,4,8, using two deterministic trial samples per size.
- Unit gains include rational non-root-of-unity phases 3/5+4i/5 and -5/13+12i/13, in addition to roots of unity.
- Direct exact matrix inversion, separately from the candidate's geometric-series construction, verifies both inverse identities, unitarity, W^N=hI, G+G*=I and the constant diagonal formula.
- Every stage verifies S+S*=3I, constant diagonal and Re(c)=3/2.
- Arbitrary nonunit complex diagonal A and B=(d/c)A^(-1), with d=2+i, verify constant target diagonal and the scalar-similarity identity at every size.
- An independently constructed 2I+X8 verifies the entire characteristic polynomial, determinant 255, three exact eigenvalues and nonzero signed double-area test -2.
- Deliberate negative controls show failure of the Hermitian-part identity with nonunit internal gains, with nonreal Green coefficients, with unrestricted masks, and with a two-stage product. Trivial holonomy is singular.

These controls support the universal proof; they do not replace it. The candidate's recorded 27-cycle/9-stage controls were inspected as code and receipt, not replayed. The fresh review contributes a distinct 24-cycle/8-stage control set; do not conflate those counts. There is no new interval certificate replay, no frozen-architecture parameter search and no finite-control inference of a universal theorem.

## Architecture and literature boundaries

This is the equal-three-term, unit-edge stage class of the certified Phase44 full-F8 architecture. It is not the broader arbitrary-weight/arbitrary-coefficient one-layer class that also occurs elsewhere in the Phase44 source. The live historical correction specifying one common seven-edge spanning tree per three-cycle stage is retained. The invariant is independent of that gauge detail, so the correction does not weaken the proof.

The separate Phase56 audit explicitly allows independent complex vertex gains, nonunit holonomies and variable complex coefficients. Nonunit gains destroy unitarity, and nonreal term coefficients do not preserve the sum identity. Do not transfer this obstruction to Phase56 or describe Phase56's two stages/seven terms as an improvement within the restricted Phase44 family.

Interstage complex diagonals and multiplication do not in general preserve a single stage's Hermitian-part or constant-diagonal properties. Therefore this argument must not be applied to the full four-stage product. It neither rules out multiple stages per circulant nor restructuring/cancellation across an entire factorization. It does not exclude a proof of the fixed F8 representation by another route.

The two requested primary theorem bodies, Huhtanen 2008 and Schmid et al. 2000, remain unread in the candidate evidence. Their retrieval failures and primary metadata are recorded there; this review did not reattempt access or independently inspect those bodies. Zero additional primary-body comparisons are completed. Eight historical completed comparisons remain historical, not reaudited by this review. No theorem number, pinpoint page, exact factor bound, global implication or source exclusion may be inferred from the elementary obstruction.

The accepted full-F8 interval result, local full-dimensional depth-four corollary and historical counts are premises outside this review. No F8-alone minimum depth, full-F16 membership, global universality, quantitative neighborhood radius, speedup, worldwide originality, priority, new discovery count or rank promotion is established.

## Stopping condition

The bounded independent review is complete. The next evidence required for the separate literature/global-implication task is authorized full primary bodies and an exact architecture-preserving theorem map. No further computation of this single-stage invariant closes that gap.

## Scope and remaining work

The direct obstruction excludes universal replacement of an arbitrary circulant by one equal-three-Green, unit-edge Phase44 stage, even with arbitrary invertible complex diagonal masks. It is not a global four-stage obstruction. Eight historical source comparisons remain inherited; Huhtanen2008 and Schmid2000 primary bodies remain unread. The open implication must preserve four stages, three equal Green terms, unit internal gains, fixed orders/common-tree gauge and allowed nonzero complex diagonal boundaries. Local expressivity and F8-alone realization are different questions. Fresh independent controls cover24 cycles/8 stages; the candidate’s separate27-cycle/9-stage controls are not counted as reviewer controls.
