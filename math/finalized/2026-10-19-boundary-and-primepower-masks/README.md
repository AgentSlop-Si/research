# F020 boundary resolution and prime-power Fourier equality masks

19 October 2026. Two independently accepted scientific advances, preserved as a separate local release for `AgentSlop-Si/research`.

## 1. Rogers–Szegő boundary b=2p

For every odd prime `p`, every `s>=2` and every primitive root `q` of order `p^s`, the actual recurrence polynomial `P_(2p)` is irreducible over `Q_p(q)` and squarefree in characteristic zero. The actual Rogers–Szegő polynomial `H_(2p)` is squarefree, and its corresponding bilinear Christoffel–Darboux kernel guard is nonzero. Algebraic nonvanishing transfers to every primitive complex embedding.

With `t=q-1` and `v(t)=1`, the exact auxiliary centers resolve the old repeated residual into `Z^p+cZ`, where `c=(-1)^((p+1)/2)`. Root differences have valuation 1 within either p-root cluster and `(2p-1)/(2p)` between clusters; `v(Disc_X P_(2p))=p(4p-3)`. The discriminant formula concerns `P_(2p)` in this precise valuation normalization, not an asserted discriminant formula for a different polynomial.

Combined with the earlier independently accepted theorem, the proven range is **0<=b<p^s and b<=2p**, for odd `p` and `s>=1`. The local/all-A theorem composes only where its other accepted guards hold. No theorem for `b>2p` or general odd composite order is supplied here. Earlier all-residual `d=9,25` and fixed-residual results remain valid.

Read the [complete proof](f020/candidate/REPORT.md), [independent review](f020/review/INDEPENDENT_REVIEW.md), and [acceptance verdict](f020/review/VERDICT.json). The 74 author assertions and 195 independently authored exact controls support proof transcription; the universal statement rests on the written proof. The independent reviewer did not execute the author or historical checkers.

## 2. Complete prime-power floor-sharpness classification

For every prime `p`, every integer `a>=1`, `N=p^a`, and every binary Fourier mask

`D[r,c]=R[r,c] zeta^(rc)`, with primitive `N`th root `zeta`,

**D*D=dI, 1<=d<=N, holds for such a mask if and only if d=p^b with 0<=b<=a.**

The new necessity proof uses a weighted character-filtration descent, both Gram identities, repeated character labels, exactly matched row tuples, unitary p-point transforms, and proved square induced blocks. It preserves the connected `(N,d)=(8,4)` equality mask; it is not a decomposition theorem for the original support into full square blocks. Divisor sufficiency is inherited from the retained accepted construction.

In the proper range `1<=d<N`, the accepted equality criterion and compactness argument give **Delta_(p^a,p^a-d)=sqrt(d/p^a) exactly when d=p^b, 0<=b<a**. Every other proper degree has a strict infimum gap. This packet proves no new quantitative gap size or exact nonsharp optimum. Existing accepted no-mask bounds and exact cases remain in force; mixed-prime necessity remains open.

Read the [complete proof](sparse/candidate/REPORT.md), [independent review](sparse/review/REVIEW.md), and [acceptance verdict](sparse/review/VERDICT.json). Exact saved controls retain both Gram orders and the original connected inverse-row minimizer. Finite controls are not an exhaustive census or the justification for the uniform theorem.

## Scope, attribution and owner gates

F020 remains `TO RESEARCH`, priority 58, with F023 its alias. The unrestricted ordinary guard, the distinct all-m characteristic-two paired-support gate and general endpoint obligation remain open. Historical-priority gaps, including Lubinsky–Saff reference-page/citation-chain and Zhedanov full-text comparisons, remain unresolved.

M-SPARSE-DEFECT remains `TO RESEARCH`, priority 42. The prime-power necessity and floor-sharpness subproblem is mathematically resolved; mixed-prime necessity, remaining exact nonsharp optima, sharper or optimal quantitative gap rates and the broader sparse inverse problem remain open. The already accepted general no-mask bound `Delta(N,s)^2 >= d/N + 1/[10 N d^(phi(N)-1)]`, `d=N-s`, the exact `Delta(3,1)=sqrt(3)/2` nonsharp optimum and codimension-two/three classifications are retained. See [ACCEPTED_RESULT_PRESERVATION.json](ACCEPTED_RESULT_PRESERVATION.json) for the immutable prior proof/review links. No all-N divisibility theorem or full-block classification follows. Existing accepted connected controls and earlier bounds remain in force. The source author’s broad “all nonsharp optima and quantitative gaps remain open” wording is retained as history and must be read with these inherited exceptions; the present release does not reopen completed subcases.

These advances make no historical originality, runtime, production, benchmark, new-owner or global discovery-count claim. [OWNER_DISPOSITIONS.json](OWNER_DISPOSITIONS.json) records the exact remaining scope. Private owner-gate evidence and proposed prose revisions are outside this publication boundary.

## Preservation and verification

All 79 files from the four frozen scientific source packets, including their original manifests and seals, are exact byte copies. Complete reports, reviews, source bindings, newly authored checkers, saved exact outputs and prerequisite reports already retained by the sources are included. [COPY_BINDINGS.json](COPY_BINDINGS.json) records every correspondence. Older dependency collections are not recursively included.

There are no source omissions, privacy projections, scientific text rewrites or path adaptations. Original author pending-review labels remain as history; the separately preserved final independent verdicts establish acceptance. Local paths and run commands are original provenance. No relocation-tested scientific replay is claimed.

Packaging checks documentary integrity only and does not rerun scientific programs. Run `python3 -B verify_package.py` from this directory to validate the exact file set, source manifests, copy bindings, acceptance, scope, and bounded privacy scan. The root manifest excludes only itself and `SEAL.json`; the seal binds the manifest, allowlist, acceptance and dispositions.

Publish exactly [PRESERVATION_ALLOWLIST.json](PRESERVATION_ALLOWLIST.json) under `math/finalized/2026-10-19-boundary-and-primepower-masks`. Do not publish the private release parent. This local package claims no GitHub commit, remote-byte verification or native table update, and does not alter earlier queued packages or their separately guarded synchronization plan.
