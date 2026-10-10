# Independent audit of the supplied scan-network certificate

9 October 2026. The supplied central exclusion is valid within its stated
scope. No uploaded executable was run, imported, or bundled here.

## What was independently reproduced

Input: the data file `new_network_certificate_N64.json` from the supplied
`fft_scan_network_gate_2026-10-09(1).zip`. An unchanged copy is included as
`scan_certificate.json` so this package can be checked without external paths.

The newly written standard-library checker reconstructed the directed graph
from forward and backward register recurrences, scalar input/output channels,
and the specified permutation. It did not call the upload's graph builder,
flow solver, rank checker, or other code.

- Graph: 1,018 vertices and 1,503 directed edges, including source/sink links.
- The recorded partition contains only valid vertices, contains the source,
  excludes the sink, and has no duplicated source-side vertices.
- Exactly the recorded 16 capacity-one edges cross the partition.
- A separately implemented integer Edmonds-Karp maximum flow is also 16.
- The old interval calculation is 9 + 4 + 4 = 17.
- The listed 17 physical rows and 17 physical columns are distinct and are
  contained in the correct bit-reversed 24-by-27 Fourier rectangle.
- Both supplied moduli were independently verified prime by trial division.
- Both roots have order 64; their 32nd powers are -1 modulo the prime.
- The same 17-by-17 determinant is nonzero at both roots:
  - modulo 998244353: 959841740;
  - modulo 2013265921: 1437727086.
- The entire rectangle has modular rank 17 over both fields. These finite
  ranks certify complex rank AT LEAST 17, not an upper bound of 17.

Thus the fixed graph permits rank at most 16, while the target Fourier
rectangle has complex rank at least 17. The chosen endpoint/middle ordering
cannot realize Fourier using two quasiseparable rank-one stages. The new
graph cut strictly improves the specified interval cut for this rectangle.

Forty additional independent sanity checks generated actual two- and
three-stage quasiseparable matrices, with widths one and two, at N=8 and
N=12. Each exact modular minor rank was at most the independently computed
network flow. These checks supplement the mathematical argument; they do
not establish it for all possible generators.

## Why the complex certificate follows

The determinant is a polynomial D(z) with integer coefficients. If it vanished
at a primitive complex 64th root, the monic minimal polynomial z^32+1 would
divide D over the integers. Its evaluation at either verified modular root
would then vanish. The nonzero exact modular determinant contradicts this.
No floating-point residual, numerical rank threshold, or random test is used
for the nonvanishing certificate.

The register graph upper bound is a standard linear information-flow bound:
the chosen outputs can depend on chosen inputs only through the scalar/vector
channels crossing any separating cut. The graph represents admissible
quasiseparable forward/backward generators, including direct diagonal paths
and the supplied scalar-wire shuffle. Each cut of total capacity c provides
a factorization of the selected transfer map through at most c scalars.

## What is not concluded

The certificate concerns exactly N=64, rank pair (1,1), bit reversal at both
endpoints, and the recorded middle permutation. It says nothing universal
about all shuffles, all endpoint orders, rank pair (2,2), or larger depth.
The upload's reported 25,000-case negative search at rank pair (2,2) was not
rerun; absence of a rank contradiction would not prove feasibility anyway.
The other uploaded aggregate stress-test counts were not re-executed.

The scan gate does not by itself produce an arithmetic lower bound or a
faster FFT. This audit adds a standalone reproduction of its decisive finite
certificate and connects it to the all-N whole-word gates in `PROOF.md`.
