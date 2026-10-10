# Quadratic Fourier–Green Phase Rigidity

**Research checkpoint:** 10 October 2026  
**Status:** Rigorous fixed-stage algebraic certificate; exact modular examples; a characteristic-zero exceptional-locus existence proof; and a fixed-stage operator-norm gap. **No new arbitrary-input faster FFT.**  
**Novelty:** New combination/application within the audited project, **not established as unpublished mathematical research**. The symmetric-square/Segre lifting idea is known.

## 1. Model and inherited reduction

Work over a field \(K\) of characteristic not 2, containing a primitive \(N\)-th root \(\omega\). Let \(F=(\omega^{ij})_{i,j=0}^{N-1}\). Consider

\[
F=L A D B E C, \tag{1}
\]

where \(A,C\in\mathrm{GL}_N(K)\), \(B\in K^{N\times N}\) has **no zero entries**, and the **unknown** matrices \(L,D,E\) are invertible diagonal matrices. For the four-Green example, \(A=G_1+G_2\), \(B=G_3+G_4\), \(C=I\), with individually permuted and diagonally gauged weighted Hamiltonian-cycle resolvents \(G_j=(I-D_{w_j}P_{\sigma_j})^{-1}\).

From the preceding Fourier–Segre project, put \(H=FC^{-1}\), and, for unknown \(c\in K^N\), define

\[
Z(c)_{uj}=\frac{(A^{-1}\operatorname{diag}(c)H)_{uj}}{B_{uj}}.
\]

Then (1) holds **iff** \(c\) has no zero entries and \(Z(c)\) is rank one with no zero entries. In that case \(Z(c)=d e^T\), and the diagonals are reconstructed as \(L=\operatorname{diag}(c^{-1}), D=\operatorname{diag}(d), E=\operatorname{diag}(e)\). This is **inherited** from the previous package, not claimed new here.

Let \(h_j=He_j\), \(b_j=Be_j\), and

\[
P_j=\operatorname{diag}(b_j^{-1})\,A^{-1}\operatorname{diag}(h_j),
\qquad Z(c)[:,j]=P_jc. \tag{2}
\]

No assumption that \(P_0\) is invertible is required for the new certificate.

## 2. New project theorem — three-column symmetric-square certificate

For \(J=\{0,1,2\}\) and every pair of rows \(u<v\) and columns \(j<k\) in \(J\), define

\[
q_{uv,jk}(c)
=(P_jc)_u(P_kc)_v-(P_kc)_u(P_jc)_v.
\tag{3}
\]

Each is a homogeneous quadratic polynomial in \(c\). Write

\[
v(c)=(c_ac_b)_{0\le a\le b<N}\in K^{N(N+1)/2}.
\]

Expand the coefficients of all \(q_{uv,jk}\) and stack them to form an explicit matrix

\[
\boxed{\mathcal Q_J\in K^{\,3\binom N2\ \times\ \binom{N+1}2}},
\qquad \mathcal Q_Jv(c)=(q_{uv,jk}(c))_{uv,jk}. \tag{4}
\]

For a diagonal monomial \(c_a^2\), its row coefficient is
\(P_j[u,a]P_k[v,a]-P_k[u,a]P_j[v,a]\). For \(a<b\), its coefficient is the sum of the two index orders, i.e.
\(P_j[u,a]P_k[v,b]+P_j[u,b]P_k[v,a]-P_k[u,a]P_j[v,b]-P_k[u,b]P_j[v,a]\).

**Theorem A (sufficient exact impossibility test).** If

\[
\boxed{\operatorname{rank}_K\mathcal Q_J=\binom{N+1}{2}},\tag{5}
\]

then (1) has **no solution** in invertible diagonal \(L,D,E\). The conclusion remains true over every extension field of \(K\), including its algebraic closure.

**Proof.** A solution to (1) gives a nonzero \(c\) such that \(Z(c)\) is rank one. Every minor (3) vanishes, so \(\mathcal Q_J v(c)=0\). But \(v(c)\ne0\) for nonzero \(c\) over a field. Full column rank contradicts this. Rank remains full under field extension. \(\square\)

A two-output-column instance gives only \(\binom N2\) equations for \(\binom{N+1}{2}\) lifted unknowns, so **at least three columns are necessary for this particular injectivity approach**. Full rank is sufficient but not necessary for rejection; lower rank does not establish existence, because \(\ker\mathcal Q_J\) may contain no decomposable \(v(c)\).

**Relation to the old commutator gate.** When \(P_0\) is invertible, the previous construction \(T_j=P_0^{-1}P_j\) has the necessary condition \(\det[T_1,T_2]=0\). That determinant being zero does not prevent (5). The new method also works when \(P_0\) is singular, a case where the old \(T_j\) was undefined.

## 3. New project theorem — all-gauge quantitative spectral gap

Now take \(K=\mathbb C\), and use the same \(\mathcal Q_J\) with unscaled monomial columns (no \(\sqrt2\) factors). Set

\[
 s=\sigma_{\min}(\mathcal Q_J)>0,\quad
 M_P=\left(\sum_{j=0}^2\|P_j\|_2^2\right)^{1/2},\quad
 b_*=\min_{u,j}|B_{uj}|>0.
\]

**Theorem B (fixed-stage approximation gap).** If (5) holds, then **every** choice of invertible diagonal \(L,D,E\) satisfies

\[
\boxed{
\|LADBEC-F\|_2\ \ge\
\frac{s\,b_*}{\sqrt{2N}\,M_P\,\|A^{-1}\|_2\,\|C^{-1}\|_2}>0.
}\tag{6}
\]

**Proof.** For any \(c\ne0\),
\[
 \|v(c)\|_2^2=\tfrac12\bigl(\|c\|_2^4+\sum_a|c_a|^4\bigr)
 \ge \tfrac12\|c\|_2^4.
\]
Thus the vector of all \(2\times2\) minors of the \(N\times3\) matrix \(Z_J(c)\) has norm at least \(s\|c\|_2^2/\sqrt2\). By Cauchy–Binet, the squared norm of that vector is
\(\sum_{i<j}\sigma_i(Z_J)^2\sigma_j(Z_J)^2\). Eckart–Young and the elementary inequality
\(\sum_{i<j}\sigma_i^2\sigma_j^2\le\|Z_J\|_F^2\operatorname{dist}_F(Z_J,\operatorname{rank}\le1)^2\)
then imply
\[
 \operatorname{dist}_F(Z_J(c),\operatorname{rank}\le1)
 \ge\frac{s}{\sqrt2M_P}\|c\|_2,
\]
since \(\|Z_J(c)\|_F\le M_P\|c\|_2\).

Given any \(L,D,E\), rescale \(L\mapsto tL\), \(D\mapsto D/t\) so that \(c_i=L_{ii}^{-1}\) satisfies \(\|c\|_2=1\), without changing their product. Write \(M=LADBEC\). The three selected columns of \(Z_M(c)\) equal those of \(de^T\) and hence are rank one. Moreover,
\[
 Z_F(c)-Z_M(c)
 =\bigl(A^{-1}\operatorname{diag}(c)(F-M)C^{-1}\bigr)\oslash B.
\]
Its Frobenius norm is bounded above by
\(\|A^{-1}\|_2\|C^{-1}\|_2\|F-M\|_F/b_*\), which is at most
\(\sqrt N\|A^{-1}\|_2\|C^{-1}\|_2\|F-M\|_2/b_*\). Combine these inequalities to get (6). \(\square\)

The constant in (6) depends on the fixed stages and may be tiny; **this is not a uniform-in-\(N\) FFT lower bound**. The floating-point diagnostic `NUMERIC_RESULTS.json` merely illustrates (6), not interval-certified decimal lower bounds.

## 4. Exceptional-locus separation for genuine four-Green networks

We supply **actual Green branch parameters** at \(N=3,4\) in `CERT_N3.json`, `CERT_N4.json`. Every branch is reconstructed in `verify.py` using its weighted-cycle finite geometric sum; the independent `independent_sympy.py` reconstructs from the sparse inverse, then derives quadratic coefficients by polarization. All calculations in the first certificate are over \(\mathbb F_{97}\), with Fourier roots \(\bar\omega_3=35\) and \(\bar\omega_4=22\).

| Length | \(\det[T_1,T_2]\pmod{97}\) | Size and rank of \(\mathcal Q_J\) | Selected maximal minor | \(f'(1)\) |
|---:|---:|---:|---:|---:|
| 3 | 0 | \(9\times6\), rank 6 | 18 mod 97 | 68 mod 97 |
| 4 | 0 | \(18\times10\), rank 10 | 66 mod 97 | 65 mod 97 |

Thus **the previous one-commutator determinant is silent**, but the new lift rules out every invertible diagonal gauge in these finite-field cases.

We can prove a **characteristic-zero existence result**, not merely extrapolate these modular examples. Keep each integer Green parameter from the JSON files fixed. In the **first Green branch of the second aggregate stage** \(B=G_3+G_4\), multiply only its first output column by a free parameter \(t\). Thus
\[
 B(t)=B(1)+(t-1)G_3e_0e_0^T.
\tag{7}
\]
This stays in the independently monomial-gauged Green branch family for \(t\ne0\). In the two-stage case \(C=I\), the old matrices are
\[
 T_j(t)=A\operatorname{diag}(b_0(t)/b_j)A^{-1}\Delta^j,
 \quad \Delta=\operatorname{diag}(1,\omega,\ldots,\omega^{N-1}),\ j=1,2.
\]
Hence \(f(t)=\det[T_1(t),T_2(t)]\) is a polynomial over the cyclotomic field \(\mathbb Q(\zeta_N)\), of degree at most \(2N\).

Mod 97, the computed polynomials (coefficients ascending in \(t\)) are:

- \(N=3\): `[33, 8, 31, 37, 67, 4, 14]`, with \(f(1)=0\), \(f'(1)=68\ne0\).
- \(N=4\): `[10, 40, 72, 60, 1, 29, 27, 56, 93]`, with \(f(1)=0\), \(f'(1)=65\ne0\).

**Theorem C (exceptional complex incompatibility).** For each \(N=3,4\), there is a choice of **algebraic complex** Green-gauge parameter \(t=\alpha_N\ne0\), with all stages admissible, such that
\[
 \det[T_1(\alpha_N),T_2(\alpha_N)]=0,
 \qquad \operatorname{rank}\mathcal Q_J(\alpha_N)=\binom{N+1}{2}.
\]
In particular, the commutator can be singular over \(\mathbb C\) while the quadratic lift still proves **no exact Fourier factorization for any remaining diagonal gauges**.

**Proof.** Since \(97\equiv1\pmod N\), reduction \(\mathbb Z[\zeta_N]\to\mathbb F_{97}\) sending \(\zeta_N\) to the recorded primitive root defines a prime above 97. The Green denominator determinants, \(\det A\), \(\det B\), the needed entries of \(b_0,b_1,b_2\), and the displayed \(\mathcal Q_J\) maximal minor are all units modulo this prime at \(t=1\), as verified independently. The reduced polynomial \(\bar f\) has a **simple** root at \(t=1\). Hensel's lemma therefore gives a root \(\alpha\equiv1\pmod{97}\) in the local completion of \(\mathbb Q(\zeta_N)\). This root is algebraic over the cyclotomic number field because it satisfies nonzero \(f\), and every previously nonvanishing regular rational function stays nonzero at \(\alpha\). Embed this finite algebraic extension into \(\mathbb C\), extending the desired standard complex embedding of \(\zeta_N\). The algebraic equalities and inequalities persist. \(\square\)

This is **not** a proof that arbitrary four-Green parameters fail: the examples describe special **incompatible** exceptional parameter choices, not all such choices. `hensel_lift.py` additionally verifies the root modulo \(97^2,97^3,97^4\), but Hensel's lemma, not a finite number of digits, gives the characteristic-zero conclusion.

## 5. What was checked, and what remains open

- `verify.py`: reconstructions from cycle data, \(2\times2\) minor coefficient identity on 9 test vectors for each \(N\), exact ranks, determinant subcertificates, polynomial interpolation and independent test points, and **positive factorization controls** with a nontrivial null moment.
- `independent_sympy.py`: independent Green reconstruction by sparse inversion, quadratic coefficient construction by polarization, identical maximal minors 18 and 66 mod 97.
- `hensel_lift.py`: lifts roots and Fourier primitive roots consistently through modulus \(97^4\).
- `numeric_gap.py`: two sampled complex instances of Theorem B and 30 gauge tests per size (numerical diagnostics only).

The certificates **do not establish** a successful exact \(O(N)\) FFT for arbitrary inputs or a lower bound against all such algorithms. Forming the dense quadratic matrix and checking its rank are offline synthesis costs and do not make a faster transform.

## 6. Novelty boundary

The following are prior art, not original theoretical primitives: Segre rank-one varieties, symmetric-square/Veronese lifting of quadratic equations, linear-algebra rejection by full column rank, Shemesh-type common-eigenvector compatibility, and Hensel's lemma. Earlier project Phase 18 also used a **different** quadratic polynomial lift (176 equations in 184 variables) for rank-one separated-generator stages. We did not relabel that older system as the new certificate.

The present *particular* three-column Fourier–Green coefficient construction, stronger singular-commutator examples, characteristic-zero lift, and all-gauge bound are **new relative to the research checkpoints inspected**. Publication-level priority/novelty is **not established**, particularly in light of Johnston–Lovitz–Vijayaraghavan (FOCS 2023) and Dastidar–Weicht–Wein (2025), who study related rank-one-subspace symmetric-tensor algorithms.

## 7. Constructive next gate

For each all-length candidate wiring, first require
\[
\operatorname{rank}\mathcal Q_J<\binom{N+1}{2}.
\]
Then compute \(\ker\mathcal Q_J\) and determine whether it contains a **decomposable** vector \(v(c)\) with \(c\in(K^*)^N\). Finally enforce the remaining Fourier columns and all nonzero gauge conditions. Rank deficiency alone is not a construction. An actual breakthrough requires a uniform family of exact phase-correct Green coefficients/cycles with **fully charged** preprocessing and \(o(N\log N)\) arithmetic cost, preferably \(O(N)\).
