# An explicit cutoff for the accepted positive-sign chirp obstruction

## Result and precise scope

Assume the two accepted, immutable source statements listed below. Define the explicit integer

\[
\boxed{N_0=2^{\,2^{534}}.}
\]

For every odd integer \(N=5m\) with \(\gcd(m,5)=1\), \(N\equiv1\pmod4\), and \(N\ge N_0\), and for every primitive complex \(N\)-th root used to define the forced chirp feedback matrix \(B_N\), that matrix has no representation as a sum of two weighted Hamiltonian-cycle Green resolvents with arbitrary diagonal endpoint masks and invertible Green denominators on the fixed coordinates.

This makes the previously accepted finite-exception conclusion effective. The cutoff is intentionally very large. No new finite-\(N\) enumeration, exceptional-list computation, expanded eliminant, or execution of historical constructor/checker code is used. The proof does not claim novelty, an asymptotic FFT lower bound, or an obstruction to general Fourier algorithms.

Here “positive-sign” means \(\epsilon_N=+1\) in \(G_N^2=\epsilon_N N\). Both possible real signs of \(G_N\) are included. The \(\epsilon_N=-1\) curve, unmatched row/column endpoint permutations, additional summands, products, and other feedback targets remain separate and unresolved by this argument. The already accepted \(N=5q^2\), \(q\equiv1\pmod{241}\) infinite family remains valid independently of this cutoff, including its members below \(N_0\).

## Accepted inputs

1. `8fcf5b11cd161e33b8fcab05acae7bf1f17d0f6775b9d2cca6c8f3807b1ea82f__REVIEW.md`, §§1–5, SHA-256 `8fcf5b11cd161e33b8fcab05acae7bf1f17d0f6775b9d2cca6c8f3807b1ea82f`: exact principal restriction, Gauss identity and scalar curve, projective generic exclusion, and the separate square-modulus exclusion.
2. `aa91fdec5f08cc03e33652869d41be9f9a53bf3c37838c2d5f8d58532dd54586__ACCEPTED_TWO_GREEN_EXCLUSION.md`, §§2–5, SHA-256 `aa91fdec5f08cc03e33652869d41be9f9a53bf3c37838c2d5f8d58532dd54586`: empty closed projective necessary system for the \(N=5\) target for all \(24^2=576\) Hamiltonian order pairs, including singular diagonal endpoint limits.

The new argument uses only their mathematical conclusions. Their finite computations are not rerun.

The one external effective theorem used is J. Kollár, “Sharp Effective Nullstellensatz,” *Journal of the American Mathematical Society* **1** (1988), 963–975, Theorem 1.5 and Corollary 1.9, printed page 965. The primary paper is available at [the UC Davis-hosted copy](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Kollar/kollarnullstellen.pdf). Its statement applies over any field, excludes generators of degree exactly two, and bounds the degree of each product in a unit-ideal certificate by a product of at most \(n\) input degrees. Consequently, for \(n=10\) and degrees at most 36, none equal to two, the bound \(36^{10}\) suffices. Only this degree conclusion is taken from the paper; all coefficient-height bounds below are proved directly.

## 1. The universal polynomial necessary system

Fix a primitive fifth root \(\eta\), put \(K=\mathbb Q(\eta)\) and \(\mathcal O=\mathbb Z[\eta]\), and let \(g\) be an indeterminate. Indices are in \(\{0,1,2,3,4\}\). Set

\[
H(g)=F-gC+g^3D,
\quad F_{ab}=\eta^{ab},\quad C_{ab}=\eta^{-3(a+b)^2},
\quad D_{ab}=\eta^{-3a^2}\delta_{ab}.
\]

Fix two Hamiltonian permutations \(\pi,\tau\). Give the five row directions coordinates \(u_i=[a_i:b_i]\) and the five column directions coordinates \(v_j=[c_j:d_j]\). Define matrices

\[
U_{i,i}=a_i,\quad U_{i,\pi(i)}=b_i,
\qquad V_{j,j}=c_j,\quad V_{\tau^{-1}(j),j}=d_j,
\]

with all other entries zero, and write \(T=UHV\). The relevant coordinates within each pair are distinct because a five-cycle has no fixed point.

Use the following finite list of polynomial equations:

* \(T_{ij}=0\) for every \(j\notin\{i,\pi(i),\tau(i)\}\).
* All 11-by-11 minors of the 25-by-11 matrix \(M\) whose row indexed by \((i,j)\) consists of the coefficients of the formal scale expression
  \[
  V_{ij}X_i+U_{ij}Y_j
  \]
  in the ten columns \(X_0,\ldots,X_4,Y_0,\ldots,Y_4\), followed by the final entry \(T_{ij}\).

The \(X_i,Y_j\) here are labels for coefficient columns, not additional variables of the polynomial system. There are exactly ten projective direction pairs.

Every off-support equation has total direction degree two and \(g\)-degree at most three. Every determinant uses its final column exactly once, so it is linear in \(H\) and has \(g\)-degree at most three.

For completeness, let the row pairs scale by \(\lambda_i\), the column pairs by \(\mu_j\), and let a minor select equation rows \(E\). If \(n_i\) of those rows have first index \(i\), and \(m_j\) have second index \(j\), its scaling weight is

\[
\prod_i\lambda_i^{n_i-1}\prod_j\mu_j^{m_j-1}.
\]

If any \(n_i=0\), its entire \(X_i\) column is zero; if any \(m_j=0\), its entire \(Y_j\) column is zero. Thus every nonzero determinant has nonnegative multidegrees, row-direction total degree \(11-5=6\), column-direction total degree six, and total direction degree twelve. These equations define a closed subscheme \(\mathcal S\) of

\[
\mathbb A^1_K\times(\mathbb P^1_K)^{10}.
\]

The accepted necessary-system theorem applies to these equations with any target in the final column. In particular, it applies to \(H(g)\).

## 2. Why the generic fiber is empty

In \(K\), put \(g_0=1+2(\eta^2+\eta^3)\). The accepted calculation gives \(g_0^2=5\) and

\[
H(g_0)=(1+5g_0)B_5.
\]

The factor \(1+5g_0\) is nonzero: its vanishing would give \(g_0=-1/5\), inconsistent with \(g_0^2=5\). Multiplying the target by a nonzero scalar multiplies each off-support equation and each maximal augmented minor by that scalar. Therefore the accepted empty \(B_5\) system implies \(\mathcal S_{g_0}\) is empty.

Projection from \(\mathbb A^1_K\times(\mathbb P^1_K)^{10}\) to \(\mathbb A^1_K\) is projective, hence proper; a closed subscheme remains proper over the base. A nonempty geometric generic fiber would place the generic point in its closed image and hence force its image to be the entire integral affine line. That would contradict the empty \(g_0\) fiber. Thus the generic fiber is empty over an algebraic closure of \(K(g)\).

This reasoning is applied separately to each of the 576 order pairs. No assertion about a negative-sign curve is needed. The accepted properness fact is also stated in [Stacks Project, Tag 01WC](https://stacks.math.columbia.edu/tag/01WC).

## 3. Complete affine charts and degree-two avoidance

Cover each \(\mathbb P^1\) by its two standard charts. On a chart, select one nonzero coordinate in each of the ten pairs and divide the pair by that coordinate, setting it to one. The other coordinate is an unrestricted affine variable. Hence the \(2^{10}=1,024\) choices cover every geometric projective point, including every point with any chosen “base” coordinates zero. Each chart has exactly ten affine variables, denoted \(z_1,\ldots,z_{10}\).

Dehomogenize the preceding equations on a fixed chart. Their coefficients belong to \(\mathcal O[g]\), their affine \(z\)-degrees are at most twelve, and their \(g\)-degrees are at most three. Replace each equation \(f=0\) by \(p=f^3=0\). Cubing does not change its zero set over an algebraically closed field. After omitting identically zero generators, each positive \(z\)-degree of a cubed generator is a positive multiple of three, at most 36, and therefore is never two. Its \(g\)-degree is at most nine.

If a remaining generator is a nonzero constant in \(z\), the ideal is already the unit ideal over \(K(g)\), with a certificate of product degree zero. In that case one may also take this generator itself as \(\Delta(g)\) in Sections 5–6: it is nonzero, has \(g\)-degree at most nine, has norm at most \(L\), and vanishes at every chart point. Otherwise Kollár’s Theorem 1.5 and Corollary 1.9, over the field \(K(g)\), apply to the empty affine zero set. In both cases there is a certificate

\[
1=\sum_j q_j(z)p_j(z),\qquad q_j\in K(g)[z],\qquad
\deg_z(q_jp_j)\le D:=36^{10}.
\]

For fewer than ten generators the theorem’s product uses at most ten degrees; for at least ten it also uses at most ten. Thus \(D\) is valid uniformly. A generic nonzero constant and any identically zero equation require no appeal to the theorem.

## 4. Coefficient heights, with all four embeddings

For a polynomial in \(g\) and any direction/chart variables, define its coefficient \(\ell^1\) norm after an embedding \(\sigma:K\hookrightarrow\mathbb C\) as the sum of absolute values of all its coefficients. This norm is submultiplicative and satisfies the triangle inequality. Every fifth root of unity has absolute value one under each of the four embeddings.

An entry of \(H\) is a sum of at most three distinct \(g\)-monomials with root-of-unity coefficients, so its norm is at most three under every embedding. Each entry of \(T=UHV\) is a sum of at most four products, one choice from each two-coordinate row/column direction, giving norm at most twelve. Every entry in the ten coefficient columns of \(M\) is either zero or one direction coordinate, of norm one.

The determinant expansion has at most \(11!\) terms, each using one \(T\) entry and ten coefficient entries. Therefore every off-support equation and every determinant has norm at most

\[
H_*:=12\cdot11! = 479001600.
\]

Setting selected coordinates to one cannot increase coefficient \(\ell^1\) norm: it only merges monomials, and the triangle inequality applies. Cubing then gives, for every chart generator and every embedding,

\[
\|\sigma(p_j)\|_1\le L:=H_*^3
=109903340320478724096000000 < 2^{87}.
\]

All coefficients remain algebraic integers in \(\mathcal O\). No division by a direction coordinate occurs in the final chart equations: the coordinate normalization is the definition of the standard affine chart, and its equations are obtained by substitution of one.

## 5. A bounded Macaulay determinant that vanishes on every chart point

Let

\[
R=\binom{D+10}{10},\qquad A=R!\,L^R.
\]

Use the monomials in ten variables of total degree at most \(D\) as rows of a matrix \(\mathcal M(g)\), of which there are \(R\). Its columns are the coefficient vectors of every \(z^\alpha p_j\) with \(|\alpha|+\deg_z p_j\le D\). The entries belong to \(\mathcal O[g]\), have \(g\)-degree at most nine, and have coefficient \(\ell^1\) norm in \(g\) at most \(L\) under every embedding. The latter follows because each entry selects a subset of coefficients from a single shifted generator.

Let \(e\) be the coefficient vector of the constant polynomial one. The certificate above says that \(e\) lies in the column span of \(\mathcal M\) over \(K(g)\). Let its rank be \(r\), so \(1\le r\le R\). Choose \(r\) linearly independent columns, forming \(\mathcal M_0\), and choose \(r\) rows \(J\) on which the resulting square matrix \(Q\) is invertible. Put

\[
\Delta(g)=\det Q\ne0,\qquad b=\operatorname{adj}(Q)e_J.
\]

Both \(\Delta\) and the entries of \(b\) lie in \(\mathcal O[g]\). Since the chosen columns span the full column space and \(e\) lies in it, Cramer’s identity on the selected rows extends to every row:

\[
\mathcal M_0 b = \Delta e.
\]

Explicitly, over \(K(g)\) the unique coefficients expressing \(e\) in the independent columns are \(Q^{-1}e_J\); multiplying by \(\Delta\) gives the identity, which then holds in \(\mathcal O[g]\) entrywise. Interpreting coefficient vectors as polynomials gives a denominator-free polynomial identity

\[
\Delta(g)=\sum_{\ell=1}^{r}b_\ell(g)z^{\alpha_\ell}p_{j_\ell}(g,z).
\]

Therefore any point of this chart at parameter \(g=t\), under any embedding, forces the corresponding embedded \(\Delta(t)\) to vanish. The determinant is not asserted to be nonzero at the anchor; only its nonzero polynomial status is required.

The determinant expansion directly gives

\[
\deg_g\Delta\le9r,\qquad
\|\sigma(\Delta)\|_1\le r!L^r\le R!L^R=A
\]

for every embedding. This step is the complete height bound on the eliminant; no unspecified arithmetic Nullstellensatz constant is used.

## 6. Field norm and a uniform integer root bound

Take the polynomial field norm

\[
P(g)=\prod_{\sigma:K\hookrightarrow\mathbb C}\sigma(\Delta(g)).
\]

The four embeddings are the substitutions \(\eta\mapsto\eta^a\), \(a=1,2,3,4\). Each conjugate factor is nonzero. Their product is fixed by \(\operatorname{Gal}(K/\mathbb Q)\), and its coefficients are algebraic integers. Hence \(P\in\mathbb Z[g]\setminus\{0\}\), with

\[
\deg P\le36r\le36R,\qquad \|P\|_1\le A^4.
\]

If an exceptional point exists in this chart for any primitive fifth-root embedding, one factor of \(P(t)\) vanishes, so \(P(t)=0\). If \(P\) is constant, the chart has no exceptional parameters. Otherwise its nonzero leading coefficient is an integer of absolute value at least one. The elementary Cauchy root bound gives

\[
|t|\le 1+\max_{j<\deg P}|P_j/P_{\deg P}|
\le 1+A^4.
\]

For reference, the bound follows by writing \(|t|^d\le M\sum_{j<d}|t|^j\) at a root of a monic-normalized polynomial, where \(M\) is the maximum absolute lower coefficient; if \(|t|>1+M\), the right side is strictly less than \(|t|^d\).

This bound is uniform in the chart and order pair. Thus no product over the 1,024 charts or 576 pairs is necessary: if any projective necessary point exists, choose one chart containing it and apply that chart’s bound. The field norm already treats all four primitive embeddings. There is no need to guess which chart, which rank minor, or which embedding contains a hypothetical point.

## 7. From parameter bound to the explicit cutoff

For the eligible moduli, the accepted exact principal-block formula is

\[
B_N[S,S]=\frac{H(G_N)}{1+G_N^3},\qquad
S=\{0,m,2m,3m,4m\},\quad \eta=\omega^{m^2}.
\]

Here \(\eta\) is a primitive fifth root because \(\gcd(m,5)=1\). The accepted Gauss identity gives \(G_N^2=N\), so \(|G_N|^2=N\), irrespective of its real sign. The denominator cannot vanish because \(|G_N^3|=N^{3/2}>1\) for \(N\ge5\).

A permitted full representation restricts to a permitted principal-block representation, including zero edge weights and singular endpoint masks. Necessity of the closed projective system and its invariance under nonzero target scaling then give a point for \(H(G_N)\). Sections 5–6 force

\[
N=|G_N|^2\le(1+A^4)^2.
\]

This already provides the exact-form integer cutoff \((1+A^4)^2+1\). To display a simpler explicit integer, use

\[
D=36^{10}=3656158440062976,\qquad D+10<2^{52},
\qquad R\le(D+10)^{10}<2^{520}.
\]

Since \(L<2^{87}\) and \(R!\le R^R\),

\[
\log_2 A\le R\log_2R+R\log_2L
<607\cdot2^{520}<2^{530}.
\]

Consequently

\[
(1+A^4)^2
<2^{\,2^{533}+2}
<2^{\,2^{534}}=N_0.
\]

Thus any eligible \(N\ge N_0\) contradicts the necessary bound. This proves the stated result.

## 8. Boundary and scope audit

* **Zero projective coordinates:** Covered by all standard charts. No affine chart is treated as globally sufficient.
* **Singular diagonal endpoints:** The accepted closed-system necessity includes them. To recall the reason, replace each zero endpoint by a formal parameter, use the invertible endpoint representation over a Laurent-series field, normalize each inverse row/column pair by its least valuation, and specialize. Each normalized pair stays projectively nonzero. The off-support equations and multihomogeneous minors specialize to zero; no scale-variable limit is needed.
* **Zero Green edge weights:** Principal restriction and the accepted necessary-system construction divide by no individual edge weight. They remain allowed.
* **Green denominators:** They must be nonzero in the original representation grammar. Nothing in this proof extends the grammar to singular Green resolvents.
* **Target denominator:** \(1+G_N^3\ne0\) for actual eligible moduli, as checked above. No symbolic exceptional denominator is silently inverted in the polynomial family.
* **All primitive additive characters:** The Gauss identity and exact principal restriction are the accepted all-character statements; the four \(\eta\) embeddings are explicitly controlled by the norm. Negative real values of \(G_N\) are included on this positive-\(\epsilon\) curve.
* **Unmatched endpoint permutations:** No inheritance theorem for them is invoked, so they remain outside the conclusion.
* **Negative-\(\epsilon\) curve:** No empty anchor or cutoff for \(F-gC-g^3D\) is asserted.
* **Previously explicit square family:** The \(q\equiv1\pmod{241}\) theorem is neither weakened nor replaced. It remains its own exact congruence-based obstruction.

## 9. Independent original checks and their limits

`original_checks.py` is newly written standard-library code. It reads the two accepted source files only as bytes to verify their hashes. It uses its own exact cyclotomic arithmetic to check \(g_0^2=5\) and the nonzero anchor scalar for each primitive embedding, checks the displayed integer constants and inequalities, confirms the combinatorial coverage counts and determinant direction-degree accounting, and tests the Macaulay rank-minor identity on an independently constructed toy polynomial system, including a singular specialization of its determinant. It does not import, execute, or depend on historical research code.

These checks supplement the proof; they are not a new finite-size target enumeration and do not prove the accepted \(N=5\) certificate from scratch. The effectiveness argument is conditional only on the same two accepted inputs as the preceding non-effective theorem.
