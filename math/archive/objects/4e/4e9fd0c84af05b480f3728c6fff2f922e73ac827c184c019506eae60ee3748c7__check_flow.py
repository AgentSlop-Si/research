#!/usr/bin/env python3
"""Independent integer max-flow controls, without networkx/scipy or source code imports."""
import json,random
from collections import deque
from pathlib import Path
BASE=Path(__file__).parent

def mask_set(n,m):return {j for j in range(n) if (j&m).bit_count()%2==0}

def network_bound(n,perms,cols,rows):
    stages=len(perms)+1;inf=n+1;V=8*n*stages+2;src=V-2;sink=V-1;graph=[[] for _ in range(V)]
    def node(s,kind,j,half):return 8*n*s+2*n*kind+2*j+half
    def edge(u,v,cap):
        graph[u].append([v,cap,len(graph[v])]);graph[v].append([u,0,len(graph[u])-1])
    for s in range(stages):
        for j in range(n):
            edge(node(s,0,j,0),node(s,0,j,1),1);edge(node(s,1,j,0),node(s,1,j,1),1);edge(node(s,0,j,1),node(s,1,j,0),inf)
        for j in range(1,n):
            edge(node(s,2,j,0),node(s,2,j,1),1);edge(node(s,0,j-1,1),node(s,2,j,0),inf);edge(node(s,2,j,1),node(s,1,j,0),inf)
            if j<n-1:edge(node(s,2,j,1),node(s,2,j+1,0),inf)
        for j in range(n-1):
            edge(node(s,3,j,0),node(s,3,j,1),1);edge(node(s,0,j+1,1),node(s,3,j,0),inf);edge(node(s,3,j,1),node(s,1,j,0),inf)
            if j:edge(node(s,3,j,1),node(s,3,j-1,0),inf)
    for s,pi in enumerate(perms):
        for j,old in enumerate(pi):edge(node(s,1,old,1),node(s+1,0,j,0),inf)
    for j in cols:edge(src,node(0,0,j,0),inf)
    for i in rows:edge(node(stages-1,1,i,1),sink,inf)
    flow=0
    while True:
        pred=[None]*V;pred[src]=(-1,-1);queue=deque([src])
        while queue and pred[sink] is None:
            u=queue.popleft()
            for j,(v,cap,_) in enumerate(graph[u]):
                if cap and pred[v] is None:pred[v]=(u,j);queue.append(v)
        if pred[sink] is None:return flow
        v=sink;delta=inf
        while v!=src:u,j=pred[v];delta=min(delta,graph[u][j][1]);v=u
        v=sink
        while v!=src:
            u,j=pred[v];back=graph[u][j][2];graph[u][j][1]-=delta;graph[v][back][1]+=delta;v=u
        flow+=delta

def shuffles(k):
    rng=random.Random(20261016+17*k);perms=[]
    for s in range(3):
        rows=[1<<j for j in range(k)]
        for _ in range(2*k*k):
            i,j=rng.sample(range(k),2)
            if rng.randrange(4)==0:rows[i],rows[j]=rows[j],rows[i]
            else:rows[i]^=rows[j]
        perms.append([sum(((x&row).bit_count()%2)<<i for i,row in enumerate(rows)) for x in range(1<<k)])
    return perms

if __name__=='__main__':
    source=json.loads((BASE/'sources/moving/EXACT_CERTIFICATES.json').read_text());tight=[];survive=[]
    for case in source['cases']:
        if case['n'] not in (128,256) or case['name'] not in ('rotations','twisted_bitrev','middle_xor'):continue
        n=case['n'];cols=mask_set(n,case['initial_parity_mask']);a=cols
        for pi in case['permutations']:a={j for j in range(n) if pi[j] in a}
        rows=set(range(n))-a;value=network_bound(n,case['permutations'],cols,rows);assert value==case['bound']
        tight.append({'N':n,'name':case['name'],'capacity':value})
    for k in (6,7,8):
        n=1<<k;ps=shuffles(k);rng=random.Random(k)
        probes=[(list(range(n//2)),list(range(n//2,n))),(list(range(0,n,2)),list(range(1,n,2))),
                (mask_set(n,1<<(k//2)),set(range(n))-mask_set(n,1<<(k//2)))]
        for _ in range(5):probes.append((rng.sample(range(n),n//2),rng.sample(range(n),n//2)))
        values=[network_bound(n,ps,c,r) for c,r in probes];assert values==[n//2]*8
        survive.append({'N':n,'probe_capacities':values})
    result={'status':'PASS','tight_selected_cuts':tight,'survivor_controls':survive,'scope':'Structural network capacity only; coefficients not fit'}
    (BASE/'FLOW_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS: six tight moving cuts and 24 full-capacity survivor probes')
