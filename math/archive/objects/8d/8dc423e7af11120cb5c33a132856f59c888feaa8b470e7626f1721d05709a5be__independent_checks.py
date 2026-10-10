#!/usr/bin/env python3
"""Independent checks for the one-extra-pole construction.

No supplied executable or source module is imported. Requires Python 3 and sympy.
Finite-field PASS lines are supplemental certificates at those sizes; the
uniform statement is proved independently in PROOF_OR_OBSTRUCTION.md.
"""
import json
from pathlib import Path
import sympy as s


def symbolic_checks():
    q,z=s.symbols('q z')
    A=[s.Integer(1)]
    for n in range(1,9):
        R=s.Poly(s.prod(z-q**k for k in range(n)),z)
        An=s.expand(sum(q**((n*(n-1)-j*(j-1))//2)*R.nth(j)*z**j for j in range(n+1)))
        A.append(An)
        for shift in range(n):
            value=sum(s.Poly(An,z).nth(j)*q**((shift+j)*(shift+j-1)//2) for j in range(n+1))
            assert s.expand(value)==0, ('orthogonality',n,shift)
        if n>=2:
            m=n-1
            aa=q**(m-1)*(q**(m+1)+q**m-1)
            bb=q**(3*m-3)*(q**m-1)
            assert s.expand(An-(z-aa)*A[n-1]+bb*A[n-2])==0, ('three_term',n)
    return {'symbolic_degrees': list(range(1,9)), 'orthogonality_and_three_term': 'PASS'}


def trim(a):
    while len(a)>1 and not a[-1]: a.pop()
    return a

def add(a,b,p):
    c=[0]*max(len(a),len(b))
    for j,x in enumerate(a): c[j]=(c[j]+x)%p
    for j,x in enumerate(b): c[j]=(c[j]+x)%p
    return trim(c)

def scale(a,t,p): return trim([(t*x)%p for x in a])

def mul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):c[j+k]=(c[j+k]+x*y)%p
    return trim(c)

def rem(a,b,p):
    a=a[:]
    inv=pow(b[-1],-1,p)
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b);v=a[-1]*inv%p
        for j,x in enumerate(b):a[j+k]=(a[j+k]-v*x)%p
        trim(a)
    return a

def gcd(a,b,p):
    while b!=[0]:a,b=b,rem(a,b,p)
    return scale(a,pow(a[-1],-1,p),p)

def deriv(a,p): return trim([(j*a[j])%p for j in range(1,len(a))] or [0])

def val(a,z,p):
    v=0
    for x in reversed(a):v=(v*z+x)%p
    return v

def A_direct(n,q,p):
    """Build from its defining product, not the three-term recurrence."""
    R=[1]
    for k in range(n):R=mul(R,[-pow(q,k,p)%p,1],p)
    return [(x*pow(q,(n*(n-1)-j*(j-1))//2,p))%p for j,x in enumerate(R)]

def field_for(N):
    k=(1_000_000+N-1)//N
    while not s.isprime(k*N+1):k+=1
    p=k*N+1
    g=int(s.primitive_root(p))
    q=pow(g,(p-1)//N,p)
    assert pow(q,N,p)==1
    assert all(pow(q,N//int(ell),p)!=1 for ell in s.factorint(N))
    return p,q

def check_size(N):
    h=N//2;p,q=field_for(N)
    ah=A_direct(h,q,p);ag=A_direct(h-1,q,p)
    assert gcd(ah,ag,p)==[1]
    assert ag[0]!=0
    moments=[pow(q,m*(m-1)//2,p) for m in range(N)]
    forbidden=[1]+[0]*(N-1)+[1]
    F=[0]+ah
    for t in range(1,2*N+1):
        B=add(F,scale(ag,t,p),p)
        if gcd(B,deriv(B,p),p)==[1] and gcd(B,forbidden,p)==[1]:break
    else:raise AssertionError(('candidate_bound_failed',N,p))
    assert len(B)==h+2 and B[-1]==1 and B[0]!=0
    for shift in range(h-1):
        assert sum(B[j]*moments[shift+j] for j in range(h+2))%p==0
    # Verify the recurrence reproduces all N moments from its first h+1 values.
    recovered=moments[:h+1]
    while len(recovered)<N:
        shift=len(recovered)-(h+1)
        recovered.append(-sum(B[j]*recovered[shift+j] for j in range(h+1))%p)
    assert recovered==moments
    return {'N':N,'p':p,'q':q,'parameter_t':t,'degree':h+1,'gcd_B_derivative':0,'gcd_B_forbidden':0,'moments':'PASS'}


def main():
    results={'symbolic':symbolic_checks(),'finite_fields':[]}
    sizes=list(range(4,132,2))+[256,512,1024]
    for N in sizes:
        r=check_size(N);results['finite_fields'].append(r)
        print(f"PASS N={N} p={r['p']} q={r['q']} t={r['parameter_t']} degree={r['degree']}",flush=True)
    results['disclaimer']='Finite tests supplement, and do not replace, the uniform proof.'
    target=Path(__file__).with_name('check_results.json')
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(f'Wrote {target}')

if __name__=='__main__':main()
