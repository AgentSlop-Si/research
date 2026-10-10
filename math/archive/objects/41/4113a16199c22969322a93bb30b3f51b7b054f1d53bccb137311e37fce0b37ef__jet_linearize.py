"""Exact first-derivative linearization of arbitrary arithmetic DAGs over F_p.

This is an auditing device, NOT a fast Fourier algorithm.  Its purpose is to
check that nonlinear algebraic intermediate computations cannot by themselves
reduce the unrestricted algebraic circuit complexity of an exact linear map.

Supported gates: inputs, field constants, +, -, *, /.  Division requires a
nonzero denominator at the selected base point.  Tangent outputs are linear in
new formal direction inputs.  The basepoint and its cost are explicit.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

P = 998244353
ROOT = 3


@dataclass(frozen=True)
class Gate:
    op: str
    a: int = -1
    b: int = -1
    v: int = 0


class ArithmeticDAG:
    def __init__(self, p: int = P):
        self.p = p
        self.gates: list[Gate] = []
        self.vars: list[int] = []
        self.constant_cache: dict[int, int] = {}

    def _put(self, op: str, a=-1, b=-1, v=0) -> int:
        self.gates.append(Gate(op, a, b, v))
        return len(self.gates) - 1

    def var(self) -> int:
        k = self._put('var', v=len(self.vars))
        self.vars.append(k)
        return k

    def const(self, v: int) -> int:
        v %= self.p
        if v not in self.constant_cache:
            self.constant_cache[v] = self._put('const', v=v)
        return self.constant_cache[v]

    def add(self, a: int, b: int) -> int:
        return self._put('add', a, b)

    def sub(self, a: int, b: int) -> int:
        return self._put('sub', a, b)

    def mul(self, a: int, b: int) -> int:
        return self._put('mul', a, b)

    def div(self, a: int, b: int) -> int:
        return self._put('div', a, b)

    def scale(self, a: int, v: int) -> int:
        v %= self.p
        if v == 1:
            return a
        if v == 0:
            return self.const(0)
        return self.mul(self.const(v), a)

    def eval_all(self, inputs: Sequence[int]) -> list[int]:
        if len(inputs) != len(self.vars):
            raise ValueError('Incorrect number of inputs')
        out = []
        p = self.p
        for g in self.gates:
            if g.op == 'var':
                v = int(inputs[g.v]) % p
            elif g.op == 'const':
                v = g.v
            else:
                a, b = out[g.a], out[g.b]
                if g.op == 'add':
                    v = (a + b) % p
                elif g.op == 'sub':
                    v = (a - b) % p
                elif g.op == 'mul':
                    v = a * b % p
                elif g.op == 'div':
                    if b == 0:
                        raise ZeroDivisionError('Rational circuit singular at this input')
                    v = a * pow(b, -1, p) % p
                else:
                    raise ValueError(g.op)
            out.append(v)
        return out

    def evaluate(self, inputs: Sequence[int], outputs: Sequence[int]) -> list[int]:
        v = self.eval_all(inputs)
        return [v[i] for i in outputs]

    def cost(self) -> int:
        return sum(g.op not in ('const', 'var') for g in self.gates)


class LinearDAG:
    """Linear circuit with only additions, subtractions and scalar multiplications."""
    def __init__(self, nvar: int, p: int):
        self.p = p
        self.gates: list[Gate] = [Gate('zero')]
        self.zero = 0
        self.vars = [self._put('var', v=i) for i in range(nvar)]
        self._scale_cache: dict[tuple[int, int], int] = {}
        self._add_cache: dict[tuple[str,int,int], int] = {}

    def _put(self, op: str, a=-1, b=-1, v=0):
        self.gates.append(Gate(op, a, b, v))
        return len(self.gates)-1

    def scale(self, a: int, c: int) -> int:
        c %= self.p
        if a == 0 or c == 0:
            return 0
        if c == 1:
            return a
        key = (a, c)
        if key not in self._scale_cache:
            self._scale_cache[key] = self._put('scale', a=a, v=c)
        return self._scale_cache[key]

    def add(self, a: int, b: int) -> int:
        if a == 0:
            return b
        if b == 0:
            return a
        if a > b:
            a, b = b, a
        key = ('add',a,b)
        if key not in self._add_cache:
            self._add_cache[key] = self._put('add', a,b)
        return self._add_cache[key]

    def sub(self, a: int, b: int) -> int:
        if b == 0:
            return a
        if a == b:
            return 0
        if a == 0:
            return self.scale(b,-1)
        key = ('sub',a,b)
        if key not in self._add_cache:
            self._add_cache[key] = self._put('sub', a,b)
        return self._add_cache[key]

    def evaluate(self, direction: Sequence[int], outputs: Sequence[int]) -> list[int]:
        if len(direction) != len(self.vars):
            raise ValueError('Incorrect number of direction inputs')
        vals = []
        for g in self.gates:
            if g.op == 'zero':
                v = 0
            elif g.op == 'var':
                v = direction[g.v] % self.p
            elif g.op == 'scale':
                v = g.v * vals[g.a] % self.p
            elif g.op == 'add':
                v = (vals[g.a] + vals[g.b]) % self.p
            elif g.op == 'sub':
                v = (vals[g.a] - vals[g.b]) % self.p
            else:
                raise ValueError(g.op)
            vals.append(v)
        return [vals[i] for i in outputs]

    def cost(self):
        return sum(g.op not in ('zero','var') for g in self.gates)


def linearize(arith: ArithmeticDAG, outputs: Sequence[int], basepoint: Sequence[int]):
    """Return linear DAG for Jacobian(basepoint) * direction.

    All Jacobian constants are exact.  Computing arith.eval_all(basepoint)
    costs at most the original s arithmetic gates and is charged separately;
    selecting a nonsingular basepoint may have additional cost.
    """
    at = arith.eval_all(basepoint)
    lin = LinearDAG(len(arith.vars), arith.p)
    tangent: list[int] = []
    for i, g in enumerate(arith.gates):
        if g.op == 'const':
            out = 0
        elif g.op == 'var':
            out = lin.vars[g.v]
        else:
            a, b = tangent[g.a], tangent[g.b]
            if g.op == 'add':
                out = lin.add(a,b)
            elif g.op == 'sub':
                out = lin.sub(a,b)
            elif g.op == 'mul':
                out = lin.add(lin.scale(a,at[g.b]),lin.scale(b,at[g.a]))
            elif g.op == 'div':
                inv = pow(at[g.b],-1,arith.p)
                out = lin.sub(lin.scale(a, inv),lin.scale(b,at[g.a]*inv*inv))
            else:
                raise ValueError(g.op)
        tangent.append(out)
    assert lin.cost() <= 3*arith.cost(), (lin.cost(), arith.cost())
    return lin, [tangent[i] for i in outputs]


def eval_dual(arith: ArithmeticDAG, base: Sequence[int], direction: Sequence[int], outputs: Sequence[int]):
    """Independent first-order dual-field interpreter, for cross-checks."""
    if len(base)!=len(arith.vars) or len(direction)!=len(arith.vars):
        raise ValueError('length mismatch')
    vs = []
    for g in arith.gates:
        if g.op == 'const':
            a,b=g.v,0
        elif g.op == 'var':
            a,b=base[g.v]%arith.p,direction[g.v]%arith.p
        else:
            x,dx=vs[g.a]
            y,dy=vs[g.b]
            if g.op=='add':
                a,b=x+y,dx+dy
            elif g.op=='sub':
                a,b=x-y,dx-dy
            elif g.op=='mul':
                a,b=x*y,x*dy+y*dx
            elif g.op=='div':
                inv=pow(y,-1,arith.p)
                a,b=x*inv,(dx*y-x*dy)*inv*inv
            else:
                raise ValueError(g.op)
            a%=arith.p;b%=arith.p
        vs.append((a,b))
    return [vs[i][1] for i in outputs]


def fft_dag(arith: ArithmeticDAG, data: Sequence[int], w: int) -> list[int]:
    n = len(data)
    if n==1:
        return list(data)
    if n<1 or n&(n-1):
        raise ValueError('power of 2 length required')
    even = fft_dag(arith,data[::2],w*w%arith.p)
    odd = fft_dag(arith,data[1::2],w*w%arith.p)
    out = [0]*n
    phase=1
    for j in range(n//2):
        t=arith.scale(odd[j], phase)
        out[j]=arith.add(even[j],t)
        out[j+n//2]=arith.sub(even[j],t)
        phase=phase*w % arith.p
    return out


def build_fft(n: int, p=P, root=ROOT):
    if n<2 or n&(n-1) or (p-1)%n:
        raise ValueError('supported radix-2 NTT length required')
    d=ArithmeticDAG(p)
    x=[d.var() for _ in range(n)]
    w=pow(root,(p-1)//n,p)
    return d,x,fft_dag(d,x,w),w


def build_nonlinear_fft(n:int, method='square'):
    d,x,y,w=build_fft(n)
    if method=='square':
        # Exact identity s = ((s+c)^2 - s^2 - c^2)/(2c)
        c=d.const(7)
        cc=d.const(49)
        out=[]
        for s in y:
            z=d.add(s,c)
            a=d.mul(z,z)
            b=d.mul(s,s)
            u=d.sub(d.sub(a,b),cc)
            out.append(d.scale(u,pow(14,-1,d.p)))
    elif method=='rational':
        # Works whenever denominator 1+x[0] is nonzero.
        denom=d.add(d.const(1),x[0])
        out=[d.div(d.mul(s,denom),denom) for s in y]
    elif method=='baseline':
        # Generalized user A-k rewrite, with arbitrary *nonlinear* k(x).
        # DFT(x-k*e_0) + k*DFT(e_0) = DFT(x) identically.
        k=d.add(d.mul(x[0],x[1]),x[0])
        shifted=list(x)
        shifted[0]=d.sub(shifted[0],k)
        y_shift=fft_dag(d,shifted,w)
        out=[d.add(s,k) for s in y_shift]
    else:
        raise ValueError('unknown method')
    return d,x,out


def direct_dft(x:Sequence[int],w:int,p=P) -> list[int]:
    n=len(x)
    return [sum(int(x[j])*pow(w,j*k,p) for j in range(n))%p for k in range(n)]
