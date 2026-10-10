# Nonabelian boundaries of prefix stabilizer optimality

10 October 2026 UTC. Bounded continuation of the accepted finite-abelian theorem.

## Result

The finite-abelian optimum extends, with the same recursive equality structure and exact counting recurrence, to each of the following classes:

1. Every finite group in which **all pairs of subgroups permute setwise**, meaning HK=KH for every H,K≤G.
2. Every finite p-group, without any subgroup-permutability assumption.

The first class contains genuinely nonabelian groups, including Q8 and the order-16 group with presentation r^8=s^2=1 and srs^(-1)=r^5. In the latter example, not all subgroups are normal. The second class also contains D8, whose subgroups do not all permute.

The abelian structural conclusion does **not** extend to all finite groups: it already fails for S3. An explicit optimal order has two proper-prefix stabilizers that generate S3, so there is no common proper subgroup containing them and no recursive right-coset-block description. Its optimum remains the abelian value 7. The actual number of labeled optimal orders is 360, whereas applying the abelian counting recurrence outside its hypotheses gives 216.

Fresh exact subset dynamic programming found the abelian numerical value for all ten tested nonabelian groups, of orders 6 through 18. No counterexample to the numerical upper bound was found. This note does not establish that bound for arbitrary finite groups, all finite solvable groups, or all finite nilpotent groups of mixed order. It makes no historical-novelty or additional Fourier-algorithm claim.

## 1 Definitions and the action convention

Let G be a finite group of order m, acting on itself by **left multiplication**. For a permutation x_1,...,x_m of G set

    T_j = {x_1,...,x_j},
    H_j = Stab_G(T_j) = {g in G : g T_j = T_j},
    Z = sum_(j=1)^m (|H_j|-1),
    M(G) = max Z,
    W(m) = sum_(p prime) v_p(m)(1-1/p), with W(1)=0.

The orbits of a subgroup K under this action are the **right cosets Kx**. Accordingly, every coset block in this note means a right coset. If K is normal, this distinction disappears. A right coset Kx is identified with K by h x ↦ h; this intertwines left multiplication by K with its left regular action.

Right translation T↦Ty leaves the left stabilizer unchanged. Thus every ordering has a unique right translate starting at the identity, with identical prefix stabilizers. This is the normalization used in the computations. Left translation would conjugate the stabilizers, preserving their sizes but not generally their identities.

Two elementary observations apply to every finite group:

- H_j acts freely on T_j, so |H_j| divides both j and m.
- Stab_G(T)=Stab_G(G\T).

## 2 Pairwise permutable subgroups

**Theorem A.** Suppose G is finite and HK=KH for all subgroups H,K≤G. Then

    M(G) = m W(m).

An ordering is maximizing if and only if it is built recursively by choosing a maximal subgroup K<G, ordering its right cosets as consecutive blocks, and using a maximizing ordering of K inside each block. Every such maximal subgroup is normal and has prime index. The top subgroup is unique for each maximizing ordering.

Writing A(G) for the number of labeled maximizing permutations, with A({e})=1, gives

    A(G) = sum_(K maximal in G) [G:K]! A(K)^[G:K].

The proof is self-contained below; in particular it does not appeal to a classification of groups with permutable subgroups.

### 2.1 Why maximal subgroups are normal of prime index

For any Sylow p-subgroup P and any g∈G, P and gPg^(-1) permute. Their product is consequently a subgroup, and its order is a power of p. Maximality of the Sylow order forces P=gPg^(-1). Thus every Sylow subgroup is normal.

Distinct Sylow subgroups commute elementwise: their commutators lie in their intersection, which is trivial. Therefore G is the direct product of its Sylow subgroups P_p. Every subgroup K≤G also splits as the product of K∩P_p. To see this directly, write x∈K as a product of its commuting p-components; each component is a power of x, by the Chinese remainder theorem on the pairwise coprime component orders, and hence belongs to K.

If K is maximal proper in G, all but one of its Sylow factors must be full, and its remaining factor is maximal in the corresponding finite p-group P. Such a maximal subgroup L is normal of index p. Here is an elementary justification of that last fact. Every proper subgroup L of a finite p-group P is strictly contained in its normalizer: induct on |P|; if the nontrivial center Z(P) is not contained in L, a central element outside L suffices; otherwise apply induction in P/Z(P) and lift. For maximal L the normalizer must therefore be P, so L is normal. The quotient P/L has no nontrivial proper subgroup and is a nontrivial p-group, hence has order p. The nontriviality of the center used here follows immediately from the conjugacy-class equation.

It follows that K is normal in G and [G:K]=p. Pairwise subgroup permutability is inherited by all subgroups, so this argument remains available throughout induction.

### 2.2 The repaired accumulated-stabilizer argument

Put K_j=⟨H_1,...,H_j⟩. Because any two subgroups permute,

    K_j = H_j K_(j-1).

Inductively,

    K_j x_1 = H_j K_(j-1) x_1 ⊆ H_j T_j = T_j.

The base case is H_1={e}. Thus K_(m-1) is proper for m>1. This is precisely the part of the accepted abelian proof that needs more than arbitrary noncommutative group multiplication. The exact hypothesis used in this induction is that H_j permutes with K_(j-1); the theorem's all-subgroups condition supplies that fact uniformly for every ordering and recursively for its subgroups.

Choose a maximal proper subgroup K containing K_(m-1). Write q=[G:K], k=|K|. Section 2.1 proves that K is normal and q is prime.

### 2.3 Upper bound and attainment

For each global insertion x_j, let C_j=Kx_j, U_j=T_j∩C_j, and

    L_j = {h in K : h U_j = U_j}.

For j<m, H_j⊆K and H_j⊆L_j. Each induced coset ordering contributes all of its own nonempty local prefixes exactly once to the sequence of active U_j. At the final insertion, H_m=G and L_m=K. Consequently

    Z ≤ sum_(cosets C) Z_C + m-k
      ≤ q M(K) + m-k.

Induction gives

    Z ≤ q k W(k)+m-k = m W(m).

For attainment, put the K-cosets in consecutive blocks and choose optimal local orders. If a proper prefix ends inside a block, it has exactly one partially occupied K-coset. Normality of K makes left multiplication act on the quotient cosets; any stabilizing element must fix that unique partial coset and therefore lie in K. Its stabilizer is exactly the local stabilizer L_j.

At a block boundary, the prefix corresponds to a nonempty proper subset of G/K. A nonidentity translation of the prime-order group G/K has a single orbit, so no such subset has a nontrivial translation stabilizer. Hence H_j=K at each proper block boundary. The final correction is m-k, so the bound is attained.

### 2.4 Equality and exact counting

At equality every local ordering is optimal and H_j=L_j at each j<m. At the first completion of a K-coset, L_j=K, hence H_j=K. Every K-coset is therefore full or empty at that moment. Since no other coset has yet completed, none has been touched. Thus the first k entries form one whole coset.

Repeating at successive completion times forces all cosets to occur consecutively, and internal optimality then supplies the recursion. Conversely, the attainment argument proves every recursively constructed order optimal.

All proper-prefix stabilizers are contained in K, and the first completed block has stabilizer exactly K. Thus

    K = ⟨H_1,...,H_(m-1)⟩,

which proves uniqueness, including the case k=1. There are q! orders of the distinct cosets and A(K)^q independent local choices. Summing over distinct maximal K yields the stated recurrence without overcounting.

## 3 Every finite p-group

**Theorem B.** If |G|=p^a, then

    M(G)=a |G|(1-1/p).

Moreover, an order is optimal exactly when

    |H_j| = gcd(j,p^a)   for every 1≤j≤p^a.

Its optimal orders have the same recursive maximal-subgroup coset-block description and unique top subgroup as in Theorem A. All maximal subgroups have index p, so

    A(G)=p! sum_(K maximal in G) A(K)^p.

**Proof of the value.** Freeness gives the pointwise bound |H_j|≤gcd(j,p^a). For 0≤t<a there are (p-1)p^(a-t-1) indices j with v_p(j)=t, and the last index has gcd p^a. Therefore

    sum_(j=1)^(p^a) [gcd(j,p^a)-1]
      = a(p-1)p^(a-1)
      = a |G|(1-1/p).

A maximal subgroup K is normal of index p by the elementary p-group argument in Section 2.1, which did not assume subgroup permutability. Recursively order its cosets in consecutive blocks. The partial-block and prime-quotient argument of Section 2.3 gives attainment. Since every pointwise deficit is nonnegative, equality of sums is equivalent to saturation at every prefix.

**Proof of the equality structure.** Let k=p^(a-1) and take an optimum. At j=k, the stabilizer K=H_k has order k, so T_k=Kx_1. This K is a normal maximal subgroup. At any later proper block boundary j=tk, 1≤t<p, the stabilizer J=H_(tk) also has order k and is normal maximal. Since T_(tk) contains Kx_1 and is J-invariant, it contains JKx_1. If J≠K then JK=G, contradicting properness. Hence H_(tk)=K for every such boundary.

Thus every T_(tk) is a union of exactly t K-cosets. Successive differences have size k and are K-invariant, so each difference is one entire K-coset. This forces consecutive coset blocks. Inside a partial block, normality of K again gives H_j=L_j. The exact sum decomposition and the inductive optimum of K show that each local order is optimal. The converse, uniqueness, and counting follow exactly as in Theorem A. ∎

This theorem explains D8 and D16 without claiming that their subgroups pairwise permute.

## 4 The smallest structural failure is S3

Let a=(12), b=(23), with products acting rightmost first, and consider

    e, a, b, ba, ab, aba.

The exact left stabilizers of the six prefixes are

    {e}, ⟨a⟩, {e}, ⟨b⟩, {e}, S3,

with orders

    1, 2, 1, 2, 1, 6.

In particular T_4={e,a,b,ba}=⟨b⟩⟨a⟩ is invariant under ⟨b⟩ but not under ⟨a⟩. The generated subgroup ⟨H_2,H_4⟩=⟨a,b⟩ is all of S3 and is not contained in T_4. Thus the accumulated-stabilizer containment fails before the final prefix, even at an optimum.

The score is 1+1+5=7=6 W(6). It cannot be represented by the abelian recursive right-coset hierarchy. A top subgroup would have order 2 or 3. In the order-2 case the first block forces K=⟨a⟩, but T_4 is not K-invariant. In the order-3 case the first three entries {e,a,b} are not a coset of the unique order-3 subgroup.

### 4.1 Proof that 7 is the exact optimum

H_1 and H_5 are trivial, H_6=S3, and the only possible nonzero proper-prefix contributions are

    |H_2|-1 ≤ 1,  |H_3|-1 ≤ 2,  |H_4|-1 ≤ 1.

If |H_3|=3, then T_3 is a coset of A3. A two-element subset of that coset has no nontrivial left stabilizer, so H_2 is trivial. Likewise, the two-element complement of T_4 lies within the other A3-coset and has trivial stabilizer, so H_4 is trivial. The score is then 7.

If H_3 is trivial, the score is at most 5+1+1=7. The displayed witness attains it. This argument is independent of computer search.

### 4.2 Exact count and failure of the abelian recurrence

There are two disjoint optimal types.

- |H_3|=3: choose either of the two A3-cosets as the first block and order both blocks freely. This gives 2·3!·3!=72 orders.
- H_3={e} and |H_2|=|H_4|=2: the first pair and the final pair must each have opposite parity. There are 3·3=9 choices of the first unordered pair, 2·2=4 choices of the disjoint final unordered pair, and 2! choices within each of the first, middle, and final pairs. This gives 9·4·8=288 orders. The middle prefix has mixed parity, so its stabilizer is indeed trivial.

Hence A(S3)=72+288=360. In the second type, requiring H_2=H_4 gives 9·2·8=144 orders; these, together with the 72 order-3-block orders, are exactly the 216 recursive right-coset hierarchies. The other 144 are optimal but not hierarchical.

The formal abelian recurrence would give

    2! A(C3)^2 + 3·3! A(C2)^3 = 72+144 = 216,

which is not the actual count. This is a failure of extending the structural/counting theorem beyond its hypotheses, not a failure of the numerical bound.

All groups of order below 6 are abelian: prime-order groups are cyclic, and a group of order 4 is either cyclic or every nonidentity element has order 2, which forces commutativity. Thus S3 is a smallest-order boundary example.

## 5 A limited lower bound for solvable groups

**Proposition.** Every finite solvable group satisfies M(G)≥|G| W(|G|).

A nontrivial finite solvable group has nontrivial abelianization, and hence a normal subgroup K of prime index. Its subgroup K is solvable. Induct on |G| and put recursively constructed local orders in consecutive K-coset blocks. The same normal-subgroup, prime-quotient calculation gives

    Z = [G:K] Z_K + |G|-|K| = |G| W(|G|).

This proves the existence of an order with the abelian value. It does not give an upper bound for all solvable groups and does not certify that every optimum is hierarchical. S3 already rules out that latter characterization. This proposition is included only to separate a generally available construction from the unproved broader optimality claim.

## 6 Fresh exact controls

The new `fresh_nonabelian_dp.py` imports only Python standard-library modules. It neither imports nor executes inherited research programs. Multiplication tables are built directly from permutations, dihedral or semidirect-product coordinates, and the quaternion-unit multiplication rule. The program verifies identity, row bijectivity, and associativity of every generated table.

For every nonempty subset S, the program explicitly constructs gS for every g and records the exact stabilizer bitset. For identity-containing subsets it applies the exhaustive recurrence

    D({e})=0,
    D(S)=|Stab_G(S)|-1 + max_(x in S\{e}) D(S\{x}).

It sums all maximizing predecessor counts and multiplies the full-group count by |G| to reverse the unique right-translation normalization. Reconstructed witnesses are checked again using literal set translation, not the subset-image recurrence.

| Group | Order | Exact maximum | m W(m) | Labeled optimal orders |
|---|---:|---:|---:|---:|
| S3 | 6 | 7 | 7 | 360 |
| D8 | 8 | 12 | 12 | 2,432 |
| Q8 | 8 | 12 | 12 | 384 |
| D10 | 10 | 13 | 13 | 156,800 |
| A4 | 12 | 20 | 20 | 82,944 |
| D12 | 12 | 20 | 20 | 878,976 |
| D14 | 14 | 19 | 19 | 100,778,496 |
| D16 | 16 | 32 | 32 | 23,691,264 |
| M16 | 16 | 32 | 32 | 4,030,464 |
| D18 | 18 | 33 | 33 | 1,011,128,832 |

Here D_(2n) has order 2n. M16 is explicitly C8⋊C2 with multiplication

    (a,b)(c,d) = (a+5^b c mod 8, b+d mod 2).

Its subgroup ⟨s⟩ is not normal because r s r^(-1)=r^4 s. The structure check enumerates all 11 subgroups and verifies HK=KH for all 121 ordered pairs, supplying a non-Dedekind example for Theorem A without relying on a classification.

The completed ten-group run covers 209,696 identity-first subset-DP states in total. Every displayed witness was verified exactly.

The separate new `check_structure.py` imports only the new task's group-construction/closure helpers, not inherited programs or a DP implementation. It:

- independently evaluates every identity-first permutation of S3, D8, and Q8 by literal set translations, covering 10,200 permutations and verifying the exact maxima and labeled counts;
- enumerates subgroup lattices of S3, D8, Q8, and M16, checks pairwise permutability and normality, and computes the formal subgroup counting recurrence;
- verifies that the recurrence agrees for D8, Q8, and M16, but gives 216 rather than 360 for S3;
- checks the explicit S3 witness and the failure of accumulated containment at prefixes 4 and 5.

All assertions pass. The results are exact integer computations with no floating-point tests. These bounded controls corroborate the proofs; they do not certify an unproved all-group extension.

Reproduce from the workspace root:

    python research_cycle_1826/nonabelian_prefix/fresh_nonabelian_dp.py \
      > research_cycle_1826/nonabelian_prefix/control_stdout.jsonl
    python research_cycle_1826/nonabelian_prefix/check_structure.py \
      > research_cycle_1826/nonabelian_prefix/structure_stdout.json

## 7 Primary source check and scope

The standard term *quasihamiltonian* for groups whose subgroups pairwise permute was checked against Anna Giordano Bruno and Flavio Salizzoni, *Additivity of the algebraic entropy for locally finite groups with permutable finite subgroups*, arXiv:2001.02419v1 (8 January 2020), page 2; page 4 also gives Q8 and S3 as contrasting examples. [Primary paper](https://arxiv.org/abs/2001.02419), [full text](https://arxiv.org/pdf/2001.02419).

That paper studies algebraic entropy. It is used here for terminology and related group-theoretic context, not as a source for this weighted prefix optimization. The present proofs do not invoke its entropy theorem or a classification of quasihamiltonian groups. A bounded source check is not a historical-priority determination, and no novelty claim is made.

The accepted abelian theorem and its independent review were read and preserved:

- `research_cycle_1744/prefix_stabilizer_optimality/PREFIX_STABILIZER_OPTIMALITY.md`
  - SHA-256: `32c0159a008be1075b5b0b682e6df46ece71c763320998bdaf60cc7e34b44ca4`
- `research_cycle_1753/prefix_independent_review/INDEPENDENT_REVIEW.md`
  - SHA-256: `bd15d243e51d9deb09d694a1502a7b685de33d2efcccc75e87e02a24281128f6`

No predecessor was modified, no inherited executable was run, and no external service or repository was changed. The current deliverable closes the specified extension and supplies a sharp structural counterexample. The numerical optimum for arbitrary finite groups remains outside the proved scope.
