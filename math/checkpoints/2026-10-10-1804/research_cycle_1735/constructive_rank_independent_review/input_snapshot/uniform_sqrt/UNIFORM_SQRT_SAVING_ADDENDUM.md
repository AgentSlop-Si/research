# A uniform square-root saving in the signed-bank count

10 October 2026. Separate new author addendum, pending independent review. The frozen rank-envelope note and three small-order certificates remain unchanged.

## 1. Statement

Let N≥1297 be odd, q a primitive Nth root, K=Q(q), and set

d=floor((sqrt(N)+16)/13), m=N−d.

Then the negative Fourier matrix F_N has a representation by at most

2m+2 = 2N−2 floor((sqrt(N)+16)/13)+2

permitted signed banks over a finite algebraic extension of K. The orientation multiplicities are (m,1,1,m), both cross-sign singleton nodes are 1, both same-sign groups use the same m distinct nonzero roots of one monic polynomial g in K[t], and every beta is 1. The extension degree is at most m!.

Thus the count is 2N−(2/13)sqrt(N)+O(1). This is an actual uniform saving larger than a constant, but its leading linear coefficient remains 2. It is not an N+O(1) or an 8N/5 theorem. It is not a K-only bank theorem, a minimum count, or a scalar FFT complexity claim. Small N retain all previously accepted bounds and the separately certified examples in the companion note.

The proof uses the whole-left recurrence system and explicit row construction already established in WHOLE_LEFT_RANK_ENVELOPE.md. The new work is to establish the monic, squarefree, nonzero-node and axis guards uniformly. All inequalities below are deliberately conservative.

## 2. The envelope and the numerical inequalities

Let A=A_(N,m), W=ker_K A, and D(z)=∏_(j=2)^(d−1)(1−q^j z). Multiplying column k by D(q^k), for k=0,…,m, gives the scaled row space. Every scaled row, and every linear combination of such rows, extends to an N-periodic sequence

B(k)=C_k E(q^k)+C_k rho^k O(q^k)+R(q^k),
C_k=q^(h k²), rho=q^e, h=4^(-1), e=2^(-1) modulo N,

where

deg E≤E_max=d−3+floor((d−1)/2),
deg O≤O_max=d−3+floor((d−2)/2),
deg R≤d−2.

For the estimates in this addendum the envelope's extra divisibility factors and endpoint relation can be discarded. They remain available for the sharper rank bound rank A≤4d−11, hence

w=dim W≥m+1−(4d−11)=N−5d+12.

The chosen d satisfies d≥4 and 13d−17<sqrt(N). This implies the auxiliary inequalities used below: N≥7d, m+1≥3(d−1), m≥4(d−1), and w≥(N+1)/2. Each follows already from N>(13d−17)^2 and d≥4.

## 3. Three explicit orthonormal bases

Choose any complex embedding of K. The following three systems are orthonormal bases of C^N:

- the coordinate vectors e_k;
- the normalized Fourier vectors F_j(k)=q^(jk)/sqrt(N);
- the normalized chirp-Fourier vectors H_j(k)=C_k q^(jk)/sqrt(N).

Every inner product between vectors from distinct bases has magnitude 1/sqrt(N). The statements involving coordinates are immediate. For the other pair, complete the square in the quadratic Gauss sum, or compute its squared absolute value directly: since N is odd and h is a unit modulo N, orthogonality in the difference variable gives |Σ_k q^(h k²+a k)|²=N. This holds for composite odd N too.

Consequently any selection of s distinct vectors from these three bases is linearly independent whenever s−1<sqrt(N). Indeed its Gram matrix has diagonal 1, off-diagonal magnitudes at most 1/sqrt(N), and is strictly diagonally dominant. If fewer actual atoms occur, the same conclusion applies.

## 4. Coordinate vectors are absent from the recurrence row space

Suppose a coordinate functional delta_j, 0≤j≤m, belonged to row(A). After column scaling, its values on k=0,…,m would be D(q^j)delta_j(k), represented by an envelope sequence B(k).

In its full N-periodic extension, B is supported at no more than d coordinate positions: the one allowed position j, plus the N−m−1=d−1 unspecified positions. On the other hand its envelope expression uses at most

(E_max+1)+(O_max+1)+(d−1)=4d−7

Fourier/chirp-Fourier atoms. The chirp frequency ranges are 0,…,E_max and e,…,e+O_max, and are disjoint without wrapping under N≥7d. Hence a nonzero B would give a linear dependence among at most 5d−7 selected atoms from the three bases. But 5d−8<sqrt(N), contradicting Section 3.

Thus no delta_j belongs to row(A). In particular W is not contained in c_m=0 or c_0=0. It contains degree-m polynomials and polynomials with nonzero constant. This also excludes the derivative evaluation functional at x=0, which is delta_1.

## 5. No derivative evaluation functional is present

Fix any x∈C, x≠0. Suppose that the ordinary derivative evaluation vector

v_x=(k x^(k−1))_(k=0)^m

belongs to row(A). The corresponding scaled envelope sequence agrees on k=0,…,m with

B(k)=k x^(k−1)D(q^k).

Let E_2 denote the step-two shift on sequences. Define the constant-coefficient difference operator

L_x=∏_(j=0)^(d−2) (E_2−x²q^(2j))².

Its degree in E_2 is r=2(d−1). Since D(q^k) is a linear combination of q^(jk), j=0,…,d−2, this operator annihilates k x^(k−1)D(q^k). Therefore L_x B vanishes at k=0,…,m−2r.

The chirp identity C_(k+2)=q^(k+1)C_k shows that a factor E_2−lambda maps the envelope polynomials by

E(z) to q z E(q²z)−lambda E(z),
O(z) to q² z O(q²z)−lambda O(z),
R(z) to R(q²z)−lambda R(z).

After r factors, the degrees of the first two components increase by at most r; the ordinary degree stays at most d−2. If either original chirp polynomial was nonzero, its transformed polynomial is nonzero: at each step the new highest-degree term comes only from the first summand and has nonzero coefficient.

The transformed envelope uses at most 4d−7+2r frequency atoms. The two chirp ranges remain disjoint without wrapping, because E_max+r and O_max+r are less than the required half-circle gaps under N≥7d. Since L_x B vanishes on m−2r+1 consecutive positions, it uses at most d+2r−1 coordinate atoms. A nonzero transformed envelope would therefore give a dependence on at most

(4d−7+2r)+(d+2r−1)=5d−8+4r=13d−16

atoms. This is impossible because 13d−17<sqrt(N).

Thus L_x B is identically zero and all its frequency coefficients vanish. The highest-degree observation forces the original E and O to vanish. We are left with an ordinary polynomial sequence R(q^k) agreeing with k x^(k−1)D(q^k) on k=0,…,m.

That agreement cannot occur. Their difference satisfies a monic constant-coefficient recurrence of order at most 3(d−1): use the roots q^j with multiplicity one for R, and xq^j with multiplicity two for the second sequence, j=0,…,d−2. Coincidences only lower the order. Since m+1≥3(d−1), the initial zero block propagates to all nonnegative k. At k=0 it gives R(1)=0. At k=N it then gives

0=R(1)=N x^(N−1)D(1),

a contradiction, since x≠0, characteristic is zero, and D(1)≠0.

No derivative evaluation vector v_x belongs to row(A), for any finite x. Together with Section 4, this proves that the common divisor of all polynomials in W has no repeated root and is not divisible by t.

## 6. The kernel has a nonempty squarefree, degree-m open subset

Work first over C. Let H be the greatest common divisor of W. By Section 5 it is squarefree; by Section 4 H(0)≠0. Divide W by H. The resulting polynomial space has no common root.

Choose a degree-m polynomial in W, and then choose a second member whose quotient by H avoids the finitely many roots of the first quotient. Such a choice exists because there is no further common root. The two quotients are coprime. In their pencil, only finitely many parameter values give a multiple root: these are the critical values of their nonconstant rational ratio. Only finitely many further values cause a quotient root to coincide with a root of H, or kill the leading/constant coefficient.

Therefore W contains degree-m squarefree polynomials with nonzero constant. Equivalently the simultaneous conditions c_m≠0, c_0≠0 and discriminant≠0 form a nonempty Zariski-open subset of P(W). This is a characteristic-zero elementary pencil argument; no probabilistic genericity is being assumed.

## 7. The axis guard can be imposed simultaneously

Put r_0=(N−1)/2. We have w−1≥r_0. Consider ordered r_0-tuples of distinct nonzero potential roots Y=(y_1,…,y_(r_0)). On the nonempty open set U where the r_0 evaluation functionals on W are independent, the incidence set

I={(Y,[g]): Y∈U, [g]∈P(W), g(y_i)=0 for every i}

is a projective bundle over U with fibers of dimension w−r_0−1. Hence it is irreducible.

This incidence set contains a polynomial from the good open subset of Section 6. To see this without assuming general position, take one squarefree degree-m g∈W with nonzero constant. Evaluation of W at all m distinct roots of g has kernel exactly the one-dimensional span of g: a polynomial of degree at most m vanishing at all those roots is a scalar multiple of g. Its evaluation rank is w−1, so r_0 of those roots give independent evaluations and hence a point of I.

Now use only the ++ and -- columns at the r_0 designated nodes, together with the singleton constant column, in the physical axis. This is an N by N matrix with a-th row

(y_1^a,…,y_(r_0)^a, 1, y_1^[-a]_N,…,y_(r_0)^[-a]_N).

Its determinant is a nonzero polynomial in Y. At y_i=q^i, 1≤i≤r_0, its columns are exactly the N distinct Fourier characters, so its determinant is nonzero. Therefore its nonvanishing is a nonempty open condition on U and on I.

The good-polynomial condition and this axis condition are two nonempty open subsets of the irreducible incidence set I; they intersect. The resulting g has distinct nonzero roots, and the designated subset already supplies full axis rank. Consequently the full moment-coordinate axis matrix from the companion note also has rank N.

All equations and guards are defined over K. The existence over C shows that at least one relevant axis minor is a nonzero polynomial on the monic affine kernel over K. Since K is infinite, the intersection of the monic, constant, discriminant and axis open conditions has a K-valued point. Thus g may be chosen in K[t], even though its individual roots need not lie in K.

## 8. Finite constructive recipe and original banks

Compute A exactly over K and an affine parametrization of its monic kernel. Its nonemptiness follows from Section 4. Enumerate rational integer choices of its free parameters, retaining the first polynomial for which c_0≠0, the resultant is nonzero, and the axis matrix has full rank. The preceding proof guarantees termination.

A coarse bounded grid also suffices. For monic g, a remainder coefficient in t^a modulo g has total degree at most a−m+1≤d in the lower coefficients whenever a≥m, and degree zero for a<m. An N-column axis minor thus has degree at most Nd. Multiplying one nonzero such minor by c_0 and the discriminant gives degree at most Nd+2m−1. Consequently a Cartesian grid of Nd+2m distinct rational integers for every affine free coordinate contains a good point. Testing the matrix rank avoids needing to know in advance which minor is nonzero. This bound is exponentially large and is not an efficiency claim.

Take the m distinct roots in a splitting field and use the exact physical-row interpolation, simultaneous reflection, Lagrange moment recovery, raw phase-weight formula, and literal resolvent identity in Section 4 of the companion note. Every denominator has now been proved legal. All rows are covered and all banks are in the original grammar. This establishes the stated 2m+2 count.

## 9. Scope and checks still required

This author proof is separate from the already checked rank envelope and small-order certificates. Independent review should focus on the coherence atom counts, the derivative-evaluation exclusion, and the incidence argument making the axis guard simultaneous. No accepted result is overwritten or weakened.

The result improves the additive saving to order sqrt(N); it leaves the coefficient-2 asymptotic barrier unresolved. The stronger approximately 8N/5 suggestion from the rank envelope still lacks a corresponding uniform guard proof. No worldwide novelty claim is made. The Gauss-sum, strict-diagonal-dominance, annihilator, and elementary linear-system ingredients are classical; the conclusion here is their explicit application to the permitted Fourier bank grammar.
