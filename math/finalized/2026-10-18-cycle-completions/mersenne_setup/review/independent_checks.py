"""Independent bounded review. Executes only the inspected new candidate snapshot.
All native full products/divisions in this file are test oracles, not cost claims.
No historical archive/code is imported or executed.
"""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import math
import random

HERE = Path(__file__).resolve().parent
SNAP = HERE.parent / 'candidate'
SEED = 20261018000846019
rng = random.Random(SEED)
counts = {}
digest = hashlib.sha256()

def record(label, value):
    counts[label] = counts.get(label, 0) + 1
    digest.update(repr((label, value)).encode())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

for name, expected in json.loads((SNAP / 'MANIFEST.json').read_text()).items():
    assert sha(SNAP / name) == expected
    record('candidate_manifest', name)
for pin in json.loads((SNAP / 'SOURCE_PINS.json').read_text()):
    assert sha(SNAP / pin['path']) == pin['sha256']
    record('source_pins', pin['path'])

# Import occurs only after the candidate code has been manually read in full.
spec = importlib.util.spec_from_file_location('inspected_new_candidate', SNAP / 'fresh_controls.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
reproduced = c.controls()
assert reproduced == json.loads((SNAP / 'CONTROL_RESULTS.json').read_text())
record('saved_run_reproduced', reproduced['result_digest'])

# Separate seed, exhaustive small products and split/carry boundary patterns.
for x in range(128):
    for y in range(128):
        assert c.kara(x, y) == x * y
        record('karatsuba_exhaustive', (x, y))
for width in (15, 16, 17, 18, 23, 24, 25, 31, 32, 33, 47, 48, 49,
              63, 64, 65, 127, 128, 129, 511, 512, 513, 2049, 4097):
    h = (width + 1) // 2
    values = (0, 1, (1 << width) - 1, 1 << (width - 1),
              (1 << h) - 1, (1 << h) + 1, rng.getrandbits(width))
    for x, y in zip(values, values[::-1]):
        assert c.kara(x, y) == x * y
        record('karatsuba_boundaries', (width, x, y))

# Independently trace each carry and the invariant, including W<t, partial
# final limbs, exact powers of two, and three short-product recursion levels.
bounds = (2, 3, 4, 127, 128, 129, 255, 256, 257, 258, 65535, 65536,
          65537, (1 << 24), (1 << 24) + 1, (1 << 40) + 17, (1 << 65) + 1)
for bound in bounds:
    t = 8 * ((max(1, (bound - 1).bit_length()) + 7) // 8)
    R = 1 << t
    for W in sorted(set((1, 2, 7, 8, 9, t - 1, t, t + 1,
                         2 * t - 1, 2 * t, 2 * t + 1, 8193, 32769))):
        mask = (1 << W) - 1
        pairs = ((0, 0), (mask, 0), (mask, 1), (mask, bound - 1),
                 (1 << (W - 1), bound - 1), (rng.getrandbits(W), rng.randrange(bound)))
        for x, k in pairs:
            assert c.short_mod(x, k, W, bound) == ((x * k) & mask)
            carry = prefix = written = 0
            q = (W + t - 1) // t
            for j in range(q):
                a = (x >> (j * t)) & (R - 1)
                z = a * k + carry
                b, carry = z & (R - 1), z >> t
                prefix += a << (j * t)
                written += b << (j * t)
                assert k * prefix == written + (carry << ((j + 1) * t))
                assert 0 <= carry < max(1, k)
                assert z.bit_length() <= 2 * t
            assert (written & mask) == ((x * k) & mask)
            record('short_product_and_carry', (bound, W, k))

# Verify actual short_mod top-level product count and child contraction.
original_kara = c.kara
stack = []
local = {'roots': 0, 'nodes': 0}
def traced_kara(x, y):
    t = max(x.bit_length(), y.bit_length())
    if stack:
        assert t <= (stack[-1] + 1) // 2
    else:
        local['roots'] += 1
    local['nodes'] += 1
    stack.append(t)
    try:
        return original_kara(x, y)
    finally:
        stack.pop()
c.kara = traced_kara
for W, bound in ((1, 2), (17, 257), (65, 65537), (1025, (1 << 24) + 1),
                 (8193, (1 << 65) + 1), (8192, (1 << 40) + 17)):
    local.update(roots=0, nodes=0)
    t = 8 * (((bound - 1).bit_length() + 7) // 8)
    x, k = (1 << W) - 1, bound - 1
    assert c.short_mod(x, k, W, bound) == ((x * k) & ((1 << W) - 1))
    assert local['roots'] == (W + t - 1) // t
    record('product_count_and_contraction', (W, bound, dict(local)))
c.kara = original_kara

# Direct full-factorial oracle only in this independent harness.
for n in (1, 2, 3, 8, 17, 32, 65, 130, 257):
    for W in (1, 2, 8, 9, 17, n + 11):
        u, inv = c.odd_tables(n, W)
        f = 1
        mod = 1 << W
        for i in range(n):
            if i:
                f *= i
            odd = f >> ((f & -f).bit_length() - 1)
            assert u[i] == odd % mod
            assert inv[i] == pow(odd, -1, mod)
        record('odd_factorial_table', (n, W))

assert c.taylor([], 1) == [] and c.taylor([], -1) == []
record('empty_shift', True)
for n in (1, 2, 4, 7, 16, 31, 33, 65):
    for h in (1, 9, 37):
        lim = (1 << h) - 1
        for a in ([lim] * n, [(-1 if i & 1 else 1) * lim for i in range(n)],
                  [rng.randrange(-lim, lim + 1) for _ in range(n)]):
            for sign in (-1, 1):
                expected = [sum(math.comb(i, j) * a[i] * (sign ** (i-j))
                                for i in range(j, n)) for j in range(n)]
                got = c.taylor(a, sign)
                assert got == expected
                assert c.taylor(got, -sign) == a
                record('signed_shift_and_inverse', (n, h, sign, got))

# Stress quotient high/low window overlap and boundary remainders.
for m in (2, 3, 4, 7, 8, 9, 15, 16, 17, 31, 63, 127, 257):
    p = (1 << m) - 1
    for q in (0, 1, p-1, p, p+1, rng.getrandbits(5*m+3)):
        for r in (0, 1, p-1):
            x = q*p+r
            assert c.div_mersenne(x, m) == (q, r)
            record('mersenne_quotient', (m, q, r))
    for n in (1, 2, 7, 17):
        digits = [rng.randrange(1 << m) for _ in range(n)]
        x = sum(a << (m*i) for i, a in enumerate(digits))
        raw = c.taylor(digits, 1)
        canon = c.canonical_p(raw, m)
        assert all(0 <= a < p for a in canon)
        assert sum(a*p**i for i, a in enumerate(raw)) == x
        assert sum(a*p**i for i, a in enumerate(canon)) == x
        binary_raw = c.taylor(canon, -1)
        assert sum(a << (m*i) for i, a in enumerate(binary_raw)) == x
        # Generate a deliberately signed raw p expansion via carry relocation.
        signed = list(canon) + [0]
        for i in range(len(canon)):
            r = rng.randrange(-13, 14)
            signed[i] += r*p
            signed[i+1] -= r
        assert c.canonical_p(signed, m) == canon
        record('conversion_and_signed_carry', (m, n, canon))

# The code audit reports all native multiplication syntax above controls;
# these are index/length operations, never represented-value products.
tree = ast.parse((SNAP/'fresh_controls.py').read_text())
core_native_products = []
for f in tree.body:
    if isinstance(f, ast.FunctionDef) and f.name == 'controls':
        break
    if isinstance(f, ast.FunctionDef):
        for node in ast.walk(f):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
                core_native_products.append({'function':f.name, 'line':node.lineno,
                                             'expression':ast.unparse(node)})
result = {'status':'PASS', 'seed':SEED, 'counts':counts,
          'independent_result_digest':digest.hexdigest(),
          'candidate_manifest_sha256':sha(SNAP/'MANIFEST.json'),
          'candidate_report_sha256':sha(SNAP/'REPORT.md'),
          'candidate_code_sha256':sha(SNAP/'fresh_controls.py'),
          'reproduced_candidate_results':reproduced,
          'core_native_product_syntax':core_native_products,
          'scope':'Finite exactness, binding and operation-structure checks; no asymptotic or timing inference.',
          'historical_code_execution':False, 'external_writes':False}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
