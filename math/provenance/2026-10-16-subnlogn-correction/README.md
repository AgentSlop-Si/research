# Sub-N-log-N checkpoint attribution correction

**Effective date: 16 October 2026. This is a provenance correction, not a new algorithm release.**

## Decision and scope

The four matched headline mechanisms from v12 and the sharp-recurrence v13 are reclassified as **attributed reproductions/integrations of prior work**, excluded from original-discovery counts and the original-research queue. The matching source is `CrocSwap/integer-mult-bounds`; the underlying framework and primitives remain attributed to the pinned OpenAI preprint and its cited predecessors.

This notice supersedes originality framing in the affected checkpoint reports and associated assistant explanations. It does not delete historical files, change arithmetic, invalidate a result merely because it was rediscovered, or reclassify unrelated project research. Originality, correctness, implementation coverage, and performance are separate review questions.

## Claim register

| ID | Local claim | Corrected status | Evidence |
|---|---|---|---|
| C01 | v12 direct nonadjacent axis schedules and revised layout margin | Reproduced prior art | S1 |
| C02 | v13 sharper recurrence with K retained explicitly | Reproduced prior art | S2, S3 |
| C03 | v13 use of original bit-network h=46 | Previously used network choice | S1 |
| C04 | v13 independent complex h=25 optimum, logarithm bounds and infinite-tail certificate | Reproduced prior art | S3 |
| C05 | Other v13: specific dependency-path guard Delta=32*d^2 | Novelty unverified; not credited as original | Separate review required |
| C06 | Other v13: restricted fixed-width swap-schedule minimum | Novelty unverified; scoped diagnostic only | Separate review required |
| C07 | Improved ratios between local conditional kappa certificates | Local metric, not discovery or measured speedup | Preserve as historical, branch-specific accounting |

S1 supplies the same mirror-pair reversal and expose/process/restore schedules, with the same changed layout margin. S2 supplies the same explicit-K geometric recurrence argument. S3 documents the h=25 complex-family optimum and the independence of bit and complex arities, with exact bounds covering the infinite tail. The historical commits below precede the 16 October local checkpoint dates; they are evidence of earlier availability, not a claim to have found the first appearance anywhere.

## Pinned attribution

**S1 — `docs/nonadjacent-axis-audit.md`**  
Repository: `CrocSwap/integer-mult-bounds`. Commit `52ce3beef6f01103431fbc0b736dacca8dafadbe`, 2026-10-07T13:35:44Z. Blob `5982be581a435bdb8d865013b37fede26e91fb5a`. [Read pinned source](https://github.com/CrocSwap/integer-mult-bounds/blob/52ce3beef6f01103431fbc0b736dacca8dafadbe/docs/nonadjacent-axis-audit.md).

**S2 — `docs/packed-movement-audit.md`**  
Repository: `CrocSwap/integer-mult-bounds`. Commit `bcd4ebde8692383539f8a48734e5fbf3a18a32c2`, 2026-10-07T19:27:07Z. Blob `cd3ae564310f194d49c118a13e06e91d0aad78c9`. [Read pinned source](https://github.com/CrocSwap/integer-mult-bounds/blob/bcd4ebde8692383539f8a48734e5fbf3a18a32c2/docs/packed-movement-audit.md).

**S3 — `docs/research/layer-preparation.md`**  
Repository: `CrocSwap/integer-mult-bounds`. Commit `6e564879f51ae16f23d392e9e196c605f36d90df`, 2026-10-08T00:27:54Z. Blob `3d416e361ad05b7e23fe59b7283e971e9ef3bbb0`. [Read pinned source](https://github.com/CrocSwap/integer-mult-bounds/blob/6e564879f51ae16f23d392e9e196c605f36d90df/docs/research/layer-preparation.md).

Credit the source project's documented authors and contributors. The nonadjacent audit credits Douglas Colkitt, with OpenAI Codex assistance. The inspected commits are attributed to Douglas Colkitt. This is not an assertion that one person originated every dependency. Existing licenses, notices, and source credits remain in the preserved archives; no new blanket license is assigned.

## Keep the two v13 branches separate

`subnlogn_research_checkpoint_v13_sharp_recurrence_2026-10-16.zip` and `subnlogn_research_checkpoint_v13_dag_guard_2026-10-16.zip` are different artifacts. Both contain files called `README_V13.md`, `AUDIT_V13.md` and `parameter_certificate_v13.json`. Those names are not unique identifiers. Use the branch-qualified ZIP name plus its SHA-256. Do not overwrite one with the other, merge their certificates, add their validation counts, or assume their gains compose.

The standalone `subnlogn_AUDIT_V13_2026-10-16.md` and validation filename were reused in the conversation. They cannot safely identify both branches. The byte-preserved ZIPs, not an ambiguous display name, determine each branch's evidence.

The guard branch is not automatically a rediscovery simply because the sharp-recurrence branch is. This correction has not established a direct prior-art match for its specific 32*d^2 proof. It has also not established that proof's originality or independently verified its complete integration. Its discovery credit remains zero pending that work.

## What remains usable

Retain the exact code, tests, local parameter calculations, written arguments, and historical measurements as reproduction and integration material. Historical test logs are not fresh test results from this correction. A passing finite test does not prove an all-size machine bound. N means integer input bit length in these checkpoints; none is reclassified as a faster arbitrary-input complex DFT.

Claims of a 23-billion-fold, 1,046-fold, or 2.5-fold increase in a local exponent saving are not measurements of execution speed or demonstrations of novelty. This correction neither recomputes nor combines those certificates. No standalone independently established sub-N-log-N multiplier or new global lower bound is asserted here.

## Admission rule for subsequent research

These four reproduced mechanisms are baseline/reference work only, not targets to rediscover or optimize under a new label. Do not import CrocSwap/Swapnil network refinements and count them as original project results. A candidate for the distinct project research track must identify its exact new mathematical step relative to pinned prior work, state its computational model and input scope, give a complete charged recurrence (including movement, precision, setup and output), and separate proof from finite validation. Unknown novelty stays unknown; absence of a search match is not proof of originality.

No new original candidate is promoted by this correction. No claim is made that all GitHub research, all historical catalogue entries, or every external source has been audited. The machine-readable register `CLAIMS.json` gives the seven bounded decisions and sets `count_as_original_discovery` to false for every one.

## Preservation and verification

The downloadable correction bundle preserves the 14 uploaded checkpoint ZIPs byte-for-byte, together with SHA-256 hashes and per-member manifests. It includes this notice, branch-specific status notes, the claim register, and a verification script. No supplied research code is executed by the integrity verifier. GitHub receives the correction documentation and register; the original ZIP payloads are retained in the downloadable bundle, not newly uploaded to the repository by this action.
