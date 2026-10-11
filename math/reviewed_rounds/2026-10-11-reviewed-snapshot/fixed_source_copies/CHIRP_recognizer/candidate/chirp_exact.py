"""Bounded exact CHIRP reference decision API. Candidate, not production certified.

Only the Nth-root family is implemented. No numerical tolerances, 2N-root
curvature extension, FFT/Toeplitz speed claim, or supplied-modulus trust mode.
All library code is newly authored; only Python standard-library imports.
"""
from collections import Counter
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
import math
import sys

SCHEMA = "chirp-exact-reference-v1"
FIELDS = {"N", "p", "r", "omega", "x"}
HARD_CAPS = {"max_n": 512, "max_r": 128, "max_p_bits": 64,
             "max_work_units": 20_000_000}

@dataclass(frozen=True)
class Limits:
    max_n: int = 128
    max_r: int = 64
    max_p_bits: int = 32
    max_work_units: int = 2_000_000

class Exhausted(Exception):
    pass

class Meter:
    def __init__(self, cap):
        self.cap = cap
        self.used = 0
        self.counts = Counter()
        self.stage = "validation"
    def pay(self, category, amount=1):
        if self.used + amount > self.cap:
            raise Exhausted(self.stage + ": " + category)
        self.used += amount
        self.counts[category] += amount

class Field:
    def __init__(self, p, meter):
        self.p, self.meter = p, meter
    def add(self, a, b):
        self.meter.pay("field_additions")
        return (a+b) % self.p
    def sub(self, a, b):
        self.meter.pay("field_additions")
        return (a-b) % self.p
    def mul(self, a, b):
        self.meter.pay("field_multiplications")
        return a*b % self.p
    def power(self, a, e):
        self.meter.pay("power_calls")
        value = 1
        while e:
            self.meter.pay("power_bit_iterations")
            if e & 1:
                value = self.mul(value, a)
            e >>= 1
            if e:
                a = self.mul(a, a)
        return value
    def inverse(self, a):
        if a == 0:
            raise ArithmeticError("Internal attempt to invert zero")
        self.meter.pay("scalar_inversions")
        return self.power(a, self.p-2)


def input_digest(problem):
    """Canonical JSON binding; this does not grant validity to a malformed input."""
    return sha256(json.dumps(problem, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _rank(matrix, f):
    a = [row[:] for row in matrix]
    h = 0
    for j in range(len(a[0])):
        pivot = None
        for i in range(h, len(a)):
            f.meter.pay("pivot_probes")
            if a[i][j]:
                pivot = i
                break
        if pivot is None:
            continue
        a[h], a[pivot] = a[pivot], a[h]
        inv = f.inverse(a[h][j])
        for k in range(j, len(a[0])):
            a[h][k] = f.mul(a[h][k], inv)
        for i in range(h+1, len(a)):
            scale = a[i][j]
            for k in range(j, len(a[0])):
                a[i][k] = f.sub(a[i][k], f.mul(scale, a[h][k]))
        h += 1
        if h == len(a):
            break
    return h


def _solve(matrix, rhs, f):
    n = len(rhs)
    a = [row[:] + [v] for row, v in zip(matrix, rhs)]
    for j in range(n):
        pivot = None
        for i in range(j, n):
            f.meter.pay("pivot_probes")
            if a[i][j]:
                pivot = i
                break
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        inv = f.inverse(a[j][j])
        for k in range(j, n+1):
            a[j][k] = f.mul(a[j][k], inv)
        for i in range(n):
            if i != j:
                scale = a[i][j]
                for k in range(j, n+1):
                    a[i][k] = f.sub(a[i][k], f.mul(scale, a[j][k]))
    return [row[-1] for row in a]


def _determinant(matrix, f):
    a = [row[:] for row in matrix]
    answer = 1
    for j in range(len(a)):
        pivot = None
        for i in range(j, len(a)):
            f.meter.pay("pivot_probes")
            if a[i][j]:
                pivot = i
                break
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            answer = f.sub(0, answer)
        answer = f.mul(answer, a[j][j])
        inv = f.inverse(a[j][j])
        for i in range(j+1, len(a)):
            scale = f.mul(a[i][j], inv)
            for k in range(j+1, len(a)):
                a[i][k] = f.sub(a[i][k], f.mul(scale, a[j][k]))
    return answer


def _poly(coefficients, node, f):
    value = 0
    for c in reversed(coefficients):
        value = f.add(f.mul(value, node), c)
    return value


def _try_phase(x, r, phase, table, f, record):
    n = len(x)
    f.meter.stage = "candidate.dechirp"
    y = []
    for j, value in enumerate(x):
        f.meter.pay("raw_dechirp_reads")
        y.append(f.mul(value, table[(-phase*j*j) % n]))
    f.meter.stage = "candidate.hankel_rank"
    f.meter.pay("matrix_cells", r*r)
    h = [[y[(i+j) % n] for j in range(r)] for i in range(r)]
    s = _rank(h, f)
    record["hankel_rank"] = s
    if s == 0:
        # A periodic zero prefix alone says nothing about later raw entries.
        f.meter.pay("full_zero_checks", n)
        return ([], "ACCEPT") if not any(y) else (None, "ZERO_PREFIX_RAW_MISMATCH")
    f.meter.stage = "candidate.node_polynomial"
    f.meter.pay("matrix_cells", s*s)
    hs = [[y[(i+j) % n] for j in range(s)] for i in range(s)]
    coeff = _solve(hs, [f.sub(0, y[(i+s) % n]) for i in range(s)], f)
    if coeff is None:
        return None, "SINGULAR_LEADING_HANKEL"
    coeff.append(1)
    f.meter.stage = "candidate.grid_roots"
    nodes = []
    for b, node in enumerate(table):
        f.meter.pay("grid_root_tests")
        if _poly(coeff, node, f) == 0:
            nodes.append(b)
    if len(nodes) != s:
        return None, "NODE_ROOT_COUNT_MISMATCH"
    f.meter.stage = "candidate.raw_recurrence"
    mismatches = 0
    for k in range(n-s):
        value = 0
        for j, c in enumerate(coeff):
            value = f.add(value, f.mul(c, y[k+j]))
        f.meter.pay("recurrence_comparisons")
        mismatches += value != 0
    if mismatches:
        record["recurrence_mismatches"] = mismatches
        return None, "RAW_RECURRENCE_MISMATCH"
    f.meter.stage = "candidate.weights"
    f.meter.pay("matrix_cells", s*s)
    vandermonde = [[table[(b*j) % n] for b in nodes] for j in range(s)]
    weights = _solve(vandermonde, y[:s], f)
    if weights is None:
        raise ArithmeticError("Distinct grid nodes yielded singular Vandermonde")
    modes = [{"b": b, "gamma": weight} for b, weight in zip(nodes, weights) if weight]
    f.meter.stage = "candidate.full_raw_synthesis"
    mismatches = 0
    for j in range(n):
        value = 0
        for mode in modes:
            value = f.add(value, f.mul(mode["gamma"], table[(phase*j*j+mode["b"]*j) % n]))
        f.meter.pay("raw_synthesis_comparisons")
        mismatches += value != x[j]
    record["raw_synthesis_checked"] = n
    if mismatches:
        record["synthesis_mismatches"] = mismatches
        return None, "RAW_SYNTHESIS_MISMATCH"
    return modes, "ACCEPT"


def recognize(problem, limits=Limits()):
    """Return a bounded decision. LIMIT is always indeterminate, never NONMEMBER.

    Parameters must be exact built-in dict/int/list/tuple, canonical residues.
    Primality is trial-division certified here, unlike the theorem's assumed
    supplied-prime mode. Unsupported N=1 or r>=N are INVALID_PARAMETERS.
    Limits cap this implementation, not the accepted mathematical theorem.
    """
    result = {"schema": SCHEMA, "status": None, "reason": None,
              "representation": None, "dft": None, "input_sha256": None,
              "validation": {"raw": False, "prime": False, "exact_order": False},
              "phases": [], "assurance": "CANDIDATE_REFERENCE_PENDING_INDEPENDENT_REVIEW"}
    if type(limits) is not Limits or any(type(v) is not int or v < 0 or v > HARD_CAPS[k]
                                       for k, v in asdict(limits).items()):
        result.update(status="INVALID_PARAMETERS", reason="Invalid resource-limit configuration")
        result["ledger"] = {"work_units": 0, "counts": {}, "limit": None, "stage": "configuration"}
        return result
    meter = Meter(limits.max_work_units)
    active = None
    phase_start = 0
    def finish(status, reason):
        result.update(status=status, reason=reason)
        result["ledger"] = {"work_units": meter.used, "counts": dict(sorted(meter.counts.items())),
                            "limit": meter.cap, "stage": meter.stage}
        return result
    try:
        meter.pay("header_checks")
        if type(problem) is not dict or set(problem) != FIELDS:
            return finish("INVALID_INPUT", "Expected exactly N, p, r, omega, x")
        if any(type(problem[k]) is not int for k in ("N", "p", "r", "omega")):
            return finish("INVALID_PARAMETERS", "Header parameters must be integers, not booleans")
        n, p, r, omega = (problem[k] for k in ("N", "p", "r", "omega"))
        if n < 2 or not 1 <= r < n or p < 2 or not 0 <= omega < p:
            return finish("INVALID_PARAMETERS", "Requires N>=2, 1<=r<N, p>=2, canonical omega")
        if n > limits.max_n or r > limits.max_r or p.bit_length() > limits.max_p_bits:
            return finish("LIMIT", "Configured dimension or modulus-bit cap exceeded")
        if (p-1) % n:
            return finish("INVALID_PARAMETERS", "N must divide p-1")
        if type(problem["x"]) not in (list, tuple) or len(problem["x"]) != n:
            return finish("INVALID_INPUT", "Expected exactly N raw coordinates in a list or tuple")
        x = []
        for value in problem["x"]:
            meter.pay("raw_validation_reads")
            if type(value) is not int or not 0 <= value < p:
                return finish("INVALID_INPUT", "Raw coordinates must be canonical integer residues")
            x.append(value)
        result["validation"]["raw"] = True
        meter.stage = "primality"
        divisor = 2
        while divisor*divisor <= p:
            meter.pay("primality_trial_divisions")
            if p % divisor == 0:
                return finish("INVALID_PARAMETERS", "Modulus is composite")
            divisor = 3 if divisor == 2 else divisor+2
        result["validation"]["prime"] = True
        f = Field(p, meter)
        meter.stage = "root_preparation"
        table, value = [], 1
        for k in range(n):
            meter.pay("root_table_writes")
            table.append(value)
            value = f.mul(value, omega)
            meter.pay("root_order_comparisons")
            if k+1 < n and value == 1:
                return finish("INVALID_PARAMETERS", "Supplied root has proper-divisor order")
        if value != 1:
            return finish("INVALID_PARAMETERS", "Supplied root does not close at N")
        result["validation"]["exact_order"] = True
        meter.stage = "input_binding"
        serialized = json.dumps(problem, sort_keys=True, separators=(",", ":")).encode()
        meter.pay("input_binding_bytes", len(serialized))
        result["input_sha256"] = sha256(serialized).hexdigest()
        meter.stage = "center_selection"
        center = None
        for j, value in enumerate(x):
            meter.pay("center_probes")
            if value and center is None:
                center = j
        if center is None:
            meter.stage = "accepted_output"
            meter.pay("raw_synthesis_comparisons", n)
            meter.pay("dft_output_writes", n)
            result["representation"] = {"a": 0, "modes": []}
            result["dft"] = [0]*n
            result["raw_synthesis_checked"] = n
            return finish("MEMBER", "Validated zero input; empty representation")
        result["center"] = center
        result["phase_count"] = n // math.gcd(2, n)
        for phase in range(result["phase_count"]):
            phase_start = meter.used
            active = {"a": phase, "status": "IN_PROGRESS"}
            result["phases"].append(active)
            meter.stage = "phase.eliminant"
            meter.pay("phase_attempts")
            meter.pay("matrix_cells", (r+1)*(r+1))
            matrix = []
            # Direct evaluation of the accepted cyclic eliminant. No factorial
            # determinant expansion or fast polynomial Toeplitz kernel is used.
            for i in range(r+1):
                row = []
                for j in range(r+1):
                    delta = i-j
                    exponent = (-2*phase*(delta*(delta-1)//2)) % n
                    row.append(f.mul(x[(center+delta) % n], table[exponent]))
                matrix.append(row)
            determinant = _determinant(matrix, f)
            active["eliminant_value"] = determinant
            if determinant:
                modes, reason = None, "ELIMINANT_NONZERO"
            else:
                meter.pay("surviving_candidates")
                modes, reason = _try_phase(x, r, phase, table, f, active)
            active["status"] = reason
            active["work_units"] = meter.used-phase_start
            active = None
            if modes is not None:
                # Compute every transform coordinate directly from the original
                # raw array. This intentionally pays N^2 rather than claiming D06.
                meter.stage = "accepted_dense_dft"
                output = []
                for k in range(n):
                    value = 0
                    for j, raw in enumerate(x):
                        value = f.add(value, f.mul(raw, table[(j*k) % n]))
                    meter.pay("dft_output_writes")
                    output.append(value)
                result["representation"] = {"a": phase, "modes": modes}
                result["dft"] = output
                result["raw_synthesis_checked"] = n
                return finish("MEMBER", "Full raw-coordinate synthesis verified")
        return finish("NONMEMBER", "Every canonical phase rejected after complete parameter validation")
    except Exhausted as exc:
        if active is not None:
            active["status"] = "LIMIT"
            active["work_units"] = meter.used-phase_start
        # A discovered representation is withheld until all requested output is
        # complete. No LIMIT response supplies a partial transform or decision.
        result["representation"] = None
        result["dft"] = None
        return finish("LIMIT", str(exc))


def _unique_object(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError("Duplicate JSON key")
        output[key] = value
    return output


def main():
    """One JSON problem on stdin, one JSON result. CLI exit 0 means transport OK."""
    data = sys.stdin.buffer.read(1_048_577)
    if len(data) > 1_048_576:
        answer = {"schema": SCHEMA, "status": "LIMIT", "reason": "JSON byte cap exceeded",
                  "representation": None, "dft": None}
    else:
        try:
            problem = json.loads(data, object_pairs_hook=_unique_object,
                                 parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite number")))
            answer = recognize(problem)
        except (ValueError, UnicodeDecodeError, RecursionError):
            answer = {"schema": SCHEMA, "status": "INVALID_INPUT", "reason": "Malformed finite JSON record",
                      "representation": None, "dft": None}
    print(json.dumps(answer, sort_keys=True))

if __name__ == "__main__":
    main()
