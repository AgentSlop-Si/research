#!/usr/bin/env python3
"""Paid modular reference for the report's exact interleaved TT core constructor.

The theorem operates over any field with a supplied primitive 2^n-th root.
This executable uses residues modulo a supplied prime. Root validation and every
modular multiplication during preparation are counted. Sparse scalar slots and
explicit index maps are counted. Python/bit costs are not equated to this ledger.
"""

def bit_order(n):
    out=[];lo=0;hi=n-1
    while lo<=hi:
        out.append(lo);lo+=1
        if lo<=hi:out.append(hi);hi-=1
    return out


def prepare(n,omega,prime):
    if not isinstance(n,int) or n<1:raise ValueError('n must be positive')
    N=1<<n
    count={'field_multiplications':0,'root_guard_multiplications':0}
    def mul(a,b):
        count['field_multiplications']+=1
        return a*b%prime
    def power(a,e):
        z=1
        while e:
            if e&1:z=mul(z,a)
            a=mul(a,a);e>>=1
        return z
    before=count['field_multiplications']
    if power(omega,N)!=1 or power(omega,N//2)==1:raise ValueError('root is not primitive')
    count['root_guard_multiplications']=count['field_multiplications']-before
    inv=power(omega,N-1)
    q=[inv]
    for _ in range(n-1):q.append(mul(q[-1],q[-1]))
    onebit=[inv]
    for p in range(n-1):onebit.append(mul(mul(onebit[-1],onebit[-1]),q[2*p] if 2*p<n else 1))
    pi=bit_order(n);s=next(k for k in range(1,n+1) if (k+1)//2>=n-k)
    cores=[];map_slots=0
    for k,p in enumerate(pi,1):
        core={}
        if k<s:
            j=k//2;phase=1
            for a in range(1<<j):
                core[(a,0,a)]=1
                core[(a,1,a+(1<<p) if k%2 else a)]=mul(onebit[p],phase)
                phase=mul(phase,q[p])
        elif k==s:
            j=k//2;D=1<<(n-k)
            # Explicit subset-sum values in the future digit order, O(D) writes.
            future=[0]
            for b in pi[k:]:future += [v+(1<<b) for v in future]
            mapping=[None]*(2*D)
            for z,y in enumerate(future):
                for x in (0,1):mapping[((x<<p)+y)>>j]=(x,z)
            map_slots=len(future)+len(mapping)
            G=1;ratio=onebit[j];zeta=1;step=q[2*j] if 2*j<n else 1
            for x,z in mapping:
                entry=G
                for a in range(1<<j):
                    core[(a,x,z)]=entry
                    entry=mul(entry,zeta)
                G=mul(G,ratio);ratio=mul(ratio,step);zeta=mul(zeta,q[j])
        else:
            for z in range(1<<(n-k+1)):core[(z,z&1,z>>1)]=1
        cores.append(core)
    count.update({'scalar_core_slots':sum(map(len,cores)),'explicit_bridge_map_slots':map_slots,'power_and_onebit_slots':2*n,'bridge_stage':s,'width':1<<((n+1)//3),'n':n})
    return cores,count
