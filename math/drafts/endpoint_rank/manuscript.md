# Fourier Rectangle Rank and Dyadic Endpoint Minimax

**DRAFT for mathematical review — 10 October 2026**

## Abstract

Let $U$ be the unitary-normalized character table of a finite abelian group of order $N$. We bound the rank and low-rank approximation error of every rectangle $U[R,H]$ in terms of the largest nontrivial translation autocorrelation of its column set. A single complementary-Gram moment calculation gives both estimates. For an abelian $2$-group of order $N=4L\ge8$, it implies that every $(2L-1)\times(2L+1)$ rectangle has rank at least $L+1$, with an explicit positive lower bound on its $(L+1)$-st singular value. For cyclic dyadic Fourier matrices, an exact cut-rank recurrence in double-bit-reversal order supplies a matching upper bound. Consequently the minimum, over independent row and column orderings, of the maximum off-diagonal cut rank is $N/4+1$.

The offset dimensions are essential: arbitrary half-size square cyclic Fourier blocks have minimum rank $N/4$. We give applications to common-coordinate factorization budgets and rank-controlled rectangles obtained from independently routed inverse sums, with the relevant scaling and model restrictions. Double digit reversal and its rank-one hierarchy are established in Delvaux–Van Barel [DV08, Lemma 7]; their Theorem 9 already implies the critical-rectangle lower bound at $N=8$. The general minimax and quantitative deficit statements are distinct from the statements of that article. Their worldwide priority is not settled here.

## 1 Notation and scope

All analytic statements are over $\mathbb C$. Let $G$ be a finite abelian group, written additively, of order $N\ge2$, with identity $0$ and character group $\widehat G$. A character $\chi:G\to\mathbb C$ has modulus one. Define

\[
U[\chi,x]=N^{-1/2}\chi(x),\qquad \chi\in\widehat G,\quad x\in G.
\tag{1.1}
\]

Character orthogonality makes $U$ unitary. A different consistent sign convention conjugates the table and leaves all conclusions unchanged. For $R\subseteq\widehat G$ and $H\subseteq G$, write

\[
r=|R|,\quad h=|H|,\quad I=\widehat G\setminus R,
\quad n=N-r,\quad V=U[R,H].
\tag{1.2}
\]

Unless explicitly stated otherwise, $1\le r,h\le N$. Coordinate subsets have their inherited Euclidean norms. The spectral norm is $\|\cdot\|_2$, the Frobenius norm is $\|\cdot\|_F$, and singular values are listed in nonincreasing order. When a matrix has $h$ columns, its singular-value list can be padded with zeros to length $h$, by using the eigenvalues of its $h\times h$ Gram matrix. Every rank is an ordinary matrix rank over the stated field.

For an $N\times N$ matrix $M$ in one specified coordinate order, put

\[
q(M)=\max_{1\le k<N}
\left\{\operatorname{rank}M[0:k,k:N],
\operatorname{rank}M[k:N,0:k]\right\}.
\tag{1.3}
\]

Intervals are half-open, with indices $0,\ldots,N-1$. If $N=1$, set $q(M)=0$. For permutations $\rho,\sigma$, choose the convention $P_\rho[i,\rho(i)]=1$; thus

\[
(P_\rho M P_\sigma^{T})[i,j]=M[\rho(i),\sigma(j)].
\tag{1.4}
\]

The row and column permutations in an endpoint minimum are independent. Inside a product, however, $q$ always refers to the same displayed coordinate order.

For cyclic $G=\mathbb Z/N\mathbb Z$, use

\[
\omega_N=e^{2\pi i/N},\qquad F_N[a,b]=\omega_N^{ab},
\qquad U_N=N^{-1/2}F_N.
\tag{1.5}
\]

Normalization has no effect on exact ranks. All numerical singular-value and error bounds below are for $U$ or $U_N$; for $F_N$, multiply them by $\sqrt N$.

## 2 A deficit bound for every Fourier rectangle

### 2.1 Translation autocorrelation

For $s\in G$, define

\[
c_H(s)=|H\cap(H-s)|,
\qquad
d_H=h-\max_{s\ne0}c_H(s).
\tag{2.1}
\]

Equivalently, $c_H(s)$ counts the ordered pairs $x,y\in H$ with $y-x=s$. We have $c_H(0)=h$, $c_H(s)=c_H(-s)$, and $0\le d_H\le h$. Moreover $d_H=0$ exactly when $H$ has a nonzero translation stabilizer: equality $c_H(s)=h$ is equivalent to $H+s=H$.

Define the two complementary quantities

\[
B_H=\frac{h(N-r)}N-\frac{d_Hr(N-r)}{N^2},
\qquad
K_H=h-B_H=\frac{rh}N+\frac{d_Hr(N-r)}{N^2}.
\tag{2.2}
\]

The quantity $d_H$ is a property of the actual column set. A cardinality hypothesis will sometimes give a lower bound for it, but is not required in the theorem.

### Theorem 2.1 General finite abelian deficit estimate

For every rectangle $V=U[R,H]$ defined above,

\[
\operatorname{rank}V\ge\lceil K_H\rceil
=\left\lceil\frac{rh}N+\frac{d_Hr(N-r)}{N^2}\right\rceil.
\tag{2.3}
\]

If $t$ is an integer with $0\le t<K_H$, then

\[
\sigma_{t+1}(V)\ge
\left(1-\sqrt{\frac{B_H}{h-t}}\right)^{1/2}>0.
\tag{2.4}
\]

Consequently every matrix $W$ of the same dimensions and rank at most $t$ satisfies

\[
\|V-W\|_2\ge
\left(1-\sqrt{\frac{B_H}{h-t}}\right)^{1/2}.
\tag{2.5}
\]

The transposed estimates also hold. More explicitly, let

\[
d_R=r-\max_{\psi\in\widehat G\setminus\{1\}}
|R\cap(\psi R)|,
\quad
B_R=\frac{r(N-h)}N-\frac{d_Rh(N-h)}{N^2}.
\tag{2.6}
\]

Then the rank lower bound can be replaced by the larger of (2.3) and

\[
\left\lceil\frac{rh}N+\frac{d_Rh(N-h)}{N^2}\right\rceil.
\tag{2.7}
\]

When $t<r-B_R$, (2.5) has the additional valid lower bound

\[
\left(1-\sqrt{\frac{B_R}{r-t}}\right)^{1/2}.
\tag{2.8}
\]

Use the larger of the valid positive error bounds.

#### Proof

On $\mathbb C^H$, form the complementary Gram matrix

\[
A=U[I,H]^*U[I,H].
\tag{2.9}
\]

The columns of the full table are orthonormal, so

\[
0\preceq A\preceq I_h,
\qquad V^*V=I_h-A.
\tag{2.10}
\]

Here $\preceq$ denotes the positive-semidefinite order. Write

\[
f_I(s)=\sum_{\chi\in I}\chi(s).
\tag{2.11}
\]

For $x,y\in H$, the entry $A[x,y]$ is $N^{-1}f_I(y-x)$. Since $A$ is Hermitian,

\[
\begin{aligned}
\operatorname{tr}(A^2)
&=\sum_{x,y\in H}|A[x,y]|^2\\
&=N^{-2}\sum_{s\in G}c_H(s)|f_I(s)|^2.
\end{aligned}
\tag{2.12}
\]

Character orthogonality gives

\[
\sum_{s\in G}|f_I(s)|^2=Nn,
\qquad f_I(0)=n.
\tag{2.13}
\]

For $s\ne0$, use $c_H(s)\le h-d_H$ in (2.12). Separating $s=0$, we obtain

\[
\begin{aligned}
\operatorname{tr}(A^2)
&\le N^{-2}\{hn^2+(h-d_H)(Nn-n^2)\}\\
&=\frac{hn}{N}-\frac{d_Hrn}{N^2}=B_H.
\end{aligned}
\tag{2.14}
\]

By (2.10), the nullity of $V$ equals the multiplicity of the eigenvalue $1$ of $A$. Each such eigenvalue contributes $1$ to $\operatorname{tr}(A^2)$, whereas every other contribution is nonnegative. Hence

\[
\operatorname{rank}V
=h-\dim\ker V
\ge h-\operatorname{tr}(A^2)
\ge h-B_H=K_H.
\tag{2.15}
\]

Taking the ceiling proves (2.3).

For the singular-value claim, let $a_1\ge\cdots\ge a_h\ge0$ be the eigenvalues of $A$. The eigenvalues of $V^*V$, in nonincreasing order, are $1-a_h,\ldots,1-a_1$. Thus

\[
\sigma_{t+1}(V)^2=1-a_{h-t}.
\tag{2.16}
\]

The first $h-t$ eigenvalues of $A$ are all at least $a_{h-t}$, whence

\[
(h-t)a_{h-t}^2\le\operatorname{tr}(A^2)\le B_H.
\tag{2.17}
\]

The hypothesis $t<K_H=h-B_H$ says exactly that $B_H<h-t$. Equations (2.16)–(2.17) prove (2.4), including strict positivity. The rank result ensures $t+1\le\operatorname{rank}V\le\min(r,h)$, so the singular value in question is not a formal padded value.

For completeness, no approximation theorem needs to be taken as an external premise. Let $E$ be the span of $t+1$ orthonormal right singular vectors belonging to the largest singular values of $V$. If $\operatorname{rank}W\le t$, the restriction $W|_E$ has a nonzero kernel. Choose a unit vector $x\in E\cap\ker W$. Then

\[
\|V-W\|_2\ge\|(V-W)x\|_2=\|Vx\|_2\ge\sigma_{t+1}(V).
\tag{2.18}
\]

This proves (2.5). Finally $U^T$ is a normalized character table of $\widehat G$ after identifying $G$ with its double dual. Apply the same argument with $R,H$ interchanged. Transposition preserves singular values and rank, giving (2.6)–(2.8). ∎

If $r=N$, then $A=0$, $B_H=0$, and every singular value of $V$ is $1$, as the theorem states. If $d_H=0$, (2.3) reduces to the familiar flat-unitary stable-rank bound $\operatorname{rank}V\ge\lceil rh/N\rceil$. That elementary bound also follows directly from $\|V\|_F^2=rh/N$, $\|V\|_2\le1$, and $\|V\|_F^2\le\operatorname{rank}(V)\|V\|_2^2$.

### Corollary 2.2 Cardinality conditions

If $G$ is a $p$-group and $p\nmid h$, then $d_H\ge1$. More generally, for any finite abelian $G$, the condition $\gcd(h,N)=1$ implies $d_H\ge1$.

Indeed, translation by a nonzero $s$ has orbits all of length $\operatorname{ord}(s)>1$. If $H+s=H$, then $H$ is a union of these orbits and $\operatorname{ord}(s)\mid h$. This is impossible when $G$ is a $p$-group with $p\nmid h$, and is also impossible when $\gcd(h,N)=1$, because $\operatorname{ord}(s)\mid N$. Since $d_H$ is an integer, it is at least $1$.

In particular, every $s\times s$ block of a $p$-group character table with $p\nmid s$ has rank at least

\[
\left\lceil\frac{s^2}{N}+\frac{s(N-s)}{N^2}\right\rceil.
\tag{2.19}
\]

The corresponding approximation estimate uses

\[
B(N,s)=\frac{s(N-s)}N-\frac{s(N-s)}{N^2},
\tag{2.20}
\]

which is a valid upper bound on the complementary second moment when only $d_H\ge1$ is known. If the actual deficit is larger, Theorem 2.1 gives the stronger bound without any coprimality assumption.

## 3 Critical rectangles in abelian two groups

### Theorem 3.1 Universal critical rectangle and singular gap

Let $G$ be a finite abelian $2$-group of order $N=4L\ge8$. For every $R\subseteq\widehat G$, $H\subseteq G$ with

\[
|R|=2L-1,\qquad |H|=2L+1,
\tag{3.1}
\]

the block $V=U[R,H]$ satisfies

\[
\operatorname{rank}V\ge L+1,
\qquad \sigma_{L+1}(V)\ge\delta_N,
\tag{3.2}
\]

where

\[
B_L=L+\frac34+\frac1{4L}+\frac1{16L^2},
\qquad
\delta_N=\left(1-\sqrt{\frac{B_L}{L+1}}\right)^{1/2}>0.
\tag{3.3}
\]

Moreover $\delta_N\sim(2N)^{-1/2}$ as $N\to\infty$ through powers of two.

#### Proof

The number $h=2L+1$ is odd, so Corollary 2.2 gives $d_H\ge1$. Substituting $r=2L-1$, $h=2L+1$, $N=4L$ into Theorem 2.1 gives

\[
K_H\ge
L+\frac14-\frac1{4L}-\frac1{16L^2}
=L+\frac{4L^2-4L-1}{16L^2}>L,
\tag{3.4}
\]

because $L\ge2$. Its ceiling is therefore at least $L+1$. The same substitution gives $B_H\le B_L<L+1=h-L$. Apply (2.4) with $t=L$, using $B_L$ in place of its possibly smaller value $B_H$, to obtain (3.2)–(3.3). This is the same moment proof as in Section 2, not a separate argument.

Finally

\[
\delta_N^2
=\frac{L+1-B_L}
{(L+1)(1+\sqrt{B_L/(L+1)})}.
\tag{3.5}
\]

The numerator tends to $1/4$ and the denominator is asymptotic to $2L$. Hence $\delta_N^2\sim1/(8L)=1/(2N)$. ∎

### Corollary 3.2 Endpoint obstruction and robustness

Give the rows and columns of $U$ any independent orderings. At the cut $k=2L-1$, the upper-right block has precisely the dimensions in (3.1). Consequently

\[
q(P_\rho U P_\sigma^T)\ge L+1
\quad\text{for every }\rho,\sigma.
\tag{3.6}
\]

If a matrix $M$ has upper-right block rank at most $L$ at that cut, then

\[
\|P_\rho U P_\sigma^T-M\|_2\ge\delta_N.
\tag{3.7}
\]

In particular (3.7) holds whenever $q(M)\le L$. Restricting rows and columns is multiplication by coordinate contractions, so the full-matrix error is at least the block error from (2.5). This proves the corollary.

The lower bound covers every finite abelian $2$-group. No matching upper ordering for every noncyclic such group is asserted.

## 4 Exact cyclic dyadic endpoint minimax

For $N=2^m$, let $b_m$ reverse the $m$ binary digits of an integer in $[0,N$); let $b_0(0)=0$. Define the double-bit-reversed, unnormalized Fourier matrix

\[
Q_N[i,j]=\omega_N^{b_m(i)b_m(j)},
\quad
r_N(k)=\operatorname{rank}Q_N[0:k,k:N],
\tag{4.1}
\]

including $r_N(0)=r_N(N)=0$. Double digit reversal and the simultaneous hierarchy of rank-one Fourier blocks are classical [DV08, Lemma 7, p. 1596]. The calculation below supplies the precise off-diagonal cut ranks needed for this minimax problem.

### Proposition 4.1 Cut recurrence including odd cuts

For $N=4L=2^m$ with $m\ge2$, and $0\le k\le2L$,

\[
r_N(k)=\left\lceil\frac{k}{2}\right\rceil
+r_L\left(\left\lfloor\frac{k}{2}\right\rfloor\right).
\tag{4.2}
\]

For every $0\le k\le N$,

\[
r_N(k)=r_N(N-k).
\tag{4.3}
\]

#### Proof of the recurrence

Put $p=\lfloor k/2\rfloor$ and $\varepsilon=k-2p\in\{0,1\}$. The first $2L$ bit-reversed natural frequency labels are even and occur in pairs

\[
b_m(2j)=2a_j,\qquad
b_m(2j+1)=2a_j+2L,
\quad a_j=b_{m-2}(j),\quad0\le j<L.
\tag{4.4}
\]

Thus the selected $k$ rows consist of $p$ complete pairs and, when $\varepsilon=1$, the first row of the next pair. Since the bit-reversed order puts all even natural labels before all odd natural labels, every odd natural-time column remains in the suffix $[k,N$).

Consider these odd columns first. Write their natural labels as $c=2\ell+1$, $0\le\ell<2L$. In the complete pair associated with $a_j$, their two entries are

\[
\omega_N^{2a_jc},\qquad
\omega_N^{(2a_j+2L)c}=-\omega_N^{2a_jc}.
\tag{4.5}
\]

On one coordinate from each complete pair, together with the additional coordinate if present, their entries have the form

\[
\omega_{2L}^{a_j}\omega_L^{a_j\ell}.
\tag{4.6}
\]

The $p+\varepsilon$ residues $a_j\pmod L$ are distinct. The corresponding rows of $F_L$ are linearly independent, and multiplying them by nonzero phases does not change their rank. As $\ell$ ranges, the odd columns therefore span a subspace $W\subseteq\mathbb C^k$ of dimension $p+\varepsilon=\lceil k/2\rceil$.

Let $S:\mathbb C^k\to\mathbb C^p$ add the two coordinates in each complete row pair and discard the extra unpaired coordinate, if one exists. Equations (4.5) show $W\subseteq\ker S$; both spaces have dimension $k-p=p+\varepsilon$, so $W=\ker S$. Thus $S$ realizes the quotient by the entire odd-column span.

For an even natural-time column $c=2\ell$, the $j$-th coordinate after applying $S$ is

\[
2\omega_L^{a_j\ell},\qquad0\le j<p.
\tag{4.7}
\]

The even columns that remain have positions $k,\ldots,2L-1$. In pair positions $2t,2t+1$, their natural labels divided by two are $a_t,a_t+L$. Modulo $L$, their distinct residues are therefore exactly

\[
a_p,a_{p+1},\ldots,a_{L-1}.
\tag{4.8}
\]

This assertion includes the odd-cut case $k=2p+1$: the first member of the $p$-th column pair has been removed, but its second member at position $2p+1$ remains. Its residue $a_p$ must be retained. Dropping that residue would give an incorrect recurrence.

Repeated residues merely repeat quotient columns. After removing repetitions and the common factor $2$, equations (4.7)–(4.8) give exactly the block $Q_L[0:p,p:L]$. Since the full selected column span contains $W$, its dimension is

\[
\dim W+\dim S(\text{selected column span})
=p+\varepsilon+r_L(p).
\tag{4.9}
\]

This proves (4.2), including $p=0$ or $p=L$.

#### Proof of reflection

Let $J$ reverse the $N$ coordinate positions, and put

\[
D=\operatorname{diag}(\omega_N^{b_m(i)})_{i=0}^{N-1}.
\tag{4.10}
\]

Bit reversal obeys $b_m(N-1-i)=N-1-b_m(i)$. Reducing the resulting exponent modulo $N$ gives

\[
JQ_NJ=\omega_N DQ_ND.
\tag{4.11}
\]

Thus simultaneous coordinate reflection changes $Q_N$ only by invertible diagonal factors. Reflection takes its upper-right cut at $k$ to its lower-left cut at $N-k$. The matrix $Q_N$ is symmetric, so the lower-left and upper-right blocks at the same cut have equal rank. This proves (4.3). ∎

### Theorem 4.2 Exact endpoint minimax

For $N=2^m\ge8$,

\[
\boxed{
\min_{\rho,\sigma\in S_N}q(P_\rho F_NP_\sigma^T)
=\frac N4+1.}
\tag{4.12}
\]

Double bit reversal attains the minimum. The same equality holds with $U_N$ in place of $F_N$.

#### Proof

Write $N=4L$. The lower bound $L+1$ follows from Corollary 3.2. For the upper bound, first consider $0\le k\le2L$. The elementary dimension bound $r_L(a)\le L-a$, combined with (4.2), gives

\[
\begin{array}{ll}
k=2a:&r_N(k)=a+r_L(a)\le L,\\
k=2a+1<2L:&r_N(k)=a+1+r_L(a)\le L+1.
\end{array}
\tag{4.13}
\]

Reflection covers the second half of the cuts. Symmetry covers both orientations. At the specific cut $k=2L-1$, $p=L-1$, and the remaining block $Q_L[0:L-1,L-1:L]$ is a nonzero single column with at least one row because $L\ge2$. Therefore

\[
r_N(2L-1)=L+r_L(L-1)=L+1.
\tag{4.14}
\]

This proves the exact upper value and hence (4.12). The recurrence has the harmless base matrices $Q_1=(1)$ and $Q_2=F_2$. The restriction $N\ge8$ matters for the formula: at $N=4$, double bit reversal has maximum cut rank $1$, not $N/4+1=2$. ∎

### Characteristic zero and field limitations

The exact cyclic rank equality also holds over any characteristic-zero field $K$ containing a primitive $N$-th root $\zeta$, with $F_N=(\zeta^{ab})$. Every relevant minor belongs to the cyclotomic subfield $\mathbb Q(\zeta)\subseteq K$. Whether such a minor vanishes is unchanged by field extension and by an embedding of that cyclotomic field in $\mathbb C$. Its image is a primitive complex root; choosing a different primitive root amounts to an invertible relabeling of cyclic frequencies. The minimax equality follows.

This argument does not require an embedding of all of $K$ into $\mathbb C$. It also does not establish the theorem in every finite characteristic. In particular, the positive-semidefinite, moment, and singular-value arguments are complex analytic; no finite-field approximation statement is intended.

## 5 Half size squares give a tight countercontrol

### Proposition 5.1 The balanced square minimum

For every integer $N=4L\ge4$,

\[
\min_{|R|=|H|=2L}\operatorname{rank}F_N[R,H]=L.
\tag{5.1}
\]

#### Proof

Every normalized $2L\times2L$ Fourier block has squared Frobenius norm $(2L)^2/N=L$ and operator norm at most $1$. Hence its rank is at least $L$.

For equality, take all even row labels and all even column labels. Their entries are

\[
F_N[2a,2b]=\omega_N^{4ab}=\omega_L^{ab},
\qquad 0\le a,b<2L.
\tag{5.2}
\]

Each residue modulo $L$ occurs twice along each axis. This is $F_L$ with duplicated rows and columns, so its rank is exactly $L$. ∎

Thus the critical rectangle in Theorem 3.1 cannot be replaced by an arbitrary balanced half-size square. There is no conflict with Theorem 4.2: $q$ maximizes over all cuts, and its universal obstruction occurs at the offset cut $N/2-1$. The even column set in (5.2) has a nontrivial translation stabilizer, so its deficit is zero, consistently with Theorem 2.1.

## 6 Applications with explicit model restrictions

### 6.1 Products measured in one coordinate order

For square matrices of the same size,

\[
q(AB)\le q(A)+q(B).
\tag{6.1}
\]

At any cut, block multiplication gives $(AB)_{12}=A_{11}B_{12}+A_{12}B_{22}$; its rank is at most $\operatorname{rank}B_{12}+\operatorname{rank}A_{12}$. The corresponding formula for $(AB)_{21}$ proves (6.1). Iteration gives product subadditivity.

In particular, if an exact factorization of a cyclic dyadic Fourier matrix is written

\[
P_\rho F_NP_\sigma^T
=S_sP_{s-1}S_{s-1}\cdots P_1S_1,
\tag{6.2}
\]

then, in that displayed common coordinate order,

\[
\sum_{j=1}^{s}q(S_j)
+\sum_{j=1}^{s-1}q(P_j)\ge L+1.
\tag{6.3}
\]

If the budget on the left is at most $L$, the same product cannot approximate any endpoint ordering of $U_N$ within operator error $\delta_N$. The latter conclusion also holds for a normalized abelian $2$-group character table of order $4L\ge8$, using only Corollary 3.2.

All internal permutations must be charged by their actual cut ranks. Independent minimization of the two endpoints does not make interstage reorderings free. These statements constrain a particular matrix invariant of a factorization; they do not identify that invariant with arithmetic-operation count, memory traffic, or FFT runtime.

### 6.2 Diagonal scales and absolute error

Let $D,E$ be invertible diagonal matrices and let

\[
T=D(P_\rho U P_\sigma^T)E,
\quad d_{\min}=\min_i|D_{ii}|,
\quad e_{\min}=\min_j|E_{jj}|.
\tag{6.4}
\]

If the critical cut of $M$ has rank at most $L$, the same is true of $D^{-1}ME^{-1}$. Hence

\[
\delta_N
\le\|P_\rho UP_\sigma^T-D^{-1}ME^{-1}\|_2
\le\frac{\|T-M\|_2}{d_{\min}e_{\min}},
\tag{6.5}
\]

so

\[
\|T-M\|_2\ge d_{\min}e_{\min}\delta_N.
\tag{6.6}
\]

The same argument applies to the general rectangle estimates. Dividing by $\|T\|_2\le d_{\max}e_{\max}$ gives the valid relative-error lower bound $\delta_N/(\kappa_2(D)\kappa_2(E))$. A condition number by itself cannot prescribe an absolute error scale: multiplying the whole target by a small nonzero scalar also scales every absolute error. Dense changes of basis do not generally preserve cut rank and are not covered by this diagonal-scaling argument.

### 6.3 A rank controlled rectangle interface

Suppose an approximant $M$ has a selected rectangle $M[R,H]$ of rank at most $t$. Theorem 2.1 immediately gives a necessary condition for exact equality $M=U$:

\[
t\ge\left\lceil\frac{rh}N+\frac{d_Hr(N-r)}{N^2}\right\rceil.
\tag{6.7}
\]

Whenever $t<K_H$, the whole-matrix operator error is at least the right-hand side of (2.5). All previous block-rank upper bounds survive further restriction of rows and columns. Thus if an argument supplies an $m\times m$ rank-at-most-$t$ block of a $p$-group Fourier target, one may choose any $1\le s\le m$ with $p\nmid s$ and use

\[
t\ge\left\lceil\frac{s^2}N+\frac{s(N-s)}{N^2}\right\rceil
\tag{6.8}
\]

as an additional exact obstruction. For a $2$-group, the largest odd $s\le m$ is always available when $m\ge1$. Its approximation counterpart is

\[
\|U-M\|_2\ge
\left(1-\sqrt{\frac{B(N,s)}{s-t}}\right)^{1/2},
\quad t<s-B(N,s),
\tag{6.9}
\]

with $B(N,s)$ from (2.20). Trimming may weaken the numerical conclusion, so retain also the untrimmed stable-rank obstruction $t\ge\lceil m^2/N\rceil$. For example, at $N=64$, $m=s=21$, (6.8) gives $8$, whereas the untrimmed stable-rank ceiling gives $7$.

### 6.4 Independently routed inverse sums

Here is a self-contained sufficient condition for the interface in Section 6.3. Let

\[
M=\sum_{i=1}^{b}L_iQ_i^{-1}R_i,
\tag{6.10}
\]

where $b,q\ge1$ are integers, each $Q_i\in\mathbb C^{N\times N}$ is invertible, and each endpoint $L_i,R_i$ has support contained in a permutation graph, with arbitrary weights including zeros. Routes may differ independently between branches. Let the undirected support graph of

\[
H_i=\begin{pmatrix}0&Q_i\\Q_i^T&0\end{pmatrix}
\tag{6.11}
\]

have the following property: for every nonnegative vertex weighting used below, deletion of at most $q$ vertices leaves every connected component with at most half the original total weight. Requiring this for every nonnegative weighting is sufficient.

Starting with $m_0=N$, define

\[
m_{j+1}=\left\lceil\frac{m_j-q}{3}\right\rceil,
\qquad 0\le j<b,
\tag{6.12}
\]

and suppose $m_j\ge4q$ at every step. Then there are target row and column sets of size $m_b$ for which the block of $M$ has rank at most $t=qb$. If an arbitrary diagonal matrix is added to (6.10), the same conclusion holds when starting from disjoint row and column sets of size $m_0=\lfloor N/2\rfloor$, provided the same step conditions hold. The diagonal vanishes on these sets and every subsequent restriction.

We include the argument to make the application independent of an unproved separator assertion. For any invertible $d\times d$ matrix $A$, and index sets $S,T$, complementary inverse-block nullity gives

\[
\operatorname{rank}A^{-1}[S,T]
=\operatorname{rank}A[T^c,S^c]+|S|+|T|-d.
\tag{6.13}
\]

Indeed, the kernel on the left corresponds under $z=A^{-1}y$ to vectors $z$ supported on $S^c$ satisfying $(Az)|_{T^c}=0$. The respective kernel dimensions are equal; rank-nullity gives (6.13). No principal block is assumed invertible.

If a separator $X$ leaves component unions $A_0,B_0$ with no edges between them, then the complementary matrix in (6.13) for $S=A_0,T=B_0$ has a zero $A_0\times B_0$ block and only $|X|$ extra rows and $|X|$ extra columns. Its rank is at most $2|X|$, so the inverse cross block has rank at most $|X|\le q$. Apply this observation to (6.11), whose inverse has $Q_i^{-1}$ in its lower-left block. Restricting to lower-row and upper-column vertices bounds the desired inverse rectangle. Endpoint weights cannot increase rank.

For the selection step, mark the routed images of $m$ current target rows red on the lower side of (6.11), and the routed images of $m$ current target columns blue on the upper side. They are distinct vertices, regardless of the branch's permutations. Mark positions even when the associated endpoint weight is zero. A half-separator leaves each component with at most $m$ marks. At most $q$ marks of either color were deleted; trim each color to $t_0=m-q$ remaining marks. Since $m\ge4q$, each component has at most $m\le4t_0/3$ retained marks and their total is $2t_0$.

Partition the components into two unions with each union containing between $2t_0/3$ and $4t_0/3$ marks in total. If a component already has weight at least $2t_0/3$, use it as one union. Otherwise accumulate components until reaching $2t_0/3$; this first passage is below $4t_0/3$. In either case the complement has the required bounds.

If the first union has $a$ red and $c$ blue marks, the second has $t_0-a,t_0-c$. At least one oriented cross pair $(a,t_0-c)$ or $(t_0-a,c)$ has both entries at least $t_0/3$. Otherwise the four possible combinations of failures imply either that one union has fewer than $2t_0/3$ marks, or that two numbers adding to $t_0$ are both less than $t_0/3$, a contradiction. Integrality permits choosing $\lceil t_0/3\rceil$ target rows on one side and equally many target columns on the other. Their branch block has rank at most $q$, by (6.13).

Apply this step in turn to each branch. Previously obtained rank bounds persist under restriction. The final sum therefore has rank at most $qb$, proving (6.12) and its diagonal variant. Substituting this $t$ and the actual selected sets into (6.7)–(6.9) is the asserted Fourier application.

The selection need not return an odd side length; legal trimming is therefore essential when using only the $2$-group cardinality argument. The deficit improvement does not assert a stronger universal asymptotic branch exponent, an optimal separator threshold, or a logarithmic lower bound at fixed positive approximation tolerance. The branch grammar (6.10) also differs from a product FFT factorization. No unrestricted FFT lower bound follows.

## 7 Relation to the final Delvaux and Van Barel article

The primary comparison in this section is with the final journal article [DV08], not only its earlier technical-report version. The supplied final article is identified in the companion source index. The following distinctions concern that particular article; they are not a worldwide novelty determination.

### 7.1 Established hierarchy and uncertainty results

Double digit reversal and its simultaneous rank-one block partitions are [DV08, Lemma 7, p. 1596]. The upper ordering in Section 4 uses exactly that classical structure. The explicit recurrence, reflection, and odd-cut residue bookkeeping explain its use for this endpoint minimax; they do not make the ordering itself new.

For a matrix $F$, define its support frontier by

\[
H_F(d)=\min\{|\operatorname{supp}(Fx)|:
x\ne0,\ |\operatorname{supp}x|\le d\}.
\tag{7.1}
\]

This is the one-vector quantity formalized in [DV08, Definition 6 and equation (18), pp. 1594–1595]. Their Theorem 9, pp. 1598–1599, states for $N=p^m$ that

\[
cp^k\le d<(c+1)p^k,\quad1\le c\le p-1,
\quad0\le k<m
\quad\Longrightarrow\quad
H_{F_N}(d)=(p-c+1)p^{m-k-1}.
\tag{7.2}
\]

These interval parameters cover $1\le d<N$; the endpoint $H_{F_N}(N)=1$ is immediate. Remark 10 on p. 1599 gives further equality-set information: at the extremal output size in (7.2), the possible output support is a union of $p-c+1$ residue classes modulo $p^{k+1}$, all within one residue class modulo $p^k$. Thus the article gives more than a cardinality-only support formula.

The prime Fourier full-spark theorem appears as [DV08, Theorem 4 and Remark 5, pp. 1592–1593], where it is credited to Chebotarev. Basic support uncertainty appears in their Theorem 1 and Lemma 2, pp. 1588–1589. These are classical antecedents, not contributions of this draft.

### 7.2 The genuine overlap at order eight

At $N=8$, every critical block is $3\times5$. Transpose it to a $5\times3$ block. If its rank were at most $2$, a nonzero vector supported on those three columns would have Fourier transform supported on at most the three omitted rows. But [DV08, Theorem 9] gives $H_{F_8}(3)=4$, a contradiction. Thus the $N=8$ critical-rectangle lower bound $3$ is already a corollary of that theorem. The matching ordering comes from the established hierarchy. This overlap is not excluded from the comparison.

### 7.3 General rank and quantitative statements

If an $r\times h$ Fourier block has rank $k<h$, some $k+1$ of its columns are dependent, so necessarily

\[
H_{F_N}(k+1)\le N-r.
\tag{7.3}
\]

When also $k<r$, transposition similarly gives $H_{F_N}(k+1)\le N-h$. For the critical rectangle and the hypothetical rank $k=L$, the dyadic formula gives $H_{F_N}(L+1)=4$. For $N\ge16$, both complementary sizes $2L+1$ and $2L-1$ exceed $4$. Therefore this direct scalar support substitution does not exclude rank $L$; Remark 10 is not an equality statement at those larger complementary sizes either.

This identifies a precise limitation of that direct substitution. It does not prove logical independence from every possible deduction using the article or the wider uncertainty literature. In contrast, Theorem 2.1 directly controls the entire eigenvalue-one eigenspace of a complementary Gram contraction. It yields the deficit-sensitive all-rectangle bound, the abelian $2$-group extension, and a positive quantitative singular-value constant. Those displayed formulas and the all-independent-order dyadic minimax are not stated in [DV08]. Their statements and proof route are distinct relative to that source.

There is no claim that the deficit estimate uniformly improves every classical uncertainty theorem. For example, at prime $N=7$, [DV08, Theorem 4] makes every $3\times3$ minor full rank, whereas the cardinality-only substitution $d_H\ge1$ in (2.3) gives only $2$. The results address different information and may be used together.

### 7.4 Remaining priority and scope questions

The final article's Remark 13 and reference [1] point to Delvaux–Van Barel's general Kronecker-product paper [DV07]. A full broader priority comparison must include that work and the literature on generalized support weights, quantitative uncertainty, Fourier restriction ranks, and ordering-dependent low-rank structure. The completed comparison with [DV08] does not settle those questions.

The mathematical claims of this draft are the statements proved in Sections 2–6. Their proofs do not depend on a negative literature search. No claim is made of all-finite-field validity, a matching upper minimax construction for every noncyclic abelian $2$-group, a uniform strengthening of all uncertainty principles, or an unrestricted arithmetic lower bound for the FFT.

## References

**[DV08]** Steven Delvaux and Marc Van Barel. *Rank-deficient submatrices of Fourier matrices*. Linear Algebra and its Applications **429** (2008), 1587–1605. DOI: [10.1016/j.laa.2008.04.043](https://doi.org/10.1016/j.laa.2008.04.043). Final journal article; the printed-page and theorem references in Section 7 were checked against the supplied final text. The double-digit-reversal antecedent is Lemma 7, p. 1596; the support frontier and equality-set statements are Theorem 9 and Remark 10, pp. 1598–1599.

**[DV07]** Steven Delvaux and Marc Van Barel. *Rank-deficient submatrices of Kronecker products of Fourier matrices*. Linear Algebra and its Applications **426** (2007), 349–367. Bibliographic details verified in [DV08, reference 1, p. 1605]. Listed as a required broader comparison source; no fresh full comparison of [DV07] is asserted in this draft.

**Draft provenance.** The mathematical development integrates the supplied general deficit proof, the accepted endpoint theorem and full bit-reversal proof, and the completed final-article comparison. Exact source locations, hashes, theorem-to-source mapping, and the scope of newly authored regression controls are recorded in `source_certificate_index.md`. Those provenance records are separate from the proofs above. No supplied research program was executed or imported to establish the claims.
