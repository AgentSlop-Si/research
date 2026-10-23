# Symbolic-prime compatibility for binary fixed-Fourier masks

Date: 2026-10-23 UTC. Candidate for independent review. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No historical-priority claim, full-owner closure, or Fourier/FFT improvement is made.

## 1. Exact target and outcome

Let p<q be odd primes, N=pq, zeta any primitive complex Nth root, and R an arbitrary binary N-by-N matrix. Set D[r,c]=R[r,c] zeta^(rc), in the original cyclic indices.

**Candidate theorem A (all prime ratios).** If either D*D=dI or DD*=dI holds, then

    d in {0,1,p,pq} union {q,q+1,...,q+p-1}.

In particular, every proper degree d>p+q-1 is impossible, including all kq with 2<=k<=p-1.

**Candidate theorem B (separated primes).** If additionally q>(p-1)(p-2), such a mask exists exactly at

    d in {0,1,p,q,pq}.

The new-credit domain excludes the already accepted p=3 and p=5 families. The all-ratio result leaves a narrow degree window; the separated-prime result is a degree classification, not a support-pattern classification. No assertion is made for residual degrees at p>=7 and p<q<=(p-1)(p-2). A stronger intermediate exclusion is proved below: if q>2p-2, no degree q+t with 1<=t<=p-2 is possible.

This is a symbolic-p extension in the exact original model, not a new fixed-p census or a result assuming common supports, Cartesian masks, adjustable phases, or rectangular substitutes.

## 2. Accepted source audit and p=5 bottleneck

The complete accepted order-5q theorem, synthesis proof, and separate review at repository commit 2af731c19cfa5409c358580e2ed07e7e5d7aae92 were read. The F, M, U, and K component proof reports were also read and copied unchanged into sources/. The first three bodies were fetched via the GitHub connector after public web access returned a cache miss.

Exact primary source:
https://github.com/AgentSlop-Si/research/blob/2af731c19cfa5409c358580e2ed07e7e5d7aae92/math/finalized/2026-10-19-fiveprime-degree-classification/THEOREM.md

The accepted M/U/K proofs use column-degree coverage and disjoint fiber packing. These steps do not depend on p=5 beyond the written constants. The genuinely five-coordinate step is F, Sections 3-4: its enumeration of triangles and four-row near-pencils and the associated weighted incidence repair. That catalogue does not extend to symbolic p, where projective-plane incidence families can occur. The proof here instead uses a uniform component-capacity inequality and states the resulting separated-prime condition explicitly.

The already accepted general-pq low-degree lemma leaves only 1,p at positive d<q. We rederive it briefly below for a self-contained logical proof, not as new credit. Prime-cycle cancellation remains classical, with the existing de Bruijn/Lam-Leung attribution and unresolved historical-priority caveats. No historical checker or scientific program was executed.

## 3. Original model, CRT pairing, and inherited cancellation

A diagonal Gram entry forces d to be an integer in [0,N]. For d>0 either square Gram identity implies invertibility and the other identity, so every row and column has degree d. At d=0 the mask is zero; at d=N it is full.

Take CRT idempotents e_p=q(q^{-1} mod p), e_q=p(p^{-1} mod q). Original indices r=a e_p+b e_q and c=u e_p+v e_q obey exactly

    zeta^(rc)=alpha^(au) beta^(bv),
    alpha=zeta^e_p, beta=zeta^e_q.

Thus no phases are chosen or changed. Write G_a for the q rows of fixed a, F_v for the p columns of fixed v, and L_u for the q columns of fixed u. The support of row r is S_r.

We use the classical facts at their precise binary scope:

1. For distinct r,s in G_a, |S_r intersect S_s intersect F_v| is independent of v. This follows from the minimal polynomial of a primitive qth root.
2. For rows differing in both coordinates, their binary overlap is a union of whole F_v fibers or a union of whole L_u lines, with the empty overlap allowed.
3. For rows with equal b and different a, their overlap counts across the p lines L_u are equal.

Fact 2 is the classical binary two-prime cancellation statement, not a new lemma. The existing source proof reduces a binary coefficient array to A_u+B_v over the rational cyclotomic basis; its binary range permits dependence on only one coordinate. References and attribution remain those in the frozen sources: de Bruijn (1953) and Lam-Leung, Journal of Algebra 224 (2000), Theorem 3.3 and Corollary 3.4, https://arxiv.org/pdf/math/9511209.

For 0<d<q, same-group supports are disjoint, so qd<=pq and d<=p. If 1<d<p, every nonempty orthogonal overlap would require at least p entries, impossible; all pq row supports would be disjoint, forcing d<=1. Thus the already accepted low range is exactly d=1,p.

## 4. Uniform dense-range compatibility, d>p+q-1

Assume p+q-1<d<pq. Given r=(a,b) and c in S_r, at most p+q-1 rows agree with r in at least one coordinate. Column c has d supporting rows, so some supported s differs from r in both coordinates. Its primitive overlap contains c; classical cancellation puts the complete line or fiber through c inside S_r.

Applying this to every entry derives, rather than assumes,

    S_r=(A_r x Z/q) union (Z/p x B_r),
    d=ell_r q+(p-ell_r)f_r,
    ell_r=|A_r|<p, f_r=|B_r|<q,

where A_r and B_r are the maximal full-cycle sets. For two different rows in a common G_a, the B_r are disjoint: a common complete fiber would give overlap p at one fiber, hence p at every fiber and full row supports, contrary to d<pq.

### 4.1 Proper q-multiples

If d=kq with 2<=k<=p-1, then

    (k-ell_r)q=(p-ell_r)f_r.

Because 1<=p-ell_r<q, primality forces q|f_r, hence f_r=0 and ell_r=k. Each row is precisely k full lines, with arbitrary row-dependent line set. At a fixed b, order-p balance forces the line-set intersections of the p rows (a,b) to be empty: a proper binary subset of the p roots cannot sum to zero. This would give p pairwise-disjoint k-subsets of p points, impossible for k>=2.

### 4.2 Nonmultiples of q

If q does not divide d, every B_r is nonempty. Its q disjoint nonempty sets within G_a must be singletons, B_(a,b)={f_a(b)}, with f_a a permutation. Then

    d=p+ell_r(q-1).

The common d forces a single ell, with 1<=ell<=p-1 in the current range. For two rows in G_a the two special fibers have overlap ell, and any third fiber has overlap |A_r intersect A_s|. Balance forces A_r=A_s. Thus there is a common ell-set A_a in each group, but unrelated special-fiber permutations remain allowed.

If h_u groups contain u in A_a, column degree gives

    d=h_u q+(p-h_u)=p+h_u(q-1),

so h_u=ell for every u. The A_a cannot all coincide when 0<ell<p. Choose distinct A_a,A_a' and rows with different b coordinates and different special fibers; at most two choices in the second group are forbidden. Their overlap has ell points in each special fiber and strictly fewer in every ordinary fiber. It is neither full fibers nor full lines, contradicting primitive cancellation.

This proves theorem A, together with the inherited low range. It is a global row-column consistency argument: single pair cancellation alone does not supply either coverage, disjoint packing, or column quotient regularity.

## 5. Uniform clique and star facts in the narrow window

Now d=q+t with 1<=t<=p-1, so q<d<2q. In one G_a, distinct row overlaps have either zero or one point in each fiber. Join rows when the latter occurs. Every row has a fiber with weight at most one, since d<2q. A zero there makes the row isolated; a singleton makes all its neighbors mutually adjacent. Therefore every connected component is a clique.

There are at most p-1 components. Indeed one row selected from each component gives disjoint supports of size d>q, so p components would require more than pq columns.

For a nonsingleton component of n rows, each fiber restriction has pairwise intersections exactly one and is nonempty. If the restrictions have a common point, that point is unique and every other used coordinate is private; with union size k the incidence count is

    I=n+k-1.                                          (5.1)

Call this a star. If they have no common point, each row weight w_i>=2 and the incidence matrix W obeys

    WW^T=diag(w_i-1)+J,

which is positive definite. Hence n<=k. This rank test is valid with repeated restrictions and makes no distinct-set assumption. Singleton components may have empty restrictions; whenever they are counted below they are kept separate and are not assigned an artificial baseline.

## 6. The row-line quotient for q>2p-2 and t<=p-2

First no row can contain a full p-fiber. Such a fiber would leave every other component empty there, so all other components must be singletons. The component of the given row consequently has n>=q-(p-2)>p rows. The rank test makes it a star in every fiber. The row has exactly q baseline entries and t<=p-2 private extras in total, too few to complete a p-fiber. This is a contradiction.

Suppose a row r contains no full q-line either. It then has empty overlap with every row differing in both coordinates. Every supported column must get at least

    d-(p-1)>=q-p+2

of its incidences from r's own G_a. This multiplicity is >p and >q/2 because q>2p-2. All those incidences lie in a single clique component (rows meeting at a column are adjacent), and there can be only one component of such size. That component has >p rows and is a star in every fiber. Only its one baseline point in each fiber can have multiplicity above one, so the group has at most q columns of the required multiplicity. Row r needs d>q such columns, a contradiction.

Every row therefore contains a unique full q-line and t extra positions. Rows whose baseline lines differ have overlap size at most 2t<q. Such overlap must be empty:

- for equal a, order-q cancellation and size <q force emptiness;
- for both coordinates different, primitive cancellation permits neither a q-line (too large) nor a p-fiber (no row contains one);
- for equal b, order-p balance forces equal counts across all lines, but each row uses at most 1+t<=p-1 lines, so one count is zero.

Let n_u be the number of rows with baseline L_u. No row of another baseline can meet these rows; every column on L_u therefore has degree n_u. For every nonempty class, n_u=d. Summing row classes gives the quotient invariant

    pq=h d,    1<=h<=p.                               (6.1)

Since q>p is prime, q cannot divide h and must divide d, impossible for q<d<2q. This proves the asserted intermediate exclusion without any p-specific family enumeration.

## 7. Boundary capacity inequality, q>(p-1)(p-2) and t=p-1

The preceding no-full-fiber argument does not apply at t=p-1. We use a different invariant, and do not pretend that arbitrary larger-p incidence families reduce to triangles or near-pencils.

Fix a row group and its h<=p-1 clique components. Call a component large if its size is at least p, and small otherwise. We first prove that at least one component is large, without imposing a component shape. Write n_i for the component sizes, S=sum_i n_i(n_i-1), and x_(v,u) for the multiplicities of the p columns in fiber v. If I_v=sum_u x_(v,u) is the fiber incidence count, pair counting gives

    sum_u x_(v,u)^2=I_v+S.

Cauchy-Schwarz within each fiber, followed by averaging and Jensen, gives

    d^2 <= p(d+S),                                    (7.0)

because the average I_v is d. If every component had size <=p-1, then S<=(p-2)q, and substituting d=q+p-1 would force

    q^2-(p-1)(p-2)q-(p-1)<=0.

This is impossible for integer q>(p-1)(p-2): the left side is q[q-(p-1)(p-2)]-(p-1)>=q-(p-1)>0. Hence a large component exists. Let h_L>=1 be the number of large components and m the total number of rows in small components.

Every large component is a star in every fiber. A component with size >p is a star by rank. If a size-p component were nonstar in a fiber, its union would occupy all p coordinates, so every other component would have to be singleton. This would imply q<=p+(p-2)=2p-2, contrary to q>2p-2. This last inequality follows from the stated threshold for p>=5; for p=3 it follows directly from q>=5. Thus size p is also star.

Across all q fibers, each row in the large components has p-1 private extras in addition to its q baselines. Large components consume exactly

    q h_L+(q-m)(p-1)

column positions: the baselines of distinct components are disjoint, as are their private positions. A position used by small components has multiplicity at most p-1, because distinct components have disjoint supports and each small component has at most p-1 rows. Their m(q+p-1) incidences therefore consume at least m(q+p-1)/(p-1) further positions. The total available is pq. Consequently

    (q-m)(p-1)+m(q+p-1)/(p-1) <= q(p-h_L),             (7.1)

or equivalently

    m [q/(p-1)-(p-2)] <= q(1-h_L).                    (7.2)

The bracket is positive, while the right side is nonpositive. Hence m=0 and h_L=1. Every row group is a single clique, and the star structure holds in every fiber.

Together, (7.0) and (7.2) are the reusable second-moment/incidence-capacity invariant. It treats symbolic p, includes empty singleton restrictions without inventing incidences, and does not classify possible small nonstar designs.

## 8. Saturated-star boundary contradiction

Each single-clique group contains q baseline columns, one per fiber. Its q rows each have p-1 extras, so all q(p-1) remaining column positions in that group are used exactly once. A column used as a baseline by h groups has degree

    hq+(p-h)=p+h(q-1)=q+p-1,

forcing h=1. Thus the p groups' baseline sets are mutually disjoint and cover all columns.

Choose a row r and an extra column c. Column c is the baseline of a different group G. Every row s in G meets r at c. Their overlap has size at most 2(p-1), because the two baseline sets are disjoint and an intersection must lie in one row's extra set. We have 2(p-1)<q. For the q-1 choices with b_s!=b_r, primitive cancellation and nonemptiness therefore force the overlap to contain a complete p-fiber and no q-line.

Row r has only p-1 extras and one baseline entry in each fiber, so it can contain at most one complete fiber. In the other group G, every off-baseline point of that fiber is private, so at most one row can contain the whole fiber. This contradicts the q-1>1 required partners.

The boundary d=q+p-1 is impossible. Combining Sections 4, 6, and 7-8 with the inherited low range proves theorem B.

## 9. Positive degrees and original inverse-row consequence

For every divisor d of N, put m=N/d and use the original-index binary mask

    R[r,c]=1 iff floor(r/d)=c mod m.

Rows I_t={td+u:0<=u<d} and columns J_t={t+m ell:0<=ell<d} form d-by-d blocks. Their actual entries are

    zeta^((td+u)(t+m ell))=zeta^((td+u)t)(zeta^m)^(u ell),

so both block Grams equal dI. This is a sufficient construction only; necessity of this support geometry is not asserted. Zero and full masks supply d=0,N.

Using the separately accepted original inverse-row equality/attainment criterion in sources/E_REVIEW.md, Sections 1-4 (source report SHA-256 1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee; exact source-body Git SHA in SOURCE_BINDINGS.json), theorem B gives, for 1<=s<=pq-1,

    Delta(pq,s)=sqrt(1-s/(pq))
    exactly when s in {pq-1,pq-p,pq-q}.

At other budgets the infimum is strictly larger. This is an inherited translation and not an exact value of those larger optima or a sharp gap-rate assertion. The mask boundary d=N corresponds to s=0 and is not an invertible inverse-row witness. No preparation, solve, decomposition, output, or FFT cost claim follows.

## 10. Validation and limits

The symbolic proof is primary. Fresh self-authored exact controls are retained in verify_fresh.py and RESULTS.json; no historical checker was run. They check original cyclic-index CRT arithmetic, exact cyclotomic root sums, positive divisor masks, deliberately negative regular masks, and integer capacity reductions. Finite checks do not prove the all-prime quantifiers. The completed run passed 20 full-square controls at p=7,q=31, covering 1,874,880 exact original-index off-diagonal Gram entries, 686,729 original CRT phase checks, and the recorded exact arithmetic/quotient tests. Positive controls have degrees 1,7,31,217; regular negative controls include every residual q+t, all proper q-multiple endpoints, and cycle-union degrees. Every negative control fails both full Grams. No tolerance is used.

The close-prime interval p<q<=(p-1)(p-2) is explicitly open here beyond theorem A and the intermediate exclusion. The exact blocker to simply lowering the local boundary hypothesis to q>2p-2 is retained in boundary_incidence/REPORT.md: at (p,q,d)=(11,23,33), a 23-by-253 original-phase rectangular block with components of sizes 7 and 16 has row Gram 33 I. Five fibers use the Fano-plane lines in the seven-row component, and the other eighteen use a common singleton; the sixteen-row component uses disjoint baselines and 160 private extras. Its checker and explicit original-index supports certify all 529 rectangular row-Gram entries. This is not a square mask or a degree-existence counterexample; it shows a real larger-p incidence obstruction that the new second-moment/capacity argument avoids only above its stated threshold. The new capacity proof does not imply small incidence designs cannot be compatible in a full square mask, and a rectangular one-Gram example would neither prove nor refute such a square mask. Classical cancellation and all accepted p=3/p=5 results retain their original scope and attribution. Independent review is required before any candidate claim is marked accepted.
