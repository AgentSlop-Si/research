# Rank-three prime-cube separation settles N = 1331

Date: 18 October 2026 UTC. Owner: M-RECTANGLE-TILING, priority 42.
Status: author-side extension; independent review pending. No external writes.

## Result

The complex cyclic Fourier disjoint-rectangle optimum at **N=1331=11³ is 175,692 = N D_N**, where D_N=11+121=132. Every optimum contains exactly N rank-one tiles; each is a full subgroup-coset × annihilator-coset rectangle, with unordered side sizes {11,121}.

The new structural theorem is:

**Prime-cube rank-three separation.** If p≥5 is prime, any rectangle of F_(p³) having complex rank at most three satisfies min(|R|,|C|)≤4p.

In the stronger residue-occupancy form, any rectangle whose row and column sets each occupy at least five distinct residue classes modulo p² has rank at least four. This is proved by an explicit four-by-four minor selection and a two-step cyclotomic-field argument. It is not inferred from sampling.

At p=11, the rank-three density is at least D_N/N + 1/484. Together with the accepted rank-two result and the stable-rank bound for rank≥4, this gives the useful (not claimed sharp) global inequality

    total cost ≥ 175,692 + A_(rank≥2)/484.

Here A_(rank≥2) is the total entry area of higher-rank tiles. The previous accepted domains plus this isolated new length cover every N from 2 through 1858. The next residual in that union is 1859=11·13², where rank three remains the problematic rank.

## 1. Exact model and dependencies

Write F_N[k,j]=ζ^(kj), with ζ a primitive N-th root. Replacing ζ by its inverse gives the previously used convention without changing any statement. Partition the entries into nonempty, disjoint Cartesian rectangles R_t×C_t. A tile with side sizes a_t,b_t and actual complex rank r_t costs r_t(a_t+b_t). There is no overlap, cancellation, or sharing between tiles.

The accepted rank-one coset/density result, sharp rank-two density, and complex stable-rank inequality are taken from the two frozen inputs:

- rectangle_rank_two_20261018_1240/REPORT.md
- rank_two_review_20261018_1248/REVIEW.md

The accepted rank-two theorem is not being reproved or re-enumerated here. The new proof is self-contained apart from elementary cyclotomic and determinant facts proved or explained below. The web literature check located Osgood–Siripuram–Wu, *Discrete Sampling and Interpolation: Universal Sampling Sets for Discrete Bandlimited Spaces*, https://arxiv.org/abs/1204.0992, as context for the elementary universal-minor lemma. That paper is not needed as a black-box theorem.

This remains a complex-coefficient, disjoint/no-sharing endpoint-incidence model. Root supply and coefficient preparation, storage, and I/O are separate. The inherited possible N extra additions for literal zero-initialized accumulation are unchanged. There is no claim about finite-field rigidity, arbitrary basis changes, unrestricted Fourier circuits, production performance, or worldwide novelty. Parent TO RESEARCH status and priority remain unchanged.

## 2. An elementary universal-minor lemma

**Lemma 1.** Let q=p^m, p prime. Let k≤p. If k row indices are pairwise distinct modulo p and k column indices are distinct modulo q, their k-by-k Fourier minor is nonsingular. The transposed statement holds.

**Proof.** Sort the row exponents e_1<…<e_k, and put x_j=ζ^(c_j). The alternating integer polynomial det[x_j^(e_i)] is divisible in Z[x_1,…,x_k] by V(x)=∏_(i<j)(x_j−x_i). Write its quotient as S(x). Taking the limit as all x_j→1, or performing successive divided differences, gives

    S(1,…,1) = ± ∏_(i<j)(e_j−e_i) / ∏_(i<j)(j−i).

The sign is immaterial. This is an integer. Its numerator and denominator are both p-adic units: the e_i have distinct residues modulo p, and 1≤j−i≤k−1<p. Thus S(1,…,1) is not divisible by p.

In Z[ζ], quotienting by the ideal (1−ζ) sends ζ to 1 and gives F_p, because Φ_(p^m)(1)=p. Hence S(ζ^(c_1),…,ζ^(c_k)) reduces to the nonzero element S(1,…,1) mod p. It cannot vanish. The x_j are distinct, so V(x) is also nonzero. QED.

The familiar prime Fourier nonvanishing-minors fact is the m=1 case, including all the two- and three-by-three prime minors used below.

## 3. Selecting manageable four-point patterns

Take any set S occupying at least five residues modulo p², and first choose five indices with distinct such residues. If they occupy at least four residues modulo p, choose four in distinct residues: call this type U.

Otherwise at most three residues modulo p occur. If a class contains at least four selected indices, choose four from it: type A=(4). If a class has exactly three and no class has four, choose those three and any other index: type B=(3,1). In the remaining case every class has size at most two; five selected indices in at most three classes force two classes of size two, giving type C=(2,2).

All selected indices remain distinct modulo p². Thus each side offers a four-element subset of type U, A, B, or C. It remains to show that every pair of selected types gives a nonsingular minor.

- If either side is U, Lemma 1 at q=p³ applies.
- If a side is A, write its indices as r_0+p u_i. The u_i are distinct modulo p. Column scaling removes r_0, leaving a p²-order Fourier minor with columns distinct modulo p². Lemma 1 at q=p² applies.
- Only B–B, C–C, and B–C (or its transpose) remain. These are established next.

## 4. Three small cyclotomic block arguments

Put ζ=ζ_(p³), η=ζ^p, ω=ζ^(p²), K=Q(η), and L=Q(ω). Then [Q(ζ):K]=p and [K:L]=p. In particular, 1,ζ,…,ζ^(p−1) are linearly independent over K, and 1,η,…,η^(p−1) are linearly independent over L. Translation of a row set or column set merely scales the opposite coordinates by nonzero numbers and does not affect nonsingularity.

### 4.1 Type B against B

Translate the triple residue classes to zero. Write the rows as p u_1,p u_2,p u_3,t and columns as p v_1,p v_2,p v_3,q. Here t,q are units modulo p, and both the u_i and v_i are pairwise distinct modulo p. Every entry except the bottom-right ζ^(tq) lies in K. Expanding by that entry writes the determinant as

    A + ζ^(tq) B,   A,B∈K,

where B is the nonzero prime Fourier determinant det[ω^(u_i v_j)]_(i,j≤3). As tq is not divisible by p, 1 and ζ^(tq) are K-independent. The determinant is nonzero.

### 4.2 Type C against C

Write the rows as p u_1,p u_2,t+p u_3,t+p u_4 and the columns as p v_1,p v_2,q+p v_3,q+p v_4. Here t,q are units mod p, and the two u values in either row class, and the two v values in either column class, are distinct mod p.

Only the bottom-right 2-by-2 block contains the factor z=ζ^(tq); after removing it, all entries are in K. The determinant is A_0+A_1 z+A_2 z² with A_i∈K. Its coefficient A_2 is, up to sign, the product of the top-left 2-by-2 determinant and the phase-removed bottom-right 2-by-2 determinant. Both are nonzero: after row/column scaling they are prime Fourier minors with distinct residues. Thus A_2≠0. Since p≥5, the elements 1,z,z² are K-independent. The determinant is nonzero.

### 4.3 Type B against C: the mixed case

Translate the triple row class and the first double column class to zero, and write

    rows:    p u_1, p u_2, p u_3, t,
    columns: p v_1, p v_2, q+p w_1, q+p w_2.

Here t,q are units mod p; the u_i are pairwise distinct mod p; v_1≠v_2 mod p; and w_1≠w_2 mod p. The u_i,v_i,w_i may contain arbitrary higher digits.

In the top three rows the first two columns have entries ω^(u_i v_j), and the last two have entries η^(u_i q)ω^(u_i w_j). In the last row the first two entries are η^(t v_j), while the last two are z η^(t w_j), with z=ζ^(tq). Therefore

    det M = A + z B,   A,B∈K.

We show B≠0. Expand B first along the last row and then along the one remaining column in the second column class. Let M_i be the signed 2-by-2 minor obtained from [ω^(u_i v_j)] by removing row i. Every M_i is nonzero by Lemma 1. Up to harmless overall signs, B is a sum of the six terms

    M_i η^(u_i q) [η^(t w_2)ω^(u_i w_1) − η^(t w_1)ω^(u_i w_2)],  i=1,2,3.

Their η exponents modulo p lie in the two translated three-element sets

    X+t w_2  and  X+t w_1,  where X={q u_1,q u_2,q u_3}⊂F_p.

The shifts differ because t(w_2−w_1)≠0 mod p. The two sets cannot coincide: a nonempty subset invariant under a nonzero translation in the cyclic group F_p is the whole group, but |X|=3<p. Thus their symmetric difference is nonempty. A residue in that difference occurs in exactly one of the six terms. After gathering powers of η modulo p, its coefficient in L is a nonzero M_i times a root of unity. The K/L basis independence proves B≠0. Finally 1,z are K-independent, so det M≠0. QED.

This mixed-case proof is the substantive new step. No positivity assumption, floating-point rank threshold, or assertion about a finite-field Fourier matrix is used.

## 5. Rank-three separation theorem

If both R and C occupy at least five residue classes modulo p², Section 3 selects one of the four types on each side. Lemma 1 and Section 4 show that the corresponding four-by-four minor is nonsingular. The rectangle therefore has rank at least four.

Contrapositively, rank≤3 forces at least one side to occupy at most four residues modulo p². Each such class contains p indices in Z_(p³), hence

    min(a,b)≤4p.

This proves the theorem for every prime p≥5. It does not claim the stronger bound 3p. Exploratory tests of all four-point patterns, including the unneeded (2,1,1) pattern, are not a proof of that stronger statement.

## 6. Closing the N=1331 density gap

Let N=1331 and transpose so a≤b. The accepted stable-rank inequality is ab≤Nr.

For rank three, the new theorem gives a≤44. Hence

    3/a + 3/b ≥ 3/a + a/1331.

The function f(a)=3/a+a/1331 is decreasing on 0<a≤44, since 44²<3·1331. Consequently

    3/a + 3/b ≥ 3/44 + 44/1331 = 49/484
                              = 132/1331 + 1/484.

This is an exact rational inequality. Alternatively, monotonicity follows from

    f(a)−f(44)=(44−a)(3/(44a)−1/1331)≥0.

The accepted rank-two theorem gives density E_2/N=143/1331=13/121, whose gap above D_N/N=12/121 is 1/121>1/484. Rank≥4 gives density at least sqrt(16N)/N, strictly larger than 49/484 (squaring verifies the comparison with exact integers). Rank-one tiles have density at least D_N/N.

Summing the tilewise inequalities using disjoint coverage ∑ab=N² yields

    cost ≥ N D_N + A_(rank≥2)/484 = 175692 + A_(rank≥2)/484.

The standard coset tiling attains 175692. Strict higher-rank slack forces every optimum to use only rank-one tiles. The accepted rank-one equality classification then forces each tile to be a full mutually annihilating coset product with sizes 11 and 121. Every such tile has area N, so every optimum has exactly N tiles. Orientations may vary from tile to tile; no single common orientation is asserted.

The coefficient 1/484 is valid but not asserted sharp. In particular the scalar corner a=44,b=3993/44 used in its derivation is not integral, and no rank-three rectangle of that shape is claimed.

## 7. A Fourier-specific negative control for naive rank-three rigidity

The projective three-class analogue of the accepted rank-two lemma is already false inside F_(p³). Take

    R=C={0,p²,2p²,1},  p≥3.

The leading 3-by-3 block is all ones. The whole matrix has rank at most three, since it is the sum of matrices supported on that block, the last column above it, and the last row. The minor on indices {0,p²,1} has determinant −(ω−1)²≠0, so the actual rank is exactly three.

All four rows and all four columns are projectively distinct. Indeed both index sets contain 0 and 1, so no distinct selected rows or columns can be proportional. At p=11 this is an actual 4-by-4 rank-three Fourier rectangle with four classes on both sides.

It does not threaten the theorem: its first three indices coincide modulo p². It also has a strictly cheaper three-piece rank-one refinement, costing (3+3)+(3+1)+(1+4)=15 rather than 3(4+4)=24. No universal rank-three refinement theorem is asserted.

## 8. Exact controls and remaining gate

`check_prime_cube.py` is fresh and does not import the accepted rank-two checker or reviewer. Its completed counts and exact certificates appear in `RESULTS.json` and `controls.stdout.txt`. It verifies the determinant-pattern claims in exact cyclotomic arithmetic, including arbitrary high digits; the finite translation obstruction; the target density inequalities; an explicit full target coset tiling; and the Fourier rank-three negative control. These controls supplement the complete proofs above.

Completed controls (all passed):

- 177,600 exhaustive canonical p=5 four-by-four minors: 1,600 B–B, 16,000 B–C, and 160,000 C–C.
- 50,000 additional exact four-by-four minors across p=5,7,11,13,17, with arbitrary higher digits and translations, covering all ten unordered pairs among U,A,B,C.
- 33654 exhaustive three-element-set/nonzero-translation pairs across p=5,7,11,13,17,19, all with nonempty symmetric difference.
- All seven integer partitions of five, checking the selection rule; 32 independent SymPy polynomial-remainder cross-checks of the exact determinant evaluator.
- 10,506 rank-three scalar shapes with side bound 44, all above the claimed density. Their integer relaxation minimum is 67/660 at (44,90); no Fourier realization is claimed.
- The full 1,331-tile target coset partition, covering all 1,771,561 entries exactly once, with cost 175,692.
- The exact Fourier four-projective-class rank-three counterexample and its disjoint rank-one refinement of cost 15 versus 24.
- A fresh domain census through 10,000, leaving 24 residual lengths and first residual 1859.

The next residual in the old domain union after adding 1331 is 1859=11·13², with D=156 and 12N<D²<16N. This prime-cube lemma does not apply to that mixed-prime length. Rank two is already excluded there, rank≥4 already has strict density slack, and rank three is again the next gate. Neither the p³ theorem nor its 1331 specialization solves all composite lengths.

## Proposed next-gate wording

Accept, after review, the prime-cube rank-three separation theorem: for p≥5, rank≤3 Fourier rectangles in F_(p³) have a side of size at most 4p. Its proof selects a nonsingular four-by-four minor from five distinct classes modulo p² and resolves the mixed (3,1)–(2,2) pattern using two cyclotomic field extensions. At N=1331 it proves the exact disjoint-tile optimum 175692, rank-one-only full-coset equality, and the valid higher-rank-area penalty 1/484. The accepted domains now cover all N≤1858; the next residual is 1859, again at rank three. Preserve all complex/disjoint/no-sharing and preparation/storage/I/O qualifications, parent TO RESEARCH status, and priority 42.
