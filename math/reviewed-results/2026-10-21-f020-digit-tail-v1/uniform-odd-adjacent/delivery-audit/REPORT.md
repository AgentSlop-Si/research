# Independent public-package audit

21 October 2026 UTC. Verdict: accepted within the stated scope, for the exact v2 ZIP only.

## Exact scientific and delivery binding

This is corrected detached audit version 2. ERRATUM.md records a summary transcription error in detached audit version 1; the main public v2 ZIP, accepted scientific sources and original audit evidence are unchanged. The package replay and failure-test results below were performed during the original audit and are carried forward, not represented as rerun for this correction.

Main archive: f020-uniform-odd-adjacent-public-20261021_v2.zip, 16,497,819 bytes, SHA-256 666c6ea4e537d2e3df1a4a634e7d6dc9e5a82d6f984bced77b25a880af9ce617.

Main manifest SHA-256: 50c50ea59450797ba581008517247850ca8afcb740c37351437aa766c6c8e323. Main seal SHA-256: f95c2c70d5b8b190f3e70eb96c3d5bc8c50a583a2863152ab22d11cbc22a6839.

The separately accepted author manifest is 438eb219f3534b41caa13905423c21afb2ae9fb777a8acdfa9b93438d126e032; the final independent-review manifest is a7deb7b69007940e8c7e49155701eabd22e7f81b01ba8012c5c94ee97a68be35. The explicit final reviewer acceptance and exact report/verdict bindings were verified before any public-byte acceptance. All 59 author and 34 review manifest entries were independently checked against the accepted original trees.

The exact theorem covers p prime, odd 3<=c<p, r>=2, s>r, n=cp^r+1 and every characteristic-zero primitive p^s phase. Original P_n and H_n are squarefree; the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root. The complete proof includes every genuine r=2 first-layer exception through the odd operator J=XP'_n-P_n, which equals t^S(2U f_U-f) in the r=2 central coordinates of the proof. A global weight bound on f_U alone is not asserted. The c=3 theorem is inherited, not newly credited.

Write N=p^r, h=floor(r/2), beta=p^h, L=N/beta=p^(ceil(r/2)), B=r(p-1)p^(r-1)/2 and K=cN/2+cB. The accepted root partition has (c-1)L boundary and L strict-interior roots in each noncentral disk, and (c-1)L boundary with L+1 strict-interior roots in the central disk. There are beta disks, so its disjoint total is (beta-1)cL+(cL+1)=cN+1=cp^r+1, and no root is zero. The r=2 central strict-interior depth is p^2/(p+1). For r=2, when p divides R_c(-1), exactly 2p central boundary roots need the additional layer; all satisfy v(U+1)>1 and v(P'_n)=K+p(p-1)/2+1. The discriminant correction is +2p precisely when r=2 and p divides R_c(-1), and is zero otherwise.

No c>=p, c=1 as a new claim, even-leading result as new credit, r=1, s<=r, arbitrary tail or intermediate digits, exact individual r>=3 interior depths, composite order, global F020/F023 closure, historical novelty, FFT or complexity claim is accepted. Bounded exact controls are diagnostics, not the uniform proof.

## Preservation, dependencies and partial inventories

The main ZIP contains 513 regular files. All 493 retained original source files were reconstructed byte-for-byte: 58 current author files, 28 current reviewer files, and 407 historical archive members. No proof, scientific script, mathematical result, retained manifest or seal was edited. Accepted originals were rechecked unchanged after testing.

Eleven original current files are omitted, with exact identities: the historical archive envelope, three local-origin metadata files, raw execution/environment/audit records and host-bound source-audit tooling. The envelope's 455 members are exhaustively classified; all 407 non-log members are retained and exactly 48 historical runtime logs are omitted. No replacement archive identity is invented.

Three separately named metadata projections remove only 49, 20 and 49 absolute local-origin fields. They preserve every other field and source identity. The projections were independently reconstructed from the accepted originals, not trusted from their declarations, and are not represented as the omitted original bytes. All 49 author source records, the duplicate 49-record snapshot and the review's 17 source snapshots remain identity-accounted.

The fifteen retained current JSON inventories, including renamed manifest snapshots, were independently enumerated and classified. Their overlapping references comprise 159 matching retained entries, 929 entries already absent in the original snapshots and 13 deliberate export omissions. Nine conventional nested manifests are separately qualified. The three omitted metadata declarations are addressed through the exact projections above.

All 55 historical JSON files inventories were also enumerated independently. They contain 3,631 matching retained references, 61 historical declarations differing from the retained archive bytes, 504 references to omitted logs and 273 references already absent from the source archive. These are overlapping reference counts, not distinct file counts. Historical original and projected report identities remain distinct; no incomplete old manifest is reissued or certified as a complete current tree. INVENTORY_QUALIFICATIONS.json records the full classifications.

The 66-record active locator ledger was independently reconstructed. All 48 file targets, six directory fingerprints, four runtime-output references, two omitted archive references, four omitted metadata references and two self-referential manifest-bound helpers were checked. All nine proof/report targets exist with their exact identities. Metadata reading adapters, review snapshots, archive parent references, public helpers and replay inputs are covered, rather than merely checking the ledger's PASS label. The two circular-hash-sensitive helpers are checked directly against the root manifest and exact ZIP.

## Canonical archive and fresh science replay

The entire ZIP was independently reconstructed from payloads and local, central-directory and end-record headers. All bytes matched the canonical sorted stored representation: one safe root, fixed metadata, regular files only, no duplicate/case-colliding paths, symlinks, unlisted members, extra records, prefix/suffix bytes or comments. The 511 manifest entries plus manifest and seal account for all 513 files.

All four unchanged scientific programs were first independently run outside the originals in normal and optimized Python. Their complete mathematical results reproduced the original frozen bytes. The exact delivered ZIP was then freshly replayed through its retained isolated runner. All 15 command receipts and both raw stream identities per command were independently verified. All eight scientific result comparisons and eight complete stdout comparisons matched the independent original-program baselines, with empty successful stderr. The unchanged author emits one newline beyond its result file; the public adapter respects those actual bytes rather than normalizing them.

Actual normal and -O child behavior was verified for all eight scientific runs, including optimization, debug and assertion probes. CPU, wall-clock, memory, file-size, core and numerical-thread caps were checked. Active probes confirmed hidden original host paths, readable but nonwritable input, writable fresh output, and denial of three Python and three direct native-libc socket families in both modes. Isolation uses read-only mounts, namespaces and architecture-checked kernel seccomp with no weaker fallback. Input identities matched before and after. Only current scientific controls run freshly; historical programs and original complete-tree inventory wrappers do not.

All 25 retained package mutations were rejected in each Python mode. Seven additional independently generated archive adversaries were rejected in both modes with their correct mutant digests: unlisted canonical member, wrong root, boolean byte count, and rehashed literal, URL-encoded, JSON-escaped and base64 local-locator canaries. Twelve independently exercised direct locator mutations were rejected in both modes before the root-manifest gate, covering proof, comparison, archive, replay, metadata, snapshot and helper references.

## Real failure safety and no-clobber behavior

The audit reused its genuinely completed exact-ZIP replay destination and verified that rejection preserved every successful receipt and raw stream. Wrong and missing digests, pre-existing output and retries into failed outputs were rejected. Real launcher exit 17 and real timeout/termination produced durable failure and retained both raw streams; retries preserved that evidence. No scientific work was run through the deliberately failing test launchers.

Separate tests observed and suspended the actual scientific Python process before interrupting the parent with SIGTERM or SIGKILL. Caught termination became terminal FAIL; uncatchable termination retained FAIL/RUNNING with completion explicitly unestablished. Both preserved all twelve earlier completed raw streams, and rejected retry without modification. Empty-digest and missing-archive failures were also durable and preserved.

Existing and dangling output symlinks were rejected in both parent modes without changing their targets. Corrupt archives were durably rejected even with the matching digest of those corrupt bytes. Finally, actual optimized author and optimized reviewer scientific children were each observed with -O and killed while their optimized parent remained alive. The nonzero status propagated to durable failure; prior completed evidence remained intact and could not be overwritten by retry.

Raw process data, execution streams, environment locators and timing diagnostics are excluded from this detached public audit. Only verified outcomes and immutable scientific identities are summarized.

## Staging history and conclusion

An earlier unaccepted v1 staging adapter inherited the incorrect assumption that author stdout equaled its result file. Independent execution identified the additional newline before public-byte acceptance. V1 was preserved as superseded; v2 explicitly binds the actual result and stdout separately. No scientific source was repaired and no comparison exception was introduced.

This corrected verdict accepts only the exact main-public-v2 identities above after the original independent bound checks and the separately recorded summary-correction validation. It does not accept the earlier staging. No unresolved public-delivery gap remains for these bytes, no external state was changed, and no broader scientific claim is introduced.
