# An eight-stage lower bound for the sixteen-point chirp

Owner: **M-MULTISCALE-CHIRP / Q24**. Date: 18 October 2026.

**Completed candidate with exact verification; independent review pending.** No external writes, catalogue edits, score/status changes, new owner, or census changes are made.

## 1. Result and boundary

Use the original literal grammar: individually invertible pure-shift resolvents `(I-alpha S^s)^-1`, arbitrary integer strides, and interspersed nonzero scalar Weyl-monomial gauges. The full target is `C[i,j]=zeta^((i-j)^2)`, where zeta is a primitive 32nd root. No arbitrary diagonal gauges, additive branches, selected-output weakening, or changed target coefficients are admitted.

**Theorem.** In characteristic zero, every legal sixteen-point representation has **at least eight odd-stride factors**, and hence at least eight resolvents in total. The same assertion holds in characteristic 97. Fifteen stages still suffice over C and a finite splitting extension of Q(zeta). Thus the characteristic-zero interval improves from the accepted `7 <= minimum <= 15` to

`8 <= minimum <= 15`.

For the concrete finite-field root `zeta=46` in F97, fifteen stages suffice over F(97^12), so the same interval holds in that field. The lower bound applies over every characteristic-97 coefficient field containing a primitive 32nd root.

This is **not** an exact minimum. The earlier characteristic-17 interval remains 7 through 15; it is not improved here. No arithmetic-runtime lower bound, FFT speedup, efficient coefficient discovery, numerical stability result, attainment over Q(zeta) itself, or historical-priority claim is made.

The new lower bound does not depend on the eight-point minimum. It directly excludes every product of at most seven odd-stride binomials satisfying the required parity identity. The field-transfer argument below explicitly handles projective boundary points, poles, lost constant coefficients, and possibly zero products.

## 2. Full target identity and normalization

Put `a=zeta^-1` and

`Q(x)=sum_(t=0)^15 a^(t^2) x^t` in `A=K[x]/(x^16-1)`.

The all-row inverse identity is

`C Q(S)=16 I`.

For cyclic displacement u the product coefficient is

`a^(u^2) sum_(j=0)^15 a^(-2uj)`,

which is 16 when u=0 and zero otherwise. The standalone verifier checks all 256 matrix entries integrally in `Z[a]/(a^16+1)`. This simultaneously binds the coefficients of the full target, proves invertibility, and survives reduction modulo 97.

Moving Weyl gauges through the resolvents only rescales binomial parameters. The remaining modulation is scalar because both the target and the binomial product are invertible circulants. A remaining monomial shift is absorbed by the exact coefficient identity

`x^r Q(x)=a^(r^2) Q(a^(-2r)x)`.

Consequently a legal representation normalizes to a scalar multiple of Q as a product of invertible shift binomials. The verifier checks all 256 coefficient instances of this shift identity.

The precise factorwise pole guard is

`alpha^(16/gcd(16,s)) != 1`.

Stride-zero scalar factors and zero-parameter identity factors may be removed. Negative strides may be reversed using a nonzero scalar and monomial, then renormalized. None of these steps introduces arbitrary diagonal operations.

## 3. The required parity relation

The exact target relation is

`Q(-x)=x^8 Q(x)`.

Write a normalized candidate product as `P=O E`, where O contains the odd-stride factors and E the even-stride factors. Since `E(-x)=E(x)` and E is a unit, cancellation is legal and gives

`O(-x)=x^8 O(x)` in A.

The new lemma is stronger than needed: in characteristic zero or 97, **no product of at most seven odd-stride binomials can satisfy this equation, even if invertibility of those binomials is not required**.

### 3.1 Exhaustive finite normalization

Normalize odd strides modulo sixteen, reverse negative representatives, and absorb extracted nonzero scalars. Representatives may be taken as 1,3,5,7. Extracting a monomial can change the parity relation to

`O(-x)=-x^8 O(x)`.

Substituting `x -> lambda x`, with `lambda^16=1` and `lambda^8=-1`, restores its sign. Such roots exist in the algebraic closure in both claimed characteristics; they already lie in F97. Zero-parameter factors need no inversion and can be treated as identity factors.

Substitution `x -> x^3`, followed by the same stride reversals and sign repair, cyclically permutes the classes

`1 -> 3 -> 7 -> 5 -> 1`.

It preserves the exponent on the right because `x^24=x^8` in A. Pad with identity factors to obtain exactly seven. There are exactly 120 count vectors `(n1,n3,n7,n5)` of sum seven, in exactly 30 rotation orbits. We take the lexicographically largest representative of each orbit.

For n factors at stride s, replace their product by the unrestricted grouped polynomial

`1 + b_(s,1)x^s + ... + b_(s,n)x^(ns)`.

This includes every original product and enlarges the coefficient domain safely for a nonexistence proof. If the cyclic grouped product is `O=sum c_i x^i`, the eight equations are

`f_i=(-1)^i c_i-c_(i+8)=0`, for 0 <= i < 8.

The other eight coefficient equations repeat these. The standalone checker reconstructs these equations from the four grouped factors and verifies complete orbit coverage.

The unrestricted parity threshold is sharp: `1+x^8` satisfies the parity equation and splits into eight stride-one binomials over the algebraic closure. However every such factor is singular, since its parameter has eighth power -1 and sixteenth power 1. This is not a legal eight-stage chirp construction. Further lower bounds must exploit invertibility or more of the full target than this unrestricted parity equation.

## 4. Exact algebraic-closure certificates in characteristic 97

For each of the thirty count representatives, a JSON file in `parity7_traces/` records a finite, exact derivation of 1 from the eight polynomials f_i over F97. These are polynomial identities over the field, so they exclude solutions over its entire algebraic closure. They are not finite-point searches.

The certificate format avoids enormous expanded multipliers. Each node is one of:

1. An independently reconstructed input polynomial f_i.
2. A nonzero field-scalar multiple of an earlier node.
3. A monomial multiple of one earlier node minus a monomial multiple of another, minus explicit polynomial multiples of earlier nodes, followed by scalar multiplication.

Every node is therefore in the ideal generated by f_0,...,f_7. The final node is literally the constant polynomial 1. The verifier recomputes every identity using integer dictionary arithmetic modulo 97. It neither trusts a claimed Groebner basis nor checks only evaluations; no symbolic algebra package or discovery code is imported. Leading-term choices and pair-selection claims are unnecessary to certificate soundness.

The verified thirty traces contain 4,568 nodes and 81,904 stored polynomial terms. All thirty final-polynomial mutations and all thirty input-equation mutations are rejected. The rootwise control checks 75,264 nonzero projective binomials, and the application control checks 1,296 exact basis-vector applications.

The discovery program uses symbolic elimination to find these derivations. Its algorithm is outside the trusted verification path. A fresh independent reviewer can reconstruct every input and audit each local polynomial equality without rerunning that elimination.

## 5. Why the characteristic-zero transfer is valid

A modular unit ideal alone does not prove characteristic-zero nonexistence. This step supplies the missing compactness and boundary argument.

Suppose a characteristic-zero solution with r <= 7 odd-stride factors existed. Its finitely many polynomial equations have rational coefficients. A solution over any characteristic-zero coefficient field implies an algebraic-number solution, by the weak Nullstellensatz applied over the algebraic closure of Q. Take a number field containing its coefficients and the required roots of unity, and a valuation above 97.

Write each factor projectively as `u_j+v_j x^(s_j)`. Scale its two coefficients so both are integral and at least one is a unit. Scaling factors does not change the homogeneous parity relation. Reduce the factors and that relation into the residue field, contained in the algebraic closure of F97.

Crucially, **the reduced product cannot be zero in `Fbar_97[x]/(x^16-1)`**. Each reduced pair is nonzero. Since s_j is odd, `lambda -> lambda^(s_j)` permutes the sixteen distinct sixteenth roots of unity. A nonzero binomial `u+v x^s` therefore vanishes at at most one of those roots; a nonzero monomial or constant vanishes at none. Seven such factors cannot cover all sixteen roots. Their product is nonzero at at least nine roots. This explicitly prevents the all-zero-product degeneration.

Remove any reduced nonzero constants and extract any reduced monomials. The remaining factors have nonzero constant coefficients and can be affinely normalized. Removing the monomial may change only the parity sign; repair it using a sixteenth root whose eighth power is -1. Reverse negative strides, repair the sign again if needed, and pad with identities. One obtains a product covered by one of the thirty characteristic-97 certificates.

Those certificates exclude every such affine product, including singular products and zero parameters. This is a contradiction. Thus no characteristic-zero parity solution with at most seven odd factors exists.

The argument makes no assumption that individual factors stay invertible under reduction. Poles, constants, monomial limits, and lost degree are all allowed and handled. Only the strict seven-versus-sixteen root-count bound prevents the product from disappearing. In particular, no finite-field rational-point minimum is transferred to characteristic zero.

## 6. Legal fifteen-stage upper bounds

### 6.1 Characteristic zero

Q has degree fifteen and constant coefficient one. In its splitting field, let rho_1,...,rho_15 be its nonzero roots, with multiplicity, and set `alpha_j=rho_j^-1`. Then

`Q(x)=product_(j=1)^15 (1-alpha_j x)`.

The all-row inverse identity proves Q is nonzero on every sixteenth root of unity. Consequently `alpha_j^16 != 1` for each factor and

`C=16 product_(j=1)^15 (I-alpha_j S)^-1`.

This is an exact algebraic witness over C and a finite splitting extension of Q(zeta), of degree at most 15!. Exact attainment over Q(zeta) itself is not asserted.

### 6.2 Explicit splitting specification in characteristic 97

Take `a=19` and `zeta=46` in F97. Their product is one and `19^16=-1`, so zeta is primitive of order 32. The exact factorization is

`Q(x)=19 (x-19) F1(x) F2(x) G1(x) G2(x)`,

where

`F1=x^3+43x^2-32x+19`,
`F2=x^3-26x^2-40x-20`,
`G1=x^4+7x^3-46x^2+5x-47`,
`G2=x^4-33x^3-30x^2+18x-47`.

All coefficients are in F97. The checker verifies multiplication and irreducibility using Frobenius powers and polynomial gcds. The irreducible degrees are 1,3,3,4,4, whose least common multiple is twelve. The factors therefore split in F(97^12).

Choose a root beta_k of each of the four nonlinear factors in that field. An exact list of fifteen shift-one parameters is

`46`,
`beta_k^(-97^j)` for k=1,2 and j=0,1,2,
`beta_k^(-97^j)` for k=3,4 and j=0,1,2,3.

Together with the scalar gauge 16 they give the same full matrix identity. The independently checked `gcd(Q,x^16-1)=1` ensures every individual pole guard. This is an algebraic specification, not a coordinate-level root table or a coefficient-discovery implementation. Minimality of the extension degree is not asserted.

## 7. Separate setup, application, and representation costs

The new lower bound counts literal resolvent stages only. For the fifteen-stage witness all strides are one. Given alpha and the precomputed value `d=(1-alpha^16)^-1`, one cyclic application uses Horner evaluation followed by the recurrence `y_i=x_i+alpha y_(i-1)`.

The exact per-factor bill is 31 coefficient-field multiplications and 30 additions. Fifteen factors plus the final scalar gauge cost

`481 M_K + 450 A_K` per vector.

Precomputing all fifteen d values adds 60 multiplications, fifteen subtractions, and fifteen inversions. If F_coeff denotes the separate cost of field construction, polynomial factorization, exact root discovery, root reciprocals, embeddings, and representation conversion, the setup-plus-one-vector bill is

`F_coeff + 541 M_K + 465 A_K + 15 Inv_K`.

F_coeff has not been proved small and must not be dropped. The lower-bound certificate computation is a separate research/proof cost, not transform coefficient setup and not vector application.

The described in-place procedure uses a sixteen-element data buffer and at most two scalar working registers, in addition to fifteen parameters and fifteen precomputed inverses. Extension-field operations are not base-field operations or constant-time bit operations. The verifier checks the recurrence and counts on every basis input for all legal F97 parameters. No precision, conditioning, stability, or FFT runtime advantage follows.

## 8. Reproduction and remaining work

Run `python verify_exact.py`. It verifies all thirty derivation certificates, reconstructs all input equations, checks all 120 count vectors, rejects corrupted certificates, checks the full integral 256-entry target inverse, verifies parity and shift normalization, verifies the explicit finite factorization and its pole exclusion, and checks the application algorithm and operation count.

`SOURCE_BINDINGS.json` pins the accepted seven-through-fifteen report and independent review. They provide the prior comparison and grammar context; their historical scripts are not imported or executed. `MANIFEST.json` freezes the canonical deliverables. Exploratory computations are segregated and are not needed for verification.

Open: the exact N=16 minimum; exclusion or construction at lengths 8 through 14; stronger uniform dyadic results; the original cyclotomic coefficient field; improved characteristic-17 bounds; efficient coefficient discovery; numerical certification; and historical attribution. The broader owner stays open.
