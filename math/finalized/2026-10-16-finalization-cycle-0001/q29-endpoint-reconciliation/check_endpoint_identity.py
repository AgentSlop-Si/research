"""Small fresh exact controls; no supplied code, solver, or numerical root census."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def add(a, b):
    c = a.copy()
    for k, v in b.items():
        c[k] = c.get(k, 0) + v
        if not c[k]:
            del c[k]
    return c

def shift(a, e, scale=1):
    return {k + e: scale * v for k, v in a.items() if scale * v}

def mul_binomial(a, e):
    return add(a, shift(a, e, -1))

def mul(a, b):
    c = {}
    for i, x in a.items():
        for j, y in b.items():
            c[i+j] = c.get(i+j, 0) + x*y
    return {k: v for k, v in c.items() if v}

row = [{0: 1}]
checks = []
for n in range(1, 22):
    old = row
    row = []
    for k in range(n+1):
        a = old[k] if k < n else {}
        b = shift(old[k-1], n-k) if k else {}
        row.append(add(a, b))
    if n % 2 == 0:
        continue
    derivative = {}
    for k in range(1, n+1):
        derivative = add(derivative, shift(row[k], 0, k*(-1)**(k-1)))
    m = (n-1)//2
    formula = {}
    phase_sums = []
    for r in range(m+1):
        term = {0: 1}
        labels = list(range(1, 2*r, 2)) + list(range(2*r+2, 2*m+1, 2))
        for j in labels:
            term = mul_binomial(term, j)
        formula = add(formula, term)
        assert len(labels) == m
        assert sum(labels) == m*(m+1)-r
        phase_sums.append(sum(labels))
    assert derivative == formula, (n, derivative, formula)
    checks.append({'n': n, 'm': m, 'identity_exact': True,
                   'q_degree': max(formula) if formula else None,
                   'phase_label_min': min(phase_sums),
                   'phase_label_max': max(phase_sums)})

remote_matches = []
for filename, local in [
    ('F021_PRIMARY_REPOSITORY.json', 'f021_primary_recovery_1055/sources/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md'),
    ('F021_REVIEW_REPOSITORY.json', 'f021_primary_recovery_1055/sources/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md')
]:
    obj = json.loads((ROOT/filename).read_text())['structuredContent']
    body = obj['content'].encode()
    assert body == (ROOT.parent/local).read_bytes()
    remote_matches.append({'path': local, 'sha256': hashlib.sha256(body).hexdigest(),
                           'repository_url': obj['display_url'], 'byte_identical': True})

result = {'status': 'PASS', 'scope': '11 small exact polynomial identities; no new fixed-layer census',
          'checks': checks, 'repository_source_matches': remote_matches,
          'supplied_programs_executed': 0, 'external_writes': 0,
          'uniform_discriminant_transfer_proved': False}
(ROOT/'BOUNDED_CONTROLS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status': result['status'], 'identities': len(checks), 'source_byte_matches': len(remote_matches)}))
