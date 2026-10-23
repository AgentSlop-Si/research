"""Data-only stored-byte checker; never imports or executes scientific programs."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, zipfile

P = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def pin(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def safe(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name

def main():
    m = json.loads((P / "PUBLIC_MANIFEST.json").read_bytes())
    ds = m["direct_files"]
    require(len(ds) == len({x["path"] for x in ds}), "Duplicate direct entry")
    require({x.name for x in P.iterdir() if x.is_file()} == {x["path"] for x in ds} | {"PUBLIC_MANIFEST.json", "evidence.zip"}, "Direct inventory mismatch")
    for e in ds:
        require(safe(e["path"]), "Unsafe direct path")
        require(pin((P / e["path"]).read_bytes()) == {k:e[k] for k in ("bytes", "sha256")}, "Direct digest mismatch: " + e["path"])
    raw = (P / "evidence.zip").read_bytes()
    require(pin(raw) == {k:m["archive"][k] for k in ("bytes", "sha256")}, "Archive pin mismatch")
    require(len(raw) <= 409600, "Archive exceeds piece limit")
    z = zipfile.ZipFile(io.BytesIO(raw))
    require(z.testzip() is None, "Archive CRC failure")
    names = z.namelist()
    members = m["archive"]["members"]
    require(len(names) == len(set(names)), "Duplicate archive member")
    require(len(members) == len({x["path"] for x in members}), "Duplicate manifest member")
    require(set(names) == {x["path"] for x in members}, "Archive member inventory mismatch")
    for e in members:
        require(safe(e["path"]), "Unsafe archive member")
        require(pin(z.read(e["path"])) == {k:e[k] for k in ("bytes", "sha256")}, "Archive member pin mismatch: " + e["path"])
    p = m["projection"]
    require(json.loads(z.read("PUBLIC_PROJECTION.json")) == p, "Projection metadata mismatch")
    require(json.loads(z.read("SCOPED_RESULTS.json")) == m["scientific_scope"], "Scientific scope mismatch")
    require(json.loads(z.read("ADMINISTRATIVE_DISPOSITION.json")) == m["administrative_disposition"], "Administrative disposition mismatch")
    maps = {x["archive_path"]:x for x in p["source_correspondence"]}
    omitted = {x["source_path"]:x for x in p["omissions"]}
    edits = {x["archive_path"]:x for x in p["projections"]}
    require(len(maps) == len(p["source_correspondence"]) == p["source_entries"], "Mapping count mismatch")
    require(len(omitted) == len(p["omissions"]), "Duplicate omission")
    require(len(edits) == len(p["projections"]), "Duplicate projection")
    require(set(names) == set(maps) | {"PUBLIC_PROJECTION.json", "SCOPED_RESULTS.json", "ADMINISTRATIVE_DISPOSITION.json"}, "Unclassified archive member")
    require(not set(maps) & set(omitted), "Omitted original published")
    require(set(edits) <= set(maps), "Projection without source mapping")
    for name, e in maps.items():
        data = z.read(name)
        require(pin(data) == e["public"], "Public source mismatch: " + name)
        if e["disposition"] == "byte-exact":
            require(e["public"] == e["original"] and name not in edits, "False byte-exact claim")
        else:
            require(e["disposition"] == "documentary-locator-only" and name in edits, "Unknown projection")
            x = edits[name]
            require(x["original"] == e["original"] and x["public"] == e["public"], "Projection pins mismatch")
            require(data.count(x["replacement"].encode()) == x["occurrences"], "Projection marker count mismatch")
            require(not name.endswith(".py"), "Scientific program projection forbidden")
    for e in omitted.values():
        require(e["published"] is False, "Invalid omission declaration")
    def original(name):
        require(name in maps or name in omitted, "Unclassified original: " + name)
        return (maps[name] if name in maps else omitted[name])["original"]
    manifest_members = set()
    manifest_entries = 0
    for spec in p["historical_manifests"]:
        data = z.read(spec["archive_path"])
        require(pin(data) == spec["pin"] and maps[spec["archive_path"]]["disposition"] == "byte-exact", "Historical manifest changed")
        obj = json.loads(data)
        for group in spec["groups"]:
            entries = obj[group["key"]]
            require(len(entries) == len({x["path"] for x in entries}), "Duplicate historical entry")
            for e in entries:
                name = group["prefix"] + "/" + e["path"]
                require(original(name) == {k:e[k] for k in ("bytes", "sha256")}, "Historical inventory mismatch: " + name)
                manifest_members.add(name)
                manifest_entries += 1
    sums_members = set()
    sums_entries = 0
    for spec in p["historical_sha256sums"]:
        data = z.read(spec["archive_path"])
        require(pin(data) == spec["pin"] and maps[spec["archive_path"]]["disposition"] == "byte-exact", "Historical SHA256SUMS changed")
        for line in data.decode().splitlines():
            digest, relative = line.split("  ", 1)
            name = spec["prefix"] + "/" + relative
            require(original(name)["sha256"] == digest, "Original checksum mismatch: " + name)
            sums_members.add(name)
            sums_entries += 1
    for name, e in omitted.items():
        require(e["historical_manifest_entry"] == (name in manifest_members), "Omission manifest classification mismatch")
        require(e["historical_sha256sums_entry"] == (name in sums_members), "Omission sums classification mismatch")
    for e in p["digest_bindings"]:
        obj = json.loads(z.read(e["binding_document"]))
        for key in e["json_pointer"]:
            obj = obj[key]
        require(obj == original(e["target_source_path"])["sha256"] == e["expected_original_sha256"], "Declared digest binding mismatch")
    for e in p["source_body_bindings"]:
        data = z.read(e["archive_path"])
        require(original(e["archive_path"]) == e["pin"], "Original source body pin mismatch")
        if maps[e["archive_path"]]["disposition"] == "byte-exact":
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            require(blob == e["git_blob"], "Source body Git blob mismatch")
        else:
            require(e["archive_path"] in edits, "Missing source projection")
    # Check all selected source-register fields against retained exact bodies.
    register = json.loads(z.read("alg064/author/SOURCE_REGISTER.json"))
    for e in register["sources"]:
        name = "alg064/author/sources/" + e["file"]
        require(original(name) == {k:e[k] for k in ("bytes", "sha256")}, "ALG064 source register mismatch")
        data = z.read(name)
        require(e["git_blob"] == e["computed_git_blob"], "ALG064 Git declaration mismatch")
        if maps[name]["disposition"] == "byte-exact":
            require(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == e["git_blob"], "ALG064 source register Git binding mismatch")
        else:
            require(next(x for x in p["source_body_bindings"] if x["archive_path"] == name)["git_blob"] == e["git_blob"], "Projected original Git declaration mismatch")
    for e in json.loads(z.read("alg064/review/BINDINGS.json"))["candidate_members"]:
        require(original("alg064/author/" + e["path"]) == {k:e[k] for k in ("bytes", "sha256")}, "ALG064 reviewer candidate member mismatch")
    predecessor = json.loads(z.read("alg076/author/sources/PREDECESSOR_BINDINGS.json"))
    ancestry = p["ancestor_reference_boundaries"]
    require(len(ancestry) == len(predecessor["source_files"]), "Ancestor reference classification incomplete")
    for e, a in zip(predecessor["source_files"], ancestry):
        require(e == a["historical_entry"], "Ancestor declaration mismatch")
        if a["retained_in_this_packet"]:
            require(original(a["target_source_path"]) == {k:e[k] for k in ("bytes", "sha256")}, "Retained ancestor mismatch")
        else:
            require(a["reason"] == "Historical ancestor reference, outside the four supplied packet inventories; not newly fetched or claimed bundled.", "Ancestor boundary mismatch")
    require(z.read("alg064/review/CONTROL.json") == z.read("alg064/review/CONTROL_OPT.json"), "Stored ALG064 normal/optimized outputs differ")
    programs = sorted(n for n in maps if n.endswith(".py"))
    require(programs == p["unchanged_scientific_programs"], "Scientific program inventory mismatch")
    require(all(maps[n]["disposition"] == "byte-exact" for n in programs), "Scientific program changed")
    require(m["administrative_disposition"]["accounting"] == {"administrative_agenda_retirements":2,"mathematical_whole_owner_completions":0,"novelty_certifications":0,"duty_transfers":0}, "Disposition accounting mismatch")
    require({x["owner"] for x in m["administrative_disposition"]["owners"]} == {"ALG-064", "ALG-076"}, "Disposition owner mismatch")
    require(all(x["priority_preserved"] == 42 and x["unresolved_obligations"] for x in m["administrative_disposition"]["owners"]), "Disposition preservation missing")
    for e in m["direct_science_copies"]:
        require((P / e["path"]).read_bytes() == z.read(e["archive_path"]), "Direct scientific copy mismatch")
    print(json.dumps({"verified":True,"archive_bytes":len(raw),"archive_members":len(names),"source_entries":len(maps),"projected_originals":len(edits),"excluded_originals":len(omitted),"historical_manifest_entries":manifest_entries,"historical_sha256sums_entries":sums_entries,"scientific_programs_unchanged":len(programs),"scientific_execution":False,"turnkey_scientific_replay_certified":False}, sort_keys=True))

if __name__ == "__main__":
    main()
