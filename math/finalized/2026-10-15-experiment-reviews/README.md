# Finalized bounded experiments and independent corrections

2026-10-15. These are scoped mathematical/implementation reviews, not a faster general FFT or integer-multiplication result.

## Exact Mersenne-prime-power route

Read mersenne_independent_finalization/FINAL_REPORT.md and REVIEW.md first. The requested radix is Q=p^d with p=2^m-1 prime. Exact grouped folding is correct. Clean comparisons show that this particular folding implementation is slower end-to-end than the matched binary baseline; a native-divmod conversion using the same Q is much closer. Original diagnostic ledgers are incomplete bit-work ledgers, as the review explains. Original REPORT.md is preserved as historical evidence; the independent FINAL_REPORT.md corrects its wording.

## Ancillary Newton follow-ons

Read newton_followon_independent_finalization/REPORT.md and VERDICTS.json. Block-carried normalization and valuation-adaptive scalar identities are accepted at their stated scopes. A generated interval schedule repairs control storage; separately repaired precision primitives implement the stated short-by-long costs. Original producer files remain unchanged; corrected versions are separate. No fast multiplier admission follows and these ancillary lanes do not substitute for the Mersenne-prime-power route.

## Reproduction and provenance

Source directories retain their relative paths, including the Newton review's required `rerun/` copies and the Mersenne review's frozen `source_snapshot/`. Test scripts and saved raw results are included; inspect individual reports for commands and test scope. The scripts use the Python standard library. Run them with assertions enabled, preferably on a disposable copy of this archive because test programs rewrite their result files. The original review commands treat this directory as the workspace root. For the block original-suite rerun, change into `newton_followon_independent_finalization/rerun/` first, then run `python block_carried_newton_tree/test_blocks.py`.

`MANIFEST.json` hashes every other file in this publication directory. `PACKAGING_VERIFICATION.json` records byte-identical source comparisons, nested-manifest checks, Python syntax checks and isolated import/source-loading checks. This packaging audit did not rerun the numerical suites or benchmarks. `mersenne_independent_finalization/reproduced/BENCHMARK_PARTIAL.json` is preserved to satisfy the original finalization hash manifest; it is a historical checkpoint, not a completed experimental result.

`TABLE_SYNC_RECEIPT.json` records the separately verified application of five previously accepted closures to the research table. Its synchronization counts are not additional mathematical results. Statements in preserved review reports that no external files changed describe those review runs, before this later synchronization and publication. Internal independent reviews are project reviews, not journal acceptance or proof-assistant verification.
