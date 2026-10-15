# Q29: independent review of the successive-layer transfer obstruction

14 October 2026 UTC. Static symbolic review of local source text only. No
supplied scientific program was executed, and no external state was changed.

## Verdict

ACCEPT the exact integral identities, the sharp lower-root substitution
failure, and the all-higher-layer obstruction to unchanged reuse of the
e=3 raw jets and content-60 normalization in
`q29_transfer_requirements_2345/SYMBOLIC_TRANSFER_AUDIT.md`.

ACCEPT the stated uniform residual-factor/Hensel consequences and the
sufficient nonsingular-reference transfer lemma. These do not discharge the
all-layer implication B_e != 0 => B_(e+1) != 0. Neither an actual higher-layer
multiple root nor a counterexample to that implication has been established.
The fixed e=3 theorem remains complete; no closure/count/priority delta follows.

## 1. Definitions and integral transport

The source H_n is the integral Rogers–Szegő polynomial
sum_k GaussianBinomial(n,k;Q) z^k. Gaussian coefficient symmetry makes
H_n(-1;Q)=0 whenever n is odd, hence its quotient V_n by z+1 is monic and
integral. Here N_e=27*5^e is always 3 modulo 4, so both half-degrees needed
for each quotient transport are odd. This avoids the parity defect identified
in the earlier general transport review for some p=3 modulo 4 towers.

Since n_(e+1)=2N_e+n_e with 0<=n_e<N_e, integral q-Lucas gives

    V_(n_(e+1))(z;Q)
      = (1+z^N_e)^2 V_(n_e)(z;Q) + Phi_(N_e)(Q) J_e(z;Q),

with J_e in Z[Q,z]. Cancellation of z+1 takes place in the universal integral
identity, before specializing or truncating. Thus no nonunit division or loss
of one v coefficient is needed at the shared center.

Put t=pi_(e+1). Under compatible roots,

    q_e=alpha(1+t)^5=alpha^-4 q_(e+1)^5,
    v_t(5)=4*5^e,
    v_t(Phi_(N_e)(q_(e+1)))=4*5^(e-1).

For the last equality, the exact cyclotomic quotient is
Phi_27(Q^(5^e))/Phi_27(Q^(5^(e-1))). At q_(e+1), its two valuations are
5^e and 5^(e-1). The relevant tame roots have unit derivatives, and neither
term vanishes at this strictly higher root. The modulus is therefore finite
and exactly as claimed, in the actual higher DVR.

The right-hand lower-index polynomial is evaluated at q_(e+1), not q_e.
The divided difference in the candidate is an integral polynomial and its
equation (2.3) is consequently an exact identity between the actual objects.

## 2. Sharp lower-root substitution check

For n=n_e,

    [z] V_n(z;Q)=S_n(Q)=Q+...+Q^(n-1),
    n=13 modulo 27,  n=2 modulo 5.

Differentiating (Q-Q^n)/(1-Q) directly gives

    alpha S_n'(alpha)
      = (alpha-2alpha^13+alpha^14)/(1-alpha)^2 modulo 5.

The denominator is a unit. The numerator is a nonzero degree-14 polynomial,
so it cannot vanish at alpha, whose residue minimal polynomial has degree 18.
The compatible-root equation gives q_(e+1)-q_e=alpha*t modulo t^2. Taylor
expansion therefore proves exact valuation 1 for S_n(q_(e+1))-S_n(q_e).

The block factor has constant coefficient 1 and no z term. Its cyclotomic
error has all coefficients of valuation at least 100 for e>=3. It cannot
cancel the displayed valuation-1 term. The draft's equation (3.1) follows.
This is a concrete failure of the proposed substitution even modulo t^2,
within the same tame component. It is not an error caused only by choosing
alpha^5 instead of alpha.

## 3. The old raw rectangle genuinely vanishes

At any level ell>=4, applying integral q-Lucas against the fixed base r=3
gives a modulus of valuation exactly 100. Characteristic-5 Frobenius is valid
modulo pi_ell^100 because v_(pi_ell)(5)>=500. Thus

    U_ell(z)=(1+z^27)^b V_1687(z;q_ell)+pi_ell^100 W_ell(z),
    b=(5^ell-125)/2>=250,

with integral W_ell. This step uses no lower discriminant nonvanishing.
At every one of the 27 centers z=-alpha^j(1+v),

    1+z^27=1-(1+v)^27=v T(v),  T(0)=-27 is a unit.

Consequently all v coefficients of degree below 250 are divisible by
pi_ell^100. The raw pi-degree<100, v-degree<100 rectangle is identically zero
in the precise quotient A_ell/(pi_ell^100)[v]/(v^100). This is also true for
the nonshared H targets. The shared U convention is exactly -H/v and is
already handled by the universal quotient identity.

With v=pi_ell Y, the first term of the identity is coefficientwise divisible
by pi_ell^b and the error by pi_ell^100. Therefore

    pi_ell^-60 U_ell(-alpha^j(1+pi_ell Y))
      belongs to pi_ell^40 A_ell[Y].

This is a whole-polynomial assertion, not just a retained-jet computation.
The accepted e=3 nonzero residue A_j Y^10(Y^4-1)^10 cannot survive unchanged.
Ordinary Y differentiation preserves this divisibility. Any later division
or variable change needs a fresh error contract.

The same reasoning with the adjacent lower layer strengthens the bound to
pi_ell^(4*5^(ell-2)-60): the modulus has valuation 4*5^(ell-2), whereas
the Frobenius block has v degree 2*5^(ell-1), which is larger. Thus even the
guaranteed content under this unchanged normalization grows with the layer.
This is only a lower bound on content; its exact value is not claimed.

The original coefficient ring really was A_3/(pi_3^100), with exclusive
precision 100, v<100, and normalized precision only min(100,100)-60=40.
The earlier mixed-characteristic contract explicitly says these zeros give
lower bounds on valuation; they cannot be read as characteristic-zero zeros.
The present result proves vanishing of those observations, not failure of
squarefreeness of the actual higher polynomial.

## 4. What does transfer uniformly

The accepted residual Ebar=H_13(z;alpha)/(z+1) is monic of degree 12,
squarefree, nonzero at all -alpha^j, and nonzero at 1. For every e,

    U_e modulo pi_e=(1+z^27)^((5^e-1)/2) Ebar.

The 27 center factors and Ebar are pairwise coprime. Complete-DVR Hensel
factorization gives one degree-12 factor E_e and 27 primary factors of degree
(5^e-1)/2. All their cross-resultants, Disc(E_e), and U_e(1) are units.
The product discriminant formula then yields exactly

    B_e=epsilon_e P_(e,0)(-1) product_j Disc(P_(e,j)),

for an actual unit epsilon_e. This is a legitimate reduction of the remaining
task to ordinary primary discriminants and the shared endpoint, not a proof
that either is nonzero. Same-q reciprocity pairs centers only within a layer.

The reciprocal sign is also correct: m_(e+1)=5m_e+3, so its parity toggles,
and B_e=(-1)^m_e [Disc(R_e)R_e(0)R_e(4)]^2. In particular m_3=843 and
m_4=4218. The all-N=1 modulo 4 problem is outside this tower.

## 5. Precision limitation versus false theorem

For fixed degree, B(P)=Disc(P)P(-1)P(1) is an integral polynomial in the
coefficients. If P and a nonsingular reference V agree modulo t^L with
L>v_t(B(V)), the leading nonzero residue of B(V) cannot cancel. This proves
the draft's sufficient transfer lemma without denominator assumptions.

The natural q-Lucas reference contains (1+z^N_e)^2 and vanishes at -1, so
B(V)=0. It cannot satisfy that nonsingular-reference condition at any finite
precision. The draft correctly demonstrates the information loss: writing
V=z^m R_0(z+2+z^-1), the polynomials V and V+c z^m are monic reciprocal with
constant coefficient 1 and agree modulo t^L whenever c is in t^L A.
Only finitely many c cause R_0+c to have a repeated root or vanish at 0 or 4.
Since the ideal has infinitely many elements, nonsingular examples exist at
every finite precision alongside the singular reference.

These alternative lifts are not asserted to belong to the Rogers–Szegő
family. Therefore the result establishes insufficiency of the unchanged
transport/precision certificate, not impossibility of another uniform proof.
The actual corrections or an independent uniform argument remain to be
controlled. B_e != 0 => B_(e+1) != 0 remains OPEN.

## Source bindings

Final candidate and source hashes are recorded in SOURCE_BINDINGS.sha256.
All files were read as inert text. The accepted e=3 aggregate was used as
an existing theorem; its full numerical reconstruction was not repeated.

Review scope: local symbolic proof and source/precision inspection only.
Supplied code executions: 0. External writes: 0. Mathematical closure delta: 0.
