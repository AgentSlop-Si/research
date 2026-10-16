"""Fresh ALG-007 adapter; no imports of supplied or historical research code.

Public entrypoint: transform. Exact fixed-prime, power-of-two model only.
Meters count declared algorithmic events, not Python bytecode or bit operations.
"""
from dataclasses import dataclass, field

P = 2013265921
GENERATOR = 31
MAX_Q = 1 << 27
IMPLEMENTATION_ID = "alg007-independent-bounded-adapter-v1"


class ContractError(ValueError):
    """Invalid domain; deliberately does not invoke a fallback for another DFT."""
    def __init__(self, message, ledger):
        super().__init__(message)
        self.ledger = ledger


class _BudgetExhausted(Exception):
    pass


@dataclass
class _Meter:
    budget: int
    phase: str = "input"
    phases: dict = field(default_factory=dict)
    spent: int = 0
    denied: object = None

    def charge(self, kind, units=1):
        self.reserve({kind: units})

    def reserve(self, charges):
        # Every call below has a fixed nonnegative integer amount. Charge BEFORE
        # the corresponding operation, so a failed reservation does no work.
        units = sum(charges.values())
        if self.phase in ("recognition", "decode"):
            if units > self.budget - self.spent:
                self.denied = {"phase": self.phase, "charges": dict(charges),
                               "units": units, "spent": self.spent}
                raise _BudgetExhausted
            self.spent += units
        bucket = self.phases.setdefault(self.phase, {})
        for kind, count in charges.items():
            bucket[kind] = bucket.get(kind, 0) + count

    def snapshot(self):
        phases = {p: dict(c) for p, c in self.phases.items()}
        total = {}
        for counts in phases.values():
            for key, value in counts.items():
                total[key] = total.get(key, 0) + value
        return {"phases": phases, "total": total,
                "total_units": sum(total.values()), "attempt_spent": self.spent,
                "attempt_budget": self.budget, "denied_reservation": self.denied}


def _fail(meter, text):
    raise ContractError(text, meter.snapshot())


def _mul(u, v, meter):
    meter.charge("field_mul")
    return u * v % P


def _add(u, v, meter):
    meter.charge("field_add")
    return (u + v) % P


def _sub(u, v, meter):
    meter.charge("field_add")
    return (u - v) % P


def _equal(u, v, meter):
    meter.charge("field_equal")
    return u == v


def _pow_mod(base, exponent, meter):
    # Modular multiplications here include primality/root/inverse preparation.
    # Before the primality certificate is finished these are ring operations.
    acc = 1
    while exponent:
        meter.charge("index_step")
        if exponent & 1:
            meter.charge("setup_modular_mul")
            acc = acc * base % P
        exponent >>= 1
        if exponent:
            meter.charge("setup_modular_mul")
            base = base * base % P
    return acc


def _zeros(n, meter):
    meter.reserve({"allocation_word": n, "data_write": n})
    return [0] * n


def _copy(values, meter):
    n = len(values)
    meter.reserve({"allocation_word": n, "data_read": n, "data_write": n})
    return list(values)


def _read(values, index, meter):
    meter.charge("data_read")
    return values[index]


def _write(values, index, value, meter):
    meter.charge("data_write")
    values[index] = value


def _phase(table, exponent, meter):
    meter.reserve({"index_step": 1, "root_lookup": 1})
    return table[exponent % len(table)]


def _ntt(values, table, sign, meter):
    """Independent DIF transform, then explicit natural-order permutation.

    table has primitive Qth root powers; len(values) divides Q. No stage-power
    oracle, library FFT, floating arithmetic, historical code, or hidden cache.
    """
    n = len(values)
    meter.charge("ntt_started")
    data = _copy(values, meter)
    span = n
    while span > 1:
        meter.charge("index_step")
        half = span // 2
        stride = len(table) // span
        for origin in range(0, n, span):
            meter.charge("index_step")
            for offset in range(half):
                meter.charge("index_step")
                first, second = origin + offset, origin + offset + half
                u, v = _read(data, first, meter), _read(data, second, meter)
                omega = _phase(table, sign * stride * offset, meter)
                _write(data, first, _add(u, v, meter), meter)
                _write(data, second, _mul(_sub(u, v, meter), omega, meter), meter)
                meter.charge("ntt_butterfly")
        span = half
    result = _zeros(n, meter)
    width = n.bit_length() - 1
    for target in range(n):
        meter.charge("index_step")
        source, value = 0, target
        for _ in range(width):
            meter.charge("index_step")
            source, value = (source << 1) | (value & 1), value >> 1
        _write(result, target, _read(data, source, meter), meter)
    meter.charge("ntt_finished")
    return result


@dataclass
class _Context:
    raw: tuple
    q: int
    m: int
    k: int
    a: int
    beta: int
    table: list
    inverse_m: int
    inverse_two: int
    root: int


def _prepare(x, m, cap, a, beta, root, meter):
    # Reject subclasses: user-defined iteration/index/equality is not executed.
    meter.charge("parameter_check")
    if type(x) not in (tuple, list):
        _fail(meter, "x must be an exact built-in list or tuple")
    q = len(x)
    meter.charge("parameter_check", 7)
    if not (4 <= q <= MAX_Q and q & (q - 1) == 0):
        _fail(meter, "Q must be a power of two in [4, 2**27]")
    if type(m) is not int or not 2 <= m <= q or m & (m - 1) or q % m:
        _fail(meter, "M must be a power-of-two divisor of Q, M >= 2")
    k = q // m
    if k < m:
        _fail(meter, "K=Q/M must satisfy K >= M")
    if type(cap) is not int or not 0 <= cap <= m:
        _fail(meter, "cap must be an integer in [0, M]")
    if type(a) is not int or not 0 <= a < q or not a & 1:
        _fail(meter, "a must be a canonical odd unit modulo Q")
    if type(beta) is not int or not 0 <= beta < q:
        _fail(meter, "beta must be canonical modulo Q")
    if root is not None and (type(root) is not int or not 0 < root < P):
        _fail(meter, "supplied root must be a nonzero canonical field integer")
    raw = _zeros(q, meter)
    for index in range(q):
        meter.charge("index_step")
        value = _read(x, index, meter)
        meter.charge("parameter_check")
        if type(value) is not int or not 0 <= value < P:
            _fail(meter, "all raw values must be canonical built-in integers")
        _write(raw, index, value, meter)
    meter.charge("allocation_word", q)
    meter.charge("data_read", q)
    meter.charge("data_write", q)
    raw = tuple(raw)
    meter.phase = "setup"
    # Complete factorization P-1=2**27 * 3 * 5. Full multiplicative order P-1
    # implies P is prime: the order cannot exceed phi(P) <= P-1, with equality
    # only for prime P. This cold check needs no imported primality library.
    meter.charge("parameter_check")
    if P - 1 != (1 << 27) * 3 * 5:
        _fail(meter, "fixed modulus factor certificate failed")
    if _pow_mod(GENERATOR, P - 1, meter) != 1:
        _fail(meter, "fixed generator order certificate failed")
    for factor in (2, 3, 5):
        meter.charge("parameter_check")
        if _pow_mod(GENERATOR, (P - 1) // factor, meter) == 1:
            _fail(meter, "fixed generator has deficient order")
    if root is None:
        root = _pow_mod(GENERATOR, (P - 1) // q, meter)
    # For dyadic Q these are necessary and sufficient exact-order checks.
    meter.charge("parameter_check", 2)
    if _pow_mod(root, q, meter) != 1 or _pow_mod(root, q // 2, meter) == 1:
        _fail(meter, "root does not have exact order Q")
    inverse_m = _pow_mod(m, P - 2, meter)
    inverse_two = _pow_mod(2, P - 2, meter)
    table = _zeros(q, meter)
    _write(table, 0, 1, meter)
    for index in range(1, q):
        meter.charge("index_step")
        _write(table, index, _mul(_read(table, index - 1, meter), root, meter), meter)
    return _Context(raw, q, m, k, a, beta, table, inverse_m, inverse_two, root)


@dataclass
class _Recognized:
    decision: str
    support: list
    columns: list
    observed_support_count: int


def _recognize(ctx, cap, meter, progress):
    """Internal interface. ACCEPT is a complete exact raw-input certificate.

    CAP_REJECT supplies only a lower bound on global support. Budget exhaustion
    propagates; no partial columns are interpreted as an accepted certificate.
    """
    q, m, k = ctx.q, ctx.m, ctx.k
    support = []
    columns = _zeros(m, meter)
    seen = _zeros(m, meter)
    for block in range(k):
        meter.charge("index_step")
        y = _zeros(m, meter)
        for t in range(m):
            meter.charge("index_step")
            exponent = ctx.a * t * (t - 1) // 2 + (ctx.a * m * block + ctx.beta) * t
            val = _mul(_read(ctx.raw, block * m + t, meter),
                       _phase(ctx.table, exponent, meter), meter)
            _write(y, t, val, meter)
        selected = _zeros(len(support), meter)
        for position, mode in enumerate(support):
            meter.charge("index_step")
            acc = 0
            for t in range(m):
                meter.charge("index_step")
                acc = _add(acc, _mul(_read(y, t, meter),
                           _phase(ctx.table, k * mode * t, meter), meter), meter)
            _write(selected, position, acc, meter)
        valid = True
        for t in range(m):
            meter.charge("index_step")
            acc = 0
            for position, mode in enumerate(support):
                meter.charge("index_step")
                acc = _add(acc, _mul(_read(selected, position, meter),
                           _phase(ctx.table, -k * mode * t, meter), meter), meter)
            reconstructed = _mul(acc, ctx.inverse_m, meter)
            if not _equal(reconstructed, _read(y, t, meter), meter):
                valid = False
            meter.charge("certificate_coordinate")
        if valid:
            for position, mode in enumerate(support):
                meter.charge("index_step")
                _write(columns[mode], block, _read(selected, position, meter), meter)
        else:
            complete = _ntt(y, ctx.table, 1, meter)
            meter.charge("discovery_finished")
            progress["full_discoveries"] += 1
            new = []
            for mode in range(m):
                meter.charge("index_step")
                nonzero = not _equal(_read(complete, mode, meter), 0, meter)
                old = _read(seen, mode, meter)
                if nonzero and not old:
                    meter.reserve({"allocation_word": 1, "data_write": 1})
                    new.append(mode)
            count = len(support) + len(new)
            if count > cap:
                meter.charge("cap_rejection")
                progress["observed_support_lower_bound"] = count
                return _Recognized("CAP_REJECT", [], [], count)
            for mode in new:
                meter.charge("index_step")
                _write(columns, mode, _zeros(k, meter), meter)
                meter.reserve({"allocation_word": 1, "data_write": 1})
                support.append(mode)
                _write(seen, mode, 1, meter)
            for mode in support:
                meter.charge("index_step")
                _write(columns[mode], block, _read(complete, mode, meter), meter)
        progress["completed_blocks"] += 1
        progress["observed_support_lower_bound"] = len(support)
    meter.charge("recognition_accept")
    return _Recognized("ACCEPT", support, columns, len(support))


def _decode(ctx, recognition, meter):
    q, m, k = ctx.q, ctx.m, ctx.k
    accumulated = _zeros(q, meter)
    for mode in recognition.support:
        meter.charge("index_step")
        beta = (ctx.beta + mode * k) % q
        spectrum = _ntt(recognition.columns[mode], ctx.table, -1, meter)
        terms = _zeros(q, meter)
        seed_sum = 0
        for h in range(q):
            meter.charge("index_step")
            index = ctx.a * h % q
            gauge_exp = ctx.a * h * (h - 1) // 2 + beta * h
            boundary_exp = -m * (index + beta) - ctx.a * m * (m - 1) // 2
            forcing = _sub(_read(spectrum, index % k, meter),
                       _mul(_phase(ctx.table, boundary_exp, meter),
                            _read(spectrum, (index + ctx.a * m) % k, meter), meter), meter)
            term = _mul(forcing, _phase(ctx.table, -gauge_exp, meter), meter)
            _write(terms, h, term, meter)
            seed_sum = _add(seed_sum, term, meter)
            meter.charge("green_seed_addition")
        seed = _mul(seed_sum, ctx.inverse_two, meter)
        prefix = 0
        for h in range(q):
            meter.charge("index_step")
            index = ctx.a * h % q
            gauge_exp = ctx.a * h * (h - 1) // 2 + beta * h
            value = _mul(_phase(ctx.table, gauge_exp, meter), _sub(seed, prefix, meter), meter)
            _write(accumulated, index, _add(_read(accumulated, index, meter), value, meter), meter)
            prefix = _add(prefix, _read(terms, h, meter), meter)
        meter.charge("green_row_finished")
    if recognition.support:
        for index in range(q):
            meter.charge("index_step")
            _write(accumulated, index, _mul(_read(accumulated, index, meter), ctx.inverse_m, meter), meter)
    return accumulated


def transform(x, m, cap, *, a=1, beta=0, root=None, attempt_budget=None):
    """Return every unnormalized negative-sign Q-DFT coordinate exactly.

    No caller-supplied executable callback is accepted. Invalid parameters raise
    ContractError. A valid input always selects an exact accepted Green output or
    the exact full NTT. The attempt budget covers recognition AND decoding; cold
    validation/setup, fallback and final output writing are separately paid.
    """
    if attempt_budget is None:
        # Read only built-in sequence length; reject other objects without hooks.
        n = len(x) if type(x) in (list, tuple) else 0
        attempt_budget = 64 * n * max(1, n.bit_length() - 1)
    if type(attempt_budget) is not int or attempt_budget < 0:
        raise ContractError("attempt_budget must be a nonnegative built-in integer", {})
    meter = _Meter(attempt_budget)
    ctx = _prepare(x, m, cap, a, beta, root, meter)
    progress = {"completed_blocks": 0, "full_discoveries": 0,
                "observed_support_lower_bound": 0}
    support = None
    try:
        meter.phase = "recognition"
        decision = _recognize(ctx, cap, meter, progress)
        if decision.decision == "ACCEPT":
            meter.phase = "decode"
            result = _decode(ctx, decision, meter)
            route = "GREEN_ACCEPT"
            # Output metadata materialization is paid in the output phase below.
            support = decision.support
        else:
            route = "FALLBACK_CAP"
            result = None
    except _BudgetExhausted:
        # Discard every partial certificate/output; preserve the same ledger.
        route = "FALLBACK_BUDGET"
        result = None
    if result is None:
        meter.phase = "fallback"
        meter.charge("fallback_dispatch")
        result = _ntt(ctx.raw, ctx.table, -1, meter)
    meter.phase = "output"
    meter.charge("allocation_word", ctx.q)
    meter.charge("data_read", ctx.q)
    meter.charge("data_write", ctx.q)
    meter.charge("output_coordinate", ctx.q)
    output = tuple(result)
    if support is not None:
        meter.charge("allocation_word", len(support))
        meter.charge("data_read", len(support))
        meter.charge("data_write", len(support))
        support = tuple(support)
    return {"implementation": IMPLEMENTATION_ID, "values": output,
            "route": route, "support": support, "progress": progress,
            "model": {"p": P, "q": ctx.q, "m": m, "k": ctx.k,
                      "root": ctx.root, "a": a, "beta": beta,
                      "sign": -1, "normalization": "unnormalized"},
            "ledger": meter.snapshot()}
