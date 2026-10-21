# F020: complete one-leading-digit and short-tail sector

This collection assembles separately accepted results for

    n = c p^r + d,
    p odd prime, r >= 2, s > r,
    1 <= c < p, 0 <= d < p,
    q any characteristic-zero primitive p^s-th root.

Within exactly this rectangle, the original P_n and H_n are squarefree, and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root. Only positions r and possibly 0 may be nonzero in the base-p expansion. This is an accepted union of existing theorems, not a new proof or new degree credit.

## Read the coverage and its separate review

- [Coverage map](assembly/COVERAGE_MAP.md), with its [explicit public-reading projection ledger](assembly/PROJECTION.json)
- [Independent assembly review](assembly/review/INDEPENDENT_REVIEW.md), [accepting verdict](assembly/review/VERDICT.json), and [credit ledger](assembly/review/CREDIT_LEDGER.json)
- [Exact common scope and exclusions](SCOPE.json)
- [Accepted source identities](assembly/SOURCE_IDENTITIES.json)
- [Immutable earlier GitHub authority](INHERITED_AUTHORITY.json)

All d=0 degrees for every 1<=c<p, and both c=1 positive-tail parities, were already accepted and published on 20 October 2026. They are inherited, not new coverage. The earlier complete zero-tail theorem is [here](https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/general/PROOF.md), with its [review](https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/general/REVIEW.md) and [acceptance](https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/general/ACCEPTANCE.json). The c=1 positive-tail sources are [odd d, historically low-even](https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/low-even/PROOF.md) and [even d, historically low-odd](https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/low-odd/PROOF.md); the historical names describe total-degree parity, not tail parity. Their final accepting reviews are linked in the authority ledger.

## Accepted uniform evidence retained here

1. [Even leading, positive even tail](even-leading-even-tail/README.md)
2. [Even leading, odd tail](even-leading-odd-tail/README.md)
3. [Uniform odd leading, adjacent tail d=1](uniform-odd-adjacent/README.md), with corrected detached audit v2, its erratum and independent editorial-correction acceptance
4. [Uniform odd leading, tail d=2](uniform-odd-plus-two/README.md), current public package v3
5. [Odd leading, odd tail](odd-leading-odd-tail/README.md), inheriting d=1
6. [Odd leading, positive even tail](odd-leading-even-tail/README.md), inheriting d=2 and adding only even d>=4 relative to its supplied predecessors

These overlap as proof dependencies, not as extra counted degree families. Separate c=3/d=2 and superseded staging packages are not separately republished. Historical dependencies already embedded in accepted archives remain unchanged. Direct zero-tail refinements add no degree coverage and are not a separate new result here.

## Exact archives and manageable readable selection

[ARCHIVES.json](ARCHIVES.json) records every accepted full main archive and separate detached audit. Original archives at most 8 MiB are stored as exact ZIP files; larger archives are consecutive exact 8 MiB parts with a shorter final part. No accepted archive is edited, extracted and repacked, or recompressed for this publication. Base64 is only a future Git API transport encoding, not the stored file representation.

From this directory:

    python3 reassemble.py --check
    python3 reassemble.py --archive even-leading-odd-tail-main --output recovered.zip

The first command verifies all stored archives/parts without creating output. The second reconstructs the selected original archive, refusing to overwrite a different file. The standard-library checker never extracts or executes research. Only after checking exact archive identity should a reader extract it and follow that package's own verification/replay guide and dependency requirements.

[SOURCE_INDEX.json](SOURCE_INDEX.json) maps every selected readable member to its accepted public source. The plus-two SOURCE_INVENTORY.json exceeds the conservative 1 MiB inline text-readback tier and is retained only inside its exact accepted archive, with the omission and member hash recorded in SOURCE_INDEX.json. Each `readable/` subtree is intentionally partial; copied source manifests describe the complete original archive, not this browser selection. Relative links and historical wrapper commands in unchanged source reports refer to their original package context. The exact assembly-review report likewise describes its separately audited original review packet; only the named public-safe report, verdict, scope checks and credit ledger are selected here. None of these reading selections claims to reconstruct private review evidence or original administrative bytes.

The source packages explicitly distinguish exact scientific bytes from narrow locator/administrative projections. Their partial-history inventories, inactive historical references, omitted original wrappers, collaborator credit and limited fresh-replay claims remain applicable. This distribution checks source/archive identity but runs no new scientific replay and strengthens none of those claims. Earlier repository publication verified exact proof/review text and archive Git identities/sizes but not every large archive's remote raw bytes. That limitation is not upgraded here. Hashes bind content, not mathematical truth or authorship signatures.

## Scope does not expand

No arbitrary intermediate digits, arbitrary degrees below p^s, p=2, r<2, s<=r, composite phase orders, unrelated finite characteristics, global F020/F023 closure, historical originality, or FFT/algorithmic cost improvement is claimed. Root geometry, ordinary derivative values and kernel valuations differ by branch; there is no single common all-root formula. In particular beta=p^floor(r/2), not p^ceil(r/2); leading-one positive-tail geometry must not be replaced by later cL-per-rho-disk geometry. Finite controls supplement the accepted uniform proofs and are not the proof of completeness.
