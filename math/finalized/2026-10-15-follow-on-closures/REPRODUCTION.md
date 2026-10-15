# Reproduction and provenance

## Integrity

Run from this directory with Python 3.8 or later:

    python -I -S verify_package.py

The standard-library verifier checks every listed file's SHA-256 and byte count, the manifest hash in `SHA256SUMS`, and the absence of unexpected payload files. The manifest and checksums are integrity evidence, not a theorem proof or publication receipt.

## Small scientific controls

No third-party Python packages or network access are required. The scripts below write their outputs beside themselves, except the conditional decimal checker, which prints JSON to standard output. Run in a copy if retaining a pristine package is important.

    python -I -S checks/alg045/check_orientation.py
    python -I -S checks/sorting/check_sorting_rank.py
    python -I -S checks/independent/independent_checks.py
    python -I -S checks/f4_replay/checks/replay_f4_accepted_checker.py
    python -I -S checks/interval/check_recorded_banach_numbers.py

- **ALG-045 orientation controls:** five exact finite-field cases compare P, P-transpose and Q actions; the N=8, GF(17) example disproves the unqualified P-orientation wording. The general proof and required Q/P-transpose orientations are in the supplement and historical acceptance. Bounded controls alone are not the all-size proof.
- **Sorting controls:** 8,188 complete binary words, 3,076 word/stride cases and 588 direct ranks over characteristics 2, 3 and 5. Exact histograms, rational moments and small-N clipping are checked. The all-size theorem remains analytic.
- **Independent review controls:** seven mixed-radix bank/action cases, 2,044 stable-sort words, 16,388 word/stride cases, 35 exact rational Gram evaluations and ten half-grid exception controls. This is independently authored code, not an execution of historical source programs.
- **F4 certificate replay:** the isolated characteristic-zero subset of the accepted REVIEW-09 checker verifies all eight two-sided inverses, denominators as units in the rational quadratic tower, both stage sums, the negative-sign F4 product, rook support, nonconstant identity-branch weights and twelve zero masks. Its exact original certificate has SHA256 `a8dc28b9b33c5df50e40cd120ea645a0e803ea0193d1cedad93b639b8731238b`. Reusing this accepted checker is a replay, not another independently authored checker. It does not replay unrelated experimental suites or prove a global lift.
- **Interval decimal consistency only:** exact rational arithmetic checks recorded eta/q/radius thresholds. It does **not** verify an original interval certificate, actual enclosures, a root or guard conditions. The source gate stays open.

`CHECK_RUN_RECEIPT.json` identifies the scripts and outputs actually rerun during package verification. Reproduced output bytes match the supplied records; numeric counts remain bounded controls. Historical larger enumerations, root certificates, normalizer runs and bank experiments are not silently counted as newly executed.

## Original versus public-export identity

The mathematical source files for ALG-045, the gauge theorem and the sorting theorem are unchanged original bytes. Exact historical outcome files and the original Phase16 review are also retained. Full original review JSON files can cover other records; their presence grants no additional closure decision beyond the four named records in this package.

The historical bank-certificate review is shared by ALG-045 and M-FOURIER4-GREEN. Original SHA256 `dd4adebbde308f21a3fa5167fe211e689201c37b65b50ebb2207e33f305f6a35` and public-export SHA256 `4e2814967fad317b59c8c52ccdaf43158ba40f8ca407c8fbbf19c8e65af17e7e` are distinct. The verified 18-byte export change removes one local workspace prefix and changes no mathematical text. Only the already-published export is included here.

The prior closure addendum similarly has original SHA256 `e6ca03e99a2c1d39cc48d43aafe9a1528c7639f5a011c685f5026a5bf01e95a3` and published export SHA256 `c7720ce006451e8b13021a69255186b1e0eca1b6ff95e9a72539b208a75082b7`. The public index identifies it as a redacted export. No byte equality with the original is claimed.

The STABLE-ARC editorial-review derivative has its own recovered/export hash. Its missing original report and manuscript hashes remain source pins, not recovered proof bytes. The packaging pass does not reconstruct either missing item.

The ALG-045 exposition and current independent-review scientific excerpt are publication derivatives with explicit input/output hashes and textual transformations in `PUBLIC_PROVENANCE.json`. The exact independent public verdict is unchanged. The interval source-audit export removes only a Library identifier and local receipt filenames. None of these presentation changes alters a mathematical acceptance or source hold.

Legacy filenames mentioned inside unchanged historical sources identify their original source context. They should not be interpreted as promises that every old appendix or archive is present in this compact package.
