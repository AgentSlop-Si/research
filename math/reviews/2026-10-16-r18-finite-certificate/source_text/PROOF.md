# R18: an exact finite Fourier factorization, and the unresolved size lift

**Date:** 16 October 2026. **Decision:** finite characteristic-zero existence
certificate in a specified two-scan stage model. No sub-N-log-N algorithm,
uniform coefficient generator, or practical FFT speedup is established.
The primitive, numerical synthesis, and contraction argument have classical
antecedents and existing counterparts in the user's research. This is not a
worldwide priority claim or independent human mathematical review.

## 1. Model and precise inherited ingredients

Here N is the number of input coefficients. Work is exact complex field
arithmetic, with O(log N)-bit array indices and N explicit outputs. This is
not the bit complexity of integer multiplication or a stable floating-point
model. The norm used for the certificate is specified separately below.

For a permutation pi of {0,...,N-1}, write pos_pi(i) for its position and set

    H_pi[i,j] = sign(pos_pi(i)-pos_pi(j)),   sign(0)=0.

The user's Phase46_Theorems.md, Theorem 46.6, already contains the skew-sign
matrix and its linear-work prefix executor. R17 contains the scaled-cycle
compiler. Both remain attributed prior ingredients. For a cycle ordered by pi,
let G be the inverse of

    u[pi(0)] + u[pi(N-1)] = x[pi(0)],
    u[pi(i)] - u[pi(i-1)] = x[pi(i)]   (1<=i<N).

Summing the recurrence gives u[pi(i)]=sum_(j<=i)x[pi(j)]-sum_j x[pi(j)]/2.
Hence **H_pi=2G-I**, where the wrap weight is -1 and all other weights are 1.
This is a fixed nonsingular Green primitive over any field of characteristic
not two. It has no fitted pole approaching a singular denominator.

A stage has two independent orders and five diagonal coefficient vectors:

    S = D_d + D_a H_pi D_b + D_c H_rho D_e.             (1)

All coefficient vectors are free; zero entries are legal. A product of t such
stages is M=S_(t-1)...S_0. Replacing H by 2G-I writes each stage as two
nontrivial diagonally ended Green inverses and one adjusted diagonal. This is
not a product of only two inverses, a common-gauge sum, or a common-cut model.
The layers and both endpoint scalings are all refitted. R17's exclusion of a
single final correction to a *frozen* prefix therefore does not apply.

## 2. Exact executor and complete literal online count

For one branch, first gather v_i=b[pi(i)] x[pi(i)]. Compute T=sum_i v_i,
h_0=v_0-T, and then

    h_i=h_(i-1)+v_(i-1)+v_i    (1<=i<N).                (2)

Induction gives h_i=sum_(j<i)v_j-sum_(j>i)v_j=H v. Scatter and accumulate
`a[pi(i)] h_i` into the output initialized as `d_i x_i`. Do this for both
branches. No dense multiplication, Fourier routine, sparse-input assumption,
cache of input answers, or arbitrary-precision giant-word trick occurs online.

For one branch the executed count is N input multiplications, N output
multiplications, N-1 total-sum additions, one subtraction for h_0, 2(N-1)
recurrence additions, and N output accumulations. Including the stage's
N diagonal multiplications gives

    multiplications per stage       = 5N,
    additions/subtractions per stage = 8N-4.            (3)

For t stages multiply both counts by t. Indexing, gathering, scattering,
reading coefficients, initialization, and output storage cost O(tN) word work.
The supplied coefficients and orders occupy O(tN) words/field elements, with
O(N) working vectors. This is a resident-array model, not a fixed-tape theorem.
Preparation and *synthesis* are separate and cannot be erased from a uniform
complexity claim. The current synthesis explicitly builds an N-by-N target
and dense Jacobians and is not a sub-N-log-N preparation method.

At N=16,t=4, (3) gives **320 multiplications and 496 additions/subtractions**.
The straightforward normalized radix-two comparator uses at most 48 and 64,
respectively (counting every twiddle product, even trivial ones, and 16 final
normalizations). Thus this finite factorization loses on this literal count.

## 3. Exact finite statement

Let F16[i,j]=zeta^(-ij)/4 with zeta=exp(2 pi i/16). Fix the eight permutations
and the 64 inactive coefficient coordinates recorded in root_candidate.json.
There are 320 complex coefficient coordinates in total. The 64 fixed values
are exactly dyadic Gaussian rationals; the remaining 256 coordinates vary.

**Finite statement.** There is a unique solution in the certified affine
neighborhood of the recorded dyadic center for which

    S_3 S_2 S_1 S_0 = F16.                             (4)

Every solved coordinate is within 2^-100 of its center in the complex l1 norm
|Re z|+|Im z|. Uniqueness refers only to this neighborhood and this choice of
fixed coordinates. It is not global uniqueness among coefficients or routes.
The constants at the isolated nonsingular solution are algebraic over
Q(zeta16). The exact factorization uses that solution, **not the dyadic
center and not the optimizer's binary64 numbers**.

The representation supplied here is a polynomial system, fixed coordinates,
and an isolating ball with a certified contraction. It is not a list of exact
radicals or an implementation of arithmetic in the root's algebraic number
field. `scan_executor.py` is exact for supplied field coefficients; loading
its dyadic-center record does not make its finite-field output a Fourier
transform. Those center tests check the executor only.

## 4. Outward arithmetic, not a floating residual test

`ball_certificate.py` encloses each complex number by a rectangle with common
coordinate radius: (a+i b)+[-r,r]+i[-r,r]. Centers and radii are integers in
units 2^-320. Additions, products, dot products, directed floor/ceiling, and
all deciding inequalities use Python integers/Fraction. NumPy object-array
dot products add and multiply those exact integers. Float values in the
preconditioner file are interpreted as their exact binary rational values;
nonfinite or insufficiently representable witnesses are rejected.

For radii r_a,r_b, the coordinate uncertainty of a product is bounded by

    (|Re a|+|Im a|)r_b + r_a(|Re b|+|Im b|) + 2r_a r_b.

Dot products sum these bounds. One outward unit covers center rounding when
needed. The norm of a rectangle is at most |Re a|+|Im a|+2r_a. Square roots
used in the *known real* half-angle construction are enclosed by integer
square roots of scaled integer interval endpoints. Starting at cos(pi/2)=0,
repeated half angles construct the positive cosine/sine for pi/8, giving the
negative primitive root for F16. Powers and the 1/4 normalization are enclosed.
No untrusted floating `exp`, sine, square root, or rank threshold defines the
certified target.

The arithmetic tests compare scalar endpoint products and matrix products
with separately formulated exact Fraction operations. These are corroborating
implementation tests; the enclosure rules above justify all intervals.

## 5. Contraction certificate

List the 256 entries of M-F16 as a complex polynomial map f:C^256 -> C^256
in the active coordinates, with every inactive coordinate fixed. Let z0 be
the dyadic center, J0=f'(z0), and B the supplied exact dyadic preconditioner.
Use the vector norm max_j (|Re z_j|+|Im z_j|), and the induced row-sum bound
for complex matrices. Let

    alpha >= ||B f(z0)||,
    beta  >= ||I-B J0||,
    b     >= ||B||.

The verifier computes these upper bounds without presuming B is an inverse.
To bound variation of J, first let L be an integer upper bound for every
coefficient's complex l1 norm on the radius-one neighborhood of z0. Here L=6.
For the matrix row-sum norm of one stage and its first two derivatives,

    B0=L+2N L^2,
    B1=1+4N L,
    B2=4N

are valid bounds for parameter directions of norm at most one. Each row has
at most N entries per skew branch. A derivative of a bilinear branch has two
terms; a second derivative has two mixed terms. The product rule consequently
bounds the second derivative of the t-stage product by

    H=t B0^(t-1) B2 + t(t-1) B0^(t-2) B1^2.            (5)

Selecting a subset of active coordinates only decreases this bound. The
output maximum-entry norm is at most the matrix row-sum norm, so (5) also
bounds the flattened residual map. For r<=1 and ||v||<=r,

    ||B(f'(z0+v)-J0)|| <= b H r.

Thus T(z)=z-B f(z) has Lipschitz constant at most

    q=beta+b H r.                                     (6)

A Taylor expansion with its integral remainder gives

    ||T(z0+v)-z0|| <= alpha+beta*r+(b H/2)r^2.          (7)

The exact verifier establishes the following convenient rational upper
bounds as well as the stronger full fractions retained in the JSON:

    alpha < 10^-89,
    beta < 10^-8,
    b < 616,
    H = 2782698762672 < 3*10^12,
    r = 2^-100.

Its tighter displayed values, which are illustrative only, are

    alpha ~ 3.5199445847e-90,
    beta  ~ 3.9518893205e-9,
    q     ~ 3.9518906721e-9,
    RHS(7) ~ 3.1174915198e-39 < r ~ 7.8886090522e-31.

Equations (6)-(7) prove that T is a strict contraction of the closed ball
into itself. Banach's theorem gives a unique fixed point. Since beta<1,
B J0 is invertible, so square B is invertible; a fixed point therefore has
f(z)=0. The derivative remains invertible throughout the ball. An isolated
nonsingular zero of a square polynomial system with algebraic coefficients
has algebraic coordinates, proving the algebraicity assertion. All matrix
entries in (4) are equal at this root, so (4) covers **every complex input**
at N=16, not a finite list of sample inputs.

The norm is not Euclidean and no probabilistic interpretation is assigned
to the radius. Contraction/root certification is classical, not an invented
verification principle. The search and QR selection only supply a witness;
the exact certificate does not assume that their floating calculations are
correct.

## 6. Why this is still not a sub-N-log-N construction

A supplied t(N)-stage identity would have online cost O(t(N)N). To obtain a
uniform all-input algorithm below N log N by this route, one must prove a
family of exact identities with t(N)=o(log N), and construct their scalar
constants, routes, and output representation in o(N log N) charged work.
A fully charged numerical/bit model would need its additional accuracy and
encoding guarantees. None follows from one fixed-size certificate.

The current synthesis uses every entry of the dense Fourier target. Its full
Jacobian in the successful affine chart is invertible. In fact, the implicit
function theorem then also gives representations of all targets in a small
neighborhood of F16 using this chart. The successful seed therefore certifies
finite expressive power, not an identified Fourier-specific scaling law.

The executed N32 searches did not extend the exact result. Four stages with
random, bit-slot, and affine/bit-reversal orders ended at relative errors
about 0.5043, 0.4961, and 0.4645; eight stages with the recorded random seed
ended near 0.1768. These are outcomes of bounded local optimization, **not**
nonexistence proofs, topology lower bounds, certified global minima, or a
reason to reject untested exact coefficient formulas. Conversely they give
no evidence of a bounded-depth family. No new asymptotic exponent is asserted.

## 7. Provenance and verification boundary

The user's table already records C09: a different certified F16 Green
construction with three layers and eight branches per layer. R18 is not the
first exact finite seed in the project. It uses four stages, eight total
nontrivial fixed-holonomy inverses and four free diagonal terms, with two
endpoint masks on each inverse. Do not compare branch counts as if masks,
diagonals, arithmetical costs, and models were identical. No worldwide
novelty assessment for this exact eight-route certificate is complete.

The Phase46 primitive, R17 scan compilation, existing C09 finite-existence
baseline, and classical synthesis/certification methods are retained in the
source ledger. No external exponent-saving construction was imported or
relabeled as this work. All new proof and checking code in this packet are
author-side; exact arithmetic is not a substitute for independent review.
