# Independent acceptance: complete distinct-odd-semiprime degree classification

Date: 2026-10-23 UTC. Verdict: **ACCEPT the separate cycle-propagation addendum.** No mathematical correction is required to the frozen bytes.

## Exact bindings and scope

Author directory: `semiprime_cycle_propagation_addendum_20261023_frozen_v1`.

- REPORT.md SHA-256: `416db6e0d1253f53cb9d4ee60aeb700d4d4608ff9dfea1b04b0c40a18bed100e`.
- MANIFEST.json SHA-256: `7d922c448c397284303ecb83f6bf434e7bcbd05c008bc97ac50c0549da79ac03`.
- All 14 manifest members and all five selected accepted-source copies were checked exactly.

For every pair of distinct odd primes p<q, every primitive complex pqth root zeta, and an arbitrary binary square R, the original matrix D[r,c]=R[r,c] zeta^(rc) has either Gram equal to dI if and only if d is one of 0,1,p,q,pq. There is no prime-ratio restriction. The new credit starts at p>=7; existing 3q and 5q results are retained, not counted again.

For the original normalized Fourier target and simultaneous inverse-row-sparsity infimum, the floor sqrt(1-s/(pq)) is consequently sharp exactly for s in {pq-1,pq-p,pq-q}, within 1<=s<=pq-1. All other budgets have a strict infimum gap, without an exact larger value or quantitative gap claim.

This closes the distinct-odd-semiprime degree-existence slice, not the whole M-SPARSE-DEFECT owner, which remains TO RESEARCH at priority 42. Support classification, general composite orders, nonsharp optima, arithmetic costs, and historical novelty remain outside scope.

## Accepted baseline and remaining obligation

The earlier compatibility report, SHA-256 `1a51d0d0e7b3a5e418eee5b5660e5752ac14fc7b1da7e26a6e0d68a2c64b010d`, and its independent review `d8b89bb1aab46aabd01bcba24946a2cb69d0ef2c8e82a0ae54c7510a4a72a1b2` are copied unchanged. Their all-ratio theorem already excludes all proper degrees above p+q-1 and all low degrees except 1,p. Divisor constructions supply the positive cases. Therefore the exact new obligation is q<d<=q+p-1.

Square invertibility gives both Grams and every row and column degree d. The proof preserves this essential column-degree hypothesis; it does not substitute a rectangular row-Gram problem. The CRT identity uses actual original indices. The classical binary two-prime cancellation theorem retains its inherited attribution.

## Independent proof review

### 1. A full q-line must occur

Assume q<d<pq and no row has a full q-line. If a supported entry (r,c), r=(a,b), lies on a p-fiber absent from its row, no primitive partner can support c: its overlap would force a complete line or fiber through c into r. Thus column c is supported inside the coordinate cross through r.

Since d>q, a supporter s=(a',b), a'!=a, exists. Every further own-group supporter t=(a,b'), b'!=b, is primitive to s, hence both contain the full p-fiber through c. At most one such t exists, since two same-group rows containing that fiber would have p intersection points in every fiber and hence overlap pq>d. Therefore the column has at most two own-group supporters and p-1 outside, giving d<=p+1<q+1<=d.

No deficient entry can exist. All row supports would then be unions of full p-fibers, with pairwise disjoint fiber sets among the q rows of each group. Since d>q>p, each uses at least two fibers, impossible with only q fibers. A full q-line therefore occurs. This is a derived global fact, not a support ansatz.

### 2. Interior of the remaining window

For d=q+t, 1<=t<=p-2, a full-line row has exactly t extra columns, no full p-fiber, and at least one missing line. An extra column cannot have a primitive supporter because its complete cycle is absent from that row. Nor can it have a same-second-coordinate supporter from another group: equal order-p line counts and the missing line force empty intersection. Its supporters are confined to its q-row group, contradicting degree d>q. This excludes the full interior without a prime-separation condition.

### 3. A boundary line row is a cross

At d=q+p-1, let a line row have p-1 extras and suppose it has no full p-fiber. Each extra column then has no primitive supporter, so its support is contained in the row's coordinate cross. Its degree equals the cross size, hence every extra column has that exact same support.

For distinct extra columns with CRT differences (delta_u,delta_v), their actual column inner product is the nonzero phase times

    q 1_(delta_v=0)+p 1_(delta_u=0)-1.

The bracket is -1, p-1, or q-1, never zero over the complex numbers. There are at least two extras because p is odd. This contradicts column orthogonality. Thus the row contains a p-fiber, and its p-1 extras complete precisely one fiber: its support is L_u union F_v.

This direct character computation uses the full column Gram, not merely regularity, and includes the same-first and same-second coordinate cases.

### 4. One cross row exceeds the global incidence capacity

Let T=F_v minus L_u, of size p-1. Its columns require (p-1)(q+p-1) total row incidences.

Within the cross row's group, its own contribution is p-1, while each other row contributes at most one: same-group overlap per fiber is at most one since d<2q. The group contributes at most q+p-2.

In another group, any primitive row meeting T must contain all F_v, so at most one such row exists. The unique possible same-second-coordinate row, if it meets any point of T, has positive equal line-overlap counts. Every off-baseline line of the cross row has just one point, forcing all those counts to equal one and hence containment of all T. It need not contain the baseline-fiber intersection point, and the proof correctly does not assert that.

These two possible supporters cannot coexist: they would overlap in the p-1>=2 points of T in one fiber, violating their same-group bound of one. Therefore each other group contributes at most p-1, not twice that amount. Total capacity is at most q+p-2+(p-1)^2. The deficit is exactly

    (p-1)(q+p-1)-[q+p-2+(p-1)^2]=(p-2)(q-1)>0.

This contradiction works for every odd p>=3 and q>p, including p=3,q=5. No enumeration of small incidence designs or one-clique theorem is needed.

## Completion and inherited inverse-row consequence

The new exclusions complete the earlier exhaustive degree partition. The original divisor masks remain valid and provide all allowed degrees. Although the new proof itself works for all odd p, the record appropriately assigns new credit only beyond the already accepted 3q and 5q families.

The separately accepted inverse-row criterion is copied with SHA-256 `54511a4d4c1e343b5d3bbe3edb7d9a054d42a4200681bb17cf0bda6c11538253`. It proves both necessity and sufficiency of a complementary degree N-s Fourier mask and a compactness argument converting absence of such a mask into strict infimum separation. Its hypotheses are unchanged, including s>=1 and the floor being below one. Thus the addendum's inverse-row translation is valid without a nonattainment loophole.

The previous p=11,q=23 rectangular Fano row-Gram control is not contradicted: the new proof uses full-square column regularity and orthogonality, and never claims all local groups must be single cliques. It bypasses, rather than denies, that local obstruction.

## Independent controls

Fresh `fresh_controls.py` was written specifically for this addendum. It executes no author or historical scientific program. The prior independent full-square divisor/negative controls remain bound through the accepted baseline rather than being relabeled as new evidence.

The new controls independently check exact signed cyclotomic-basis identities for every cross center and every nonzero column difference at (p,q)=(3,5),(5,7),(7,11),(7,13),(11,13), including both coordinate-zero difference cases. They also exhaust cross-row intersection patterns at (3,5),(5,7),(7,11), verify the positive same-b balance implication to all of T, reject coexistence of the two supporter types, detect a missing-T-point mutation, and check the exact sharpened capacity and deficient-column contradictions on a bounded prime grid. Normal and optimized outputs are byte-identical; detailed counts are in RESULTS.json. These are independent formula and mutation controls, not a finite proof of the universal theorem.

No external state was changed by this review. Publication remains with the designated sole publisher.
