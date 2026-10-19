# C8 unrestricted phase minimax: quantitative global bound and strict local certificate

19 October 2026 UTC. The unrestricted value is not determined here. This packet proves a coarse explicit global lower bound and a strict local minimum in all phase directions at the previously accepted upper witness. These statements do not imply global optimality.

## 1. Scope and prerequisites

Let F[j,k] = exp(−π i j k/4)/sqrt(8), with indices 0 through 7. Write

    δ = min over diagonal unitary P,Q of σ₃(Im(PFQ)).

The singular values are in decreasing order. The accepted equivalence to the original unrestricted-real-core, complex-rank-one approximation problem is unchanged. We use two previously accepted statements, whose source and independent review are frozen in `sources/`:

1. δ ≤ s = sin(π/16), attained by the witness below.
2. Every pair with p[j+4]²=p[j]² and q[k+4]²=q[k]² has σ₃(Im(PFQ)) ≥ s.

No old research program is executed. The new characteristic-zero checker verifies the finite identities used in the local argument.

## 2. A global explicit lower bound

### Theorem 1

For every diagonal unitary P,Q,

    σ₃(Im(PFQ)) ≥ sin(π/16) / sqrt(13 + 4 sqrt(3) cos(π/16)).

Thus

    0.0438487379148837407… ≤ δ ≤ 0.1950903220161282678… .

The decimal is illustrative; the displayed radical/trigonometric expression is the exact lower constant.

### 2.1 Energy localizes phases near the periodic sector

Put Y=Im(PFQ), τ=σ₃(Y), E=||Y||_F², a_j=p_j², b_k=q_k². The real imaginary-part contraction gives ||Y||₂≤1, so

    E ≤ 2 + 6τ².                                           (2.1)

Let J exchange j and j+4, Π=(I+J)/2, and H[j,k]=exp(−π i j k/2). Direct Fourier orthogonality gives H*H=HH*=16Π and HΠ=ΠH=H. The standard energy identity is

    E = 4 − Re(aᵀ H b)/16.

Set A=||(I−Π)a||² and B=||(I−Π)b||². Since ||a||²=||b||²=8,

    Re(aᵀ H b) ≤ 4 sqrt((8−A)(8−B)),
    E ≥ 4 − sqrt((8−A)(8−B))/4 ≥ 2+(A+B)/8.               (2.2)

The last inequality is the arithmetic-geometric mean inequality. Combining (2.1) and (2.2) gives A+B≤48τ². This is a quantitative estimate, not the invalid assertion that A=B=0 at positive error.

Independent real row and column signs do not affect any singular value of Y. Choose these signs so that each phase pair can be written

    p_r = exp(iα_r+iρ_r),       p_{r+4}=exp(iα_r−iρ_r),
    q_r = exp(iβ_r+iη_r),       q_{r+4}=exp(iβ_r−iη_r),

where |ρ_r|,|η_r|≤π/4. This is possible by choosing the relative phase of each pair modulo π. Then

    A=2 Σ_r sin²(2ρ_r),       B=2 Σ_r sin²(2η_r),
    Σ_r sin²(2ρ_r)+Σ_r sin²(2η_r) ≤24τ².                   (2.3)

If τ≥1/sqrt(24), Theorem 1 is immediate. Otherwise let u=max|ρ_r| and v=max|η_r|. Equation (2.3) gives sin²(2u)+sin²(2v)≤24τ²<1. For 0≤a,b≤π/2 with sin²a+sin²b<1, one has a+b<π/2 and

    sin²a+sin²b = 1−cos(a+b)cos(a−b) ≥ 1−cos(a+b)
                = 2 sin²((a+b)/2).

Apply this with a=2u,b=2v to obtain

    u+v ≤ arcsin(sqrt(12) τ).                              (2.4)

### 2.2 Angular perturbation estimate

Here is an elementary real-subspace proof, supplied and checked independently in `REVIEW.md`. Regard complex Euclidean space as a real Euclidean space. For a unit vector z, its angle to the real subspace R⁸ is arcsin(||Im z||). If a diagonal unitary D has arguments bounded in absolute value by a≤π/2, then

    Re(z*Dz) ≥ cos(a).

Thus D moves every unit vector through an angle at most a. By the angular triangle inequality, its distance to R⁸ can increase by at most a.

Let U be unitary. On a real six-dimensional subspace attaining the singular-value min–max formula for σ₃(Im U), every unit x has ||Im(Ux)||≤σ₃(Im U), and ||Ux||=1. Apply the preceding pointwise angle estimate to Ux, and use that same real subspace in the min–max formula for Im(DU). This gives

    arcsin σ₃(Im(DU)) ≤ arcsin σ₃(Im U)+a.

If the right side exceeds π/2, the inequality is automatic; otherwise take sine, apply the min–max formula, and take arcsine. The right-multiplication version follows by transposition, because Uᵀ is unitary and singular values are unchanged by transposition. Reversing both rotations gives the absolute-value version. In particular, for two diagonal phase rotations with arguments bounded by a and b,

    |arcsin σ₃(Im(D₁UD₂)) − arcsin σ₃(Im U)| ≤ a+b.       (2.5)

This proof requires no differentiable eigenvalue branches and works at multiple singular values.

Let P₀,Q₀ be the four-periodic phases obtained by replacing every ρ_r and η_r by zero. The path from P₀FQ₀ to PFQ has speeds u and v. The accepted sector theorem and (2.4)–(2.5) therefore imply

    π/16 ≤ arcsin τ + arcsin(sqrt(12) τ).                  (2.6)

The right side is increasing. Its equality solution is

    τ₀ = s / sqrt(s²+(sqrt(12)+c)²)
       = s / sqrt(13+4 sqrt(3)c),       c=cos(π/16).

Both inverse-sine arguments lie in [0,1] at this solution, and the corresponding sum is π/16. This proves Theorem 1.

## 3. Strict local optimality across all phases

### Theorem 2

At the accepted witness, σ₃(Im(PFQ))=s is a strict local minimum modulo the unavoidable scalar transfer (P,Q)↦(e^{it}P,e^{−it}Q). In particular, sufficiently small genuinely nonperiodic phase perturbations cannot give a counterexample to the conjectured global value s.

This is a local existence statement. No explicit radius, global basin, uniqueness of global minimizers, or global lower bound s is asserted.

### 3.1 Exact matrices and coordinates

Let z=exp(iπ/16),

    q=(1,z²,1,z¹⁰,1,z²,1,z¹⁰),  Q=diag(q),  P=zQ,
    V₀=PFQ=X+iY,
    a=(1,0,−1,0,−1,0,1,0)ᵀ/2,
    b=(0,1,0,1,0,1,0,1)ᵀ/2,
    R=aaᵀ+bbᵀ,       L=I−R,       γ=c²−s²=cos(π/8)>0.

The baseline identities are

    YᵀY=s²L+c²R,     rank L=6,     rank R=2.

For phase perturbations x_j,y_k, write

    V(h)=diag(exp(ix_j)) V₀ diag(exp(iy_k)),
    D[j,k]=x_j+y_k,
    Im V(h)=Y+Y₁+Y₂+O(||h||³),
    Y₁=X∘D,       Y₂=−Y∘D∘D/2,
    H(h)=(Im V(h))ᵀ Im V(h)=H₀+H₁+H₂+O(||h||³),
    H₁=YᵀY₁+Y₁ᵀY,
    H₂=Y₁ᵀY₁+YᵀY₂+Y₂ᵀY.

The symbol ∘ is entrywise multiplication. Split the phases as

    x_r=α_r+ρ_r,       x_{r+4}=α_r−ρ_r,
    y_r=β_r+η_r,       y_{r+4}=β_r−η_r.

Fix β₀=0 by scalar transfer. This is a valid smooth coordinate chart on the 15-dimensional phase quotient near the witness. Let

    μ=(α₀,α₁,α₂,α₃,β₁,β₂,β₃),
    ν=(ρ₀,ρ₁,ρ₂,ρ₃,η₀,η₁,η₂,η₃).

### 3.2 Exact first- and second-order certificate

Define the symmetric operators, supported on L,

    G=LXYL/(sc),
    Ω=(3L−G)/16.

Because V₀ is symmetric unitary, X and Y are real symmetric and commute. Moreover R=(Y²−s²I)/γ, so X and Y commute with R and L. Thus G and Ω are real symmetric. The exact identities are

    G²=L,       tr G=2,
    Ω|_L has eigenvalues 1/8 (four times), 1/4 (twice),
    tr Ω=1.

Thus Ω is positive definite on the six-dimensional low spectral space.

Let A(h)=LH₁(h)L. The checker verifies:

1. A depends only on μ; all eight coefficients in ν vanish.
2. tr(Ω A(h))=0 in every one of the fifteen directions.
3. The seven μ-coefficient matrices A_k are linearly independent. Explicitly, their Gram matrix, divided by (sc)², is

       5 0 1 0 1 2 1
       0 5 0 1 2 1 2
       1 0 5 0 1 2 1
       0 1 0 5 2 1 2
       1 2 1 2 5 0 1
       2 1 2 1 0 5 0
       1 2 1 2 1 0 5

   Its determinant is 12288.
4. For every ν, setting μ=0 gives the exact quadratic identity

       tr Ω[H₂(0,ν) − H₁(0,ν) R H₁(0,ν)/γ]
           = κ ||ν||²,       κ=cos(π/8)/(4 sqrt(2))>0.     (3.1)

Identity (3.1) is verified coefficientwise for all 36 entries of the symmetric eight-variable quadratic-form matrix. It is not a numerical Hessian estimate. The rank-seven first-variation calculation and the positive scalar κ are the new mechanism that handles nonperiodic directions locally.

### 3.3 The low-cluster reduction and its correction term

The eigenvalue s² of H₀ is separated from c² by γ>0. For h near zero, the invariant six-dimensional low spectral space is an analytic graph over L. Writing its graph map as Z(h):L→R gives

    Z(h)=−R H₁(h)L/γ+O(||h||²).

Use the orthonormal graph embedding (I+Z)(I+ZᵀZ)^(−1/2). The resulting real symmetric operator K(h) on the fixed space L has exactly the six low eigenvalues of H(h), and expansion

    K(h)=s² I_L + A(μ)
       + L[H₂(h)−H₁(h)R H₁(h)/γ]L + O(||h||³).          (3.2)

The negative resolvent term is essential. It accounts for movement of the spectral subspace. Omitting it fails the exact coefficient check. Since the other two eigenvalues remain separated above these six, σ₃(Im V(h))²=λ_max(K(h)).

### 3.4 Why the certificate proves a strict minimum

For every μ≠0, A(μ) is nonzero, symmetric, and has Ω-weighted trace zero. Because Ω is positive definite on L, A(μ) cannot be negative semidefinite. Thus λ_max(A(μ))>0. By compactness on the unit sphere in the seven μ-coordinates, there is a constant k>0 such that

    λ_max(A(μ)) ≥ k||μ||.                                 (3.3)

Suppose there were nonzero h_n=(μ_n,ν_n)→0 with λ_max(K(h_n))≤s². Equations (3.2)–(3.3) force

    ||μ_n||=O(||h_n||²).

Apply tr Ω to (3.2). The linear term vanishes. The full quadratic coefficient differs from its μ=0 value by O(||μ_n||||h_n||), because it is a quadratic form. Hence (3.1) gives

    tr Ω(K(h_n)−s² I_L)
       = κ||ν_n||² + O(||μ_n||||h_n||)+O(||h_n||³)
       = κ||h_n||² + O(||h_n||³) > 0

for all sufficiently large n. This contradicts λ_max(K(h_n))≤s² and tr Ω=1, Ω≥0. Therefore there is a neighborhood in which every nonzero quotient phase perturbation has σ₃(Im V(h))>s. Theorem 2 follows.

## 4. What remains global

Neither theorem proves δ=s. A globally better point could lie outside the local neighborhood. The remaining exact spectral anti-concentration lemma, equivalent to the requested sharp lower bound and avoiding the earlier 78-variable frame formulation, is stated in `GLOBAL_LEMMA.md`. No proof or exact counterexample for that lemma is supplied.
