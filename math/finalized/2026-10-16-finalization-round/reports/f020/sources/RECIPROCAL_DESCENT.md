# Exact q-content and quadratic descent of the full reciprocal obstruction

13 October 2026 UTC. **An all-m algebraic lemma, with independent fixed controls. The general low-order support assertion remains OPEN.**

The new results are the exact q-adic orders of the endpoint and split resultant, and a multiplicity-exact descent of the entire reciprocal gcd to the invariant parameter T=q+q^(-1). This is a uniform structural mechanism, not an all-m coprimality proof. It uses every endpoint/collision channel. It neither repeats the failed same-prime normalization route nor extends the fixed-m census.

## 1. Setup and the previously accepted target

Work in F₂[q]. For m≥1, put b=2m+1 and use the integral Gaussian polynomial reduced modulo two:

H_b(z;q)=(z+1)U_m(z;q),
U_m(z;q)=z^m P_m(z+z^(-1);q),
P_m(X;q)=A_m^old(X²;q)+X B_m^old(X²;q).

Here the superscript `old` distinguishes the original split in the residual trace variable X from the new split in the parameter q. Put

E_m=P_m(0;q), R_m=Res_y(A_m^old,B_m^old), Q_m=E_m R_m,
N_m=deg Q_m=m(m+1)(2m+1)/3,
L_b=∏_(r=0)^m (1+q^(2r+1)).

The accepted degree theorem makes Q_m nonzero and monic. Reversal Q_m*=q^(N_m)Q_m(q^(-1)) always uses this actual nonzero degree. The known general target is

(Q_m,Q_m*)=(1) in F₂[q,1/L_b].                                       (1)

It is equivalent to the explicit polynomial certificate aQ_m+cQ_m*=L_b^(N_m). Equivalently, at every parameter of odd order greater than b, the residuals at q and q^(-1) cannot both fail squarefreeness. No implication below asserts that (1) holds for every m.

## 2. Uniform exact q-adic content

**Theorem 1.** For every m≥1,

v_q(E_m)=m mod 2,
v_q(R_m)=floor(m/2),
v_q(Q_m)=ceil(m/2).                                                (2)

These are exact valuations, not lower bounds and not valuations of an integer content. As a corollary, F_m=E_m R_m² has v_q(F_m)=m.

### 2.1 Three-term trace recurrence

The Gaussian recurrence gives

H_n=(1+z)H_(n−1)+z(1+q^(n−1))H_(n−2).

This identity follows coefficientwise from q-Pascal, so it holds over the polynomial ring before any localization. Introduce a formal invertible w, put z=w², and x=w+w^(-1). The normalized polynomials h_n=w^(-n)H_n(w²;q) satisfy

h_n=x h_(n−1)+(1+q^(n−1))h_(n−2),
h_(2m+1)=x P_m(x²;q).

Eliminating the intervening even h gives, for m≥2,

P_m(X)=[X+q^(2m−1)+q^(2m)]P_(m−1)(X)
       +(1+q^(2m−1))(1+q^(2m−2))P_(m−2)(X),                       (3)

with P_0=1 and P_1=X+q+q². These polynomial identities require no specialization or squarefreeness assumption.

Let p_0=1, p_1=X, p_j=Xp_(j−1)+p_(j−2), and p_(−1)=0. Reduction of (3) modulo q² gives, uniformly,

P_m(X;q)≡p_m(X)+q p_(m−1)(X) (mod q²).                            (4)

Indeed all new diagonal coefficients in (3) vanish modulo q², and every new off-diagonal coefficient equals one modulo q². The displayed P_1 checks the seed.

The polynomials p_j have parity j in X, are monic, and satisfy gcd(p_j,p_(j−1))=1 by repeated application of their recurrence. Also p_j(0)=1 for even j and zero for odd j. Equation (4) proves the first identity in (2).

### 2.2 Split-resultant content without illegal division

For m=2r, p_m=a(X²) and p_(m−1)=Xb(X²), with gcd(a,b)=1. Equation (4) says that all coefficients of B_m^old are divisible by q, that A_m^old modulo q is a, and that (B_m^old/q) modulo q is b. Since A_m^old is monic of degree r,

R_m=q^r Res(A_m^old,B_m^old/q).

The quotient on the right is first formed in F₂[q,y]. Its reduction modulo q is Res(a,b)=1. Therefore v_q(R_m)=r exactly.

For m=2r+1, p_m=Xb(X²), p_(m−1)=a(X²), again with gcd(a,b)=1. Now all coefficients of A_m^old are divisible by q, B_m^old is monic of degree r, and

R_m=q^r Res(A_m^old/q,B_m^old).

The reduced resultant is again one. This includes m=1, r=0, using the accepted resultant-of-two-nonzero-constants convention. Thus the second identity in (2) holds in every case; the third follows by multiplication. No vanishing residue factor, leading coefficient, factorial, or ramified integer is inverted.

## 3. The balanced quadratic coefficient pair

Write

v=ceil(m/2), qbar_m=q^(−v)Q_m ∈ F₂[q], d=N_m−v,
ε=d mod 2, V_m=(1+q)^ε qbar_m, 2s=d+ε.

Both the leading and constant coefficients of qbar_m and V_m are one, and s≥1. Define the balanced Laurent polynomial

f_m=q^(−s)V_m.

The invariant parameter T=q+q^(-1) gives a free rank-two algebra

F₂[q,q^(-1)] ≅ F₂[T,q]/(q²+Tq+1),                                (5)

with basis 1,q. Thus uniquely

f_m=A_m(T)+q B_m(T).                                               (6)

**Theorem 2, degree clause.** A_m is monic of degree s and either B_m=0 or deg B_m≤s−2. The new pair has roughly half the parameter degree of Q_m; this degree reduction alone is not a tractability or coprimality proof.

For an explicit formula set F_0=0, F_1=1, F_(k+1)=T F_k+F_(k−1). Then for k≥1,

q^k=qF_k+F_(k−1),  q^(−k)=qF_k+F_(k+1).

Apply these to the coefficients of q^(−s)V_m. The coefficients of q^s and q^(−s) are both one. Their two F_s contributions to B cancel, so only k≤s−1 remains and deg B≤s−2. The q^(−s) term contributes the unique degree-s monomial to A through F_(s+1). This proves the clause, including s=1, where B=0.

## 4. Exact ideal descent after the permitted localization

For r≥0 define the monic degree-r polynomial

J_(2r+1)(T)=q^(−r)(1+q+⋯+q^(2r))
           =1+Σ_(k=1)^r(q^k+q^(−k)).                              (7)

The right side is invariant, hence belongs to F₂[T]. Its constant coefficient is one. Define

D_m(T)=T ∏_(r=1)^m J_(2r+1)(T),
deg D_m=1+m(m+1)/2.                                                (8)

The factor identity

1+q^(2r+1)=(1+q)q^r J_(2r+1)(T)                                  (9)

shows that the quadratic extension of C_m=F₂[T,1/D_m] is precisely

S_m=F₂[q,q^(-1),1/L_b].                                           (10)

Here T=(q+1)²/q is a unit. Conversely, if D_m is inverted, every J factor and T is a unit; q+1 is then a unit as well, giving every factor of L_b. The extension C_m→S_m remains free of rank two and is faithfully flat. It is étale because the derivative in q of q²+Tq+1 is the unit T.

Let σ(q)=q^(-1), σ(T)=T. Equation (6) gives

f_m=A_m+qB_m,  σ(f_m)=A_m+q^(-1)B_m,
T B_m=f_m+σ(f_m),
T A_m=q^(-1)f_m+qσ(f_m).                                         (11)

These are explicit two-by-two syzygies. Since T is a unit,

(f_m,σ(f_m))=(A_m,B_m) S_m.                                       (12)

Moreover

f_m=q^(−s−v)(q+1)^ε Q_m,
σ(f_m)=q^(−s)(q+1)^ε Q_m*,                                       (13)

so the left side of (12) equals (Q_m,Q_m*)S_m. Notice the different powers of q in (13); treating qbar_m and Q_m as having the same reversal degree would be wrong.

The common ideal (Q_m,Q_m*) has no q-primary component, since Q_m*(0)=1. Consequently adjoining q^(-1) cannot change whether it is the unit ideal. Faithful flatness, or simply coefficient comparison in the free basis 1,q, now proves the exact equivalence

(Q_m,Q_m*)=(1) in F₂[q,1/L_b]
  ⇔ (A_m,B_m)=(1) in F₂[T,1/D_m].                                (14)

In particular, (14) retains all four disjunctive endpoint/collision branches. No norm replaces the coefficient pair, and no simplicity assumption is used.

### An explicit bounded certificate in the descended ring

Let g_m=gcd(A_m,B_m), using gcd(A,0)=A. It has degree at most s. Since F₂[T] is a PID, the following are equivalent:

- the conditions in (14);
- every irreducible factor of g_m divides D_m;
- g_m divides D_m^s;
- there are a_m(T),c_m(T)∈F₂[T] with

  a_m A_m+c_m B_m=D_m^s.                                         (15)

When B_m≠0 the degree bound s−2 can replace s, but the uniform exponent s covers the B=0 boundary. Equation (15) is a smaller exact certificate target, not an asserted all-m identity. Combining (14) with the accepted multiplicity bound for Q_m returns the original right-hand side L_b^(N_m); no new characteristic-zero conclusion is claimed without proving (15).

## 5. Multiplicity-exact reciprocal gcd, including both orbit types

The descent is stronger than a radical-support equivalence. Put

K_m=gcd(Q_m,Q_m*),
g_m,0=g_m/T^(v_T(g_m)),
K_m,0=K_m/(q+1)^(v_(q+1)(K_m)).

**Theorem 2, gcd clause.** There is an exact polynomial identity

K_m,0(q)=q^(deg g_m,0) g_m,0(q+q^(-1)).                            (16)

Proof: at each irreducible f(q) other than q or q+1, all q and q+1 factors used above are units, and T is a unit. Thus (11) identifies the local common ideal exactly with the ideal generated by g_m(T). The map T=q+q^(-1) has derivative T/q, nonzero at every such root. Therefore each irreducible factor in T pulls back with ramification index one. Removing T and q+1 removes the only exceptional finite branch, and multiplying by q^(deg g_m,0) clears Laurent exponents. The result on the right is monic, has constant coefficient one, and has precisely the same irreducible multiplicities as K_m,0. This proves (16).

For an irreducible f≠q,q+1 with a root α and trace β=α+α^(-1), let h be the minimal polynomial of β. If f=f*, then inversion is a nontrivial Frobenius power on F₂(α), the trace field has index two, and

f(q)=q^(deg h)h(T), deg f=2 deg h.

If f≠f*, then F₂(α)=F₂(β), the quadratic splits over the trace field, and

f(q)f*(q)=q^(deg h)h(T), deg f=deg h.

Indeed α satisfies X²+βX+1; a nontrivial extension of degree two would have inversion as its Galois automorphism. This is exactly the self-reciprocal case. In both cases the valuation of h in g_m is the paired minimum valuation represented by K_m. A single self-reciprocal factor and a complete distinct inverse pair are both detected; an isolated member of a distinct inverse pair is not.

### Explicit ramified multiplicity, without computing the original gcd

The removed q+1 multiplicity is itself read exactly from the descended pair. Put h=v_T(g_m), and define δ=1 if v_T(B_m)<v_T(A_m+B_m), otherwise δ=0, with v_T(0)=+∞. Then

κ_m=2h+δ−ε=v_(q+1)(K_m),
K_m=(q+1)^(κ_m) q^(deg g_m,0) g_m,0(T).                            (17)

To prove this, set w=q+1, so T=w²/q and

f_m=(A_m+B_m)(T)+wB_m(T).

The two summands have valuations 2v_T(A_m+B_m) and 1+2v_T(B_m). Their parity differs, so no lowest-order cancellation is possible. Also v_T(g_m)=min(v_T(A_m+B_m),v_T(B_m)). The displayed minimum is therefore 2h+δ. Removing the purposely added factor (q+1)^ε gives κ_m. Inversion preserves the q+1 valuation, so the same exponent occurs in K_m. Nonnegativity follows from the construction of V_m. This formula handles B_m=0 and shows precisely where the ramified branch differs from the unramified lift.

### Necessary ramified-boundary guard

Equation (16) cannot omit the removal of T and q+1. Already at m=1,

Q_1=q(q+1), K_1=q+1, A_1=T, B_1=0.

The uncorrected trace lift of gcd(A_1,B_1)=T is (q+1)², not K_1. This exact counterexample explains why the branch T=0 must be removed, rather than hidden in a global unramified claim. The permitted localization includes q+1 from the outset, so the exception does not weaken (14).

## 6. Fixed controls and a norm-only obstruction

Only m=1,2,12 are reconstructed; these are the boundary and previously accepted witnesses. There is no new m stage or enlarged search grid.

| m | v_q(Q_m) | N_m | s | deg A_m | deg B_m | deg gcd(A_m,B_m) |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 2 | 1 | 1 | −∞ | 1 |
| 2 | 1 | 10 | 5 | 5 | 3 | 3 |
| 12 | 6 | 1300 | 647 | 647 | 640 | 318 |

The two algorithms independently reconstruct every displayed polynomial, all four channel gcds, the exact fold, (16), and both bounded support certificates at these fixed controls. The independent field computation gives residual/derivative gcd degrees 2 at the m=2 order-15 factor f=q⁴+q³+1, zero at its reciprocal f*=q⁴+q+1, and 4 at the m=12 self-reciprocal order-17 collision factor q⁸+q⁷+q⁶+q⁴+q²+q+1.

The corresponding trace polynomials are

h_15(T)=T⁴+T³+1,
h_17(T)=T⁴+T³+T²+T+1.

For the synthetic one-sided polynomial f=q⁴+q³+1, its balanced coefficient pair is (A,B)=(T²,1). Thus gcd(A,B)=1, but its quadratic norm is

Norm(A+qB)=A²+TAB+B²=h_15(T).

The norm vanishes at the order-15 trace even though the coefficient pair is primitive. Consequently a norm-unit argument is strictly stronger and cannot replace (14). The actual m=2 family already realizes the same one-sided phenomenon. This is a guard against losing the inverse-orbit distinction, not a counterexample to the desired RS support bound.

Four separately labelled synthetic assignments of f and f* to E and R check the endpoint–endpoint, endpoint–collision, collision–endpoint, and collision–collision branches. These are algebraic channel controls, not alleged RS instances. The actual m=12 collision witness remains within 17≤25 and therefore still does not refute the target order bound.

## 7. What this proves, and the precise unresolved obligation

Proved uniformly in m:

1. Exact q-content (2), including the m=1 convention.
2. The free quadratic coefficient representation with the strict degree gap.
3. Exact ideal equality after the allowed localization, via explicit syzygies (11).
4. The bounded certificate equivalence (15).
5. The multiplicity-exact gcd lift (16), the full ramified correction (17), and preservation of both Frobenius orbit types and every endpoint/collision channel.

Still unproved: that gcd(A_m,B_m) has no irreducible factor outside D_m for all m. The three-term recurrence proves the q-content but does not furnish a recurrence for the new pair that forces this coprimality. The degree gap does not itself rule out a common factor. An acceptable completion is one all-m certificate (15), or one actual-family h outside D_m together with its lifted irreducible factor(s), exact odd order greater than 2m+1, and verified occurrence in both reciprocal sides. A norm zero, a synthetic pair, or an enlarged finite grid does not complete that task.

The characteristic-two paired support bound remains a sufficient transport guard for the characteristic-zero residual statement: a characteristic-zero cyclotomic divisor reduces to a full reciprocal cyclotomic divisor modulo two. The converse does not follow. Neither the present descent nor a future modular counterexample alone implies a characteristic-zero counterexample. General all-A overlap simplicity remains a separate obligation.

The recurrence, resultant homogeneity, quadratic invariant theory, and étale ideal descent are classical ingredients. The assembled exact RS q-content and coefficient-pair target are new relative to the supplied packet. No historical novelty, publication priority, Fourier runtime improvement, or completed general theorem is claimed.

## 8. Next-task ranking

Retain **58/100** for the remaining all-m support proof-or-obstruction, with dimensions (information gain, tractability, defensible novelty opportunity, scope/impact, evidence readiness)=(4,2,1,4,4). The exact descent halves the parameter-degree representation and exposes a primitive-coefficient condition, but it does not justify increasing tractability before a uniform certificate or actual-family obstruction exists. The completed structural lemma is subject to the completed-stage cap 15. The separate all-A overlap next gate remains 57; frozen F020=67 and ALG-RS-PAIR=42 are unchanged.
