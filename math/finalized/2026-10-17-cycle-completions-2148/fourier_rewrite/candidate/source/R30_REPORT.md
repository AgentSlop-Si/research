# R30 — graph workbench and a guarded cross-operator fusion

18 October 2026.

## Bottom line

We do not need to invent a new data representation to "move to graph": R29
already records a logical arithmetic graph for register reuse. R30 decodes that
actual bytecode back to one node per value, audits exact common subexpressions,
and adds a guarded algebraic rewrite across a tensor/Green/tensor-inverse window.

No new FFT speedup or sub-N-log-N exponent is established. This round has no
wall-clock benchmark. The successful fusion is a deliberately constructed
eligible operator window, not an occurrence shown in a complete Fourier program.

## What the audit found

All 54 R29 programs at dimensions 0..8, three modes and both directions, export
exactly to the expected logical graph. Full symbolic comparisons after structural
CSE preserve every output. No addition computes a normalized linear form already
available elsewhere in the same leaf, even allowing sign/power-of-two equivalence.
This is not proof of minimum additions, but rules out simple duplicate-result
reuse as a source of immediate arithmetic savings in those leaves.

## What was fused

The implemented pattern is

    C tensor -> (I-3 Z_v)^(-1) -> inverse C tensor

where Z_v is a specified parity-sign diagonal. On selected axes S the whole
operator equals

    -(I+3 M_v)/8,
    (M_v x)_j = (-i)^popcount(v&S) (-1)^popcount(v&j) x_(j xor (v&S)).

This is a classical conjugation identity. It joins the existing R29 C tensor
with R23's legal weighted-permutation Green operator model. The denominators
are nonsingular. The rule is input-independent, not answer caching. Unknown
masks, rounding barriers, mismatched axes/directions, and externally observed
intermediate results are not erased.

At 256 coefficient positions and eight selected axes, the full unfused sandwich
uses 7168 real additions; the fused graph uses 1024. The other operation counts
are reported in PROOF.md and validation_fusion.json, not hidden. This removes
whole tensor passes for this operator, rather than merely recycling their storage.

## What it does NOT prove

The resulting matrix has at most two entries per row. It is not Fourier. No full
sandwich occurs inside one R29 leaf, and no new cyclic DFT factorization using
these windows is supplied. Ordinary Fourier phase masks eta^j have full Walsh
support, as proved and checked, and cannot be treated as one parity term.
Thus the positive example does not justify calling a complete FFT linear-time.

The next graph-level question is whether an actual Fourier construction admits
many legal cross-operator cancellations or a jointly evaluated structure with
less TOTAL arithmetic. Repeating already excluded same-shift filters or merely
increasing a codelet width is not counted as a new solution.

## Evidence

- 54 real bytecode exports and exact graph-CSE map checks.
- 420 complete symbolic rewrite identities.
- 4416 rational vector comparisons (including basis cases).
- 12 larger checked-grid comparisons through 1024 complex positions, and four
  checks through the original R29 bit-word arena.
- Exact counts, invalid/overflow/division/mutation controls, and ten full-support
  phase controls.

All checks are author-side and reproducible. Dense symbolic audit costs are
paid offline and are not claimed to be sub-N-log-N coefficient preparation.
The R29 archive is preserved byte-for-byte under baseline_r29. No remote files
are changed. Classical compiler, Walsh, conjugation, and resolvent identities
retain attribution; no historical priority claim is made.
