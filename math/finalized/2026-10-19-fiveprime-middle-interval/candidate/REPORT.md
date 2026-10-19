# Order 5q: exclusion of the entire middle open interval

Date: 2026-10-19 UTC. Owner M-SPARSE-DEFECT; retain TO RESEARCH and priority 42. Proof candidate pending independent review. All work is local. No novelty, historical-priority, Fourier-algorithm improvement, or general support-block claim is made.

## 1. Exact statement, normalization, and dependency boundary

Let q>5 be prime, N=5q, zeta any primitive N-th root of unity, and R a binary N-by-N matrix. Set

    D[r,c] = R[r,c] zeta^(rc),     0 <= r,c < N.

There is no such matrix satisfying D*D=dI at any integer

    2q < d < 3q.

Because D is square and d>0, the hypothesis also gives DD*=dI. Every row and column of R therefore has degree d. Both row orthogonality and column degrees are used in the proof. Equivalently, for the normalized fixed Fourier matrix F_N[r,c]=zeta^(rc)/sqrt(N), no binary entry mask C=F_N entrywise R has either Gram equal to (d/N)I in this interval.

The accepted first-interior exclusions q<d<2q, including the q=7 boundary, and the accepted N=3q classification remain unchanged. None is used to infer a new middle-interval claim. Their reports and independent verdicts are frozen only to bind the exact existing target and prior scope. The proof uses elementary prime-order balance and the classical binary two-prime cancellation lemma, restated below. The inherited inverse-row consequence additionally uses the already accepted equality/attainment theorem and quantitative no-mask bound. Source bindings are in SOURCE_BINDINGS.json.

This packet addresses only 2q<d<3q. It does not claim the endpoints 2q or 3q, the other remaining order-5q intervals, a complete semiprime classification, or the uniform divisibility conjecture.

## 2. Exact CRT coordinates and cancellation

Put e_5=q(q^(-1) mod 5) and e_q=5(5^(-1) mod q), modulo N. These are orthogonal idempotents with e_5+e_q=1. Relabel actual indices by

    r=a e_5+b e_q,    c=u e_5+v e_q,
    a,u in Z/5,      b,v in Z/q.

With alpha=zeta^(e_5), beta=zeta^(e_q), the unchanged original phase is exactly

    zeta^(rc)=alpha^(au) beta^(bv).

Let G_a be the q rows with first coordinate a; F_v the five columns with second coordinate v; and L_u the q columns with first coordinate u.

For distinct rows in G_a, their difference has character order q. Consequently their row supports satisfy

    |S_r intersect S_s intersect F_v| = k(r,s)

independently of v. This is the rational minimal-polynomial identity for the prime root beta. In our interval k is 0, 1, or 2, since qk<=d<3q.

For rows with both a and b different, their difference character is primitive of order 5q. A binary column subset with zero character sum must be a union of complete F_v fibers or a union of complete L_u lines. To see this without changing phases, nonzero coordinate character multipliers can first permute the coordinates. Reducing in the rational basis alpha^i beta^j, 0<=i<4, 0<=j<q-1, gives for its binary array epsilon

    epsilon[i,j]-epsilon[i,q-1]-epsilon[4,j]+epsilon[4,q-1]=0.

Thus epsilon[u,v]=A[u]+B[v] for integer-valued A,B. If both varied, each range would have length at least one, and their sum on the Cartesian grid would have range at least two, impossible for a binary array. One is constant, giving the asserted parallel-line alternative. Empty overlaps are permitted.

The binary two-prime cancellation content is classical, credited to de Bruijn and Lam--Leung, rather than a new lemma of this packet: T. Y. Lam and K. H. Leung, On Vanishing Sums of Roots of Unity, Journal of Algebra 224 (2000), 91--109, Theorem 3.3 and Corollary 3.4, DOI 10.1006/jabr.1999.8089, https://arxiv.org/pdf/math/9511209; N. G. de Bruijn, On the factorization of cyclic groups, Indagationes Mathematicae 15 (1953), 370--377. The self-contained basis argument fixes its precise binary/original-phase scope.

## 3. Column-degree coverage lemma: every supported entry lies on a full cycle

Fix any row r=(a,b), and any c in S_r. Among all rows, at most q+4 have first coordinate a or second coordinate b: there are q in G_a and four more in the other groups with second coordinate b. This count includes r itself.

Our interval satisfies d>=2q+1>q+4, since q>5. Column c has d supporting rows. Hence it contains some supporting row s whose first and second coordinates both differ from r's. The intersection S_r intersect S_s contains c and has a primitive zero character sum. By Section 2, that intersection is a union of full F fibers or full L lines. The full fiber or line through c is therefore contained in S_r.

Apply this to every c in S_r. Let A_r be the set of all u for which L_u is contained in S_r, and B_r the set of all v for which F_v is contained in S_r. We have derived, without assuming a support geometry,

    S_r = (A_r x Z/q) union (Z/5 x B_r).

Put ell_r=|A_r| and f_r=|B_r|. Since d<3q, ell_r<=2. Since d>2q, f_r cannot be zero. The exact degree is

    d = ell_r q + (5-ell_r) f_r.                 (3.1)

A_r and B_r are the complete sets of full lines and fibers in the row. In particular no accidental unlisted full cycle is being excluded.

This is a union-of-cycles conclusion for individual row supports. It is not a Cartesian-product assumption or a decomposition into full square blocks of the whole mask.

## 4. Same-group disjointness collapses the degree to 2q+3

Take distinct r,s in G_a. Their sets B_r and B_s are disjoint. If they shared v, both rows would contain all five columns of F_v, so k(r,s)=5 in that fiber. Prime-order balance would force k=5 in every fiber, giving their whole intersection size 5q, contrary to d<3q.

There are q rows in G_a, and their q nonempty sets B_r lie disjointly in the q-element fiber set. Hence each B_r is a singleton and they partition all fibers. Write B_r={f_a(b)}; the map f_a:Z/q -> Z/q is a bijection.

Equation (3.1) now becomes

    d = 5 + ell_r(q-1),    ell_r in {0,1,2}.

The values for ell=0,1 are 5 and q+4, both below 2q. Therefore every row has ell=2 and

    d = 2q+3.                                           (4.1)

All other degrees in the target interval have already been excluded.

Moreover every row in a fixed G_a has the same two-line set A_a. For distinct r,s in the group, their special fibers f_a(b_r), f_a(b_s) are different. Their intersection has exactly two entries in each special fiber, and |A_r intersect A_s| entries in every other fiber. There is another fiber since q>2. Prime balance makes |A_r intersect A_s|=2; the two two-element sets are equal.

Thus any remaining candidate must have the literal CRT mask

    R[(a,b),(u,v)]=1 iff u in A_a or v=f_a(b),
    |A_a|=2,    each f_a a permutation of Z/q.            (4.2)

This form was proved from both Grams; it was not imposed as a search restriction.

## 5. Column degrees force different baseline pairs

For u in Z/5, let h_u be the number of groups a with u in A_a. At any column (u,v), each such group contributes q rows. Every other group contributes exactly one, because f_a is a permutation. Hence the column degree is

    h_u q+(5-h_u)=5+h_u(q-1).

By (4.1), this is 2q+3, forcing h_u=2 for every u. In particular the five pairs A_a cannot all be identical. Choose a!=a' with A_a!=A_a'. Their intersection has size h in {0,1}.

## 6. A primitive cross-group overlap gives the final contradiction

Fix r=(a,b). In G_(a'), exclude the one row s with b_s=b and the one row s with f_(a')(b_s)=f_a(b). These may be the same row; at most two rows are excluded. Since q>5, some s remains.

The pair r,s has different a and b, so its zero Gram requires primitive binary cancellation. Its special fibers v=f_a(b) and w=f_(a')(b_s) are different. From (4.2), the intersection S_r intersect S_s has

    2 entries in F_v and F_w;
    h=|A_a intersect A_a'| <=1 entries in every other F_t.

This set cannot be a union of full five-column fibers, since its special fibers contain two entries. It cannot be a union of full q-lines, since the fiber cardinalities are not constant. There is at least one other fiber. Both alternatives from Section 2 fail, contradicting the primitive zero Gram.

This excludes the sole remaining degree 2q+3, and proves the whole theorem.

## 7. Exact controls and reproducibility

Run `python verify_middle.py`. The checker is self-authored for this packet and uses only the Python standard library. It does not execute historical scripts. It checks:

- original-index CRT idempotent and phase congruences;
- exact rational-basis reduction of Gram entries, in original index order, without floating tolerances;
- both full Grams and both degree counts for divisor masks at d=1,5,q,5q;
- regular near-masks (4.2) with A_a={a,a+1} and f_a(b)=b, at d=2q+3; all same-group row Grams vanish, but primitive cross-group Grams fail;
- all two-element baseline pair choices and distinct special-fiber choices in a finite primitive-overlap sweep, retaining an explicit nonzero original-phase witness;
- the exact degree reduction and the two-excluded-rows selection bound;
- source-copy hashes and a sealed manifest.

The near-mask is a deliberately negative full-square control. It is not an equality construction: its complete Grams are tested and fail. Its q-by-5q same-group row blocks are exact rectangular controls, illustrating why global constraints are essential. The completed run passed 157,000 full Gram entries, 486,720 primitive-overlap cases, 34,784 cycle-union support cases, 15,368 partner-selection counts, 16 interval-degree reductions, and 37,950 original-phase CRT pair congruences. All seven source copies matched their frozen hashes and RUN.stderr was empty. Finite checks supplement the symbolic proof; no exhaustive square-mask search, optimizer infeasibility, or unsupported numerical observation is used.

## 8. Inherited inverse-row consequence and limits

The separately accepted equality/attainment criterion gives, throughout the newly excluded interval,

    Delta_(5q,5q-d) > sqrt(d/(5q)).

Composing with the already accepted quantitative no-mask bound gives

    Delta_(5q,5q-d)^2 >= d/(5q) + 1/[50 q d^(4q-5)].

Here phi(5q)=4(q-1). This quantitative bound is inherited and nonsharp; no new sharp optimum, sharp rate, or Fourier/FFT complexity improvement is claimed.

The earlier first-interior and N=3q results, prime-power and N=2q classifications, complementary-divisor constructions, and connected (8,4) obstruction to full-square-block geometry are preserved. The owner remains M-SPARSE-DEFECT, TO RESEARCH, priority 42. No external repository or catalogue write, owner closure, or self-acceptance is performed.
