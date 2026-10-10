# Cache-directed internal rewrites: what the twist changes

## The corrected question

The earlier analysis of replacing a whole integer `A` by `A-k` evaluated two
products independently. That model does not cover a graph where one product
already exists. The relevant question is whether a local rewrite exposes a
cached subgraph large enough to pay for the correction and its discovery.

Let `P = U * B` already have a valid cached value. For a target `A * B`, derive
`K = A-U`. Then

\[
A B = P + K B.
\]

There is no requirement that `K` be numerically small. It must be inexpensive
in the actual representation, or `K B` must itself be available. A dense seed
can be a cheap correction if its transform was already computed and that cost
has been charged. Merely observing small numerical distance does not certify
a graph identity.

The prototype uses the supplied engine's real circular-convolution ring. Its
full spectra are computed with `scipy.fft`; the rule operates above those FFT
calls. This is distinct from replacing a twiddle multiplication inside a scalar
FFT butterfly or rewriting recursive FFT calls of different lengths.

## A structural proof, with an independently executable audit

For selected graph nodes, define a linear signature

\[
\sigma(X)=\sum_j c_j a_j.
\]

The `a_j` are immutable opaque nonlinear nodes or unit impulses. `sum` and
integer `scale` nodes expand into this signature; products remain opaque atoms.
Coefficients are exact bounded integers. Constructor output is checked against
the intended correction signature before a proposal can be accepted.

The candidate construction guarantees:

1. The target factors as `A * B` in the stored canonical DAG.
2. The cached node factors as `U * B`, verified by canonical node identity.
3. `sigma(K) = sigma(A) - sigma(U)`.

By induction through the signature expansion, equality of these signatures
implies `A = U + K` for every assignment to the atoms in a commutative ring.
Distributivity then gives `A*B = U*B + K*B`. This proves the rewrite under the
canonical DAG's algebraic semantics. It does not prove that floating-point
execution is unchanged bit for bit, or that the original construction of an
arbitrary floating expression was exact.

The delivered audit independently evaluates small graph instances in
`F_p[z]/(z^n-1)` by quadratic circular convolution, with `n` in `{5,8,13}` and
`p` in `{97,257}`. Forty-eight witness instances pass all four checks: the
additive relation, target factorization, cached factorization, and replacement
equality. A deliberately corrupted correction is rejected in the test suite.
These are exact implementation checks, not a substitute for the general
algebraic argument or a formally verified optimizer.

## Graph cost and the cached frontier

Let `C` be the set of available node values. Define `W(R | C)` by traversing
the DAG rooted at `R`, stopping at available nodes, and counting each remaining
node once with its local vector-operation weight. This avoids charging a shared
descendant once for every parent.

The local acceptance condition is

\[
W(P+KB\mid C) < W(AB\mid C).
\]

The implementation counts additions, multiplications, scalar operations and
fills; phasor generation receives a conservative heuristic weight. These are
work estimates, not calibrated CPU costs. Search, copying and allocation can
outweigh a predicted arithmetic saving, especially at small `n`.

After selection, the cached frontier of the replacement is pinned in the
current evaluation memo. This prevents LRU eviction from invalidating the
availability assumption used by the cost estimate. Candidates that would
depend on the target's uncomputed value are rejected. The resulting policy
is local, bounded, and non-optimal: it does not solve global DAG extraction,
predict every future consumer, or optimize cache replacement over a query
sequence.

There was also a separate baseline issue. The supplied `evaluate_spectrum`
first enumerates all descendants, then checks whether each node is cached.
With a small LRU this can recompute evicted descendants and even evict the
cached parent before it is reached. The new evaluator checks the parent first
and stops immediately on a hit. Both benchmark modes include this correction;
none of that improvement is attributed to the distributive rewrite.

## Positive graph family and measured scope

Take a product `G` of `m` immutable signals and a common operand `B`. First
compute `P=G*B`; then request

\[
Q_i=(G+i\delta_0)*B=P+iB.
\]

In the supplied canonicalizer, products flatten. Thus the node for `P` does
not necessarily retain `G` as a evaluated child: the factors of `G` are
merged into `P`. With a small result cache, subsequent `Q_i` evaluations can
reconstruct and repeatedly lose `G`. The rule instead uses `P` or a more
recent `Q_j`, with correction `(i-j)B`.

For this evaluation strategy, graph vector work can fall from order `nmV`
to order `n(m+V)` for `V` related versions under cache pressure. This is a
statement about this graph family and evaluation strategy, not a lower bound
on all other algorithms. A sufficiently large cache already preserves `G`;
explicit polynomial updates or an ideal algebraic optimizer can also exploit
the same relation.

The benchmark uses `m=24`, eight versions, and **25 input FFTs plus nine full
inverse FFTs**, all charged. The tight result cache holds three spectra.
The measured pointwise multiplication count drops from 193 to 24. Every query
starts from explicit immutable graph nodes; no numerical nearest-neighbor
oracle supplies a free correction.

A separate initially cold graph is

\[
F=P+C*((G+\delta_0)*B+H).
\]

The `P` branch is evaluated earlier in the same call, exposing reuse in the
later internal product. There is no previous-query cache at entry. The
supplied one-pass common-factor optimizer is applied to this workload before
both modes run. Vector multiplication counts drop from 49 to 25, although
input FFT costs and measurement noise can erase the end-to-end gain. A simpler
already factored expression is also included as a negative control; the new
rule saves nothing there.

Inputs are dense Gaussian perturbations of a unit impulse, chosen to keep
long products numerically well scaled. They are a specified graph workload,
not a distribution of arbitrary integers. Here `n` is one signal's length;
the total input contains many such signals. This is not a benchmark of
multiplying two fresh `n`-bit integers.

See `BENCHMARKS.md` for all sizes, including losses. Timings close to 1x should
be treated as inconclusive. The raw repeated measurements are retained.

## Floating-point counterexample

Let all factors of `G` be impulses, with one factor equal to
`(-1 + 2**-52) delta_0`; let `B = 10**16 delta_0`. The target is
`(G+delta_0)*B`. Its exact nonzero output is `10**16 / 2**52`.

The ordinary evaluation returns `2.220446049250313`. Reusing `G*B` and adding
`B` returns `2.0` due to cancellation. The ring identity remains true, but
arithmetic savings alone do not establish acceptable numerical error.

An exact modular implementation would preserve the identity modulo its prime.
An exact integer implementation must additionally reconstruct sufficiently large
coefficients and propagate carries. A floating implementation needs a precision
or error policy; none is silently assumed here. The small modular oracle is
not a fast NTT backend and provides no integer-multiplication runtime result.

## Why this does not yet beat the global target

There are three different reusable things:

| Reused object | What still costs work |
|---|---|
| Input-independent graph, schedule, twiddles | Numerical gates on each fresh input |
| Input-dependent cached subproduct | Discovery, correction, additions and storage |
| Whole cached result or suitable output representation | Reading or producing the requested outputs |

This prototype still performs conventional input FFTs and a full inverse FFT
for each full time-domain output. For `R` registered length-`n` seeds and `Q`
outputs, its cost ledger includes

\[
O((R+Q)n\log n) + O(n\,W_{\rm missing})
+ T_{\rm construction}+T_{\rm search}+T_{\rm cache}.
\]

It therefore supplies no sub-`n log n` fresh-input bound. Nor is its fixed
machine-precision vector-operation model a bit-complexity proof.

More generally, even perfect reuse of a multiplication can leave linear
correction work at each recursion level. If a level costs `c n` and there
are `log n` levels, that sum is still `Theta(n log n)`. A sub-logarithmic
improvement would need to bypass or jointly process enough whole subgraphs
across levels and prove that all remaining corrections, discovery, preparation,
precision and output costs stay below the target on every allowed fresh input.
The identity alone supplies no such universal reuse guarantee.

A scoped counting obstruction illustrates the missing assumption. Suppose
the current block is uniform in `F_q^d` and independent of a fixed cache of
`M` base blocks. If corrections are restricted to at most `s` nonzero
coordinates, a union bound gives

\[
\Pr[\exists\ U\text{ cached}:\|A-U\|_0\le s]
\le \min\!\left(1,\frac{M}{q^d}\sum_{j=0}^{s}\binom dj(q-1)^j\right).
\]

For fixed `q`, polynomial `M`, and `s=o(d)`, this tends to zero exponentially.
This does **not** apply to the related graph family above: its operands are
deliberately dependent. It also says nothing by itself about more general
cheap circuits, low-rank corrections, nonuniform inputs, adaptive correlated
caches, or the impossibility of a different fast FFT algorithm.

## Connection to the previous research

| Earlier component | What this phase adds or leaves open |
|---|---|
| Persistent chains and explicit sparse updates | Reuse discovered at an internal product without an externally supplied update path |
| Polynomial jets in the sum/product engine | The degree-one identity is compatible; known higher-degree update machinery is not replaced |
| Canonical compiler and common factoring | A cached expanded product can be preferable to a freshly factored expression; cache-aware demand evaluation now cuts descendants |
| Selected-frequency/projection queries | The same graph idea may apply there, but those query costs are not full-transform costs |
| Fresh Fourier skeleton/rank experiments | Their stated decoder restrictions do not disprove cache-directed DAG reuse |
| Whole-integer signed-digit translation | Independent-product weight arguments do not cover a cached product |
| Fresh annihilating filters in Phase 11 | A possible source of cheap structured corrections; linear convolution and circular convolution must be reconciled explicitly |
| `integer-mult-kappa` | Still a separate conditional asymptotic route; this package changes no exponent certificate |

The highest-value next integration is to feed these exact graph witnesses into
the existing update machinery or an exact modular evaluator, while charging
all conversions. For the asymptotic question, the unresolved object is an
explicit all-input family of reusable recursive subgraphs with a complete
cost recurrence. No finite benchmark establishes that object.
