"""Fresh data-only audit. Parse archived programs as text; never import/execute them."""
import ast
import hashlib
import json
from pathlib import Path
import zipfile

BASE = Path(__file__).resolve().parent
PRIVATE = BASE / "private"
checks = []
def check(name, value):
    checks.append({"name": name, "pass": bool(value)})
    if not value:
        raise AssertionError(name)

def sha(data):
    return hashlib.sha256(data).hexdigest()

archives = {
    "precision_archive.zip": (59410, "6381acc0cf5bf6aff7af69b645f77462026fa92949d7d685abaf0c5f523fc4b2"),
    "wrapper_archive.zip": (155889, "1ea2f4ce8db36d0f7e13141e8c1e679cf02e552f2054afe84a0dbda738ea5797"),
}
for name, (length, digest) in archives.items():
    data = (PRIVATE / name).read_bytes()
    check(name + " length", len(data) == length)
    check(name + " SHA256", sha(data) == digest)

member_pins = [
    ("precision_archive.zip", "REPORT.txt", "8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8"),
    ("precision_archive.zip", "INDEPENDENT_REVIEW.txt", "31820fc28ff120f5982d4be0a03922600f06c3b7fb1a707b2617ae6e65201bf4"),
    ("precision_archive.zip", "checks/fresh_controls.py", "3e5941756a99f51f628c3d3972967374cd4e425eb9d1164dd8172305af52d5b8"),
    ("precision_archive.zip", "checks/independent_controls.py", "2f7fb49c261bf8ac0beccdb6f9a8cedcc00dc068e7ca8b1e291bca5842df96a8"),
    ("wrapper_archive.zip", "paid_source_adapter_independent_1618/REVIEW.txt", "b481803172638f847edf296cd5d32272bc4a73e730e979cb5ca15cffb3f7b4c7"),
    ("wrapper_archive.zip", "paid_source_adapter_independent_1618/evidence/INPUT_CONTRACT.txt", "b8add9064ecf19f9656c9ca043003090b557c46608e4d455ca9e0dfb1d9918e5"),
    ("wrapper_archive.zip", "paid_source_adapter_independent_1618/inspected_source/paid_source.py", "5cd35d6b3dc1dd6b077db3f1b957cbf4794479aa1b0e592008edf83fa5216d2b"),
]
bodies = {}
pins = []
for archive, member, digest in member_pins:
    with zipfile.ZipFile(PRIVATE / archive) as z:
        body = z.read(member)
    check(member + " SHA256", sha(body) == digest)
    bodies[member] = body.decode("utf-8")
    pins.append({"archive": archive, "member": member, "bytes": len(body), "sha256": digest})

def function(text, name):
    # ast.parse inspects syntax only. No compiled or imported source is run.
    return next(x for x in ast.parse(text).body if isinstance(x, ast.FunctionDef) and x.name == name)

source = bodies["checks/fresh_controls.py"]
f = function(source, "fixed_producer")
check("reference producer arguments", [a.arg for a in f.args.args] == ["x", "n", "b", "a", "beta", "p"])
check("reference producer is normalized-input interface", ast.get_docstring(f) == "x is already exact normalized dyadic data.")
check("reference producer source bounds", (f.lineno, f.end_lineno) == (83, 116))
check("reference producer has no adapter call", not any(isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == "adapt" for x in ast.walk(f)))
source = bodies["checks/independent_controls.py"]
f = function(source, "pipeline")
check("independent pipeline arguments", [a.arg for a in f.args.args] == ["n", "b", "a", "beta", "W", "t", "seed"])
check("independent pipeline source bounds", (f.lineno, f.end_lineno) == (80, 137))
tree = ast.parse(source)
check("reference global G=224", any(isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "G" for t in x.targets) and isinstance(x.value, ast.Constant) and x.value.value == 224 for x in tree.body))
source = bodies["paid_source_adapter_independent_1618/inspected_source/paid_source.py"]
f = function(source, "adapt")
check("adapter only accepts payload and declaration", [a.arg for a in f.args.args] == ["payload", "certificate"])
check("adapter source bounds", (f.lineno, f.end_lineno) == (179, 278))
contract = bodies["paid_source_adapter_independent_1618/evidence/INPUT_CONTRACT.txt"]
check("explicit no producer trace condition", "The adapter recomputes no original input or producer trace." in contract)
check("explicit conditional soundness retained", "CONDITIONAL_ON_TRUSTED_UPSTREAM_CONTRACT" in contract)
all_length = json.loads((PRIVATE / "all_length_REPORT.json").read_text())["structuredContent"]["content"].encode()
check("all-length report identity", sha(all_length) == "7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062")
obligations = json.loads((BASE / "OBLIGATIONS.json").read_text())
check("owner status unchanged", obligations["owner_status"] == "TO RESEARCH" and obligations["priority"] == 48)
check("no duplicate obligation IDs", len({x["id"] for x in obligations["items"]}) == len(obligations["items"]))

result = {
    "result": "PASS_DATA_ONLY_SOURCE_AUDIT",
    "checks_passed": len(checks),
    "checks": checks,
    "source_members": pins,
    "archived_programs_imported_or_executed": False,
    "producer_execution_or_integration_certified": False,
    "new_mathematical_result_claimed": False,
    "external_mutations": False,
}
(BASE / "AUDIT_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k not in ["checks", "source_members"]}))
