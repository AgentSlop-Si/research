# Structural limits for short Fourier factorizations

Exact cut-rank arguments restrict several proposed short Fourier factorizations. Three quasiseparable stages require total stage order growing at least proportionally to log N under the endpoint conditions below. A separate paired-cycle theorem forces Ω(sqrt N) layers for the fixed natural and bit-reversed cycle geometry, even with arbitrary same-block Fourier banks. An explicit Fourier minor also rules out scalar-only copying through a specified four-fiber grid fold, even after scalar normalization. These are scoped representation obstructions, not lower bounds for all Fourier algorithms. Publication novelty has not been established.

## The statement

Let F_N[i,j] = ω^(ij), where ω has order N in a field. Suppose F_N = S₃ P₂ S₂ P₁ S₁. Each Sᵢ has both strict off-diagonal cut ranks at most rᵢ in its natural stage coordinates; P₁ and P₂ are arbitrary permutations.

Define D(π) = max over W,t of |#{i < W : π(i) < t} − Wt/N|. Then

D(P₂⁻¹) ≤ 2r₁ + r₂ + r₃,

D(P₁) ≤ r₁ + r₂ + 2r₃.

The classical planar discrepancy theorem implies r₁ + r₂ + r₃ = Ω(log N). The orders therefore cannot all remain constant as N grows.

## Why the bound holds

1. Fix an output prefix I of width W and let J range over all cyclic input intervals of width W. Restricting the two outer stages loses at most r₃ + 2r₁ rank, including wrapped intervals.

2. Set R = P₂⁻¹(I), C = P₁(J). At a middle cut t, put a = |R ∩ [0,t)| and b = |C ∩ [0,t)|. Deleting W − |a − b| rows and columns leaves a strict off-diagonal block. Thus rank S₂[R,C] ≤ r₂ + W − |a − b|.

3. The Fourier prefix on any W distinct columns is a nonsingular Vandermonde matrix. Its rank W forces |a − b| ≤ 2r₁ + r₂ + r₃.

4. Every input coordinate belongs to exactly W of the N cyclic windows. Consequently the average of b is exactly Wt/N. Averaging gives the first discrepancy inequality; transposition gives the second.

5. The point set {(i/N, π(i)/N)} has continuous unnormalized star discrepancy at most D(π) + 2. Schmidt’s lower bound is c log N, proving the conclusion.

Averaging only nonwrapping windows would not justify step 4.

## Explicit bit reversal certificate

For N = 128, use output indices 0 through 42 and input indices 85 through 127. Under seven-bit reversal and middle cut 43, delete 27 mapped rows and 12 mapped columns. The remaining block crosses one cut.

Three order-one stages therefore give rank at most 1 + 1 + 1 + 27 + 12 = 42. The 43 by 43 Fourier block has rank 43, a contradiction.

More generally, repeated bit reversal at N = 2^m requires r₁ + r₂ + r₃ ≥ ceil(m/2). The previously tested widths 6 and 8 missed this larger-window witness.

## Sharper fixed layout boundary and finite positive control

A subsequently supplied uniform cut improves the repeated-bit-reversal order-one exclusion to every dyadic N ≥ 64. Write N = 32m. The first 13m inputs and last 13m outputs are separated by 12m + 1 scalar wires, whereas their Fourier block has Vandermonde rank 13m. The source supplies this uniform cut; independent graph reconstruction verifies it. At N = 32 the counts are equal, so this witness gives no contradiction.

At N = 8, an exact rational contraction certificate proves that three separated-generator stages with repeated bit reversal do represent the normalized Fourier matrix. The coefficients are defined as a unique local polynomial-system root. This is finite-size existence, not a uniform coefficient compiler or an asymptotic speedup.

## Four stages with a low crossing middle permutation

Write F_N = S₄ P₃ S₃ Q S₂ P₁ S₁. For each prefix [0,t), count the adjacent membership changes along Q⁻¹([0,t)); let κ(Q) be their maximum. A quasiseparable matrix S of order r then satisfies qs(Q S Q⁻¹) ≤ κ(Q)r.

To prove this, split the prefix preimage into natural intervals. Its off-diagonal interaction with the complement has rank at most r per exposed interval boundary. Summing those boundary contributions gives the crossing count. The reverse block follows by transposition. No nonzero-generator or invertibility assumption is needed.

Set T = S₃(Q S₂ Q⁻¹). Product cut ranks are subadditive, so qs(T) ≤ r₃ + κ(Q)r₂. The four-stage word becomes exactly S₄ P₃ T (Q P₁) S₁. The three-stage theorem therefore gives

D(P₃⁻¹) ≤ 2r₁ + r₃ + κ(Q)r₂ + r₄.

Thus bounded stage orders require κ(Q) = Ω(log N), unless the middle stage has zero off-diagonal rank, in which case the collapse is immediate. A growing crossing count is only necessary; it does not supply Fourier-compatible coefficients.

For Q(j) = 3j mod N at dyadic lengths, every prefix preimage has at most three intervals and contains index zero. Hence κ(Q) ≤ 5. Four order-one stages have discrepancy budget 9, even with arbitrary other internal permutations. More generally, a fixed positive coprime multiplier a gives κ(Q) ≤ 2a − 1.

For the specific outer bit-reversal layout, an explicit rectangle at N = 2^m has discrepancy m/3 + 1/9 − (−1)^m/(9N). It exceeds 9 for every m ≥ 27. Therefore the four-stage bit reversal–multiply by three–bit reversal word fails for every N ≥ 2^27. This is a uniform witness, not an optimal cutoff or a claim of globally maximal discrepancy.

## A growing depth bound for paired cycle layers

A separate cut argument closes the natural-cycle plus bit-reversed-cycle construction even when each stage is a sum of two independently weighted Green inverses. Let N = 2^k, m = 2^floor(k/2), and q = N/m. Partition the coordinates into consecutive blocks of length m. Each of L layers uses the two cycle orders Z and RZR, with arbitrary edge weights and nonsingular diagonal endpoints; R is bit reversal and Z is the natural cycle. More generally, endpoints may permute within each block. Every defining cycle inverse must exist, but edge weights may be zero.

Allow arbitrary additional matrices that are block diagonal on these same blocks, including a partially or fully active bank of length-m Fourier transforms. Any exact Fourier factorization in this class must satisfy

L(q/2 + m) ≥ N/2, or L ≥ ceil(N/(q + 2m)).

Three layers therefore fail at every dyadic N ≥ 128, and four fail at every dyadic N ≥ 256. In general, the number of layers must grow as Ω(sqrt N). This is a representation and layer-count bound; it is not a lower bound on every optimized arithmetic circuit.

### Proof of the paired cycle bound

Let I contain the even-numbered blocks and let Iᶜ contain the odd-numbered blocks. The Fourier rectangle F[I,Iᶜ] has rank N/2. To see this, put t = q/2 and write its row and column indices as i = 2ma + b and j = 2mc + m + d. Since t divides m, ω^(ij) = ζ^(ad + bc) ω^(b(m + d)), with ζ = ω^(2m). Fourier changes of basis in a and c leave square blocks of size ℓ = m/t, each diagonally equivalent to [η^(uv)] for η = ω^(t²). The order of η is 2ℓ, so those blocks are invertible Vandermonde matrices.

For A = I − D_w P, the complementary off-diagonal ranks of A and A⁻¹ are equal. The natural cycle has q/2 edges entering I; the bit-reversed cycle has m. Each paired layer thus contributes at most q/2 + m cross rank. Cross ranks are subadditive under sums and products, and inserted block-diagonal banks contribute zero. Comparing with Fourier rank N/2 proves the bound, including zero weights and cancellations.

At N = 128, m = 8 and q = 16: three layers have rank budget 48 against the target rank 64. Four layers have budget 64, so this witness does not exclude that boundary case. At N = 256, four layers have budget 96 against target rank 128.

Arbitrary cycle orders and endpoint permutations mixing the two striped classes lie outside this theorem. The current root-free weighted natural/bit-reversal three-stage family is inside it, regardless of the tensor ranks of its diagonal masks. Positive compressed-path identities in that family remain identities, but cannot yield a full all-length three-stage FFT.

The full proofs, independent exact checks and source history are preserved in [the reviewed checkpoint](library-file:[private-id]). Publication priority is unverified.

## Scalar normalization cannot repair this grid fold

Let b = 2^r, a = b or 2b, and N = ab. Label the small grid by t = bx + y and the large grid by j = 2bX + Y. Let Q sum the four coordinates projecting under (X,Y) ↦ (X mod a,Y mod b). Use a primitive 4N-th root ω and the compatible small root ω⁴, over a field whose characteristic does not divide 4N.

For every scalar γ, the N by 4N matrix QF₄N − γF_NQ has row rank N. This includes γ = 2, where the earlier complex norm-gap argument would give no information.

### An explicit minor proves the claim

For each t = bx + y, choose the large column j(t) = 2bx + y when y > 0, and j(t) = 2bx + b when y = 0. These columns project bijectively onto the small coordinates, so (F_NQ)[:,J] = F_N. Put K = F_N⁻¹(QF₄N)[:,J].

The four-fiber sum vanishes on odd j. For even j, the small x-coordinate Fourier sum forces K[s,t] = 0 unless s ≡ j(t)/2 modulo a. Define ν(t) as the binary valuation of t mod b, capped at r when that remainder is zero. Every nonzero K[s,t] lowers ν by one; columns with ν(t) = 0 vanish. Hence K^(r+1) = 0.

Consequently det((QF₄N − γF_NQ)[:,J]) = det(F_N)(−γ)^N, which is nonzero whenever γ ≠ 0. At γ = 0, full row rank follows because Q has row rank N and F₄N is invertible. The proof also covers b = 1 and either consistent Fourier sign.

### Consequence for copying layer coefficients

Consider the fixed product C = H₃H₂BH₁. At the small level, B applies unnormalized F_b on active blocks J and identity elsewhere; at the large level it applies F₂b on the pulled-back active set J ∪ (J+a). This bank has rank(QB_large − B_smallQ) = b|J|.

If every layer obeys QH_l,large = γ_l H_l,smallQ with nonzero scalars, telescoping confines the whole product discrepancy to rank b|J|. Fourier targets at both levels require rank N, even when the targets have independent nonzero scalar normalizations. A proper active bank therefore cannot succeed by scalar-only layer copying.

More generally, define D_l = QH_l,large − γ_lH_l,smallQ. Exact Fourier identities require rank(D₁) + rank(D₂) + rank(D₃) ≥ N − b|J|. Each factor occurrence is charged separately. This is a necessary compatibility condition, not an operation lower bound: one nonconstant character on the four-point fibers already supplies full defect rank with linear-time mask generation and application.

The conclusion depends on this precise grid, compatible roots, bank placement and bank discrepancy. Genuine four-channel coefficient mixing and other layouts remain open. The complete proof, normalization conditions and independent exact checks are in [the reviewed folding and feedback checkpoint](library-file:[private-id]).

## Scope and next construction target

The argument includes zero generators, singular intermediate parameter choices and the complete quasiseparable class. It permits either endpoint to be affine with coprime stride while the other is arbitrarily permuted. Invertible endpoint diagonal scalings preserve the result.

At complex prime lengths, Chebotarev’s full-spark theorem also permits two arbitrary endpoint permutations. At composite lengths this extension is not established here. The results do not exclude general four-stage layouts, five or more stages, or cheaply applicable matrices with large quasiseparable order. Growing rank alone is not an unrestricted arithmetic-operation lower bound. See [Tao’s primary proof of the prime full-spark theorem](https://arxiv.org/abs/math/0308286).

The next constructive directions need sufficient routing across every relevant cut and exact global Fourier compatibility. The paired-cycle theorem specifically requires changing the natural/bit-reversed geometry or allowing endpoint routing that mixes its striped classes. Larger cut rank, surviving finite tests and finite-size existence alone do not establish a growing-length algorithm; coefficient preparation and full application must also remain cheap.

## Evidence and attribution

The proof was derived in the current research round and independently checked. Separate exact controls include wrapped-window localization, cyclic averaging, Fourier minor ranks and degenerate stage cases. The general proof, rather than those finite tests, establishes the all-size conclusion.

The imported discrepancy theorem is classical: W. M. Schmidt, Irregularities of distribution VII, 1972. Its unnormalized formulation appears as equation 1.2 on page 2 of [Bilyk, Lacey, Parissis and Vagharshakyan](https://arxiv.org/abs/0810.5544). The connection above is a deduction using that theorem; it is not a new proof of planar discrepancy.

Status: mathematically reviewed, architecture-specific, publication priority unverified. Updated 10 October 2026 UTC.

