"""Data-only archive integrity checker. Never imports or executes scientific code."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, zipfile

P = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def same(data, item):
    return pin(data) == {key: item[key] for key in ("bytes", "sha256")}

def safe(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name

def original(maps, omitted, name):
    require(name in maps or name in omitted, "Unclassified original inventory entry: " + name)
    return maps[name]["original"] if name in maps else omitted[name]["original"]

def main():
    m = json.loads((P / "PUBLIC_MANIFEST.json").read_text())
    direct = m["direct_files"]
    require(len({x["path"] for x in direct}) == len(direct), "Duplicate direct file")
    expected_direct = {x["path"] for x in direct} | {"PUBLIC_MANIFEST.json", "evidence.zip"}
    require({p.name for p in P.iterdir() if p.is_file()} == expected_direct, "Direct file inventory mismatch")
    for x in direct:
        require(safe(x["path"]), "Unsafe direct path")
        require(same((P / x["path"]).read_bytes(), x), "Direct file mismatch: " + x["path"])
    data = (P / "evidence.zip").read_bytes()
    require(same(data, m["archive"]), "Archive hash or size mismatch")
    require(len(data) <= 409600, "Unsplit archive exceeds limit")
    z = zipfile.ZipFile(io.BytesIO(data))
    require(z.testzip() is None, "ZIP CRC failure")
    names = z.namelist()
    require(len(names) == len(set(names)), "Duplicate ZIP member")
    declared = m["archive"]["members"]
    require(len(declared) == len({x["path"] for x in declared}), "Duplicate manifest member")
    require(set(names) == {x["path"] for x in declared}, "ZIP member inventory mismatch")
    for name in names:
        require(safe(name), "Unsafe archive path: " + name)
    for x in declared:
        require(same(z.read(x["path"]), x), "Archive member mismatch: " + x["path"])
    projection = m["projection"]
    require(json.loads(z.read("PUBLIC_PROJECTION.json")) == projection, "Projection metadata mismatch")
    require(json.loads(z.read("SCOPED_RESULT.json")) == m["scope"], "Scope metadata mismatch")
    source_entries = projection["source_correspondence"]
    maps = {x["archive_path"]: x for x in source_entries}
    require(len(maps) == len(source_entries) == projection["source_entries"], "Source mapping count mismatch")
    require(set(names) == set(maps) | {"PUBLIC_PROJECTION.json", "SCOPED_RESULT.json"}, "Unclassified archive member")
    omitted = {x["source_path"]: x for x in projection["omissions"]}
    require(len(omitted) == len(projection["omissions"]), "Duplicate omission")
    require(not (set(omitted) & set(maps)), "Excluded original is published")
    for x in omitted.values():
        require(x["published"] is False, "False omission classification")
    edits = {x["archive_path"]: x for x in projection["projections"]}
    require(len(edits) == len(projection["projections"]), "Duplicate projection")
    require(set(edits) <= set(maps), "Projection without source")
    for name, x in maps.items():
        raw = z.read(name)
        require(pin(raw) == x["public"], "Public source mapping mismatch: " + name)
        if x["disposition"] == "byte-exact":
            require(x["original"] == x["public"], "False byte-exact claim: " + name)
            require(name not in edits, "Exact source is projected")
        else:
            require(x["disposition"] == "documentary-locator-only" and name in edits, "Undeclared projection")
            e = edits[name]
            require(e["original"] == x["original"] and e["public"] == x["public"], "Projection pins mismatch")
            require(raw.count(e["replacement"].encode()) == e["occurrences"], "Projection marker count mismatch")
            require(not name.endswith(".py"), "Scientific program projection forbidden")
    manifest_members = set()
    for x in projection["historical_manifests"]:
        raw = z.read(x["archive_path"])
        require(same(raw, x), "Historical manifest byte mismatch")
        require(maps[x["archive_path"]]["disposition"] == "byte-exact", "Historical manifest changed")
        inventory = json.loads(raw)["files"]
        require(len(inventory) == len({f["path"] for f in inventory}), "Duplicate historical member")
        for f in inventory:
            name = x["inventory_prefix"] + "/" + f["path"]
            expected = {"bytes": f["bytes"], "sha256": f["sha256"]}
            require(original(maps, omitted, name) == expected, "Original manifest mapping mismatch: " + name)
            manifest_members.add(name)
    for name, x in omitted.items():
        require(x["historical_manifest_entry"] == (name in manifest_members), "Omission manifest classification mismatch")
    sums_count = 0
    for x in projection["historical_sha256sums"]:
        raw = z.read(x["archive_path"])
        require(same(raw, x), "Historical SHA256SUMS byte mismatch")
        require(maps[x["archive_path"]]["disposition"] == "byte-exact", "Historical SHA256SUMS changed")
        for line in raw.decode().splitlines():
            digest, relative = line.split("  ", 1)
            name = x["inventory_prefix"] + "/" + relative
            require(original(maps, omitted, name)["sha256"] == digest, "Original checksum mapping mismatch: " + name)
            sums_count += 1
    for x in projection["source_bindings"]:
        target = x["target_archive_path"]
        require(maps[target]["original"]["sha256"] == x["expected_original_sha256"], "Source binding mismatch")
        if "git_blob" in x:
            raw = z.read(target)
            git_digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            require(git_digest == x["git_blob"], "Historical Git blob mismatch")
    candidate_binding = json.loads(z.read("author/SOURCE_BINDINGS.json"))
    for x in candidate_binding["sources"]:
        target = "author/" + x["local_path"]
        require(maps[target]["original"] == {k: x[k] for k in ("bytes", "sha256")}, "Candidate source declaration mismatch")
    review_binding = json.loads(z.read("review/SOURCE_BINDINGS.json"))
    for key, target in (("candidate_manifest_sha256", "author/MANIFEST.json"), ("candidate_report_sha256", "author/REPORT.md"), ("candidate_executor_sha256", "author/prime_field_executor.py"), ("original_sha256", "review/sources/ORIGINAL_REMOTE.md")):
        require(maps[target]["original"]["sha256"] == review_binding[key], "Review source declaration mismatch")
    verdict = json.loads(z.read("review/VERDICT.json"))
    require(verdict["review_sha256"] == maps["review/INDEPENDENT_REVIEW.md"]["original"]["sha256"], "Verdict original-review binding mismatch")
    require(json.loads(z.read("review/MANIFEST.json"))["candidate_manifest_sha256"] == maps["author/MANIFEST.json"]["original"]["sha256"], "Review candidate-manifest binding mismatch")
    require(z.read("author/sources/ORIGINAL.md") == z.read("review/sources/ORIGINAL_REMOTE.md"), "Original README copies differ")
    for role in ("author", "review"):
        require(z.read(role + "/CONTROLS.log") == z.read(role + "/CONTROL_RESULTS.json"), "Stored control copies differ")
    for x in m["direct_science_copies"]:
        require((P / x["path"]).read_bytes() == z.read(x["archive_path"]), "Direct science copy mismatch")
    print(json.dumps({"verified": True, "archive_bytes": len(data), "archive_members": len(names), "source_entries": len(maps), "historical_manifest_entries": len(manifest_members), "historical_sha256sums_entries": sums_count, "excluded_originals": len(omitted), "projected_originals": len(edits), "scientific_execution": False, "turnkey_scientific_replay_certified": False}, sort_keys=True))

if __name__ == "__main__":
    main()
