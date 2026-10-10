"""Numerical sanity checks for analytic error bounds, not certified FP outputs.

NumPy dense solves/DFTs are independent references and test-input generation.
The conditional residual-error experiment is not a word-RAM decoder claim.
"""
import cmath
import heapq
import json
import math
from pathlib import Path
import numpy as np


def cycle_solve(permutation,coefficients,rhs):
    n=len(rhs);order=[];j=0
    for _ in range(n):order.append(j);j=permutation[j]
    assert j==0 and len(set(order))==n
    product=1+0j
    for j in order:product*=coefficients[j]
    value=0j
    for j in reversed(order):value=rhs[j]+coefficients[j]*value
    value/=1-product
    out=np.zeros(n,dtype=complex)
    for j in reversed(order):
        value=rhs[j]+coefficients[j]*value;out[j]=value
    return out


def mass_box(x):return float(np.abs(x.real).sum()+np.abs(x.imag).sum())


def main():
    rng=np.random.default_rng(7403)
    results={'status':'PASS','scope':'Analytic exact bounds plus nonrigorous floating-point sanity checks',
             'structured_residual_cases':[],'rational_no_gain_cases':[],'green_norm_cases':[]}
    for n in (16,32,64,128):
        roots=np.exp(2j*np.pi*np.arange(n)/n)
        a,b,shift=5,1,1;inverse_a=pow(a,-1,n)
        source=np.array([(a*j+shift)%n for j in range(n)])
        target=np.array([inverse_a*(k+b)%n for k in range(n)])
        parameter=(1-1/n)*cmath.exp(1j*math.pi/(2*n))
        source_coeff=parameter*roots
        target_coeff=parameter*roots[(-shift*target)%n]
        u=(rng.normal(size=n)+1j*rng.normal(size=n))/(n*n);u[0]=1
        matrix=np.eye(n,dtype=complex)
        matrix[np.arange(n),source]-=source_coeff
        # Independent dense linear solve is used only to generate a test input.
        x=np.linalg.solve(matrix,u)
        actual_u=x-source_coeff*x[source]
        keep=heapq.nlargest(1,range(n),key=lambda j:abs(actual_u[j]))
        head=np.zeros(n,dtype=complex)
        for j in keep:head[j]=actual_u[j]
        tail=actual_u-head
        head_transform=np.zeros(n,dtype=complex)
        for j in keep:head_transform+=head[j]*roots[(j*np.arange(n))%n]/math.sqrt(n)
        y=cycle_solve(target,target_coeff,head_transform)
        reference=np.fft.ifft(x)*math.sqrt(n)
        radius=abs(parameter)
        inverse_norm=sum(radius**t for t in range(n))/abs(1+parameter**n)
        bound=inverse_norm*float(np.abs(tail).sum())/math.sqrt(n)
        error=float(np.abs(y-reference).max())
        assert error<=bound+1e-10
        # Deliberately inject arbitrary bounded decoder error to test transport.
        epsilon=.125
        tail_reference=np.fft.ifft(tail)*math.sqrt(n)
        perturbation=epsilon*mass_box(tail)/math.sqrt(n)*np.exp(2j*np.pi*rng.random(n))
        z=cycle_solve(target,target_coeff,head_transform+tail_reference+perturbation)
        propagated_error=float(np.abs(z-reference).max())
        propagated_bound=inverse_norm*epsilon*mass_box(tail)/math.sqrt(n)
        assert propagated_error<=propagated_bound+1e-10
        raw=inverse_norm*float(np.abs(actual_u).sum())
        original=float(np.abs(x).sum())
        assert raw+1e-9>=original
        for scale in (.25,2.0,16.0):
            assert abs((inverse_norm/scale)*float(np.abs(scale*actual_u).sum())-raw)<=1e-9
        results['structured_residual_cases'].append({'N':n,'input_nonzero_entries':int(np.count_nonzero(x)),
            'inverse_norm':inverse_norm,'raw_mass_bound_over_original_mass':raw/original,
            'tail_mass':float(np.abs(tail).sum()),'deterministic_head_error':error,
            'deterministic_head_bound':bound,'head_bound_over_direct_L1_bound':bound/(original/math.sqrt(n)),
            'injected_decoder_error':propagated_error,'conditional_decoder_bound':propagated_bound})
    for n in (4,8,16,32):
        roots=np.exp(2j*np.pi*np.arange(n)/n);indices=np.arange(n)
        unitary=roots[(indices[:,None]*indices[None,:])%n]/math.sqrt(n)
        m=np.zeros((n,n),dtype=complex)
        m[indices,(5*indices+1)%n]=roots
        inverse_a=pow(5,-1,n);target=(inverse_a*(indices+1))%n
        mhat=np.zeros((n,n),dtype=complex);mhat[indices,target]=roots[-target%n]
        assert np.max(np.abs(unitary@m-mhat@unitary))<1e-12
        for name,left,right in [
            ('affine_linear',np.eye(n)-.7*m,np.eye(n)-.7*mhat),
            ('dense_resolvent',np.eye(n)+np.linalg.inv(np.eye(n)-m),
                                np.eye(n)+np.linalg.inv(np.eye(n)-mhat))]:
            source_norm=float(np.linalg.norm(np.linalg.inv(left),1))
            target_norm=float(np.linalg.norm(np.linalg.inv(right),np.inf))
            assert abs(source_norm-target_norm)<1e-10
            x=rng.normal(size=n)+1j*rng.normal(size=n)
            ratio=target_norm*np.abs(left@x).sum()/np.abs(x).sum()
            assert ratio>=1-1e-10
            results['rational_no_gain_cases'].append({'N':n,'filter':name,
                'source_inverse_1_norm':source_norm,'target_inverse_infinity_norm':target_norm,
                'raw_mass_factor':float(ratio)})
        t=3*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1)
        h=unitary@t@unitary.conj().T
        s=np.linalg.inv(t)+np.linalg.inv(t+np.eye(n))
        target_s=unitary@s@unitary.conj().T
        h_inverse_norm=float(np.linalg.norm(np.linalg.inv(h),np.inf))
        s_inverse_norm=float(np.linalg.norm(np.linalg.inv(target_s),np.inf))
        assert h_inverse_norm<=5+1e-12
        assert s_inverse_norm<=73/18+1e-12
        results['green_norm_cases'].append({'N':n,'H_inverse_infinity_norm':h_inverse_norm,
                                           'S_conjugate_inverse_infinity_norm':s_inverse_norm})
    Path('approximation_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
