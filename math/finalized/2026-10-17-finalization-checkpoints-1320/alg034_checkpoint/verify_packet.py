"""Verify packet integrity only; do not import or execute scientific programs."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "SAFE_MANIFEST.json").read_text())
    entries = manifest["files"]
    expected = {"SAFE_MANIFEST.json"}
    for item in entries:
        name = item["path"]
        relative = PurePosixPath(name)
        assert not relative.is_absolute() and ".." not in relative.parts
        assert name not in expected, "Duplicate manifest path"
        expected.add(name)
        target = root.joinpath(*relative.parts)
        assert target.is_file() and not target.is_symlink(), name
        body = target.read_bytes()
        assert len(body) == item["bytes"], name + ": length mismatch"
        assert hashlib.sha256(body).hexdigest() == item["sha256"], name + ": hash mismatch"
    actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    assert actual == expected, "Unexpected or missing packet files"
    assert not any(path.is_symlink() for path in root.rglob("*")), "Symlinks are forbidden"
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == manifest["payload_listing_sha256"]
    pins = json.loads((root / "SOURCE_PINS.json").read_text())
    indexed = {entry["path"]: entry for entry in entries}
    for pin in pins["files"]:
        for field in ("bytes", "sha256"):
            assert indexed[pin["path"]][field] == pin[field]
    status = json.loads((root / "STATUS.json").read_text())
    assert status["owner"] == "ALG-034" and status["priority"] == 48
    assert status["owner_status"] == "TO RESEARCH" and not status["parent_closed"]
    assert status["maximum_verifier_success"] == "BINDING_CONSISTENT_PRODUCER_UNVERIFIED"
    print(json.dumps({"result": "PASS_PACKET_INTEGRITY", "files": len(expected),
                      "byte_identical_source_files": len(pins["files"]),
                      "owner": "ALG-034", "owner_status": "TO RESEARCH", "priority": 48,
                      "payload_listing_sha256": manifest["payload_listing_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
