# ALG-036: sharp Gaussian thin-deficit endpoint

19 October 2026. Independently accepted at the stated scope.

For a proper complex Gaussian `Z ~ CN(0,P)`, where `P` is an orthogonal complex rank-`d` projector on `C^N` and `p_j=P_jj`, every translation `b` and radius `r>0` satisfy

`Pr(||Z-b||_infinity <= r) <= product_(p_j>0) (1-exp(-r^2/p_j))^p_j <= (1-exp(-N r^2/d))^d`.

The infinity norm uses complex modulus and `CN(0,I_d)` has density `pi^(-d) exp(-||z||^2)`. Incompatible zero-leverage coordinates make the probability zero; positive rank and radius zero also give probability zero. Rank zero is deterministic and is handled separately. Equal-coordinate-block projectors attain the rank-only bound whenever `d` divides `N`; exact nondivisible extremality is not claimed.

Start with the [full report](candidate/REPORT.md), [independent review](review/REVIEW.md) and [accepted verdict](review/VERDICT.json). [FINAL_ACCEPTANCE.json](FINAL_ACCEPTANCE.json) binds the exact accepted bytes.

## Information model and endpoint

The adaptive consequence requires a proper isotropic Gaussian input, fixed complex target unitary, input-independent seed, measurable complex-linear query rows chosen only from prior answers, a transcript-only decoder, and a quantitative terminal pathwise complex rank deficit. It includes almost-sure finite transcript stopping and countably infinite limiting transcripts. An exceptional rank event costs its probability; expected deficit alone is insufficient. There is no raw-input, uncharged norm or nonlinear-statistic side channel. Gaussian conditioning is on the transcript only. Norm envelopes are applied by unconditional event inclusions, without conditioning that posterior on a norm event.

For relative error `C||x||_2/sqrt(N)`, fixed `C>0`, the sharp first-order deficit scale is `C^2 N/log N`: above that coefficient all admissible schemes have vanishing Gaussian-average success; below it nearly equal blocks yield high Gaussian-average success on all dimensions. The critical variable is `w_N=NC^2/d-log d`. In the critical `d` comparable to `N/log N` regime, shrinking norm envelopes give universal limsup upper bound `exp(-exp(-s))` when `w_N -> s`. Equal blocks attain it on sequences with `d|N` and the stated limit. The center is `d_c=NC^2/W(NC^2)`, whose denominator is `log N-log log N+log(C^2)+o(1)`; the width is `d_c/(log d_c+1)`, of order `N/log^2 N`. Divisor-lattice and integer-sequence qualifications remain essential. Merely `d/(N/log N) -> C^2` does not determine a success limit.

For nondivisible nearly equal blocks, the critical exceedance intensity has the explicit rounding factor `A(theta,C)=(1-theta) exp(theta C^2)+theta exp(-(1-theta) C^2)` where `theta` is the fractional part of `N/d`. Its limiting success can be `exp(-A(theta_0,C) exp(-s))`. This construction does not identify the unknown nondivisible universal extremum.

## Sphere and worst-case boundaries

The fixed homogeneous linear block construction has exact samplewise equivalence between Gaussian relative-error success and radius-`C` success on the complex sphere of radius `sqrt(N)`. A universal sphere transfer is asserted only when query rows and stopping choices are unchanged by positive rescaling of answers and the decoder scales accordingly. The posterior for an arbitrary sphere-prior algorithm is not Gaussian. No universal upper theorem for arbitrary nonhomogeneous sphere algorithms is asserted.

A vanishing Gaussian-average upper bound rules out an every-fixed-input uniformly high randomized guarantee. High average success of the construction does not give a matching every-fixed-input positive guarantee. The unrestricted complement-query construction uses exactly `N-d` complex measurements, but may not belong to the original block-local architecture and carries no Fourier arithmetic or runtime claim.

## Attribution and owner scope

The constant-one geometric Brascamp–Lieb theorem is borrowed from [Bennett, Carbery, Christ and Tao](https://math.berkeley.edu/~mchrist/Papers/bcct11.pdf), at the precise printed locations recorded in [the source check](candidate/sources/PRIMARY_THEOREM_CHECK.md). The complex rank-two coisometry/disk specialization is derived here, with a direct heat-flow proof of the needed input case, and independently reviewed. Historical novelty is not claimed. No full copyrighted paper is included.

The selected thin-deficit proof gate is complete. The broad `ALG-036` owner remains `TO RESEARCH`, priority 34, with source-specific attribution and other information-model questions separate. No new owner, count, status or priority change is proposed. See [OWNER_DISPOSITION.json](OWNER_DISPOSITION.json).

## Evidence and historical status labels

All 25 files from the final candidate and independent-review manifests, including the manifests themselves, are exact copies; see [COPY_BINDINGS.json](COPY_BINDINGS.json). Candidate status labels saying that review is pending are intentionally frozen historical labels, superseded for scientific acceptance by the sealed independent verdict. Earlier endpoint reports and the retained research selection proposal likewise describe their historical states; unrelated tasks and census figures in that proposal are not updated or adopted by this release.

The preserved reviewer controls include independently authored exact complex-frame, posterior, derivative, critical-window and Dirichlet integration checks, plus a byte-identical replay of the author's newly written checker. Those finite checks support the analytic proof and do not replace it. Packaging has not rerun scientific programs. Original local paths remain provenance, and no relocated scientific replay is claimed.

## Integrity and publication

Run `python3 -B verify_package.py` here for file, hash, scope, copy-binding and bounded privacy checks only. Publish exactly [PRESERVATION_ALLOWLIST.json](PRESERVATION_ALLOWLIST.json) under `math/finalized/2026-10-19-alg036-thin-deficit`. Root [MANIFEST.json](MANIFEST.json) excludes only itself and [SEAL.json](SEAL.json); the seal binds the manifest, allowlist, acceptance and disposition. Private native snapshots, proposal, builders and receipts remain outside the public root.

This seal does not claim publication, remote byte verification or a native Sheet write. The publisher must let the separately pending prior index action resolve, verify its outcome, and freshly guard the repository base. Previously frozen approvals and artifacts are unchanged.
