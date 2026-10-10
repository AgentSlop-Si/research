# Phase 30 — Galois–Fourier rank and one-layer twiddle obstruction

**Date:** 2026-10-10  
**Status:** Exact characteristic-zero mathematics, independently reproducible integer/multiple-finite-prime checks. The mathematical derivation is supplied here, but historical novelty and independent peer review have **not** been established. **Not a faster generic FFT.**

## 1. The rank problem

Let `A` be a finite abelian group of order `N` and exponent `m`, let `K=Q(zeta_m)`, and let `F_A` be its unnormalized character table: `F_A[chi,a] = chi(a) in K`. Every Q-linear functional `L: K -> Q` gives a rational matrix `M_L=L(F_A)` by applying `L` entrywise. Let `c(A)` be the number of **cyclic subgroups** of `A`, including `{0}`.

**Theorem 30.1 (exact spectral rank law).** For `a in K`, set `L_a(z)=Tr_{K/Q}(a z)`. Write `U=(Z/m Z)^x`, and for `u in U` put `a_u = sigma_u(a)` with `sigma_u(zeta_m)=zeta_m^u`. With a suitable ordering of the characters,

    M_{L_a} = Q_a F_A,        Q_a = sum_{u in U} sigma_u(a) P_u,

where `P_u` permutes character rows by `chi -> chi^u`. Over a splitting extension for `U`, the eigenvalue of `Q_a` on the `eta`-isotypic space of the permutation representation is

    Lambda_eta(a) = sum_{u in U} sigma_u(a) eta(u)

(up to replacing `eta` by its inverse, depending on the permutation convention). Therefore

    rank_Q M_{L_a} = sum_{eta: Lambda_eta(a) != 0} mult_A(eta).

Here `mult_A(eta)` is the multiplicity of character `eta` in the action of `U` on the character set of `A`. The right side is an **exact rank formula for every** `a`, not only a generic statement.

**Corollary 30.2 (three ranks).**

* `L=Tr_{K/Q}`: `rank_Q M_L=c(A)`.
* If `L(1)=0`, then `rank_Q M_L <= N-c(A)`; **equality holds for a Zariski-open dense set** of those functionals.
* For a Zariski-open dense set of unrestricted Q-linear functionals `L`, `rank_Q M_L=N`.

For a cyclic group `A=C_N`, its cyclic subgroups correspond to positive divisors, so `c(C_N)=tau(N)` (the divisor-counting function). Thus the generic traceless rank is exactly

    rank_Q (L(zeta_N^(jk))) = N - tau(N).

The formula makes no reference to floating-point roots and holds in characteristic zero.

## 2. Proof

The standard Fourier matrix over `K` is nonsingular, by character orthogonality. For each pair `(chi,x)`:

    Tr(a chi(x)) = sum_{u in U} sigma_u(a) sigma_u(chi(x))
                 = sum_{u in U} sigma_u(a) chi(x)^u.

This is precisely `(Q_a F_A)[chi,x]` and proves the factorization. As `U` is finite abelian, all its permutation matrices commute and can be simultaneously diagonalized over an extension containing its character values; `Q_a` acts on the `eta`-isotypic part by the displayed Fourier coefficient. Multiplication by invertible `F_A` does not change rank. Because `M_{L_a}` has rational entries, its rank over `Q` equals its rank after extending scalars.

The trivial `U`-character occurs with multiplicity equal to the number of orbits of `U` on `A^`. Two elements of a finite abelian group belong to the same orbit under multiplication by units modulo the exponent exactly when they generate the same cyclic subgroup. (For `x` of order `d|m`, any automorphism of `<x>` given by a unit modulo `d` lifts to a unit modulo `m`.) The number of these orbits is `c(A)`. The trivial eigenvalue is `Lambda_1(a)=Tr(a)=L_a(1)`.

For `a=1`, the Galois conjugates are all 1, and the character-sum orthogonality identity gives `Lambda_eta(1)=0` for every nontrivial `eta`, while `Lambda_1(1)=|U|`. This proves the trace rank.

If `Tr(a)=0`, the trivial eigenspace vanishes, proving the upper bound `N-c(A)`. For any nontrivial `eta`, the map `a -> Lambda_eta(a)` is **not** identically zero on the hyperplane `Tr(a)=0`: distinct field automorphisms are linearly independent over `K` as linear maps (Artin independence), while the character coefficients are not all equal. Thus its zero set cuts out a proper subspace (over a suitable algebraic extension). The complement of finitely many such zero sets is nonempty and Zariski open over the infinite field `Q`. There all nontrivial isotypic eigenvalues are nonzero; hence rank is `N-c(A)`. The same argument without `Tr(a)=0` gives generic full rank. The field trace pairing is nondegenerate, so **every** Q-linear functional is some `L_a`. QED.

## 3. Explicit nullspace interpretation

For generic traceless `L`, the kernel on the input side is exactly the rational space of vectors constant on the unit-multiplication orbits of `A`, one orbit for each cyclic subgroup. In the cyclic case, the canonical kernel vectors are indicators of the gcd classes

    v_d[k] = 1_{gcd(k,N)=d},   d|N,

where `gcd(0,N)=N`. Indeed, the DFT of each orbit indicator is a Ramanujan sum, hence rational at every frequency; a functional with `L(1)=0` annihilates its transform. Their number is `tau(N)` and the generic-rank theorem proves that there are no additional nullspace directions.

The corresponding statement for a noncyclic group uses orbit indicators indexed by its cyclic subgroups.

## 4. Circuit corollary: a one-layer scaling-rank lower bound

Suppose the exact `N`-point Fourier matrix over `K` is represented as

    F_A = R + B diag(c_1,...,c_r) C,

where `B,C,R` have rational coefficients and the middle scalars are algebraic or complex constants. Let `s` be the number of middle scalars that are **not rational**. Choose a generic rational-linear functional `L:K->Q` with `L(1)=0` and `rank L(F_A)=N-c(A)`. Extend it Q-linearly to a finite-dimensional space containing the `c_i` if necessary. Applying `L` entrywise annihilates `R` and all rational middle scalars, while each remaining term has rank at most 1:

    L(F_A) = sum_{i: c_i not rational} L(c_i) B[:,i] C[i,:].

Therefore the number of nonrational scalar channels satisfies

    s >= N-c(A).

**Scope:** one diagonal multiplication stage, surrounded by arbitrary rational linear maps, with a rational correction matrix allowed for free. It does **not** apply to arbitrary multi-layer nonrational arithmetic circuits, and does not imply an unrestricted `N log N` lower bound.

## 5. Stronger special case: the isolated Phase 29 twiddle layer is optimal in that model

Let `h=2^t >= 1`, `g=8h`, and `w` be a primitive `g`th root. The isolated noncoprime twiddle layer is the diagonal linear operator

    D_{u,q}=w^(u*q),    0<=u<8, 0<=q<h.

Its rational entries are exactly those with `u=0` or `q=0`. For `u>0` and `q>0`, `0<u*q<8h`, and the 2-adic valuation is at most `(2)+(t-1)=t+1`, whereas `g/2=2^(t+2)`; hence `w^(u*q)` is neither +1 nor -1, the only rational roots of unity. Thus precisely `7(h-1)` entries are nonrational. Fifteen separate CRT columns require `105(h-1)` such slots.

For a diagonal matrix `D` over the cyclotomic field, there is a Q-linear `L` vanishing on Q but **nonzero on every nonrational entry**, since finitely many proper hyperplanes cannot cover that vector space. Then `L(D)` is diagonal with exactly `105(h-1)` nonzero entries, hence its rank is that number. The one-layer argument of Section 4 shows:

    ANY rational-preweave / single-diagonal / rational-postweave
    representation of that isolated twiddle layer needs at least
    105(h-1) nonrational scalar channels.

Phase 29 pays exactly `105(h-1)` separate nonidentity twiddle products. **It is optimal only for that isolated layer and that circuit class.** This does not prevent a saving when twiddles are fused with adjacent nonrational Fourier stages; that is the still-open research gate.

This special bound differs from the Phase 29 C4-free row/column-gauge bound: the latter permits free **nonrational** row/column gauges for an upper bound on identities, whereas here the surrounding operations are restricted to **rational** maps and a single middle diagonal.

## 6. Verification and reproducibility

`cyclotomic_rank_certificate.py` builds the characteristic-zero projected matrices as **integer** coefficient matrices modulo the exact cyclotomic polynomial, and checks nonzero Gaussian-elimination minors modulo prime `998244353`. Nonzero modular minors prove nonzero rational minors (not merely probability of correctness). The matching rank upper bounds are proved in Sections 1-3.

* All 22 cyclic sizes in `RANK_CERTIFICATES.json`: ranks `(tau(N), N-tau(N), N)` for trace, explicit traceless, and explicit unrestricted functionals.
* All 15 finite abelian group products in `ABELIAN_RANK_CERTIFICATES.json`: ranks `(c(A), |A|-c(A), |A|)` in the same three modes.
* The full Phase 29 preweave and postweave linear forms were compiled over Z. No two computed intermediate forms coincide, even up to sign. The complete 120-point graph, including field scalings, was checked for repeated values in **two distinct finite fields**: none were found. Thus uncomplicated CSE is not a new arithmetic saving. Details in `NEGATIVE_GATE.md`.

The nonzero-minor certificates prove the claimed ranks of those *explicitly tested* characteristic-zero integer matrices, but do not constitute a machine-checked Lean proof of the general theorem.

## 7. Research and priority limits

This rank law follows from standard representation/Galois theory. The specific formula and FFT-circuit corollary were derived within our Phase 30 research, but independent literature review is insufficient to assert historical novelty or publication priority. Rational character orbits, Ramanujan sums, and Winograd tensor decompositions predate this work.

Neither theorem nor finite-field audits produce an exact all-input `o(N log N)` FFT. The leading Phase 29 complexity remains `Theta(N log N)`; this phase identifies which structural approaches **cannot** lower the cost and what a truly cross-stage solution would have to escape.
