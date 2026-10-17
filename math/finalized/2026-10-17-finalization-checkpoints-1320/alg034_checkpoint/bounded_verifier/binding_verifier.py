"""Fresh bounded ALG-034 exact-input/policy/payload consistency checker.

No producer, historical module, network service, or floating-point operation is
used. A successful record is NOT an execution attestation or error certificate.
See REPORT.md for the trust boundary and deliberately unmet obligations.
"""
from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
from math import comb, gcd, lcm

SCHEMA = "ALG034_BINDING_RECORD_V1"
MAX_N = 64
MAX_RAW_BITS = 1024
MAX_PAYLOAD_BITS = 8192
MAX_META_BITS = 128
MAX_JSON_BYTES = 4 * 1024 * 1024
POLICY_ID = "accepted-all-length-policy:7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062"


class Rejection(ValueError):
    def __init__(self, code, detail):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


def reject(code, detail):
    raise Rejection(code, detail)


def exact_int(x, label, bits=MAX_META_BITS):
    if type(x) is not int:
        reject("GRAMMAR", f"{label} must be a built-in integer, excluding bool")
    if abs(x).bit_length() > bits:
        reject("RESOURCE_LIMIT", f"{label} exceeds this checker's {bits}-bit cap")
    return x


def keys(obj, required, label):
    if type(obj) is not dict or set(obj) != set(required):
        reject("GRAMMAR", f"{label} must have exactly {sorted(required)}")


def strict_loads(text):
    """JSON intake rejects duplicate keys, constants, floats, and huge input."""
    if type(text) is not str:
        reject("GRAMMAR", "JSON input must be a string")
    try:
        byte_length = len(text.encode("utf-8"))
    except UnicodeEncodeError:
        reject("GRAMMAR", "JSON text contains an unpaired Unicode surrogate")
    if byte_length > MAX_JSON_BYTES:
        reject("RESOURCE_LIMIT", "JSON exceeds the 4 MiB intake cap")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                reject("GRAMMAR", f"duplicate JSON key: {key}")
            out[key] = value
        return out

    def bad_number(value):
        reject("GRAMMAR", "floating-point and nonfinite JSON numbers are forbidden")

    def integer(value):
        if len(value.lstrip("-")) > 2500:
            reject("RESOURCE_LIMIT", "JSON integer exceeds 2500 decimal digits")
        return int(value)

    try:
        parsed = json.loads(text, object_pairs_hook=pairs, parse_float=bad_number,
                            parse_constant=bad_number, parse_int=integer)
        canonical_bytes(parsed)  # Apply the same tree/aggregate budget as the API.
        return parsed
    except (json.JSONDecodeError, RecursionError) as error:
        reject("GRAMMAR", f"invalid JSON: {error.__class__.__name__}")


def canonical_bytes(obj):
    # Also used for untrusted nested policy records: reject coercible subclasses,
    # oversized trees, and floats rather than relying on Python equality.
    remaining = [200000]
    byte_budget = [MAX_JSON_BYTES]

    def charge(count):
        byte_budget[0] -= count
        if byte_budget[0] < 0:
            reject("RESOURCE_LIMIT", "canonical serialization exceeds the conservative 4 MiB budget")

    def check(value, depth=0):
        remaining[0] -= 1
        if remaining[0] < 0 or depth > 32:
            reject("RESOURCE_LIMIT", "serialized object exceeds this checker's tree cap")
        kind = type(value)
        if value is None or kind is bool:
            charge(5)
            return
        if kind is int:
            exact_int(value, "serialized integer", MAX_PAYLOAD_BITS)
            charge(abs(value).bit_length() * 30103 // 100000 + 2)
        elif kind is str:
            if len(value) > MAX_JSON_BYTES:
                reject("RESOURCE_LIMIT", "serialized string is too large")
            # At most two six-byte UTF-16 escapes per Unicode code point.
            # Charge before JSON encoding, so repeated huge strings cannot
            # force a massive temporary allocation. This is conservative.
            charge(2 + 12 * len(value))
        elif kind is list:
            charge(2 + len(value))
            for child in value:
                check(child, depth + 1)
        elif kind is dict:
            charge(2 + 2 * len(value))
            for key, child in value.items():
                if type(key) is not str:
                    reject("GRAMMAR", "serialized keys must be built-in strings")
                check(key, depth + 1)
                check(child, depth + 1)
        else:
            reject("GRAMMAR", "unsupported serialized type")

    check(obj)
    return json.dumps(obj, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def digest(domain, obj):
    return sha256(b"ALG034:BINDING:V1\0" + domain.encode("ascii") + b"\0"
                  + canonical_bytes(obj)).hexdigest()


def ceil_log2(n):
    if n < 1:
        reject("INTERNAL", "ceil_log2 requires a positive integer")
    return (n - 1).bit_length()


def vectors(obj, exponent_key, n, bits, label):
    keys(obj, {"real", "imag", exponent_key}, label)
    exponent = exact_int(obj[exponent_key], label + "." + exponent_key)
    result = {exponent_key: exponent}
    for part in ("real", "imag"):
        values = obj[part]
        if type(values) is not list or len(values) != n:
            reject("GRAMMAR", f"{label}.{part} must have exactly {n} entries")
        result[part] = [exact_int(x, f"{label}.{part}[{j}]", bits)
                        for j, x in enumerate(values)]
    return result


def dyadic_value(nums, scale):
    """Canonical exact vector m*2**scale without materializing that power.

    Remove the common power of two from all nonzero signed components. All-zero
    vectors have scale zero. Coordinate order and length are preserved.
    """
    nonzero = [abs(x) for part in ("real", "imag") for x in nums[part] if x]
    if not nonzero:
        shift, scale = 0, 0
    else:
        shift = min((x & -x).bit_length() - 1 for x in nonzero)
        scale += shift
    return {"scale": scale,
            "real": [x >> shift for x in nums["real"]],
            "imag": [x >> shift for x in nums["imag"]]}


def validate_state(state):
    keys(state, {"N", "B", "a", "beta"}, "state")
    s = {key: exact_int(state[key], "state." + key) for key in state}
    n, b, a, beta = (s[key] for key in ("N", "B", "a", "beta"))
    if n < 3 or not 3 <= b <= n or not 0 < a < n or gcd(a, n) != 1 or not 0 <= beta < n:
        reject("DOMAIN", "invalid ALG-034 state")
    if n > MAX_N:
        reject("RESOURCE_LIMIT", f"this standalone verifier only supports N <= {MAX_N}")
    short, long_count = divmod(n, b)
    lengths = [short + (j < long_count) for j in range(b)]
    starts, offset = [], 0
    for length in lengths:
        starts.append(offset)
        offset += length
    return {**s, "h": n % 2, "lengths": lengths, "starts": starts,
            "cycle_to_frequency": [(a * j) % n for j in range(n)],
            "payload_order": "frequency-index-0-through-N-minus-1"}


def trim(poly):
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return out


def monic_divmod(dividend, divisor):
    """Exact integer polynomial long division, ascending coefficient order."""
    remainder, divisor = trim(dividend), trim(divisor)
    if not divisor or divisor[-1] != 1:
        reject("INTERNAL", "divisor is not monic")
    quotient = [0] * max(0, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor):
        offset = len(remainder) - len(divisor)
        factor = remainder[-1]
        quotient[offset] = factor
        for j, coefficient in enumerate(divisor):
            remainder[offset + j] -= factor * coefficient
        remainder = trim(remainder)
    return trim(quotient), remainder


@lru_cache(maxsize=64)
def cyclotomic(order):
    """Construct Phi_order from X^n-1 and proper-divisor polynomials."""
    table = {}
    for n in range(1, order + 1):
        polynomial = [-1] + [0] * (n - 1) + [1]
        for divisor in range(1, n):
            if n % divisor == 0:
                polynomial, remainder = monic_divmod(polynomial, table[divisor])
                if remainder:
                    reject("INTERNAL", "cyclotomic division was inexact")
        table[n] = polynomial
    return tuple(table[order])


def derive_policy(raw, state, t, q, p=None):
    """Recompute the accepted policy; do not infer any producer execution.

    p, if supplied, is the caller's expected actual fractional precision, not a
    certificate-selected value. A nonzero policy defaults to its minimum p.
    """
    s = validate_state(state)
    n, b = s["N"], s["B"]
    raw = vectors(raw, "F", n, MAX_RAW_BITS, "raw")
    t, q = exact_int(t, "t"), exact_int(q, "q")
    if t < 0 or q < ceil_log2(n):
        reject("DOMAIN", "require t >= 0 and q >= ceil(log2 N)")
    if p is not None:
        p = exact_int(p, "expected p")
        if p < 0:
            reject("DOMAIN", "expected p must be nonnegative")
    width = max(abs(x).bit_length() for part in ("real", "imag") for x in raw[part])
    raw_id = digest("raw-input", raw)
    value_id = digest("dyadic-vector-value", dyadic_value(raw, -raw["F"]))
    state_id = digest("canonical-state", s)
    common = {"policy_id": POLICY_ID, "raw_input_sha256": raw_id,
              "input_value_sha256": value_id, "state_sha256": state_id,
              "W": width, "t": t, "q": q}
    if width == 0:
        if p is not None:
            reject("DOMAIN", "zero branch must not declare producer precision")
        return {**common, "outcome": "EXACT_INPUT_ZERO", "p": None,
                "prepass": None, "plan": None}
    order = lcm(2 * n, 4)
    modulus = list(cyclotomic(order))
    blocks = []
    for start, length in zip(s["starts"], s["lengths"]):
        polynomial = [0] * order
        for j in range(length):
            phase = (s["a"] * j * (j - 1) + 2 * (s["a"] * start + s["beta"]) * j
                     + s["h"] * j) % (2 * n)
            exponent = ((order // (2 * n)) * phase) % order
            polynomial[exponent] += raw["real"][start + j]
            polynomial[(exponent + order // 4) % order] += raw["imag"][start + j]
        polynomial = trim(polynomial)
        _, remainder = monic_divmod(polynomial, modulus)
        blocks.append({"g": polynomial, "remainder": remainder,
                       "mass": sum(abs(x) for x in polynomial)})
    prepass = {"L": order, "D": len(modulus) - 1, "modulus": modulus, "blocks": blocks}
    nonzero = [(block["mass"], index) for index, block in enumerate(blocks) if block["remainder"]]
    if not nonzero:
        if p is not None:
            reject("DOMAIN", "projected-zero branch must not declare producer precision")
        return {**common, "outcome": "EXACT_PROJECTED_ZERO", "p": None,
                "prepass": prepass, "plan": None}
    mass, selected = min(nonzero)
    k = ceil_log2(mass)
    g = width + (prepass["D"] - 1) * k
    h_bound = min(comb(n + b - 1, b), 1 << (n - b))
    c_bound = 64 * h_bound * b * (1 << b) * n * n
    c = ceil_log2(c_bound)
    minimum = max(width, c + t + 1, c + q + g + 2)
    if p is None:
        p = minimum
    p = exact_int(p, "selected actual p")
    if p < minimum:
        reject("PRECISION", "expected actual p does not satisfy the accepted one-shot inequalities")
    integer_bits = b + 2 * ceil_log2(n) + 10
    plan = {"selected_block": selected, "A": mass, "K": k, "G": g,
            "H": h_bound, "C": c_bound, "c": c, "p_min": minimum,
            "I": integer_bits, "kappa": width - raw["F"] - p,
            "radius": {"coefficient": c_bound, "scale": width - raw["F"] - p},
            "mu_scale": -raw["F"] - (prepass["D"] - 1) * k,
            "sufficient_65536_bit_width_bound": p + integer_bits <= 65536}
    return {**common, "outcome": "NONZERO_PLAN", "p": p, "prepass": prepass, "plan": plan}


def check_payload(payload, policy, n):
    if policy["outcome"] != "NONZERO_PLAN":
        if payload is not None:
            reject("ZERO_BRANCH", "zero policy stops before producer or adapter payload creation")
        return None
    value = vectors(payload, "kappa", n, MAX_PAYLOAD_BITS, "payload")
    if value["kappa"] != policy["plan"]["kappa"]:
        reject("SCALE", "payload kappa is not W - F - expected p")
    if not any(x for part in ("real", "imag") for x in value[part]):
        reject("ZERO_APPROXIMATION", "zero approximation contradicts a genuine one-shot nonzero run")
    return value


def assemble_record(policy, payload):
    record = {"schema": SCHEMA, "policy": policy,
              "policy_sha256": digest("policy", policy), "payload": payload,
              "payload_grid_sha256": digest("payload-grid", payload),
              "payload_value_sha256": digest("dyadic-vector-value", dyadic_value(payload, payload["kappa"]))
              if payload is not None else None}
    return {**record, "binding_sha256": digest("binding-record", record)}


def make_record(raw, state, t, q, payload=None, p=None):
    """Create a consistency record for data, never a numerical certificate."""
    policy = derive_policy(raw, state, t, q, p)
    return assemble_record(policy, check_payload(payload, policy, state["N"]))


def verify(raw, state, t, q, record, p=None, expected_payload=None):
    """Verify against independently supplied caller context.

    expected_payload, when present, is compared component-by-component with the
    exact grid representation, not merely by digest or dyadic value equivalence.
    This function does not authenticate that reference or who supplied it.
    """
    policy = derive_policy(raw, state, t, q, p)
    keys(record, {"schema", "policy", "policy_sha256", "payload", "payload_grid_sha256",
                  "payload_value_sha256", "binding_sha256"}, "record")
    if record["schema"] != SCHEMA:
        reject("GRAMMAR", "unknown record schema")
    # Fresh policy equality is checked before trusting any record commitment.
    if canonical_bytes(record["policy"]) != canonical_bytes(policy):
        reject("POLICY_MISMATCH", "record policy differs from exact recomputation on caller context")
    payload = check_payload(record["payload"], policy, state["N"])
    expected = assemble_record(policy, payload)
    if canonical_bytes(record) != canonical_bytes(expected):
        reject("BINDING_MISMATCH", "record content or domain-separated commitments disagree")
    exact_reference_match = None
    if expected_payload is not None:
        reference = check_payload(expected_payload, policy, state["N"])
        if payload != reference:
            reject("PAYLOAD_REFERENCE_MISMATCH", "payload differs from external exact-grid reference")
        exact_reference_match = True
    return {"status": "BINDING_CONSISTENT_PRODUCER_UNVERIFIED",
            "policy_outcome": policy["outcome"], "binding_sha256": expected["binding_sha256"],
            "exact_payload_matches_external_reference": exact_reference_match,
            "authenticated_provenance": False, "producer_execution_verified": False,
            "numerical_error_certificate_verified": False, "adapter_invoked": False,
            "downstream_integration_verified": False}


def exact_payload_width(payload):
    """Diagnostic only; does not decide the legacy adapter's full grammar."""
    if payload is None:
        return None
    return max(abs(x).bit_length() for part in ("real", "imag") for x in payload[part])
