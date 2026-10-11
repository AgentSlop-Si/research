#!/usr/bin/env python3
"""Bounded reference verifier for the accepted finite RS/Q08 certificate.

Newly authored implementation. Python standard library only. No source code is
loaded or executed from the evidence directory. This is an analytic certificate
checker, not a numerical root solver or a growing-degree stability theorem.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import re
import sys

# Decimal rendering has a fixed cap independent of the request arithmetic
# budget. Parsing and geometry preparation may construct larger temporaries
# before the next checked arithmetic boundary; no peak-memory bound is claimed.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(50000)

VERSION = "rs-q08-reference-1.1"
REQUEST_FORMAT = "rs-q08-request-v1"
CERTIFICATE_FORMAT = "rs-q08-certificate-v1"
MAX_INPUT_BYTES = 65536
MAX_CERTIFICATE_BYTES = 1048576
MAX_RATIONAL_CHARS = 256
MAX_BITS = 65536
MAX_STEPS = 200000
MAX_N, MAX_A, MAX_D = 128, 16, 31
SOURCE_PINS = {
    "accepted_finite_proof.tex": "3b472a7adb4a157c52c6ad4f8da5e1d94717e360bce8326e8c4d8732cfbcc100",
    "accepted_finite_review.md": "a412af68fbeffe1d6f332280a5b59e3ac74d91481c492232981319c51e0b6033",
    "accepted_example_controls.json": "eaf00162dc76a9296c30193324b199ee4cdd63db2fe3975ca073716b274576c6",
    "accepted_independent_controls.json": "17600b59cff55dc2e8a8d11d102b2243fa1cbc0a8c930987f56ff58d765dc4d4",
    "accepted_scope_archive.zip": "2f2180470328e69db523339981b83918698b62f2589ad750010806b4fc8923ef",
    "accepted_scope_controls.py.txt": "91f960dd2ea9f9ed8583aca33cffea4f519975e7c0424b593d52b7eef70b9889",
    "accepted_review_controls.py.txt": "2c1428f24b5ff380b95aadd2a61279d5bedfc28ad3ca3115149559be2003fdb2",
    "accepted_q08_envelope.md": "02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787",
}
REQUEST_KEYS = {
    "format", "profile", "parameters", "s", "r", "eta", "X",
    "epsilon_min", "geometry_bits", "budget", "source_pins",
    "max_inverse_norm_squared",
}


class Stop(Exception):
    def __init__(self, status, reason):
        self.status, self.reason = status, reason
        super().__init__(reason)


def reject(reason):
    raise Stop("REJECT", reason)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def strict_loads(data, maximum=MAX_INPUT_BYTES):
    """Bounded JSON, with no duplicate keys, floating numbers, or NaN/Infinity."""
    if not isinstance(data, bytes) or len(data) > maximum:
        reject("INPUT_SIZE_LIMIT")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                reject("DUPLICATE_JSON_KEY")
            out[key] = value
        return out

    def forbidden(_):
        reject("NONINTEGER_JSON_NUMBER")

    def bounded_int(text):
        if len(text) > 10:
            reject("JSON_INTEGER_SIZE_LIMIT")
        return int(text)

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                          parse_float=forbidden, parse_constant=forbidden,
                          parse_int=bounded_int)
    except (ValueError, UnicodeError, RecursionError):
        reject("MALFORMED_JSON")


class Arithmetic:
    """Exact fractions; fail closed on a deterministic bit/work budget.

    Cross products are counted before comparisons. Every primitive operation
    checks unreduced integer intermediates at its explicit check boundaries.
    The bit budget is a checked-arithmetic admission limit, not a hard limit
    on allocation or parsing/geometry temporaries. No unchecked over-budget
    rational is admitted to a certified answer.
    """
    def __init__(self, bits, steps):
        self.bits, self.steps = bits, steps
        self.counts = Counter()
        self.total = 0
        self.max_integer_bits = 0
        self.stage = "input"

    def tick(self, kind):
        self.counts[f"{self.stage}:{kind}"] += 1
        self.total += 1
        if self.total > self.steps:
            raise Stop("PRECISION_EXHAUSTED", "ARITHMETIC_WORK_BUDGET")

    def ints(self, *values):
        width = max((abs(x).bit_length() for x in values), default=0)
        self.max_integer_bits = max(self.max_integer_bits, width)
        if width > self.bits:
            raise Stop("PRECISION_EXHAUSTED", "EXACT_INTEGER_BIT_BUDGET")

    def make(self, numerator, denominator=1):
        self.tick("rational_normalization")
        self.ints(numerator, denominator)
        if denominator == 0:
            reject("ZERO_DENOMINATOR")
        return Fraction(numerator, denominator)

    def parse(self, value):
        if (not isinstance(value, str) or len(value) > MAX_RATIONAL_CHARS
                or re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value) is None):
            reject("NONCANONICAL_RATIONAL")
        parts = value.split("/")
        a = self.make(int(parts[0]), int(parts[1]) if len(parts) == 2 else 1)
        if str(a) != value:
            reject("NONCANONICAL_RATIONAL")
        return a

    def add(self, a, b):
        self.tick("add")
        a, b = Fraction(a), Fraction(b)
        x, y, d = a.numerator*b.denominator, b.numerator*a.denominator, a.denominator*b.denominator
        self.ints(x, y, d, x+y)
        return self.make(x+y, d)

    def neg(self, a):
        self.tick("negate")
        return self.make(-a.numerator, a.denominator)

    def sub(self, a, b):
        return self.add(a, self.neg(Fraction(b)))

    def mul(self, a, b):
        self.tick("multiply")
        a, b = Fraction(a), Fraction(b)
        return self.make(a.numerator*b.numerator, a.denominator*b.denominator)

    def div(self, a, b):
        self.tick("divide")
        a, b = Fraction(a), Fraction(b)
        return self.make(a.numerator*b.denominator, a.denominator*b.numerator)

    def power(self, a, exponent):
        self.tick("power")
        if type(exponent) is not int or exponent < 0 or exponent > 10000:
            reject("INTERNAL_EXPONENT_DOMAIN")
        value, a = Fraction(1), Fraction(a)
        while exponent:
            if exponent & 1:
                value = self.mul(value, a)
            exponent //= 2
            if exponent:
                a = self.mul(a, a)
        return value

    def cmp(self, a, b):
        self.tick("compare")
        a, b = Fraction(a), Fraction(b)
        left, right = a.numerator*b.denominator, b.numerator*a.denominator
        self.ints(left, right)
        return (left > right) - (left < right)

    def sqrt_enclosure(self, a, precision):
        """Dyadic floor/ceiling sqrt, proved with integer square comparisons."""
        self.tick("sqrt_enclosure")
        if self.cmp(a, 0) < 0:
            reject("NEGATIVE_SQRT")
        scale = 1 << precision
        scaled_num = a.numerator * scale * scale
        self.ints(scale, scaled_num, a.denominator)
        self.tick("integer_sqrt")
        lower_int = isqrt(scaled_num // a.denominator)
        self.ints(lower_int*lower_int*a.denominator)
        upper_int = lower_int if lower_int*lower_int*a.denominator == scaled_num else lower_int+1
        low, high = self.make(lower_int, scale), self.make(upper_int, scale)
        if self.cmp(self.power(low, 2), a) > 0 or self.cmp(self.power(high, 2), a) < 0:
            reject("INTERNAL_SQRT_ENCLOSURE")
        return low, high

    def costs(self):
        return {"arithmetic_steps": self.total,
                "maximum_integer_bits_observed": self.max_integer_bits,
                "operations_by_stage": dict(sorted(self.counts.items())),
                "bit_budget": self.bits, "step_budget": self.steps}


def keys(obj, expected, name):
    if type(obj) is not dict or set(obj) != expected:
        reject(f"{name}_FIELDS")


def verify_sources(directory, progress=None):
    total = 0
    for name, digest in sorted(SOURCE_PINS.items()):
        try:
            with (Path(directory) / name).open("rb") as stream:
                data = stream.read(1048577)
        except OSError:
            reject("SOURCE_UNAVAILABLE:" + name)
        if len(data) > 1048576:
            reject("SOURCE_SIZE_LIMIT:" + name)
        total += len(data)
        if progress is not None:
            progress["source_bytes_hashed"] = total
            progress["source_files_read"] += 1
        if hashlib.sha256(data).hexdigest() != digest:
            reject("SOURCE_HASH_MISMATCH:" + name)
    return total


def _geometry(req, ar):
    p, profile = req["parameters"], req["profile"]
    A, d, b = p["A"], p["d"], p["b"]
    ar.stage = "guard_and_geometry_preparation"
    if profile == "separated-2-3-0":
        if (A, d, b) != (2, 3, 0):
            reject("PROFILE_PARAMETER_MISMATCH")
        # Exact P_alpha directions +/-alpha/sqrt(3), c modulus 9.
        radius, gap = ar.make(3, 5), ar.make(1)
        if ar.cmp(ar.power(radius, 2), ar.make(1, 3)) < 0 or ar.cmp(ar.power(gap, 2), ar.make(4, 3)) > 0:
            reject("INTERNAL_EXACT_GEOMETRY")
        return [{"label": "ordinary", "count": 3, "m": 2,
                 "radius": radius, "gap": gap, "c": ar.make(9)}], ar.make(1), 3, ["G=1; Disc(G)=Res(F,G)=1", "center_distance_squared=3"]
    if profile == "overlap-1-3-1":
        if (A, d, b) != (1, 3, 1):
            reject("PROFILE_PARAMETER_MISMATCH")
        # In Q[w]/(w^2+w+1), tau=1-w, N(tau)=1-(-1)+1=3.
        # g=U=1; J_2=y^2-tau; N(Disc(J_2))=N(4*tau)=48>0.
        tau_norm = ar.add(ar.sub(ar.make(1), ar.make(-1)), ar.make(1))
        disc_norm = ar.mul(16, tau_norm)
        if ar.cmp(tau_norm, 3) != 0 or ar.cmp(disc_norm, 0) <= 0:
            reject("OVERLAP_GUARD_FAILURE")
        radius, gap = ar.make(7, 8), ar.make(1)
        if ar.cmp(ar.power(radius, 4), ar.make(1, 3)) < 0 or ar.cmp(ar.power(gap, 4), ar.make(16, 3)) > 0:
            reject("INTERNAL_EXACT_GEOMETRY")
        return [
            {"label": "exceptional", "count": 1, "m": 2, "radius": radius, "gap": gap, "c": ar.make(3)},
            {"label": "ordinary", "count": 2, "m": 1, "radius": ar.make(0), "gap": None, "c": ar.make(3)},
        ], ar.make(1), 4, ["U=g=1; Disc(U)=Res(F,U)=1", "tau=1-w; norm(tau)=3", "norm(Disc(J_2))=48", "ordinary |c|=3*sqrt(3)>=3", "center_distance_squared=3"]
    if profile == "b0-hermite":
        if b != 0:
            raise Stop("INDETERMINATE", "UNSUPPORTED_RESIDUAL_OR_OVERLAP_GUARDS")
        if A == 1:
            radius, gap = ar.make(0), None
        else:
            _, radius = ar.sqrt_enclosure(ar.make(4*(A-1), d), req["geometry_bits"])
            # pi > 3 gives delta >= 3/sqrt(d*(A+1/2)).
            gap, _ = ar.sqrt_enclosure(ar.make(18, d*(2*A+1)), req["geometry_bits"])
            if ar.cmp(gap, 0) <= 0:
                raise Stop("PRECISION_EXHAUSTED", "GEOMETRY_RESOLUTION")
        # sin(x)>=2x/pi on [0,pi/2], so 2sin(pi/d)>=4/d.
        center = ar.make(4, d)
        exponent = ((A*d)**2//4 + d-1)//d
        return [{"label": "ordinary", "count": d, "m": A,
                 "radius": radius, "gap": gap, "c": ar.power(ar.make(d), A)}], center, exponent, ["G=1; Disc(G)=Res(F,G)=1", "accepted Hermite radius and gap bounds", "pi>3; sin(pi/d)>=2/d"]
    raise Stop("INDETERMINATE", "UNSUPPORTED_PROFILE")


def evaluate(request, source_directory):
    """Return a deterministic result; only CERTIFIED is a positive certificate."""
    ar, source_bytes, input_bytes = None, 0, 0
    source_progress = {"source_bytes_hashed": 0, "source_files_read": 0}
    try:
        # Reparse canonical bytes to impose identical checks on Python API use.
        try:
            raw = canonical(request)
        except (TypeError, ValueError, RecursionError):
            reject("NON_JSON_REQUEST")
        input_bytes = len(raw)
        req = strict_loads(raw)
        keys(req, REQUEST_KEYS, "REQUEST")
        if req["format"] != REQUEST_FORMAT:
            reject("REQUEST_FORMAT")
        keys(req["parameters"], {"A", "d", "b", "embedding_index"}, "PARAMETER")
        keys(req["budget"], {"max_bits", "max_steps"}, "BUDGET")
        bits, steps = req["budget"]["max_bits"], req["budget"]["max_steps"]
        if type(bits) is not int or not 32 <= bits <= MAX_BITS or type(steps) is not int or not 1 <= steps <= MAX_STEPS:
            reject("BUDGET_DOMAIN")
        ar = Arithmetic(bits, steps)
        if req["source_pins"] != SOURCE_PINS:
            reject("SOURCE_PIN_SET_MISMATCH")
        source_bytes = verify_sources(source_directory, source_progress)
        p = req["parameters"]
        if any(type(v) is not int for v in p.values()):
            reject("NONINTEGER_PARAMETER")
        A, d, b, embedding = (p[k] for k in ("A", "d", "b", "embedding_index"))
        if A < 1 or d < 3 or d % 2 != 1 or b < 0 or b >= d:
            reject("PARAMETER_DOMAIN")
        if not 1 <= embedding < d or gcd(embedding, d) != 1:
            reject("NONPRIMITIVE_EMBEDDING")
        n = A*d+b
        if A > MAX_A or d > MAX_D or n > MAX_N:
            raise Stop("INDETERMINATE", "SUPPORTED_FINITE_PARAMETER_CAP")
        if type(req["geometry_bits"]) is not int or not 0 <= req["geometry_bits"] <= 64:
            reject("GEOMETRY_PRECISION_DOMAIN")
        if type(req["profile"]) is not str:
            reject("PROFILE_TYPE")
        s, r, eta, X, emin = (ar.parse(req[k]) for k in ("s", "r", "eta", "X", "epsilon_min"))
        target = req["max_inverse_norm_squared"]
        if target is not None:
            target = ar.parse(target)
            if ar.cmp(target, 0) <= 0:
                reject("NORM_TARGET_DOMAIN")
        if not (ar.cmp(0, r) < 0 and ar.cmp(r, s) < 0 and ar.cmp(s, 1) < 0):
            reject("RADIUS_DOMAIN")
        if ar.cmp(eta, 0) <= 0 or ar.cmp(X, 0) < 0:
            reject("TUBE_DOMAIN")
        if ar.cmp(emin, 0) <= 0 or ar.cmp(emin, r) > 0:
            reject("ANNULUS_DOMAIN")
        groups, center_gap, majorant_exponent, guards = _geometry(req, ar)
        if sum(g["count"]*g["m"] for g in groups) != n:
            reject("INTERNAL_ROOT_COUNT")
        for g in groups:
            if ar.cmp(X, ar.add(g["radius"], eta)) < 0:
                raise Stop("INDETERMINATE", "DIRECTION_DISK_NOT_COVERED")
            if g["m"] > 1 and ar.cmp(ar.mul(2, eta), g["gap"]) >= 0:
                raise Stop("INDETERMINATE", "DIRECTION_DISKS_NOT_SEPARATED")
        ar.stage = "cauchy_rouche"
        # Formula (7), using an integer power >= floor(n^2/4)/d.
        # The two pinned examples preserve their printed conservative powers.
        B = ar.mul(ar.power(ar.add(1, ar.power(s, 2)), majorant_exponent),
                   ar.power(ar.add(2, ar.mul(s, X)), n))
        local = []
        for g in groups:
            m = g["m"]
            mu = ar.mul(g["c"], eta)
            gamma = None
            if m > 1:
                mu = ar.mul(mu, ar.power(ar.sub(g["gap"], eta), m-1))
                gamma = ar.sub(g["gap"], ar.mul(2, eta))
            E = ar.div(ar.mul(B, r), ar.mul(ar.power(s, m), ar.sub(s, r)))
            threshold = ar.div(ar.mul(mu, ar.power(s, m+1)), ar.add(B, ar.mul(mu, ar.power(s, m))))
            passed = ar.cmp(E, mu) < 0
            local.append({"label": g["label"], "count": g["count"], "multiplicity": m,
                          "direction_radius_upper": str(g["radius"]),
                          "direction_gap_lower": None if g["gap"] is None else str(g["gap"]),
                          "leading_modulus_lower": str(g["c"]), "mu_lower": str(mu),
                          "E_upper": str(E), "strict_r_threshold": str(threshold),
                          "gamma_lower": None if gamma is None else str(gamma), "passed": passed})
            g["gamma"] = gamma
        Delta = ar.sub(center_gap, ar.mul(2, ar.mul(r, X)))
        R = ar.add(1, ar.mul(r, X))
        bounds = {"n": n, "majorant_integer_exponent": majorant_exponent,
                  "B_upper": str(B), "local": local, "center_gap_lower": str(center_gap),
                  "Delta_lower": str(Delta), "root_modulus_upper": str(R),
                  "guard_checks": guards}
        if not all(item["passed"] for item in local):
            return _result("INDETERMINATE", "STRICT_ROUCHE_TEST_NOT_MET", ar, source_bytes, input_bytes, bounds)
        if ar.cmp(Delta, 0) <= 0:
            return _result("INDETERMINATE", "CROSS_CLUSTER_DISKS_NOT_SEPARATED", ar, source_bytes, input_bytes, bounds)
        ar.stage = "q08_norm_envelope"
        factors = []
        for g in groups:
            denom = ar.power(Delta, n-g["m"])
            if g["m"] > 1:
                denom = ar.mul(denom, ar.power(ar.mul(emin, g["gamma"]), g["m"]-1))
            factors.append(ar.div(1, denom))
        worst = factors[0]
        for value in factors[1:]:
            if ar.cmp(value, worst) > 0:
                worst = value
        inv2 = ar.mul(n, ar.mul(ar.power(ar.add(1, R), 2*(n-1)), ar.power(worst, 2)))
        R2, term, series = ar.power(R, 2), ar.make(1), ar.make(0)
        for _ in range(n):
            series = ar.add(series, term)
            term = ar.mul(term, R2)
        forward2 = ar.mul(n, series)
        condition2 = ar.mul(inv2, forward2)
        bounds.update({"inverse_norm_squared_upper": str(inv2),
                       "forward_norm_squared_upper": str(forward2),
                       "condition_number_squared_upper": str(condition2),
                       "certified_root_count": n,
                       "applicability": {"tubes": "0 < |epsilon| <= r", "norms": "epsilon_min <= |epsilon| <= r", "all_complex_arguments": True}})
        if target is not None and ar.cmp(inv2, target) > 0:
            return _result("INDETERMINATE", "REQUESTED_NORM_CEILING_NOT_CERTIFIED", ar, source_bytes, input_bytes, bounds)
        return _result("CERTIFIED", "FINITE_ANALYTIC_TUBES_AND_Q08_ENVELOPE", ar, source_bytes, input_bytes, bounds)
    except Stop as exc:
        return _result(exc.status, exc.reason, ar, source_progress["source_bytes_hashed"], input_bytes)


def _result(status, reason, ar, source_bytes, input_bytes, bounds=None):
    code_bytes = Path(__file__).read_bytes()
    out = {"checker_version": VERSION, "checker_sha256": hashlib.sha256(code_bytes).hexdigest(), "status": status, "reason": reason,
           "implementation_review": "PENDING_INDEPENDENT_REVIEW",
           "costs": {"canonical_input_bytes": input_bytes, "source_bytes_hashed": source_bytes,
                     "source_files_required": len(SOURCE_PINS),
                     "checker_bytes_hashed": len(code_bytes),
                     "cost_model": "byte volumes and exact arithmetic primitive counts; no bit-complexity or wall-time claim",
                     "all_preparation_repeated_on_each_validation": True}}
    if ar is not None:
        out["costs"].update(ar.costs())
    if bounds is not None:
        out["bounds"] = bounds
    return out


def make_certificate(request, source_directory):
    result = evaluate(request, source_directory)
    try:
        raw = canonical(request)
    except (TypeError, ValueError, RecursionError):
        return {"format": "rs-q08-certificate-error-v1", "result": result}
    return {"format": CERTIFICATE_FORMAT, "request": request,
            "request_sha256": hashlib.sha256(raw).hexdigest(),
            "result": result}


def verify_certificate(certificate, source_directory):
    """Recompute everything, then compare canonical bytes including cost trace."""
    try:
        keys(certificate, {"format", "request", "request_sha256", "result"}, "CERTIFICATE")
        if certificate["format"] != CERTIFICATE_FORMAT:
            reject("CERTIFICATE_FORMAT")
        expected = make_certificate(certificate["request"], source_directory)
        if canonical(expected) != canonical(certificate):
            reject("CERTIFICATE_MISMATCH")
        return {"verified": True, "status": expected["result"]["status"],
                "reason": expected["result"]["reason"]}
    except Stop as exc:
        return {"verified": False, "status": exc.status, "reason": exc.reason}
    except (TypeError, ValueError, RecursionError):
        return {"verified": False, "status": "REJECT", "reason": "NON_JSON_CERTIFICATE"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("certify", "verify"))
    parser.add_argument("input", type=Path)
    parser.add_argument("--sources", type=Path, default=Path(__file__).with_name("sources"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        maximum = MAX_INPUT_BYTES if args.operation == "certify" else MAX_CERTIFICATE_BYTES
        with args.input.open("rb") as stream:
            value = strict_loads(stream.read(maximum+1), maximum)
        out = make_certificate(value, args.sources) if args.operation == "certify" else verify_certificate(value, args.sources)
    except Stop as exc:
        out = {"status": exc.status, "reason": exc.reason}
    except OSError:
        out = {"status": "REJECT", "reason": "INPUT_IO_ERROR"}
    data = canonical(out) + b"\n"
    if args.output:
        args.output.write_bytes(data)
    else:
        sys.stdout.buffer.write(data)
    status = out.get("result", out)["status"]
    return {"CERTIFIED": 0, "REJECT": 2, "INDETERMINATE": 3, "PRECISION_EXHAUSTED": 4}[status]


if __name__ == "__main__":
    raise SystemExit(main())
