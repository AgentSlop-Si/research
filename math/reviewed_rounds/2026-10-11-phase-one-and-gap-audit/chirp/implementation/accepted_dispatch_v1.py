"""Bounded candidate v2: metered non-dyadic guard before sparse frontend setup.

Source: accepted cyclic theorem, sections 5/7, specialized to a=0, t=r.
The reviewed dense reference is vendored byte-for-byte as reference_v1.py.
It is called with the remaining work budget. Non-dyadic inputs route directly
after a metered structural guard; rejected dyadic attempts still pay repeated setup.
No fast common-chirp eliminant or min(B,H) dispatcher is claimed here.
"""
from collections import Counter
from dataclasses import asdict, replace
from hashlib import sha256
import json
import sys

import reference_v1 as ref

Limits = ref.Limits
REFERENCE_SHA256 = "7d263f616526bd1123658771afc73bb44fc15282ef8ee0131e48ade0b59d18b7"
IMPLEMENTATION = "chirp-metered-nondyadic-dispatch-candidate-v2"
ACCEPTED_FRONTEND_SHA256 = "e9fdd8c89d2e1e8c1569f91cea16159dce690da0793cef78b0d699cac2e200e5"


class Meter(ref.Meter):
    """Same unit budget as reference, with additional new-kernel write events."""
    def __init__(self, cap):
        super().__init__(cap)
        self.stages = Counter()

    def pay(self, category, amount=1):
        super().pay(category, amount)
        self.stages[self.stage] += amount


def _append(array, value, meter, category="field_entry_writes"):
    meter.pay(category)
    array.append(value)


def _copy(array, meter):
    meter.pay("field_entry_writes", len(array))
    return array[:]


def _bm(sequence, f):
    """Ordinary Berlekamp--Massey: C[0]=1, backward connection coefficients."""
    mtr = f.meter
    mtr.pay("field_entry_writes", 3)
    c, previous, discrepancy_scale = [1], [1], 1
    order, shift = 0, 1
    for k in range(len(sequence)):
        mtr.pay("bm_steps")
        discrepancy = sequence[k]
        for i in range(1, order+1):
            ci = c[i] if i < len(c) else 0
            discrepancy = f.add(discrepancy, f.mul(ci, sequence[k-i]))
        if discrepancy == 0:
            shift += 1
            continue
        factor = f.mul(discrepancy, f.inverse(discrepancy_scale))
        old = _copy(c, mtr)
        while len(c) < len(previous)+shift:
            _append(c, 0, mtr)
        for j, value in enumerate(previous):
            updated = f.sub(c[j+shift], f.mul(factor, value))
            mtr.pay("field_entry_writes")
            c[j+shift] = updated
        if 2*order <= k:
            order = k+1-order
            previous, discrepancy_scale, shift = old, discrepancy, 1
            mtr.pay("field_entry_writes")
        else:
            shift += 1
    while len(c) > 1 and c[-1] == 0:
        mtr.pay("coefficient_trim_tests")
        c.pop()
    return order, c


def _pruned_fft(support, n, table, f, trace):
    """Positive-sign radix-2 DIT; ONLY nonempty input-support subtrees run.

    support contains distinct (input_index, nonzero_coefficient) pairs.
    All FFT nodes use powers from the already validated order-N root table.
    No dense FFT is computed and subsequently labeled pruned.
    """
    mtr, full_n = f.meter, len(table)
    trace.update(input_support=len(support), length=n, calls_by_depth={},
                 output_slots_by_depth={}, butterflies=0)

    def run(pairs, size, depth):
        mtr.pay("pruned_active_nodes")
        trace["calls_by_depth"][depth] = trace["calls_by_depth"].get(depth, 0)+1
        trace["output_slots_by_depth"][depth] = trace["output_slots_by_depth"].get(depth, 0)+size
        if size == 1:
            if len(pairs) != 1 or pairs[0][0] != 0:
                raise ArithmeticError("Invalid internal sparse support")
            mtr.pay("field_entry_writes")
            return [pairs[0][1]]
        evens, odds = [], []
        for index, value in pairs:
            mtr.pay("sparse_support_routes")
            mtr.pay("field_entry_writes")
            (odds if index & 1 else evens).append((index//2, value))
        half = size//2
        even = run(evens, half, depth+1) if evens else None
        odd = run(odds, half, depth+1) if odds else None
        # Charge zero initialization as well as every subsequent output write.
        mtr.pay("field_entry_writes", size)
        output = [0]*size
        for k in range(half):
            mtr.pay("pruned_combine_positions")
            trace["butterflies"] += 1
            if odd is None:
                low = high = even[k]
            else:
                mtr.pay("root_table_reads")
                rotated = f.mul(table[(full_n//size)*k], odd[k])
                if even is None:
                    low, high = rotated, f.sub(0, rotated)
                else:
                    low, high = f.add(even[k], rotated), f.sub(even[k], rotated)
            mtr.pay("field_entry_writes", 2)
            output[k], output[k+half] = low, high
        return output

    if not support:
        mtr.pay("field_entry_writes", n)
        trace["empty_output_writes"] = n
        return [0]*n
    return run(support, n, 0)


def _horner(coefficients, z, f):
    value = 0
    for c in reversed(coefficients):
        value = f.add(f.mul(value, z), c)
    return value


def _sparse_attempt(x, r, table, f, detail):
    n, mtr = len(x), f.meter
    mtr.stage = "sparse.bm"
    mtr.pay("sparse_attempts")
    moments = []
    for j in range(2*r):
        mtr.pay("periodic_prefix_reads")
        _append(moments, x[j % n], mtr)
    s, c = _bm(moments, f)
    detail["bm_order"], detail["connection_degree"] = s, len(c)-1
    if s > r or len(c)-1 != s or c[0] != 1:
        return None, "BM_ORDER_OR_DEGREE_REJECT"

    mtr.stage = "sparse.grid_roots"
    support = []
    for j, value in enumerate(c):
        mtr.pay("coefficient_support_tests")
        if value:
            _append(support, (j, value), mtr)
    detail["root_fft"] = {}
    values = _pruned_fft(support, n, table, f, detail["root_fft"])
    roots = []
    for v, value in enumerate(values):
        mtr.pay("grid_root_tests")
        if value == 0:
            _append(roots, v, mtr, "root_index_writes")
    detail["grid_root_count"] = len(roots)
    if len(roots) != s:
        return None, "GRID_ROOT_COUNT_REJECT"

    mtr.stage = "sparse.weights"
    numerator, derivative = [], []
    for k in range(s):
        value = 0
        for i in range(k+1):
            value = f.add(value, f.mul(c[i], x[k-i]))
        _append(numerator, value, mtr)
    for j in range(1, s+1):
        _append(derivative, f.mul(j % f.p, c[j]), mtr)
    modes = []
    for v in roots:
        b = (-v) % n
        mtr.pay("root_table_reads", 2)
        z, node = table[v], table[b]
        denominator = _horner(derivative, z, f)
        if denominator == 0:
            raise ArithmeticError("Distinct full-degree roots must have nonzero derivative")
        weight = f.mul(f.sub(0, f.mul(node, _horner(numerator, z, f))), f.inverse(denominator))
        mtr.pay("weight_nonzero_tests")
        if weight:
            _append(modes, {"b": b, "gamma": weight}, mtr)

    mtr.stage = "sparse.full_raw_synthesis"
    support = []
    for mode in modes:
        _append(support, (mode["b"], mode["gamma"]), mtr)
    detail["synthesis_fft"] = {}
    synthesized = _pruned_fft(support, n, table, f, detail["synthesis_fft"])
    mismatches = 0
    for j, value in enumerate(synthesized):
        mtr.pay("raw_synthesis_comparisons")
        mismatches += value != x[j]
    detail["raw_synthesis_checked"] = n
    detail["raw_synthesis_mismatches"] = mismatches
    if mismatches:
        return None, "FULL_RAW_SYNTHESIS_REJECT"
    return modes, "ACCEPT"


def _known_non_dyadic(problem, max_n, meter):
    """A paid structural guard, never an input-validity or signal decision.

    Only exact built-in dict/int operations are used. Every type/length/key
    check, header read, range check, and dyadic test introduced here is charged
    before execution. Bounds precede the bit test. All other validation is
    left to the unchanged reference or accepted frontend, as appropriate.
    """
    meter.pay("dispatch_problem_type_checks")
    if type(problem) is not dict:
        return False
    meter.pay("dispatch_record_length_reads")
    if len(problem) != 5:
        return False
    meter.pay("dispatch_N_presence_checks")
    if "N" not in problem:
        return False
    meter.pay("dispatch_N_reads")
    n = problem["N"]
    meter.pay("dispatch_N_type_checks")
    if type(n) is not int:
        return False
    meter.pay("dispatch_N_lower_bound_checks")
    if n < 2:
        return False
    meter.pay("dispatch_N_upper_bound_checks")
    if n > max_n:
        return False
    meter.pay("dispatch_dyadic_tests")
    return bool(n & (n-1))


def recognize(problem, limits=Limits()):
    """Same mathematical core and hard caps as the reviewed dense reference.

    A metered exact structural guard routes known non-dyadic N directly to
    the unchanged dense reference. It does not validate the remaining input.
    Dyadic t=r attempts and their fully paid rejected-attempt fallback are
    unchanged. Every route shares the original cap, minus all guard work.
    """
    result = {"schema": ref.SCHEMA, "implementation": IMPLEMENTATION,
              "status": None, "reason": None, "representation": None,
              "dft": None, "input_sha256": None, "phases": [],
              "validation": {"raw": False, "prime": False, "exact_order": False},
              "assurance": "CANDIDATE_FRONTEND_PENDING_INDEPENDENT_REVIEW",
              "frontend": {"status": "NOT_STARTED"}, "route": "frontend"}
    if type(limits) is not Limits or any(type(v) is not int or v < 0 or v > ref.HARD_CAPS[k]
                                       for k, v in asdict(limits).items()):
        result.update(status="INVALID_PARAMETERS", reason="Invalid resource-limit configuration")
        result["ledger"] = {"work_units": 0, "counts": {}, "limit": None, "stage": "configuration"}
        return result
    meter = Meter(limits.max_work_units)

    def snapshot():
        return {"work_units": meter.used, "counts": dict(sorted(meter.counts.items())),
                "stages": dict(sorted(meter.stages.items())), "limit": meter.cap, "stage": meter.stage}

    def finish(status, reason):
        result.update(status=status, reason=reason)
        result["ledger"] = snapshot()
        return result

    def run_reference(route):
        front_ledger = snapshot()
        fallback_limits = replace(limits, max_work_units=meter.cap-meter.used)
        fallback = ref.recognize(problem, fallback_limits)
        fallback_ledger = fallback["ledger"]
        result.update(fallback)
        result.update(implementation=IMPLEMENTATION, route=route,
                      assurance="CANDIDATE_FRONTEND_PENDING_INDEPENDENT_REVIEW",
                      reference_source_sha256=REFERENCE_SHA256)
        counts = Counter(front_ledger["counts"])
        counts.update(fallback_ledger["counts"])
        result["ledger"] = {"work_units": front_ledger["work_units"]+fallback_ledger["work_units"],
                            "counts": dict(sorted(counts.items())), "limit": meter.cap,
                            "stage": "fallback."+fallback_ledger["stage"],
                            "frontend": front_ledger, "fallback": fallback_ledger}
        return result

    try:
        meter.stage = "dispatch"
        if _known_non_dyadic(problem, limits.max_n, meter):
            result["frontend"]["status"] = "SKIPPED_NON_DYADIC"
            return run_reference("dense_reference_direct")
        meter.stage = "validation"
        meter.pay("header_checks")
        if type(problem) is not dict or set(problem) != ref.FIELDS:
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
            _append(x, value, meter)
        result["validation"]["raw"] = True
        meter.stage = "primality"
        divisor = 2
        while divisor*divisor <= p:
            meter.pay("primality_trial_divisions")
            if p % divisor == 0:
                return finish("INVALID_PARAMETERS", "Modulus is composite")
            divisor = 3 if divisor == 2 else divisor+2
        result["validation"]["prime"] = True
        f = ref.Field(p, meter)
        meter.stage = "root_preparation"
        table, value = [], 1
        for k in range(n):
            _append(table, value, meter, "root_table_writes")
            value = f.mul(value, omega)
            meter.pay("root_order_comparisons")
            if k+1 < n and value == 1:
                return finish("INVALID_PARAMETERS", "Supplied root has proper-divisor order")
        if value != 1:
            return finish("INVALID_PARAMETERS", "Supplied root does not close at N")
        result["validation"]["exact_order"] = True
        meter.stage = "input_binding"
        encoded = json.dumps(problem, sort_keys=True, separators=(",", ":")).encode()
        meter.pay("input_binding_bytes", len(encoded))
        result["input_sha256"] = sha256(encoded).hexdigest()

        modes = None
        if n & (n-1):
            result["frontend"]["status"] = "SKIPPED_NON_DYADIC"
        else:
            result["frontend"]["status"] = "IN_PROGRESS"
            modes, reason = _sparse_attempt(x, r, table, f, result["frontend"])
            result["frontend"]["status"] = reason
        if modes is not None:
            meter.stage = "sparse.accepted_scatter"
            # Positive-sign DFT: the mode gamma * omega^(b*j) lands at k=-b.
            meter.pay("dft_output_writes", n)
            output = [0]*n
            for mode in modes:
                value = f.mul(n % p, mode["gamma"])
                meter.pay("dft_output_writes")
                output[(-mode["b"]) % n] = value
            result["representation"] = {"a": 0, "modes": modes}
            result["dft"] = output
            result["raw_synthesis_checked"] = n
            result["route"] = "sparse_frontend"
            return finish("MEMBER", "Dyadic phase-0 sparse representation verified against every raw coordinate")

        # A real dyadic sparse rejection still pays all previous work and
        # repeated setup. The reference bytes and fallback call are unchanged.
        return run_reference("dense_reference_fallback")
    except ref.Exhausted as exc:
        if result["frontend"]["status"] == "IN_PROGRESS":
            result["frontend"]["status"] = "LIMIT"
        result["representation"], result["dft"] = None, None
        return finish("LIMIT", str(exc))


def main():
    data = sys.stdin.buffer.read(1_048_577)
    if len(data) > 1_048_576:
        answer = {"schema": ref.SCHEMA, "status": "LIMIT", "reason": "JSON byte cap exceeded",
                  "representation": None, "dft": None}
    else:
        try:
            problem = json.loads(data, object_pairs_hook=ref._unique_object,
                                 parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite number")))
            answer = recognize(problem)
        except (ValueError, UnicodeDecodeError, RecursionError):
            answer = {"schema": ref.SCHEMA, "status": "INVALID_INPUT", "reason": "Malformed finite JSON record",
                      "representation": None, "dft": None}
    print(json.dumps(answer, sort_keys=True))


if __name__ == "__main__":
    main()
