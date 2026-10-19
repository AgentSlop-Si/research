# Order 5q: exclusion of the three proper q-multiple endpoints

Date: 2026-10-19 UTC. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. Local proof candidate pending independent review. No historical novelty, support-block classification, Fourier/FFT improvement, external write, or owner closure is claimed.

## 1. Precise statement and scope

Let q>5 be prime, N=5q, and zeta any primitive Nth root of unity. For an arbitrary binary N-by-N matrix R, define

    D[r,c] = R[r,c] zeta^(rc),    0 <= r,c < N.

There is no such R with either square Gram identity D*D=dI or DD*=dI at any of the three degrees

    d = 2q, 3q, 4q.

Either Gram identity implies the other because D is square and d>0. Thus every row and every column has exactly d supported entries. Equivalently, no binary mask of the normalized fixed Fourier matrix has scalar Gram (d/N)I at these three degrees.

This packet settles only these endpoints. It does not claim the remaining interval 4q<d<5q, the range d<=q, a complete order-5q classification, or any other semiprime order. All previously accepted interval results and their limits remain unchanged. Frozen accepted middle/upper reports and independent verdicts bind the model and prior scope; the endpoint proof below is self-contained and does not treat an interior theorem as an endpoint theorem.

## 2. Literal CRT phases and primitive binary cancellation

Choose the orthogonal idempotents modulo N

    e_5 = q (q^(-1) mod 5),    e_q = 5 (5^(-1) mod q).

Write the original indices as r=a e_5+b e_q and c=u e_5+v e_q, with a,u in Z/5 and b,v in Z/q. Put alpha=zeta^(e_5) and beta=zeta^(e_q). These have orders 5 and q, and the original, unchanged phase is exactly

    zeta^(rc) = alpha^(au) beta^(bv).

Let L_u be the complete q-column line with fixed u, and F_v the complete five-column fiber with fixed v.

If two rows differ in both CRT coordinates, their difference character has order 5q. A binary subset of the column grid whose sum against that character is zero is a union of complete L_u lines or a union of complete F_v fibers. Empty subsets are allowed. This classical two-prime binary cancellation fact can be seen directly: permute coordinates by the two nonzero character multipliers, and expand in the rational basis alpha^i beta^j, 0<=i<4 and 0<=j<q-1. A zero sum for a binary array epsilon gives

    epsilon[i,j]-epsilon[i,q-1]-epsilon[4,j]+epsilon[4,q-1] = 0.

Consequently epsilon[u,v]=A[u]+B[v] for integer A,B. If both varied, each would have integer range at least one, and the range of their sum on the Cartesian grid would be at least two, contradicting binary values. One is constant, giving exactly the stated parallel-cycle alternatives. The basis has 4(q-1)=phi(5q) elements and spans the cyclotomic field, so it is indeed a basis.

This cancellation lemma is classical, not asserted as novel: T. Y. Lam and K. H. Leung, On Vanishing Sums of Roots of Unity, Journal of Algebra 224 (2000), 91-109, Theorem 3.3 and Corollary 3.4, DOI 10.1006/jabr.1999.8089, https://arxiv.org/pdf/math/9511209; N. G. de Bruijn, On the factorization of cyclic groups, Indagationes Mathematicae 15 (1953), 370-377. The argument here fixes its exact binary/original-phase scope.

## 3. Coverage derives the row geometry at every endpoint

Write d=kq with k in {2,3,4}. Fix any supported entry (r,c), with r=(a,b). There are exactly q+4 rows agreeing with r in at least one CRT coordinate: q rows with first coordinate a and four additional rows with second coordinate b. This count includes r.

Column c has kq supporting rows, and

    kq >= 2q > q+4,

because q>5. Hence another supporting row s differs from r in both coordinates. Its intersection with r contains c and has zero primitive character sum. By Section 2, the full q-line or five-fiber through c lies inside this intersection, and therefore inside the support S_r.

Applying this separately to every c in S_r proves, without presupposing support geometry,

    S_r = (A_r x Z/q) union (Z/5 x B_r),

where A_r and B_r are the complete sets of full lines and full fibers of that row. They are maximal sets of cycles. Put ell_r=|A_r| and f_r=|B_r|. Then

    kq = ell_r q + (5-ell_r) f_r,      0 <= ell_r <= k < 5.     (3.1)

The pure-line branch f_r=0 is explicitly permitted. Unlike an interior proof, no nonempty-fiber or singleton-fiber argument is used here.

## 4. Endpoint arithmetic eliminates every mixed row

Because d<5q, the support is not full, so f_r<q. Rearranging (3.1),

    (k-ell_r)q = (5-ell_r) f_r.

The integer 5-ell_r lies between 1 and 5, while q is prime and greater than 5. It is therefore coprime to q. It follows that q divides f_r. Since 0<=f_r<q, necessarily

    f_r=0,    ell_r=k.

Thus every row support consists of exactly k complete q-lines:

    S_(a,b) = A_(a,b) x Z/q,    |A_(a,b)|=k.                   (4.1)

All A_(a,b) remain arbitrary and may depend on both row coordinates. No common line set within a group, common fiber assignment, special permutation, or full-square-block structure is assumed or concluded.

## 5. The five rows at one second coordinate contradict prime-5 balance

Fix any b in Z/q and take two distinct rows (a,b) and (a',b). Their difference character has order 5. In (4.1), write

    C = A_(a,b) intersect A_(a',b).

Their exact row Gram entry is

    q sum_(u in C) alpha^((a-a')u).

Since a!=a', alpha^(a-a') is primitive of order 5. A binary subset sum of the fifth roots vanishes only for the empty set or all five roots, by the minimal polynomial 1+x+x^2+x^3+x^4. But |C|<=k<5, so row orthogonality forces C to be empty.

Therefore the five k-element sets A_(a,b), as a ranges over Z/5, must be pairwise disjoint subsets of a five-element set. Their disjoint union would have size 5k>5, impossible for k=2,3,4. This proves all three endpoint exclusions.

The final obstruction is order 5 rather than a primitive cross-group overlap. In particular it survives arbitrary row-dependent line choices and does not require any permutation alignment.

## 6. Fresh exact controls and limits

Run `python verify_endpoints.py`. It is self-authored for this packet, uses only the Python standard library, and neither imports nor executes a historical checker. Root sums are computed at original integer indices by exact integer polynomial reduction modulo Phi_(5q)(x), independently of the rational CRT-basis presentation used in the proof. The polynomial is obtained by exact division Phi_q(x^5)/Phi_q(x). No floating tolerance is used.

Controls include:

- The literal original-phase CRT identity and the exact cyclotomic polynomial identity.
- Every integer row degree solution at the three endpoints for all primes 7<=q<=1000, allowing f=0 throughout.
- Every canonical union-of-cycles row support at q=7,11, verifying maximal full lines/fibers and the degree equation. At each q the endpoint supports are precisely 10 two-line sets, 10 three-line sets, and 5 four-line sets, with no full fibers.
- All arbitrary five-row choices of k-element line sets at q=7,11, without row-group uniformity or permutation restrictions. Each has an exact nonzero order-5 row overlap. This is a complete finite test of the reduced five-row obstruction, not an arbitrary-square-mask census.
- Both complete original-index Grams and both degree counts for positive divisor masks at degrees 1,5,q,5q and q=7,11,13.
- Both complete Grams for deliberately invalid regular endpoint masks at d=2q,3q,4q. One family uses A_(a,b)={a,...,a+k-1} modulo 5. A second family uses A_(a,b)={a+b^2+b,...,a+b^2+b+k-1} modulo 5, genuinely varying with b within each first-coordinate group. These are regular in rows and columns but fail both full Grams. Their distinct-b row overlaps vanish exactly; the same-b obstruction is retained. Literal q=7 masks and original-index nonzero witnesses are included.
- Frozen source hashes and a sealed manifest.

RESULTS.json and RUN.stdout record the completed counts; RUN.stderr records any failure. Finite controls supplement the symbolic all-prime proof. They do not replace it with numerical evidence or an unsupported exhaustive-mask claim.

## 7. Administrative and inheritance boundary

The theorem is only the three endpoint exclusions above. Accepted first/middle/upper open-interval theorems, other orders, divisor constructions, and previous gap results remain unchanged. This packet does not compose inherited gap formulas, infer a full classification, claim a sharp defect optimum, or make historical novelty claims.

Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No external repository/catalogue write, owner closure, score change, or independent self-acceptance is performed.
