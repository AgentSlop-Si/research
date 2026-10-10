# Source 40: run_experiments.py

SHA-256: `0e7b5c0aa8319b229c7c0084e81803a4c90b2b8be7d52f0505962234c15ceadd`

Path: `additions/2115/multistage/extracted/fft_three_tap_multistage_gate_2026-10-10(1)/fft_local_annihilator_gate_2026-10-10/run_experiments.py`

All 68 lines (3,340 bytes) were read. Source execution/import/compile/AST parsing: none.

## Role

Local-annihilator experiment generator

## Complete logic review

Lines 6-28 collect seven finite two-stage witnesses and 76 layout/width entries. Lines 30-39 additionally and unconditionally produce bitrev_all_widths for N=16/32/64. Lines 41-60 collect six random-layout sampling records and three explicit three-stage rank checks, then write EXPERIMENT_RESULTS.json.

## Guards and domain

Fixed cases and seeds reproduce a bounded exploration. Top-level loops execute on import. A sampled layout fraction is not a probability theorem and a no-violation result is not factorization existence.

## Charged costs

Repeated quadratic window-pair scans with O(W log W) each, further summed over all widths in the added sweep; has a coarse O(N^4 log N) bound. Exact Fourier probes are dense; no linear-time exploration claim.

## Findings and evidence limits

ACTUAL SAVED-EVIDENCE GAP: archived EXPERIMENT_RESULTS.json lacks bitrev_all_widths despite this source unconditionally generating it. Both exact source and output hashes match the co-packaged SHA manifest. The JSON cannot be the complete unmodified output of this source version. Existing seven witnesses/76 entries/six samples/three ranks are retained, but no archived evidence for the added all-width sweep is credited.

## Exact dependencies

- annihilator_gate: 9d9c07569db82c4f55755a96b4af4ca471846b3d5b47a06b672fc1a725d20bc5 (adjacent/package-parent literal file; runtime import not performed)
- hashlib: standard-library/external dependency; no source version pinned here
- json: standard-library/external dependency; no source version pinned here
- random: standard-library/external dependency; no source version pinned here

## Preserved stored evidence

- `evidence/103_EXPERIMENT_RESULTS.json` SHA-256 `ebd11b3a8840d64e402bef46a318009cb22c37a2ca3aa6a4d0e82ea00b0302b1` (original `fft_research_master_20261009/additions/2115/multistage/extracted/fft_three_tap_multistage_gate_2026-10-10(1)/fft_local_annihilator_gate_2026-10-10/EXPERIMENT_RESULTS.json`)
- `evidence/104_EXPERIMENT_RUN_LOG.txt` SHA-256 `a1d41da1b0b9f46ba8acd1ac944b61bd071c63f74fa20240d6086af5be4cba22` (original `fft_research_master_20261009/additions/2115/multistage/extracted/fft_three_tap_multistage_gate_2026-10-10(1)/fft_local_annihilator_gate_2026-10-10/EXPERIMENT_RUN_LOG.txt`)
- `evidence/112_SHA256SUMS.txt` SHA-256 `236e5c81be10bb947566d9febce4ba3683f0958e9238a9c3241a20cf702f9b67` (original `fft_research_master_20261009/additions/2115/multistage/extracted/fft_three_tap_multistage_gate_2026-10-10(1)/fft_local_annihilator_gate_2026-10-10/SHA256SUMS.txt`)

Static source coverage is not theorem acceptance, successful current execution, provenance proof of a historical run, full dependency closure, or completion of all research checks.
