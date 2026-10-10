#!/usr/bin/env python3
"""Independent exact controls; no inherited research program is imported or executed."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

def primes_of(n):
    ans=[]
    p=2
    while p*p<=n:
        if n%p==0:
            ans.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:ans.append(n)
    return ans

def is_prime(n):
    if n<2:return False
    p=2
    while p*p<=n:
        if n%p==0:return False
        p+=1
    return True

def field_for(N):
    k=1
    while not is_prime(k*N+1):k+=1
    p=k*N+1
    for a in range(2,p):
        q=pow(a,k,p)
        if pow(q,N,p)==1 and all(pow(q,N//r,p)!=1 for r in primes_of(N)):
            return p,q
    raise AssertionError('root missing')

def val(P,z,p):
    out=0
    for a in reversed(P):out=(out*z+a)%p
    return out

def mul(P,Q,p):
    out=[0]*(len(P)+len(Q)-1)
    for i,a in enumerate(P):
        for j,b in enumerate(Q):out[i+j]=(out[i+j]+a*b)%p
    return out

def transform_one(P,lam,q,h,rho,p):
    out=[0]*(len(P)+1)
    for i,a in enumerate(P):
        out[i]=(out[i]-lam*a)%p
        out[i+1]=(out[i+1]+pow(q,h,p)*pow(rho,i,p)*a)%p
    return out

def transform_two(P,lam,q,mult,p):
    # E multiplier q; O multiplier q^2.
    out=[0]*(len(P)+1)
    for i,a in enumerate(P):
        out[i]=(out[i]-lam*a)%p
        out[i+1]=(out[i+1]+mult*pow(q,2*i,p)*a)%p
    return out

def annihilate(vals,lambdas,step,p):
    for lam in lambdas:
        vals=[(vals[k+step]-lam*vals[k])%p for k in range(len(vals)-step)]
    return vals

def vandermonde_product(nodes,p):
    out=1
    for i,x in enumerate(nodes):
        for y in nodes[i+1:]:out=out*(y-x)%p
    return out

boundaries={}
for name,start,den,offset in [('step_one',27,10,13),('step_two',45,16,19)]:
    count=0
    for N in range(start,100002,2):
        d=(N+offset)//den;m=N-d;b=d-1
        u=d-3+(d-1)//2;v=d-3+(d-2)//2
        assert d>=4 and N>=den*d-offset
        assert m>=(N-1)//2
        assert N-5*d+12>=(N+1)//2
        assert m+1>=3*b
        assert 2*u<=3*d-7 and 2*v+1<=3*d-7
        assert max(2*u,2*v+1)==3*d-7
        assert u+v+2==3*d-6
        if name=='step_one':
            deg=6*d-10;zeros=N-4*d+4
            assert zeros>=deg+1 and deg<N
            assert N-2*d>=4*d-7 # shortest of three special coordinate intervals
            assert m-1>=b
        else:
            assert u+3*b<(N+1)//2
            assert (N+1)//2+v+3*b<N
            assert N-7*d+7>=9*d-12
            assert (m+1)//2>=7*d-10
            assert N-3*d+1>=5*d-8
        count+=1
    d=(start+offset)//den
    boundaries[name]={'orders_checked':count,'first_N':start,'last_N':100001,'first_d':d,
        'first_m':start-d,'first_bank_bound':2*(start-d)+2}

finite=[]
for N in [27,29,35,37,45,47,59,99,101,135,165,201]:
    p,q=field_for(N);h=pow(4,-1,N);e=pow(2,-1,N);rho=pow(q,e,p)
    d=(N+13)//10;m=N-d;b=d-1
    D=[1]
    for j in range(2,d):D=mul(D,[1,-pow(q,j,p)%p],p)
    assert len(D)==d-1
    assert all(val(D,pow(q,k,p),p)!=0 for k in range(m+1))
    P=[(i*i+3*i+7)%p for i in range(3*d-6)]
    P[-1]=1
    R=[(2*j+5)%p for j in range(b)]
    ordinary=[pow(q,j,p) for j in range(b)]
    scalar_checks=0
    for x in [1,2,q,pow(q,-1,p)]:
        lambdas=[pow(x*qj,1,p) for qj in ordinary for _ in range(2)]
        total=lambdas+ordinary
        samples=[(k*pow(x,k-1,p)*val(D,pow(q,k,p),p))%p for k in range(m+1)]
        assert not any(annihilate(samples,lambdas,1,p))
        chirp=[pow(q,(h*k*k)%N,p)*val(P,pow(rho,k,p),p)%p for k in range(m+1)]
        whole=[(chirp[k]+val(R,pow(q,k,p),p))%p for k in range(m+1)]
        out=annihilate(whole,total,1,p)
        PP=P[:]
        for lam in total:PP=transform_one(PP,lam,q,h,rho,p)
        expected=[pow(q,(h*k*k)%N,p)*val(PP,pow(rho,k,p),p)%p for k in range(len(out))]
        assert out==expected
        assert len(PP)-1==6*d-10 and PP[-1]!=0
        assert len(out)==N-4*d+4
        scalar_checks+=len(out)
    nodes=[pow(rho,k,p) for k in range(6*d-9)]
    det=vandermonde_product(nodes,p)
    assert det!=0
    # Check exact merger, all chirp shift identities and every special-coordinate shrink.
    u=d-3+(d-1)//2;v=d-3+(d-2)//2
    E=[(i+2)%p for i in range(u+1)];O=[(3*i+1)%p for i in range(v+1)]
    merged=[0]*(3*d-6)
    for i,a in enumerate(E):merged[2*i]=a
    for i,a in enumerate(O):merged[2*i+1]=a
    for k in range(N):
        t=pow(rho,k,p);z=pow(q,k,p)
        assert val(merged,t,p)==(val(E,z,p)+t*val(O,z,p))%p
        c=pow(q,h*k*k,p)
        assert pow(q,h*(k+1)*(k+1),p)==pow(q,h,p)*t*c%p
        assert pow(q,h*(k+2)*(k+2),p)==pow(q,k+1,p)*c%p
    for j,start,end in [(0,1,m),(m,0,m-1),(1,2,m)]:
        samples=[int(k==j) for k in range(m+1)]
        out=annihilate(samples,ordinary,1,p)
        assert all(out[k]==0 for k in range(start,end-b+1))
        assert end-b-start+1>=4*d-7
    finite.append({'N':N,'d':d,'p':p,'q':q,'rho':rho,'vandermonde_determinant_mod_p':det,
                   'exact_chirp_values_checked':scalar_checks,'derivative_values_x':[1,2,q,pow(q,-1,p)]})

# Additional step-two controls at its own sharp thresholds.
step_two=[]
for d in range(4,16):
    N=16*d-19;m=N-d;b=d-1;p,q=field_for(N);h=pow(4,-1,N);e=pow(2,-1,N)
    u=d-3+(d-1)//2;v=d-3+(d-2)//2
    E=list(range(1,u+2));O=list(range(2,v+3));E[-1]=O[-1]=1
    x=2
    ordinary=[pow(q,2*j,p) for j in range(b)]
    lambdas=[x*x*qj%p for qj in ordinary for _ in range(2)]+ordinary
    EE=E[:];OO=O[:]
    for lam in lambdas:
        EE=transform_two(EE,lam,q,q,p)
        OO=transform_two(OO,lam,q,q*q%p,p)
    samples=[pow(q,h*k*k,p)*(val(E,pow(q,k,p),p)+pow(q,e*k,p)*val(O,pow(q,k,p),p))%p for k in range(m+1)]
    out=annihilate(samples,lambdas,2,p)
    expected=[pow(q,h*k*k,p)*(val(EE,pow(q,k,p),p)+pow(q,e*k,p)*val(OO,pow(q,k,p),p))%p for k in range(len(out))]
    assert out==expected
    assert len(out)==N-7*d+7==9*d-12
    freqs=list(range(u+3*b+1))+list(range(e,e+v+3*b+1))
    assert len(freqs)==len(set(f%N for f in freqs))==9*d-12
    det=vandermonde_product([pow(q,f,p) for f in freqs],p)
    assert det!=0
    step_two.append({'N':N,'d':d,'p':p,'q':q,'frequencies':len(freqs),'zeros':len(out),'vandermonde_determinant_mod_p':det})

result={'status':'PASS','method':'Fresh standard-library exact integer and finite-field controls; no inherited program imported or executed. General proofs, not these finite controls, establish the all-order theorems.',
        'integer_ranges':boundaries,'step_one_exact_controls':finite,'step_two_exact_controls':step_two,
        'guard_scope':'Step one excludes only delta_0, delta_m, delta_1; it does not assert the stronger all-coordinate exclusion at its sharp range.'}
(OUT/'FRESH_LINEAR_SAVING_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','integer_ranges':boundaries,'finite_step_one_cases':len(finite),'finite_step_two_cases':len(step_two)},indent=2))
