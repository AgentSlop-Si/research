#!/usr/bin/env python3
"""Fresh exact controls; no historical code imported or executed."""
import json, math, hashlib
from fractions import Fraction
from pathlib import Path
from prepare_cores import prepare
P=65537
COUNTS={'roots':0,'core_instances':0,'core_entries_checked':0,'all_entry_reconstructions':0,'full_unfolding_ranks':0,'cut_factorizations':0,'negative_controls':0,'integer_profiles':0}

def order(n):
    out=[];lo=0;hi=n-1
    while lo<=hi:
        out.append(lo);lo+=1
        if lo<=hi:out.append(hi);hi-=1
    return out

def chirp(t,w,p):return pow(w,(-t*(t+1)//2)%(p-1),p)

def rank(A,p):
    A=[r[:] for r in A];m=len(A);n=len(A[0]);r=0
    for c in range(n):
        z=next((z for z in range(r,m) if A[z][c]%p),None)
        if z is None:continue
        A[r],A[z]=A[z],A[r];inv=pow(A[r][c],-1,p)
        A[r]=[(v*inv)%p for v in A[r]]
        for z in range(r+1,m):
            x=A[z][c]
            if x:A[z]=[(b-x*a)%p for a,b in zip(A[r],A[z])]
        r+=1
        if r==m:break
    return r

def subset_value(x,bits):return sum(((x>>a)&1)<<b for a,b in enumerate(bits))

def make_cores(n,w,p):
    """Generic exact sparse cores from the theorem, powers computed directly for controls.
    This checker intentionally does not implement the asymptotically cheaper preparation
    recurrence from the report; its calls to pow are charged separately below.
    """
    pi=order(n)
    s=next(k for k in range(1,n+1) if (k+1)//2>=n-k)
    cores=[];types=[]
    for k,bit in enumerate(pi,1):
        core={}
        if k<s:
            j=k//2 # ceil((k-1)/2)
            for a in range(1<<j):
                for x in (0,1):
                    new=a+(x<<bit) if k%2 else a
                    core[(a,x,new)]=chirp(x<<bit,w,p)*pow(w,-a*(x<<bit),p)%p
            types.append('prefix')
        elif k==s:
            j=k//2
            for a in range(1<<j):
                for x in (0,1):
                    for z in range(1<<(n-k)):
                        y=subset_value(z,pi[k:]);v=(x<<bit)+y
                        core[(a,x,z)]=chirp(v,w,p)*pow(w,-a*v,p)%p
            types.append('bridge')
        else:
            for z in range(1<<(n-k+1)):
                x=z&1
                core[(z,x,z>>1)]=1
            types.append('suffix')
        cores.append(core)
    return cores,types,s

def contract(t,cores,pi,p):
    v={0:1}
    for k,core in enumerate(cores):
        x=(t>>pi[k])&1;out={}
        for (a,b,c),z in core.items():
            if b==x and a in v:out[c]=(out.get(c,0)+v[a]*z)%p
        v=out
    return v.get(0,0)

def run():
    evidence=[]
    for n in range(1,12):
        N=1<<n;pi=order(n)
        for u in (1,3,5):
            w=pow(3,((P-1)//N)*u,P)
            assert pow(w,N,P)==1 and pow(w,N//2,P)!=1
            COUNTS['roots']+=1
            cores,types,s=make_cores(n,w,P)
            paid,ledger=prepare(n,w,P)
            assert paid==cores
            assert ledger['field_multiplications']<=20*n+20*(1<<((n+1)//3))+2*(1<<((n+1)//3))**2
            COUNTS['core_instances']+=1
            COUNTS['core_entries_checked']+=sum(map(len,cores))
            actual=[]
            for k in range(1,n):
                states={z for a,x,z in cores[k-1]}
                want=1<<min((k+1)//2,n-k)
                assert len(states)==want
                actual.append(len(states))
            W=max(actual,default=1)
            assert W==1<<((n+1)//3)
            for t in range(N):
                got=contract(t,cores,pi,P)
                assert got==chirp(t,w,P),(n,u,t,got,chirp(t,w,P))
                COUNTS['all_entry_reconstructions']+=1
            evidence.append({'n':n,'embedding':u,'width':W,'bridge_stage':s,'nonzero_core_entries':sum(map(len,cores)),'entry_count':N,'paid_preparation':ledger})
            if n<=8:
                for k in range(1,n):
                    rows=[subset_value(a,pi[:k]) for a in range(1<<k)]
                    cols=[subset_value(b,pi[k:]) for b in range(1<<(n-k))]
                    H=[[chirp(a+b,w,P) for b in cols] for a in rows]
                    assert rank(H,P)==1<<min((k+1)//2,n-k)
                    COUNTS['full_unfolding_ranks']+=1
                    j=(k+1)//2
                    for a in rows:
                        low=a% (1<<j)
                        for b in cols:
                            assert chirp(a+b,w,P)==chirp(a,w,P)*chirp(b,w,P)*pow(w,-low*b,P)%P
                    COUNTS['cut_factorizations']+=1
    # Guard mutations: ordinary order cannot inherit interleaved rank profile;
    # ignoring the cross interaction cannot reconstruct the target.
    n=6;N=1<<n;w=pow(3,(P-1)//N,P)
    H=[[chirp(a+(b<<3),w,P) for b in range(8)] for a in range(8)]
    assert rank(H,P)==8 and 8>1<<((n+1)//3);COUNTS['negative_controls']+=1
    assert chirp(1+2,w,P)!=chirp(1,w,P)*chirp(2,w,P)%P;COUNTS['negative_controls']+=1
    try:
        prepare(n,w*w%P,P)
    except ValueError:
        COUNTS['negative_controls']+=1
    else:
        raise AssertionError('nonprimitive root was admitted')
    # Closed width and size claims, without exponentially large allocations.
    for n in range(1,301):
        pi=order(n);s=next(k for k in range(1,n+1) if (k+1)//2>=n-k)
        ranks=[1]+[1<<min((k+1)//2,n-k) for k in range(1,n)]+[1]
        W=1<<((n+1)//3)
        assert max(ranks)==W
        B=2*ranks[s-1]*ranks[s]
        M=sum(2*ranks[k-1] for k in range(1,s))+B+sum(ranks[k-1] for k in range(s+1,n+1))
        assert B<=2*W*W and M<=2*W*W+8*W
        COUNTS['integer_profiles']+=1
    # Exact rational sufficient Taylor-degree certificates, pi<22/7.
    degrees=[]
    for n in (18,30,64,128,1024):
        eps=Fraction(1,10**6);R=1;b=Fraction(88,7)
        while (n-1)*b**(2*R)>eps*eps*math.factorial(R)**2:R+=1
        degrees.append({'n':n,'relative_epsilon':'1/1000000','sufficient_rank':R,'exact_width':str(1<<((n+1)//3)),'squared_rational_bound_verified':True})
    return {'verdict':'PASS','counts':COUNTS,'core_controls':evidence,'taylor_degree_certificates':degrees,'scope':'Finite modular checks are indexing/implementation controls only. Uniform field, rank, storage and complex-error results rely on the report proofs. No historical executable or source code was imported.'}

if __name__=='__main__':
    result=run();out=Path(__file__).with_name('CHECK_RESULTS.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['counts'],sort_keys=True));print('PASS')
