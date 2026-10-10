"""Exact two-stage Fourier incompatibility with arbitrary diagonal gauges.

Factor S_j=diag(left_j) H(a_j,b_j,d_j) diag(right_j).
The two-stage certificate remains valid for every arbitrary internal permutation.
"""
from dataclasses import dataclass
from scan_resolvent import Scan, apply_scan, apply_A, apply_B, permute, e, orientation, apply_dft


def product(x,y,p):return [(a*b)%p for a,b in zip(x,y)]

def invert(x,p):return [pow(int(v),-1,p) for v in x]

@dataclass
class WeightedScan:
    base: Scan
    left: list[int]
    right: list[int]
    def __post_init__(self):
        assert len(self.left)==len(self.right)
        assert all(self.left) and all(self.right)
    def apply(self,x,p):
        return product(self.left,apply_scan(self.base,product(self.right,x,p),p),p)
    def B_left(self,x,p):
        return product(self.left,apply_B(self.base,product(invert(self.left,p),x,p),p),p)
    def B_right(self,x,p):
        return product(invert(self.right,p),apply_B(self.base,product(self.right,x,p),p),p)
    def A(self,x,p):
        return product(self.left,apply_A(self.base,product(self.right,x,p),p),p)


def weighted_two_column_certificate(s1,s2,n,p,w,order):
    direction=orientation(s1.base,p)
    if direction=='+': column_indices=(1,2)
    elif direction=='-': column_indices=(0,1)
    else: raise ValueError('nontrivial scan expected')
    d2=orientation(s2.base,p)
    if d2=='scalar': raise ValueError('nontrivial scan expected')
    lhs=[]; rhs=[]
    for j in column_indices:
        x=e(n,j)
        lhs.append(s2.B_left(apply_dft(s1.B_right(x,p),w,p),p))
        rhs.append(s2.A(permute(s1.A(x,p),order),p))
    # Bound 6 on support of the union of adjacent input columns in RHS.
    support_union=sum(bool(rhs[0][i] or rhs[1][i]) for i in range(n))
    interior_indices=range(n-1) if d2=='+' else range(1,n)
    common_zero=sum(lhs[0][i]==0 and lhs[1][i]==0 for i in interior_indices)
    return {
        'columns':column_indices,'support_union':support_union,
        'left_common_zeros':common_zero,'right_common_zeros':sum(rhs[0][i]==0 and rhs[1][i]==0 for i in interior_indices),
        'left':lhs, 'right':rhs
    }
