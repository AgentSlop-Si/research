# A nonvanishing phase eliminant for exact finite field chirp recognition

Working manuscript • 10 October 2026 • Consolidation of the accepted common-phase eliminant and recognizer proofs

## Abstract

We consider complete raw vectors over a supplied prime field that become a short sum of grid exponentials after multiplication by one unknown quadratic phase. A centered Toeplitz determinant eliminates this phase. At any permitted nonzero center its constant coefficient is nonzero, its degree is at most \(\binom{r+2}{3}\), and every leading principal minor is a unit in the relevant truncated polynomial ring. These properties make the eliminant usable without a generic-position assumption. A deterministic recognizer enumerates its possible phases and verifies every surviving representation against the entire input. For dyadic length \(N\), cap \(1\le r\le\lfloor N/3\rfloor\), and a supplied exact-order root in \(\mathbb F_p\), every complete recognition attempt uses
\[
O\!\left(Nr^3\log(r+2)+r^{2+3\log_2 3}\right)
\]
field additions and multiplications, \(O(1+r^4)\) separately charged scalar inversions, and \(O(N+r^4)\) field elements of storage. The arithmetic bound includes rejected candidates, final rejection, and all Fourier values on acceptance. We give the full decision contract, an all-length variant, and separate charges for a sparse-first attempt and for applying an associated operator to fresh vectors. The recovery, Toeplitz, and Fourier kernels are classical. Historical priority of this particular eliminant and decision composition remains unresolved.

## 1 Scope and notation

Let \(N\ge3\), let \(p\) be a supplied certified prime with \(N\mid p-1\), and let \(\omega\in\mathbb F_p\) have exact order \(N\). The data are the complete vector \(x=(x_0,\ldots,x_{N-1})\in\mathbb F_p^N\), in canonical residue encoding, and an integer cap \(1\le r\le\lfloor N/3\rfloor\). No phase, frequency support, recurrence, or coefficient decomposition is supplied.

Define \(\mathcal C_r\) by the existence of a representation
\[
x_j=\omega^{a j^2}\sum_{\ell=1}^{s}\gamma_\ell\omega^{u_\ell j},
\qquad 0\le j<N,\qquad 0\le s\le r,                 \tag{1}
\]
where the \(u_\ell\) are distinct modulo \(N\) and each listed \(\gamma_\ell\ne0\). The empty sum represents zero. Put
\[
g=\gcd(2,N),\quad L=N/g,\quad
D=\binom{r+2}{3},\quad C_* =\min(D,L),\quad \kappa=\log_2 3.       \tag{2}
\]
We search \(0\le a<L\). For even \(N\), replacing \(a\) by \(a+N/2\) multiplies the chirp by \(\omega^{(N/2)j}\), because \(j^2-j\) is even. That factor is absorbed into every frequency. This proves completeness of the canonical phase range, without asserting uniqueness within it. At a fixed phase, Fourier coefficients are unique; the returned phase need not minimize \(s\) over all phases.

The Fourier convention throughout is positive-sign and unnormalized:
\[
(F_\omega x)_k=\sum_{j=0}^{N-1}x_j\omega^{kj}.             \tag{3}
\]
All formulas involving \(1/2\) in an exponent mean exact integer division before reduction modulo the relevant order. They never require dividing by two in the field.

This is an exact decision theorem. Its inputs are not noisy samples, floating-point data, compressed descriptions, or oracle-access signals. Materializing an alternative input representation has its own cost. The position of this result in a research catalogue does not restrict the variable cap \(r\) to three.

## 2 Main theorems

**Theorem 1  Uniformly nonzero phase eliminant.** Suppose \(x\ne0\). Every member of \(\mathcal C_r\) has a nonzero coordinate \(x_c\) with \(r\le c\le N-r-1\). For any such center, define
\[
f(d)=d(d-1)/2,\qquad
A(z)_{ij}=x_{c+i-j}z^{f(i-j)},\quad 0\le i,j\le r,
\qquad E(z)=\det A(z).                                  \tag{4}
\]
Then:

1. \(E(0)=x_c^{r+1}\ne0\), so \(E\) is never the zero polynomial.
2. \(\deg E\le D\); equality is not asserted.
3. The leading principal minor of order \(k\) has constant coefficient \(x_c^k\), for \(1\le k\le r+1\).
4. Every phase in a representation (1) satisfies \(E(\omega^{-2a})=0\).
5. There are at most \(C_*\) possible phases among \(0\le a<L\).

The determinant and unit-minor conclusions hold for every field and every indicated nonzero center. The recognizer below uses the more specific supplied-prime-field contract of Section 1.

**Theorem 2  Exact dyadic recognition with dense accepted output.** Under Section 1, additionally suppose \(N\) is a power of two. A deterministic algorithm accepts exactly \(\mathcal C_r\), returning a verified representation (1) and all \(N\) values (3). Every complete attempt, including rejection, has the field-arithmetic and storage bounds stated in the abstract. More precisely, with
\[
T(r)=r^2(D+1)^\kappa,
\]
its addition and multiplication count is \(O(H(N,r))\), where
\[
\begin{split}
H(N,r)={}&T(r)+D+N\log(\min(D+1,L)+2)\\
 &+C_*\,[N\log(r+2)+r^2]+Nr+N.                         \tag{5}
\end{split}
\]
It uses \(O(1+C_*r)\) scalar field inversions and \(O(N+r(D+1))\) field elements. Field certification, integer gcd and modular-inverse work, and conversion to a particular word or bit model are charged separately in Appendix A.

**Theorem 3  All-length recognition.** Without the dyadic assumption, the same decision and accepted-output contract is available with
\[
\begin{split}
B(N,r)={}&T(r)+N(D+1)\\
 &+C_*\,[N(r+1)^{\kappa-1}+r^3]+Nr+N                  \tag{6}
\end{split}
\]
inside the \(O(\cdot)\) arithmetic bound. In particular,
\[
B(N,r)=O\!\left(Nr^{2+\kappa}+r^{2+3\kappa}\right).
\]
The inversion and storage bounds remain \(O(1+r^4)\) and \(O(N+r^4)\). This all-length statement does not assume additional Fourier roots, an extension field, or an all-length \(O(N\log N)\) backend.

These theorems consolidate the previously proved contracts [P1–P4]. Their proof source was independently reviewed in [R1]; that review is a local mathematical audit, rather than journal peer review or production certification. No worldwide originality, optimality, numerical stability, or unrestricted Fourier improvement is asserted here.

## 3 Proof of the eliminant theorem

### 3.1 A usable center always exists on members

Write a nonzero dechirped member as \(y_j=\sum_{\ell=1}^s\gamma_\ell\lambda_\ell^j\), where \(\lambda_\ell=\omega^{u_\ell}\), \(1\le s\le r\), and the nodes are nonzero and distinct. If \(s\) consecutive values starting at \(j_0\) vanish, then
\[
[\lambda_\ell^i]_{0\le i<s,\,1\le\ell\le s}
\,(\gamma_\ell\lambda_\ell^{j_0})_\ell=0.
\]
The square Vandermonde is invertible, contradicting nonzero amplitudes. Multiplying by a nonzero chirp preserves zero locations. The interval \([r,N-r-1]\) has \(N-2r\ge r\) entries, so it cannot be all zero on a nonzero member. A nonzero raw input with no such center can therefore be rejected immediately, after the charged scan.

### 3.2 Constant coefficient and degree

For integer \(d\), \(f(d)\ge0\), with equality exactly at \(d=0,1\). Thus \(A(0)\) is lower bidiagonal with diagonal \(x_c\). This proves both its determinant constant and the assertion about every leading principal minor.

For a determinant term corresponding to a permutation \(\sigma\) of \(\{0,\ldots,r\}\), its exponent is
\[
\sum_{i=0}^{r}f(i-\sigma(i))
=\sum_{i=0}^{r}i^2-\sum_{i=0}^{r}i\sigma(i).
\]
The rearrangement inequality puts its maximum at \(\sigma(i)=r-i\). The maximum equals
\[
2\sum_{i=0}^{r}i^2-r\sum_{i=0}^{r}i
=\frac{r(r+1)(r+2)}6=D.
\]
Cancellation can reduce the degree, but cannot increase it. The same bound holds for each square minor: extend its partial row–column matching to a full permutation, whose extra exponents are nonnegative. This argument is independent of field characteristic and does not need \(D<p\).

### 3.3 Every true phase is a root

For a true phase \(a\), put \(y_j=\omega^{-aj^2}x_j\). At \(z=\omega^{-2a}\), with \(d=i-j\),
\[
A(z)_{ij}
=y_{c+i-j}\,\omega^{ac^2+a(2c+1)(i-j)}.              \tag{7}
\]
The factors outside \(y_{c+i-j}\) separate into nonzero row and column scalings. Moreover
\[
y_{c+i-j}=\sum_{\ell=1}^{s}
(\gamma_\ell\lambda_\ell^c)\lambda_\ell^i\lambda_\ell^{-j}
\]
has rank at most \(s\le r\). Consequently its determinant of order \(r+1\), and hence \(E(\omega^{-2a})\), vanishes.

The values \(\omega^{-2a}\), \(0\le a<L\), are distinct. A nonzero polynomial of degree at most \(D\) has at most \(D\) roots, proving the final assertion. This root count always concerns \(E\) itself. If reducing \(E\) modulo \(z^L-1\) gives zero, then \(D\ge L\), all \(L\) phases are retained, and \(C_*=L\). No degree bound is applied to a zero reduced polynomial. This proves Theorem 1.

## 4 Constructing the determinant without pivot failures

Work in \(R=\mathbb F_p[z]/(z^{D+1})\). Put \(a_d=x_{c+d}z^{f(d)}\) and \(T_k=[a_{i-j}]_{i,j=1}^k\), with \(\det T_0=1\). Theorem 1 makes every \(\det T_k\) a unit of \(R\). The following is a nonsymmetric Levinson-type recurrence, a classical structured-linear-algebra mechanism [C3]. Its unit guarantee here is supplied by the centered polynomial normalization, not by positivity or generic nonsingularity.

Let \(u^{(k)},v^{(k)}\) have indices \(0,\ldots,k\), initial coordinate one, and satisfy
\[
\sum_{j=0}^{k}a_{i-j}u_j^{(k)}=0,\qquad
\sum_{j=0}^{k}a_{j-i}v_j^{(k)}=0,\qquad 1\le i\le k.
\]
The invertibility of \(T_k\) gives these vectors uniquely. Schur complements give
\[
e_k=\sum_{j=0}^{k}a_{-j}u_j^{(k)}
=\sum_{j=0}^{k}a_jv_j^{(k)}
=\frac{\det T_{k+1}}{\det T_k},\qquad e_k(0)=x_c.       \tag{8}
\]
Initialize \(u=v=(1)\), \(e=a_0\), and \(\delta=a_0\). For \(k=1,\ldots,r\), use the previous length-\(k\) vectors to form
\[
A_k=a_k+\sum_{j=1}^{k-1}a_{k-j}u_j,\qquad
B_k=a_{-k}+\sum_{j=1}^{k-1}a_{j-k}v_j,
\qquad \alpha_k=-A_k/e,\quad\beta_k=-B_k/e.
\]
Update simultaneously
\[
u'_j=u_j+\alpha_kv_{k-j},\qquad
v'_j=v_j+\beta_ku_{k-j}\quad(1\le j<k),
\]
set \(u'_0=v'_0=1\), \(u'_k=\alpha_k\), \(v'_k=\beta_k\), and set
\[
e'=e+\alpha_kB_k=e-A_kB_k/e,\qquad \delta'=\delta e'.  \tag{9}
\]
Reversing the previous \(v\)-equations shows that their contribution in the \(u'\)-equations is zero for the first \(k-1\) rows and \(e\) in the last row. The choice of \(\alpha_k\) cancels that last residual. The transpose argument proves the \(v'\)-equations. Expanding the definition of \(e'\) yields (9), so (8) is preserved. The final product is \(\det T_{r+1}=E\) modulo \(z^{D+1}\), which is its complete polynomial because of the degree bound.

Every series inverse uses the same initial scalar \(x_c^{-1}\). Newton doubling
\[
g_{\rm new}=g(2-eg)
\]
squares the residual \(1-eg\); it does not divide by two. With truncated Karatsuba multiplication \(M(m)=O(m^\kappa)\), one inverse costs \(O(M(D+1))\). There are \(O(r^2)\) ring arithmetic operations and \(r\) reciprocals, giving \(O(T(r))\) field additions and multiplications, one scalar inversion, and \(O(r(D+1))\) live coefficients. Coefficient initialization, truncation, and writes fit these bounds. Neither polynomial factoring nor interpolation at \(D+1\) field points is required. The full ring recurrence and accounting are also recorded in [P2].

## 5 Exact sparse recovery at a fixed phase

Let \(\mathcal S_t\) be the family \(y_j=\sum_{\ell=1}^{s}\gamma_\ell\omega^{u_\ell j}\), \(s\le t\). For dyadic \(N\) and \(1\le t\le N/2\), there is an exact test \(D_t\) costing
\[
O(A(N,t)),\qquad A(N,t)=N\log(t+2)+t^2,              \tag{10}
\]
with \(O(t)\) scalar inversions and \(O(N)\) field elements. This is the classical Prony and Berlekamp–Massey recovery mechanism [C1,C2], with a paid full-grid search and full-input check [P3].

Run the quadratic Berlekamp–Massey algorithm on the first \(2t\) samples. Its minimal recurrence order is nondecreasing as the prefix grows, so an order above \(t\) permits early rejection of this phase. Otherwise let its final order be \(s\), with connection polynomial
\[
C(z)=1+C_1z+\cdots+C_sz^s.
\]
For \(s=0\), accept only after checking that every raw coordinate is zero. For \(s>0\), require degree exactly \(s\). Evaluate \(C\) on all \(\omega^v\); require exactly \(s\) distinct grid roots. For each root \(\rho_\ell=\omega^{v_\ell}\), put \(\lambda_\ell=\rho_\ell^{-1}=\omega^{-v_\ell}\). The negation of the root index is essential.

Define
\[
Q(z)=C(z)\sum_{j=0}^{s-1}y_jz^j\pmod{z^s},\qquad
\gamma_\ell=-\lambda_\ell\frac{Q(\rho_\ell)}{C'(\rho_\ell)}.  \tag{11}
\]
Require nonzero denominators and listed amplitudes. Finally synthesize \(\sum_\ell\gamma_\ell\lambda_\ell^j\) at all \(N\) coordinates and compare with the entire \(y\). Acceptance requires every comparison to pass.

For a true \(s\)-term sum, its leading moment Hankel block is
\[
[y_{i+j}]_{0\le i,j<s}=V\operatorname{diag}(\gamma_\ell)V^{\mathsf T},
\quad V_{i\ell}=\lambda_\ell^i,
\]
and is nonsingular. The first \(2t\ge2s\) samples therefore determine the minimal connection polynomial \(\prod_\ell(1-\lambda_\ell z)\). Formula (11) follows by evaluating the numerator in
\(\sum_jy_jz^j=\sum_\ell\gamma_\ell/(1-\lambda_\ell z)\)
at each reciprocal root. Thus every member passes. Conversely, the final full comparison proves membership for every accepted raw input, regardless of its prefix.

For completeness, the Fourier pruning cost used twice here has an elementary tree proof. With \(h\) supported inputs, input-parity recursion has at depth \(d\) at most \(\min(2^d,h)\) active subproblems, each of size \(N/2^d\). Summing combine work gives \(O(N[1+\log(h+1)])\); all-zero subproblems are omitted. Depth-first evaluation needs \(O(N)\) storage. Root-table access and bookkeeping are included. This is classical FFT pruning [C4], and is used only at dyadic lengths. The recurrence and formula (11) cost \(O(t^2)\); discrepancy and derivative inverses require \(O(t)\) scalar inversions. The result applies to rejection as well as acceptance.

## 6 Phase search and the dyadic decision

After validating the contract and handling zero, scan the interior interval. If no nonzero center exists, reject. Otherwise construct \(E\) as in Section 4. Put \(\eta=\omega^{-2}\), of dyadic order \(L=N/2\). Accumulate coefficients by their exponents modulo \(L\), obtaining \(\overline E=E\bmod(z^L-1)\) in \(O(D+L)\) work. Its support is at most \(\min(D+1,L)\). A pruned length-\(L\) transform at \(\eta\) gives all \(E(\eta^a)\) within
\[
O\!\left(N\log(\min(D+1,L)+2)\right)
\]
work. Retain every zero, including all phases if \(\overline E=0\).

For each retained \(a\), construct all \(y_j=\omega^{-aj^2}x_j\) in \(O(N)\) work and run \(D_r\). Discard a failed phase and continue. The first successful phase gives a complete representation. If all retained phases fail, reject. Candidates use one reusable vector and workspace.

Every true phase survives by Theorem 1 and passes Section 5, proving completeness. An accepted sparse decomposition, followed by multiplying back the nonzero chirp, proves soundness at every raw coordinate. Therefore exhaustively failed candidates imply nonmembership. A single failed candidate does not.

There are at most \(C_*\) candidates, each costing \(O(N\log(r+2)+r^2)\), including dechirping. Adding determinant construction, phase scan, validation, and the output procedure below proves (5). Since \(D=O(r^3)\), \(C_*\le D\), and \(C_*r^2=O(r^5)\) is absorbed by \(r^{2+3\kappa}\), (5) gives Theorem 2. Its scalar inversions are one for construction and \(O(r)\) per candidate; sequential workspaces give the stated storage bound.

## 7 The all length variant

At general \(N\), evaluate \(E\) by Horner on all \(L\) phase points, at cost \(O(N(D+1))\). For a candidate phase, compute the rank \(s\) of \([y_{i+j}]_{0\le i,j<r}\). If \(s=0\), require the entire vector to vanish. Otherwise require the leading \(s\)-square block to be nonsingular, solve
\[
\sum_{j=0}^{s-1}p_jy_{i+j}=-y_{i+s}\quad(0\le i<s),\qquad p_s=1,
\]
and require exactly \(s\) distinct roots of \(p(z)=\sum_{j=0}^sp_jz^j\) on the supplied grid. Check every residual \(\sum_{j=0}^sp_jy_{k+j}\), \(0\le k<N-s\), and solve the node Vandermonde system for the first \(s\) samples. Remove any zero amplitudes before listing the representation.

A true member has rank \(s\) and nonsingular leading block by the Vandermonde factorization. Conversely, a reconstructed exponential sum matches the first \(s\) samples and obeys the checked monic recurrence. Induction gives equality at all later coordinates. Dense elimination and amplitude recovery cost \(O(r^3)\) and \(O(r)\) scalar inversions per candidate.

The grid scan and full residual test use blocked ordinary convolution. For \(b=s+1\), a grid block \(k=K+a\), \(0\le a<b\), satisfies
\[
f(\omega^{K+a})=\omega^{\binom a2}
\sum_{j=0}^{s}\left[f_j\omega^{Kj+\binom{j+1}2}\right]
\omega^{-\binom{a-j}2}.                               \tag{12}
\]
This follows from the integer identity \(aj=\binom a2+\binom{j+1}2-\binom{a-j}2\). Each block is a convolution of arrays of length \(O(b)\). Karatsuba gives \(O(b^\kappa)\) work per block, including scaling and the final partial block. Across \(\lceil N/b\rceil\) blocks the cost is \(O(Nb^{\kappa-1})\). Convolving \(y\) in length-\(b\) chunks with \([p_s,\ldots,p_0]\), then overlap-adding, checks every residual at the same cost. This is the established blocked convolution argument [P4], using a classical chirp-convolution identity; it requires no extra roots. Substitution into the candidate ledger proves (6) and Theorem 3.

## 8 Dense Fourier output on acceptance

Given a verified representation, define
\[
G_a(k)=\sum_{j=0}^{N-1}\omega^{aj^2+kj},\qquad
(F_\omega x)_k=\sum_{\ell=1}^s\gamma_\ell G_a(k+u_\ell).       \tag{13}
\]
The shift is \(k+u_\ell\), consistent with (3). We give the complete Gauss-row reduction, including even lengths and nonunit phases, so this output claim does not depend on an unavailable historical byte string.

Put \(d=\gcd(a,N)\), \(m=N/d\), \(A=a/d\), and \(\xi=\omega^d\). For \(a=0\), use \(d=N,m=1,A=0\). Splitting \(j=u+vm\) shows that \(G_a(k)=0\) unless \(d\mid k\). For \(k=dw\),
\[
G_a(dw)=dT(w),\qquad T(w)=\sum_{u=0}^{m-1}\xi^{Au^2+wu}.    \tag{14}
\]
For \(m=1\), this is the \(N\)-spike. For odd \(m>1\), compute \(T(0)\) directly in \(O(m)\) work and use integer completion of squares:
\[
T(w)=T(0)\xi^{-w^2(4A)^{-1}\bmod m}.                    \tag{15}
\]
Here the inverse is an integer modular inverse, charged separately.

For even \(m=2q\), \(A\) is odd. Translating the summation index by \(q\) multiplies each term by \((-1)^{Aq+w}\), so \(T(w)=0\) unless \(w\equiv q\pmod2\). Set \(w_0=q\bmod2\), compute \(T(w_0)\) by one pass, and, for permitted \(w\), choose
\[
u=\frac{w-w_0}{2}A^{-1}\pmod q.
\]
For \(q=1\), choose \(u=0\), without an inverse modulo one. Translation then gives
\[
T(w)=T(w_0)\xi^{-Au^2-w_0u}.                            \tag{16}
\]
Changing \(u\) by \(q\) changes the exponent by a multiple of \(2q\), since \(Aq+w_0\) is even. All divisions by two above have even integer numerators.

The complete row requires \(O(N)\) field work and storage, plus the indicated integer work. Equation (13) then writes all outputs in \(O(Ns+N)\), which is covered by \(Nr+N\) in (5)–(6). For a sparse phase-zero certificate, one may instead initialize \(N\) zeros and write \(N\gamma_\ell\) at \(k=-u_\ell\), costing \(O(N+s)\).

## 9 Sparse first recognition and operator applications

At dyadic \(N\), one may first run \(D_t\) on the raw \(x\), with \(1\le t\le N/2\). This dispatcher recognizes \(\mathcal S_t\cup\mathcal C_r\). On sparse acceptance, its cost is \(O(N+A(N,t))\), and dense Fourier output uses the scatter formula. After sparse rejection, it must still decide \(\mathcal C_r\); its cost is \(O(N+A(N,t)+K(N,r))\), where one may choose \(K=\min(B,H)\) using fixed parameter envelopes because both methods decide the same family. All scalar inversions from both attempted branches are added.

At \(t=r\), \(\mathcal S_r\subseteq\mathcal C_r\); thus the dispatcher still decides exactly \(\mathcal C_r\), and the paid first attempt is absorbed in the common-chirp envelope while preserving the cheap sparse-success path. For unequal caps it recognizes the union, and \(A(N,t)\) cannot automatically be absorbed. These components do not give an \(O(\min(A,B))\) bound for every common-chirp input.

Transforming the recognized input is separate from applying an operator to a fresh vector. For supplied diagonal vectors \(\alpha,\beta\), define
\[
M_x=\operatorname{diag}(\alpha)F_\omega\operatorname{diag}(x)
F_\omega\operatorname{diag}(\beta).
\]
For a phase-zero certificate, character orthogonality gives
\[
(M_xv)_i=N\alpha_i\sum_\ell\gamma_\ell
\beta_{-i-u_\ell}v_{-i-u_\ell}.                         \tag{17}
\]
Each fresh \(v\) costs \(O(N(s+1))\), including reading and writing; \(J\) vectors cost \(O(JN(s+1))\) after recognition. A general common-chirp certificate instead gives
\[
(M_xv)_i=\alpha_i\sum_m\beta_mv_m(F_\omega x)_{i+m},
\]
which is generally dense. The sparse-shift bound does not follow.

Indeed, for odd \(N\) and a unit phase \(a\), (15) makes \(G_a(i+m)\) diagonally equivalent to a Fourier matrix with primitive root \(\omega^{-(2a)^{-1}}\). Its common Gauss factor is nonzero: otherwise (15) would make the invertible Fourier transform of a nonzero chirp zero. With nonzero external diagonals, a uniform linear-time fresh-vector application theorem for these one-chirp operators would imply a linear-time arbitrary-vector Fourier algorithm in that domain. This is an implication explaining the contract boundary, not a lower bound against such algorithms.

## 10 Rejection fallback and scope limits

A completed rejection proves nonmembership in the stated family and supplies no Fourier output for that rejected vector. It also promises no succinct negative witness. The deterministic decision can be checked by replaying the full recognizer with its paid ledger. A failed coordinate or root condition only refutes the corresponding candidate.

A wrapper computing the transform on every input must add a backend after rejection. Dyadic radix-two evaluation costs \(O(N\log N)\); all-length convolution from (12) gives \(O(N^\kappa)\) in the same field. A different all-length backend must have its own established field, root, preparation, and output contract. Total cost includes the entire failed recognition attempt. A recognition attempt stopped at a budget limit gives UNKNOWN membership, never REJECT.

For \(r=o((\log N/\log\log N)^{1/3})\), the dyadic addition and multiplication envelope is \(o(N\log N)\). Optional certification, scalar inversions, and integer work must also meet the intended total-model bound before claiming a total-cost improvement. This structured path does not give a sub-\(N\log N\) arbitrary-input transform. Storage is linear in \(N\) only under a further condition such as \(r^4=O(N)\). No tolerance, perturbation radius, or floating-point error guarantee is part of the exact equality predicate.

## 11 Related work and unresolved comparison

Prony recovery from moment-type samples and Berlekamp–Massey recurrence synthesis are classical [C1,C2]. The nonsymmetric Toeplitz predictor mechanism [C3] and Fourier pruning [C4] are also established. This manuscript does not claim those methods as new. Its mathematical subject is the particular center-normalized polynomial, its uniform unit guarantee, and the complete finite-field decision and cost contract.

Shared-parameter elimination by imposing a low-rank Hankel condition already appears in the homoscedastic-mixture literature. Agostini, Améndola, and Ranestad [C5], Section 4.3, equations (90)–(92) in the cited preprint, describe a determinant equation for common variance followed by recovery. Wu and Yang [C6], Section 4.2, give a statistical moment procedure with almost-sure qualifications. These antecedents establish the general elimination-and-recovery framework. They are not silently reinterpreted as every-input decisions on raw \(\mathbb F_p\) vectors.

Three important comparisons remain incomplete, as documented in [R2]. Derin [C7] is presently supported by an author abstract and metadata; its full mathematical text has not been inspected. Applebaum, Howard, Searle, and Calderbank [C8] has indexed primary passages concerning complex chirp recovery, but complete-PDF inspection remains outstanding. Lindsay [C9], Theorem 5B, is presently an attribution read in [C5], not a theorem independently inspected in its original source. The accompanying concordance records these access limits and the different input interfaces. None is marked cleared, and none is asserted to contain the present exact theorem.

Priority of the precise eliminant and composition therefore remains unresolved. This working manuscript can state its proved contract without turning an incomplete comparison into an originality claim.

## Appendix A Exact rejection and cost contract

### A1 Input and terminal states

Required data are the complete canonical-residue vector \(x\in\mathbb F_p^N\), integers \(N\ge3\) and \(1\le r\le\lfloor N/3\rfloor\), a supplied certified prime \(p\) with \(N\mid p-1\), and a supplied element \(\omega\) of exact order \(N\). The dyadic implementation additionally requires \(N\) to be a power of two. A separate sparse-first cap, if used, satisfies \(1\le t\le N/2\). Missing field/root discovery is not an assumed free subroutine.

| State | Exact meaning | Output obligation |
|---|---|---|
| ACCEPT | The full input has a representation within the applicable cap and family | Field/root identifiers, canonical phase, distinct frequency indices, nonzero amplitudes, branch label if dispatching, and all \(N\) positive-sign unnormalized DFT values |
| REJECT | All necessary complete paths establish nonmembership in \(\mathcal C_r\), or in \(\mathcal S_t\cup\mathcal C_r\) when that union is the chosen contract | Decision only; no arbitrary-input DFT and no promised succinct negative witness |
| INVALID_CONTRACT | Size/cap/encoding assumptions fail, the established prime-field premise is absent, or the supplied root fails validation | Identification of the invalid condition; no assertion of family nonmembership over some other field or grid |
| UNKNOWN | An explicitly budget-limited wrapper stopped before membership was decided | No negative membership claim; a separately paid DFT backend may still run |

A field-certificate verification whose validity has not been established cannot be treated as a successful field premise. The stated complete decision theorem concerns valid-contract inputs; budget or resource failure is not mathematical rejection.

Zero is accepted with an empty representation only after the complete raw-vector zero scan. Its dense output consists of \(N\) zeros. The accepted representation is not certified to use the globally smallest number of terms across phases.

### A2 Validation and shared preparation

1. Read the declared length, caps, field/root data, and all raw coefficients. Check the vector length and canonical residue conditions. Reading \(N\) field elements is charged.
2. The theorem accepts an established prime-field premise. If primality or an untrusted primality certificate is to be verified, add the actual certification cost \(C_{\rm field}(p)\) and its storage. Neither prime search nor primitive-root discovery is included.
3. Without factoring \(N\), compute \(1,\omega,\ldots,\omega^N\). Require \(\omega\ne0\), \(\omega^N=1\), and \(\omega^j\ne1\) for \(1\le j<N\). This proves exact order and supplies the power table. Work, equality checks, and storage are \(O(N)\), including failure paths. An independently valid root certificate can replace the order test; constructing the table remains paid.
4. Use table indices for inverse powers. This step does not spend a scalar inverse on each root or dechirped coordinate.
5. Find the all-zero case and an interior nonzero center. A nonzero vector with no center in \([r,N-r-1]\) is a genuine early rejection by the no-consecutive-zeros proof.

Write \(G=O(N)\) for this shared field work and traffic, excluding optional field certification and the declared integer-arithmetic costs. It is already covered by the final \(+N\) terms of the stand-alone recognizer envelopes. In a dispatcher, charge shared preparation once.

### A3 Every rejection route

| Stage | Failing condition | Scope of the failure | Cost paid before continuing or stopping |
|---|---|---|---|
| Contract validation | Invalid size, cap, residue, field premise, divisibility, or root order | INVALID_CONTRACT | Actual validation and table/read work already performed, plus any certification work |
| Zero handling | A later entry is nonzero after a zero prefix | No zero acceptance; continue appropriate nonzero path | Full scan or subsequent full verification; a zero prefix alone never accepts |
| Center search | Nonzero input has no allowed nonzero center | Final REJECT for \(\mathcal C_r\) | \(O(N)\) scan |
| Phase scan | No root of \(E\) on the canonical phase grid | Final REJECT for \(\mathcal C_r\) | Entire determinant construction and phase scan |
| Dyadic candidate BM | Prefix recurrence order exceeds cap, or final polynomial degree differs from recorded order | Reject this phase only | BM work up to failure, at most \(O(r^2)\) |
| Dyadic candidate roots | Fewer or more than the required distinct grid roots | Reject this phase only | Full necessary root scan within \(O(N\log(r+2))\) |
| Dyadic candidate amplitudes | Zero derivative denominator or zero listed amplitude | Reject this phase only | Polynomial work \(O(r^2)\), with actual scalar inversions charged |
| Dyadic candidate synthesis | Any synthesized coordinate differs from raw dechirped input | Reject this phase only | Full synthesis bound \(O(N\log(r+2))\), and comparisons up to failure |
| All-length prefix | Leading block at the computed positive rank is singular | Reject this phase only | Dense rank and solve budget \(O(r^3)\) |
| All-length roots | Monic recurrence does not have the required number of distinct grid roots | Reject this phase only | Blocked scan \(O(N(r+1)^{\kappa-1})\) |
| All-length residuals | Any of the \(N-s\) recurrence residuals is nonzero | Reject this phase only | Blocked full-residual budget \(O(N(r+1)^{\kappa-1})\) |
| Rank zero | Entire dechirped vector is not zero | Reject this phase only | Full scan \(O(N)\) |
| Candidate exhaustion | Every retained phase failed its complete necessary tests | Final REJECT for \(\mathcal C_r\) | Sum of every attempted phase cost, bounded by \(C_*\) candidate budgets |
| Sparse-first failure | Raw input is not in \(\mathcal S_t\) | Continue the common-chirp branch | Entire first-attempt cost \(A(N,t)\), even if the later branch also rejects |
| Budget exhaustion | An optional time/work cap is reached | UNKNOWN | Actual work already spent; backend cost is additional if requested |

For the all-length test, a successful Vandermonde solve may include zero weights; omit those weights. The checked recurrence and first samples still force full equality. For the dyadic test, the minimal-recurrence recovery explicitly rejects zero amplitudes. These equivalent acceptance mechanisms need not have identical intermediate rejection labels.

A derivative-zero guard is harmless even when the required distinct-root count already makes it impossible on a degree-\(s\) candidate. Failure of a polynomial-ring pivot would indicate a broken implementation or invalid arithmetic, not a legitimate family rejection: the nonzero-center proof guarantees those pivots are units.

### A4 Dyadic cost ledger

Let \(D=\binom{r+2}{3}\), \(L=N/2\), \(C_* =\min(D,L)\), \(\kappa=\log_2 3\), and \(T(r)=r^2(D+1)^\kappa\).

| Component | Additions and multiplications | Scalar inversions | Live field elements |
|---|---:|---:|---:|
| Shared raw reads, root table, zero and center checks | \(O(N)\) | 0 | \(O(N)\) |
| Toeplitz determinant in \(\mathbb F_p[z]/(z^{D+1})\) | \(O(T(r))\) | 1 cached inverse of \(x_c\) | \(O(r(D+1))\) |
| Coefficient reduction modulo \(z^L-1\) | \(O(D+L)\) | 0 | \(O(D+L)\), reusable |
| Phase-grid pruned transform | \(O(N\log(\min(D+1,L)+2))\) | 0 | \(O(N)\) |
| One candidate dechirp, BM, grid roots, amplitudes, and full synthesis | \(O(N\log(r+2)+r^2)\) | \(O(r)\) | \(O(N)\) |
| All candidate attempts | \(O(C_*[N\log(r+2)+r^2])\) | \(O(C_*r)\) | One candidate workspace at a time |
| Accepted Gauss row and all dense outputs | \(O(Ns+N)\subseteq O(Nr+N)\) | No additional field inversions | \(O(N)\) |

The sum is
\[
H=T(r)+D+N\log(\min(D+1,L)+2)
+C_*[N\log(r+2)+r^2]+Nr+N
\]
inside a uniform \(O(H)\) bound. On rejection the final output work is absent, but the same bound applies. Candidate dechirping is absorbed into its \(N\log(r+2)\) term. All equality checks, coefficient initialization, copying, zero-filling, and corresponding index/array traffic are covered at the stated elementary-operation scale.

The total scalar-inversion count is \(O(1+C_*r)\). BM may cache its nonzero discrepancy inverse whenever that discrepancy changes; there are only \(O(r)\) such events in a \(2r\)-sample run. Amplitude denominators add \(O(r)\). The Toeplitz series inverses all start from the same \(x_c^{-1}\); ring inversions are not counted as free scalar operations.

Peak storage is \(O(N+r(D+1))\), not the sum of candidate workspaces. Hence the simplified envelopes are
\[
O(Nr^3\log(r+2)+r^{2+3\kappa}),\quad
O(1+r^4)\text{ inversions},\quad O(N+r^4)\text{ field elements}.
\]

### A5 All length ledger

Replace the dyadic phase scan by \(O(N(D+1))\) Horner work. Replace each sparse candidate test by the dense prefix setup and two blocked kernels described in manuscript Section 7:
\[
O\!\left(N(r+1)^{\kappa-1}+r^3\right),
\quad O(r)\text{ inversions},\quad O(N+r^2)\text{ workspace}.
\]
Thus
\[
B=T(r)+N(D+1)+C_*[N(r+1)^{\kappa-1}+r^3]+Nr+N,
\quad L=N/\gcd(2,N).
\]
The \(O(r^6)\) total dense prefix term is absorbed by \(r^{2+3\kappa}\). The phase term \(Nr^3\) is absorbed by \(Nr^{2+\kappa}\), yielding Theorem 3. All scalar inversions and storage retain their prior bounds. This ledger uses Horner scanning deliberately; it does not require a fast transform at general length.

### A6 Sparse first overhead and optional fallback

Let \(A=N\log(t+2)+t^2\), and use \(K=\min(B,H)\) at dyadic lengths, \(K=B\) otherwise. The minimum is justified only because \(B\) and \(H\) decide the same \(\mathcal C_r\) contract. Equivalent integer size templates can choose between them without a real-logarithm oracle.

| Path | Field arithmetic | Scalar inversions | Storage |
|---|---:|---:|---:|
| Dyadic sparse-first acceptance | \(O(G+A+N)\) | \(O(t)\) | \(O(N)\) |
| Dyadic sparse rejection followed by chirp acceptance or rejection | \(O(G+A+K)\) | \(O(t+1+C_*r)\) | \(O(N+r^4)\) |
| Nondyadic complete decision | \(O(G+B)\) | \(O(1+C_*r)\) | \(O(N+r^4)\) |

For \(t=r\), the first attempt is absorbed in either chirp envelope, yet it is still performed and paid. For \(t\ne r\), retain its explicit charge and the union family \(\mathcal S_t\cup\mathcal C_r\). A failed sparse recognition does not by itself exclude a nonzero common phase.

On final rejection, an arbitrary-input transform wrapper adds all backend preparation, arithmetic, storage, and output work. The available same-field choices proved here are dyadic \(O(N\log N)\) radix-two evaluation or all-length \(O(N^\kappa)\) convolution. A separate backend of cost \(F(N,p)\) gives total \(O(G+A+K+F(N,p))\) when the sparse attempt exists; omit \(A\) otherwise. Peak memory is the maximum of sequential stages only if earlier workspaces are actually released. A backend-sized budget may abort recognition, but then membership remains UNKNOWN.

### A7 Integer word and bit costs

The main theorem counts exact field additions/multiplications and separately lists scalar inversions. The Gauss-row output also performs integer gcd and modular-inverse computations on \(O(\log N)\)-bit integers. Its inverses modulo \(m\) or \(q\) are not field inversions and must be paid separately. Powers such as \(aj^2\), binomial exponents, degree indices, and addresses need properly sized integer arithmetic; table lookups do not make their index computations free.

For a word-RAM interpretation, assume \(\log p=O(\log N)\), sufficiently wide address-capable words, and the stated cost for modular addition, multiplication, and reduction. With word inversion cost \(I_{\rm word}(p)\), a chirp path costs
\[
O(K+(1+C_*r)I_{\rm word}(p)+G_{\rm int}(N)+C_{\rm field}(p)),
\]
plus any preceding \(G+A\) work and \(O(t)\) inversions. The degree \(D=O(N^3)\) and maximum workspace addresses occupy \(O(\log N)\) bits with a suitable constant factor. If modular multiplication is not unit-cost on the target machine, its true cost multiplies the appropriate arithmetic count. For larger \(p\), each field element occupies multiple words.

For a conservative bit conversion, put \(b=\lceil\log_2p\rceil\), let \(M_{\rm mod}(b)\) upper-bound the relevant modular arithmetic cost, and let \(I_{\rm bit}(b)\) be inversion cost. A dispatcher path is bounded by
\[
O\!\left((G+A+K)M_{\rm mod}(b)
 +(t+1+C_*r)I_{\rm bit}(b)
 +G_{\rm index,int}(N)+C_{\rm field}(p)\right),
\]
with absent branches removed and the full actual index-operation total used in \(G_{\rm index,int}\). Include \(\Omega(Nb)\) input and accepted-output traffic. Storage is \(O((N+r^4)b)\) field-data bits, plus indices and certification workspace. This is a parameterized conversion, not an optimized bit-complexity theorem.

No scalar inversion, field certification, input decoding, root discovery, numerical tolerance, or fresh-vector operator application is concealed in the headline field-operation count.

## Appendix B Claim proof and citation concordance

### B1 Mathematical claim map

| Claim | Manuscript proof location | Frozen proof source | Review evidence and limits |
|---|---|---|---|
| Complete raw-input prime-field contract; no supplied phase or frequencies | Sections 1–2; Appendix A1–A2 | P1 Sections 2–3 | R1 “Contract and exact correctness”; does not extend the shared theorem to every exact field |
| Canonical phase range of size \(N/\gcd(2,N)\) is complete | Section 1 | P1 Section 2 | R1 checks absorption of the even-length phase redundancy; uniqueness across phases is not asserted |
| Nonzero members have an allowed interior nonzero center | Section 3.1 | P2 Section 6; P4 Section 2; P1 Section 4.2 | R1 Vandermonde/no-consecutive-zeros argument; needs \(N\ge3r\) |
| \(E(0)=x_c^{r+1}\ne0\), \(\deg E\le\binom{r+2}{3}\), every leading minor has nonzero constant coefficient | Theorem 1; Section 3.2 | P2 Sections 1–2 | R1 determinant and rearrangement audit; equality of degree is not guaranteed |
| Every true phase is a root; at most \(C_*\) grid candidates | Section 3.3 | P1 Section 4.2; P4 Section 2 | R1 derives the separate row and column factors explicitly |
| Zero reduction modulo \(z^L-1\) retains all phases | Sections 3.3 and 6 | P1 Sections 4.3 and 10 | R1 checks both an accepting and rejecting zero-reduction control; root count always uses original nonzero \(E\) |
| Unit-safe ring recurrence and \(T(r)=r^2(D+1)^\kappa\) construction envelope | Section 4 | P2 Section 4 | R1 confirms nonsymmetric predictor invariants and cached scalar inverse; classical Toeplitz kernel C3 |
| Exact fixed-phase dyadic membership from BM, root scan, amplitudes, global synthesis | Section 5 | P3 Section S2; P1 Section 4.1 | R1 checks index negation, amplitude formula, and arbitrary-prefix rejection; classical C1–C2 recovery and C4 pruning |
| Complete dyadic attempt ledger, inversions, storage | Theorem 2; Section 6; Appendix A4 | P1 Section 4.3 | R1 “Hybrid bound and complete rejection ledger”; proof-level bound, not runtime measurement |
| All-length blocked scan and global recurrence verification | Theorem 3; Section 7; Appendix A5 | P4 Sections 3–6; P1 Section 4.2 | R1 accepts original B-envelope; no generic all-length FFT prerequisite |
| All-length Gauss row including \(a=0\), nonunit phases, even reduced lengths, and \(q=1\) | Section 8 | P1 Section 6 | R1 “Dense outputs fallback and operator applications”; 1,176 historical direct-row controls; current proof independent of D06 historical-byte identity |
| Sparse-first cost and equal/unequal-cap semantics | Section 9; Appendix A6 | P1 Section 5 | R1 checks the paid failed first attempt; no universal \(\min(A,B)\) conclusion |
| Sparse fresh-vector operator cost remains separate | Section 9 | P3 Section S2; P1 Section 8 | R1 checks the sign, factor \(N\), and odd-length one-chirp Fourier reduction; no application lower bound |
| Complete rejection differs from budget abort; paid backend | Section 10; Appendix A1, A3, A6 | P1 Section 7 | R1 accepts REJECT/UNKNOWN distinction; no DFT promised on REJECT |
| Word and bit-model conversions remain parameterized | Appendix A7 | P1 Section 9 | R1 requires paid inversion, certification, integer work, and input/output traffic |

### B2 Classical attribution map

| Ingredient | Citation and location | Use in this manuscript | What is not attributed to that source |
|---|---|---|---|
| Minimal recurrence synthesis | C1 Massey 1969, Section III, Theorems 2–3 and corollary | Berlekamp–Massey on a finite-field prefix, with nondecreasing minimal order | The common-phase eliminant, phase scan, or complete chirp decision ledger |
| Prony and Vandermonde reconstruction | C2 Peter–Plonka, Theorem 2.1 and Section 5 | Classical exponential-sum recovery; the manuscript supplies its finite-field factorization and full-input check | A claim that the cited complex-domain theorem directly states our exact finite-field decision interface |
| Nonsymmetric Toeplitz predictors | C3 Gutknecht–Hochbruck 1995, Section 2, equations (2.7)–(2.10), Algorithm 1, and (2.17)–(2.20) | Paired predictors, pivot/Schur-complement structure | The center-derived unit guarantee over a truncated finite-field polynomial ring; that algebraic specialization is proved in Section 4 |
| Fourier pruning | C4 FFTW official documentation | Classical \(O(N\log h)\)-type arithmetic saving for known support; the exact input-parity tree bound is proved in Section 5 | Practical speedup, optimized implementation, or a non-dyadic support-pruning theorem |
| Karatsuba and Newton arithmetic | P2 Section 4 supplies the recurrences and local cost derivation | The standard multiplication recurrence \(M(m)=3M(\lceil m/2\rceil)+O(m)\) and Newton residual squaring | An original polynomial-multiplication or series-inversion algorithm |
| Chirp convolution and overlap-add | P4 Sections 3–4 give the explicit integer-binomial identity and block accounting | Established convolution mechanisms with no field half or extra roots | A new general chirp-z transform, or a blanket all-length \(O(N\log N)\) backend |

The present pass reopened the primary C1, C2, C3, and C4 sources and inspected the relevant passages. C5 and C6 were also reopened as versioned primary PDFs. This activity checks cited source locations; it does not turn the incomplete C7–C9 comparison into a completed literature survey.

### B3 Input interface comparison

| Work | Data and domain supported by inspected evidence | Shared unknown parameter and conclusion | Comparison depth and remaining work |
|---|---|---|---|
| This manuscript | Every complete raw \(x\in\mathbb F_p^N\); supplied prime and exact-order root; variable cap | Unknown grid quadratic phase; exact all-input membership and full verification; DFT on acceptance; paid rejection | Complete scoped proofs and the preserved local independent review |
| C5 Agostini–Améndola–Ranestad | Ordinary moments of homoscedastic Gaussian mixtures | Trial common variance in a deconvolved Hankel determinant; atomic recovery once variance is chosen | Primary Section 4.3 inspected; v2 equations (90)–(92), published (79)–(81). Establishes conceptual elimination antecedent, not a matched raw-vector decision theorem |
| C6 Wu–Yang | Empirical moments from statistical samples | Shared-variance root procedure and quadrature with statistical/almost-sure qualifications | Primary v2 Section 4.2, Algorithm 3, Lemmas 6–7; footnote 6 gives an exceptional empirical configuration. Numerical root-finding work is not an exact finite-field root/rejection ledger |
| C7 Derin 1987 | Abstract describes Gaussian-mixture estimation and moment equations | Equal-variance or equal-mean component estimation using Prony’s method | Abstract and metadata only. Obtain and inspect pp. 142–148 before attributing unknown-common-variance assumptions, determinant equations, or universal guarantees |
| C8 Applebaum et al. 2009 | Inspected passages use complex-valued chirps on prime-length grids | Decoder based on delay products, Fourier peaks, dechirping, and residual stopping; a separate sparse-minimizer uniqueness theorem | Indexed primary passages only; full PDF inspection pending. Distinguish uniqueness of the \(\ell_0\) minimizer from every-input correctness of the peak decoder |
| C9 Lindsay 1989 | Moment-matrix setting known through C5’s discussion | Theorem 5B is cited by C5 for selecting a variance root | Original theorem not independently read. Obtain its statement, hypotheses, and surrounding argument before claiming exact correspondence or exclusion |

Observed random samples, ordinary moments, equispaced density ordinates, characteristic-function ordinates, complex chirps, and \(\mathbb F_p\)-valued arrays are different input interfaces. Their relation may motivate a comparison; it cannot substitute for one. In particular, a shared quadratic-exponential factor in Gaussian ordinate formulas is a reason to examine older methods carefully, not a reason to assert that an uninspected paper either contains or excludes this theorem.

The C7/C8/C9 gaps are priority/comparison gaps. They are not missing lemmas in the current finite-field proof. No source has been marked cleared merely because access failed.

### B4 Identity and historical evidence qualifications

- The current proof source P1 has SHA-256 `670fc97d4969b0130ba7b99661de1092c6989272c717d3c8dade17771eb4a11c` and 28,692 bytes. Its historical header says independent review was pending. The later R1 acceptance applies to those exact bytes; this packet preserves the historical header rather than silently rewriting it.
- R1 has SHA-256 `5caac961c8ef5120c55fa024063080e0d87b67e8cc5847387f239221cb6d3cbb` and 15,374 bytes. Its receipt binds the reviewed report, checker, and saved result. Packet verification checks these identities without rerunning inherited research code.
- The available D06 repository variant has 13,619 bytes and actual SHA-256 `8bb0ccc144506e968df1a9999300e3e42d060dc055b9e7f6a1049e1b36753b0f`. It is 28 bytes shorter than the historical record and does not match historical SHA-256 `e871250b94c9a5823adacee7da26bb6d4477af0758c684aa8c8ff9e34be21f89`. The mismatch remains explicit. Manuscript Section 8 uses P1’s self-contained, subsequently reviewed Gauss proof.
- R1’s saved controls include 1,043 hybrid decisions, 1,250 sparse decisions, 240 accepted-certificate and dense-output checks, 204 pruned transforms, 150 Toeplitz/permutation comparisons, and 1,176 Gauss rows. These are historical reviewer results. They are not fresh runs for this manuscript, optimized implementation evidence, or all-parameter proof substitutes.
- The reviewer used schoolbook polynomial arithmetic for controls. The asymptotic claim derives from the mathematical recurrence and cost proof, not timings of that checker.
- The new packet’s integrity checks establish byte identities, receipt links, and local document links. They do not constitute independent mathematical peer review of this editorial consolidation. No submission, outreach, repository mutation, or new fusion is performed by this packet’s authoring workflow.

### B5 Remaining work before stronger claims

1. Obtain authorized readable original bodies for Derin and Lindsay and complete the Applebaum journal-body inspection. Make theorem-level comparisons of assumptions, data interfaces, uniform nonvanishing, candidate completeness, and worst-case rejection costs.
2. Obtain a fresh review of this assembled manuscript if it is to be circulated as a formally finalized paper. Its underlying theorem is already locally reviewed; the manuscript is a new editorial object.
3. If claiming practical speed or an optimized implementation, implement and benchmark the specified kernels under a declared machine model. This is not required for the mathematical working draft.
4. Resolve historical D06 bytes only if historical source identity itself is needed. The currently proved output theorem does not depend on resolving that provenance discrepancy.

No additional theorem extension, rank census, generic FFT experiment, or fusion is required to state the present scoped result. Worldwide novelty remains unclaimed.

## References

### Classical and comparison literature

[C1] J. L. Massey, *Shift-Register Synthesis and BCH Decoding*, IEEE Transactions on Information Theory 15(1), 122–127 (1969), Section III, Theorems 2–3 and the subsequent corollary. [Author archive PDF](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf). Berlekamp’s iterative algorithm is explicitly credited in this source.

[C2] T. Peter and G. Plonka, *A Generalized Prony Method for Reconstruction of Sparse Sums of Eigenfunctions of Linear Operators*, author manuscript, Theorem 2.1 and Section 5. [Author PDF](https://na.math.uni-goettingen.de/pdf/Operator_Prony_revised2.pdf). Cited as a classical recovery reference; its displayed complex-domain result is not itself the finite-field decision theorem proved here.

[C3] M. H. Gutknecht and M. Hochbruck, *Look-ahead algorithms for Toeplitz systems*, Numerische Mathematik 70, 181–227 (1995), Section 2, equations (2.7)–(2.10), Algorithm 1, and equations (2.17)–(2.20). [Author-hosted electronic version](https://people.math.ethz.ch/~mhg/pub/mhg-published/GutH95-NM70-laLSnHTs.pdf). Electronic page labels may differ from print. Its real/complex presentation is not cited as stating our truncated-ring theorem.

[C4] FFTW authors, *Pruned FFTs*. [Official documentation](https://fftw.org/pruned.html). Cited for the classical pruning mechanism and arithmetic-versus-runtime distinction; the exact tree count used here is proved in Section 5.

[C5] D. Agostini, C. Améndola, and K. Ranestad, *Moment Identifiability of Homoscedastic Gaussian Mixtures*, arXiv:1905.05141v2 (2020), Section 4.3, printed pp. 23–24, equations (90)–(92). [Versioned preprint](https://arxiv.org/pdf/1905.05141v2). Published in Foundations of Computational Mathematics 21, 695–724 (2021), corresponding equations (79)–(81), [publisher version](https://link.springer.com/article/10.1007/s10208-020-09469-6).

[C6] Y. Wu and P. Yang, *Optimal estimation of Gaussian mixtures via denoised method of moments*, arXiv:1807.07237v2 (2019), Section 4.2, printed pp. 18–19, Algorithm 3, Lemmas 6–7, and footnote 6. [Versioned preprint](https://arxiv.org/pdf/1807.07237v2).

[C7] H. Derin, *Estimating Components of Univariate Gaussian Mixtures Using Prony’s Method*, IEEE TPAMI 9(1), 142–148 (1987). [DOI](https://doi.org/10.1109/TPAMI.1987.4767880); [indexed author abstract](https://pubmed.ncbi.nlm.nih.gov/21869385/). Full-text comparison pending.

[C8] L. Applebaum, S. D. Howard, S. Searle, and R. Calderbank, *Chirp sensing codes: Deterministic compressed sensing measurements for fast recovery*, Applied and Computational Harmonic Analysis 26, 283–290 (2009). [DOI](https://doi.org/10.1016/j.acha.2008.08.002); [primary PDF location](https://www.ese.wustl.edu/~nehorai/MURI/publications/Applebaum_2009.pdf). Existing inspection is passage-level, not a complete-PDF read.

[C9] B. G. Lindsay, *Moment Matrices: Applications in Mixtures*, Annals of Statistics 17(2), 722–740 (1989). [DOI](https://doi.org/10.1214/aos/1176347138). Original Theorem 5B comparison pending; its attribution is presently indirect through [C5].

### Project proof and review sources

[P1] *Exact recognizer unification with a paid rejection ledger*, 10 October 2026, Sections 2–9. Preserved as `evidence/P1_RECOGNIZER_UNIFICATION.md`.

[P2] *Constructive extension: a polynomial-cost phase eliminant*, Sections 1–4. Preserved as `evidence/P2_TOEPLITZ_ELIMINANT.md`; source commit and bytes are pinned in `SOURCE_PINS.json`.

[P3] *Structured fusion second pass: proved results and strict boundaries*, Section S2 only. Preserved as `evidence/P3_STRUCTURED_THEOREMS.md`. Other sections are not claims of this manuscript.

[P4] *Exact common-chirp recognition with blocked verification*, Sections 1–6. Preserved as `evidence/P4_BLOCKED_THEOREM.md`.

[R1] *Independent review of unified exact recognizers*, 10 October 2026, scoped proof verdict PASS. Preserved as `evidence/R1_INDEPENDENT_REVIEW.md`, with its original receipt and saved results. Historical tests are not presented as newly rerun tests.

[R2] *Common-chirp eliminant: bounded antecedent comparison*, 10 October 2026. Preserved as `evidence/R2_PRIORITY_COMPARISON.md`, with its source-access ledger. It explicitly leaves priority unresolved.
