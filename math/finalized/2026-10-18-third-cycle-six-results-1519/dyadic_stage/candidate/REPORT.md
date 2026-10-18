# A dyadic norm obstruction and a seven-stage lower bound at sixteen points

Owner: **M-MULTISCALE-CHIRP / Q24**. Date: 18 October 2026.

**Candidate result; independent review pending.** No external write, catalogue edit, status change, new owner, score change, or census change is made.

## 1. Result and limits

Keep the original literal grammar: individually invertible factors `(I-alpha S^s)^-1`, arbitrary integer strides, and interspersed nonzero scalar Weyl-monomial gauges. The target is the full chirp matrix `C[i,j]=zeta^((i-j)^2)`. No arbitrary diagonal gauges, additive branches, selected-output weakening, or changed target coefficients are used.

The new results are:

1. **General dyadic norm transfer.** For `N=2^m >= 4`, a legal length-L representation descends to a representation of the `N/2` chirp with `L+e` factors, where e counts its even strides. Every descended factor is individually invertible. An iterated, valuation-weighted version is proved below.
2. **Sixteen-point obstruction.** In characteristic zero, with zeta any primitive 32nd root, **at least seven resolvents are required**. This improves the inherited `m+1=5` lower bound by two stages. The proof combines a new, exact six-odd-factor requirement with the accepted eight-point minimum seven.
3. **Declared upper bounds.** Fifteen legal stages suffice over C and over an explicit finite splitting extension of Q(zeta). In characteristic 17, for `zeta^2=3`, the same lower bound seven holds, and fifteen stages suffice over **F(17^12)** by a verified factorization into degrees 1,4,4,6.

Thus the new interval at N=16 is **7 <= minimum <= 15** in the stated attainment fields. This is **not an exact sixteen-point minimum** and does not close the parent. There is no FFT speedup, arithmetic-runtime lower bound, efficient coefficient-discovery result, numerical stability claim, or historical priority claim.

## 2. Algebra and normalization

Write `a=zeta^-1` and

`Q_N(x) = sum_(t=0)^(N-1) a^(t^2) x^t` in `A_N=K[x]/(x^N-1)`.

Even N makes the coefficients N-periodic. The geometric-character sum gives

`C Q_N(S) = N I`.

Indeed, its cyclic coefficient at displacement u is `a^(u^2) sum_j a^(-2uj)`, equal to N for u=0 and zero otherwise. This proves invertibility over any field of characteristic not dividing 2N containing zeta.

As in the accepted N=8 proof, move all Weyl gauges through the resolvents. Their conjugations only rescale the binomial parameters. The final modulation must be scalar because the target and binomial product are invertible circulants. A net shift is absorbed using

`x^r Q_N(x) = a^(r^2) Q_N(a^(-2r) x)`.

Thus, after a root-of-unity rescaling of the variable, a hypothetical representation gives `P(x)=h Q_N(x)`, h nonzero, with P a product of L invertible shift binomials. Zero parameters and stride-zero scalar factors can be removed. Negative strides can be reversed by extracting a nonzero scalar and monomial, then applying the same shift normalization. At N=16 the remaining stride representatives are 1,...,8.

The exact pole guard for a stride s is

`alpha^(N/gcd(N,s)) != 1`.

Replacing it by an indiscriminate `alpha^N != 1` would exclude legal nongenerating strides. All proofs below use actual factorwise invertibility.

## 3. General dyadic norm transfer

Put n=N/2 and y=x^2. The even subalgebra of A_N is `B_n=K[y]/(y^n-1)`. Define

`Norm(f)(y) = f(x) f(-x)`.

This is multiplicative. Direct cyclic convolution gives the exact identity

`Norm(Q_N)(y) = H_N Q_n(-y)`,

where Q_n uses the primitive `2n`th root `zeta^2`, and

`H_N = sum_(t=0)^(N-1) (-1)^t a^(2t^2)`.

For completeness, the coefficient of x^(2u) in the norm is

`sum_t (-1)^t a^(t^2+(2u-t)^2)
 = (-1)^u a^(2u^2) sum_t (-1)^t a^(2t^2)`.

The odd coefficients are zero. Q_N and its norm are units, so H_N is nonzero. This also avoids selecting a square-root value of a Gauss sum.

For a factor, the exact rules are:

- s odd: `Norm(1-alpha x^s) = 1-alpha^2 y^s`;
- s even: `Norm(1-alpha x^s) = (1-alpha y^(s/2))^2`.

Each displayed binomial is a unit. One proof is to evaluate at every n-th root y and lift to the two N-th roots x and -x: its value, or its square in the even case, is a product of two nonzero original values. Equivalently the same fact follows from the explicit pole guards.

Apply the norm to `P=h Q_N`, then replace y by -y and absorb the nonzero scalar. The result is a legal all-row representation of the n-point chirp in the same grammar. There is one descended factor per odd stride and **two per even stride**, for a total `L+e`. The norm is a mathematical reduction; it is not a free implementation of the original transform.

### Iterated form

For `1 <= k <= m-1`, let `v_2(s)` be the valuation of a nonzero stride representative modulo N. After k norm descents, the factor arising from s has multiplicity

`w_k(s)=2^min(v_2(s),k)`.

Consequently any known lower bound `b_(N/2^k)` in the same coefficient field implies the necessary inequality

`sum_(j=1)^L 2^min(v_2(s_j),k) >= b_(N/2^k)`.

Variable rescalings and scalar gauges during descent alter parameters but do not change multiplicities or legality. This is a general field-sensitive obstruction for dyadic chains; it does not assert that these inequalities alone are sufficient.

## 4. A new N=16 parity obstruction

For N divisible by eight,

`Q_N(-x)=x^(N/2) Q_N(x)`.

At N=16, split P into its odd-stride product O and even-stride product E. Since E(-x)=E(x) and E is a unit, the target identity forces

`O(-x)=x^8 O(x)` in `K[x]/(x^16-1)`.

**Lemma.** In characteristic zero, or characteristic 17, no product of at most five odd-stride binomials can satisfy this equation. In particular every legal sixteen-point representation contains at least six odd-stride factors.

The lemma is stronger than necessary in that the normalized coefficient equations have no solution even if factorwise invertibility is dropped. Here is a complete finite, exact proof.

### 4.1 Exhaustive normalization

Reverse negative odd strides as above, so their representatives are 1,3,5,7. Reversing a nonzero factor can extract a monomial. For the parity equation, removing a monomial changes its right-hand sign by at most -1. Such a sign is restored by substituting x -> lambda x with `lambda^8=-1`, `lambda^16=1`. This can be done over the algebraic closure when proving a lower bound. A zero-parameter factor is the identity and requires no inversion; it can remain a zero-parameter factor at the new representative stride.

The substitution x -> x^3 followed by sign reversal permutes these four stride classes in the cycle

`1 -> 3 -> 7 -> 5 -> 1`.

The same sign-restoring substitution deals with the extracted monomials. Pad a shorter product with identity factors to obtain five. There are 56 count vectors `(n1,n3,n7,n5)` summing to five and exactly fourteen orbits under this cyclic action. Use the lexicographically largest vector in each orbit.

For a group of n factors of stride s, write the unrestricted polynomial

`1 + a_(s,1) x^s + ... + a_(s,n) x^(ns)`.

These coefficients include every original binomial product. Allowing arbitrary grouped coefficients enlarges the possible solution set and is therefore safe for an exclusion.

### 4.2 Exact certificate

Expand the four grouped polynomials cyclically to `O=sum c_i x^i`. The eight necessary equations are

`f_i=(-1)^i c_i-c_(i+8)=0`, 0 <= i < 8.

For each of the fourteen normalized count vectors, PARITY_CERTIFICATES.json stores rational polynomials H_i satisfying the literal polynomial identity

`sum_(i=0)^7 H_i f_i = 1`.

The fourteen multipliers have 182 nonzero terms in total. The largest product degree is 13. All denominators have prime divisors only in {2,3,5,7}, so exactly the same identities reduce modulo 17. No finite-point search or characteristic-zero specialization argument is used here: the identities hold over the algebraic closure in both claimed characteristics.

The certificate vectors, in `(n1,n3,n7,n5)` order, are:

`(2,1,1,1), (2,1,2,0), (2,2,0,1), (2,2,1,0),
 (3,0,0,2), (3,0,1,1), (3,0,2,0), (3,1,0,1),
 (3,1,1,0), (3,2,0,0), (4,0,0,1), (4,0,1,0),
 (4,1,0,0), (5,0,0,0)`.

The standard-library checker independently reconstructs every f_i from the grouped product before checking every identity. It also enumerates all 56 count vectors and verifies their complete orbit coverage. No Gröbner engine, numerical solver, or generator code is imported during verification.

As an illustrative short elimination for the most mixed pattern, write

`O=(1+A x+B x^2)(1+c x^3)(1+d x^5)(1+e x^7)`.

Its equations include

`f0=(Ae-1)(cd-1)`, `f2=B(1-cd)-ce`, `f3=-c(Ae+1)`.

They satisfy

`Bc f0 + B(cd-1) f3 - 2c f2 = 2c^2 e`.

If the three displayed single factors are nontrivial, this already contradicts the equations. The stored unit certificate handles all zero-parameter boundary cases as well.

## 5. Seven-stage lower bound

Suppose a sixteen-point chain used at most six resolvents. The parity lemma forces at least six odd-stride factors, so the only remaining case has exactly six factors and all strides odd. Its dyadic norm therefore has exactly six factors, rather than a doubled even-stride cost. Section 3 gives a legal six-stage eight-point chirp representation over the same coefficient field.

This contradicts the independently accepted N=8 minimum seven:

- in characteristic zero, for the root `zeta^2`, the inherited lower bound holds over every coefficient field containing that primitive sixteenth root;
- in characteristic 17 with `zeta^2=3`, the inherited five polynomial certificates exclude smaller chains over the **algebraic closure** of F17. Therefore they also exclude the descended chain over any extension used here.

This proves `L>=7` in both stated settings. No conclusion is inferred from the old F17-rational minima 10 and 11.

## 6. Exact fifteen-stage constructions

### 6.1 Characteristic zero

At N=16,

`Q_16(x)=1+a x+a^4 x^2+a^9 x^3-x^4-a^9 x^5+a^4 x^6-a x^7
          +x^8-a x^9+a^4 x^10-a^9 x^11-x^12+a^9 x^13+a^4 x^14+a x^15`.

Let rho_1,...,rho_15 be its roots in a splitting field, counted with multiplicity, and set `alpha_j=rho_j^-1`. The nonzero constant coefficient ensures that all roots are nonzero, and

`Q_16(x)=product_(j=1)^15 (1-alpha_j x)`.

The exact inverse identity proves Q_16 has no zero on the sixteenth roots of unity. Hence `alpha_j^16 != 1` for every j, and

`C = 16 product_(j=1)^15 (I-alpha_j S)^-1`.

This is an exact algebraic all-row witness, not a list of approximate parameters. It applies over C and a finite splitting extension of Q(zeta), of degree at most 15!. Attainment over Q(zeta) itself is not asserted.

### 6.2 A finite-field construction over F(17^12)

Choose zeta with `zeta^2=3` in F(17^2); then zeta has order 32. Put a=zeta^-1, so `a^2=6`. Substituting x=a z yields the F17 polynomial

`R(z)=Q_16(a z)=sum_(t=0)^15 6^(t(t+1)/2) z^t`.

The exact factorization is

`R(z)=-(z-1) G1(z) G2(z) G3(z)`,

where

`G1=z^4+2z^3-4z^2+2z+1`,
`G2=z^4-6z^3+8z^2-6z+1`,
`G3=z^6-6z^5+3z^4+6z^3+3z^2-6z+1`.

The checker verifies the multiplication and irreducibility of all three polynomials using Frobenius powers and polynomial gcds. Their splitting degrees are 4,4,6, so they split in F(17^12), which also contains zeta. This uses the standard finite-field splitting/subfield theorem; see Keith Conrad's [Finite Fields](https://kconrad.math.uconn.edu/blurbs/galoistheory/finitefields.pdf), Sections 2 and 5.

If beta_1,beta_2,beta_3 are any chosen roots of G1,G2,G3 in this field, an exact list of fifteen shift-one parameters is

`zeta`,
`zeta / beta_1^(17^j)` for j=0,...,3,
`zeta / beta_2^(17^j)` for j=0,...,3,
`zeta / beta_3^(17^j)` for j=0,...,5.

These are exact finite-field element definitions. The formal factorization and inverse identity give the same fifteen-stage equality and pole guards. We do not claim a coordinate-level root list, a minimal coefficient extension, or that fifteen is the field's minimal stage count.

## 7. Fully separated cost accounting

The lower bound concerns literal resolvent count only. For the construction, all fifteen factors have stride one. Given a parameter alpha and precomputed `d=(1-alpha^16)^-1`, one application solves

`y_i-alpha y_(i-1)=x_i` cyclically.

First evaluate `H=alpha^15 x_0+...+x_15` by Horner and set `y_15=d H`. Then recover y_0,...,y_14 by `y_i=x_i+alpha y_(i-1)`. This costs **31 coefficient-field multiplications and 30 additions**. It uses an in-place sixteen-element input/output buffer and at most two scalar working registers once the parameter and d are loaded. The checker verifies both the equation and operation counts on an exact positive control.

Therefore fifteen applications plus the final scalar gauge cost **481 multiplications and 450 additions** per vector. Precomputing the fifteen d values by four squarings for each alpha adds **60 multiplications, 15 subtractions and 15 inversions**. The counted setup-and-one-vector total is **541 multiplications, 465 additions/subtractions and 15 inversions**, plus the following separate, unavoidable coefficient costs:

- construction/factorization of Q_16 and exact discovery of its roots;
- selection/construction of the splitting field and embeddings;
- computation of the fifteen reciprocals or their equivalent parameter representation;
- conversion to the representation used for coefficient-field arithmetic.

Call the total of those coefficient-discovery/representation costs `F_coeff`. The complete symbolic bill is **F_coeff + 541M_K + 465A_K + 15Inv_K**. F_coeff is not proved small here; no comparison may silently omit it. The fifteen alpha values and fifteen d values occupy thirty coefficient-field elements, in addition to the sixteen-element data buffer and two working registers. A general coefficient-field multiplication is not a base-field operation or a constant-time bit operation. No numerical approximation, precision, condition-number, or stability bound has been supplied.

The finite-field factorization is an exact existence/splitting certificate, not an implementation with F_coeff already paid. The characteristic-zero root specification has the same limitation. Consequently this result provides no runtime or memory advantage over a conventional FFT.

## 8. Exact controls and source binding

Run `python verify_exact.py`. Its standard-library checks cover:

- fourteen rational unit-ideal identities and their reductions modulo 17;
- independent reconstruction of the inputs and all 56 stride-pattern orbits;
- all 256 entries of the sixteen-point inverse matrix identity in `Z[a]/(a^16+1)`;
- exact norm identities at N=4,8,16,32,64;
- 6,663 legal individual-factor norm cases in F17, F97 and F193, with correct stride-sensitive pole guards;
- the finite factorization, irreducibility degrees, and primitive-32-root condition;
- an exact cyclic-resolvent application and its operation count;
- corrupted multiplier, defining-equation, and chirp-target controls, all rejected.

`make_certificates.py` is supplied to regenerate the rational certificates, but is not part of the trusted verification path. It uses only rational arithmetic and an elementary tracked polynomial-basis calculation. Exploratory scripts are segregated from the proof deliverable.

`SOURCE_BINDINGS.json` hashes the accepted N=8 report and independent review, plus the inherited grammar audit and selected owner record. This pass uses those as mathematical sources and does not run their historical scripts. The current result establishes a general transfer rule and a larger-N obstruction. The exact N=16 minimum, stronger general stage bounds, attainment over the original cyclotomic coefficient field, fast coefficient discovery, numerical conditioning, and prior-art attribution remain open.
