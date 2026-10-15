# Q29: exact successive-layer identity and the missing transfer theorem

14 October 2026 UTC. Bounded symbolic audit. Local deliverable only; no
scientific program from a supplied packet was executed and no external write
was made. This is not a fixed-instance census or a proof of the proposed
all-layer implication.

## Result

There is an exact integral cyclotomic polynomial relation between successive
indices. It does **not** identify the lower polynomial at the actual lower
root with its value at the higher root. That substitution already fails at
the first power of the higher uniformizer. Moreover, the old e=3 raw
100-by-100 local rectangles vanish at every higher layer, and the old
content-60 normalization has zero residue there. These are proved
obstructions to reusing the current certificates unchanged, not
counterexamples to squarefreeness of the actual higher Rogers–Szegő
polynomials.

The accepted e=3 theorem remains complete. The implication

    B_e != 0  ==>  B_(e+1) != 0,  for every e >= 3,

remains unproved. A concrete sufficient integral transfer certificate is
stated in Section 6; the existing relation fails its nonsingular-reference
requirement.

## 1. Exact objects and parity guards

Use the source definition

    H_n(z;Q) = sum_(k=0)^n GaussianBinomial(n,k;Q) z^k.

For odd n, Gaussian symmetry gives the exact integral quotient

    V_n(z;Q) = H_n(z;Q)/(z+1) in Z[Q,z].

Fix alpha of order 27 in the unramified degree-18 ring O over Z_5. Set

    N_e = 27*5^e,  n_e = (N_e-1)/2,  m_e = (N_e-3)/4,
    q_e = alpha*zeta_(5^e),  pi_e = zeta_(5^e)-1,
    A_e = O[pi_e],  K_e = Frac(A_e),
    U_e(z) = V_(n_e)(z;q_e).

All N_e are 3 modulo 4, so all n_e are odd and every quotient used below
exists integrally. Also

    n_(e+1) = 2N_e+n_e = 5n_e+2,
    m_(e+1) = 5m_e+3.

Thus m_e has the parity of e. The reciprocal representation and its ordinary
discriminant identity give

    U_e(z) = z^m_e R_e(z+2+z^-1),
    U_e(-1) = (-1)^m_e R_e(0),  U_e(1) = R_e(4),
    Disc(U_e) = Disc(R_e)^2 R_e(0) R_e(4),
    B_e = (-1)^m_e [Disc(R_e) R_e(0) R_e(4)]^2.

In particular, the sign in the last identity alternates between successive
layers: m_3=843 and m_4=4218. No N=1 modulo 4 claim is made.

Use compatible roots, so in A_(e+1), with t=pi_(e+1),

    pi_e = (1+t)^5-1,
    q_e = alpha*(1+t)^5 = alpha^-4 q_(e+1)^5,
    v_t(x) = 5 v_(pi_e)(x) for nonzero x in K_e.

The tame factor alpha^-4 is essential. Replacing q_e by q_(e+1)^5
changes the primitive component.

## 2. The actual integral successive-index relation

Write N=N_e and n=n_e. The q-Lucas block identity, over the universal
integral polynomial ring, yields a polynomial J_e in Z[Q,z] such that

    V_(5n+2)(z;Q)
      = (1+z^N)^2 V_n(z;Q) + Phi_N(Q) J_e(z;Q).       (2.1)

Proof: modulo the monic cyclotomic polynomial Phi_N(Q), the finite Euler
product splits into N-term blocks. Because N is odd, the triangular
q-weights cancel and n_(e+1)=2N+n. This proves the H identity. Both indices
are odd, so division by the monic persistent factor z+1 is legitimate in
the integral quotient. Monic division in Q then supplies integral J_e.
This is the accepted guarded block mechanism, specialized to adjacent
layers; it is not a new q-Lucas theorem.

At q'=q_(e+1), set delta_e=Phi_N(q'). The valuation is exactly

    h_e := v_t(delta_e) = phi(5^e) = 4*5^(e-1),
    v_t(5) = 5h_e.

Indeed Phi_(27*5^e)(Q)=Phi_27(Q^(5^e))/Phi_27(Q^(5^(e-1))).
At q' the two numerator/denominator valuations are 5^e and 5^(e-1),
respectively. The relevant tame roots of Phi_27 are simple modulo 5,
so their Taylor derivatives are units. Neither value is zero because
q' has the strictly higher order 27*5^(e+1).

Consequently (2.1) evaluates to

    U_(e+1)(z) = (1+z^N)^2 V_n(z;q') + delta_e J_e(z;q').  (2.2)

The lower-index polynomial on the right is evaluated at q', not q_e.
To express an exact relation to the actual U_e, define the integral divided
difference

    D_e(z;X,Y) = [V_n(z;X)-V_n(z;Y)]/(X-Y) in Z[X,Y,z].

Then the genuine successive-object relation is

    U_(e+1)(z)
      = (1+z^N)^2 U_e(z)
        + (q'-q_e)(1+z^N)^2 D_e(z;q',q_e)
        + delta_e J_e(z;q').                         (2.3)

Equation (2.3) is exact and integral. It exposes two correction terms;
the first has a coefficient of valuation exactly 1, while the second is
only guaranteed to have coefficient valuations at least h_e.

## 3. Sharp first-coefficient obstruction to lower-root substitution

For any odd n>=3,

    [z] V_n(z;Q) = S_n(Q) := Q+Q^2+...+Q^(n-1).

Since n_e=27a+13 with a=(5^e-1)/2, and n_e=2 modulo 5,

    alpha S_n'(alpha)
      = [alpha-2alpha^13+alpha^14]/(1-alpha)^2 modulo 5.

This is nonzero: the denominator is a unit, and its numerator is a
nonzero polynomial of degree 14 in alpha, whose minimal polynomial over
F_5 has degree 18. Also q'=alpha(1+t) while q_e=alpha(1+t)^5, hence

    q'-q_e = alpha*t modulo t^2.

It follows that

    v_t(S_n(q')-S_n(q_e)) = 1.

The factor (1+z^N)^2 does not alter the z coefficient, and h_e>=100 for
e>=3. Thus (2.2) proves the stronger, exact failure statement

    v_t([z]{U_(e+1)-(1+z^N)^2 U_e}) = 1.             (3.1)

In particular, replacing V_n(z;q') by U_e(z) in (2.2) does not even
preserve a congruence modulo t^2, let alone modulo t^h_e. This failure is
within the same fixed tame component; it is distinct from the additional
error of omitting alpha^-4 in the power relation.

## 4. A quantified obstruction to reusing the e=3 jets or normalization

Fix any higher layer ell>=4 and compare it to r=3. The integral block
relation gives

    V_(n_ell)(z;q_ell)
      = (1+z^3375)^a V_1687(z;q_ell) + pi_ell^100 W(z),
    a = (5^(ell-3)-1)/2,

with W integral. Since

    1+z^3375 = (1+z^27)^125 modulo 5

and v_(pi_ell)(5)>=500, this becomes

    U_ell(z)
      = (1+z^27)^b V_1687(z;q_ell) + pi_ell^100 W_ell(z),
    b = (5^ell-125)/2 >= 250.                        (4.1)

All polynomials here are integral. The same identity holds for H instead
of V; the quotient version is valid because all relevant n are odd.

At each center a_j=-alpha^j, j=0,...,26, substitute z=a_j(1+v). Then

    1+z^27 = 1-(1+v)^27 = v T(v),  T(0)=-27 in O^x.

Therefore every coefficient of v-degree less than 250 in the local
U_ell polynomial is divisible by pi_ell^100. In particular its entire
old raw rectangle

    pi-degree <100,  v-degree <100

is zero. The same holds for the local H targets used in the nonshared
e=3 certificates. At the shared center use the exact quotient convention
U(-1-v)=-H(-1-v)/v, as in the accepted source.

Apply the exact old e=3 scaling v=pi_ell Y and content division by
pi_ell^60. Equation (4.1) gives

    pi_ell^-60 U_ell(a_j(1+pi_ell Y))
      in pi_ell^40 A_ell[Y] for every ell>=4.        (4.2)

The first term has valuation at least b-60>=190 and the second at least
40. The corresponding nonshared H statement follows identically.
Thus the e=3 residue A_j Y^10(Y^4-1)^10, with A_j nonzero, cannot
reappear under that unchanged normalization at any higher layer.
Ordinary differentiation preserves this coefficientwise pi^40
divisibility, so it supplies no old nonzero derivative-residue witness
either. A new variable-scale/derivative division would need its own
proved valuation and remaining-precision bounds.

This is stronger than saying that the available precision is unspecified:
the old retained rectangle and old normalized unit witness provably vanish.
It does not assert that the actual higher polynomial vanishes or has a
multiple root. Its decisive terms are beyond these old observations.

## 5. Uniform structure that does carry, and the remaining local problem

The accepted degree-12 residue Ebar=H_13(z;alpha)/(z+1) is squarefree,
nonzero at every -alpha^j, and nonzero at 1. The same block identity at
alpha proves at every layer

    U_e modulo pi_e = (1+z^27)^a_e Ebar(z),
    a_e=(5^e-1)/2,  a_(e+1)=5a_e+2.

Hensel factorization therefore gives, uniformly,

    U_e = E_e product_(j=0)^26 P_(e,j),
    deg E_e=12,  deg P_(e,j)=a_e.

Disc(E_e), every cross-primary resultant, and every E_e/primary resultant
are units. Also U_e(1) is always a unit because its residue is
2^a_e Ebar(1), which is nonzero. Nonshared P_(e,j)(-1), j!=0, and
E_e(-1) are units. Hence there is an actual unit epsilon_e in A_e such
that

    B_e = epsilon_e P_(e,0)(-1) product_(j=0)^26 Disc(P_(e,j)). (5.1)

This exact identity follows by collecting the known unit factors in the
ordinary product-discriminant formula; it introduces no normalized
discriminant in place of the ordinary one. Same-q reciprocal inversion
pairs j and 27-j and transfers only those partner discriminants by a
unit multiplier. It does not transfer across e.

Thus the remaining bridge needs to control the new primary factors of
degree 5a_e+2 and the shared endpoint. The residual factor, cross-center
separation, and the +1 endpoint require no new finite census. B_e!=0
alone does not furnish any coefficients of these new primary factors.

## 6. A precise sufficient transfer certificate and why (2.2) is insufficient

For a monic reciprocal polynomial P of even degree with constant term 1,
write

    B(P)=Disc(P)P(-1)P(1).

This is a polynomial with integer coefficients in the coefficients of P.
Consequently, over a DVR, coefficientwise congruence P=V modulo t^L
implies B(P)=B(V) modulo t^L. No discriminant denominator or derivative
normalization is hidden in this assertion.

**Sufficient transfer lemma.** For each e>=3, construct from accepted
lower-layer data a monic reciprocal V_e in A_(e+1)[z] of degree
deg(U_(e+1)) and an integer L_e such that:

1. B_e!=0 implies B(V_e)!=0, by a proved identity or controlled estimate;
2. all coefficients of U_(e+1)-V_e are divisible by t^L_e;
3. L_e>v_t(B(V_e)) whenever B_e!=0.

Then B_(e+1)!=0. Proof: the congruence of the B invariants and the strict
valuation inequality prevent cancellation of the nonzero leading term
of B(V_e). Any variable-e construction must prove all three statements,
including the growth of L_e, without merely assuming a higher-layer
nonvanishing guard.

The natural reference furnished by (2.2) is

    V_e(z)=(1+z^N_e)^2 V_(n_e)(z;q_(e+1)).

It has an explicit repeated factor and V_e(-1)=0. Therefore B(V_e)=0,
regardless of B_e. No finite error precision can satisfy condition 3
for this reference. Replacing its lower root by q_e also fails condition
2 already at precision 2 by (3.1).

This limitation is an information obstruction, not merely a missing
valuation estimate. Given this repeated monic reciprocal reference V_e,
write V_e=z^m R_0(z+2+z^-1). For any L one may compare

    V_e  and  V_e + c z^m,  with c in t^L A_(e+1).

Both are monic reciprocal with constant term 1 and agree modulo t^L.
The first has B=0. For all but finitely many choices of nonzero c in
that ideal, the second has B!=0: R_0(w)+c has a repeated root only when
-c is a critical value of R_0, and its endpoint values vanish for at
most two additional c. Characteristic zero ensures R_0' is nonzero,
so there are finitely many such exceptional values. The ideal contains
infinitely many choices. This argument preserves reciprocal and endpoint
parity conventions. It does not claim these perturbed polynomials are
the actual Rogers–Szegő family.

Accordingly, the transport congruence and the old lower certificates do
not distinguish singular from nonsingular higher lifts. A valid bridge
must supply genuine new control of the actual correction term J_e and
the same-component divided difference, or an independent uniform
argument for the upper ordinary resultant and shared endpoint. Neither
is provided by the fixed e=3 local precision certificates.

## Source bindings and scope

All source files were read as inert text. Their SHA256 values at this audit:

- q29_final_scope_checklist_2341/FINALIZATION_CHECKLIST.md:
  b620a5ef032d3eab7ddc69cbf3e6d475750bbe75301c3d23c628a05024d4910a
- q29_aggregate_accounting_review_2045/FINAL_AGGREGATE_REVIEW.md:
  0a17797f8e77976e8af5b6233973a2e4818e4f2fcd5821529119c138b3534396
- q29_center1_pair_2029/THEOREM_AND_PROOF.md:
  a6e47979a5e11c9e1e490f643044a8e9a7a1a81518acbcaa741b00b72747d118
- q29_higher_layer_recovery_0057/sources/Q29_SPLIT_REVIEW.md:
  ecd7d6c430a5361c13f58546ead58f24d2e24be0f55f42158d902b1ca30b6598
- q29_remaining_pairs_2044/THEOREM_AND_PROOF.md:
  3a086d0468a0a961132a50dda737b1f1540f3e9a6fe7bde95f28174d77887a97
- q29_higher_layer_recovery_0057/REPORT.md:
  17057203aeab6f70f9cd03caacf9a25425fbdfb5c6831cb8a9b156d5fe1240dd

The checklist supplies the proposed target and mandatory guards. The final
aggregate review supplies accepted B_3!=0, v_(pi_3)(B_3)=127812, the residue
Ebar certificate, and the exact reciprocal/ordinary-discriminant identities.
The center theorem supplies the exact Gaussian definition and finite
precision contract. The split review supplies the accepted universal
integral block identity with its corrected parity domain. Sections 3, 4
(with r=3), and 6 above are the present symbolic specialization and audit.

No broader status, priority, closure count, or publication decision changes.
