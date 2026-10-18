# Independent review: arbitrary sparse-core inverse obstruction

18 October 2026. Owner: M-NONLINEAR-COMPATIBILITY.

## Verdict

**ACCEPT the restricted-family theorem and its stated corollaries. No mathematical correction is required.** Keep the unrestricted owner **TO RESEARCH, priority 34**. The full 64-equation F8 target ideal remains undecided.

Reviewed candidate: `catalogue_sparse_inverse_20261018_1748/REPORT.md`, SHA256 `a7c94f9059542cded0cb4169cc7bf3383588c9ad4cc749abbf3bab1de6692352`.

The all-N theorem is justified by the analytic argument, not by finite numerical evidence. No new novelty, arithmetic-runtime, global catalogue, or full-owner-closure conclusion follows. No external write or source modification was made in this review.

## Source model and hypotheses

The retained accepted chart specifies complex scalar stages with entries

- T[i,i] = d[i]
- T[i,j] = l[i] m[j] for i > j
- T[i,j] = u[i] v[j] for i < j.

Individual generators can vanish. A block whose every row index exceeds every column index is an outer product and has rank at most one. Transposition preserves the chart. This is the exact separated-generator chart, not the class of all quasiseparable matrices or all fast linear circuits.

The accepted target is the unnormalized Fourier matrix, with F[i,j] = zeta^(i*j), and F = B P A. The source permutation has P e_j = e_p(j), p = [7,0,6,3,4,1,2,5]. The candidate's proof works for every middle permutation and consequently includes the pinned convention. F and P are invertible, so A and B are automatically invertible in any solution; no separate inverse guard is lost.

All 12 candidate manifest entries were independently hash/length checked. The three retained primary source bodies reproduce their stated Git blob SHA1s and SHA256s. This checks the supplied source bytes and bindings; the review did not perform a second remote source retrieval or a catalogue-wide source audit.

## Independent proof review

### Consecutive sampling

For m consecutive rows beginning at a and any frequency set U of size at most m, the first |U| rows, after nonzero column scaling, are a square Vandermonde matrix at distinct roots zeta^j. Therefore the Fourier sample map is injective on the full coordinate subspace supported on U. Wraparound modulo N is harmless because zeta^N = 1. No ordering or spacing condition is needed for U.

### One-debit kernel argument

Let C_J = S_J + R_J have k independent columns and let T be injective on im(S_J). The map x -> R_J x from ker(T C_J) into im(R_J) is injective. Indeed, T C_J x = 0 and R_J x = 0 imply T S_J x = 0, then S_J x = 0, then C_J x = 0, then x = 0. Thus dim ker(T C_J) <= rank(R_J), yielding rank(T C_J) >= k - rank(R_J).

This reasoning is valid even when S_J has dependent columns or the full sparse core S is singular. The actual corrected columns C_J supply the independence. The proposed improvement from two rank debits to one is valid.

### Cut geometry and dimensions

Set k = r+2 and m = sk, for integers s >= 1 and r >= 0. The first k columns of B = F C P^(-1) select k distinct columns of the invertible C = A^(-1). Their S supports have union size at most m. The last m Fourier rows therefore give sampled rank at least k-r = 2.

The size condition N >= m+k = (s+1)(r+2) simultaneously ensures both sample sets exist and that their smallest row index N-m is at least k. Their largest column index is k-1. The entire block is strictly below the diagonal, including the equality case N = m+k, so the chart forces rank at most one. The contradiction is sound.

No probability, generic nonvanishing, or invertible-core assumption is used. The stronger local statement with the actual support union and rank(R[:,J]) is also valid.

### Orientation and rescaling

Transposing F = B P A gives F = A^T P^T B^T. Consequently a row-sparse core for B^(-1) gives the required column-sparse core for the right inverse after transposition. An arbitrary column-sparse hypothesis on B^(-1) is not claimed and would not follow from this step. For a diagonal core the two orientations agree.

For a target D_L F D_R, pass to B' = D_L^(-1) B and A' = A D_R^(-1). Their inverses are B^(-1) D_L and D_R A^(-1), respectively. These invertible diagonal multiplications preserve the relevant sparse supports and correction ranks, and the chart is preserved. The stated diagonal-rescaling extension is therefore valid. Endpoint permutations are correctly not asserted.

The rank-t cut variant follows by replacing k by r+t+1, for a nonnegative integral rank bound t.

## Corollaries and genuinely surviving boundary

- At r=0, the bound is N >= 2s+2 for arbitrary s-sparse inverse columns, with the transposed row statement on the other inverse.
- At s=1, diagonal-plus-rank-r inverses are excluded for N >= 2r+4, including singular diagonal cores. The previous 4r+4 result remains true but is weaker.
- At N=8, this excludes diagonal-plus-rank-two inverses on either stage, arbitrary three-sparse A^(-1) columns, and arbitrary three-sparse B^(-1) rows.
- The stage A = I + E[2,0] + E[5,7] is exactly in the accepted chart. Its inverse I - E[2,0] - E[5,7] is column-two-sparse, outside cyclic-tridiagonal support, and outside diagonal-plus-rank-one because its disjoint rows [2,5], columns [0,7] minor is 1. Thus the extension is substantive within the source chart.
- The accepted stage with diagonal 3, lower entries 1, and upper entries 2 has an inverse with all 64 entries nonzero. Its disjoint rows [0,2,4], columns [1,3,5] minor is exactly -8/511. It is therefore outside the two explicit new F8 corollaries (three-sparse inverse and diagonal-plus-rank-two inverse).

The dense boundary is not proved outside every possible sparse-core-plus-low-rank decomposition. The candidate explicitly preserves this distinction. Neither boundary example is a Fourier factorization.

## Independent exact controls

The fresh `check_independent.py` uses SymPy 1.14 DomainMatrix arithmetic over the exact algebraic field Q(zeta8), represented by zeta8 = sqrt(2)(1+i)/2. It neither imports nor executes the candidate or historical programs. It checks:

1. All 2,040 nonempty square Fourier minors with consecutive cyclic output rows, across all sizes 1 through 8 and all frequency subsets, against a separately formed Vandermonde formula. Size counts: 64, 224, 448, 560, 448, 224, 64, 8.
2. The 4,278 unordered pairs of nonempty supports of size at most three and direct exact rank of each of their 246 distinct support unions under the last-six-row sample map.
3. Exact two-sided inverse identities, source-chart generators, and disjoint minors for the newly excluded and surviving dense stages. The dense inverse was recomputed independently by matrix inversion.
4. An independently constructed five-sample collision from an exact nullspace, completed to an invertible column-three-sparse matrix. Its sampled rank rises from one to two when the sixth consecutive row is added. The candidate's separately stored collision was also verified.
5. An independently reconstructed diagonal-core/rank-two-correction example with determinant one, correction rank two, and sampled rank exactly 4-2 = 2; it agrees with the candidate's stored example.
6. A singular sparse core repaired to I, the nonconsecutive-row and dependent-column failure controls, and an additional general-map example where a singular one-sparse core attains k-r with a rank-one repair.

All checks passed. `RUN.stderr` is empty. `RESULTS.json` contains exact outcomes.

## Sharpness and scope discipline

The k-r estimate is attained and therefore sharp under the kernel lemma's hypotheses. The five-versus-six sample control demonstrates that the particular arbitrary-three-support injectivity argument cannot simply use five samples. It does not show that no stronger Fourier or chart argument exists with fewer samples.

Neither control establishes sharpness of N >= (s+1)(r+2), nor existence of a factorization below that threshold. The candidate states these limitations accurately. It supplies a restricted-family structural theorem, not a decomposition-recognition algorithm, a numerical-tolerance theorem, a machine-formalized proof, an unrestricted characteristic-zero infeasibility certificate, or a computational lower bound.

## Disposition

Accept this new restricted mathematical boundary. Preserve the owner ID, status, priority, historical classifications, and the unrestricted target gate. No corrective changes are requested.
