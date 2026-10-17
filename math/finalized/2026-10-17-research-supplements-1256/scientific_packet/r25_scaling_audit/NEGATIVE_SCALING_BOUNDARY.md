# Exact boundary for future R25-style searches

## Proven restriction

For `N=2^g`, partition the same unpruned classical DIT computation into any positive block lengths `q_1,...,q_c` summing to `g`. Use R25's preweights and the ordinary radix-two local codelet, skipping unit multipliers. Do not change the computation inside the blocks.

Then the online residue-payload operations are exactly

`A(N)=Ng`,

`M(N)=Ng/2−N+1`,

independent of every block cut and reduction placement. Boundary reductions cost `N(c+1)` including input normalization; immediate product reductions add `M(N)`.

The proof is the per-group identity

`M_group=Nq_i/2−N/h_i+N/h_(i+1)`, with `h_(i+1)=2^q_i h_i`,

which telescopes, and `A_group=Nq_i`. Thus this execution cannot be `o(N log N)` in a scalar model charging its additions. Boundary-only reduction does not remove operations by leaving them unreduced.

This applies to fixed, increasing, nonuniform, or adaptively chosen block cuts whenever the execution still performs the same complete codelet graph. It applies to a hypothetical uncapped generator as well as the actual capped prototype. It does not assert a lower bound for arbitrary algorithms computing the same Fourier map.

## Do not reopen as an asymptotic lead

Absent a changed circuit, these modifications alone cannot clear the target:

- Increase q or B; rename several levels as one stage.
- Move or defer modulo operations; count only remainder operations.
- Generate or unroll the same expressions; reduce array passes or dispatch overhead.
- Pack wider intermediate integers but omit their bit cost.
- Report prepared timings while omitting cold regressions, planning, or field/root costs.
- Extrapolate a fitted exponent from a finite range or a fixed field's finite root orders.

These may still be useful engineering experiments. Keep their objective and measurements separate from an arithmetic-complexity claim.

## Reopening gate

A genuinely new candidate must identify what changes in the operation graph and show a complete charged construction rather than merely fewer block boundaries. Before expensive benchmarking, require:

1. A distinct local or global circuit and an all-input exact transform identity, including every required output, input/output permutations, and any normalization.
2. A count of all variable-dependent additions, multiplications, reductions and conversions; constants, coefficient generation, storage and planning separately accounted for. Saving multiplications while retaining exactly `Ng` charged additions still does not prove a sub-`N log N` total.
3. A specified asymptotic field/root family and arithmetic/bit model, with intermediate widths and construction costs. Fixed `p=998244353` cannot supply an infinite length family.
4. A recurrence or direct total-work bound showing the required improvement after all overheads, rather than a local-stage label or isolated operation category.
5. Independent correctness tests with explicit failures and separately written oracles, followed by complete, reproducible performance comparisons if practical speed is also claimed.

No claim is made that satisfying this gate is easy, that a global Fourier lower bound exists, or that every different architecture must use the same kind of blocks. The stopping condition for the present idea is established: **larger cuts of the unchanged R25 graph have been excluded as an arithmetic-exponent improvement**.

## Finite empirical boundary

- Completed main timings stop at `N=65,536`; `N=262,144` timing was interrupted at the command level, with no retained performance result.
- The largest reported exact suite reaches `N=262,144` for q=4 boundary, q=6 boundary, q=4 products, and growing q=5 boundary. It does not establish q=8 at that endpoint.
- Author-reported q=8 widths at `N=65,536` reach 266 magnitude bits under a 278-bit conservative ceiling. Those measurements were not rerun in the clean replay or this audit.
- Prepared q=8 improvements and cold regressions coexist. There is no general replacement rule for R24 and no independent hardware/library superiority result.
