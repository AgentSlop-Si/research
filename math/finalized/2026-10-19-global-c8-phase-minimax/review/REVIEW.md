# Independent review: sharp unrestricted C8 rank-one phase minimax

Review date: 19 October 2026 UTC.

## Verdict

ACCEPT. The new global commutator proof closes the unrestricted continuous-phase lower bound. For the normalized negative-sign Fourier matrix

F[j,k] = exp(−π i j k/4)/sqrt(8), 0≤j,k<8,

one has

min over diagonal unitary P,Q of σ₃(Im(PFQ)) = sin(π/16).

Singular values are ordered decreasingly. Equivalently, the minimum external operator-norm error in approximating F by L(B+E)R is sin(π/16), where B is an unrestricted real 8×8 matrix, rank_C(E)≤1, and L,R are arbitrary invertible complex monomial matrices. Arbitrary magnitudes and permutations do not enlarge the represented feasible set beyond diagonal unitary outer phases, by the absorption argument below.

No mathematical correction to the candidate's global proof is required. A requested clarification about arbitrary monomial outer gauges preserves the accepted model; it is not an additional hypothesis. The independently accepted upper witness is also reverified here from scratch.

The accepted additional spectral statement is: for arbitrary diagonal unitary A,B, every open arc of angular width π/4 contains at most five eigenvalues, with multiplicity, of F A F B. The word open is essential.

## 1. Exact conventions and Hankel intertwining

Let S e_j=e_{j+1}, all indices modulo eight. C=F A F is unitary because F and A are unitary. Its entries are

C[j,k]=(1/8) Σ_l a_l exp(−π i(j+k)l/4).

Thus C[j,k] depends only on j+k modulo eight. Entrywise,

(CS)[j,k]=C[j,k+1]=C[j+1,k]=(S* C)[j,k].

Hence CS=S*C and CSC*=S*. These signs and the use of F on both sides of A, rather than F*, are correct.

Set M=CB and T=B*SB. Since B is unitary,

M T M*=C S C*=S*,
K=M T M* T*=S* B* S* B.

The reviewer independently checked the generic coefficient formula for all 512 triples (j,k,l), the symbolic Hankel relation for eight arbitrary coefficients, and the weighted-shift formula. No phase sample is used in any generic check.

## 2. Spectral replacement, including multiplicities

Suppose n−r eigenvalues of a unitary M lie in |arg λ|<θ, with 0<θ<π/2. Choose an orthonormal eigenbasis and select n−r of its vectors. Replacing precisely those eigenvalues by one produces a unitary M0 with rank(M0−I)≤r. This construction is valid even if a repeated eigenvalue has vectors both inside and outside the selected list. No simple-spectrum assumption or differentiable eigenvalue branches are needed.

E=M0*M is unitary. Its eigenvalues are the selected eigenvalues of M and r copies of one. All have principal arguments strictly between −θ and θ. For each e^{it} in that spectrum,

sin²θ − |e^{it}−cosθ|² = 2 cosθ (cos t−cosθ)>0.

The inequality is strict also for t=0 because θ>0. Normality and finiteness of the spectrum therefore give a strict uniform operator-norm bound

||E−cosθ I||<sinθ.

This scalar centering is the crucial factor-two improvement over bounding E−I directly. The proof does not assume that all eigenvalues of the original M lie in the arc.

## 3. Fixed-space dimension and norm transfer

For K0=M0 T M0* T*,

K0−I=(M0T−TM0)M0*T*.

Since M0T−TM0=(M0−I)T−T(M0−I), rank(K0−I)≤2r. Thus L=ker(K0−I) has dimension at least n−2r over the complex numbers. All dimension counts in the proof are complex counts, consistent with unitary eigenvalue multiplicities.

The factorization M=M0E gives

||K−K0||=||ETE*−T||=||ET−TE||
≤2||E−cosθ I||<2sinθ.

The equality of norms follows by multiplication on the left and right by unitaries. No commutation between E and T is assumed. The fact M0 commutes with E is true but unnecessary for this estimate.

For every x∈L,

||(K−I)x||=||(K−K0)x||≤||K−K0|| ||x||.

The uniform upper bound is strictly less than 2sinθ.

## 4. Singular-value-to-eigenphase count

For a positive semidefinite H=(K−I)*(K−I), the min–max principle on the subspace L implies that at least dim L eigenvalues of H are strictly smaller than 4sin²θ. This implication does not assert that L is an invariant subspace for K or H.

An equivalent direct dimension argument avoids any ordering ambiguity. If fewer than dim L singular values were strictly below 2sinθ, the span of right singular vectors having singular values at least 2sinθ would intersect L nontrivially. Every nonzero vector in that intersection would contradict the strict norm bound on L.

Because K is unitary, K−I is normal, so its singular values are exactly |λ−1| for the eigenvalues λ of K, with multiplicities. For principal arguments φ∈[−π,π],

|e^{iφ}−1|=2sin(|φ|/2).

On [0,π/2], sine is strictly increasing. Therefore |λ−1|<2sinθ is equivalent to |arg λ|<2θ. At least n−2r eigenvalues of K lie in that open arc. No inference from nonnormal eigenvalue perturbation is involved.

The closed-arc variant with selected phases |arg λ|≤θ similarly gives a non-strict conclusion. The candidate correctly uses the strict version at θ=π/8.

## 5. Exact weighted cycles and contradiction

The action of K is

K e_j=(b_j/b_{j−1}) e_{j−2}.

Even and odd coordinates give two invariant cycles of length four. Their products are Γ and Γ⁻¹, where Γ=(b0 b2 b4 b6)/(b1 b3 b5 b7). Hence

χ_K(x)=(x⁴−Γ)(x⁴−Γ⁻¹).

Every root of either factor is simple because Γ≠0. Its four roots have angular spacing exactly π/2. An open arc of angular width π/2 contains at most one root from either factor. If the factors coincide or share roots, multiplicity adds across the two cycles; the same upper bound of two still holds.

If M has six eigenvalues in an open arc of width π/4, scalar rotation centers that arc at one. Scalar rotation cancels out of M T M*T*, so it leaves K unchanged. Apply the replacement lemma with n=8, r=2 and θ=π/8. It forces at least four eigenvalues of K into |arg λ|<π/4, an open arc of width π/2. The exact cycle count permits at most two. This is the required contradiction, valid for every diagonal unitary A,B, including transcendental phases.

## 6. Link to the original objective

For V=PFQ, write V=X+iY with X,Y real, and W=VᵀV. Then

W=Q F P² F Q,  Q⁻¹WQ=F P² F Q².

W is symmetric and unitary. Its real and imaginary parts are commuting real symmetric matrices, hence admit a common real orthonormal eigenbasis. Unitarity of V gives

YᵀY=(I−Re W)/2.

Thus the singular values of Y, as a multiset, are |sin(φ_j/2)|, where e^{iφ_j} are the eigenvalues of W with principal arguments. A strict inequality σ₃(Y)<sin(π/16) would give at least six eigenvalues |φ_j|<π/8. The spectral theorem just proved rules that out. Squaring phases causes no restriction: every diagonal unitary A,B has diagonal unitary square roots P,Q.

For fixed V, entrywise imaginary part is an operator-norm contraction: Im Z=(Z−conjugate Z)/(2i), and ||conjugate Z||=||Z||. If rank_C E≤1, rank_R Im E≤2. Real Eckart–Young therefore gives

||V−B−E||≥σ₃(Im V)

for every real B. Conversely a best real rank-two approximation Y0 to Y can be written a1 b1ᵀ+a2 b2ᵀ. The complex rank-at-most-one matrix

E=(a1+i a2)(b2+i b1)ᵀ

has Im E=Y0. Taking B=Re(V−E) realizes equality in the norm bound. The phase torus is compact and the singular-value objective continuous, so the global minimum is attained.

For arbitrary invertible complex monomial L,R, factor L=D_L S_L and R=S_R D_R with D_L,D_R diagonal unitary and S_L,S_R real invertible monomial. Then

L(B+E)R=D_L(S_L B S_R+S_L E S_R)D_R.

The new real core remains unrestricted real and the complex correction rank is unchanged. This is equality of represented approximating matrices before subtraction from F. It does not transform the external residual by ill-conditioned inverse gauges. Consequently no conditioning restriction or additional factor appears.

## 7. Exact attainment and endpoint controls

With z=exp(iπ/16), q=(1,z²,1,z¹⁰,1,z²,1,z¹⁰), Q=diag(q), P=zQ, s=sin(π/16), c=cos(π/16), and

a=(1,0,−1,0,−1,0,1,0)ᵀ/2,
b=(0,1,0,1,0,1,0,1)ᵀ/2,
R=aaᵀ+bbᵀ,

the fresh independent checker verifies

Y²=s² I+(c²−s²)R,  Ya=cb,  Yb=ca.

R and I−R are orthogonal projectors of ranks two and six. Therefore σ₃(Y)=s. The explicit correction E=c(a+i b)(a+i b)ᵀ and real core B=Re V−c(aaᵀ−bbᵀ) have residual iYres, with Yres²=s²(I−R). Its norm is exactly s. Every one of the 784 two-by-two minors of E vanishes, and E is nonzero. The original outer residual identity is checked exactly.

Independent exact spectral projectors verify the boundary spectra:

- M: z² with multiplicity four; z⁻² with multiplicity two; z¹⁴ with multiplicity two.
- K: z⁴, z⁻⁴, z¹², z⁻¹², each with multiplicity two.

Thus the closed original arc |arg λ|≤π/8 contains six eigenvalues, and the closed commutator arc |arg λ|≤π/4 contains four. Both corresponding closed-arc anti-concentration statements are false. These controls confirm the necessity of the strict endpoints rather than merely leaving that point implicit.

## 8. Verification provenance and accepted limits

The reviewer wrote and executed only the fresh independent_checker.py in this review directory. It uses standard-library exact Fractions, a separate explicit cyclotomic arithmetic implementation, and installed SymPy for symbolic rational-function identities and exact polynomial inverses. It imports no author or historical research program. The candidate's narrow checker was read but not executed; the independent implementation independently confirms its mathematical outputs.

INDEPENDENT_RESULTS.json records all checks, 512 generic Fourier coefficients, 784 rank-one minors, exact spectral projectors, and six destructive controls. Finite checks support the algebraic identities; the universal proof is the analytic argument above. No numerical optimization, phase grid, floating-point eigenvalues, unproved periodicity reduction, local-neighborhood assumption, or semialgebraic search is used.

This acceptance closes the named C8 unrestricted-real-core, one-complex-rank-one, external-operator-norm minimax problem, and the stated spectral anti-concentration theorem. It does not establish uniqueness or classify all minimizers; it does not claim historical novelty, a general finite-group minimax theorem, an FFT operation-count lower bound, or a Green-specific construction. Existing exact rank-only results and local results retain their own scopes, but they are no longer needed as missing ingredients for this sharp lower bound.

No external service, repository, Library item, or historical source was modified during this review. Frozen candidate and source snapshots and a SHA-256 manifest are included separately.
