# C10 prime-field costs and one common quadratic witness field

This inert delivery contains the complete accepted author v3 proof and contract, complete independent mathematical review and acceptance, recorded arithmetic-control results, and pinned preceding C10 proof evidence. It closes only the named prime-field root/representation/bit-cost obligation. The entire C10 owner remains open.

## Read the accepted result

1. [Author proof](author/REPORT.md), [exact contract](author/CANDIDATE_CONTRACT.json), and [input domain](author/INPUT_DOMAIN_FREEZE.json).
2. [Independent review](review/INDEPENDENT_REVIEW.md) and [exact acceptance](review/ACCEPTANCE.json). [Acceptance bindings](ACCEPTANCE_BINDINGS.json) connect these bytes to the exact author v3 manifest and review seal.
3. [Current scope and cost summary](SCOPE.json).
4. [Source map](provenance/SOURCE_MAP.json) resolves the complete preceding reduction review, complete sorting/sequential-2SAT proof and exact C10-only prior independent-review excerpt.
5. [Empty-input correction](history/V2_CORRECTION.md) and [existential/binary clarification](history/V3_CORRECTION.md), with exact inert report/JSON diff text in history/V2_DIFF.txt and history/V3_DIFF.txt.

Every selected system with canonical F_p input that is feasible over the algebraic closure has at least one solution in one common F_(p^2). This is an existence statement, not a claim that every closure solution lies in that field. The existing forest, sorting, sequential 2SAT and repair algorithm is unchanged.

The deterministic decision bound is D = O((N+M+1)(b^2+ell)+M b^3+M log2(M+1)(b+ell)), where b=ceil(log2(p+1)) and ell=ceil(log2(N+M+2)). The +1 includes empty-input overhead. The supplied-nonsquare witness surcharge is O(b^3+W(b^3+s^2 b^2)), with W<=min(N,M). For p=2 use s=0, no nonsquare and O(1+W) root work. Odd-prime nonsquare discovery is separately expected Las Vegas O(b^3), or an explicit deterministic O(p b^3) scan surcharge. Output includes the field descriptor and decision bit; normalized coordinates cost an additional O(N b^3).

These bounds use the specified charged record-random-access bit model. Prime validation, oversized input reduction and same-model concrete target preparation/extraction are not free. Columns, scales, legal Green integration, full factorization, Fourier runtime and whole-owner closure remain open. No historical novelty or arbitrary-field bit theorem is claimed.

## Lineage and historical wording

The author proof and contract retain their historical candidate/pending-review wording unchanged. The included later independent review and acceptance provide the final mathematical acceptance of those exact v3 bytes. The v1 fixed-cost omission was repaired in v2; v3 made the common-field assertion explicitly existential and the p=2 notation explicit. Earlier candidates are not promoted to accepted sources. Correction notes, exact report/JSON diffs and original identities preserve that history. The separately prepared reviewer proposal is superseded, non-authoritative and excluded.

The original preceding independent review covers three topics. Only its exact contiguous C10 section, lines 47-61, is distributed. Its full-source size, SHA-256, Git blob and immutable source URL remain pinned separately from the excerpt identity. No excerpt is called the complete original review.

## Safe export and identity qualifications

[Public allowlist](PUBLIC_ALLOWLIST.json) is the exact membership list. [Original/public identity ledger](provenance/ORIGINAL_PUBLIC_IDENTITIES.json) records all retained source identities and two narrowly projected predecessor-directory locators. Only those locator strings are substituted; every other byte in those two metadata files is unchanged. The projected files are clearly named .public.json and have their own hashes. They are not verbatim originals. Original source files remain unchanged privately.

[Historical inventories](provenance/HISTORICAL_INVENTORIES.json) qualify every entry in the original author v1/v2/v3 manifests and review seal. The complete original manifests/seal are retained unchanged as evidence, not as active package inventories. Their references to omitted programs, private snapshots, raw retrieval envelopes, superseded candidates or relocated copies do not assert those bodies are included. SOURCE_MAP.json is the active source-reading map; the root MANIFEST.json is the active payload hash inventory.

[Omissions](provenance/OMISSIONS.json) describes the boundary. No research/control program payloads, private native captures, raw connected-service envelopes, account/runtime identifiers or unsealed review drafts are included. Diff files contain only inert changes to mathematical prose and JSON metadata. No research or control program was executed, imported, compiled or parsed during this packaging pass. Only newly authored packaging and byte/inventory checks were used. Historical control counts are faithfully retained as earlier recorded evidence; no fresh mathematical replay is claimed and this is not an executable replay bundle. Historical instructions to run or inspect omitted files are not current instructions.

## Integrity and audit status

All active links and mapped delivered identities were checked. The archive contains only allowlisted regular UTF-8 text/JSON files, with fixed timestamps and ordinary non-executable modes; no directories, symlinks, scripts or extra archive members are emitted. MANIFEST.json binds the payload bytes other than itself and SEAL.json. SEAL.json binds that manifest; use the separately supplied trusted manifest and ZIP digests to authenticate the delivery.

The independent mathematical acceptance is complete. Independent auditing of this public ZIP is a separate gate and is not claimed here. Packaging performed no repository, native-table or other external writes. No current native status or publication status is inferred from historical source text.
