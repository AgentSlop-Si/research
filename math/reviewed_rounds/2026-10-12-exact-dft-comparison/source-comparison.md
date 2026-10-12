# Finite Exact DFT Source Comparison

Source review date: 12 October 2026 UTC.

## Conclusion

The project titled **Finite Network Improvements for the Exact Discrete Fourier Transform** studies finite constructions that yield an asymptotic improvement for the exact DFT at every positive length. Its score is the exponent saving δ in `T(n) = O(n (log n)^(1−δ))`. A construction at one small size, a low parameter count, or a numerical fit does not by itself improve that score.

The named project's selected result is **δ = 0.000754736**. A stronger comparable published result was found in Jacob Sussman's repository: **δ = 0.0008762478**. Both figures below are descriptions of pinned upstream sources. This review did not rebuild their proof projects, rerun their verifiers, or establish an exhaustive global frontier. It establishes neither a new result nor a verified improvement by the present research project.

## Pinned sources and reported results

| Source | Revision inspected | Reported all length DFT saving | Evidence boundary |
|---|---|---:|---|
| [Ryan Shea project](https://github.com/shea256/fourier-transform-below-nlogn/tree/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4) | `c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4` | `7547360/10^10 = 0.000754736` | Registry selects the imported Sussman and Boukhalfa result as formalized; the repository reports a reproduced Lean build and audits. |
| [Jacob Sussman project](https://github.com/jacobalansussman/wht-power-saving-lean/tree/9c94857bbaee886f8649edee0bc2d3c738f9555e) | `9c94857bbaee886f8649edee0bc2d3c738f9555e` | `8762478/10^10 = 0.0008762478` | README reports Lean and statement-comparator checks for the all-length DFT and convolution theorem. |

The selected Shea record has tensor saving `a = 7547361/10^10`, with `a−δ = 10^−10`. Sussman's stronger record reports tensor/Walsh–Hadamard saving `8762479/10^10`, also one unit of `10^−10` above its DFT saving. These are different parameters from the integer-multiplication saving κ. Ratios between such parameters are not measured runtime speedups. Sources: [selected registry](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/results/registry.json), [Sussman README](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/README.md).

## Computational model and exactness

The stated model charges unit cost for exact complex field operations, allows unbounded coefficients and intermediate magnitudes, and supplies a specified root of unity whose order is below `1024 n^3`. Integer operations and random access use a fixed number of `O(log(n+2))`-bit words. Preparation of scalars, initialization, indexing and data movement are charged. The claim concerns a uniform algorithm producing the entire exact transform for arbitrary inputs and every positive length. It is not a bit-complexity, bounded-coefficient, stability or practical FFT speed claim. Source: [finite-network framework](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/paper/framework.md).

The fixed tensor kernel is

`C = (1/2) [[1+i, 1−i], [1−i, 1+i]]`.

A compatible witness fixes integers `m ≥ 2`, `W ≥ 1` and nonnegative integer call multiplicities `n_r` for `1 ≤ r < m`. For every `f ≥ 1`, its algorithm must apply `C^(⊗mf)` to all `W` arbitrary arrays, including arrays used as dirty auxiliary storage. Recursive calls transform `rf` binary axes, independently on every remaining fiber. All necessary adapters must be explicitly implemented.

For `k = mf+b`, `0 ≤ b < m`, other work must be bounded by `A W 2^k` with `A` independent of `k` and `f`. This includes copies, scalar operations, phases, layouts and inverses. Preparation is constructive; live storage is `O(W2^k)`; addresses occupy a fixed number of `O(k+1)`-bit words. Correctness must cover arbitrary data and scratch, and the histogram must include real recursive calls and endpoint corrections. A finite cover may multiply the physical stock and call counts; its cancellation from a normalized formula does not eliminate allocation or routing obligations. Source: [framework sections 1 and 3](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/paper/framework.md).

## Exact score and certificate acceptance

With the algorithmic contract established, certify a rational `0 < a < 1` such that

`Ψ(1−a) = (1/W) Σ[r=1..m−1] n_r (r/m)^(1−a) < 1`.

The resulting tensor bound is `O(2^k (k+1)^(1−a))`. Under the stated Fourier compiler and all-length reduction, each fixed `0 < δ < a` gives `O(n (log n)^(1−δ))`; the positive gap absorbs the remaining log-log overhead. Acceptance inequalities are certified by rational bounds, rather than rounded decimal values. A passing moment alone is not an algorithm or a transfer proof. Source: [framework sections 2 and 4](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/paper/framework.md).

The selected Shea witness records `m=110`, `W=14692` per cover vertex, `358975` recursive children, maximum child width `46`, and weighted width sum `1613040 = 110×14692−3080`. Its reference certificate includes the physical histogram, provenance bindings and exact rate checks. The imported recursion engine also requires the finite-fill inequality

`(1−2^−40) Ψ(1−a) + 2^−40 [(109/110)^(1−a) + (1/110)^(1−a)] < 1`.

The recorded ordinary moment gap exceeds `8.05×10^−10` at its selected `a`. A larger value `a = 7547365/10^10` fails for that same histogram. This negative control is not an upper bound for different networks. Sources: [selected construction](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/results/five-stage-pr233.md), [reference certificate](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/verification/certificates/five_stage_reference.json).

The selected source-column Python check does not replay every dirty-input column. Its arbitrary-scratch conclusion depends on the imported formal invocation theorem's subtraction and cleanup argument. This distinction matters when comparing a new certificate with this result. Source: [five-stage audit](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/verification/FIVE_STAGE_AUDIT.md).

## Incorporation and formalization requirements

The project's update procedure requires pinned complete source witnesses and licenses, a new result record and verifier, a reconstructed physical histogram, exact rate and absorption checks, and explicit inherited and new proof obligations. Incomplete work remains a candidate. A written transfer with successful finite checks can be proposed. Formalized status additionally requires reproduction of the pinned Lean build, an axiom audit, theorem and definition comparisons, and retained receipts with hashed logs. Previous records and publication artifacts are preserved. Source: [update procedure](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/results/README.md).

The documented checks include `python3 verification/run_checks.py`, the selected finite verifier `python3 verification/verify_five_stage.py`, and a separate Lean reproduction command using `verification/verify_five_stage_lean.py`. The Python suite alone does not run Lean. Shea's audit explicitly distinguishes its reproduction from an independent proof kernel and independent human mathematical review. Sussman's stronger result also reports that line-by-line human review is pending and discloses that its official-comparator runs used a stand-in for the comparator sandbox. Sources: [Shea audit](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/verification/FIVE_STAGE_AUDIT.md), [Sussman verification guide](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/VERIFY.md).

## Comparison boundary

A future claim must distinguish an improvement over the named project's selected figure from an improvement over the strongest comparable published figure found at that later time. This lookup found a stronger published comparator, but did not exhaust current repositories and proposals or independently verify their proofs.

Fixed-size exact DFT factorizations can be useful ingredients. To support this particular asymptotic claim, they still need a scalable construction meeting the tensor interface, charged exact coefficient preparation, arbitrary-scratch correctness, a physical call histogram, and the certified transfer. Isolated existence of constants is not by itself a constructive preparation procedure. A savings claim based only on parameter count, a subset of output rows, or a few finite dimensions therefore remains outside this comparison until those obligations are discharged.

This report records a completed source lookup. No new search experiment, proof reproduction, benchmark execution, or external repository modification was performed for it.
