# Independent review: the order-3q, weight-2q Fourier-mask endpoint

Date: 2026-10-19 UTC.

## Verdict and scope

**PASS.** For every prime q>3, there is no binary matrix R of order N=3q such that D[r,c]=R[r,c] zeta^(rc), with zeta any primitive N-th root, satisfies D*D=2q I. The self-contained proof is correct without a repair. The conclusion remains in the original fixed-Fourier-phase binary class. In particular, it does not assume that arbitrary equality masks have full square support components.

This verdict binds the frozen candidate directory `/workspace/shared/sparse_threeq_endpoint_20261019_1054`:

- Manifest SHA-256: `918a8048cf86741e1e58b070f2d96147be53732fb89b53d0274382b3af807b49`
- Report SHA-256: `0f712d2a44f41405de345ce44bd4a76f8d57ab467e5a61d2645363e1cb433453`

The separately accepted strict-upper-range theorem then excludes every 2q<=d<3q. The remaining N=3q interval q<d<2q is not settled here. Neither the complete mixed-prime divisibility conjecture nor a classification of all admissible support patterns follows. M-SPARSE-DEFECT remains TO RESEARCH, priority 42. This review changes no external record or owner status and makes no novelty claim.

## 1. Exact phases, squareness, and cancellation

Let A=q^(-1) modulo 3 and B=3^(-1) modulo q. The CRT idempotents are e_3=qA and e_q=3B modulo N. The actual integer row and column labels satisfy

    r=(r mod 3)e_3+(r mod q)e_q,
    c=(c mod 3)e_3+(c mod q)e_q,
    rc=au e_3+bv e_q modulo N.

Consequently alpha=zeta^(e_3) and beta=zeta^(e_q) have orders 3 and q and satisfy zeta^(rc)=alpha^(au) beta^(bv) exactly. The candidate does not silently replace its phases by a different Fourier pairing. This identity holds for any primitive choice of zeta. The fresh checker also verifies the congruence for all row-column labels and every primitive-root multiplier at q=5,7,11,13,17, including both possibilities for q modulo 3.

From D*D=2qI, D is invertible and DD*=2qI. All row and column degrees are therefore 2q. The proof is allowed to use both the row Gram and column norms even though the theorem initially states only one Gram. In fact column off-diagonal orthogonality is not separately needed after squareness.

For two distinct rows with the same residue a modulo 3, the difference has order q. Grouping the common support by the three-column fibers F_v gives integer coefficients k_v. A degree-at-most-q-1 rational polynomial vanishing at a primitive q-th root is a scalar multiple of Phi_q, so all k_v agree. Since two 2q-subsets of a 3q-set meet in at least q and at most 2q, their fiber counts are uniformly one or uniformly two. The second case gives intersection size 2q and therefore identical full row supports.

The primitive binary overlap lemma is also valid. The products alpha^i beta^j, i=0,1 and 0<=j<q-1, span the field because zeta=alpha beta and the prime relations reduce both exponents. The dimension is 2(q-1), so these products are a basis. Reduction gives epsilon_uv=A_u+B_v. Integer-valued A and B cannot both vary: the range of their sum on a Cartesian product would be at least two, contradicting binary coefficients. Thus any primitive binary vanishing support is a union of complete three-column fibers or complete q-column lines. Multiplying the two coordinates by units preserves these families. No weighted extension is inferred from the binary lemma.

## 2. The full-fiber argument is genuinely global

This is the first point where a shortcut could invalidate the proof. The candidate takes the necessary global step correctly.

If row r contains all three columns of one fiber F_w, no other same-group row can have the identical full support: identical supports would yield fiber overlap three at F_w, which the preceding prime-order balance excludes. Thus r has global overlap q with every other same-group row, and every other row has exactly one entry at F_w. These singleton restrictions must all coincide, because every same-group pair has local overlap at least one. Their pairwise overlaps at F_w are one, hence their global overlaps are q and their local overlaps are one in every fiber. This proves the pairwise-one hypothesis for the entire group in each fiber.

The local statement alone that all pairwise scalar products belong to {1,2} would be insufficient. For example, four copies of the two-subset {0,1} and one copy of {0,1,2} satisfy that weaker statement. The global implication “overlap 2q means identical supports” rules out this misleading local configuration. The independent controls explicitly retain this guard; the candidate proof does not make the shortcut.

For n>=4 binary length-three vectors with pairwise scalar product one, a singleton must occur. If none occurred, a full vector could not coexist with any other vector of weight at least two, and only the three distinct two-subsets would remain, too few. All vectors contain the singleton coordinate. Their extra-coordinate sets are pairwise disjoint, leaving at most two extras total. The total incidence count is at most n+2, with repeated singleton vectors allowed.

Applied to the q rows and q fibers, this bounds incidences by q(q+2), strictly less than 2q^2 at q>=5. Thus a full fiber is impossible. Since each row has 2q entries and each of its q fiber restrictions has size at most two, every restriction has size exactly two. This conclusion follows from the argument; it is not a uniformity assumption based on average degree.

At the smallest permitted q=5, the contradiction is 35<50. The local lemma applies because five is at least four. There is no q=5 boundary exception. The theorem does not cover q=3, where this CRT decomposition would be invalid.

## 3. Repeated functions and primitive partners

Write f_r(v) for the column coordinate omitted by row r in F_v. Two rows in the same group whose functions agree anywhere have local overlap two there, hence global overlap 2q and identical supports. Distinct functions in a group therefore disagree at every v. Evaluation at one fixed v is injective on the distinct functions, giving at most three of them. As q>3, some function is used by two distinct rows. The functions need not be distinct, equidistributed, or attached to prescribed b-labels.

Let f be repeated by rows r_1,r_2 in one a-group. They have distinct b-coordinates. For every row s in another group, at most one of r_1,r_2 has s's b-coordinate. There is therefore a primitive row difference to at least one of the two repeated rows. This primitive partner can depend on s; the argument never requires one partner to work for all other rows.

The support intersection has one or two entries in every fiber, so it cannot be a union of complete three-column fibers. The primitive lemma forces a fixed nonempty set K of one or two u-coordinates in every fiber.

If f is nonconstant, K cannot have size two: the two supports would both equal that same two-subset in every fiber. If K={t}, the omitted values f(v), g(v) must be the two distinct elements other than t. Hence f has precisely those two values, and g is their pointwise swap. If f had three values, no such partner g could exist at all. Thus, in the only possible nonconstant case, f uniquely determines t and g.

Every row in both other groups must then use the same g, not merely a choice from a family of potential partners. A column omitted by g receives no incidence from those 2q rows and at most q from the original group, contradicting its column degree 2q. This is the essential explicit column-norm step. It rules out every nonconstant repeated function.

## 4. Propagation and the final nonprimitive obstruction

Choose a repeated constant function f=f_0. For every row in either other group, the fixed intersection K with the constant support A={0,1,2} minus {f_0} forces its function g to be constant:

- If K=A has size two, then g=f_0 everywhere.
- If K={t}, g is the unique element of A other than t, everywhere.

Both other groups consist only of constant functions. One of these groups again has a repeated function because it has q>3 rows and only three possible constants. Using it as the anchor forces all functions in the original group to be constant as well.

Every row now supports exactly two full q-lines. Choose rows with distinct a but equal b, which are present among the original full set of 3q row labels. Their difference has order three. Their supports intersect in one or two complete q-lines, so their row Gram is

    q times the sum of one or two distinct powers of alpha^(a-a').

It cannot vanish. One term is nonzero; two distinct third roots sum to the negative of the third. This contradicts the row Gram. No unsupported synchronization or matching hypothesis is left at this step. Full q-lines were derived only at the end, and there was never a premise about full square support components.

Checking only primitive differences would miss this obstruction. The regular near-mask R[r,c]=1 iff r mod 3 differs from c mod 3 satisfies all degree conditions and all order-q and order-3q off-diagonal Grams, yet fails every order-three pair. It is an exact negative control, not an equality mask or an endpoint optimizer.

## 5. Fresh independent exact controls

`independent_checks.py` was written for this review. Its mask calculations use integer cyclotomic reduction, with Phi_(3q) independently generated as Phi_q(X^3)/Phi_q(X). Its original inverse reconstructions use SymPy's general-purpose exact rational algebraic fields. It imports no candidate or historical research code. There are no numerical tolerances.

Completed checks in `INDEPENDENT_RESULTS.json`:

1. Twelve newly generated divisor masks, at N=15,21,33 and d=1,3,q,N, pass both full Grams and all row/column degrees.
2. Five newly generated endpoint near-masks, at q=5,7,11,13,17, have degree 2q and vanish in both Gram orders at every order-q and primitive difference. Exactly 6q ordered pairs fail in each Gram, all of order three.
3. Every one of the 32,768 binary subsets at N=15 is checked exactly. The 38 vanishing supports are all unions of one of the two parallel-line families.
4. Every multiset of q length-three binary vectors is tested at q=5,7,11: 792, 3,432, and 31,824 multisets, respectively. Each q has exactly 15 pairwise-one multisets. Their maximum total weights are 7,9,13, respectively. Multiplicity weighting accounts for all labeled configurations; repeated singleton vectors are not discarded.
5. All 59,049 ordered pairs of q=5 missing functions are checked. Exactly 99 have a constant intersection. A constant first function has three constant partners; a first function using two values has exactly one swap partner; a function using all three values has none. There are 3,90,150 first functions of these three types.
6. Three original inverse-model witnesses are independently reconstructed from newly generated N=15 masks with d=1,3,5. For B_tilde=(H-D)*/(N-d), the checker inverts B_tilde exactly to obtain M_tilde. Both inverse products equal I, both Grams of M_tilde-H equal dI, and every inverse row and column has exactly N-d nonzeros. Full rational cyclotomic matrices are retained in `ORIGINAL_MODEL_WITNESSES.json`.

These checks corroborate the analytic proof; no full endpoint-mask census is asserted.

## 6. Frozen candidate data and source integrity

`audit_candidate_data.py` separately reads the frozen candidate only as data. It checks the seal, all manifest entries, and each source copy against its recorded hash and original local file. It repeats the integrity check after its mathematical calculations.

It independently recomputes both complete Grams for all 14 retained positive masks, including the connected order-eight control and its order-24 odd CRT lift. It recomputes all five retained negative controls, verifying every nonzero Gram residue, its squared modulus, its character order, and every zero-count record. These include four endpoint near-masks and one degree-preserving corruption.

For all six retained original-model witnesses, the audit decodes every rational coefficient and verifies the mask Grams, B_tilde's defining formula, E_tilde=M_tilde-H, both inverse products, both error Grams, and every inverse-row and inverse-column support count. It does not trust the witness files' success flags. The exact results and immutable source binding appear in `CANDIDATE_AUDIT.json`.

## 7. Original-model implication, prior art, and limits

At N=3q and d=2q, the original inverse support budget is s=N-d=q>0. The accepted equality-mask criterion gives strict nonattainment of the sqrt(2/3) endpoint. The accepted quantitative no-mask bound directly supplies

    Delta_(3q,q)^2 >= 2/3 + 1/[30q (2q)^(2q-3)],

since phi(3q)=2(q-1). This is a correct substitution into an inherited bound, not a new gap rate or an exact nonsharp optimum. The d=N divisor controls are only mask controls and are not offered as s=0 invertible inverse-model witnesses.

The candidate credits the previously unaccepted endpoint lead and the accepted earlier results. Its primitive vanishing-sum ingredient has classical provenance. I independently checked the mathematical attribution to Lam and Leung, Theorem 3.3 and Corollary 3.4 on printed pages 7–8 of their [primary preprint](https://arxiv.org/pdf/math/9511209). Those statements give the two-prime prime-cycle structure, and the text traces it to de Bruijn. At squarefree order, a binary coefficient set cannot contain cycles in both directions because they intersect. This supports the cited ingredient; it is not a historical-priority investigation for the masked Fourier endpoint theorem.

No external service, repository, table, registry, owner status, or priority was modified. The only writes are this independent local review packet. No candidate or historical research program was imported or executed.
