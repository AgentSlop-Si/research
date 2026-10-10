"""Independent exact identities, original-material checks, and charged probes."""
from pathlib import Path
from fractions import Fraction as Q
from random import Random
from collections import Counter
import hashlib
import json
import sys

from exact_fields import PrimeField, CyclotomicField, inverse, mm, mv, rank, fourier
from resolvent_escape import prepare_affine, signed_cycle_forward, varying_rank_one_gauge_recognize

ORIGINAL = Path(__file__).resolve().parent.parent/'fft_new_fusion_materials_20261009'/'green'/'fft_global_green_gauge'
sys.path.insert(0,str(ORIGINAL))
from gauge_fft import GaugeFFT
from gauge_recognizer import gauge_recognize
from norm_budget import exact_green_condition1


class Rational:
    zero,one = Q(0),Q(1)
    def add(self,a,b):return a+b
    def sub(self,a,b):return a-b
    def mul(self,a,b):return a*b
    def neg(self,a):return -a
    def inv(self,a):return 1/a
    def integer(self,a):return Q(a)


class Probe:
    def __init__(self,field):
        self.field=field;self.zero=field.zero;self.one=field.one;self.count=Counter()
    def add(self,a,b):self.count['add']+=1;return self.field.add(a,b)
    def sub(self,a,b):self.count['sub']+=1;return self.field.sub(a,b)
    def mul(self,a,b):self.count['mul']+=1;return self.field.mul(a,b)
    def inv(self,a):self.count['inverse']+=1;return self.field.inv(a)


def identity(field,n):
    return [[field.one if i==j else field.zero for j in range(n)] for i in range(n)]


def plus(field,a,b):
    return [[field.add(x,y) for x,y in zip(r,s)] for r,s in zip(a,b)]


def minus(field,a,b):
    return [[field.sub(x,y) for x,y in zip(r,s)] for r,s in zip(a,b)]


def norm1(a):
    return max(sum(abs(x) for x in col) for col in zip(*a))


def monomial(field,permutation,coefficients):
    n=len(permutation)
    return [[coefficients[i] if permutation[i]==j else field.zero for j in range(n)] for i in range(n)]


def check_escape():
    rng=Random(991)
    out={'basis_cases':0,'fresh_roundtrips':0,'intertwining_matrices':0,
         'counted_preparations':0,'counted_applications':0,'rational_norms':[],
         'signed_forward_cases':0,'singular_modular_rejections':0,'invalid_rejections':0}
    for field,sizes in ((PrimeField(97),(2,4,8,16)),(PrimeField(193),(2,4,8,16,32)),
                        (CyclotomicField(4),(4,)),(CyclotomicField(8),(8,))):
        for n in sizes:
            q=field.root(n)
            for a,b,shift in ((1,1,1),(5,3,5),(-3,-1,-3)):
                probe=Probe(field)
                plan=prepare_affine(probe,n,q,a,b,shift)
                assert plan.preparation_counts==dict(probe.count)
                assert sum(probe.count.values())==2*n+(n.bit_length()-1)+4
                out['counted_preparations']+=1
                eye=identity(field,n)
                m=monomial(field,plan.source,plan.source_coefficients)
                kh=plus(field,eye,inverse(field,minus(field,eye,monomial(field,plan.target,plan.target_coefficients))))
                k=plus(field,eye,inverse(field,minus(field,eye,m)))
                ki=inverse(field,k)
                f=fourier(field,n)
                assert mm(field,f,k)==mm(field,kh,f)
                out['intertwining_matrices']+=1
                for j in range(n):
                    x=[field.one if i==j else field.zero for i in range(n)]
                    for reverse,expected in ((False,k),(True,ki)):
                        probe=Probe(field)
                        y,counts=plan.apply(probe,x,inverse=reverse)
                        assert counts==dict(probe.count)
                        assert sum(counts.values())==(6*n+1 if reverse else 5*n+1)
                        assert y==mv(field,expected,x)
                        out['basis_cases']+=1;out['counted_applications']+=1
                for _ in range(3):
                    x=[field.integer(rng.randrange(-20,21)) for _ in range(n)]
                    y,_=plan.apply(field,x)
                    z,_=plan.apply(field,y,inverse=True)
                    assert z==x
                    out['fresh_roundtrips']+=1

    field=Rational()
    for n in (1,2,3,4,8,16,32):
        eye=identity(field,n)
        perm=list(range(1,n))+[0]
        c=monomial(field,perm,[Q(1)]*(n-1)+[Q(-1)])
        k=plus(field,eye,inverse(field,minus(field,eye,c)))
        ki=inverse(field,k)
        assert all(x!=0 for row in k+ki for x in row)
        nk,ni=norm1(k),norm1(ki)
        assert nk==Q(n+2,2)
        assert ni==Q(2**n,2**n+1)
        assert nk*ni==Q((n+2)*2**(n-1),2**n+1)
        for j in range(n):
            x=[Q(int(i==j)) for i in range(n)]
            probe=Probe(field)
            y,counts,setup=signed_cycle_forward(probe,x)
            assert y==mv(field,k,x)
            assert counts==dict(probe.count)
            assert sum(counts.values())==3*n+1 and sum(setup.values())==2
            out['signed_forward_cases']+=1
        out['rational_norms'].append(dict(N=n,norm1_K=str(nk),norm1_inverse=str(ni),
                                         kappa1=str(nk*ni),inverse_nonzeros=n*n,
                                         signed_cold_field_gates=3*n+1,
                                         inverse_denominator_bits=(2**n+1).bit_length()))
    for p,n in ((5,2),(17,4),(257,8),(65537,16)):
        field=PrimeField(p)
        try:prepare_affine(field,n,field.root(n))
        except ValueError as e:
            assert 'singular numerator' in str(e)
            out['singular_modular_rejections']+=1
        else:raise AssertionError('singular K accepted')
    field=PrimeField(97)
    for args in ((1,1,5,1,1),(3,1,5,1,1),(4,1,5,1,1),
                 (4,field.root(4),2,1,1),(4,field.root(4),5,2,1),
                 (4,field.root(4),5,1,2)):
        try:prepare_affine(field,*args)
        except ValueError:out['invalid_rejections']+=1
        else:raise AssertionError('invalid request accepted')
    try:signed_cycle_forward(Rational(),[])
    except ValueError:out['invalid_rejections']+=1
    else:raise AssertionError('empty signed input accepted')
    return out


def check_green_bounds():
    field=Rational();out=[]
    for n in (2,4,8,16):
        t=[[Q(3) if i==j else Q(-1) if abs(i-j)==1 else Q(0) for j in range(n)] for i in range(n)]
        eye=identity(field,n);u=plus(field,t,eye)
        s=plus(field,inverse(field,t),inverse(field,u))
        si=inverse(field,s)
        claimed=mm(field,mm(field,u,inverse(field,plus(field,t,u))),t)
        assert claimed==si
        n1,ninv=norm1(s),norm1(si)
        assert (n1,ninv,n1*ninv)==exact_green_condition1(n)
        assert n1<Q(3,2) and ninv<Q(17,6) and n1*ninv<Q(17,4)
        # Slightly sharpened all-N bound from the sign pattern and Gjj>=1/7.
        assert ninv<Q(58,21) and n1*ninv<Q(29,7)
        out.append(dict(N=n,norm1=str(n1),norm1_inverse=str(ninv),kappa1=str(n1*ninv)))
    return out


def literal_gauge_action(gauge,x,inverse=False):
    p=gauge.p;dot=0;count=Counter()
    for a,y in zip(gauge.v,x):
        dot=(dot+a*y)%p;count['mul']+=1;count['add']+=1
    scale=(gauge.neg_beta if inverse else gauge.alpha)*dot%p;count['mul']+=1
    out=[]
    for y,a in zip(x,gauge.u):
        out.append((y+scale*a)%p);count['mul']+=1;count['add']+=1
    return out,count


def check_gauges():
    out={'original_gauge_cases':[],'varying_gauge_cases':[],'corruptions_rejected':0}
    field=PrimeField(998244353);rng=Random(45)
    for n in (4,8,16,32):
        plan=GaugeFFT(n)
        b=[plan.physical_matrix(i,dressed=False) for i in range(len(plan.stages))]
        g=[plan.physical_matrix(i,dressed=True) for i in range(len(plan.stages))]
        assert gauge_recognize(b,g,plan.p)['match']
        assert varying_rank_one_gauge_recognize(field,b,g,mm,inverse,rank)['match']
        for j in range(n):
            x=[int(i==j) for i in range(n)]
            y,stats=plan.apply(x)
            assert y==mv(field,fourier(field,n),x)
        x=[rng.randrange(plan.p) for _ in range(n)]
        literal_calls=[]
        for reverse in (False,True):
            stats=dict(add=0,mul=0,reads=0,writes=0,gauge_calls=0)
            y=plan.gauge.action(x,inverse=reverse,stats=stats)
            independent,actual=literal_gauge_action(plan.gauge,x,inverse=reverse)
            assert independent==y and actual['add']==stats['add']+1
            assert actual['mul']==stats['mul']==2*n+1
            literal_calls.append(dict(reported_add=stats['add'],literal_add=actual['add']))
        L=len(plan.stages)
        out['original_gauge_cases'].append(dict(N=n,gauge_calls=2*(L-1),
                undercounted_additions=2*(L-1),literal_call_counts=literal_calls,
                all_stages_dense=all(all(v!=0 for row in a for v in row) for a in g)))
        if L<3:continue
        eye=identity(field,n);previous=eye;varying=[]
        for i,base in enumerate(b):
            if i==L-1:h=eye
            else:
                u=[(j+1)*(i+1)%field.p for j in range(n)]
                v=[(3*j+1+i)%field.p for j in range(n)]
                h=plus(field,eye,[[u[j]*v[k]%field.p for k in range(n)] for j in range(n)])
            varying.append(mm(field,mm(field,h,base),inverse(field,previous)))
            previous=h
        result=varying_rank_one_gauge_recognize(field,b,varying,mm,inverse,rank)
        assert result['match']
        assert not gauge_recognize(b,varying,plan.p)['match']
        bad=[[row[:] for row in a] for a in varying];bad[-1][0][0]=(bad[-1][0][0]+1)%plan.p
        assert not varying_rank_one_gauge_recognize(field,b,bad,mm,inverse,rank)['match']
        out['corruptions_rejected']+=1
        singular=[[row[:] for row in a] for a in varying];singular[0]=[[0]*n for _ in range(n)]
        assert not varying_rank_one_gauge_recognize(field,b,singular,mm,inverse,rank)['match']
        out['corruptions_rejected']+=1
        out['varying_gauge_cases'].append(dict(N=n,ranks=result['ranks'],constant_gauge_detector_accepts=False))
    return out


def main():
    folder=Path(__file__).parent
    result=dict(status='PASS',escape=check_escape(),green_bounds=check_green_bounds(),gauges=check_gauges())
    result['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob('*.py'))}
    result['dependency_path']='../fft_new_fusion_materials_20261009/green/fft_global_green_gauge'
    result['dependency_sha256']={name:hashlib.sha256((ORIGINAL/name).read_bytes()).hexdigest()
                                 for name in ('gauge_fft.py','gauge_recognizer.py','green_stages.py','norm_budget.py')}
    (folder/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
