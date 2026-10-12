# Independent review of Rogers–Szegő overlap for b=21
ACCEPT for the bounded scope below
12 October 2026 UTC

## Decision

The frozen candidate proves the original Rogers-Szego overlap discriminant
nonzero for b=21, every odd d=45,47,...,163, every primitive order-d root
in characteristic zero, and every integer A>=1. Its fifty-nine annulus
certificates and its separate d=45 certificate at prime 7 pass a freshly
authored independent verifier. The written uniform arguments are valid.
No mathematical repair to the candidate is required.

The pinned accepted general lower strip gives odd d=23,...,43, and the
pinned improved general tail gives odd d>=165. Consequently the full
b=21 overlap family holds for every odd d>21, every primitive root in
characteristic zero, and every A>=1. The accepted full families through
b=19 remain unchanged. The global F020 gate remains progressed/open.

Frozen candidate
  RS_B21_Middle_Overlap_CANDIDATE_2026-10-12.zip
  25658794 bytes
  SHA256 9ba5fd3d162ff17823025bbad00774f078810f2c1764e6326024fd194cf1af8b
  20 complete manifest entries
  Certificate SHA256
  096bba01fc7958ccb9cea2162dc4ec9e91cdd63b38b264f51fc35d22939d7270

## 1 Original quantities and independent arithmetic

The parameter is exactly tau=dW/g, where
  H_21(z;q)=sum_j [21 choose j]_q z^j,
  g=H'_21(-1;q),
  W=product_(r=1)^21(1-q^r) /
    product_(r=1)^((d+21)/2)(1-q^(2r)).
The polynomial is J_(A+1)=x He_A-A tau He_(A-1), with He_0=1,
He_1=x and He_(n+1)=x He_n-n He_(n-1). Its degree is A+1; b=21
is the separate Rogers-Szego parameter.

The fresh verifier builds all Gaussian coefficients by polynomial Pascal
recurrence and checks all 22 original quotient identities over Z[X]. It
constructs g both by direct differentiation and by the cleared prefix
formula. Exact equality of the degree-110 coefficient arrays is required.

For all sixty d, integer cyclotomic arithmetic independently checks the
original W cancellation and E S_h=d, where h=(d-1)/2,
  E=product_(r=1)^h(1-q^(2r)),
  B_10=product_(r=1)^10(1-q^(2r)),
  S_j=sum_(v=0)^j product_(r=1)^v(1-q^(2r-1))/(1-q^(2r)).
The prefix identity gives g=B_10 S_10 and tau=S_h/S_10=d/(E S_10).
The cyclotomic polynomials are rebuilt recursively from X^d-1. Their
irreducibility over Q is the standard cyclotomic theorem; a nonzero
derivative remainder therefore proves g does not vanish at a primitive
root. Original product factors are nonzero because q and q^2 have exact
order d and all product lengths are below d.

No author or historical program was imported or executed. The three new
reviewer programs are independent_math.py, verify_certificate.py and
audit_sources.py. They use only the Python standard library. The author
proof and certificates, and the accepted predecessor texts, were read as
inert input data.

## 2 The uniform annulus argument

The inherited principal-embedding sector proof gives g nonzero and tau
nonreal. In that embedding s_j=a_j exp(-ij*pi/d), a_j>0, j<=h, and
  Im((S_h-S_10) conjugate(S_10))
   =-sum_(j=11)^h sum_(r=0)^10 a_j a_r sin((j-r)*pi/d)<0.
All arguments of the sine are strictly between zero and pi/2. Nonreality
transfers to other primitive embeddings because cyclotomic automorphisms
commute with complex conjugation. A metric bound does not transfer by
this argument.

The repeated-zero cases are exactly tau=0 for odd A and tau=-1/A for even
A, obtained from the constant and linear Hermite coefficients. Nonreality
excludes both. At a nonzero repeated root, consecutive Hermite factors
cannot vanish simultaneously; descent in the recurrence reaches He_0=1.
The differentiated original J then gives
  x^2=tau(1+A tau)/(tau-1).
Every divided factor is nonzero under these hypotheses.

For A>=3, the parity Hermite recurrence gives J=x^s det(x^2 I-M), where
A+1=2r+s and M is the real Jacobi matrix with diagonal 4j+2alpha+2,
off-diagonal 2 sqrt(j(j+alpha)), alpha=s-1/2, and last-diagonal addition
A(tau-1). This is an identity for arbitrary A. The nonzero off-diagonals
make every eigenspace one-dimensional and an eigenvector's last entry
nonzero. A repeated eigenvalue therefore has a Jordan chain. Complex
symmetry gives u^T u=0; this is a bilinear, not Hermitian, identity.
It implies 0<t=|u_r|^2/||u||^2<=1/2. The separate Hermitian identity and
the displayed formula for x^2 give
  A t=A-(A+1)/rho,   rho=|tau-1|^2.
Thus any multiple root forces
  1+1/A<rho<=2+2/A<=8/3.
The strict lower endpoint and inclusive upper endpoint are correct.
The argument never assumes diagonalizability of the complex symmetric
matrix. For A=1,2, the exact discriminants are 4tau and
4(1+2tau)^3. Hence a witness with nonreal tau and rho>8/3 proves all A>=1.

## 3 Fifty-nine reconstructed interval certificates

The independent implementation uses 640-bit outward-rounded dyadic
intervals. It obtains pi from 230 alternating terms per arctangent in
Machin's identity, with the next-term signed bound. It first reduces
angles to [-pi,pi], then uses separate real sine and cosine Taylor sums
of degrees 359 and 358. Remainders are bounded by 4^360/360! and
4^359/359!, respectively. The angle-radius guard |theta|<4 is checked.
These choices differ from the author's 512-bit complex exponential
construction and its 256-term arctangents.

All 767 complex enclosures (13 quantities per order) lie inside the frozen
candidate intervals. They include q, the original W numerator and full
denominator, W, the original and polynomial derivatives, E, B_10, S_10,
S_h, and all three tau constructions. All 177 candidate rho enclosures
also contain independently reconstructed bounds. All 6136 individual
nontrivial root-factor lower bounds and 4602 recorded division guards
are verified positive and no larger than the independent lower bounds.
The candidate's coarse rational bounds are checked too. The smallest
outer lower bound is 3123/1000 at d=55, exceeding 8/3 by 1369/3000.

This certifies the actual frozen endpoints, rather than merely finding
nearby floating values. The exact cyclotomic identities separately establish
normalization. No finite-A experiment supplies the infinite A quantifier.

## 4 The exceptional order forty five

The characteristic-zero annulus method need not provide an all-A witness
at d=45. The candidate instead uses p=7, which does not divide 45.
Fresh arithmetic verifies Phi_45 is separable modulo 7 and factors as
  (X^12+2X^9+4X^6+X^3+2)
  (X^12+4X^9+2X^6+X^3+4).
Both factors pass the full degree-12 Rabin test: X^(7^12)=X and the
required gcd tests for degree divisors 2 and 3. Root-order checks verify
X^45=1, while X^9-1 and X^15-1 are units in the full quotient.

The verifier works in R=F_7[X]/Phi_45, a product of fields, and never
silently treats that quotient as a field. It independently reconstructs
the original W and every Gaussian quotient, checking all inverse guards,
and independently differentiates the Gaussian polynomial. It obtains
  t=[4,0,1,6,0,5,5,5,3,6,6,6,3,4,1,3,3,2,0,3,0,4,2,3]
in ascending powers of X. The candidate's characteristic-zero rational
tau, whose common denominator is 12449190864385801585529191, is verified
by cross multiplication against the ORIGINAL W denominator and g in
Q[X]/Phi_45. The denominator is coprime to 7 and its reduction gives
the same t. All forty-four saved root-factor inverses are checked.

The values t^7-t, t, t-1, and 1+a t (a=0,...,6) are units. Thus at either
of these two specific primes above 7 the parameter is integral and its
residue lies outside F_7. This is an exact statement for this case, not
a universal good-prime theorem.

For r=1,...,6, define R_r=x He_r-r t He_(r-1). Two genuinely separate
checks exclude common roots of R_r and its derivative:
- Fraction-free Sylvester determinants over Z[T] reconstruct all six
  integer discriminants, reduce them modulo 7, and verify the candidate
  values and multiplicative inverses.
- Euclidean arithmetic over R constructs explicit polynomial Bezout
  identities U_r R_r+V_r R'_r=1. Every leading coefficient divided by
  during this calculation is itself checked to be a unit of R.
Both sets of results are retained in INDEPENDENT_RESULTS.json.

## 5 Why the six residue classes prove every A

For any odd prime p, the factorial formula gives He_p=x^p modulo p:
every lower coefficient contains an uncancelled factor p. The recurrence
gives He_(p+1)=x^(p+1), and induction gives He_(n+p)=x^p He_n for every
n>=0. Thus He_(pu+r)=x^(pu) He_r for every u>=0 and 0<=r<p.

Suppose tau is integral at a prime above p with residue t outside F_p,
and each R_r (1<=r<p) is squarefree over the residue field. The values
tau, tau-1 and 1+A tau are units for every integer A. A zero multiple root
would require tau=0 or tau=-1/A. The second value is nonintegral if p|A,
and otherwise has prime-field residue; neither is possible.

At a hypothetical nonzero multiple root, x^2=tau(1+A tau)/(tau-1) is a
local unit. After extending the valuation to a field containing x, x is
therefore a unit and has nonzero reduction. If A=pu+r with r>0, then
  J_(A+1)=x^(pu) R_r,   J'_(A+1)=x^(pu) R'_r modulo p.
Their common nonzero reduction contradicts the checked Bezout identity.
If r=0, J reduces to x^(A+1), which cannot vanish at this nonzero residue.
The contradiction is uniform for all u and hence for every A>=1.

The p=7,d=45 certificate meets all these hypotheses. The finite six-class
verification is a check of an arbitrary-index recurrence theorem, not an
extrapolation from six sizes. At A=7 the entire reduction is x^8, which
has a repeated zero. This remains an explicit warning against claiming
squarefree reduction of the whole J. Only the characteristic-zero result
is accepted.

## 6 Conjugates and accepted source composition

For each fixed A, D_A(T)=Disc_x J_(A+1)(x;T) lies in Q[T]. If it vanished
at one primitive embedding, it would vanish at the certified conjugate
or at the locally certified algebraic parameter. The uniform proofs
exclude this. Consequently discriminant nonvanishing holds at every
primitive embedding, and then in any characteristic-zero field containing
a primitive order-d root via its injective cyclotomic subfield map. No
embedding of the entire ambient field in C is assumed.

The independent source audit verifies the current candidate CRC and all
20 manifest entries, all six current source pins, and eight complete
historical archive manifests along the accepted chain. The two general
source texts agree byte-for-byte with the accepted b15 candidate texts
reached through the b19, b17, general-prime and b15 acceptance chain:
- General lower-strip review SHA256
  c4009870cdb96f0af09065b4e41e98346d8159cc3962d7954a92b73963b2e78c.
- Improved general-tail review SHA256
  4f3ef60634b8bc1962e22d28ad3d5254b9d9ce49d21c749040db131a92835a79.
The full b19 acceptance has SHA256
  36fc43fd11e91d6af485181bc0e1183d30e51385d01abd8e6d8035653b57857c.

Despite the tail source's degree-nine title, its theorem is explicitly
valid for every odd b>=1. At b=21 the lower endpoint range is 23..43,
the new middle is 45..163, and the tail starts at 165. The tail's strict
bound |tau|^2>131/18 gives rho>8/3 because
  (101/18)^2-4*(131/18)=769/324>0.
There is no missing order or A endpoint.


## 7 Scope and replay boundary

The accepted new scope is full b21 overlap, not a theorem for all b.
Complete accepted overlap parameter families are b=1,3,...,21. The
remaining general overlap strip begins at odd b>=23, with
2b+1<d<15(b+1)/2 except separately proved instances. The next concrete
b23 middle is the sixty-six odd orders 49..179.

Ordinary residual squarefreeness remains separate and unchanged: accepted
for odd b<=25 at all odd d>b, and for odd b>=3 at odd d>=4b^2. The general
residual remainder is odd b>=27, b<d<4b^2, except separately proved cases.
The accepted derivative-nonzero and separation guards remain independent
inputs. The broader F020 problem remains open. Classical Hermite/Laguerre/Jacobi and Carlitz/Grosu-Grosu,
Sawa-Uchida attribution is unchanged. The Carlitz original has not been
newly read and historical priority remains unresolved.

Even orders, nonprimitive roots, A=0, a positive-characteristic theorem,
quantitative conditioning, universal-prime assertions, and worldwide
novelty are outside this acceptance. The earlier bad-prime controls are
not superseded.

Twenty-nine mathematical/domain/certificate corruptions and three archive
or manifest corruptions are rejected. The review ZIP contains the frozen
candidate, fresh reviewer programs, exact results,
source audit and this report. Portable cold replay
verifies the review digest and complete manifest, extracts into a fresh
temporary directory, reruns only the new reviewer programs, and requires
byte-for-byte equality with both saved outputs. The external cold receipt
records completion and leaves the sealed archive unchanged. No author or
historical program, external service write, or finite-A proof scan occurs.

Derivative note: the title explicitly identifies b=21 as the Rogers–Szegő parameter, distinct from polynomial degree A+1. Private tracking snapshot, row instructions and administrative counts are omitted. The ambiguous phrase “nonreal rho” is clarified as nonreal tau with real rho>8/3; all proof formulas, exact source hashes, local-prime qualifications, uniform-A reasoning and remaining limits are unchanged. Original report SHA-256: `59ef2c9c838010167a15fb9d28eb850997cd3df97eeeac16101fa39b37fb862f`.
