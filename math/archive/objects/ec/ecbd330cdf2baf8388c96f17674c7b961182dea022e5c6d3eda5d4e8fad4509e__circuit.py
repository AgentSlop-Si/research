"""Exact scalar circuits and a compiled H(0)v evaluator.

Research utility, not a faster FFT. The compiler accepts only scalar field
operations with every inverse regular at the origin. No data-dependent lookup,
comparison, exponent oracle, or vector operation is an arithmetic gate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Gate:
    op: str
    a: int = -1
    b: int = -1
    value: int = 0


class Circuit:
    def __init__(self, n: int, modulus: int):
        if n < 1 or modulus < 3:
            raise ValueError('positive input dimension and odd prime modulus required')
        self.n = n
        self.p = modulus  # The caller must supply a prime; tests certify theirs.
        self.gates = [Gate('input', value=i) for i in range(n)]
        self.output = 0

    def const(self, value: int) -> int:
        self.gates.append(Gate('const', value=value % self.p))
        return len(self.gates) - 1

    def _gate(self, op: str, a: int, b: int = -1) -> int:
        if not 0 <= a < len(self.gates) or (b != -1 and not 0 <= b < len(self.gates)):
            raise ValueError('invalid predecessor')
        self.gates.append(Gate(op, a, b))
        return len(self.gates) - 1

    def add(self, a: int, b: int) -> int:
        return self._gate('add', a, b)

    def sub(self, a: int, b: int) -> int:
        return self._gate('sub', a, b)

    def mul(self, a: int, b: int) -> int:
        return self._gate('mul', a, b)

    def inv(self, a: int) -> int:
        return self._gate('inv', a)

    @property
    def arithmetic_gates(self) -> int:
        return sum(g.op not in ('input', 'const') for g in self.gates)

    def values(self, x: Sequence[int]) -> list[int]:
        if len(x) != self.n:
            raise ValueError('wrong input length')
        vals: list[int] = []
        p = self.p
        for g in self.gates:
            if g.op == 'input':
                z = x[g.value]
            elif g.op == 'const':
                z = g.value
            elif g.op == 'add':
                z = vals[g.a] + vals[g.b]
            elif g.op == 'sub':
                z = vals[g.a] - vals[g.b]
            elif g.op == 'mul':
                z = vals[g.a] * vals[g.b]
            elif g.op == 'inv':
                if vals[g.a] == 0:
                    raise ZeroDivisionError(f'singular inverse at gate {len(vals)}')
                z = pow(vals[g.a], -1, p)
            else:
                raise ValueError('unsupported gate')
            vals.append(z % p)
        return vals

    def evaluate(self, x: Sequence[int]) -> int:
        return self.values(x)[self.output]


class LinearProgram:
    """Append-only scalar SSA. Construction uses zero/one folding, not hashing."""
    def __init__(self, n: int, modulus: int):
        self.n, self.p = n, modulus
        self.gates = [Gate('input', value=i) for i in range(n)]
        self.zero = len(self.gates)
        self.gates.append(Gate('const', value=0))
        self.outputs: list[int] = []

    def scale(self, a: int, c: int) -> int:
        c %= self.p
        if a == self.zero or c == 0:
            return self.zero
        if c == 1:
            return a
        self.gates.append(Gate('scale', a, value=c))
        return len(self.gates) - 1

    def add(self, a: int, b: int) -> int:
        if a == self.zero:
            return b
        if b == self.zero:
            return a
        self.gates.append(Gate('add', a, b))
        return len(self.gates) - 1

    def apply(self, x: Sequence[int]) -> list[int]:
        if len(x) != self.n:
            raise ValueError('wrong input dimension')
        vals = []
        for g in self.gates:
            if g.op == 'input':
                z = x[g.value]
            elif g.op == 'const':
                z = g.value
            elif g.op == 'add':
                z = vals[g.a] + vals[g.b]
            elif g.op == 'scale':
                z = vals[g.a] * g.value
            else:
                raise ValueError('nonlinear gate in emitted program')
            vals.append(z % self.p)
        return [vals[i] for i in self.outputs]

    @property
    def arithmetic_gates(self) -> int:
        return sum(g.op in ('add', 'scale') for g in self.gates)


def compile_hessian_at_zero(c: Circuit) -> tuple[LinearProgram, dict]:
    """Emit an exact linear program for Hessian(c)(0) times an arbitrary vector.

    Preparation and compilation are O(number of scalar gates + input count).
    The emitted program uses no division or data-dependent control flow.
    """
    vals = c.values([0] * c.n)  # Reject any intermediate inverse singular here.
    p, gates = c.p, c.gates
    # First and second local derivatives; each gate has at most two arguments.
    first: list[list[tuple[int, int]]] = []
    second: list[list[tuple[int, int, int]]] = []
    for idx, g in enumerate(gates):
        if g.op in ('input', 'const'):
            f, h = [], []
        elif g.op == 'add':
            f, h = [(g.a, 1), (g.b, 1)], []
        elif g.op == 'sub':
            f, h = [(g.a, 1), (g.b, p-1)], []
        elif g.op == 'mul':
            f = [(g.a, vals[g.b]), (g.b, vals[g.a])]
            h = [(g.a, g.b, 1), (g.b, g.a, 1)]
        elif g.op == 'inv':
            z = vals[idx]
            f, h = [(g.a, -z*z % p)], [(g.a, g.a, 2*z*z*z % p)]
        else:
            raise ValueError('unsupported gate')
        first.append(f)
        second.append(h)
    adjoint = [0] * len(gates)
    adjoint[c.output] = 1
    for idx in range(len(gates)-1, -1, -1):
        for a, coefficient in first[idx]:
            adjoint[a] = (adjoint[a] + adjoint[idx]*coefficient) % p
    program = LinearProgram(c.n, p)
    tangent = [program.zero] * len(gates)
    for idx, g in enumerate(gates):
        if g.op == 'input':
            tangent[idx] = g.value
        else:
            z = program.zero
            for a, coefficient in first[idx]:
                z = program.add(z, program.scale(tangent[a], coefficient))
            tangent[idx] = z
    adjoint_tangent = [program.zero] * len(gates)
    for idx in range(len(gates)-1, -1, -1):
        for a, coefficient in first[idx]:
            term = program.scale(adjoint_tangent[idx], coefficient)
            adjoint_tangent[a] = program.add(adjoint_tangent[a], term)
        for a, b, coefficient in second[idx]:
            term = program.scale(tangent[b], adjoint[idx]*coefficient)
            adjoint_tangent[a] = program.add(adjoint_tangent[a], term)
    program.outputs = adjoint_tangent[:c.n]
    return program, {
        'source_arithmetic_gates': c.arithmetic_gates,
        'source_total_nodes': len(c.gates),
        'emitted_arithmetic_gates': program.arithmetic_gates,
        'emitted_total_nodes': len(program.gates),
        'base_inversions': sum(g.op == 'inv' for g in gates),
        'data_dependent_inversions': 0,
        'scope': 'compiler test; source need not be Fourier or fast'
    }


# Independent degree-two bivariate formal jet algebra, basis 1,t,u,t²,tu,u².
EXP = ((0,0),(1,0),(0,1),(2,0),(1,1),(0,2))
EXP_INDEX = {e:i for i,e in enumerate(EXP)}


def jet_mul(a: list[int], b: list[int], p: int) -> list[int]:
    z = [0]*6
    for i, e in enumerate(EXP):
        for j, f in enumerate(EXP):
            g = (e[0]+f[0], e[1]+f[1])
            if sum(g) <= 2:
                k = EXP_INDEX[g]
                z[k] = (z[k] + a[i]*b[j]) % p
    return z


def jet_inv(a: list[int], p: int) -> list[int]:
    if a[0] == 0:
        raise ZeroDivisionError('nonregular formal jet')
    inv = pow(a[0], -1, p)
    delta = a.copy()
    delta[0] = 0
    square = jet_mul(delta, delta, p)
    z = [(int(i == 0)*inv - inv*inv*delta[i] + inv**3*square[i]) % p for i in range(6)]
    return z


def two_direction_jet(c: Circuit, v: Sequence[int], w: Sequence[int]) -> list[int]:
    if len(v) != c.n or len(w) != c.n:
        raise ValueError('direction dimension mismatch')
    vals = []
    p = c.p
    for g in c.gates:
        if g.op == 'input':
            z = [0, v[g.value] % p, w[g.value] % p, 0, 0, 0]
        elif g.op == 'const':
            z = [g.value,0,0,0,0,0]
        elif g.op == 'add':
            z = [(a+b)%p for a,b in zip(vals[g.a], vals[g.b])]
        elif g.op == 'sub':
            z = [(a-b)%p for a,b in zip(vals[g.a], vals[g.b])]
        elif g.op == 'mul':
            z = jet_mul(vals[g.a], vals[g.b], p)
        elif g.op == 'inv':
            z = jet_inv(vals[g.a], p)
        else:
            raise ValueError('unsupported jet operation')
        vals.append(z)
    return vals[c.output]


def direct_dft(x: Sequence[int], root: int, p: int) -> list[int]:
    n = len(x)
    return [sum(x[j]*pow(root, j*k, p) for j in range(n)) % p for k in range(n)]


def dense_fourier_potential(n: int, root: int, p: int, noise: str = 'none') -> Circuit:
    """DELIBERATELY QUADRATIC-SIZE reference, not a fast synthesis."""
    c = Circuit(n, p)
    out = c.const(0)
    half = pow(2, -1, p)
    for i in range(n):
        out = c.add(out, c.mul(c.const(half*pow(root,i*i,p)), c.mul(i,i)))
        for j in range(i+1, n):
            out = c.add(out, c.mul(c.const(pow(root,i*j,p)), c.mul(i,j)))
    if noise != 'none' and n >= 3:
        term = c.mul(c.mul(0,1),2)
        if noise == 'rational':
            term = c.mul(term, c.inv(c.add(c.const(1),0)))
        elif noise != 'polynomial':
            raise ValueError('unknown noise kind')
        out = c.add(out, term)
    c.output = out
    return c


def four_point_potential(root: int, p: int) -> Circuit:
    """Classical small control: Q4=(x0+x2)^2/2+(x0-x2)(x1+x3)+i(x1-x3)^2/2."""
    if pow(root,2,p) != p-1:
        raise ValueError('root must have order four')
    c = Circuit(4,p)
    a,b = c.add(0,2), c.sub(0,2)
    d,e = c.add(1,3), c.sub(1,3)
    t1 = c.mul(c.const(pow(2,-1,p)),c.mul(a,a))
    t2 = c.mul(b,d)
    t3 = c.mul(c.const(root*pow(2,-1,p)),c.mul(e,e))
    c.output = c.add(c.add(t1,t2),t3)
    return c


def prefix_square_potential(n: int, p: int) -> Circuit:
    """Linear-size, dense-full-rank Hessian, but NOT Fourier."""
    c = Circuit(n,p)
    prefix = out = c.const(0)
    half = c.const(pow(2,-1,p))
    for i in range(n):
        prefix = c.add(prefix,i)
        out = c.add(out,c.mul(half,c.mul(prefix,prefix)))
    c.output = out
    return c
