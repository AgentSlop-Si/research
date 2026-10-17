"""Candidate bounded ALG034 -> Q16 source boundary. No ALG034 implementation.

Importing the two pinned Q16 modules creates their classes; this wrapper only
constructs the accepted DyadicSource record. It never runs numerical Q16 code.
The certificate is an explicit trusted upstream premise, not a proof object
whose mathematical or origin authenticity can be established by this parser.
"""
from dataclasses import dataclass
from hashlib import sha256
from buckets import DyadicSource

MAX_M = 4096
MAX_NUMERATOR_BITS = 65536
MAX_METADATA_INTEGER_BITS = 256
MAX_C_BITS = 16384
PRODUCER = 'ALG034-SERIAL-FIXED-POINT-v1'
TARGET = 'U_negative(P_balanced_longer_first(x))'
PHASES = 'ALG034-accepted-phase-embedding-v1'
ORDER = 'frequency-index-order'
PREMISE = 'I attest all accepted ALG034 producer, phase, rounding, range and input premises'
SOUNDNESS = 'CONDITIONAL_ON_TRUSTED_UPSTREAM_CONTRACT'
SECOND_TARGET = 'R(P_balanced_longer_first(x))/alpha; R[j]=(-j mod M)'
CERT_FIELDS = ('producer', 'target', 'phases', 'order', 'premise', 'input_sha256',
               'output_sha256', 'N', 'B_A', 'a', 'beta_A', 'F_in', 'W_in',
               'p', 't', 'C', 'original_input_zero')


@dataclass(frozen=True)
class Receipt:
    events: tuple
    input_integer_bits: int
    max_input_integer_bits: int
    arithmetic_work_upper: int
    produced_integer_bits: int
    allocated_slots: int
    byte_work_units: int
    max_integer_bits: int
    bookkeeping_work_upper: int
    total_bit_work_upper: int
    cumulative_storage_upper_bits: int


class _Ledger:
    def __init__(self):
        self.events = {}; self.input_bits = 0; self.input_max = 1
        self.work = 0; self.produced = 0; self.slots = 0; self.bytes = 0; self.width = 1
    def event(self, kind, count=1):
        self.events[kind] = self.events.get(kind, 0) + count
    def record(self, kind, args, value):
        sizes = [max(1, abs(x).bit_length()) for x in (*args, value)]
        self.event(kind); self.work += 32 * (2 + sum(sizes)) ** 2
        self.produced += sizes[-1] + 1; self.width = max(self.width, *sizes)
        return value
    def integer(self, value, path, cap):
        self.event('integer_type_check')
        if type(value) is not int: self.reject('INTEGER_TYPE', path)
        bits = max(1, abs(value).bit_length())
        self.input_bits += bits + 1; self.input_max = max(self.input_max, bits)
        self.record('input_integer', (), value)
        if bits > cap: self.reject('INTEGER_WIDTH_LIMIT', path)
        return value
    def add(self, a, b): return self.record('add', (a,b), a+b)
    def sub(self, a, b): return self.record('subtract', (a,b), a-b)
    def mul(self, a, b): return self.record('multiply', (a,b), a*b)
    def div(self, a, b): return self.record('divide', (a,b), a//b)
    def shift(self, n):
        assert 0 <= n <= 2*MAX_NUMERATOR_BITS + MAX_M + 1024
        return self.record('binary_power', (n,), 1 << n)
    def bits(self, n): return self.record('bit_length', (n,), n.bit_length())
    def allocate(self, n): self.slots += n; self.event('allocated_slots', n)
    def bytework(self, n):
        self.bytes += n; self.event('byte_processing', n); self.event('byte_operation')
    def snapshot(self):
        count = sum(v for k,v in self.events.items() if k != 'byte_processing') + 256
        width = max(self.width, self.input_max) + count.bit_length() + 2
        control = 1024*count*width*width
        return Receipt(tuple(sorted(self.events.items())), self.input_bits,
                       self.input_max, self.work, self.produced, self.slots,
                       self.bytes, self.width, control,
                       self.work + control + 8192*self.bytes,
                       self.produced + 1024*count*width + 8*self.bytes)
    def reject(self, code, path):
        self.event('rejection'); raise Rejection(code, path, self.snapshot())


class Rejection(ValueError):
    def __init__(self, code, path, receipt):
        self.code, self.path, self.receipt = code, path, receipt
        super().__init__(code + ': ' + path)


@dataclass(frozen=True)
class ProducerContract:
    fields: tuple
    # Each field is immutable. This record does not authenticate its assertions.


@dataclass(frozen=True)
class SourceResult:
    status: str
    source: object
    alpha_exponent: object
    normalization_L: object
    doubling: int
    delta: tuple  # (nonnegative significand, signed binary exponent)
    rho: tuple
    requantization_error: tuple
    target_budget: str
    target: str
    second_transform_target: str
    producer_contract: ProducerContract
    output_sha256: str
    conditional_soundness: str
    receipt: Receipt


def _sequence(x, size, path, L):
    L.event('sequence_type_check')
    if type(x) not in (tuple, list): L.reject('SEQUENCE_TYPE', path)
    n = L.record('sequence_length', (), len(x))
    if n != size: L.reject('SEQUENCE_LENGTH', path)
    return x


def _text(value, path, L, expected=None, digest=False):
    L.event('text_type_check')
    if type(value) is not str: L.reject('TEXT_TYPE', path)
    n = L.record('text_length', (), len(value)); L.bytework(4*n)
    if n > 256: L.reject('TEXT_LENGTH_LIMIT', path)
    if expected is not None and value != expected: L.reject('CONTRACT_TAG', path)
    if digest and (n != 64 or any(c not in '0123456789abcdef' for c in value)):
        L.reject('DIGEST_ENCODING', path)
    return value


def _encoded_integer(n, L):
    """Canonical signed binary: sign byte, four-byte magnitude length, magnitude."""
    width = L.bits(abs(n)); size = L.div(L.add(width, 7), 8)
    body = abs(n).to_bytes(size, 'big')
    L.bytework(size + 5); L.allocate(3)
    return bytes((1 if n < 0 else 0,)) + size.to_bytes(4, 'big') + body


def _error_constant(N, B, L):
    # Exact binomial via a finite multiplicative recurrence, no math.comb oracle.
    choose = 1
    for j in range(1, B+1):
        choose = L.div(L.mul(choose, L.add(N, L.sub(j, 1))), j)
        L.event('binomial_step')
    H = min(choose, L.shift(L.sub(N, B)))
    return L.mul(L.mul(L.mul(64, H), B), L.mul(L.shift(B), L.mul(N, N)))


def _dyadic_le_power(c, exponent, target_exponent, L):
    """Compare c*2^exponent <= 2^target_exponent without huge shifts."""
    if c == 0: return True
    gap = L.sub(target_exponent, exponent)
    highest = L.sub(L.bits(c), 1)
    if gap < highest: return False
    if gap > highest: return True
    # Here the shift width is the actual significand's width, never |exponent|.
    return c == L.shift(highest)


def _round_scaled(n, shift, L):
    """Nearest even integer to n*2^shift, with signed ties treated symmetrically."""
    L.event('cartesian_round')
    if shift >= 0: return L.mul(n, L.shift(shift))
    denominator = L.shift(-shift)
    sign = -1 if n < 0 else 1
    quotient = L.div(abs(n), denominator)
    remainder = L.sub(abs(n), L.mul(quotient, denominator))
    twice = L.mul(2, remainder)
    if twice > denominator or (twice == denominator and quotient % 2):
        quotient = L.add(quotient, 1)
    return L.mul(sign, quotient)


def adapt(payload, certificate):
    """Parse/copy bounded in-memory input; return immutable Q16 source or zero.

    payload = (N, kappa, [(real_integer, imag_integer), ...]).
    certificate has CERT_FIELDS order. Only exact tuple/list containers and
    exact int/str scalars are admitted. All reached integer widths are charged
    before width/domain rejection. Inputs must not change during the call.
    Hard deployment caps are explicit restrictions, not a universal theorem.
    """
    L = _Ledger(); L.event('adapter_call'); L.allocate(2)
    payload = _sequence(payload, 3, 'payload', L)
    N = L.integer(payload[0], 'payload.N', MAX_METADATA_INTEGER_BITS)
    kappa = L.integer(payload[1], 'payload.kappa', MAX_METADATA_INTEGER_BITS)
    if N < 4 or N > MAX_M or N & (N-1): L.reject('LENGTH_DOMAIN', 'payload.N')
    m = L.sub(L.bits(N), 1)
    P = L.add(L.mul(16, m), 16); F = L.add(P, 1)
    cert = _sequence(certificate, len(CERT_FIELDS), 'certificate', L)
    expected = (PRODUCER, TARGET, PHASES, ORDER, PREMISE)
    textfields = []
    for j, tag in enumerate(expected):
        textfields.append(_text(cert[j], 'certificate.'+CERT_FIELDS[j], L, tag))
    for j in (5,6):
        textfields.append(_text(cert[j], 'certificate.'+CERT_FIELDS[j], L, digest=True))
    integers = []
    for j in range(7,17):
        integers.append(L.integer(cert[j], 'certificate.'+CERT_FIELDS[j],
                                  MAX_C_BITS if j == 15 else MAX_METADATA_INTEGER_BITS))
    cN, B, a, beta, Fin, Win, p, t, claimed_C, original_zero = integers
    L.allocate(34)
    contract = ProducerContract(tuple(textfields + integers))
    if cN != N: L.reject('CERTIFICATE_LENGTH_MISMATCH', 'certificate.N')
    if not 3 <= B <= N: L.reject('BLOCK_DOMAIN', 'certificate.B_A')
    if not 0 < a < N or a % 2 != 1: L.reject('STATE_DOMAIN', 'certificate.a')
    if not 0 <= beta < N: L.reject('STATE_DOMAIN', 'certificate.beta_A')
    if min(Win, p, t) < 0 or original_zero not in (0,1):
        L.reject('PRECISION_DOMAIN', 'certificate')
    if original_zero:
        if Win != 0 or claimed_C != 0 or kappa != 0 or p != 0 or t != 0:
            L.reject('ZERO_CONTRACT', 'certificate')
        C = 0
    else:
        if Win < 1 or p < Win: L.reject('PRECISION_DOMAIN', 'certificate.p/W_in')
        if kappa != L.sub(L.sub(Win, Fin), p):
            L.reject('EXPONENT_BINDING', 'payload.kappa')
        C = _error_constant(N, B, L)
        if claimed_C != C: L.reject('ERROR_CONSTANT', 'certificate.C')
        if not _dyadic_le_power(L.mul(2,C), -p, -t, L):
            L.reject('PRECISION_CERTIFICATE', 'certificate.p/t')
    rows = _sequence(payload[2], N, 'payload.rows', L)
    digest = sha256(); prefix = b'ALG034-OUTPUT-v1\x00'; digest.update(prefix); L.bytework(len(prefix))
    digest.update(_encoded_integer(N,L)); digest.update(_encoded_integer(kappa,L))
    S = 0
    for index in range(N):
        cell = _sequence(rows[index], 2, 'payload.rows['+str(index)+']', L)
        for axis in range(2):
            n = L.integer(cell[axis], 'payload.rows['+str(index)+']['+str(axis)+']', MAX_NUMERATOR_BITS)
            digest.update(_encoded_integer(n,L))
            S = L.add(S, L.mul(n,n)); L.event('source_validation_field')
    output_hash = digest.hexdigest(); L.bytework(64); L.allocate(1)
    if output_hash != cert[6]: L.reject('OUTPUT_BINDING', 'certificate.output_sha256')
    if original_zero and S != 0: L.reject('ZERO_OUTPUT_CONTRADICTION', 'payload.rows')
    if S == 0:
        L.event('zero_return'); L.allocate(15)
        return SourceResult('EXACT_ZERO_INPUT' if original_zero else 'ZERO_APPROXIMATION',
                            None, None, None, 1, (C,kappa), (1,-P), (0,0),
                            'NO_NORMALIZED_SOURCE', TARGET, SECOND_TARGET, contract,
                            output_hash, SOUNDNESS, L.snapshot())
    scale = L.div(L.add(L.bits(L.sub(S,1)),1),2)
    rounded = []; L.allocate(N)
    Sq = 0; shift = L.sub(F,scale)
    for row in rows:
        pair = []
        for n in row:
            L.event('source_second_pass_read')
            q = _round_scaled(n, shift, L); pair.append(q)
            Sq = L.add(Sq,L.mul(q,q))
        rounded.append(tuple(pair)); L.allocate(4)
    unit = L.shift(F)
    doubling = 2 if L.mul(4,Sq) <= L.mul(unit,unit) else 1
    alpha = L.sub(L.add(kappa,scale), 1 if doubling == 2 else 0)
    output = []; L.allocate(N); final_squared = 0
    for pair in rounded:
        components = []
        for q in pair:
            n = L.mul(doubling,q)
            if abs(n) > unit: L.reject('INTERNAL_MAGNITUDE', 'requantized_source')
            final_squared = L.add(final_squared,L.mul(n,n))
            components.append((n,F)); L.allocate(3); L.event('dyadic_field_write',2)
        output.append(tuple(components)); L.allocate(2); L.event('complex_cell_write')
    if L.mul(4,final_squared) <= L.mul(unit,unit):
        L.reject('INTERNAL_STRICT_NORM', 'requantized_source')
    values = tuple(output); L.allocate(N+2); L.event('immutable_source_copy',N)
    source = DyadicSource(values,F)
    # delta/alpha = C * 2^(kappa-alpha), including the doubling adjustment.
    passes = _dyadic_le_power(C,L.sub(kappa,alpha),-P,L)
    L.allocate(15); L.event('nonzero_return')
    return SourceResult('VALID_SOURCE',source,alpha,scale,doubling,(C,kappa),
                        (1,-P),(1,1-F),
                        'TARGET_BUDGET_PASS' if passes else 'TARGET_BUDGET_NOT_ESTABLISHED',
                        TARGET,SECOND_TARGET,contract,output_hash,SOUNDNESS,L.snapshot())
