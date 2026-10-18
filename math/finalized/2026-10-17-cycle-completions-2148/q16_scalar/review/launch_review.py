"""Fresh independent audit launcher with finite process limits and source pins."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
AUTHOR = Path(__file__).resolve().parent / '../candidate'
WRAPPER = Path(__file__).resolve().parent / '../../q16_wrapper/candidate'
FILES = ('production_scalar.py', 'independent_oracle.py', 'launch_review.py')
LIMITS = {'cpu_soft_seconds': 90, 'cpu_hard_seconds': 100,
          'wall_seconds': 180, 'address_space_bytes': 536870912,
          'file_size_bytes': 33554432}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def caps():
    resource.setrlimit(resource.RLIMIT_CPU, (90, 100))
    resource.setrlimit(resource.RLIMIT_AS, (536870912, 536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE, (33554432, 33554432))


def verify_author():
    expected = '1cd5e42337f2c9305c2a15883676712ce92b60156b498ca0721b6e2e7a328e27'
    assert digest(AUTHOR / 'MANIFEST.json') == expected
    manifest = json.loads((AUTHOR / 'MANIFEST.json').read_text())
    for name, info in manifest.items():
        data = (AUTHOR / name).read_bytes()
        assert len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256']
    return {'manifest_sha256': expected, 'member_count': len(manifest), 'all_members_verified': True}


def main():
    author_check = verify_author()
    before_hashes = {f: digest(HERE / f) for f in FILES}
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    try:
        process = subprocess.run([sys.executable, '-B', 'independent_oracle.py'], cwd=HERE,
                                 preexec_fn=caps, capture_output=True, timeout=180,
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        code, out, err, timeout = process.returncode, process.stdout, process.stderr, False
    except subprocess.TimeoutExpired as exc:
        code, out, err, timeout = None, exc.stdout or b'', exc.stderr or b'', True
    wall = time.monotonic() - start
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    after_hashes = {f: digest(HERE / f) for f in FILES}
    assert verify_author() == author_check
    (HERE / 'RUN.stdout').write_bytes(out)
    (HERE / 'RUN.stderr').write_bytes(err)
    result = {'limits': LIMITS, 'exit_code': code, 'timeout': timeout,
              'wall_seconds': wall,
              'cpu_seconds': after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
              'max_rss_kib': after.ru_maxrss,
              'pre_sha256': before_hashes, 'post_sha256': after_hashes,
              'source_hashes_unchanged': before_hashes == after_hashes,
              'author_packet': author_check,
              'historical_source_executed': False,
              'status': 'PASS' if code == 0 and not timeout and before_hashes == after_hashes else 'FAILED'}
    (HERE / 'PROCESS_EXIT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
