"""Boolean-cube polynomial quotient R[x]/(x_i^2-x_i) exact demonstrations.

Exponential expansions are for *small proof tests*, not a practical FFT.
"""
from __future__ import annotations
from math import comb


def quotient_product(a:dict[int,int], b:dict[int,int])->dict[int,int]:
    out={}
    for u,cu in a.items():
        for v,cv in b.items():
            m=u|v  # x_i^2 = x_i
            out[m]=out.get(m,0)+cu*cv
    return {m:c for m,c in out.items() if c}


def power_of_sum(n:int, exponent:int)->dict[int,int]:
    if n<1 or exponent<0: raise ValueError
    base={1<<i:1 for i in range(n)}
    result={0:1}
    while exponent:
        if exponent&1: result=quotient_product(result,base)
        exponent//=2
        if exponent: base=quotient_product(base,base)
    return result


def coefficient_by_onto_functions(degree:int, support:int)->int:
    """# functions from degree labeled factors onto support labeled variables."""
    return sum((-1)**(support-j)*comb(support,j)*j**degree
               for j in range(support+1))


def evaluate_quotient(poly:dict[int,int], x:list[int])->int:
    out=0
    for mask,c in poly.items():
        mon=1
        for i in range(len(x)):
            if mask>>i &1:mon*=x[i]
        out+=c*mon
    return out


def boolean_jet_failure(x:list[int], c:list[list[int]],p:int)->tuple[list[int],list[int]]:
    """FFT linear forms applied to x_i^2: equal on cube, zero derivative at 0."""
    y=[sum(row[i]*x[i]**2 for i in range(len(x)))%p for row in c]
    derivative_at_zero=[0]*len(x)
    return y,derivative_at_zero
