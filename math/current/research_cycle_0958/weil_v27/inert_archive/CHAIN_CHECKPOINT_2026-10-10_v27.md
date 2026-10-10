# Chain checkpoint — primitive-phase invariant-subspace rigidity v27

## Inherited state

- v24: higher-dimensional finite-field Weil operators are partial tensor DFTs; cyclic prime-power Fourier is excluded.
- v25: one-dimensional local-ring Weil cells are partial cyclic DFTs, but proper cells cannot assemble the full Fourier Weyl element.
- v26: higher-dimensional local-ring Weil words produce additive-group Fourier cores, not the cyclic transform of the same dimension.
- Exact arbitrary-input cyclic sub-`N log N` FFT remains open.

## New primitive Weyl theorem

For a field containing a primitive `N`th root `zeta`, any exact operators

`X^N=Z^N=I`, `ZX=zeta XZ`

have normal form

`X=S_N tensor I_m`, `Z=D_N tensor I_m`.

Hence every nonzero invariant subspace has dimension divisible by `N`; the generated algebra is `M_N tensor I_m`, with commutant `I_N tensor M_m`.

## New swap rigidity

Every exact swap satisfying

`J X J^-1=Z`, `J Z J^-1=X^-1`

has the form

`J=F_N tensor U`.

For any covariant injection `E` and extraction `P`,

`P J E = scalar * F_N`.

Thus an exact primitive-phase invariant-subspace embedding exposes a full Fourier core; it does not create a smaller transform.

## New character-table direct-factor theorem

If an `N x N` coordinate submatrix of the additive Fourier table of `(Z/NZ)^n` is monomially equivalent to `F_N`, then its row/column labels have

`x_i=x_0+i*u+w_i`, `y_j=y_0+j*v+w'_j`,

with `<u,v>=1` and all spectator pairings zero. The ambient module splits as

`R*u direct-sum ker(<-,v>)`.

Nontrivial spectators may exist over rings with zero divisors, but they carry no primitive phase.

## Verification

- 9 automated test groups pass.
- Weyl monomial span rank `N^2` at `N=3,5,7,9`.
- Exact commutant and swap-solution dimensions `m^2` at five `(N,m)` cases.
- Exhausted 254,016 ordered submatrix candidates in `F_3^2`:
  - 9,720 Fourier embeddings;
  - all 9,720 satisfy the theorem;
  - 7,776 have nontrivial spectators.
- Exact nontrivial local-ring lifts at `N=9,25`.
- Independent verifier passes.
- v26 predecessor ZIP CRC passes.

## Do not repeat

- embedding cyclic Fourier into a larger additive/Weil space while assuming primitive Weyl covariance creates a smaller core;
- counting ambient dimension or multiplicity as computational sharing without restricting the operator;
- treating ring nilpotent spectator coordinates as extra Fourier information;
- claiming this scoped rigidity theorem is an unrestricted FFT lower bound.

## Exact next target

Either:

1. a non-covariant injection/extraction with a fully charged sub-`N log N` ambient evaluator; or
2. a non-Weil high-treewidth operator with a genuine exact non-Krylov fast solver; or
3. a global arithmetic DAG outside character-table/Heisenberg covariance.
