# Independent audit of the Green Phase20 checkpoint

Date: 9 October 2026. Scope: the extracted `fft_green_phase20_weyl_shared_state` materials, the Phase20 start-here note, and the preceding master checkpoint. This report does not change the master or upload anything.

## Bottom line

The core Phase20 algebra is correct under its stated hypotheses. It improves exact certification of a fixed linear Fourier candidate; it does not supply a new Fourier evaluator or an unrestricted Fourier arithmetic lower bound. All uploaded Python files and logs were treated as source text/data, never imported or executed.

Two useful bounds can be strengthened:

1. If even one row of an invertible candidate's inverse has at most `s<N` nonzeros, then `||M-F||₂ >= sqrt(1-s/N)`. Thus a pure product whose inverse rows have at most `s^t` nonzeros has error at least `sqrt(max(0,1-s^t/N))`. The source's weaker `delta/(1+delta)` is valid.
2. If `rank([M,Z]) <= r<N`, then `||M-F||₂ >= cos((2 floor(r/2)+1) pi/(2N))`. For the source's stationary Green architecture with `r=2qt<N`, the bound is `cos((2qt+1) pi/(2N))`. It tends to 1 when `qt=o(N)`, improving the source's limit `1/sqrt(2)`.

Both remain restricted matrix-architecture obstructions. Sums of inverses need not have sparse total inverse; arbitrary intermediate phase masks or independent path permutations need not have low commutator rank.

Independent exact checks and numerical controls all passed. `independent_checks.py` and `results.json` are portable evidence. The numerical parts are controls, not substitutes for the proofs below.

## 1. Full Weyl duality and its quantitative gap

Use `F[j,k]=omega^(jk)/sqrt(N)`, `Z e_k=e_(k+1)`, `D e_k=omega^k e_k`, with primitive complex `omega=exp(-2 pi i/N)`.

From `MZ=DM`, each column is D times its predecessor, hence `M[j,k]=b_j omega^(jk)`. The equation `MD=Z^-1 M` then gives `b_(j+1)=b_j`. Therefore `M=cF`; no invertibility assumption is needed. The `(0,0)` normalization fixes c. This proof works for every integer `N>=2`, not just powers of two, and over a field with a primitive Nth root (with a chosen square root only if normalized F is required).

Let `K=F* M`. Left multiplication of the two defects by F* gives `[K,Z]` and `[K,D]`. The matrices `D^a Z^b/sqrt(N)` are an orthonormal Frobenius basis, and the exact quadratic defect weights are

`|1-omega^a|² + |1-omega^b|²`.

Only `(a,b)=(0,0)` has zero weight. The smallest positive weight is `4 sin²(pi/N)`. Consequently

`min_c ||M-cF||F <= (||MZ-DM||F²+||MD-Z^-1 M||F²)^(1/2)/(2 sin(pi/N))`.

Taking `M=FD` gives equality. This verifies both the constant and its `Theta(1/N)` decay. A small unnormalized residual at increasing N is not a uniform closeness certificate. The bound concerns distance to the scalar Fourier family; the exact scalar calibration is a separate condition.

Independent evidence:

- Exact joint-equation ranks at N=2,3,4,6,8 are N²−1 over GF(20161), so the solution dimension is one.
- Fresh numerical Weyl-basis quadratic identities and equality examples cover N=3,4,5,6,8,9,12,16,24,32,64,128.
- Largest relative discrepancy in the quadratic identity: `3.30e-15`.

## 2. The `1+3h` oracle-call verifier

One call on e0 checks the scalar normalization. In each trial, the calls `M r`, `M(Zr)` and `M(Dr)` check both residuals on the same r. If

`A=MZ-DM`, `B=MD-Z^-1 M`, `rho=rank([A;B])`,

then for a genuinely uniform vector in GF(p)^N the exact joint acceptance probability is `p^(-rho)`. With independent trials it is `p^(-h rho)`. Whenever at least one defect is nonzero, rho>=1, giving the stated `p^-h` bound. Reusing r for the two equations is sound: the relevant kernel is their intersection. If both defects vanish but the scalar is wrong, calibration rejects deterministically.

The guarantee requires a fixed linear map, independent fresh uniform trials, exact field arithmetic and the prescribed dimension. It is not a linearity test, nor protection against an adaptive/stateful oracle that changes its map in response to queries. Source runs with fixed seeds are reproducible tests, not actual draws to which an unconditional Monte Carlo confidence statement can be attached. An OS-backed sampler is a practical randomness source; the mathematical proof is for the ideal independent uniform distribution.

Additional work is linear per trial once field/root/normalizer preparation is available. Streaming uses O(N) extra workspace. The candidate's own preprocessing, memory movement, parameter generation and complete per-input cost remain charged. Field-operation counts are not bit-complexity bounds, and fixed p limits the available transform lengths.

A modular rejection excludes that field realization. To transfer a rejection to a proposed characteristic-zero identity, the entire coefficient specialization must exist: roots and square roots must be compatible, every used inverse must survive, and every denominator must be nonzero. A finite number of passes is not a complex identity proof.

Independent exhaustive enumeration checks over GF(5), N=2, and GF(7), N=3 give exactly `p^(N-rho)` accepted vectors for calibrated entry-perturbed and row-scaled examples. Wrong global scalars pass both identities and fail calibration. Every recorded two-trial positive control uses exactly seven calls.

## 3. Projective curvature, composite lengths, and insufficiency of histograms

All four-entry cross-ratios of a monomially transformed Fourier matrix are Nth roots. A zero entry or non-root cross-ratio is a valid exact exclusion of all invertible outer diagonal scalings and arbitrary row/column permutations. Two queried columns suffice to find such a witness. Passing a selected witness is inconclusive.

For two distinct Fourier columns with permuted index difference Delta, the anchored ratios are `omega^(alpha_j Delta)`, where alpha runs through all residues. If `d=gcd(Delta,N)`, these enumerate the subgroup of order N/d, each element exactly d times. This proof holds for every N, including mixed-prime composite N. The source's dyadic specialization has d a power of two.

For a nonzero-entry explicit matrix, define

`R[j,k]=M[j,k] M[0,0]/(M[j,0] M[0,k])`.

The necessary and sufficient condition is the existence of residue permutations alpha and beta such that `R[j,k]=omega^(alpha_j beta_k)` for every j,k. Anchoring forces `alpha_0=beta_0=0`: beta contains 1 and all entries of R's first row equal 1, and conversely for alpha. Reconstruction is

`M[j,k] = M[j,0] omega^(alpha_j beta_k) M[0,k]/M[0,0]`.

This is a full equivalence criterion, not merely ordinary matrix rank over a possibly nonfield residue ring.

### General composite-length recognition

If the grid is Fourier-equivalent, a primitive anchored root occurs because both residue permutations contain 1. Choose its exponent t at `(i0,j0)` with `gcd(t,N)=1`. Then recover

`alpha_i = E[i,j0]/t mod N`, `beta_j=E[i0,j]`,

check that both are permutations, and check every `E[i,j]=alpha_i beta_j mod N`. Inverting the unit t is legitimate even for composite N. An odd exponent alone is not sufficient outside the dyadic case.

The uploaded `modular_root` explicitly restricts N to powers of two; the uploaded full recognizer uses an odd-exponent pivot and the histogram routine visits dyadic subgroup indices. These choices are consistent with its declared domain, but the file must not be called an implemented arbitrary-composite recognizer. The fresh audit recognizer uses a gcd-unit pivot and works at all admissible lengths.

A root lookup table can be built with N successive multiplications. In the uploaded implementation, tables are built with N separate modular exponentiations; this is additional preparation under a multiplication-level or variable-field-size cost model. Per-entry modular inverses similarly need a convention or can be batch-inverted. The linear-work mathematical fingerprint is attainable, but the primitive-operation implementation/preparation distinction should be retained. This is unrelated to any claimed FFT speedup.

### A concrete all-pairs counterfeit

The Sylvester real Hadamard matrix of order `N=2^m`, m>=2, has only ±1 entries. Every distinct column pair produces ratios +1 and −1, each N/2 times. Thus every two-column subgroup histogram passes with `d=N/2`. Nevertheless it cannot be monomially equivalent to F_N: all its cross-ratios are real, while F_N has a primitive nonreal cross-ratio. The complete recognizer rejects it for lack of a unit-exponent pivot.

Therefore even checking every column-pair histogram is not sufficient; consistency of the full recovered residue grid remains essential. This remains true before considering any evaluation cost.

Independent exact controls reconstruct arbitrary outer-scaled/permuted Fourier matrices at 18 lengths:

`2,3,4,5,6,7,8,9,10,12,15,16,18,20,21,24,28,32`.

All column pairs are checked at each length over GF(20161). Sylvester counterfeits at N=4,8,16 pass all 6,28,120 pair histograms and are rejected by full recognition.

## 4. Sparse-column Weyl defect

For a column b of support at most s<N, write `b_j=omega^(-kj)c_j`. Its k-th defect column has squared norm

`||(Z-omega^k I)b||² = sum_j |c_(j-1)-c_j|²`.

Zeros cut the cycle into Dirichlet paths, each of length at most s. The minimal path-Laplacian eigenvalue is `4 sin²(pi/(2(s+1)))`. Summing the column bounds proves

`||ZB-BD||F >= 2 sin(pi/(2(s+1))) ||B||F`.

A contiguous s-site sine vector with the stated phase gives equality. This proves the sharp constant for every 1<=s<N. If B=M^-1, the exact identity `B(MZ-DM)B=ZB-BD` proves nonvanishing independent of conditioning. Turning it into an absolute lower bound for the defect of M by dividing by `||B||₂²` introduces a gain/conditioning-dependent scale, as the source correctly warns.

## 5. Stronger inverse-support approximation bound

The source's estimate `delta/(1+delta)` follows correctly from inverse perturbation. A direct row argument is stronger and avoids that loss.

Let b be row i of M^-1, with support size s and norm x>0. Then bM=e_i, and because every entry of F has magnitude 1/sqrt(N),

`|(bF)_i| <= sqrt(s/N) x`.

For `epsilon=||M-F||₂`,

`epsilon² x² >= ||b(M-F)||² = ||e_i-bF||² >= 1+x²-2 sqrt(s/N)x`.

Dividing by x² and completing the square gives

`epsilon² >= (1/x-sqrt(s/N))² + 1-s/N >= 1-s/N`.

Hence `||M-F||₂ >= sqrt(1-s/N)`. This needs only one sparse inverse row. If different rows have different support sizes s_i, the strongest available bound uses the smallest s_i.

For a product of t inverses whose sparse denominators each have at most s entries per row, with arbitrary interposed monomial matrices, inverse row support is at most s^t. Thus

`||M-F||₂ >= sqrt(max(0,1-s^t/N))`.

For fixed epsilon<1, achieving error <=epsilon requires `s^t >= N(1-epsilon²)`, and for s>1,

`t >= log_s(N(1-epsilon²))`.

For `t=o(log_s N)`, the bound tends to 1. Exact equality still forces the original support requirement `s^t>=N`. It does not automatically force N log N scalar operations in a shared-state evaluator, nor apply to sums of Green inverses.

The bound is sharp if the only restriction is one inverse row. The audit script checks the independent rank-one construction described in the accompanying exact-bridge work; this report does not claim sharpness under the stronger requirement that every inverse row be sparse. Source and improved values, and numerical equality controls, are recorded in `results.json`.

## 6. Stationary Green commutators and the sharper spectral bound

For `B=aI+bL+cU` in a common cyclic coordinate frame, direct multiplication verifies

`[B,Z]=e0(c e0^T-b e_(N-2)^T)+(b e1-c e_(N-1)) e_(N-1)^T`.

Its rank is at most two, and inversion preserves that rank because `[B^-1,Z]=-B^-1[B,Z]B^-1`. Rank subadditivity and `[AB,Z]=A[B,Z]+[A,Z]B` give budget 2qt for a t-fold product of q-term sums. No uniform conditioning assumption is used.

For Fourier, `[F,Z]=(D-Z)F`. Put `U=D*Z`, a unitary cyclic monomial matrix. It obeys `U^N=(-1)^(N-1)I` and has all N distinct roots of this scalar as eigenvalues. Thus the singular values of D−Z are `|1-lambda|` for those eigenvalues. In descending order, for index r=0,...,N−1, they are exactly

`sigma_(r+1) = 2 cos((2 floor(r/2)+1) pi/(2N))`.

For even N these are all positive, giving Fourier commutator rank N; for odd N the last is zero, giving rank N−1. The source's even-length determinant −2 is correct.

If rank([M,Z])<=r<N, the best rank-r operator approximation inequality gives

`2||M-F||₂ >= ||[M-F,Z]||₂ >= sigma_(r+1)([F,Z])`.

Therefore

`||M-F||₂ >= cos((2 floor(r/2)+1) pi/(2N))`.

With the even budget r=2qt<N this becomes `cos((2qt+1) pi/(2N))`. For example, q=t=2 at N=16,32,64,128 gives lower bounds approximately 0.63439, 0.90399, 0.97570, 0.99391. These use the proved budget 8, not a potentially unreliable floating-point measured rank. They approach 1 when qt=o(N).

For odd N, exact equality requires `2qt>=N−1`; for even N it requires `2qt>=N`. The sharp singular-spectrum formula is independently checked numerically for both parities through N=128, with maximum absolute discrepancy `1.34e-14`. Exact modular path/rank checks cover odd and even lengths 3 through 32.

These arguments exclude independently permuted path frames, arbitrary intermediate nonconstant diagonal masks, and arbitrary outside factors unless those factors are separately shown to obey the needed commutator budget. The strongest surviving noncommuting Green-sum architecture in the source is not excluded by this theorem.

## 7. Real cores and one complex diagonal mask

A real nonzero-entry core has real cross-ratios. Row/column scalings and permutations cannot change that property. F_N has a nonreal primitive-root cross-ratio for N>=3. A core with any zero is excluded immediately. The real-core obstruction is therefore valid under arbitrary outer complex monomial gauges.

For the separate factorization `F=AQB`, with real invertible A,B and complex invertible diagonal Q and no other complex gauges, write F=C+iS. The real symmetric matrices C,S satisfy

`CS=0`, `C²=(I+J)/2`, `S²=(I−J)/2`.

With c the number of fixed points of reflection, their ranks are `(N+c)/2` and `(N−c)/2`. Multiplication by real invertible A,B shows these ranks count the nonzero real and imaginary parts of the diagonal entries of Q. Because Q has N nonzero entries and the counts sum to N, no entry can have both parts nonzero. Exactly the stated numbers are real and purely imaginary. Unit-modulus entries are ±1 or ±i.

A real simultaneous eigenbasis of C and S proves sharpness. In fact, a specified invertible diagonal Q admits some real invertible A,B if and only if it has those axis counts: reorder the Fourier eigenvalues to match the real/imaginary coordinates and absorb their real nonzero ratios to Q into a real factor. This is a factorization classification, not a fast construction of the dense real mixers.

Multiplying Q by a generic global complex phase and cancelling it with an additional outside complex scalar already shows why allowing extra complex outer gauges changes this axis conclusion. The source's explicit restriction is essential.

Fresh even/odd numerical controls confirm the ranks and a real-eigenbasis reconstruction through N=128; largest reconstruction spectral error is `5.69e-14`.

## 8. What was independently replicated versus source-reported

Independently replicated:

- All proof arguments described above.
- Exact dual-Weyl solution dimensions and exhaustive common-kernel probabilities at small lengths.
- General-N full monomial recovery, every pair histogram, and explicit counterfeits.
- Exact common-frame path commutator decompositions and Green product rank budgets.
- Six actual source-parametrized Green products: both ordinary and near-resonant families at N=8,16,32, reconstructed using dense Gaussian inversion rather than the uploaded tridiagonal solver. Every recorded calibration/identity flag, nonzero-coordinate count, oracle-call count and histogram rejection matches the source JSON. Both exact residual matrices have full rank N in all six cases.
- Independent complex numerical equality and stress controls for the claimed constants and stronger bounds.

Read but not reexecuted:

- The source's 74-test log (74 test definitions are present).
- The large N=16384 and N=65536 source runs, inherited 128 tests and nested lineage runners.
- Uploaded benchmark or implementation timing claims.

The six finite-field source reconstructions exclude those specific candidates, not all parameter values or complex-field families. Sample full residual rank is not a general rank theorem.

This audit does not verify the publication-priority claims or the external URLs in `PRIOR_ART.md`/the public-context section. Those are separate bibliographic questions; none is needed for the algebraic conclusions here. Source inventory and nested Phase19 provenance are handled by the enclosing audit.

## 9. Recommended checkpoint wording

Phase20 supplies correct fixed-linear-map Weyl tests, a sharp residual gap, exact projective rejection and explicit equivalence recovery, and valid restricted Green-circuit obstructions. Its inverse-sparse and stationary-commutator approximation floors can both be strengthened to approach 1 in the respective sublogarithmic/sublinear stage regimes. The complete curvature criterion extends to arbitrary N, but the uploaded implementation is dyadic; the independent audit supplies a general-length implementation. Passing even every two-column histogram is insufficient. No new exact unrestricted sub-N-log-N evaluator or arbitrary-arithmetic Fourier lower bound is established.
