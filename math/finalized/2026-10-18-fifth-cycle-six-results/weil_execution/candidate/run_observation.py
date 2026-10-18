import datetime
import hashlib
import json
import pathlib
import subprocess
import time

BASE = pathlib.Path(__file__).resolve().parent
previous = json.loads((BASE / "RUN_RECORD.json").read_text())
cmd = previous["command"][:-1] + [str(BASE / "checks" / "observe_q9_candidate.py")]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
with (BASE / "logs/candidate_q9.stdout.json").open("wb") as out, (BASE / "logs/candidate_q9.stderr.log").open("wb") as err:
    result = subprocess.run(cmd, stdout=out, stderr=err, check=False)
record = {
    "command": cmd, "started_utc": start,
    "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "elapsed_seconds": time.monotonic() - t0, "exit_status": result.returncode,
    "observer_sha256": hashlib.sha256((BASE / "checks/observe_q9_candidate.py").read_bytes()).hexdigest(),
    "stdout": "logs/candidate_q9.stdout.json", "stderr": "logs/candidate_q9.stderr.log",
}
(BASE / "OBSERVATION_RUN_RECORD.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: v for k, v in record.items() if k != "command"}, indent=2))
raise SystemExit(result.returncode)
