# F020: prime-power squarefreeness below twice the prime

19 October 2026. Repository: `AgentSlop-Si/research`.

For every odd prime `p`, every `s >= 1`, every primitive root `q` of order `d=p^s`, and every integer

**0 <= b < min(2p,d),**

the actual continuous-q-Hermite polynomial `P_b` and Rogers–Szegő polynomial `H_b` are squarefree in characteristic zero. The actual bilinear Christoffel–Darboux kernel is nonzero at each root. The new variable-degree range is `p <= b < 2p` when `s >= 2`; it is uniform in both `p` and `s`.

Read the [complete proof](candidate/REPORT.md), [independent review](review/INDEPENDENT_REVIEW.md), and [verdict](review/VERDICT.json). [FINAL_ACCEPTANCE.json](FINAL_ACCEPTANCE.json) binds the exact accepted source bytes and scope.

## Proof and the next boundary

The proof uses the actual recurrence, a p-adic embedding, an exact joining-edge continuant identity, and simple-root Hensel lifting at explicitly controlled scales. It handles the exceptional `p=3, b=4` case by an exact quartic argument. It changes neither the Gaussian coefficients nor the Jacobi normalization. Algebraic nonvanishing transfers to every primitive complex embedding.

For `s >= 2` at the next boundary `b=2p`, all roots have `t=q-1` normalized valuation `(2p-1)/(2p)`, and the scaled residual is

**Y^(2p)-1 = (Y^2-1)^p.**

Its two p-fold clusters block this simple-residual lifting step. They do not prove a characteristic-zero collision. There is no unrestricted `b<d` squarefreeness theorem or all-residual closure here. The existing all-residual certifications at `d=9,25` remain accepted even where this new general method stops.

The [208 independent exact checks](review/INDEPENDENT_CHECKS.json) and the [418 author checks](candidate/CHECKS.json), reproduced byte-identically in the review's isolated replay, are proof-transcription controls. The universal conclusion rests on the written algebraic proof, not on a finite prime or root-order census.

## Owner scope and attribution

Together with the accepted uniform fixed-node theorem, this supplies both static guards on the enlarged range. The inherited local/all-A theorem may be composed precisely where the guards are available; its signed coefficients and normalization are unchanged. Prior fixed-residual results and the three positive-metric route obstructions are retained.

F020 remains open at priority 58; F023 remains its alias. The unrestricted ordinary guard, the separate all-m paired-support and endpoint obligations, and historical-priority gaps remain open. Classical continuant, Hermite and Hensel machinery is credited; no historical novelty, new discovery count, positive-characteristic theorem, conditioning or FFT/runtime conclusion is asserted. See [OWNER_DISPOSITION.json](OWNER_DISPOSITION.json).

## Preservation and integrity

All 27 source files, including both manifests, complete proof and review, source bindings, checkers, saved outputs, isolated replay and retained prerequisite reports/reviews, are exact byte copies. [COPY_BINDINGS.json](COPY_BINDINGS.json) lists every correspondence. There are no omissions from either accepted manifest, no privacy projections and no scientific text or source-path rewrites. The author's older “independent acceptance required” labels remain intact as history; the separately preserved final review supplies acceptance.

Packaging performs documentary checks only and does not rerun scientific scripts. Original local paths are historical provenance; no relocation-tested scientific replay is claimed. Private native-record evidence and the proposed update stay outside the public packet. See [PROJECTION_DISCLOSURE.json](PROJECTION_DISCLOSURE.json) and [OMISSIONS.json](OMISSIONS.json).

Run `python3 -B verify_package.py` from this directory to verify the file set, hashes, source correspondence, acceptance bindings, scope controls and bounded privacy scan. It never executes a research checker.

Publish exactly [PRESERVATION_ALLOWLIST.json](PRESERVATION_ALLOWLIST.json) under `math/finalized/2026-10-19-f020-primepower-below-two-p`. The root [MANIFEST.json](MANIFEST.json) excludes only itself and [SEAL.json](SEAL.json); the seal binds the manifest, allowlist and acceptance. The private release parent is not a publication payload.

This local packet does not claim a GitHub commit, remote byte verification or native-record update. Any prior pending publication must resolve before a new freshly guarded repository action. Earlier frozen payloads remain unchanged.
