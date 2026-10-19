# Order 35: exclusion of the complete first interior

Date: 2026-10-19 UTC. Finished proof candidate, pending independent review. No historical-priority claim. No external write or repository change.

## Theorem and scope

Let zeta be any primitive 35th root of unity and R a binary 35-by-35 matrix. Put D[r,c] = R[r,c] zeta^(rc), with the original indices 0 through 34. There is no such R satisfying D*D = dI for any integer

    7 < d < 14.

The same statement follows from DD*=dI, and either identity implies the other because D is square and d>0. In particular both row and column degrees equal d. This closes the q=7 first-interior boundary left by the accepted theorem for N=5q, prime q>=11. That accepted theorem is used only for background, not rerun or counted as new work. The present proof does not classify the remaining degrees at N=35, nor general odd semiprimes.

The proof below is symbolic. The accompanying exact checker corroborates the finite local lemmas and original-phase controls; it is not an exhaustive search over square masks. Failure of a search is not used as evidence of nonexistence.

## 1. Original phases and necessary cancellation

Set e_5=21 and e_7=15 modulo 35. They are orthogonal CRT idempotents. For actual indices

    r=21a+15b, c=21u+15v (mod 35),
    zeta^(rc)=alpha^(au) beta^(bv),
    alpha=zeta^21, beta=zeta^15.

Here a,u are modulo 5 and b,v modulo 7. Let G_a be the seven rows of first coordinate a, F_v the five columns of second coordinate v, and L_u the seven columns of first coordinate u.

For rows in the same G_a, prime-order balance says the seven numbers |S_r intersection S_s intersection F_v| are equal. Since |S_r intersection S_s|<=d<14, each is either zero or one.

For row differences nonzero in both CRT coordinates, a vanishing binary overlap is a union of whole F_v fibers or a union of whole L_u lines. For completeness, reduction in the rational basis alpha^i beta^j, 0<=i<4, 0<=j<6, gives

    epsilon_(i,j)-epsilon_(i,6)-epsilon_(4,j)+epsilon_(4,6)=0.

Thus the binary coefficient grid has form A_i+B_j with integers A,B. Both cannot vary, because their sum would then have range at least two. This proves the asserted alternative. Empty overlaps are permitted. Nonzero character multipliers only permute CRT coordinates.

This cancellation fact is classical, not a new result here: de Bruijn; Lam and Leung, On Vanishing Sums of Roots of Unity, Journal of Algebra 224 (2000), 91–109, Theorem 3.3 and Corollary 3.4, DOI 10.1006/jabr.1999.8089; https://arxiv.org/pdf/math/9511209. The elementary proof is included to fix its exact binary and original-phase scope.

## 2. Clique components and five-coordinate local families

Join two rows in one G_a when they intersect once in every F_v. Nonadjacent rows have disjoint whole supports. Every row has a fiber with at most one entry, since d<14. If it is empty, the row is isolated. If it is a singleton, all its neighbors contain that same point and are mutually adjacent. Consequently every component is a clique. There are at most four components: representatives of five components would give five disjoint supports of size d>7 inside 35 columns.

A nonsingleton component of n rows restricts in every fiber to n nonempty subsets with pairwise intersection exactly one. Let k be their union size and I their total incidence. If there is a common point, every other used point is private and

    I=n+k-1.

Call this a star. The formula also holds for a singleton component with k=0 allowed.

A nonstar has all row weights at least two. Its incidence matrix W obeys WW^T=diag(w_i-1)+J, which is positive definite, so n<=k<=5. The complete nonstar list is:

    n=3, k=3,4,5: I=k+3;
    n=4, k=4,5:   I=k+5;
    n=5, k=5:     I=12.

For n=3 the three pair-meeting points are distinct, and any remaining point is private. For n=4, point multiplicities are at most three and their pair counts sum to six. With k=4 or 5, the only possible patterns are (3,2,2,2) with optional private point. The alternative containing two triple points is impossible: two triples of four rows intersect in at least two rows. For n=5,k=5, multiplicities are at most four and pair counts sum to ten. The only numerical possibilities, in increasing order, are (1,1,2,3,4), (1,2,3,3,3), and (2,2,2,2,4). The first has a triple and quadruple sharing at least two rows. The second has three triples with pairwise intersection at most one, whose union would have at least six rows. Both are impossible. The last is the five-row near-pencil.

Different components use disjoint coordinates in a fiber. Therefore summing the local possibilities gives this complete upper-bound table (component partitions are fixed across fibers):

| Component sizes | Maximum incidence in one fiber |
|---|---:|
| 7 | 11 |
| 1+6 | 10 |
| 2+5 | 10 |
| 3+4 | 12 |
| 1+1+5 | 12 |
| 1+2+4 | 11 |
| 1+3+3 | 10 |
| 2+2+3 | 10 |
| 1+1+1+4 | 10 |
| 1+1+2+3 | 9 |
| 1+2+2+2 | 8 |

No assumption about square blocks in the full support graph is made.

## 3. Excluding 12 and 13; restricting degree 11

Every fiber has incidence at most twelve, so d<=12. If d=12, every fiber must attain twelve. For partition 3+4 this requires the four-row near-pencil on four coordinates and the three-row component repeated on the fifth coordinate. The three rows then have degree seven. For partition 1+1+5 it requires the five-row near-pencil using all five coordinates; the two singleton rows are empty in every fiber. Both contradict degree twelve. Thus d=12,13 are impossible.

At d=11, the table leaves only 7, 3+4, 1+1+5, and 1+2+4.

For 1+2+4, attaining eleven in every fiber requires the four-row near-pencil, the two-row component repeated on the remaining point, and the singleton empty. This contradicts its positive degree.

For 1+1+5, write I_5 for incidence of the five-row component and I_s for the two singletons' combined incidence. If the component is a star with union k, then I_5=k+4 and I_s<=5-k, so

    4 I_5 + 7 I_s <= 51-3k <=48.

If it is a nonstar, (I_5,I_s)=(12,0), giving the same inequality. Summing all seven fibers yields

    34d <=336,

so d<=9. Hence every degree-eleven row group is either a single seven-clique or a 3+4 split.

## 4. Two useful line lemmas

### 4.1 At most one high-multiplicity coordinate per fiber

In any seven-row group, at most one coordinate of a fixed fiber can have multiplicity at least four. Two such coordinates would have to belong to the same component, since two components of size at least four do not fit in seven rows. If that component is a star, only its common point has multiplicity greater than one. If it is a nonstar, its size is at most five, and two four-fold coordinates would share at least two rows, contradicting exact-one intersections.

### 4.2 Lines inside one clique

Suppose every row of a clique contains a full L_u. Each row has a unique such line because d<14. If two clique rows have the same line L_u, their entire intersection is precisely L_u. A third row with a different line L_w cannot have a singleton restriction in any fiber: such a singleton would be {w}, and the first two rows would then meet at both u and w in that fiber. Its degree would be at least fourteen. Therefore either all clique rows have the same line, or all their line labels are distinct.

In the distinct-label case, at most one row can be a singleton in any fiber. Thus a clique of n rows has at least 2n-1 incidences per fiber and

    nd >=7(2n-1).

In particular a three-clique needs d>=12, a four-clique needs d>=13, and a seven-clique cannot have distinct labels at all because only five labels exist.

## 5. Excluding degrees 8, 9, and 10

First, no row can contain a full F_v. A row in a nonsingleton component has at least one entry in every fiber, so a full fiber would give degree at least 5+6=11. A singleton component has some other nonsingleton component in its group (seven rows, at most four components); that component occupies at least one disjoint point in every fiber, again preventing a full fiber.

Suppose a row r also contains no full L_u. Primitive binary cancellation forces r to be disjoint from every row in another G_a with different b. At every supported column, each of the four other groups can contribute at most its unique row with b=b_r. Column degree d therefore forces multiplicity at least d-4>=4 inside r's own group. By Lemma 4.1 there are at most seven such columns in the entire group. But r has degree d>7. Contradiction. Every row contains a unique full line, and has t=d-7<=3 other entries.

Rows with different full lines have intersection size at most 2t<=6. If they are in the same G_a, any nonempty vanishing overlap would have at least seven entries, so their supports are disjoint. If both CRT coordinates differ, primitive cancellation would require a full fiber (already excluded) or a full line (too large). If their b coordinates agree, the order-five character forces equal intersection counts in all five L_u lines. Each row occupies at most its baseline line plus three other lines, leaving one count zero, hence all zero.

Thus distinct line classes have disjoint supports. If n_u rows have baseline L_u, every column on an occupied L_u belongs to exactly those n_u rows. Column degree gives n_u=d. The occupied classes partition all 35 rows, so

    35=hd, 1<=h<=5.

There is no integer solution for d=8,9,10. These degrees are excluded.

## 6. Excluding split groups at degree 11

A row in a 3+4 split cannot contain a full fiber, because the other nonsingleton component occupies a disjoint point in every fiber. If the row also lacked a full line, the same primitive-disjointness argument as in Section 5 would force multiplicity at least 11-4=7 from its own group at every supported column. A split group's column multiplicity is at most four. Contradiction. Therefore every row in a 3+4 group contains a full seven-line.

By Lemma 4.2, each three- or four-clique must have the same line for all its rows: distinct labels require degree at least twelve or thirteen. Each component is consequently a star in every fiber. Since the two components are disjoint, their total fiber incidence is at most 7+5-2=10. Their average would have to be eleven. Contradiction.

There are therefore no split row groups at degree eleven.

## 7. Excluding the remaining single-clique degree-eleven case

All five groups are seven-cliques. By the rank argument every fiber is a star. Its incidence is at most eleven, and the seven fibers total 7*11, so equality holds everywhere. In each fiber a group has one baseline coordinate of multiplicity seven and four private coordinates of multiplicity one. Let B_a be the group's baseline set, one coordinate per fiber. Every row in G_a has B_a plus four extras.

If a column is a baseline for h groups, its degree is 7h+(5-h)=5+6h=11, forcing h=1. The five B_a are pairwise disjoint and partition all columns.

Fix a row r and one of its extras c. This column is on the baseline of another group G. Every row of G meets r at c. For each of the six partners s in G with b_s!=b_r, the character is primitive. Their intersection is contained in the union of their two four-element extra sets because their baseline sets are disjoint, and hence has size at most eight.

If r had no full seven-line, every such nonempty overlap would be exactly one full five-fiber. Row r can contain at most one full fiber, because completing a fiber uses all four of its extras. All six partners would have to contain that same fiber. Yet G has multiplicity one at each of the four off-baseline points in that fiber, so at most one G-row can contain the full fiber. Contradiction. Every row therefore contains a full seven-line.

Within each seven-clique, some two rows have the same line label by pigeonhole. Lemma 4.2 forces all seven rows to have that same line, so B_a itself is a full L_u. Different groups have different baseline lines, since the B_a are disjoint.

Repeat the extra-column argument. Now two rows in different groups cannot have a full line in their intersection: each contains only its own, different, unique full line. Therefore all six primitive overlaps must again be one full fiber of r, and the same six-versus-one contradiction applies. This excludes degree eleven.

Sections 3, 5, and 7 prove the theorem for all six degrees 8 through 13.

## 8. Exact obstruction to extending the retained rectangular control

The accepted 7-by-35 degree-eleven control remains a valid rectangular row Gram. It is not altered or reinterpreted as a square construction. Its original row indices are 0,15,30,10,25,5,20. Six of its rows have neither a full seven-line nor a full five-fiber; row 5 alone contains L_3.

For a particularly small extension certificate, original row 0 contains original column 5, has no full line or fiber, and column 5 has multiplicity two in the retained block. In any hypothetical square extension on the other four row groups, all primitive partners of row 0 must be disjoint from it. Each other group can then contribute at most its one b=0 row at column 5. That column's total degree is at most 2+4=6, whereas a square degree-eleven mask requires eleven. Thus this exact original-phase block cannot be extended. This is a rigorous extension obstruction, not a failed search.

The general theorem is stronger: it rules out all possible degree-eleven row blocks in a full square mask, not only the retained example.

## 9. Reproducible exact evidence and limits

Run `python verify_q7.py` in this directory. It uses the Python standard library only. It exhaustively checks local five-coordinate families through size five, all eleven component partitions, the saturated equality cases and the integer weighted certificate. It also enumerates the twelve possible baseline-label multiplicity cases for a 3+4 split, retaining exact local certificates for their incompatibility with degree eleven.

All CRT congruences and Gram controls are evaluated in original index order using integer polynomial reduction modulo Phi_35. Positive divisor controls and regular negative controls exercise both full row and column Grams. The retained rectangular block is checked directly and its extension obstruction is recomputed from the mask entries. Source files are hash-bound, and the final manifest is sealed.

These controls supplement the proof; no complete square-mask census is claimed. No floating tolerance, optimizer infeasibility flag, unsupported solver, service-limit retry, external write, repository action, owner change, or self-acceptance is used. The broader research task remains open beyond this scoped theorem.
