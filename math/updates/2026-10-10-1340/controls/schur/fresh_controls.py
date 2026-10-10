"""Fresh audit controls; no uploaded code is imported or executed."""
from itertools import combinations, permutations
from collections import deque
from pathlib import Path
from random import Random
import json

def det(a,p):
    a=[list(row) for row in a]; n=len(a); ans=1
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]%p),None)
        if k is None:return 0
        if k!=j:a[j],a[k]=a[k],a[j];ans=-ans
        x=a[j][j]%p;ans=ans*x%p
        for k in range(j+1,n):
            t=a[k][j]*pow(x,-1,p)%p
            for l in range(j,n):a[k][l]=(a[k][l]-t*a[j][l])%p
    return ans%p

def rank(a,p):
    a=[list(row) for row in a];r=0
    if not a:return 0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]%p),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]; q=pow(a[r][j]%p,-1,p)
        a[r]=[v*q%p for v in a[r]]
        for k in range(len(a)):
            if k!=r:
                t=a[k][j]%p;a[k]=[(x-t*y)%p for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r

def sub(a,I,J):return [[a[i][j] for j in J] for i in I]

def pairs(n):
    for k in range(1,n+1):
        for I in combinations(range(n),k):
            for J in combinations(range(n),k):yield I,J

def flow(nn,E,I,O):
    # Independent Edmonds-Karp implementation, not the source's Dinic method.
    s,t=2*nn,2*nn+1;cap=[{} for _ in range(2*nn+2)]
    def edge(u,v,c):cap[u][v]=cap[u].get(v,0)+c;cap[v].setdefault(u,0)
    for u in range(nn):edge(2*u,2*u+1,1)
    for u,v,_ in E:edge(2*u+1,2*v,nn)
    for u in I:edge(s,2*u,1)
    for v in O:edge(2*v+1,t,1)
    f=0
    while True:
        prev={s:None}; q=deque([s])
        while q and t not in prev:
            u=q.popleft()
            for v,c in cap[u].items():
                if c and v not in prev:prev[v]=u;q.append(v)
        if t not in prev:return f
        v=t
        while v!=s:u=prev[v];cap[u][v]-=1;cap[v][u]+=1;v=u
        f+=1

def transfer(nn,E,I,O,p):
    vectors=[[0]*len(I) for _ in range(nn)]
    for j,u in enumerate(I):vectors[u][j]=1
    outgoing=[[] for _ in range(nn)]
    for u,v,w in E:outgoing[u].append((v,w))
    for u in range(nn):
        for v,w in outgoing[u]:
            vectors[v]=[(a+w*b)%p for a,b in zip(vectors[v],vectors[u])]
    return [vectors[v] for v in O]

def depth(nn,E,I,O):
    ds=[None]*nn
    for u in I:ds[u]=0
    for u in range(nn):
        for a,v,_ in E:
            if a==u and ds[u] is not None:ds[v]=max(ds[v] or 0,ds[u]+1)
    return max(ds[v] or 0 for v in O)

def benes(n,seed,p):
    k=n.bit_length()-1; bits=list(range(k))+list(range(k-2,-1,-1)); rng=Random(seed)
    E=[]
    for layer,bit in enumerate(bits):
        for u in range(n):
            for v in (u,u^(1<<bit)):E.append((layer*n+u,(layer+1)*n+v,rng.randrange(1,p)))
    return (len(bits)+1)*n,E,list(range(n)),list(range(len(bits)*n,(len(bits)+1)*n))

def depth2_support_ok(n,mask):
    # Direct enumeration of all vertex-disjoint length-two path families.
    for I,J in pairs(n):
        k=len(I);works=False
        for mids in permutations(range(n),k):
            if not all(mask>>(i*n+m)&1 for i,m in zip(I,mids)):continue
            for outs in permutations(J):
                if all(mask>>(n*n+m*n+j)&1 for m,j in zip(mids,outs)):
                    works=True;break
            if works:break
        if not works:return False
    return True

out={"uploaded_programs_run_or_imported":False}
mins=[]
for n in (2,3):
    size=2*n*n
    for e in range(2*n,size+1):
        winners=0
        for ix in combinations(range(size),e):
            mask=sum(1<<i for i in ix)
            if depth2_support_ok(n,mask):winners+=1
        if winners:mins.append({"n":n,"middle_count":n,"edges":e,"minimizers":winners});break
out["depth2_minima"]=mins
assert [(a['edges'],a['minimizers']) for a in mins]==[(6,12),(11,216)]

bn=[];p=1000003
for n in (4,8):
    nn,E,I,O=benes(n,3100+n,p); M=transfer(nn,E,I,O,p);checked=0
    for rows,cols in pairs(n):
        assert det(sub(M,rows,cols),p)
        assert flow(nn,E,[I[j] for j in cols],[O[i] for i in rows])==len(rows)
        checked+=1
    bn.append({"n":n,"nodes":nn,"edges":len(E),"depth":depth(nn,E,I,O),"all_minors_and_path_pairs":checked,"first_row":M[0]})
out["benes"]=bn

rng=Random(20261010);checks=0
for trial in range(80):
    n=3;nn=10;I=list(range(n));O=list(range(nn-n,nn));E=[]
    for u in range(nn-n):
        for v in range(max(u+1,n),nn):
            if rng.random()<.3:E.append((u,v,rng.randrange(-2,3)))
    rng.shuffle(E);M=transfer(nn,E,I,O,101)
    # Delete zero-weight edges to test the actual effective support as well.
    active=[e for e in E if e[2]%101]
    for rows,cols in pairs(n):
        assert rank(sub(M,rows,cols),101)<=flow(nn,active,[I[j] for j in cols],[O[i] for i in rows]);checks+=1
out["random_rank_flow"]=dict(graphs=80,subblocks=checks,field=101,weights_include_zero_and_minus_one=True)

fs=[]
for n,p,w in ((5,11,4),(7,29,16),(11,23,2)):
    m=n//2;B=[[pow(w,i*j,p) for j in range(n-m,n)] for i in range(m)]
    failures=[];num=0
    for rows,cols in pairs(m):
        num+=1
        if not det(sub(B,rows,cols),p):failures.append({"rows":rows,"local_columns":cols,"actual_columns":[n-m+j for j in cols]})
    fs.append({"n":n,"field":p,"root":w,"m":m,"rank":rank(B,p),"det":det(B,p),"minors_checked":num,"zero_minor_count":len(failures),"first_failure":failures[0] if failures else None})
out["fourier_half_rectangles"]=fs
assert fs[0]['zero_minor_count']==fs[1]['zero_minor_count']==0
assert fs[2]['zero_minor_count']>0

# Complete bipartite depth-one support is a superconcentrator, but all-one
# specialization is rank one. This is a cancellation/field-size control.
E=[(i,2+j,1) for i in range(2) for j in range(2)]
M=transfer(4,E,[0,1],[2,3],2)
assert flow(4,E,[0,1],[2,3])==2 and rank(M,2)==1
out["non_converse_control"]={"matrix":M,"field":2,"path_capacity":2,"rank":1,"comment":"Only possible all-nonzero 2x2 matrix over F2; no TN specialization over F2."}
out['status']='PASS'
Path(__file__).with_name('fresh_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
