# Parity-complete inverse pairing and three composite half-order families

10 October 2026 UTC. This is a scoped mathematical extension, not an all-composite simplicity theorem or a priority claim. Source programs were not executed. Small controls in this directory were freshly authored.

## Result

For every prime p ≡ 1 (mod 4) and every s ∈ {3,7,11}, put d=sp. Then

H_((d−1)/2)(z;ζ_d)

is squarefree over characteristic zero for every primitive ζ_d. Therefore, for U_d=H_((d−1)/2)/(z+1), Disc(U_d)≠0. Together with the inherited uniform resonance theorem and half-order disk theorem, the previously guarded one-simple-overlap local expansion at lower order d is unconditional for every local index A≥1 in these three infinite families.

All these d are 3 modulo 4. The root −1 remains present and simple. For the scalar-bank application it remains a forbidden resonant node, so this result does not improve the m+1 bank minimum at these target orders.

The older source already covers p ≡ 3 (mod 4) for these bases, subject to its repeated-prime handling. The new quantified regime here is p ≡ 1 (mod 4). Such a p cannot divide 3,7,11, so the new family statement has no repeated-prime exception.

## 1. The complete finite-characteristic pairing lemma

Let p be an odd prime, A=(p−1)/2, and k any field of characteristic p. Write H=He_A for the monic probabilists' Hermite polynomial. Set

J(y;τ)=yH(y)−τH′(y).

Suppose τ,τ′∈k are nonzero and 1/τ+1/τ′=1. Then at least one of J(y;τ), J(y;τ′) is squarefree over the algebraic closure, with exactly one exceptional case:

p ≡ 1 (mod 4) and τ=τ′=2.

In that exceptional case both have a root of multiplicity three at zero.

### Proof

The recurrence and derivative identities are H_n=yH_(n−1)−(n−1)H_(n−2) and H_n′=nH_(n−1). Since A<p, consecutive H_A,H_(A−1) are coprime: a common root would descend through every nonzero recurrence coefficient to H_0=1. Thus H and H′ are coprime, and H cannot vanish at a root of J with τ≠0.

The Hermite equation H″−yH′+AH=0 gives, at a root of J,

J′(y;τ)=[1+Aτ+(1−τ)y²/τ]H(y).

Our parameter assumptions imply τ≠1 and τ′=τ/(τ−1). Since A=−1/2 in k, a multiple root must satisfy

y²=t(τ):=τ(τ−2)/[2(1−τ)],
t(τ′)=−t(τ).

Assume both polynomials have multiple roots and the first has a nonzero multiple root y. Choose i²=−1 in the algebraic closure. By parity, the second has a multiple root at iy: its possible squared value is −y², and roots of both parities occur in opposite pairs. Define V(y)=i^(−A)H(iy). The equations for H and V give

[H′V−HV′−yHV]′=−(2A+1)HV=0.

This polynomial has degree p, leading coefficient −1, and zero constant term, so in characteristic p

H′V−HV′−yHV=−y^p.

At the two supposed multiple roots H,V are nonzero, H′/H=y/τ and V′/V=−y/τ′. The left side therefore vanishes, while −y^p does not. Contradiction.

Any simultaneous failure must consequently have y=0. The formula for t and τ≠0,1 then forces τ=τ′=2. If A is odd, H′(0)≠0 and J(0;2)=−2H′(0)≠0, so failure is impossible. If A is even, H(0)≠0, J is odd, and J′(0;2)=(1+2A)H(0)=0. Thus zero is multiple. It has multiplicity exactly three: writing H=c_0+c_2 y²+c_4 y⁴+…, the differential equation gives c_2=−Ac_0/2 and c_4=A(A−2)c_0/24. Hence the y³ coefficient of yH−2H′ is A(1−2A)c_0/6=−c_0/6≠0 in k. Here p≡1 mod4 implies p≥5, so 6 is invertible. This proves the lemma. ∎

The cubic coefficient formula also covers A=2 with c_4=0. The Wronskian identity is an inherited elementary instance of established Hermite-Wronskian congruence theory; the new use is the exact exceptional parameter and its elimination in the previously excluded parity.

## 2. An augmented lower-content criterion

Fix s=4r+3, b=(s−1)/2=2r+1. Work in O_s=Z[ω], ω primitive of order s. Define the following integral elements, with Disc(1)=1:

U_s(z)=H_b(z;ω)/(z+1),
g_s=U_s(−1),
v_s=(ω²;ω²)_r (ω;ω²)_b,
Γ_s=Disc_z(U_s) Res_z(z^s+1,U_s),
δ_s=2g_s−v_s.

Write ι for ω↦ω⁻¹ and let

c_s^+=cont_s(Γ_s Γ_s^ι δ_s).

Equivalently this is the positive gcd of the coefficients of the unique remainder modulo Φ_s of the indicated product; set content zero for the zero element. This is reduced-coordinate content, not content of an unreduced product in Z[q].

### Theorem

If p≡1 mod4 is prime, p∤s, c_s^+≠0 and p∤c_s^+, then H_((sp−1)/2)(z;ζ_(sp)) is squarefree in characteristic zero.

### Proof

Since p∤s, O_s/pO_s is a product of finite fields. The content condition provides one factor, represented by a primitive s-th root ω̄, where

Γ_s(ω̄) Γ_s(ω̄⁻¹) δ_s(ω̄) ≠ 0.

Thus both inverse residual discriminants and resultants are nonzero in that same factor. The resultant contains the value U_s(−1), so both g_s and g_s^ι are units there. Every factor 1−ω̄^j appearing in v_s or v_s^ι is nonzero because 0<j<s, so v_s and v_s^ι are units too.

The inherited half-order identity

g_s v_s^ι+g_s^ι v_s=v_s v_s^ι

is an integral identity, and reduces in this factor. Therefore τ=v_s/g_s and τ′=v_s^ι/g_s^ι satisfy 1/τ+1/τ′=1. Nonvanishing of δ_s rules out τ=2, and hence also τ′=2. Section 1 supplies one of the two inverse roots where the Hermite cluster polynomial J_(A+1), A=(p−1)/2, has nonzero discriminant.

For clarity, the characteristic-zero local formula used here is the already proved one-simple-overlap formula from FINAL_THEOREMS.md, Theorem 2. Put n=As+b=(sp−1)/2 and L=sA(A−1)/2+A. Its nonzero coefficient is

C_ov=(−1)^(A(s−1)/2) s^[sA(A+1)/2+A] P_A^(s−1)
      · Disc(J_(A+1)) Disc(U_s) Res(z^s+1,U_s)^(2A) g_s²,

where P_A=∏_(j=1)^A j^j. At the selected root every displayed factor is a p-unit: A<p, p∤s, and the remaining factors were selected above.

The same nonvanishing also verifies the characteristic-zero guards. The exact local order L gives the integral factorization

D_n(q)=Φ_s(q)^L E(q), E∈Z[q],
E(ω)=Q_s(ω)^L C_ov, Q_s(q)=(q^s−1)/Φ_s(q).

Here Q_s(ω) is a p-unit because q^s−1 is squarefree modulo p. Hence E is nonzero in the selected residue factor. If D_n(ζ_(sp)) were zero, irreducibility would force Φ_(sp)|E. But

Φ_(sp)(q) ≡ Φ_s(q)^(p−1) (mod p),

forcing E to vanish in every lower residue factor, a contradiction. This uses exact cyclotomic division before reduction and never assumes L<p−1. ∎

The single augmented product is important. Different good components for Γ_s, Γ_s^ι and δ_s separately do not suffice. A nonzero norm alone also does not establish the content hypothesis.

## 3. Exact lower-base certificates

Fresh recurrence/resultant computations in fresh_augmented_content.py produce the complete coefficient remainders in FRESH_AUGMENTED_CONTENT.json. They give

s=3: c_s^+=1.
s=7: c_s^+=49=7².
s=11: c_s^+=161051=11⁵.

These finite calculations concern degrees 0,2,4 in z; they are exact certificates for fixed constants in an all-p theorem, not a target-order census. The theorem therefore proves the three families in the opening result.

For s=3 everything is immediate by hand: U=1, g=1, v=1−ω, Γ=1 and δ=1+ω is a unit with norm 1.

For s=7,

Γ=490q⁵+735q⁴+588q³+154q²−259q−336,
δ=−2q⁴+q³−q+2,
rem_(Φ_7)(ΓΓ^ιδ)
 =−2151590q⁵−3491642q⁴−3011393q³−1075795q²+859803q+1340052.

Its coefficient gcd is 49. Notably Norm(δ)=1183=7·13²: at the unramified prime 13 some components have the exceptional parameter. The simultaneous augmented product nevertheless has content 49, so a different good component exists and p=13 is covered. This is a concrete reason to keep the existential-component criterion rather than imposing the stronger, unnecessary norm-unit condition.

An exact adverse component control at s=7,p=13 is recorded in FRESH_EXCEPTION_CONTROL.json. Over F_13,

Φ_7=(q²+3q+1)(q²+5q+1)(q²+6q+1),
gcd(Φ_7,ΓΓ^ι)=1,
gcd(Φ_7,δ)=q²+6q+1.

All three irreducible quadratic factors are inverse-stable. In the last one τ=τ′=2, so both cluster polynomials are singular despite good residual guards. The first two factors pass the augmented selection. Thus merely extending the old parity statement without its new exception would be false.

For s=11 the complete larger coefficients are recorded in the JSON. Dividing its augmented remainder by 11⁵ leaves coefficient gcd 1. No numerical approximation is used.

## 4. A characteristic-zero sector lemma for the new obstruction

For every s=4r+3, not just the three bases, δ_s is nonzero in characteristic zero. Moreover g_s≠0. This statement does not assert that Γ_s is nonzero.

Take the principal embedding ω=exp(2πi/s). Put a_j=(ω;ω²)_j/(ω²;ω²)_j. The inherited product identities give

g_s/v_s=(Σ_(j=0)^r a_j)/(ω;ω²)_b.

Each a_j has argument −jπ/s and positive modulus, because each sine in

(1−ω^(2k+1))/(1−ω^(2k+2))
 = exp(−iπ/s) sin((2k+1)π/s)/sin((2k+2)π/s)

is positive for the relevant k. Also M=(ω;ω²)_b has argument −bπ/(2s), modulo 2π: summing the phases of its b factors gives −bπ/2+πb²/s=−bπ/(2s), since 2b=s−1.

Consequently every summand a_j/M has argument

(b/2−j)π/s ∈ [π/(2s), bπ/(2s)] ⊂ (0,π/4).

Their sum has strictly positive imaginary and real parts. Thus g_s/v_s is nonzero and cannot equal 1/2, proving g_s≠0 and δ_s≠0. The inverse identity further gives Re(g_s/v_s)=1/2. Because nonzero algebraic elements stay nonzero under Galois embeddings, the nonvanishing holds at every primitive ω.

As a result, whenever the residual squarefreeness/resonance guards hold at a fixed s, c_s^+ is nonzero and only finitely many primes p≡1 mod4 are excluded by the augmented criterion. This complements the existing p≡3 mod4 statement but does not identify the excluded primes uniformly in s.

## 5. What remains open and which shortcuts fail

1. All composite d≡3 mod4 are still not covered. In particular the proof does not settle arbitrary repeated-prime orders or composite lower orders whose Γ_s is not known nonzero.
2. The precise next arithmetic lemma is simultaneous nonvanishing of Γ_sΓ_s^ιδ_s in at least one factor of O_s/pO_s for every p≡1 mod4 with p∤s, assuming the lower characteristic-zero guards. Equivalently: no such p divides c_s^+. A pure-support theorem for the augmented content would remove this last prime-selection exclusion for that bridge. The three fixed-base certificates do not prove it.
3. If p already divides s, the argument using squarefree q^s−1 modulo p and unit Q_s fails. A repeated-prime theorem needs new analysis.
4. The ordinary derivative cannot be replaced by the q-derivative. For n<ord(q), the identities H_n(qz)−H_n(z)=(q^n−1)zH_(n−1)(z) and consecutive coprimality show H_n(z),H_n(qz) have no common root. This does not imply H_n,H_n′ are coprime. At q=−3, H_2=(z−1)² while its q-shift shares no root. This is an exact counterexample to that inference, not to the root-of-unity conjecture.
5. Complex formal orthogonality does not imply simple zeros. Self-reciprocity alone likewise permits repeated reciprocal pairs. The root-of-unity continuous-q-Hermite factorization concerns terminal degrees and does not supply the half-degree assertion.

## 6. Primary-literature and provenance boundary

The following primary sources were reread through authorized public routes:

- Spiridonov–Zhedanov, *Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity*, arXiv:q-alg/9605034v2, pp.1–2, explicitly distinguishes positive real recurrence from complex coefficients and requires a separate simplicity check. Its root-of-unity terminal polynomial formulas do not remove the present half-order guard. https://arxiv.org/pdf/q-alg/9605034
- Grosu–Grosu, *The irreducibility of some Wronskian Hermite polynomials*, arXiv:2007.00065v1, Theorem 8 and its surrounding definitions, supplies established Hermite-Wronskian congruence theory. The elementary identity used here should not be advertised as a newly invented general congruence. https://arxiv.org/pdf/2007.00065v1
- Gómez-Ullate–Grandati–Milson, arXiv:1612.05514, supplies the existing pseudo-Wronskian equivalence background cited by the earlier package. https://arxiv.org/pdf/1612.05514
- Cigler, *Elementary observations on Rogers–Szegö polynomials*, arXiv:1602.07850, provides established special-value/q-product background. https://arxiv.org/pdf/1602.07850

The project-specific extension is the parity-complete exception analysis, its augmented residue criterion, and the three p≡1 mod4 family corollaries. No exhaustive literature-priority claim is made. Lubinsky–Saff 1987 and Zhedanov 1997 full-text comparison remains unclosed. The denied Vanderbilt route was not revisited.

Project inputs and exact hashes are recorded in SOURCE_PROVENANCE.json. They were read as inert text/data. No source code was executed, imported, compiled or AST-parsed.
