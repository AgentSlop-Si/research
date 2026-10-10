# A base-field Fourier upper bound of 2N−4 signed banks

10 October 2026. New author theorem, submitted for independent review. All predecessor packets are frozen and unchanged. This note constructs a new base-field representation; it does not purport to descend the individual banks of either frozen splitting-field witness.

## 1. Statement and unresolved smaller counts

Let N≥7 be odd, q a primitive Nth root of unity, K=Q(q), and F_N[k,t]=q^(−kt). Use exactly the accepted signed bank grammar

B_(ε,δ)(α,β;w) = (1/N) Σ_(j=0)^(N−1) w_j (I−αS^ε−βq^(εδj)T^δ)^−1,

where S e_i=e_(i+1), T e_i=q^i e_i, ε,δ∈{1,−1}, and 1−α^N−β^N≠0. No new operations are admitted.

THEOREM. F_N is a sum of at most 2N−4 permitted banks with every node, parameter and raw phase weight in K. All β values equal 1; both cross-sign singleton nodes equal 1; the same N−3 distinct nonzero K-nodes are used for ++ and −−. Thus the orientation multiplicities are (N−3,1,1,N−3).

In particular M_K(F_7)≤10 and M_K(F_11)≤18, improving the preceding K-only bounds 12 and 20. The accepted order-seven lower bound gives 8≤M_K(F_7)≤10. This result does not decide whether eight banks at N=7 or fourteen banks at N=11 are attainable over K. It does not improve the accepted complex-field bounds eight and fourteen at those orders. It is an all-odd-order Fourier-specific bound over the base field; its leading asymptotic coefficient remains 2.

The proof is constructive through a finite grid of explicitly bounded size. It does not infer complete splitting from a nonempty open set of coefficient parameters. Instead, complete splitting is built into rational root coordinates before openness is used.

## 2. Coefficients and edge moments

For (a,b) modulo N, let r=[εa]_N and ℓ=[δb]_N, and define

G_(ε,δ)(a,b) = [r+ℓ choose ℓ]_(q^(εδ)) when r+ℓ≤N−1, and 0 otherwise.

Every displayed nonzero G is nonzero in K, since its Gaussian product uses only factors 1−q^j with 1≤j≤N−1. Put

C=(1/N)Σ_t q^(−t²),   f(a,b)=q^(h(a+b)²),   4h≡1 modulo N.

The ordinary odd-order quadratic Gauss-sum identity gives C≠0. The accepted Weyl expansion of F_N has coefficient C f(a,b) at S^aT^b. A β=1 bank with normalized sector amplitudes h_ℓ contributes C h_ℓ α^r G_(ε,δ)(a,b). Arbitrary h_ℓ are recovered from raw weights by the formula in Section 6.

Write d=N−3, m=N−4=d−1, and H=q/(1+q). Define the d+1 edge moments s_0,…,s_d by

s_0=1,
s_(a−1) = (f(a,1)/H − G_-+(a,1))/G_++(a,1),   2≤a≤N−2.

All denominators are nonzero. One particularly useful identity, valid for every odd N≥7, is

s_2=q.

Indeed, at a=3 one has f(3,1)=q^4, G_-+(3,1)=−q(1+q), and G_++(3,1)=(1+q)(1+q²). Substitution gives s_2=q. No numerical embedding or primality of N is used.

Let L:K[t]_(≤d)→K be the K-linear functional L(t^j)=s_j.

## 3. Rationally enforced split annihilators

Take independent root coordinates Y=(y_1,…,y_m). Define

p_Y(t)=∏_(i=1)^m(t−y_i),
D(Y)=L(p_Y),   U(Y)=L(t p_Y),   x(Y)=U(Y)/D(Y).

Whenever D≠0, the polynomial

g_Y(t)=(t−x(Y))p_Y(t)

is monic of degree d, splits over K at every K-valued parameter point, and satisfies the single required recurrence L(g_Y)=0. The remaining requirements are that all d roots be distinct/nonzero and that the axis system have full rank. We verify a single explicit nonzero polynomial whose nonvanishing guarantees all of these.

For a=0,…,N−1 form an N×N matrix A(Y) with columns, in this order:

- y_i^a, for i=1,…,m;
- the constant column 1;
- y_i^[−a]_N, for i=1,2,3.

Let A_0(Y)=det A(Y). Its entries are ordinary polynomials, including at a=0 where the exponent is 0. At y_i=q^i, the columns are the N distinct Fourier characters with frequency exponents

1,…,N−4, 0, N−1,N−2,N−3.

Thus A_0 is not identically zero. This determinant uses only the first m nodes and the singleton, not the rationally solved last node x.

Define

Γ(Y)=A_0(Y) D(Y) U(Y) (∏_i y_i) (∏_(i<j)(y_i−y_j)) (∏_i(U(Y)−y_iD(Y))).

Every factor is a nonzero polynomial:

1. D has coefficient (−1)^m s_0=(−1)^m at y_1⋯y_m.
2. U has coefficient (−1)^(m−1)s_2=(−1)^(m−1)q at each squarefree monomial of degree m−1. Such a monomial corresponds to the coefficient of t in p_Y.
3. For fixed i, the coefficient of ∏_(j≠i)y_j in U−y_iD is (−1)^(m−1)(s_2−2y_i s_1+y_i²s_0), a nonzero polynomial in y_i because s_0=1.
4. A_0 is nonzero by the Fourier specialization; the elementary coordinate and difference factors are nonzero.

Since K[Y] is a domain, Γ is nonzero. Its nonvanishing gives D≠0, x≠0, y_i≠0, pairwise distinct y_i, x≠y_i, and A_0≠0 simultaneously. Consequently the same root set X={y_1,…,y_m,x} consists of d distinct nonzero elements of K and supplies a full-rank b=0 system.

### Explicit finite construction

The degree of Γ in any one y_i is at most 4N−7. The axis determinant contributes at most 2N−2, because any variable occurs in at most two columns. D and U contribute 1 each, ∏y_i contributes 1, the pairwise differences contribute m−1, and ∏(U−y_jD) contributes at most m+1. The sum is 4N−7.

A nonzero polynomial of individual degree at most B−1 cannot vanish on all of a Cartesian product of B distinct field elements, by repeated univariate interpolation. Therefore some tuple

Y∈{1,2,…,4N−6}^m

has Γ(Y)≠0. Enumerate this finite grid and take its first such point. All evaluations and tests are exact in K. This gives a bounded deterministic recipe with at most (4N−6)^(N−4) candidates; it is an existence/construction bound, not an efficient algorithm claim. In this grid version, m of the d distinct nodes are positive rational integers and only the last is generally nonrational in K.

This is the sole openness argument. It occurs in already-split root coordinates and is supported by explicit polynomial factors and a finite grid. It makes no assertion that complete splitting is a Zariski-open condition in the accepted N11 sextic coefficient plane.

## 4. Assign every physical row

Use ++ and −− banks at every x_i∈X, and the −+ and +− singleton banks at 1. For each physical b, every bank uses sector ℓ=[δb]_N. These sectors are independent as b varies.

For d distinct nonzero nodes, the Vandermonde matrices with consecutive exponents 0,…,d−1 or 1,…,d are invertible. To assign fewer moments, use the first required number of nodes and give the others zero amplitude.

### Axis b=0

Use only the N columns selected in A(Y): ++ at y_1,…,y_m, the −+ singleton, and −− at y_1,y_2,y_3. Solve A(Y) against (f(a,0))_(a=0)^(N−1) and set all omitted sector amplitudes to zero. Since A_0≠0, this matches the complete row in K.

### Edge b=1

Assign the −+ singleton amplitude H. Choose ++ amplitudes A_i so that

Σ_i A_i x_i^a = H s_(a−1),   1≤a≤d.

The moment equation L(g)=0 forces the same identity at a=d+1=N−2: every root power sequence obeys g, and the leading coefficient is 1. At a=1 the ++ contribution is (1+q)H=q=f(1,1). At a=N−1 the −+ singleton gives G_-+(N−1,1)H=1=f(N−1,1). At every 2≤a≤N−2 the definition of s gives the target.

Set every −− amplitude to zero. The +− singleton at this physical row has ℓ=N−1, so it affects only a=0. Assign it f(0,1)−H−Σ_i A_i. This completes the row.

### Interior positive rows 2≤b≤(N−1)/2

The coordinate a_*=N−b belongs exclusively to the −+ orientation. Give that singleton amplitude

T_b=f(N−b,b)/G_-+(N−b,b),

and give the +− singleton amplitude zero. There are N−b−1≤N−3=d nonaxis coordinates in the left interval 1≤a≤N−b−1. Choose ++ amplitudes A_i with

Σ_i A_i x_i^a = (f(a,b)−T_b G_-+(a,b))/G_++(a,b)

at these consecutive exponents, using the first N−b−1 nodes and setting the rest to zero.

Choose −− amplitudes B_i with the b moments

Σ_i B_i = f(0,b)−T_b−Σ_i A_i,
Σ_i B_i x_i^r = (f(N−r,b)−T_b G_-+(N−r,b))/G_--(N−r,b),   1≤r≤b−1.

This is possible since b≤d. These −− sectors affect only a=0 and the right interval N−b+1≤a≤N−1. Thus they do not disturb the left interval or a_*. The scalar Gaussian factors in all formulas are nonzero on their indicated support. The axis, left interval, exclusive coordinate, and right interval account for all N entries, proving exact compatibility.

### Remaining rows

For b=1,…,(N−1)/2 reflect the assigned row simultaneously by (a,b)↦(−a,−b) and swap ++↔−− and −+↔+−. This preserves f(a,b), εδ and the local coordinates r,ℓ. The two same-sign groups have identical node sets, so the reflection assigns amplitudes in existing banks and matches row N−b. Reflection is only a proof and coefficient-assignment device; it is not an extra operation in the representation grammar.

Every coefficient row has now been matched using K-valued amplitudes.

## 5. Explicit small-order nodes

The simpler specialization y_i=q^i also works for N=7 and N=11. The exact final roots obtained from U/D are:

N=7:
X={q,q²,q³,(3−q−q²+q⁵)/2}.

N=11:
X={q,q²,…,q⁷,
(19+41q+81q²+68q³+13q⁴−18q⁵+3q⁶+60q⁷+80q⁸+39q⁹)/23}.

Fresh exact field arithmetic verifies D≠0, distinct/nonzero nodes, the single edge recurrence, all row equations, the complete raw-weight transform, and the literal Fourier Weyl traces. The full control additionally checks both inverse products for every original resolvent branch and all original matrix entries. Output status is recorded separately in the control receipts; no uncompleted control is presumed passed by this note.

## 6. Original legal weights and counted cost

For bank n, let its normalized amplitudes be h_(n,ℓ), α_n∈X or 1, and Δ_n=−α_n^N. For every j put

w_(n,j)=C Δ_n Σ_(ℓ=0)^(N−1) h_(n,ℓ) q^(−ε_nδ_njℓ).

All terms belong to K. Orthogonality gives (1/N)Σ_j w_(n,j)q^(ε_nδ_njℓ)=CΔ_nh_(n,ℓ), with exactly the accepted normalization. Since α_n≠0, every Δ_n≠0. For X_j=α_nS^ε+q^(εδj)T^δ,

X_j^N=(α_n^N+1)I,
(I−X_j)^−1=(I+X_j+⋯+X_j^(N−1))/Δ_n.

Both inverse identities follow by telescoping. Substitution of the raw weights yields exactly the coefficients matched above, hence equality in all original matrix entries.

There are 2N−4 whole banks and N(2N−4) declared raw branch weights. Zero banks could be omitted. Nothing is counted as one bank merely because it is a trace or a Galois orbit. No claim about minimum count, arithmetic complexity, stability, field-operation cost, or FFT speedup follows. The bounded grid is intentionally conservative and exponentially large.

## 7. Field-descent boundary and prior art

The classical finite-node criterion over K requires a squarefree annihilator that splits completely over K, not merely a squarefree polynomial in K[t]. Once nodes are in K, Vandermonde recovery places the weights in K. Without splitting, the same method supplies banks only over a splitting field.

A Galois-invariant sum over extension-field banks may have matrix entries in K while its individual nodes do not. Averaging all conjugates either retains extension-field nodes and counts the resulting bank occurrences, or writes grouped trace operations that are not permitted banks. It does not yield a count-preserving K-bank decomposition. The present theorem avoids that operation entirely by reconstructing the target with a larger split node set.

The accepted two-parameter N11 family gives fourteen banks over K conditionally on an admissible sextic splitting into six distinct K-roots. The nonzero exceptional polynomial in that family certifies legal distinct roots and solvable rows over a splitting field; it does not certify that arithmetic splitting condition. The new theorem neither proves nor disproves the existence of such a family point.

Primary-source comparison: Tokcan, “On the Waring Rank of Binary Forms,” Theorem 1.1, states the classical field-sensitive Sylvester/Hankel criterion using distinct linear factors over the field; Theorem 3.2 distinguishes minimal decompositions and splitting fields. Potts and Tasche, “Parameter estimation for exponential sums by approximate Prony method,” Section 2, treats annihilating polynomials and Vandermonde recovery. These support the classical ingredients, not the exact signed-bank theorem proved here. The rooted one-recurrence construction and all four coupled orientation rows are proved directly above. A bounded source check is not a worldwide novelty claim.

Sources:
- https://arxiv.org/pdf/1610.09065
- https://www-user.tu-chemnitz.de/~potts/paper/prony.pdf
- https://www.jmilne.org/math/CourseNotes/FT.pdf

Internal mathematical predecessors read as inert text/data: the accepted small-order synthesis editorial_v2, accepted N11 construction and parametric addendum, independent N11 review, and universal fixed-bank architecture note. No predecessor research program was run, imported or changed.
