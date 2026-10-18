# Q2 dense torus: full canonical Weyl displacement of the actual boundary

18 October 2026. Owner scope: Q2-DENSE-TORUS-20261013, task 4 of the pinned six-gate plan. This is an author-side proof candidate requiring independent review.

## Result and terminal stopping point

The proposed route was to prepare the true cyclic boundary matrix using a uniformly bounded displacement rank relative to one of its two natural Weyl generators, and then obtain a cold O(m²) boundary solve.

**That structural premise is false.** For every m≥4, every primitive complex m-th root q, and the prescribed parameter

    λ = 2^(-4-m ceil(log₂(2m))),

both F and F⁻¹ have **full displacement rank m** relative to U and Q:

    rank(F-UFU⁻¹) = rank(F-QFQ⁻¹) = m,
    rank(F⁻¹-UF⁻¹U⁻¹) = rank(F⁻¹-QF⁻¹Q⁻¹) = m.       (A)

Here F is exactly I-T_(m-1)…T_0 from the pinned inverse reduction, not a surrogate monodromy. The theorem is uniform over all m≥4 and all primitive embeddings. It is proved analytically and algebraically below; finite controls are transcription checks only.

This is a precise failed premise for the proposed canonical-displacement representation. It does **not** prove a superlinear lower bound, exclude displacement equations with other or different left/right generators, exclude other useful structure, or construct the requested cold O(N) inverse. The inverse gate therefore remains open. No Fourier construction, historical-code validation, priority change, or wider owner closure follows.

## 1. Source and exact family

The controlling source is `SOURCE_REPORT.md`, copied byte-for-byte from Git blob `6699b54831c182d8131dc4a9dfbd202dfa3d4e70`, repository `AgentSlop-Si/research`, path `math/finalized/2026-10-16-mathematical-development-1221/q2/REPORT.md`, pinned commit `22e4fbdff0dd655d4cac7408964142fd2476686d`. Its sections 1–6 and 10 specify the family, correct operator order, actual row reduction, paid setup, and still-open cold question. No historical scientific package or source program was executed.

For m≥2, N=m², coordinates (a,c) lie in Z_m². With q primitive of order m,

    (Av)[a,c]=v[a-1,c],       (Bv)[a,c]=q^a v[a,c-1],
    L=I-(A+B)/4,
    φ(a,c)=(-c,a+c),         P e_x=e_φ(x),
    M=P⁻¹LP,                S=L⁻¹+λM⁻¹.

The source's supplied-root model allows q directly, or q=ω_N^m from a supplied primitive N-th root. Work is counted in exact characteristic-zero scalar operations, with separately charged word addressing. These are not unit-cost bit-complexity claims.

Let K=M+λL. Without commuting L and M,

    S=L⁻¹KM⁻¹,                 S⁻¹=MK⁻¹L.             (1)

The conjugated terms are

    (A'v)[a,c]=v[a-1,c+1],      (B'v)[a,c]=q^(-c)v[a-1,c].

Thus, on row vectors indexed by c, define

    (Uv)[c]=v[c-1],            Q=diag(q^(-c)),
    s=1+λ,                    β=λ/(4s),
    D_a=s(I-βq^a U),           R=(U⁻¹+Q+λI)/4,
    T_a=D_a⁻¹R,
    E=T_(m-1)…T_0,             F=I-E.                 (2)

Here β is the inverse row-recurrence coefficient; it is called t in the pinned report. The block system Ky=g is exactly

    D_a y_a - R y_(a-1) = g_a,
    y_a = D_a⁻¹g_a + T_a y_(a-1).                    (3)

Sweeping (3) from boundary b=y_(m-1) produces last row p+Eb, where p is the zero-boundary output. Therefore Fb=p, and a second sweep recovers every component. This is the actual ordered product throughout this report.

## 2. Exact first variation of the true monodromy

Introduce a complex variable z in place of λ, leaving m and q fixed:

    W=U⁻¹+Q,
    H_a=I-q^a U/4,
    T_a(z)=(I+zH_a)⁻¹(W+zI)/4,
    E(z)=T_(m-1)(z)…T_0(z).                         (4)

The basic Weyl relations are QU=q⁻¹UQ and QU⁻¹=qU⁻¹Q. The cyclic bidiagonal determinant gives

    det(xI-W)=x^m-2,        W^m=2I.                 (5)

For the determinant identity, the only contributing permutations are the diagonal permutation and the complete cyclic shift. The diagonal product is ∏_c(x-q^(-c))=x^m-1, and the cyclic-shift contribution is -1. Cayley–Hamilton gives the second identity. In particular W is invertible and ||W||₂≤2.

Differentiating the **ordered** product at zero gives

    E(0)=2·4^(-m) I,
    E'(0)=4^(-m) Σ_(a=0)^(m-1)
        W^(m-1-a) [I-W+(q^a/4)UW] W^a.             (6)

The potentially noncommuting sum in (6) vanishes for m>2. Indeed,

    WU=q⁻¹UW+(1-q⁻¹)I,
    W^k U=q^(-k)UW^k+(1-q^(-k))W^(k-1).

Hence

    Σ_a q^a W^(m-1-a) U W^(a+1)
      = (Σ_a q^(2a+1)) UW^m
        + (Σ_a(q^a-q^(2a+1))) W^(m-1) = 0,         (7)

because both Σq^a and Σq^(2a) vanish when q is primitive and m>2. Therefore

    C₁:=E'(0)
      = m4^(-m)(W^(m-1)-2I)
      = 2m4^(-m)(W⁻¹-I).                          (8)

This calculation uses the given forward row order. Reversing the product or changing the q phase would produce a different calculation.

## 3. Full-rank first-order commutators, uniformly in the root

For either X=U or X=Q, the commutator [W,X]=WX-XW is a nonzero scalar times a unitary matrix:

    [W,U]=(q⁻¹-1)UQ,
    [W,Q]=(1-q)U⁻¹Q.                              (9)

From (8),

    [C₁,X]=-2m4^(-m) W⁻¹[W,X]W⁻¹.

Since ||W||₂≤2,

    σ_min([C₁,X]) ≥ (m/2)4^(-m)|1-q|.

Every primitive complex m-th root satisfies |1-q|≥2sin(π/m)≥4/m. Consequently

    σ_min([C₁,X]) ≥ 2·4^(-m),     X∈{U,Q}.        (10)

The phase separation, including primitive embeddings far from e^(2πi/m), is explicitly accounted for.

## 4. A uniform analytic remainder bound at the prescribed λ

It is essential to prove the first-order rank survives at the actual fixed λ, rather than infer it from generic parameters.

Set r=1/(8m), and assume m≥4. Since ||H_a||₂≤5/4, (4) is analytic throughout |z|≤r. There,

    ||T_a(z)||₂ ≤ (2+r)/(4(1-5r/4))
                 ≤ (1/2) exp(2r).

For completeness, log(1+r/2)-log(1-5r/4)
≤r/2+(5r/4)/(1-5r/4)<2r when r≤1/32. Thus

    max_(|z|=r) ||E(z)||₂ ≤ 2^(-m) exp(1/4)
                              < 2^(1-m).         (11)

The matrix-valued Cauchy coefficient bound follows by applying the contour integral and the operator-norm triangle inequality. If 0<λ<r/2, the sum of Taylor terms of degree at least two, denoted J(λ), satisfies

    E(λ)=E(0)+λC₁+J(λ),
    ||J(λ)||₂
      < 2^(1-m) (λ/r)²/(1-λ/r)
      ≤ 256m²2^(-m)λ².

As U and Q are unitary,

    ||[J(λ),X]||₂ < 512m²2^(-m)λ².                (12)

The prescribed λ obeys, for every m≥4,

    λ ≤ 1/[16(2m)^m] ≤ 1/[256m²2^m] < r/2.       (13)

The middle inequality is equivalent to m^(m-2)≥16, which holds for m≥4, with equality at m=4. Combining (10)–(13),

    ||[J(λ),X]||₂ < 2λ4^(-m)
                     ≤ σ_min(λ[C₁,X]).           (14)

Since E(0) is scalar, [E(λ),X]=λ[C₁,X]+[J(λ),X]. The strict perturbation inequality (14) proves this commutator invertible, for X=U and X=Q. No finite sample or numerically estimated singular value is used.

As [F,X]=-[E,X] and F-XFX⁻¹=[F,X]X⁻¹, both displacements of F have rank m.

## 5. Inverse, coordinate changes, and precise scope

For the fixed complex family, the source's row contraction gives

    ||T_a||₂ ≤ (2+λ)/(4+3λ)<1/2,
    ||E||₂<2^(-m)<1.

Thus F is invertible. The identity

    [F⁻¹,X]=-F⁻¹[F,X]F⁻¹

preserves rank and proves the two remaining statements in (A).

Simultaneously conjugating the matrix and its displacement generator preserves rank. Therefore diagonalizing U with a dense m-point Fourier change of basis, or exchanging the standard Weyl generators, cannot turn these particular displacements into constant-rank ones. A dense boundary-only Fourier change costs O(m²)=O(N), so that cost was not an obstruction; the proposed bounded-rank premise itself fails.

The result does **not** cover an equation AF-FB with independently chosen A and B, a parameter-dependent change that changes rather than conjugates the proposed displacement equation, or every structured representation of F. Full displacement rank alone is not a computational lower bound: even full-rank generators might have extra exploitable structure. The only rejected proposal is a uniformly bounded-rank representation for the two explicitly displayed canonical same-generator displacement equations.

The theorem covers all m≥4, which is already an unbounded-size obstruction. The m=3 control in the check file is a transcription control; the all-m proof does not require it. The old scalar-monodromy m=2 counterexample is neither rerun nor used as the new result.

## 6. Full invertibility versus the row-executor guards

All relevant guards must remain distinct.

1. The supplied root must be primitive of the specified order, and scalar denominators such as 4 must be units. In the original complex model these conditions hold by hypothesis.
2. The current row executor uses s≠0 and 1-β^m≠0. Indeed U^m=I and

       (I-βq^aU)⁻¹
         = [Σ_(j=0)^(m-1)(βq^aU)^j]/(1-β^m).

   Over C with the prescribed positive λ, s>0 and 0<β<1/4. These are row-executor conditions, not standalone necessary conditions for existence of the full inverse.
3. Once the row inverses exist, block elimination yields

       det K = (∏_a det D_a) det F.

   Under those row-unit assumptions, K is invertible exactly when F is invertible. Without them, F in (2) is not defined, and that boundary route cannot decide full invertibility.
4. In the source field, L and M are invertible, and (1) says S is invertible exactly when K is. Over C, ||(A'+B'+λA+λB)/(4s)||₂≤1/2 proves K invertible independently of row elimination.

An exact guard-separation example uses the **actual prescribed member m=2** reduced to the characteristic-79 extension F₇₉[i]/(i²+1). The supplied primitive fourth root is i, and q=i²=-1. Here λ=1/256=25, s=26, β=1. Thus 1-β²=0 and both D_a have rank one, but the full K is

    [26 53 33 59]
    [53 26 59 73]
    [33 59 26 26]
    [59 73 26 26]             over F₇₉,

with det K=39≠0. Direct permutation construction gives det L=det M=2≠0. Hence S exists and is invertible although this row executor is unavailable. The extension is a field since -1 is a nonsquare modulo 79. This finite-field example is about the guard distinction only; analytic complex rank estimates are not asserted after finite-field reduction.

If the symbol β is instead used for the original forward coefficient 1/4, its analogous distinction is visible algebraically: (A+B)^m=2I makes L=I-β(A+B) invertible whenever 1-2β^m≠0, whereas the row-wise inverses I-βq^aU additionally require 1-β^m≠0. These are different statements. No field reduction may omit either executor guard simply because the full transform is invertible.

## 7. Honest cold-work and storage ledger

No new exact cold executor is claimed. The best executor established by the pinned source remains the paid dense-boundary method. Its cold ledger, for fresh m, root, coefficients, and right-hand side, is:

- Root powers and row coefficients: O(m) field operations if the supplied root contract is accepted. Optional exhaustive order validation of a supplied primitive N-th root can be charged O(N) scalar operations and O(1) extra space.
- Construct ell and λ: O(m log m) repeated-halving operations as in the source, which is O(N) for m≥2; no free gigantic rational constant or root oracle is introduced.
- β, β^m, reciprocals, q^a, row addressing and auxiliary tables: O(m) scalar and O(N) word work at most, with all guards checked.
- Form E by its m basis-vector sweeps: exactly 10m³+m² scalar additions/multiplications in the source implementation.
- Form F: m² subtractions.
- Exact dense LU: m(m-1)/2 divisions and m(m-1)(2m-1)/3 multiplications/subtractions, plus charged pivot/address work.
- First right-hand side: Lf, zero-boundary sweep, triangular solves, reconstruction sweep, and My total 32N+m scalar operations in the source's ledger, plus O(N) reads/writes/copies/addressing. All N outputs are produced.
- Storage: O(m²)=O(N) scalars and words, including F/LU and vectors. Exact scalar representation lengths are not bounded by this storage count.

Thus total cold work remains O(N^(3/2)), storage O(N), with O(N) warm work for each additional vector. Any direct use of these dense tables must pay preparation again for fresh parameters. The failed displacement premise gives no entitlement to replace that cost by O(N).

A rank-r factorization of either canonical displacement needs r≥m by (A), so the contemplated constant-width generator interface is unavailable. This observation alone neither lower-bounds every possible generator algorithm nor rules out a differently represented cold O(N) boundary solve. The unresolved construction is still an exact cold O(N) application of F⁻¹, or a different exact cold O(N) solve of K, with every source/coefficient/address/output cost charged.

## 8. Fresh verification and disposition

`check_obstruction.py` is a new standard-library-only transcription checker. It does not import or execute the historical implementation. It independently constructs U,Q, differentiates the ordered product with exact dual-number arithmetic modulo 14401, checks (8), and checks the two commutator ranks for F and F⁻¹ at m=3,4,5,6. It also checks the fixed-family characteristic-79 guard example by constructing M through the explicit permutation, and confirms exact threshold inequalities for m=4,…,100 as implementation controls. `CHECK_RESULTS.json` contains its output. These are not warm timing evidence and not substitutes for Sections 2–5.

**Disposition:** proposed canonical bounded-Weyl-displacement route refuted uniformly for m≥4; exact cold linear-work inverse **OPEN**. This is a terminal failed-structural-premise result for this attempt, pending independent review. No repository or spreadsheet was modified.
