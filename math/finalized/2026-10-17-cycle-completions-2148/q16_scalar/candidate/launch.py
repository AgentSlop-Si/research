"""Finite resource launcher for the fresh numerical code only."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
FILES = ('production_scalar.py', 'test_scalar.py', 'launch.py')
LIMITS = {'cpu_soft_seconds': 45, 'cpu_hard_seconds': 50, 'wall_seconds': 90,
          'address_space_bytes': 536870912, 'file_size_bytes': 16777216}


def hashes():
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in FILES}


def apply_caps():
    resource.setrlimit(resource.RLIMIT_CPU, (45, 50))
    resource.setrlimit(resource.RLIMIT_AS, (536870912, 536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16777216, 16777216))


def main():
    pre = hashes()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    try:
        p = subprocess.run([sys.executable, '-B', 'test_scalar.py'], cwd=HERE,
                           preexec_fn=apply_caps, timeout=90, capture_output=True,
                           env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        code, out, err, timeout = p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as exc:
        code, out, err, timeout = None, exc.stdout or b'', exc.stderr or b'', True
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    post = hashes()
    (HERE / 'RUN.stdout').write_bytes(out)
    (HERE / 'RUN.stderr').write_bytes(err)
    receipt = {'limits': LIMITS, 'exit_code': code, 'timeout': timeout,
               'wall_seconds': time.monotonic() - start,
               'cpu_seconds': after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
               'max_rss_kib': after.ru_maxrss, 'pre_sha256': pre, 'post_sha256': post,
               'source_hashes_unchanged': pre == post,
               'status': 'PASS' if code == 0 and not timeout and pre == post else 'BLOCKED_OR_FAILED'}
    (HERE / 'PROCESS_EXIT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt['status'] == 'PASS' else 1


if __name__ == '__main__': raise SystemExit(main())
