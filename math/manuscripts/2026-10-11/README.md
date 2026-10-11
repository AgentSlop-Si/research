# Two reviewed working manuscripts — 11 October 2026

This research-only publication preserves the frozen manuscripts, editable sources, independent review reports and receipts, exact-control programs/results, and source-provenance manifests. The manuscripts have scoped internal mathematical acceptance. They are not journal-accepted papers, and historical priority remains unresolved.

## Read the manuscripts

- **Routed inverse sums:** [15-page PDF](routed/MANUSCRIPT.pdf), [Markdown](routed/MANUSCRIPT.md), [LaTeX](routed/MANUSCRIPT.tex), [independent review](routed/review/REVIEW.md), [review receipt](routed/review/RECEIPT.json).
- **Fourier endpoint minimax and deficit bounds:** [12-page PDF](endpoint/WORKING_MANUSCRIPT.pdf), [Markdown](endpoint/WORKING_MANUSCRIPT.md), [LaTeX](endpoint/WORKING_MANUSCRIPT.tex), [independent review](endpoint/review/REVIEW.md), [review receipt](endpoint/review/RECEIPT.json).

Both PDF/Markdown/LaTeX triples are exact copies of the frozen artifacts. Existing ranks remain ROUTED 4 and MINIMAX 5. No theorem, source conclusion, or ranking is changed here.

## Scope and provenance

The routed manuscript consolidates ordered common rectangles, the independently routed marked-separator theorem with guarded correction terms and fixed-branch error floors, and the separate exact-field column-two Fourier obstruction. The endpoint manuscript consolidates the cyclic-dyadic independent-endpoint minimax theorem, separate half-square minimum, and finite-abelian complex deficit rank and indexed norm bounds.

The source manifests and author seals are historical snapshots of the full author packets. Their source locators are provenance labels; this compact publication does not duplicate their larger source archives, page images, logs, or duplicate review snapshots. Consequently, those historical manifests describe more files than are distributed in this folder. The standalone manuscripts contain the proofs; their source hashes and bounded literature comparisons remain available for audit. Earlier author-side phrases saying independent review was pending are preserved unchanged and superseded by the separate, later review receipts.

[PROVENANCE.json](PROVENANCE.json) maps every copied artifact to its original locator, original SHA-256, and published SHA-256. It records fresh verification of all 30 source-copy bindings and the accepted receipt pins, plus exact agreement of both PDFs with the delivered and separately materialized copies. The routed review receipt is the sole metadata-normalized export: its internal reviewer locator was removed, every other JSON field was retained, and the original checksum is recorded. The endpoint receipt and both review reports are byte-for-byte unchanged. This export is not a new mathematical review.

The inherited exact-control results are accompanied by their original reviewer programs. They supplement the all-size proofs; finite tests do not establish universal claims. They were not rerun as part of publication. Build scripts are retained for editable-source use and may depend on a compatible Pandoc/TeX environment. A rebuild can differ bytewise from the accepted frozen PDF.

Raw third-party article bodies, provider metadata, private transfer identifiers, spreadsheet exports, and the failed Word rendering are excluded. No original file or existing repository path was edited.

## Integrity

Run `sha256sum -c SHA256SUMS.txt` from this folder. The checksum list covers every publication file except itself. `PUBLICATION_MANIFEST.json` is the explicit research-only allowlist, with byte counts, SHA-256 values, and Git blob identities for all data files and this README/provenance. The allowlist and checksum list are the only generated envelope files outside that list.
