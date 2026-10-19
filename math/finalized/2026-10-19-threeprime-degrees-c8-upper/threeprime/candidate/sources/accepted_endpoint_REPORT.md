# The order-3q, weight-2q endpoint is impossible

Date: 2026-10-19 UTC. Research owner M-SPARSE-DEFECT, priority 42.
Disposition: a self-contained proof candidate with fresh exact controls, pending independent review. The wider owner remains TO RESEARCH.

## 1. Theorem and scope

**Theorem.** Let q>3 be prime, N=3q, and let zeta be any primitive N-th root of unity. There is no binary matrix R of size N by N such that

    D[r,c] = R[r,c] zeta^(rc),       D*D = 2q I_N.

Equivalently, no original fixed-Fourier-phase equality mask exists at (N,d)=(3q,2q). Squareness makes D*D=2qI and DD*=2qI equivalent. The proof uses the row Gram and the column norms explicitly; it does not change the admissible mask class, substitute a weighted quotient, or assume support components are full square blocks.

This settles the formerly unproved lower endpoint of the accepted upper-range exclusion for N=3q. In combination with that accepted result, all 2q<=d<3q are impossible. It leaves the interior q<d<2q unresolved. It does not prove the general mixed-prime divisibility conjecture or classify arbitrary odd-semiprime masks.

The proper original inverse-row consequence, using the separately accepted equality-mask criterion and attainment result, is

    Delta_(3q,q) > sqrt(2/3).

The inherited quantitative bound, if used, gives

    Delta_(3q,q)^2 >= 2/3 + 1/[30q (2q)^(2q-3)].

Here phi(3q)=2(q-1). This is only a substitution into an accepted bound, not a new sharp error formula or a new gap method.

## 2. Exact CRT phases and the two elementary cancellation facts

Let e_3=q(q^(-1) mod 3) and e_q=3(3^(-1) mod q), regarded modulo 3q. They are the CRT idempotents: e_3 is 1 modulo 3 and 0 modulo q, e_q is 0 modulo 3 and 1 modulo q, e_3+e_q=1, e_3e_q=0, and each is idempotent modulo N.

Write rows and columns as

    r=a e_3+b e_q,      c=u e_3+v e_q,
    a,u in Z/3,        b,v in Z/q.

Define alpha=zeta^(e_3) and beta=zeta^(e_q). Then alpha has order 3, beta has order q, and the original, unchanged phase satisfies exactly

    zeta^(rc)=alpha^(au) beta^(bv).

Thus CRT here is only a relabeling of the original matrix. No independent phases are chosen. Let F_v={(u,v): u in Z/3} be a three-column fiber and L_u={(u,v): v in Z/q} a q-column line. Let G_a be the group of q rows whose first coordinate is a.

We will use two facts, with proofs included.

**Prime-order balance.** If rational coefficients k_v satisfy sum_v k_v beta^(hv)=0 for nonzero h modulo q, then all k_v are equal. Indeed beta^h has minimal polynomial 1+X+...+X^(q-1), so any polynomial of degree at most q-1 vanishing there is a rational multiple of this polynomial. This includes zero coefficients.

**Binary primitive-character lemma.** If epsilon_(u,v) is binary and

    sum_(u,v) epsilon_(u,v) alpha^(h u) beta^(k v)=0,
    h!=0 mod 3, k!=0 mod q,

then its support is a union of full F_v fibers or a union of full L_u lines.

To prove it, relabel u and v by the units h and k. The 2(q-1) products alpha^i beta^j, 0<=i<2 and 0<=j<q-1, span Q(zeta): reduce alpha^2 and beta^(q-1) by their prime cyclotomic relations. Since [Q(zeta):Q]=phi(3q)=2(q-1), they are a basis. Reduction of the vanishing sum therefore gives

    epsilon_(i,j)-epsilon_(i,q-1)-epsilon_(2,j)+epsilon_(2,q-1)=0.

For all u,v, put A_u=epsilon_(u,q-1)-epsilon_(2,q-1) and B_v=epsilon_(2,v). Then epsilon_(u,v)=A_u+B_v, including the boundary row and column. A and B are integer-valued. If both varied, each would have range at least one, so their sum over the Cartesian product would have range at least two, impossible for binary epsilon. Hence one is constant, giving precisely one of the two asserted parallel-line forms. Relabeling by units preserves both line families. Conversely either line form vanishes because a complete nontrivial prime character sums to zero.

The primitive binary lemma is classical in content, and is not presented as a new vanishing-sum theorem. Section 8 gives its prior-art credit.

## 3. Same-group overlaps constrain every fiber

Assume a mask exists. D*D=2qI gives every column degree 2q. It also makes D invertible, so DD*=2qI, and every row degree is 2q.

For distinct r,s in G_a, their difference has only a nonzero q-coordinate. Define

    k_v=|S_r intersect S_s intersect F_v|.

Their exact row Gram and prime-order balance show that k_v is a constant k. Since both supports have size 2q in a universe of size 3q,

    q <= |S_r intersect S_s| <= 2q.

Consequently k is 1 or 2. The case k=2 holds if and only if the two complete supports are identical, because their intersection then has their full size 2q. Otherwise they have one common column in every fiber.

We next prove that every individual row has exactly two entries in every F_v. This is a deduction, not an assumption based on its average degree.

Suppose a row r in G_a contains all three entries in one fiber F_w. It cannot have the same complete support as any other row: such a pair would have local overlap three at F_w, whereas the preceding balance allows only one or two. Thus r has overlap q with every other row in G_a, and each other row has exactly one entry in F_w. These singleton restrictions must all be the same singleton, because any two distinct rows have local overlap at least one at F_w. Their mutual local overlaps are therefore one. It follows that every pair of distinct rows in G_a, including pairs not involving r, has overlap q and local overlap one in every fiber.

Use the following elementary counting lemma. If n>=4 binary vectors of length three have pairwise scalar product one, their total weight is at most n+2. A zero vector cannot occur. If all weights were at least two, a weight-three vector could not coexist with another vector, and the remaining vectors would have to be distinct two-subsets. There are only three such subsets, contradicting n>=4. Hence a singleton occurs. All vectors contain its coordinate, and the sets of extra coordinates in different vectors are disjoint. Only two coordinates remain, so at most two extras occur in total. This proves the lemma, including repeated singleton vectors.

Apply it with n=q separately in each of the q fibers. The number of incidences in G_a is at most q(q+2), whereas its q rows of degree 2q require 2q^2 incidences. Since q>=5, q(q+2)<2q^2, a contradiction.

No row can contain three entries in any fiber. Each has degree 2q across q fibers and therefore has exactly two in every fiber.

Define the missing-column function f_r:Z/q -> Z/3 by

    S_r intersect F_v = F_v minus {(f_r(v),v)}.

For distinct rows in one G_a, agreement f_r(v)=f_s(v) at even one v gives local overlap two, hence identical complete supports and f_r=f_s. Distinct missing functions in one group therefore differ at every v. Evaluating at any fixed v is injective on the set of distinct functions, so that set has at most three elements. Since q>=5, at least one function is repeated by two distinct rows of each G_a.

## 4. A repeated missing function must be constant

Fix G_a and a function f shared by two distinct rows r_1,r_2. Their b-coordinates differ. Take any row s in either of the other two groups and write its missing function as g. At most one of r_1,r_2 has the same b-coordinate as s. Choose the other one. The chosen row and s differ in both CRT coordinates, so their difference character is primitive of order 3q.

Their intersection has either one or two entries in every F_v. The primitive binary lemma cannot represent it as a union of full three-element fibers, because such a union would have zero or three entries per fiber. It is therefore a union of q-lines. Equivalently, there is a fixed nonempty K subset of Z/3, of size one or two, such that for every v

    (Z/3 minus {f(v)}) intersect (Z/3 minus {g(v)}) = K.    (4.1)

Suppose f were nonconstant. Then |K| cannot be two: a two-element intersection would be both of the two-element sets and would make f constant. Write K={t}. For every v, f(v),g(v),t are then the three different elements of Z/3. In particular f takes values in the two-element complement of {t}. Because it is nonconstant, it takes both, so its image determines t uniquely, and g is uniquely determined as the pointwise swap between those two values.

This argument applies to every s in both other groups, even though the chosen primitive partner among r_1,r_2 may depend on s. All 2q of those rows must have that same missing function g. Choose any v. The column (g(v),v) has no entries from those 2q rows and at most q entries from G_a. Its degree would be at most q, contradicting its required degree 2q from D*D.

Thus every repeated missing function is constant. The column-degree condition is essential at this point of the proof as written, so the argument has not dropped the second Gram.

## 5. Constancy propagates to all rows

Choose a repeated function f in G_a; Section 4 proves it is a constant f_0. For every row s in either other group, equation (4.1) again holds with a fixed K. Let A=Z/3 minus {f_0}.

If |K|=2, then K=A and the other two-element set equals A, so g=f_0 is constant. If |K|=1, say K={t}, then g(v) must be the unique element of A minus {t}, for every v. Indeed that is exactly the element of A that the other two-element support omits. Thus g is again constant.

Both other groups now contain only constant missing functions. Choose one of those groups. Its q>=5 rows have only three possible constant functions, so one is repeated. Apply the same argument with this group as the anchor to every row of the original G_a. Those remaining functions are constant as well.

Every row support is therefore a union of exactly two full q-lines L_u.

## 6. The final order-three obstruction

Fix b and choose two rows (a,b),(a',b) with a!=a'. Their row difference has order three. Each support is the union of two of the three q-lines. Their intersection is the union of one or two such lines, with an index set J of size one or two. Their exact row Gram is

    q sum_(u in J) alpha^((a-a')u).

It is nonzero. A single third root is nonzero; the sum of two distinct third roots is the negative of the remaining third root and is also nonzero. Equivalently, prime-order balance would require the binary coefficient vector of J to be constant, which it is not.

This contradicts DD*=2qI. The theorem is proved for every prime q>3, including q=5. In particular, the proof does not end after checking only primitive row differences: the missing order-three pairs are precisely the final obstruction.

## 7. Fresh exact controls in the original model

The new standard-library program verify_endpoint.py imports or executes no historical research code. It generates cyclotomic polynomials by exact division, reduces every original exponent modulo Phi_N, and uses rational cyclotomic arithmetic for matrix inversion. No floating-point tolerances or solver conclusions enter any claim.

Its controls are independent corroboration of the displayed identities, not a census proof:

- Divisor masks at N=15,21,33 and d=1,3,q,3q are checked in both full Gram orders. The accepted connected (8,4) mask and its connected (24,12) odd CRT lift are retained literally as positive controls. No arbitrary support is reduced to full square blocks.
- For q=5,7,11,13, the regular endpoint near-mask R[r,c]=1 exactly when r mod 3 differs from c mod 3 has degree 2q in every row and column. In both Gram orders, all order-q and primitive order-3q off-diagonal entries vanish exactly. Precisely the 6q ordered order-three entries fail, each with squared modulus q^2. This all-q countercontrol has the structure forced at the last proof stage and isolates the final obstruction. It is not an equality mask.
- A degree-preserving 2-by-2 switch in a true divisor mask retains every row/column count and fails both exact Grams.
- Small local exhaustive checks corroborate the length-three intersection bound, the binary primitive lemma, and the fixed-intersection missing-function logic. No full endpoint mask census is performed or needed.
- Proper divisor controls at (N,d)=(15,1),(15,3),(15,5),(21,3),(21,7), and the connected (8,4) mask are reconstructed in the original invertible inverse-row problem. With H[r,c]=zeta^(rc), A=H-D, B_tilde=A*/(N-d), and M_tilde=B_tilde^(-1), the program verifies both inverse products, every inverse row and column support N-d, and both error Grams of E=M_tilde-H equal to dI. Thus M=M_tilde/sqrt(N) has the original simultaneous inverse-row budget and squared spectral error d/N. Full exact matrices are retained.

The completed run passes 14 positive masks, four endpoint near-mask countercontrols, one degree-preserving corruption, and six full original-model inverse witnesses. It evaluates 11,161 row-Gram entries and 11,161 column-Gram entries, 3,242 inverse-product entries, and 3,242 error-Gram entries. The local checks cover 36,048 length-three multisets, 32,768 order-15 binary supports, and 59,049 ordered pairs of q=5 missing functions. Standard error is empty. RESULTS.json and the four control files retain the check counts and exact witnesses. These checks neither manufacture an endpoint optimizer nor replace the analytic nonexistence proof.

## 8. Provenance, prior art, and limitations

The accepted order-2q classification and general-pq small-density/strict-upper-range results are inputs, not contributions of this packet. The report and independent review are copied under sources with SHA-256 bindings. This packet does not repeat their already-proved N=2q theorem as the target.

The prior unaccepted ENDPOINT_3Q.md lead supplied the endpoint argument architecture. Every step has been independently derived here, including the local incidence bound, multiplicity argument, exact CRT phases, use of column norms, propagation, and the final order-three contradiction. The lead is copied and credited as a source; this packet does not claim independent discovery of the architecture or historical priority. Its contribution is a self-contained completed derivation and original exact controls submitted for independent review.

The vanishing-sum ingredient belongs to classical work. Lam and Leung, “On Vanishing Sums of Roots of Unity,” Journal of Algebra 224(1) (2000), 91–109, Theorem 3.3 and Corollary 3.4, describe nonnegative relations for orders with at most two prime factors in terms of prime cycles. Their account traces this structure to de Bruijn. At squarefree order 3q, binary coefficients prohibit mixing a three-cycle and a q-cycle because the two lines intersect, giving the parallel-line lemma used here. Our elementary basis proof above is self-contained and makes no novelty claim for it. Verified primary sources: https://arxiv.org/pdf/math/9511209 (preprint, printed pp. 7–8) and https://doi.org/10.1006/jabr.1999.8089 (published bibliographic record).

The exact endpoint exclusion for these masked Fourier matrices is not asserted to be historically new; the limited citation check is not a priority search. The minimal-polynomial and CRT facts are standard. Complementary-divisor sufficiency, the equality criterion, the original-model attainment implication, the quantitative gap bound, prime-power classification, and connected controls are retained with their existing credits and scopes.

What remains open includes q<d<2q at N=3q, larger odd-semiprime interior ranges, general mixed-prime divisibility, remaining nonsharp optima, sharper gap rates, and the wider owner's other obligations. No conclusion about arbitrary phases, weighted CRT descent, or a full-block classification follows. M-SPARSE-DEFECT remains TO RESEARCH / priority 42.

All source artifacts were read as data. All writes were confined to this new local packet. No external service, repository, registry, status table, owner status, or priority was changed. No historical program was run. MANIFEST.json and SEAL.sha256 freeze the packet after its controls finish.
