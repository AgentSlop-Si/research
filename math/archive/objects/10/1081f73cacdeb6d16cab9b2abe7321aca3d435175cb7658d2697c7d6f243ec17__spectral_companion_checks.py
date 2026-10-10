#!/usr/bin/env python3
"""Independent spectral sanity checks. No uploaded source is imported."""
import json
import math
from pathlib import Path
import numpy as np

rng = np.random.default_rng(2026100902)
results = {"spectral_instances": [], "normalized_green_instances": [], "isolation_instances": [], "boundary_controls": []}


def weighted_cycle(n):
    w = np.exp(1j*rng.uniform(-math.pi,math.pi,n))
    w[-1] = -1/np.prod(w[:-1])
    m = np.zeros((n,n),complex)
    for j in range(n):
        m[(j+1)%n,j] = w[j]
    assert np.allclose(m.conj().T @ m,np.eye(n),atol=1e-11)
    assert np.allclose(np.linalg.matrix_power(m,n),-np.eye(n),atol=1e-10)
    return m


def k_stage(n):
    m = weighted_cycle(n)
    return np.eye(n)+np.linalg.inv(np.eye(n)-m)


def formula(n):
    a = math.sqrt(2+1/(4*math.sin(math.pi/(2*n))**2))
    b = math.sqrt(2+1/(4*math.cos(math.pi/(2*n))**2))
    logd = (n-1)*math.log(2)+math.log1p(2.0**(-n))
    g = math.exp(logd/n)
    return a,b,g,logd


def normalize(a):
    _, logd = np.linalg.slogdet(a)
    return a / math.exp(logd/a.shape[0])


def opnorm(a):
    return float(np.linalg.svd(a,compute_uv=False)[0])


def unitary(n):
    q,_ = np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
    return q


def green(n):
    t=3*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1)
    p=np.eye(n)[rng.permutation(n)]
    b=p @ t @ p.T
    return np.linalg.inv(b)+np.linalg.inv(t)/20


def left_product(factors,n):
    p=np.eye(n,dtype=complex)
    for factor in factors:
        p=factor @ p
    return p


for n in (2,4,6,8,16,32,64,128):
    a,b,g,logd=formula(n)
    assert g<2 and b>=1.5 and g/b<4/3
    assert a>=n/math.pi and b<=math.sqrt(2.5)+1e-14
    ratio=None if n==2 else math.log(a/b)/math.log(g/b)
    for trial in range(2):
        k=k_stage(n)
        singular=np.linalg.svd(k,compute_uv=False)
        theta=(2*np.arange(n)+1)*math.pi/n
        expected=np.sort(np.abs((2-np.exp(1j*theta))/(1-np.exp(1j*theta))))[::-1]
        assert np.allclose(singular,expected,atol=1e-9,rtol=1e-10)
        assert abs(singular[0]-a)<1e-9 and abs(singular[-1]-b)<1e-9
        phase,measuredlogd=np.linalg.slogdet(k)
        assert abs(phase-1)<1e-9 and abs(measuredlogd-logd)<1e-9
        khat=normalize(k)
        assert abs(opnorm(khat)-a/g)<1e-9
        assert abs(opnorm(np.linalg.inv(khat))-g/b)<1e-9
        results["spectral_instances"].append({"n":n,"trial":trial,"a":a,"b":b,"g":g,
            "forward_stage_lower_bound":ratio,
            "integer_lower_bound":None if ratio is None else math.ceil(ratio-1e-10)})

for n in (2,4,8,16,32):
    for use_inverse in (False,True):
        a=green(n)
        if use_inverse:
            a=np.linalg.inv(a)
        singular=np.linalg.svd(a,compute_uv=False)
        condition=float(singular[0]/singular[-1])
        ahat=normalize(a)
        inverse_norm=opnorm(np.linalg.inv(ahat))
        assert inverse_norm<=condition+1e-10 and condition<5
        results["normalized_green_instances"].append({"n":n,"inverse":use_inverse,
            "kappa2":condition,"normalized_inverse_norm":inverse_norm})

for n in (2,4,8,16):
    a,b,g,_=formula(n)
    for s in (0,1,2):
        for t in (1,2,3):
            factors=[unitary(n)]
            distinguished=None
            for j in range(t):
                factors.append(normalize(k_stage(n)))
                if distinguished is None:
                    distinguished=len(factors)-1
                factors.append(unitary(n))
            for j in range(s):
                m=green(n)
                if j%2:
                    m=np.linalg.inv(m)
                factors.append(normalize(m))
                factors.append(unitary(n))
            w=left_product(factors,n)
            left=left_product(factors[distinguished+1:],n)
            right=left_product(factors[:distinguished],n)
            isolated=np.linalg.inv(left) @ w @ np.linalg.inv(right)
            assert np.allclose(isolated,factors[distinguished],atol=1e-9,rtol=1e-9)
            upper=5**s*(g/b)**(t-1)*opnorm(w)
            assert a/g<=upper+1e-8
            results["isolation_instances"].append({"n":n,"green_count":s,"k_count":t,
                "distinguished_normalized_k_norm":a/g,"general_product_upper_bound":upper})

# Boundary realizations in the enlarged arbitrary-unitary model. Pair singular
# eigenspaces in reverse order; phases are harmless for scalar-unitarity.
for n in (2,4):
    theta=(2*np.arange(n)+1)*math.pi/n
    eigen=(2-np.exp(1j*theta))/(1-np.exp(1j*theta))
    k=np.diag(eigen)
    order=np.argsort(np.abs(eigen))
    permutation=np.zeros((n,n))
    for j in range(n):
        permutation[order[j],order[n-1-j]]=1
    w=k @ permutation @ k
    _,_,g,_=formula(n)
    residual=opnorm(w.conj().T @ w-g**4*np.eye(n))
    assert residual<1e-10
    results["boundary_controls"].append({"n":n,"two_stage_scalar_unitary_residual":residual})

results["summary"]={"status":"PASS","spectral_instances":len(results["spectral_instances"]),
    "normalized_green_instances":len(results["normalized_green_instances"]),
    "isolation_instances":len(results["isolation_instances"]),
    "boundary_controls":len(results["boundary_controls"]),"uploaded_code_imported_or_executed":False}
Path(__file__).with_name("spectral_results.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results["summary"],indent=2))
