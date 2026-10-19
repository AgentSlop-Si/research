# An explicit all-phase improvement of the C8 rank-zero lower bound

19 October 2026 UTC.

## Result and scope

In the original model with arbitrary invertible complex monomial outer matrices, unrestricted real core, and the external operator norm,

\[
\boxed{\sin\left(\frac{3\pi}{16}+10^{-6}\right)
<\delta_{8,0}\leq\frac12\sqrt{1+\sqrt{\sqrt2-1}}.}
\]

The new lower endpoint is approximately 0.5555710644889368. It improves the previously accepted endpoint by approximately 0.0000008314693346. The upper bound is the previously accepted exact witness and is not reproved here. The exact global optimum remains unresolved.

This is a quantitative stability argument valid for every choice of phases. Four-periodicity is neither assumed nor asserted. In particular, the argument below uses compressions of the original unitary; those compressions need not be invariant or unitary. This avoids a potentially unjustified passage to a periodic surrogate.

## 1. Original model and notation

Let F[j,k]=8^(-1/2) exp(-2 pi i j k/8), with indices modulo eight. The real monomial magnitudes and permutations in arbitrary complex monomial outer factors are absorbed into the unrestricted real core. Only diagonal unitaries are applied to the external residual. Also, for any complex V,

    min over real C of ||V-C||_2 = ||Im V||_2,

because entrywise imaginary part is an operator-norm contraction, and C=Re V attains the bound. Thus the original problem is exactly

    delta_(8,0) = min_(P,Q diagonal unitary) ||Im(P F Q)||_2.

For V=P F Q, the symmetric unitary V^T V is similar to U=F A F B, where A=P^2 and B=Q^2. Its phase eigenvalues exp(i phi) correspond to squared singular values sin^2(phi/2) of Im V. Consequently a residual at most sin(theta/2), for theta<pi/2, implies

    spectrum(U) lies in |arg z| <= theta,
    (U+U*)/2 >= cos(theta) I.

Fix throughout

    theta_0 = 3 pi/8,
    epsilon = 1/500000,
    theta = theta_0 + epsilon,
    c = cos(theta),
    rho = sqrt(10 epsilon) + epsilon,
    eta = 2 sqrt(2) rho.

Suppose for contradiction that phases attain residual at most sin(theta/2).

## 2. Quantitative endpoint localization

Let S e_j=e_(j+1), T=B* S B, and C=F A F. The cyclic-Hankel relation C S=S* C gives

    K = U T U* T* = S* B* S* B,
    K e_j = (b_j/b_(j-1)) e_(j-2).

The spectral arc for U implies ||U-cI|| <= sin(theta), and hence

    ||K-I|| = ||U T-T U|| <= 2 sin(theta).

Thus every eigenvalue of K has principal argument in [-2theta,2theta]. Its even and odd cycles each have length four, and their products are Gamma and Gamma^(-1). Each cycle's spectrum is a rotated square. The four points can avoid the open gap centered at -1, of width pi/2-4epsilon, only if they have arguments

    pi/4+d, 3pi/4+d, -3pi/4+d, -pi/4+d,

with |d|<=2epsilon. The second cycle then has offset -d. Put

    lambda_e = exp(i(3pi/4+d)),
    lambda_o = exp(i(3pi/4-d)),
    Lambda = lambda_e lambda_o = -i.

We need a quantitative substitute for exact endpoint rigidity. If K v=exp(i kappa)v, ||v||=1, and s=kappa/2, set a=<v,Uv>. Write D=T U* T*. Since U D v=exp(i kappa)v, we have <v,Dv>=exp(i kappa) conjugate(a). Accretivity of U and D gives

    Re(a) >= c,
    Re(exp(2is) conjugate(a)) >= c.

Adding these inequalities after writing a=exp(is) a' yields

    Re(a') >= c/cos(s),
    ||U v-exp(is)v||^2 <= 2(1-c/cos(s)).

For any of the four extreme cycle eigenvalues, |s| is between theta_0-epsilon and theta_0+epsilon. Since tan(theta)<5/2,

    2(1-c/cos(s)) <= 4epsilon tan(theta) < 10epsilon.

Moving exp(is) to u=exp(i theta_0), or to conjugate(u) at the negative endpoint, costs at most epsilon. Therefore every normalized positive-endpoint cycle eigenvector has residual at most rho for eigenvalue u, and every negative-endpoint one has residual at most rho for conjugate(u).

## 3. Exact recurrences and approximate Fourier equations

Choose the positive-endpoint eigenvectors on the even and odd cycles. Write their coordinates as x_t/2 on index 2t and y_t/2 on index 2t+1, respectively, where t is modulo four and x_0=y_0=1. All x_t and y_t have modulus one. Put d_t=b_(2t), e_t=b_(2t+1). Their exact recurrences are

    x_(t+1) = lambda_e e_t/d_(t+1) x_t,
    y_(t+1) = lambda_o d_(t+1)/e_(t+1) y_t.

Multiplication gives the exact identities

    e_t x_t y_t = e_0 Lambda^t,
    d_t x_t y_(t-1) = e_0 lambda_o^(-1) Lambda^t.       (3.1)

The second identity involves lambda_o, not lambda_e; the offsets need not vanish.

Let omega=i and define the normalized four-point Fourier transforms

    X_n = (1/2) sum_t x_t omega^(-nt),
    Y_n = (1/2) sum_t y_t omega^(-nt),
    D_k = F_4(d x)_k, E_k = F_4(e y)_k.

Equation (3.1) and unit-modulus coordinates imply exactly

    D_k = e_0 lambda_o^(-1) omega^(-k-1) conjugate(Y_(-k-1)),
    E_k = e_0 conjugate(X_(-k-1)).                    (3.2)

The endpoint residual bounds, after multiplying by F*, imply for every j and k=j mod 4

    |a_j D_k - u X_(-k)| <= eta,
    |a_j E_k - u omega^k Y_(-k)| <= eta.              (3.3)

The factor 2 sqrt(2) in eta accounts for the normalized eight-point Fourier transform and the endpoint vectors' coordinates of modulus 1/2.

Taking absolute values in (3.2)-(3.3), and then eliminating a_j by multiplication rather than division, gives for n modulo four

    ||X_n|-|Y_(n-1)|| <= eta,
    ||Y_n|-|X_(n-1)|| <= eta,                        (3.4)

    |X_n conjugate(X_(n-1))
       -lambda_e Y_n conjugate(Y_(n-1))|
       <= eta (|X_(n-1)|+|Y_(n-1)|).                (3.5)

Here lambda_o^(-1) omega^(-1)=lambda_e exactly. In particular,

    ||X_n|-|X_(n-2)|| <= 2eta,
    sum_n |X_n|^2 = sum_n |Y_n|^2 = 4.              (3.6)

## 4. Quantitative complementary support

We prove that both Fourier coefficients of one parity have modulus at most 7eta, while both Y coefficients of the opposite parity have modulus at most 8eta.

Let m=min_n |X_n| and M=max_n |X_n|. Parseval gives M>=1. Suppose m>5eta. Then all X and Y coefficients are nonzero. For

    z_n=X_n conjugate(X_(n-1)),
    w_n=Y_n conjugate(Y_(n-1)),

(3.4)-(3.6) imply

    |z_n| >= m(M-2eta),
    |w_n| >= (m-eta)(M-3eta),
    |z_n-lambda_e w_n| <= eta(2M+eta).

Indeed, each adjacent pair contains a coefficient in the parity of a maximum, and those coefficients are at least M-2eta.

For nonzero complex z,w,

    |z/|z| - w/|w|| <= |z-w|/sqrt(|z||w|),

as follows by expanding |z-w|^2. We have eta<1/50. Using M>=1 and m>5eta therefore gives

    sqrt(|z_n||w_n|) > (21/25)mM,
    |z_n-lambda_e w_n| <= (101/50)M eta.

Both products over n of z_n/|z_n| and w_n/|w_n| equal one, by telescoping. The product-difference inequality for unit complex numbers yields

    |1-lambda_e^4|
      <= sum_n |z_n/|z_n| - lambda_e w_n/|w_n||
      < 202/105 < 199/100.

But lambda_e^4=-exp(4id), and |d|<=2epsilon, so

    |1-lambda_e^4| = 2|cos(2d)|
      >= 2 cos(4epsilon) > 199/100.

This contradiction proves m<=5eta. The coefficient of the same parity differs in modulus by at most 2eta, proving the asserted 7eta bound. Equation (3.4) gives the 8eta bound for Y on the complementary parity.

Let s in {+1,-1} be the half-shift sign of the other, potentially large, X parity. Fourier inversion now gives the coordinatewise estimates

    |x_(t+2)-s x_t| <= 14eta,
    |y_(t+2)+s y_t| <= 16eta.                         (4.1)

Together with (3.1), Lambda^2=-1 and unit-modulus coordinates, these imply

    |b_(j+4)-b_j| <= 30eta for every j.               (4.2)

For example, x_(t+2)y_(t+2) is within 30eta of -x_t y_t, while e_(t+2)x_(t+2)y_(t+2)=-e_t x_t y_t exactly. The d identity is the same calculation with y_(t-1). No phase is changed and no exact periodicity is claimed.

## 5. Flat-vector compressions give a contradiction

Let xi be the normalized even-cycle positive endpoint vector. Its coordinates are (x_0,x_1,x_2,x_3)/2 on indices (0,2,4,6). Replace only its last two coordinates by (s x_0,s x_1)/2 to obtain a unit vector v in the even, half-shift-s subspace. In that subspace's standard orthonormal basis

    (e_0+s e_4)/sqrt(2), (e_2+s e_6)/sqrt(2),

v has two equal-modulus coordinates. By (4.1),

    ||v-xi|| <= 7sqrt(2)eta,
    ||(U-uI)v|| <= r := rho+14sqrt(2)eta.            (5.1)

The negative-endpoint even-cycle vector has coordinates i^t x_t/2, because multiplication by i^t changes its K eigenvalue to i lambda_e=exp(i(-3pi/4+d)). The same argument supplies a flat unit vector in the even, half-shift-(-s) subspace with residual at most r for conjugate(u).

If a unitary U has a unit vector v with ||(U-zI)v||<=r and |z|=1, then also ||(U*-conjugate(z)I)v||<=r. In a two-dimensional subspace containing v as a flat vector, let w be its flat orthogonal complement. Both |w*Uv| and |v*Uw| are at most r. In the subspace's standard basis, the difference of the two diagonal entries of its compression of U is therefore at most 2r. This uses no invariance or unitarity of the compression.

Write C[j,k]=c_(j+k), and set

    beta_0=(b_0+b_4)/2, beta_2=(b_2+b_6)/2.

The diagonal entries of the two even half-shift compressions of the actual U=CB are exactly

    plus sector:  (c_0+c_4) beta_0, (c_0+c_4) beta_2;
    minus sector: (c_0-c_4) beta_0, -(c_0-c_4) beta_2.

Since Re U>=cI and |beta_j|<=1, both |c_0+c_4| and |c_0-c_4| are at least c. The preceding flat-vector estimates imply

    |beta_0-beta_2| <= 2r/c,
    |beta_0+beta_2| <= 2r/c.

On the other hand, (4.2) and |b_j|=1 give

    |beta_0|, |beta_2| >= sqrt(1-225eta^2).

The parallelogram identity therefore forces

    r >= c sqrt(1-225eta^2)/sqrt(2).                 (5.2)

The following strict bounds hold at epsilon=1/500000:

    rho < 9/2000,
    eta < 8/625 < 1/50,
    r < 13/50,
    c > 19/50,
    sqrt(1-225eta^2) > 49/50,
    (19/50)(49/50)/sqrt(2) > 13/50.

They contradict (5.2). All these numerical constants are proved with rational arithmetic and squared positive quantities in the accompanying checker. Consequently the supposed phase choice does not exist. Compactness of the phase torus, or simply applying the argument to a minimizing phase choice, proves the strict lower bound stated above.

## 6. Checks, limits, and unfinished question

The fresh exact checker verifies the recurrence/Fourier formulas, the arbitrary-Hankel compression formulas, the flat-vector diagonal identity, and every rational numerical margin used in the proof. It checks destructive controls that distinguish lambda_o from lambda_e in (3.1) and reject an incorrect minus-sector sign. Numerical values are informational; no sampling or optimization is used to establish the lower bound.

The established interval is still wide. This result supplies an explicit positive gap, not a global optimality certificate for the accepted upper witness. Stronger quantitative constants could be obtained by retaining exact expressions, but tightening this stability argument alone does not currently approach the upper endpoint. The potentially lossy steps are pointwise residual bounds, the Fourier phase-product estimate, and replacing exact spectral information by flat-vector residuals.
