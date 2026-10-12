# Phase 56 gauge-dimension and finite-rank proof review

Review date: 12 October 2026. Decision: **accepted within the stated scope, with the coordinate exposition repaired below**. This review concerns Sections 56.3 and 56.4 of the hash-bound Phase 56 source. It establishes an all-depth dimension upper bound and exact image dimensions for thirteen specified two-stage configurations. The lower-bound witnesses are finite; they do not constitute an all-size dominance theorem.

## 1. Family, domain, and target

Let N >= 2. For an ordered Hamiltonian cycle o on the vertices 0,...,N-1, nonzero complex gains g_i, and a holonomy h outside {0,1}, define

    G[o,g,h]_(ij) = (g_i/g_j)/(1-h) * e_o(i,j),
    e_o(i,j) = 1 if pos_o(i) >= pos_o(j), and h otherwise.

Equivalently, G=(I-W)^(-1), where W sends each cycle vertex to its successor with weight g_successor/g_predecessor and includes h on the closing edge. The formula directly gives the conjugation identity

    G[o,Ag,h] = A G[o,g,h] A^(-1)

for every invertible diagonal A. A common scalar multiplying all gains of one term has no effect on G. Normalize that redundancy by using relative gains u_i=g_i/g_0 with u_0=1.

Fix a positive depth d, nonempty stage term counts q_k >= 1, their sum T, every cycle order, and every interstage permutation P_k. Set

    S_k = sum over t of a_(k,t) G[o_(k,t),u_(k,t),h_(k,t)],
    M = S_d D_(d-1) P_(d-1) S_(d-1) ... S_2 D_1 P_1 S_1,

where every D_k is invertible diagonal. The finite rank audit uses d=2, identity interstage permutation, and M=S_2 D S_1. Other fixed-permutation placement conventions are equivalent by conjugating the adjacent diagonal.

Each term has N-1 gain ratios, one holonomy, and one coefficient, for N+1 parameters. Thus the fixed-order parameter domain has dimension

    P = T(N+1) + (d-1)N.

Work on the dense open set where a designated coefficient in each stage is nonzero and every entry of M is nonzero. The logarithmic comparison further restricts all coefficients to be nonzero, as they are at all audited samples. These are open conditions in an irreducible fixed-order rational parameter space. They are nonempty: positive gains, positive coefficients and masks, and real 0<h<1 give positive Green entries and positive product entries. The matrix determinant need not be nonzero; “nonzero entries” is the relevant condition.

External row and column diagonal multiplications are factored out. On the all-entries-nonzero locus their only stabilizer is the reciprocal scalar pair, so an orbit has dimension 2N-1. Equivalently, the coordinates

    Y_ij = M_ij M_00 / (M_i0 M_0j),  1 <= i,j < N,

identify the quotient with a torus of dimension (N-1)^2. Indeed, row and column scaling makes the first row and first column all ones, leaving these Y_ij as freely variable remaining entries.

## 2. Free gauge action proves the all-depth upper bound

For each stage choose a diagonal A_k with A_k[0]=1 and a nonzero scalar c_k. For each interstage mask choose a nonzero scalar b_k. Act on the parameter coordinates by

    u_(k,t) -> A_k u_(k,t),
    a_(k,t) -> c_k a_(k,t),
    h_(k,t) -> h_(k,t),
    D_k -> b_k A_(k+1) D_k P_k A_k^(-1) P_k^(-1).

The transformed mask is diagonal and invertible. The gain identity gives S_k -> c_k A_k S_k A_k^(-1). Multiplication cancels the inner conjugators, leaving

    M -> (product of c_k)(product of b_k) A_d M A_1^(-1).

Consequently every cross ratio is invariant. The acting torus has dimension

    d(N-1) + d + (d-1) = d(N-1)+2d-1.

Its parameter-space stabilizer is trivial on the chosen open set:

1. In a nonempty stage, equality of any term's nonzero normalized gains before and after the action forces A_k=I.
2. Equality of the designated nonzero coefficient then forces c_k=1.
3. Equality of each invertible mask then forces b_k=1.

Although all the c_k and b_k affect M through one overall scalar, they act independently on the parameter coordinates. Their full dimension must therefore be counted in the fiber. This explicit stabilizer check is what makes the subtraction valid; identifiability of the representation is unnecessary.

Each fiber of the quotient map contains a free orbit of this dimension. Hence

    dim(image closure) <= P - [d(N-1)+2d-1]
                       = T(N+1)-N-d+1.

The image closure of a rational map on the dense open domain is the same as the image closure obtained after deleting the coefficient-zero loci. Such boundary loci cannot enlarge the generic image dimension. Additional parameter redundancies can only lower that dimension. For fixed N,d,T there are finitely many discrete cycle and permutation choices; a finite union retains the same upper bound.

A family dominant onto the generic quotient must therefore satisfy

    T >= ceil((N^2-N+d)/(N+1)).

For 1 <= d <= N-1, write the numerator as (N-2)(N+1)+(d+2). Since 0<d+2<=N+1, the ceiling is N-1. This is a necessary generic-matrix term count. It is not a lower bound for representing any specified structured matrix, including a Fourier matrix. No FFT lower bound follows.

## 3. Explicit two-stage gauge slice

Use relative gains normalized at vertex zero. Let B_k=diag(u_(k,first)) and let alpha_k=a_(k,first). Then

    S_k = alpha_k B_k S'_k B_k^(-1),

where the first term in S'_k has all gains one and coefficient one. Every nonfirst term has relative gains u_(k,t)/u_(k,first) and coefficient a_(k,t)/alpha_k; its holonomy is unchanged. Write E=B_2^(-1) D B_1 and divide all its entries by E_0. The scalar alpha_1 alpha_2 E_0 and exterior B_2,B_1^(-1) disappear under dephasing. Thus the normalized representative is S'_2 (E/E_0) S'_1.

This fixes the first term's N-1 gains in each stage, both first coefficients, and the first mask entry. Its ordinary direct coordinates consist of

- (T-2)(N-1) nonfirst-term gain ratios;
- T holonomies;
- T-2 nonfirst coefficients;
- N-1 mask entries.

The sum is B=T(N+1)-N-1. This is a rational gauge slice on the stated open set, not an unsupported subtraction of independent constraints. The chosen normalization uniquely fixes the gauge there and yields a local product of the gauge orbit with the slice. Since the quotient output is constant along the orbit, raw and reduced direct differentials have the same rank at corresponding points.

## 4. Repair: what the original rank probe actually differentiates

The source prose first introduces this reduced direct chart. Its probe instead retains T(N+1)+N columns: N-1 gain directions, one holonomy and one coefficient for every term, followed by all N middle-mask directions. It uses logarithmic input directions and logarithmic cross-ratio output differentials. The distinction must be stated, but it does not change the audited ranks.

The raw gain columns vary vertices 0,...,N-2, holding the last gain as the reference; the reduced chart uses vertex zero as its reference. Changing the reference gain is an invertible rational coordinate change on the nonzero-gain torus. At any of the checked points, Euler directions x partial/partial x differ from direct coordinate directions by multiplication by an invertible diagonal matrix. No choice of a global logarithm is needed, in characteristic zero or over a finite field.

For the output, the source calculates dY_ij/Y_ij. Multiplication of each row by the nonzero Y_ij recovers dY_ij. In notation for any fixed raw direct coordinate system,

    J_log = diag(1/Y) J_direct diag(x).

Both diagonal factors are invertible on the checked domain. Combining these scalings with the rational gauge slice establishes the stated rank equivalence.

In particular,

    partial G_ij / partial h = (g_i/g_j)/(1-h)^2,

while the probe's holonomy column is h times this derivative. Its gain, coefficient, and mask columns likewise use logarithmic directions. Also,

    dY_ij = Y_ij (dM_ij/M_ij + dM_00/M_00
                 - dM_i0/M_i0 - dM_0j/M_0j)

uses the stronger all-entry-nonzero domain. Ordinary cross ratios themselves only require the first-row and first-column denominators to be nonzero. Every audited witness satisfies the stronger condition, so no conclusion at a zero-entry point is inferred from the logarithmic formula.

The main audit rebuilt both charts, checked every cross ratio before and after normalization, and verified 2N+1 independent raw-kernel gauge directions in every case: 2(N-1) stage-diagonal directions, two stage-coefficient scalings, and one mask scaling. This is a certified gauge subspace of the kernel, not necessarily the whole kernel: target-dominant configurations can have additional parameter redundancy.

## 5. Exact arithmetic evidence and guard conditions

The main audit preserves precisely the original thirteen configurations, seed 560123, and primes 65521 and 1000003. It regenerates the same integer samples without resampling. Gains, coefficients and mask entries lie in 1,...,19; holonomies lie in 2,...,19. The source research program was read as inert text and was neither run nor imported.

A separately authored reconstruction builds W, exactly inverts I-W modulo p, verifies the inverse, and differentiates by dG=G(dW)G. It obtains both the raw logarithmic and reduced direct Jacobians. For each of the 26 cases it records one nonzero minor in each chart, with ordered original row and column indices and its determinant: 52 witnesses in total. Elimination pivot products agree with a distinct blocked Schur-complement determinant calculation. Zeroing the first row makes each tested reduced minor reject. A separate exact dual-number calculation in a direction involving every direct coordinate agrees with multiplication by the rebuilt Jacobian in every case.

Both primes were verified prime by trial division. All gains, holonomies, coefficients and masks required by the logarithmic chart are nonzero modulo either prime. Every 1-h, normalization denominator and output entry is nonzero. Rejection controls cover zero gain, h=1, h=0, zero coefficient and zero mask. The h=0 and coefficient-zero exclusions belong to this comparison domain; they do not assert that an extended direct rational family is undefined at every such boundary point.

Ranks and determinants use exact modular arithmetic, without floating-point tolerances. Fixed-width matrix products first reduce their multiplicands and check

    inner dimension * (p-1)^2 <= 2^63-1.

The conservative maximum is 991*1000002^2=991003964003964, below 9223372036854775807. Elimination product/subtraction bounds and sums of residue matrices also fit. Python scalar calculations use arbitrary-precision integers. Static source review found no int64 overflow in the original bounded cases; that conclusion does not extend to arbitrary larger sizes or primes, for which the original program has no general guard.

A second independent review used pure-Python multivariate dual arithmetic through the explicit Green-entry, product and ordinary-cross-ratio formulas. It rebuilt ten complete direct Jacobians: (N,q1,q2)=(5,2,2),(7,3,3),(8,3,4),(11,3,3),(13,5,5), each at both primes. Their entire matrix hashes, samples and ranks agree with the main reconstruction. This is ten independently rebuilt full matrices, not a second complete 26-case execution. The second review additionally read the full main checker and reconciled all 26 receipts with the original table.

The frozen evidence package passed extraction-manifest checking, a fresh-process replay of all 26 cases and 52 minors, and the independent ten-matrix replay. All 40 regenerated main JSON outputs were byte-identical. The post-replay manifest also passed. The public source-binding file identifies the exact final reports, checker, manifest, cold seal and evidence-package bytes; this prose derivative does not include the programs or archive.

## 6. Characteristic-zero inference and exact quantifiers

The matrix entries, normalization and direct cross ratios are rational functions over the rationals in the direct coordinates. Every audited finite-field point is the reduction of the recorded integer sample and its rational gauge normalization. Every denominator used in the direct Jacobian and chosen minor is a unit modulo the relevant prime.

A nonzero minor determinant modulo p therefore proves that the corresponding rational determinant at that same characteristic-zero point is nonzero. If it were zero over the rationals, its defined reduction would be zero. This is a deterministic nonzero-minor implication, not a claim that arbitrary finite-field ranks always equal characteristic-zero ranks. One successful prime suffices; the second corroborates the same integer geometry.

At a regular characteristic-zero point, image dimension is at least differential rank. Each audited rank r equals min(B,(N-1)^2). The gauge ceiling and target dimension therefore make this lower bound exact for each recorded fixed tuple of cycle orders, and hence for the corresponding finite union of order choices.

Nine configurations have r=(N-1)^2: N=5 with 2+2 terms, N=7 with 3+3, N=8 with 3+4, N=11 with 5+5, N=13 with 6+6, N=17 with 8+8, N=19 with 9+9, N=23 with 11+11, and N=31 with 15+15. Their rational maps are Zariski-dominant and are local holomorphic submersions at a characteristic-zero witness. Each image contains a Euclidean-open neighborhood of some quotient classes. These nine cases have T=N-1, so they attain the necessary generic term-count threshold at precisely the listed sizes in the unrestricted complex-gain model.

Four configurations attain a smaller ceiling: N=11 with 3+3, 4+4 and 4+5 terms have image dimensions 60, 84 and 96; N=13 with 5+5 has image dimension 126. They are not dominant onto their full target quotients.

For each listed configuration the conclusion is existential for the recorded fixed cycle orders and generic in its continuous parameters. It does not assert that every order choice or every point has the rank, that every target class is represented, or that any untested size is dominant. Even dominance does not establish membership of a specified Fourier matrix. The earlier five finite Fourier-existence certificates remain separate evidence and are unchanged by this audit.

No Fourier-specific minimal term count, phase-only or unit-edge transfer, uniform conditioning, fast parameter synthesis, runtime improvement, FFT or integer-multiplication speedup, or external novelty or priority claim is established.
