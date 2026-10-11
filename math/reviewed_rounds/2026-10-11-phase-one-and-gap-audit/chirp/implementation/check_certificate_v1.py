"""Fresh structurally separate decision checker; no recognizer imports.

Checks mathematical decisions by direct Fourier coefficients / synthesis.
It does not authenticate runtime telemetry or certify optimized complexity.
This is same-author differential checking, not independent human/agent review.
"""
import hashlib
import json
import math

class CheckLimit(Exception):
    pass


def check(problem, certificate, max_terms=2_000_000):
    used = 0
    def pay(amount=1):
        nonlocal used
        if used+amount > max_terms:
            raise CheckLimit()
        used += amount
    def output(status, reason):
        return {"status": status, "reason": reason, "checked_terms": used}
    try:
        if type(max_terms) is not int or not 0 <= max_terms <= 20_000_000:
            return output("INVALID_CHECKER_PARAMETERS", "Invalid term limit")
        if type(problem) is not dict or set(problem) != {"N", "r", "p", "omega", "x"}:
            return output("INVALID_PROBLEM", "Wrong problem fields")
        if any(type(problem[k]) is not int for k in ("N", "r", "p", "omega")):
            return output("INVALID_PROBLEM", "Noninteger header")
        n, r, p, w = (problem[k] for k in ("N", "r", "p", "omega"))
        if not (n >= 2 and 1 <= r < n and p >= 2 and 0 <= w < p):
            return output("INVALID_PROBLEM", "Outside stated domain")
        if n > 512 or r > 128 or p.bit_length() > 64:
            return output("CHECKER_LIMIT", "Checker dimension/bit cap exceeded")
        if (p-1) % n or type(problem["x"]) not in (list, tuple) or len(problem["x"]) != n:
            return output("INVALID_PROBLEM", "Invalid grid or raw length")
        x = problem["x"]
        for z in x:
            pay()
            if type(z) is not int or not 0 <= z < p:
                return output("INVALID_PROBLEM", "Noncanonical raw input")
        for d in range(2, math.isqrt(p)+1):
            pay()
            if p % d == 0:
                return output("INVALID_PROBLEM", "Composite modulus")
        # Independent powers, intentionally distinct from recurrence-built table.
        roots = []
        for k in range(n+1):
            pay(k.bit_length()+1)
            roots.append(pow(w, k, p))
        if roots[-1] != 1 or any(z == 1 for z in roots[1:-1]):
            return output("INVALID_PROBLEM", "Wrong root order")
        if type(certificate) is not dict or certificate.get("schema") != "chirp-exact-reference-v1":
            return output("INVALID_CERTIFICATE", "Wrong schema")
        encoded = json.dumps(problem, sort_keys=True, separators=(",", ":")).encode()
        pay(len(encoded))
        if certificate.get("input_sha256") != hashlib.sha256(encoded).hexdigest():
            return output("INVALID_CERTIFICATE", "Input binding mismatch")
        decision = certificate.get("status")
        if decision not in ("MEMBER", "NONMEMBER"):
            return output("NO_DECISION", "Only complete mathematical decisions can be checked")
        L = n // math.gcd(2, n)
        if decision == "MEMBER":
            rep = certificate.get("representation")
            if type(rep) is not dict or set(rep) != {"a", "modes"}:
                return output("INVALID_CERTIFICATE", "Malformed representation")
            a, modes = rep["a"], rep["modes"]
            if type(a) is not int or not 0 <= a < L or type(modes) is not list or len(modes) > r:
                return output("INVALID_CERTIFICATE", "Noncanonical phase or excessive mode count")
            seen = set()
            for mode in modes:
                pay()
                if type(mode) is not dict or set(mode) != {"b", "gamma"}:
                    return output("INVALID_CERTIFICATE", "Malformed mode")
                b, g = mode["b"], mode["gamma"]
                if type(b) is not int or type(g) is not int or not 0 <= b < n or not 1 <= g < p or b in seen:
                    return output("INVALID_CERTIFICATE", "Invalid/duplicate mode")
                seen.add(b)
            for j in range(n):
                y = 0
                for mode in modes:
                    pay()
                    y += mode["gamma"] * pow(w, (a*j*j+mode["b"]*j) % n, p)
                if y % p != x[j]:
                    return output("INVALID_CERTIFICATE", "Raw synthesis mismatch")
            dft = certificate.get("dft")
            if type(dft) is not list or len(dft) != n or any(type(z) is not int or not 0 <= z < p for z in dft):
                return output("INVALID_CERTIFICATE", "Malformed dense DFT output")
            for k in range(n):
                value = 0
                for j in range(n):
                    pay()
                    value += x[j] * pow(w, (j*k) % n, p)
                if value % p != dft[k]:
                    return output("INVALID_CERTIFICATE", "Positive-sign unnormalized DFT mismatch")
            return output("VERIFIED_MEMBER", "All raw coordinates and all dense DFT outputs checked")
        if certificate.get("representation") is not None or certificate.get("dft") is not None:
            return output("INVALID_CERTIFICATE", "NONMEMBER must not supply a representation or transform")
        phases = certificate.get("phases")
        if type(phases) is not list or len(phases) != L:
            return output("INVALID_CERTIFICATE", "Incomplete canonical phase log")
        for a, record in enumerate(phases):
            if type(record) is not dict or type(record.get("a")) is not int or record.get("a") != a or type(record.get("status")) is not str or record.get("status") not in {
                "ELIMINANT_NONZERO", "ZERO_PREFIX_RAW_MISMATCH", "SINGULAR_LEADING_HANKEL",
                "NODE_ROOT_COUNT_MISMATCH", "RAW_RECURRENCE_MISMATCH", "RAW_SYNTHESIS_MISMATCH"}:
                return output("INVALID_CERTIFICATE", "Invalid rejection log")
            # The independent criterion: support of inverse DFT of dechirped
            # raw input. Scaling by N^-1 is unnecessary for zero/nonzero support.
            support = 0
            for b in range(n):
                coeff = 0
                for j in range(n):
                    pay()
                    coeff += x[j]*pow(w, (-a*j*j-b*j) % n, p)
                support += coeff % p != 0
            if support <= r:
                return output("INVALID_CERTIFICATE", "A canonical phase is a member")
        return output("VERIFIED_NONMEMBER", "All canonical phases have Fourier support exceeding r")
    except CheckLimit:
        return output("CHECKER_LIMIT", "No verified decision; checker term budget exhausted")
