# Smaller splitting fields for eight and fourteen banks

10 October 2026. Separate author addendum, pending independent review. The accepted base-field 2N−4 theorem and all predecessor packets remain unchanged. These constructions preserve the small bank counts over smaller extensions; they do not assert attainment over K itself.

## 1. Eight order-seven banks over a quadratic extension

Let q have order seven and K=Q(q). Keep the accepted order-seven moments s_0,…,s_4 (called m_0,…,m_4 in the manuscript), with s_0=1, s_2=q and H=q/(1+q). Define

A=(−31−5q+5q²+20q³−q⁴−18q⁵)/29,
B=(−9−37q−21q²+3q³+10q⁴+6q⁵)/29,
h(t)=t²+A t+B,
g(t)=(t−q)h(t).

The resulting cubic has ascending coefficients

c_0=(6+15q+43q²+27q³+3q⁴−4q⁵)/29,
c_1=(−27−24q−34q²−20q³−28q⁴−11q⁵)/29,
c_2=(−31−34q+5q²+20q³−q⁴−18q⁵)/29,
c_3=1.

Direct reduction modulo Φ_7 proves the two exact recurrence equations

Σ_(k=0)^3 c_k s_k=0,
Σ_(k=0)^3 c_k s_(k+1)=0.

The quadratic discriminant is

δ=(1215+3313q+1617q²−1884q³−1843q⁴+60q⁵)/841.

Use the same three-node mirrored architecture (3,1,1,3), with the roots of g in both same-sign groups and singleton nodes 1. The construction does not need c_2=0: solve the edge moments at exponents 1,2,3, and the two displayed recurrences supply exponents 4,5. The opposite-delta singleton supplies the axis. For b=0,2,3 use exactly the manuscript's selected column sets after replacing t^r modulo the old cubic with t^r modulo this new g. The same simultaneous reflection supplies the other rows. The ordinary Lagrange/Vandermonde amplitudes and original raw-weight formula then prove the literal Fourier identity with eight permitted banks.

Here is a short good-reduction certificate for all new guards. At (43,q−4), q has order seven and 29 is a unit. The cubic is t³+18t²+9t+42. Its constant coefficient is 42, δ has residue 10, and h(q) has residue 29. Thus all three roots are distinct and nonzero. The selected b=0,2,3 row minors have residues 27,19,3, respectively, all nonzero. The exact cyclotomic vectors of these minors are in N7_QUADRATIC_SPECIALIZATION.json; the two recurrence identities are characteristic-zero equalities.

The splitting field is K(√δ), so its degree is at most two. It is exactly two for this specialization: at the equally valid prime (43,q−16), δ has residue 12, a nonsquare in F_43. If δ were a square in K, its unit residue at that prime would be a square. Hence this particular eight-bank construction is not K-only. This does not exclude another K-only eight-bank construction.

This is a new cubic in the full recurrence pencil, not a claim that the frozen depressed cubic has a smaller splitting field. The frozen witness remains intact.

## 2. Fourteen order-eleven banks with extension degree at most 24

This section is the canonical degree-24 construction. Its forced roots are the rational integers 7 and 8. A separate exploratory q,q²-root computation in this folder is not this construction and is not used here.

Use the accepted N11 parametric family g_(λ,μ), its edge moments s_0,…,s_8 and u_0,…,u_6, and the four selected row minors D_0,D_3,D_4,D_5. Since the coefficients depend affinely on the parameters, write

g_(λ,μ)(t)=g_0(t)+λ g_λ(t)+μ g_μ(t),

where g_0 is the frozen base sextic, g_λ=g_(1,0)−g_0, and g_μ=g_(0,1)−g_0. These three explicit K-polynomials are specified by the accepted fixed 4×4 moment solve. Define the exact parameter pair by

[λ,μ]^t = − [[g_λ(7),g_μ(7)],[g_λ(8),g_μ(8)]]^−1 [g_0(7),g_0(8)]^t.

The two-by-two matrix is invertible, as certified below. The root constraints hold by construction, so

g_(λ,μ)(t)=(t−7)(t−8)h_4(t),   h_4∈K[t] monic of degree four.

N11_RATIONAL_ROOT_SPECIALIZATION.json records all exact rational-basis coefficients of λ,μ,g and h_4. Direct exact arithmetic verifies both root equations; membership in the accepted affine family gives all four moment recurrences identically.

At the accepted prime (23,q−2), the affine derivative coefficients, in ascending powers of t, are

g_λ=(11,22,12,16,1,0,0),
g_μ=(5,2,21,20,0,1,0).

The two-by-two root matrix reduces to [[17,13],[18,6]], with determinant 6. The right side reduces to zero because 7 and 8 are roots of the frozen reduced sextic. Consequently λ and μ belong to the local ring and reduce to zero. All original nonzero exceptional factors therefore survive unchanged:

gbar(t)=t^6+4t³+2t²+21t+12,
c_0=12,
Res(gbar,gbar′)=6,
(D_0,D_3,D_4,D_5)=(5,3,18,8).

Their product has residue 17≠0. This exact parameter pair is thus in the accepted admissible family, so the fourteen-bank theorem applies without modifying any row formula or orientation count. All roots are distinct/nonzero, and the phase-weight and resolvent guards are legal.

Since two roots are already in K, the complete splitting field L is the splitting field of h_4 over K and satisfies [L:K]≤4!=24. The quartic reduces to

hbar_4(t)=t^4+15t³+8t²+20t+15,

which is irreducible over F_23. Therefore h_4 is irreducible over K, [K(x):K]=4 for each of its roots, and 4 divides [L:K]≤24. No exact degree24 claim is made. This particular specialization is genuinely not K-only, while the question of another fourteen-bank realization entirely over K remains open.

The reduction is used only to certify nonzero denominators, nonzero exceptional factors, and irreducibility of a characteristic-zero polynomial already defined by exact K equations. No finite-field point is assumed to lift to K.

## 3. Primary-source and interpretation boundary

These are explicit arithmetic refinements of particular signed-bank recipes. Forcing known field roots reduces the elementary factorial splitting-field bound. No trace operation, Galois-averaged block, or orbit is counted as one permitted bank. All field-dependent weights are obtained from actual individual roots by the accepted original formulas.

The general field-sensitive Sylvester principle and its splitting-field interpretation are classical. In particular, Reznick's “On the length of binary forms,” Theorem 4.10, gives a root-parameter construction of split Sylvester forms over K; the 2N−4 theorem's one-recurrence root-coordinate mechanism should be understood alongside that result. The separate contribution under examination here is the explicit Fourier signed-bank realization, its cross-orientation compatibility, and these displayed specializations, not a new general theorem about rational roots or field descent.

Primary sources inspected:
- https://reznick.web.illinois.edu/hdfv3.pdf, Theorem 4.10 and Corollary 2.2.
- https://arxiv.org/pdf/1610.09065, Theorem 1.1 and Section 3.

Fresh controls are in this new packet. No frozen predecessor program was executed or imported. Independent review is required for this addendum separately from the already reviewed all-order bound.
