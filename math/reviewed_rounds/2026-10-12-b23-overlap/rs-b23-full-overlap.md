# Independent review: Rogers–Szegő parameter b=23 full overlap family
12 October 2026 UTC
Bounded ACCEPT; consult the external cold receipt for portable replay verification

1. Decision and exact scope

The new middle theorem is accepted for b=23, every odd d=49,51,...,179,
every primitive order-d root q in characteristic zero, and every integer
A>=1. The polynomial is exactly
  J_(A+1)(x;tau)=x He_A(x)-A tau He_(A-1)(x),
where He_0=1, He_1=x and He_(n+1)=x He_n-n He_(n-1). Its degree is A+1,
not b. The original parameter is tau=d W/H'_23(-1;q), with
  W=product_(r=1)^23(1-q^r)/product_(r=1)^((d+23)/2)(1-q^(2r)).
The conclusion is Disc_x J_(A+1)!=0. No finite-A extrapolation is used.

Sixty-five outer-annulus certificates cover the odd orders 51..179.
The remaining order 49 has a genuine residue-field certificate at p=3.
The pinned accepted general lower theorem covers odd d=25..47 and the
improved general tail covers odd d>=181. Thus these results compose to
EVERY odd d>23, every primitive q in characteristic zero, and every A>=1.
Full overlap families b=1,3,...,21 remain inherited accepted inputs.

Frozen candidate SHA256: 7eac463290af07926bb43861db6f215c6a6f3ec1ba3f209b3f7dbcc1f6e327db
Frozen certificate SHA256: d80d731b961734454502ea5f23698e3388cffbe11258698727affaf160d590ac

The archive and certificate hashes, exact counts and source results are
in VERDICT.json and SOURCE_AUDIT.json. This review did not run or import
any author or historical program. All arithmetic was independently
implemented in arithmetic.py and verify_certificate.py; audit_sources.py
treats the prior archives and source programs solely as inert bytes.

2. Original normalization and denominator guards

The fresh arithmetic constructs all 24 Gaussian coefficients by polynomial
Pascal recursion over Z[X] and verifies each original quotient identity
by exact multiplication with the two denominator products. Differentiating
the original coefficient polynomials gives g=H'_23(-1;q). A separately
constructed cleared prefix sum gives exactly the same integer polynomial:
  g=B_11 S_11,
  B_j=product_(r=1)^j(1-q^(2r)),
  s_j=product_(r=1)^j(1-q^(2r-1))/(1-q^(2r)), S_j=sum_(r=0)^j s_r.
At h=(d-1)/2 put E=B_h. The derivative recurrence at degree d, where
H_d=1+z^d, gives E S_h=d. All 66 orders pass an independent cyclic
integer-coefficient reconstruction of that identity modulo Phi_d.

The original W cancellation is checked by exact exponent multisets:
its denominator after E consists precisely of the odd numerator factors.
Therefore W=B_11/E and tau=S_h/S_11=d/(E S_11). These are identities of
the ORIGINAL quantities, not new definitions or numerical agreements.

All original product lengths are below d. Since d is odd, q and q^2
both have exact order d, so none of their root factors vanishes. The
fresh checker rebuilds each Phi_d recursively from X^d-1 and verifies
g modulo Phi_d is nonzero. Cyclotomic irreducibility over Q, a standard
exact theorem, makes this an all-primitive-root nonvanishing statement.
The complex certificates independently guard all 7410 root factors
and every displayed original product or derivative inversion. No
arbitrary nonzero quotient-ring element is silently treated as a unit.

3. The infinite-A annulus proof

In the principal embedding q=exp(2iv), v=pi/d, write s_j=a_j exp(-ijv).
Every a_j is positive and 0<=jv<pi/2. Thus Re S_11>0. Since h>11,
  Im((S_h-S_11) conjugate(S_11))
    =-sum_(j=12)^h sum_(r=0)^11 a_j a_r sin((j-r)v)<0.
Hence tau is nonreal. Cyclotomic automorphisms commute with complex
conjugation; nonreality holds at every primitive embedding. This does
not transport any norm inequality.

A multiple zero root requires tau=0 for odd A or tau=-1/A for even A,
by the constant or linear Hermite coefficients. Both are real and are
excluded. At a nonzero multiple root, consecutive Hermite polynomials
cannot vanish simultaneously: their recurrence would descend to He_0=0.
Differentiation of the original J gives
  J'=(1+A tau)He_A+A x(1-tau)He_(A-1).
Legitimate elimination therefore yields
  y=x^2=tau(1+A tau)/(tau-1)
       =A tau+(A+1)+(A+1)/(tau-1).

For A+1=2r+s, s in {0,1}, alpha=s-1/2, the factorial Hermite formula
proves the parity recurrence and the identity
  J=x^s det(x^2 I-M).
Here M is the real symmetric Jacobi matrix with diagonals 4j+2alpha+2,
0<=j<r, off-diagonals 2 sqrt(j(j+alpha)), 1<=j<r, and last-diagonal
shift A(tau-1). The recurrence proves this for arbitrary A.

For A>=3 a nonzero repeated x gives a repeated eigenvalue y. All
Jacobi off-diagonals are nonzero, so the eigenspace has dimension one
and its last coordinate is nonzero. A repeated eigenvalue then has a
Jordan chain (M-yI)w=u. Complex symmetry implies u^T u=0. The bilinear
identity gives 0<t=|u_r|^2/||u||^2<=1/2. Separately, the Hermitian
identity gives Im y=A Im tau t. Using rho=|tau-1|^2 in the rational
expression above and dividing by the nonzero Im tau gives
  A t=A-(A+1)/rho,
  1+1/A<rho<=2+2/A<=8/3.
The lower endpoint is strict and the upper endpoint is inclusive.
Diagonalizability of the complex symmetric matrix is not assumed.
For A=1,2 the exact discriminants are 4tau and 4(1+2tau)^3. Thus a
nonreal witness with rho>8/3 excludes multiple roots for EVERY A>=1.

4. Fresh containment checks of all frozen interval endpoints

The independent implementation uses 704-bit outward-rounded dyadic
intervals, with only exact integer arithmetic. It obtains pi from
300 terms in each arctangent in Machin's identity, using the first
omitted alternating term as a one-sided error bound. All root angles
are reduced to (-pi,pi); the checked radius is less than 4. It uses
separate cosine and sine polynomials of degrees 478 and 479, with
valid absolute remainders 4^479/479! and 4^480/480!, respectively.

Unlike the author q-power factor propagation, the independent checker
constructs EACH root factor at its directly reduced angle. Original
Gaussian products, W, g, E, B_11, S_11, S_h, and all three tau routes
are reconstructed. The polynomial derivative is checked separately.
All 910 complex quantity enclosures and 195 norm enclosures fit inside
the frozen candidate endpoints, rather than merely agreeing to decimal
precision. Every saved denominator and root-factor lower bound is
positive and bounded above by the independent exact lower bound.

The weakest coarse witness is d=55,k=16:
  2942/1000 <= rho <= 2943/1000.
Its strict margin above 8/3 is 413/1500. All other certified coarse
lower endpoints are at least as large. Floating-point searches were
used only to suggest primitive indices and supply no proof evidence.

5. Exact local certificate at order 49

At p=3, which does not divide 49,
  Phi_49=X^42+X^35+X^28+X^21+X^14+X^7+1
is irreducible. Fresh arithmetic verifies X^(3^42)=X modulo Phi_49
and the three Rabin gcd tests for degree prime divisors 2,3,7. It also
checks separability and exact root order: X^49=1 while X^7-1 is a unit.
Thus the quotient is an actual field F_(3^42), established before any
field argument, and defines a prime of the cyclotomic field above 3.

The original products and every Gaussian quotient are reconstructed
in this residue field. All 48 root-factor inverses, 23 nonconstant
Gaussian denominator inverses, original W denominator inverse and
g inverse are checked by exact multiplication. Consequently the
ORIGINAL tau is integral at this prime and reduces to the displayed
candidate t. Independent prefix and W-cancellation routes agree.
There is no need to assume that an unrelated rational denominator
happens to be prime to 3: local integrality follows directly from the
checked original denominator units.

The ascending coefficients of t are
 [0,2,0,1,0,2,1,2,0,0,0,1,2,2,2,2,2,2,1,2,2,1,2,2,1,0,2,0,0,1,
  0,0,2,0,2,0,2,2,2,2,1,2].
The values t, t-1, t^3-t and 1+a t for a=0,1,2 all have exact saved
inverse witnesses. In particular t is outside the prime field.
For r=1,2 the original monic polynomials are
  R_1=x^2-t, R_2=x^3-(1+2t)x.
Their integer discriminants are 4t and 4(1+2t)^3; their residue
values and inverse witnesses match independent evaluation exactly.
One may also see coprimality directly: R_1 and 2x have Bezout
coefficients -t^(-1) and x/(2t), while R'_2=-(1+2t) is a unit.

6. Why the local certificate covers all A, including divisible A

The Hermite recurrence gives He_3=x^3 and He_4=x^4 modulo 3.
Induction in n then gives He_(n+3)=x^3 He_n for every n>=0, because
n and n+3 have the same residue. Hence
  He_(3u+r)=x^(3u) He_r, 0<=r<3, for every u>=0.
This is an arbitrary-index identity, not a finite scan over A.

Because t is outside F_3, tau, tau-1 and 1+A tau are local units for
every integer A. The zero-root possibilities tau=0 and tau=-1/A are
impossible. The latter is nonintegral if 3 divides A and otherwise
has prime-field residue.
At a hypothetical nonzero multiple root, the elimination formula
makes x^2=tau(1+A tau)/(tau-1) a local unit. Extend the valuation to
the field containing x; then x is a unit and its residue xbar is
nonzero. If A=3u+r, r=1,2, reduction gives
  J=x^(3u)R_r, J'=x^(3u)R'_r.
The common nonzero root would contradict the checked coprimality.
If r=0 then J reduces to x^(A+1), which has no nonzero root. This
covers every A>=1 in characteristic zero.
At A=3 the whole reduction is x^4 and has a repeated zero. That
explicit boundary control rules out the false claim that the entire
reduced polynomial must be squarefree. Only the characteristic-zero
conclusion is accepted.

7. All primitive roots, source composition and scope preservation

For each fixed A, D_A(T)=Disc_x J_(A+1)(x;T) lies in Q[T]. Vanishing
at any primitive embedding would imply vanishing at the certified
annulus conjugate, or at the algebraic tau excluded by the local
argument. Therefore nonvanishing holds at every primitive root.
Any characteristic-zero field containing such a root contains an
injective image of Q(zeta_d); nonzero discriminants stay nonzero.
An embedding of the whole ambient field into C is unnecessary.

The source audit checks ten complete historical archive manifests,
CRCs and pinned digests along the accepted b21, b19, b17, general
prime-criterion and b15 chain. The general lower and improved-tail
texts are byte-identical to the exact accepted source copies.
Their explicit theorems are valid for general odd b, despite the
degree-nine title of the tail source. At b=23, the lower theorem
gives odd 25..47, the new middle gives odd 49..179, and the tail
threshold d>=180 gives first odd order 181. No order is missing.
The strict tail comparison is
  |tau|^2>131d/(270*12)>=131/18,
  (101/18)^2-4*(131/18)=769/324>0,
which implies rho>8/3. All size quantifiers remain A>=1.

The general F020 problem remains open. This bounded acceptance preserves all prior results and unresolved broader obligations.

After this bounded acceptance the remaining general overlap strip
starts at odd b>=25, odd 2b+1<d<15(b+1)/2, except separately proved
instances. The next concrete b25 middle is odd d=53..193, 71 orders.
Ordinary residual squarefreeness is separate and unchanged: accepted
for odd b<=25 at all odd d>b and for odd b>=3 at odd d>=4b^2; the
remaining general residual range is odd b>=27, b<d<4b^2, except
separately proved instances. General derivative nonvanishing and
separation remain separate accepted inputs.

Even orders, nonprimitive roots, A=0, positive-characteristic claims,
universal good-prime claims, conditioning and worldwide novelty are
outside this acceptance. Classical Hermite/Laguerre/Jacobi and
Carlitz/Grosu-Grosu/Sawa-Uchida attribution is unchanged. The Carlitz
original has not been newly read. Historical priority remains open.

8. Negative controls and portable cold replay

Thirty-seven independent mathematical/domain/certificate mutations
are rejected, including wrong normalization, finite-A scope, missing
or duplicated orders, nonprimitive indices, forged norm endpoints,
nonunit denominator guards, corrupt local primes/moduli/inverses,
omitted residue classes, and whole-reduction overclaims. Nonzero
nilpotents in a genuinely nonfield quotient are explicit controls
against silently interpreting a quotient ring as a field. Three
archive/hash/manifest corruptions are rejected separately.

The review archive contains the frozen candidate, independent exact results, source audit, fresh reviewer programs and this report. Portable replay validates all archive
members, extracts into a fresh temporary directory and reruns ONLY
the independent reviewer programs under isolated Python. It requires
byte-for-byte equality with both saved arithmetic and source outputs.
The cold receipt is external to the sealed archive, avoiding circular
self-reference. Consult its PASS result before downstream integration.

Derivative note: private tracking snapshots, cell-address and administrative-count instructions are omitted. The complete proof, exact witnesses, original normalization, lower/tail composition, classical attribution and remaining scope are unchanged. Original report SHA-256: `92336c746d6cab0c8f31b6707b945b2ad7c84ca4eb0d80a45adc7b060a7e0394`.
