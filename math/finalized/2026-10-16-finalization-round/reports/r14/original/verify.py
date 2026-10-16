"""Independent exact-field checks of the ordering and proof identities.

Requires sympy only for splitting primes and characteristic-zero arithmetic.
Finite-field rank checks do NOT certify a universal complex lower bound.
"""
from __future__ import annotations
import argparse,json,time,sys,platform
from itertools import product
from pathlib import Path
from fractions import Fraction
from math import prod
import sympy as sy
from sympy.polys.matrices import DomainMatrix
from annihilator_order import construct,theorem_value,Group


def rank_mod(matrix,p):
    if not matrix or not matrix[0]:return 0
    a=[list(r) for r in matrix];n=len(a);m=len(a[0]);rank=0
    for c in range(m):
        pivot=next((j for j in range(rank,n) if a[j][c]%p),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][c],-1,p)
        row=[v*inv%p for v in a[rank]];a[rank]=row
        for j in range(rank+1,n):
            v=a[j][c]
            if v:a[j]=[(u-v*w)%p for u,w in zip(a[j],row)]
        rank+=1
        if rank==n:break
    return rank


def all_cuts(a,rank):
    n=len(a)
    return ([rank([row[k:] for row in a[:k]]) for k in range(n+1)],
            [rank([row[:k] for row in a[k:]]) for k in range(n+1)])


def prime_root(e,start):
    p=int(sy.nextprime(start))
    while (p-1)%e:p=int(sy.nextprime(p))
    z=pow(int(sy.primitive_root(p)),(p-1)//e,p)
    assert pow(z,e,p)==1
    assert all(pow(z,e//int(q),p)!=1 for q in sy.factorint(e))
    return p,z


def matrix_exponents(order):
    g=order.group
    return ([[g.pairing_exponent(a,x) for x in order.columns] for a in order.rows],
            [[g.pairing_exponent(a,x) for x in order.column_representatives]
             for a in order.row_representatives])


def validate_order(order):
    g=order.group;n=g.size;e=g.exponent
    assert len(set(order.rows))==n and len(set(order.columns))==n
    x,chi=order.involution,order.character
    assert x!=g.zero and g.add(x,x)==g.zero
    assert chi!=g.zero and g.add(chi,chi)==g.zero
    assert g.pairing_exponent(chi,x)==0
    assert g.pairing_exponent(order.row_coset,x)==e//2
    assert g.pairing_exponent(chi,order.column_coset)==e//2
    assert all(g.pairing_exponent(a,x)==0 for a in order.rows[:n//2])
    assert all(g.pairing_exponent(chi,h)==0 for h in order.columns[:n//2])
    assert all(order.rows[n-1-j]==g.sub(order.row_coset,order.rows[j]) for j in range(n))
    assert all(order.columns[n-1-j]==g.sub(order.column_coset,order.columns[j]) for j in range(n))


def check_field(order,p,z):
    validate_order(order);n=order.group.size;ae,qe=matrix_exponents(order)
    a=[[pow(z,x,p) for x in row] for row in ae]
    q=[[pow(z,x,p) for x in row] for row in qe]
    r,s=all_cuts(a,lambda a:rank_mod(a,p));qr,qs=all_cuts(q,lambda a:rank_mod(a,p))
    for k in range(n//2+1):
        assert r[k]==(k+1)//2+qr[k//2]
        assert s[k]==(k+1)//2+qs[k//2]
    assert all(r[k]==s[n-k] for k in range(n+1))
    assert max(r+s)==theorem_value(n)
    return {'p':p,'upper':r,'lower':s,'quotient_upper':qr,'quotient_lower':qs,
            'rank_computations':2*(n+1)+2*(n//4+1)}


def check_charzero(moduli):
    order=construct(moduli);validate_order(order);ae,qe=matrix_exponents(order)
    k=sy.QQ.cyclotomic_field(order.group.exponent);z=k.unit
    powers=[k.one]
    for _ in range(1,order.group.exponent):powers.append(powers[-1]*z)
    def mat(ex):return [[powers[x] for x in row] for row in ex]
    def rank(a):
        if not a or not a[0]:return 0
        return DomainMatrix(a,(len(a),len(a[0])),k).rank()
    a=mat(ae);q=mat(qe);r,s=all_cuts(a,rank);qr,qs=all_cuts(q,rank)
    n=order.group.size
    for cut in range(n//2+1):
        assert r[cut]==(cut+1)//2+qr[cut//2]
        assert s[cut]==(cut+1)//2+qs[cut//2]
    assert all(r[cut]==s[n-cut] for cut in range(n+1))
    assert max(r+s)==theorem_value(n)
    return {'moduli':moduli,'N':n,'field':f'Q(zeta_{order.group.exponent})',
            'upper':r,'lower':s,'quotient_upper':qr,'quotient_lower':qs,
            'rank_computations':2*(n+1)+2*(n//4+1)}


def partitions(n,cap=None):
    if n==0:
        yield ();return
    for k in range(min(n,cap or n),0,-1):
        for rest in partitions(n-k,k):yield (k,)+rest


def types_of_order(n):
    choices=[]
    for p,e in sy.factorint(n).items():
        choices.append([tuple(int(p)**a for a in part) for part in partitions(int(e))])
    for combo in product(*choices):yield tuple(v for fac in combo for v in fac)


def modular_suite():
    cases=[];distinct=[];count=0
    for n in [4,8,12,16,20,24,28,32,36,40,48]:
        for moduli in types_of_order(n):
            distinct.append(moduli)
            for seed in [None,1701+n]:
                order=construct(moduli,seed);p,z=prime_root(order.group.exponent,100)
                first=check_field(order,p,z);p2,z2=prime_root(order.group.exponent,p)
                second=check_field(order,p2,z2)
                count+=first['rank_computations']+second['rank_computations']
                cases.append({'moduli':moduli,'N':n,'seed':seed,'fields':[first,second]})
    # Extra composite cyclic layouts and one larger dyadic layout.
    for moduli in [(12,),(20,),(24,),(28,),(36,),(40,),(48,),(64,)]:
        order=construct(moduli,99);p,z=prime_root(order.group.exponent,100)
        result=check_field(order,p,z);count+=result['rank_computations']
        cases.append({'moduli':moduli,'N':order.group.size,'seed':99,'fields':[result]})
    rational=[]
    for L in range(2,10002):
        n=4*L;h=2*L+1;r=2*L-1
        import math
        assert math.gcd(n,h)==1
        lower=Fraction(r*h,n)+Fraction(r*(n-r),n*n)
        B=Fraction(h*(n-r),n)-Fraction(r*(n-r),n*n)
        assert lower>L and B<L+1 and B>=0
        if L<=10:rational.append({'N':n,'rank_lower_before_ceiling':str(lower),'B':str(B)})
    rejected=0
    for mod in [(2,),(3,),(6,),(9,),(),(0,),(1,),(2.0,)]:
        try:construct(mod)
        except ValueError:rejected+=1
        else:raise AssertionError(f'invalid shape accepted: {mod}')
    return {'scope':'finite splitting fields; not a universal characteristic-zero lower proof',
            'distinct_abelian_group_types':len(distinct),'construction_cases':len(cases),
            'field_runs':sum(len(c['fields']) for c in cases),
            'rank_computations_including_quotients_and_empty_cuts':count,
            'rational_margin_cases':10000,'rejections':rejected,'cases':cases,
            'sample_rational_margins':rational}


def charzero_suite():
    cases=[(4,),(2,2),(8,),(4,2),(2,2,2),(12,),(2,2,3),(16,),(4,4),(20,),(2,2,5),(24,),(4,2,3)]
    out=[check_charzero(mod) for mod in cases]
    return {'scope':'exact arithmetic in cyclotomic number fields, not floating point',
            'construction_cases':len(out),
            'rank_computations_including_quotients_and_empty_cuts':sum(c['rank_computations'] for c in out),
            'cases':out}


def main():
    if not __debug__:
        raise RuntimeError("Run without -O: verification requires assertions enabled")
    ap=argparse.ArgumentParser();ap.add_argument('--suite',choices=['modular','charzero','all'],default='all')
    ap.add_argument('--output',default='validation.json');args=ap.parse_args();t=time.perf_counter()
    result={'status':'PASS','python':sys.version,'sympy':sy.__version__,'platform':platform.platform(),
            'model':'rank verification only; no Fourier runtime benchmark'}
    if args.suite in ('all','modular'):result['modular']=modular_suite()
    if args.suite in ('all','charzero'):result['charzero']=charzero_suite()
    result['elapsed_seconds']=time.perf_counter()-t
    Path(args.output).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk not in ('cases','sample_rational_margins')}
                       if isinstance(v,dict) else v for k,v in result.items()},indent=2))
if __name__=='__main__':main()
