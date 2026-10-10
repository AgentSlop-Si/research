# Independent comparison: the supplied uniform three-stage bit-reversal cut

Date: 2026-10-09 UTC.

## Accepted result and attribution

The newly supplied `fft_three_stage_bitrev_no_go_2026-10-10.zip`, Library `[private-id]`, version 1, contains a correct uniform scalar-network cut excluding three quasiseparable-order-one stages separated twice by bit reversal at every dyadic length `N>=64`. The uniform `12m+1` cut and threshold 64 are credited to this source. They strengthen the earlier independently derived explicit threshold 128; they do not replace the broader arbitrary-permutation three-stage discrepancy theorem.

The original archive has 658,342 bytes and SHA-256 `9d3e4fce68dfe0e8ae89fcd8bcc7408325586f97472dd3497d554315542b5bea`. A source copy and provenance are included as inert data. No uploaded code was executed or imported.

## Cut and proof

Let `N=32m` be a power of two. Inputs are `C=[0,13m)` and outputs are `R=[19m,32m)`, each of width `13m`. Number stages from zero. A lower state at index `i` receives inputs before `i`; an upper state at `i` receives inputs after `i`.

Remove the following scalar nodes:

1. Stage 0: lower state `13m`.
2. Stage 1: input nodes `32z+24`, `32z+26`, and `32z+28` for `0<=z<m`.
3. Stage 1: lower state `32z+21` for `0<=z<m`.
4. Stage 1: upper state `32z+31` for `0<=z<m-1`.
5. Stage 2: all input nodes in the seven length-`m` blocks with labels `20,22,24,25,26,28,30`.
6. Stage 2: lower state `19m`.

The total is `1+3m+m+(m-1)+7m+1=12m+1` nodes.

The first cut confines stage-0 influence to `[0,13m)`. Write an index as `am+b`, with `0<=a<32` and `0<=b<m`. Bit reversal obeys

\[
\operatorname{rev}_N(am+b)=32\operatorname{rev}_m(b)+\operatorname{rev}_{32}(a).
\]

Thus stage-1 inputs initially occupy the residues

`0,2,4,6,8,10,12,16,18,20,24,26,28`

in each 32-position block. Input-node cuts delete residues 24, 26 and 28. The lower-state cut at residue 21 prevents forward propagation past residue 20. The upper-state cuts at residue 31 block propagation backward from the following block. Consequently stage-1 outputs are supported only at residues `0,...,20` in each block.

The second reversal sends these to length-`m` blocks with labels

`0,1,2,4,5,6,8,9,10,12,14,16,17,18,20,22,24,25,26,28,30`.

The seven labels at least 19 are exactly those removed at stage 2. All remaining stage-2 inputs lie below `19m`; its lower-state cut at `19m` prevents their influence reaching `R`. This proves disconnection for all dyadic `m`, rather than merely the tested sizes.

## Why the graph covers full QS1

This graph is the complete scalar-transition representation of a quasiseparable-order-one matrix, not just the transition-free separated-generator chart. A lower-triangular part is represented by a one-dimensional state recurrence, with arbitrary scalar transitions; the upper part has the reverse recurrence, plus a diagonal input-to-output edge. Zero transitions and zero cut ranks are permitted. The representation follows by choosing generators for each nested off-diagonal cut row space; restriction to the previous cut is a scalar multiple, including the zero case. A zero cut separates the state and needs no division. The independently reviewed full proof is in the earlier `review_four_stage/NETWORK_REVIEW.md` milestone.

Every source-to-target path crosses one of the removed scalar nodes. The corresponding transfer block factors through at most `12m+1` scalar values, so its rank is at most `12m+1`, for any stage coefficients.

The Fourier block `F_N[R,C]` has rank `13m`: factoring a nonzero column power leaves a square Vandermonde matrix on distinct roots. For `m>=2`, `12m+1<13m`. At `m=1` the capacities are equal, so this certificate does not exclude `N=32`.

## Exact independent controls

The newly authored `check_uniform_cut.py` constructs the cut from the formulas, independently propagates Boolean lower and upper states, and reconstructs an adjacency-list graph for a separate breadth-first check at lengths 32, 64 and 128. It verifies disconnection, cut cardinality, every intermediate support description, and the no-cut control for all dyadic lengths 32 through 8192.

It also verifies Fourier full-rank controls over `F_65537` using distinct-root Vandermonde products:

- `N=64`, root 8224, rows `[38,64)`, columns `[0,26)`: determinant 33858.
- `N=128`, root 13987, rows `[76,128)`, columns `[0,52)`: determinant 64219.

These nonzero determinants are exact checks, not floating-point ranks. The uniform proof is the reason the theorem covers all larger dyadic lengths.

## Scope and comparison

The cut concerns exactly three full QS1 stages with the two specified internal bit-reversal permutations. Natural Fourier endpoints are covered. More generally, either one endpoint can be affine-coprime while the other is any permutation, because the selected contiguous rows or columns still give a Vandermonde block; nonsingular diagonal endpoint scales do not alter ranks. Both endpoint permutations arbitrary at composite lengths are not asserted.

The source's four-stage finite capacity survival is insufficient to establish a factorization. The independently verified four-stage repeated-bit-reversal cut at `N=2048` already provides a contrary fixed-size obstruction to extending such survival. That fact does not impair this source's three-stage proof.

The source's nested `prior_checkpoint_full.zip` has SHA-256 `a3d6acc7bff7ba31a17c4ecf44c16d4409d58b0f9baf3b6f02513e6da4bf8d9d`, matching the previously reviewed multistage archive. It is retained as provenance inside the original archive; it was not executed. The present independent verdict concerns the uniform cut, rank implication and stated comparison, rather than treating every experimental remark in the source as a theorem.
