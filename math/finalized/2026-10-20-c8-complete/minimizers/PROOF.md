# Complete C8 rank-zero minimizer classification

20 October 2026 UTC. Candidate extension of the accepted global optimum; pending independent review.

## Scope and result

Let F[j,k] = exp(-2 pi i j k/8)/sqrt(8), with indices modulo eight. The accepted global value is a premise, not reproved here. Write

    h = sqrt(sqrt(2)-1), k = sqrt(2-sqrt(2)),
    m = (1-h)/2, n = 1-m,
    theta = acos(m), beta = acos(n) = theta-pi/4,
    d = sqrt((1-m)/2), e = sqrt((1-sin(theta))/2).

In particular 0<m<1/2, 0<e<d, and h^2+k^2=1.

The conclusions are:

1. Every minimizing squared-phase pair A=P^2, B=Q^2 is four-periodic. This is stronger than existence of a periodic replacement. The unsquared P,Q need only be four-periodic up to independent real signs.
2. Modulo (A,B) -> (g A,g^{-1} B), |g|=1, there are exactly 32 minimizing squared-phase pairs. Explicit formulas are given below.
3. These 32 pairs form one orbit under the natural Fourier-compatible row/column cyclic translations and conjugation with Fourier reversal. Thus the accepted witness generates every minimizing phase pair under these symmetries, scalar gauge, and real square-root signs. This is an algebraic classification, not a finite-grid assertion.
4. The full original model has additional continuous real-core freedom. For each minimizing P,Q, the complete family of nearest real cores is a two-by-two matrix norm ball described in Section 7. Arbitrary invertible real-monomial gauges recover every original L,C,R representation.

The broader owner PHASE-DEFECT-RANK remains open. No positive correction-rank assertion is made.

## 1. Strict equality in the scalar inequality

We use the accepted sharp inequality: for a positive two-by-two contraction R with every entry at least m,

    sum arcsin(R_ij) <= 2 asin(m)+2 asin(1-m).

Here is its complete equality case, extracted from the accepted pair-balancing proof.

For R=[[a,b],[c,d0]], let t=sqrt((1-a)(1-d0)). The first balancing inequality is

    asin(b)+asin(c) <= 2 asin(t).

Equality requires norm(R)=1: otherwise increasing b,c together to the norm-one boundary strictly increases the left side. On that boundary the accepted proof has q=bc<=t^2 and a strictly decreasing function of q for the cosine of the angle sum. Thus equality forces q=t^2; the boundary identity then gives (b+c)^2=4bc. Hence b=c=t. Conversely these conditions give equality.

The balanced contraction is [[a,t],[t,d0]]. Applying the same equality criterion to its column swap [[t,a],[d0,t]] shows that equality in the second balancing step forces a=d0=1-t. Finally t belongs to [m,1-m], and

    f(t)=asin(t)+asin(1-t)

is strictly convex on (0,1), with equal values at the two endpoints. Because m<1/2, equality in the endpoint bound requires t=m or t=1-m. Consequently the only equality matrices are

    [[m,n],[n,m]]  and  [[n,m],[m,n]].                 (1)

All implications are necessary because each step in the accepted inequality is in the same direction. The converse is immediate.

## 2. Complete equality conditions for a periodic pair

For four-periodic A,B write their first four entries a0,a1,a2,a3 and b0,b1,b2,b3. Define

    alpha=(a0+a2)/2, beta0=(a0-a2)/2,
    gamma=(a1+a3)/2, delta=-i(a1-a3)/2.

The four accepted exact unitary blocks, in sector order even,+; even,-; odd,+; odd,-, are

    M0=[[alpha,beta0],[beta0,alpha]] diag(b0,b2),
    M1=[[gamma,delta],[delta,-gamma]] diag(b0,b2),
    M2=[[beta0,alpha],[alpha,beta0]] diag(b1,b3),
    M3=[[delta,-gamma],[-gamma,-delta]] diag(b1,b3).

The sector bases are

    (e_j+eta e_{j+4})/sqrt(2),
    (e_{j+2}+eta e_{j+6})/sqrt(2),

for j=0,1 and eta=+1,-1. Put p_i=|tr M_i|/2. The accepted trace contraction is K=[[p0,p1],[p2,p3]].

Assume Herm(F A F B)>=m I. Choose the two actual principal eigenphases of M_i in [-theta,theta], and write them as sigma_i +/- beta_i, beta_i>=0. Then

    beta_i=acos(p_i),  |sigma_i|+beta_i<=theta,
    sigma0+sigma3-sigma1-sigma2 = pi/2 modulo pi.

The accepted scalar and determinant estimates now squeeze the same number:

    4 theta-pi/2 <= sum_i beta_i
                       <= 4 theta-sum_i |sigma_i|
                       <= 4 theta-pi/2.

Every inequality is equality. Section 1 gives (1) for K. The two sectors with p_i=m have beta_i=theta and sigma_i=0. The two sectors with p_i=n have beta_i=beta and |sigma_i|=pi/4. They occupy the same sign in the signed determinant sum, so that identity forces their midpoints to have the same sign: both are epsilon pi/4, epsilon in {+1,-1}.

Therefore a four-periodic pair is minimizing if and only if its complex sector traces are one of

    (tr M0,tr M1,tr M2,tr M3)
       = 2(m,n eta,n eta,m),
    or = 2(n eta,m,m,n eta),

    where eta=exp(i epsilon pi/4), epsilon in {+1,-1}. (2)

For sufficiency, a two-by-two unitary with nonzero trace 2p exp(i sigma), p>0, has determinant exp(2i sigma). This follows by writing its eigenvalues exp(i t1),exp(i t2) and squaring the phase of their nonzero sum. Its eigenvalues are exp(i sigma)(p +/- i sqrt(1-p^2)). Thus (2) places all eigenphases in [-theta,theta] and attains both endpoints.

In every case the full spectrum has six eigenvalues whose real part is m, and two whose real part is sin(theta)>m. More precisely it is

    exp(i theta) twice, exp(-i theta) twice,
    exp(i epsilon theta) twice,
    exp(i epsilon (pi/2-theta)) twice.               (3)

There is no branch ambiguity in (2) or (3).

## 3. Equality in normalization forces actual periodicity

We isolate the equality statement needed for the accepted normalization lemma.

Let Z be unitary, T diagonal with 0<=T<=I, and suppose Herm(Z T)>=m I and Herm(Z)>=m I. For a unit eigenvector x of Z with Re(lambda)=m, normality gives

    m <= x* Herm(Z T) x = m x* T x <= m.

Since m>0, equality holds and (I-T)x=0. Therefore T_jj=1 at every coordinate j on which the critical spectral subspace

    Ecrit = ker(Herm(Z)-m I)

has nonzero support. In particular T=I if Ecrit has support on every coordinate.

Every periodic minimizing pair has this full-support property. Its two p_i=m sectors are either (M0,M3) or (M1,M2). Each whole two-dimensional sector lies in Ecrit, since both its eigenphases are +/-theta. In the first case these are even,+ and odd,-; in the second they are even,- and odd,+. The orthogonal projector onto their sum has every diagonal entry exactly 1/2. Thus Ecrit has nonzero support on every coordinate.

Now begin with any minimizing pair A,B, without periodicity. The accepted first averaging/normalization step replaces B by a four-periodic D and yields Herm(F A F D)>=m I. Cyclic unitary similarity yields Herm(F D F A)>=m I. The second averaging step writes

    (A+H A H)/2 = A' T_A,

where A' is four-periodic diagonal unitary and 0<T_A<=I, and proves

    Herm((F D F A') T_A)>=m I,
    Herm(F D F A')>=m I.

Both D and A' are periodic. By the accepted global optimum and Section 2, F D F A' is a periodic minimizer and has a full-support critical subspace. The equality statement above gives T_A=I. Equality in the triangle inequality for two unit complex numbers then forces a_j=a_{j+4} for every j, and A=A'.

Return to the first step. It wrote (B+H B H)/2=D T_B with Herm((F A F D)T_B)>=m I. We have just proved that A is periodic, so F A F D is now a fully periodic minimizer with full critical support. Hence T_B=I, forcing b_j=b_{j+4} and B=D.

This proves that EVERY optimal A,B is four-periodic. The distinction from the accepted value proof matters: full coordinate support of the final critical subspace is the additional equality ingredient. No assertion of strict improvement at an arbitrary nonoptimal phase point is needed.

For P,Q themselves, A=P^2 and B=Q^2 give only

    P_{j+4}= +/- P_j,  Q_{j+4}= +/- Q_j.

All sixteen square-root signs are independent; they are real diagonal gauges and can be absorbed into the real core. Therefore literal periodicity of every unsquared P,Q or every original monomial exterior is false, although every squared-phase pair is periodic.

## 4. Modulus equality and explicit 32-family parameterization

The contraction K from Section 2 is the entrywise product U o V, where the nonnegative factor U has unit column norms and V has unit row norms. In the accepted angular notation,

    U=[[|cos x|,|cos y|],[|sin x|,|sin y|]],
    V=[[|cos v|,|sin v|],[|cos r|,|sin r|]].

For either equality matrix (1), take l=k0=(1,1)/sqrt(2). Then l^T K k0=1. Equality in the Cauchy-Schwarz proof forces U=V entrywise, since both length-four vectors used there have norm one and nonnegative entries. Hence, if tau=p0 in {m,n},

    |cos x|^2=|cos v|^2=tau,
    |cos y|^2=|cos r|^2=1-tau.

Equivalently, with q=2 tau-1, the four phase ratios have the form

    u=a2/a0=q+i xi_u k,
    v=a3/a1=-q+i xi_v k,
    w=b2/b0=q+i xi_w k,
    z=b3/b1=-q+i xi_z k,                             (4)

where each xi is independently +1 or -1. Here q is either -h or +h and k is the fixed positive constant above.

The following formulas describe exactly all minimizers. Choose tau in {m,n}, choose the four independent signs in (4), and choose |g|=1. Set

    s_tau = +1 if tau=m, and -1 if tau=n,
    epsilon = s_tau xi_u xi_v xi_w xi_z,
    eta = exp(i epsilon pi/4).

If tau=m, set (t0,t1,t2,t3)=(m,n eta,n eta,m).
If tau=n, set (t0,t1,t2,t3)=(n eta,m,m,n eta).
Define the unit phases

    B0 = 4 t0 / ((1+u)(1+w)),
    A1 = 4 t1 / (B0 (1+v)(1-w)),
    B1 = 4 t2 / ((1-u)(1+z)).                        (5)

All denominators are nonzero and every displayed phase has modulus one. Repeat the following four entries twice:

    A = g (1,A1,u,A1 v),
    B = g^{-1} (B0,B1,B0 w,B1 z).                   (6)

To verify the fourth trace, direct substitution gives

    (tr M0)(tr M3) / ((tr M1)(tr M2))
      = -i (xi_u xi_v xi_w xi_z) (tau/(1-tau))^2.    (7)

Indeed (1+u)/(1-u)=i xi_u sqrt(tau/(1-tau)); the corresponding factors for w are the same, while (1-v)/(1+v) and (1-z)/(1+z) equal -i times their signs times that square root. The desired trace ratio in (2) is -i epsilon (tau/(1-tau))^2 when tau=m, and +i epsilon (tau/(1-tau))^2 when tau=n. The definition of epsilon makes these agree. The first three traces were fixed by (5), so the fourth is correct.

Conversely, every minimizing pair is periodic by Section 3, its moduli force (4), its trace midpoints force (2), and (7) forces the stated epsilon. Normalize a0=1 with the scalar gauge. The first three trace equations uniquely give (5), and therefore (6) recovers the pair.

There are exactly 2*2^4=32 normalized pairs: tau distinguishes Re(a2/a0), and the four nonzero imaginary signs distinguish their four ratios. Thus (6) has no duplication after imposing a0=1. The only remaining continuous squared-phase parameter is the scalar gauge g.

## 5. Fourier symmetries, permutations, and conjugation

Let omega=exp(-2 pi i/8), D_a=diag(omega^{a j}), S_a e_j=e_{j+a}, and J e_j=e_{-j}. All S_a and J are real permutation matrices. The exact identities

    S_a F = F D_{-a},  F S_b = D_b F,  J conjugate(F)=F

give norm-preserving transformations of V=P F Q:

- Row translation: V -> S_a V, with

      P' = S_a P S_a^{-1},  Q' = D_{-a} Q.

- Column translation: V -> V S_b, with

      P' = D_b P,  Q' = S_b^{-1} Q S_b.

- Conjugation/reversal: V -> J conjugate(V), with

      P' = J conjugate(P) J,  Q' = conjugate(Q).

These preserve the norm of the entrywise imaginary part. Plain conjugation without the indicated reversal changes the Fourier target and is not asserted to be a target-preserving symmetry. Transposition is also a symmetry because F is symmetric; it exchanges P,Q and transposes the real core.

On the normalized labels (tau;xi_u,xi_v,xi_w,xi_z), one-step row and column translations induce

    R: (tau;a,b,c,d0) -> (1-tau;-b,a,-c,-d0),
    C: (tau;a,b,c,d0) -> (1-tau;-a,-b,d0,-c).

They commute, have order four, and preserve epsilon. Their action of Z4 x Z4 is free. If the powers have odd total parity they change tau. If both powers are even, the nonidentity possibilities flip at least one sign pair. If both powers are odd, their action on the first sign pair is a quarter rotation, so it has no fixed sign pair. Thus each orbit has 16 elements. Exactly 16 labels have either value of epsilon, so each epsilon class is one orbit.

Conjugation/reversal acts as

    (tau;a,b,c,d0) -> (tau;-a,b,-c,-d0),

and flips epsilon. Consequently all 32 normalized pairs form one orbit under these symmetries. The accepted witness has tau=m and signs (+1,-1,+1,+1), so epsilon=-1. It therefore generates the entire classification.

Arbitrary permutations in the original monomial exteriors are handled by real-core absorption, not by claiming that every permutation preserves F. Section 8 spells out this distinction.

## 6. Singular values at every phase minimizer

For V=P F Q=X+iY, with X,Y real, the accepted identity is

    Y^T Y = (I-Herm(V^T V))/2,

and V^T V is unitarily similar to F A F B. The complete phase spectrum (3) gives exactly the singular values

    d with multiplicity six,  e with multiplicity two. (8)

Both are positive. Choose any real singular-value decomposition

    Y = O_L diag(d I6,e I2) O_R^T,

where O_L,O_R are real orthogonal. Independent square-root signs in P,Q merely change these real orthogonal bases and do not invalidate the description.

## 7. All nearest real cores, not just Re(V)

For a fixed minimizing P,Q, the complete set of real C satisfying ||V-C||_2=d is

    C = X + O_L diag(0_6,K2) O_R^T,

    K2 real 2-by-2,  ||K2+i e I2||_2 <= d.            (9)

Proof of necessity: put D=C-X. For a real unit right singular vector v of Y with singular value d,

    ||(-D+iY)v||^2 = ||Dv||^2+d^2 <= d^2,

so Dv=0. Applying the same argument to the adjoint and the six real left singular vectors gives D^T u=0. Thus D has only a lower two-by-two block in these SVD bases. The residual then has blocks i d I6 and -K2+i e I2. Its norm equals d precisely when the second block norm is at most d. Complex conjugation and negation show that this is equivalent to the condition in (9). Sufficiency is immediate from this same block decomposition.

For an entirely real algebraic form, put K2=[[a,b],[c,d0]] and t=d^2-e^2. Condition (9) is equivalent to

    t-a^2-c^2 >= 0,
    t-b^2-d0^2 >= 0,
    (t-a^2-c^2)(t-b^2-d0^2)
       >= (ab+c d0)^2+e^2(b-c)^2.                  (10)

This is the two-by-two positive-semidefiniteness condition for

    t I2-K2^T K2-i e(K2^T-K2).

In particular K2=s I2 is permitted for every real |s|<=sqrt(d^2-e^2). Therefore the real core is not unique; identifying only C=Re(V) would not classify all original minimizers. The set (9) has nonempty interior in the four-dimensional real space of two-by-two matrices, since e<d.

## 8. Recovery of every original monomial representation

The original approximation is L C_orig R with arbitrary invertible complex-monomial L,R and real C_orig. Write

    L=P^* M,  R=N Q^*,

where P,Q are diagonal unitary and M,N are arbitrary invertible real-monomial matrices. Set C=M C_orig N. Unitary exterior invariance gives

    ||F-L C_orig R||_2 = ||P F Q-C||_2.

If an original triple is globally minimizing, contractivity of entrywise imaginary part implies ||Im(P F Q)||<=d. The accepted global minimum forces equality, so P,Q belong to the complete phase classification above; then Section 7 forces precisely (9).

Conversely choose any phase pair from (6), any diagonal-unitary square roots P,Q (all real signs allowed), any core C from (9), and any invertible real-monomial M,N. Then

    L=P^* M,  R=N Q^*,  C_orig=M^{-1} C N^{-1}       (11)

is a minimizing original triple. Equations (6), (9), and (11) are exhaustive.

This includes continuous scalar phase gauge, arbitrary nonzero real scales and signs in the monomial factors, every permitted exterior permutation, the full real-core freedom, and Fourier-compatible conjugation/translation symmetries. The representation is intentionally redundant in M,N and square-root signs, since they are gauge choices rather than different necessary phase patterns.

## 9. Dependencies and verification scope

The only substantive inherited premise is the accepted global value and its exact sector/trace-contraction identities. The strict scalar equality, normalization rigidity, explicit phase classification, symmetry orbit, and core classification above are proved here. No numerical optimizer or sampled phase grid is a proof premise. A fresh checker accompanies this candidate as a supporting control for the finite algebraic formulas and exact identities; it is not a replacement for the quantified arguments.

Sources:

- sources/global_primary_PROOF.md
- sources/global_independent_PROOF.md
- sources/global_independent_REVIEW.md

No external service was modified.
