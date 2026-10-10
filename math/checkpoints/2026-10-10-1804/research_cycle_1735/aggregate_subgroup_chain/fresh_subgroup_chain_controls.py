#!/usr/bin/env python3
"""Fresh standalone exact controls; imports no source/author research program."""
from fractions import Fraction
from functools import reduce
from math import gcd
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent


def factors(n):
    ans=[]; q=2
    while q*q<=n:
        while n%q==0: ans.append(q); n//=q
        q+=1
    if n>1: ans.append(n)
    return ans


def primitive_root(p):
    fs=set(factors(p-1))
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in fs))


def order_exponents(p):
    """Each d_j-sized consecutive block is a coset of H_j."""
    N=p-1; fs=factors(N); ds=[1]
    for q in fs: ds.append(ds[-1]*q)
    def rec(j):
        if not j: return [0]
        return [(e+a*(N//ds[j]))%N for a in range(fs[j-1]) for e in rec(j-1)]
    es=rec(len(fs)); g=primitive_root(p)
    return [pow(g,e,p)-1 for e in es],fs,ds,g


def root_zero(p, xs, t):
    """Exact cyclotomic test; the signed coefficient sum is zero."""
    counts=[0]*p
    for x in xs:
        counts[((t+1)*x)%p]+=1
        counts[((t-1)*x)%p]-=1
    return all(v==0 for v in counts)


def stabilizer(p,xs):
    T=set(xs)
    return [a for a in range(1,p) if {(a*x)%p for x in T}==T]


class K:
    p=None
    def __init__(self,v=0,d=1):
        p=K.p
        if isinstance(v,int): v=[v]+[0]*(p-1)
        v=list(v)
        if len(v)==p-1: v.append(0)
        assert len(v)==p and d
        v=[x-v[-1] for x in v]
        if d<0: v=[-x for x in v]; d=-d
        z=reduce(gcd,v,d)
        self.v=tuple(x//z for x in v); self.d=d//z
    def __add__(self,b):
        if isinstance(b,int): b=K(b)
        return K([a*b.d+c*self.d for a,c in zip(self.v,b.v)],self.d*b.d)
    __radd__=__add__
    def __neg__(self): return K([-a for a in self.v],self.d)
    def __sub__(self,b): return self+(-b if isinstance(b,K) else -K(b))
    def __mul__(self,b):
        if isinstance(b,int): b=K(b)
        v=[0]*K.p
        for i,a in enumerate(self.v):
            if a:
                for j,c in enumerate(b.v):
                    if c: v[(i+j)%K.p]+=a*c
        return K(v,self.d*b.d)
    __rmul__=__mul__
    def __eq__(self,b):
        if isinstance(b,int): b=K(b)
        return self.v==b.v and self.d==b.d
    def __bool__(self): return any(self.v)
    def conj(self):
        v=[0]*K.p
        for i,a in enumerate(self.v): v[-i%K.p]+=a
        return K(v,self.d)


def root(e):
    v=[0]*K.p; v[e%K.p]=1
    return K(v)


def beta_inv(x):
    p=K.p; v=[0]*p
    for k in range(1,p): v[(x+2*x*k)%p]+=k
    return K(v,p)


def full_control(p):
    K.p=p
    inds,fs,ds,g=order_exponents(p); N=p-1
    beta={n:root(n+1)-root(-n-1) for n in inds}
    inv={n:beta_inv(n+1) for n in inds}
    assert all(beta[n]*inv[n]==1 for n in inds)
    C=[[K(0) for _ in range(p)] for _ in range(p)]
    I=[[K(0) for _ in range(p)] for _ in range(p)]
    for n in range(p): C[n][n]=K(1); I[n][n]=K(1)
    for j in range(1,N): C[inds[j]][inds[j-1]]=-beta[inds[j-1]]*inv[inds[j]]
    F=[[root(i*t) for t in range(p)] for i in range(p)]
    R=[[K(0) for _ in range(p)] for _ in range(p)]
    for t in range(p):
        Q=K(0)
        for n in inds:
            Q=Q+beta[n]*F[n][t]
            R[n][t]=Q*inv[n]
        R[p-1][t]=F[p-1][t]
    Cinv=[[K(0) for _ in range(p)] for _ in range(p)]
    for j,n in enumerate(inds):
        for i in range(j+1): Cinv[n][inds[i]]=beta[inds[i]]*inv[n]
    Cinv[p-1][p-1]=K(1)
    cr=[[sum((C[i][j]*R[j][t] for j in range(p)),K(0)) for t in range(p)] for i in range(p)]
    assert cr==F
    assert [[sum((C[i][j]*Cinv[j][t] for j in range(p)),K(0)) for t in range(p)] for i in range(p)]==I
    assert [[sum((Cinv[i][j]*F[j][t] for j in range(p)),K(0)) for t in range(p)] for i in range(p)]==R
    Z=N*sum((Fraction(q-1,q) for q in fs),Fraction(0))
    assert Z.denominator==1; Z=int(Z)
    rc=[sum(bool(R[i][t]) for i in range(p)) for t in range(p)]
    assert sum(rc)==p*p-Z
    # Direct per-color entries after actual C multiplication. B_t has column t only.
    h=pow(2,-1,p); gauss=sum((root(-h*t*t) for t in range(p)),K(0))
    assert gauss*gauss.conj()==p
    slice_entries=0
    accumulated=[[K(0) for _ in range(p)] for _ in range(p)]
    for t in range(p):
        phase=root(-h*t*t)
        bt=[phase*R[j][t] for j in range(p)]
        left=[sum((C[i][j]*bt[j] for j in range(p)),K(0)) for i in range(p)]
        for i in range(p):
            for j in range(p):
                value=left[i]*F[t][j]
                assert value==phase*F[i][t]*F[t][j]
                accumulated[i][j]=accumulated[i][j]+value
                slice_entries+=1
    invgauss=K(gauss.conj().v,gauss.d*p)
    for i in range(p):
        for j in range(p):
            assert invgauss*root(-h*i*i)*accumulated[i][j]*root(-h*j*j)==F[i][j]
    c_count=sum(bool(x) for row in C for x in row)
    ci_count=sum(bool(x) for row in Cinv for x in row)
    assert c_count==2*p-2 and ci_count==N*(N+1)//2+1
    return {'p':p,'primitive_root':g,'prime_radices':fs,'order':inds,'zeros':Z,'nnz_C':c_count,'nnz_C_inverse':ci_count,'nnz_R':p*p-Z,'column_counts_R':rc,'nnz_A':p*p,'total_edges':p*p+c_count+sum(rc),'dense_saving':Z-(p-2),'full_slice_entries':slice_entries,'corrected_transfer_entries':p*p,'CR_equals_F':True,'explicit_inverse_verified':True,'Gauss_norm_squared':p}


def support_control(p):
    inds,fs,ds,g=order_exponents(p); N=p-1
    assert sorted(inds)==list(range(N))
    H={d:{pow(g,j*(N//d),p) for j in range(d)} for d in ds}
    for d in ds:
        for start in range(0,N,d):
            T={x+1 for x in inds[start:start+d]}; a=next(iter(T))
            assert T=={a*h%p for h in H[d]}
    T=[]; rows=[]; total=0
    for L,n in enumerate(inds,1):
        T.append(n+1)
        d=max(d for d in ds if L%d==0)
        zs=[t for t in range(p) if root_zero(p,T,t)]
        assert len(zs)==d-1
        expected=[]
        for t in range(p):
            if t not in (1,p-1) and (t+1)*pow(t-1,-1,p)%p in H[d]: expected.append(t)
        assert zs==expected
        total+=len(zs)
        rows.append({'prefix_length':L,'stabilizer_size':d,'zeros':zs})
    formula=N*sum((Fraction(q-1,q) for q in fs),Fraction(0))
    assert total==formula
    return {'p':p,'primitive_root':g,'prime_radices':fs,'subgroup_sizes':ds,'order':inds,'zeros':total,'total_edges':2*p*p+2*p-2-total,'dense_saving':total-(p-2),'prefixes':rows}


def main():
    full=[full_control(p) for p in (5,7,11,13,17)]
    supports=[support_control(p) for p in (5,7,11,13,17,19,23,29,31,37,41,73,97,193,257)]
    result={'arithmetic':'Exact integer prime-cyclotomic reduction and rational denominators; no numerical tolerance','source_programs_executed_or_imported':False,'full_field_controls':full,'independent_prefix_support_controls':supports,'full_slice_entries_checked':sum(x['full_slice_entries'] for x in full),'corrected_transfer_entries_checked':sum(x['corrected_transfer_entries'] for x in full),'status':'PASS'}
    (OUT/'EXACT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','full_cases':len(full),'support_cases':len(supports),'slice_entries':result['full_slice_entries_checked'],'largest_support_case':{k:v for k,v in supports[-1].items() if k!='prefixes' and k!='order'}},indent=2))

if __name__=='__main__': main()
