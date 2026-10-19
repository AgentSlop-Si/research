# Independent review: sharp cyclic phase minimax family

Date: 19 October 2026 UTC.

**Verdict: ACCEPT.** The analytic statements and the legal attaining construction in the candidate proof are correct. No mathematical correction is required.

Frozen candidate:
- `/workspace/shared/phase_cyclic_family_20261019_1001/PROOF.md`
- Proof SHA-256: `fa7beae832b28c7f372be757ea4416863b2f003c5104a1ba51fdf0d954595f2b`
- Author manifest SHA-256: `a1d1a3eb5b8451f0c4cd309782034e5b768fcdcc994ade9d5d69cb42704fd31a`
- Every one of the eight author-manifest entries was independently rehashed and byte-count checked. All matched.

This review independently checks the proof, writes and executes new exact verification programs, and does not execute the author's code or any historical code. The existing accepted C8 proof and verdict were read as a baseline, not used as executable inputs. All writes were confined to this new local review directory. No external publication, repository write, novelty determination, or general FFT claim is part of this review.

## 1. Accepted result and exact model

Let F_N[j,k]=N^(-1/2)exp(-2πijk/N), and let δ_(N,r) be the minimum external spectral norm of F_N−L(B+E)R, where B is an unrestricted real N-by-N matrix, E is complex with complex rank at most r, and L,R are arbitrary invertible complex monomial matrices. Under this exact model:

1. For even N≥4 and integer r≥0 satisfying 4r<N−2,
   δ_(N,r)≥sin(π(N−4r−2)/(4N)).
2. For every integer m≥1,
   δ_(4m,m−1)=sin(π/(8m)).
3. For N=4m, zero error is possible exactly when r≥m. Thus the least exact correction rank is m.
4. For N=4m and any diagonal unitary A,B, an open arc of width 2π/N contains at most N/2+1 eigenvalues of F_N A F_N B, with algebraic multiplicity. The witness puts N/2+2 eigenvalues in a closed arc of the same width, showing that the width cannot be enlarged with that count bound.

The lower bound can also be stated for all integer 0≤r<N/4: the additional even-N boundary case N=4m+2,r=m is simply the trivial bound δ≥0. The candidate appropriately states only the strictly positive portion.

The optional odd-N companion lower bound, sin(π(N−4r−1)/(4N)) when N−4r−1>0, is also correctly derived. No odd-N attainment is established.

## 2. Gauge absorption and fixed-phase rank reduction

Any invertible complex monomial matrix admits the indicated diagonal-unitary/real-monomial factorization, including arbitrary permutations and positive magnitudes. Absorbing the real monomial factors into B and E is bijective and preserves both realness of B and complex rank of E. Crucially, this changes the represented approximant rather than multiplying the residual by a nonunitary matrix. Therefore it introduces no condition-number restriction or norm distortion.

For a fixed complex V and Y=Im V, entrywise imaginary part is a contraction in the complex spectral norm because Im Z=(Z−conjugate(Z))/(2i). If rank_C E≤r, the real matrix Im E has real rank at most 2r. The real singular-value min–max argument therefore gives the lower bound σ_(2r+1)(Y).

Conversely, let a best rank-at-most-2r truncation of Y be T=Σ_a v_a u_a^T, with zero summands added if necessary. Then

E=Σ_l(v_(2l−1)+iv_(2l))(u_(2l)+iu_(2l−1))^T

has complex rank at most r and Im E=T. Choosing B=Re(V−E) makes the residual exactly i(Y−T), so equality holds. This verifies the rank reduction without assuming E is real or confusing complex rank with real rank. The r=0 case is the empty sum. With the usual zero singular-value convention, larger r cause no difficulty.

Consequently δ_(N,r)=min_(P,Q) σ_(2r+1)(Im(PF_NQ)). The phase torus is compact, the objective is continuous, and the fixed-phase minimum is attained, so using “minimum” rather than merely “infimum” is justified even though the original gauges are noncompact.

## 3. Spectral reduction and strict commutator estimate

For unitary V=P F_N Q, the symmetric unitary W=V^T V is similar to F_N P² F_N Q². Writing V=X+iY gives Y^T Y=(I−Re W)/2. The real and imaginary parts of W are commuting real symmetric matrices. They can therefore be simultaneously diagonalized over the reals, and the imaginary singular values are exactly |sin(φ_j/2)| for the eigenvalues exp(iφ_j) of W, with multiplicity.

The commutator lemma is valid with the count stated in the candidate. If N−k selected eigenvalues of U lie in |arg λ|<θ, replace those eigenvalues by 1 to obtain U_0, so rank(U_0−I)≤k. For E=U_0*U, every eigenvalue lies strictly in that same arc, including the unselected directions where E has eigenvalue 1. Since 0<θ<π/2,

||E−cos(θ)I||<sin θ.

For K=UTU*T* and K_0=U_0TU_0*T*, the unitary cancellations give

||K−K_0||=||ET−TE||<2 sin θ,
rank(K_0−I)≤2k.

Thus K−I is uniformly smaller than 2 sin θ on a subspace of dimension at least N−2k. Singular-value min–max forces at least N−2k singular values below this strict threshold. Normality of K−I turns this into at least N−2k eigenvalues of K in |arg λ|<2θ. The passage from the norm bound to a strict eigenvalue count is sound; no endpoint is included.

In the correction problem k=2r. The forced count is N−4r, not N−2r. The candidate retains this essential factor throughout. Rotating U by a scalar changes neither commutator, so arbitrary arc centers are covered.

## 4. Cyclic obstruction and the lower bounds

The entry formula C[j,k]=N^(-1)Σ_l a_l exp(-2πi(j+k)l/N) proves CS=S* C directly. For M=CB and T=B*SB,

K=MTM*T*=S*B*S*B,
K e_j=(b_j/b_(j−1))e_(j−2).

For even N the even and odd coordinates are two cycles of length L=N/2. Their weight products are Γ and Γ^(-1). Thus the characteristic polynomial is exactly (x^L−Γ)(x^L−Γ^(-1)), even if those factors share roots. The count correctly adds multiplicities from the two factors.

An open arc of width 2πa/L, with integer 1≤a<L, contains at most a of the equally spaced roots of each factor. Set a=N/2−2r−1 and θ=πa/N. The asserted strict singular-value violation puts N−2r eigenvalues of M in an arc of radius θ. The lemma would then put N−4r eigenvalues of K in an open arc of width 4θ, whereas the cycle count permits only 2a=N−4r−2. This proves the lower bound for every phase, without a periodicity restriction or a phase search.

For odd N, stepping by −2 gives a single cycle with telescoping product 1. The characteristic polynomial is x^N−1. Choosing θ=π(N−4r−1)/(2N) produces the stated companion bound by the same argument.

For the open-arc theorem, N/2+2 hypothetical eigenvalues of M use k=N/2−2 and θ=π/N. The forced count is four, while the two length-N/2 cycles permit at most two. This establishes the claimed uniform open-arc count.

## 5. Witness for all m, with both parities and m=1 included

Use N=4m, h=2m, ζ=exp(2πi/N), α=π/N, t=(−1)^mζ^(−1), z=exp(iπ/(2N)), and the displayed q_j. Squaring the q_j gives b_j=1 on the even coordinates and b_j=tζ^(2j) on the odd coordinates, exactly as claimed. Setting P=zQ therefore supplies genuine diagonal unitary phases.

The geometric sums give

F_N B_0 F_N=(Π_+ +tS²Π_−)R_0,
Π_±=(I±S^h)/2.

The formula includes coincident Fourier locations at N=4; no argument requires those locations to be distinct. Since h is even, the parity subspaces are preserved by S^h. Since ζ^(2h)=1, B_0 preserves its ±1 eigenspaces. Hence the four simultaneous parity/half-shift spaces are invariant and each has dimension m.

On these four spaces the scaled product M=z²F_NB_0F_NB_0 has blocks

exp(iα)J_1, exp(−iα)J_2, exp(−iα)J_3, exp(iα)J_4,

where the four J_a are exactly the involutions specified in the candidate. In particular, (S²R_0D)²=ζ^4I, making J_4=ζ^(−2)S²R_0D a unitary involution. The scalar factors in the other three blocks also agree. A unitary involution is Hermitian, so its only eigenvalues are ±1.

The independent fixed-coordinate trace calculation gives:
- m odd: traces (1,1,1,1)
- m even: traces (2,0,0,2)

For example, on a parity sector the restriction trace is half the trace of J+ηHJ. The relevant fixed-coordinate equations are 2j=0, 2j=h, 2j=2, and 2j=h+2. The parity of m determines exactly which extra pairs contribute; the phase weights at those pairs are the signs stated in the candidate. The total trace is always 4.

It follows that the eigenvalue multiplicities, in the order exp(iα), exp(−iα), −exp(iα), −exp(−iα), are

(m+1+e, m+o, m−1−e, m−o),

with e=1 for m even and o=1−e. These numbers are nonnegative for every m≥1 and sum to 4m. Thus Im V has exactly 2m+2 singular values s=sin(π/(8m)) and 2m−2 singular values c=cos(π/(8m)).

For m=1 the four blocks have dimension one and are all +1. The spectrum multiplicities are (2,2,0,0), and Im V has all four singular values equal to s. The empty rank-zero correction is valid. For m=2 the multiplicities are (4,2,0,2), giving the accepted C8 value; no assertion that all four blocks have only positive signs is made at larger m.

## 6. Constructive correction and exact-rank threshold

For the witness, R=(Y^T Y−s²I)/(c²−s²) is a real orthogonal projector of rank 2m−2. Its range is precisely the c-singular subspace. A real orthonormal basis u_a of that range gives YR=Σ_a(Yu_a)u_a^T. Pairing these terms by the fixed-phase construction supplies a complex correction E of rank at most m−1. With B=Re V−Re E, the exact residual is iY(I−R) and its norm is s.

The Gram–Schmidt prescription is deterministic in exact arithmetic: the projected coordinate vectors span the range, zero residuals are skipped, and positive normalization constants select the stated signs. It is a legitimate explicit finite construction, not a phase or rank optimization. The outer gauges P* and Q* convert this witness back to the original external residual without changing its norm.

For unphased F_(4m), reversal R_0 has negative eigenspace dimension 2m−1. Hence rank_R Im F_(4m)=2m−1, and pairing its rank-one real factors gives a complex correction of rank at most m with zero error. The strictly positive optimum at m−1 and rank monotonicity rule out every smaller correction rank. This proves the exact threshold.

The witness has Γ=−1, so its commutator characteristic polynomial is (x^(N/2)+1)². The nearest commutator eigenvalues to 1 lie exactly at exp(±2πi/N), each twice. The original small eigenvalues are exactly on exp(±iπ/N), with total multiplicity N/2+2. Consequently the candidate's endpoint warnings are necessary and correct. Enlarging the arc width strictly includes both original endpoints and defeats the N/2+1 count; this establishes width-sharpness without claiming the open-arc maximum is attained.

## 7. Fresh independent exact checks

Two new programs accompany this review.

### Cyclotomic witness checks

`independent_exact_checker.py` works in exact rational cyclotomic fields of order 4N, never in floating-point matrix arithmetic. It independently constructs the Fourier sums and phases. At N=4,8,12,16,20,24,28,32,36,40,44,48,64 it checks:
- the direct Fourier sum against the four-shift expression, including N=4 collisions;
- unitarity and all four invariant block identities;
- all four involution and Hermitian identities;
- the exact parity-dependent traces and multiplicities;
- both weighted-cycle products equal to −1.

At N=4,8,12,16,20 it additionally constructs U=√N V directly, verifies U*U=NI, computes W=U^T U/N, compares the phase similarity, checks the direct real-imaginary Gram identity, and checks the projector equation, symmetry, realness, trace and exact rank.

To avoid merely repeating the author's Gram–Schmidt algorithm, the checker constructs a separate correction from a rank factorization T=G R=A B, where G=√N Im V. It pairs columns of A with rows of B into complex rank-one summands. It then verifies exact complex rank, the imaginary part, realness of the resulting core, and the residual identity. The final checked residual Gram is exactly s²(I−R) after dividing by N. The observed correction ranks are 0,1,2,3,4, respectively.

All checks passed. The candidate proof hash was the same before and after the run.

### Formal-variable cycle checks

`independent_symbolic_cycles.py` uses independent formal nonzero variables b_j and generic formal cyclic-Hankel coefficients. For N=3,4,5,6,7,8,9,10,12 it checks CS=S^T C, the weighted two-step action, and the exact characteristic polynomial. These are symbolic rational-function checks, not numerical phase samples. All passed.

The finite checks certify the implementations and finite identities. The all-phase, all-rank, and infinite-m proofs are the analytic arguments reviewed above; finite checks are not substituted for them.

## 8. Scope limits retained

This acceptance does not establish matching upper bounds at r<m−1, classify all minimizers, prove an odd-order attaining family, prove a theorem for general finite groups, supply a jointly real Green construction, or establish an FFT operation-count conclusion. It does not assess literature novelty. The candidate's stated open problem and its exclusion of those stronger claims are appropriate.
