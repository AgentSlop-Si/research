# C8 rank-one positive-error approximation: exact upper witness and periodic-sector theorem

Date: 18 October 2026 UTC. Scope: normalized negative-sign Fourier matrix, unrestricted real core, one complex rank-one correction, operator norm. The unrestricted phase-torus lower bound is **not proved** here.

## 1. Model and accepted reduction

Use zero-based indices and

\[
F_{jk}=8^{-1/2}\exp(-\pi i jk/4),\qquad 0\leq j,k<8.
\]

The quantity in the gate is

\[
\delta_1=\min_{P_o,Q_o\;\mathrm{diagonal\ unitary},\ B\in\mathbb R^{8\times8},\ \operatorname{rank}_{\mathbb C}E\leq1}
\|F-P_o(B+E)Q_o\|_2.
\]

The accepted absorption argument already includes arbitrary invertible complex monomial outer gauges: their real monomial factors can be absorbed into unrestricted real B and into E without changing the represented approximating matrix or the correction rank. No conditioning restriction is introduced.

For completeness, the accepted fixed-phase identity is

\[
\delta_1=\min_{P,Q}\sigma_3(\operatorname{Im}(PFQ)).
\]

Indeed, Im(E) has real rank at most two and entrywise Im is an operator-norm contraction. This gives the lower inequality by the real Eckart–Young theorem. Conversely, any real rank-at-most-two approximant to Im(PFQ) is Im(E) for a complex rank-at-most-one E, using

\[
\operatorname{Im}\big((a_1+i a_2)(b_2+i b_1)^T\big)
=a_1b_1^T+a_2b_2^T.
\]

Choosing B = Re(PFQ−E) gives the reverse inequality. P_o=P* and Q_o=Q* reparameterize the outer phases.

## 2. Explicit rank-one witness at sin(pi/16)

Put

\[
a_0=\pi/16,\quad s=\sin a_0,\quad c=\cos a_0,\quad z=e^{i a_0},
\]

and set

\[
q=(1,z^2,1,z^{10},1,z^2,1,z^{10}),\quad
Q=\operatorname{diag}(q),\quad P=zQ,\quad V=PFQ.
\]

Define the real orthonormal vectors

\[
a=\tfrac12(1,0,-1,0,-1,0,1,0)^T,
\qquad
b=\tfrac12(0,1,0,1,0,1,0,1)^T,
\]

and R=aa^T+bb^T. Writing Y=Im(V), one has the exact identities

\[
Ya=cb,\quad Yb=ca,\quad Y^2=s^2 I+(c^2-s^2)R.\tag{1}
\]

Here V and Y are symmetric. Hence Y has two singular values c and six singular values s. In particular, sigma_3(Y)=s.

An explicit legal correction and real core are

\[
E=c(a+i b)(a+i b)^T,
\qquad
B=\operatorname{Re}V-c(aa^T-bb^T).\tag{2}
\]

E has complex rank exactly one: a+i b is nonzero, c is nonzero, and E is its nonzero scalar outer product. B is real. Let

\[
Y_0=Y-c(ab^T+ba^T).
\]

Then

\[
V-(B+E)=iY_0,\qquad Y_0^2=s^2(I-R).\tag{3}
\]

Since I−R is a nonzero rank-six orthogonal projector, (3) gives ||Y_0||_2=s exactly. Taking

\[
P_o=P^*,\qquad Q_o=Q^*
\]

in the original problem gives

\[
\|F-P_o(B+E)Q_o\|_2=s.
\]

Thus the unrestricted original problem has the rigorous upper bound

\[
\boxed{\delta_1\leq\sin(\pi/16).}\tag{4}
\]

All matrix entries in (1)–(3), all 64 entries of the original external-residual identity, unitarity, and all 784 two-by-two minors of E are checked in exact characteristic-zero arithmetic by the fresh checker. `WITNESS.json` supplies every F,V,B,E and inner-residual entry as coefficients in Q[z]/(z^16+1), with z interpreted as exp(i*pi/16).

The value s is the smallest positive root of

\[
128s^8-256s^6+160s^4-32s^2+1=0,
\]

isolated by

\[
0.1950903220161282678<s<0.1950903220161282679.
\]

This is an algebraic description of the attained upper value, **not a certified defining polynomial for the unrestricted optimum**.

## 3. Four-periodic phases: exact continuous minimization

### Theorem

Restrict phases to

\[
p_{j+4}^2=p_j^2,\qquad q_{k+4}^2=q_k^2\qquad(0\leq j,k<4).
\]

Then

\[
\boxed{\min\sigma_3(\operatorname{Im}(PFQ))=\sin(\pi/16).}\tag{5}
\]

This includes all real-sign variants of four-periodic phases. The proof treats the remaining phases continuously; it is not a phase-grid argument.

### 3.1 Exact block decomposition

Independent real row and column signs make p and q literally four-periodic. Such signs preserve the singular values of the imaginary part.

For r=0,1,2,3 and d=0,1 let

\[
h_r^d=(e_r+(-1)^d e_{r+4})/\sqrt2.
\]

Order the real row basis by h_{c+2u}^d and the real column basis by h_{d+2v}^c, with blocks (c,d)=(0,0),(0,1),(1,0),(1,1), and u,v in {0,1}. The matrix becomes the direct sum of four unitary two-by-two blocks

\[
C_{cd}[u,v]=\frac{p_{c+2u}q_{d+2v}}{\sqrt2}
\exp\left(-\frac{\pi i}{4}(c+2u)(d+2v)\right).\tag{6}
\]

The real transforms commute with taking imaginary parts, so the eight singular values of Y are the union of those of Im(C_cd).

At the witness of section 2, the two diagonal blocks are zH_2, where H_2 is the normalized real Hadamard matrix, while the two off-diagonal blocks are

\[
\frac{z^3}{\sqrt2}\begin{pmatrix}1&i\\-i&-1\end{pmatrix},\qquad
\frac{z^3}{\sqrt2}\begin{pmatrix}1&-i\\i&-1\end{pmatrix}.
\]

Each diagonal block contributes s,s, and each off-diagonal block contributes c,s. This also proves (1)–(3) directly with the displayed a,b.

### 3.2 Four block-angle parameters

Choose real arguments p_j=e^{i alpha_j}, q_k=e^{i beta_k}. For c,d in {0,1} put

\[
A_c=(\alpha_c+\alpha_{c+2})/2,\quad R_c=\alpha_{c+2}-\alpha_c,
\]
\[
D_d=(\beta_d+\beta_{d+2})/2,\quad S_d=\beta_{d+2}-\beta_d,
\]
\[
\theta_{cd}=A_c+D_d-\frac\pi4(cd+c+d),
\]
\[
r_{cd}=(R_c-\pi d/2)/2,\quad s_{cd}=(S_d-\pi c/2)/2.
\]

Then C_cd=e^{i theta_cd} diag(e^{-i r_cd},e^{i r_cd}) H_2 diag(e^{-i s_cd},e^{i s_cd}). In particular

\[
\theta_{00}+\theta_{11}-\theta_{01}-\theta_{10}=-\pi/4.\tag{7}
\]

Define phi_cd in [0,pi/2] by

\[
\cos(2\phi_{cd})=h_{cd},
\]

where

\[
h_{00}=\cos R_0\cos S_0,\quad h_{01}=\sin R_0\cos S_1,
\]
\[
h_{10}=\cos R_1\sin S_0,\quad h_{11}=\sin R_1\sin S_1.\tag{8}
\]

The two singular values of Im(C_cd) are

\[
|\sin(\theta_{cd}+\phi_{cd})|,\qquad
|\sin(\theta_{cd}-\phi_{cd})|.\tag{9}
\]

To verify (9), C_cd^T C_cd has determinant exp(4i theta_cd) and trace 2 exp(2i theta_cd) h_cd. Its eigenvalues are exp(2i(theta_cd±phi_cd)). A symmetric unitary has commuting real and imaginary parts, so they are simultaneously diagonalizable by a real orthogonal matrix. Finally

\[
\operatorname{Im}(C_{cd})^T\operatorname{Im}(C_{cd})
=\tfrac12(I-\operatorname{Re}(C_{cd}^TC_{cd})).
\]

### 3.3 Assume six small singular values

Suppose sigma_3(Y)<sin(pi/16), and set epsilon=arcsin(sigma_3(Y)), so 0<=epsilon<pi/16. Call a block good if both singular values in (9) are at most sin(epsilon). At most two of the eight singular values exceed sin(epsilon), so at least two blocks are good.

For a good block, the two angles theta±phi are each within epsilon of pi*Z. Their difference shows

\[
|h_{cd}|\geq\cos(2\epsilon).\tag{10}
\]

Two adjacent blocks cannot both be good: for a row-adjacent pair, (8) and (10) would imply

\[
1=\cos^2R_c+\sin^2R_c\geq2\cos^2(2\epsilon)>1;
\]

the column argument uses S_d. Therefore exactly two opposite blocks are good, and each of the other two blocks has at least one small singular value. There are precisely two cases.

Write d_L(x)=min_{m in Z}|x−mL| for distance to the lattice L*Z.

### 3.4 Case A: blocks 00 and 11 are good

Real signs on p_2,q_2,p_3,q_3 can arrange cos R_0, cos S_0, sin R_1, sin S_1 to be positive. Choose representatives

\[
R_0,S_0\in[-\pi/2,\pi/2],\qquad
R_1=\pi/2+u,\ S_1=\pi/2+v,\qquad u,v\in[-\pi/2,\pi/2].
\]

Then h_00,h_11 are positive and

\[
0\leq\phi_{00},\phi_{11}\leq\epsilon,
\]
\[
|R_0|,|S_0|\leq2\phi_{00},\qquad |u|,|v|\leq2\phi_{11}.\tag{11}
\]

The two good-block angle conditions give

\[
d_\pi(\theta_{00})\leq\epsilon-\phi_{00},\qquad
d_\pi(\theta_{11})\leq\epsilon-\phi_{11}.\tag{12}
\]

For the other two blocks, (8) gives

\[
\phi_{01}=\pi/4+\tfrac12\arcsin(\sin R_0\sin v),
\]
\[
\phi_{10}=\pi/4+\tfrac12\arcsin(\sin u\sin S_0).
\]

Since |arcsin(sin x sin y)|<=min(|x|,|y|) for x,y in [−pi/2,pi/2], (11) implies

\[
|\phi_{01}-\pi/4|+|\phi_{10}-\pi/4|
\leq2\min(\phi_{00},\phi_{11})\leq\phi_{00}+\phi_{11}.\tag{13}
\]

Each remaining block has at least one small singular value. Thus some independent signs in (9), together with (13), yield

\[
d_{\pi/2}(\theta_{01}+\theta_{10})
\leq2\epsilon+\phi_{00}+\phi_{11}.\tag{14}
\]

On the other hand (12) yields

\[
d_\pi(\theta_{00}+\theta_{11})\leq2\epsilon-\phi_{00}-\phi_{11}.
\]

Combining this with the exact relation (7) gives

\[
d_{\pi/2}(\theta_{01}+\theta_{10})
\geq\pi/4-2\epsilon+\phi_{00}+\phi_{11}.\tag{15}
\]

Equations (14) and (15) force pi/4<=4epsilon, contradicting epsilon<pi/16.

### 3.5 Case B: blocks 01 and 10 are good

This case does not require a symmetry or an unproved sign normalization. Use independent real signs to make sin R_0,cos S_1,cos R_1,sin S_0 positive. Choose

\[
R_0=\pi/2+u,\ S_1=v,\ R_1=w,\ S_0=\pi/2+x,
\qquad u,v,w,x\in[-\pi/2,\pi/2].
\]

Then phi_01,phi_10<=epsilon, with |u|,|v|<=2phi_01 and |w|,|x|<=2phi_10. The other two parameters are

\[
\phi_{00}=\pi/4-\tfrac12\arcsin(\sin u\sin x),
\]
\[
\phi_{11}=\pi/4-\tfrac12\arcsin(\sin w\sin v).
\]

Consequently their deviations from pi/4 sum to at most phi_01+phi_10. Repeat (12)–(15) with the good and other pairs exchanged; (7) has the same absolute pi/4 discrepancy. Again pi/4<=4epsilon, a contradiction.

Both cases are impossible. This proves the lower inequality in (5), and section 2 gives equality.

## 4. Why this does not prove the original global optimum

The accepted rank-only argument forced four-periodicity through equality in the Frobenius-energy bound at hypothetical imaginary rank at most two. A positive-error competitor need not attain the energy minimum, so that implication cannot be reused.

Indeed the upper witness here has

\[
\|Y\|_F^2=2c^2+6s^2=2+4s^2>2.
\]

The missing global statement is

\[
\sigma_3(\operatorname{Im}(PFQ))\geq\sin(\pi/16)
\quad\text{for every pair of arbitrary diagonal unitary }P,Q.\tag{G}
\]

An alternative sufficient theorem would assert that some globally minimizing pair has p_{j+4}^2=p_j^2 and q_{k+4}^2=q_k^2. No such phase-reduction theorem is proved here. Neither the accepted positive rank lower bound nor the finite numerical searches supplies it.

The precise residual semialgebraic feasibility problem equivalent to a counterexample to (G), after the proven periodic sector is removed, is given in `GLOBAL_PHASE_GAP.md`. The terminal status of the original gate is **OPEN: unresolved global continuous-phase lower inequality**.
