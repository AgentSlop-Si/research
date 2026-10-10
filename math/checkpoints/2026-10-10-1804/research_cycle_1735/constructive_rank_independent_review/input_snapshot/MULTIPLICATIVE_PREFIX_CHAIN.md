# A subgroup-ordered cancellation chain with growing aggregate savings

10 October 2026. New constructive continuation; earlier accepted files remain unchanged.

## Result and scope

Let p≥5 be prime, N=p−1, and write N as a product of primes, with repetition,

    N = q₁⋯qᵣ,
    W(N) = Σⱼ (1−1/qⱼ) = Σ_{q prime} v_q(N)(1−1/q).

There is an explicit square-invertible, separately colored aggregate Gauss graph with the exact count

    E(p) = 2p²+2p−2 − (p−1)W(p−1).

Its saving relative to the dense aggregate count 2p²+p is

    Δ(p) = (p−1)W(p−1) − (p−2).

In particular, for every prime p≥5,

    E(p) ≤ 2p²+(p+3)/2,
    Δ(p) ≥ (p−3)/2.

This strictly improves the previously accepted packed four-chain count for every p≥7 and agrees with its 54-edge witness at p=5. The improvement is stronger when p−1 has many prime factors. For example:

| p | prime factors of p−1 | Fourier zeros Z | total E | saving Δ |
|---:|:---|---:|---:|---:|
| 5 | 2,2 | 4 | 54 | 1 |
| 7 | 2,3 | 7 | 103 | 2 |
| 11 | 2,5 | 13 | 249 | 4 |
| 13 | 2,2,3 | 20 | 342 | 9 |
| 17 | 2,2,2,2 | 32 | 578 | 17 |
| 31 | 2,3,5 | 59 | 1923 | 30 |
| 97 | 2,2,2,2,2,3 | 304 | 18706 | 209 |
| 257 | eight copies of 2 | 1024 | 131586 | 769 |

The saving divided by p is unbounded along an unconditional sequence of primes. More quantitatively, prime divisors of Fermat numbers give Ω(p log log p) savings along a sequence, without assuming infinitely many Fermat primes. Section 7 proves this elementary corollary.

The graph and its literal coefficient table remain quadratic. One endpoint is the dense Fourier matrix; this is neither a subquadratic FFT nor a global minimum theorem. Every color slice is charged separately, including any overlapping locations.

## 1. The exact prefix-zero identity

Let ζ=exp(2πi/p), and F[i,t]=ζ^(it), with indices in F_p. Put

    βₙ = ζ^(n+1) − ζ^(−n−1),       0≤n≤p−2.

Every βₙ is nonzero: otherwise 2(n+1)=0 modulo p, impossible in this index range.

For any nonempty set T⊆F_p* define the polynomial on the root grid

    Q_T(ζ^t) = Σ_{x∈T} β_(x−1) ζ^((x−1)t)
             = ζ^(−t) [ Σ_{x∈T} ζ^((t+1)x) − Σ_{x∈T} ζ^((t−1)x) ].

Write

    H(T) = {a∈F_p*: aT=T}

for its multiplicative stabilizer, which is a subgroup of F_p*.

**Lemma 1.** Q_T has exactly |H(T)|−1 zeros on the pth-root grid.

**Proof.** A rational linear relation among 1,ζ,…,ζ^(p−1) has all its coefficients equal, since the minimal polynomial is 1+X+⋯+X^(p−1). The signed coefficient sum in the displayed difference is zero. Consequently its vanishing is equivalent to equality of the two exponent multisets

    (t+1)T = (t−1)T.

At t=1 or t=−1 one side is supported only at exponent zero and the other side has no exponent zero, so equality is impossible. At other t both multipliers are nonzero, and equality is equivalent to

    λ_t = (t+1)/(t−1) ∈ H(T).

The map t↦λ_t bijects F_p\{1,−1} with F_p*\{1}; its inverse is t=(λ+1)/(λ−1). Thus there is exactly one grid zero for each member of H(T) other than 1. ∎

This is an exact characteristic-zero cyclotomic cancellation statement. The finite-field set calculation labels exponents; it is not substituting a finite-field matrix computation for a complex one.

## 2. A hierarchical order with completely known prefix stabilizers

Define d₀=1 and dⱼ=q₁⋯qⱼ. Let Hⱼ be the unique subgroup of F_p* of order dⱼ. Choose an ordering x₁,…,x_N of F_p* in which every aligned block of dⱼ consecutive entries is a coset of Hⱼ, for every j.

Such an order is explicit. Choose a primitive root g modulo p. Let L₀=(0) be a list of exponents modulo N and form recursively

    Lⱼ = concatenation over a=0,…,qⱼ−1 of [ e+aN/dⱼ : e∈L_(j−1) ].

Take x₁,…,x_N to be g raised to the entries of Lᵣ. The recursion enumerates every exponent once and has the stated coset-block property.

For 1≤L≤N put T_L={x₁,…,x_L}. Let j(L) be the largest j for which dⱼ divides L; set j(N)=r.

**Lemma 2.** The prefix stabilizer is exactly

    H(T_L)=H_(j(L)).

**Proof.** Complete dⱼ-blocks show that Hⱼ stabilizes T_L. If L<N and j=j(L), then T_L consists of some complete H_(j+1)-cosets, one nonempty proper partial H_(j+1)-coset, and no elements in the remaining cosets. Multiplication by any stabilizer element must carry this unique partial coset to itself. It therefore lies in H_(j+1). The quotient H_(j+1)/Hⱼ has prime order q_(j+1), so a subgroup between Hⱼ and H_(j+1) is one of those two groups. The latter would fill the partial coset, a contradiction. Hence the stabilizer is Hⱼ. At L=N the set is all of F_p*, with stabilizer Hᵣ. ∎

Combining the two lemmas, the Lth prefix has exactly d_(j(L))−1 grid zeros. Counting L divisible by dⱼ but not by d_(j+1), and then the final L=N, gives

    Z = Σ_{L=1}^N (d_(j(L))−1)
      = [N + Σ_{j=0}^{r−1} dⱼ(N/dⱼ−N/d_(j+1))] − N
      = N Σ_{j=1}^r (1−1/qⱼ)
      = N W(N).

The total is independent of the ordering of the prime factors. The per-color distribution may depend on that order.

## 3. The endpoint matrix and its Fourier factor

Set n_L=x_L−1 in the ordinary index range 0,…,p−2. Use these N indices in one directed chain and leave index p−1 as an isolated identity block. Define

    C = I − Σ_{L=2}^N [β_(n_(L−1))/β_(n_L)] E_(n_L,n_(L−1)).

The links are nonzero, C is unit lower triangular in chain order, and

    nnz(C)=p+(N−1)=2p−2.

Let R=C⁻¹F. The recurrence CR=F gives the explicit rows

    R[n_L,t] = Q_(T_L)(ζ^t)/β_(n_L),
    R[p−1,t] = ζ^((p−1)t).

Indeed the row equation subtracts the preceding prefix from the current one, leaving β_(n_L)ζ^(n_L t). Therefore

    nnz(R)=p²−Z=p²−(p−1)W(p−1).

There is no numerical fitting and no uncharged inverse evaluation. If desired, the inverse itself has the explicit formula

    C⁻¹[n_L,n_M] = β_(n_M)/β_(n_L) for M≤L,
    C⁻¹[p−1,p−1]=1,

and all its other entries are zero. Hence

    nnz(C⁻¹)=N(N+1)/2+1,
    nnz(C⁻¹)−nnz(C)=(N−1)(N−2)/2.

For a more detailed colored ledger, let t≠±1 and let j be the first index with λ_t∈Hⱼ. Since λ_t≠1, j≥1. Exactly the prefix lengths divisible by dⱼ vanish at this t, so

    r_t=nnz(R[:,t])=p−N/dⱼ.

At t=±1, r_t=p. There are dⱼ−d_(j−1) colors in the jth case, and these counts sum to p−2. This independently recovers the total Z.

## 4. Full separately colored aggregate graph

Take A=F, so S=FA⁻¹=I. Put h=2⁻¹ modulo p and define

    B_t=ζ^(−h t²) R[:,t] e_tᵀ.

For every output i, input j, and separately labeled color t,

    (C B_t A)[i,j]
      = ζ^(−h t²) (CR)[i,t] F[t,j]
      = ζ^(−h t²) ζ^(it) ζ^(tj).

Thus every required color fiber is correct, including its cancellation. The slices happen to use distinct middle columns, but no merging of colors is used in the count. The complete ledger is

    input endpoint A:             p²,
    output endpoint C:            2p−2,
    colored middle edges:         p²−Z,
    total:                        2p²+2p−2−Z.

Let G=Σ_t ζ^(−h t²). Completing the square gives

    (C (Σ_t B_t) A)[i,j] = G ζ^(h(i+j)²).

The elementary Gauss norm identity gives |G|²=p, so G≠0. Absorb G⁻¹ζ^(−h i²) into output row i of C and ζ^(−h j²) into input column j of A. These are all nonzero endpoint scalars and preserve every charged support. The resulting ordinary transfer is F exactly; no extra uncharged layer is introduced.

The construction genuinely escapes the fixed-gauge pointwise character condition. The first chain vertex receives every color because its R row is a nonzero character. Its C column has nonzero entries at two distinct outputs n₁,n₂. Their fixed weight ratio cannot equal a fixed endpoint-gauge ratio times ζ^((n₂−n₁)t) for both t=0 and t=1. Thus the saving requires aggregate cancellation, not a disguised pointwise witness.

## 5. Uniform improvement over the four-chain family

Write N=2M, M≥2. For positive integers a,b≥2,

    (1−1/a)+(1−1/b) − (1−1/(ab)) = (a−1)(b−1)/(ab)>0.

Applying this repeatedly to the prime factors of M gives

    W(N) ≥ 1/2 + (1−1/M) = 3/2−2/N.

It follows that Z≥3N/2−2=(3p−7)/2 and

    Δ(p)≥(p−3)/2,
    E(p)≤2p²+(p+3)/2.

Equality in this estimate occurs when M is prime, including M=2. Factoring a composite M into its prime factors strictly strengthens it. The bound exceeds floor(p/4) in saved edges for every prime p≥7.

A separate center-out ordering of the same β coefficients attains exactly this weaker uniform count: n=(k−1,k,k−2,k+1,…,0,p−2), p=2k+1. It has no zeros at odd prefix lengths, one at each proper even prefix, and p−2 at the last prefix. The subgroup-ordered result already dominates it, so it is not needed for the main theorem.

For completeness, at an odd prefix length L the residue set T={n+1} is an interval centered at k, with first moment Lk≠0 modulo p. Any multiplicative stabilizer must therefore be 1. At a proper even length L, T=−T and its second moment is L(L²−1)/12≠0 modulo p (2≤L≤p−3). Any stabilizer a must satisfy a²=1, so it is exactly {1,−1}. The last prefix is F_p*. Lemma 1 now proves all the asserted center-out zero counts.

## 6. Numerical examples are exact support counts

The attached freshly authored control performs two different exact checks:

1. Full rational cyclotomic matrix controls at p=5,7,11,13,17: the explicit β inverse, C⁻¹, CR=F, C⁻¹F=R, every colored slice entry, the Gauss norm and every chirp-corrected Fourier entry.
2. Independent integer exponent-multiset checks for every prefix and every color at p=5,7,11,13,17,19,23,29,31,37,41,73,97,193,257. It also verifies every coset block and the predicted zero positions.

The script imports only the Python standard library and does not execute or import any supplied or earlier author program. It computes both the candidate and the exact tests afresh. The proofs above establish the all-prime theorem; finite controls are implementation evidence and do not supply its universality.

## 7. Unconditional superlinear savings on a prime sequence

For each integer m≥1, choose any prime divisor p_m of the Fermat number

    2^(2^m)+1.

The multiplicative order of 2 modulo p_m is exactly 2^(m+1): its 2^mth power is −1, whereas its 2^(m+1)st power is 1. Hence

    2^(m+1) divides p_m−1,
    p_m≥2^(m+1)+1,
    W(p_m−1)≥(m+1)/2.

Consequently

    Δ(p_m)≥(p_m−1)(m−1)/2+1,

so Δ(p_m)/p_m is unbounded. This does not assume that the Fermat numbers themselves are prime.

Moreover p_m−1≤2^(2^m), giving log₂log₂(p_m−1)≤m. Thus

    Δ(p_m)≥[(p_m−1)/2][log₂log₂(p_m−1)−1]+1.

This is an unconditional Ω(p_m log log p_m) saving along the stated sequence. It is a support saving against the dense aggregate baseline, not a complexity exponent improvement.

## 8. Costs, limitations and stopping boundary

Since the number of prime factors with repetition is at most log₂N,

    0≤Z≤N log₂N=O(p log p).

Thus nnz(R)=p²−O(p log p), A is dense, and E=Θ(p²). The chain endpoint is sparse, while its inverse is quadratic. The sparsity diagnostic is obeyed and is not claimed to be sufficient in other families.

A root-power table, explicit β values and the displayed recurrence generate the coefficient table without solving any nonlinear system. All nonzero β inverses can also be written directly as

    β_(x−1)⁻¹ = (1/p) Σ_{k=1}^{p−1} k ζ^((2k+1)x),       x∈F_p*.

The formula follows by multiplying the geometric derivative sum by ζ^x−ζ^−x. It supplies an explicit quadratic-size arithmetic construction even if no inverse oracle is assumed. Primitive-root search and the integer factorization/order generation are separate finite modular computations; no free preprocessing, bit-complexity, finite-word stability, or live-memory improvement is claimed.

The result is an exact all-prime construction and an unconditional growing-saving corollary. It does not solve the paired-sparse-endpoint problem or prove a global optimum. No parameter search, external mutation, or long-running experiment is left open by this deliverable.
