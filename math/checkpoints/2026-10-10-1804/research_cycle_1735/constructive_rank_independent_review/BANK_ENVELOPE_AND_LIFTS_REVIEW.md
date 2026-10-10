# Independent review: whole-left recurrence envelope and exact bank lifts

Review date: 10 October 2026. Verdict: PASS for the analytical rank envelope, the guarded representation theorem, and the three finite-order characteristic-zero lifts below. This review is independent of the aggregate-chain result in the same review folder. No accepted predecessor is changed.

## 1. Accepted conclusions and limits

For odd N, primitive q of order N, m≥(N−1)/2 and d=N−m≥4, let A_(N,m) be the whole-left recurrence matrix defined below. Over K=Q(q),

rank A_(N,m)≤min((d−1)(d−2)/2,4d−11).

A monic degree-m kernel polynomial with nonzero constant, nonzero resultant with its derivative, and a full-rank axis matrix yields at most 2m+2 accepted signed banks over its splitting field. The three explicitly defined polynomials in the reviewed certificates satisfy every guard and therefore establish

M_C(13)≤18, M_C(17)≤24, M_C(35)≤54.

All nodes are actual individual roots, counted separately in each same-sign orientation. These are splitting-field bounds. None is asserted to be attainable with all nodes and raw weights in K. Their splitting-field degrees are at most 8!, 11!, and 26!, respectively; smaller degrees are not established here.

Choosing d=floor((N+11)/5) gives a nonzero homogeneous kernel, but this alone does not establish a monic vector, a squarefree/nonzero-root polynomial, or the axis condition. Consequently a uniform approximately 8N/5 bank theorem remains unproved. The finite examples and the rank envelope are not a substitute for those missing guards.

## 2. Whole-left matrix and independent rank argument

Write h=4^−1 modulo N, e=2^−1 modulo N, and f(a,b)=q^(h(a+b)²). For the usual orientation Gaussian factors G, define

T_b=1/G_-+(N−b,b),
v_b(j)=[f(j,b)−T_b G_-+(j,b)]/G_++(j,b), 1≤j≤N−b−1.

The denominators are nonzero because each product uses only nonzero factors 1−q^u with 1≤u≤N−1. The row indexed by positive a,b with a+b≤d−1 is

(v_b(a),v_b(a+1),…,v_b(a+m)).

These are every length-(m+1) window from each whole-left sequence. There are (d−1)(d−2)/2 rows. The condition d≤(N+1)/2 ensures all physical b used are in the positive half.

Multiply column k, 0≤k≤m, by D(q^k), where

D(z)=∏_(j=2)^(d−1)(1−q^j z).

Every such factor is nonzero, since 2≤j+k≤N−1. This column scaling preserves rank.

Fix a row and put t=a+b. Write P(z)=∏_(j=1)^b(1−q^(a+j)z), F(z)=D(z)/P(z), R_0(z)=∏_(j=1)^b(1−q^(a−j)z), Q_b=∏_(j=1)^b(1−q^j), and B_b=T_b(−1)^bq^(b(b+1)/2). The product formulas for the two Gaussian binomials give exactly

D(q^k)v_b(a+k)
 =Q_b q^(ht²)q^(hk²)q^(etk)F(q^k)−B_bR_0(q^k)F(q^k).

The formula also covers a+k≤b, where the −+ Gaussian factor has no support: its numerator contains 1−q^0 and is zero. Thus no illegal support extension was introduced by the product formula.

Let C_k=q^(hk²), ρ=q^e. If t=2u, q^(etk)=(q^k)^u; if t=2u+1, it is ρ^k(q^k)^u. Every scaled row is the evaluation of a formal triple (E,O,R):

C_k E(q^k)+C_kρ^k O(q^k)+R(q^k).

E is divisible by z, has degree at most d−3+floor((d−1)/2), and has the additional factor 1−q^(d−1)z if d is even. O is divisible by z, has degree at most d−3+floor((d−2)/2), and has that additional factor if d is odd. The extra factor follows because the maximum t of the relevant parity is less than d−1, leaving the last factor of D uncanceled. R has degree at most d−2.

The formal direct-sum space of these triples has dimension 4d−10. This is a polynomial-space count, before evaluation; no assumption of linearly independent evaluated chirp functions is required.

There is one further relation. Set k_*=m+1=N−d+1, z_*=q^(−(d−1)). For t<d−1, F(z_*)=0 and all three row components vanish there. For t=d−1, the uncanceled numerator at physical coordinate a+k_*=N−b is

Q_b[f(N−b,b)−T_bG_-+(N−b,b)]=Q_b(1−1)=0.

Consequently every row triple satisfies

C_(k_*)E(z_*)+C_(k_*)ρ^(k_*)O(z_*)+R(z_*)=0.

This evaluates a polynomial numerator after clearing/canceling factors, not a quotient at a vanishing Gaussian denominator. The displayed functional is nonzero on the formal triple space: applied to (0,0,1), it equals 1. Its kernel has dimension 4d−11. Evaluation on the actual columns cannot increase that dimension, proving the asserted rank envelope, including for composite odd N.

## 3. Why the guarded kernel gives all physical rows

Let g(x)=Σ_(j=0)^m c_jx^j be monic, satisfy A c=0, have c_0≠0 and Res(g,g')≠0, and let its m roots x_i be distinct and nonzero in a splitting field L/K.

For positive b, fix the −+ singleton's amplitude at T_b and the +− singleton's amplitude at zero. The ++ group must realize v_b(a) throughout 1≤a≤N−b−1. If the sequence has at least m entries, solve its first m moments at exponents 1,…,m. The distinct, nonzero nodes make this Vandermonde matrix invertible. All remaining moments follow from the monic recurrence A c=0. If there are fewer than m entries, use a square truncated consecutive-power Vandermonde system and set the unused node amplitudes to zero.

The right interval a=N−b+1,…,N−1, together with a=0, requires b moments in the −− group, at exponents 0,…,b−1. There are enough nodes because b≤(N−1)/2≤m. These −− amplitudes do not change the already matched left interval or the exclusive coordinate a=N−b. The latter was exactly what forced T_b. Thus every positive physical row is matched, including its multiple small-a boundary entries. Using central intervals alone would not justify this step; the whole-left recurrence condition is important.

Reflect (a,b) to (−a,−b), exchanging ++ with −− and −+ with +−. Since the two same-sign groups use the same nodes and f is invariant, this assigns every negative physical row to existing banks. The physical-row-to-sector map is bijective in each orientation, so no sector receives conflicting assignments.

For b=0, let p_a be the coefficient vector of x^a modulo the monic polynomial g. The axis matrix has row (p_a,1,p_[-a]_N). Its full row rank is the final guard. A nonzero N-column minor supplies an exact axis solve. Initial moments convert into root amplitudes by the distinct-root Vandermonde matrix.

Finally, β=1 and every α is nonzero, so Δ=1−α^N−1=−α^N≠0. The accepted raw-weight inverse transform and geometric resolvent identity recover each legal bank from its sector amplitudes. These are literal banks, not trace/grouped operations. There are 2m+2 banks and N(2m+2) raw branch weights. Nothing in this argument grants an arithmetic-complexity or FFT-speedup claim.

## 4. Why the finite certificates prove characteristic-zero existence

An arbitrary solution modulo a prime would not suffice. The reviewed certificates instead define a polynomial over K by a selected square linear system: selected nonleading coefficient columns are solved, all remaining nonleading coefficients are fixed to the stated rational integers, and c_m=1.

In each example the selected defining minor is nonzero modulo the indicated prime of the cyclotomic ring. Therefore it is a unit in the corresponding localization, and the exact coefficients exist there and reduce to the recorded modular coefficients. The analytical rank envelope (or simply the total row count in the first two examples), combined with the same nonzero modular minor, proves the complete characteristic-zero recurrence rank equals the selected rank. Every omitted row is then a K-linear combination of the selected rows, so all recurrence equations hold exactly.

The constant coefficient, derivative resultant, and chosen axis minor also reduce to nonzero residues. Since the exact coefficients lie in the local ring and the quotient polynomial is monic, these guards are well-defined there. Nonzero reduction proves each is nonzero over K. The resulting exact polynomial is therefore monic, squarefree, has no zero roots, and has full axis rank. This proves the guarded construction in characteristic zero without assuming a lifting theorem for arbitrary finite-field solutions or complete splitting over K.

At N=13 and N=17 the selected rows exhaust the whole-left recurrence system. At N=35 there are 28 rows, and the nonzero 25-minor together with the 4d−11=25 analytical bound is essential. A finite-field rank of 25 alone would not justify dropping the other three rows.

## 5. Fresh certificate verification

fresh_bank_lift_check.py was written for this review. It imports only standard libraries and SymPy and reads author JSON as inert data. It imports or executes no author/predecessor research code.

For each example it independently:

- Verifies the reduction prime and exact multiplicative order of q.
- Constructs Gaussian binomials by Pascal recurrence and every whole-left moment from the Fourier target.
- Reconstructs every recurrence row and label, the selected equation/coefficient submatrix, and its determinant.
- Solves the defining system using the certificate's fixed integer coefficients, checking every recurrence.
- Computes the derivative resultant independently with SymPy polynomial arithmetic.
- Constructs the monic quotient powers by repeated multiplication by x, verifies the selected axis minor, and checks every supplied physical-row solution against newly constructed orientation matrices.
- Constructs the polynomial row triples independently, checks their stated degree/divisibility restrictions, every scaled row evaluation, and the omitted-endpoint relation.

The reproduced guard tuples (defining minor, constant, resultant, axis minor) are:

N=13, m=8, modulo 53, q=16: (13,14,32,49), rank 6 of 6 rows, 18 banks.
N=17, m=11, modulo 103, q=72: (35,9,7,3), rank 10 of 10 rows, 24 banks.
N=35, m=26, modulo 71, q=49: (29,37,39,69), rank 25 of 28 rows, 54 banks.

Every required denominator is nonzero. The controls check 65 physical rows and 1,683 coefficient entries, besides every recurrence/envelope evaluation. FRESH_BANK_LIFT_RESULTS.json records the results. The all-order envelope and exact-definition local-ring argument above, rather than the finite tests alone, establish the characteristic-zero claims.

## 6. Separate order-eleven obstruction

BANK_QUINTIC_INDEPENDENT_REVIEW.md supplies a separate independent proof of the N=11 restricted obstruction. A fresh six-by-six central Hankel matrix has determinant 4 modulo 23 at q=2, with all denominators units. Hence no ≤5-node ++ group is possible when the −+ group is one effective α=1 singleton, irrespective of the −− count. Reflection yields the corresponding −− bound when the +− singleton is also at α=1.

Thus fourteen banks are necessary in that fixed-cross-singleton architecture, and the earlier accepted fourteen-bank splitting-field construction attains the restricted count. This does not establish an unrestricted fourteen-bank minimum or K-only attainment. The envelope/lift theorem and this obstruction are logically separate conclusions and should be reported separately.

## 7. Classification

The annihilator, recurrence, Vandermonde and local-ring nonvanishing ingredients are standard. The derived 4d−11 envelope addresses the specific Fourier whole-left sequences and their coupled signed-bank realization. This review establishes correctness and scope, not historical priority. The concrete finite-order bounds may be used with their splitting-field qualification; the approximately 8N/5 suggestion must remain an unresolved guarded direction.


## 8. Frozen source bindings

The verdict applies to the exact source bytes listed in BANK_ENVELOPE_REVIEW_RECEIPT.json. Copies are preserved in input_snapshot/bank_envelope. The uniform square-root-saving addendum is excluded from this receipt and reviewed separately.
