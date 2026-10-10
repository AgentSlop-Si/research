# Chain checkpoint — two-line Weyl product rigidity v22

## Inherited state

- v20: one fixed-shift Weyl–Green orbit has `O(N)` character aggregates but a quadratic-fiber obstruction.
- v21: all shift steps span Fourier exactly, but the Fourier coefficients collapse onto one Weyl line and become Bluestein chirp convolution.
- Exact arbitrary-input sub-`N log N` FFT remains open.

## New exact classification

Use symmetric Weyl operators `D_(a,b)=omega^(ab/2) X^a Z^b`. The Fourier Weyl symbol is

`f(a,b)=gamma omega^(-(a^2+b^2)/4)`.

For independent line directions `u,v`, remove the known product cocycle from the coefficient tensor. Its rank is

- `1` when `kappa = u dot v + sigma(u,v) = 0`;
- `N` otherwise.

Thus a single two-line product exists iff `kappa=0`. All compatible directions are

`v=t*(a-b,a+b)`

with `a^2+b^2 != 0`.

## Exact factorization

For

`L_u=sum_m omega^(-||u||^2 m^2/4) D_(m u)`,

and compatible `v`,

`F = L_u * (gamma L_v)`.

The factors are unique up to one reciprocal scalar.

## Rigidity of successful factors

- A vertical line factor is a diagonal quadratic chirp.
- Every nonvertical anisotropic line factor is exactly `D_left P F D_right`.
- An isotropic factor has rank one and cannot occur in an independent successful pair.

Therefore every successful two-line factorization contains at least one factor already Fourier-equivalent; if both directions shift, both factors are Fourier-equivalent.

For an incompatible fixed pair, a sum of `r` products requires `r>=N` by the dephased tensor rank.

If a hard factor is represented as `q(C)^(-1)p(C)`, the one-cycle recurrence gate forces

`deg q >= floor((N-deg p)/2)`.

## Verification

- 8 automated test groups pass.
- Exhaustive pair classification at `N=5,7`.
- Exact factorizations at `N=7,11,13,17`.
- Independent verifier passes four cases.
- Closed-form factor matrices checked for every tested anisotropic direction.

## Do not repeat

- another arbitrary search over two Weyl lines without checking `kappa` first;
- treating a compatible two-line product as a speedup: one factor is already Fourier-equivalent;
- a constant/polylog-order rational recurrence for the hard factor;
- sums of a sublinear number of products on an incompatible fixed pair.

## Exact next target

Either:

1. a three-line/metaplectic product whose factors are individually easier and admit a genuinely joint executor; or
2. a high-treewidth non-Krylov exact stage outside Weyl line algebras.
