# Source 20: halfcut_certificate.py

SHA-256: `5b13aa4ea55c8d161cfcc631002c27bfd7f79f439e0edba4744753dfb5ba3853`

Exact bytes: 4555; fully read lines: 1-128.

Snapshot: `snapshots/20_halfcut_certificate.py`

Inspection: complete inert first-to-last source reading. No source execution, import, compilation or syntax/AST parsing.

## Mathematical and operational scope

Finite-field halfcut certificate for two quasiseparable stages with one interstage permutation/diagonal weighting. Necessary condition r_left+r_right>=N/4 follows because complementary overlap counts sum to N/2 and one is at most N/4. Input or output relabeling alone preserves an appropriate consecutive-exponent Vandermonde argument; both simultaneously are explicitly excluded.

## Control/dataflow and algebra

Creates structured dense stages, optionally checks every cut, selects two complementary column halves, separates crossing/outer/inner contributions, and bounds ranks by r_left, r_right and overlap count. It compares each Fourier rectangle rank to N/2 and derives theoretical_rejection from the rank threshold.

## Input/guard and acceptance review

Even N, root divisibility and no simultaneous external permutations are asserted. Positive N/order bounds, bijections, matrix dimensions and gain lengths are not explicit in public helpers. fourier_rect checks only w^N=1, with exact primitiveness depending on the known fixed prime/generator. Integer-to-float m/2 in the rejection condition is unnecessary and can lose precision at enormous N, although dense allocation makes such N infeasible first.

## Cost accounting

O(N^2*r) stage construction, O(N^3) rectangular products and rank checks; cut_bound over all cuts can total O(N^4) for N<=64. The proof formula is constant-time once valid structural hypotheses are known, but this empirical audit is not.

## Test coverage and limitations

test_halfcut includes rejection, equality where the theorem is silent, nonunit diagonal gains and separate input/output permutations. It does not explicitly test the required simultaneous-reordering rejection or odd/nondividing sizes.

## Dependency identity

Exact in-batch minor_certificate supplies stage, rank, permutation and MOD. Rank helper reuse makes tests corroborative rather than fully independent implementations.

## Finding references

F03, F06, F09, F12
