# Exact common-chirp recognition with blocked verification

10 October 2026. Candidate new-to-corpus complexity sharpening of C06. Classical short convolution, Prony and chirp-z identities are the mechanisms; external priority is unresolved. Rabiner–Schafer–Rader1969 explicitly discusses sectioned chirp-z with overlap-add/save, so the block mechanism itself is established; the new-to-corpus result is its charged integration into this exact recognizer. This is a proof of an algorithmic bound, not a claim that the old dispatcher implements it.

## 1. Full theorem and model

Let r≥1, N≥3r, p be a supplied prime with N|(p−1), and ω∈F_p a supplied certified primitive Nth root. Let κ=log_2 3. There is a deterministic exact recognizer for the union

x_j=ω^{aj²}Σ_{ell=1}^s c_ell ω^{b_ell j}, 0≤j<N, 0≤s≤r,

with distinct b_ell modulo N and nonzero listed c_ell. It accepts precisely this family, returns a completely verified representation, and on acceptance computes all N DFT outputs. The empty representation handles the zero vector.

Using the established polynomial Toeplitz eliminant construction, plus the blocked procedures proved below, the costs are

O(Nr^{2+κ}+r^{2+3κ}) field additions and multiplications,
O(1+r^4) scalar field inversions,
O(N+r^4) field-element storage.

All input reads, dechirping, tables of supplied root powers, candidate tests, coefficient writes and output writes are included. Field/root discovery, bit complexity, exact input encoding, and numerical stability are separate. Indices have O(log N) bits; products of a constant number of such indices occupy O(1) appropriately sized words or are reduced using charged modular arithmetic. Integer gcd/inverse work in the accepted Gauss evaluator is separately charged as in the existing theorem.

In particular, for r=o((log N)^{1/(2+log_2 3)}), this arithmetic count is o(N log N). The exponent 1/(2+log_2 3)≈0.27894 improves the earlier sufficient exponent 1/4. This is only a certified structured-input fast path, with exact rejection outside the family. It neither transforms arbitrary rejected inputs nor proves a general exact sub-NlogN Fourier algorithm.

## 2. Established eliminant ingredient, with its exact contract

For a nonzero family member, no r consecutive entries can be zero: after dechirping, any s consecutive zeros give an invertible s-node Vandermonde system. Since [r,N−r−1] contains at least r entries, it has a center c with x_c≠0. An arbitrary nonzero input lacking such a center can be rejected.

Set n=r+1 and f(d)=d(d−1)/2 for every integer d. Form the polynomial Toeplitz matrix

A(t)_{ij}=x_{c+i−j}t^{f(i−j)}, 0≤i,j≤r.

Its determinant E(t) has degree at most D=binom(r+2,3), constant term x_c^{r+1}≠0, and vanishes at t=ω^{−2a} for every valid common phase. The vanishing follows by column reversal and nonzero chirp row/column scalings from the dechirped (r+1)-square Hankel determinant. The degree follows from rearrangement of Σ_i f(i−σ(i)); the maximum is D. The only zero exponents f(d) occur at d=0,1, so A(0) is lower bidiagonal with nonzero diagonal x_c.

Thus every leading principal minor has invertible constant term. A nonsymmetric Levinson recursion over F_p[t]/(t^{D+1}) computes det A in O(r² M(D+1)) operations and O(r(D+1)) storage, where M(k)=O(k^κ) is Karatsuba polynomial multiplication. Each ring inverse starts from the same scalar x_c^{-1}; Newton doubling g←g(2−eg) works in every characteristic. No integer division, field extension, factoring, or D+1 distinct interpolation nodes is assumed. This is the prior independently audited Toeplitz construction; its recurrence and proof are preserved in the source manifest.

Scan E at the L=N/gcd(2,N) distinct values ω^{−2a}, 0≤a<L, by Horner at cost O(N(D+1)). At most C=min(D,L) phases remain. When N is even, a+N/2 is absorbed by translating every linear frequency by N/2, so the canonical range is complete. It does not assert uniqueness of the accepted representation.

## 3. Blocked evaluation on the full root grid

Let f(z)=Σ_{j=0}^s f_jz^j, s≤r, and b=s+1. All f(ω^k), 0≤k<N, can be computed in

O(Nb^{κ−1}+b^κ)=O(N(r+1)^{κ−1})

field operations and O(N+b) storage, since b≤r+1≤N.

Partition k=K+a into blocks 0≤a<b, allowing a shorter final block. For fixed K put u_j=f_jω^{Kj+binom(j+1,2)}, and v_d=ω^{−binom(d,2)} for −s≤d≤b−1. The integer identity

aj=binom(a,2)+binom(j+1,2)−binom(a−j,2)

gives

f(ω^{K+a})=ω^{binom(a,2)}Σ_{j=0}^s u_jv_{a−j}.

This is a length-b by length-(2b−1) ordinary convolution. A constant number of balanced Karatsuba products suffices, in O(b^κ). Root powers and all scalings cost O(b) per block. The kernel is reusable, and passing K to K+b updates f_jω^{Kj} using precomputed ω^{bj} in O(b). Hence ceil(N/b) blocks have the claimed fully charged cost. The formula uses integer binomial exponents only, with no division by 2 in the field and no square root of ω.

## 4. Blocked full-input recurrence verification

Given monic p(z)=Σ_{j=0}^s p_jz^j and the entire dechirped vector y, every recurrence residual

R_k=Σ_{j=0}^s p_jy_{k+j}, 0≤k<N−s,

can be computed with the same O(N(s+1)^{κ−1}) bound. Convolve y with the reversed coefficient list [p_s,…,p_0]; R_k is coefficient k+s. Partition y into chunks of length b=s+1, multiply each chunk by that fixed length-b list, and overlap-add. There are ceil(N/b) products of degree O(b), plus O(N) coefficient accumulation. Every input coordinate is included. This is an exact global verification, not a test of a short prefix.

## 5. A sound and complete per-phase Prony test

For each candidate a, dechirp all N entries in O(N). Compute s=rank H_r, H_r=[y_{i+j}]_{0≤i,j<r}, using dense elimination. If s=0 accept this phase only when the full vector is zero. Otherwise require that the leading s-square Hankel block be nonsingular, and solve

Σ_{j=0}^{s−1}p_jy_{i+j}=−y_{i+s}, 0≤i<s,

then set p_s=1. Reject the phase if the leading block is singular. This setup costs O(r³) additions/multiplications and O(r) inversions, with at most O(r²) storage.

Use §3 to scan every ω^k. Require exactly s distinct roots of p on this supplied grid. This certifies that p has precisely these roots, all nonzero and simple, without uncharged factorization. Use §4 to require all N−s recurrence residuals to be zero. Solve the s-square Vandermonde system for weights using the first s entries, and omit any zero weights.

Soundness: the reconstructed exponential sum matches the first s samples and obeys the same monic recurrence. The fully checked residual equations and induction force agreement with all N raw samples. Completeness: for a true s-term sum, H_r=V_r diag(c)V_r^T has rank s because V_r has full column rank and V_r^T full row rank. Its leading H_s has determinant (det V_s)²∏c_ell≠0. The solved p is exactly the product over its s distinct nodes; every subsequent check passes. Prefix rank defects for arbitrary inputs cannot create false acceptance because roots and the entire recurrence are verified.

Per candidate the cost is therefore O(N(r+1)^{κ−1}+r³) additions/multiplications and O(r) inversions. Candidates are processed sequentially.

## 6. Combining the ledger, including accepted outputs

The total recognition ledger is

O(r²(D+1)^κ + N(D+1) + C[N(r+1)^{κ−1}+r³] + N).

With D=O(r³), C≤D and r≥1, this is

O(Nr^{2+κ}+r^{2+3κ}).

The r^6 candidate setup term is dominated by r^{2+3κ}, and Nr³ phase scanning is dominated by Nr^{2+κ}. Toeplitz construction uses one scalar inverse; candidate elimination and Vandermonde solves use O(Cr)=O(r^4) further inversions. Storage is O(N+r(D+1)+r²)=O(N+r^4).

For an accepted phase, the established exact all-length quadratic Gauss-row evaluator constructs G_a(k)=Σ_jω^{aj²+kj} in O(N) field operations plus integer gcd/modular-inverse work. All outputs are Σ_ell c_ellG_a(k+b_ell), at O(Nr). This fits the bound. Its parity and nonunit-phase cases remain essential; a prime-length completion-of-squares formula alone would not justify the stated all-length theorem.

The growing-r corollary follows because r^{2+κ}=o(log N), while r^{2+3κ} is polylogarithmic. If p=N^{O(1)} and scalar inversion costs O(log N) word operations, the additional O(r^4 log N) remains o(N log N) in that schedule. This conditional observation is not a complete bit-complexity theorem.

## 7. Controls and limits

New independent controls in fresh_controls.py compare blocked values and all recurrence residuals with direct sums in 285 cases, including odd/even grids, non-power-of-two block lengths and final partial blocks. Exhaustive r=1 recognition checks cover all 343 vectors of F_7^3 and all 625 vectors of F_5^4; 120 structured cases at r≤4 cover six larger grids, with 120 arbitrary per-phase candidates also reconstructed on acceptance. All passed.

The control recognizer deliberately uses a direct low-r determinant expansion to isolate the newly changed recognition/verification steps. It is not a production implementation of the Toeplitz eliminant, and the tests are not a benchmark or proof of asymptotic speed. The uniform theorem combines the existing audited Toeplitz proof with the new block-convolution proofs above.
