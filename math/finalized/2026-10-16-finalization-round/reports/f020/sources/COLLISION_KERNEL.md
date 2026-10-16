# A collision-kernel identity and an exact obstruction to one-sided recurrence arguments

13 October 2026 UTC. Candidate structural result and a do-not-repeat certificate, pending separate mathematical review. The all-m paired-support theorem remains OPEN at 58/100.

## Result and scope

The accepted trace recurrence gives a uniform Christoffel–Darboux kernel, explicit multiplicity-preserving collision-ideal syzygies, and an exact resultant identity. These statements isolate the extra noncancellation assertion that a recurrence-based squarefreeness proof would need.

That extra assertion is false, even for the actual Rogers–Szegő family outside every permitted low-order factor. In the existing m=12 control, an irreducible factor of the accepted R_12 has order 31,775. Every recurrence edge and all twelve kernel summands are nonzero at a repeated trace root, but the summands cancel. The inverse parameter is good. Thus this is a one-sided ordinary derivative collision and a counterexample to the proposed no-cancellation shortcut, not a paired-support or endpoint counterexample.

No m grid was extended. The witness is extracted from the already accepted m=12 polynomial, not an independently discovered family or a new accepted finite stage. Its role is to prevent repeating a particular invalid proof route.

## 1. Definitions and permitted localization

Work in F₂[q,X], m≥1. Retain the accepted normalization

P_0=1, P_1=X+q+q²,
P_j=(X+a_j)P_(j−1)+c_j P_(j−2),
a_j=q^(2j−1)+q^(2j), c_j=(1+q^(2j−1))(1+q^(2j−2)), j≥2.

As before, H_(2m+1)(z;q)=(z+1)U_m(z;q), U_m=z^mP_m(z+z⁻¹;q), and

P_m=A_old(X²)+X B_old(X²),
E_m=P_m(0), R_m=Res(A_old,B_old), Q_m=E_mR_m.

A prime means the ordinary X derivative unless explicitly stated otherwise. Write

L_b=∏_(r=0)^m(1+q^(2r+1)), b=2m+1,
Z_m=∏_(k=2)^m c_k, J_m=∏_(k=2)^m c_k^(k−1).

Both empty products at m=1 are 1. Every c_k is a unit in R_loc=F₂[q,1/L_b]. The odd factor has exponent 2k−1≤b. The even factor 1+q^(2k−2) is a power of 1+q^u, where u is the odd part of 2k−2 and u≤2k−2<b. Thus its support is also inverted. This does not assert that all other polynomial expressions formed from the edges are units.

## 2. Uniform collision-kernel lemma

Define

Δ_m=P_m'P_(m−1)+P_mP_(m−1)'.

Then, for all m≥1:

Δ_m=Σ_(j=0)^(m−1) [∏_(k=j+2)^m c_k] P_j².                 (1)

In particular Δ_m is a monic polynomial in X of degree 2m−2, contains only even powers of X, and has no assumed nonvanishing after parameter specialization.

There are explicit u_m,v_m∈F₂[q,X] satisfying

u_mP_m+v_mP_(m−1)=Z_m.                                    (2)

They are defined by u_1=0, v_1=1 and, for m≥2,

u_m=v_(m−1),
v_m=c_m u_(m−1)+(X+a_m)v_(m−1).

These give the two exact syzygies

Δ_m=P_(m−1)P_m'+P_mP_(m−1)',
Z_mP_m'=v_mΔ_m+P_m[u_mP_m'+v_mP_(m−1)'].                  (3)

Consequently the following is equality of ideals, not merely equality of root sets:

(P_m,P_m')=(P_m,Δ_m) in R_loc[X].                         (4)

Finally,

Res_X(P_m,P_(m−1))=J_m,
Res_X(P_m,Δ_m)=R_m² J_m.                                  (5)

The square on R_m is essential. Formula (5) does not replace the ordinary collision factor R_m by the low-order product J_m. It factors the larger resultant into the unresolved ordinary collision factor and a known unit.

### Proof

Differentiating the recurrence gives

P_m'=P_(m−1)+(X+a_m)P_(m−1)'+c_mP_(m−2)'.

Substitution into Δ_m cancels the two terms containing X+a_m. The remaining expression is

Δ_m=P_(m−1)²+c_mΔ_(m−1).

The base Δ_1=1 proves (1). Its final j=m−1 summand is monic of degree 2m−2, while every other summand has lower X degree, proving the degree and parity claims.

Multiply the identity (2) at m−1 by c_m and replace c_mP_(m−2) with P_m+(X+a_m)P_(m−1). This gives the displayed u_m,v_m recursion and proves (2). Multiplying the defining Δ_m by v_m and applying (2) proves the second identity in (3). Since Z_m is a unit after the permitted localization, (3) proves (4) in both directions without dividing by a value of P or P'.

For the first resultant identity in (5), reduction modulo the monic P_(m−1) gives

Res(P_m,P_(m−1))=c_m^(m−1)Res(P_(m−1),P_(m−2)).

Signs disappear in characteristic two. The m=1 value is 1. Induction yields J_m. Modulo P_m, Δ_m=P_m'P_(m−1); multiplicativity of the monic resultant gives the second identity because Res(P_m,P_m')=R_m². This is a polynomial identity, valid also at a multiple root; it does not require generic simplicity at the specialization. The constant-resultant convention at m=1 gives R_1=1 and both identities remain valid. ∎

### Precisely what is missing

At an allowed nonzero parameter α of odd order greater than b, P_m and P_(m−1) have no common root by (2). At a root x of P_m,

P_m'(x)=0 if and only if Δ_m(x)=0.

Thus a one-sided collision-exclusion argument using this recurrence would still have to prove that the sum (1) cannot vanish there. Unit edges alone do not imply this, and the counterexample below shows that even requiring every summand to be nonzero is insufficient.

## 3. Exact actual-family failure of kernel noncancellation

Binary hexadecimal integers encode polynomials with bit i equal to the coefficient of q^i. Let

m=12, b=25,
f(q)=0x1cca03=q²⁰+q¹⁹+q¹⁸+q¹⁵+q¹⁴+q¹¹+q⁹+q+1,
F=F₂[q]/(f), α=q mod f.

The two implementations prove f irreducible using the degree-20 Rabin conditions: α^(2²⁰)=α and gcd(f,q^(2¹⁰)+q)=gcd(f,q^(2⁴)+q)=1. They prove its exact order is

ord(α)=31,775=5²·31·41

by α^31775=1 and nonunit powers with exponents 31775/p for p=5,31,41. All explicit residues are in RESULTS.json. In particular every factor of L_25 is nonzero at α.

The accepted polynomial R_12 is divisible by f exactly once. This is checked by exact polynomial division and independently by a Sylvester determinant over F. At this parameter,

E_12(α)=0x83bed≠0,
gcd_X(P_12(X;α),P_12'(X;α))=X²+0x60c3e.

The repeated trace root is x=0x9beb1, whose square is 0x60c3e. Its second Hasse coefficient is nonzero, so its multiplicity in P_12 is exactly two. Ordinary second derivatives, which vanish in characteristic two, are not used for this test.

At x, all P_j(x;α), 0≤j≤11, are nonzero. In increasing j order the twelve weighted summands from (1) are

0xf8e85, 0x36d70, 0xdb88a, 0x2c48, 0xf4813, 0x16f51,
0x7fd07, 0x3fdfe, 0x5f38c, 0x25a98, 0x376fc, 0xf8f64.

Every entry is nonzero, and their characteristic-two sum is zero. All eleven c_2,…,c_12 are nonzero as well. The unweighted final term P_11(x;α)² is 0xf8f64, so the cancellation cannot be dismissed as a vanished adjacent polynomial.

This refutes, in the actual family, each proposed implication:

- invertible recurrence edges imply ordinary trace squarefreeness;
- consecutive coprimality implies ordinary trace squarefreeness;
- nonzero weighted square summands cannot cancel at a trace root;
- the low-order resultant Res(P_m,P_(m−1)) can replace the ordinary derivative resultant.

It does not refute a statement that also uses an additional, genuinely proved reciprocal-parameter condition.

### The inverse is good

The actual-degree reciprocal is f*=0x180a67, distinct from f. The full accepted Q_12 reversal is Q_12*=q^1300Q_12(q⁻¹), using deg Q_12=1300; its own degree is 1294 because Q_12 has q-content six. No padded reversal is used.

At α,

Q_12*(α)=0xfae08≠0.

Independent Gaussian construction at α⁻¹ verifies E_12(α⁻¹)≠0 and gcd_X(P_12(X;α⁻¹),P_12'(X;α⁻¹))=1. Direct construction of the residual U_12 gives derivative-gcd degrees four at α and zero at α⁻¹. Thus this is a pure one-sided collision. It contributes no factor to gcd(Q_12,Q_12*).

## 4. Exact interface with the accepted quadratic descent

Keep the accepted q-content removal and balanced pair, without changing any reversal:

v=6, s=647, ε=0,
f_12=q^(−653)Q_12=A_12(T)+qB_12(T), T=q+q⁻¹,
g_12=gcd(A_12,B_12).

The current witness has β=α+α⁻¹=0xe6503. Its minimal polynomial is the irreducible degree-20 trace factor

h(T)=0x123821,
q²⁰h(q+q⁻¹)=f(q)f*(q).

One implementation verifies the full polynomial lift; the other constructs h by multiplying the twenty Frobenius conjugates of β, independently of the folding algorithm. At β,

A_12(β)=0x58e48,
B_12(β)=0x2c724,
g_12(β)=0x9610a.

All three are nonzero, and A_12(β)=αB_12(β). Therefore A+αB=0 at the bad parameter while the coefficient pair is primitive at h. The quadratic norm A²+TAB+B² vanishes at β, although h divides neither g_12 nor the permitted folded denominator D_12.

This is an actual one-sided collision version of the already known norm-only obstruction. It does not establish a new general quadratic transformation, and does not turn a norm zero into a common factor of A and B. It reinforces the exact remaining requirement to control the coefficient pair, preserving both inverse-orbit types.

The identities in Section 2 concern the ordinary collision branch only. They do not remove the endpoint–endpoint, endpoint–collision, collision–endpoint, or collision–collision branch from Q=ER. The full Q gcd remains the multiplicity authority; taking the lcm of the four channel gcds is still invalid. The accepted ramified q=1 correction is unchanged and is not involved in this high-order witness.

## 5. Comparison with existing controls and a do-not-repeat rule

The existing m=2/order-15 control is one-sided endpoint failure: E_2 vanishes and R_2 does not. The present m=12/order-31,775 control is one-sided ordinary trace collision: R_12 vanishes and E_12 does not. Together they prevent proving the paired statement by simply excluding every single-parameter endpoint or collision. They are not two new families or new general-stage discoveries.

The accepted m=12/order-1285 control uses a different auxiliary polynomial W_12 and a different assertion: W_12(r)=W_12(αr)=0 at r=0x2892 modulo 0x14847, whereas W_12 and W_12(α²x) are coprime. Its endpoint values are 0x910b and 0xae8f, both nonzero. It refutes arbitrary-x q-shift separation. The current witness instead uses the ordinary X derivative of P_12 and refutes collision-kernel noncancellation. Both are bounded obstructions within the already studied m=12 family; this packet neither claims their logical independence as family discoveries nor counts either as an endpoint or paired-support counterexample. The older order-1285 facts are source-bound accepted findings, not newly replayed calculations in this packet.

The m=12/order-17 self-reciprocal collision remains a paired collision of allowed low order 17≤25. The current factor has distinct inverse orbits, high order, and only one bad orbit. Confusing those two controls would reverse the conclusion.

Do not reopen the unit-edge/no-cancellation route unless a proposed argument supplies a new hypothesis that this explicit order-31,775 witness fails, and proves that hypothesis uniformly in the reciprocal problem. Do not reopen generic q-shift separation without addressing the existing order-1285 witness. A larger finite m search or a further one-sided bad factor is not the completion condition.

## 6. Remaining question, priority and novelty

The concrete unresolved question is unchanged: for every m≥1, does the accepted balanced pair satisfy

support(gcd(A_m,B_m)) ⊆ support(D_m),
D_m=T∏_(r=1)^m J_(2r+1)(T)?

Equivalently, construct one uniform certificate a_mA_m+c_mB_m=D_m^s, or produce an actual-family factor outside D_m with its exact lifted order greater than 2m+1 and verified occurrence in both reciprocal sides. A recurrence-based continuation must use reciprocal parameters to rule out simultaneous endpoint/collision degeneracy, because same-parameter noncancellation is false.

Retain the four-channel next-task priority 58/100, dimensions (information gain, tractability, defensible novelty opportunity, scope/impact, evidence readiness)=(4,2,1,4,4). There is no automatic promotion from finding another obstruction. This completed bounded do-not-repeat stage is capped at 15; the disproved one-sided unit-edge route is capped at 8. The separate endpoint and all-A gates remain 53 and 57; frozen F020=67 and ALG-RS-PAIR=42 are unchanged.

The Christoffel–Darboux mechanism is classical; the standard confluent formula is recorded in [NIST DLMF 18.2.13](https://dlmf.nist.gov/18.2.E13). Its positive-measure setting must not be used to infer finite-field noncancellation. Section 2 supplies a direct characteristic-two polynomial proof. The accepted general reciprocal transformation is also classical. The present contribution is the explicit RS collision-ideal interface and this source-bound route-blocking certificate. No historical novelty, publication-priority, characteristic-zero counterexample, all-m support theorem, or FFT/runtime improvement is claimed.
