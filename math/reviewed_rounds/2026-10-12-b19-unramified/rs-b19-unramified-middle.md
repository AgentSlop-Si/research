# Independent review of the b=19 unramified middle overlap
12 October 2026 UTC

## Decision

ACCEPT the candidate's precise bounded result: b=19, all 37 odd orders
41 <= d <= 149 with 3 not dividing d, every primitive order-d q in
characteristic zero, and every integer A >= 1. The original polynomial
J_(A+1)(x;tau) = x He_A(x) - A tau He_(A-1)(x) has nonzero discriminant,
with the original parameter tau=dW/H'_19(-1;q) and the original W products.

This is an application of an already accepted general sufficient criterion.
It is not a new general theorem or an unbounded b19 result. No mathematical
repair of the candidate is needed. The full b19 family and the global
F020::remaining-guards gate remain open. All 18 ramified middle orders remain:
45,51,57,63,69,75,81,87,93,99,105,111,117,123,129,135,141,147.

## Source and scope binding

The exact candidate is RS_B19_Unramified_Middle_Overlap_CANDIDATE_2026-10-12.zip,
24,815 bytes, SHA256
182657668bef85dd2f8ca1301134f6b844c8706ee2d857ad021d39d8cadc8997.
Its ZIP CRC, complete nine-member manifest, accepted-source member hashes,
pass independent checks. Both copied accepted-source
members are byte-identical to the accepted predecessor archive, SHA256
e1a457a85dfbd30e1910d70850255dc155f3450078c3ae721f4306e3db7cfa69.
That predecessor's review and verdict explicitly accept the general odd-b,
unramified odd-d>b criterion. They do not restrict it to b=17.

The accepted general criterion is an inherited input; its unrelated b17 theorem is not newly audited or needed for this bounded advance. The sealed review contains its source inputs for a self-contained replay.

## Independent finite verification

The fresh reviewer program uses SymPy 1.14.0 exact polynomial arithmetic and
Python 3.12.14. It does not import or execute the candidate's mathematical
program or any predecessor program. The candidate program was inspected as
source text. The new implementation uses a single fully cleared denominator
for S9, independently of the candidate's repeated rational additions, and
reconstructs the original Gaussian derivative over Z from the finite Euler
product, independently of the candidate's Gaussian Pascal recurrence.

The normalized S9=N9/D9 has deg N9=deg D9=59 and monic D9. Its numerator
and denominator are coprime, D9 divides the original B9, and the original
Gaussian derivative satisfies g D9=B9 N9 modulo three. The obstruction
P9=N9^8-X D9^8 has degree 473. Every recorded coefficient matches.

For every named order, the checker independently builds the integer
cyclotomic polynomial, reduces it modulo three, and verifies separability
and exact order of every root. Exact-order verification additionally checks
coprimality with X^(d/l)-1 for every prime divisor l of d. It then rebuilds
the complete nonzero remainder of N9 P9, the bad gcd H, and K=C/H. Every
stored case field, including K and the complete tau residue, matches.

The positive-degree polynomial K need not be irreducible. All inversions
are verified in the quotient algebra; gcd(K,N9 P9)=gcd(K,D9)=1. In that
algebra the independently reconstructed t=dD9/(E N9) satisfies
  gcd(K,t^3-t)=1,
  t^8 N9^8=X D9^8,
  E^8 X=1.
The three possible A residues separately give units 1+A t. Both t and t-1
are units. Thus every irreducible factor of K supplies a genuine good prime;
no field property is silently assigned to a reducible quotient.

The checker independently multiplies every original factor in
  W = product_(r=1)^19(1-q^r) /
      product_(r=1)^((d+19)/2)(1-q^(2r)),
then verifies dW/g=t and WE=B9. Every individual original product factor
is a unit. No shortened or rescaled W is substituted without equality
checks. This is important because the denominator length depends on d.

## The uniform A argument

The accepted local lemma has also been checked directly. Fix a prime above
three where tau is integral and its residue t is outside F3. Then tau,
tau-1 and 1+A tau are units for every integer A: reduction of A has only
three possibilities. This is a universal arithmetic statement, not a
finite range of A verified by computation.

For odd A, a zero root would require tau=0. For even A, a repeated zero
would require tau=-1/A. If 3 divides A, this is nonintegral; otherwise its
residue lies in F3. Both possibilities contradict the selected prime.

For a nonzero hypothetical common root of J and J', consecutive Hermite
polynomials cannot both vanish in characteristic zero, by descending the
recurrence to He_0=1. Differentiation and elimination give
  J'=(1+A tau)He_A + A x(1-tau)He_(A-1),
  x^2=tau(1+A tau)/(tau-1).
All denominators used here are legitimate: A is nonzero in characteristic
zero, and tau-1 is a local unit. The displayed square is a local unit, so
at an extended valuation x and x^(-1) are integral and the reduction of x
is nonzero.

Modulo three the Hermite recurrence, by induction in blocks of three, is
  He_(3u)=x^(3u),
  He_(3u+1)=x^(3u+1),
  He_(3u+2)=x^(3u)(x^2-1).
Accordingly J reduces to x^(3u) times x, x^2-t, or x^3-(1+2t)x,
according as A is 0,1,2 modulo three. At a nonzero root, the first is
nonzero, the second has derivative 2x nonzero, and the third has derivative
t-1 nonzero. This contradicts a repeated root and proves the all-A claim.
Finite Hermite controls in the checker only corroborate this induction.

In particular, J4 reduces to x^4 and has a repeated zero modulo three.
This does not undermine the characteristic-zero theorem: the local-unit
identity rules out reducing a hypothetical characteristic-zero multiple
root to zero. Whole-polynomial squarefree reduction is neither asserted
nor used. No factorial or Laguerre normalization is inverted locally.

One good prime suffices for the number-field discriminant to be nonzero.
Cyclotomic conjugation then transfers that nonvanishing, together with the
original rational-function definitions, to every primitive q. An embedding
of the cyclotomic field in any characteristic-zero field is injective, so
nonvanishing survives. No universal claim about the primes or valuation
signs of every conjugate is needed.

## The bad prime at order 121

The reviewer independently confirms
  F=X^5+X^4+X^2+2X+2,
  gcd(C121,N9)=F, gcd(C121,P9)=1, deg K121=105.
Irreducibility is checked by excluding every monic factor of degrees one
and two. Every reducible quintic has such a factor. This is independent of
the candidate's Rabin check. Exact modular powers show X^121=1 and
X^11!=1 modulo F, so all its roots have order 121.

At this prime N9 and the original g vanish, whereas d, D9, B9 and every
original factor of W are units. The original g is nonzero in the number
field, as follows independently from a good factor of C121. Consequently
v(g)>0, v(dW)=0, and v(tau)<0. This genuinely refutes every-prime-good
wording. It does not exhibit a repeated root of the original polynomial.
The other 36 tested orders have bad gcd equal to one.

## Controls and reproducibility

FRESH_REVIEW_RESULTS.json records all 3,672 positive checks and 27 rejected
negative controls, including malformed coefficient arrays, invalid orders,
zero/nonzero nonunits, coefficient corruption, omitted orders, omitted d121
and false every-prime-good data. Logical controls retain the distinctions
between nondivisibility and coprimality, separable and inseparable tests,
and t^8=1 versus membership in F3.

Run python review_b19_independent.py from an extracted review packet with
SymPy 1.14.0 available. It uses only enclosed source inputs and writes its
fresh results beside the program. The manifest and integrity checker seal
the reviewed material. A clean extracted replay is recorded separately.
The original sealed candidate directory is fingerprinted before and after;
no file there is edited. No external write is performed by this review.

## Remaining work and preserved attribution

The next b19 middle task is precisely the 18 ramified orders, uniformly for
every A>=1. The unramified reduction argument cannot be reused unchanged:
reduction can lower exact order, d reduces to zero, and factors of E can
be nonunits. The broader overlap remainder and the separate ordinary
residual strip for odd b>=27 remain as inherited except for separately
accepted evidence. No acceptance of even orders, nonprimitive roots, A=0,
positive-characteristic squarefreeness or quantitative conditioning occurs.

Classical Hermite/Laguerre/Jacobi, Carlitz/Grosu-Grosu and Sawa-Uchida
attribution is preserved. This review did not newly inspect primary papers
or read the Carlitz original. No new theorem identity, full-family closure, historical-priority or novelty claim is added.

Derivative note: private tracking snapshots, identifiers and administrative counts are omitted. The proof, original normalization, bounded order list, bad-prime example and remaining limits are unchanged. Original report SHA-256: `b04daed78b8dd40383bf2c2b9af04bc9d4f68ab587fef3097955d5d00854ea91`.
