# Exact full Fourier membership at N=6 with two Green-sum stages, 2+3 terms

## Verdict and exact scope

This candidate proves the declared, previously unlisted **N=6, q1=2, q2=3** full negative-sign unnormalized Fourier membership in the original Phase56 complex-gain model. All five cycle orders are fixed to `(0,1,2,3,4,5)`, the middle diagonal is the identity, and the interstage permutation is the identity. The construction supplies every gain, holonomy, coefficient and external diagonal by exact algebraic definitions. It proves all 36 entries and all original nonvanishing guards.

This is a **target-membership certificate using classical ingredients**, not a claim of worldwide novelty, an FFT speedup, an optimal term count, or an all-length construction. The source's existing thirteen finite-rank claims and its five earlier membership certificates are neither rerun nor changed. A conditional inverse-polynomial compilation lemma is recorded below; its hypotheses are checked here only at N=6.

## 1. Source binding and legal grammar

Owner: `PHASE56-COMPLEX-GREEN-N5-N8-20261011`. Private native worksheet row locators are omitted. The source's current action is to select an untested size and fixed cycle/term split and separately establish full Fourier membership, without repeating generic-rank work.

Original source: `Phase56_Lightweight_Fresh.zip`, SHA-256 `179a5b7de5575e7c05adf354421a70b8914fb698a3b1b81e22d38e242a737272`; `phase56/PHASE56_THEOREMS.md`, SHA-256 `de2d028094611802a644484c122f07949d0643948aad1e11248ee0f211e25986`. Original §§56.1 and 56.5 define

\[
G[o,g,h]_{ij}=\frac{g_i/g_j}{1-h}
\begin{cases}1,&\operatorname{pos}_o(i)\geq\operatorname{pos}_o(j),\\h,&\operatorname{pos}_o(i)<\operatorname{pos}_o(j),\end{cases}
\quad F_N=L S_2 D S_1 R.
\]

Each stage is a sum of Green terms with variable complex coefficients; gains are arbitrary nonzero complex numbers, `h` is nonzero and unequal to 1, and `L,D,R` are invertible diagonal masks. The source explicitly allows unrestricted independent Hamiltonian cycle orders and imposes **no distinct-cycle condition**. Repeated natural cycles are therefore legal. The original fitter was read inertly as corroboration: it samples each cycle independently and imposes no deduplication. No archived research program was executed or imported.

The first-term gain/coefficient normalizations in source §56.4 and its numerical fitter are gauge coordinates, not restrictions on the §56.1 family. The present proof uses the original unrestricted coordinates directly.

Earlier full Fourier certificates are N=5(2+2), 7(3+3), 8(3+4), 11(5+5), and 13(6+6). N=6(2+3) is not among these or the thirteen finite-rank configurations. A bounded comparison with this recovered original source and nearby Phase44/M-CHIRP owner summaries did not locate this exact certificate. This is not an exhaustive priority investigation.

## 2. Exact constants and fixed parameter assignment

Set

\[
a=e^{-\pi i/6}=(\sqrt3-i)/2,\qquad a^{12}=1,\quad a^6=-1.
\]

Let `P` denote the cyclic shift with `P[i,j]=1` exactly when `i=j+1 mod 6`. Define

\[
C(z)=\sum_{k=0}^{5}a^{-k^2}z^k,\qquad
Q(z)=\sum_{k=0}^{5}a^{k^2}z^k
=1+a(z+z^5)+a^4(z^2+z^4)+i z^3.
\]

Define `t1,...,t5` as the five roots, listed in increasing lexicographic order of `(Re t, Im t)`, of

\[
p(t)=t^5Q(1/t)=t^5+a t^4+a^4t^3+i t^2+a^4t+a.
\]

This definition is exact; no printed floating-point root is a parameter. Section 3 proves that there are exactly five distinct nonzero roots. Their ordering specifies one fixed allocation, not a continuous free parameter. The proof in fact works for any labeling of the five roots.

For explicit algebraic setup, one root is `a^{-1}` and the remaining four are exactly the roots of

\[
H(t)=t^4+\sqrt3\,t^3+t^2+
(\sqrt3/2+3i/2)t-1/2+\sqrt3 i/2,
\qquad p(t)=(t-a^{-1})H(t).
\]

Set `A={1,2}` and `B={3,4,5}`. For every index `s`, define

\[
b_s=\prod_{r\in A\setminus\{s\}}(1-t_r/t_s)^{-1}\quad(s\in A),
\qquad
b_s=\prod_{r\in B\setminus\{s\}}(1-t_r/t_s)^{-1}\quad(s\in B).
\]

All five terms have the fixed order `o_s=(0,1,2,3,4,5)` and

\[
g_s(v)=t_s^v\quad(0\leq v<6),\qquad h_s=t_s^6.
\]

The stage coefficients and all diagonals are

\[
S_1=\sum_{s\in A}b_sG[o_s,g_s,h_s],\quad
S_2=\sum_{s\in B}6b_sG[o_s,g_s,h_s],\quad
D=I,\quad L_{ii}=R_{ii}=a^{i^2}.
\]

This is exactly two terms in stage 1 and three in stage 2, with no omitted zero terms and no extra permutations or factors outside the original grammar.

## 3. Exact polynomial certificate and all guards

First,

\[
\boxed{Q(z)C(z)\equiv6\pmod {z^6-1}.}
\tag{1}
\]

For completeness, the coefficient at cyclic offset `r` in the product is

\[
\sum_{k=0}^5 a^{k^2-(r-k)^2}
=a^{-r^2}\sum_{k=0}^5(a^{2r})^k.
\]

The chirp coefficient sequences are 6-periodic because `a^{(k+6)^2-k^2}=a^{12k+36}=1`. The geometric sum is 6 at `r=0` and zero at the other five offsets, proving (1). The fresh verifier independently multiplies all coefficients exactly in `Q[a]/(a^4-a^2+1)`.

Second, `Q` is squarefree. Here is a small exact certificate requiring no numerical roots or large discriminant. Specialize the integral cyclotomic coefficient ring by `a -> 2 mod 13`; this is legitimate since `2^4-2^2+1=13`. The resulting polynomial is

\[
\bar Q=1+2z+3z^2+5z^3+3z^4+2z^5.
\]

Over `F13`, put

\[
U=2+z-2z^2+4z^3,\quad
V=6-z-6z^2-4z^3-6z^4.
\]

Direct multiplication verifies

\[
\boxed{U\bar Q+V\bar Q'=1\quad\text{in }\mathbb F_{13}[z].}
\tag{2}
\]

The degrees of `Q` and `Q'` do not drop in this specialization, since their leading coefficients map to 2 and 10. Thus their resultant has nonzero reduction. Their characteristic-zero resultant is nonzero, so `Q` is squarefree. This standard specialization argument concerns an algebraic resultant, not a numerical rank inference.

Now every required guard follows:

1. `Q` has degree 5 and constant coefficient 1, hence five roots counting multiplicity and no zero root. Equation (2) makes them distinct. Their reciprocals `t_s` are likewise distinct and nonzero.
2. If `t_s^6=1`, then `r=1/t_s` satisfies `r^6=1` and `Q(r)=0`, contradicting (1). Therefore every `h_s=t_s^6` is nonzero and unequal to 1.
3. Every gain `t_s^v` is nonzero. Every denominator and factor in `b_s` is nonzero because the `t_s` are nonzero and distinct. Therefore all five stage coefficients are nonzero.
4. `D=I` and every diagonal entry of `L,R` are nonzero.
5. Section 4 proves `M=S2 D S1=C(P)`, whose entries are `a^{-(i-j)^2}` and never zero. In particular, the first-row and first-column guards and the entire dense-output chart hold.

There is no appeal to generic dominance, parameter counting, approximate residuals, or unproved regularity of a selected optimizer.

## 4. All-entry original-grammar identity

For every `s`, the original natural-cycle Green formula gives

\[
G[o_s,g_s,h_s]=(I-t_sP)^{-1}.
\tag{3}
\]

Indeed, its `(i,j)` entry is `t_s^(i-j)/(1-t_s^6)` if `i>=j`, and `t_s^(i-j+6)/(1-t_s^6)` otherwise, exactly the finite cyclic geometric resolvent. These inverses exist by Section 3.

For a set `E` of distinct nonzero scalars, the elementary partial-fraction identity is

\[
\prod_{r\in E}(1-t_r z)^{-1}
=\sum_{s\in E}\frac{\prod_{r\in E\setminus\{s\}}(1-t_r/t_s)^{-1}}{1-t_s z}.
\tag{4}
\]

To prove (4), multiply by the denominator. The numerator difference has degree at most `|E|-1` and vanishes at all `|E|` distinct points `z=1/t_s`; it is therefore identically zero.

Because `Q(0)=1`, its reciprocal-root factorization is exactly

\[
Q(z)=\prod_{s=1}^5(1-t_s z).
\]

Using (3), (4), and commutation of polynomials in `P`,

\[
S_2S_1
=6\prod_{s=1}^5(I-t_sP)^{-1}
=6Q(P)^{-1}
=C(P),
\]

where the last step is (1) and `P^6=I`.

Finally, for **every** `0<=i,j<6`, not just a submatrix or cross-ratio system,

\[
(LS_2DS_1R)_{ij}
=a^{i^2}\,a^{-(i-j)^2}\,a^{j^2}
=a^{2ij}=e^{-2\pi i\,ij/6}=F_6[i,j].
\tag{5}
\]

Cyclic wrap-around does not alter the middle factor because the chirp is 6-periodic. Equation (5) also verifies the zeroth row and column and the exact Fourier sign and normalization. `verify_exact.py` independently checks all 36 equalities in the cyclotomic field.

## 5. Reusable conditional compilation lemma

Let `P` be the N-cycle shift. Suppose a desired circulant `C(P)` has inverse polynomial `Q(P)/kappa` with

- `C(z)Q(z) == kappa mod(z^N-1)`, where `kappa != 0`;
- `Q(0)=1`, degree `T>=2`, and `Q` squarefree.

Then splitting its `T` reciprocal roots into any two nonempty groups produces two original complex-gain Green sums with those term counts, middle diagonal `I`, and product exactly `C(P)`. Formulae (3)-(4) supply the gains, holonomies and coefficients. No root can be zero or have Nth power 1, and all coefficients are nonzero.

The same proof establishes this conditional algebraic lemma. It does **not** prove its squarefreeness/full-degree hypotheses for arbitrary chirp lengths, a Fourier-specific minimum, or a sublinear-in-N number of terms.

## 6. Setup, arithmetic, and limitations

The exact setup is explicit and separate from transform execution:

1. Construct `a=(sqrt(3)-i)/2` in `Q(sqrt(3),i)`.
2. Factor/isolate the four roots of the displayed quartic `H`, adjoin them to a splitting field, include `a^-1`, and compare exact real/imaginary algebraic values to perform the fixed ordering. This is a genuine algebraic preprocessing task; numerical approximations alone do not implement it. Up to ten root-order comparisons suffice by a simple insertion sort. No uniform bit-cost or conditioning bound for this algebraic work is claimed.
3. Once the five roots are supplied, powers, inverse powers, holonomies, partial-fraction coefficients, and folded output factors can be prepared using at most **93 complex multiplications, 13 subtractions, and 15 scalar inversions**, plus the explicitly separate algebraic root construction and comparisons. This conservative bound includes generating the needed outer chirp powers. It is an arithmetic count in the chosen algebraic splitting field, not a unit-cost claim for arbitrary bit precision.

For online action, precompute `1/g_s(v)`, `h_s/(1-h_s)`, and the stage coefficient times `g_s(v)`. A supplied Green term of size 6 then uses 13 complex multiplications and 11 additions: six input scalings, a five-addition prefix scan, one total-prefix scaling, six additions, and six output scalings. Five terms cost 65 multiplications and 55 additions. Summing the two stage outputs costs `6[(2-1)+(3-1)]=18` additions. The two outer diagonals cost another 12 multiplications, and `D=I` costs nothing. Thus one direct execution uses at most

\[
\boxed{77\text{ complex multiplications and }73\text{ complex additions},}
\]

with no online divisions, six input reads and six output writes, after the specified constants are supplied. At most 71 complex precomputed constants suffice for this direct prefix schedule; stage workspace can be reused. This is a representation certificate, not a competitive six-point FFT implementation.

With a hypothetical analogous `T=N-1` family, direct Green execution would cost `O(N^2)`, not improve `O(N log N)`. The present proof establishes no such all-length family and no numerical stability theorem.

## 7. Attribution and review boundary

The chirp-to-convolution identity is classical (Bluestein), and the resolvent factorization uses elementary polynomial factorization and partial fractions. The original Phase56 model and research target are retained as source attribution. Official AMD rocFFT documentation displays the same chirp identity used here: <https://rocm.docs.amd.com/projects/rocFFT/en/docs-5.7.1/design/bluestein.html>. This citation concerns the classical identity, not a claim that the documentation contains this specific Green-network certificate.

The resulting contribution to this record is bounded: an exact, non-iterative certificate for the previously unlisted original target `N6(2+3)` and a clear conditional compilation criterion. It should receive **no discovery-count, rank-count, priority-score, or worldwide-novelty promotion** merely from correctness. All broader original agenda items remain separate.

The candidate verifier is newly authored, standard-library-only exact arithmetic. Independent review must separately assess the source grammar, specialization argument, partial fractions, guards, all-entry identity, and accounting. Candidate success is not itself an independent acceptance.
