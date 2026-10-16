# Q29: exact obstructions to a phase-only noncancellation proof

16 October 2026 UTC. Mathematical-development pass. External sources were
read only; this is a local proof artifact.

## Result

Two exact statements close a specific proposed route without claiming to
close Q29.

1. The actual reciprocal recurrence cannot be turned into a positive real
   Jacobi recurrence by a single affine spectral change and diagonal
   similarity, once its degree is at least two in the Q29 regime. Thus the
   ordinary positive-orthogonality argument is not recovered by merely
   choosing different phases for the recurrence basis.
2. Even the exact geometric phase progression of the q-Hermite matrix,
   together with positive real and imaginary parts of its diagonal pencil
   metric, all nonzero edges, a simple persistent zero, and reciprocal
   endpoint exclusion, does not imply kernel noncancellation. An explicit
   five-vertex family has characteristic polynomial x(x^2-lambda)^2. Its
   two-term contracted kernel cancels exactly at lambda.

The second family changes the edge magnitudes. It is NOT the Rogers--Szego
family and is NOT a counterexample to its squarefreeness or to the actual
successive-layer implication. Its role is to stop a precisely identified
overgeneralization. The first obstruction does apply to the actual family,
but excludes only the specified affine/diagonal positivity repair.

The present phase-only route is stopped. A successful future proof must use
additional information, such as the actual sine-amplitude law, a different
noncancellation mechanism, or a sufficiently controlled nonsingular
reference. No new fixed-layer or endpoint census is justified by these
results. Q29 and the broader composite squarefreeness owner remain open.

## 1. Actual recurrence and the exact affine-positivity criterion

The source-bound reciprocal recurrence is

    C_0=1,
    C_1=w-d_0,
    C_(k+1)=(w-d_k) C_k-beta_k C_(k-1),
    d_k=2-q^(2k+1)-q^(2k+2),
    beta_k=(1-q^(2k))(1-q^(2k+1)).

For a general such monic recurrence with nonzero beta coefficients, make
the single affine change w=A y+B, A!=0, and retain monicity by setting
P_k(y)=A^(-k) C_k(Ay+B). Its recurrence coefficients become

    delta_k=(d_k-B)/A,       gamma_k=beta_k/A^2.

**Affine-positivity criterion.** These polynomials have a real Jacobi
recurrence with strictly positive subdiagonal coefficients if and only if

    (d_k-B)/A is real for all k,
    beta_k/A^2 is positive real for every k>=1.       (1.1)

This follows immediately by substitution. It is also the exact criterion
for an affine transform of the associated tridiagonal matrix to become a
real symmetric Jacobi matrix under diagonal similarity: diagonal entries
and the products of opposing off-diagonal entries are invariant under
diagonal similarity. Conversely, when (1.1) holds, recursive diagonal
scaling makes both off-diagonal entries equal to sqrt(gamma_k)>0.

This is a structural test for the specified repair, not a theorem that all
possible positive metrics or non-diagonal similarities have been excluded.

### Application to the actual family

Use the principal root q=exp(2 pi i/N) and N=4m+3, as in the actual odd-index
contraction. Write theta=pi/N. All relevant j satisfy 0<j<N, so

    1-q^j = 2 sin(j theta) exp(i[-pi/2+j theta]).

For m>=3, beta_1 and beta_2 both occur. Their ratio has positive modulus
and phase

    arg(beta_2/beta_1)=4 pi/N.

Since N>=15, this ratio is not positive real. Condition (1.1) would force
beta_2/beta_1=gamma_2/gamma_1>0, a contradiction. No translation B can repair
this invariant.

For m=2, N=11, one beta occurs. A necessary consequence of (1.1) is

    (d_1-d_0)^2/beta_1 is nonnegative real.

But d_1-d_0=q(1+q)(1-q^2), and hence

    (d_1-d_0)^2/beta_1
      = q^2 (1+q)^2 (1-q^2)/(1-q^3).

Its modulus is positive and its phase is 5 pi/N, which is not real at N=11.
Thus the affine-positivity repair fails at this remaining degree as well.
Degree one has no squarefreeness issue. The same argument rules out the
m=2 repair for every N>5 with these recurrence coefficients.

For the selected tower m_e=(27*5^e-3)/4, m_e>=3, so the beta-ratio obstruction
applies at every requested layer. This is an actual-family proof-route
obstruction, not evidence that its discriminant vanishes.

## 2. A matching-phase counterexample with exact kernel cancellation

The usual positive-complex-pencil argument proves endpoint simplicity but
does not control nonzero eigenvalues. The following counterexample retains
more than positivity alone: its diagonal phase matrix is exactly the one
used in the accepted q-Hermite resonance proof.

Let N>9 be an integer and set

    t=pi/(2N),
    s=sin(3t)/(1-sin(t)),
    L=cos(3t)+s cos(t),
    E=exp(i[-pi/2+5t]),
    lambda=E L.

Then s>0, L>0, and lambda is strictly in the fourth quadrant. Set

    a_1=E exp(-3it),
    a_2=s E exp(-it),
    a_3=s E exp(it),
    a_4=E exp(3it).                                (2.1)

Every a_j is nonzero, and

    arg(a_j)=-pi/2+j pi/N,

which is exactly the principal phase of the ACTUAL coefficient 1-q^j,
where q=exp(2 pi i/N). Only the magnitudes have been changed:

    (|a_1|,|a_2|,|a_3|,|a_4|)=(1,s,s,1).

Let S_0=1, S_1=x, and S_(j+1)=x S_j-a_j S_(j-1). Direct continuant
expansion gives

    S_5=x[x^4-(a_1+a_2+a_3+a_4)x^2
                 +(a_1 a_3+a_1 a_4+a_2 a_4)].

The defining relation s(1-sin t)=sin 3t gives

    a_1+a_2=E(L-is),
    a_3+a_4=E(L+is),
    a_2 a_3=s^2 E^2.

Consequently

    S_3=x[x^2-E(L-is)],
    S_5=x(x^2-lambda)^2.                          (2.2)

The lower odd polynomial S_3 is squarefree because E(L-is)!=0. The zero
of S_5 is algebraically simple, since S_5'(0)=lambda^2!=0, while both
nonzero roots of S_5 are double. Thus nonzero recurrence coefficients and
lower-prefix simplicity do not prevent a subsequent double root even in
this matching-phase class.

### Exact cancellation in the denominator-free contracted kernel

Write S_(2r+1)=x C_r(x^2). The first two contracted polynomials here are

    C_1(w)=w-E(L-is),
    C_2(w)=(w-lambda)^2,
    beta_1=a_2 a_3=s^2 E^2.

The same ordinary-derivative Christoffel--Darboux identity as in the actual
family gives

    K_2(w)=C_1(w)^2+beta_1.

At the repeated root,

    C_1(lambda)=isE,
    K_2(lambda)=(isE)^2+s^2 E^2=0.                 (2.3)

Neither summand is zero. Cancellation is exact, not a small floating-point
residual. Equivalently, the symmetric contracted matrix

    [ E(L-is)    sE     ]
    [   sE     E(L+is)  ]

has eigenvector (1,i)^T at lambda, with bilinear norm 1+i^2=0. Its
geometric eigenspace is one-dimensional, but lambda is algebraically double.

## 3. The same positive geometric pencil, and the same endpoint properties

Choose c_j=sqrt(|a_j|) exp(i[-pi/4+j pi/(2N)]), so c_j^2=a_j. Let J be the
5-by-5 complex symmetric zero-diagonal Jacobi matrix with edges c_j.
Define exactly the q-Hermite phase diagonal

    D_jj=exp(i theta_j),
    theta_j=-pi/8+pi(2j+1)/(8N),  j=0,...,4.

Then J=D R D, where R is real symmetric, zero diagonal, and has positive
edges sqrt(|a_j|). Put B=D^(-2). Since N>9,

    0<arg(B_jj)=pi/4-pi(2j+1)/(4N)<pi/4.

Thus Re(B) and Im(B) are both strictly positive definite diagonal Hermitian
matrices. The pencil R-xB has the same roots, with the same multiplicities,
as xI-J, up to a nonzero constant determinant factor.

In particular all of the following hold simultaneously:

- a real symmetric unreduced Jacobi R;
- exactly the geometric B phase progression used for the q-Hermite matrix;
- Re(B)>0 and Im(B)>0;
- an algebraically simple zero eigenvalue;
- no nonzero real eigenvalue;
- nonzero eigenvalues of algebraic multiplicity two.

The counterexample therefore survives the actual endpoint argument, rather
than contradicting it. Positivity of v* B v is not positivity of v^T B v.

The corresponding reciprocal polynomial is explicitly

    Htilde_5(z)=(z+1)[z^2+(2-lambda)z+1]^2,
    Utilde_5(z)=[z^2+(2-lambda)z+1]^2.

Its quotient is monic reciprocal with constant term 1. Its endpoints are

    Utilde_5(-1)=lambda^2!=0,
    Utilde_5(1)=(4-lambda)^2!=0.

Because lambda is nonreal, neither zero of its quadratic factor lies on
the unit circle: for |z|=1, z+2+z^(-1) is real in [0,4]. The quadratic has
distinct roots because lambda(lambda-4)!=0, but both have multiplicity two
in the quotient. Hence endpoint nonvanishing and exclusion from [0,4]
do not repair the exact cancellation (2.3).

At N=11, the size also matches the original half-order relation
5=(N-1)/2. This is nevertheless not H_5(z;zeta_11): the original edge
magnitudes are 2 sin(j pi/11), whereas (2.1) has magnitudes (1,s,s,1).
For general N>9, the example has five vertices and is not claimed to match
the half-order dimension. Taking N large makes its geometric phase spread
arbitrarily small; that observation does not create an actual large-N
Rogers--Szego counterexample.

## 4. What this settles and what it leaves open

The two statements above are useful rejection tests for proof proposals:

1. A proposal to restore ordinary positive Jacobi orthogonality solely by
   affine spectral rotation and diagonal basis rephasing is contradicted
   by the actual beta-ratio invariant.
2. A proposed theorem that uses only nonzero edges, the exact geometric
   phase progression, positive pencil parts, and the accepted endpoint
   properties is contradicted by (2.1)--(2.3).

A theorem that also uses the actual amplitudes 2 sin(j pi/N), their
particular recurrence relations, or additional arithmetic structure is
not contradicted. Those features are exactly what this example does not
preserve. No counterexample to a theorem with those hypotheses has been
established here.

In particular the actual statement

    Disc(R_e)!=0 => Disc(R_(e+1))!=0, e>=3,

remains unresolved. The result is not an inter-layer transfer theorem,
a nonvanishing theorem for the actual kernel, or an actual-family multiple
root. The accepted fixed e=3 theorem is unchanged. There is no claimed
scalar-bank count improvement, broader classification, novelty priority,
or status promotion.

The scope requested for this route ends at the exact obstruction. Do not
turn this construction into another automatic fixed-layer census. A restart
requires a proposed mechanism using information that survives neither of
the two obstructions above, with its actual-family hypotheses proved.

## 5. Provenance and checks

The controlling report was fetched at the requested baseline commit:

https://github.com/AgentSlop-Si/research/blob/de5dc664448d8e3e219df9651b2805d5a2cecbb1/math/finalized/2026-10-16-finalization-round/reports/q29/REPORT.md

It supplies the actual recurrence, ordinary kernel, and open transfer gate.
The local original report and its accepted F021 primary source were read
as inert text. The primary source supplies the exact phase diagonal used
above. SOURCE_BINDINGS.json records source hashes and the fetched blob SHA.

Fresh self-authored symbolic controls verify the continuant factorization,
the contracted kernel cancellation, the lower polynomial, and the
reciprocal polynomial identity as rational-function identities, without
numerical root finding or supplied code. The phase and positivity guards
are proved analytically above. Exploratory small-degree discriminants and
a small synthetic search were used to evaluate alternative routes; neither
is evidence for an actual-family all-layer claim. No endpoint census, old
certificate replay, or higher-layer production computation was performed.

Supplied programs executed: zero. External writes: zero. New actual-family
squarefreeness certificates: zero. This report is a proof-route exclusion
with a fully explicit synthetic witness and an actual recurrence invariant.
