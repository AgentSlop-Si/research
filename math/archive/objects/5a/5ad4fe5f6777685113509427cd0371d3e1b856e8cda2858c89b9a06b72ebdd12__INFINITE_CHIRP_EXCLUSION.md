# An explicit infinite family excluded from two diagonal-ended cycle Green sums

## Theorem and exact scope

Let q be a positive odd integer with gcd(q,5)=1 and q≡1 (mod 241), and let N=5q². For any specified primitive complex Nth root ω, define

- F_N[i,j]=ω^(ij), the unnormalized positive-exponent Fourier matrix;
- h=(N+1)/2 and A_N=diag(ω^(h j²));
- B_N=(F_N^(-1)+A_N)^(-1).

Then B_N is well-defined and there do not exist two Hamiltonian structural cycles σ₀,σ₁ on the fixed N coordinates, arbitrary complex row edge weights w₀,w₁, and arbitrary diagonal endpoint matrices L₀,R₀,L₁,R₁ such that

    B_N=L₀(I-W₀)^(-1)R₀+L₁(I-W₁)^(-1)R₁,
    (W_b x)_i=w_b(i)x_(σ_b(i)),
    1-∏_i w_b(i)≠0 for b=0,1.

Zero edge weights and singular endpoint masks are included. In particular q=2410k+1, k=0,1,2,… gives an explicit infinite sequence N=5(2410k+1)². Its first lengths are 5, 29,064,605 and 116,210,205.

This is an infinite family of exact representation exclusions for the specified forced chirp B. It is not a lower bound for arbitrary Fourier algorithms, a claim about every length, a speedup, or an exclusion of unmatched endpoint permutations, other feedback choices, more summands, or products of Green sums. The N=3 positive control from the predecessor work is unaffected.

The sole computational exclusion input is the accepted all-order N5 certificate: at p=241 and ζ₅=91 its closed projective necessary system has no point over the algebraic closure, for all 24²=576 ordered Hamiltonian-cycle pairs. That input includes endpoint boundaries and is independently audited in `source/ACCEPTED_N5_REVIEW.md`. This report supplies the restriction, arithmetic and specialization argument needed to pass from that finite certificate to the infinite theorem. The former draft is preserved verbatim as `source/PREDECESSOR_EXTENSION.md`; it additionally treats a generic positive-sign parameter curve. The theorem here does not depend on that generic-curve corollary or an uncomputed eliminant.

## 1. Principal restriction preserves the precise Green grammar

Over any field, let σ be one N-cycle and W the row-action weighted cycle above. Write ρ=∏_i w(i). Since W^N=ρI, for 1-ρ≠0,

    (I-W)^(-1)=(I+W+⋯+W^(N-1))/(1-ρ).                  (1)

Choose any nonempty set S, and list its elements in whatever coordinate order is wanted for the principal submatrix. Starting at each s∈S, follow σ to the next vertex σ_S(s)∈S. Let ℓ_s≥1 be that first return length and

    w_S(s)=∏_(t=0)^(ℓ_s-1) w(σ^t(s)).

The arcs partition the N structural edges. Thus σ_S is one |S|-cycle, ∑_sℓ_s=N and ∏_s w_S(s)=ρ. If W_S uses σ_S and these effective weights, then

    [(I-W)^(-1)]_[S,S]=(I-W_S)^(-1).                   (2)

Indeed, for distinct i,j∈S, the numerator entry in (1) is the product along the unique forward path from i to j of length less than N. Decomposing that path into retained arcs gives exactly the numerator in the |S|-cycle version of (1). The two diagonal numerators are 1, and the denominators agree. For |S|=1, the effective loop has weight ρ and both sides are 1/(1-ρ).

No edge is divided out. Thus the proof includes zero edges, zero effective arcs, and arbitrary reordered retained coordinates. It also proves exact preservation of the inverse guard: an excluded ρ=1 remains excluded after restriction.

For diagonal L,R, matrix multiplication gives

    [L(I-W)^(-1)R]_[S,S]=L_[S,S](I-W_S)^(-1)R_[S,S].   (3)

This identity includes singular L,R. Applying it separately to two branches preserves their sum; the two induced cyclic orders may be different. In particular, any permitted N-coordinate representation restricts to a permitted five-coordinate representation in the all-order N5 universe. Unmatched endpoint permutations would destroy this direct principal-block statement, which is why they are not included.

## 2. Direct chirp formula, retaining every scalar and sign

For any odd N and primitive ω, define G_N=∑_(j=0)^(N-1)ω^(h j²), Fbar[i,j]=ω^(-ij), M=F_N A_N and c=N G_N. Completion of the square modulo N uses 2h≡1:

    h j²+(i+k)j=h(j+i+k)²-h(i+k)².

Consequently

    M²=G_N A_N^(-1)Fbar,     M³=N G_N I=cI.

If 1+c≠0, then (I+M)^(-1)=(I-M+M²)/(1+c), and therefore

    B_N=[F_N-F_N A_N F_N+c A_N^(-1)]/(1+c),
    B_N[i,j]=[ω^(ij)-G_N ω^(-h(i+j)²)
                  +N G_N ω^(-h i²)δ_ij]/(1+N G_N).     (4)

No normalized Fourier matrix or unspecified Gauss sign is substituted. The identity follows by direct finite sums, and remains valid over a splitting field of characteristic not dividing 2N whenever its separate denominator guard holds.

Set m=q², N=5m, and retain S=(0,m,2m,3m,4m) in that order. Put η=ω^(m²)=ω^(q⁴). Since gcd(q,5)=1,

    ord(η)=N/gcd(N,q⁴)=5.

As h≡3 (mod5), define the five-coordinate matrices

    F(η)[a,b]=η^(ab),
    C(η)[a,b]=η^(-3(a+b)²),
    D(η)[a,b]=η^(-3a²)δ_ab.

Substitution in (4) gives the exact principal block

    B_N[S,S]=[F(η)-G_N C(η)+N G_N D(η)]/(1+N G_N).     (5)

## 3. Elementary CRT and square-modulus Gauss arithmetic

Every x modulo N=5q² has a unique expression

    x=q²u+5v,    u modulo5, v modulo q².

This follows since the map is injective modulo5 and modulo q² when gcd(5,q)=1. The cross term in h(q²u+5v)² is divisible by N. With ξ=ω^5, an exact primitive q²-th root, the sum separates:

    G_N=(∑_(u mod5)η^(h u²))
        (∑_(v mod q²)ξ^(5h v²)).                      (6)

The first factor is g=G₅(η)=1+2(η²+η³). To evaluate the second without a square-root convention, let a be any integer coprime to q. For q>1 write v=s+qt, 0≤s,t<q. Then

    ∑_(v mod q²)ξ^(a v²)
      =∑_(s modq)ξ^(a s²)∑_(t modq)(ξ^q)^(2ast)=q.   (7)

Because q is odd and gcd(a,q)=1, the inner geometric sum is zero unless s=0, and equals q there. In (6), a=5h is a unit modulo q: 2h≡1 (modq) and gcd(5,q)=1. The case q=1 has the same value directly. Hence, for every supplied primitive ω, including composite q,

    G_(5q²)=q G₅(η)=qg.                               (8)

No Legendre/Jacobi sign choice or ambient root reduction was used. Reducing the polynomial g² modulo Φ₅(η)=1+η+η²+η³+η⁴ gives g²=5. Thus the principal block is the matrix over K=Q(η)

    T_q(η)=[F(η)-qg C(η)+5q³g D(η)]/D_q,
    D_q=1+5q³g.                                       (9)

Moreover (1+5q³g)(1-5q³g)=1-125q⁶≠0 for positive q, so D_q≠0 in characteristic zero. This proves the required nonresonance and the existence of B_N in the theorem.

The five-coordinate block lies in Q(η) before specialization. It is generally not B₅: F,C,D are linearly independent because the off-diagonal ratios C[0,1]/F[0,1]=η² and C[0,2]/F[0,2]=η³ differ, and D is nonzero diagonal. Comparing (9) with its q=1 instance would first force equal F coefficients, then qg=g, hence q=1. For every q>1 the actual complex block differs from B₅.

## 4. The ring of definition and the exact special fiber

Use the abstract cyclotomic ring O=Z[t]/(Φ₅(t)), with K its fraction field, and write g(t)=1+2(t²+t³). The map

    O → F₂₄₁,    t↦91

is well-defined because Φ₅(91)=0 (mod241); its kernel is the maximal ideal 𝔭=(241,t-91). Let R=O_𝔭. This is an integral local ring with fraction field K and residue field F₂₄₁. Every specified primitive complex η supplies an embedding K→C by t↦η.

At the residue map,

    ord(91)=5,   g(91)=103,
    q≡1,   5q³g≡33,   D_q≡34≠0 (mod241).             (10)

Thus D_q is a unit in R; all entries of (9) belong to R. Their reduction is exactly

    [[161, 20,102,102, 20],
     [ 20,182, 62, 26, 92],
     [102, 62,236, 28, 26],
     [102, 26, 28,236, 62],
     [ 20, 92, 26, 62,182]],                           (11)

the N5 target excluded by the accepted certificate. The modular identity is universal in q≡1 (mod241), not an inference from finitely many samples.

There is no map here sending a primitive Nth root to a fifth root. Only the already descended K-valued block is reduced. If an ambient prime is desired, a prime above 𝔭 exists in the ring of integers of Q(ω) by integrality and lying over. Since 241∤N, the reduction of ω still has order N, possibly over a larger residue field: otherwise its reduction would be a root of both Φ_N(X) and X^d-1 for a proper divisor d of N, contradicting squarefreeness of X^N-1 in characteristic241. The latter polynomial is squarefree since its derivative is N X^(N-1). This optional ambient explanation is not needed for the proof.

## 5. The closed projective necessary system and properness

Fix one of the 576 ordered pairs π,τ of five-coordinate cycles. Give row i of U a projective direction at positions i,π(i), and column j of V a projective direction at rows j,τ^(-1)(j). Thus directions live in (P¹)^10; individual direction coefficients may be zero, but each pair is nonzero. For target T put K_T=UTV. Impose:

1. K_T[i,j]=0 whenever j∉{i,π(i),τ(i)};
2. every 11-by-11 minor of the 25-by-11 matrix whose equation row (i,j) has V[i,j] in scale column x_i, U[i,j] in scale column y_j, and K_T[i,j] in its last column, all other scale entries being zero.

An invertible-branch Green sum yields these conditions from

    Q₀ T Q₁=Q₀+Q₁,
    Q₀=D_ρ U, Q₁=V D_τ,
    U T V=D_x V+U D_y.

For a singular endpoint representation, replace zero endpoint entries by ε, keeping weights and legal Green denominators fixed. Over C((ε)) the endpoints and branches are invertible. Normalize each inverse row/column direction by its minimum ε valuation. Its reduction is a nonzero projective pair. The multihomogeneous equations specialize to zero, so the original singular representation also supplies a point of the necessary system. This uses no surviving affine scale or base-coordinate guard.

For completeness, rescaling U to D_λU and V to VD_μ multiplies equation row (i,j) by λ_iμ_j and divides coefficient columns x_i,y_j by λ_i,μ_j respectively. A full 11-column minor using equation rows E is multiplied by

    ∏_i λ_i^(n_i-1) ∏_j μ_j^(m_j-1),

where n_i,m_j count occurrences in E. If some count is zero its corresponding scale column is zero, making the minor identically zero. Every nonzero minor therefore has nonnegative multidegrees. The off-support equations and these minors define a closed subscheme X_(π,τ)(T) of (P¹_R)^10 when T∈Mat₅(R). No Green-denominator inequality, invertibility inequality or normalization patch is included in that closed system.

For T=T_q, (10)–(11) make its geometric special fiber exactly the accepted N5 necessary system, which is empty for every π,τ. The morphism X_(π,τ)(T_q)→Spec R is proper: projective space is proper, products of proper schemes are proper, and closed immersions are proper. These facts are stated in [Stacks, projective morphisms](https://stacks.math.columbia.edu/tag/01WC) and [Stacks, proper morphisms](https://stacks.math.columbia.edu/tag/01W0), checked on 2026-10-10.

If the complex fiber under any K→C embedding had a point, the generic fiber over K would be nonempty. The image of a proper morphism is closed, so an image containing the generic point of the integral local base contains its closed point. This would give a nonempty geometric special fiber, a contradiction. Therefore no allowed two-Green representation of T_q exists. Finally, (2)–(3) and (5) show that any claimed representation of the full B_N would restrict to one of T_q. This proves the theorem.

The specialization lifts emptiness of a closed projective system. It does not promote an affine inconsistency, an open inverse guard, or a finite-field nonexistence search restricted to rational points.

## 6. Executed controls and dependency boundary

`check_certificate.py` is newly authored standard-library Python. It neither imports nor executes a predecessor/uploaded program. Its exact controls include:

- 1,470 legal principal Green restrictions at N=1,…,7, covering all nonempty subsets, reordered retained coordinates, different structural orders, variable/nonzero, one-zero and all-zero weights; 16,869 Green entries and the same number of singular-endpoint entries are checked.
- Every tested illegal unit-product guard remains singular after restriction; singleton loops and one two-summand N11 positive control with distinct induced orders are included.
- 24 square-modulus CRT/Gauss cases at q=1,3,7,9,11,13,21,27 and three supplied primitive roots each. Complete CRT residue bijections and the individual inner character-sum cancellations are checked, including non-squarefree composite q.
- Nine direct finite-field inversions of F_N^(-1)+A_N at N≤65 verify their 25 retained entries against (5). These are exact finite controls, not a method for applying B_N cheaply.
- The polynomial reduction g²=5, target (11), guard34, and all 25 entries of six explicit sequence parameters are checked. A coefficient-divisibility check separately verifies the universal congruence (1+2410k)³≡1 (mod241).
- Two deliberate N5 resonances in F31 reject the zero feedback denominator before inversion.

These computations support the all-length proof; they do not replace it. The 576-pair N5 emptiness theorem is an explicitly identified, independently audited predecessor, not a claim to have rerun its entire enumeration in this script. The source report, accepted audits and hashes are preserved as inert data. See `EXACT_RESULTS.json`, `CHECK_RUN.log`, `REPRODUCE.md`, and the sealed manifest.

## 7. Completion status

The requested explicit infinite-subfamily construction, guard accounting and proof are complete. No expanded generic eliminant, numerical all-length cutoff, negative-sign generic anchor, large dense Fourier matrix, admissible B generator, or application complexity improvement is supplied or needed for this theorem. Independent review of this new extension remains a separate artifact; its acceptance does not alter the stated grammar or target scope.
