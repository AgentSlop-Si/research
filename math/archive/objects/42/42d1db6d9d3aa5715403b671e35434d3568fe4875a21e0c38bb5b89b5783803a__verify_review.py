"""Bounded independent audit of Green mixers and the Fourier path bridge.

Uses independent dense rational/modular references and field-call probes.
No candidate audit helpers, matrix generators, or expected answers imported.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parent.parent


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec)
    sys.modules[name]=obj
    spec.loader.exec_module(obj)
    return obj


ESCAPE=module('reviewed_green_escape',ROOT/'fft_green_fusion_research/resolvent_escape.py')
BRIDGE=module('reviewed_path_bridge',ROOT/'fft_green_conditioned_bridge_research/green_bridge.py')


class Probe:
    def __init__(self,p=None):
        self.p=p;self.zero=0 if p else Q(0);self.one=1 if p else Q(1)
        self.calls=Counter()
    def reduce(self,x):return x%self.p if self.p else Q(x)
    def add(self,a,b):self.calls['add']+=1;return self.reduce(a+b)
    def sub(self,a,b):self.calls['sub']+=1;return self.reduce(a-b)
    def mul(self,a,b):self.calls['mul']+=1;return self.reduce(a*b)
    def inv(self,a):
        self.calls['inverse']+=1
        return pow(a,-1,self.p) if self.p else 1/Q(a)
    def integer(self,a):self.calls['integer_embed']+=1;return self.reduce(a)


def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def reduce(x,p):return x%p if p else Q(x)
def mm(a,b,p=None):
    return [[reduce(sum(x*y for x,y in zip(row,col)),p) for col in zip(*b)] for row in a]
def mv(a,x,p=None):return [reduce(sum(u*v for u,v in zip(row,x)),p) for row in a]
def add(a,b,p=None):return [[reduce(x+y,p) for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,b,p=None):return [[reduce(x-y,p) for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def inverse(a,p=None):
    n=len(a);a=[[reduce(x,p) for x in row]+[reduce(int(i==j),p) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:raise ValueError('singular matrix')
        a[j],a[pivot]=a[pivot],a[j]
        factor=pow(a[j][j],-1,p) if p else 1/a[j][j]
        a[j]=[reduce(x*factor,p) for x in a[j]]
        for i in range(n):
            if i!=j:
                factor=a[i][j]
                a[i]=[reduce(x-factor*y,p) for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]


def norm1(a):return max(sum(abs(x) for x in col) for col in zip(*a))


def root(n,p):
    for a in range(2,p):
        q=pow(a,(p-1)//n,p)
        if pow(q,n,p)==1 and pow(q,n//2,p)!=1:return q
    raise ValueError('root unavailable')


def fourier(n,q,p):return [[pow(q,i*j,p) for j in range(n)] for i in range(n)]


def signed_norm_checks():
    records=[]
    for n in (1,2,3,4,8,12):
        c=[[0]*n for _ in range(n)]
        for i in range(n-1):c[i][i+1]=1
        c[-1][0]=-1
        k=add(eye(n),inverse(sub(eye(n),c)))
        ki=inverse(k)
        assert all(v for row in k for v in row)
        assert all(v for row in ki for v in row)
        assert norm1(k)==Q(n+2,2)
        assert norm1(ki)==Q(2**n,2**n+1)
        condition=norm1(k)*norm1(ki)
        assert condition==Q((n+2)*2**(n-1),2**n+1)
        for j in range(n):
            x=[Q(int(i==j)) for i in range(n)]
            probe=Probe()
            out,counts,setup=ESCAPE.signed_cycle_forward(probe,x)
            assert out==mv(k,x)
            assert counts==dict(probe.calls)
            assert sum(setup.values())==2 and sum(counts.values())==3*n+1
        if n==2:
            gram=mm([list(row) for row in zip(*k)],k)
            assert gram==[[Q(5,2),0],[0,Q(5,2)]]
        records.append({'N':n,'norm1_K':str(norm1(k)),'norm1_inverse':str(norm1(ki)),
                        'kappa1':str(condition),'cold_signed_application_gates':3*n+1})
    return records


def affine_checks():
    records=[]
    for p,n in ((3,2),(17,2),(97,2),(97,4),(97,8)):
        q=root(n,p)
        f=fourier(n,q,p);fi=inverse(f,p)
        for a,b,h in ((5,1,1),(1,-1,-3),(9,3,5)):
            probe=Probe(p)
            plan=ESCAPE.prepare_affine(probe,n,q,a,b,h)
            assert plan.preparation_counts==dict(probe.calls)
            assert sum(probe.calls.values())==2*n+(n.bit_length()-1)+4
            m=[[0]*n for _ in range(n)]
            for i in range(n):m[i][(a*i+h)%n]=pow(q,b*i%n,p)
            k=add(eye(n),inverse(sub(eye(n),m,p),p),p)
            ki=inverse(k,p)
            target=mm(mm(f,k,p),fi,p);target_inv=inverse(target,p)
            for j in range(n):
                x=[int(i==j) for i in range(n)]
                for is_target,is_inverse,reference in ((False,False,k),(False,True,ki),
                                                       (True,False,target),(True,True,target_inv)):
                    before=Counter(probe.calls)
                    out,counts=plan.apply(probe,x,target=is_target,inverse=is_inverse)
                    assert out==mv(reference,x,p)
                    assert counts==dict(probe.calls-before)
                    assert sum(counts.values())==(6 if is_inverse else 5)*n+1
            records.append({'p':p,'N':n,'descriptor':[a,b,h],
                            'matrix_K_nonzeros':sum(bool(v) for row in k for v in row)})
    invalid=0
    for p,n in ((5,2),(17,4),(257,8),(65537,16)):
        try:ESCAPE.prepare_affine(Probe(p),n,root(n,p))
        except ValueError as e:assert 'singular numerator' in str(e);invalid+=1
        else:raise AssertionError('singular modular numerator accepted')
    for permutation in ([],[0,1],[1,1],[2,0]):
        try:ESCAPE.cycle_order(permutation)
        except ValueError:invalid+=1
        else:raise AssertionError('invalid cycle accepted')
    return {'cases':records,'invalid_cases':invalid}


def bridge_checks():
    records=[]
    p=65537
    for n in (4,8):
        q=root(n,p);probe=Probe(p);plan=BRIDGE.FourierPathGreen(probe,n,q)
        assert plan.preparation_operations==dict(probe.calls)
        t=[[3 if i==j else -1 if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)]
        t=[[v%p for v in row] for row in t]
        f=fourier(n,q,p);fi=inverse(f,p);h=mm(mm(f,t,p),fi,p)
        s=add(inverse(t,p),inverse(add(t,eye(n),p),p),p)
        si=inverse(s,p);fsfi=mm(mm(f,s,p),fi,p);fsifi=mm(mm(f,si,p),fi,p)
        for k in range(n):
            for l in range(n):
                expected=((3-pow(q,k,p)-pow(q,-k,p))*(k==l)
                          +pow(n,-1,p)*(pow(q,l,p)+pow(q,-k,p)))%p
                assert h[k][l]==expected
        x=[(i+1)**2%p for i in range(n)];y=mv(f,x,p)
        checks=[(plan.source_t,x,t),(plan.target_h,y,h),(plan.source_s,x,s),
                (plan.source_s_inverse,x,si),(plan.target_s,y,fsfi),
                (plan.target_s_inverse,y,fsifi)]
        for fn,values,reference in checks:assert fn(values)==mv(reference,values,p)
        assert dict(plan.c.count)==dict(probe.calls)
        for fn in (plan.source_t,plan.target_h,plan.source_solve,plan.target_solve):
            for length in (n-1,n+1):
                try:fn([0]*length)
                except ValueError:pass
                else:raise AssertionError('invalid input length accepted')
        records.append({'N':n,'entrywise_rank2_identity_checks':n*n,
                        'direct_dense_operator_comparisons':len(checks)})
    return records


def main():
    signed=signed_norm_checks()
    affine=affine_checks()
    bridge=bridge_checks()
    n=32;denominator=2**n+1
    fractions=[Q(2**j,denominator) for j in range(n-1)]
    assert all(v.denominator==denominator for v in fractions)
    result={'status':'PASS','signed_exact_norm_cases':signed,'affine_checks':affine,
            'path_bridge_checks':bridge,
            'inverse_basis_output_bit_example':{'N':n,'offdiagonal_fraction_count':n-1,
                'bits_per_reduced_denominator':denominator.bit_length(),
                'denominator_bits_when_materialized_separately':sum(v.denominator.bit_length() for v in fractions)},
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (ROOT/'fft_green_fusion_research/resolvent_escape.py',
                          ROOT/'fft_green_conditioned_bridge_research/green_bridge.py',Path(__file__))}}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
