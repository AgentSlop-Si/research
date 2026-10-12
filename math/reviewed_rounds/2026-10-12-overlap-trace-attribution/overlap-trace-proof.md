# A trace proof of the Hermite overlap annulus

12 October 2026 UTC.

## Accepted statement and scope

Let He_0(x)=1, He_1(x)=x and He_(n+1)(x)=x He_n(x)-n He_(n-1)(x) be the monic probabilists' Hermite polynomials. For an integer A>=1 and a nonreal complex number tau, set

    F(x)=J_(A+1)(x;tau)
        =He_(A+1)(x)+A(1-tau)He_(A-1)(x)
        =x He_A(x)-A tau He_(A-1)(x),
    rho=|tau-1|^2.

If F has a repeated root, then A>=3 and

    1+1/A < rho <= 2+2/A <= 8/3.

In particular, rho<=1 or rho>8/3 is sufficient for squarefreeness simultaneously for all A>=1. Membership in the annulus is only a necessary condition for a repeated root; it is not sufficient.

An independent review accepted the trace argument below as a replacement for the Jordan-chain step in the existing overlap proof. The conclusion, parameter normalization, zero-root guards and low-degree guards are unchanged. This is a proof and attribution addendum, not new Rogers–Szegő family coverage. No cyclotomic certificates are re-established by this argument, and no first-publication or FFT-speed claim is made.

## 1. The parity determinant

Write A+1=2r+s with s in {0,1}, and put alpha=s-1/2. Then r>=1. Define monic polynomials P_j by

    He_(2j+s)(x)=x^s P_j(x^2).

Applying the Hermite recurrence twice gives the arbitrary-index recurrence

    P_0(y)=1,
    P_1(y)=y-(2s+1),
    P_(j+1)(y)=(y-(4j+2s+1))P_j(y)
                -4j(j+s-1/2)P_(j-1)(y).

Let B be the real symmetric r-by-r tridiagonal matrix whose diagonal entries are 4j+2alpha+2 for j=0,...,r-1 and whose off-diagonal entries are 2 sqrt(j(j+alpha)) for j=1,...,r-1. Every off-diagonal entry is strictly positive. Expansion of the tridiagonal determinant proves P_r(y)=det(yI-B).

Write e_r for the last coordinate vector. Shifting the last diagonal entry changes the determinant by the corresponding leading principal minor, so

    M=B+A(tau-1)e_r e_r^T,
    det(yI-M)=P_r(y)+A(1-tau)P_(r-1)(y),
    F(x)=x^s det(x^2 I-M).

Here y=x^2. The variable y used in this proof is twice the Laguerre variable in the companion source comparison. The factor of two is essential.

## 2. Endpoint positivity and the trace

Put c=A Im(tau), which is a signed, nonzero real number. If M u=lambda u with u nonzero, multiplication by the conjugate transpose u* gives

    Im(lambda) ||u||^2 = c |u_r|^2.

This uses that B is Hermitian. It does not use the bilinear transpose u^T.

The endpoint u_r cannot vanish: otherwise the last matrix row, then each preceding row, forces all coordinates to vanish because the off-diagonal entries are nonzero. The case r=1 is immediate. Consequently

    t_lambda=Im(lambda)/c=|u_r|^2/||u||^2 > 0.

Let lambda_j be the distinct eigenvalues and m_j their algebraic multiplicities. The coefficient of y^(r-1) in the characteristic polynomial gives

    sum_j m_j lambda_j = tr(M).

This identity holds even when M is defective. Taking imaginary parts and dividing this equality by c yields

    sum_j m_j t_(lambda_j) = 1.

All terms are positive, including when Im(tau)<0. A repeated eigenvalue with algebraic multiplicity m>=2 therefore satisfies

    0 < t_lambda <= 1/m <= 1/2.

Only an equality was divided by the potentially negative c. No inequality changes direction unnoticed. This step requires neither a Jordan chain nor a complete eigenbasis, self-orthogonality or a proof of one-dimensional eigenspaces.

## 3. Repeated roots and elimination

Suppose x_0 is a nonzero repeated root, and let y_0=x_0^2. The multiplicity of x_0 in F equals the multiplicity of y_0 in det(yI-M): x^s is a local unit at x_0 and x^2-y_0=(x-x_0)(x+x_0), whose second factor is nonzero at x_0. Thus y_0 is a repeated eigenvalue.

Consecutive Hermite polynomials share no zero. Otherwise the recurrence would descend to He_0=0. Moreover He_(A-1)(x_0) is nonzero: if it vanished, F(x_0)=0 and x_0!=0 would force He_A(x_0)=0.

The derivative identity He_n'=n He_(n-1), obtained inductively from the recurrence, gives

    F'=(1+A tau)He_A + A x(1-tau)He_(A-1).

Eliminating He_A and He_(A-1) from F(x_0)=F'(x_0)=0 is therefore legitimate. Since nonreal tau also excludes tau=1, it gives

    y_0=tau(1+A tau)/(tau-1)
       =A tau+(A+1)+(A+1)/(tau-1).

Taking imaginary parts and using rho=|tau-1|^2 yields

    t_(y_0)=1-(A+1)/(A rho).

Combining this identity with 0<t_(y_0)<=1/2 proves

    1+1/A < rho <= 2+2/A.

The lower endpoint is strict and the upper endpoint is inclusive.

## 4. Zero roots and small degrees

For odd A, F is even and F(0)=-A tau He_(A-1)(0), where the Hermite value is nonzero. Hence zero is a repeated root exactly when tau=0. For even A, F is odd and F'(0)=(1+A tau)He_A(0), with He_A(0) nonzero. Thus zero is repeated exactly when tau=-1/A. Both exceptional parameters are real and are excluded by the hypothesis.

For A=1,2, the parity determinant has size r=1 and cannot have a repeated eigenvalue. Equivalently,

    Disc_x J_2(x;tau)=4 tau,
    Disc_x J_3(x;tau)=4(1+2 tau)^3.

Neither discriminant vanishes for nonreal tau. For A>=3, 2+2/A<=8/3. This completes the all-A proof and both uniform sufficient criteria stated above. No finite-degree extrapolation is involved.

## 5. Sharp boundary checks and necessary guards

For A=3, take

    tau=(-1+2i sqrt(2))/3.

Direct expansion gives

    F(x)=(x^2-(1+i sqrt(2)))^2,
    rho=8/3,
    t=1/2.

For A=4, take tau=i sqrt(6)/2. Then

    F(x)=x(x^2-(3+i sqrt(6)))^2,
    rho=5/2,
    t=1/2.

Their complex conjugates give the lower-half-plane cases. The examples prove that a strict upper endpoint would be false in general. The trace equality t=1/2 forces multiplicity exactly two and no other eigenvalues, hence r=2. Thus equality is impossible for A>=5. This supplementary observation is not needed for the accepted annulus or its applications.

Three safeguards are essential. A reducible matrix such as diag(0,z) can have an eigenvector with zero last coordinate, so irreducibility cannot be dropped. Summing only distinct eigenvalues loses algebraic multiplicity and fails on the displayed double-eigenvalue examples. Finally, the map x to x^2 is ramified at zero, so the nonzero-root multiplicity argument cannot replace the separate zero-root analysis.

## 6. Verification and attribution

Fresh exact controls in the accepted independent review check the parity determinant and derivative identities for A=1,...,32, and both conjugates of the A=3,4 equality examples. A further isolated replay during preparation of this addendum reproduced the recorded controls byte-for-byte. These finite checks corroborate conventions; the arbitrary-index recurrence and trace proof establish the infinite scope.

The accepted review archive and cold receipt are bound by the content hashes in [the minimal verification record](MINIMAL_VERIFICATION.json). The original review remains intact. No author or historical candidate program was executed for this addendum.

The polynomial family, Hermite–Laguerre reduction, quasi-Laguerre discriminant framework and dissipative-Jacobi methods have established antecedents. The [bounded source comparison](overlap-source-comparison.md) identifies the exact substitutions and inspected passages. It distinguishes these antecedents from the unresolved historical priority of the explicit annulus and its Rogers–Szegő application.
