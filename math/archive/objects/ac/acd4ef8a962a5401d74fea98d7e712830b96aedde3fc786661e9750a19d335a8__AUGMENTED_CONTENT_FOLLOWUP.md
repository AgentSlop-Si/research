# Two further augmented-content families and a residue-component obstruction

10 October 2026 UTC. This is a separate follow-up to the accepted `composite_guard/final_v1` theorem package. It does not modify that freeze. All project programs were treated as inert inputs; the controls here were newly authored. Mathematical scope and external publication priority remain separate; priority is provisional.

## 1. Result and precise limits

The two requested exact augmented contents are

- c_15^+ = 3^12 · 5^9 = 1,037,970,703,125.
- c_19^+ = 19^11 = 116,490,258,898,219.

Consequently the accepted augmented-content criterion proves that

H_((15p−1)/2)(z;ζ_(15p)) is squarefree over characteristic zero for every prime p ≡ 1 (mod 4), p ≠ 5,

and

H_((19p−1)/2)(z;ζ_(19p)) is squarefree over characteristic zero for every prime p ≡ 1 (mod 4).

These statements hold for every primitive root in the indicated order. Both are fixed-base, all-p families, rather than finite target-order tests. The first is a genuinely composite lower base, and its exclusion p=5 is essential to the applicability of this proof: the accepted unramified bridge assumes p∤s. No claim of nonsimplicity at the excluded order 75 is made.

The root −1 is present and simple. Its forbidden resonance in the scalar-bank application remains, so these d ≡ 3 (mod 4) families do not lower the m+1 bank minimum.

The prospective general no-extra-prime-content lemma has **not** been proved or disproved. The exact bases and the bounded independent finite-field countertest are consistent with it. There is a concrete counterexample to the stronger assertion that every unramified residue component is good: s=63,p=5 has a bad resonance component and a good augmented component. This also defeats a norm-unit replacement for the existential content condition. It is not a counterexample to characteristic-zero simplicity or to the actual content lemma.

## 2. Definitions and exact certificate convention

For s=4r+3, b=(s−1)/2, ω primitive of order s, put

H_n(z;q)=Σ_(k=0)^n [n choose k]_q z^k,
U_s=H_b(z;ω)/(z+1),
g_s=U_s(−1),
v_s=∏_(j=1)^r(1−ω^(2j)) ∏_(j=0)^(b−1)(1−ω^(2j+1)),
Γ_s=Disc_z(U_s) Res_z(z^s+1,U_s),
δ_s=2g_s−v_s,
A_s=Γ_sΓ_s^ιδ_s,
where ι(ω)=ω^−1. The discriminant uses the ordinary z derivative. Disc(1)=1. The reduced-coordinate content is the positive gcd of the coefficients of A_s in the basis 1,q,…,q^(φ(s)−1), after reduction modulo Φ_s(q).

`EXACT_CONTENT_S15.json` and `EXACT_CONTENT_S19.json` contain complete coefficient arrays for Φ_s, U_s, its reciprocal-polynomial transform P_s, g_s, v_s, δ_s, Disc(U_s), the resultant, Γ_s, Γ_sΓ_s^ι and A_s. Every cyclotomic-element q-array is in ascending powers and padded to φ(s); Φ_s itself has φ(s)+1 coefficients; U and P have an outer ascending-power array in z and t respectively. The integer contents and their factorizations are also included. No floating-point arithmetic occurs.

The checked contents are:

s=15:
cont(Disc U)=1;
cont(Res(z^15+1,U))=3^6·5^3;
cont(Γ)=3^6·5^4;
cont(ΓΓ^ι)=cont(A)=3^12·5^9;
cont(δ)=1.

s=19:
cont(Disc U)=19;
cont(Res(z^19+1,U))=19^4;
cont(Γ)=19^5;
cont(ΓΓ^ι)=cont(A)=19^11;
cont(δ)=1.

Contents do not multiply mechanically: the s=15 and s=19 rows explicitly show extra reduced-product valuations. These are not unreduced polynomial contents.

### Proof of the two families

The exact arrays prove c_s^+≠0 with the asserted prime support. If s=15 and p≡1 (mod4), p≠5, then p∤s c_s^+. If s=19 and p≡1 (mod4), then p≠19 automatically, hence again p∤s c_s^+. Apply Section 2 of the accepted `COMPOSITE_GUARD_EXTENSION.md`. That theorem selects one common residue factor where Γ, Γ^ι and δ are all nonzero, applies its parity-complete Hermite inverse-pairing lemma, and uses exact cyclotomic division before reduction. Its hypotheses, including the characteristic-zero residual guards, follow from that same nonvanishing. ∎

The independently reconstructed s=3,7,11 controls also reproduce c_s^+=1,7²,11⁵ coefficient for coefficient. A separate reviewer has reconstructed all five bases by Gaussian-binomial subset enumeration and direct determinants; its receipt records that independent comparison.

## 3. Structural reduction of the residual guards

This section supplies a general exact reduction, not a uniform support theorem.

U_s is monic reciprocal of degree 2r, so there is a unique monic polynomial P_s(t) of degree r such that

U_s(z)=z^r P_s(z+z^−1).

Let S_0(t)=2, S_1(t)=t and S_(j+1)=tS_j−S_(j−1). Thus S_j(z+z^−1)=z^j+z^−j. For odd s=2b+1, define C_s by C_1=1, C_3=t−1 and C_(s+2)=tC_s−C_(s−2). Then

z^s+1=(z+1)z^b C_s(z+z^−1),
S_s(t)+2=(t+2)C_s(t)^2.

For every monic reciprocal U=z^rP(z+z^−1), polynomial identities over the integers give

Disc_z U=P(2)P(−2)(Disc_t P)^2,
Res_z(U,z^s+1)=Res_t(P,S_s+2)=(-1)^r P(−2) Res_t(P,C_s)^2.

Hence

Γ_s=(-1)^r P_s(2)P_s(−2)^2 [Disc(P_s) Res(P_s,C_s)]^2.

To verify the identities, first work with generic distinct roots t_i of P and the inverse pairs λ_i,λ_i^−1 satisfying λ_i+λ_i^−1=t_i. The within-pair squared difference is t_i²−4, and the squared cross-pair contribution is (t_i−t_j)^4. This yields the discriminant identity. The paired resultant contribution is (λ_i^s+1)(λ_i^−s+1)=S_s(t_i)+2=(t_i+2)C_s(t_i)^2. Both sides are integral polynomial expressions in the coefficients, so these generic identities extend to all coefficients and all characteristics by specialization.

Thus at an odd-characteristic residue component the lower guard is exactly the simultaneous nonvanishing of P_s(2), P_s(−2), Disc(P_s) and Res(P_s,C_s). This cuts the determinant degree from 2r to r but does not show that some component passes both inverse guards and δ. In particular, orthogonality or positivity in a complex embedding cannot be transferred into these finite fields.

The exact s=15 and s=19 calculations independently check their full-degree discriminant/resultant determinants against these half-degree formulas.

## 4. Exact adverse component: s=63, p=5

Work over F_5. Both

f(q)=q^6+q^4+3q^3+q²+1,
h(q)=q^6+q^5+2q^4+2q²+q+1

are irreducible factors of Φ_63. For a root θ of either one, the certificate checks θ^63=1, θ^21≠1 and θ^9≠1, hence θ has exact order 63. Irreducibility is checked by θ^(5^6)=θ and gcd(f,q^25−q)=gcd(f,q^125−q)=1, and likewise for h.

In K_f=F_5[q]/(f), put θ=q mod f and U=H_31(z;θ)/(z+1). The exact controls give

δ=4θ+θ³ ≠ 0,
gcd(U,U′)=1,
gcd(U,z^63+1)=z²+a z+1,
a=3+2θ+2θ²+4θ³+4θ⁴+4θ⁵.

For the inverse parameter θ^−1, the derivative gcd again has degree zero and the resonance gcd again has degree two. Thus Γ and Γ^ι vanish in this component, even though the residual polynomial is squarefree and the Hermite exceptional parameter is absent.

In K_h=F_5[q]/(h), the controls instead give

δ=4+4θ+3θ⁴+2θ⁵ ≠ 0,
gcd(U,U′)=gcd(U,z^63+1)=1,
gcd(U^ι,(U^ι)′)=gcd(U^ι,z^63+1)=1.

Consequently A_63 is nonzero in K_h, so 5∤c_63^+. The K_f result shows that the norm of Γ_63 is divisible by 5. Both facts hold simultaneously. A bad component therefore cannot by itself refute the content criterion; requiring Γ to be a unit in every component is unnecessarily strong.

`S63_P5_COMPONENT_CERTIFICATE.json` includes complete U and U^ι coefficient arrays in both fields, their δ values, and monic resonance gcds. This control uses a second fresh implementation: q-Pascal coefficients plus polynomial Euclid, rather than the exact determinant/recurrence code.

## 5. Bounded countertest and remaining decisive lemma

`MODULAR_COMPONENT_TESTS.json` records 43 pairs drawn from s=3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63 and p=5,13,17, omitting p|s. For each pair the search stops as soon as a single factor passes both inverse residual guards and δ. Every pair passes. The only pair that needs a second factor in this ordered test is (63,5), documented above. This bounded test is evidence and an adverse-component control, not a proof for untested primes or bases. No further base census was used to claim a theorem.

The decisive unresolved lemma is still:

For every s≡3 (mod4) with Γ_s≠0, and every prime p≡1 (mod4) with p∤s, there is an irreducible factor f of Φ_s over F_p for which

P_s(2)P_s(−2)Disc(P_s)Res(P_s,C_s),
its q↦q^−1 counterpart, and δ_s

are all nonzero modulo f.

Equivalently p∤cont_s(Γ_sΓ_s^ιδ_s). The inverse-pair selection, not merely separate nonzero factors, is essential. The characteristic-zero nonvanishing of δ is already provided by the accepted sector lemma; the general residual Γ_s≠0 hypothesis and this finite-characteristic simultaneous-support assertion are distinct remaining issues. Repeated-prime target orders require a separate bridge and are not addressed here.

The present result supports keeping the no-extra-prime-content assertion as a plausible research target, but does not promote it to a theorem. No publication-priority claim is made for the reciprocal-polynomial identities or the inherited Hermite/cyclotomic machinery. New literature comparisons may change attribution without changing these exact arithmetic certificates.
