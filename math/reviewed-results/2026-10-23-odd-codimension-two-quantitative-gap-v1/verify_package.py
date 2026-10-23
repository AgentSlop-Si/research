"""Data-only package integrity checker. Executes no archived scientific program."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, zipfile
P=Path(__file__).resolve().parent
def require(condition, message):
    if not condition:
        raise RuntimeError(message)
def pin(data):
    return {"bytes":len(data), "sha256":hashlib.sha256(data).hexdigest()}
def same(data, item):
    return pin(data)=={key:item[key] for key in ("bytes","sha256")}
def main():
    m=json.loads((P/"PUBLIC_MANIFEST.json").read_text())
    data=(P/"evidence.zip").read_bytes()
    require(same(data,m["archive"]),"Archive hash or size mismatch")
    z=zipfile.ZipFile(io.BytesIO(data))
    require(z.testzip() is None,"ZIP CRC failure")
    names=z.namelist()
    require(len(names)==len(set(names)),"Duplicate ZIP member")
    require(set(names)=={x["path"] for x in m["archive"]["members"]},"ZIP member inventory mismatch")
    for name in names:
        p=PurePosixPath(name)
        require(not p.is_absolute() and ".." not in p.parts,"Unsafe archive member")
    for x in m["archive"]["members"]:
        require(same(z.read(x["path"]),x),"Archive member mismatch: "+x["path"])
    projection=m["projection"]
    require(json.loads(z.read("PUBLIC_PROJECTION.json"))==projection,"Projection metadata mismatch")
    require(json.loads(z.read("SCOPED_RESULT.json"))==m["scope"],"Scope metadata mismatch")
    maps={x["archive_path"]:x for x in projection["source_correspondence"]}
    require(len(maps)==projection["source_entries"],"Source count mismatch")
    for name,x in maps.items():
        require(pin(z.read(name))==x["public"],"Public mapping mismatch: "+name)
        if x["disposition"]=="byte-exact":
            require(x["original"]==x["public"],"False exact-copy claim: "+name)
    for x in projection["historical_manifests"]:
        raw=z.read(x["archive_path"])
        require(same(raw,x),"Historical manifest mismatch")
        inventory=json.loads(raw)["files"]
        if isinstance(inventory,dict):
            inventory=[dict(path=k,**v) for k,v in inventory.items()]
        for f in inventory:
            n=x["inventory_prefix"]+"/"+f["path"]
            expected={"bytes":f.get("bytes",f.get("size")),"sha256":f["sha256"]}
            require(maps[n]["original"]==expected,"Original inventory mismatch: "+n)
    for x in projection["historical_seals"]:
        raw=z.read(x["archive_path"])
        require(same(raw,x),"Historical seal mismatch")
        for name,digest in json.loads(raw).items():
            n=x["inventory_prefix"]+"/"+name
            require(maps[n]["original"]["sha256"]==digest,"Original seal mismatch: "+n)
    for x in projection["source_bindings"]:
        require(maps[x["target_archive_path"]]["original"]["sha256"]==x["expected_original_sha256"],"Source binding mismatch")
        n=x["local_copy_archive_path"]
        if n:
            require(maps[n]["original"]["sha256"]==x["expected_original_sha256"],"Bound local copy mismatch")
    for x in m["direct_science_copies"]:
        require((P/x["path"]).read_bytes()==z.read(x["archive_path"]),"Direct science mismatch")
    for x in m["direct_files"]:
        require(same((P/x["path"]).read_bytes(),x),"Direct file mismatch: "+x["path"])
    print(json.dumps({"verified":True,"archive_bytes":len(data),"archive_members":len(names),"source_entries":len(maps),"scientific_execution":False},sort_keys=True))
if __name__=="__main__":
    main()
