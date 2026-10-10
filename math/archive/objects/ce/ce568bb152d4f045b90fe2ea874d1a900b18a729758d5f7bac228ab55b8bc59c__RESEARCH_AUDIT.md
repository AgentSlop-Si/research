# Source audit and novelty register (October 10, 2026)

**Method:** inspected prior theorem checkpoints and recent canonical reports, then scanned all `.md`, `.txt`, and `.py` entries from accessible top-level archives for overlaps. Archive-member counts include repeated nested copies. This is not a line-by-line independent formal review of 3,000+ source files.

## Material inventory

| Accessible ZIP | Members | Selected relevance |
|---|---:|---|
| `fft_all_research_fusion_20261009.zip` | 29 | Haar/Green fusion and correction audits |
| `fft_divisor_spectrum_v13(1).zip` | 22 | Approximate divisor-spectrum and novelty caveats |
| `fft_green_research_phase22_2026-10-09.zip` | 15 | Weyl and Gram restrictions |
| `fft_green_research_phase26_2026-10-10.zip` | 17 | Restricted affine-run Green multi-stage cuts; requires phase-correct non-affine candidates |
| `fft_hero0_phase2_composite_green_2026-10-09.zip` | 24 | Approximate composite-length Green/sampling approach |
| `fft_hero17_tensor_fiber_graph_union_2026-10-10.zip` | 18 | O(N) exact structured-input fiber algorithms, not worst-case arbitrary |
| `fft_hero1_mixedradix_v13_20261010.zip` | 27 | Exact phase-bank identity, no joint sub-NlogN evaluator |
| `fft_offset_class_joint_v12.zip` | 19 | Offset-class joint scan sharing; full gate cost still unproved |
| `fft_phase23_window_verified_1825.zip` | 56 | Real-resolvent/window-rank verification and scoped barriers |
| `fft_phase24_sorting_verified_1845.zip` | 51 | Ordering/shift-defect barrier and independent audit |
| `fft_research_master_20261009.zip` | 3532 | Master checkpoint; collision, reuse, Green/Weyl, global scan, no-go, phase24 and proof history |
| `fft_sparse_defect_green_gate_2026-10-10.zip` | 14 | Sparse-inverse plus low-rank defects; rank obstructions and non-sparse inverse escape |

**Top-level ZIP members counted:** 3824 (including duplicate/nested source material).

## Earlier local theorem packages reviewed

- `fft_prime_spark_hybrid_20261010/THEOREM.md` — row-sparse preconditioner + additive separated-rank prime Fourier restriction; bridge polynomial gate.
- `fft_new_exact_theory/THEOREM.md` — simultaneous row/column separation for additive Green sums; *not* product-of-sums.
- `fft_new_theory/THEOREM.md` — randomized approximate Word-RAM path; weaker additive accuracy contract.
- Earlier cycle-uncertainty and theoretical-gate notes — special sparse-sandwich obstructions.

## Textual overlap checks

Keyword searches in directly readable members (including duplicates) found no `twirl` or `Hutchinson` terms. Many files do contain Weyl covariance, graph cuts, and Fourier full-spark work. This does **not** rule out synonymous formulations in the project or outside literature.

## Novelty verdict

The Weyl-twirl identity is standard mathematics; the project-specific O(N)-probe phase certificate and its fusion with Green cycle expansion may be a useful new workflow, but publication-level novelty is **not established**. Structural cut ranks have extensive prior art. No exact O(N) FFT construction was found or proved.

## Essential non-repetition guardrails

- Do not treat `A*B=(A-k)*B+k*B`, packing, caching, known updates, or threads as worst-case fresh-input FFT progress.
- Do not count only the number of Green resolvents without coefficient generation, phase fidelity, scalar operations, and precision.
- Do not confuse a graph mincut pass or a low Weyl-loss numerical sample with exact Fourier equality.
- Do not treat approximate ℓ_inf error scaled by `||x||_1/sqrt(N)` as exact or strong relative ℓ_2 accuracy.
- Any Fourier factorization target must handle a growing family of N, not only N8 or N16.
