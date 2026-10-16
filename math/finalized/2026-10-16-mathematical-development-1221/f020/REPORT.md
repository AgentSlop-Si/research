# F020: actual-family ramified deflation and a full-cyclotomic degree filter

16 October 2026 UTC. New mathematical-development candidate, author-checked; independent review pending. External sources and records were read only. No supplied research program was executed.

## Result and boundary

The actual Rogers–Szegő coefficients give a uniform polynomial deflation at the ramified parameter q=1. Put w=q+1, r=floor(m/2), and

- v=ceil(m/2),
- N=m(m+1)(2m+1)/3,
- kappa=m+3 floor(m^2/4)+2 floor(m/4).

Then

    v_w(E_m)=m,
    v_w(R_m)>=3 floor(m^2/4)+2 floor(m/4),
    q^v w^kappa divides Q_m.

The first equality is exact for every m. The R bound is exact at m=1,2,3, but is not asserted exact in general. There is an explicit resultant deflation before the last, smaller lower bound; its reduced coefficient pairs are given below.

Consequently, for every odd d>2m+1,

    phi(d)>N-v-kappa  implies  reduced Phi_d does not divide Q_m.

This is a sufficient full-cyclotomic nondivisibility condition, strictly stronger than the raw degree test. It excludes all primitive components vanishing together in this range; it does not assert a good value at every primitive component. Combined with the accepted discriminant implication, it suffices for the characteristic-zero ordinary residual squarefreeness at the orders it covers. It does not remove the remaining orders, prove the full paired-support statement, establish a broader FFT consequence, or change the OPEN gate.

No historical novelty or publication-priority claim is made. The proof uses elementary continuant matchings, resultant homogeneity, and a local determinant divisibility argument. Its actual-family contribution is the coefficientwise cubic divisibility after one prescribed translation, followed by the explicit residual pairs.

## 1. Source-bound setup

Use precisely the accepted characteristic-two recurrence

    P_0=1, P_1=X+q+q^2,
    P_j=(X+a_j)P_(j-1)+c_j P_(j-2),
    a_j=q^(2j-1)(1+q),
    c_j=(1+q^(2j-1))(1+q^(2j-2)), j>=2.

Split P_m=A_old(X^2)+X B_old(X^2), and set

    E_m=P_m(0), R_m=Res(A_old,B_old), Q_m=E_m R_m.

The accepted identities are Disc_X(P_m)=R_m^2, deg Q_m=N, and v_q(Q_m)=v. This note neither changes the actual-degree reversal Q_m*=q^N Q_m(q^-1) nor replaces Q_m by a single endpoint/collision channel.

The directly read sources were the accepted finalization report and its RECIPROCAL_DESCENT.md and COLLISION_KERNEL.md formula files. Their SHA-256 values are recorded in MANIFEST.json. Baseline supplied by the parent was AgentSlop-Si/research commit de5dc664448d8e3e219df9651b2805d5a2cecbb1. This packet makes no claim that local source copies were freshly compared with that commit.

## 2. Exact endpoint valuation

Every a_j has w-valuation 1. Every c_j has w-valuation at least 3: the odd factor has valuation 1, and 1+q^(2j-2) is divisible by w^2. Thus E_0=1 and E_1=a_1 have valuations 0 and 1. If the valuations at j-1 and j-2 are j-1 and j-2, the two terms in

    E_j=a_j E_(j-1)+c_j E_(j-2)

have valuations exactly j and at least j+1. Their lowest terms cannot cancel. Induction proves v_w(E_m)=m, with leading residue 1.

## 3. A prescribed translation and coefficientwise cubic divisibility

Translate by the actual first diagonal, not an arbitrary spectral value:

    T_m(X)=P_m(X+a_1).

The new diagonals are

    b_j=a_j+a_1=w q (1+q^(2j-2)).

In particular b_1=0. For every j>=2, both b_j and c_j are divisible by w^3. More precisely,

    (b_j/w^3)(1)=(c_j/w^3)(1)=1 if j is even,
    (b_j/w^3)(1)=(c_j/w^3)(1)=0 if j is odd.

For b_j this follows from

    (1+q^(2j-2))/w^2 = ((1+q^(j-1))/w)^2,

whose value at q=1 is j-1 modulo 2. For c_j, the extra quotient (1+q^(2j-1))/w has value 1. This also checks b_1=0 separately.

The path-continuant expansion expresses T_m as a sum over disjoint edges (dimers) and selected unmatched diagonal vertices (monomers), with X on the remaining unmatched vertices. A term contributing to X^(m-k) uses e dimers and s diagonal monomers with 2e+s=k. It contains e+s factors divisible by w^3. Since e+s>=ceil(k/2),

    w^[3 ceil(k/2)] divides [X^(m-k)] T_m.          (3.1)

Cancellation can only increase this valuation. This proves (3.1) at every coefficient, including zeros and the leading coefficient.

## 4. Exact split-resultant deflation

Write T_m(X)=A(X^2)+X B(X^2). Translation preserves the discriminant, and both original and translated split resultants square to that discriminant. Squaring is injective in F2[q], so

    Res(A,B)=R_m.                                 (4.1)

For m=2r, define genuine polynomials by coefficientwise exact division:

    A(w^3 Y)=w^(3r) A_tilde(Y),
    B(w^3 Y)=w^(3r) B_tilde(Y).

Here A_tilde is monic of degree r and B_tilde has generic degree r-1. Equation (3.1) proves that every division is integral. Resultant scaling gives

    R_(2r)=w^(3r^2) Res(A_tilde,B_tilde).          (4.2)

For m=2r+1 with r>=1, define

    A(w^3 Y)=w^[3(r+1)] A_tilde(Y),
    B(w^3 Y)=w^(3r) B_tilde(Y).

Here B_tilde is monic of degree r, and A_tilde has generic degree r. Again all divisions are integral and

    R_(2r+1)=w^[3r(r+1)] Res(A_tilde,B_tilde).     (4.3)

For clarity, the scaling law is Res(f(cY),g(cY))=c^(ab)Res(f,g), where a,b are the generic degrees. Scalar extraction then proves (4.2) and (4.3). No specialization in which a degree drops is used in that argument.

At m=1, translation gives A=0 and B=1. Set the zero-versus-unit resultant to 1, consistently with the monic linear discriminant. Treat this case directly: R_1=1. No division by a zero coefficient or a nonunit specialization is made.

## 5. Explicit residual pairs and an additional uniform factor

A bar denotes reduction of the integral tilde polynomials at w=0. Let epsilon be r modulo 2. The matching expansion used in Section 3 gives

    m=2r:    A_bar=(Y+1)^r,
             B_bar=epsilon (Y+1)^(r-1);

    m=2r+1:  B_bar=(Y+1)^r,
             A_bar=epsilon Y (Y+1)^(r-1).         (5.1)

These formulas are for r>=1. To verify them without relying on a guessed leading form, group the vertices into the r pairs (1,2),(3,4),...,(2r-1,2r), with the final odd vertex left over when m is odd. Only even-index edges survive the minimal valuation; each pair therefore contributes Y+1. A coefficient of the opposite X parity at the minimal valuation requires exactly one diagonal monomer. Only an even-index monomer survives, replacing that pair's Y+1 by X. There are r choices. For odd m, its remaining X multiplies the final unmatched X to produce Y. Terms with at least three diagonal monomers have strictly larger valuation and vanish in (5.1); odd-index edges or monomers also vanish by the residue calculation in Section 3.

If r is even, (5.1) says every coefficient of one tilde polynomial is divisible by w. The other tilde polynomial is monic of degree r, so homogeneity of the resultant gives a further factor w^r.

If r is odd, the reduced pair has gcd exactly (Y+1)^(r-1). Its Sylvester matrix therefore has corank r-1 over F2. A square matrix over F2[q] whose reduction modulo w has corank s has determinant divisible by w^s: apply constant invertible row/column operations reducing its residue to diag(I,0); each of the last s rows then has every entry divisible by w. Thus the tilde resultant is divisible by w^(r-1).

In both cases,

    w^[2 floor(r/2)] divides Res(A_tilde,B_tilde).

Using floor(r/2)=floor(m/4), (4.2)-(4.3) prove

    v_w(R_m)>=3 floor(m^2/4)+2 floor(m/4).        (5.2)

For r=1 the reduced resultants in (5.1) are 1. Hence (5.2) is exact at m=2 and m=3; m=1 was checked separately. For r>=2, no equality is asserted. The reductions explicitly show why further factors can occur; this is not an illegal inference from a vanished norm or from invertible chain edges.

## 6. Full-cyclotomic consequence and its exact scope

By the accepted q-content theorem and Sections 2 and 5,

    Q_hat_m = Q_m / [q^v (q+1)^kappa]

is a nonzero monic polynomial of degree

    B_m=N-v-kappa.

Its factors at every nonzero parameter other than 1 are exactly those of Q_m, with the same multiplicities. In particular for every odd d>2m+1, reduced Phi_d is coprime to q(q+1), so

    reduced Phi_d divides Q_m
      iff reduced Phi_d divides Q_hat_m.         (6.1)

The reduced cyclotomic polynomial is squarefree of degree phi(d), and its roots have exact order d. Therefore phi(d)>B_m rules out (6.1). There is no need to identify inverse Frobenius orbits for this all-components criterion.

The accepted characteristic-zero discriminant implication says that failure of ordinary residual squarefreeness at a primitive odd d-th root forces the entire reduced Phi_d to divide Q_m. Hence the degree criterion proves ordinary residual squarefreeness for those d. It does not imply localized coprimality of Q_m and Q_m*: a proper reciprocal subset of primitive components may still occur. It also does not settle orders with phi(d)<=B_m, or remove the separate overlap-simplicity guard.

This is an infinite all-m order filter with an explicit deflation, not a finite endpoint census or an all-m solution. No status/priority/score change is justified by this packet alone.

## 7. Author-side checks

The self-authored check_packet.py uses only the Python standard library and local polynomial arithmetic. It imports no supplied research program. At the fixed boundary/source controls m=1,2,3,4,12 it checks:

- independent Gaussian q-Pascal reconstruction and trace folding against the accepted recurrence;
- exact endpoint w-valuation;
- every coefficient divisibility (3.1);
- the translated split-resultant identity;
- both exact deflations (4.2)-(4.3);
- every residual coefficient in (5.1), not just resultant values;
- the additional valuation bound and the q^v w^kappa quotient degree;
- exact bound-sharpness at m=1,2,3;
- negative controls rejecting an extra forced power at those sharp boundaries and corrupted residual coefficients.

The development file check_valuation.py is also self-authored. Its initial diagnostic evaluations were valuations only, not endpoint-order support certifications; none is presented as a new finite support stage. RESULTS.json and SHA-256 bindings are retained. These checks do not substitute for the all-m proof or independent review.
