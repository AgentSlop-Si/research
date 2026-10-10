"""Independent, self-contained audit of uploaded numerical proof objects.

This program was written for the audit. It does not import or execute uploaded
source. Only the JSON certificate is consumed as data.
"""
from pathlib import Path
from itertools import combinations
from collections import deque
import json
import random
import hashlib
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'superconcentrator_N8_certificate.json'
C = json.loads(SOURCE.read_text())
N, P, PRIME = C['n'], C['fixed_middle_shuffle'], C['field_prime']

class Flow:
    def __init__(self, size, edges):
        self.adj = [[] for _ in range(size)]
        for a,b,c in edges:
            x = [b,c,len(self.adj[b])]
            y = [a,0,len(self.adj[a])]
            self.adj[a].append(x); self.adj[b].append(y)

    def value(self, source, target):
        total = 0
        while True:
            level = [-1]*len(self.adj); level[source] = 0
            q = deque([source])
            while q:
                a = q.popleft()
                for b,c,_ in self.adj[a]:
                    if c and level[b] < 0:
                        level[b] = level[a]+1; q.append(b)
            if level[target] < 0: return total
            ptr = [0]*len(self.adj)
            def push(a, amount):
                if a == target: return amount
                while ptr[a] < len(self.adj[a]):
                    e = self.adj[a][ptr[a]]
                    b,c,reverse = e
                    if c and level[b] == level[a]+1:
                        got = push(b,min(amount,c))
                        if got:
                            e[1] -= got; self.adj[b][reverse][1] += got
                            return got
                    ptr[a] += 1
                return 0
            while True:
                got = push(source, N+1)
                if not got: break
                total += got

def network(n,r,p):
    ids = {}
    def port(*key):
        if key not in ids: ids[key] = len(ids)
        return ids[key]
    edges=[]; big=n+1
    def edge(a,b,c=big): edges.append((a,b,c))
    for stage in (0,1):
        for j in range(n):
            xi,xo,yi,yo = [port(stage,kind,j,side) for kind,side in [('x',0),('x',1),('y',0),('y',1)]]
            edge(xi,xo,1); edge(yi,yo,1); edge(xo,yi)
        # A forward state exists between j-1 and j, and contributes only to
        # outputs j and later. A backward state is the reverse counterpart.
        for direction in (1,-1):
            order = list(range(n)) if direction == 1 else list(range(n-1,-1,-1))
            last = None
            for previous,current in zip(order,order[1:]):
                a,b = port(stage,'s'+str(direction),current,0),port(stage,'s'+str(direction),current,1)
                edge(a,b,r); edge(port(stage,'x',previous,1),a)
                edge(b,port(stage,'y',current,0))
                if last is not None: edge(last,a)
                last=b
    for j,k in enumerate(p): edge(port(0,'y',k,1),port(1,'x',j,0))
    source,target = port('source'),port('target')
    return edges,ids,source,target

def all_cuts():
    edges,ids,src,sink = network(N,1,P)
    counts={}
    for k in range(1,N+1):
        subsets=list(combinations(range(N),k)); count=0
        for rows in subsets:
            ends=[(ids[1,'y',j,1],sink,N+1) for j in rows]
            for cols in subsets:
                starts=[(src,ids[0,'x',j,0],N+1) for j in cols]
                value=Flow(len(ids),edges+ends+starts).value(src,sink)
                assert value==k,(rows,cols,value)
                count+=1
        counts[str(k)]=count
    assert counts==C['flow_counts_by_size']
    return counts

def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col))%PRIME for col in zip(*b)] for row in a]

def stage_values(params):
    low,lv,up,uv,diag=params
    return [[diag[i] if i==j else (low[i]*lv[j] if i>j else up[i]*uv[j])%PRIME for j in range(N)] for i in range(N)]

def perturbations(params):
    low,lv,up,uv,diag=params
    # Match the declared parameter ordering, but construct derivatives directly
    # from the elementary monomials defining each triangular matrix entry.
    for kind in range(5):
        for k in range(N):
            a=[[0]*N for _ in range(N)]
            if kind==0: a[k][k]=1
            elif kind==1:
                for j in range(k): a[k][j]=lv[j]
            elif kind==2:
                for i in range(k+1,N): a[i][k]=low[i]
            elif kind==3:
                for j in range(k+1,N): a[k][j]=uv[j]
            elif kind==4:
                for i in range(k): a[i][k]=up[i]
            yield a

def gauss(matrix, determinant=False):
    a=[row[:] for row in matrix]; nr=len(a); nc=len(a[0]); rank=0; det=1
    for col in range(nc):
        pivot=next((i for i in range(rank,nr) if a[i][col]%PRIME),None)
        if pivot is None: continue
        if pivot!=rank: a[pivot],a[rank]=a[rank],a[pivot]; det=-det
        v=a[rank][col]%PRIME; det=det*v%PRIME; vi=pow(v,-1,PRIME)
        a[rank]=[x*vi%PRIME for x in a[rank]]
        for i in range(rank+1,nr):
            v=a[i][col]%PRIME
            if v: a[i]=[(x-v*y)%PRIME for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==nr: break
    if determinant: return det%PRIME if rank==nr else 0
    return rank

def jacobian_check():
    rng=random.Random(C['generator_parameter_seed'])
    one=[[rng.randrange(1,PRIME) for _ in range(N)] for _ in range(5)]
    two=[[rng.randrange(1,PRIME) for _ in range(N)] for _ in range(5)]
    a,b=stage_values(one),stage_values(two)
    pa=[a[j] for j in P]
    columns=[]
    for da in perturbations(one): columns.append(sum(matmul(b,[da[j] for j in P]),[]))
    for db in perturbations(two): columns.append(sum(matmul(db,pa),[]))
    j=[list(row) for row in zip(*columns)]
    selected=[[j[r][c] for c in C['jacobian_minor_columns']] for r in C['jacobian_minor_rows']]
    rank,det=gauss(j),gauss(selected,determinant=True)
    assert rank==60
    assert det==C['jacobian_minor_determinant_mod_prime']==4779
    # Verify every coordinate derivative with exact one-unit polynomial
    # differences. The map is affine in each individual parameter.
    m=sum(matmul(b,pa),[])
    for idx,col in enumerate(columns):
        pars=[v[:] for v in (one if idx<5*N else two)]
        local=idx%(5*N); kind,k=divmod(local,N)
        position=[4,0,1,2,3][kind]; pars[position][k]+=1
        aa=stage_values(pars) if idx<5*N else a
        bb=b if idx<5*N else stage_values(pars)
        value=sum(matmul(bb,[aa[t] for t in P]),[])
        assert [(v-w)%PRIME for v,w in zip(value,m)]==col
    return {'shape':[N*N,10*N],'rank':rank,'saved_minor_determinant':det,'field_prime':PRIME,'exact_coordinate_derivatives_checked':len(columns)}

if __name__=='__main__':
    start=time.monotonic()
    result={'input_certificate_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'uploaded_code_executed':False}
    result['jacobian']=jacobian_check()
    print('Jacobian certificate verified:',result['jacobian'],flush=True)
    result['flow_counts_by_size']=all_cuts()
    result['nonempty_equal_size_cuts']=sum(result['flow_counts_by_size'].values())
    result['seconds']=round(time.monotonic()-start,3)
    (ROOT/'independent_nonlinear_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
