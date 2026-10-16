"""Explicit Fourier endpoint ordering for finite abelian groups of order 4L.

This constructs permutations, NOT a fast Fourier transform. The input is an
explicit direct product of cyclic groups. No decomposition of a black-box group
is performed. Standard-library only. See PROOF.md for model and scope.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import lcm, prod
from random import Random
from typing import Sequence

Element = tuple[int, ...]

@dataclass(frozen=True)
class Group:
    moduli: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.moduli or any(type(n) is not int or n < 2 for n in self.moduli):
            raise ValueError("Provide at least one integer cyclic modulus >= 2")

    @property
    def size(self) -> int:
        return prod(self.moduli)

    @property
    def exponent(self) -> int:
        return lcm(*self.moduli)

    @property
    def zero(self) -> Element:
        return (0,) * len(self.moduli)

    def elements(self):
        return product(*(range(n) for n in self.moduli))

    def add(self, a: Element, b: Element) -> Element:
        return tuple((x+y) % n for x, y, n in zip(a, b, self.moduli))

    def sub(self, a: Element, b: Element) -> Element:
        return tuple((x-y) % n for x, y, n in zip(a, b, self.moduli))

    def pairing_exponent(self, a: Element, x: Element) -> int:
        e = self.exponent
        return sum(u*v*(e//n) for u, v, n in zip(a, x, self.moduli)) % e

    def index(self, a: Element) -> int:
        result = 0
        for x,n in zip(a,self.moduli):
            result = result*n+x
        return result

@dataclass
class Ordering:
    group: Group
    rows: list[Element]
    columns: list[Element]
    row_representatives: list[Element]
    column_representatives: list[Element]
    involution: Element
    character: Element
    row_coset: Element
    column_coset: Element

    def index_permutations(self) -> tuple[list[int],list[int]]:
        return ([self.group.index(a) for a in self.rows],
                [self.group.index(x) for x in self.columns])


def construct(moduli: Sequence[int], seed: int | None = None) -> Ordering:
    """O(k*N) word-operation bound; stores O(k*N) coordinate words.

    For seed=None, use a direct mixed-radix generator: no character or addition
    table and no Fourier matrix. A seed shuffles/flips representative pairs for
    adversarial validation; the proof allows these choices independently.
    """
    g = Group(tuple(moduli)); ns=g.moduli; k=len(ns)
    if g.size % 4:
        raise ValueError("This construction requires group order divisible by four")
    divisible4 = [i for i,n in enumerate(ns) if n%4==0]
    if divisible4:
        i=j=divisible4[0]
    else:
        even=[i for i,n in enumerate(ns) if n%2==0]
        if len(even)<2:
            raise AssertionError("Order-four divisibility did not supply two even factors")
        i,j=even[:2]
    x=[0]*k; chi=[0]*k; tau=[0]*k; t=[0]*k
    x[i]=ns[i]//2; chi[j]=ns[j]//2; tau[i]=1; t[j]=1
    x,chi,tau,t=tuple(x),tuple(chi),tuple(tau),tuple(t)
    cranges=[range(n) for n in ns]; rranges=[range(n) for n in ns]
    if i==j:
        cranges[i]=range(0,ns[i]//2,2)
        rranges[i]=range(0,ns[i]//2,2)
    else:
        cranges[i]=range(ns[i]//2); cranges[j]=range(0,ns[j],2)
        rranges[i]=range(0,ns[i],2); rranges[j]=range(ns[j]//2)
    hr=list(product(*cranges)); ar=list(product(*rranges))
    if seed is not None:
        rng=Random(seed)
        rng.shuffle(hr);rng.shuffle(ar)
        hr=[g.add(h,x) if rng.randrange(2) else h for h in hr]
        ar=[g.add(a,chi) if rng.randrange(2) else a for a in ar]
    hfirst=[z for h in hr for z in (h,g.add(h,x))]
    rfirst=[z for a in ar for z in (a,g.add(a,chi))]
    rows=rfirst+[g.sub(tau,a) for a in reversed(rfirst)]
    columns=hfirst+[g.sub(t,h) for h in reversed(hfirst)]
    if len(rows)!=g.size or len(columns)!=g.size:
        raise AssertionError("Wrong permutation length")
    return Ordering(g,rows,columns,ar,hr,x,chi,tau,t)


def theorem_value(n: int) -> int:
    if type(n) is not int or n < 4 or n%4:
        raise ValueError("The proved theorem here is restricted to N divisible by four")
    return 1 if n==4 else n//4+1


if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('moduli',nargs='+',type=int)
    args=parser.parse_args()
    order=construct(args.moduli)
    rows,cols=order.index_permutations()
    print(json.dumps({'moduli':args.moduli,'N':order.group.size,'rows':rows,
                      'columns':cols,'proved_minimax':theorem_value(order.group.size),
                      'not_a_fast_fourier_transform':True},indent=2))
