# Exact minimum of eight signed magnetic banks at length seven

10 October 2026 at 13:20 UTC. Bounded mathematical follow-up.

The negative Fourier matrix of length seven has exact minimum **eight** in the stated signed magnetic-resolvent bank grammar over the complex numbers. The conclusion combines two separately hash-scoped accepted results:

- The [lower-bound proof](notes/01_lower_bound.md) requires at least four banks of each delta sign, hence at least eight in total, over every characteristic-zero extension field containing a primitive seventh root.
- The [upper-bound proof and construction](notes/02_upper_bound.md) supplies eight legal banks over the splitting field of an explicit separable cubic over Q(q). Its orientation counts are (3,1,1,3) in (++,-+,+-,--) order, with beta=1 in every bank.

Consequently the minimum is also eight over that splitting field and fields containing it. Attainment using parameters restricted to Q(q) itself is not established here. This is a count of whole phase-weighted banks in this precise representation grammar; it is not an arithmetic runtime or FFT lower bound, a speedup claim, a historical-priority claim, or a classification of every eight-bank realization.

## What closes the gap

The lower proof isolates two coefficient rows that receive no contribution from banks of the opposite delta sign. It derives two necessary degree-nine polynomials and verifies the exact identity U R + V F = 1 over Q(q). The argument includes zero or repeated forward nodes, vanishing amplitudes and D=0; literal symmetries, unique corner supports and legal zero padding cover every smaller orientation count. A separate good-reduction check has resultant 24 and quotient norm 19 modulo 29.

The upper construction uses a separable cubic algebra to specify every amplitude exactly and to sum its three root banks by the algebra trace. All 56 literal phase-resolvent branches are checked, including both inverse products, and all 49 original Fourier matrix entries agree exactly. The row ranks are (7,5,7,7,7,7,5); the two deficient rows are verified consistent rather than inferred from their ranks. Existence is proved in characteristic zero, without lifting a finite-field point.

## Exact files and reproduction

- [Lower exact controls and data](controls/lower/README.md)
- [Upper exact controls and data](controls/upper/README.md)
- [Lower acceptance](receipts/lower_acceptance.json) and [upper acceptance](receipts/upper_acceptance.json)
- [Accepted sources and public transformations](SOURCE_ACCEPTANCE.json)
- [Precise proof scope](PROOF_STATUS.json) and [remaining qualifications](PENDING_SCOPES.json)
- [Dated supersession of the 13:10 open-case status](SUPERSESSION.md)
- [Artifact manifest](ARTIFACT_MANIFEST.json) and [SHA-256 checksums](SHA256SUMS)

The included executable files are benign independent verification controls. Run them only in a disposable copy, since they regenerate their result files. Author and predecessor programs, raw logs, private-service identifiers, chat records and publisher PDFs are excluded. Every earlier packet, including the historical 13:10 partial N7 result, is preserved unchanged. This packet stops with the current lower/upper pair.
