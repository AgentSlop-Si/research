#!/usr/bin/env python3
"""Independent selected-projective-system controls; bounded finite-field oracle only."""
from itertools import product
from pathlib import Path
import json,random
OUT=Path(__file__).resolve().parent

def matmul(A,B,p): return tuple(sum(A[2*r+k]*B[2*k+c] for k in range(2))%p for r in range(2) for c in range(2))
def transpose(A): return (A[0],A[2],A[1],A[3])
def matvec(A,x,p):return ((A[0]*x[0]+A[1]*x[1])%p,(A[2]*x[0]+A[3]*x[1])%p)
def adj(A,p):return (A[3]%p,-A[1]%p,-A[2]%p,A[0]%p)
def rank(A,p): return 2 if (A[0]*A[3]-A[1]*A[2])%p else int(any(a%p for a in A))
def point(x,p):
    assert any(a%p for a in x)
    return (1,x[1]*pow(x[0],-1,p)%p) if x[0]%p else (0,1)
def P1(p):return [(1,t) for t in range(p)]+[(0,1)]
def bilinear(A,x,y,p):return (y[0]*(A[0]*x[0]+A[1]*x[1])+y[1]*(A[2]*x[0]+A[3]*x[1]))%p

def trim(a):
    a=list(a)
    while a and a[-1]==0:a.pop()
    return a

def gcd(a,b,p):
    a,b=trim(a),trim(b)
    while b:
        r=a[:]
        while len(r)>=len(b):
            t=r[-1]*pow(b[-1],-1,p)%p;j=len(r)-len(b)
            for k,z in enumerate(b):r[j+k]=(r[j+k]-t*z)%p
            r=trim(r)
        a,b=b,r
    return [(z*pow(a[-1],-1,p))%p for z in a] if a else []

def amo(ids,nextvar):
    k=len(ids)
    if k<=1:return [],nextvar
    ss=list(range(nextvar,nextvar+k-1));clauses=[]
    for i in range(k-1):clauses.append(((ids[i],False),(ss[i],True)))
    for i in range(1,k-1):clauses.append(((ss[i-1],False),(ss[i],True)))
    for i in range(1,k):clauses.append(((ids[i],False),(ss[i-1],False)))
    assert len(clauses)==3*k-4
    return clauses,nextvar+k-1

def satsolve(n,clauses):
    graph=[[] for _ in range(2*n)];rev=[[] for _ in graph]
    for aa,bb in clauses:
        a=2*aa[0]+int(aa[1]);b=2*bb[0]+int(bb[1])
        for u,v in ((a^1,b),(b^1,a)):graph[u].append(v);rev[v].append(u)
    vis=set();order=[]
    def dfs(u):
        vis.add(u)
        for v in graph[u]:
            if v not in vis:dfs(v)
        order.append(u)
    for u in range(2*n):
        if u not in vis:dfs(u)
    cc=[-1]*(2*n)
    def assign(u,k):
        cc[u]=k
        for v in rev[u]:
            if cc[v]<0:assign(v,k)
    k=0
    for u in reversed(order):
        if cc[u]<0:assign(u,k);k+=1
    if any(cc[2*i]==cc[2*i+1] for i in range(n)):return None
    sol=[cc[2*i+1]>cc[2*i] for i in range(n)]
    assert all(sol[a[0]]==a[1] or sol[b[0]]==b[1] for a,b in clauses)
    return sol

def solve(n,edges,p):
    I=(1,0,0,1);J=(0,1,p-1,0);adjlist=[[] for _ in range(n)]
    for i,k,L in edges:
        if rank(L,p)==2:
            R=matmul(J,L,p);adjlist[i].append((k,R));adjlist[k].append((i,adj(R,p)))
    comp=[None]*n;T=[None]*n;roots=[]
    for r in range(n):
        if comp[r] is not None:continue
        c=len(roots);roots.append(r);comp[r]=c;T[r]=I;todo=[r]
        while todo:
            i=todo.pop()
            for k,R in adjlist[i]:
                if comp[k] is None:comp[k]=c;T[k]=matmul(R,T[i],p);todo.append(k)
    qlist=[[] for _ in roots];cross=[]
    for i,k,L in edges:
        B=matmul(matmul(transpose(T[k]),L,p),T[i],p)
        if comp[i]==comp[k]:qlist[comp[i]].append((B[0],(B[1]+B[2])%p,B[3]))
        elif rank(B,p)==1:
            a,b=next((a,b) for a in range(2) for b in range(2) if B[2*a+b])
            row=(B[2*a],B[2*a+1]);col=(B[b],B[2+b])
            alpha=point((row[1],-row[0]),p);beta=point((col[1],-col[0]),p)
            # Exact factor-derived disjunction, exhaustive on P1 for this test field.
            assert all((bilinear(B,x,y,p)==0)==(x==alpha or y==beta) for x,y in product(P1(p),repeat=2))
            cross.append((comp[i],alpha,comp[k],beta))
        else:assert rank(B,p)==0
    domains=[]
    for qs in qlist:
        gg=[];inf=True
        for q in qs:
            gg=gcd(gg,q,p);inf&=(q[2]==0)
        direct=[x for x in P1(p) if all((a*x[0]*x[0]+b*x[0]*x[1]+c*x[1]*x[1])%p==0 for a,b,c in qs)]
        by_gcd=[(1,t) for t in range(p) if sum(a*pow(t,j,p) for j,a in enumerate(gg))%p==0]
        if inf:by_gcd.append((0,1))
        assert direct==by_gcd
        if not direct:return None
        domains.append(direct)
    labels=sorted({(a,x) for a,x,b,y in cross}|{(b,y) for a,x,b,y in cross})
    ids={key:i for i,key in enumerate(labels)};nextvar=len(ids);clauses=[];groups=[]
    for c in range(len(roots)):
        group=[ids[(cc,x)] for cc,x in labels if cc==c];groups.append(group)
        aa,nextvar=amo(group,nextvar);clauses+=aa
    for c,x in labels:
        if x not in domains[c]:clauses.append(((ids[(c,x)],False),(ids[(c,x)],False)))
    for a,x,b,y in cross:clauses.append(((ids[(a,x)],True),(ids[(b,y)],True)))
    sol=satsolve(nextvar,clauses)
    if sol is None:return None
    choices=[];repaired=0
    for c in range(len(roots)):
        named=[x for cc,x in labels if cc==c and sol[ids[(cc,x)]]]
        assert len(named)<=1
        if named:choice=named[0]
        else:
            choice=domains[c][0];repaired+=1
            if (c,choice) in ids:sol[ids[(c,choice)]]=True
        assert choice in domains[c];choices.append(choice)
    # Recompute sequential prefix variables after repairs and check every clause.
    cursor=len(ids)
    for group in groups:
        if len(group)>=2:
            for j in range(len(group)-1):sol[cursor+j]=any(sol[v] for v in group[:j+1])
            cursor+=len(group)-1
    assert all(sol[a[0]]==a[1] or sol[b[0]]==b[1] for a,b in clauses)
    directions=[point(matvec(T[i],choices[comp[i]],p),p) for i in range(n)]
    assert all(bilinear(L,directions[i],directions[k],p)==0 for i,k,L in edges)
    return directions,repaired

def exhaustive(n,edges,p):
    return next((xs for xs in product(P1(p),repeat=n) if all(bilinear(L,xs[i],xs[k],p)==0 for i,k,L in edges)),None)

def run():
    rng=random.Random(287121);total=accepted=repaired=0
    for p in (2,3,5):
        for n in (1,2,3,4):
            for trial in range(160):
                edges=[(rng.randrange(n),rng.randrange(n),tuple(rng.randrange(p) for _ in range(4))) for _ in range(rng.randrange(0,10))]
                got=solve(n,edges,p);want=exhaustive(n,edges,p)
                assert (got is None)==(want is None),(p,n,edges,got,want)
                total+=1
                if got is not None:accepted+=1;repaired+=got[1]
    # All matrices, one edge; includes singular directions and characteristic two.
    exhaustive_matrices=0
    for p in (2,3,5):
        for L in product(range(p),repeat=4):
            assert solve(2,[(0,1,L)],p) is not None
            exhaustive_matrices+=1
    amo_patterns=0
    for k in range(0,9):
        cs,n=amo(list(range(k)),k)
        for flags in product((False,True),repeat=k):
            units=[((i,flags[i]),(i,flags[i])) for i in range(k)]
            assert (satsolve(n,cs+units) is not None)==(sum(flags)<=1)
            amo_patterns+=1
    # Closure/base-field distinction: t^2+1 over F3 has closure roots only.
    g=gcd([], [1,0,1],3)
    assert len(g)==3 and not any(sum(a*pow(t,j,3) for j,a in enumerate(g))%3==0 for t in range(3))
    # Three quadratics can be needed: xy, x(x-y), y(x-y).
    tight=0
    for p in (2,3,5,7):
        qs=[(0,1,0),(1,p-1,0),(0,1,p-1)]
        ds=[{x for x in P1(p) if (q[0]*x[0]**2+q[1]*x[0]*x[1]+q[2]*x[1]**2)%p==0} for q in qs]
        assert not set.intersection(*ds) and all(ds[i]&ds[j] for i in range(3) for j in range(i))
        tight+=1
    result={'status':'PASS','random_full_selected_graphs':total,'satisfiable_random_graphs':accepted,'all_false_components_repaired':repaired,'exhaustive_single_edge_matrices':exhaustive_matrices,'AMO_flag_patterns':amo_patterns,'tight_three_quadratic_fields':tight,'base_vs_closure_root_counterexample':'t^2+1 over GF(3)','fields':[2,3,5],'max_vertices':4,'method':'Fresh forest/rank-one/gcd/sequential-SCC solver compared to exhaustive original projective assignments; root enumeration is a bounded verifier oracle, not the proposed complexity bound.'}
    (OUT/'INDEPENDENT_C10_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
