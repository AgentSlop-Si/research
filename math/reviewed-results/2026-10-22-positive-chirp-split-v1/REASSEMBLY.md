# Exact reassembly and static validation

The 25 files in parts/ are ordered contiguous binary slices of one ZIP, not independently extractable archives. Parts 001 through 024 are 409,600 bytes each; part 025 is 26,650 bytes. Their byte lengths, zero-based offsets, SHA-256 values and Git blob identities are in SPLIT_MANIFEST.json.

## Recommended procedure

Obtain the full distribution, preserving every relative path. Use a trusted copy of the directory and expected checksum identities: a checksum file stored beside files is an integrity check, not a signature or independent authenticity guarantee. From this directory, run:

    sha256sum -c SHA256SUMS
    python3 -B verify_distribution.py .
    mkdir ../fresh-positive-reassembly
    python3 -B verify_distribution.py . --output ../fresh-positive-reassembly/complete.zip
    sha256sum ../fresh-positive-reassembly/complete.zip

The new checker uses only the Python 3.10+ standard library. It has no network calls, does not extract archives, and does not import or execute any archived scientific or historical program. It independently reads the parts and checks the outer checksum coverage, fixed original source identities, exact concatenation, all 252 package members and their manifest/CRC, all 101 audit members and their manifest/CRC, author/reviewer freezes, the detached acceptance/release binding, preserved inconclusive residue test and integer supplement, and declared live-source static import closure. Static import closure is not a universal dynamic-dependency proof. The checker reports JSON to stdout and exits nonzero on failure. A fresh output path outside the distribution is required; it refuses to overwrite an existing file.

The reconstructed file must have exactly 9,857,050 bytes and:

- SHA-256: 28eff2a2662f7da43286ff8679ffec0cbf67305c2b672e7d21ae5a66d7ba6201
- Git blob SHA-1 (including Git blob header): 59e63836057d2db7ae5d16956648dbf0ca820c59

The output is byte-identical to positive-chirp-exact-classification-20261020.zip. No archive member, compression stream, metadata or historical evidence is changed. The original ZIP is intentionally not duplicated in this directory.

## Transparent concatenation alternative

After sha256sum -c SHA256SUMS succeeds, create a fresh destination directory outside this distribution and concatenate the explicit ordered list below. The subshell enables noclobber so it will not silently overwrite a prior complete.zip:

    mkdir ../fresh-positive-manual
    (
      set -C
      cat \
        parts/complete.zip.part001 \
        parts/complete.zip.part002 \
        parts/complete.zip.part003 \
        parts/complete.zip.part004 \
        parts/complete.zip.part005 \
        parts/complete.zip.part006 \
        parts/complete.zip.part007 \
        parts/complete.zip.part008 \
        parts/complete.zip.part009 \
        parts/complete.zip.part010 \
        parts/complete.zip.part011 \
        parts/complete.zip.part012 \
        parts/complete.zip.part013 \
        parts/complete.zip.part014 \
        parts/complete.zip.part015 \
        parts/complete.zip.part016 \
        parts/complete.zip.part017 \
        parts/complete.zip.part018 \
        parts/complete.zip.part019 \
        parts/complete.zip.part020 \
        parts/complete.zip.part021 \
        parts/complete.zip.part022 \
        parts/complete.zip.part023 \
        parts/complete.zip.part024 \
        parts/complete.zip.part025 > ../fresh-positive-manual/complete.zip
    )
    wc -c < ../fresh-positive-manual/complete.zip
    sha256sum ../fresh-positive-manual/complete.zip

Require the exact length and SHA-256 above before extraction. The recommended checker performs additional archive and acceptance-chain validation beyond concatenation. Do not use arbitrary glob order, omit a part, decode the binary parts as text, recompress, or substitute a convenient subset of documents.

## Scientific reproduction remains separate

This step is packaging validation, not a new proof or replay. Before scientific replay, read the reconstructed archive's README.md, RUNTIME_DEPENDENCIES.json, RUNTIME_COMPARISON_POLICY.json and REVIEW_REPLAY_PLAN.json. The scientific runtime remains Linux, Python 3.12.14 exactly, SymPy 1.14.0 and mpmath 1.3.0, with runtime installation external to this distribution. Dependency installation may need network access; replay declares no network or external scientific data inputs. Installed runtime dependencies remain trusted, and Python audit/resource controls are not a kernel sandbox. Use the package's documented replay.py with fresh destinations, not historical author freeze/orchestration helpers. No archived program was executed while preparing this split distribution.

Mathematical scope, the original inconclusive 87/B1/W1 residue flag, the separate integer-root completion, historical PENDING_DETACHED_AUDIT field and detached acceptance remain unchanged. No novelty, Fourier/FFT lower-bound, speedup, unrestricted algorithmic conclusion or broader owner closure is asserted. The distribution files alone do not establish whether a remote upload happened.
