# A strict rank-zero obstruction for C8

19 October 2026 UTC. This packet proves a strict obstruction at the first rank not settled by the accepted cyclic boundary-rank family. It does not determine the exact C8 rank-zero optimum, assert a quantitative gap, establish strictness at every larger order, or make a novelty or FFT-complexity claim.

## 1. Statement and scope

Let

F_N[j,k] = N^(-1/2) exp(-2 pi i j k/N).

Let delta_(N,r) be the minimum external operator norm of F_N - L(B+E)R, over arbitrary real B, arbitrary complex E of complex rank at most r, and arbitrary invertible complex monomial L,R.

**Theorem 1 (strict all-phase obstruction).**

    sin(3 pi/16) < delta_(8,0) <= 1/sqrt(2).

In particular, the accepted even-order lower bound

    delta_(N,r) >= sin(pi(N-4r-2)/(4N))

is not sharp for every smaller correction rank: it is already nonsharp at N=8,r=0. The strict inequality is an analytic all-phase result, not an inference from a numerical sweep. Compactness supplies a positive, but here unquantified, gap.

**Theorem 2 (uniform necessary equality structure).** Let N=4m, L=N/2, theta=pi/2-pi/N, and let A,B be diagonal unitaries. If U=F_N A F_N B has every eigenvalue in the closed arc |arg z|<=theta, then

    a_(j+L)=a_j and b_(j+L)=b_j for every j.

The proof supplies additional complementary Fourier-support information about the two parity-cycle endpoint eigenvectors. For m>=3 these are necessary conditions only; this packet does not show that they are impossible.

## 2. Legal reduction of the original model

Factor any invertible complex monomial outer matrix into a diagonal unitary times an invertible real monomial, with the real monomial on the side adjacent to the core. Absorb both real monomials into the unrestricted real core and the correction. Realness and complex correction rank are preserved. Only diagonal unitaries multiply the external residual, so no condition number or residual-norm distortion is introduced.

For a fixed V and Y=Im V, entrywise imaginary part is a contraction in the complex operator norm, since Im Z=(Z-conjugate Z)/(2i). Thus

    min_(B real) ||V-B||_2 = ||Im V||_2,

with the upper bound attained by B=Re V. In the rank-zero problem E is zero. Therefore

    delta_(N,0) = min_(P,Q diagonal unitary) ||Im(P F_N Q)||_2.   (2.1)

The phase torus is compact and the objective is continuous, so this is a minimum.

For comparison with the accepted general-rank model, the same argument gives sigma_(2r+1)(Im V) when a complex-rank-r correction is allowed. The lower bound uses rank_R Im E<=2r. Conversely, write a best real rank-2r truncation as T=sum_a v_a u_a^T and pair consecutive terms via

    E=sum_l (v_(2l-1)+i v_(2l))(u_(2l)+i u_(2l-1))^T.

Then rank_C E<=r and Im E=T; choosing B=Re(V-E) gives the matching residual. No real-rank/complex-rank interchange is assumed.

If V=P F_N Q is unitary, W=V^T V is symmetric unitary and is similar to

    U=F_N A F_N B,   A=P^2, B=Q^2.

Writing V=X+iY gives

    Y^T Y = (I-Re W)/2.

The real and imaginary parts of W are commuting real symmetric matrices. In their simultaneous real orthogonal eigenbasis, an eigenvalue exp(i phi) of W contributes the singular value |sin(phi/2)| to Y. Consequently, ||Y||<=sin(theta/2), with 0<theta<pi/2, means that all eigenvalues of U lie in |arg z|<=theta. In that case

    Re U := (U+U*)/2 >= cos(theta) I > 0.                  (2.2)

Here Re U is the Hermitian part; it is not an entrywise-real operation unless explicitly stated.

## 3. Closed-arc commutator and endpoint rigidity

Let S e_j=e_(j+1), C=F_N A F_N, and T=B* S B. The cyclic-Hankel relation C S=S* C gives

    K=U T U* T* = S* B* S* B,
    K e_j=(b_j/b_(j-1)) e_(j-2).                         (3.1)

If the spectrum of U lies in |arg z|<=theta<pi/2, then

    ||U-cos(theta)I|| <= sin(theta),
    ||K-I|| = ||U T-T U|| <= 2 sin(theta).

Hence the spectrum of K lies in |arg z|<=2theta.

We also need the following equality statement. If Kx=exp(2i theta)x, then

    Ux=exp(i theta)x.                                   (3.2)

Similarly, an eigenvector of K with eigenvalue exp(-2i theta) is an eigenvector of U with eigenvalue exp(-i theta).

To prove this, put D=T U* T*, so K=UD and D has spectrum in the same theta-arc. For a unit eigenvector x of K at exp(2i theta),

    <x,Dx> = exp(2i theta) <x,U*x>.

Both expectations lie in the convex hull of that theta-arc. That hull lies in the sector of arguments [-theta,theta], strictly in the right half-plane. Its intersection with its rotation through 2theta is just the common boundary endpoint relevant to this equation: necessarily <x,U*x>=exp(-i theta) and <x,Dx>=exp(i theta). One can see this directly from their arguments; wrapping by 2pi cannot create another overlap because theta<pi/2. A convex combination of points on the theta-arc lies on either boundary ray only at the corresponding endpoint. An expectation of modulus one for a unitary forces its vector to be an eigenvector, proving (3.2). The negative endpoint is identical with signs reversed.

For N=2L even, the two parity cycles of K each have length L. Their products are Gamma and Gamma^(-1), where

    Gamma = product_(j even) b_j / product_(j odd) b_j.

Thus chi_K(x)=(x^L-Gamma)(x^L-Gamma^(-1)). If L is even and

    theta=pi/2-pi/(2L),

the permitted K arc has radius 2theta=pi-pi/L. Its complementary open gap has width exactly 2pi/L. An L-point regular polygon can avoid that gap only if the two gap endpoints are consecutive polygon vertices. Therefore both cycles must have the roots of x^L+1, and

    Gamma=-1,  lambda=exp(2i theta),  lambda^L=-1.

Each endpoint lambda and lambda^(-1) occurs once on each parity cycle. This reasoning also proves the usual non-strict lower bound: a strictly smaller theta would make the forbidden gap wider than one polygon spacing.

## 4. Uniform complementary-support rigidity

Assume the hypotheses of Theorem 2. Write N=2L=4m, omega=exp(2pi i/L), and

    lambda=exp(i(pi-pi/L)),  u=exp(i theta).

Then lambda=u^2, lambda^2=omega^(-1), and lambda^L=-1.

Put d_t=b_(2t), e_t=b_(2t+1), with t modulo L. Choose endpoint eigenvectors x and y of K at lambda, supported on even and odd indices respectively. Write their nonzero coordinates as x_t and y_t and normalize x_0=y_0=1. The cyclic recurrence shows that every x_t and y_t has modulus one, and

    x_(t+1)=lambda e_t/d_(t+1) x_t,
    y_(t+1)=lambda d_(t+1)/e_(t+1) y_t.                 (4.1)

By (3.2), Ux=u x and Uy=u y. Multiplying the recurrences gives the useful identities

    e_t x_t y_t = e_0 lambda^(2t),
    d_t x_t y_(t-1) = e_0 lambda^(2t-1).                (4.2)

Define the normalized L-point Fourier transforms

    X_n=L^(-1/2) sum_t x_t omega^(-nt),
    Y_n=L^(-1/2) sum_t y_t omega^(-nt),

and D=F_L(d x), E=F_L(e y). Equations (4.2), using modulus-one coordinates, imply

    D_k=e_0 lambda^(-1) omega^(-k-1) conjugate(Y_(-k-1)),
    E_k=e_0 conjugate(X_(-k-1)).                         (4.3)

The equations A F_N Bx=u F_N* x and A F_N By=u F_N* y become, for k=j modulo L,

    a_j D_k=u X_(-k),
    a_j E_k=u omega^k Y_(-k).                           (4.4)

For n=-k, eliminating a_j without division yields

    X_n conjugate(X_(n-1))
      =lambda Y_n conjugate(Y_(n-1)),                   (4.5)

and taking absolute values in (4.3)-(4.4) gives

    |X_n|=|Y_(n-1)|,  |Y_n|=|X_(n-1)|.                (4.6)

Thus the absolute values of X and Y are two-periodic. If none of them vanished, multiplying (4.5) over all n would give a strictly positive real number equal to lambda^L=-1 times a strictly positive real number, impossible. Since X and Y are nonzero transforms, their supports must therefore be precisely complementary parity classes: for some eta in {+1,-1},

    x_(t+m)=eta x_t,
    y_(t+m)=-eta y_t.                                  (4.7)

The nonzero Fourier coefficients in each parity class have constant modulus; in particular their union covers every Fourier index.

Shift (4.2) by m. Both products x_t y_t and x_t y_(t-1) change sign by (4.7), while lambda^(2m)=lambda^L=-1. Hence

    d_(t+m)=d_t, e_(t+m)=e_t,

or b_(j+L)=b_j.

Finally compare (4.4) at j and j+L. The right and left Fourier vectors are both periodic on the even-supported vector, and both antiperiodic on the odd-supported vector, so their signs cancel. At each Fourier index at least one of the two equations has a nonzero Fourier coefficient, by complementary support and (4.3)-(4.6). It follows that a_(j+L)=a_j. This proves Theorem 2, including possible Fourier zeros; no division by a possibly zero coefficient was used to obtain (4.5).

The endpoint vectors at lambda^(-1) can be taken as

    x'_t=omega^t x_t,  y'_t=omega^t y_t.                (4.8)

This follows immediately from (4.1), since lambda^(-2)=omega. They have modulus-one coordinates, and (because omega^m=-1) their half-shift signs are opposite to those in (4.7). Equation (3.2) gives Ux'=u^(-1)x' and Uy'=u^(-1)y'.

## 5. The C8 contradiction

Set N=8, L=4, m=2 and theta=3pi/8. Suppose phases attained ||Im(PF_8Q)||=sin(3pi/16). Sections 2-4 apply, and A,B are four-periodic.

Let H=S^4. Four-periodicity of A makes C=F_8 A F_8 vanish between opposite parities: its Fourier coefficients of odd index are zero. Four-periodicity of B, together with C H=H C, makes U commute with H. Consequently the four spaces

    H_(parity,eta) = {vectors of the chosen parity, Hx=eta x},
    eta in {+1,-1},

are invariant under U, and each has complex dimension two.

By (4.7)-(4.8), every one of these four spaces contains one endpoint eigenvector of U, at either u or u^(-1), with equal-magnitude coordinates in the standard half-shift basis. In a two-dimensional unitary matrix, a flat eigenvector forces the two diagonal entries to be equal: its orthogonal complement is also flat, and the spectral decomposition is

    U_block = z_1 v v* + z_2 w w*,

where both diagonal entries of each rank-one projector are 1/2. This statement remains true if z_1=z_2.

Write the cyclic-Hankel entries as C[j,k]=c_(j+k). On the even,+ sector, in the basis

    (e_0+e_4)/sqrt(2), (e_2+e_6)/sqrt(2),

the two diagonal entries of U are

    (c_0+c_4)b_0,  (c_0+c_4)b_2.

Their equality implies b_0=b_2, because (2.2) makes the real part of each diagonal entry strictly positive, so c_0+c_4 is nonzero.

On the even,- sector, in the corresponding difference basis, the diagonal entries are

    (c_0-c_4)b_0,  -(c_0-c_4)b_2.

Their equality implies b_0=-b_2, because c_0-c_4 is again nonzero by (2.2). This contradicts |b_0|=|b_2|=1.

Thus equality is impossible for every phase choice. Section 3 proves the lower bound, and compactness in (2.1) upgrades nonattainment to the strict inequality in Theorem 1.

## 6. A legal exact upper control

Take P=exp(i pi/4)I, Q=I, E=0, and real core B_core=Re(PF_8). The reversal matrix R_0=F_8^2 has eigenvalues +/-1, so W=(PF_8)^T(PF_8)=i R_0 has eigenvalues +/-i. Therefore every singular value of Im(PF_8) is exactly 1/sqrt(2). With external gauges L=P*, R=I, the original residual has exactly that norm. This verifies the upper bound in the same unrestricted monomial model.

## 7. What is and is not closed

Closed: the conjectured sharpness of the accepted lower-bound formula at all smaller ranks is false, by the strict all-phase C8 rank-zero obstruction. The equality-case half-periodicity theorem is uniform for N divisible by four.

Open here: the exact value of delta_(8,0), an explicit positive numerical gap above sin(3pi/16), strictness or attainment for N=4m with m>=3 at rank zero, and the remaining smaller positive correction ranks. The two-dimensional argument is deliberately not extrapolated to higher-dimensional sectors.

The accompanying fresh exact checker verifies the weighted-cycle, Fourier, invariant-sector, flat-projector, contradiction, and legal upper-control identities. It does not run any historical code. Exploratory numerical files are not proof inputs and are excluded from the certificate manifest.
