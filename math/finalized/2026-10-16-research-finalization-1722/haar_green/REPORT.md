# ALG-048: uniform covariance obstruction for one small-strength Haar–Green stage

16 October 2026. Repository baseline: `AgentSlop-Si/research` at `0339a31eb6109f0b96074ab8321f8653641e7530`.

## Result and exact disposition

For every `N=2^n >= 8`, the original Phase 13 Haar–Green stage, or its inverse, has a uniformly large Fourier covariance defect, even after arbitrary unitary monomial matrices are placed at both endpoints and both paths are relabeled arbitrarily. At least `3N/4` singular values of that defect exceed

`gamma = sqrt(2-sqrt(2)) - 129/256 = 0.26146... > 1/4`.

Consequently every additive correction that makes its Fourier covariance exact has rank at least `3N/8`. This is an all-size theorem for the original fixed one-stage architecture, not an extrapolation of the old modular samples. The stronger historical full-rank defects at five specific lengths remain historical evidence and are not superseded by this weaker-rank, wider-domain theorem.

**Complete this bounded one-stage, small-strength, low-rank-additive-repair gate. Keep ALG-048 `TO RESEARCH`, priority 42.** Its selected general Haar/Green hierarchy remains open. No owner is archived; the open/closed census does not change. The Ailon comparison and absolute-value guard were already completed and corrected, respectively; they receive no new credit here.

The argument is an elementary weighted-cycle computation plus standard singular-value perturbation. It is not a historical novelty claim, an exact Fourier construction, a runtime lower bound, or an all-parameter obstruction.

## 1. Sources and the genuinely remaining obligation

The [immutable Phase 13 source](https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/c0/c0f726bac9b539db9eb642a223584e7cbc5345597dd76cba0d498b25357465d3__012_c0f726bac9b539db.md) defines the Haar replacement in section 3. Section 4 proves the elementary repair inequality `rank(E) >= rank(AZ-DA)/2` but supplies full-rank defects only for particular matrices at `N=8,16,32,64,128`. Section 6 selects a uniform explicitly parameterized Fourier-covariant hierarchy as the next construction gate. Section 7 rejects six particular two-stage pairings at those lengths and explicitly excludes arbitrary endpoint monomials and all-parameter conclusions.

The [completed bounded finalization](https://github.com/AgentSlop-Si/research/blob/e3368ff3a44ca7c4bcea7b9fb838ce92e77fa000/math/finalized/2026-10-16-research-finalization-1412/algebra/ALGEBRA_FINALIZATION_REPORT.md), section 3, leaves that hierarchy open. This pass does not repeat its fixed-p obstruction or its Ailon-model comparison.

The owner's other [low-rank/induced-1 source](https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/a2/a225972f7ad1fc75050588293f2b7a7c5b9670e208c7c1b6a63fcdc27a20420a__045_a225972f7ad1fc75.inert.txt) was also read in full. Its `7^t(B+1)^2 >= N` theorem concerns a different condition-bounded Green primitive with rank-one factors, using a sparse-kernel/flatness argument. The Haar modification is full rank and escapes the old fixed-p budget. That sibling theorem is preserved, not re-proved or renamed as this result.

The present result closes the concrete all-N additive-patch question for the original one-stage Haar replacement. It rejects any sublinear-rank additive correction uniformly, with arbitrary unitary monomial endpoints. It does not supply or rule out the unspecified multistage hierarchy of section 6.

## 2. Precise theorem

Work over the complex numbers. Let `N=2^n`, `n>=3`, and `m=N/2`. Set `omega=exp(2*pi*i/N)`, `Z e_j=e_(j+1 mod N)` and `D=diag(1,omega,...,omega^(N-1))`. Any other primitive N-th root gives the same theorem by the product calculation below.

Let `H` be the orthonormal Haar synthesis on `m` coordinates and put

`R_H = [[0,H],[H*,0]]`,

`V = (I+i*epsilon*R_H)/sqrt(1+epsilon^2)`, with `epsilon=1/512`,

`C_j = (I+i*A_j/32)(I-i*A_j/32)^(-1)`,

`S = V C_1 C_2`.

Here `A_1,A_2` are real symmetric adjacency matrices of arbitrarily labeled unweighted paths on N vertices. In fact the proof only uses their Hermitian property and spectral norms at most 2. Let `T` be either `S` or `S^(-1)`. For arbitrary unitary monomial matrices `L,R`, define `A=L T R` and `Ecal(A)=AZ-DA`.

Then

1. `sigma_(3N/4)(Ecal(A)) > gamma > 1/4`, with singular values sorted in decreasing order;
2. `rank(Ecal(A)) >= 3N/4`;
3. for every complex matrix `E`, if `(A+E)Z=D(A+E)`, then `rank(E) >= 3N/8`;
4. more robustly, if `rank(E)<3N/8`, then `||Ecal(A+E)||_2 > gamma`.

No invertibility, coefficient bound, or unitary property is required of the additive correction E. For a nonzero overall scalar `cA`, the rank conclusions remain identical and the singular-value/residual thresholds become `|c| gamma`.

## 3. Complete proof

### 3.1 The actual stage is uniformly close to the identity

For Hermitian `A_j` with `||A_j||_2<=2`, the spectral theorem gives unitarity of `C_j` and

`||C_j-I||_2 <= 2/sqrt(257) < 1/8`.

Indeed the Cayley eigenvalue at a real eigenvalue lambda has difference from 1 of magnitude `2|lambda|/32 / sqrt(1+lambda^2/32^2)`.

The Haar involution satisfies `R_H*=R_H` and `R_H^2=I`. Hence V is unitary, its eigenvalues are `exp(±i arctan(epsilon))`, and

`||V-I||_2 = 2 sin(arctan(epsilon)/2) < epsilon = 1/512`.

Telescoping the product, using unitary invariance of the spectral norm, yields

`||S-I||_2 <= ||V-I||_2 + ||C_1-I||_2 + ||C_2-I||_2 < 129/512`.

Because S is unitary, `||S^(-1)-I||_2=||S-I||_2`. Thus in both cases

`||T-I||_2 < rho`, where `rho=129/512`.

This estimate is independent of N and of both path permutations. It is a spectral-neighborhood estimate, not the fixed-p norm budget that the Haar replacement escapes.

### 3.2 Arbitrary endpoint monomials leave a universal baseline spectrum

Put `Z'=RZR*` and `D'=L*DL`. Multiplication of the covariance defect on the left by `L*` and on the right by `R*` preserves all singular values and gives

`L* Ecal(A) R* = T Z' - D' T`.

Because L is unitary monomial, D' is a permutation of D's diagonal. Because R is unitary monomial, Z' is a weighted permutation matrix whose underlying permutation is one N-cycle; its cycle-weight product is 1. To see the latter directly, write `R e_j = u_j e_(p(j))`, `|u_j|=1`: the cycle weights of `RZR*` are `u_(j+1)/u_j` and telescope.

Consequently `W=D'^* Z'` is a unitary weighted N-cycle with total weight

`product_k conjugate(D'_(kk)) = omega^(-N(N-1)/2) = -1`,

since N is even. Replacing omega by any primitive N-th root still gives −1, because its exponent relative to `exp(2*pi*i/N)` is odd.

A weighted N-cycle has characteristic polynomial `lambda^N` minus its total cycle weight. One direct proof chooses a cyclic basis starting at any coordinate and successively applies W; the final application returns the first vector multiplied by the cycle weight. Thus the eigenvalues of W are exactly

`exp(i*(2j+1)*pi/N)`, `j=0,...,N-1`.

Since W is unitary, the singular values of `Z'-D'=D'(W-I)` are precisely

`s_j=2 sin((2j+1)*pi/(2N))`, `j=0,...,N-1`.

The sines here are positive. This computation is unaffected by either endpoint permutation or any endpoint phase.

### 3.3 A linear number of robust singular values survives

Exactly `3N/4` of those singular values exceed `s0=2 sin(pi/8)=sqrt(2-sqrt(2))`. The relevant indices are

`j=N/8, N/8+1, ..., 7N/8-1`.

There is no threshold equality, since `(2j+1)` is odd and `N/4` is even for `N>=8`. Meanwhile

`(TZ'-D'T) - (Z'-D') = (T-I)Z' - D'(T-I)`

has norm strictly less than `2rho=129/256`.

For completeness, the needed singular-value perturbation step follows directly from the min-max principle. On the `3N/4`-dimensional subspace spanned by the right singular vectors of the baseline having singular values above s0, every nonzero x satisfies

`||(TZ'-D'T)x||_2 >= ||(Z'-D')x||_2 - ||perturbation||_2 ||x||_2 > (s0-2rho)||x||_2`.

Equivalently, its `3N/4`-th singular value exceeds gamma. There is a uniform strict margin because the subspace is finite dimensional and its smallest baseline singular value is strictly larger than s0. This proves claims 1 and 2.

An exact rational check shows `gamma>1/4`: this is equivalent to `sqrt(2-sqrt(2))>193/256`, which follows from `sqrt(2)<93823/65536`; the latter follows by squaring positive quantities because `93823^2>2*65536^2`.

### 3.4 Additive repair and approximate residual

The source's covariance map is linear and

`rank(EZ-DE) <= rank(EZ)+rank(DE) <= 2 rank(E)`.

If `Ecal(A+E)=0`, it follows that `rank(Ecal(A))<=2 rank(E)`, proving claim 3. This uses no first-column normalization: even the weaker covariance requirement already forces the stated rank.

For claim 4, let U be the `3N/4`-dimensional high-singular subspace for `Ecal(A)`. If `rank(E)<3N/8`, the map `EZ-DE` has rank below `dim(U)`, so its kernel intersects U nontrivially. On a unit vector in that intersection the repaired covariance equals the original covariance and has norm greater than gamma. Hence its operator norm exceeds gamma. The scaled variant follows by dividing the candidate and correction by c.

## 4. Comparison with established mathematics

The perturbation ingredient is the ordinary deterministic Weyl singular-value inequality, not a new matrix-perturbation result. [O'Rourke, Vu and Wang, Theorem 7](https://arxiv.org/pdf/1311.2657), page 3 of the inspected v7 text, explicitly states the spectral-norm bound on changes to ordered singular values. That paper presents the statement for real rectangular matrices; the complex case needed here is proved directly above using the singular-vector subspace and the triangle inequality. Its random improvements are not used.

The weighted-cycle characteristic polynomial and unitary singular-value computation are also elementary. This report makes an exact application to the source architecture and identifies the resulting all-N boundary. It does not claim that the combined application is historically unprecedented. The existing qualified Ailon comparison and the separate low-rank/condition-number source are unaffected.

## 5. Fresh controls and their limitations

`fresh_controls.py` was authored for this pass; it imports no historical project code. Its recorded run passed:

- exact integer threshold/dimension checks at all 18 dyadic lengths from 8 through 1,048,576;
- 70 exact weighted-cycle exponent/product checks at lengths 8 through 512, with independently sampled permutations and root-of-unity phases;
- 30 newly assembled dense complex stage/inverse controls at lengths 8,16,32,64,128, covering independently permuted paths and arbitrary sampled unit-modulus endpoint phases/permutations;
- the exact rational positivity certificate above.

The numerical controls check stage distance, unitarity, endpoint reduction, the full baseline singular-value list, weighted-cycle N-th powers, and the `3N/4`-th covariance singular value. The smallest checked such singular value was approximately 0.77618, comfortably above the proved conservative gamma. Floating-point samples do not certify exact ranks, an all-N identity, or generality over parameters. The theorem follows from section 3, not these checks. No old modular defect or two-stage test was rerun.

## 6. Stop boundary, retained history and application

Stop attempting a one-stage original-small-strength Haar–Green transform plus an `o(N)`-rank additive correction, even with arbitrary unitary monomial endpoints: the theorem rules out that entire fixed architecture. Preserve the historical stronger full-rank sampled results, finite strong-Haar/two-stage exclusions, prior accepted norm/low-rank arguments, corrections and attribution qualifications.

This proof does **not** show full defect rank for every N, does not cover the retuned strength-1/2/epsilon-1/2 source family, does not cover arbitrary unequal-magnitude endpoint gains, and does not establish any obstruction for arbitrary multistage Haar–Green hierarchies. It does not turn a stage count or repair rank into an execution-cost lower bound. The selected successor remains an explicitly parameterized hierarchy with an all-N Fourier covariance identity, correct first-column normalization, and fully charged preparation/execution, or an equally explicit further scoped failure.

`NATIVE_CELL_PROPOSAL.json` proposes only six dated history-preserving prefixes: Catalogue AE82/AF82, `novelity breakthough` Y43/Z43, and Research overview P60/Q60. Append a verified immutable publication link when available. Re-read live preimages and preserve all previous text, rich-text runs, notes, statuses, priorities and source links. This document and proposal are not external-write receipts. Independent mathematical acceptance and separate postwrite verification remain required.
