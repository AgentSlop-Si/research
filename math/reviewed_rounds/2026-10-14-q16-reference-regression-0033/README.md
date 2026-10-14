# Q16 bounded reference regression: publication-safe edition

Verdict: **ACCEPT_NEW_REFERENCE_REGRESSION_ONLY**.

This is a same-agent reference/oracle experiment, not independent-agent review and not production outer-wrapper acceptance. A separate author has not independently reviewed this new source.

The new reference and a separately implemented B=900 exact enclosure oracle evaluated three coefficients at D=5, m=57, N=2^55-1, M=2^57, odd s=285. The zero-limit, negative-ratio and minimum-residue branches pass exact enclosure/certificate checks. The minimum-residue absolute error is certified at most 2^-460, below eta=2^-456. Exactly 9123 bounded support incidences were enumerated; only three coefficients were evaluated. No asymptotic speed or full integration follows from this finite run.

## Static acceptance source

The companion static acceptance is preserved in the separately prepared 00:23 research round:

- Repository-relative source: `../2026-10-14-reviewed-0023/q16_outer_contract/REVIEW.md`
- Static review SHA-256: `3bf51b058a64f94784d8c33abe3206b1d61aa5810be97adaf0d4c2cd6407ce63`
- Original static-review manifest SHA-256: `638994dd26876d73a878086b5e482250952db0fbf7e8a4ee121c5367c00ff117`
- Exact recovered candidate SHA-256: `0c7f8c8c4eedf4a4f6e332e429c4a785c02c952ba1ffe4c87a51537b00f502bc`

These bindings identify the source even before the companion publication finishes. The static verdict covers incidence, signed powers, fixed precision and paid arithmetic bounds. It is separate from this finite regression.

## Production gap

The experiment has not executed a source-pinned production outer wrapper or bound its input through the accepted sparse-output adapter. Independent source/ledger review, actual production API binding, all required malformed-input/negative controls and a source-pinned production replay remain open. Full-stream scatter, accumulation, scale-back, dense fallback, all-length dispatch and amplification are also separate gates. The 32-byte fixture label is not proof of production provenance.

## Exact scientific evidence and publication projection

REPORT.md describes the mathematical experiment. RESULTS.json preserves exact enclosures, squared-error certificates and paid ledgers. The evaluator, bounded launcher, outputs and execution receipt are copied byte-for-byte from the sealed source. The execution receipt records exit 0, empty stderr, unchanged evaluator hash and a 180-second cap. The experiment was not rerun during preservation.

Documentation and status are explicitly projected for publication. This ZIP is not an original byte-preserved archive. ORIGINAL_SOURCE_MANIFEST.json and ORIGINAL_SOURCE_SEAL.json preserve the original manifest/seal bytes; their documentation hashes describe the untouched original edition, not these edited documents. PUBLICATION_PROJECTION.json maps original and published hashes. The new MANIFEST.json and SEAL.json authenticate this publication edition.

UTC experiment interval: 2026-10-14 00:24:22 to 00:31:34, 7 minutes 12 seconds of wall time. Actual token counts are unknown.
