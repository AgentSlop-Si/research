# Fourier research supplement: 17:42 batch

Independent audit and bounded mathematical extensions, 9 October 2026.

Start with `THREE_LATEST_AUDIT.md`. Append `CHECKPOINT_ADDITION.md` to the preceding master while preserving its full residual systems, chart exceptions and exact/approximate distinctions. This supplement is suitable for the master's `additions/1742/` folder.

## Main reports

- `phase21_audit/PHASE21_AUDIT.md`: exact Weyl–Green identities, independently reconstructed finite Prony certificates, stronger spectral floor and cut-crossing extension.
- `prony_extension/PROOF_OR_OBSTRUCTION.md`: uniform h-or-h+1 pole bound for every even N=2h, with a finite valid-parameter construction.
- `v11_audit/V11_AUDIT.md`: streamed Bessel fusion, sharper H=0 bias, reduced-channel information rank and the frozen-block rational-Taylor variant.
- `v11_audit/FP_CONTRACT_REVIEW.md`: missing fused-summary interface, sufficient explicit rounding ledger and charged coefficient preparation.
- `SOURCE_PROVENANCE.md`: exact archive identities and byte comparison against the declared source union through17:17.
- `attachment_recheck/RECHECK_RESULT.json`: exact-ID fresh-retrieval confirmation of the triple-intersection source comparison.
- `PRIMARY_REFERENCES.md`: checked attribution for classical ingredients.
- `VERIFICATION.json` and `AUDIT_ENVIRONMENT.json`: verified scopes and reproduction environment.

## Reproduce the independent checks

Use Python3 with NumPy, SymPy and mpmath. From this folder:

```sh
python3 audit_provenance.py
(cd phase21_audit && OPENBLAS_NUM_THREADS=1 python3 independent_checks.py)
(cd prony_extension && OPENBLAS_NUM_THREADS=1 python3 independent_checks.py)
(cd v11_audit && OPENBLAS_NUM_THREADS=1 python3 independent_v11_checks.py)
```

These are independently authored audit runners. They do not import, execute or invoke the programs preserved under `extracted/`. Source Python, test logs, bytecode and nested archives are inert evidence. Source benchmark timings are not reproduced or claimed as independent results.

The runners rewrite their result JSON files; timing fields can differ on a rerun without changing the mathematics. Exact modular checks and universal proofs have different scopes, and floating controls are corroboration rather than exact symbolic or production-implementation certificates.

`SHA256SUMS.txt` seals the delivered bytes. Verify it before rerunning generators:

```sh
sha256sum -c SHA256SUMS.txt
```

This supplement does not establish an unrestricted exact sub-N-log-N transform, a shared-runtime lower bound, or publication priority. It does preserve a uniform positive representation result, stronger restricted barriers and explicit approximate numerical obligations.
