# Second independently reviewed fixed-F11 continuation round

Date: 2026-10-10 UTC. This addendum preserves a narrow selection of research reports, mathematical certificates, fresh independent checker sources, and three frozen independent PASS receipts. It records bounded consequences on previously accepted guarded charts.

## Accepted scope and remaining questions

- **Regular H!=0, A=B=0 exception:** every retained solution satisfies the monic degree-10 condition F10(e)=0. The F10!=0 piece is excluded by the reviewed necessary-condition proof. The F10=0 locus remains unresolved and retains the complete original exception circuit and inputs (b,q,e). The decic condition alone is not sufficient.
- **Regular H=0 chart:** original E25 is equivalent to the 54-term remainder S(e,c,q), with degrees (2,4,3), on the accepted guarded domain. The division-free E41/E25 Sylvester determinant is identically zero modulo H. The verified necessary linear pseudo-remainder has 30 terms in each of L1 and L0. Reconstruction q=-L0/L1 is valid only on L1!=0; the complete L1=0 case remains with q retained, L0=0 required, and every original predicate. This determinant gives no nontrivial q-free condition or global q elimination.
- **Regular H!=0, A!=0 piece:** retained E25=0 is equivalent on this guarded piece to N2(b,e)=0 and core(b,e)=0, where N2=b^10 e^3 H core. N2 has 370 terms and multidegree (19,39); the core has 340 terms and multidegree (9,33). These are necessary conditions for the full circuit only. No new solved pivot is established. Nonaffinity of the stored core does not rule out other pivots, factors, eliminations, or solutions.

All 50 original residuals, all 19 original guards, accepted additional conditions, reconstruction definitions, and denominator/cancellation exclusions remain compulsory. The A=B=0 exception remains a separate piece; the generic-core calculation does not remove it. Optional-zero cases are preserved. The accepted historical charts and reconstruction theorems remain the explicitly stated trust boundary.

These results establish no fixed-F11 feasibility or infeasibility conclusion, dimension theorem, global two-input theorem, full Fourier factorization, general FFT improvement, ranking change, or novelty certification.

## Controlling independent acceptances

- [Affine-exception review](research_cycle_2328/f11_exception_review/REPORT.md) and [receipt](research_cycle_2328/f11_exception_review/RECEIPT.json): SHA-256 8938c0d67c13e630797439bd978199c2efdb7763bc591bbf9aaee7a8cadc4c29.
- [H=0 pseudo-remainder review](research_cycle_2332/f11_zero_pseudoremainder_review/REVIEW.md) and [receipt](research_cycle_2332/f11_zero_pseudoremainder_review/RECEIPT.json): SHA-256 832372ce6031a1dfb492d6befe1d8c9f76893d9250d87a92675c08cf8e0a832e.
- [Generic-core review](research_cycle_2333/f11_generic_core_review/REPORT.md) and [receipt](research_cycle_2333/f11_generic_core_review/RECEIPT.json): SHA-256 1be5c73ee149da836d24c2c42bae8fab34238d0a72db89790109b81fd2778b66.

Author-side files intentionally retain their earlier candidate/independent-review-required wording. These later receipts supersede that historical status only within their exact bounded accepted scopes. No original file is rewritten, and publication does not perform a new mathematical review.

## Selection and reproducibility boundary

[ALLOWLIST.json](ALLOWLIST.json) defines the entire publication: 27 byte-identical source files plus README.md, SOURCE_AUDIT.json, ALLOWLIST.json and SHA256SUMS. [SHA256SUMS](SHA256SUMS) hashes every included file other than itself. [SOURCE_AUDIT.json](SOURCE_AUDIT.json) records copied-file hashes, accepted receipts, locally checked source bindings, original manifest/seal hashes and explicitly omitted entries.

This is a **partial selection**, not a complete copy of the six original packets or their transitive dependency closure. Original receipt and certificate references to historical inputs, author parts, logs, seals and programs are retained as provenance; a reference or digest does not mean that its target is included here. In particular, the H=0 summary certificate references omitted DERIVATION.json and ELIMINATION.json, and the generic-core checker requires omitted author companions and seals. Original full-packet manifests are not repurposed as this selection's manifest.

The three independent checker sources are included for inspection. They need the exact pinned historical input tree and omitted packet files; this directory alone cannot replay the reviews. Original reproduction instructions describe that larger corpus. Do not run checkers in place expecting this subset to be self-contained: they write arithmetic result files, and a rerun changes runtime fields and requires resealing. This publication pass verifies bytes, receipt bindings, JSON parsing and checker syntax; it neither reruns the mathematical checkers nor revises proofs.

Excluded: private Sheet exports, readbacks, screenshots and update payloads; provider metadata; private chat or Library identifiers/URLs; credentials; third-party article bodies; archives; raw execution logs; and caches. Existing repository paths and the Sheet are outside this addendum's changes.
