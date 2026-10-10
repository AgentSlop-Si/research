# Independent review: sine-difference aggregate chains

Review date: 10 October 2026. Verdict: mathematical PASS for the exact center-out and subgroup-hierarchy families stated below. This review changes no predecessor file. The constructions are quadratic support improvements in the separately colored aggregate model. It grants no historical novelty, unrestricted optimality, bounded-weight, or FFT-speedup status.

## 1. Accepted statements

Let p≥5 be prime, let ζ be a primitive pth root, and put N=p−1. For any ordering n_0,…,n_(N−1) of 0,…,p−2, define

β_n=ζ^(n+1)−ζ^(−n−1),
C=I−Σ_(j=1)^(N−1) [β_(n_(j−1))/β_(n_j)] E_(n_j,n_(j−1)),
A=F, where F[i,t]=ζ^(it), and R=C^−1 F.

The unused index p−1 is an identity singleton. All β_n and every displayed C edge are nonzero. For the first L indices, let T_L={n_j+1:0≤j<L}⊂F_p^*. Then the Lth chain row has exactly

|Stab×(T_L)|−1

zeros on the pth-root Fourier grid. Therefore, with Z=Σ_(L=1)^N (|Stab×(T_L)|−1), the complete separately colored construction has exactly

nnz(A)=p², nnz(C)=2p−2, Σ_t nnz(B_t)=p²−Z,
E=2p²+2p−2−Z.

Two specific orders give:

1. Center-out: if p=2k+1, order (k−1,k,k−2,k+1,…,0,p−2). Then Z=(3p−7)/2 and E=2p²+(p+3)/2.
2. Subgroup hierarchy: factor N=q_1⋯q_r into primes with multiplicity, put d_j=q_1⋯q_j, and order F_p^* in nested subgroup-coset blocks of sizes d_j. Then

Z=N Σ_(j=1)^r (1−1/q_j)
 =(p−1) Σ_(q|p−1) v_q(p−1)(1−1/q),
E=2p²+2p−2−(p−1) Σ_(q|p−1) v_q(p−1)(1−1/q).

These are exact counts, not only upper bounds. The total is independent of the order of the prime factors, although the individual prefix supports can change.

## 2. Coefficients, invertibility, and the grid-zero identity

If β_n=0, then ζ^(2n+2)=1. Since p is odd and 1≤n+1≤p−1, this is impossible. In chain order C is unit lower bidiagonal. It is invertible, has N diagonal chain entries, N−1 chain links, and the singleton diagonal, giving 2p−2 nonzeros.

Solving CR=F forward gives, for the Lth chain row n_(L−1),

R[n_(L−1),t]=Q_L(ζ^t)/β_(n_(L−1)),
Q_L(z)=Σ_(j=0)^(L−1) β_(n_j) z^(n_j).

This includes L=1, where the quotient is ζ^(n_0 t). No inverse or preprocessing is assumed free. The inverse chain entries are β_(n_i)/β_(n_j) for j≥i, all nonzero, so

nnz(C^−1)=p(p−1)/2+1,
nnz(C^−1)−nnz(C)=(p−2)(p−3)/2.

For any nonempty T⊂F_p^*, the corresponding numerator satisfies

Q_T(ζ^t)=ζ^(−t)[Σ_(x∈T) ζ^((t+1)x)−Σ_(x∈T) ζ^((t−1)x)].

Write the bracket as Σ_(a=0)^(p−1) c_a ζ^a. The c_a are integers and Σ_a c_a=0. The prime cyclotomic polynomial is 1+X+⋯+X^(p−1); hence a polynomial of degree at most p−1 vanishing at ζ has all its coefficients equal. Their zero sum then makes every c_a zero. Thus the numerator vanishes exactly when the two exponent multisets agree.

At t=1 or t=−1 one multiset consists solely of zeros and the other entirely of nonzero residues, so neither t is a zero. For every other t, both multipliers are nonzero, and multiset equality is equivalent to

λ_t=(t+1)/(t−1) ∈ Stab×(T).

The map t↦λ_t bijects F_p\{1,−1} with F_p^*\{1}; its inverse is (λ+1)/(λ−1). This proves exactly |Stab×(T)|−1 zeros, including t=0 when −1 stabilizes T. There is no omission at t=0 and no spurious zero at t=±1.

Primality is essential to this cyclotomic-independence argument. No composite-order extension is accepted here.

## 3. Independent center-out proof

For L=2r+1, the prefix T_L is the integer interval {k−r,…,k+r} modulo p. Its first moment is Lk, nonzero modulo p, because 1≤L<p and k≠0. If λT_L=T_L, its first moment equals λ times itself, forcing λ=1. Hence each odd prefix has no grid zeros.

For L=2r<N, T_L={k−r+1,…,k+r}. It is stable under negation and has first moment zero modulo p. Its second moment is

Σ_(x∈T_L) x²=L(L²−1)/12 modulo p.

For p≥5 this is nonzero: 12 is invertible, 2≤L≤p−3, and L is neither 0 nor ±1 modulo p. Any stabilizer λ therefore satisfies λ²=1, while both ±1 do stabilize T_L. Its stabilizer is exactly {1,−1}, so every proper even prefix has exactly one zero, t=0.

The final prefix is F_p^*, with stabilizer of order p−1 and exactly p−2 zeros, all t except ±1. There are (p−3)/2 proper even prefixes. Consequently

Z=(p−3)/2+(p−2)=(3p−7)/2.

Column counts provide an additional off-by-one check: r(0)=(p+1)/2; r(1)=r(p−1)=p; and r(t)=p−1 for all remaining t. These sum to p²−Z.

## 4. Independent subgroup-hierarchy proof

Let H_j be the unique subgroup of F_p^* of size d_j, with H_0={1}. A nested order has every consecutive aligned block of d_j elements equal to an H_j coset. Such an order exists by recursively listing the q_j cosets of H_(j−1) inside each H_j coset. An explicit implementation chooses a primitive root g and recursively builds its exponent order: begin [0]; when extending from d to dq, concatenate q translates of the current list by hN/(dq), h=0,…,q−1.

Fix L<N and let j be maximal with d_j dividing L. The prefix is a union of H_j cosets, so H_j is contained in its stabilizer. At the next level, it contains some full H_(j+1) cosets and exactly one partially occupied H_(j+1) coset, with all later cosets empty. This uniqueness is a consequence of the aligned block order.

A multiplicative stabilizer permutes H_(j+1) cosets and preserves their intersection cardinalities with the prefix. It must fix the unique partially occupied coset. Therefore the stabilizer lies in H_(j+1). Between H_j and H_(j+1) there is no intermediate subgroup, since the quotient has prime order q_(j+1). The stabilizer cannot be H_(j+1), because the unique partial coset is not full. Thus it is exactly H_j. For L=N it is H_r=F_p^*.

This also explains why simply adding all subgroup contributions per prefix would overcount. Instead write

|Stab×(T_L)|−1=Σ_(j=1)^r (d_j−d_(j−1)) · 1_(d_j divides L).

Summing over L=1,…,N gives

Z=Σ_(j=1)^r (d_j−d_(j−1))N/d_j
 =NΣ_(j=1)^r(1−1/q_j).

The final prefix is included exactly once in each telescoping increment, not counted as several unrelated zero sets.

The hierarchy is never worse than the center-out count. Separate one factor 2 from N. For any prime factorization of M=N/2, Σ_(q factors of M)(1−1/q)≥1−1/M; this follows repeatedly from (1−1/a)+(1−1/b)−(1−1/(ab))=(1−1/a)(1−1/b)≥0. Therefore Z≥N(3/2−2/N)=(3p−7)/2, with strict inequality when M is composite.

## 5. Colored identities and full edge ledger

Put γ_t=ζ^(−t²/2), with division by 2 modulo p, and

B_t=γ_t R_[:,t] e_t^T.

Each color t remains a separate slice. Since CR_[:,t]=F_[:,t] and e_t^T A=F_[t,:],

C B_t A=γ_t χ_t χ_t^T.

The number of middle edges of this color is exactly the number of nonzeros in its R column. Although the slices have disjoint columns here, no latent-color identification is used to save edges. A alone has p² edges; C has 2p−2; the sum of all colored middle counts is p²−Z.

For B=Σ_t B_t and G=Σ_t γ_t≠0, quadratic completion gives

(CBA)[i,j]=Gζ^((i+j)²/2).

The corrected boundaries C'=G^−1 diag(ζ^(−i²/2))C and A'=A diag(ζ^(−j²/2)) therefore satisfy C'BA'=F. These are nonzero rescalings of existing edges and change none of the counts. They add no uncharged layer.

The fixed-endpoint-gauge pointwise character condition genuinely fails. At the first chain root n_0, its R row is the nonzero character ζ^(n_0t), so all colors reach that vertex. Its C column touches the distinct outputs n_0,n_1 with fixed nonzero relative weight. A pointwise character law would require that same fixed ratio to equal a fixed endpoint-gauge ratio times ζ^((n_1−n_0)t) for every t. Colors 0 and 1 contradict this because n_1≠n_0 modulo p.

## 6. Fresh exact controls

The reviewer-authored fresh_aggregate_check.py imports only Python standard libraries and SymPy. It imports, executes, or modifies no author/predecessor program. It constructs the formulas from scratch in Q(ζ_p), solves CR=F by forward substitution, independently solves inverse columns, checks both inverse products, and multiplies the full Gauss-corrected transfer. Exact zero tests determine every prefix and color support.

Both orders passed at p=5,7,11,13,17. The subgroup (Z,E) values are (4,54), (7,103), (13,249), (20,342), (32,578). Center-out agrees in the first three cases and gives (16,346), (22,588) in the last two. FRESH_AGGREGATE_EXACT_RESULTS.json contains exact zero positions, node orders, inverse support counts, and each separately charged color count.

An independent finite-group check additionally verifies exact prefix stabilizers for every prime 5≤p≤127, for both ascending and descending orders of the prime factors. Its receipt is FRESH_AGGREGATE_STABILIZER_RESULTS.json. These controls support implementation; the all-prime claims are established by the proofs above.

## 7. Scope and comparison

The subgroup hierarchy and diagonal-scaled cumulative-sum/difference operators are classical ingredients. In chain coordinates C=D^−1(I−S)D, so C^−1 is a weighted prefix-sum operator. The zero test is an elementary prime cyclotomic-period identity. No worldwide literature search or novelty clearance is completed by this review.

The accepted multiplicative-character Fourier baseline in research_cycle_1535/subgroup_fourier_weights/EXACT_SUBGROUP_FACTORIZATION.md uses subgroup Fourier transforms and partial Gauss-sum middle blocks. Its uncolored three-layer count is 3+2d(p−1)+(p²−1)/d. That is a different ledger from the separately colored aggregate-fiber identity required here. At p=13 its accepted d=3 graph has 131 edges, versus 342 in this aggregate chain; at p=17 its d=4 graph has 203, versus 578. Thus this result is not a best Fourier graph even among the already reviewed constructions. Its useful conclusion is a stronger constructive escape from the dense aggregate support count under the specified color constraints.

The construction remains Θ(p²), because A itself is dense. Z≤(p−1)Ω(p−1)≤(p−1)log_2(p−1), so the change is lower order. If p−1=2^r, the exact formula gives Z=(p−1)r/2. This conditional arithmetic specialization does not assert infinitely many Fermat primes. The stronger unconditional prime-divisor corollary below is also accepted. Neither gives a uniform logarithmic factor for all primes or any reduction to O(p log log p) computation. Nor is a uniform modulus-one bound on the chain coefficients claimed; ratios of sine differences need not be bounded independently of p. Preprocessing, bit complexity, arithmetic work, stability, and live state are not covered by the edge count.


## 8. Independent review of the unconditional prime sequence

The frozen author note additionally takes, for every m≥1, any prime divisor p_m of 2^(2^m)+1. This corollary passes independently.

The prime is odd. Modulo p_m, 2^(2^m)=−1, so the order of 2 divides 2^(m+1) but does not divide 2^m. Since all divisors of a power of two are powers of two, the order is exactly 2^(m+1). Thus 2^(m+1) divides p_m−1 and W(p_m−1)≥(m+1)/2. The edge saving satisfies

Δ(p_m)=(p_m−1)W(p_m−1)−(p_m−2)
       ≥(p_m−1)(m−1)/2+1.

Different m give different multiplicative orders and therefore distinct primes p_m; also p_m≥2^(m+1)+1, so the sequence tends to infinity. On the other hand p_m−1≤2^(2^m), hence log_2 log_2(p_m−1)≤m. Combining these inequalities gives exactly

Δ(p_m)≥[(p_m−1)/2][log_2 log_2(p_m−1)−1]+1.

This proves an unconditional Ω(p_m log log p_m) support saving along the prime-divisor sequence. It uses the existence of a prime divisor of each Fermat number, not primality of the Fermat numbers themselves. The baseline and constructed counts still have leading term 2p_m². No logarithmic saving uniformly over all primes is claimed.

## 9. Frozen author-document binding

The complete author document was read as inert text after finishing the independent construction and controls:

research_cycle_1735/aggregate_subgroup_chain/MULTIPLICATIVE_PREFIX_CHAIN.md
SHA-256: 5cb007e621d502605bbb81df85f0f3a15a43c2ace487d4024e46bb6573ac2e03.

The verdict applies to those exact bytes, including Sections 1–8, the center-out corollary, color distribution, explicit inverse, and prime-divisor asymptotic corollary. A copy is preserved in input_snapshot for reproducible binding. No correction to the frozen document is required. Historical-priority clearance remains separate.
