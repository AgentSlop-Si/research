#!/usr/bin/env python3
"""Additional exact screen using all contiguous intervals in both orders.
The rank allowance is q + boundary(A)+boundary(B), with a prefix/suffix
having one boundary and a strict interior interval two. NumPy int64 only.
"""
import json
from pathlib import Path
from fractions import Fraction
import numpy as np
from discrepancy_screen import structured, screen

def interval_screen(p):
    n=len(p)
    p=np.array(p,dtype=np.int64)
    starts=[];ends=[];costs=[]
    for c in range(n):
        for d in range(c+1,n+1):
            starts.append(c);ends.append(d)
            costs.append(2-int(c==0)-int(d==n))
    starts=np.array(starts);ends=np.array(ends);costs=np.array(costs)
    best=(-10*n,None)
    for a in range(n):
        for b in range(a+1,n+1):
            costA=2-int(a==0)-int(b==n)
            z=np.concatenate(([0],np.cumsum(n*((p>=a)&(p<b)).astype(np.int64)-(b-a))))
            signed=z[ends]-z[starts]
            totalcost=costA+costs
            excess=np.abs(signed)-n*totalcost
            # Ignore the full/full, zero-allowance equality.
            excess=np.where(totalcost>0,excess,-10*n)
            ix=int(np.argmax(excess))
            if int(excess[ix])>best[0]:
                c=int(starts[ix]);d=int(ends[ix]);
                q=sum(a<=int(x)<b for x in p[c:d])
                assert int(signed[ix])==n*q-(b-a)*(d-c)
                best=(int(excess[ix]),dict(A=[a,b],B=[c,d],q=q,
                      discrepancy=str(Fraction(abs(int(signed[ix])),n)),
                      boundary_allowance=int(totalcost[ix])))
    return dict(passes=best[0]<=0,maximum_scaled_excess=best[0],witness=best[1])

out=[]
for n in (32,64):
    seen=set();rows=[]
    for family,parameters,p in structured(n):
        if not screen(p)['passes'] or tuple(p) in seen:
            continue
        seen.add(tuple(p))
        rows.append(dict(family=family,parameters=parameters,**interval_screen(p)))
    if n==32:
        for sigma in [(3,4,2,1,0),(4,2,3,1,0),(4,3,1,2,0),(4,3,2,0,1),(4,3,2,1,0)]:
            p=[sum(((j>>sigma[t])&1)<<t for t in range(5)) for j in range(n)]
            if tuple(p) not in seen:
                seen.add(tuple(p));rows.append(dict(family='coordinate_bits',parameters={'sigma':sigma},**interval_screen(p)))
    print('N',n,'unique corner-screen survivors',len(rows),'interval-screen failures',sum(not r['passes'] for r in rows),flush=True)
    for r in rows:
        if not r['passes']:print(r,flush=True)
    out.append(dict(n=n,candidates=rows))
Path(__file__).with_name('discrepancy_interval_results.json').write_text(json.dumps(out,indent=2)+'\n')
