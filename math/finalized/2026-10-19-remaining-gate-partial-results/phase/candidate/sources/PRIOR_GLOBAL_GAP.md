# Exact remaining global continuous-phase component

The proven periodic-sector theorem and explicit witness are in `PROOF.md`. This file specifies the missing problem; it is **not an infeasibility certificate**.

## 1. Algebraic constants

Let

\[
t=\sin^2(\pi/16)
\]

be the unique real root in

\[
0.0380602337443566219<t<0.0380602337443566220
\]

of

\[
128t^4-256t^3+160t^2-32t+1=0.
\]

Work over the real algebraic coefficient field K=Q(t), in that isolated embedding. It contains r=sqrt(2)=16t^2−16t+2>0.

Define the exact tables indexed by m=0,...,7:

\[
C_m=(1,r/2,0,-r/2,-1,-r/2,0,r/2)_m,
\]
\[
S_m=(0,r/2,1,r/2,0,-r/2,-1,-r/2)_m.
\]

These are cos(pi*m/4) and sin(pi*m/4).

## 2. Variables and equations

There are 78 real variables:

- a_j,b_j for j=0,...,7, representing p_j=a_j+i b_j (16 variables);
- u_k,v_k for k=1,...,7, representing q_k=u_k+i v_k (14 variables);
- T_jl for j=0,...,7 and l=0,...,5 (48 variables).

Set u_0=1,v_0=0. Fixing q_0=1 loses no phase pair: replace P by q_0 P and Q by conjugate(q_0)Q.

Impose the 15 circle equations

\[
a_j^2+b_j^2=1\quad(0\leq j<8),\qquad u_k^2+v_k^2=1\quad(1\leq k<8),
\]

and the 21 orthonormal-frame equations

\[
\sum_{j=0}^7T_{jl}T_{jm}=\delta_{lm}\quad(0\leq l\leq m<6).
\]

Define the 8-by-8 real polynomial matrix

\[
Y_{jk}=\frac r4\big[(a_jv_k+b_ju_k)C_{jk\bmod8}
-(a_ju_k-b_jv_k)S_{jk\bmod8}\big].\tag{1}
\]

This is precisely Im(PF_8Q), with the required negative Fourier sign and normalization.

Put

\[
M=tI_6-T^TY^TYT,
\]

and let Delta_l denote the determinant of its leading l-by-l principal block, for l=1,...,6.

The six strict inequalities are

\[
\Delta_l>0\qquad(1\leq l\leq6).\tag{2}
\]

They express M positive definite by Sylvester's criterion. Keeping the determinant expressions as a straight-line specification avoids an unnecessary expansion; each is a completely specified polynomial in the stated variables over K. Their degrees in the phase/frame variables are at most 6l, hence at most 36.

## 3. Remove the sector already settled

Define the nonnegative polynomial

\[
N_p=\sum_{j=0}^3\big[(a_j^2-b_j^2-a_{j+4}^2+b_{j+4}^2)^2
+4(a_jb_j-a_{j+4}b_{j+4})^2\big],
\]

and define N_q by replacing a,b,j with u,v,k, again summing k=0,...,3 and using u_0=1,v_0=0. Thus N_p+N_q=0 exactly when both squared phase arrays are four-periodic.

The remaining component includes the strict guard

\[
N_p+N_q>0.\tag{3}
\]

The periodic-sector theorem proves that the complementary zero set cannot satisfy (2). Consequently adding (3) changes neither existence nor nonexistence of a global counterexample.

## 4. Exact equivalence to the missing lower inequality

Let H=Y^TY have eigenvalues lambda_1>=...>=lambda_8. The min-max theorem gives

\[
\lambda_3=\min_{T^TT=I_6}\lambda_{\max}(T^THT).
\]

Therefore the equations and inequalities (1)–(2) have a real solution if and only if some arbitrary phase pair satisfies

\[
\sigma_3(Y)<\sqrt t=\sin(\pi/16).
\]

The forward implication follows by the min-max theorem; for the reverse implication choose the six orthonormal eigenvectors belonging to lambda_3,...,lambda_8. By the periodic theorem any such solution automatically satisfies (3).

Thus the exact remaining task is to decide emptiness of the stated 78-variable real semialgebraic set (36 equality constraints, six leading-minor strict inequalities, and one nonperiodicity strict inequality), over the specified real algebraic field.

- A rigorous emptiness certificate, together with the existing witness, would prove delta_1=sin(pi/16) globally.
- A feasible exact point would refute that proposed global value. It would not by itself identify the new global optimum.
- A reduction theorem forcing a global minimizer into the squared-four-periodic sector is another sufficient route, but is currently unproved.

No quantifier elimination, cylindrical algebraic decomposition, or Positivstellensatz certificate was completed for this component. The numerical searches in the packet do not establish emptiness, and no computational-resource estimate is asserted as if such an elimination had run.
