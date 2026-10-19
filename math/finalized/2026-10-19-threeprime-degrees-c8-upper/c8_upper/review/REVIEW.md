# Independent review of the exact C8 rank-zero upper witness

19 October 2026 UTC.

## Verdict and bound

**ACCEPT. All 746 independent exact assertions passed.** The mathematical construction is valid as written; no correction to its phases, Fourier normalization, sector formulas, angular branches, or multiplicities is required.

In the original model,

\[
\sin(3\pi/16)<\delta_{8,0}\leq
\frac12\sqrt{1+\sqrt{\sqrt2-1}}
=0.641013699718185162114664052034\ldots.
\]

The lower bound is inherited from the previously accepted strict C8 obstruction. This review independently proves and checks the new upper bound. It does not claim the upper bound equals the minimum.

Frozen candidate proof: `phase_rankzero_exact_20261019_1220/PROOF.md`, SHA-256 `22f8462ed90c58119b0b3abf36d5d47416dd31747716a66d3b0f0a931be0f6e2`.

Inherited lower-bound proof: `phase_rankzero_20261019_1053/PROOF.md`, SHA-256 `4eff619bfde38551a47bf2e109307bb565e09eea5cc42d59213f9513023cb621`. Its accepted independent review is bound separately in the source receipts. No lower-bound checker was rerun.

## 1. Original model and external norm

The accepted definition minimizes

\[
\|F_8-L(C+E)R\|_2
\]

over arbitrary invertible complex monomial outer matrices, arbitrary real matrix core C, and a complex correction E of rank at most r. Here r=0, so E=0. The Fourier matrix is exactly

\[
F_{jk}=8^{-1/2}e^{-2\pi i jk/8},\qquad 0\leq j,k<8.
\]

The unrestricted real core absorbs all real monomial magnitude and permutation factors. Indeed, write L=D_L M_L and R=M_R D_R, with the D factors diagonal unitary and the M factors real invertible monomial. Then LCR=D_L(M_LCM_R)D_R, with a real middle matrix. This is an equality of represented approximants; it does not apply nonunitary scaling to a residual. Thus the model has no hidden conditioning restriction.

For this upper bound, even that full reduction is unnecessary: diagonal unitaries are legal members of the original admissible class. For any diagonal-unitary P,Q, set

\[
V=PFQ,\quad C=\operatorname{Re}_{\rm entry}(V),\quad L=P^*,\quad R=Q^*,\quad E=0.
\]

Then

\[
F-LCR=P^*\big(i\operatorname{Im}_{\rm entry}V\big)Q^*.
\]

The equality of external residual norms is exact because both exterior factors are unitary. The real core has ordinary scalar real entries and is completely specified by the formula. No internal norm or transformed normalization is substituted for the requested norm.

For completeness, minimizing over real C for fixed V gives exactly ||Im V||: taking entrywise imaginary parts is contractive in complex operator norm, and C=Re V attains equality. This establishes the accepted phase reduction without restricting the original model.

## 2. Legal square roots and explicit phases

Let

\[
h=\sqrt{\sqrt2-1},\quad t=\sqrt{2-\sqrt2},\quad z=h+it,
\quad \zeta=e^{i\pi/4},\quad \rho=e^{i\pi/8}.
\]

The positive radicals satisfy h²+t²=1, so |z|=1. Also 0<h<1/√2 and t>h, so the argument of z is strictly between π/4 and π/2. Define

\[
w=\sqrt{(1+h)/2}+i\sqrt{(1-h)/2}.
\]

Then |w|=1. Squaring gives real part h and positive imaginary part √(1−h²)=t, hence w²=z with no sign ambiguity. Also ρ²=ζ.

Repeat the following four entries twice:

\[
P=\operatorname{diag}(-iw,\rho^{-1}w,1,\rho^{-1},\ldots),
\qquad
Q=\operatorname{diag}(1,\rho^3w^{-1},iw^{-1},\rho^3,\ldots).
\]

All entries have unit modulus, and their squares are exactly

\[
A=P^2=\operatorname{diag}(-z,\zeta^{-1}z,1,\zeta^{-1},\ldots),
\qquad
B=Q^2=\operatorname{diag}(1,\zeta^3/z,-1/z,\zeta^3,\ldots).
\]

In particular, the third entry of Q squares to −1/z, not +1/z. The independent destructive control changes that sign and rejects the claimed Gram spectrum.

## 3. Full Fourier decomposition

Set U=FAFB. Four-periodicity is an imposed feature of this witness only. The coefficient formula

\[
(FAF)_{jk}=\frac18\sum_{m=0}^{7}a_m\zeta^{-(j+k)m}
\]

vanishes when j+k is odd, since pairing m with m+4 contributes the factor 1+(−1)^{j+k}. Also U commutes with the half-shift j↦j+4. Therefore the four two-dimensional parity/half-shift sectors form a complete orthogonal decomposition of the full eight-dimensional space.

For parity j=0 or 1 and sign η=±1, take the ordered basis

\[
\frac{e_j+\eta e_{j+4}}{\sqrt2},\qquad
\frac{e_{j+2}+\eta e_{j+6}}{\sqrt2}.
\]

Define

\[
\alpha=(1-z)/2,\quad \beta=-(1+z)/2,
\quad \gamma=\zeta^{-1}(1+z)/2,
\quad \delta=i\zeta^{-1}(1-z)/2.
\]

Direct eight-point summation gives, in the order even,+; even,−; odd,+; odd,−,

\[
\begin{aligned}
M_0&=\begin{pmatrix}\alpha&\beta\\\beta&\alpha\end{pmatrix}\operatorname{diag}(b_0,b_2),\\
M_1&=\begin{pmatrix}\gamma&\delta\\\delta&-\gamma\end{pmatrix}\operatorname{diag}(b_0,b_2),\\
M_2&=\begin{pmatrix}\beta&\alpha\\\alpha&\beta\end{pmatrix}\operatorname{diag}(b_1,b_3),\\
M_3&=\begin{pmatrix}\delta&-\gamma\\-\gamma&-\delta\end{pmatrix}\operatorname{diag}(b_1,b_3).
\end{aligned}
\]

The fresh checker builds F, A, B and the orthogonal change of basis directly, verifies every full-matrix entry of this decomposition, and then computes each trace and determinant. Because z+z⁻¹=2h, the exact results are

- M₀ and M₃: trace 1−h; determinant 1.
- M₁ and M₂: trace ζ⁻¹(1+h); determinant −i.

All four blocks are unitary. No sector is dropped, and no spectral exclusion of an anti-diagonal matrix is used.

## 4. Exact spectral multiplicities and branches

Write

\[
c=(1-h)/2,\quad d=(1+h)/2=1-c,
\quad \theta=\arccos c,\quad \beta_0=\arccos d.
\]

The first block type has characteristic polynomial x²−2cx+1, so its roots are e^{±iθ}. The second type has roots ζ⁻¹e^{±iβ₀}; multiplication by ζ changes its determinant to one and its trace to 2d.

There is an exact useful identity

\[
s:=\sqrt2d-c>0,\qquad c^2+s^2=1.
\]

It follows from h²=√2−1. Thus s=sin θ and

\[
\cos(\theta-\pi/4)=(c+s)/\sqrt2=d.
\]

Since 0<c<1/2, θ∈(π/3,π/2). Hence θ−π/4 lies in (0,π/2), and comparison with β₀∈(0,π/2) yields β₀=θ−π/4. This explicitly fixes the branch, rather than inferring an angle from its cosine alone.

Across all four blocks the complete spectrum is

\[
e^{i\theta}\ (2),\qquad e^{-i\theta}\ (4),\qquad
e^{i(\theta-\pi/2)}\ (2).
\]

These three eigenvalues are distinct. The maximum absolute principal argument is θ, because |θ−π/2|<θ. The candidate's eight eigenvalues and multiplicities are therefore correct.

For V=X+iY, W=VᵀV is symmetric unitary. Unitarity of V gives

\[
Y^T Y=(I-\operatorname{Re}_{\rm entry}W)/2.
\]

Also Q⁻¹WQ=FAFB=U. The real and imaginary parts of W commute and are real symmetric, so an eigenvalue e^{iφ} contributes (1−cos φ)/2 to YᵀY with the same multiplicity. Thus

\[
\|Y\|_2=\sin(\theta/2)=\frac12\sqrt{1+h}.
\]

The entrywise real part of W equals its Hermitian part because W is symmetric. For the generally nonsymmetric U, only its Hermitian part is used; those operations are not conflated.

## 5. Independent direct external-residual certificate

There is also a direct verification that avoids using phase eigenvalues to compute the final norm. Expanding the actual real core gives the actual external residual

\[
D:=F-P^*\operatorname{Re}_{\rm entry}(PFQ)Q^*
=\frac12\left(F-A^{-1}\overline F B^{-1}\right).
\]

Since F is symmetric unitary, direct multiplication yields

\[
D^*D=\frac12B\left(I-\frac{U+U^*}{2}\right)B^*.
\]

Define

\[
a=(1+h)/4,\qquad b=(3-\sqrt2-(1+\sqrt2)h)/4.
\]

The fresh checker constructs D from its full eight-by-eight formula, multiplies out its Gram matrix G=D*D, and independently verifies exactly

\[
(G-aI)(G-bI)=0,\qquad \operatorname{tr}G=6a+2b.
\]

It additionally checks all off-sector zeros of G and the trace and determinant of each direct Gram block: two have (2a,a²), and two have (a+b,ab). Thus the characteristic polynomial is exactly

\[
\chi_G(x)=(x-a)^6(x-b)^2.
\]

Here b=(1−sin θ)/2, a=(1−cos θ)/2 and π/4<θ<π/2, so 0<b<a. The actual original-model external residual has singular values √a with multiplicity six and √b with multiplicity two. Its norm is exactly √a, proving the upper bound by a second route. This is not merely a floating-point residual check.

## 6. Independent controls and integrity

`independent_exact_controls.py` is newly written for this review. Its core algebra uses exact rational algebraic-field coefficients and polynomial reduction by

\[
h^2=\sqrt2-1,\qquad z^2-2hz+1=0.
\]

Conjugation sends z to 2h−z and i to −i. The positive radical embedding is verified separately, including all actual P²=A and Q²=B identities. These identities apply to the stated radicals; no numerical tolerance is used in the proof controls.

Checks cover normalized Fourier unitarity, phase unitarity, all sector entries, all block traces and determinants, actual square roots, the directly computed external residual Gram, its exact two-root polynomial, multiplicities, and the angular/half-angle identities. Destructive controls reject removal of the Fourier normalization and a sign error in the third B phase.

The candidate manifest and all five of its certificate files are independently byte-counted and hashed before and after the computation. Both the inherited lower proof and its accepted review are similarly bound. Candidate source code is only hashed, never imported or executed. Neither historical code nor exploratory optimization code is executed. No external state is modified. The completed machine-readable result records 746 passing assertions and 36.32410109299235 seconds of measured checker runtime. All planned controls completed; no pending calculation or timeout remains.

The candidate's historical exploratory evaluation counts and timings are its own reported provenance, not independently measured by this review. They are not mathematical premises of the accepted bound.

## 7. Scope and derived comparison

The witness has four-periodic phases. This does not imply that every feasible point or every minimizer is four-periodic; the proof establishes an upper bound from one legal point in the unrestricted model. Arbitrary nonperiodic phases, arbitrary complex monomial magnitudes/permutations, and every admissible real core remain within the original minimization problem.

The exact global optimum remains open. The inherited strict lower bound is unchanged. In particular, this result gives no explicit new positive lower gap above sin(3π/16), no minimizer classification, and no claim at other dimensions or correction ranks.

The interval width is approximately 0.08544346669858294. Relative to the former interval with upper endpoint 1/√2, the width decreases by approximately 43.6153%. This percentage is a derived secondary comparison, not an independent theorem or a claim about a search's progress toward the true optimum.
