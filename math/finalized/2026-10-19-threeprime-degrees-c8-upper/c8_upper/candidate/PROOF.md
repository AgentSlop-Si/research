# An explicit exact upper bound for the C8 rank-zero phase defect

19 October 2026 UTC.

## Result and scope

In the unrestricted complex-monomial, real-core, external-operator-norm model of the accepted C8 rank-zero packet,

\[
\boxed{\sin(3\pi/16)<\delta_{8,0}\leq
\frac{\sqrt{1+\sqrt{\sqrt2-1}}}{2}
=0.641013699718185\ldots.}
\]

The lower bound is the previously accepted strict obstruction. This packet proves the new upper bound by an exact legal witness. It does not claim that the new upper bound is the global optimum. Four-periodicity is imposed only to construct a witness; no all-phase periodicity reduction is assumed. No anti-diagonal shortcut is used.

## 1. Reduction needed for an upper witness

Let F=F8 with F[j,k]=exp(-2 pi i j k/8)/sqrt(8). For any diagonal unitaries P,Q, put V=PFQ and take the real core C=Re(V), outer matrices L=P*, R=Q*. Then

F-LCR=P* (i Im V) Q*,

so the original-model external residual has norm ||Im V||. This uses only admissible diagonal-unitary outer matrices, which are a subset of the allowed invertible complex monomial matrices.

For unitary V=X+iY, the symmetric unitary W=V^T V satisfies

Y^T Y=(I-Re W)/2.

The real and imaginary parts of W are commuting real symmetric matrices, so an eigenvalue exp(i phi) of W contributes sin²(phi/2) to the spectrum of Y^T Y. Here Re W can equivalently mean its entrywise real part or its Hermitian part, because W is symmetric.

If A=P² and B=Q², then W=Q F A F Q is similar to U=F A F B. Thus it is enough to compute the eigenvalues of U exactly.

## 2. Explicit phases

Set

h=sqrt(sqrt(2)-1),
z=h+i sqrt(2-sqrt(2)),
zeta=exp(i pi/4), rho=exp(i pi/8).

Then |z|=1. Write z=exp(i a) with a in (pi/4,pi/2), and let w=exp(i a/2), equivalently

w=sqrt((1+h)/2)+i sqrt((1-h)/2).

Repeat each following list twice along the diagonal:

P=(-i w, rho^(-1) w, 1, rho^(-1)),
Q=(1, rho^3 w^(-1), i w^(-1), rho^3).

These are diagonal unitaries. Their squares are

A=(-z, zeta^(-1)z, 1, zeta^(-1)),
B=(1, zeta^3/z, -1/z, zeta^3),

again repeated twice. This completely specifies the attaining witness for the new upper bound, including a real core C=Re(PFQ), external L=P*, R=Q*, and correction E=0.

## 3. Four invariant sectors and their exact blocks

Write C0=FAF and C0[j,k]=c_(j+k), with indices modulo 8. Since A is four-periodic, c_l=0 for odd l, so parity sectors are invariant. Since B is also four-periodic, U=C0B commutes with the half-shift H e_j=e_(j+4).

For each parity and eta in {+1,-1}, use the basis

(e_j+eta e_(j+4))/sqrt(2), (e_(j+2)+eta e_(j+6))/sqrt(2),

with j=0 for even parity and j=1 for odd parity. Direct Fourier summation gives the four blocks, in the order even,+; even,-; odd,+; odd,-:

M0=[[alpha,beta],[beta,alpha]] diag(b0,b2),
M1=[[gamma,delta],[delta,-gamma]] diag(b0,b2),
M2=[[beta,alpha],[alpha,beta]] diag(b1,b3),
M3=[[delta,-gamma],[-gamma,-delta]] diag(b1,b3),

where

alpha=(1-z)/2, beta=-(1+z)/2,
gamma=zeta^(-1)(1+z)/2, delta=i zeta^(-1)(1-z)/2.

These sector identities are also verified by forming the full exact 8-by-8 Fourier matrix and the real orthogonal sector change of basis in the accompanying independent fresh checker.

Because (z+z^(-1))/2=h, the traces and determinants are:

- M0 and M3: trace 1-h, determinant 1.
- M1 and M2: trace zeta^(-1)(1+h), determinant -i.

Every block is unitary, as a restriction of U to an orthogonal invariant sector.

## 4. Exact spectral radius in phase

Put

c=(1-h)/2, d=(1+h)/2=1-c,
theta=arccos(c), beta0=arccos(d).

Both angles are in (0,pi/2). The first type of block has eigenvalues exp(+-i theta). The second has eigenvalues exp(-i pi/4) exp(+-i beta0).

The identity h²=sqrt(2)-1 gives

(4+2sqrt(2))c(1-c)=1,

and hence

sqrt(1-c²)=sqrt(2)(1-c)-c.

The right side is positive. Therefore

cos(theta-pi/4)=(c+sqrt(1-c²))/sqrt(2)=1-c=d.

Since theta is in (pi/4,pi/2), this proves beta0=theta-pi/4. Consequently the spectrum of U, with multiplicity, is

- exp(i theta), twice;
- exp(-i theta), four times;
- exp(i(theta-pi/2)), twice.

All eigenphases have absolute value at most theta. Since theta>pi/4, |theta-pi/2|<theta, and the largest absolute eigenphase is exactly theta. Thus

||Im(PFQ)||=sin(theta/2)
=sqrt((1-c)/2)
=sqrt(1+h)/2.

The witness therefore attains the claimed upper bound exactly. This is a global legal upper bound regardless of the behavior of nonperiodic phase choices.

## 5. Improvement and remaining problem

The new value is strictly below 1/sqrt(2), since h<1. It lowers the previous upper endpoint by about 0.06609, approximately 9.35 percent.

Determining whether arbitrary nonperiodic phases can improve it remains open in this packet. The numerical search is discovery evidence only and is excluded from the proof. The accepted strict all-phase lower bound remains unchanged. Numerically, the remaining certified interval is 0.555570233019602... < delta_(8,0) <= 0.641013699718185..., of width 0.085443466698583.... The new upper endpoint decreases the previous interval width by approximately 43.61 percent.

## 6. Original computations and complete cost disclosure

All computations in this directory were newly written. No historical code or source-packet checker was executed.

- A 16-start direct Powell search: 23,274 objective evaluations, 0.821 seconds reported computation time; no useful optimum from random starts.
- A 30-start smooth spectral search, with six fixed smoothing levels per start: 5,361 analytic value/gradient evaluations, 1.204 seconds reported computation time. Best smoothed endpoint was about 0.6410589156. This suggested a one-parameter periodic family.
- A fresh bounded scalar minimization in that family located about 0.6410136998; the exact formulas above were derived analytically afterward. This scalar exploratory command was not initially instrumented with an evaluation counter. Its exact count is not known; its SciPy bounded-method default maximum of 500 evaluations gives a conservative hard upper bound. It completed within the returned 0.279-second shell wall time. Thus all numerical discovery work used at most 29,135 objective/value-gradient evaluations. This omission does not affect the exact proof.
- The exact checker performs symbolic Fourier/sector, trace, determinant, phase-square, radical and half-angle identities. An initial run exposed only an incomplete SymPy radical simplification in the P²=A check. The check was strengthened by exact complex expansion; no mathematical formula or witness changed.

The exact checker output records the verified bound and its own runtime. Exploratory artifacts are kept separate from the certificate’s mathematical claims.
