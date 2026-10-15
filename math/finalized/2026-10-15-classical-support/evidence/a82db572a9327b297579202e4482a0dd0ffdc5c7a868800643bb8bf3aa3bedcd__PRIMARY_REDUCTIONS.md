# Exact reductions to established polynomial identities

This file gives the actual substitutions supporting the priority assessment. They are derivations made in this assessment from identified primary theorems, rather than claims that the cited papers discuss the project's Rogers–Szegő application. All Hermite polynomials `He_n` are monic probabilists' polynomials. The finite checks in `NORMALIZATION_CHECKS.json` guard normalization; the arguments below are not inferred from them.

## 1 The shared polynomial is a quasi Laguerre pullback

Put `J_(A+1)(y;τ)=He_(A+1)(y)+A(1−τ)He_(A−1)(y)` and `t=y²/2`.

For `A=2m−1`, the classical even Hermite–Laguerre relation gives

`J_(2m)(y;τ)=2^m P_m(y²/2)`,

`P_m(t)=(-1)^m m![L_m^(-1/2)(t)+c L_(m−1)^(-1/2)(t)]`,

`c=(2m−1)(τ−1)/(2m)`.

For `A=2m`, the odd relation gives

`J_(2m+1)(y;τ)=y 2^m P_m(y²/2)`,

`P_m(t)=(-1)^m m![L_m^(1/2)(t)+(τ−1)L_(m−1)^(1/2)(t)]`.

In both cases `P_m` is monic. Thus the gap-two Hermite combination becomes an adjacent-degree quasi-Laguerre combination. This is the important comparison: the adjacent-degree quasi-Hermite formula alone would concern a different parity pattern.

Masanori Sawa and Yukihiro Uchida, *Discriminants of classical quasi-orthogonal polynomials, with combinatorial and number-theoretic applications*, arXiv:1802.00605v1, Theorem 4.8 and (4.13), gives the ordinary discriminant of `f=L_m^(α)+cL_(m−1)^(α)`. With

`ξ=[m c²+(2m+α)c+m+α]/c`,

it is

`Disc(f)=[(-c)^m f(ξ)/(m+α+mc)] × ∏_(k=1)^m k^(k−2m+3) × ∏_(k=1)^(m−1)(k+α)^(k−1)`.

The apparent singularities are interpreted by the polynomial identity after cancellation. Their order-one quasi-Hermite result is Theorem 4.10. [Primary PDF](https://arxiv.org/pdf/1802.00605v1)

Here is the remaining discriminant conversion, derived directly from pairs of roots in this assessment. If `P` is monic of degree `m`, then

`Disc_y[2^mP(y²/2)]=(-1)^m 2^(2m²+m) P(0) Disc_t(P)²`,

`Disc_y[y2^mP(y²/2)]=(-1)^m 2^(2m²+3m) P(0)³ Disc_t(P)²`.

Indeed, the roots of the even polynomial occur in pairs `±√(2r_i)`. Within-pair squared differences give `∏8r_i`; the differences between two pairs give `16(r_i−r_j)^4`. For the odd polynomial, the additional zero contributes the square of the even polynomial's constant term. Consequently the standalone `S_A(τ)=Disc J_(A+1)` is explicitly covered by an established ordinary-discriminant theorem plus an elementary quadratic-pullback identity. Its appearance as a factor of the Rogers–Szegő local discriminant is a separate question.

## 2 The reciprocal parameter becomes ordinary inversion

Now let `p≡3 mod4`, `A=(p−1)/2`, and `m=(p+1)/4`. In characteristic `p`, `m=1/4` and the coefficient above simplifies to `c=1−τ`. If `τ′=τ/(τ−1)`, then

`c′=1−τ′=1/c`.

At `α=−1/2`, the Sawa–Uchida evaluation point is

`ξ(c)=(c−c^−1)/4=τ(τ−2)/[4(1−τ)]`,

and `ξ(c′)=−ξ(c)`. All constant product factors in the discriminant formula are nonzero: `m<p`, `k−1/2` cannot vanish for `1≤k<m`, and `m+α+mc=−τ/4`. The hypotheses make `c≠0` and `τ≠0`. Also `P(0)≠0`, equivalently `J(0;τ)≠0`.

Therefore the paired-good lemma is equivalently a claim that the two quasi-Laguerre discriminants at `c` and `1/c` do not both vanish in this characteristic. The possible repeated-root location in the project is exactly twice `ξ(c)` after `t=y²/2`. This locates the lemma precisely in existing quasi-orthogonal discriminant theory; it does not by itself prove the inversion nonvanishing claim.

## 3 The finite characteristic Wronskian is a known hook congruence

For any integer `A≥0`, define

`U(y)=He_A(y)`, `V(y)=i^(−A)He_A(iy)`,

`K_A(y)=yUV−U′V+UV′`.

Both `U` and `V` are monic integral polynomials, since the powers of `i` cancel. The source identity used by the overlap proof is `K_A(y)=y^p` in characteristic `p=2A+1`.

An exact characteristic-zero identification is

`K_A(y)=He_λ(y)`, `λ=(A+1,1^A)`,

where

`He_λ=Wr[He_1,He_2,…,He_A,He_(2A+1)]/Δ(1,2,…,A,2A+1)`.

The determinant on the right is the normalized Wronskian for the displayed hook partition.

### Source theorem and specialization

Gómez-Ullate, Grandati and Milson, *Durfee rectangles and pseudo-Wronskian equivalences for Hermite polynomials*, arXiv:1612.05514, Definition 3.1, Proposition 3.1 (12), and Theorem 3.1 (15), identifies the determinants associated to translated Maya diagrams up to explicit nonzero constants. [Primary PDF](https://arxiv.org/pdf/1612.05514)

To specialize it, take a Maya diagram with every negative position occupied except `−A−1`, and with the single nonnegative occupied position `A`. Its Frobenius data have one conjugate index `A` and one ordinary index `A`. Its two-function pseudo-Wronskian in the source's physicists' normalization is

`exp(−x²) Wr[exp(x²) H̃_A(x),H_A(x)]`, `H̃_A(x)=i^(−A)H_A(ix)`.

After `y=√2 x` this is a nonzero scalar times `U′V−UV′−yUV=−K_A`. Translating the diagram by `A+1` leaves all negative positions occupied and the positive set `{1,…,A,2A+1}`. The source theorem thus identifies it with the ordinary Wronskian displayed above up to a scalar. Both `K_A` and the Vandermonde-normalized Wronskian are monic, which fixes that scalar and proves the identity exactly.

Codruţ Grosu and Corina Grosu, *The irreducibility of some Wronskian Hermite polynomials*, arXiv:2007.00065v1, Definition 1 and Theorem 8 (proof in §5), gives

`He_λ(y) ≡ y^(|λ|−|μ|) He_μ(y) mod m`

when `m` is odd and coprime to the Vandermonde of the degree sequence; `μ` has the reduced degree sequence modulo `m`. Its Theorem 31 recalls and proves the underlying Carlitz congruence. [Primary PDF](https://arxiv.org/pdf/2007.00065v1)

For the hook above and `m=p=2A+1` prime, all pairwise degree differences are nonzero modulo `p`. Reducing and sorting the degree sequence yields `{0,1,…,A}`, the zero partition. Its normalized Wronskian is 1. Hence the cited theorem gives

`K_A(y) ≡ y^p mod p`,

exactly the project's signed Wronskian identity. This works for every odd prime; the restriction `p≡3 mod4` enters only when excluding the zero-root obstruction in the subsequent paired-good argument.

This is a substantive antecedent, not merely a similar title. It means that the Wronskian identity should not be advertised as a new general prime-characteristic identity. The short differential-equation proof in the project remains preferable for exposition; it independently derives a special case of established mathematics.

## 4 What remains in the paired good argument

At a multiple root, the project reduces `J′=0` to `y²=2ξ(c)`. If both parameters were bad, the second root can be chosen as `iy`. The two logarithmic derivatives would then make `K_A(y)=0`. The hook congruence gives `K_A(y)=y^p`; nonvanishing of `J(0;τ)` excludes `y=0`. Thus the paired-good conclusion is a short corollary of the above established identities and this elementary root argument.

No inspected primary theorem was found that states this exact reciprocal-parameter nonvanishing lemma or couples it to the half-degree Rogers–Szegő residue parameters. It remains a possible new application/combination. That is narrower and more defensible than claiming a new polynomial family or a new Wronskian congruence.

## 5 The arithmetic content conversion is standard

If an algebraic integer `B=Φ_s(ζ_(sp))^L E(ζ_(sp))` has `E` integral at every prime above `p` and a unit at at least one, then the minimum prime-ideal valuation of `B` is `L`. When `p∤s`, ramification index is `p−1`, so the largest rational power `p^k` dividing `B` has `k=floor(L/(p−1))`. Its coordinates in the cyclotomic integral basis have exactly this content exponent.

Sharifi's *Algebraic Number Theory*, Lemma 3.1.13 and Propositions 3.1.20–3.1.21, supply respectively the prime-power uniformizer, full ring of integers and general cyclotomic ramification. [Author notes](https://math.ucla.edu/~sharifi/notes/algnum-ch03.html)

For the project's element, the nontrivial input is the exact local order `L=3sA²/2` and the existence of one unit leading coefficient; the floor formula then follows. Thus `floor(3s(p−1)/8)` is a specific conditional consequence of the local Rogers–Szegő formulas. No new general content or ramification principle is required. This distinction leaves room for a new useful application without overclaiming its theoretical depth.
