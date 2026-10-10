# Source 01: conductor_tradeoff.py

SHA-256: `4f70e27cb39fa23e6f3bd166254d1c0988c6462e98a2772a7c0e04488da5659f`

Exact bytes: 3678; fully read lines: 1-99.

Snapshot: `snapshots/01_conductor_tradeoff.py`

Inspection: complete inert first-to-last source reading. No source execution, import, compilation or syntax/AST parsing.

## Mathematical and operational scope

General conductor B=2^b, N=2^m with 3<=b<m<=2b. The orbit decomposition of multiplication by 1+B and the exponent identity are checked using integers. For L=N/B<=B, each orbit contributes one nonzero per input column to A; the N*c(N,B) count follows. For L>B the returned impossibility applies to one K_B-defined sandwich by the primitive-L-eigenvalue field obstruction, not to unrestricted multiphase algorithms.

## Control/dataflow and algebra

Lines 24-36 enumerate disjoint cycles. Lines 46-85 verify their lengths, the linearized multiplier and, when full_check=True, every phase exponent; lines 86-92 report counts. The method does not construct or apply a sparse A matrix. The identity B*r*t+r+L*h=k*j modulo N matches the documented factorization.

## Input/guard and acceptance review

Main factor and orbit entry points assert positive powers of two, B>=8, B<N; L>B returns a scoped negative result. cycle_count_formula at 39-43 instead permits B=1 or 2, outside the formula assumptions. For example N=8,B=2 has five cycles under multiplication by 3, while the returned expression is four. All structural assertions disappear under optimized Python.

## Cost accounting

Full phase audit performs sum_over_orbits(N*orbit_length)=N^2 exponent comparisons, plus O(N*number_of_cycles) work and O(N) cycle storage. full_check=False omits the N^2 loop and labels the flag False; it is count-only evidence. The proposed naive application cost Theta(N*(B+(B/2)*log2(N/B))) is explicitly charged and is not a sub-N-log-N result.

## Test coverage and limitations

test_phase14 lines 80-88 cover positive threshold cases and L>B rejection. They do not cover B=1,2, malformed types, optimized execution or full_check=False. Main examples are written cases, not review executions.

## Dependency identity

Only standard-library Counter and math.gcd (dynamically imported at line 64); no supplied algorithmic dependency.

## Finding references

F03, F06, F09
