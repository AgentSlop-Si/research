# Independent review of the prefix stabilizer manuscript

10 October 2026 UTC.

## Verdict

**Accept the mathematical manuscript within its stated hypotheses. No mathematical correction is required.** The maximum, complete optimizer characterization, unique top-subgroup recovery, and labeled count are valid for finite groups whose subgroups pairwise permute and, separately, for all finite prime power groups. The S3 structural boundary and the solvable-group lower bound are correct. The consolidation does not strengthen the accepted model.

This acceptance is bound to `research_cycle_2223/prefix_manuscript/MANUSCRIPT.md`, SHA-256 `b15dc520910febb2f0336eb6874ea56835512c835182cda55992309d8b9f96a8`, and the exact companion files in `FINAL_INPUT_SNAPSHOT.json`. The manuscript package's `SHA256SUMS` has SHA-256 `d62bf560ded550ee70c6afba651a0c6c011ba273518ad2689ff20fd20a8c8509`.

The review checks proof correctness, editorial scope, provenance, and concordance with available local citation audits. It does not certify historical originality or re-audit all primary literature. The EFK full-body comparison remains open. No inherited executable was run or imported. No source file, repository, or external service was changed.

## 1 Model and theorem contract

The full prefix is included in the objective, contributing m−1. All labels are retained. The regular action is on the left, so subgroup orbits are right cosets Kx. Replacing a coset representative changes the coordinate identification by right translation inside K; this preserves the actual left stabilizer, not merely its size. Consequently the count has no extra coset-representative factor.

The two group classes remain distinct. Pairwise subgroup permutability is used only where it is supplied, and the proof for arbitrary p-groups does not import that condition. The manuscript explicitly rejects substitution of the weaker “finitely quasihamiltonian” terminology. It does not extend the upper bound or equality theorem to all solvable groups, mixed-order nilpotent groups, or arbitrary finite groups.

The recursive ordering is defined independently of optimality. The equality statement is therefore a substantive characterization rather than a circular definition. Subgroup inheritance permits both inductions. The singleton has value zero and one ordering, while top-subgroup recovery is restricted to nontrivial groups. Prime-order groups correctly have the trivial top subgroup and p! maximizing labeled orders.

## 2 Proof transition audit

### Lemma 3.1 and the free-action bounds

Left multiplication by a subgroup is free. Its orbits partition an invariant subset, so the subgroup order divides the subset size as well as m. Complementation and right translation preserve the stabilizer exactly. The resulting pointwise upper bound is valid. The manuscript correctly refrains from assuming these separate bounds are jointly attainable at mixed-prime orders.

### Lemmas 3.2 and 3.3

The p-group normalizer induction is sound. A central element outside L immediately enlarges its normalizer. Otherwise Z(P) lies inside L and the induction in P/Z(P) lifts to a strict normalizer enlargement. The quotient has smaller order because the center is nontrivial. Maximality then implies normality, and a nontrivial p-group quotient with no proper nontrivial subgroup has order p.

Under pairwise permutability, a Sylow subgroup times its conjugate is a p-subgroup containing it. Sylow maximality therefore forces equality and makes every Sylow subgroup normal. Different normal Sylow subgroups commute through their trivial intersections. The subgroup decomposition into Sylow components follows by Chinese-remainder powers of each element. A maximal subgroup has exactly one deficient component, where the preceding p-group result applies. Normal prime index is therefore established without a hidden classification theorem.

### Lemma 4.1 and equation (9)

The lemma assumes precisely what it needs: K contains every proper-prefix stabilizer. It does not assume that insertions already occur in blocks or that K is normal. An element of H_j lies in K and preserves both the active right coset and the whole prefix, so H_j is contained in its active local stabilizer L_j.

Each local nonempty prefix appears once when its coset receives an insertion. The final local stabilizer is K while the final global stabilizer is G, giving the exact correction m−k. The remaining differences are nonnegative subgroup-order deficits. Adding the nonnegative local optimality losses proves the stated necessary and sufficient equality conditions. There is no missing full-prefix term or double counting.

### Lemma 4.2 and equation (10)

Normality makes left multiplication permute the right K-cosets. A strict partial-block prefix has exactly one partially occupied coset, so a stabilizer must fix that coset and thus lie in K. Conversely, K fixes every full or empty coset and only the active local prefix matters. At a proper block boundary the occupied cosets form a nonempty proper subset of a prime-order quotient, whose translation stabilizer is trivial. The full stabilizer is exactly K. This covers k=1, when there are no strict partial blocks.

### Lemma 4.3

At the first coset completion, equality gives H_j=L_j=K. K-invariance forces every coset to be full or empty. No different coset can already be full at the first completion, and a single insertion cannot finish two different cosets. Thus every other coset is empty, forcing a whole first block. The same argument works at each later proper completion, while the final coset fills the remaining positions. This induction does not incorrectly assert persistence of earlier prefix stabilizers.

### Lemma 5.1 and the permutability induction

Pairwise permutability gives B_j=H_j B_(j−1). The previous accumulated coset lies in the new prefix, and applying its current stabilizer leaves the prefix invariant. This proves B_j x_1 contained in T_j. It asserts containment of one coset, not invariance under all earlier stabilizers. At m−1 the containment forces B_(m−1) to be proper.

A maximal K containing that subgroup exists. Lemma 3.3 supplies normal prime index q, and subgroup inheritance supplies the induction hypothesis on K. The identity W(m)=W(k)+1−1/q makes the upper bound exact. Lemma 4.2 attains it. At an optimum all losses in this same upper bound vanish, so Lemma 4.3 forces blocks and local optimality. The converse uses the same attained identity. Equation (12) is exact nonnegative accounting; the manuscript does not label it a metric stability theorem.

### Section 6 and Theorem 2

The p-adic valuation count gives the claimed sum of gcd values, with the final j=p^a contribution included separately. Normal index-p recursion attains the pointwise upper bound. Equality of a sum of nonnegative pointwise deficits is equivalent to saturation at every prefix.

For necessity, saturation at k=p^(a−1) gives K=H_k of order k and T_k=Kx_1. Each proper boundary stabilizer J=H_(tk) is another normal maximal subgroup of that order. If J differs from K, then JK is a subgroup properly containing maximal K, hence G; J-invariance of a prefix containing Kx_1 would then force the entire group into a proper prefix. Thus all boundary stabilizers equal K. Successive differences of the boundary prefixes are K-invariant sets of size k and hence individual K-cosets.

This argument covers p=2 and a=1. In the latter case all boundary stabilizers are the trivial subgroup, and every singleton block is legitimate. Lemma 4.2 and equality of the total force every induced order to be optimal. The general p-group proof never uses the permutability accumulation lemma.

### Section 7 and the recurrence

In a maximizing block ordering all proper-prefix stabilizers lie inside K, and the first completed block has stabilizer K. Hence their generated subgroup is exactly K. This establishes uniqueness for a fixed ordering and prevents overlap across top choices; it does not claim the same K for all optimizers or nested prefix stabilizers.

For fixed K, q distinct labeled cosets have q! orders, and each fixed coset identification has A(K) internal orders. The local choices are independent. The resulting q! A(K)^q count is exact, with no translation or automorphism quotient and no representative multiplier. Summing over the uniquely recovered top subgroup proves equation (5); the common p index proves equation (8).

## 3 Examples and boundary statements

The cyclic recurrence and the displayed counts for C4, C6, C8, C12, C2×C2, Q8, and D8 agree with fresh computations. In particular A(C12)=31,872, A(Q8)=384, and A(D8)=2,432. The stated maximal subgroup types of Q8 and D8 give exactly these counts.

The C12 witness has stabilizer orders 1,2,1,2,1,6,1,1,3,1,1,12 and score 20. Its top is the even residues. H2 and H9 are incomparable, confirming the need for independent recursive branching rather than one common fixed subgroup chain.

For S3, the witness uses the stated rightmost-first composition and has stabilizer orders 1,2,1,2,1,6. The upper-bound split on |H3|=3 or 1 is exhaustive. An order-three invariant prefix is a parity coset; its first pair and the complement of its fourth prefix have equal parity and trivial stabilizer. Otherwise only the two possible order-two contributions remain, again giving maximum 7.

The count splits into 72 parity-triple orders and 288 orders with opposite-parity first and last pairs. Exactly 144 of the second type have consecutive cosets of their order-two top subgroup; together with the first type this gives 216 hierarchical orders and 144 nonhierarchical optimizers. The formal out-of-scope recurrence gives 216, so it fails structurally and enumeratively, while the numerical value mW(m) still holds. All groups of smaller order are abelian, establishing the stated smallest-order boundary.

Proposition 9.2 uses nontrivial abelianization of a nontrivial solvable group to obtain a normal prime-index subgroup. Solvability passes to its subgroup, and induction with Lemma 4.2 constructs the claimed score. This is only a lower bound and does not prove the omitted upper bound or characterization.

Equation (16) is an exact double count. Summing connectivity cuts over g counts |H_j| at every proper prefix. The subtraction of m unit terms in Z cancels the full-prefix |H_m|=m term, so the result equals Z. The identity element's connectivity contribution is correctly included.

## 4 Fresh independent controls

`independent_controls.py` was written for this review before inspecting the submitted validator. It imports only Python standard-library modules. It does not import or execute the manuscript validator or an older research program. The provenance manifest is read only as data; predecessor programs are hashed, not run. The submitted validator was subsequently read statically.

The independent program builds multiplication tables directly. D8 comes from permutations of a square, Q8 from two 2×2 matrices over F3, and S3 from permutations of three points. It verifies identity, row and column bijectivity, and associativity. All subset stabilizers are obtained through literal left translations.

A full labeled subset dynamic program, beginning at the empty set, computes both the maximum and its exact labeled count. Independently, every subgroup is recognized by closure, maximal subgroups are determined by inclusion, and a general recursive coset recognizer tests hierarchy membership. The formal subgroup recurrence is computed separately from the subset dynamic program.

Coverage is 13 groups and 6,062 full subset-DP states including empty states: C1, C2, C3, C4, C2×C2, C6, C8, D8, Q8, C9, C3×C3, C12, and S3. The program exhausts all identity-first permutations for the listed groups of order at most nine other than S3, and all 720 labeled S3 permutations, totaling 96,616 explicitly inspected orders. Right translation justifies restoring labeled histograms from the normalized cases, and those counts independently agree with the full labeled DP.

For every enumerated ordering in either theorem class, optimality is equivalent to hierarchy membership. Each nontrivial optimum has exactly one possible top subgroup, equal to that generated by its proper-prefix stabilizers. The prime-power cases also satisfy the pointwise saturation equivalence, and every enumerated ordering in a pairwise-permutable group satisfies the accumulated-coset containment. The S3 tests recover precisely 360 optimizers, 216 hierarchical and 144 nonhierarchical.

The C12 witness is checked literally, including its incomparable stabilizers and unique top. The gcd sum formula is checked for primes 2,3,5,7,11 and exponents 0 through 4, including the singleton edge case. Connectivity is independently computed from the regular permutations for one concrete ordering in each of the 13 groups and agrees with the prefix objective.

All controls passed with exit code zero. `CONTROL_RESULTS.json` records the complete results and source-pin checks; `CONTROL_STDOUT.txt` preserves the bounded run summary. These finite controls corroborate the general proof and do not replace it or extend its hypotheses.

## 5 Source concordance and novelty boundary

All 15 source files listed in the manuscript's input manifest match their exact SHA-256 and byte-count pins. The ten entries attributed to the publication-readiness snapshot also match that snapshot. P1–P4 provide the same theorem contracts and proof arguments used here. The manuscript's claim/proof concordance points to the relevant sections without importing a stronger hypothesis or conclusion. The larger historical computation totals are accurately attributed to saved reviews rather than relabeled as this review's fresh execution.

The citation and novelty audit here is against the available P5 comparison and source registry, together with P4's terminology audit. It is not a new retrieval of every cited primary paper. The manuscript accurately retains the following boundaries:

- BS20 supports pairwise-permutability terminology and the Q8/S3 contrast; its broader entropy hypothesis is not imported.
- GVS03 supplies fixed-chain transversal and logarithmic-signature background, with a different objective.
- Sta05 supplies the existing connectivity statistic; the manuscript proves its elementary simultaneous-group reformulation directly.
- Cal03 supplies earlier individual-permutation decompositions. The preprint and journal body are not silently identified as equally inspected.
- ST09 supplies classical maximal-subgroup-chain recursion, not a count of the present element orderings. The exposed-page limitation is disclosed.
- MBKK18 supplies a modern account of classical rooted-tree direct/wreath products, with Jordan credited through that source and no claim to have inspected Jordan's original paper.
- EFK92 remains a potentially relevant antecedent whose full body has not been compared. The C4 antichain substitution control excludes only that substitution, not the entire paper.

The candidate contribution is correctly located in optimizer necessity, independent coset branching, and unique top recovery. Sum/product enumeration itself is not claimed as a new method. No worldwide-first result, external peer review, arbitrary-group maximum, new theorem fusion, or Fourier algorithm improvement is asserted. EFK's missing Lemma 2.1, Theorem 2.1, remainder of Section 4, Proposition 5.1, Corollary 6.1, and proof coverage remain unresolved. The known denied route was not retried.

## 6 Receipt and preservation

`INITIAL_SNAPSHOT.json` records the exact manuscript package when this review began. `FINAL_INPUT_SNAPSHOT.json` binds the accepted sealed package. `SOURCE_PIN_VERIFICATION.json` records the readiness-pin comparison. `REVIEW_RECEIPT.json` binds those artifacts, this report, and the newly written controls and outputs. `SHA256SUMS` binds the review package without self-reference.

No blocking or nonblocking mathematical correction is requested. The remaining full EFK comparison is a priority limitation, not a missing premise for the stated proof. This is a local independent correctness review, not formal proof-assistant certification or external journal review.
