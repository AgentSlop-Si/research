## Independent review of the Rogers–Szegő b=25 overlap family
12 October 2026 UTC

Decision and scope

Bounded ACCEPT after verification of the sealed candidate and independent
cold replay. The new assertion is nonvanishing of Disc_x J_(A+1)(x;tau)
for b=25, every odd d=53,55,...,193, every primitive order-d root q in
characteristic zero, and every integer A>=1. There are 71 middle orders.
The accepted general lower theorem covers odd 27..51 and the improved
general tail covers d>=195, including 195. Their union proves the full
b25 overlap family for every odd d>25. Earlier full odd b<=23 families
are inherited from the pinned accepted b23 packet.

The original definitions are essential:
  H_25(z;q)=sum_(j=0)^25 [25 choose j]_q z^j=(z+1)U(z),
  g=H'_25(-1;q)=U(-1),
  W=product_(r=1)^25(1-q^r)/product_(r=1)^((d+25)/2)(1-q^(2r)),
  tau=dW/g,
  J_(A+1)(x;tau)=He_(A+1)(x)+A(1-tau)He_(A-1)(x)
               =x He_A(x)-A tau He_(A-1)(x).
He_0=1, He_1=x and He_(n+1)=x He_n-n He_(n-1). The polynomial degree
is A+1, not 25. Section 3.2 equations (5)–(6) and the Hermite definition
of the included original v3 working note have been read and compared.
Its product-length m=(d+b)/2 is not the prefix index (b-1)/2=12.

The frozen candidate digest, proof digest, certificate digest and exact
verification counts are in VERDICT.json and SOURCE_AUDIT.json. The source
and candidate programs were never executed or imported. Fresh reviewer
code alone was run. No external state was changed during the review.

Original normalization and guards

The reviewer independently reconstructed all 26 Gaussian coefficients
from the finite Euler product and checked every original product quotient
identity by multiplication in Z[q]. The derivative sum
sum j(-1)^(j-1)[25 choose j]_q agrees identically with the separately
constructed cleared prefix recurrence, yielding g=B_12 S_12. Here
B_j=product_(r=1)^j(1-q^(2r)), s_j=product_(r=1)^j
(1-q^(2r-1))/(1-q^(2r)), and S_j=sum_(r=0)^j s_r.

At h=(d-1)/2 and E=B_h, the odd derivative recurrence evaluated at degree
d, where H_d=1+z^d, proves E S_h=d. Fresh cyclic integer arithmetic checks
this identity modulo independently constructed Phi_d for all 71 orders.
Every g modulo Phi_d is nonzero. Cyclotomic irreducibility over Q then
gives all-primitive nonvanishing. We do not interpret arbitrary nonzero
elements of a nonfield quotient as units.

The factors of the original W denominator after E are precisely the odd
numerator factors 1-q,1-q^3,...,1-q^25. The exact exponent multisets match
at each order. Cancellation gives W=B_12/E and
  tau=d/(E S_12)=S_h/S_12.
These are consequences of the original definition, not replacement
parameters. Each certificate separately encloses the original route,
the prefix route and the cancelled route.

All product lengths are less than odd d, and q and q^2 both have order d;
thus every root factor is nonzero. The independent exact intervals also
verify all 8662 saved root-factor squared-norm intervals and all 6461
saved division guards. This includes 1846 original Gaussian quotient
denominators, the original W denominator, the original derivative, every
prefix quotient and both final prefix denominators. Every lower bound
is strictly positive. No unguarded inversion is accepted.

All-size proof

In the principal embedding q=exp(2iv), v=pi/d, write s_j=a_j exp(-ijv),
where all a_j are positive and 0<=jv<pi/2. Consequently Re S_12>0 and
  Im((S_h-S_12) conjugate(S_12))
   =-sum_(j=13)^h sum_(r=0)^12 a_j a_r sin((j-r)v)<0.
The nonempty double sum proves tau is nonreal. Cyclotomic automorphisms
commute with complex conjugation, so tau-conjugate(tau) stays nonzero
at all primitive embeddings. This transports only nonreality, never
the metric bound. The selected certificate imaginary intervals also
exclude zero independently.

A repeated zero root requires tau=0 for odd A or tau=-1/A for even A;
the Hermite constant and linear coefficients prove these alternatives.
They are real and impossible here. Consecutive Hermite polynomials cannot
share a zero, since their recurrence would descend to He_0=0. Thus at a
nonzero repeated root, elimination using
  J'=(1+A tau)He_A+A x(1-tau)He_(A-1)
is legitimate and yields
  y=x^2=tau(1+A tau)/(tau-1)
       =A tau+(A+1)+(A+1)/(tau-1).

For A+1=2r+s, s=0 or 1, alpha=s-1/2, the Hermite factorial formula
and monic parity recurrence prove, for arbitrary r,
  J=x^s det(x^2 I-M).
The real Jacobi part has diagonal 4j+2alpha+2 for 0<=j<r and nonzero
real off-diagonal 2 sqrt(j(j+alpha)) for 1<=j<r. The last diagonal is
shifted by A(tau-1). This arbitrary-index recurrence is the proof; fresh
exact checks through A=19 corroborate conventions but do not supply an
infinite-A extrapolation.

When A>=3, a nonzero repeated root gives a repeated eigenvalue y. The
irreducible tridiagonal recurrence forces a one-dimensional eigenspace
and a nonzero last eigenvector coordinate. A repeated eigenvalue therefore
has a Jordan chain (M-yI)w=u. Complex symmetry gives u^T u=0. Taking
absolute values in u_r^2=-sum_(j<r)u_j^2 proves
  0<t=|u_r|^2/||u||^2<=1/2.
The separate Hermitian identity gives Im y=A Im tau t. With
rho=|tau-1|^2, imaginary parts of the eliminated formula give
  A t=A-(A+1)/rho,
  1+1/A<rho<=2+2/A<=8/3.
The lower endpoint is strict and the upper endpoint inclusive. No
complex-symmetric diagonalizability assumption has been made. For A=1,2
the exact discriminants are 4tau and 4(1+2tau)^3. Hence nonreal tau with
rho>8/3 excludes repeated roots for every A>=1.

For each fixed A the discriminant is a polynomial in Q[tau]. If it
vanished at one primitive embedding, Galois conjugation would force
vanishing at the certified embedding. Thus one suitable conjugate per
order proves all-primitive algebraic nonvanishing. For an arbitrary
characteristic-zero field containing q, its copy of Q(zeta_d) injects;
a nonzero discriminant remains nonzero. An embedding of the entire
ambient field into C is unnecessary.

Independent endpoint reconstruction

Fresh reviewer arithmetic uses only Python standard-library integers and
rational numbers, with 896-bit outward-rounded dyadic intervals. It
bounds pi using the different identity
  pi=4(atan(1/2)+atan(1/3)),
600 alternating terms per arctangent and the first omitted term. Tangent
addition gives tan(sum)=1 and the quadrant determines pi/4. Each root
factor and each derivative-polynomial monomial is constructed at its
directly reduced angle, whose absolute value is checked to be less than
4. The sine and cosine degrees are 639 and 638; Lagrange remainder bounds
are 4^640/640! and 4^639/639!, respectively. All evaluations and divisions
round outwards. Neither binary floating-point nor approximate search
results enter any acceptance bound.

All 994 saved complex quantities and all 213 rho intervals contain their
much narrower independent reconstructions, with containment checked after
exact integer rescaling from 896 to the candidate's 256 bits. This proves
the submitted endpoints, rather than merely numerical agreement. The
original Gaussian quotient derivative also overlaps the independently
evaluated derivative polynomial and the cleared-prefix route.

The weakest coarse witness is d=65,k=3:
  3420/1000<=rho<=3421/1000.
Its strict lower margin above 8/3 is 113/150. Every other lower coarse
endpoint is at least as strong. All 71 selected indices are coprime to
their exact order. No local-unit exception is needed or claimed.

The preserved d=53,k=1 certificate is genuinely inside the outer-annulus
threshold, with 1084/1000<=rho<=1085/1000. It independently verifies and
rejects any claim that the same exterior inequality holds at every
conjugate. Its failure of a sufficient criterion is not a repeated-root
counterexample. The successful d53 conjugate is k=24.

Source composition and exact boundaries

The pinned b23 independent acceptance has SHA256
 a067a868cde351f259d437e7a51f4db98a07f8d67934073f7e6597579ba77b5c.
The fresh source audit checks all 30 distinct nested historical archives,
CRCs, manifest member hashes and sizes. Twenty-nine have complete primary
manifests. One much older degree-nine archive excludes a single auxiliary
sources/MANIFEST_SHA256.json from its primary manifest; its exact archive
bytes are nevertheless transitively bound to the pinned b23 archive.
This known manifest-only exclusion is explicitly identified by exact
archive hash and path in SOURCE_AUDIT.json. No unlisted payload omission
is allowed. The new candidate manifest must be complete.

The general lower and improved-tail review texts and original v3 note
are identical to historical accepted copies. Their exact SHA256s are
recorded in SOURCE_AUDIT.json. The general statements have been read,
not inferred from titles. The general lower proof gives
rho=|S_(h-m-1)|^2/|S_m|^2<=1 exactly when d<=2b+1. At b25 it covers
odd 27..51, including equality rho=1 at d51, strictly below the repeated-
root annulus.

The improved-tail source proves d>=15(m+1)=15(b+1)/2. At b25 this is
d>=195. Its strict bounds give
  |S_m|^2<270(m+1)/131, |S_h|^2=d,
  |tau|^2>131d/(270(m+1))>=131/18.
The positive exact comparison (101/18)^2-4(131/18)=769/324>0 gives
rho>8/3 even at d195. All divided trigonometric factors are positive;
(2m+1)pi/d<2pi/15 is still strict at the threshold. Odd d193 is covered
by the new middle certificate and odd d195 starts the tail. There is no
uncovered order or A boundary.

Integration guidance

Add b25 to the accepted full overlap families: odd b=1,3,...,25, all
odd d>b, all primitive characteristic-zero roots and every A>=1.
The general remaining overlap strip now starts at odd b>=27:
  odd 2b+1<d<15(b+1)/2,
except separately proved cases. Its next b27 middle is odd d57..209,
77 orders; threshold 210 makes the first odd tail order 211. This review
makes no theorem claim for that next strip.

Ordinary residual squarefreeness is separate and unchanged. Accepted
ranges remain odd b<=25 at all odd d>b, and odd b>=3 at odd d>=4b^2.
Its remaining domain is odd b>=27, b<d<4b^2, except separately proved
instances. General derivative nonvanishing and separation remain inherited
accepted inputs.

The broader F020 problem remains open. No global closure or new
canonical mathematical identity is asserted. No historical priority or worldwide novelty
claim is made. Classical Hermite/Laguerre/Jacobi and inherited
Carlitz/Grosu–Grosu/Sawa–Uchida attribution is preserved; the Carlitz
original has not been newly read. Even order, nonprimitive roots, A=0,
positive characteristic, quantitative conditioning and universal good-
prime assertions are outside scope.

Negative controls and portable replay

Twenty-nine mathematical, endpoint, domain and normalization mutations
are rejected, including omitted d, duplicate d, nonprimitive k, dropping
the factor d from tau, finite-A scope, wrong Hermite degree, corrupt
cyclotomic/prefix/cancellation data, forged rho bounds, omitted or zero
divisor guards, false universal-conjugate bounds and unsafe zero inversions.
Four independent archive mutations reject wrong pins, changed payloads,
missing payloads and unbound payloads.

The independent review archive carries the frozen candidate, complete
independent results, source audit, review and exact row guidance, plus
fresh reviewer programs. Portable cold replay verifies the full sealed
manifest, extracts into a fresh temporary directory, and runs only the
reviewer's new programs under isolated Python. It requires byte-for-byte
reproduction of the mathematical and source results. The external cold
receipt binds to the final review archive without circular self-reference.
Its PASS receipt is required before downstream integration.

Repository derivative disclosure: private tracking and integration instructions
were removed; all proof, source-composition and mathematical limits are
preserved. Original review SHA256: 51cf06b8b5b6a920deebeb4c4b354df5b6d1c2e49f9d42361e17c323a739ad30.
