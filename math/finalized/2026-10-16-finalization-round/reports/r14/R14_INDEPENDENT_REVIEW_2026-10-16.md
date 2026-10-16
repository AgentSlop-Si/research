# Independent audit of R14 mixed-prime Fourier endpoint minimax

Date: 16 October 2026. Scope: mathematical proof, relevance, targeted prior-art check, archive integrity, and independently written exact finite tests. No external state was changed and no program supplied in the archive was executed.

## Decision

**The stated complex-rank theorem passes this independent in-session audit.** For every finite abelian group of order N=4L≥8, the minimum over independent row and column permutations of the maximum upper/lower off-diagonal cut rank is L+1. For N=4 it is 1. I found no mathematical defect in the supplied self-contained proof.

**This is a rank-structure result, not a faster Fourier transform. Global originality is unverified.** A suitable status is “independently checked project-scope corollary of attributed ingredients.” This audit does not certify worldwide priority or constitute external peer review. Do not add it to a list of globally novel discoveries on this evidence alone.

## Material reviewed

- `fft_R14_mixed_prime_PROOF_2026-10-16.md`: full supplied proof, 11,561 bytes.
- `fft_R14_mixed_prime_AUDIT_2026-10-16.md`: full supplied audit, 5,239 bytes.
- `fft_R14_mixed_prime_research_2026-10-16.zip`: manifest, source list, README, research log, saved validation data, and constructor source inspected as data.
- All 13 files covered by the archive's manifest matched both their recorded byte lengths and SHA-256 hashes. This confirms internal consistency, not the historical authenticity of recorded runs.
- The supplied constructor was read but not executed. Its direct-product implementation supports the stated O(kN) word-operation and O(kN) coordinate-word storage accounting. This cost constructs labels only and assumes the cyclic decomposition is supplied.

## Independent mathematical checks

### 1. Orthogonal involutions and the quotient

If one cyclic factor has order divisible by four, its halfway group element and halfway character have order two and pair to one. If there is no such factor, divisibility of N by four forces two distinct even cyclic factors; choosing the element and character on different factors gives the same orthogonality. Thus the required pair always exists.

For H=ker χ and R=ann(x), the pairing between R/⟨χ⟩ and H/⟨x⟩ is well-defined and perfect. Both quotient groups have order L, with no requirement that L be a power of two. This is the decisive removal of the earlier project scope restriction.

### 2. Exact first-half cut identity

For k=2p+e≤N/2 with e∈{0,1}, take the linear map that adds each complete selected character pair and discards the optional extra row. Its kernel has dimension p+e. Restrictions to the entire opposite coset span that kernel: the p+e distinct quotient characters are independent and multiplication by coset constants does not change independence.

After quotienting out this kernel, the remaining columns are precisely the quotient suffix beginning at p. In particular, at an odd cut the second member of column pair p survives. Therefore the identity

    r_A(k)=ceil(k/2)+r_B(floor(k/2))

is correct. Transposition gives the lower-corner identity without requiring either matrix to be symmetric.

### 3. Reflection and attainment

The reflected row and column labels multiply the original matrix entries only by nonzero row factors, column factors, and one global scalar. Hence reflection exchanges the upper cut k with the lower cut N−k without changing rank.

The quotient corners have at most L−p columns or rows. Consequently even first-half cuts have rank at most L and odd ones at most L+1. At k=2L−1, the quotient corner is a nonzero (L−1)-by-1 column, giving rank L+1 whenever L≥2. At L=1 this argument has an empty corner, correctly producing the exceptional profile (0,1,1,1,0).

### 4. Universal lower bound

Let Y contain r rows, Z contain h columns, I be the complementary n=N−r rows, and U be the normalized character matrix. Write C=U[I,Z]*U[I,Z]. Then 0≤C≤Id and U[Y,Z]*U[Y,Z]=Id−C.

With d=h−max_{s≠0}|Z∩(Z−s)|, character orthogonality gives

    tr(C²) ≤ hn/N − d r n/N².

The nullity of U[Y,Z] is the multiplicity of the eigenvalue 1 of C, at most tr(C²). Thus

    rank U[Y,Z] ≥ rh/N + d r(N−r)/N².

If gcd(h,N)=1, a nonzero translation cannot preserve Z: its nontrivial orbit length would divide both h and N. This proves d≥1. At r=2L−1, h=2L+1, N=4L, the gcd is one and the bound becomes

    rank ≥ L + (4L²−4L−1)/(16L²) > L  for L≥2.

The fraction is already 7/64 at L=2 and is positive thereafter. Integer rank is therefore at least L+1 for every independent ordering. This lower proof uses complex positivity/orthogonality, and must not be transferred to arbitrary finite characteristic without a separate argument.

### 5. Approximation statement

The supplied singular-value index is correct: C has h=2L+1 eigenvalues, so the (L+1)-st descending singular value squared of U[Y,Z] is 1−c_(L+1), where the c's decrease. The trace-of-square bound yields the displayed δ_N. It is positive for L≥2.

The statement is a non-optimal normalized operator-error obstruction. Its displayed bound decays as δ_N ~ 1/sqrt(2N); it does not supply a size-independent approximation barrier.

## Fresh independent tests

`check_r14_independently.py` was written for this audit from the mathematical statement. It does not import or execute either supplied Python program. It finds an orthogonal pair by brute-force enumeration of involutions, constructs subgroup representatives with independently randomized pair choices/order, and computes ranks exactly using SymPy 1.14.0 cyclotomic number fields.

Results: **PASS, 34 constructions, 17 distinct abelian group types, 1,856 rank calls including empty and quotient cuts.** Two fixed seeds were used per type. All upper and lower cuts, first-half quotient identities, reflection identities, and claimed maxima were checked.

Tested presentations:

    C4; C2×C2;
    C8; C4×C2; C2×C2×C2;
    C12; C2×C2×C3;
    C20; C2×C2×C5;
    C24; C4×C2×C3; C2×C2×C2×C3;
    C28;
    C36; C4×C3×C3; C2×C2×C3×C3;
    C40.

The maximum ranks were respectively 1 at N=4 and N/4+1 otherwise. Full profiles are in `independent_checks.json`. These finite tests support implementation and indexing correctness; the universal result rests on the proof above. This test suite is neither a transform benchmark nor a re-execution of the submitted verification suite.

## Prior-art assessment and evidence limits

Delvaux and Van Barel's 2007 paper already studies Fourier Kronecker products for arbitrary finite abelian groups and constructs rank-deficient submatrices from subgroup-associated rank-one blocks. This is supported by the [publisher record](https://doi.org/10.1016/j.laa.2007.05.009) and [institutional TW477 record](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW477.abs.html).

Indexed author-preprint text dated 15 November 2006 includes Section 3.1, its conclusion, and a discussion of Theorem 14's rank-one-block construction. These portions reinforce the attribution, but do not establish whether the precise simultaneous-cut minimax equality was already stated or follows immediately. [Indexed preprint](https://citeseerx.ist.psu.edu/document?doi=8e34019b75494fa56d9b8791527fcaed304a7ff9&repid=rep1&type=pdf)

The direct institutional PDF redirected to authentication; the indexed mirror's full-file retrieval returned HTTP 403. I did **not** read the full TW477/final-paper body. No conclusion of global novelty or complete equivalence to that paper is justified. Absence of a matching targeted search result is not novelty evidence.

R14 already discloses these limitations and attributes the ingredients appropriately. The safe contribution claim is the explicit project-scope extension and checked derivation. A full theorem-by-theorem comparison, including generalized support-weight literature, remains needed before any stronger priority claim.

## Meaning for the faster-FFT goal

The result rules out obtaining constant or logarithmic off-diagonal cut rank merely by independently reordering a full Fourier character matrix, including mixed-prime orders divisible by four. It therefore closes a specific representation shortcut within this research approach.

It gives no sub-N-log-N recurrence, arithmetic circuit, transform implementation, or speed measurement. It also gives no universal Omega(N log N) algorithmic lower bound: final-matrix cut rank alone does not bound the complexity of arbitrary sparse multistage factorizations. The label constructor's speed must not be substituted for transform cost.

## Recommended wording

“For finite abelian groups of order N divisible by four, the attributed Fourier endpoint-rank argument extends to the exact independent-permutation minimax N/4+1 for N≥8, with N=4 exceptional. The proof passed an independent in-session mathematical audit and exact finite checks. This is a project-scope corollary; worldwide originality is unverified and no faster FFT is claimed.”

