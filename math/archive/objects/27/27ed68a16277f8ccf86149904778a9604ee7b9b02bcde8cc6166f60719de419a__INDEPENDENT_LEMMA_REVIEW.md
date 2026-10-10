# Independent review of the streaming robust selector

Reviewed 9 October 2026. Scope: the deterministic selector, probabilistic amplification, and Section 3 of `STREAMING_ROBUST_SYNTHESIS.md`. This is a proof review; no uploaded code was imported or executed. The chirp variance and per-row runtime are taken as premises from the separate decoder audit.

## Verdict

The five-representative selector and the strengthened condition **b < R/4** are valid. Section 3 correctly transfers the guarantee to complex output coordinates. Its O(N)-register result is sound under the stated exact-arithmetic model. The growing-row schedule needs an explicit upper as well as lower choice of s; a ceiling of the displayed expression supplies both. The implementable power-of-two threshold changes the displayed error constant by at most a factor of two.

## Deterministic accounting

Insertion only after all distance tests fail preserves pairwise representative separation greater than 2B. There are at most three near representatives, where near means distance at most 3B from the target: four would span more than 6B. Every insertion or increment into a far counter originates from a bad sample. This includes the initial count at insertion.

Let D count full decrements, N_near be the final near mass, and F be the final far mass. Each full decrement consumes at least two far units and at most three near units. Good arrivals are discarded at most D times, so

    N_near >= R - b - 4D,
    F + 2D <= b.

The second inequality counts disjoint surviving and consumed units, all originating from bad arrivals. Therefore

    max_near - max_far >= (R - 4b + 2D)/3 > 0

when b < R/4. If there are no far counters, the conclusion is immediate. A positive near count exists because 2D <= b gives N_near >= R - 3b > 0. Arbitrary matching choices, representative deletion and reinsertion, and equality at the distance thresholds do not invalidate the argument. R = 4s - 1 and b <= s - 1 satisfy the strict hypothesis.

## Amplification and complex constants

Independent repetitions with bad probability at most p give

    Pr[at least s bad rows] <= binom(4s-1,s) p^s.

Identical distributions are unnecessary. Dependence among different output coordinates or between real and imaginary parts of the same row is harmless. For sigma squared = (2M/N) times ||x||_2 squared, a union bound over 2N real coordinates gives the stated failure probability at

    B squared = sigma squared * (2N A_s/delta)^(1/s).

Each real coordinate has error at most 3B; each complex coordinate therefore has absolute error at most 3 sqrt(2) B. Substitution yields the displayed constant 6. This conservatively uses the complex second-moment bound for each real component and is valid.

## Scale preparation without real-power or floor primitives

Computing E = ||x||_2 squared uses O(N) field operations. E = 0 is detected exactly in this model and permits returning zero. Otherwise the algorithm can store T = B squared and test (z-c) squared <= 4T.

Let C = 2N A_s/delta > 1. Choose the least power of two A >= 1 satisfying A^(2s) >= C, and set T = (2M/N) E A squared. Then

    C^(1/(2s)) <= A < 2 C^(1/(2s)).

Consequently this implementation satisfies the same probability guarantee, with error less than twice the ideal-threshold bound: the ideal constant 6 may be replaced by 12. The formula with constant 6 remains correct when explicitly restricted to equality in the ideal threshold.

For a concrete arithmetic-only preparation, compute A_s by its s-factor product with exact division and q = 4^s by s multiplications. Start A = P = 1 and repeatedly replace A by 2A and P by qP until P >= C. At termination P = A^(2s). This costs O(s + log A) scalar operations, uses constant additional registers, and needs neither logarithms nor floors. The operation count is negligible in both stated regimes. This observation does not claim bounded-bit complexity.

## Schedule and storage clarifications

- Specify s = max(1, ceil(log(2N/delta)/(2 epsilon log log N))) for sufficiently large N, or choose s within a constant factor of that quantity. Merely requiring s to exceed the expression permits arbitrarily larger runtimes.
- The little-o runtime statement assumes fixed a >= 0 and fixed epsilon > 0, with 1 <= f = o(log log N). Then s is Theta(((1+a)/epsilon) log N / log log N), each row costs O(Nf), and the claimed total runtime follows.
- A_s <= (4e)^s gives ideal amplification at most sqrt(4e) (log N)^epsilon. Power-of-two rounding adds only the constant factor already noted.
- There are two counter lists per complex output location, each containing at most five pairs: ten pairs total, rather than ten lists. Thus all selectors together use O(N) registers. Counts require O(log R) bits and indices O(log N) bits; stored numerical values remain ideal exact registers.

No substantive obstruction was found within this review's scope.
