#!/usr/bin/env python3
"""Verify split transport and frozen evidence without executing archived programs.

Uses Python 3.10+ standard library only. The scientific replay has separate,
unchanged Python 3.12.14 / SymPy 1.14.0 / mpmath 1.3.0 requirements.
"""
import argparse
import ast
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

ARCHIVE_BYTES = 9857050
ARCHIVE_SHA256 = "28eff2a2662f7da43286ff8679ffec0cbf67305c2b672e7d21ae5a66d7ba6201"
ARCHIVE_GIT_SHA1 = "59e63836057d2db7ae5d16956648dbf0ca820c59"
SOURCE_PINS = {
    "audit.zip": (72915, "c7ec3399598f02bdf56d5aee5abaadcc5d86f9bf6ec3ef732a87cd26bb52ad7e"),
    "release/RELEASE_VALIDATION.json": (2552, "03b30647ad3796da8df8744274f6fa68790ee37af8aa93a9fe8b87070e9e7446"),
    "bundle/author/POSITIVE_PROOF.md": (14566, "1e1a1b95a5b8427c52f65ba9157125deead29d68dca7951dbef0960ceca84eae"),
    "bundle/review/INDEPENDENT_REVIEW.md": (14021, "ef254aa66fd5eecc494b2c8dc69ae500458678b066e7adeabf63e71a9afde0dc"),
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def identity(data):
    return {"bytes": len(data), "sha256": sha256(data), "git_blob_sha1": hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()}


def safe_name(name):
    p = PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and ".." not in p.parts
            and "\\" not in name and p.as_posix() == name,
            "Unsafe or noncanonical relative path: " + repr(name))
    return name


def local_bytes(root, name):
    safe_name(name)
    p = root / name
    require(not any(q.is_symlink() for q in [p, *p.parents]), "Symlink path: " + name)
    require(p.is_file(), "Missing regular file: " + name)
    return p.read_bytes()


def verify_zip(data, count, unpacked, manifest_name):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        require(len(names) == count and len(set(names)) == count, "Wrong/duplicate archive members")
        require(sum(i.file_size for i in z.infolist()) == unpacked, "Wrong uncompressed archive size")
        for info in z.infolist():
            safe_name(info.filename)
            require(not info.is_dir() and not info.flag_bits & 1, "Directory/encrypted ZIP member")
            mode = info.external_attr >> 16
            require(not stat.S_ISLNK(mode), "Symlink archive member")
        require(z.testzip() is None, "ZIP CRC failure")
        contents = {n: z.read(n) for n in names}
    manifest = json.loads(contents[manifest_name])
    entries = manifest["entries"]
    require(len(entries) == count - 1, "Wrong archive manifest count")
    require({e["path"] for e in entries} == set(names) - {manifest_name}, "Incomplete manifest coverage")
    check_entries(contents, entries)
    return contents


def check_entries(contents, entries, prefix=""):
    names = [safe_name(prefix + e["path"]) for e in entries]
    require(len(names) == len(set(names)), "Duplicate manifest entry")
    for e, name in zip(entries, names):
        require(name in contents, "Missing manifest member: " + name)
        b = contents[name]
        require(sha256(b) == e["sha256"], "Member hash mismatch: " + name)
        if "bytes" in e:
            require(len(b) == e["bytes"], "Member length mismatch: " + name)


def verify_source_chain(root, complete, audit):
    c = lambda name: json.loads(complete[name])
    a = lambda name: json.loads(audit[name])
    author = c("author/FROZEN_MANIFEST.json")
    review = c("review/FROZEN_REVIEW_MANIFEST.json")
    require(len(author["entries"]) == 78 and len(review["entries"]) == 99, "Frozen source count")
    check_entries(complete, author["entries"], "author/")
    check_entries(complete, review["entries"], "review/")
    author_hash = sha256(complete["author/FROZEN_MANIFEST.json"])
    review_hash = sha256(complete["review/FROZEN_REVIEW_MANIFEST.json"])
    require(review["verdict"] == "ACCEPT SCOPED", "Review verdict changed")
    require(review["candidate_manifest_sha256"] == author_hash, "Reviewer/author binding")
    for name, data in complete.items():
        if name.startswith("author/"):
            require(complete.get("review/source/" + name[7:]) == data, "Reviewer source copy: " + name)
    acceptance = a("INDEPENDENT_PACKAGING_ACCEPTANCE.json")
    final = a("FINAL_RELEASE_BINDING.json")
    validation = json.loads(local_bytes(root, "release/RELEASE_VALIDATION.json"))
    frozen_audit = a("FROZEN_AUDIT_MANIFEST.json")
    require(acceptance["status"] == final["status"] == validation["status"] == "PASS", "Acceptance status")
    require(acceptance["verdict"] == final["verdict"] == frozen_audit["verdict"] == "ACCEPT", "Acceptance verdict")
    for record in [acceptance["archive"], final["archive"], final["audited_candidate"],
                   validation["archive"], validation["audited_candidate"], frozen_audit["accepted_final_archive"]]:
        require(record["sha256"] == ARCHIVE_SHA256 and record["bytes"] == ARCHIVE_BYTES, "Archive acceptance binding")
    manifest_hash = sha256(complete["MANIFEST.json"])
    require(acceptance["package_manifest_sha256"] == final["package_manifest_sha256"]
            == validation["manifest_sha256"] == validation["package_manifest"]["sha256"]
            == manifest_hash, "Package manifest binding")
    require(final["producer_validation_sha256"] == sha256(local_bytes(root, "release/RELEASE_VALIDATION.json")), "Release validation binding")
    require(final["acceptance_sha256"] == validation["independent_packaging_acceptance"]["sha256"]
            == sha256(audit["INDEPENDENT_PACKAGING_ACCEPTANCE.json"]), "Detached acceptance binding")
    require(acceptance["author_manifest_sha256"] == validation["author_manifest_sha256"] == author_hash, "Author acceptance binding")
    require(acceptance["review_manifest_sha256"] == validation["review_manifest_sha256"] == review_hash, "Review acceptance binding")
    check_entries(audit, acceptance["evidence"])
    gate = c("ACCEPTANCE_GATE.json")
    require(gate["packaging_audit"] == "PENDING_DETACHED_AUDIT", "Historical packaging status altered")
    require(gate["author_manifest_sha256"] == author_hash and gate["review_manifest_sha256"] == review_hash, "Historical gate source binding")
    check_entries(complete, gate["evidence"])
    require(local_bytes(root, "bundle/author/POSITIVE_PROOF.md") == complete["author/POSITIVE_PROOF.md"], "Direct proof copy")
    require(local_bytes(root, "bundle/review/INDEPENDENT_REVIEW.md") == complete["review/INDEPENDENT_REVIEW.md"], "Direct review copy")
    leaf = c("author/POSITIVE_RANK_087_B1_W1.json")
    supplement = c("author/INTEGER_BRANCH_087_B1_W1.json")
    require(leaf["resultant_check"]["excludes_v5_N_1"] is False, "Original inconclusive test altered")
    require(supplement["source_sha256"] == sha256(complete["author/POSITIVE_RANK_087_B1_W1.json"]), "Integer supplement source binding")
    require(supplement["status"] == "PASS" and supplement["excludes_all_positive_integer_N_with_v5_1"] is True, "Integer supplement status")
    partition = {"successful_5adic_tests": 875, "separate_integer_root_completions": 1, "original_inconclusive_test_preserved": True}
    require(gate["arithmetic_partition"] == acceptance["arithmetic_partition"] == validation["arithmetic_partition"] == partition, "Arithmetic partition changed")
    inventory = c("SOURCE_INVENTORY.json")
    recovered = inventory["recovered_positive_input_manifest"]
    require(sha256(complete[recovered["path"]]) == recovered["sha256"], "Inherited source inventory binding")
    for record in recovered["files"]:
        check_entries(complete, [{**record, "path": record["package_path"]}])
    for record in inventory["operational_adapters"]:
        check_entries(complete, [record])
    runtime = c("RUNTIME_DEPENDENCIES.json")
    require(runtime["python"] == "3.12.14" and runtime["packages"] == {"sympy": "1.14.0", "mpmath": "1.3.0"}, "Scientific runtime pins changed")
    require(runtime["required_external_scientific_inputs"] == [] and runtime["network_required"] is False
            and runtime["runtime_aliases"] == [], "Runtime closure declaration changed")
    live = [r["path"] for r in runtime["author_scripts"] + runtime["review_scripts"]
            if not r["role"].startswith("historical")]
    live += ["replay.py", "guard_job.py", "verify.py", "assemble_review_ranks.py", "package_controls.py"]
    require(len(live) == len(set(live)) == 22, "Live source inventory changed")
    imports = []
    for name in live:
        tree = ast.parse(complete[name], filename=name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                require(node.level == 0 and bool(node.module), "Unexpected relative/dynamic import form")
                modules = [node.module]
            else:
                continue
            for module in modules:
                top = module.split(".")[0]
                local = (PurePosixPath(name).parent / (top + ".py")).as_posix()
                if local in complete or top + ".py" in complete:
                    kind = "packaged_local"
                elif top in runtime["packages"]:
                    kind = "pinned_runtime"
                elif top in sys.stdlib_module_names:
                    kind = "stdlib"
                else:
                    raise ValueError("Unresolved static import: " + name + ":" + module)
                imports.append({"script": name, "module": module, "classification": kind})
    plan = c("REVIEW_REPLAY_PLAN.json")
    require(plan["review_manifest_sha256"] == review_hash, "Replay source binding")
    require(all(n in complete for n in plan["runtime_sources"] + plan["exact_outputs"]), "Replay dependency absent")
    return {"frozen_author_entries": 78, "frozen_review_entries": 99,
            "source_bindings": "PASS", "live_scripts_ast_parsed": 22,
            "static_imports": imports, "unresolved_static_imports": 0,
            "source_closure_limit": "Static declared/import closure, not execution or a universal dynamic dependency proof.",
            "scientific_runtime": {"python": runtime["python"], "packages": runtime["packages"]},
            "inconclusive_leaf_and_integer_supplement_preserved": True}


def verify(root):
    root = root.resolve()
    checksum_bytes = local_bytes(root, "SHA256SUMS")
    checksums = {}
    for line in checksum_bytes.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "Malformed checksum line")
        digest, name = match.groups()
        safe_name(name)
        require(name not in checksums and name != "SHA256SUMS", "Duplicate/self checksum")
        checksums[name] = digest
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() or p.is_symlink()}
    require(actual == set(checksums) | {"SHA256SUMS"}, "Missing/unlisted distribution files")
    require(len(actual) == 34, "Distribution must contain exactly 34 files")
    for name, digest in checksums.items():
        require(sha256(local_bytes(root, name)) == digest, "Distribution checksum: " + name)
    for name, (length, digest) in SOURCE_PINS.items():
        b = local_bytes(root, name)
        require(len(b) == length and sha256(b) == digest, "Preserved source mismatch: " + name)
    split = json.loads(local_bytes(root, "SPLIT_MANIFEST.json"))
    require(split["schema"] == "positive-chirp-exact-split-distribution-v1", "Split schema")
    require(split["part_count"] == 25 and split["max_part_bytes"] == 409600, "Split dimensions")
    records = split["parts"]
    require(len(records) == 25, "Wrong part count")
    chunks, offset = [], 0
    for i, record in enumerate(records, 1):
        name = "parts/complete.zip.part%03d" % i
        require(record["index"] == i and record["path"] == name and record["offset"] == offset, "Part order/offset")
        b = local_bytes(root, name)
        expected_size = 409600 if i < 25 else 26650
        require(len(b) == expected_size, "Wrong part size: " + name)
        ident = identity(b)
        require(all(record[k] == ident[k] for k in ident), "Part identity: " + name)
        chunks.append(b)
        offset += len(b)
    archive = b"".join(chunks)
    archive_id = identity(archive)
    require(archive_id == {"bytes": ARCHIVE_BYTES, "sha256": ARCHIVE_SHA256,
                           "git_blob_sha1": ARCHIVE_GIT_SHA1}, "Reconstructed archive identity")
    require(all(split["reconstructed_archive"][k] == archive_id[k] for k in archive_id), "Split/archive manifest binding")
    complete = verify_zip(archive, 252, 35450791, "MANIFEST.json")
    audit = verify_zip(local_bytes(root, "audit.zip"), 101, 274149, "FROZEN_AUDIT_MANIFEST.json")
    source = verify_source_chain(root, complete, audit)
    report = {"status": "PASS_STATIC_DISTRIBUTION_VALIDATION", "distribution_files": len(actual),
              "checksum_covered_files": len(checksums), "parts": len(records),
              "reconstructed_archive": archive_id, "complete_members": len(complete),
              "audit_members": len(audit), "source_chain": source,
              "archived_programs_executed": False, "scientific_replay_performed": False,
              "remote_publication_checked": False}
    return archive, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, help="Write verified complete.zip to a NEW path outside the distribution; no extraction or replay")
    args = parser.parse_args()
    archive, report = verify(args.directory)
    if args.output:
        destination = args.output.resolve()
        root = args.directory.resolve()
        require(destination != root and root not in destination.parents, "Output must be outside immutable distribution")
        require(destination.parent.is_dir(), "Output parent must already exist")
        with destination.open("xb") as stream:
            stream.write(archive)
        require(identity(destination.read_bytes()) == report["reconstructed_archive"], "Written archive mismatch")
        report["reassembled_output_written"] = True
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, SyntaxError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
