#!/usr/bin/env python3
"""Independent construction checks for the composite bounds and dyadic proof."""
from fractions import Fraction
import math,json
import numpy as np
from independent_composite_probe import phi,full_exact,block_norm

def layer_masks(m):
    p=1<<(m-1).bit_length()
    d=np.arange(1,m)[:,None];u=np.arange(m)[None,:]
    layers=[d==u]
    width=2
    while width<=p:
        layers.append((d//width==u//width)&(d%width<width//2)&(u%width>=width//2))
        width*=2
    return layers

def exact_count_bound(n,m):
    shell={g:[0]*m for g in range(1,m) if n%g==0}
    for u in range(m):
        for d in range(u-m+1,u+1):
            if d:shell[math.gcd(n,d)][u]+=1
    c=sum((Fraction(max(v),phi(n//g)) for g,v in shell.items()),Fraction(0))
    for g,v in shell.items():
        assert max(v)<=(m-1)//g
        assert Fraction(phi(n),phi(n//g))<=g
    coarse=Fraction((m-1)*len(shell),phi(n))
    assert c<=coarse
    return c,coarse,len(shell)

def test_explicit_analysis(n,m):
    ns=np.arange(n);unitary=np.exp(-2j*np.pi*np.outer(ns,ns)/n)/np.sqrt(n)
    rows=[];ds=[]
    for d in range(1,m):
        g=math.gcd(n,d)
        factor=math.sqrt(phi(n)/phi(n//g))
        for k in range(n):
            if math.gcd(k,n)==g:rows.append(factor*unitary[k]);ds.append(d)
    t=np.array(rows);ds=np.array(ds);u=ns%m
    tp=t*(ds[:,None]<=u[None,:]);tn=t*(ds[:,None]<=m-1-u[None,:])
    q=np.array(full_exact(n,m),float)
    residual=np.max(np.abs((tp.conj().T@tp+tn.conj().T@tn)/phi(n)-q))
    assert residual<5e-13,(n,m,residual)
    opnorm=np.linalg.norm(t,2)
    assert opnorm**2<=m-1+1e-11
    layers=layer_masks(m);parts=[]
    for layer in layers:
        a=t*layer[ds-1][:,u]
        assert np.linalg.norm(a,2)<=opnorm+1e-11
        parts.append(a)
    assert np.max(np.abs(sum(parts)-tp))<1e-13
    assert np.linalg.norm(tp,2)<=len(layers)*opnorm+1e-11
    c,coarse,shells=exact_count_bound(n,m)
    norm=block_norm(n,m)
    dyadic=Fraction(2*(m-1)*len(layers)**2,phi(n))
    assert norm<=float(c)+1e-11
    assert norm<=float(dyadic)+1e-11
    return dict(N=n,M=m,gram_residual=float(residual),exact_C=str(c),divisor_bound=str(coarse),dyadic_bound=str(dyadic),covariance_norm=norm,unmasked_norm_squared=float(opnorm**2),number_of_layers=len(layers),shells=shells)

def main():
    for m in range(2,513):
        masks=layer_masks(m)
        s=sum(a.astype(int) for a in masks)
        expected=np.arange(1,m)[:,None]<=np.arange(m)[None,:]
        assert np.array_equal(s,expected)
    count=0
    for n in range(4,1001):
        for m in range(2,math.isqrt(n)+1):
            if n%m==0:exact_count_bound(n,m);count+=1
    records=[test_explicit_analysis(n,m) for n,m in [(12,2),(12,3),(18,3),(30,5),(36,6),(60,5),(60,6),(64,8),(72,8),(100,10),(120,10)]]
    result=dict(dyadic_partition_checks=511,exact_count_checks=count,explicit_analysis_checks=records,status='passed')
    with open('bound_certificate_results.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
