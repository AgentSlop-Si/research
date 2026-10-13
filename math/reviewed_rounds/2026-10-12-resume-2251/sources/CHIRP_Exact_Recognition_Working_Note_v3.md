---
title: Exact recognition of common quadratic chirps
subtitle: Version 3 with implementation and antecedent appendices
date: 11 October 2026
---

## 1 Purpose and main theorem

This note gives a deterministic, exact membership test for finite-field signals that share one unknown quadratic phase and have at most a specified number of linear frequency modes. A cyclically centered determinant is a nonzero polynomial whose roots include every valid common phase. Each surviving phase is then checked against the entire raw input. On acceptance, a quadratic Gauss-row calculation produces the complete discrete Fourier transform.

The cyclic formulation permits every rank bound $1\le r<N$; the former interior-window assumption $N\ge 3r$ is unnecessary. This is a scope refinement of the same recognition method. Prony recovery, Toeplitz predictor recurrences, short convolution, FFT pruning, and quadratic Gauss identities are classical ingredients. Historical priority of the exact combined recognition contract remains unresolved.

**Theorem 1.** Let $N\ge2$, let $p$ be a supplied prime with $N\mid(p-1)$, and let $\omega\in\mathbb F_p$ be supplied with certified exact order $N$. Let $1\le r<N$. Given all $N$ coordinates of $x\in\mathbb F_p^N$, define the target family by

$$x_j=\omega^{a j^2}\sum_{\ell=1}^{s}\gamma_\ell\omega^{b_\ell j},\qquad 0\le j<N,\quad 0\le s\le r. \tag{1}$$

Here $a,b_\ell\in\mathbb Z/N\mathbb Z$, the listed $b_\ell$ are distinct, and the listed $\gamma_\ell\in\mathbb F_p$ are nonzero. The empty sum represents zero. There is a deterministic exact algorithm that accepts precisely this family, returns one fully verified representation on acceptance, and then returns all positive-sign unnormalized DFT values

$$\widehat x_k=\sum_{j=0}^{N-1}x_j\omega^{kj},\qquad 0\le k<N. \tag{2}$$

Rejection certifies nonmembership in (1); it does not supply the rejected vector's transform. Put $\kappa=\log_2 3$. For arbitrary admissible lengths the algorithm uses

$$O\!\left(Nr^{2+\kappa}+r^{2+3\kappa}\right) \tag{3}$$

field additions and multiplications. When $N$ is dyadic, a separate refinement uses

$$O\!\left(Nr^3\log(r+2)+r^{2+3\kappa}\right). \tag{4}$$

Both routes use $O(1+r^4)$ scalar field inversions and $O(N+r^4)$ live field elements. All raw reads, coefficient processing, supplied-root tables, failed candidates, verification work, and accepted output writes are charged. Integer index arithmetic, gcd and modular inverses of integers are accounted for separately from these field-operation counts. Field/root discovery, a bit-complexity bound, numerical robustness, optimized implementation timings, and constant-round parallelism are outside the theorem.

## 2 Circular centering and the phase polynomial

Define $x^{\circ}_j=x_{j\bmod N}$ for every integer $j$, including negative indices. This is a lookup into the supplied data, not an extra observation. A model term is itself $N$-periodic: replacing $j$ by $j+N$ changes its exponent by $2aNj+aN^2+b_\ell N$, a multiple of $N$. Thus a valid model matching the raw input matches this periodic continuation.

Read all coordinates first. Accept the zero vector with its empty representation and zero transform. Otherwise choose any center $c$ with $x_c\ne0$. Set

$$f(d)=\frac{d(d-1)}2,\qquad A_c(t)_{ij}=x^{\circ}_{c+i-j}t^{f(i-j)},\qquad 0\le i,j\le r, \tag{5}$$

and let $E_c(t)=\det A_c(t)$. The fraction in $f$ is an integer formula, so no field division by two is involved.

**Lemma 2.** The polynomial $E_c$ is nonzero, has degree at most $D=\binom{r+2}{3}$, and vanishes at $t=\omega^{-2a}$ for every phase $a$ in a representation (1). Every leading $k$-square minor of $A_c$ has constant term $x_c^k$.

**Proof.** For integer $d$, $f(d)\ge0$, and $f(d)=0$ precisely for $d=0,1$. Consequently $A_c(0)$ is lower bidiagonal, with diagonal $x_c$ and subdiagonal $x^{\circ}_{c+1}$. It follows that

$$E_c(0)=x_c^{r+1}\ne0. \tag{6}$$

The same argument applies to every leading square block. Repetition of coordinates under cyclic lookup has no effect on this exponent pattern or on the unique degree-zero determinant contribution.

For a determinant term indexed by a permutation $\sigma$ of $\{0,\ldots,r\}$, its exponent is

$$\sum_{i=0}^{r}f(i-\sigma(i))=\sum_{i=0}^{r}i^2-\sum_{i=0}^{r}i\sigma(i). \tag{7}$$

Strict rearrangement maximizes (7) at reversal $\sigma(i)=r-i$, giving

$$D=2\sum_{i=0}^{r}i^2-r\sum_{i=0}^{r}i=\frac{r(r+1)(r+2)}6. \tag{8}$$

Every minor also has degree at most $D$: extend a partial row-column matching to a full permutation, adding only nonnegative exponents. No characteristic or distinct-coordinate assumption enters this bound.

For a genuine phase $a$, let $y_j=x^{\circ}_j\omega^{-a j^2}$ on all integers and put $h=c-r$. It is an $s$-term exponential sequence. At $t_a=\omega^{-2a}$,

$$x^{\circ}_{h+i+j}t_a^{\binom{i+j}{2}}=y_{h+i+j}\omega^{a h^2+a(2h+1)(i+j)}. \tag{9}$$

The extra factor separates into nonzero row and column multipliers, so the $(r+1)$-square matrix in (9) has rank at most $s\le r$. Column reversal and Laurent row-column scaling give

$$E_c(t)=(-1)^{r(r+1)/2}t^{-E_{\min}}\det\!\left(x^{\circ}_{h+i+j}t^{\binom{i+j}{2}}\right)_{i,j=0}^{r}, \tag{10}$$

where $E_{\min}=(r+1)r(r-1)/2$. Indeed, after column reversal use $\binom{r+i-j}{2}=\binom r2+r(i-j)+f(i-j)$; the row and column powers total $E_{\min}$. Equation (10) is a Laurent identity, evaluated only at $t_a\ne0$. It proves $E_c(t_a)=0$, even when $h<0$ or indices wrap. This completes the proof.

The degree bound is attained for this particular polynomial. If every $x_j=1$, a Vandermonde factorization yields

$$E_c(t)=\prod_{k=1}^{r}(1-t^k)^{r+1-k}. \tag{11}$$

To see this, factor $t^{f(i)}$ from row $i$ and $t^{f(-j)}$ from column $j$; the remaining entries are $(t^{-j})^i$. The powers extracted from its Vandermonde factors cancel the initial powers. The degree is $\sum_{k=1}^r k(r+1-k)=D$, with leading coefficient $\pm1$ in every characteristic. This proves degree sharpness for $E_c$, not optimality over other certificates or a maximal number of distinct phase roots.

## 3 The phase quotient and exact recovery

Put

$$L=\frac{N}{\gcd(2,N)},\qquad Q=\min(D,L). \tag{12}$$

The points $\omega^{-2a}$, $0\le a<L$, are distinct. If $N$ is even, the change $a\mapsto a+N/2$ can be absorbed by $b_\ell\mapsto b_\ell+N/2$, because $j^2-j$ is even. Hence this canonical range covers every representation. It removes only a universal redundancy; more signal-dependent ambiguities may remain. For example, with $N=3$, $p=7$, $\omega=2$, $r=2$, the vector $(0,1,3)$ belongs at all three canonical phases.

Since $E_c$ is nonzero, at most $Q$ phases survive its root test. The usual polynomial root bound applies even if $D\ge p$. It is possible for every phase point to be a root. Reducing $E_c$ modulo $t^L-1$ can accelerate evaluation, but the reduced polynomial may be zero and must not replace the original nonzero certificate.

### 3.1 The all length candidate test

For each surviving phase $a$, dechirp all raw samples by $y_j=x_j\omega^{-a j^2}$. Read the first $2r$ entries of the periodic continuation $y^{\circ}$; since $r<N$, this uses fewer than $2N$ lookups. The following test is deterministic.

**Step 1.** Compute $s=\operatorname{rank}H_r$, where $H_r=(y^{\circ}_{i+j})_{0\le i,j<r}$. If $s=0$, require the entire raw vector to be zero. Otherwise continue.

**Step 2.** Require the leading $s$-square Hankel block to be nonsingular. Solve for the monic node polynomial $P(z)=\sum_{j=0}^s P_jz^j$, with $P_s=1$, from $\sum_{j=0}^sP_jy^{\circ}_{i+j}=0$ for $0\le i<s$.

**Step 3.** Evaluate $P$ at every supplied grid point $\omega^b$, $0\le b<N$. Require exactly $s$ distinct grid roots $\lambda_\ell=\omega^{b_\ell}$.

**Step 4.** Require every ordinary unwrapped residual to vanish:

$$R_k=\sum_{j=0}^{s}P_jy_{k+j}=0,\qquad 0\le k<N-s. \tag{13}$$

**Step 5.** Solve the first $s$ moments $y_j=\sum_\ell\gamma_\ell\lambda_\ell^j$, $0\le j<s$, using the nonsingular Vandermonde matrix. Omit zero weights and return the resulting representation.

**Soundness.** The constructed exponential sum agrees with the first $s$ entries and satisfies the same monic recurrence. Equation (13) propagates equality to all $N$ raw entries by induction. Thus a misleading periodic prefix cannot cause false acceptance. Even when $s=N-1$, the one residual checks the final raw coordinate after $N-1$ initial moments. A zero prefix alone never certifies a nonzero raw input.

**Completeness.** For a true $s$-mode sequence, $H_r=V_r\operatorname{diag}(\gamma)V_r^{\mathsf T}$, where $V_r$ has full column rank $s$, its transpose has full row rank $s$, and all weights are nonzero. Hence $\operatorname{rank}H_r=s$. Its leading block has determinant $(\det V_s)^2\prod_\ell\gamma_\ell\ne0$. The solved polynomial is $\prod_\ell(z-\lambda_\ell)$, so the grid and residual tests pass and the moments recover the weights. This argument remains valid when $2r>N$, because a genuine model has exactly the periodic continuation being used.

Dense prefix rank, recurrence and Vandermonde solves cost $O(r^3)$ additions/multiplications and $O(r)$ inversions per candidate, including failed candidates. Full residual checking, rather than an extra uncharged $O(Nr)$ synthesis, will supply the all-length fast verification bound.

### 3.2 The dyadic recovery alternative

For dyadic $N$, ordinary Berlekamp-Massey on the $2r$ periodic-prefix values uses $O(r^2)$ work and $O(r)$ scalar inversions. A failed finite prefix can have order as large as $2r$; that still fits these costs. Reject if the output order $s$ exceeds $r$. Require a connection polynomial $C(z)=1+C_1z+\cdots+C_sz^s$ of degree exactly $s$ and exactly $s$ distinct grid roots. For a true sequence,

$$C(z)=\prod_{\ell=1}^{s}(1-\lambda_\ell z). \tag{14}$$

A root $\omega^v$ corresponds to node $\lambda=\omega^{-v}$, rather than $\omega^v$. This convention differs from the monic node polynomial in Section 3.1. Compute

$$B(z)=C(z)\left(\sum_{j=0}^{s-1}y_jz^j\right)\bmod z^s,\qquad
\gamma_\ell=-\frac{\lambda_\ell B(\lambda_\ell^{-1})}{C'(\lambda_\ell^{-1})}. \tag{15}$$

The generating function is $\sum_\ell\gamma_\ell/(1-\lambda_\ell z)$. Multiplying it by $C$ and evaluating at a reciprocal node proves (15); differentiation contributes the factor $-\lambda_\ell$. Distinct roots make the denominators nonzero. Quadratic polynomial arithmetic and Horner evaluations cost $O(r^2)$ work and $O(r)$ inversions. Finally synthesize and compare all $N$ raw dechirped entries exactly. The zero-order case also requires zero full synthesis. Completeness follows from the invertible leading Hankel block and $2r\ge2s$; soundness follows from full synthesis.

## 4 Computing the eliminant with unit Toeplitz pivots

Let $R$ be the ring of polynomials over $\mathbb F_p$ modulo $t^{D+1}$. All coefficient arithmetic can be performed in $R$, since the final determinant has degree at most $D$. Write $a_d=x^{\circ}_{c+d}t^{f(d)}$ and $T_k=(a_{i-j})_{i,j=1}^{k}$, with $\det T_0=1$. Lemma 2 makes every $\det T_k$ a unit in $R$.

For completeness, the inherited nonsymmetric predictor recursion is given explicitly. Let $u^{(k)},v^{(k)}$ be indexed from $0$ through $k$, with $u_0=v_0=1$, satisfying

$$\sum_{j=0}^{k}a_{i-j}u_j=0,\qquad \sum_{j=0}^{k}a_{j-i}v_j=0,\qquad 1\le i\le k. \tag{16}$$

Their common error term is

$$e_k=\sum_{j=0}^{k}a_{-j}u_j=\sum_{j=0}^{k}a_jv_j=\frac{\det T_{k+1}}{\det T_k},\qquad e_k(0)=x_c. \tag{17}$$

The equalities follow from Schur complements and transposition. Initialize $u=v=(1)$, $e=a_0$, and $\Delta=a_0$. At step $k=1,\ldots,r$, use the previous length-$k$ vectors to form

$$A_k=a_k+\sum_{j=1}^{k-1}a_{k-j}u_j,\qquad B_k=a_{-k}+\sum_{j=1}^{k-1}a_{j-k}v_j, \tag{18}$$

$$\alpha_k=-A_k/e,\qquad \beta_k=-B_k/e. \tag{19}$$

Simultaneously update $u'_j=u_j+\alpha_kv_{k-j}$ and $v'_j=v_j+\beta_ku_{k-j}$ for $1\le j<k$, setting $u'_0=v'_0=1$, $u'_k=\alpha_k$, and $v'_k=\beta_k$. Then set

$$e'=e+\alpha_kB_k=e-A_kB_k/e,\qquad \Delta'=\Delta e'. \tag{20}$$

The reversed old predictor contributes zero to the first $k-1$ equations and $e$ to the new final equation. Thus (19) cancels its residual and preserves (16). Expanding the new error gives (20). At completion $\Delta=E_c$ in $R$ and therefore as a degree-at-most-$D$ polynomial.

Every reciprocal starts from the same scalar inverse $x_c^{-1}$. Newton doubling $g\leftarrow g(2-eg)$ lifts a reciprocal to twice its precision, since $1-eg_{\mathrm{new}}=(1-eg)^2$. This identity uses no division by two. Karatsuba multiplication costs $M(m)=O(m^\kappa)$; each unit-series reciprocal costs $O(M(D+1))$. The $O(r^2)$ ring operations and $r$ reciprocal calculations therefore cost

$$O\!\left(r^2(D+1)^\kappa\right) \tag{21}$$

field additions/multiplications, one scalar inverse, and $O(r(D+1))$ live coefficients. The construction has $r$ predictor stages and $O(\log(D+1))$ precision doublings for each reciprocal. A small scalar-inversion count does not imply constant sequential depth.

## 5 Paying for evaluation and full verification

### 5.1 Arbitrary admissible lengths

Let $F(z)=\sum_{j=0}^{s}F_jz^j$ and $b=s+1\le N$. Split the output indices into blocks $k=K+u$, $0\le u<b$, allowing a shorter last block. The integer identity

$$uj=\binom u2+\binom{j+1}{2}-\binom{u-j}{2} \tag{22}$$

gives

$$F(\omega^{K+u})=\omega^{\binom u2}\sum_{j=0}^{s}\left(F_j\omega^{Kj+\binom{j+1}{2}}\right)\omega^{-\binom{u-j}{2}}. \tag{23}$$

Each block is a length-$b$ by length-$(2b-1)$ ordinary convolution, computed by a constant number of balanced Karatsuba products in $O(b^\kappa)$ operations. All scalings cost $O(b)$ per block; the kernel is reusable, and changing $K$ by $b$ updates the coefficients with precomputed $\omega^{bj}$. The total is $O(Nb^{\kappa-1})$ work and $O(N+b)$ storage. No square root of $\omega$, extension field, or smooth transform length is needed.

For the residuals (13), convolve $y$ with the reversed coefficients $(P_s,\ldots,P_0)$. The residual $R_k$ is convolution coefficient $k+s$. Partition $y$ into length-$b$ chunks, multiply each by this fixed length-$b$ kernel, and overlap-add. The same $O(Nb^{\kappa-1})$ bound pays for all $N-s$ residuals and every raw coordinate. The sole size condition is $b=s+1\le N$, which follows from $r<N$.

Horner evaluation of $E_c$ on all $L$ phase points costs $O(N(D+1))$. Thus each surviving candidate, including every failure, costs $O(N(r+1)^{\kappa-1}+r^3)$ work and $O(r)$ inversions.

### 5.2 The dyadic refinement

When $N$ is a power of two, a radix-two DFT with at most $q$ nonzero input coefficients can skip all-zero branches. At recursion depth $d$, at most $\min(2^d,q)$ branches of length $N/2^d$ are active. Its combine work is bounded by

$$O\!\left(N\sum_{d=0}^{\log_2N-1}\min(1,q/2^d)\right)=O(N\log(q+2)). \tag{24}$$

This uses only roots of orders dividing $N$. Applying it to the degree-$s$ connection polynomial costs $O(N\log(r+2))$. Applying it to the at-most-$s$ frequency weights produces full synthesis at the same cost. Together with Section 3.2, this gives $O(N\log(r+2)+r^2)$ per surviving phase.

For phase enumeration, reduce $E_c$ modulo $t^L-1$ in $O(D+L)$ work, paying for each coefficient. The reduced array has support at most $\min(D+1,L)$. A length-$L$ pruned DFT with root $\omega^{-2}$ scans the phase points; $L=1$ is evaluated directly. The cost is $O(D+N\log(\min(D+1,L)+2))$. If reduction yields the zero polynomial, all phase points survive and are still charged. These dyadic bounds are not asserted for arbitrary $N$.

## 6 All accepted Fourier outputs from one Gauss row

After accepting one representation, form the shared row

$$G_a(v)=\sum_{j=0}^{N-1}\omega^{aj^2+vj}. \tag{25}$$

Then $\widehat x_k=\sum_{\ell=1}^s\gamma_\ell G_a(k+b_\ell)$, with indices modulo $N$. The row costs $O(N)$ field operations and the final combination costs $O(Ns+N)$, including output writes. The construction below covers nonunit phases and even composite lengths.

Use the representative $0\le a<N$, set $d=\gcd(a,N)$, $m=N/d$, and $A=a/d$. For $a=0$, set $d=N$, $m=1$, $A=0$. Write $j=u+vm$. Summing the geometric progression over $v$ shows that $G_a(c)=0$ unless $d\mid c$. If $c=dw$, then

$$G_a(dw)=d\,T(w),\qquad T(w)=\sum_{u=0}^{m-1}\eta^{Au^2+wu},\qquad \eta=\omega^d. \tag{26}$$

For $m=1$, this is the $N$-spike row: $G_0(0)=N$ and the other entries vanish. Otherwise $A$ is invertible modulo $m$.

If $m$ is odd, a shift completing the square gives

$$T(w)=T(0)\eta^{-w^2(4A)^{-1}}, \tag{27}$$

where the inverse is modulo the integer $m$. Compute $T(0)$ by one explicit length-$m$ sum; a table of powers of $\eta$ then gives the row.

If $m=2q$ is even, $A$ is odd. Translation by $q$ multiplies the summand by $(-1)^{Aq+w}$, so $T(w)=0$ unless $w$ has the parity of $q$. Set $w_0=q\bmod2$ and compute $T(w_0)$ directly in $O(m)$ field work. For an allowed $w$, solve

$$u=\frac{w-w_0}{2}A^{-1}\pmod q,\qquad T(w)=T(w_0)\eta^{-Au^2-w_0u}. \tag{28}$$

When $q=1$, use $u=0$ without an inverse modulo one. The shift $j\mapsto j+u$ proves (28). Changing $u$ by $q$ changes the exponent by a multiple of $2q$, because $Aq+w_0$ is even. Thus the chosen lift does not matter. Since $p>N\ge2$, characteristic two is excluded from the recognition theorem, and the parity cancellation is valid.

Integer gcd and modular-inverse calculations in (26)--(28) are separate from scalar inversion in $\mathbb F_p$. This direct base-row construction does not assume a closed-form square root of a Gauss sum or an uncharged Gauss-sum oracle.

## 7 The complete cost ledger

Process candidates one at a time and stop at the first fully verified representation. Worst-case bounds still pay for all $Q$ surviving phases. With $D=\binom{r+2}{3}$, $Q=\min(D,L)$, the all-length work is

$$O\!\left(r^2(D+1)^\kappa+N(D+1)\right) \tag{29}$$

plus

$$O\!\left(Q\left(N(r+1)^{\kappa-1}+r^3\right)+Nr+N\right). \tag{30}$$

The dyadic work is

$$O\!\left(r^2(D+1)^\kappa+D+N\log(\min(D+1,L)+2)\right) \tag{31}$$

plus

$$O\!\left(Q\left(N\log(r+2)+r^2\right)+Nr+N\right). \tag{32}$$

The terms have the following meanings.

**Raw input and supplied roots.** All $N$ reads, the zero test, nonzero center, root-power tables, and $O(N)$ preprocessing.

**Polynomial certificate.** Coefficient creation, the unit Toeplitz recursion and coefficient writes in (21).

**Phase scan.** Horner at arbitrary length; paid reduction and support-pruned scan at dyadic length.

**Every surviving phase.** All dechirping, prefix recovery, root checks, weights, and full-input residual or synthesis checks, including failures.

**Accepted transform.** One complete Gauss row and $O(Nr+N)$ combination and output work.

Because $D=O(r^3)$ and $Q\le D$, (29)--(30) imply (3): the $r^6$ dense-prefix contribution is dominated by $r^{2+3\kappa}$, and the scan term $Nr^3$ by $Nr^{2+\kappa}$. Equations (31)--(32) imply (4), with the $r^5$ recovery contribution also dominated by $r^{2+3\kappa}$.

The Toeplitz construction uses one scalar inverse. A candidate needs $O(r)$ further scalar inversions, hence the total is $O(1+Qr)=O(1+r^4)$. Live storage is

$$O\!\left(N+r(D+1)+r^2\right)=O(N+r^4). \tag{33}$$

This accounts for the raw and output arrays, coefficient/predictor storage and one candidate's matrices or recurrence. Scalar inversion, field arithmetic, coefficient storage and sequential stages are distinct quantities. Dense elimination may have $O(r)$ pivot stages; dyadic transforms have logarithmic recursion depth.

For fixed $r$, the all-length bound is $O_r(N)$. More generally, its sufficient growing-rank regime for $o(N\log N)$ field additions/multiplications is $r=o((\log N)^{1/(2+\kappa)})$. This is a statement about membership recognition and accepted structured outputs. It neither computes transforms of rejected inputs nor improves a general-purpose FFT theorem. For $r$ comparable to $N$, the conservative bounds are expensive.

## 8 Classical antecedents and the unresolved comparison

The conceptual division matters for evaluating the contribution. The certificate in Lemma 2 has a data-independent nonvanishing guarantee once any nonzero center is selected; it is joined to a supplied-grid, full-input acceptance and rejection contract. The reconstruction and arithmetic tools underneath it have established antecedents. The cyclic extension removes a witness-placement restriction; it neither changes the asymptotic exponents nor creates a separate discovery claim.

**Prony and dechirping.** Once a phase is fixed, recurrence recovery, a node polynomial, and a Vandermonde amplitude solve are ordinary exponential-sum reconstruction. Plonka, Stampfer and Keller [2], Section 4 and Theorem 4.1, treat a known nonvanishing factor and a supplied quadratic coefficient on a uniform grid. Their Theorem 5.3 treats varying unknown quadratic coefficients on a square-root sampling grid; Section 6.2 uses a fixed coefficient with cosine and sine data. These are distinct input interfaces. Cuyt and Lee [3], Section 5, equation (31) and Theorem 4, also supply a common Gaussian width before exponential reconstruction. Their cited Peter thesis pages 85--91 remain outside the inspected evidence.

**Shared-parameter elimination.** Agostini, Améndola and Ranestad [1], Section 4.3, equations (79)--(81), use trial variance to transform moments, obtain a Hankel determinant polynomial, and then apply Prony/Vandermonde recovery. This establishes the shared-parameter elimination framework. The present ordinates are fixed raw finite-field samples multiplied by binomial monomials; moment-domain statements alone do not settle the exact same certificate and decision contract. The attribution to Lindsay's Theorem 5B in [1] does not replace inspection of Lindsay's original hypotheses.

**Toeplitz and convolution.** The paired predictors and nonsingular-leading-minor condition are classical nonsymmetric Levinson/Schur machinery, explicitly developed in Gutknecht and Hochbruck [4], Section 2, equations (2.7)--(2.10) and Algorithm 1. Here the cyclic normalization supplies the unit-pivot guarantee in a truncated polynomial ring and the ledger pays for its arithmetic. The blocked chirp-z and overlap-add mechanisms in Section 5 are likewise classical, with the sectioned chirp-z precedent recorded in Rabiner, Schafer and Rader [8]. This note claims neither a new general Toeplitz kernel nor a new convolution or FFT identity.

**Quadratic Gauss sums.** Equations (26)--(28) are elementary reductions by a geometric sum and changes of variable. Including their nonunit and even-length cases is essential to the all-length contract; they are not offered as a new theory of Gauss sums.

Three original-source gaps remain: the complete body of Derin (1987) [5], the original statement and context of Lindsay (1989), Theorem 5B [6], and the complete journal body of Applebaum, Howard, Searle and Calderbank (2009) [7]. Existing abstract, indexed-passage and later-article comparisons cannot be promoted to a full primary-body read. In particular, a sparse-representation uniqueness theorem and a peak-based decoder must not be conflated with deterministic full-input recognition. Failed access is not evidence that an antecedent is absent. No first-ever or submission-ready priority claim follows from the mathematical review.

## 9 Review evidence and remaining limits

The cyclic-window theorem was independently reviewed on 11 October 2026 with no mathematical repair required. Its accepted scope includes $1\le r<N$, arbitrary nonzero cyclic centers, the periodic recovery prefix, all candidate-failure costs and the separate dyadic refinement. The exact source and review bindings are recorded in the accompanying provenance file.

The independent reference controls recorded 4,250 vector/rank decisions and 15,687 per-phase decisions with no disagreement against a separately evaluated Fourier-support oracle. They included exhaustive spaces $\mathbb F_3^2$, $\mathbb F_7^3$ and $\mathbb F_5^4$ for every $1\le r<N$, followed by 1,680 random and structured cases through $N=16$. There were 21,658 true-phase/nonzero-center checks, 436 false-phase eliminant roots rejected by full tests, 480 wrapped Laurent-identity checks, and 24 constant-window degree identities. Further controls covered 780 periodic-prefix Berlekamp-Massey/partial-fraction decisions, 67 pruned-FFT vectors, and 115 Gauss rows with 1,809 entries. Two late-spike controls rejected a zero recovery prefix followed by a nonzero raw entry.

Those are finite reference checks, not an optimized implementation of the combined polynomial Toeplitz, blocked verification, pruned-transform and Gauss pipeline. The proofs establish general correctness and the operation bounds; the counts do not establish asymptotic performance, external priority or benchmark superiority. Extra characteristic-two determinant controls concern polynomial algebra only and are not admissible recognition instances for $N\ge2$.

All $N$ raw entries remain necessary inputs to this stated algorithm. It supplies no sample-reduction theorem, no noisy or floating-point recognition guarantee, no unique common-phase theorem and no transform upon rejection. For $r\ge N$, every vector already has an ordinary dense Fourier representation with $a=0$; this separate trivial branch is not a new structured fast-transform result. The case $N=1$ is immediate. Further publication work consists of resolving the named source gaps and, if implementation performance is to be claimed, integrating and independently testing the complete optimized pipeline.

## References and source access

The comparison below follows the recorded primary-source inspection and its access limits. It does not claim a new literature search. The proofs in Sections 2--7 are supplied in the note.

1. Agostini, Améndola and Ranestad, primary article, Section 4.3, equations (79)--(81). Relevant complete HTML body inspected in the source comparison. https://link.springer.com/article/10.1007/s10208-020-09469-6

2. Plonka, Stampfer and Keller, author manuscript dated 19 July 2018. Sections 4, 5.2 and 6.2; Theorems 4.1, 5.3 and 6.2. Searchable 28-page primary PDF inspected at the cited sections; rendered-page inspection was not available. https://num.math.uni-goettingen.de/~gplonka/pdfs/general-Prony-revised-sw.pdf

3. Cuyt and Lee, primary article, Section 5, equation (31) and Theorem 4. Relevant complete HTML body inspected. https://link.springer.com/article/10.1007/s11075-023-01564-3

4. Gutknecht and Hochbruck, Look-ahead Levinson and Schur algorithms for non-Hermitian Toeplitz systems (1995). Section 2, electronic pages 184--186, equations (2.7)--(2.10), Algorithm 1, and equations (2.17)--(2.20). Searchable primary author PDF inspected. https://people.math.ethz.ch/~mhg/pub/mhg-published/GutH95-NM70-laLSnHTs.pdf

5. Derin (1987). Original body remains unavailable in the source record; abstract and bibliographic evidence only. https://doi.org/10.1109/TPAMI.1987.4767880

6. Lindsay (1989). Original Theorem 5B and its surrounding hypotheses remain unread; attribution checked in [1]. https://doi.org/10.1214/aos/1176347138

7. Applebaum, Howard, Searle and Calderbank (2009). Indexed primary passages were compared previously; the complete journal body remains uninspected. https://doi.org/10.1016/j.acha.2008.08.002

8. Rabiner, Schafer and Rader (1969), The chirp z-transform algorithm. Classical sectioned chirp-z and overlap-add/save antecedent as documented in the inherited blocked-verification dependency. No fresh full-body inspection is claimed here.

9. CHIRP cyclic window and primary comparison, 11 October 2026. Author theorem, historical comparison and dependency proofs, preserved as the source package.

10. CHIRP cyclic window independent review, 11 October 2026. Scoped mathematical PASS, reviewed statement, independent reference controls and input verification, preserved as the review package.

## Appendix A Supplementary bit cost contract

This appendix adds an explicit binary representation and conservative bit-cost corollary to the field-operation theorem. Theorem 1 and equations (1)--(33) are unchanged. Its exclusion of bit complexity applies to that theorem; the separate statement below uses additional representation and machine assumptions. The appendix follows the independently reviewed bit-cost statement, including its counter-width correction and block-input clarification. It does not add a novelty or performance claim.

### A1 Binary input and paid access model

Let $N\ge2$, $1\le r<N$, and let $p>N$ be a supplied prime with $N\mid(p-1)$. Let $\omega$ be supplied as a residue, and put $B=\operatorname{bitlen}(p)=\lfloor\log_2p\rfloor+1$. On this admissible prime domain $p$ is odd and $B=\lceil\log_2p\rceil$. No polynomial bound on $p$ in terms of $N$ is assumed unless explicitly stated.

Encode $p,N,r$ as Elias gamma codes of $v+1$, in that order. For a positive integer $u$ with binary length $\ell$, this code consists of $\ell-1$ zero bits followed by the $\ell$-bit binary expansion of $u$. Follow the three headers by $\omega,x_0,\ldots,x_{N-1}$, each as a canonical $B$-bit unsigned residue in $\{0,\ldots,p-1\}$. No trailing bits are allowed. Let $S$ be the actual input-record length. For a valid complete record,

$$S=\sum_{v\in\{p,N,r\}}\left(2\operatorname{bitlen}(v+1)-1\right)+(N+1)B=\Theta(NB). \tag{34}$$

Use a deterministic sequential bit-cost arithmetic RAM. Copying, addition and comparison of $h$-bit integers cost $O(h)$; schoolbook multiplication and division cost $O(h^2)$. Access to a contiguous $h$-bit record at an $a$-bit address costs $O(h+a)$. Input is a finite record with end-of-input detection. All address calculations, counters and control work are charged. This is not an unqualified multitape-Turing-machine theorem or a fixed hardware-word theorem.

A paid reader parses gamma prefixes in geometrically increasing contiguous blocks. It compares each block with zero and locates the first one in the final block by successive splitting. Copy each header's binary payload once. The total copied or compared bits are linear in the inspected prefix; the sum of address and counter overheads is absorbed by this amount and the $O(B^2)$ header allowance. Reject impossible $N$ or $r$ from its decoded length or bounds before allocating arrays. Read field coordinates in $B$-bit records, and probe once after the final expected field to detect trailing input. Thus parsing and format checks cost $O(S+B^2)$ on the valid-parameter contract. This does not assume that arbitrary one-bit absolute-address accesses have constant cost.

### A2 Parameter preparation and result meanings

Validate the header constraints and residue ranges. Generate $h_0=1$ and $h_k=h_{k-1}\omega\bmod p$ through $k=N$. Require $h_N=1$ and $h_k\ne1$ for $0<k<N$; retain $h_0,\ldots,h_{N-1}$. This both certifies exact order $N$ and constructs the supplied-root table in $O(NB^2)$ bit time. A smaller order would have appeared as an earlier return to one. No factorization of $N$ or $p-1$, discrete logarithm or root search is used. A cached table is outside this default grammar; supporting one requires its own framing, validation and cost.

Complete the selected parameter-validation policy and inspect all raw coordinates before accepting a zero vector. On every valid prime/grid instance, the unchanged recognizer accepts exactly the common-quadratic-phase family (1). Acceptance returns a fully verified representation and all positive-sign unnormalized DFT coordinates (2), encoded as canonical $B$-bit residues. Rejection certifies nonmembership only; it supplies no transform of the rejected vector.

Malformed records have status INVALID_INPUT. Detected invalid bounds, order or other parameter conditions have status INVALID_PARAMETERS. Neither status is structured nonmembership. No complexity expression through nonexistent decoded $N,r,B$ is asserted for a malformed header. Supplied-prime mode assumes primality; Section A5 gives a separately paid validator for an arbitrary supplied modulus.

### A3 Supplementary corollary and unchanged ledgers

Use the same $\kappa=\log_2 3$, $D=\binom{r+2}{3}$, $L=N/\gcd(2,N)$ and $Q=\min(D,L)$, and set $I=1+Qr$. Collect equations (29)--(30) and (31)--(32), respectively, as

$$W_{\mathrm{all}}=r^2(D+1)^\kappa+N(D+1)+Q\left[N(r+1)^{\kappa-1}+r^3\right]+Nr+N, \tag{35}$$

$$W_{\mathrm{dyadic}}=r^2(D+1)^\kappa+D+N\log_2(\min(D+1,L)+2)+Q\left[N\log_2(r+2)+r^2\right]+Nr+N. \tag{36}$$

These are the accepted arithmetic ledgers with no term removed. Use $W=W_{\mathrm{all}}$ at arbitrary admissible lengths; the alternative $W=W_{\mathrm{dyadic}}$ is available only for dyadic $N$. Both include preparation, raw reads, coefficient processing, every failed candidate, full verification and accepted output writes.

**Corollary A1.** In the representation and paid-address RAM of Section A1, there is an implementation of the exact recognizer with

$$O\!\left(S+B^2W+IB^3\right)\text{ bit time},\qquad O\!\left((N+r^4)B\right)\text{ working bits}. \tag{37}$$

The corollary applies to the valid prime/grid computation, including both membership acceptance and nonmembership rejection. The optional arbitrary-modulus validation charge in Section A5 is additional.

**Arithmetic and inverse costs.** Every scalar product is reduced modulo $p$, so an unreduced product has at most $2B$ bits. A field addition or multiplication, with reduction and paid access, costs at most $O(B^2)$. Dense polynomial coefficients remain field residues throughout. For a nonzero scalar, Fermat inversion by binary exponentiation to $p-2$ uses $O(B)$ modular multiplications and costs $O(B^3)$ time and $O(B)$ scalar scratch.

There is one Toeplitz seed inverse $x_c^{-1}$. All Newton unit-series reciprocals reuse it as their initial scalar inverse; their polynomial operations are already in $W$. Every attempted phase, including failed candidates, uses $O(r)$ further scalar inversions. Divisors are tested or known nonzero before use. Hence all scalar inversions cost $O(IB^3)$. A constant number of integer gcd and modular-inverse calls in the accepted Gauss construction costs $O(B^3)$ in total, absorbed because $I\ge1$. The $a=0$, $m=1$ and $q=1$ branches avoid an inverse modulo one. Negative root exponents are table lookups after integer reduction, not field inversions.

### A4 Integer control work and storage

Structural indices and fixed-degree polynomial exponent expressions have $O(\log N)$ bits. Binary I/O offsets, bit-array addresses and arithmetic-loop counters may require $O(\log N+\log B)$ bits, which is $O(B)$. The broader assertion that every integer counter has $O(\log N)$ bits is not valid for unrestricted $p$: even with fixed $N$, a Fermat loop can require a $\Theta(\log B)$-bit counter. The optional trial-divisor index in Section A5 can use $O(B)$ bits. Indices and addresses are never reduced modulo $p$.

To see addressability, write $M=N+r(D+1)+r^2=O(N+r^4)=O(N^4)$. A flattened $O(MB)$-bit allocation has address width $O(\log M+\log B)=O(\log N+\log B)=O(B)$ because $N<p<2^B$. These addresses can be constant multiples of $B$ bits. In particular, the number of field cells can exceed $p$; an address is not required to fit in one field residue.

The number of ordinary high-level control steps can be $O(W)$. Dense Toeplitz and Newton coefficient scans, Karatsuba splits and combinations, candidate rank and solve work, blocked evaluation and overlap-add residual checks fit their existing ledgers. Process predictor stages and candidate phases sequentially. For dyadic pruning, split current support by index bits, using at most $\min(2^d,q)$ occupied subproblems at depth $d$ as in (24). Build occupancy by scanning the length-$N$ grid and this same tree, without adding an unanalysed sorting or balanced-tree routine. This pays the array traffic and metadata inside the accepted pruned-transform bound.

Ordinary address and fixed-degree integer calculations cost at most $O(B^2)$ per such step. Integer degree, padding and recursion logic implement the algorithms: $D$ is formed by integer arithmetic, precision and padding use doubling, and dyadic recursion uses index bits and depth counters. The real logarithms and $\kappa$ in the displayed bounds are analysis notation, not runtime numerical-log oracles.

Combining $O(NB^2)$ exact-order preparation, $O(B^2W)$ coefficient and control work, $O(IB^3)$ inversions, and $O(S+B^2)$ parsing gives (37), since $W\ge N\ge2$. Field records and $O(B)$-bit pointers require $O(MB)$ bits. The raw input, root table, live predictors, one candidate and all accepted outputs fit this storage; scalar scratch and depth-first recursion metadata fit within the same bound. This is a valid-parameter working-space claim, not a claim about arbitrary malformed records with no defined parameter tuple.

### A5 Prime validation and representation specific consequences

An optional validator for an arbitrary supplied modulus first rejects $p<2$, then performs deterministic trial division by integers $d=2,3,\ldots$ while $d^2\le p$. Each division, square comparison and increment costs at most $O(B^2)$. This adds

$$O\!\left(\sqrt p\,B^2\right)\text{ time and }O(B)\text{ scratch}. \tag{38}$$

This conservative time is exponential in $B$. The validator does not discover a suitable $p$ or $\omega$ from $N$. Exact-order validation alone is not a primality test: $p=9,N=2,\omega=8$ passes divisibility and order checks but is not a prime-field instance. Supplied-prime mode makes no primality-verification claim; its prime promise must not be removed silently. The optional validator must run before zero-vector acceptance.

If $r$ is fixed and, additionally, $p=N^{O(1)}$, then $B=\Theta(\log N)$ and (37) specializes to

$$O_r\!\left(N(\log N)^2+(\log N)^3\right)\text{ time},\qquad O_r(N\log N)\text{ working bits}. \tag{39}$$

This specialization uses supplied-prime mode; the optional trial-division cost remains additional if chosen. No polynomial-size modulus assumption is made in the unrestricted-$p$ statement (37).

The explicit fixed-width raw array contains $NB$ coordinate bits, and the accepted output emits $NB$ bits. The required full scan and full output therefore entail $\Omega(NB)$ bit traffic in this contract, hence $\Omega(N\log N)$ because $p>N$. Consequently the little-$o(N\log N)$ field-operation regime in Section 7 is not a little-$o(N\log N)$ bit-time claim for this interface. This is a representation-specific consequence, not a universal lower bound for compressed input or output, promise access, or a different problem.

No new FFT theorem, novelty, beta-dependent bound, constant-round result or optimized-timing claim follows. The Derin, Lindsay Theorem 5B and complete Applebaum-body comparison gaps in Section 8 remain open. Finite preparation checks in the supplementary review are functional controls, not an optimized integrated recognizer or a proof from timing measurements.

### A6 Supplementary sources and version record

Version 2 preserves the original mathematical body and adds this appendix. The author, review and consistency packets remain unchanged. The source package records exact SHA-256 and Library-version bindings. The corrected statement in [12] controls this appendix; final integration fidelity is a separate check.

11. CHIRP Bit Contract Audit and Supplement, 11 October 2026. Original author report and preparation controls, with the counter-width correction supplied by [12].

12. CHIRP Bit Contract Independent Review, 11 October 2026. Accept with corrected counter widths and paid block-input clarification. Includes the controlling reviewed statement; the field-operation theorem remains unchanged.

13. CHIRP Working Note Consistency Review, 11 October 2026. PASS for the original nine-page note, binding its Markdown, editable Word mathematics and PDF to the accepted theorem.

14. Victor Shoup, A Computational Introduction to Number Theory and Algebra, Version 2 (2008). Theorem 3.3; Theorems 4.4--4.5; Section 10.1. Primary-text arithmetic background as inspected in [12]. The paid-address model is specified here. No fresh full-book inspection is claimed. https://shoup.net/ntb/ntb-v2.pdf

## Appendix B Bounded exact reference implementation

The independently reviewed reference [15--16] realizes the exact decision interface with explicit resource limits. It is a dense reference, not the fast implementation of Theorem 1. This appendix updates the implementation checkpoint in Section 9 without changing Theorem 1, equations (1)--(33), or the corrected bit-cost contract in Appendix A. The original source archive is preserved unchanged; its historical candidate labels are superseded by the independent review for the pinned bytes only.

### B1 Input interface and resource caps

The Python entry point is `recognize(problem, limits=Limits())`. The problem is an exact built-in dictionary with exactly the keys `N`, `p`, `r`, `omega`, and `x`. The four headers are exact built-in integers; booleans and integer subclasses are excluded. The raw vector is an exact built-in list or tuple of exactly $N$ exact built-in integers, each a canonical residue in $\{0,\ldots,p-1\}$.

The domain is $N\ge2$, $1\le r<N$, supplied prime $p$, $N\mid(p-1)$, and supplied canonical $\omega$ of exact order $N$. This implementation verifies primality by trial division and verifies exact order by generating the root powers. It does not discover the field or root. Validation of all raw coordinates, primality, and root order precedes zero-vector acceptance. The $N=1$ and $r\ge N$ branches discussed separately in Section 9 are outside this API. The order-$2N$-root curvature extension is also excluded.

The default limits are $N\le128$, $r\le64$, $\operatorname{bitlen}(p)\le32$, and 2,000,000 metered work units. Configurable limits are exact nonnegative integers and cannot exceed the hard caps $512$, $128$, $64$ bits, and 20,000,000 units, respectively. A zero limit is permitted, although it can prevent all nontrivial completions. Satisfying the dimension and modulus-width limits does not guarantee completion within the work limit; prime validation can itself exhaust that budget.

The JSON command-line interface accepts one finite record of at most 1 MiB. It rejects duplicate keys, nonfinite numeric constants, malformed UTF-8 or JSON, and trailing JSON values. A zero exit code reports transport completion, not membership. The Python input object is assumed already resident. This is not Appendix A's gamma-coded bit-record parser, and the CLI byte cap is not a network timeout. Ordinary runtime or operating-system failures are not promised to become status results.

### B2 Decision and output meanings

**MEMBER.** Parameters and every raw coordinate have passed validation. One representation in family (1) has been checked by full raw synthesis. The result also contains every positive-sign unnormalized DFT value in (2), evaluated densely from the original raw vector. The empty representation is used for zero. Returned phases satisfy $0\le a<N/\gcd(2,N)$; this is a canonical range, not a uniqueness assertion.

**NONMEMBER.** Every canonical phase has been rejected after valid parameter preparation. Both representation and transform are null. This is a completed nonmembership decision; it does not supply the rejected vector's transform.

**INVALID_INPUT.** A malformed record, unexpected key, unsupported raw container or type, wrong length, or noncanonical coordinate was detected. **INVALID_PARAMETERS.** A header, domain, primality, root, or limit-configuration failure was detected. Neither status means signal nonmembership.

**LIMIT.** A dimension, width, work, or CLI-byte cap prevented completion. The outcome is indeterminate and supplies neither representation nor transform, even if a legal representation had been found before dense DFT output finished. The first detected condition controls: LIMIT does not establish input validity, and progress flags or an earlier accepted-phase log do not turn it into MEMBER. An internal arithmetic invariant failure raises an exception rather than being relabeled NONMEMBER.

The cyclic eliminant is only a phase filter. For each surviving phase, dense Hankel rank and leading-block recovery, distinct supplied-grid roots, ordinary unwrapped recurrence checks, and weight recovery are followed by full synthesis against the raw input. Periodic-prefix instances with $2r>N$ are included. The final output is installed only after its last dense DFT write succeeds.

### B3 Arithmetic and checker boundaries

Let $L=N/\gcd(2,N)$ and $B=\operatorname{bitlen}(p)$. The reviewed dense bound is $O(L(r^3+Nr)+N^2+N)$ field additions and multiplications before inversion internals, $O(Lr)$ scalar inversions, and $O(LrB)$ additional implemented Fermat-inversion multiplications. The accepted-output $N^2$ term is absent on NONMEMBER. Live arrays use $O(N+r^2)$ field entries plus $O(L)$ phase records. Trial division and ordinary integer/control work are separate. These bounds describe the reviewed reference; they do not replace the all-length or dyadic bounds of Theorem 1.

The deterministic ledger instruments validation, root preparation, attempted and rejected phases, recovery arithmetic, inversions and their exponentiation work, full synthesis, and accepted output writes. It is not a processor-time measure, complete bit-cost RAM accounting, or a process-memory limit. Python object construction, copies, comparisons, JSON processing, allocations, set operations, and interpreter overhead are not each completely charged. Appendix A's separate representation and paid-address assumptions remain necessary for its bit-cost conclusion.

The separate checker imports no recognizer code. For MEMBER it independently validates parameters, phase and mode legality, all raw synthesis values, and every dense DFT entry. For NONMEMBER it independently tests Fourier support at every canonical phase; it does not rely on the recorded eliminant or rejection reasons. Its VERIFIED statuses certify the mathematical decision, not execution telemetry, per-phase rejection explanations, or runtime claims. The canonical-JSON digest is a content binding, not authentication or input validation. The checker enforces $N\le512$, $r\le128$, and $\operatorname{bitlen}(p)\le64$, with a default 2,000,000-term budget configurable up to 20,000,000. It can return CHECKER_LIMIT for a valid certificate.

### B4 Review evidence and implementation status

The independent controls in [16] passed 643,632 differential decisions, including 640,921 exhaustive raw vectors checked against explicit generation of the target family. They also passed 1,366 recognizer cutoffs, 802 checker cutoffs, and 27 corrupted-certificate controls. A separate full-rank $N=512$, $r=128$ case passed; removing the last work unit needed for its final dense DFT write produced LIMIT with both public outputs withheld. The pinned author suite replayed without failure. These are recorded finite controls, not fresh experiments in this manuscript integration or timing evidence for an asymptotic theorem.

The accepted milestone is a bounded dense exact reference. Fast Toeplitz construction, blocked verification, the dyadic dispatcher, and Gauss-output integration remain outside this implementation review. No production-readiness, measured-speedup, new bit-cost theorem, numerical-robustness, historical-priority, constant-round, or general-purpose FFT claim follows.

## Appendix C Strengthened antecedent comparisons

The unknown common-quadratic-phase model, polynomial-phase aliases, dechirping, Prony and annihilating-filter recovery, and Hankel-pencil formulations have established antecedents. Complex chirp identification has also been formulated using structured two-dimensional spectral lifting with rank and positivity constraints. The result studied here supplies a particular cyclic polynomial filter that is nonzero at every chosen nonzero raw center, with degree at most $\binom{r+2}{3}$, and combines it with an exact supplied-prime-field membership algorithm for all $1\le r<N$ and an explicit full-input, failed-candidate and accepted-output cost contract. Historical priority of the complete combination remains unresolved.

The nine component comparisons below follow the audit [17] as corrected and accepted by [18]. A matching component or model specialization does not make two complete theorems equivalent. A difference in hypotheses or interfaces does not prove superiority or originality. The source locators record the scope of the underlying primary-text inspection; no fresh external proof audit, source-PDF byte verification, or missing-formula reconstruction is claimed here.

### C1 Shared phase models and rank formulations

**S1 Barbarossa, Scaglione and Giannakis [19].** Section III-B, condition c3, Corollaries 2--3 and the prose introducing equation (24), pp. 694--695, make all component phase coefficients from order two upward agree. The degree-two specialization is a common quadratic factor times a sum of tones. Section IV-A, pp. 697--698, treats two equal-rate chirps and changes lag products in this regime. Condition c3 is the shared-coefficient hypothesis, not itself a lag-selection condition. The noise-free infinite continuous-time assumption concerns the stated PHAF illustration and is not generalized to every part of that paper. The available primary reader omits some displayed formulas, including (24); its surrounding prose supports this model attribution without an invented transcription. The equivalent model component supplies no prime-field every-input decision theorem.

**S2 Shukla, Kundu, Mitra and Grover [20].** Equation (1), p. 1, is a real sine/cosine model with one unknown quadratic coefficient. Assumptions 1--3, p. 3, and Theorems 1--2, pp. 4--5, support consistency and asymptotic-normality results for the described estimators, with the component count supplied. Nonzero amplitude means a nonzero sine/cosine pair, not that each scalar must be nonzero. Expansion into complex exponentials gives both quadratic phase signs, so this real statistical model is not silently identified with the complex common-factor observation model. Neither analytic-signal conversion nor finite-input exact rejection follows from it.

**S3 Yang, Ge and Wang [21].** Equation (2), p. 3, uses the positive phase $\exp(i2\pi(fn+\tau n^2))$. Theorem 4, pp. 4--5, bounds the absolute frequency by $1/2$ and the absolute rate by $\delta<1/2$, and assumes odd $M\ge\max(N,2K+1)$. It characterizes unique identification through unique lifted $Y$ and two-level Toeplitz $T$ satisfying a complex positive-semidefinite block constraint of rank at most $K$, an interval-localizing positive-semidefinite constraint, and $Y_{n,n^2}=y_n$. Section 4 uses numerical convex iteration. Equal rates specialize the representation to a common phase, but positivity, conjugation, absolute amplitudes, and real interval restrictions have no direct $\mathbb F_p$ substitution. Continuous-parameter identifiability differs from returning any verified finite-field representation on every valid input.

The proof of Theorem 2 in [21] gives $y_0y_2/y_1^2=\exp(i4\pi\tau)$. Under the phase-coefficient dictionary $\tau=a/N$, the accepted rank-one eliminant root is its reciprocal, $\omega^{-2a}$. This credits the established curvature identity without transferring uniqueness or assigning an earliest date to that identity from the 2025 source.

### C2 Aliases and phase conventions

**S4 Yang and Xi [22].** Section II-C, p. 3, explicitly gives identical integer samples for two normalized parameter pairs differing by one half in both frequency and quadratic coefficient. The positive exponent is $\exp(i2\pi(fn+\theta n^2))$; the exact dictionary is $f=b/N$, $\theta=a/N$, with no factor of two in $\theta$. These are phase coefficients, not instantaneous-frequency slopes.

For even $N$, the dictionary yields $(a,b)\mapsto(a+N/2,b+N/2)$ modulo $N$. The exponent difference is $(N/2)j(j+1)$, a multiple of $N$. This is an integer-exponent identity in the supplied cyclic root group, not an embedding of complex numbers into $\mathbb F_p$. The assumptions $N\ge2$ and $N\mid(p-1)$ force odd $p$; for even $N$, $\omega^{N/2}=-1$. No inverse of two modulo even $N$ is used. The same translation applies to every component with unchanged weights. Canonicalization removes this universal redundancy but does not establish mixture uniqueness or include the order-$2N$-root family.

Section II-B, equations (4)--(9), p. 2, supplies the structured two-dimensional spectral reformulation. Proposition 3.1, p. 3, gives an SDP lower bound with equality under its stated rank condition. Theorem 3.1, p. 4, separately supplies a conditional dual-certificate result. Neither result is an unconditional every-input finite-field recognizer. The HTML version numbers these results III.1.

**S7 McKilliam [25].** Chapter 7, Theorem 7.1, printed p. 108 (one-based PDF page 126), characterizes integer-sample polynomial-phase aliases by an integer-valued difference polynomial. Corollaries 7.1--7.2, printed p. 109 (PDF page 127), give multiplicative and lattice forms. The polynomial $(j^2+j)/2$ explains the simultaneous half-shift; changing the linear sign gives the same shift modulo integers. This is an established alias structure, not an attribution of the locally used nonvanishing determinant normalization to that theorem. The separate 2009 journal body's access status remains unchanged.

### C3 Recovery and shared parameter elimination

**S5 Potts and Tasche [23].** The noiseless lemmas assume distinct nonzero complex nodes and nonzero weights, with $M\le L\le n$ and $2n$ samples. Lemma 2.1, author-PDF p. 5, gives Hankel rank $M$; Lemma 2.2, p. 6, relates node annihilation, the linear recurrence system, and the shifted-Hankel companion identity. See also equation (1.5), p. 3, annihilating filters, p. 8, and Algorithms 3.1--3.2, pp. 10--12. These polynomial and Vandermonde identities apply algebraically to distinct supplied finite-field nodes after dechirping. Complex SVD/QR thresholds and numerical guarantees are not transferred. Periodic reuse for $2r>N$ belongs to the accepted local interface; it does not make Prony new. The inequality removed in their QR discussion is not CHIRP's former witness-placement condition.

**S6 van der Hoeven and Lecerf [24].** Section 5, Algorithm 4 and equation (10), p. 14, give an explicit finite-field sparse-interpolation antecedent. A black-box polynomial with degree and sparsity bounds is sampled on a geometric progression; a minimal rational generating function is recovered, followed by roots, exponents, and coefficients. The source explicitly identifies fast Padé approximation. Its denominator roots are $\omega^{-e_i}$, reciprocal to the exponential nodes $\omega^{e_i}$. With fixed phase, $P(z)=\sum_b\gamma_bz^b$ and $y_j=P(\omega^j)$ give the corresponding finite-field Prony structure. An enumerated root grid is not a generic discrete-log breakthrough. Algorithm 4's order requirement of at least $\max(D,2T)$ does not itself authorize the local $2r>N$ periodic-prefix interface; identical complete algorithms or costs are not claimed.

**S8 Agostini, Améndola and Ranestad [1].** Section 4.3, equations (79)--(80), the following degree/root paragraph, and equation (81) transform ordinary moments through a trial common variance and zero a Hankel determinant. The stated degree is $\binom{k+1}{2}$ in $\sigma^2$, not in $\sigma$. Smallest-nonnegative-root selection is attributed there to Lindsay's Theorem 5B. This establishes a related shared-parameter elimination pattern, not equality with entrywise dechirping of fixed raw finite-field ordinates. No reduction preserving those exact interfaces was established, and the original Lindsay theorem remains unread.

**S9 Plonka, Stampfer and Keller [2].** Section 4 supplies the known factor $H$ and divides it out. Theorem 4.1, pp. 14--15, supplies $\beta$ in shifted Gaussian chirps, assumes nonzero weights and distinct real shifts, and recovers from $2M$ uniform samples; purely imaginary $\beta$ requires the stated alias-avoiding step restriction. Theorem 5.3, p. 19, uses square-root sample locations for different quadratic coefficients. Section 6.2 and Theorem 6.2, pp. 24--25, use paired real cosine/sine data. These are relevant recovery antecedents with different supplied-factor or sampling interfaces. The Cuyt--Lee, Toeplitz, convolution, and Gauss comparisons in Section 8 remain in force.

### C4 Exact remaining comparison and source gaps

The corrected F6 feature is: a uniformly nonzero cyclic eliminant at any nonzero raw coordinate, degree at most $\binom{r+2}{3}$ with a sharp worst-case bound for this eliminant, and leading-minor constants $x_c^k$. The constant-vector example proves sharpness for this chosen polynomial; it does not say that every raw input attains the maximum degree or that the degree is optimal among all certificates. None of the inspected comparisons establishes historical equivalence of this simultaneous guarantee and the complete supplied-grid decision/cost contract. That is an unresolved comparison, not evidence that no antecedent exists. Simple exhaustive phase enumeration with Fourier-support checking already gives a decision baseline, so mere existence of an exact recognizer is not a novelty claim.

The inherited gaps remain precise: Derin (1987), full pp. 142--148 [5]; Lindsay (1989), original Theorem 5B, its hypotheses and proof/context [6]; and Applebaum, Howard, Searle and Calderbank (2009), complete pp. 283--290 [7]. Kumaresan and Verma, *On estimating the parameters of chirp signals using rank reduction techniques*, Asilomar 1987, pp. 555--558, is an additional original-body target. Its bibliography is verified in [19], reference [15], p. 707; its actual rank-reduction construction, common-rate mixture hypotheses, trial-dechirped determinant, nonvanishing, and failure behavior remain unestablished. No theorem is inferred from its title.

The audit's Wang--Zhou (1998) and Xia (2000) original-body access limits also remain, including the unread DCFT comment/response context. The Peter thesis pages 85--91 mentioned in Section 8 remain outside the inspected evidence. Searchable primary-reader passages supported the stated Potts--Tasche, van der Hoeven--Lecerf, and McKilliam comparisons; this is not possession or hashing of their public PDF bytes. Missing formulas have not been filled in, and unavailable bodies or search misses do not support a worldwide-priority claim. The nine accepted component comparisons do not certify originality or publication readiness.

### C5 Added primary references

19. Barbarossa, Scaglione and Giannakis. *Product High-Order Ambiguity Function for Multicomponent Polynomial-Phase Signal Modeling*. IEEE Transactions on Signal Processing 46(3), 691--708 (1998). [DOI 10.1109/78.661336](https://doi.org/10.1109/78.661336). [Author-uploaded primary text](https://www.researchgate.net/publication/3316755_Product_high-order_ambiguity_function_for_multicomponent_polynomial-phase_signal_modeling).

20. Shukla, Kundu, Mitra and Grover. *On estimating parameters of a multi-component Chirp Model with equal chirp rates*. 2023 author preprint. [arXiv 2302.07098v1](https://arxiv.org/pdf/2302.07098v1).

21. Yang, Ge and Wang. *Pursuing the Limit of Chirp Parameter Identifiability: A Computational Approach*. 2025. [arXiv 2507.01286v1 HTML](https://arxiv.org/html/2507.01286v1); [versioned PDF](https://arxiv.org/pdf/2507.01286v1).

22. Yang and Xi. *Gridless Chirp Parameter Retrieval via Constrained Two-Dimensional Atomic Norm Minimization*. 2025. [arXiv 2503.15164v1 HTML](https://arxiv.org/html/2503.15164v1); [versioned PDF](https://arxiv.org/pdf/2503.15164v1).

23. Potts and Tasche. *Parameter estimation for nonincreasing exponential sums by Prony-like methods*. Linear Algebra and its Applications 439 (2013), 1024--1039. [Author PDF](https://www-user.tu-chemnitz.de/~potts/paper/LAA_Prony.pdf).

24. van der Hoeven and Lecerf. *Sparse polynomial interpolation: Faster strategies over finite fields*. Final author version, 2 May 2024. [Primary PDF](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf).

25. McKilliam. *Lattice theory, circular statistics and polynomial phase signals*. University of Queensland doctoral thesis, December 2010. [Primary thesis](https://robbymckilliam.github.io/papers/thesis.pdf).

## Appendix D Version and source bindings

Version 3 preserves the v2 mathematical body and Appendix A, with the subtitle updated and Appendices B--D added. The original 33 numbered equations and all six supplementary numbered displays are unchanged. No author identity is supplied. The separate v2 integration review accepted its preservation and corrected bit-contract fidelity. This v3 candidate still requires its own independent integration-fidelity review; the underlying theorem, bit supplement, bounded reference, and substantive antecedent comparisons retain their recorded scopes.

### D1 Implementation sources

**[15]** *CHIRP Bounded Exact Recognizer CANDIDATE*, 11 October 2026. Immutable source Library identity `libfile_bf879c07b8208191a33e55429d9675ca`, version 1. Archive SHA-256:

f0f6ab4c1601a2875d48aa61c48fd347154357b95f21cf41e0de351d0a61c9db

The review archive [16] preserves this exact source ZIP and its code. The recognizer `chirp_exact.py` SHA-256 is:

7d263f616526bd1123658771afc73bb44fc15282ef8ee0131e48ade0b59d18b7

The separate `check_certificate.py` SHA-256 is:

556337c6bc1f4215d1782f82fb63bfd67771152a442af1688bf91080f763699f

**[16]** *CHIRP Bounded Exact Recognizer Independent Review PASS*, 11 October 2026. Library identity `libfile_bdc15bd8232881919496a838a30f85b5`, version 0. The controlling members are `REVIEWED_STATEMENT.md` and `REPORT.md`; the code is preserved under `candidate/`. Archive SHA-256:

0f90f725ab1a2952929f0332e30f04a9dd9ea135c16352e136cc9cfd9fc084af

### D2 Antecedent and preservation sources

**[17]** *CHIRP Recognizer Theorem Level Antecedent Audit*, 11 October 2026. Library identity `libfile_68163fef2fe08191bfe157e7abca1bc2`, version 0. Archive SHA-256:

94996424d3869a8fcb648b2e983106dd39d9264c520d98762f622acdcd86ad1e

**[18]** *CHIRP Antecedent Comparison Independent Review*, 11 October 2026. Library identity `libfile_8d3df32de6fc8191b6dedc3a5bc22a69`, version 0. Its `REVIEW.txt` controls the F6 degree repair and the nine comparison qualifications. Archive SHA-256:

bbb5abaeb3fd940aedb58ac9ebd8322b640000e106ae06dbe2e87fec5d2699c3

The v2 source package is Library `libfile_a23ba3a27bcc8191ac8f5b5f96c03ae2`, version 0, SHA-256:

478ba14a1ac8a0d54aef65016e3631e8f8fe74f8292703973d9ff088ec1d3e46

Its accepted integration review is Library `libfile_d5b7a4869f948191998dd9aea73ef80c`, version 0, SHA-256:

ee4fbb7c4f674d22c390d88107407970de6102512121d454b79cb417dd573c41

The accompanying preservation package contains these exact archives and the v1/v2 originals, source text, build instructions, member hashes, and the candidate's preservation and rendering checks. Hashes bind supplied artifact bytes, not authorship, external publication priority, public-paper PDF bytes, or a new review verdict. No research program in the preserved archives was executed during this document integration.
