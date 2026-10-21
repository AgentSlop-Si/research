#!/usr/bin/env python3
"""Verify split archive bytes and optionally reconstruct complete.zip without overwrite.

This is distribution metadata, not a new scientific test or proof.
Python 3 standard library only. No network access, package install or extraction.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

ARCHIVE_BYTES = 20840908
ARCHIVE_SHA256 = "4205b42b7ae7f8b68d93aaa88f6750a9f2cf41fb6e51688c94c56980f2025e71"
PART_BYTES = [8388608, 8388608, 4063692]
PART_SHA256 = ['24e11dd6bc7e70a8e0c88bf0ad5ed0f512b869df3bc261e0c4476720d4fef219', '77b7815e402ce64e416f7d43bf6bc208f4dfd8955ea76e64b32b0fe6a90007fa', 'e0650f776efb2d33a917f8824e53aa28577ff2573eab46351a859ab2fe6269ec']


def verified_archive(root):
    manifest_path = root / "archive" / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("Archive manifest must be a regular non-symlink file")
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (m.get("schema") != "negative-chirp-split-archive-v1" or
            m.get("archive", {}).get("bytes") != ARCHIVE_BYTES or
            m.get("archive", {}).get("sha256") != ARCHIVE_SHA256 or
            m.get("join") != "binary concatenation in listed order; no decompression or recompression" or
            len(m.get("parts", [])) != 3):
        raise ValueError("Unexpected archive manifest identity or structure")
    chunks = []
    offset = 0
    for i, (size, digest) in enumerate(zip(PART_BYTES, PART_SHA256), 1):
        expected_path = "archive/complete.zip.part%03d" % i
        expected = {"index": i, "path": expected_path, "offset": offset,
                    "bytes": size, "sha256": digest}
        if m["parts"][i - 1] != expected:
            raise ValueError("Part manifest does not match pinned layout")
        part = root / expected_path
        if part.is_symlink() or not part.is_file() or part.parent.is_symlink():
            raise ValueError("Part must be a regular non-symlink file: " + expected_path)
        if part.stat().st_size != size:
            raise ValueError("Wrong part size: " + expected_path)
        data = part.read_bytes()
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError("Part integrity mismatch: " + expected_path)
        chunks.append(data)
        offset += size
    data = b"".join(chunks)
    if len(data) != ARCHIVE_BYTES or hashlib.sha256(data).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Reconstructed archive identity mismatch")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify only; do not create a ZIP")
    parser.add_argument("--output", type=Path, help="Output ZIP path; default: complete.zip beside this script")
    args = parser.parse_args()
    if args.check and args.output is not None:
        parser.error("--check and --output cannot be combined")
    root = Path(__file__).resolve().parent
    data = verified_archive(root)
    if args.check:
        print("Verified all 3 parts and exact complete.zip: %d bytes, SHA256 %s" % (len(data), ARCHIVE_SHA256))
        return
    output = args.output if args.output is not None else root / "complete.zip"
    if output.is_symlink():
        raise ValueError("Refusing a symlink output")
    if output.exists():
        if (output.is_file() and output.stat().st_size == ARCHIVE_BYTES and
                hashlib.sha256(output.read_bytes()).hexdigest() == ARCHIVE_SHA256):
            print("Already reconstructed and verified: " + str(output))
            return
        raise ValueError("Refusing to overwrite an existing output")
    fd, temporary = tempfile.mkstemp(prefix=".complete-verified-", dir=output.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        # Atomic create-only installation on the same filesystem; never replace output.
        os.link(temporary, output)
    finally:
        os.unlink(temporary)
    print("Reconstructed and verified: %s (%d bytes, SHA256 %s)" % (output, len(data), ARCHIVE_SHA256))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Verification failed: " + str(error), file=sys.stderr)
        sys.exit(1)
