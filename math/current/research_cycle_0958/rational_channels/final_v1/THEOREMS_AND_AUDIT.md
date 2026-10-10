# Rational Fourier projections and scalar-channel audit

10 October 2026. Complete reconstruction from definitions. Source programs were not executed, imported, compiled, or AST-parsed. The newly written control scripts use only standard-library arithmetic and source JSON as data. This note proves mathematical statements; it makes no historical-priority, general FFT speedup, or total-operation optimality claim.

## 0. Disposition

1. Phase 30's exact Galois spectral formula, trace rank c(A), generic annihilating-Q rank |A|−c(A), and generic unrestricted full rank are correct with the fields and genericity below.
2. Its rational-preprocessing / one-diagonal / rational-postprocessing channel bound is correct. The warning that the same bound is unavailable at arbitrary depth is unnecessarily restrictive: the gate-cut argument below proves it for arbitrary-depth scalar linear straight-line circuits in the stated base-field model.
3. The isolated dyadic twiddle matrix has exactly 105(h−1) nonrational scalar-gate complexity, even with arbitrary depth and rational operations free. This is an isolated-operator statement. It cannot be charged additively to neighboring nonrational operators after fusion.
4. Every nonzero scalar multiple αF_A still has generic annihilating-Q projection rank at least |A|−c(A). Equality need not hold. This closes the scalar normalization issue in a fully charged Weyl-covariant extraction.
5. Branch count, scalar-gate count, real multiplication count, total arithmetic cost, and bit complexity remain different resources. None of these results implies an Ω(N log N) lower bound or a faster unrestricted FFT.

## 1. Exact objects and fields

Let A be a finite abelian group of cardinality N≥1 and exponent m. Fix an embedding K=Q(ζ_m) into C and a primitive root ζ_m. Write G=Gal(K/Q)≅(Z/mZ)^×; for m=1, G is the trivial group. Let Â=Hom(A,μ_m) and set

    F_A[χ,x]=χ(x),   χ∈Â, x∈A.

This is the unnormalized character table. It is invertible over K by character orthogonality. The word “projection” below means entrywise application of a Q-linear functional L:K→Q; it does not assert an idempotent projection operator. “Annihilating-Q” means L(1)=0, equivalently L vanishes on every rational number. This is distinct from choosing the trace functional itself.

Every such L has a unique trace-dual parameter a∈K:

    L_a(z)=Tr_(K/Q)(az).

The trace pairing is nondegenerate because K/Q is separable. This can also be seen from the invertible embedding matrix of the power basis. Take E=Q(ζ_m,ζ_|G|), a common splitting field containing K and all values of characters η of G. All eigenvalue calculations occur over E. Matrix L_a(F_A) has rational entries, so its rank over Q, K, E, or C is the same.

For u∈G define the row permutation by (P_u v)_χ=v_(χ^u). Then P_uP_v=P_(uv), and define

    Q_a=Σ_(u∈G) σ_u(a)P_u,
    λ_η(a)=Σ_(u∈G) σ_u(a)η(u).

Here η indexes the simultaneous eigenspaces with P_u v=η(u)v. Changing the permutation convention consistently replaces η by η⁻¹, without changing any rank.

## 2. The spectral rank theorem, with proof

For every a∈K,

    L_a(F_A)=Q_a F_A,
    rank_Q L_a(F_A)=Σ_(η:λ_η(a)≠0) mult_A(η).              (2.1)

Indeed, its (χ,x) entry is

    Σ_u σ_u(a)σ_u(χ(x))=Σ_u σ_u(a)χ(x)^u.

The commuting finite-order matrices P_u are simultaneously diagonalizable over E, since characteristic is zero. On the η-isotypic space Q_a acts by λ_η(a). Multiplication by the invertible F_A preserves rank, proving (2.1) for every a, including zero and exceptional nongeneric parameters.

Let c(A) be the number of cyclic subgroups of A, including {0}. The trivial-character multiplicity is c(A). To prove this, invariant functions on Â are precisely functions constant on G-orbits. If χ has order d|m, its orbit consists of all generators of ⟨χ⟩: the map (Z/mZ)^×→(Z/dZ)^× is surjective. For a unit residue modulo d, choose a lift avoiding every prime dividing m but not d by the Chinese remainder theorem; primes already dividing d impose no problem. Thus each cyclic subgroup of Â contributes one orbit. A and Â have the same invariant factors, hence the same number of cyclic subgroups.

More precisely, if O is an orbit with stabilizer H_O⊆G, its permutation representation is the regular representation of G/H_O. It contributes multiplicity one to η exactly when η|_(H_O)=1. Consequently

    mult_A(η)=Σ_O 1_(η|H_O=1),   0≤mult_A(η)≤c(A).       (2.2)

In particular λ_1(a)=Tr(a)=L_a(1). For a=1, λ_1=|G| and every nontrivial λ vanishes. Therefore

    rank_Q Tr(F_A)=c(A).                                  (2.3)

### Genericity, without an implicit field change

Identify K with Q^d in any fixed Q-basis, d=[K:Q]. “Generic” means a nonempty Zariski-open subset of this affine Q-space, or of its rational hyperplane Tr(a)=0. After extension to E, the conjugate-coordinate map

    K⊗_Q E → E^G,   a↦(σ_u(a))_u

is invertible. In the power basis 1,ζ_m,...,ζ_m^(d−1) its matrix is Vandermonde on the distinct primitive roots ζ_m^u. Fourier transformation on G then sends these coordinates invertibly to (λ_η)_η. Thus each nontrivial λ_η is nonzero as a linear functional on the hyperplane λ_1=0. A finite union of its proper zero hyperplanes cannot fill that hyperplane over E.

This yields a nonzero maximal minor of the rational-entry matrix L_a(F_A). That minor is a polynomial over Q in rational coordinates on Tr(a)=0. A nonzero polynomial over the infinite field Q cannot vanish at every rational point. Its nonvanishing locus is the required nonempty Q-open set, and is dense. This avoids interpreting an E-valued eigenvalue as a Q-valued coordinate or assuming random choices are always generic.

It follows that

    max_(L(1)=0) rank_Q L(F_A)=N−c(A),
    generic unrestricted rank_Q L(F_A)=N.                 (2.4)

For m=1 or 2, K=Q, the annihilating-Q functional space is the zero vector space; its unique functional has rank zero. Every element of A has order at most two, c(A)=N, so (2.4) still holds, with the entire zero-dimensional parameter space as its open set.

## 3. Kernels, prime/composite cases, and tensor warnings

For each G-orbit O⊆A, the Fourier image of its indicator 1_O has rational coordinates: Galois automorphisms only permute the summands. Therefore every L with L(1)=0 annihilates F_A1_O. The c(A) indicators are linearly independent. At a generic parameter they span the entire input kernel by (2.4).

For A=C_N, orbits are gcd classes, including {0}, and c(A)=τ(N). Hence the rank is N−τ(N). For a prime p this is p−2; for p^t it is p^t−(t+1). This includes p=2,N=2, where the rank is zero. Composite lengths require divisor counting, not N−2. For example N=120 gives 104, and N=240 gives 220.

For A=(C_p)^r,

    c(A)=1+(p^r−1)/(p−1),
    N−c(A)=(p^r−1)(p−2)/(p−1).

Thus all elementary abelian 2-group character tables are rational and this invariant is zero, despite potentially large dense matrices.

Nonzero L need not be generic. In K=Q(ζ_5), the power-basis functional L(1)=0,L(ζ)=1,L(ζ²)=L(ζ³)=0 has rank 2, whereas the generic rank is 3. L=0 always gives zero. Genericity is essential.

For character tables F_A⊗F_B=F_(A×B), one must compute c(A×B) using the actual common cyclotomic field and its diagonal Galois action. Applying L does not commute with tensor product. For C_3×C_3 the projected rank is 4, although each individual generic rank is 1. For coprime exponents, cyclic subgroups split uniquely and c(A×B)=c(A)c(B), giving |A||B|−c(A)c(B), still not the product of the individual projected ranks. A zero tensor factor gives the zero matrix and invalidates any nonzero-factor conclusion.

Likewise L does not commute with matrix multiplication: F_4²=4J, with J the rational inversion permutation. Each F_4 has generic rank 1 after L, but its square has rank zero. Local projection ranks are not additive across circuit stages.

## 4. Arbitrary-depth scalar-linear gate-cut theorem

Let T be an n-by-k complex matrix computed exactly on every complex input by a finite acyclic scalar linear straight-line circuit. Allowed gates are rational linear combinations of already computed scalar values and gates q_i=c_i v_i with c_i∈C\Q. Count each execution of the latter as one nonrational scalar multiplication, even if its coefficient is reused or precomputed. Let s be their number. Fanout, rational coefficients, and rational linear work may be free for this lower-bound model. Division by a fixed nonzero constant is included by multiplying by its reciprocal.

For every Q-linear functional L on a finite Q-vector space containing 1 and all relevant coefficients, with L(1)=0,

    rank_Q L(T)≤s.                                        (4.1)

Proof: cut the output wire of each of the s nonrational gates and regard the cut outputs q_1,...,q_s as independent scalar symbols. The remaining graph uses only rational linear operations. Its outputs therefore have the form

    y=R x+B q,   R∈Q^(n×k), B∈Q^(n×s).

In the actual linear computation q=H x for an s-by-k complex matrix H. Hence T=R+BH and L(T)=B L(H), proving (4.1). Gate dependencies before a cut do not alter this argument. Only the finitely many coefficients in H and T are needed, so their Q-span together with K suffices even when constants are transcendental; an unnecessarily finite field extension need not be assumed. Extend a functional from K to this finite vector space by extending a basis.

Combining (4.1) with (2.4) gives s≥N−c(A) for F_A at arbitrary scalar-linear depth. The one-diagonal source theorem is an immediate special case, not the maximal valid depth.

### Model exclusions and N=4 sanity check

This does not count vector/matrix operations as one scalar gate. It grants no free nonrational coefficients, coordinate changes, Green solves, or Fourier transforms. It excludes multiplication or division of input-dependent quantities, non-linear gates, and free conjugation / real-imaginary extraction or recombination outside the scalar complex-linear rational-coefficient model. No addition, precision, routing, storage, or coefficient-preparation lower bound follows.

For N=4 the bound is 4−τ(4)=1, and multiplication by i is nonrational over Q. In a real-coordinate implementation, i multiplication is only a sign/swap of real and imaginary wires; the real-expanded F_4 has entries 0,±1 and this obstruction is zero. Therefore these counts must never be substituted for published real-multiplication counts without a stated conversion. If Q(i)-linear operations are free, use the base-field variant below instead.

### Base-field variant

Let k⊆C be a characteristic-zero field and K=k(ζ_m), with G=Gal(K/k) the corresponding subgroup of (Z/mZ)^×. The same proof gives generic k-linear annihilating-k projection rank N−o_G(Â), where o_G is the number of G-orbits. It bounds scalar gates whose constants lie outside k when k-linear operations are free. For k=Q(i), N=2^t,t≥2, the unit subgroup u≡1 mod4 has 2t orbits on C_N, so the bound is N−2t; for N=4 it is zero. It is generally different from the Q-base formula.

## 5. Isolated diagonal optimality and the dyadic twiddle count

For any diagonal complex matrix D, let k be the number of nonrational diagonal entries. In the finite Q-span of 1 and those entries, each condition L(d_j)=0 for a nonrational d_j is a proper hyperplane inside L(1)=0. Choose L outside their finite union. Then L(D) has exactly k nonzero diagonal entries, so (4.1) forces at least k nonrational scalar gates at any depth. Direct coordinatewise scaling uses k. Thus k is the exact optimum in this model, with rational work free. Repeated nonrational entries still count once per independently scaled coordinate; a broadcast coefficient is not a broadcast multiplication of different inputs.

For h=2^t≥1, g=8h and w primitive of order g, consider diagonal entries w^(u q), 0≤u<8,0≤q<h. A rational root of unity is ±1. If u,q>0, then v_2(uq)≤2+(t−1)=t+1, while g/2 has valuation t+2; hence w^(uq)≠±1. Precisely the entries u=0 or q=0 are rational. One copy has 7(h−1) nonrational entries and fifteen independent copies have 105(h−1). For h=1 the count is zero. The source's direct twiddle scaling meets this bound.

This optimum concerns the isolated diagonal operator. A circuit computing a fused product with neighboring nonrational matrices has another target, so no additional 105(h−1) charge may be inserted without a valid whole-target argument.

## 6. Nonzero scalar normalization lemma

Let α∈C be nonzero. On W=K+αK, consider Q-linear L with L(1)=0. Then

    generic rank_Q L(αF_A) ≥ N−c(A).                      (6.1)

If α∉K, then αK∩Q={0}; otherwise αk=q≠0 would imply α=q/k∈K. Thus the restriction of L to αK is unconstrained by L(1)=0, and the unrestricted part of (2.4) gives generic full rank N.

If α∈K, use L_a and put b=aα. The parameter constraint becomes Tr(bα⁻¹)=0. In the independent conjugate coordinates x_u=σ_u(b), it is the hyperplane

    Σ_u σ_u(α⁻¹)x_u=0.

The eigenvalues of L_a(αF_A) are the distinct Fourier coordinates Σ_u η(u)x_u. At most one of these coordinates can vanish identically on one nonzero hyperplane. Every other one is generically nonzero. If an eigenvalue is forced to zero, its multiplicity is at most c(A) by (2.2), proving (6.1).

More precisely, the exceptional case is exactly

    σ_u(α⁻¹)=α⁻¹η(u) for all u,

for some η∈Ĝ, and then the generic rank is N−mult_A(η). Otherwise the generic rank is N. Such η must take values in {±1}: its values belong to K by the displayed ratio; applying σ_v to that equality and comparing the equations for uv and v gives σ_v(η(u))=η(u), hence η(u)∈Q. As a root of unity it is ±1. Rational α gives the trivial character and the original N−c(A).

Examples: ζ_3F_3 has generic rank 3, while F_3 has rank 1; √5F_5 and F_5/√5 have generic rank 4, while F_5 has rank 3; (1+ζ_5)F_5 has rank 5. The normalized F_2/√2 has rank 2, while F_2 has rank 0. Therefore arbitrary normalization preserves the lower bound, not necessarily the exact equality.

The gate-cut theorem now gives s≥N−c(A) for every αF_A, α≠0. The zero scalar must be excluded.

## 7. Complete, hypothesis-matched fusion statements

### 7.1 Fixed-pair Weyl–Green grammar plus scalar gate count

Retain the exact F014 grammar from the reviewed fixed-pair theorem: odd N, one fixed ordered pair U=S^uT^v,V=S^rT^s with D=us−vr a unit, and branches c(I−aU)⁻¹(I−bV)⁻¹ with a^N,b^N≠1 and no extra branch-dependent Weyl endpoints. Over characteristic zero, any such representation equal to F_N, implemented by a scalar-linear circuit as in §4, obeys BOTH

    branch count ≥ max{N/gcd(N,δ), min((N+1)/2,N/gcd(N,u²+v²)),
                       min((N+1)/2,N/gcd(N,r²+s²))},
    total nonrational scalar gates ≥ N−τ(N),

where δ=(D−ur−vs)/2 modulo N. Proof: apply the independently proved F014 coefficient/Hankel theorem to the representation and §4 to its exact whole-target evaluator. These are simultaneous constraints on different resources, not a product bound. A coefficient-rank branch is not one scalar gate. If verified implementation budgets give s_shared+Σ_i s_i gates, then that sum must exceed N−τ(N); there is no justified multiplication of a branch lower bound by an isolated per-branch gate lower bound when sharing/cancellation is allowed. The rational-channel statement here is characteristic zero; it is not automatically the finite-field version of F014.

### 7.2 Weyl-covariant embedding/extraction, with normalization included

Suppose exact primitive Weyl covariance supplies PJE=αF_N, α≠0, as in the v27 swap classification, and the actual E,J,P evaluation is a scalar-linear circuit. Then the ENTIRE implementation needs at least N−τ(N) nonrational scalar gates, by §6 and §4. If separate implementations use s_E,s_J,s_P, their concatenation satisfies

    s_E+s_J+s_P≥N−τ(N).

Only if E and P are rational-coefficient maps can their gate charge be zero in this model. A potentially dense, nonrational conjugating basis from a normal-form proof cannot be treated as free. Covariance alone does not locate the gate charge inside J. The conclusion is independent of scalar normalization and circuit depth, but remains only linear in N.

### 7.3 Inverse Fourier channels: exact counterexample to additive charging

Let S be the cyclic shift, choose nonzero a∈Q with a^N≠1, and put C=(I−aS)⁻¹. Its geometric-series identity is

    C=(1−a^N)⁻¹ Σ_(j=0)^(N−1) a^j S^j,

so every entry is rational and every annihilating-Q projection is zero. A cyclic first-order recurrence evaluates C in O(N) rational arithmetic operations, with coefficient preparation and final normalization charged. There are zero nonrational scalar multiplications.

In Fourier coordinates its diagonal entries are μ_k=(1−aζ_N^k)⁻¹, up to a harmless index sign convention. Such μ_k is rational exactly when ζ_N^k is rational, because a≠0 and ζ_N^k=(1−μ_k⁻¹)/a. Hence the isolated diagonal has N−gcd(N,2) nonrational entries, and is optimally that expensive in §5's model, while the complete Fourier–diagonal–inverse-Fourier product has zero nonrational complexity. This is a concrete, all-input fusion countercontrol. It does not provide a speedup for a general Fourier target.

Consequently the reviewed inverse-multiplier error/preparation contract and these exact algebraic obstructions may be used together only with their separate hypotheses retained: nonzero spectrum, paid multiplier preparation, precision and conditioning for numerical use; actual whole-target scalar circuit for gate counts. A finite-word approximation theorem may use nonlinear rounded operations and is not constrained by §4 without another model argument.

## 8. Independent controls and source status

The source Library ZIP is `[private-id]`, filename `fft_hero1_phase30_20261010.zip`, SHA-256 `10be5f81e18be5f5f8d6bf00fa1de4d61f640b32597d499de7ce85409e0ec664`. `SOURCE_MANIFEST.json` records all 39 member hashes, including source theorem and nested Phase29 archive. Only text and JSON members were extracted for this audit. Source Python and shell files remained inert.

The source conversation reader returned visible user continuations but omitted the assistant messages. Mathematical attribution therefore rests on the exact ZIP, not on inaccessible conversation text: [private source omitted] .

`fresh_rank_controls.py` constructs cyclotomic polynomials by exact division of x^n−1, builds power-basis vectors by reduction, constructs abelian character exponents directly, and finds fresh functional coordinates independently. It checks 37 groups (22 cyclic, 15 noncyclic), 111 fresh matrices and 222 modular rank certificates over 998244353 and 1000000007. Every selected nonzero minor is recorded with explicit original row/column indices and its determinant; a separate elimination recomputes that minor. Small cases also have exact Fraction elimination. Orbit-indicator nullspaces are checked over the integers.

The 44 supplied cyclic traceless/full functional vectors were independently rebuilt as data and rechecked in both primes. The source abelian JSON does not include its functionals, so those particular numeric determinants were not replayed; instead all 15 groups were checked with newly supplied explicit functionals. This distinction is retained in the result receipt.

`fresh_edge_controls.py` independently constructs the unit group's characters and checks 27 exact spectral profiles, scalar twists, the tensor mismatch and exact F_4²=4J cancellation. It imports only the new control module in this folder. Nine dyadic isolated-twiddle counts h=1 through256 were independently counted. All controls pass. These are exact finite witnesses, not a machine-checked proof of the general theorem and not evidence about source-program operation counts or numerical stability.

## 9. Remaining work and stopping boundaries

- Use the complete theorem as an exact rejection check for fully specified scalar-linear candidates. Record the base field, real/complex wire convention, scalar normalization, coefficient setup, and total additions as separate fields.
- Search genuine whole-product rewrites, rather than attempt to beat an isolated diagonal's exact scalar-gate count at greater depth. The rational Green inverse in §7.3 demonstrates the relevant cancellation mechanism but does not resolve the nonrational DFT target.
- Obtain and compare the full Auslander–Feig–Winograd 1984 and Tolimieri 1986 texts before any novelty statement. Closely related classical rational-subspace / multiplicative-character theory is already identified; primary abstract access is not theorem-by-theorem inspection.
- No finite-field, bounded-word, approximate, or unrestricted nonlinear-circuit extension is claimed without a separate proof. No Ω(N log N) statement follows from a lower bound of N−τ(N).
