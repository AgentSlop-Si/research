# Independent acceptance of the full p=3 aggregate lower bound

10 October 2026. This note independently checks the proof supplied by the separate aggregate reviewer. It is distinct from that reviewer's verification of the constructive p≥5 family.

## Accepted theorem

For invertible complex 3×3 A,C in the accepted colored aggregate model,

    E(A,C) ≥ 21 + Σ_t (r(t)−1)(s(t)−1) ≥21.

In particular, 21 is the exact minimum because A=C=F3 gives R=S=I and 9+9+3 edges.

## Independently checked two-factor proof

Suppose F3=XY and nnz(X)+nnz(Y)≤11. At least one factor has at most five nonzeros. If necessary transpose the factorization, using F3^T=F3, to put such a factor on the left.

A nonzero determinant supplies a perfect matching. Permuting hidden columns and scaling those columns normalizes the left factor to I+N with at most two nonzero off-diagonal entries. The right factor undergoes only monomial row operations, so both support counts are unchanged.

The possible off-diagonal patterns are exhausted by:

- zero or one entry;
- two noncomposable directed entries, including common-row and common-column forks;
- a directed two-cycle;
- a length-two directed path on three distinct vertices.

In the first two cases N²=0 and inverse support is unchanged. In the two-cycle case the nonsingular 2×2 block and its inverse each have four nonzeros. In these cases the accepted prime Fourier uncertainty bound gives nnz(X)+nnz(X⁻¹F3)≥12.

In the three-vertex path case, the all-prime arbitrary-index chain proof in `four_chain_v2/GAUSS_CHAIN_FAMILY.md`, Section 4, excludes more than two Fourier cancellations against the two extra edges. It again gives a total of at least12. The classification uses only the two extra arrows, so there is no missed longer path or cycle.

Therefore every two-factor realization of F3 has at least12 entries, attained by F3·I.

Finally C R=F3 and S A=F3, so both nnz(C)+nnz(R) and nnz(S)+nnz(A) are at least12. Since

    Σ_t r(t)s(t)=nnz(R)+nnz(S)−3+Σ_t(r(t)−1)(s(t)−1),

substitution into the exact aggregate objective proves the displayed bound. No pointwise-path assumption, color merging, rectangular-layer claim, or finite-field specialization is used.

## Review decision

Accepted as a complete p=3 theorem for the square-invertible aggregate model. The p≥5 explicit chain construction is consistent with it and shows why this result cannot simply be promoted to every prime.
