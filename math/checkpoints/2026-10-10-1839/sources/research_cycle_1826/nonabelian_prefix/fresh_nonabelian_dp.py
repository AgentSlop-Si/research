#!/usr/bin/env python3
"""Fresh exact finite-group subset DP, authored for this boundary check."""
from itertools import permutations
from fractions import Fraction
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

def permutation_group(n, even=False):
    els = [p for p in permutations(range(n)) if not even or sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)) % 2 == 0]
    ix = {p:i for i,p in enumerate(els)}
    return [str(p) for p in els], [[ix[tuple(a[b[i]] for i in range(n))] for b in els] for a in els]

def dihedral(n, action=None):
    if action is None: action=n-1
    assert pow(action,2,n)==1
    els = [(a,b) for b in range(2) for a in range(n)]
    ix = {x:i for i,x in enumerate(els)}
    return [f'r{a}s{b}' for a,b in els], [[ix[((a+action**b*c)%n,(b+d)%2)] for c,d in els] for a,b in els]

def quaternion():
    # Units 1,i,j,k, signs positive then negative; i*j=k, j*k=i, k*i=j.
    els = [(s,u) for s in (1,-1) for u in range(4)]
    ix = {v:i for i,v in enumerate(els)}
    def mul(x,y):
        s,a=x;t,b=y
        if a==0:return (s*t,b)
        if b==0:return (s*t,a)
        if a==b:return (-s*t,0)
        return ((s*t if (a,b) in ((1,2),(2,3),(3,1)) else -s*t),6-a-b)
    return [('' if s==1 else '-')+('1','i','j','k')[u] for s,u in els], [[ix[mul(x,y)] for y in els] for x in els]

def abelian_value(n):
    d=n;p=2;w=Fraction(0)
    while d>1:
        while d%p==0:w+=1-Fraction(1,p);d//=p
        p+=1
    return int(n*w)

def subgroup_closure(mask, table):
    old=-1
    while old!=mask:
        old=mask;els=[x for x in range(len(table)) if mask>>x&1]
        for a in els:
            for b in els:mask|=1<<table[a][b]
    return mask

def run(name, labels, table):
    n=len(table);full=(1<<n)-1
    assert all(table[0][i]==i==table[i][0] for i in range(n))
    assert all(sorted(row)==list(range(n)) for row in table)
    assert all(table[table[a][b]][c]==table[a][table[b][c]] for a in range(n) for b in range(n) for c in range(n))
    stabilizers=[0]*(1<<n)
    for g in range(n):
        trans=[0]*(1<<n)
        for mask in range(1,1<<n):
            bit=mask&-mask;x=bit.bit_length()-1
            trans[mask]=trans[mask^bit]|(1<<table[g][x])
            if trans[mask]==mask:stabilizers[mask]|=1<<g
    # Right translation sends x_1 to e and leaves each left stabilizer unchanged.
    best=[-1]*(1<<n);count=[0]*(1<<n);last=[-1]*(1<<n)
    best[1]=0;count[1]=1
    for mask in range(3,1<<n,2):
        rem=mask^1;b=-1;c=0;xlast=-1
        while rem:
            bit=rem&-rem;rem^=bit;x=bit.bit_length()-1
            prev=mask^bit
            if best[prev]>b:b=best[prev];c=count[prev];xlast=x
            elif best[prev]==b:c+=count[prev]
        best[mask]=b+stabilizers[mask].bit_count()-1
        count[mask]=c;last[mask]=xlast
    witness=[];mask=full
    while mask!=1:
        x=last[mask];witness.append(x);mask^=1<<x
    witness.append(0);witness.reverse()
    weights=[];stablabels=[];mask=0;acc=1;first_failure=None
    for j,x in enumerate(witness,1):
        mask|=1<<x;stab=stabilizers[mask]
        literal=sum(1<<g for g in range(n) if {table[g][y] for y in range(n) if mask>>y&1}=={y for y in range(n) if mask>>y&1})
        assert literal==stab
        weights.append(stab.bit_count());stablabels.append([labels[g] for g in range(n) if stab>>g&1])
        acc=subgroup_closure(acc|stab,table)
        if acc&~mask and first_failure is None:first_failure=j
    result=dict(group=name,order=n,maximum=best[full],abelian_value=abelian_value(n),labeled_optimal_orders=n*count[full],witness=[labels[x] for x in witness],witness_indices=witness,stabilizer_orders=weights,stabilizers=stablabels,accumulated_containment_first_failure=first_failure,states=1<<(n-1))
    assert sum(h-1 for h in weights)==best[full]
    print(json.dumps(result),flush=True)
    return result,table,stabilizers,best

if __name__=='__main__':
    cases=[('S3',permutation_group(3)),('D8',dihedral(4)),('Q8',quaternion()),('D10',dihedral(5)),('A4',permutation_group(4,True)),('D12',dihedral(6)),('D14',dihedral(7)),('D16',dihedral(8)),('M16',dihedral(8,5)),('D18',dihedral(9))]
    results=[run(name,*data)[0] for name,data in cases]
    (OUT/'fresh_exact_results.json').write_text(json.dumps(results,indent=2)+'\n')
