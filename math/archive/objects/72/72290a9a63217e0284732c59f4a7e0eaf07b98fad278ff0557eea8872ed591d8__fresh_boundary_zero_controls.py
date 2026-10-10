"""Fresh exact cyclotomic zero scan. No supplied code or numerical zero test."""
from functools import lru_cache
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent
@lru_cache(None)
def cyclo(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d:continue
        b=cyclo(d);q=[0]*(len(a)-len(b)+1)
        while len(a)>=len(b):
            pos=len(a)-len(b);v=a[-1];q[pos]=v
            for j,c in enumerate(b):a[pos+j]-=v*c
            while a and not a[-1]:a.pop()
        assert not a;a=q
    return tuple(a)

def scan(n,b):
    phi=cyclo(n);deg=len(phi)-1;zero=(0,)*deg;one=(1,)+(0,)*(deg-1)
    nonzero_phi=[(j,c) for j,c in enumerate(phi[:-1]) if c]
    def reduce(a):
        a=list(a)
        while len(a)>deg:
            v=a.pop();off=len(a)-deg
            if v:
                for j,c in nonzero_phi:a[off+j]-=v*c
        return tuple(a+[0]*(deg-len(a)))
    def mulroot(a,k):return reduce([0]*(k%n)+list(a))
    def add(a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(a):return tuple(-x for x in a)
    aa=(n-1)//2-b;c=[one]
    # q=omega^{-1} is also primitive: its choice is harmless in this exact scan.
    for k in range(aa+1,n-aa):
        new=[zero]*(len(c)+1)
        for r,z in enumerate(c):
            new[r]=add(new[r],neg(mulroot(z,k)));new[r+1]=add(new[r+1],z)
        c=new
    hs=[mulroot(z,(r-b)*(r-b-1)//2) for r,z in enumerate(c)]
    lam=[]
    for k in range(n):
        z=zero
        for r,h in enumerate(hs):z=add(z,mulroot(h,k*(r-b)))
        lam.append(z)
    zeros=[k for k,z in enumerate(lam) if z==zero]
    # Check recurrence exactly in the same ring, using independently built sums.
    for k in range(n):
        rhs=add(lam[k],mulroot(lam[(k+2)%n],k-aa-b))
        lhs=add(mulroot(lam[(k+1)%n],b),mulroot(lam[(k+1)%n],k-aa))
        assert lhs==rhs
    return {'N':n,'a':aa,'b':b,'zero_indices':zeros,'nonzero_certified_over_complex_numbers':not zeros,'exact_recurrence_checked':True}
start=time.time();cases=[]
for n in range(3,34,2):
    for b in range((n-1)//2+1):cases.append(scan(n,b))
for n in [37,41,45,49,53,57,61,65]:cases.append(scan(n,(n-1)//4))
r={'evidence':'Exact integer polynomial remainders modulo Phi_N, not floating thresholds. Finite cases only.','cases':cases,'case_count':len(cases),'frequency_count':sum(x['N'] for x in cases),'zero_cases':[x for x in cases if x['zero_indices']],'seconds':time.time()-start}
(OUT/'fresh_boundary_zero_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='cases'},indent=2))
