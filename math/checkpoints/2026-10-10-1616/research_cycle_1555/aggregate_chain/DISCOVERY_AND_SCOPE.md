# Bounded discovery ledger and scope

10 October 2026.

## Main result

The deliverable is `four_chain_v2/GAUSS_CHAIN_FAMILY.md`: a symbolic family with E=2p²+p−floor(p/4) for every odd prime p≥5, plus the one-sided no-saving theorem when nnz(C)≤p+2. It does not depend on the search code for its proof.

The original independently verified five-chain witness is preserved unchanged in `EXPLICIT_P5_CERTIFICATE.json` and `fresh_explicit_certificate.py`. Its count is 25+9+20=54. The simpler four-chain v2 has 25+8+21=54, and generalizes uniformly. These are different certificates, not contradictory ledgers.

The separately supplied full p=3 theorem is independently checked in `INDEPENDENT_P3_REVIEW.md`; it establishes the optimum21 only for the square-invertible colored aggregate model.

## Bounded search performed

Only p=5 nonzero unit-bidiagonal chains were searched. For a chain ordering i0,…,i4, write nonzero prefix coefficients b0,…,b4. Its inverse Fourier rows, up to nonzero row factors, are

    Q_j(t)=Σ_(k≤j) b_k ζ^(i_k t).

Each prospective zero is therefore a linear equation in five complex unknown coefficients. Five or more zeros imply some five-constraint mask among the 20 possible stage/root positions with j=1,…,4. All 15,504 masks were considered.

Two necessary exclusions are exact:

1. Stage j has at most j grid zeros by prime Fourier uncertainty (also ordinary degree for the consecutive ordering).
2. Adjacent stages cannot both vanish at the same root, because their difference is one nonzero monomial.

The remaining 2,885 masks were tested by exact determinant arithmetic in Q(ζ5). A 5×5 determinant was evaluated by its permutation expansion, accumulating exponents modulo5; it vanishes exactly when its five integer coefficient totals are equal. Singular kernels were classified using exact minors, with a candidate retained only if no coordinate is forced zero.

For consecutive ordering (0,1,2,3,4), the masks split as 6,779 degree/support exclusions, 5,840 additional adjacent-stage exclusions, 2,705 full-rank matrices, and 180 rank-four kernels forcing a coefficient zero. This proves no five-zero possibility in this restricted chain family, hence no improvement there.

The only extension was the six affine-normalized row orderings with i0=0,i1=1 and a permutation of 2,3,4. It produced feasible kernels, including order (0,1,2,4,3), from which the explicit witness was derived. No arbitrary coefficient grid or wide unrestricted matrix search was run. No source/uploaded research program was imported or executed. All scripts here were newly authored.

The counter named `excluded_by_degree` in the all-order discovery output means the support-uncertainty exclusion for nonconsecutive orders; its calculation is the same bound of at most j zeros. The candidate list is not a minimum-edge certificate. In particular, neither the search nor the constructive theorem proves that54 is the global p=5 optimum.

## Stopping point

The task ends with the explicit family, support threshold, exact controls, and separate independent review. It leaves no parameter search running. Both the family and the dense baseline are quadratic, and no faster FFT or general lower bound has been obtained.
