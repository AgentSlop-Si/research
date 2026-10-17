# F020: bounded residual boundary beyond b<p

17 October 2026 UTC. Local research packet; no external writes.

## Result

No characteristic-zero counterexample occurs in the complete excluded residual sets

- d=9, b=3,...,8;
- d=25, b=5,...,24.

For every listed pair and every primitive dth root omega, the exact conclusions are

    gcd(H_b, derivative_z H_b) = 1,
    gcd(H_b, 1+z^d) = 1       if b is even,
    gcd(H_b, 1+z^d) = z+1     if b is odd.

Here H_b(z;omega)=sum_{k=0}^b Gaussian(b,k)_omega z^k. Set U=H_b for even b and U=H_b/(z+1) for odd b. In all cases U is squarefree and gcd(U,1+z^d)=1. In particular the odd-case forced-root derivative U(-1) is nonzero.

These are bounded exact, computer-assisted certifications, with independently checkable finite-field Bezout witnesses and a second exact number-field computation. They are stronger than floating-point tests, but do not prove the same assertions for an unrestricted root order. A separate verifier has reported PASS for all 26 reconstructed static cases, all 52 Bezout identities, and all 14 full reduced-resultant records. Its review is a separate deliverable.

Combining these finite certifications with the already accepted b<p static theorem fills the entire static residual range 0<=b<d at d=9 and d=25. Combining that bounded static result with the already accepted all-odd overlap theorem and the retained local theorem yields the following bounded-root-order consequence:

    For d in {9,25}, n=Ad+b, A>=0, 0<=b<d,
    ord_(Phi_d) Disc_z H_n = d*A*(A-1)/2 + A*(b mod 2).

The inherited signed leading coefficients are nonzero in these two orders, under their existing normalization. This is an all-A consequence of the accepted local theorem, not an extrapolation of a finite A sweep. A=0 uses the certified residual squarefreeness; n=0,1 retain the stated discriminant conventions. No parent-gate closure, arbitrary-prime-power theorem, novelty claim, or external record change is proposed.

## Exact certificate mechanism

Let O=Z[omega]=Z[q]/Phi_d(q), and let ell be a rational prime with a in F_ell satisfying Phi_d(a)=0. The substitution omega -> a defines a ring homomorphism O -> F_ell.

Suppose a certificate gives polynomials A,B,C,D over F_ell such that

    A Hbar_b + B derivative_z Hbar_b = 1,
    C Ubar + D (1+z^d) = 1.

The two reduced resultants are nonzero. Resultants commute with specialization because they are polynomial expressions in coefficients. Hence the corresponding resultants in O are nonzero. Consequently the characteristic-zero gcds of H_b with its ordinary derivative, and U with 1+z^d, are 1. For odd b the exact polynomial identity H_b=(z+1)U then gives the asserted node gcd z+1. All primitive embeddings share these conclusions by cyclotomic automorphisms.

This is a sufficient condition for characteristic-zero nonvanishing. Failure of one reduction is inconclusive and is not a characteristic-zero counterexample. The argument neither claims nor needs a uniform positive-characteristic theorem.

`modular_certificates.json` supplies all 26 pairs, their reduced H and U coefficients, and both Bezout identities. All coefficient lists are in ascending powers of z. The generator constructs Gaussian coefficients by Pascal's identity rather than the RS recurrence used in the independent number-field implementation.

- d=9: ell=19, omega -> 4 works for all b=3,...,8.
- d=25: ell=101, omega -> 5 works for all b=5,...,24 except b=9.
- d=25, b=9: ell=151, omega -> 9 works.

All stated images have exact multiplicative order d, and Phi_d(image)=0 is checked. The stored identities have constant right-hand side exactly 1, avoiding a subjective numerical tolerance or an unreported genericity assumption.

### A real bad-reduction control

At d=25, b=9, ell=101, omega -> 5, the ordinary-derivative gcd is still 1, but

    gcd(Ubar,1+z^25) = z^2+18z+1 = (z-13)(z+31) in F_101[z].

At ell=151, omega -> 9, the node gcd is 1. The direct characteristic-zero calculation also gives gcd(U,1+z^25)=1. Thus the first modular failure is a false alarm for the characteristic-zero question. `bad_reduction_control.json` records a separate reconstruction of this case.

## Independent exact characteristic-zero route

`fresh_exact_field.py` constructs H recursively using

    H_0=1, H_1=1+z,
    H_(n+1)=(1+z)H_n-z(1-omega^n)H_(n-1)

over the exact algebraic field QQ[omega]/Phi_d. It directly computes the ordinary-derivative and node gcds for all six excluded d=9 cases. A corrected supplemental run uses the same direct route for d=25, b=5,6,7; those results are supplementary, not needed for the complete d=25 coverage below.

`fresh_trace_field.py` separately implements reciprocal reduction over the same exact number field. Every U has even degree 2m and satisfies

    U(z)=z^m Q(z+z^(-1)).

Writing S_j(y)=z^j+z^(-j), it constructs S_0=2, S_1=y, S_(j+1)=y S_j-S_(j-1), and

    Q(y)=u_m+sum_{j=1}^m u_(m+j) S_j(y).

Reciprocity is explicitly checked before this transformation. For odd d=2h+1 it similarly constructs R with

    (1+z^d)/(z+1)=z^h R(z+z^(-1)).

All twenty d=25 cases b=5,...,24 have

    gcd(Q,Q')=1, Q(2)!=0, Q(-2)!=0, gcd(Q,R)=1

by exact number-field arithmetic. These conditions imply U is squarefree: away from z=+-1 the map z -> z+z^(-1) is unramified; Q(+-2)!=0 excludes both ramification nodes. Also gcd(Q,R)=1 and Q(-2)!=0 give gcd(U,1+z^d)=1. In odd b, Q(-2)!=0 makes the additional factor z+1 simple. Thus every ordinary H_b is squarefree, not merely the reciprocal trace polynomial.

`trace_field_d25.json` records every gcd degree and both node-value checks. No historical or uploaded program was imported or executed. Only scripts freshly written for this bounded probe were executed. Standard SymPy exact algebraic-number arithmetic was used for the direct number-field computations; the Bezout certificate generator uses Python integer modular arithmetic.

## Structural sufficient condition for the ordinary residual guard

The accepted static proof supplies the integral factorization

    D_b(q)=(q-1)^N V_b(q),  N=b(b-1)/2,  V_b in Z[q].

For an odd prime p, suppose V_b mod p is not zero and define

    t_p(b)=ord_(q-1)(V_b mod p).

Then

    t_p(b) < phi(p^s)  ==>  D_b(omega) != 0

for every primitive p^s-th root omega. Indeed, if Phi_(p^s) divided V_b in Z[q], reduction modulo p would imply

    (q-1)^phi(p^s) divides V_b mod p,

because Phi_(p^s)(q) mod p=(q-1)^phi(p^s). This contradicts the inequality. Since omega!=1, nonvanishing of V_b implies nonvanishing of D_b. The old evaluation-at-1 argument is the special case t_p(b)=0.

This lemma is proved independently of the finite d=9,25 checks. It is a sufficient condition for ordinary squarefreeness only. It does not establish the fixed-node separation guard, and failure of the inequality is inconclusive.

Fresh exact reduced resultants give the following bounded values. These entries are computational data supporting applications of the lemma, not a guessed general formula:

| p | b | t_p(b) | Sufficient exponent s |
|---|---|---|---|
| 3 | 3,5 | 3 | s>=2 |
| 3 | 4 | 8 | s>=3 |
| 3 | 6,8 | 12 | s>=3 |
| 3 | 7 | 16 | s>=3 |
| 5 | 5,7,9 | 10 | s>=2 |
| 5 | 6,8 | 16 | s>=2 |
| 5 | 10 | 40 | s>=3 |
| 7 | 7 | 21 | s>=2 |
| 7 | 8 | 30 | s>=2 |

For example, every fixed b in {3,...,8} is squarefree at every primitive 3^s-th root with s>=3, and the d=9 exact certificate covers the remaining order 9. Likewise b=5,...,9 is squarefree at every order 5^s with s>=2. These are ordinary residual conclusions only until separation is independently supplied.

`fresh_reduction_orders.py` constructs H directly over F_p[q][z], computes its resultant with its ordinary derivative, shifts q=1+u, and records the least nonzero u exponent minus N. Resultant signs do not affect this order. `reduction_orders.json` includes the full sparse shifted-resultant coefficients, so the order is auditable rather than merely asserted.

## Scope and source baseline

The accepted input documents are:

- `../rs_discriminant_1017/frozen_review/INDEPENDENT_REVIEW.md`
- `../f020_second_review_20261017/public/SECOND_REVIEW.md`
- The retained local theorem: `../rs_discriminant_1017/frozen_review/sources/RS_Local_Discriminants_Working_Note_v3.tex`
- The accepted composition and normalization: `../rs_discriminant_1017/frozen_review/sources/archive_report.tex`, especially conditions (3), static factorization (17), and equations (20)-(25).

F020 remains the canonical owner and F023 its alias. Previously accepted fixed-residual families and all-odd overlap results remain accepted. This packet does not settle general b<d for arbitrary prime powers, arbitrary odd-composite static squarefreeness, characteristic-two paired-support or endpoint obligations, positive-characteristic generalizations, historical priority, or numerical conditioning. The original FFT objective and operation counts are unchanged. No external file or canonical record was changed.
