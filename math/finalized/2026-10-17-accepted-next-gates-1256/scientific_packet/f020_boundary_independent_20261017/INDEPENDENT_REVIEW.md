# F020 residual boundary: independent certificate review

17 October 2026 UTC

## Decision

**ACCEPT the bounded characteristic-zero static certifications and their stated all-A consequence for d=9 and d=25.** All 26 excluded residual pairs pass independent reconstruction and all 52 supplied finite-field Bezout identities are exact.

The separately proposed finite-reduction-order lemma is also valid. All 14 supplied reduction-order records pass an independent full-coefficient calculation. That lemma concerns the ordinary residual discriminant only; it supplies no fixed-node separation assertion.

No producer script was executed, imported, or evaluated. This review made no external writes. It does not change the canonical owner, project status, priority, historical attribution, or any parent gate.

## 1. Exact bounded conclusion

Let

    H_b(z;q) = sum_{k=0}^b Gaussian(b,k)_q z^k,
    F(z) = 1+z^d,
    U(z) = H_b(z;omega)                 for even b,
           H_b(z;omega)/(z+1)           for odd b,

where omega is any primitive dth root in characteristic zero.

For each of

- d=9, b=3,...,8;
- d=25, b=5,...,24,

the accepted exact results are

    gcd(H_b, ordinary derivative_z H_b) = 1,
    gcd(U,F) = 1,
    Disc(U) != 0,
    gcd(H_b,F) = 1       for even b,
                 z+1     for odd b.

In particular, for odd b the forced-root derivative g=U(-1)=H_b'(-1) is nonzero. This accepts all excluded residuals at these two particular root orders, rather than a subset selected after seeing the results.

### Coefficient and ring checks

The reviewer reconstructed the Gaussian coefficients in Z[q] using

    C(n,k) = C(n-1,k-1) + q^k C(n-1,k),

with the usual endpoint values. The reconstruction uses integer addition and shifts, with no unreduced Gaussian quotient and no inversion of a vanishing root-of-unity denominator. Endpoints, coefficient integrality, reciprocity, and C(n,k)(1)=binomial(n,k) were checked through n=24.

For every odd b, division of H_b by the monic factor z+1 was performed directly over Z[q]. Its remainder was exactly zero, and the quotient was monic. Thus U belongs to Z[q,z] before specialization. The independent reduced coefficients in Z[omega], for all 26 pairs, are saved in `independent_exact_coefficients.json`.

For p=3,5 and d=p^2, the reviewer constructed

    Phi_d(q) = 1+q^p+...+q^((p-1)p).

It divides q^d-1. The coefficients of Phi_d(q+1) were verified to satisfy Eisenstein's criterion at p: leading coefficient 1, every lower coefficient divisible by p, constant coefficient p and not divisible by p^2. Hence Phi_d is irreducible over Q. The ring O=Z[q]/Phi_d is a characteristic-zero domain whose fraction field is Q(omega), and every primitive embedding is a conjugate of the same field.

### Modular certificate checks and lifting logic

For each record the reviewer independently checked:

1. The modulus ell is prime, and the recorded omega image has exact order d.
2. Phi_d(omega_image)=0, so O -> F_ell is a well-defined ring homomorphism.
3. Every supplied coefficient of H and U agrees with the independently reconstructed integral polynomial evaluated under that map.
4. Both supplied identities hold coefficient by coefficient:

       A Hbar + B Hbar' = 1,
       C Ubar + D Fbar = 1.

5. Independent Euclidean gcds agree with both identities, and with the asserted ordinary H/F gcd and U/U' gcd.
6. The degrees and leading coefficients are preserved. H, U and F are monic; the ordinary derivative of H has leading coefficient b, with ell>b, so its degree is exactly b-1 after reduction.

The finite-field identities imply nonzero reduced resultants. The Sylvester determinant is polynomial in the integral coefficients and commutes with this specialization. Therefore the corresponding resultants in O cannot be zero. Since O embeds into Q(omega), they are nonzero in characteristic zero. This argument proves nonvanishing; it does not claim that the finite-field Bezout identity with right-hand side 1 lifts to an integral Bezout identity with the same right-hand side.

Irreducibility ensures that the resulting nonzero field elements remain nonzero at every primitive dth root. A modular map need not be injective; only the implication that a zero maps to zero is used.

### Ordinary and deflated guards

The first certificate concerns the ordinary z-derivative of H, hence its ordinary discriminant. The second concerns U and the whole F=1+z^d.

For odd b, H and F necessarily share z+1, so Res(H,F) is zero and is not the overlap guard. The accepted guard is Res(U,F)!=0. With H=(z+1)U and gcd(U,F)=1, the common factor is exactly z+1, and U(-1)!=0. Squarefreeness of H also gives squarefreeness of U. No ordinary-discriminant conclusion is inferred solely from a trace-polynomial discriminant.

The producer's exact number-field and reciprocal-trace calculations are supplementary. This review's acceptance of all 26 static cases is already supplied by the independently verified modular certificates, without relying on booleans in those logs.

### Bad-reduction control

For d=25,b=9, ell=101 and omega_image=5, the independently recomputed results are

    gcd(Hbar,Hbar') = 1,
    gcd(Ubar,Fbar) = z^2+18z+1 = (z-13)(z-70) in F_101[z].

For ell=151 and omega_image=9, both required gcds are 1. The good certificate therefore establishes characteristic-zero nonvanishing despite the first reduction's extra common roots. This explicitly prevents treating a failed modular test as a characteristic-zero counterexample.

## 2. Composition with the accepted local theorem

The inherited version-3 local theorem fixes a characteristic-zero field, odd d>=3, A>=1, 0<=b<d, and n=Ad+b. Its hypotheses are:

- Separated case: Disc(H_b) Res(F,H_b) != 0.
- Odd simple-overlap case: H_b=(z+1)U, g=U(-1)!=0, and Disc(U) Res(F,U) Disc(J_(A+1)) != 0.

Here the original normalization is retained:

    m=(d+b)/2,
    W=(omega;omega)_b / (omega^2;omega^2)_m,
    tau=dW/g,
    J_(A+1)(x;tau)=He_(A+1)(x)+A(1-tau)He_(A-1)(x).

For odd b<d, m<d and omega^2 has exact order d. Every denominator factor in W is nonzero. The accepted all-odd overlap theorem supplies Disc(J_(A+1))!=0 for every A>=1 at this actual tau; it is not an assertion that arbitrary nonreal tau suffices.

The new certificates supply the static hypotheses for the 26 excluded pairs. The previously accepted b<p static theorem supplies b=0,1,2 at d=9 and b=0,...,4 at d=25. Thus the complete residual interval 0<=b<d is covered at each of these two d.

It follows that, for d in {9,25}, A>=0, and 0<=b<d,

    ord_(Phi_d) Disc_z H_(Ad+b) = d*A*(A-1)/2 + A*(b mod 2).

For A=0, this is simply residual squarefreeness, with Disc(1)=Disc(monic linear)=1 at n=0,1. The local theorem itself is invoked only for A>=1. There is no finite-A-to-infinite-A extrapolation.

The inherited leading coefficients are nonzero. Explicitly, put P_A=product_(j=1)^A j^j. In the parameter q^d-1 they are

    C_sep = (-1)^[A(d-1)/2] d^[dA(A+1)/2] P_A^d
            Disc(H_b) Res(F,H_b)^(2A),

    C_ov  = (-1)^[A(d-1)/2] d^[dA(A+1)/2+A] P_A^(d-1)
            Disc(J_(A+1)) Disc(U) Res(F,U)^(2A) g^2.

Each displayed factor is nonzero in characteristic zero: d and P_A are nonzero integers; the static factors are supplied above; the J factor is supplied by the accepted theorem. If M denotes the corresponding exponent, the leading coefficient in q-omega is C*(d*omega^(-1))^M. For these prime-square orders,

    [D_n/Phi_d^M](omega) = C*(omega^(d/p)-1)^M,

which is also nonzero since omega^(d/p) has order p. The parameter normalization is not silently changed.

## 3. Separate reduction-order obstruction

### Integral deflation and exact lemma

The accepted static argument gives

    D_b(q)=(q-1)^e V_b(q),  e=b(b-1)/2,  V_b in Z[q].

The full deflation exponent is e, not b(b-1). One way to see integrality is to substitute q=1+t^2 and z=-1+tx. The Rogers–Szegő recurrence inductively gives H_b(-1+tx;1+t^2)=t^b K_b(x,t), with K_b integral and monic and K_b(x,0)=He_b(x). Root scaling then gives D_b(1+t^2)=t^[b(b-1)] Disc_x K_b(x,t). Since D_b(1+t^2) is a polynomial in t^2, (q-1)^e divides D_b in Z[q]. Moreover V_b(1)=Disc(He_b)=product_(j=1)^b j^j, so no larger characteristic-zero universal deflation is being assumed.

Let p be odd. If V_b mod p is nonzero, define the finite integer

    t_p(b)=ord_(q-1)(V_b mod p).

Then t_p(b)<phi(p^s) implies D_b(omega)!=0 at every primitive p^s-th root. Indeed, if D_b(omega)=0, irreducibility of Phi_(p^s) implies Phi_(p^s)|D_b over Q[q]. Since Phi_(p^s) is coprime to q-1, it divides V_b; because it is monic, the quotient belongs to Z[q]. Reduction modulo p, using

    Phi_(p^s)(q) = (q-1)^phi(p^s) mod p,

forces t_p(b)>=phi(p^s), contrary to the hypothesis. The nonzero-reduction condition is essential; the order of the zero polynomial is not a finite successful certificate. Equality or failure of the strict inequality is inconclusive.

### Independent coefficient verification

The reviewer reconstructed H_b(z;1+t) from the integer Gaussian recurrence, reduced over GF(p)[t], and formed the b-by-b matrix of multiplication by the ordinary derivative H_b' in GF(p)[t,z]/(H_b). H_b is monic, so the determinant is Res(H_b,H_b'). This method also remains valid when p divides b and the derivative's degree drops.

Every coefficient of all 14 producer shifted-resultant polynomials matches these independently computed determinants. The raw producer coefficients are resultants. The reviewer applied the ordinary-discriminant sign (-1)^e, verified nonzero reduction, removed t^e, and checked the least remaining nonzero exponent. The verified t values are:

| p | b in the displayed order | t_p(b) |
|---|---|---|
| 3 | 3,4,5,6,7,8 | 3,8,3,12,16,12 |
| 5 | 5,6,7,8,9,10 | 10,16,10,16,10,40 |
| 7 | 7,8 | 21,30 |

The producer's stated sufficient s thresholds follow directly from p^(s-1)(p-1)>t and are correct. These are fixed-b ordinary residual conclusions. No static node separation or arbitrary-prime-power all-residual theorem follows from this table alone.

## 4. Reproduction, provenance, and scope

Run in this directory:

    python verify_data_only.py
    python verify_reduction_orders.py

The first verifier uses only Python's standard library. The second uses SymPy 1.14.0 for exact polynomial-ring determinants and imports only the reviewer's first script. The retained producer programs are not needed and are not included.

Primary artifacts:

- `verification_results.json`: all 26 static checks, ring checks, and bad-reduction control.
- `independent_exact_coefficients.json`: reviewer-reconstructed H and U in Z[omega].
- `reduction_order_verification.json`: full verified deflated shifted discriminants and 14 finite t values.
- `sources/modular_certificates.json`, SHA-256 `fe1586ce38e82e76c7420b2c87009a57e3353024dcc2887dcbe1f9042ed76237`: inert producer Bezout data.
- `sources/reduction_orders.json`: inert producer shifted-resultant data; its hash is bound by the result file and manifest.
- `sources/accepted_local_theorem_v3.tex`: inherited local theorem, Section 3, equations (2), (8), (4), and (10).
- `sources/accepted_overlap_first_review.md` and `sources/accepted_overlap_second_review.md`: accepted all-odd J theorem and prior b<p static scope.
- `sources/producer_REPORT.md`: the report reviewed here.
- `MANIFEST.sha256`: all retained packet files except the manifest itself.

This acceptance adds bounded static coverage at d=9,25 and the consequent unlimited-A local formulas at those two orders. It does not establish the full b<d static theorem for arbitrary prime powers, arbitrary odd composites, positive-characteristic unit statements, characteristic-two paired support, general endpoints, numerical conditioning, historical novelty, FFT speedups, or operation-count changes. F020 ownership and F023 aliasing, accepted earlier subfamilies, and independent unresolved gates remain as recorded in the inherited reviews.
