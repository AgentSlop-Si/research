# An explicit C8 lower gap and the F020 third partial p-block

19 October 2026 UTC. Two independently accepted scientific results, preserved without changing their source bytes. This packet is locally prepared and awaits independent packaging review and root release. Both broader owners remain open; no status, priority, score, or census change is proposed.

## Accepted scope

1. **C8 rank zero, all phases.** For normalized F8, arbitrary invertible complex monomial outer factors, an unrestricted real core, zero correction rank, and the original external complex operator norm,

   sin(3 pi/16 + 1/1000000) < delta_(8,0) <= sqrt(1+sqrt(sqrt(2)-1))/2.

   The new strict lower endpoint is approximately 0.5555710644889367420; the inherited upper endpoint is approximately 0.6410136997181851621. The lower endpoint increases by approximately 8.31469334517290149e-7 relative to the previously certified sin(3 pi/16) endpoint. Arbitrary phases are covered. No global periodicity reduction, periodic surrogate, invariant compression, or unitary compression is assumed. The exact global optimum and minimizer classification remain open.

2. **F020 third partial p-block.** For every odd prime p, s>=1, primitive p^s-th root q, and 0<=b<min(3p,p^s), the actual recurrence polynomial P_b and actual Gaussian Rogers–Szego polynomial H_b are squarefree. The original ordinary-square bilinear Christoffel–Darboux kernel is nonzero at every P_b root. The new degrees are 2p<b<3p for s>=2; b=2p is an inherited accepted input. For b=2p+r, 0<=r<p, s>=2, the accepted result also provides the transported residual Z^p+cZ, full root count and all pairwise valuations, an irreducible degree-2p inner factor over Q_p(q), and

   v(Disc P_(2p+r)) = p(4p-3)+2pr+r(r-1)/2+(r mod 2)(2p-2), with v(q-1)=1.

   There is a simple exact zero precisely for odd r; in particular P_(2p+1)/X is irreducible. The theorem handles p=3, including b=7,8, uniformly. There is no assertion at b>=3p, no unrestricted F020 or all-A closure, and no new root-order census. F023 remains the alias of F020, whose priority remains 58.

## Evidence and verification

- [C8 proof](c8_lower/candidate/PROOF.md), [independent review](c8_lower/review/REVIEW.md), and [PASS verdict](c8_lower/review/VERDICT.json). The retained author controls report 186 exact assertions; the separate independent controls report 1,190.
- [F020 proof](f020_third_block/candidate/REPORT.md), [independent review](f020_third_block/review/INDEPENDENT_REVIEW.md), and [ACCEPT verdict](f020_third_block/review/VERDICT.json). The retained author controls report 543 exact assertions; the separate independent controls report 386.
- Twelve complete source-manifest payloads, including the inherited C8 lower/upper and F020 two-digit/boundary proofs and reviews, are retained. Every nonarchive source file bound by either new independent audit is preserved. The duplicate C8 upper archive was hash-checked and its members compared byte-for-byte with the preserved unpacked files.
- [FINAL_ACCEPTANCE.json](FINAL_ACCEPTANCE.json) binds the accepted proof and review hashes. [COPY_BINDINGS.json](COPY_BINDINGS.json) and [SOURCE_REFERENCE_MAP.json](SOURCE_REFERENCE_MAP.json) map unchanged source bytes to this tree. [HISTORY_AND_SCOPE.md](HISTORY_AND_SCOPE.md) preserves the derivation history and limits.

Run `python verify_package.py` to verify only the publication tree, hashes, full source-manifest coverage, acceptance bindings, and scope constraints. It does not import or execute mathematical programs. The quoted scientific check counts describe retained prior outputs, not new packaging runs. Finite controls supplement the proofs and do not establish the unlimited theorems alone. Original programs may refer to original workspace paths; those paths and source bytes were deliberately not rewritten.

## Publication boundary

[PRESERVATION_ALLOWLIST.json](PRESERVATION_ALLOWLIST.json) is the exact proposed public payload. [OMISSIONS.json](OMISSIONS.json) records exclusions. Everything outside this public directory is local operational material and must not be published. No native workbook rows, private assistant notes, private source-path maps, credentials, full third-party papers, unrelated files, or duplicate archive containers are included.

Earlier candidate files retain their original pending-review labels. Those labels are historical; the final independent reviews control current scientific acceptance. Packaging acceptance and publication remain separate gates. No external writes, scientific reruns, literature-novelty claims, or FFT algorithm/complexity improvement claims are made by this packet.
