"""Exact finite-field simulation of differentiating a selected arithmetic branch.

The mathematical generic-open-branch theorem is over infinite fields; modular
experiments are only exact finite checks of the algebra, not a proof of the
real/complex open-set statement.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Node:
    op: str
    a: int = -1
    b: int = -1
    c: int = 0


class Circuit:
    def __init__(self, n: int, p: int):
        self.n, self.p = n, p
        self.nodes = [Node('input', c=i) for i in range(n)]
        self.outputs: list[int] = []

    def const(self, c: int) -> int:
        self.nodes.append(Node('const', c=c % self.p))
        return len(self.nodes) - 1

    def add(self, a: int, b: int) -> int:
        self.nodes.append(Node('add', a=a, b=b))
        return len(self.nodes) - 1

    def sub(self, a: int, b: int) -> int:
        self.nodes.append(Node('sub', a=a, b=b))
        return len(self.nodes) - 1

    def mul(self, a: int, b: int) -> int:
        self.nodes.append(Node('mul', a=a, b=b))
        return len(self.nodes) - 1

    def div(self, a: int, b: int) -> int:
        self.nodes.append(Node('div', a=a, b=b))
        return len(self.nodes) - 1

    def scale(self, a: int, c: int) -> int:
        self.nodes.append(Node('scale', a=a, c=c % self.p))
        return len(self.nodes) - 1

    def eval_all(self, x: Sequence[int]) -> list[int]:
        assert len(x) == self.n
        p = self.p
        v: list[int] = []
        for g in self.nodes:
            if g.op == 'input': val = int(x[g.c])
            elif g.op == 'const': val = g.c
            elif g.op == 'add': val = v[g.a] + v[g.b]
            elif g.op == 'sub': val = v[g.a] - v[g.b]
            elif g.op == 'mul': val = v[g.a] * v[g.b]
            elif g.op == 'div': val = v[g.a] * pow(v[g.b], -1, p)
            elif g.op == 'scale': val = v[g.a] * g.c
            else: raise ValueError(g.op)
            v.append(val % p)
        return v

    def evaluate(self, x: Sequence[int]) -> list[int]:
        v = self.eval_all(x)
        return [v[i] for i in self.outputs]

    @property
    def cost(self) -> int:
        return sum(g.op not in ('input', 'const') for g in self.nodes)


class LinearProgram:
    def __init__(self, n: int, p: int):
        self.n, self.p = n, p
        self.nodes = [Node('input', c=i) for i in range(n)] + [Node('zero')]
        self.zero = n
        self.outputs: list[int] = []

    def scale(self, u: int, k: int) -> int:
        k %= self.p
        if k == 0 or u == self.zero: return self.zero
        if k == 1: return u
        self.nodes.append(Node('scale', a=u, c=k))
        return len(self.nodes)-1

    def add(self, u: int, v: int) -> int:
        if u == self.zero: return v
        if v == self.zero: return u
        self.nodes.append(Node('add', a=u, b=v))
        return len(self.nodes)-1

    def sub(self, u: int, v: int) -> int:
        if v == self.zero: return u
        if u == self.zero: return self.scale(v, -1)
        self.nodes.append(Node('sub', a=u, b=v))
        return len(self.nodes)-1

    def evaluate(self, x: Sequence[int]) -> list[int]:
        p = self.p
        values = []
        for g in self.nodes:
            if g.op == 'input': y = int(x[g.c])
            elif g.op == 'zero': y = 0
            elif g.op == 'scale': y = values[g.a]*g.c
            elif g.op == 'add': y = values[g.a]+values[g.b]
            elif g.op == 'sub': y = values[g.a]-values[g.b]
            else: raise ValueError(g.op)
            values.append(y%p)
        return [values[i] for i in self.outputs]

    @property
    def cost(self) -> int:
        return sum(g.op not in ('input','zero') for g in self.nodes)


def differentiate(c: Circuit, base: Sequence[int]) -> LinearProgram:
    """Linear circuit for the directional derivative of every selected output.

    The branch has ALREADY been fixed by a nonempty-open-cell selector.
    For a circuit with s arithmetic gates, extracted cost <= 3s.
    Values at base are treated as prepared constants (nonuniform conversion).
    """
    values = c.eval_all(base)
    lin = LinearProgram(c.n, c.p)
    tangent: list[int] = []
    for g in c.nodes:
        if g.op == 'input': v = g.c
        elif g.op == 'const': v = lin.zero
        elif g.op == 'add': v = lin.add(tangent[g.a], tangent[g.b])
        elif g.op == 'sub': v = lin.sub(tangent[g.a], tangent[g.b])
        elif g.op == 'scale': v = lin.scale(tangent[g.a], g.c)
        elif g.op == 'mul':
            v = lin.add(lin.scale(tangent[g.a], values[g.b]),
                        lin.scale(tangent[g.b], values[g.a]))
        elif g.op == 'div':
            val = values[g.b]
            if val == 0: raise ZeroDivisionError('branch base point is singular')
            v = lin.sub(lin.scale(tangent[g.a], pow(val,-1,c.p)),
                        lin.scale(tangent[g.b], values[g.a]*pow(val,-2,c.p)))
        else: raise ValueError(g.op)
        tangent.append(v)
    lin.outputs = [tangent[i] for i in c.outputs]
    assert lin.cost <= 3*c.cost
    return lin


def primitive_nth_root(n: int,p: int=998244353,g: int=3) -> int:
    if n<2 or n&(n-1) or (p-1)%n: raise ValueError('power-of-two supported root needed')
    for candidate in (g, *range(2,min(p,4096))):
        w=pow(candidate,(p-1)//n,p)
        if pow(w,n,p)==1 and pow(w,n//2,p)!=1:
            return w
    raise ValueError('no primitive root located')


def transform_fft_gates(c: Circuit, inputs: Sequence[int], omega: int) -> list[int]:
    """Unnormalized forward radix-two FFT with exact modular twiddles."""
    n=len(inputs)
    bits=n.bit_length()-1
    a=[inputs[int(format(j,f'0{bits}b')[::-1],2)] for j in range(n)]
    width=2
    while width<=n:
        step=pow(omega,n//width,c.p)
        for start in range(0,n,width):
            w=1
            for j in range(width//2):
                i=start+j
                k=i+width//2
                u,v=a[i], c.scale(a[k],w)
                a[i],a[k]=c.add(u,v),c.sub(u,v)
                w=w*step%c.p
        width*=2
    return a


def build_adaptive(n: int, base: Sequence[int], p: int=998244353,
                   mode: str='polynomial') -> tuple[Circuit,str]:
    """A fixed path in an adaptive k(x) program.

    For general inputs, the program chooses a path based on input sign and
    denominator-zero tests. The selected path is an EXACT identity on its
    nonsingular domain, so its derivative is the complete FFT matrix.
    """
    c=Circuit(n,p)
    omega=primitive_nth_root(n,p)
    x=list(range(n))
    i=n//3
    if mode=='polynomial':
        s=c.add(x[0],x[1])
        k=c.add(c.mul(s,s),c.scale(x[0],7))
        label='branch: polynomial baseline'
    elif mode=='rational':
        numer=c.add(c.mul(x[0],x[1]), x[0])
        denom=c.add(c.const(1),c.mul(x[-1],x[-1]))
        if (1+int(base[-1])**2)%p==0:
            k=c.mul(x[0],x[0]);label='branch: rational singularity fallback'
        else:
            k=c.div(numer,denom);label='branch: rational baseline'
    elif mode=='sign_branch':
        signed=int(base[0])%p
        if signed <= p//2:
            k=c.mul(x[0],x[0]);label='branch: nonnegative representative'
        else:
            k=c.mul(x[1],x[1]);label='branch: negative representative'
    else:
        raise ValueError(mode)
    modified=x[:]
    modified[i]=c.sub(x[i],k)
    out=transform_fft_gates(c,modified,omega)
    c.outputs=[c.add(y,c.scale(k,pow(omega,i*j,p))) for j,y in enumerate(out)]
    return c,label


def reference_dft(x: Sequence[int],p: int=998244353) -> list[int]:
    n=len(x);w=primitive_nth_root(n,p)
    return [sum(int(x[j])*pow(w,k*j,p) for j in range(n))%p for k in range(n)]
