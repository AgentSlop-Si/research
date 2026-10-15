# Chord rigidity and sparse bridge polynomial degree

**Revision date:** 14 October 2026. Source manuscript dated 10 October 2026.  
**Status:** Complete proof of the stated complex-field bounds, with the classical incidence argument attributed to Heineken and the prime Fourier-minor theorem attributed to Chebotarev through Tao. Independent acceptance of this revised artifact remains a separate review step. Historical priority of the project-specific composition is unresolved. No general FFT algorithm or unrestricted complexity lower bound is claimed.

## 0. Motivation and exact problem

The source research note studies a product of two Green sums

\[
M=(A^{-1}+B^{-1})(C^{-1}+D^{-1}),
\]
with \(A,B,C,D=I-\operatorname{diag}(w)P_\sigma\), arbitrary non-affine Hamiltonian cycle permutations and invertible denominators. Each resolvent applies in \(O(N)\) ideal-field operations once its weights, order, and inverse denominator have been prepared. The old exact *sparse bridge* is

\[
A M D=(A+B)(CB)^{-1}(C+D)=XK^{-1}Y. \tag{B}
\]

Indeed, \(A(A^{-1}+B^{-1})=(A+B)B^{-1}\) and \((C^{-1}+D^{-1})D=C^{-1}(C+D)\), while \(B^{-1}C^{-1}=(CB)^{-1}\). This proves (B) without commuting any factors.

The earlier `FFT_FOURIER_CYCLE_UNCERTAINTY_THEORY_2026-10-10.md` established a \(\ge N^2/4\) entry-densification bound for \(A L^{-1}F_pR^{-1}B\) at **prime** \(p\), with arbitrary non-affine cycles. We strengthen that for **odd** lengths with primitive local affine triples and connect it to an exact lower bound on polynomial graph shortcuts to the bridge.

### Sources and scope

The complete-line incidence ingredient follows from Hermann Heineken, *Regelmässige Vielecke und ihre Diagonalen*, L'Enseignement Mathématique (2) 8 (1962), 275–278, DOI [10.5169/seals-37967](https://doi.org/10.5169/seals-37967). His unnumbered theorem is on p. 278; his proof is Eqs. (1)–(9), pp. 276–278. The proof uses arbitrary real line parameters, so exterior intersections are included. The side-line extension is established explicitly below rather than silently replacing his word “diagonals.” The n=5 case follows separately from endpoint counting.

The prime Fourier-minor fact is Chebotarev's theorem, cited here through the proof in Terence Tao, *An uncertainty principle for cyclic groups of prime order*, arXiv:math/0308286v6, Lemma 1.3, p. 3, proof pp. 3–4. This is a source and proof attribution, not a claim that Tao originated that classical theorem. The exact project-specific combination has no established worldwide-priority claim. The bounds below retain the original mathematical scope.

## 1. Notation

Let \(n\ge5\) be odd and \(\omega=e^{-2\pi i/n}\). Use the **unnormalized** DFT \(F_n[r,c]=\omega^{rc}\), so all its entries are nonzero.

For a permutation \(\sigma\), let \(P_\sigma[i,\sigma(i)]=1\). Write

\[
A=I-\operatorname{diag}(a_i)P_\alpha,\quad
B=I-\operatorname{diag}(b_i)P_\beta,
\]
where \(\alpha,\beta\) are arbitrary \(n\)-cycles unless further restricted. Let \(L,R\) be invertible monomial matrices (permutations and nonzero diagonal scalings); \(L^{-1}\) maps Fourier frequency rows according to some permutation \(\rho\). Set

\[
T=A L^{-1}F_n R^{-1}B.
\]

A local pair of adjacent \(\alpha\)-cycle rows is \((i,j)\), \(j=\alpha(i)\). Its three Fourier-frequency labels are \((\rho(i),\rho(j),\rho(\alpha(j)))\). Call this pair **primitive-affine** if these labels form an arithmetic progression modulo \(n\) with common difference \(d\) satisfying \(\gcd(d,n)=1\).

## 1a. Complete vertex line incidence

**Lemma H (Heineken argument with explicit side-line extension).** For odd n≥5, three distinct complete real lines, each joining two vertices of a regular complex n-gon, cannot have a common finite point other than a polygon vertex. Side lines and intersections exterior to the polygon are included.

**Proof.** A real line through distinct unit points x,y is exactly

\[
z+xy\overline z=x+y.
\]

Indeed, this equation is equivalent to \((z-y)/(x-y)\) being real. Distinct such lines cannot coincide, since a line meets the circle in at most two points. If three meet at a nonvertex point, they must therefore have six distinct endpoints and cannot be parallel. This already proves n=5.

For n≥7, rotate one endpoint to 1 and write the three pairs as (1,R), (S,T), (U,V), all powers of a primitive nth root. Eliminating z and its conjugate from the three line equations gives

\[
F=(1-T)(1-S)(1-UV/R)-(1-U)(1-V)(1-ST/R)=0.
\]

In fact the 3 by 3 concurrence determinant with rows (1,R,1+R), (1,ST,S+T), (1,UV,U+V) equals −RF. Since n is odd, the cyclotomic automorphism that squares the primitive root gives \(F(R^2,S^2,T^2,U^2,V^2)=0\). Define

\[
G=(1+T)(1+S)(1+UV/R)-(1+U)(1+V)(1+ST/R).
\]

Factoring the squared identity yields

\[
F(R^2,S^2,T^2,U^2,V^2)
 -(1+T)(1+S)(1+UV/R)F
 =(1-U)(1-V)(1-ST/R)G.
\]

The factors on the right preceding G are nonzero. Distinct endpoints exclude U=1 and V=1; ST=R would make the first two distinct chord lines parallel, which finite concurrence excludes. Hence G=0. Subtracting F from G and multiplying by R/2 gives

\[
Q=(R-U)(R-V)-(R-S)(R-T)=0.
\]

Apply the same cyclotomic automorphism to Q. With
\(J=(R+U)(R+V)-(R+S)(R+T)\), direct factorization gives

\[
Q(R^2,S^2,T^2,U^2,V^2)-(R+S)(R+T)Q=(R-U)(R-V)J.
\]

Distinctness makes the right prefactor nonzero, so J=0. But Q+J=2(UV−ST), forcing UV=ST and making the last two lines parallel, a contradiction. Equal endpoint products give equal chord-line directions because the real direction through x,y has argument half the argument of xy plus π/2, modulo π. No step requires nonadjacent endpoints or a real parameter between 0 and 1; the argument therefore covers side lines and exterior intersections. This is the algebra of Heineken's proof, written with explicit guards and full-line interpretation. □

## 2. Local chord rigidity theorem

**Theorem A (odd-length primitive-affine two-row barrier).** For every primitive-affine adjacent pair \((i,\alpha(i))\), *regardless of the second cycle \(\beta\), all edge weights (including zero weights), all nonzero monomial endpoint scales, and all column permutations*,

\[
\boxed{\big|\operatorname{supp}T[i,:]\cup\operatorname{supp}T[\alpha(i),:]\big|\ge n-2.} \tag{A}
\]

This is stronger than the previously proved \(\ge\lceil n/2\rceil\) bound for prime lengths. It also holds for **odd composite** lengths, such as \(9,15,21,25,27,\ldots\), whenever the progression step is coprime to \(n\).

### Proof

Step 1. Disregard nonzero row and column scalings and relabel output columns. A primitive-affine Fourier triple lets us represent the two rows of \(H=A L^{-1}F_n R^{-1}\), up to nonzero per-column scalar, as

\[
h(t)=\begin{pmatrix}1-a t\\t(1-bt)\end{pmatrix},\qquad t\in\mu_n=\{1,\omega^d,\ldots,\omega^{(n-1)d}\},
\]
with arbitrary complex \(a,b\). Since \(d\) is a unit, the \(t\)'s are all distinct.

Step 2. For distinct \(t,u\in\mu_n\), direct expansion gives

\[
\det(h(t),h(u))=(u-t)\big[1-b(t+u)+abtu\big]. \tag{1}
\]

If \(b=0\), every pair of columns is independent. If \(b\ne0\), dependent nonzero columns must satisfy

\[
t+u-a t u=z,\qquad z=1/b. \tag{2}
\]

Step 3. If there are two **distinct** unordered dependent pairs, their products \(tu\) differ: if two distinct pairs had the same product, (2) would give the same sum, hence the pairs would be the same roots of one quadratic. Conjugate (2) using \(\bar t=1/t\) and \(\bar u=1/u\):

\[
t+u=\bar a+\bar z\,tu.
\]

Comparing the two distinct product values forces \(a=\bar z\). Thus **every dependent pair** is a chord \((t,u)\) lying on the real Euclidean line through the common point \(z\), because its chord equation is

\[
t+u=z+\bar z\,tu. \tag{3}
\]

Step 4. No three **nonzero** columns of \(h\) can all be proportional. Indeed \(h(t)\) is the image, under a rank-two \(2\times3\) coefficient matrix, of the Vandermonde vector \((1,t,t^2)^T\). Any three distinct \(t\)'s produce an invertible \(3\times3\) Vandermonde matrix, so the image has rank two. Consequently, dependent *nonzero* column pairs have disjoint endpoints.

Step 5. If there are at least two dependent nonzero pairs, Step 3 places all such pairs on complete chord lines through the finite point z=1/b. This point cannot be a polygon vertex: every chord line through a vertex must have that vertex as an endpoint, whereas Step 4 makes the pairs disjoint. Lemma H, using Heineken's proof with its explicit side-line extension, excludes three such lines for odd n≥7. For n=5 three disjoint pairs would require six vertices. Therefore there are at most two unordered dependent pairs among nonzero columns for every odd n≥5.

Step 6. The matrix \(T=H B\) has columns \(T_{:,\beta(k)}=H_{:,\beta(k)}-b_k H_{:,k}\). If the selected two entries of this column vanish, the two original selected columns must be dependent. A Hamiltonian cycle uses each unordered pair as a directed edge at most once (\(n\ge3\)). Therefore at most two columns of the selected row pair of \(T\) can both vanish.

The exceptional case of a zero selected two-vector \(h(t_0)=0\) entails \(a=b=t_0^{-1}\). For every \(t\ne t_0\), \(h(t)=(1-t/t_0)(1,t)^T\): all remaining columns are nonzero and pairwise independent. Hence a \(\beta\)-cycle can then create at most one jointly zero output column (the one at \(t_0\), requiring a zero incoming weight). Thus (A) always holds. \(\square\)

### Sharpness of the *local* bound

For every odd n≥5 write w=ω and take disjoint pairs (1,w²) and (w,w³). Set

\[
a=\frac{1+w^2}{w^2(1+w)},\qquad
z=\frac{w(1+w^2)}{1+w},\qquad
b=\frac{1+w}{w(1+w^2)}=1/z.
\]

All denominators are nonzero: a primitive root of odd order n≥5 has w≠0, w≠−1, w²≠−1 and w³≠1. Direct substitution gives

\[
h(w^2)=-\frac{w^3}{1+w+w^2}h(1),\qquad
h(w^3)=-w(1+w+w^2)h(w).
\]

The two displayed multipliers are nonzero. No h(t) vanishes, since a=b would imply
\((1+w^2)^2-w(1+w)^2=(w-1)^2(w^2+w+1)=0\), impossible for this primitive w. Use α(i)=i+1 modulo n, identity monomial endpoints, left edge weights a₀=a, a₁=b and all other left weights zero. Choose β in the cyclic order (0,2,1,3,4,…,n−1), give its 0→2 and 1→3 edges the two displayed multipliers, and give every other edge weight zero. Exactly columns 2 and 3 vanish jointly in rows 0 and 1; every other selected output column equals its nonzero h(t). The support union is therefore exactly n−2.

Both weighted-cycle denominators are nonsingular: for a weighted n-cycle, det(I−diag(c)P)=1−∏cᵢ, and both products here are zero. This proves local sharpness for all odd n≥5 directly over C. It makes no assertion that the global density bound is attained.

## 3. Global and hybrid non-affine theorems

**Theorem B (global odd densification).** If every local adjacent \(\alpha\)-pair is primitive-affine (e.g. \(\alpha(i)=i+d\) with \(\gcd(d,n)=1\) and \(\rho\) an affine permutation with unit slope), then

\[
\boxed{\operatorname{nnz}(T)\ge \left\lceil\frac{n(n-2)}2\right\rceil.}\tag{4}
\]

**Proof.** Sum (A) over the \(n\) cyclic adjacent row pairs. Each row's support is counted exactly twice, and a union is no larger than the sum of its two row supports. \(\square\)

**Theorem C (non-affine interpolation at prime length).** Let \(n=p\ge5\) be prime with **arbitrary** Hamiltonian \(\alpha,\beta\) and arbitrary endpoint monomial matrices. Let \(g\) count the \(p\) adjacent \(\alpha\)-pairs whose three Fourier-frequency labels in \(\rho\) form a modular arithmetic progression. Then

\[
\boxed{\operatorname{nnz}(T)\ge
\left\lceil\frac{g(p-2)+(p-g)\lceil p/2\rceil}{2}\right\rceil.}\tag{5}
\]

**Proof.** Each of the g progression pairs has union support at least p−2 by Theorem A. For another adjacent pair, the two selected rows are a rank-two coefficient map applied to three distinct Fourier-frequency rows. The map has rank two even when a left edge weight is zero: its first and second rows have nonzero leading entries in their respective first and second frequency positions. Every three-column restriction of those three Fourier rows is invertible by Chebotarev's theorem (Tao v6, Lemma 1.3, p. 3; proof pp. 3–4). Thus every three-column restriction of the selected two-row matrix has rank two, also after nonsingular endpoint scalings and column permutation.

If all selected columns are nonzero, each proportionality class has at most two members. Hence at most floor(p/2) disjoint unordered dependent pairs exist. Each jointly zero output column must arise from one of these pairs, and the Hamiltonian right cycle uses each unordered pair at most once. If a zero selected column exists, there cannot be a second one, and every pair of remaining columns is independent; otherwise a three-column restriction would have rank at most one. Only the zero target column with zero incoming edge weight can then vanish. In either case the support union is at least ceil(p/2). Summing these p local inequalities and dividing by two yields (5). □

For \(g=0\) this recovers the old \(\approx p^2/4\) bound. For \(g=p\) it gives \(\approx p^2/2\). The \(g\)-dependent statement connects **non-affine cycle geometry** with a quantified algebraic obstruction; it does not require the cycle itself to be affine.

## 4. Consequence for the surviving Green-sum sparse bridge

From the exact noncommutative identity (B), the two-stage Fourier hypothesis \(F_n=(A^{-1}+B^{-1})(C^{-1}+D^{-1})\) implies

\[
A F_n D=X K^{-1}Y,
\qquad X=A+B,\ K=CB,\ Y=C+D. \tag{6}
\]

Here \(X,Y\) have at most **three** nonzeros per row, and \(K\) at most **four**. Suppose a proposed shortcut evaluates that center *exactly* as a scalar-coefficient polynomial \(P_L(K)=\sum_{r=0}^L c_rK^r\), so that

\[
A F_n D=X P_L(K)Y.\tag{7}
\]

If the cycle in the **leftmost** denominator \(A\) is primitive stride, and \(n\) is odd, Theorem B applies to the left/right Fourier sandwich \(AF_nD\) (\(D\) may have any Hamiltonian cycle). A product of row-\(x\)-sparse, row-\(k\)-sparse and row-\(y\)-sparse matrices has at most \(xk^ry\) nonzero entries per row, so

\[
\operatorname{nnz}(XP_L(K)Y)\le n\,xy\sum_{r=0}^L k^r.\tag{8}
\]

With \((x,k,y)=(3,4,3)\), combine (4), (7) and (8):

\[
\boxed{9\sum_{r=0}^L4^r\ge\frac{n-2}{2},\quad
4^{L+1}\ge1+\frac{n-2}{6},\quad
L\ge \log_4\!\left(1+\frac{n-2}{6}\right)-1.}\tag{9}
\]

This is a **logarithmic exact graph-polynomial degree barrier** to replacing the sparse-bridge inverse by a uniformly bounded-degree polynomial. It is *not* a lower bound on all possible \(O(N)\)-work recurrences for \(K^{-1}\), nor proof that separate polynomial powers require separate unshared work. If the leftmost cycle is arbitrary non-affine and \(n=p\) prime, the earlier FCUT \(\Omega(p^2)\) support bound still supplies \(L=\Omega(\log p)\), with a weaker constant.

**Escape route still open:** genuinely nonlocal exact sparse solves, non-polynomial shared-state graph algorithms, non-affine phases, and multi-stage products that satisfy exact Fourier/Weyl covariance. None has been constructed here.

## 5. Accepted scope and historical qualification

The proof establishes Theorem A, its all-odd local sharpness, Theorem B, the prime hybrid Theorem C, and the scalar-polynomial degree consequence (9) in their stated models. The classical geometric dependency has now been incorporated with precise attribution, a full-line argument, side-line guards and the n=5 endpoint case. The prime hybrid proof is also explicit rather than relying on an unexpanded project predecessor lemma.

The following boundaries remain essential:

- All geometric near-full bounds are over C, at odd n≥5 with a primitive-affine local frequency step. Arbitrary non-affine composite triples are outside this theorem.
- Endpoint monomial matrices are nonsingular; the right routing is a Hamiltonian cycle. Zero edge weights are allowed. Inverse formulas additionally require nonsingular weighted-cycle denominators.
- The n−2 bound is false over arbitrary finite fields. A freshly reconstructed GF(19), n=9 example with primitive root 4, α(i)=i+1, left weights (1,12,0,0,0,0,0,0,0), β=(3,8,5,4,1,6,7,0,2) as a permutation array, and right weights (0,14,15,0,0,0,10,0,0) has joint-zero columns 5,7,8 in rows 0,1. Its union support is 6<7 and both denominator determinants are 1. This is a counterexample to field-generalization, not a counterexample over C.
- The bridge conclusion concerns scalar-coefficient polynomials in K of specified degree. It does not rule out a general fast sparse solve, non-polynomial recurrences, shared-state algorithms, or the full two-stage product-of-sums architecture.
- Geometric incidence, Chebotarev full spark and elementary sparse-polynomial reachability are classical ingredients. Worldwide priority of this Fourier-sandwich composition is unresolved. No discovery count, novelty rank or stronger general theorem is promoted by this revision.

## 6. References

1. H. Heineken, *Regelmässige Vielecke und ihre Diagonalen*, L'Enseignement Mathématique (2) 8 (1962), 275–278. DOI: https://doi.org/10.5169/seals-37967 . Unnumbered theorem p. 278; proof Eqs. (1)–(9), pp. 276–278; finite/nonvertex exclusions p. 275. Primary text: https://www.e-periodica.ch/cntmng?bot=1&pid=ens-001%3A1962%3A8%3A%3A93 . Complete primary PDF text extraction was read; PDF bytes and visual facsimile inspection are not claimed.
2. T. Tao, *An uncertainty principle for cyclic groups of prime order*, Math. Res. Lett. 12 (2005), 121–127; arXiv:math/0308286v6 (22 July 2004). https://arxiv.org/pdf/math/0308286v6 . Lemma 1.3, p. 3, proof pp. 3–4, is the cited proof of Chebotarev's prime Fourier-minor theorem. Tao's paragraph following the lemma gives the historical attribution to Chebotarev; this note does not independently establish original priority.
3. J. F. Rigby, *Multiple intersections of diagonals of regular polygons, and related topics*, Geometriae Dedicata 9 (1980), 207–238. DOI: https://doi.org/10.1007/BF00147438 . Retained as historical background from the source manuscript; not required to fill a gap in the proof above.
4. A. Sidorenko, *Explicit Formulas for Odd-Indexed Terms in A344899, A146212, and A344857* (2021), https://oeis.org/A344857/a344857.txt . Historical route to the complete-line interpretation, retained as background.
5. B. Poonen and M. Rubinstein, *The Number of Intersection Points Made by the Diagonals of a Regular Polygon*, SIAM J. Discrete Math. 11 (1998), 135–156. https://arxiv.org/abs/math/9508209 . Historical interior-geometry background.
6. Source manuscript: `fft_cycle_chord_20261010/THEOREM.md` within `FFT_CHORD_RIGIDITY_BRIDGE_THEORY_2026-10-10.zip`, retained byte-for-byte with this revision. Its predecessor FCUT and sparse-bridge pointers remain historical provenance; the required hybrid argument and bridge identity are explicitly present here.

## 7. Verification and preservation

The original manuscript and archive are preserved. The revision diff records the citation integration, complete-line proof, n=5 case, exact sharpness simplification, expanded prime hybrid proof and finite-field boundary correction. A new independently authored checker verifies fourteen exact algebraic identities and reconstructs the full GF(19) counterexample. No original or candidate historical program was executed, imported, compiled or AST-parsed. The checker is supplemental arithmetic evidence; all-length assertions follow from the proofs above. The separate source manifest binds every local artifact by SHA-256 and distinguishes captured primary text from unavailable PDF bytes.
