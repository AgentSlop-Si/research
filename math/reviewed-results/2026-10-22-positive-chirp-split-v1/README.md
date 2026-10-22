# Complete original positive-chirp exclusion: exact split distribution

This distribution preserves the exact accepted positive-chirp archive and its detached audit. The archive is physically split for transport and must be reassembled before extraction; its bytes are unchanged. This directory does not itself attest to remote publication. For every positive odd integer N with v5(N) = 1 and N congruent to 1 modulo 4, and every primitive Nth root, the original matrix B_N = (F inverse + A) inverse exists and is not a sum of two legal weighted Hamiltonian-cycle Green resolvents in the original fixed coordinates. Arbitrary complex diagonal endpoint masks, including singular and entirely zero masks, zero edge weights and coincident cycles are included. Each Green denominator must be nonzero. The original positive exception set E_plus is empty, without a size cutoff.

Read the unchanged [author proof](bundle/author/POSITIVE_PROOF.md) and [separate independent review](bundle/review/INDEPENDENT_REVIEW.md). The review verdict is ACCEPT SCOPED for the exact frozen author candidate, not for an earlier draft or a wider problem. The author's historical pending-review wording is preserved; acceptance is supplied separately rather than written into the original source.

## Complete evidence and exact provenance

This directory has 34 files: 25 archive parts, four unchanged source artifacts and five distribution-wrapper files. Its two directly readable scientific documents are a convenience selection, not a second complete replay distribution.

- The 25 binary files identified by [SPLIT_MANIFEST.json](SPLIT_MANIFEST.json) concatenate to the byte-identical accepted positive-chirp-exact-classification-20261020.zip, locally named complete.zip after reassembly. The first 24 parts are 409,600 bytes each and the final part is 26,650 bytes. These are raw slices, not separate ZIP files; no archive recompression or content change occurred. The reconstructed archive has 252 members and 35,450,791 uncompressed bytes. It contains the original author and reviewer freezes, inherited accepted restriction/necessity inputs, all 90 block certificates, 50 row-excluded representatives, all 44 rank leaves, the separate integer-root supplement, source programs, portable verifier/replay harness, manifests and historical evidence.
- [audit.zip](audit.zip) is the byte-identical detached independent packaging audit. Its 101 members include INDEPENDENT_PACKAGING_ACCEPTANCE.json, FINAL_RELEASE_BINDING.json and FROZEN_AUDIT_MANIFEST.json, plus the separate replay receipts, command results and controls. These documents are inside audit.zip, not separately duplicated here.
- [release/RELEASE_VALIDATION.json](release/RELEASE_VALIDATION.json) is retained unchanged because it is outside both archives. The final release binding inside audit.zip identifies this validation by SHA-256.
- [SHA256SUMS](SHA256SUMS) binds the 33 other distribution files. [REASSEMBLY.md](REASSEMBLY.md) gives exact reassembly instructions, and [verify_distribution.py](verify_distribution.py) independently checks the split layout and frozen source bindings without executing any archived program. The direct proof and review are byte-identical to complete.zip members author/POSITIVE_PROOF.md and review/INDEPENDENT_REVIEW.md, respectively. Their relative references describe the complete extracted package, not the reduced direct-reading layout.

The reconstructed complete archive is 9,857,050 bytes, SHA-256 `28eff2a2662f7da43286ff8679ffec0cbf67305c2b672e7d21ae5a66d7ba6201`. The audit archive is 72,915 bytes, SHA-256 `c7ec3399598f02bdf56d5aee5abaadcc5d86f9bf6ec3ef732a87cd26bb52ad7e`.

Within complete.zip, the author frozen manifest has SHA-256 `028aec843d3bc9d494cfc5a0b7dbdd3d1fec0e55e0c4ff4d2fcedf84f5e927fa` and the separate reviewer frozen manifest has SHA-256 `e58d753ecffc6c50425bf2075a84c5973d06e1a64588a72a8958378900b5a64f`. Within audit.zip, INDEPENDENT_PACKAGING_ACCEPTANCE.json has SHA-256 `4647c03882392a4bb058acf873aad11f8f8d8733451b72a98ca998d4275f0465` and FINAL_RELEASE_BINDING.json has SHA-256 `4c34f6c8c11881acbc842ae2776ef91338bded5fb0880795ff8ad84c5cf8584d`.

## Qualifications that remain unchanged

All 576 ordered cycle pairs are covered: 384 by row certificates and 192 by exhaustive residual leaves. Of 876 retained nonvanishing checks, 875 have successful 5-adic unit-residue tests. The original test in author/POSITIVE_RANK_087_B1_W1.json remains false/inconclusive. The separate author/INTEGER_BRANCH_087_B1_W1.json completes that leaf over the required integer domain. Neither file is replaced, and the failed sufficient test is not relabeled as successful.

The unchanged in-archive ACCEPTANCE_GATE.json records mathematical acceptance and producer replay, while its packaging field remains PENDING_DETACHED_AUDIT. Only the separately bound detached acceptance inside audit.zip supplies packaging acceptance. Historical statements that the package itself did not publish a repository or edit a table remain provenance, not claims about the later act of publishing this directory.

The frozen evidence records 19 replay jobs, 56 byte-exact mathematical outputs and 99 unchanged copied inputs. Split-distribution preparation rechecked file identities, exact archive reassembly, archive inventory/CRC and static source dependencies without executing supplied programs or repeating the proof or scientific replay. The historical receipts are not presented as a new publication-time replay.

## Runtime, verification and reproduction

The scientific source and certificate inputs are included; the installed runtime is external. The reference runtime is Linux, Python 3.12.14 exactly, SymPy 1.14.0 and mpmath 1.3.0. Supply those versions in a separate environment, for example with Python 3.12.14 already installed:

    python3.12 -m venv ../positive-chirp-runtime
    ../positive-chirp-runtime/bin/python -m pip install sympy==1.14.0 mpmath==1.3.0

Dependency installation can require network access. Certificate replay itself declares no network and no external scientific data inputs. Installed Python and packages remain trusted dependencies; Python audit controls and resource caps are not a kernel security sandbox.

First check the distribution hashes and reassemble to a fresh path outside this directory, using Python 3.10 or newer for the standard-library-only distribution checker:

    sha256sum -c SHA256SUMS
    mkdir ../fresh-positive-reassembly
    python3 -B verify_distribution.py . --output ../fresh-positive-reassembly/complete.zip

The checker validates all 25 parts, the exact reconstructed archive, all 252 archive members, all 101 audit members and static source/acceptance bindings. It neither extracts the archive nor executes archived programs, and it does not replace mathematical replay. SHA256SUMS is an integrity list, not an independent signature; obtain this directory and its expected identities from a trusted source. See REASSEMBLY.md for the complete procedure.

Extract the verified ../fresh-positive-reassembly/complete.zip into a new directory outside this immutable distribution layout, and read its README.md, RUNTIME_DEPENDENCIES.json, RUNTIME_COMPARISON_POLICY.json and REVIEW_REPLAY_PLAN.json before running anything. Use the pinned environment's Python as `python` in the archive's documented commands. From the extracted package, the documented entry points are:

    python -B verify.py .
    python -B package_controls.py
    python -B replay.py ../fresh-positive-replay

Every replay destination must be fresh and outside the extracted immutable package. The archive also documents verified safe extraction using verify.py. All 56 mathematical outputs must reproduce byte-for-byte, without ignored or projected mathematical fields; new logs, timings, runtime build strings and receipts are separate run-specific evidence. Use replay.py rather than the historical author freeze/orchestration helpers.

## Scope boundary

This is the original positive family only. It does not prove a statement about noninteger real parameters, another chirp family, moduli divisible by 25, unmatched endpoint permutations, different feedback, extra summands, products, a full-target three-term upper bound, unrestricted Fourier/FFT algorithms, FFT speedup or complexity, numerical stability, performance or historical novelty. The broader original O(N) forced-B question remains open outside the excluded representation grammar; this publication does not close an owner or a broader research program.

The already published negative-family result is separate and is not republished here. This README, checksum list, split manifest, reassembly instructions and distribution checker are new transport wrappers, not new mathematical evidence. The unchanged detached acceptance applies to the reconstructed original bytes; it does not claim acceptance of the split wrapper, remote transport or an original publication protocol.
