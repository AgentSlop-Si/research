# Local Rogers–Szegő discriminants, reduced-coordinate contents, and legal scalar banks

Research manuscript draft, 10 October 2026. Mathematical results are separated from publication-priority claims. The local formulas and bank classification below consolidate the supplied independently audited work. The disk theorem and half-order overlap guard removal in Theorems 2A–2B, and the separate content formulas and uniform carry law in Theorem 4, are newly derived in this pass. Worldwide novelty is not established.

## 1. Definitions and the exact scope

Write

H_n(z;q) = Σ_{k=0}^n [n choose k]_q z^k,
D_n(q) = Disc_z H_n(z;q),
R_N(q) = Res_z(z^N+1,H_{(N−1)/2}(z;q)).

Discriminants use the ordinary z derivative. All H_n are monic. Set Disc(1)=Disc(linear)=1. The recurrence is

H_0=1, H_1=1+z,
H_n=(1+z)H_{n−1}+(q^{n−1}−1)zH_{n−2}.

For odd N, put O_N=Z[ζ_N]. If a∈O_N is nonzero, define its **reduced-coordinate content** cont_N(a) as the positive gcd of its coordinates in the integral basis 1,ζ_N,…,ζ_N^{φ(N)−1}. Equivalently, for f∈Z[q], it is the coefficient content of the unique remainder of f modulo Φ_N. This is also max{k∈Z_{>0}:a∈kO_N}.

Define

d_N=cont_N(D_{(N−1)/2}(ζ_N)),
r_N=cont_N(R_N(ζ_N)),
c_N=cont_N(D_{(N−1)/2}(ζ_N)R_N(ζ_N)),

when the elements are nonzero; set the corresponding content to zero for the zero element. Put c_1=1. The operation cont_N is not the ordinary content of an unreduced polynomial in Z[q]. In particular Gauss's lemma does not assert c_N=d_N r_N. It is essential to reduce the product modulo Φ_N before taking c_N.

The bank application fixes one natural N-cycle P and permits scalar coefficients only. Branch-dependent diagonal endpoints, independently routed cycles, higher-order resolvents, and arbitrary matrix inverses are outside this theorem.

## 2. The fixed-root local theorem

Let d be odd, ω primitive of order d, n=Ad+b with A≥1 and 0≤b<d. Set F=z^d+1, G=H_b(z;ω), P_A=∏_{j=1}^A j^j and q(ε)=ω(1+ε²)^{1/d}. Thus q(ε)^d−1=ε² exactly.

### Theorem 1: separated clusters

Assume Disc(G)Res(F,G)≠0. For each α^d=−1,

H_n(α+εx;q(ε))
= ε^A (−1)^A d^{A/2}G(α) He_A(√d x/α)+O(ε^{A+1}).

Here He_A is the monic probabilists' Hermite polynomial. Put K=dA(A−1)/2. Then

D_n(q(ε))=ε^{2K}(C_sep+O(ε²)),
C_sep=(−1)^{A(d−1)/2}d^{dA(A+1)/2}P_A^d Disc(G)Res(F,G)^{2A}.

Consequently ord_{Φ_d}D_n=K. Apparent square roots cancel coefficientwise.

### Proof

The classical q-Lucas identity gives H_n(z;ω)=F(z)^A G(z). To obtain the splitting coefficient, use the formal generating function

Σ_{n≥0} H_n(z;q)t^n/(q;q)_n
=exp(Σ_{k≥1}(1+z^k)t^k/[k(1−q^k)]).

This follows from the q-exponential equation E(qt)=(1−t)E(t); it requires no convergence argument. Separate the logarithm into d-divisible and nondivisible k and put u=t^d. At z=α+εx the first two singular logarithmic terms are xu/(αε)−u²/(2dε²). Terms of u-degree l≥3 have pole order at most two, strictly less than l. Thus the ε^{−A} term in the u^A coefficient is d^{−A/2}He_A(√d x/α)/A!. The regular t^b coefficient is G(α)/(ω;ω)_b. Finally

(q(ε);q(ε))_n=(−1)^A A! d^A(ω;ω)_b ε^{2A}(1+O(ε²)).

Multiplication proves the local formula. Its Hermite roots lift to A formal branches α+εαh_j/√d+O(ε²). Disc He_A=P_A follows from He_A′=AHe_{A−1} and the recurrence. The d within-cluster products give ε^{2K}d^{−K}P_A^d; between clusters they give Disc(F)^{A²}; residual roots give Disc(G)Res(F,G)^{2A}. Since Disc(F)=(−1)^{(d−1)/2}d^d, the displayed coefficient follows. Its nonvanishing proves the exact order. Evenness in ε gives the O(ε²) normalized remainder. ∎

### Theorem 2: one simple shared residual root

Let d≥3, b odd, G=(z+1)U and g=U(−1). Define

W=(ω;ω)_b/(ω²;ω²)_{(b+d)/2},
τ=dW/g,
J_{A+1}(y;τ)=He_{A+1}(y)+A(1−τ)He_{A−1}(y).

Suppose Disc(U)Res(F,U)Disc(J_{A+1})≠0. This implies g≠0. Then

H_n(−1+εx;q(ε))
=ε^{A+1}(−1)^{A+1}d^{(A−1)/2}gJ_{A+1}(−√d x;τ)+O(ε^{A+2}).

Put L=dA(A−1)/2+A. Then

D_n(q(ε))=ε^{2L}(C_ov+O(ε²)),
C_ov=(−1)^{A(d−1)/2}d^{dA(A+1)/2+A}P_A^{d−1}
×Disc(J_{A+1})Disc(U)Res(F,U)^{2A}g².

Hence ord_{Φ_d}D_n=L.

### Proof

The same singular generating series applies at α=−1. This time the regular t^b coefficient vanishes at ε=0 and its linear term is εxg/(ω;ω)_b. Precisely one further regular coefficient contributes at leading order: at degree b+d it equals 1/(ω²;ω²)_{(b+d)/2}. Indeed at z=−1 the full logarithm has only even powers, and no positive even multiple of odd d is below 2d; b+d<2d. Terms b+jd with j≥2 start later. Multiplication by the factorial factor gives the asserted J combination.

There are A roots in each nonshared cluster and A+1 in the −1 cluster. The within-cluster squared differences contribute ε^{2L}d^{−L}P_A^{d−1}Disc(J). For F_0=F/(z+1), F_0(−1)=d and Disc(F_0)=(−1)^{(d−1)/2}d^{d−2}. Between nonshared clusters and the shared cluster, the product is (−1)^{A(d−1)/2}d^{dA²+2A}. Residual factors give Disc(U)Res(F,U)^{2A}g². Multiplication yields C_ov. ∎

The general-b overlap theorem retains its Disc(J) guard. For the half-order residual degree, the following new derivation removes it.

### Theorem 2A: an explicit disk free of nonreal multiple-root parameters

Let A≥1, H=He_A, and J(y;τ)=yH(y)−τH′(y). If a nonreal parameter τ makes J have a multiple root, then

|1−τ|²>(A+1)/A.

For real τ, the only multiple-root parameters are τ=0 when A is odd, and τ=−1/A when A is even. Consequently J is squarefree whenever τ≠0 and |1−τ|≤√((A+1)/A), in particular on |1−τ|=1.

#### Proof

The real zeros of H are simple and symmetric. For nonzero y away from these zeros, let z=y². Pairing opposite zeros gives the rational function

f(z)=H′(y)/(yH(y))=Σ_j w_j/(z−a_j),

where a_j are nonnegative real numbers: squares of positive Hermite zeros with weight w_j=2, together with a_j=0 of weight 1 if A is odd. Every weight is positive.

For τ≠0, a nonzero multiple root y of J cannot be a zero of H, since H and H′ are coprime. It satisfies f(z)=1/τ and f′(z)=0. The Hermite equation H″−yH′+AH=0, combined with J=J′=0, yields

1+Aτ+(1−τ)z/τ=0.

If τ=1 this reads 1+A=0, impossible; otherwise putting σ=1−τ gives

z=(2A+1)−Aσ−(A+1)/σ.

For nonreal τ, taking imaginary parts in f(z)=1/τ gives

Im z · Σ_j w_j/|z−a_j|² = Im τ/|τ|².

Thus Im z has the same nonzero sign as Im τ, which is the opposite sign of Im σ. On the other hand the displayed formula for z gives

Im z=Im σ [(A+1)/|σ|²−A].

The bracket must be negative, proving the strict bound.

If τ is real and nonzero, the imaginary-part identity makes z real. But f′(z)=−Σ_jw_j/(z−a_j)²<0, a contradiction. Thus no real nonzero parameter has a multiple root away from zero. At zero, if A is odd then H′(0)≠0 and J(0;τ)=−τH′(0), so zero is a root only for τ=0, where yH has a double zero. If A is even, H(0)≠0 and J′(0;τ)=(1+Aτ)H(0), giving exactly τ=−1/A; parity then makes the zero multiple. For τ=0 and A even, yH has only simple zeros. These exhaust the real cases and prove the disk statement. ∎

The radius bound is sufficient, not asserted sharp for a given A. Its proof is elementary classical orthogonal-polynomial machinery; its use to eliminate this RS guard is the new-to-corpus addition.

### Corollary 2B: half-order overlap needs only the residual guards

Let d≡3 mod4, b=(d−1)/2, A≥1, ω primitive of order d, U=H_b(z;ω)/(z+1). If

Disc(U)Res(z^d+1,U)≠0,

then every conclusion of Theorem 2 holds, without separately assuming Disc(J_{A+1})≠0.

#### Proof

The residual resultant ensures g=U(−1)≠0; W is nonzero. Write d=4r+3, Q=ω², m=2r+1, v=dW. Finite q-product cancellation gives

v=(Q;Q)_r(ω;Q)_m,
g=(Q;Q)_r Σ_{j=0}^r (ω;Q)_j/(Q;Q)_j.

The first identity completes the denominator of W to the full nontrivial-root product d; the second follows by differentiating the Rogers–Szegő recurrence at −1. Let a_j=(ω;Q)_j/(Q;Q)_j and M=(ω;Q)_m. Since ω=Q^{−m}, the finite q-binomial theorem yields Σ_{j=0}^m a_j=M. Under ι:ω↦ω^{−1}, direct product cancellation gives a_j^ι=ω^j a_j and a_{m−j}=(M/M^ι)a_j^ι. Pairing the two halves of the sum yields

gv^ι+g^ιv=vv^ι.

As τ=v/g and ι is complex conjugation, this becomes 1/τ+1/conj(τ)=1, equivalently |τ−1|=1. Theorem 2A proves Disc(J)≠0, so Theorem 2 applies. ∎

For example at d=3, U=1 and τ=1−ω. Thus all A≥1 have the exact order ord_{Φ_3}D_{3A+1}=3A(A−1)/2+A, with the nonzero leading coefficient in Theorem 2. This all-A conclusion no longer carries an unevaluated quasi-Hermite discriminant guard. It is not an all-composite squarefreeness theorem at q=ζ_N.

### Corollary 2C: all local indices over prime lower orders

For every prime d≡3 mod4, every primitive d-th root ω and every A≥1, put n=Ad+(d−1)/2. The overlap expansion, exact order L=dA(A−1)/2+A, and nonzero coefficient C_ov of Theorem 2 hold unconditionally.

More generally, for any d≡3 mod4 the only lower characteristic-zero condition needed in Corollary 2B is squarefreeness of H_{(d−1)/2}(z;ω).

#### Proof and exact dependency

The supplied uniform resonance theorem gives gcd(H_b,z^d+1)=z+1 and says that −1 is simple, for b=(d−1)/2 and every primitive ω. Therefore g≠0 and Res(F,U)≠0 automatically. The remaining condition Disc(U)≠0 is equivalent to squarefreeness of H_b.

For prime d, the latter follows from the q→1 Hermite degeneration: D_b(q)=(q−1)^{b(b−1)/2}E_b(q) with E_b∈Z[q] and E_b(1)=∏_{j=1}^b j^j. If D_b(ω)=0, then Φ_d divides E_b, implying d=Φ_d(1) divides that product, impossible since b<d. Apply Corollary 2B. ∎

This corollary combines the old resonance and prime-order simplicity arguments with the newly proved disk lemma. It is an unconditional two-parameter local formula for prime lower orders, not a uniform simplicity assertion for all composite target orders.

## 3. From a lower residue component to a larger cyclotomic order

### Theorem 3: separated arithmetic bridge

Let s≡1 mod4, p an odd prime, p∤s, and c_s≠0. If p∤c_s, then

D_{(sp−1)/2}(ζ_{sp})≠0.

### Proof

Set A=(p−1)/2, b=(s−1)/2, n=As+b. Since p∤s, O_s/pO_s is a product of fields. The canonical reduction of D_b Res(z^s+1,H_b) is not identically zero modulo p exactly when some component makes both factors nonzero. Fix such a prime 𝔭 over p. It supplies separated characteristic-zero guards and a p-unit leading coefficient C_sep, because A<p, p∤s and P_A is a p-unit.

Theorem 1 gives the exact integer factorization

D_n(q)=Φ_s(q)^K E_D(q), K=sA(A−1)/2, E_D∈Z[q].

Writing Q_s(q)=(q^s−1)/Φ_s(q), the quotient value is

E_D(ω)=Q_s(ω)^K C_sep.

It is nonzero modulo 𝔭; Q_s is a unit there since q^s−1 is squarefree modulo p. If D_n(ζ_{sp}) vanished, irreducibility would force Φ_{sp}|D_n and hence Φ_{sp}|E_D. But Φ_{sp}≡Φ_s^{p−1} modulo p, forcing E_D(ω)=0 in every residue component, a contradiction. ∎

This is exact cyclotomic division before reduction. It does not require K<p−1 and is not an informal inference from the first term of a p-adic series.

For the overlap alternative, s≡3 mod4, set U_s=H_{(s−1)/2}/(z+1), Γ_s=Disc(U_s)Res(z^s+1,U_s), and c_s^pair=content rem_{Φ_s}[Γ_s(q)Γ_s(q^{s−1})]. If p≡3 mod4 and p∤s c_s^pair, the same conclusion holds using Theorem 2. The extra ingredient is the identity 1/τ(ω)+1/τ(ω^{−1})=1 and the following finite-characteristic pairing: at A=(p−1)/2, at least one of the two J polynomials is squarefree. A direct proof uses U=He_A, V=i^{−A}He_A(iy) and

U′V−UV′−yUV=−y^p in characteristic p.

Simultaneous multiple roots would make the left side vanish at a nonzero y. The identity follows by differentiation and degree; nonzero y follows from A odd and J(0;τ)≠0. This Wronskian identity is also a special case of established hook-Wronskian congruences. Pairing is used only to select one good component, not to claim every component is good.

## 4. New sharpened arithmetic corollary: a carry after cyclotomic reduction

### Theorem 4: separate reduced-coordinate valuations and carry

Assume s≡1 mod4, p≡1 mod4 is prime, c_s≠0 and p∤s c_s. Let N=sp. Then d_N,r_N,c_N are nonzero and

v_p(d_N)=⌊s(p−3)/8⌋,
v_p(r_N)=⌊N/4⌋,
v_p(c_N)=⌊3s(p−1)/8⌋.

In particular

v_p(c_N)−v_p(d_N)−v_p(r_N)
=1 if p≡1 mod8, and 0 if p≡5 mod8.

This is a statement about integral-coordinate contents in O_N. It does not contradict polynomial-content multiplicativity in Z[q].

### Proof

Set A=(p−1)/2, which is even. The previous proof supplies one lower prime 𝔭 over p for which Disc G and Res(z^s+1,G) are both units. The exact factorization for D_n has exponent K=sA(A−1)/2 and quotient E_D unit at 𝔭.

Introduce the integer polynomial

J_N(q)=∏_{j=0}^{N−1}H_n(−q^j;q).

It is not generally the polynomial R_N(q); they agree at q=ζ_N. Along q(ε), −q^j=−ω^j+O(ε²). Theorem 1 and He_A(0)=(−1)^{A/2}(A−1)!! give

H_n(−q^j;q)=(q^s−1)^{A/2}κG(−ω^j)+O((q^s−1)^{A/2+1}),
κ=(−s)^{A/2}(A−1)!!.

Each leading coefficient is nonzero in characteristic zero. Exact monic division at all primitive s-th roots gives J_N=Φ_s^{NA/2}E_R with E_R∈Z[q]. Because each lower cluster root occurs p times,

E_R(ω)=Q_s(ω)^{NA/2}κ^N Res(z^s+1,G)^p.

This is a unit at the same prime 𝔭. No factor in κ is divisible by p, since A<p.

For any prime 𝔓 of O_N over p, normalize v_𝔓 by v_𝔓 of a uniformizer equal to one. Since p∤s, its ramification index is e=p−1 and v_𝔓(Φ_s(ζ_N))=1. Integral quotients give v_𝔓(D_n(ζ_N))≥K and v_𝔓(R_N(ζ_N))≥NA/2 at every 𝔓. At a prime above the chosen good lower component, both are equalities, because E_D(ζ_N) and E_R(ζ_N) reduce to their unit values at ω.

Thus the separate minimum valuations are K and NA/2, and the minimum valuation of their product is their sum. For a nonzero a∈O_N,

v_p(cont_N(a))=min_{𝔓|p}⌊v_𝔓(a)/(p−1)⌋.

Consequently

v_p(d_N)=⌊K/(p−1)⌋=⌊s(p−3)/8⌋,
v_p(r_N)=⌊NA/[2(p−1)]⌋=⌊N/4⌋,
v_p(c_N)=⌊[K+NA/2]/(p−1)⌋=⌊3s(p−1)/8⌋.

Finally, s≡1 mod4 implies the fractional part of N/4 is 1/4. The fractional part of s(p−3)/8 is 3/4 when p≡1 mod8 and 1/4 when p≡5 mod8. Their sum yields exactly the stated carry. ∎

The separate discriminant formula requires only an odd prime p and the separated lower good-component hypothesis; the resultant and carry statement above deliberately retains p≡1 mod4. For odd A, He_A(0)=0, so this proof cannot be reused for the resultant exponent.

The contribution of Theorem 4 is a sharpened, project-specific corollary with transparent normalization. Cyclotomic ramification, integral-coordinate divisibility, and the floor conversion are classical. The theorem does not establish that c_N has no primes outside N, nor any repeated-p statement.

## 5. Exact scalar-bank consequence

Let N=2m+1≥3, q primitive of order N, h=(N+1)/2 and

C=Σ_{k=0}^{N−1}q^{hk²}P^k.

A legal first-order bank is δI+Σ_{j=1}^Q a_j(I−λ_jP)^{−1}, with a_jλ_j≠0 and λ_j^N≠1. Its poles may be algebraic over Q(q).

### Corollary 5

For N=sp satisfying Theorem 4, the minimum legal branch count with a free scalar diagonal is Q_min=m. The same conclusion holds under the paired overlap criterion when s≡p≡3 mod4. Without a free diagonal, Q_min=m+1 for every odd N.

When Q_min=m, the diagonal is forced:

δ=(−1)^m q^{−m(m+1)/2}∏_{j=1}^m(1−q^j)≠0.

### Proof of the fusion and dependency boundary

The resolvent identity turns branch synthesis into a finite exponential-moment problem. The m×m shifted Hankel matrix factors as invertible chirp diagonals times a Vandermonde matrix, so its rank is m and Q≥m. Its unique degree-m annihilator is T_m(z)=(-1)^mH_m(−z;q). If T_m has simple nonzero nonresonant roots, partial fractions produce exactly m nonzero branches; conversely any m-branch decomposition must use those roots.

The supplied uniform resonance theorem states gcd(T_m,z^N−1)=1 for N≡1 mod4 and z−1 for N≡3 mod4; T_m(0)=(-1)^m excludes zero. Theorem 3 or its paired alternative supplies the missing squarefreeness for the stated families, hence the minimum. The determinant ratio of the full and shifted Hankel systems forces δ. The universal m+1 upper construction and the no-free-diagonal lower bound are the separately audited bank theorem, not new consequences of local discriminants alone.

An arbitrary free diagonal does not enlarge this fixed circulant grammar, since a diagonal circulant is scalar. Exact pole count says nothing by itself about a subquadratic evaluation algorithm or numerical stability. The available root-free quotient-algebra realization has O(N²) application cost.

## 6. Precise unresolved next lemmas

1. **Unramified content support.** For d=4r+1, write H_{2r}(z;ζ_d)=z^rP(z+z^{−1}), η_j=−ζ_d^j−ζ_d^{−j}, C_d^*=∏_{j=2}^{2r−1}(u−η_j). Put M_d=Res_u(P,(u−2)P′C_d^*). The unresolved lemma is: for every prime ℓ∤d, M_d is nonzero in at least one factor of O_d/ℓO_d. The established reciprocal reduction makes this equivalent to ℓ∤c_d. Special-value units, a single Frobenius orbit, or nonzero norm do not prove it.
2. **Repeated-prime ramification.** At N=sp^a, a≥2, the local index A=(p^a−1)/2 is at least p, so P_A is p-divisible. The current unit-quotient argument fails. New higher-order or divided-power analysis is required.
3. **Residual overlap guards remain.** Corollary 2B resolves the characteristic-zero quasi-Hermite guard at half-order overlap. It does not establish Disc(U)Res(z^d+1,U)≠0 for arbitrary d, nor remove any finite-characteristic p-unit guard. A complex disk inequality has no direct meaning after reduction modulo p; the paired modular proof is still needed.
4. **Priority comparison.** The exact fixed-ω moving-z coefficient and full ordinary-discriminant coefficient still need theorem-by-theorem comparison with legitimate full texts of Lubinsky–Saff (1987) and Zhedanov (1997). Absence of public access is not evidence of novelty.

## 7. Primary-literature comparison and attribution

- Atakishiyeva, Atakishiyev and Koornwinder, *On a q-extension of Mehta's eigenvectors…*, arXiv:0811.4100v2, §2, equations (2.7)–(2.8), explicitly gives the root-of-unity continuous-q-Hermite factorization. Equation (3.8) records the q→1 Hermite limit. These are established inputs. The inspected sections do not state the fixed nontrivial-ω moving-z discriminant coefficient here. https://arxiv.org/pdf/0811.4100
- Spiridonov and Zhedanov, *Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity*, §1 and §§2,5, studies root-of-unity limits and finite complex-weight orthogonality. It explicitly warns that complex recurrence coefficients do not ensure simple zeros. Terminal-degree nodes alone cannot settle the half-degree guard. https://arxiv.org/pdf/q-alg/9605034
- Sawa and Uchida, *Discriminants of classical quasi-orthogonal polynomials…*, Theorem 4.8, already provides adjacent quasi-Laguerre discriminants. The parity substitution t=y²/2 turns J into exactly such a combination; therefore Disc J is not a new general discriminant formula. The new candidate is its precise occurrence in the RS local coefficient. https://arxiv.org/pdf/1802.00605v1
- Gómez-Ullate, Grandati and Milson's pseudo-Wronskian equivalence and Grosu–Grosu's Hermite-Wronskian congruence contain the hook specialization used in the finite-characteristic pairing. The short elementary proof remains useful exposition, not a new general congruence. https://arxiv.org/pdf/1612.05514 and https://arxiv.org/pdf/2007.00065v1
- Durán, *Zeros of linear combinations of Laguerre polynomials* (2025), introduction, Theorems 1.3–1.6 and §2 inspected, treats real coefficient combinations and real-zero counts. It does not directly cover the complex parameter disk in Theorem 2A. Its companion *Zeros of linear combinations of Hermite polynomials*, introduction, Theorems 1.2–1.3 and §3, likewise assumes real coefficient data and supplies established differential/interlacing mechanisms. These comparisons narrow the possible delta but do not establish its priority. https://arxiv.org/html/2507.22425v1 and https://arxiv.org/html/2505.15330v1
- Cigler's *Elementary observations on Rogers–Szegö polynomials* is correctly arXiv:1602.07850. Its introduction, special-value normalizations and Hankel discussion were rechecked. It is relevant prior special-value theory; no citation typo is alleged. https://arxiv.org/pdf/1602.07850
- Lubinsky–Saff, *Convergence of Padé approximants of partial theta functions and the Rogers–Szegö polynomials*, Constr. Approx. 3 (1987), 331–361: publisher abstract and bibliography checked; full text is subscription-only. Author preprint index did not provide the 1987 article; an author-uploaded ResearchGate landing record was found, but fulltext retrieval failed. No conclusion about absence of the exact theorem is justified. https://link.springer.com/article/10.1007/BF01890574
- Zhedanov, *Gauss sums and orthogonal polynomials*, IJMPA 12 (1997), 289–294: institutional bibliography and primary successor reference checked; original full text unavailable through the tested DOI/publisher routes. https://doi.org/10.1142/S0217751X97000438

This is a bounded primary-source comparison, not an originality clearance. No denied Vanderbilt PDF route was retried or bypassed. No source programs were executed, imported, compiled or AST-parsed. Fresh controls in this new directory are separately labeled and do not upgrade old source self-tests to independent verification.
