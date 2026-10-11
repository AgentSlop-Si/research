# Independent review of the finite abelian prefix proof

11 October 2026 UTC. Mathematical correctness and project provenance review.

## Decision

**ACCEPT the mathematical theorem and its proof for every finite abelian group. No mathematical repair is required. REPAIR its project positioning: this is a recovered specialization and reproof of an already accepted, stronger project theorem, not a new finite-abelian scope extension or a new accumulated-stabilizer lemma.**

The sealed candidate is `Prefix_All_Finite_Abelian_Optimizer_Candidate_2026-10-11.zip`, 460,479 bytes, SHA-256 `b84d38846f27d43981bd78bbfb0f37c48db5623825faad6d4a614e1a2990d1c0`. Its mathematical proof is `ABELIAN_EXTENSION_PROOF.md`, 11,011 bytes, SHA-256 `33c2ddba3ad970c7d4816a2c513cedaee7e4993e3899910917c91fbc76887732`.

This review independently checks the symbolic proof and freshly reconstructs the finite certificates. It is a project review, not external peer review or proof-assistant certification. No Sheet or GitHub write is included. No submitted, inherited, or uploaded mathematical program was executed or imported.

## Accepted mathematical statement

Let G be a finite abelian group of order N=product_p p^(a_p). For a labeled ordering x_1,...,x_N, define T_j={x_1,...,x_j}, S_j={g:gT_j=T_j},

    Z_G(x) = sum_(j=1)^N (|S_j|-1),
    B(x) = <S_j:1<=j<N>,
    V(G) = N sum_p a_p(1-1/p).

The full prefix contributes N-1 exactly once and is excluded from B. The empty prefix is not scored. Equivalently, Z_G(x)=sum_(j=1)^(N-1)|S_j|, including the empty sum at N=1.

For N>1, B(x) is proper for every ordering. The maximum is V(G). The maximizing orders are exactly the recursive maximal-subgroup right-coset orders: choose a maximal proper subgroup J, place its distinct right cosets consecutively in any order, and choose a maximizing local order independently in each coset; recurse to singletons. A nontrivial optimizer has unique top J=B(x).

Writing A(G) for the number of labeled optimizing orders,

    A(1)=1,
    A(G)=sum_(J maximal proper in G) [G:J]! A(J)^[G:J],  N>1.

The sum is over actual subgroups. No translations, automorphisms, or conjugacy classes are quotiented out, and no coset-representative multiplier appears. For prime N, the unique top is the trivial subgroup and A(G)=N!. The singleton has score zero, one ordering, and no top subgroup.

## Proof transition audit

### Accumulated orbit containment

Candidate lines 45–67 are correct. Put B_j=<S_1,...,S_j>. At j=1 the singleton stabilizer is trivial. In an abelian group, the product S_j B_(j-1) is a subgroup containing both factors, hence equals their generated subgroup B_j. Assuming B_(j-1)x_1 is contained in T_(j-1), it is contained in T_j, and therefore

    B_j x_1 = S_j B_(j-1)x_1 ⊆ S_j T_j = T_j.

At j=N-1 this places a set of |B_j| elements inside a proper subset of G. Hence B(x)<G. There is no use of persistence or nestedness of the individual stabilizers. They may be incomparable. No numerical q-adic escape estimate is needed in this scope.

The same proof works under pairwise subgroup permutability, as the earlier project manuscript already states. Abelianity is sufficient, not the sharp hypothesis of this lemma. The candidate is correct to avoid asserting the lemma for arbitrary nonabelian groups.

### Choosing the top subgroup and importing induction

Candidate lines 76–81 correctly choose a maximal subgroup J containing B(x). Since G is abelian, J is normal and the simple finite quotient G/J is cyclic of prime order p. Thus |J|=N/p. J is itself abelian and smaller, so the simultaneous induction over all finite abelian groups applies to its actual group structure. There is no assumption that the optimum depends only on cardinality in the counting argument.

### Exact accounting and full-prefix normalization

Candidate lines 83–99 are correct. For each insertion j, the active local prefix is the intersection of T_j with the J-coset containing x_j. Right translation identifies that coset with J and preserves the left J-action. For j<N, every global stabilizer is contained in J and preserves each right J-coset, hence S_j≤L_j for its active local stabilizer.

Each nonempty local prefix is encountered exactly once at an active insertion. At j=N the active local prefix is all of its coset, so L_N=J while S_N=G. Consequently the correction is exactly N-|J|:

    Z_G(x) = sum_C Z_J(x restricted to C) + N-|J|
             - sum_(j<N)(|L_j|-|S_j|).

The empty local prefix is never inserted into the sum. The full local prefix of every coset is counted once. Every remaining deficit is nonnegative. Since one factor p is removed from the order on passing to J,

    p V(J)+N-N/p = V(G).

This proves the upper bound for every ordering, without assuming optimality or consecutive blocks in advance.

### Attainment and exact proper stabilizers

Candidate lines 101–109 are correct. In a consecutive J-coset ordering, a strict partial-block prefix has exactly one partially occupied coset. Normality makes a putative stabilizer permute the J-cosets; it must fix that partial coset, which forces the stabilizing element into J. At a proper block boundary, the occupied quotient cosets form a nonempty proper subset of the prime-order group G/J, whose translation stabilizer is trivial. Thus every proper global stabilizer lies in J.

Within J, full and empty cosets impose no additional conditions, so the global stabilizer equals the active local one. All deficits vanish and optimal local orders attain V(G). If J is trivial, all blocks are singleton boundaries and the boundary argument covers the entire construction.

### Equality forces consecutive blocks

Candidate lines 113–122 correctly use equality of a finite sum of nonnegative local losses and deficits. Each local order must maximize, and S_j=L_j for every j<N.

At the first completion of a J-coset, the insertion is necessarily a proper prefix because [G:J]≥2. Its local stabilizer is J, so the global stabilizer is J. The whole prefix must be a union of complete J-cosets. No other coset was complete earlier, and a single insertion cannot complete two cosets. Therefore every other coset is empty, forcing the first block. At each subsequent proper completion the same argument forces the next block. The final coset occupies all remaining positions. Applying the induction to each local order gives exactly the stated recursion.

### Unique top and overlap-free labeled counting

Candidate lines 124–136 are correct. The first completed block is a proper prefix with stabilizer exactly J, and all other proper stabilizers lie in J. Their generated subgroup is therefore exactly J. This proves unique top for a fixed optimizer and separates distinct choices of maximal subgroup.

For fixed J of index p, there are p! orders of its distinct labeled cosets and A(J) local choices in each one. Fixed coset identifications give p! A(J)^p global orders. A different representative induces a bijection on the same local labeled sequences, rather than another multiplicity. The resulting global order recovers its boundaries and local orders. Consequently there is neither within-top duplication nor overlap between different tops. The singleton is the explicit base case, not an empty recurrence sum.

## Finite certificate audit

The candidate's periodic-state method is valid for the specified finite computation. Every positive-weight cyclic prefix is a periodic subset. Its complete list is an inclusion chain in the periodic-subset poset; conversely any such chain extends to an element ordering. Extra positive-weight prefixes can only improve the score. Therefore maximum weighted-chain score equals maximum element-order score.

For an optimal predecessor edge T⊂S, there can be no periodic U strictly between them: its positive weight would give F(U)>F(T), contradicting predecessor optimality. Thus every one of the (|S|-|T|)! orderings of the difference creates no omitted positive-weight prefix along an optimal edge. Every global optimizing order has one complete periodic-prefix chain, so the factorial-gap count has no chain duplication.

For C30, every nontrivial stabilizer contains a subgroup of prime order 2, 3, or 5. Enumerating unions of those subgroup orbits gives all periodic states, and restricting to orbits contained in a target gives all periodic predecessors. Direct rotation tests calculate the exact stabilizer of each state. The subgroup generated by cyclic stabilizers has order equal to the least common multiple of their orders. The full-state stabilizer must be excluded from this accumulator; both submitted and reviewer implementations do so.

The separately reconstructed augmented chain values are scores of chains at a prescribed accumulated subgroup order. They are not, for a general non-full subgroup B, asserted to be exact optima of all element orders having that exact B. Completing a chain may add stabilizers and enlarge B. The candidate correctly discloses this limitation. For full escape, added stabilizers cannot change B=G, so full-escape reachability and the empty-state conclusion are legitimate.

The reviewer wrote `review_controls.py` using Python standard-library modules. The submitted C++ and Python sources were read statically before this independent implementation was written; no claim of a blind or algorithmically unrelated C30 implementation is made. Candidate CSV data was read only after the reviewer reconstructed the C30 values and counts. Both entire CSVs were then compared row by row.

Fresh results:

- C30: 33,814 states including empty and full; 14,587,235 proper predecessor pairs; 184,251 optimizing edges.
- Maximum 59; exactly 467,058,592,972,800 labeled optimizing orders.
- B of order 6: 2,985,984,000,000 optimizers.
- B of order 10: 208,641,982,464,000 optimizers.
- B of order 15: 255,430,626,508,800 optimizers.
- No other B class has an optimizer; the full-escape chain state is unreachable.
- Every state, size, stabilizer, optimum, and count in `PERIODIC_DP_C30.csv` agrees with the fresh computation.
- Every prescribed-B chain score in `CHAIN_B_DP_C30.csv` agrees with the fresh computation.

The fresh independent full-subset DP additionally checked all 24 nontrivial finite abelian isomorphism types of order at most 16 and the singleton. The 25 groups use 398,350 subset states, including 398,348 from the nontrivial groups. It compares both maximum and labeled count against a separately enumerated actual subgroup lattice and recursive count. It also checks 931,991 local orbit-containment instances, including one from the singleton. These totals reproduce the candidate's 24-group results and add the explicit base case. Checking the distinguished identity suffices because all translates of all subsets occur in the exhaustive population.

For C30 the recurrence agrees arithmetically:

    A(C6)=120, A(C10)=32640, A(C15)=11301120,
    A(C30)=5! 120^5 + 3! 32640^3 + 2! 11301120^2
           =467058592972800.

The submitted unsigned-128-bit count arithmetic has enough range at n=30: every counted prefix order is a labeled order of a subset, so each count and nonnegative partial sum is at most 30!<2^128. The reviewer uses arbitrary-precision Python integers. The C++ program's assertion guards are adequate under the documented build without NDEBUG. Robust handling of malformed CLI input is outside the mathematical certificate claim.

These computations corroborate the theorem. They do not prove the universal result, establish historical originality, or extend the nonabelian scope.

## Numerical and nonabelian boundaries

The mixed-base gcd identity in candidate lines 169–199 is correct. For n=q^a r^c, coprimality gives

    sum_(j=1)^n gcd(j,n)
      =n[1+a(1-1/q)][1+c(1-1/r)].

The unmodified dense mixed-base envelope therefore exceeds the desired value by Nac(1-1/q)(1-1/r). At C30, with base n=6 and third prime 5, the gcd sum is 15 and the relaxed bound is 69 instead of 59. This proves failure of that particular direct proof substitution. It is neither a counterexample to the value theorem nor an exclusion of all multivariate approaches.

The D8 witness in candidate lines 201–223 is correct. With labels 2i+j for r^i s^j, the order 0,1,2,3,5,6,4,7 has proper-prefix stabilizers {0}, {0,1}, {0}, {0,3}, {0}, {0,3}, {0}. The generated subgroup is D8. The score is 10, while a separate exhaustive 256-state reviewer DP gives maximum 12 and 2,432 optimizers. Thus arbitrary nonabelian no-escape is false even for a p-group, although the previously accepted p-group optimizer theorem remains valid.

No general nonabelian three-Sylow or all-finite-nilpotent theorem follows from this candidate. The earlier pairwise-permutable theorem covers some nonabelian groups already; the remaining open scope must be phrased as arbitrary nonabelian three-Sylow products, not as the absence of every nonabelian example.

## Required project provenance correction

Two original accepted sources dated 10 October 2026 are decisive, rather than merely a later audit's recollection. The earlier exact all-abelian source is `precedent_snapshots/04_PREFIX_STABILIZER_OPTIMALITY.md`, SHA-256 `32c0159a008be1075b5b0b682e6df46ece71c763320998bdaf60cc7e34b44ca4`. Its sections 1–4 already give the same accumulated-stabilizer lemma, maximum, recursive equality characterization, unique top, and labeled recurrence. Its independent acceptance, `precedent_snapshots/05_INDEPENDENT_REVIEW.md`, SHA-256 `bd15d243e51d9deb09d694a1502a7b685de33d2efcccc75e87e02a24281128f6`, binds that exact proof and accepts all four conclusions.

The subsequently consolidated manuscript extends this existing result to the stronger pairwise-permutable class:

- `precedent_snapshots/00_MANUSCRIPT.md`, 33,749 bytes, SHA-256 `b15dc520910febb2f0336eb6874ea56835512c835182cda55992309d8b9f96a8`.
- Its lines 41–47 explicitly include all abelian groups and describe consolidation of the already accepted abelian proof and extensions.
- Theorem 1, lines 51–80, states the same maximum, complete recursive optimizer classification, unique top, and exact labeled recurrence for every finite group whose subgroups pairwise permute, and separately for all p-groups.
- Lemma 5.1, lines 203–224, proves exactly the candidate's supposedly new containment B_j x_1⊆T_j by exactly the product-equals-generated-subgroup induction, under the stronger pairwise-permutability scope.
- Lemmas 4.1–4.3, lines 150–201, contain the same exact accounting, block-stabilizer, and first-completion arguments.
- The sibling accepted review `precedent_snapshots/01_REVIEW.md`, 16,299 bytes, SHA-256 `df6e666aadb5a7b5ab1b9ea9c441c572b1aa3038ced0ae4fdf1327dcf13a8f30`, explicitly accepts that manuscript at lines 5–19, binds its exact hash, and audits these proof steps at lines 33–65.

The later `PRIMARY_COMPARISON.md` section 1 and `AUDIT.md` section 1 agree with those originals; they are supplementary evidence. `PRECEDENT_BINDINGS.json` records all six complete source paths, hashes, and snapshot names. Every copied snapshot was verified byte-for-byte against the original.

Accordingly, replace descriptions such as “new gate,” “new finite-abelian scope,” or “extension from two Sylow factors to all abelian groups” with “recovered finite-abelian specialization of the accepted pairwise-permutable theorem, with fresh finite corroboration.” The all-abelian class was already mathematically closed. The accepted arbitrary two-Sylow theorem remains a separate, genuinely different scope covering nonabelian factors without subgroup permutability; it was not the complete prior project baseline.

The candidate can still be useful as a concise self-contained specialization and a refreshed C30 certificate. No research-family, discovery-count, novelty-rank, or historical-priority promotion follows. This review does not audit whether these exact C30 files are unprecedented within every earlier archive, so it claims fresh reviewer execution rather than a new historical computation.

The inherited external EFK source-comparison gap remains open. No new public-literature search or whole-paper exclusion was performed here. That gap concerns historical positioning, not a missing premise in the elementary symbolic proof.

## Source binding and preservation

`SOURCE_AUDIT.json` records the candidate archive and all 20 members, verifies every archive member against its current local counterpart, and independently verifies the four accepted source snapshots against their original files. Those include the arbitrary two-Sylow candidate proof, accepted statement and review, and the later priority review. `PRECEDENT_BINDINGS.json` adds the recovered exact all-abelian proof and its acceptance, the pairwise-permutable manuscript and its acceptance, and the two concordant later audits.

`INDEPENDENT_CONTROLS.json` and `INDEPENDENT_CONTROL_RUN.txt` preserve the fresh reviewer results. `REVIEW_RECEIPT.json` records the separate mathematical and provenance decisions. A final preservation check is in `SOURCE_UNCHANGED.json`. The review archive contains no executable copied from the author candidate and no source-file modification. The sole mathematical program run for this review is the newly authored `review_controls.py`.

**Final disposition:** mathematical ACCEPT; provenance REPAIR to recovered/reproved scope; C30 finite certificates verified; no expansion to arbitrary nonabelian three-Sylow products; no novelty or ranking change.
