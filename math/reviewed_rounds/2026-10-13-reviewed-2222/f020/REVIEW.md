# Independent review: F020 off-line endpoint transport

13 October 2026 UTC.

## Verdict

**ACCEPT at the exact endpoint-only scope.** No mathematical repair is needed.

For every integer m >= 1, in every field of characteristic two, the actual endpoint values E_m(alpha) and E_m(alpha^-1) cannot both vanish when alpha has exact odd order d = 2m+3, 2m+5, or 2m+7. The proof includes composite orders and all primitive Frobenius components. It does not assume inversion is a Frobenius power.

The uniform complementary affine transport, half-product eighth-root identity, three displayed symbolic gcd certificates, and guarded equivalence with the proposed all-n endpoint contract are all correct. The all-n contract is not proved by this packet.

The full four-channel F020 paired-support gate remains OPEN at 58/100. The general endpoint gate remains OPEN at 53/100. The completed lemma has the inherited completed-stage cap 15. These are work priorities, not correctness or novelty probabilities. No comparative evidence warrants changing the remaining-work scores.

Candidate archive SHA-256:
6dcafc0ede275e0bbe439400ca3c2fa3f1c246d212a8860d204f8f7f17ebce3d

Candidate theorem SHA-256:
9f8710be41ee1f36ab114727b7123f475cd5c7dcf6d0ee65e7bc30fe98040b35

## 1. Identity and normalization agreement with the accepted source

The accepted source has E_0 = E_0* = 1, E_j = D_j + (1+q^(2j))E_(j-1), deg E_j = j(j+1), and E_j* = q^[j(j+1)]E_j(q^-1). These are the candidate's conventions. The Gaussian derivative H'_(2j+1)(1) is the actual endpoint P_j(0); it is not a spectral derivative or a differently normalized reversal.

For d = 2h+1, exact odd order is essential. The positive exponents appearing in C_j and D_j for j <= h lie strictly below d, so every factor is a unit. This does not require d to be prime. Merely assuming alpha^d = 1 would be insufficient.

The previously accepted complementary identity is exactly

C_h C_n E_m + D_h C_m E_n* = C_m C_n,

with m+n = h-1. The accepted source's tail reflection starts at m+1 and ends at h, and therefore n = h-m-1, not h-m. The new proof preserves that index, both reciprocal weights, and all empty-product cases. This review checked the copied source against the local accepted source bytes and the prior independent-review seal; no predecessor code was executed.

## 2. Half-product eighth root and its choice

Since d is odd, X^d+1 is separable. Its roots are 1, alpha, ..., alpha^(d-1), including when d is composite. Evaluating (X^d+1)/(X+1) at X=1 gives

C_h D_h = product_(r=1)^(d-1)(1+alpha^r) = d = 1.

The negatives of 2,4,...,2h modulo d are precisely the odd exponents 1,3,...,2h-1. Consequently

D_h = alpha^[-h(h+1)] C_h,
D_h^2 = alpha^[-h(h+1)].

Raising the last equality to the fourth power and using 4h(h+1) = d^2-1 gives D_h^8 = alpha. Hence C_h^8 = alpha^-1. No sign, complex root selection, square-root convention, or prime-order assumption is involved. Also C_h(alpha^-1) = D_h(alpha) and D_h(alpha^-1) = C_h(alpha) by the same exponent-set permutation.

An eighth root is unique in a characteristic-two field: if u^8 = v^8, then (u+v)^8 = 0, hence u=v. Thus D_h is the unique eighth root already constructed by the product. This is stronger than selecting an arbitrary root from an extension. All divisions in the proof occur after nonvanishing has been established.

## 3. Both cleared affine identities

Divide the swapped accepted identity by C_h C_m, and the original identity by D_h C_m. In characteristic two subtraction and addition agree. The results are

E_n + D_h C_n = D_h^2 (C_n/C_m) E_m*,
E_n* + C_h C_n = C_h^2 (C_n/C_m) E_m.

Frobenius raising to the eighth power gives D_h^16 = alpha^2 and C_h^16 = alpha^-2. Therefore, for

F_n = E_n^8 + q C_n^8,
G_n = q(E_n*)^8 + C_n^8,

the two correct cleared equations are exactly

C_m^8 F_n = alpha^2 C_n^8 (E_m*)^8,
alpha C_m^8 G_n = C_n^8 E_m^8.

In particular the factor alpha^2 in the first equation and the factor alpha in the second equation are both necessary. Every remaining factor is a unit. Since eighth powers detect zeros and E_m* differs from E_m(alpha^-1) by a nonzero alpha power, the paired zero condition is equivalent to F_n(alpha)=G_n(alpha)=0 and to the displayed complementary affine endpoint values.

The congruence formulation modulo Phi_d reduced over F2 is valid. For odd d the reduced cyclotomic polynomial is separable, all of its roots have exact order d, and its quotient is a product of fields. The proof and equivalence hold in each component. The candidate does not exploit a conveniently selected irreducible factor.

The map n = (d-2m-3)/2 is correct. A smaller complementary index produces an affine-value condition, not a smaller paired-zero instance, so the candidate correctly declines to claim an induction.

## 4. Exact symbolic gcd and support certificates

The reviewer independently reconstructed E_n from the original Gaussian coefficient recurrence, using H'_(2n+1)(1), and then formed C_n, E_n*, F_n and G_n. Sparse sets of exponents were used for exact F2 polynomial arithmetic. Neither the candidate checker nor a historical program was read as executable code, imported, or run.

All six displayed F/G masks and all three gcd masks match. Independent Euclidean gcds, direct division, and multiplication of the supplied Bezout coefficients establish

gcd(F_0,G_0) = q+1 = 0x3,
gcd(F_1,G_1) = (q+1)^8 Phi_3 = 0x707,
gcd(F_2,G_2) = (q+1)^16 Phi_3 Phi_5 = 0x5d005d.

Both classes of certificate pass exactly: u_n F_n+v_n G_n equals the gcd, and a_n F_n+b_n G_n equals L_(2n+1)^r for r=1,4,6. Equality plus divisibility proves each stated gcd; a Bezout equality alone would not suffice. The additional universal degree-bound exponent also succeeds in these three instances.

For n=0,1,2, each irreducible gcd factor has root order at most 2n+1. With m>=1 and d=2m+2n+3, exact d is strictly larger than 2n+1. The two affine polynomials therefore have no common primitive d-th root, and transport proves the three claimed all-m lines. This is an infinite theorem from three symbolic polynomial identities and the uniform transport, rather than an extrapolation from finite parameter tests.

The one-sided conclusion on self-reciprocal Frobenius orbits is also correctly qualified: there an E_m root would force its inverse root because E_m has coefficients in F2. On distinct inverse orbits only simultaneous vanishing has been excluded.

## 5. Boundaries and proposed general contract

At m=0, E_0=E_0*=1 and its paired zero condition is impossible. The transport and product guards still apply with n=h-1. The independent checks explicitly include (m,n,d)=(0,0,3),(0,1,5),(0,2,7). There is no need to invent a negative endpoint index or divide by an absent block value.

At n=0, F_0=G_0=q+1. For d>=3 this is nonzero at an exact-order parameter. In particular the new line d=2m+3 has no missing empty-complement case. The original m=1 boundary retains E_1=q+q^2 and E_1*=1+q, with reversal at degree 2.

The proposed assertion that every irreducible factor of gcd(F_n,G_n) divides L_(2n+1), for every n>=0, is genuinely equivalent to the general endpoint theorem at orders greater than 2m+1:

- Given d>2m+1, odd parity makes n=(d-2m-3)/2 a nonnegative integer, so transport applies.
- Conversely, an irreducible common factor outside L_(2n+1) has a nonzero root of finite odd order d>2n+1. Then m=(d-2n-3)/2>=0. The m=0 boundary is automatically impossible and all other cases fall under the general endpoint theorem.
- q=0 is no lost component because G_n(0)=C_n(0)^8=1.

F_n is monic of degree M=8n(n+1)+1. If every gcd factor occurs in L, then its multiplicity in the gcd is at most M, so the gcd divides L^M. Bezout therefore gives a_n F_n+b_n G_n=L^M. The converse is immediate. This establishes the equivalence of the proposed support and certificate formulations, not the missing all-n assertion itself.

## 6. Independence, guards, and replay

The local-source audit passes 478 exact assertions:

- Pinned candidate archive, 14 manifest-bound payloads, closed archive membership, six source snapshots and byte-identical local originals.
- Prior accepted review manifest seal and all 45 bound local payload files, read/hash only.
- Three symbolic gcd and support certificates, including exact multiplicities.
- Thirteen complete reduced-cyclotomic quotient controls: the nine candidate cases m=1,2,12 and n=0,1,2; three required m=0 boundary cases; and the previously accepted unbalanced identity case (m,n,d)=(2,4,15). The last is an identity control, not a new n=4 gcd census.
- Gaussian q-Pascal endpoint reconstruction, first-order and continuant recurrence agreement, actual-degree reversal, full Gaussian specialization, primitive-order guards, all half-product unit guards, both accepted complementary identities, both new transport identities, and componentwise common-zero equivalence.

Fourteen named negative controls reject changed u/v coefficients for all three masks; omission of alpha^2; a wrong second alpha power; fourth rather than eighth powers; an off-by-one complementary index; D_h^4=alpha; a wrong reversal degree; q=1 denominator inversion; and an exact-order-9 element mislabeled as order 27. These are targeted interface tests, not an exhaustive adversarial claim.

Two fresh-directory executions of only this reviewer's new checker reproduce the portable result bytes. Their receipt records the precise commands, code/candidate/result hashes and assertion count. Portable replay verifies the embedded source snapshots; the additional local-original and prior-manifest checks are retained in the first result. No candidate or historical program was executed in any run.

## 7. What remains open and next priority

This result excludes only endpoint/endpoint simultaneous failure on three new exact-order lines. It supplies no endpoint/collision, collision/endpoint, or collision/collision exclusion. In particular the accepted synthetic full-spectrum countermodel remains relevant: reflection, unit edges and full-chain squarefreeness alone do not prevent complementary collisions at different coordinates.

Retain the full gate at 58, with dimensions (information gain, tractability, defensible novelty opportunity, scope/impact, evidence readiness)=(4,2,1,4,4), and the separate endpoint gate at 53. The new equivalent affine contract does not by itself justify a tractability increase. The completed transport/three-line lemma is capped at 15.

The next admissible mathematical advance is a genuinely uniform endpoint argument or a property specific to the actual RS diagonal/edge formulas that controls all remaining inverse-parameter collision channels. Full closure requires the original localized Q_m,Q_m* unit ideal for every m, or an actual-family common factor with certified exact order greater than 2m+1. Do not substitute another fixed-b census, automatic growing-n search, a one-sided collision, a synthetic countermodel, or a norm reformulation.

No full four-channel F020 completion, characteristic-zero transfer, all-A overlap, runtime consequence, actual-family counterexample, or historical originality is accepted here. No external service, repository, table, or pre-existing file was changed.
