# Independent review: strict rank-zero obstruction for C8

Date: 19 October 2026 UTC.

## Verdict and frozen scope

**ACCEPT.** The analytic proof is correct as written; no mathematical correction is required. All 758 independent exact assertions passed: 752 in the main checker and six in the boundary checker.

Frozen candidate: `/workspace/shared/phase_rankzero_20261019_1053/PROOF.md`.

Proof SHA-256: `4eff619bfde38551a47bf2e109307bb565e09eea5cc42d59213f9513023cb621`.

The candidate's six manifest entries were independently rehashed and byte-count checked before and after the control run. All matched, and the proof remained unchanged. The complete source hash receipt is included. Neither the candidate's code nor historical code was executed. New independent checks were written in this review directory. No external publication, repository change, novelty search, or operation-count conclusion forms part of this review.

The accepted baseline was read from `phase_cyclic_family_20261019_1001/PROOF.md` and `phase_cyclic_review_20261019_1011/REVIEW.md`. The strict result here is compatible with that earlier exact boundary-rank family and settles a different, smaller-rank question.

Accepted statements, in the original external operator-norm model with arbitrary invertible complex monomial gauges, unrestricted real matrix core, and zero complex correction rank:

1. sin(3π/16) < δ_(8,0) ≤ 1/√2.
2. If N=4m and U=F_N A F_N B has all eigenvalues in the closed centered arc of radius θ=π/2−π/N, then both diagonal unitary matrices A and B have period N/2.
3. The two parity-supported commutator eigenvectors at its positive endpoint have complementary Fourier parity supports. Their opposite-endpoint partners have the opposite half-shift signs.

The general periodicity is **half-periodicity**, not four-periodicity at arbitrary N. It becomes four-periodicity for N=8. A=P² and B=Q² are the squared phases in the spectral reduction; the theorem does not assert that P and Q themselves must have those periods.

The exact value of δ_(8,0), a quantitative positive gap, rank-zero attainment or strictness for m≥3, and the remaining smaller positive correction ranks remain open here. No minimizer classification or historical novelty is accepted or claimed.

## 1. Original model, norm, and compactness

An arbitrary invertible complex monomial matrix factors into a diagonal unitary and an invertible real monomial, with the real factor placed adjacent to the real core. Both real monomial factors are absorbed into that unrestricted core, preserving realness. At rank zero there is no correction; the analogous absorption also preserves complex correction rank in the broader model.

This modifies the represented approximant rather than multiplying the residual by a nonunitary matrix. Thus arbitrary magnitudes and permutations are covered, without a hidden conditioning restriction or a norm comparison in a different model.

For fixed V, entrywise imaginary part satisfies ||Im Z||≤||Z|| because Im Z=(Z−conjugate Z)/(2i), and complex conjugation preserves the spectral norm. Consequently min_(R real)||V−R||=||Im V||, attained by R=Re V. Hence

δ_(N,0)=min_(P,Q diagonal unitary)||Im(PF_NQ)||.

The phase torus is compact and the norm objective is continuous. The minimum exists even though the original monomial description is noncompact. This is the necessary compactness fact for upgrading the C8 nonattainment argument to a strict lower bound on the infimum.

The candidate's optional general-rank reduction also checks out: rank_R Im E≤2 rank_C E gives the lower bound, and pairing two real rank-one terms into one complex rank-one term realizes any real rank-2r truncation. No erroneous equality between real and complex ranks is used.

## 2. Spectral reduction and scalar centering

For unitary V=P F_N Q, W=V^T V is symmetric unitary, and

Q^(-1) W Q=F_N P² F_N Q².

Writing V=X+iY with X,Y real gives Y^T Y=(I−Re_entrywise W)/2. The real and imaginary parts of W are commuting real symmetric matrices, so simultaneous real orthogonal diagonalization proves that an eigenvalue exp(iφ) contributes |sin(φ/2)| to the singular spectrum of Y, with multiplicity. Thus a norm at most sin(θ/2), for 0<θ<π/2, puts every eigenvalue of U in the closed centered θ-arc.

There is no phase-center omission. The norm reduction supplies that centered arc directly. If starting from an arbitrarily centered arc instead, its scalar center can be absorbed into A without changing the commutator; diagonal phase squaring is surjective. After centering, the Hermitian part (U+U*)/2 is at least cos θ I, with cos θ>0.

The proof distinguishes the entrywise-real operation on W from the Hermitian part of U. They are not confused in the sector argument.

## 3. Weighted cycles and endpoint equality

The cyclic-Hankel identity C S=S* C, for C=F_N A F_N, gives

K=U T U* T*=S* B* S* B,  T=B* S B,
K e_j=(b_j/b_(j−1))e_(j−2).

For N=2L the even and odd cycles have length L and products Γ and Γ^(-1), respectively. Their characteristic polynomial is (x^L−Γ)(x^L−Γ^(-1)). Multiplicities must be added when the factors share roots.

The bound ||U−cos θ I||≤sin θ yields ||K−I||≤2 sin θ, so every K eigenvalue lies in the closed arc of radius 2θ. For θ=π/2−π/(2L), the forbidden open gap about −1 has exactly the spacing 2π/L of a regular L-gon. An L-gon avoiding that gap must have consecutive vertices at both gap endpoints. When L is even, both endpoint Lth powers equal −1, so Γ=−1. Each endpoint occurs once on each cycle, hence has multiplicity exactly two for K. There is no assumed simplicity of U's endpoint eigenvalues.

The endpoint-rigidity implication is valid without a hidden equality assumption in a triangle inequality. Here is an explicit scalar proof. If Kx=exp(2iθ)x with ||x||=1, put D=T U* T*, z=<x,U*x>, and w=<x,Dx>. Then w=exp(2iθ)z. Both Re z and Re w are at least a=cos θ>0, while |z|≤1. Therefore

2a Re(exp(iθ)z)=Re z+Re w≥2a.

It follows that Re(exp(iθ)z)≥1 and |exp(iθ)z|≤1, forcing z=exp(−iθ). Equality in the unitary expectation implies U*x=exp(−iθ)x, hence Ux=exp(iθ)x. The negative endpoint is identical with signs reversed. This directly verifies the frozen proof's equivalent convex-hull argument, including any argument-branch wrapping. The positivity a>0 is essential and is available throughout the stated theorem.

The same cycle gap argument rules out every strictly smaller arc, proving the non-strict lower bound before equality is excluded.

## 4. Complementary support, including Fourier zeros

Write d_t=b_(2t), e_t=b_(2t+1), and choose the two K eigenvectors x,y at λ=exp(i(π−π/L)), supported on even and odd indices. Normalize x_0=y_0=1. Their coordinates have modulus one because the weighted shift is unimodular, and direct recurrence gives

x_(t+1)=λ e_t d_(t+1)^(-1)x_t,
y_(t+1)=λ d_(t+1)e_(t+1)^(-1)y_t.

Multiplication and shifting yield

e_t x_t y_t=e_0 λ^(2t),
d_t x_t y_(t−1)=e_0 λ^(2t−1).

These identities also hold at wraparound because λ^L=−1 and λ^(2L)=1. The endpoint-rigidity result supplies Ux=u x and Uy=u y, with u²=λ.

I independently expanded the L-point Fourier transforms. With ω=exp(2πi/L), λ²=ω^(−1), X=F_L x, Y=F_L y, D=F_L(d x), E=F_L(e y), the exact identities are

D_k=e_0 λ^(−1)ω^(−k−1)conjugate(Y_(−k−1)),
E_k=e_0 conjugate(X_(−k−1)).

The full N-point eigenvector equations reduce to

a_jD_k=uX_(−k),
a_jE_k=uω^kY_(−k),  k=j mod L.

In the odd-supported equation, the forward transform carries exp(−2πij/N), while the inverse transform carries exp(2πij/N). Their ratio is ω^k. This verifies the sign most susceptible to a transpose/adjoint or Fourier-index error.

Eliminating a_j by multiplication, without division, gives

X_n conjugate(X_(n−1))=λY_n conjugate(Y_(n−1)),
|X_n|=|Y_(n−1)|,  |Y_n|=|X_(n−1)|.

The magnitudes of X are two-periodic; Y has the swapped two magnitudes. If both magnitudes were nonzero, multiplying the first identity over all n would equate the positive number |product X_n|² to λ^L |product Y_n|², a negative number. Therefore one magnitude vanishes. Invertibility of the Fourier transform excludes both magnitudes vanishing. The surviving parity class is nonzero at every one of its indices, and X,Y have exactly complementary parity supports.

This argument treats all Fourier zeros, rather than assuming them away. Inverse Fourier transformation yields x_(t+m)=ηx_t and y_(t+m)=−ηy_t for a sign η. Shifting the two product identities by m negates both coordinate products and also multiplies λ^(2t) by λ^L=−1. Hence d_(t+m)=d_t and e_(t+m)=e_t, proving B's half-periodicity.

Comparing the full Fourier equations at j and j+L now proves A's half-periodicity: their reduced expressions are the same, and at every frequency at least one equation has a nonzero Fourier factor. No division by an unverified nonzero coefficient is needed. The original odd-coordinate transform signs cancel on the two sides before this comparison.

The negative-endpoint vectors are x'_t=ω^t x_t and y'_t=ω^t y_t. The factor λ^(−2)=ω changes the recurrence to λ^(−1), while ω^m=−1 reverses their half-shift signs. This accounts for all four parity/sign combinations in the C8 application.

## 5. Exact C8 blocks, flatness, and degeneracies

At N=8, half-periodicity means a_(j+4)=a_j and b_(j+4)=b_j. Direct Fourier summation makes C vanish between opposite parities. Also C commutes with H=S^4 and B commutes with H. Thus U preserves the four mutually orthogonal parity/half-shift spaces, each of complex dimension two; their restrictions are unitary.

For transparency, define

α=(a_0+a_2)/2, β=(a_0−a_2)/2,
γ=(a_1+a_3)/2, δ=i(a_3−a_1)/2.

In the basis (e_j+ηe_(j+4))/√2, with j=0,2 for even and j=1,3 for odd, the blocks are exactly

- even,+ : [[α,β],[β,α]] diag(b_0,b_2)
- even,− : [[γ,δ],[δ,−γ]] diag(b_0,b_2)
- odd,+ : [[β,α],[α,β]] diag(b_1,b_3)
- odd,− : [[δ,−γ],[−γ,−δ]] diag(b_1,b_3).

The endpoint vectors constructed above supply a flat eigenvector in each block. Equal magnitudes in the original nonzero coordinates become equal magnitudes in the normalized half-shift basis. For a two-dimensional unitary with one flat normalized eigenvector, its orthogonal complementary eigenvector is also flat. Both eigenprojections have diagonal (1/2,1/2), so the unitary has equal diagonal entries. A repeated eigenvalue causes no exception: the unitary is then scalar, and its diagonal entries are again equal.

The even,+ block therefore gives α(b_0−b_2)=0. The even,− block gives γ(b_0+b_2)=0. The positive Hermitian part has every diagonal entry, in every orthonormal block basis, at least cos(3π/8)>0. Hence α and γ cannot vanish. Thus b_0=b_2 and b_0=−b_2, contradicting |b_0|=1. Equivalently, γ times the first equation plus α times the second gives 2αγb_0=0 with all three factors nonzero.

No anti-diagonal shortcut appears in this accepted proof. The actual contradiction is the pair of equal-diagonal equations together with strict positivity. It does not assume an eigenvalue is simple, omit a sector, or exclude a zero factor without justification.

## 6. Strict infimum and legal upper witness

The lower bound holds for all phases; the equality argument excludes every phase pair at the threshold. Since the phase minimum is attained, its value is strictly greater than sin(3π/16). This supplies an existential positive gap but no numerical estimate of it.

For the upper bound, choose P=exp(iπ/4)I and Q=I. Then W=(PF_8)^T(PF_8)=iR_0, where R_0 is reversal, so W has eigenvalues ±i and all singular values of Im(PF_8) equal 1/√2. Taking the real core Re(PF_8) and external left gauge P* gives an original-model residual with exactly that norm. This is a legal zero-correction witness, not an internal-residual norm in a rescaled model.

## 7. Independent controls and remaining limits

`independent_controls.py` was written for this review and has three separate verification routes:

1. Formal direct eight-point Fourier summation with arbitrary a_0,…,a_3,b_0,…,b_3 verifies all four blocks, their invariance, both half-shift commutations, and their commutator characteristic polynomials. A formal flat eigenprojection verifies equal diagonals and repeated-eigenvalue coverage; the two even-sector equations yield the explicit contradiction certificate.
2. Exact rational cyclotomic arithmetic for N=4,8,12,16,20,24 verifies generic flat weighted endpoint cycles, product recurrences, Fourier identities, nondividing elimination, full N-point forward/inverse residual signs, both complementary-support signs, the induced half-periodicity of B, and the opposite endpoint's reversed half-shift signs. The arbitrary cycles are not assumed to satisfy the impossible C8 attainment equations.
3. An independent exact residual computation verifies Y^T Y=I/2 and the external residual Gram I/2 for the upper witness.

Destructive controls check that a nonflat eigenvector does not imply equal diagonal entries, and that a wrong Fourier index fails. The source manifest is independently checked. The main exact result file records 752 passing assertions. `independent_boundary_controls.py` adds six passing exact assertions: an attaining C4 equality example confirms the lower-order boundary is retained, and U=diag(i,−i), T=[[0,1],[1,0]] gives K=−I while a flat K eigenvector is not a U eigenvector. This rejects extending endpoint rigidity to θ=π/2. All planned finite cases completed; no case remains pending or timed out.

Finite controls verify the algebraic implementations, not a continuum or an infinite family by samples. The all-phase C8 exclusion and the uniform necessary theorem follow from the analytic proof audited above. The two-dimensional diagonal argument is deliberately not extrapolated to larger sectors, and the review does not claim the true C8 optimum, a numerical gap, strictness for all larger m, or a general rank/error tradeoff.
