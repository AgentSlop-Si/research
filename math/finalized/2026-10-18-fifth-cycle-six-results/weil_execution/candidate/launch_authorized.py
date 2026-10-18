"""Fresh local launcher for the explicitly authorized, hash-pinned package."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

BASE = pathlib.Path(__file__).resolve().parent
WORK = BASE / "work"
STATIC = (BASE.parent / "preflight/static")
records = json.loads((BASE / "INPUT_HASHES.json").read_text())
for rec in records:
    assert hashlib.sha256((WORK / rec["file"]).read_bytes()).hexdigest() == rec["sha256"]
command = [
    "/usr/bin/timeout", "--signal=TERM", "--kill-after=5s", "180s",
    "/usr/bin/prlimit", "--cpu=120", "--as=536870912",
    "--fsize=16777216", "--nofile=128", "--core=0", "--",
    "/usr/bin/bwrap", "--die-with-parent", "--new-session",
    "--unshare-user", "--unshare-pid", "--unshare-uts", "--unshare-ipc",
    "--ro-bind", "/", "/", "--tmpfs", "/tmp", "--proc", "/proc", "--dev", "/dev",
    "--bind", str(WORK), "/tmp/weil-work",
]
# Every original member is a read-only file mount inside the writable output root.
for rec in records:
    command.extend(["--ro-bind", str(STATIC / rec["file"]), "/tmp/weil-work/" + rec["file"]])
command.extend([
    "--chdir", "/tmp/weil-work", "--clearenv",
    "--setenv", "HOME", "/tmp", "--setenv", "TMPDIR", "/tmp",
    "--setenv", "PATH", str(pathlib.Path(sys.executable).parent) + ":/usr/bin:/bin",
    "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
    "--setenv", "PYTHONNOUSERSITE", "1",
    "--setenv", "PYTHONHASHSEED", "0",
    "--setenv", "LC_ALL", "C.UTF-8",
    sys.executable, "-B", "-s", "run_all.py",
])
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
with (BASE / "logs" / "run_all.stdout.log").open("wb") as stdout, (BASE / "logs" / "run_all.stderr.log").open("wb") as stderr:
    result = subprocess.run(command, stdout=stdout, stderr=stderr, check=False)
record = {
    "command": command, "started_utc": started,
    "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "elapsed_seconds": time.monotonic() - t0, "exit_status": result.returncode,
    "network_namespace": "not requested; inherited environment network restrictions",
    "source_files": "all 17 package members bind-mounted read-only",
    "assertions_enabled": True,
    "stdout": "logs/run_all.stdout.log", "stderr": "logs/run_all.stderr.log",
}
(BASE / "RUN_RECORD.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
raise SystemExit(result.returncode)
