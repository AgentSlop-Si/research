# Radial and branch-preserving basis normalization: exact physical obstruction

17 October 2026. Candidate completion for a sharply defined FUS-06 / Q20 / NF-03 continuation. This packet does not claim historical novelty, a production executor, or completion of the wider RS program.

## 1. Exact question, inherited model, and scope

The accepted compact family has N=2h≥4, q=exp(2πi/N), c_j=q^{j(j−1)/2},

R_n(z)=∏_{k=0}^{n−1}(z−q^k)=Σ_j r_(n,j)z^j,
P_n(z)=Σ_j(c_n/c_j)r_(n,j)z^j,
B_t(z)=zP_h(z)+tP_(h−1)(z), m=h+1.

Choose any legal compact parameter: |t|≤1 and B_t has distinct nonzero roots α_l, none satisfying α_l^N=−1. In particular the accepted least legal member of {1/(2N),…,1} qualifies. Let β_l match the first m moments, hence all N required moments by the accepted recurrence, and set γ_l=β_l(1+α_l^N). Retain possible zero residues.

Fix the signed cyclic shift T e_j=e_(j+1) for j<N−1 and T e_(N−1)=−e_0. Thus T is unitary and T^N=−I. The exact accepted scalar common-shift bank is

C=Σ_{j=0}^{N−1}c_jT^j=Σ_{l=1}^m C_l,
C_l=γ_l(I−α_lT)^(−1), H=C/√N.

The source's normalized negative-sign Fourier map is obtained from H by unit-modulus diagonal endpoint phases, so physical Euclidean norms and forward/inverse errors are unchanged by those endpoints. The following results work directly with H and explicitly charge any additional nonunitary transformations.

The candidate under test is:

> Preserve these poles and individual first-order branches, but normalize poles radially and/or apply an invertible coordinate basis to make the displayed solves better conditioned or contractive. Infer improved physical forward and inverse robustness from that normalization alone.

This packet proves an exact negative result for that candidate, including arbitrary branch-preserving invertible similarities under the specified relative-branch-error model, and a quantitative exponential obstruction for the concrete geometric diagonal state normalization. It does not exclude a new pencil, a genuinely recombined/fused branch algorithm, correlated error cancellation, structured preparation with a better error bound, or a general polynomial basis that changes the branch architecture.

The original gate asks for a scoped conditioning estimate/counterexample with coefficient field, resonance, preparation, precision, and all-output costs explicit. The already accepted unscaled-V obstruction is not re-proved here. Its sole quantitative input is the retained root-radius implication

ρ=max_l |α_l| ≥ √(9/8), for even N≥44 and |t|≤1.                 (A)

All new claims below first hold for any legal exact bank. Only the final uniform exponential corollary invokes (A).

## 2. The physical bank is a flat unitary

Every entry of C is one signed chirp coefficient, so |H_(a,b)|=1/√N. The chirp extends antiperiodically: c_(j+N)=−c_j, because N is even. Consequently signed cyclic autocorrelation at lag k is, up to a unit-modulus constant, Σ_(j=0)^(N−1)q^(kj), which is N for k=0 and zero for 1≤k<N. Therefore

HH*=H*H=I, and |H_(a,b)|=|H*_(a,b)|=1/√N.                   (1)

Equivalently T has simple eigenvalues τ_k=exp((2k+1)πi/N), and every eigenvalue λ_k of H has modulus one. This proves the target and inverse are perfectly conditioned in their original physical Euclidean coordinates. A poor internal matrix is not a lower bound on this target condition number.

## 3. Exact forward and inverse branch-error invariant

For each spectral point τ define the normalized branch response

b_l(τ)=γ_l/[√N(1−α_lτ)],
χ=max_(τ^N=−1) Σ_l |b_l(τ)|.                               (2)

Legality makes all denominators nonzero; zero-residue terms simply contribute zero. Since Σ_l b_l(τ)=λ(τ) and |λ(τ)|=1, χ≥1.

The error model is explicit: each prepared branch coefficient acquires an arbitrary independent complex relative perturbation δ_l with |δ_l|≤u, while poles and branch solves are otherwise exact. Define

H_δ=Σ_l (1+δ_l) C_l/√N.

These perturbations can model independent coefficient errors or a uniform relative multiplicative error applied to each branch result. They do not claim to describe every rounding algorithm or every preparation error.

**Theorem 1 (exact physical forward and inverse sensitivities).**

sup_(|δ_l|≤u) ||H_δ−H||₂ = uχ.                             (3)

If uχ<1, every H_δ is invertible and

sup_(|δ_l|≤u) ||H_δ^(−1)−H^(−1)||₂ = uχ/(1−uχ).            (4)

Since H and H^−1 are unitary, these are also worst-case relative forward and inverse action errors over nonzero physical inputs.

**Proof.** The commuting normal branches diagonalize in the same orthonormal eigenbasis of T. Thus the norm in (3) is max_τ |Σ_l δ_l b_l(τ)|, at most uχ. At a maximizing τ*, choose the phases of δ_l so all nonzero δ_l b_l(τ*) align. This attains uχ. For (4), write e(τ)=Σ_l δ_l b_l(τ). Then |e(τ)|≤uχ<1, and the scalar inverse difference is |e(τ)|/|λ(τ)+e(τ)|≤uχ/(1−uχ). Choose δ_l phases at τ* so e(τ*)=−uχ λ(τ*); this attains equality. ∎

**Corollary 1 (basis/scaling invariant, with physical decoding).** Let S be any invertible matrix, including any diagonal state scaling, and store branches S^−1 C_l S. Use exact input S^−1x and output decoding S. Applying the same relative branch errors gives

S[Σ_l (1+δ_l)S^−1 C_l S/√N]S^−1=H_δ.                     (5)

Hence both exact sensitivities (3)–(4) are unchanged. Splitting a branch coefficient into compensated nonzero scalar factors has the same invariance for a relative perturbation of the resulting branch coefficient. A smaller Euclidean condition number of an intermediate matrix cannot by itself lower χ or either physical sensitivity.

This is an invariant of the fixed actual bank and its fixed branch-error model, not the old worst-case right-side condition number of a Vandermonde preparation solve. It does not prove χ grows exponentially for all compact parameters. The numerical χ values below are diagnostics only.

## 4. Scalar radial normalization leaves the entire branch unchanged

Choose r>0 and a_l=α_l/r. To preserve the polynomial bank, simultaneously use T_r=rT and d_j=c_j/r^j. Then

d_j T_r^j=c_jT^j,
I−a_lT_r=I−α_lT,
T_r^N=−r^N I,
1+a_l^N r^N=1+α_l^N.                                     (6)

Thus poles, resonance margins in the physical resolvent, inverse norms, χ, forward errors, and inverse errors are exactly unchanged. Using 1+a_l^N in the numerator or imposing T_r^N=−I would be a different, generally incorrect bank. Even if |a_l|≤1, the Neumann ratio obeys ||a_lT_r||₂=|α_l|, not |a_l|.

The same conclusion holds after any invertible similarity: the spectral radius of α_l S^−1TS is |α_l|. No induced operator norm can be smaller than that spectral radius. Whenever ρ>1, a radial normalization combined with any exact similarity cannot make all original first-order inverse branches Neumann contractions. Reciprocal/reversed branches or actual branch recombination are different candidates and are not excluded here.

## 5. Geometric diagonal normalization pays an exponential wrap and decode cost

The standard geometric state choice is

D_r=diag(1,r,…,r^(N−1)), r≥1,
S_r=D_r^−1 T D_r.

It gives N−1 ordinary links 1/r, but its signed wrap is −r^(N−1):

S_r e_j=r^−1 e_(j+1) for j<N−1,
S_r e_(N−1)=−r^(N−1)e_0,
S_r^N=−I.                                                 (7)

So the ordinary links of α_lS_r appear normalized to α_l/r, while the wrap becomes −α_l r^(N−1). Omitting that wrap changes the problem. More generally, diagonal similarity preserves the product of cyclic link weights, and the spectral radius argument above rules out uniform contraction.

The problem is measurable at the complete transformed target and inverse, not merely in this one wrap entry.

**Theorem 2 (flat-unitary diagonal range bound).** For any invertible diagonal D, set κ_D=max_j|D_jj|/min_j|D_jj|. Then

||D^−1 H D||₂ ≥ κ_D/√N,
||(D^−1 H D)^−1||₂ ≥ κ_D/√N,
κ₂(D^−1 H D) ≥ κ_D²/N.                                   (8)

**Proof.** Choose i with minimal |D_ii| and j with maximal |D_jj|. The (i,j) entry of D^−1HD has modulus κ_D/√N by (1), and operator norm dominates each entry. Its inverse is D^−1H*D, whose corresponding entry has the same modulus. Multiply. ∎

For D_r, κ_D=r^(N−1), so

κ₂(D_r^−1 H D_r) ≥ r^[2(N−1)]/N.                           (9)

If r≥ρ is chosen to put every pole inside the unit disk, (A) gives, uniformly for every legal compact parameter and even N≥44,

κ₂(D_r^−1 H D_r) ≥ (9/8)^(N−1)/N.                         (10)

This lower bound can be below one near its threshold; its asymptotic exponential meaning is the claim. Include max{1,right side} if a finite numerical condition lower bound is required. The proof applies to all diagonal phase choices with the same magnitudes.

**Exact decoding-error cost, in both directions.** Suppose the scaled forward computation guarantees only an unstructured relative output error

||δz||₂≤u||D^−1Hx||₂.

After decoding, its worst-case physical relative error over x≠0 and allowed δz is exactly uκ_D. The upper bound is the usual ratio of largest to smallest diagonal magnitudes. To attain it, choose Hx=e_i at a coordinate of minimal |D_ii|, and δz of norm u/|D_ii| along a coordinate e_j of maximal |D_jj|. Unitarity supplies such an input x=H*e_i with ||x||=1. For the inverse operation choose x=He_i and repeat with H*; the same factor is attained. Thus

sup physical relative forward error = uκ_D,
sup physical relative inverse error = uκ_D.                (11)

This statement is about all errors allowed by the advertised scaled-output norm contract. It does not assert an unavoidable actual rounding error for every algorithm. Componentwise/structured error guarantees, weighted norms, or certified corrections may avoid the worst case, but must be proved and charged; their benefit cannot be inferred from normalization alone. If physical norms are transported exactly to scaled coordinates, the target condition stays one and the sensitivity χ stays (2), with no claimed gain.

## 6. Fully explicit legal family and cost/range ledger

Take the accepted least legal compact-grid parameter at every even N and choose r=8. The accepted all-embedding root bound |α_l|≤6 gives |a_l|≤3/4. This is a concrete radial/state-normalization family, not a new legal-node theorem.

Its apparently favorable pole disk does not imply contraction: (6) preserves every physical branch. Under geometric state coordinates,

κ_D=8^(N−1)=2^[3(N−1)],
κ₂(D^−1HD)≥64^(N−1)/N,
and the worst-case decoding amplification in either direction is exactly 8^(N−1).

The preparation and execution ledger is therefore:

- Legal parameter, nodes, residues and all resonance guards remain exactly those of the accepted bank. The inherited general certified preparation costs 2^[O(p+N³)] bit operations; radial normalization proves no improvement to it. The current packet does not execute that exhaustive preparation.
- Forming all normalized nodes and a scale sequence costs O(N) scalar operations/storage once the bank exists. A geometric state application uses N input scalings and N output scalings in addition to the underlying evaluator. Any explicit transformed matrix uses N² entries; no uncharged dense basis construction is used here.
- r=8 scalings are exact binary exponent adjustments when the format has enough exponent range. Exactness of those adjustments does not eliminate the dynamic range 2^[3(N−1)] or the sensitivity in (11). The largest and smallest scale magnitudes must be supported, including subnormal/overflow behavior in a real implementation.
- Under the unstructured scaled-output relative-error contract, guaranteeing physical relative error ≤2^−p requires scaled relative error ≤2^[−p−3(N−1)] for both forward and inverse. Equivalently the contract must pay 3(N−1) additional accuracy bits. This is a requirement on that error contract, not a universal floating-point bit-complexity lower bound.
- At inverse branch-coefficient level, the exact forward requirement is uχ≤ε, and the exact inverse requirement is uχ≤ε/(1+ε). Scaling does not change χ. Node errors, solve residuals, endpoints, and summation rounding require their own budgets; this packet does not silently absorb them into u.
- For moment preparation, a row/basis transformation W and column transformation E give WVEx=Wc and physical β=Ex. Exact propagation of a physical right-side perturbation is E(WVE)^−1W δc=V^−1δc. Smaller displayed κ(WVE) alone is not a new physical error proof. No worst-case perturbation assertion is made about the one fixed chirp right side.
- The accepted simultaneous evaluator, including all branches and all N outputs, remains O(N^log₂3) rational operations with its separate finite-bit ledger. No runtime improvement or production benchmark follows from the O(N) scaling overhead, and no use of a pre-existing FFT is hidden in the candidate.

## 7. Fresh controls and what they establish

`fresh_controls.py` was newly written for this packet and executes no inherited research program.

1. Direct signed-circulant autocorrelation is verified exactly in Z[q]/Φ_N(q), for every even N=4,…,128 and every lag. Replacing the negative wrap by a positive wrap is a failing control.
2. Exact rational matrices verify T^N=−I, the geometric wrap, radial-generator equality, similarity of each resolvent, and invariance of multiplicative branch errors at N∈{4,6,8,10}, r∈{3/2,2,8}, and α∈{1/3,3/2,2}. Forgetting the rescaled generator or geometric wrap is rejected.
3. Exact rational dyadic range controls check the r=8 accuracy and condition-bound exponents through N=128.
4. Fresh 90-digit RS numerical banks use the recurrence-derived tridiagonal matrix, solve the moment system, check all N chirp moments and flat spectral magnitudes, and construct extremizing perturbations for both (3) and (4). They also test radial invariance and the dense transformed-target bound (8). Parameters t=1/(2N) and t=1 are tested at explicitly recorded finite even N only. Numerical separation and resonance values are reported but are not legal-node certificates or evidence that either parameter is always legal.

The exact counts, actual completed numerical cases, errors, timings, and limitations are in `RESULTS.json`. No finite test replaces the all-N proofs. In particular observed χ growth is not promoted into a uniform asymptotic theorem.

## 8. Resolution and remaining boundary

**Resolved:** the specified branch-preserving radial/basis normalization cannot improve the exact physical relative-branch forward or inverse sensitivity; its apparent unit-disk Neumann argument is invalid. The concrete geometric diagonal state normalization incurs the proved exponential transformed-target condition and decoding-error cost, uniformly for the compact family at the stated lengths. This is a sharply scoped negative completion beyond the accepted unscaled moment-Vandermonde result.

**Not resolved:** arbitrary new polynomial bases/pencils; improved structured preparation; a bound on χ uniform in all compact parameters; a fused/recombined stable bank implementation; useful polynomial certified preparation; FFT-competitive production execution; h-pole optimality; universal t choices; Q08's separate obligations; historical priority. The parent owner must remain open. A materially different candidate needs a new explicitly stated physical error and cost contract.
