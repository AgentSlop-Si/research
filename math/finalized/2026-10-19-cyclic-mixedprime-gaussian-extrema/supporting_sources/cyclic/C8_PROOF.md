# Sharp unrestricted C8 phase minimax by a cyclic-shift commutator

19 October 2026 UTC. This is a new global argument. The argument is analytic and uniform over the full phase torus; no finite search or local certificate is used to establish its lower bound. It makes no claim of literature novelty.

## 1. Statement and conventions

All indices are modulo 8. Let

F[j,k] = exp(−π i j k/4)/sqrt(8),

and let S be the forward cyclic shift, S e_j = e_{j+1}. A star denotes conjugate transpose. Singular values are ordered decreasingly.

**Theorem.** For every pair of diagonal unitary matrices A,B of order 8, every open arc of angular width π/4 contains at most five eigenvalues, counted with multiplicity, of M=F A F B.

Consequently, for diagonal unitaries P,Q,

min σ₃(Im(P F Q)) = sin(π/16).

The lower bound is proved below without a periodicity assumption. The accepted explicit upper witness is restated in Section 6. Together with the accepted fixed-phase rank-one reduction, this determines the original unrestricted-real-core, complex-rank-one operator-norm approximation value as sin(π/16).

## 2. An elementary commutator approximation lemma

**Lemma.** Let M,T be unitaries of order n. Suppose at least n−r eigenvalues of M lie in an open arc centered at 1 with angular radius θ, where 0<θ<π/2. Put K=M T M* T*. Then at least n−2r eigenvalues of K, counted with multiplicity, have principal arguments of absolute value strictly less than 2θ, provided n−2r>0.

**Proof.** Choose n−r eigenvalues in the given arc, with a full orthonormal eigenbasis for M, including repeated eigenspaces. Form the unitary M₀ by replacing those selected eigenvalues by 1 and leaving the remaining r eigenvalues unchanged. Then

rank(M₀−I) ≤ r.

The unitary E=M₀* M has the selected eigenvalues of M and r further eigenvalues equal to 1. Thus every eigenvalue e^{it} of E has |t|<θ. Since E is normal and cos θ>0,

|e^{it}−cos θ|² = 1+cos²θ−2cos θ cos t < sin²θ,

and therefore ||E−cos θ I||₂ < sin θ. (For the unselected eigenvalues t=0 this is also strict.)

Let K₀=M₀ T M₀* T*. The matrices M₀ and E commute, though the estimate below only uses M=M₀E. We have

rank(K₀−I)
 = rank((M₀T−TM₀)M₀*T*)
 ≤ rank((M₀−I)T) + rank(T(M₀−I)) ≤ 2r.

Hence L=ker(K₀−I) has dimension at least n−2r. Moreover,

||K−K₀||₂
 = ||E T E*−T||₂
 = ||ET−TE||₂
 = ||(E−cos θ I)T−T(E−cos θ I)||₂
 ≤ 2||E−cos θ I||₂ < 2sin θ.

For every x∈L,

||(K−I)x||₂ = ||(K−K₀)x||₂ < 2sin θ ||x||₂

when x≠0. In fact the displayed operator-norm bound is uniform on L. The singular-value min–max principle implies that at least n−2r singular values of K−I are strictly below 2sin θ. Because K is unitary, K−I is normal and these singular values are exactly |λ−1| for the eigenvalues λ of K, with multiplicities. For the principal argument φ∈[−π,π],

|e^{iφ}−1| = 2sin(|φ|/2).

Since θ<π/2, the inequality |e^{iφ}−1|<2sin θ is equivalent to |φ|<2θ. This proves the lemma. □

Multiplying M by any scalar unitary changes neither K nor the lemma's argument. Hence the lemma applies to an arc with any center after rotating M.

## 3. The exact cyclic-Hankel commutator

Write C=F A F. Its entries have the cyclic-Hankel form

C[j,k] = (1/8) Σ_{l=0}^7 a_l exp(−π i(j+k)l/4).

Thus C is unitary and

C S = S* C,  equivalently C S C* = S*.

Set T=B* S B. It is unitary, and for M=C B,

M T M* = C B(B*SB)B*C* = C S C* = S*.

Therefore the exact commutator is

K=M T M* T* = S* B* S* B.                       (3.1)

In particular, A has disappeared from this commutator. Writing B=diag(b₀,…,b₇), formula (3.1) gives

K e_j = b_j conjugate(b_{j−1}) e_{j−2}.           (3.2)

This is a direct sum, on the even and odd coordinate spaces, of two weighted cyclic shifts of length four. Each weight is unimodular. If

Γ=(b₀b₂b₄b₆)/(b₁b₃b₅b₇),

then the two cycle products are Γ and Γ⁻¹. Consequently

χ_K(x)=(x⁴−Γ)(x⁴−Γ⁻¹).                        (3.3)

Each degree-four factor has four distinct roots equally spaced by π/2 around the unit circle. Each open arc of width π/2 contains at most one root of each factor, so at most two eigenvalues of K in total, counted with multiplicity. This remains true if the two factors have common roots, in which case such roots are counted once from each cycle.

The identity (3.3) follows directly by applying (3.2) four times on each cycle. It is not inferred from sample phases.

## 4. Proof of the spectral anti-concentration theorem

Suppose that M has at least six eigenvalues in some open arc of width π/4. Rotate M by a scalar unitary so the arc is centered at 1. This rotation does not change K in (3.1). The six selected eigenvalues lie in |arg λ|<π/8.

Apply the commutator lemma with n=8, r=2, and θ=π/8. It gives at least 8−4=4 eigenvalues of K in the open arc |arg λ|<π/4, whose angular width is π/2. Section 3 proves that this arc contains at most two eigenvalues. The contradiction proves the theorem. □

Both openness and multiplicity have been retained at every step. At the sharp witness, relevant eigenvalues may be at the arc endpoints, so replacing either open arc by its closed counterpart is not permitted.

## 5. Reduction to imaginary singular values

Let V=P F Q, with P,Q diagonal unitary, and put W=VᵀV. As Fᵀ=F,

W=Q F P² F Q,
Q⁻¹ W Q=F P² F Q².

Thus W has the spectrum of a matrix M from the theorem. It is both symmetric and unitary. Write W=R+iJ, where R,J are real symmetric. Unitarity implies R²+J²=I and RJ=JR. Therefore R,J are simultaneously diagonalizable by a real orthogonal matrix, with eigenvalues cos φ_j and sin φ_j, where e^{iφ_j} are the eigenvalues of W.

Writing V=X+iY and using V*V=I yields

YᵀY = (I−Re W)/2.

Hence the singular values of Y are, as a multiset,

|sin(φ_j/2)|.

If σ₃(Y)<sin(π/16), at least six eigenvalues of W have principal arguments |φ_j|<π/8. This contradicts the theorem applied to A=P² and B=Q². Thus

σ₃(Im(PFQ)) ≥ sin(π/16)

for all P,Q.

This argument does not restrict squared phases to the four-periodic sector and does not use the previously available coarse lower bound or local analysis.

## 6. Sharpness and original rank-one objective

For the accepted witness, let z=exp(iπ/16), s=sin(π/16), c=cos(π/16),

q=(1,z²,1,z¹⁰,1,z²,1,z¹⁰), Q=diag(q), P=zQ,
V=PFQ, Y=Im V,
a=(1,0,−1,0,−1,0,1,0)ᵀ/2,
b=(0,1,0,1,0,1,0,1)ᵀ/2,
R=aaᵀ+bbᵀ.

The exact identities

Y²=s²I+(c²−s²)R,  Ya=cb,  Yb=ca

give σ₃(Y)=s. They are restated from the accepted witness; a fresh narrow characteristic-zero check accompanies this packet.

For the original fixed-phase problem, every complex rank-at-most-one E has real rank(Im E)≤2, so real Eckart–Young and the operator-norm contraction of entrywise imaginary part give

min over real B and rank_C E≤1 ||V−(B+E)||₂ ≥ σ₃(Im V).

Conversely, every real rank-at-most-two matrix Y₀=a₁b₁ᵀ+a₂b₂ᵀ is the imaginary part of

E=(a₁+i a₂)(b₂+i b₁)ᵀ,

which has complex rank at most one. Set B=Re(V−E). This realizes the reverse inequality and establishes equality for every fixed V. Diagonal unitary multiplication preserves the operator norm, so the global objective in the original outer-phase formulation is also s.

The same value applies when the allowed outer gauges are arbitrary invertible complex monomial matrices. Indeed, write the left gauge as P₀R₁ and the right gauge as R₂Q₀, where P₀,Q₀ are diagonal unitary and R₁,R₂ are invertible real monomial matrices. Then

P₀R₁(B+E)R₂Q₀ = P₀(B′+E′)Q₀,

where B′=R₁BR₂ is an arbitrary real matrix and E′=R₁ER₂ still has complex rank at most one. Invertibility makes this a bijective reparameterization of the allowed B,E. No nonunitary multiplication of the residual is performed, so no condition-number factor or conditioning assumption is introduced.

At the displayed witness an explicit legal correction is

E=c(a+i b)(a+i b)ᵀ,
B=Re V−c(aaᵀ−bbᵀ).

Then V−(B+E)=i[Y−c(abᵀ+baᵀ)], whose norm is exactly s. Therefore the lower bound is attained.

## 7. Scope and verification

The universal proof is Sections 2–5. Exact symbolic checks verify the finite algebraic identities and the sharp witness, not the continuum of all phase choices by sampling. Independent review should check the commutator rank bound, the strict scalar-centering bound, the min–max multiplicity count, the two weighted cycles, and the original objective reduction.
