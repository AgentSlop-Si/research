"""Exact additive weaving cost for Winograd tensor circuits.

A codelet i has n_i input/output channels, r_i diagonal channels,
p_i additions before diagonal, and q_i additions after diagonal.
When factors commute as tensor operators, reordering independent preweaves
and postweaves is valid. Sorting the input transforms by (r_i-n_i)/p_i
ascending and output transforms by (r_i-n_i)/q_i descending is optimal.
"""
from dataclasses import dataclass
from itertools import permutations
from fractions import Fraction

@dataclass(frozen=True)
class Factor:
    name:str
    n:int
    rank:int
    pre:int
    post:int

FACTORS=(Factor('F3',3,3,3,3),Factor('F4',4,4,4,4),Factor('F5',5,6,8,9))

def cost_pre(order):
    total=0;prev=1
    for i,fac in enumerate(order):
        after=1
        for oth in order[i+1:]:after*=oth.n
        total+=prev*fac.pre*after
        prev*=fac.rank
    return total

def cost_post(order):
    total=0;prev=1
    for i,fac in enumerate(order):
        after=1
        for oth in order[i+1:]:after*=oth.rank
        total+=prev*fac.post*after
        prev*=fac.n
    return total

def optimal():
    # before: expansion/add increasing. post: expansion/add decreasing.
    B=sorted(FACTORS,key=lambda f:Fraction(f.rank-f.n,f.pre))
    A=sorted(FACTORS,key=lambda f:Fraction(f.rank-f.n,f.post),reverse=True)
    return B,A,cost_pre(B)+cost_post(A)

def enumerate_results():
    rows=[]
    for o in permutations(FACTORS):
        rows.append({'order':','.join(x.name for x in o), 'pre_adds':cost_pre(o),'post_adds':cost_post(o)})
    return rows

if __name__=='__main__':
    print(enumerate_results())
    B,A,total=optimal()
    print('optimal B:',[f.name for f in B],'A:',[f.name for f in A],'total',total)
    assert total==444
    assert min(r['pre_adds'] for r in enumerate_results())==216
    assert min(r['post_adds'] for r in enumerate_results())==228
