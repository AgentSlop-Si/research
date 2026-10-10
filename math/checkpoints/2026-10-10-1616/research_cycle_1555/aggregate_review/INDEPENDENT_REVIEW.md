# Independent review: an aggregate Gauss escape and sharp small-support boundaries

10 October 2026. Exact complex arithmetic; local review only. No author or source program was executed or imported. The reviewer controls are freshly written and use only their own arithmetic helpers and the Python standard library.

## Decision

**Accept the constructive aggregate-only escape.** For every odd prime p >= 5, the square-invertible, separately charged latent-color model has an explicit graph with

    E = 2p² + p - floor(p/4).

This disproves extension of the strict pointwise-fiber lower bound 2p²+p to this aggregate-only model. It does not contradict the correctly scoped pointwise theorem. The construction remains quadratic, including coefficient generation. It does not beat the ordinary FFT or claim historical priority.

**Accept the exact p=3 optimum:** all square-invertible aggregate bases satisfy E >= 21, attained by the dense Gauss realization. At p=5, the construction gives E=54; this review does not prove that 54 is optimal.

**Accept the sharp first-sparsity threshold:** in the one-sided A=F_p family, every invertible C with nnz(C) <= p+2 has E >= 2p²+p. A four-vertex chain has nnz(C)=p+3 and attains E=2p²+p-1 for every prime p>=5.

## 1. Model and ledger

Use p inputs, p first hidden vertices, p second hidden vertices and p outputs, with ordinary endpoint matrices A,C invertible. Let F[i,t]=zeta^(it), R=C^-1 F and S=F A^-1. The exact aggregate condition is

    C B_t A = zeta^(-t²/2) chi_t chi_t^T.

It forces B_t=zeta^(-t²/2) R[:,t] S[t,:]. Every nonzero entry of every color slice is charged separately, even if two colors occupy the same matrix position. The ledger is

    E = nnz(A)+nnz(C)+sum_t r_t s_t.

Our construction sets A=F, so S=I and B_t has only column t. Thus different colors in this particular witness do not even overlap at matrix positions. The exact middle count is nnz(R), and no path multiplicity is substituted for an edge count.

The nonzero Gauss scalar and diagonal endpoint chirps are absorbed into existing endpoint entries. This does not change their support. It is not permission to omit their arithmetic preparation.

## 2. One four-vertex block

Let zeta be primitive of odd order p>=5 and set

    a = 1 + zeta + zeta^-1.

Both a and a-1 are nonzero: their vanishing would force zeta to have order 3 or 4, respectively. Also a is real.

For the single index order (0,1,2,p-1), take

    C = I + E_(1,0) + a E_(2,1) + E_(p-1,2).

The matrix is a unit triangular chain after simultaneous index permutation, so it is invertible. For z=zeta^t, the four corresponding rows of R=C^-1 F are

    1,
    z-1,
    z²-a z+a,
    z^-1-z²+a z-a.

All other rows are unchanged characters. The second row has exactly one grid zero. The third row has no unit-circle zero. Indeed, if z²-a z+a=0 and |z|=1, conjugating and multiplying by z² gives 1-a z+a z²=0. Subtracting yields (1-a)(z²-1)=0. Because a!=1 and the grid has odd order, z=1, which fails the original equation.

For the last row,

    z^-1-z²+a z-a = -z^-1 (z-1)(z-zeta)(z-zeta^-1).

It has exactly three grid zeros, at t=0,1,p-1. The support count is therefore nnz(C)=p+3, nnz(R)=p²-4, and E=2p²+p-1. This proof needs neither numerical fitting nor an assumption that a particular row reaches its uncertainty limit.

The polynomial argument actually works for every odd length at least five; the prime-length statement is the relevant comparison to the strict-fiber lower bound. No prime-only uncertainty fact is silently asserted for composites.

## 3. Packed independent blocks

Let m=floor(p/4). For k=0,...,m-1, put q=4k and use the block on {q,q+1,q+2,q+3}, in chain order (q+1,q+2,q+3,q). Explicitly,

    C = I + sum_k [ E_(q+2,q+1) + a E_(q+3,q+2) + E_(q,q+3) ].

The blocks are disjoint. Their four R rows are the four polynomials above multiplied by the nonvanishing character z^(q+1). Each contributes exactly four zeros and three extra C entries. Thus

    nnz(C) = p+3m,
    nnz(C^-1) = p+6m,
    nnz(R) = p²-4m,
    E = 2p²+p-m.

The latent column counts are

    r_0=p-2m; r_1=r_(p-1)=p-m; all other r_t=p,
    s_t=1 for every t.

The inverse-expansion diagnostic is consistent: delta_C=3m, delta_A=0 and the mixing penalty is zero. Its general lower estimate is 2p²+p-3m, which is weaker than the actual count by 2m. The diagnostic is necessary, not sufficient, and does not prohibit this witness.

## 4. Full fiber identity and corrected transform

Define B_t=zeta^(-t²/2) R[:,t] e_t^T. Since CR=F and e_t^T F=chi_t^T, the full slice identity follows for every i,j,t, including zero entries and all cancellation within a fiber.

Summing over t gives G zeta^((i+j)²/2), where G=sum_t zeta^(-t²/2) and |G|²=p. Multiplication by G^-1 zeta^(-i²/2) on the output side and zeta^(-j²/2) on the input side gives F exactly. The fresh controls verify the entire slice identity, this corrected transfer and the Gauss norm; the first explicit five-chain control also verifies the Fourier inverse and Weyl covariance.

The pointwise law fails even with arbitrary fixed endpoint gauges. In the first packed block, C column 1 has equal nonzero entries at outputs 1 and 2. R[1,t]=zeta^t is nonzero for every t, so this column receives middle edges with labels 0 and 1. A pointwise character ratio would require the same fixed output-weight ratio to equal a fixed gauge ratio times zeta^t at both labels. Label 0 fixes the gauge ratio; label 1 contradicts primitivity. Aggregate cancellation is therefore essential.

## 5. Arbitrary-index three-chain exclusion

For any distinct i,j,k and nonzero u,v, consider C=I+u E_(j,i)+v E_(k,j). Only two rows of C^-1 F change:

    chi_j-u chi_i,
    chi_k-v chi_j+uv chi_i.

Prime Fourier uncertainty bounds their zeros by one and two respectively. Suppose all three zeros occurred. The first fixes u at a pth-root phase. Translate the latent coordinate so its zero is at t=0, and remove the common character; the altered rows then have forms z^x-1 and z^y-v'(z^x-1), with x,y distinct nonzero residues. The latter cannot vanish at t=0.

If it vanished at distinct nonzero t=s,t=r, elimination of v' would give

    zeta^(ys+xr)+zeta^(yr) = zeta^(yr+xs)+zeta^(ys).

A rational relation among pth roots with coefficient sum zero has all coefficients zero, by the prime cyclotomic polynomial. Hence the two exponent multisets must agree. One matching gives x(r-s)=0; the other gives xr=xs=0. Both are impossible. Thus the two rows have at most two zeros in total, and nnz(C)+nnz(C^-1 F)>=p²+p.

This supplies a complete all-parameter exclusion; a parameter grid would not suffice.

## 6. Every basis with at most p+2 entries fails one-sided

If an invertible p-by-p X has at most p+2 nonzeros, a nonzero term of its determinant supplies a perfect matching. Permute and scale its hidden columns to normalize that matching to the identity. These operations preserve nnz(X), nnz(X^-1) and nnz(X^-1 F). The normalized matrix is I+N with at most two nonzero off-diagonal entries.

There are only three possibilities for two entries:

- They do not compose, so N²=0 and inverse support is unchanged.
- They form a two-cycle on two coordinates; the invertible 2-by-2 block and its inverse have the same support.
- They form a directed three-vertex chain, covered by Section 5.

With zero or one off-diagonal entry the inverse support is also unchanged. In every nonchain case, rowwise prime uncertainty gives

    nnz(X^-1 F) >= p(p+1)-nnz(X^-1) >= p(p+1)-nnz(X).

The chain case has the same conclusion. Thus no X with at most p+2 nonzeros can give a one-sided saving. Section 2 shows the threshold p+3 is attained.

## 7. The full p=3 aggregate optimum

For any F_3=XY, nnz(X)+nnz(Y)>=12. Otherwise one factor has at most five nonzeros. Since F_3 is symmetric, transpose the factorization if necessary to put that factor on the left. Section 6, with p=3, then contradicts a total below 12.

Now use F_3=CR and F_3=SA in the aggregate objective. Let P=sum_t(r_t-1)(s_t-1). Because all columns of R and rows of S are nonzero,

    sum_t r_t s_t = nnz(R)+nnz(S)-3+P.

Therefore E >= 12+12-3+P = 21+P >=21. The dense Gauss graph attains 21. This lower bound covers all complex invertible 3-by-3 endpoint matrices, not merely triangular examples.

At p=5, a global lower bound of 55 is false. The accepted construction gives 54, but neither this argument nor the uncertainty diagnostic proves that 54 is optimal.

## 8. Consecutive p=5 chain: exact restricted lower control

An invertible unit lower-bidiagonal C in the consecutive Fourier order (0,1,2,3,4), with all four links nonzero, has inverse rows proportional to prefix polynomials P_j(z)=sum_(k<=j) b_k z^k with all b_k nonzero. Any five grid zeros would include a five-element subset of the twenty stage/root constraints (j,t), 1<=j<=4, 0<=t<=4.

The independent exact screen processes all 15,504 such subsets. Degree excludes 6,779. Adjacent stages vanishing at the same root would force a b_k to be zero and exclude another 5,840. Of the remaining 2,885 homogeneous systems over Q(zeta_5), 2,705 have rank five. All 180 others have rank four and force b_0=b_1=b_2=b_3=0. Thus no valid parameter vector gives five zeros, and this specific consecutive-order chain has E>=55. Equality follows from the all-minus-one chain.

The positive witness uses a different Fourier order. This is a substantive hypothesis distinction, not a conflict between the positive and negative certificates. The finite screen is exhaustive for arbitrary complex parameter values because its matrices are exact algebraic matrices and the kernel exclusions persist under every field extension. It is not a finite-field or finite-parameter search promoted to a complex theorem.

## 9. Which prior lower bounds apply?

- **Strict pointwise Gauss theorem:** does not apply. Section 4 gives an explicit gauge-robust failed hypothesis. The theorem itself remains correct.
- **Prime Fourier uncertainty:** applies throughout the prime lower-bound arguments. The inverse-expansion inequality is obeyed, not contradicted.
- **Unit-root or positive-rational path-cancellation gates:** do not apply to arbitrary cyclotomic linear-combination weights. In particular a=1+zeta+zeta^-1 and the R entries are not constrained to individual roots with positive rational amplitudes. The endpoint Gauss normalization is also charged and is not such a root constraint.
- **Unique-path edge bounds:** do not apply; there are multiple actual paths and cancellation within a color. Path counts cannot be charged as distinct arithmetic work.
- **Green, sparse-denominator and cycle-sandwich lower bounds:** no automatic implication. They concern explicitly prescribed sums/products of Green resolvents, sparse inverses or a particular sparse-sandwich target. Here C^-1 is used to derive the finite coefficient table R; the actual execution graph applies C and R, and pays for the dense input F and every middle edge. A dense inverse alone is not the hypothesis of a Green impossibility theorem. Even applicable weak quadratic-support estimates would not conflict with this quadratic construction.
- **General three-layer Fourier algorithms or superconcentrator supports:** neither establish nor refute the colored slice certificate. This review checks the stronger per-color aggregate identities explicitly.

## 10. Costs and stopping boundary

With a supplied primitive root, an O(p) table generates all root powers. The coefficient a and all block links use explicit formulas. Each R entry is obtained by at most three local recurrence operations from root powers; constructing all A and B_t nonzeros costs O(p²). Gauss and endpoint factors cost O(p) additional ideal-field work and can be folded into existing endpoint coefficients. Literal storage and evaluation are O(p²). No inverse is charged as one free operation. A careful streaming schedule could reduce some live storage, but no subquadratic runtime or finite-word improvement is asserted.

The result closes the proposed 2p²+p aggregate lower-bound extension and supplies a constructive sparse-inverse-dense escape. It does not close the search for a subquadratic aggregate graph with both boundary matrices subquadratic, nor prove optimality of this packed family.

## 11. Independent evidence

- First explicit p=5 five-chain witness: all 125 slices and 25 corrected entries, exact inverse and Weyl tests; E=25+9+20=54. Preserved as a separate discovery control.
- Uniform one-block family: p=5,7,11,13,17; 8,909 exact slice entries and 653 corrected entries.
- Packed family: p=5,7,11,13,17,19; 15,768 exact slice entries and 1,014 corrected entries, inverse support and pointwise-gauge counterchecks.
- Consecutive p=5 lower control: all 15,504 masks, with complete rank-four constraint records.
- Sparse pattern inventory: all 22 normalized p=3 patterns with at most two off-diagonal entries.
- Three-chain cyclotomic multiset controls: p=3,5,7,11, independently enumerated without author code.

The all-length positive and lower-bound statements rest on the displayed proofs. The finite controls are additional verification. The classical prime uncertainty input is Terence Tao, *An uncertainty principle for cyclic groups of prime order* (2005), https://arxiv.org/abs/math/0308286. No literature-wide novelty assertion is made.
