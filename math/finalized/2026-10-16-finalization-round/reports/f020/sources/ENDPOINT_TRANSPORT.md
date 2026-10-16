# Off-line complementary endpoint transport for F020

13 October 2026 UTC. Author-proved candidate; independent review is pending.

## Result and limitation

The accepted complementary endpoint identity has an additional useful consequence: paired endpoint zeros at the same index transfer to an explicit affine pair at the complementary index. The coefficient needed for this transfer is an eighth root of the parameter, with no arbitrary root choice.

This gives a new uniform endpoint-only conclusion relative to the inspected packet:

**For every integer m >= 1, and every characteristic-two parameter of exact odd order d equal to 2m+3, 2m+5, or 2m+7, the two actual endpoint values E_m(alpha) and E_m(alpha^-1) cannot both vanish.**

The proof uses three fixed, small complementary-index polynomial identities, not a new fixed-b census or extension to b=33. The statement quantifies over all m and all primitive components of each indicated order. Composite orders are included. These lines were not the prior balanced line d=4m+3, though individual intersections are possible.

This does not prove the all-four-channel support theorem, or exclude a one-sided endpoint zero on a split inverse pair. It does not prove arbitrary off-line endpoint support, ordinary characteristic-zero residual squarefreeness, or all-A overlap. No historical originality is asserted.

## 1. Source-bound current obligation

The current_round_reconciliation_v5_2053 task selects F020 uniform-support contract work at 58/100 and explicitly excludes repeating either completed b31 stage or substituting another fixed-b census. Its source and the relevant accepted mathematical sources are copied unchanged and hashed in SOURCE_BINDINGS.json.

In the accepted characteristic-two normalization,

H_(2m+1)(z;q) = (z+1) U_m(z;q),
U_m(z;q) = z^m P_m(z+z^-1;q),
P_m(X;q) = A_old(X^2;q) + X B_old(X^2;q),
E_m = P_m(0;q), R_m = Res(A_old,B_old), Q_m = E_m R_m.

The full target is (Q_m,Q_m*)=(1) after inverting L_(2m+1), where

L_(2m+1) = product_(j=0)^m (1+q^(2j+1)),
Q_m* = q^N Q_m(q^-1), N=m(m+1)(2m+1)/3.

The accepted quadratic descent makes this equivalent to the prescribed-support statement for its balanced coefficient pair. That equivalence is complete; its conclusion is not yet proved. All actual reversal degrees and the m=1 boundary must be retained.

Why both E and R are essential: a simple nonzero root X of P has two distinct nonzero preimages under z+z^-1. The only finite ramified value is X=0, whose preimage z=1 is double. Thus U is squarefree precisely when E and the ordinary trace collision factor R are nonzero. A paired failure can use endpoint/endpoint, endpoint/collision, collision/endpoint, or collision/collision. Excluding only paired endpoint zeros is strictly weaker than the full target.

The accepted complementary full-chain argument supplies a squarefree full spectrum and excludes shared collision coordinates. Its accepted synthetic countermodel has different repeated coordinates in the two complementary blocks. It therefore prevents promotion of the result below to the collision channels by an argument using only reflection, nonzero edges, or full-chain semisimplicity.

## 2. Endpoint conventions and the accepted complementary identity

Work over any characteristic-two field K containing alpha of exact odd order d=2h+1>=3. For j>=0 set

C_j(q) = product_(r=1)^j (1+q^(2r)),
D_j(q) = product_(r=1)^j (1+q^(2r-1)),
E_0=1,
E_j = D_j + (1+q^(2j)) E_(j-1),
E_j* = q^[j(j+1)] E_j(q^-1).

The recurrence and deg E_j=j(j+1) are accepted at all j. They can also be derived by ordinary differentiation of the Gaussian degree recurrence at z=1. E_0*=1 is the seed; no zero-degree boundary is omitted.

For m,n>=0 with m+n=h-1, the accepted exact identity is

C_h C_n E_m + D_h C_m E_n* = C_m C_n.                 (2.1)

Here and below products in equations specialized at alpha are evaluated at alpha. Every C_j,D_j for j<=h is nonzero: its factor exponents lie strictly between zero and d. This remains true for composite d because alpha has exact order d, not merely alpha^d=1.

The source theorem SHA256 is 2c3fe11c5c1016924b89616940020b246b640d6c98b25da6648c4f70b071d93e. The prior independent review accepts (2.1), including m=0 and n=0, but only states the balanced same-index endpoint corollary. No historical program from that packet was executed here.

## 3. Half-product eighth-root lemma

**Lemma.** At every such alpha,

C_h D_h=1,  D_h^8=alpha,  C_h^8=alpha^-1.             (3.1)

Moreover C_h(alpha^-1)=D_h(alpha) and D_h(alpha^-1)=C_h(alpha).

**Proof.** The d distinct d-th roots are 1,alpha,...,alpha^(d-1), since d is odd. Evaluating (X^d+1)/(X+1) at X=1 gives

product_(r=1)^(d-1)(1+alpha^r)=d=1 in K.

This is C_h D_h=1. The odd exponent set is the negative of the even exponent set modulo d, so

D_h=product_(r=1)^h(1+alpha^(-2r))
   =alpha^[-h(h+1)] C_h.

Consequently D_h^2=alpha^[-h(h+1)]. Raise this equality to the fourth power. Since 4h(h+1)=d^2-1, D_h^8=alpha. Inverting gives C_h^8=alpha^-1. Reversing the exponent sets proves the final two equalities.

All products were nonzero before division. This proof needs no evaluation of a complex Gauss sum, no prime-order assumption, and no finite-field involution. The notation alpha^(1/8), if used, means D_h. Eighth roots are unique in a field of characteristic two; existence here has been proved. QED.

## 4. Exact complementary affine transport

Define two actual polynomials over F2[q], for every n>=0:

F_n(q) = E_n(q)^8 + q C_n(q)^8,
G_n(q) = q (E_n*(q))^8 + C_n(q)^8.                    (4.1)

These are different from the balanced A_m,B_m used in the accepted quadratic descent and from the old spectral split. They are not substituted for the full Q_m obstruction.

**Theorem.** Whenever m+n=h-1, there are the exact cleared identities at alpha

C_m^8 F_n = alpha^2 C_n^8 (E_m*)^8,
alpha C_m^8 G_n = C_n^8 E_m^8.                       (4.2)

In particular,

E_m(alpha)=E_m(alpha^-1)=0
  iff F_n(alpha)=G_n(alpha)=0                         (4.3)
  iff E_n(alpha)=D_h C_n(alpha)
      and E_n*(alpha)=C_h C_n(alpha).

**Proof.** Apply (2.1) as written and with m,n exchanged. Since C_h D_h=1, solve without dividing by an endpoint:

E_n + D_h C_n = D_h^2 (C_n/C_m) E_m*,
E_n* + C_h C_n = C_h^2 (C_n/C_m) E_m.

Raise both equations to the eighth power. Frobenius distributes over the sum in characteristic two. Substitute (3.1), and multiply the first by C_m^8 and the second by alpha C_m^8. This is (4.2). Every displayed prefactor is a unit; an element of a field has eighth power zero exactly when it is zero. Finally E_m* differs from E_m(alpha^-1) by a nonzero alpha power. This proves the equivalences. QED.

The same identities hold as polynomial congruences modulo the reduced cyclotomic polynomial Phi_d in F2[q]. That quotient is a product of fields, since d is odd and Phi_d divides the separable q^d+1. Thus (4.3) handles every primitive Frobenius component, including self-reciprocal and distinct inverse orbits. It does not select a convenient single factor.

This is a genuine index-changing interface: n=(d-2m-3)/2. For d<4m+3 the complementary index is smaller than m. For larger d it is larger. It is not an induction by itself: the smaller-index target is an affine value, not another zero pair. Treating it as the original paired-zero assertion would be invalid.

## 5. Three exact symbolic certificates and the infinite off-line corollary

Let Phi_3=q^2+q+1 and Phi_5=q^4+q^3+q^2+q+1. Exact polynomial identities give

gcd(F_0,G_0) = q+1,
gcd(F_1,G_1) = (q+1)^8 Phi_3,
gcd(F_2,G_2) = (q+1)^16 Phi_3 Phi_5.                  (5.1)

For reproduction, the inputs are

E_0=E_0*=C_0=1,
E_1=q+q^2, E_1*=1+q, C_1=1+q^2,
E_2=1+q^2+q^3+q^4+q^5+q^6,
E_2*=1+q+q^2+q^3+q^4+q^6,
C_2=(1+q^2)(1+q^4).

The small exact Bezout coefficients, complete F_n,G_n masks, and certificates are saved in RESULTS.json. Each includes both u_n F_n+v_n G_n=gcd and a_n F_n+b_n G_n=L_(2n+1)^r, with r=1,4,6 for n=0,1,2 respectively. They are ordinary polynomial identities over F2, so checking them is a finite algebraic proof of (5.1), not a numerical approximation or sampling claim. The checker independently verifies the common gcd divides both inputs via its Euclidean construction and reconstructs the equality by multiplication.

For a compact certificate readable without running software, encode a polynomial by a hexadecimal integer whose bit i is its q^i coefficient. The tuples (n,F_n,G_n,gcd,u_n,v_n) are

- (0, 0x3, 0x3, 0x3, 0x0, 0x1)
- (1, 0x30102, 0x10203, 0x707, 0x1, 0x3)
- (2, 0x3010301030003, 0x3000302030203, 0x5d005d, 0x47855f7, 0x47b823c)

Polynomial multiplication and XOR verify u_n F_n+v_n G_n=gcd, and direct division verifies the displayed gcd divides each input. The gcd masks equal the products in (5.1).

For any m>=1 and n in {0,1,2}, put d=2m+2n+3. Then m+n=(d-1)/2-1, so (4.3) applies. Every factor of (5.1) has root order at most 2n+1, while d>2n+1. Therefore no primitive d-th root can be a common root of F_n,G_n. Equation (4.3) excludes paired E_m zeros. This proves exactly the infinite lines d=2m+3,2m+5,2m+7 claimed at the beginning.

Equivalently, for those d,

gcd(E_m,E_m*, reduced Phi_d)=1 in F2[q].              (5.2)

On an orbit where inversion is a Frobenius power, an E_m zero would automatically give its inverse zero, so (5.2) also excludes a one-sided endpoint zero on that orbit. On a distinct inverse pair only simultaneous vanishing is excluded. No positivity or analytic conjugation is used.

## 6. The decisive contract and the unresolved uniform gap

A precise endpoint continuation suggested by (4.2) is the following all-n statement:

Every irreducible factor of gcd(F_n,G_n) divides L_(2n+1), for every n>=0.   (6.1)

It is equivalent to the general paired-endpoint theorem, rather than a claimed easier theorem. To see both directions, a parameter of exact order d>2m+1 defines n=(d-2m-3)/2>=0. Conversely a parameter of order d>2n+1 defines m=(d-2n-3)/2>=0. The m=0 case has E_0=1 and is automatically impossible by (4.3); every remaining case is in the endpoint theorem. All nonzero algebraic parameters over F2 have finite odd order; q=0 is not a common root because G_n(0)=1. Thus no component is lost.

Both F_n and G_n have degree at most 8n(n+1)+1. Since F_n is monic of that degree, a fully specified equivalent certificate is

a_n F_n+b_n G_n=L_(2n+1)^[8n(n+1)+1].                (6.2)

The exponent safely bounds every irreducible multiplicity of their gcd. This certificate is not asserted for all n. The n=0,1,2 certificates above prove only their exact symbolic instances and their resulting infinite lines.

For the full F020 task, the decisive additional question is still: what property of the actual RS diagonal/edge formulas prohibits simultaneous ordinary degeneracy at inverse parameters, including different collision coordinates and endpoint/collision mixtures? Neither (6.1), if proved, nor the accepted balanced endpoint line answers those three other channels. A valid full completion must prove the existing localized Q_m,Q_m* unit ideal for all m, or return one actual-family common factor with certified exact order greater than 2m+1. A synthetic spectral countermodel, a norm zero, a one-sided actual collision, or another fixed-b certificate is not such a completion.

The present interface has a specific use: it provides a correct off-line endpoint transport with all coefficients fixed, and prevents falsely treating complementary zeros as a smaller paired-zero instance. It does not justify launching a growing n census. The full collision gap remains structural and needs an RS-specific mechanism beyond the accepted nonimplication countermodel.

## 7. Validation and scope boundaries

The newly authored check_transport.py uses only Python's standard library and imports no historical program. The retained sources were read and hashed only.

Author checks passed: 223 assertions, three exact symbolic Bezout/support certificates, and nine quotient-ring controls. The controls use existing indices m=1,2,12 and complementary indices n=0,1,2. For each d=2m+2n+3 they operate modulo the complete reduced Phi_d, verify exact primitive order and all product-unit guards, reconstruct endpoints from independent Gaussian q-Pascal differentiation, check actual-degree reversal, prove the half-product and two transport identities, and check the restricted paired-endpoint exclusion. Full-chain h is only an auxiliary construction index. No R_m support census is performed.

Four deliberate transport corruptions are rejected: omitted alpha^2, wrong reciprocal alpha power, replacing the eighth power with the fourth, and an off-by-one complementary index. Three changed Bezout coefficients are also rejected. Tests are author-side orthogonal controls, not independent-person review. The theorem in Sections 3-5 is the source of the all-m conclusion; finite controls do not supply its quantifier.

No old files, research table cells, repository contents, or external services were changed. The two b31 stages remain complete, and no b enlargement is selected.

## 8. Priority and recommendation

Retain nextpriority=58/100 for the full all-m paired-support proof-or-obstruction, with the inherited dimensions (information gain, tractability, defensible novelty opportunity, scope/impact, evidence readiness)=(4,2,1,4,4). Retain the separate endpoint gate at 53. These are remaining-work priorities, not correctness or novelty probabilities.

The named new result is ready for independent review. Once reviewed, that completed lemma has the completed-stage cap 15. No increase in tractability is justified by an exact equivalent contract alone. The practical next step is to review the eighth-root/affine transport and the three small certificates, then require a genuinely uniform endpoint or actual-family collision mechanism before opening further computation. No broader closure or historical novelty should be recorded.
