#!/usr/bin/env python3
"""Independent exact controls for sparse-reference Green products."""
import json,random
from pathlib import Path
from exact_utils import Field,root
P=998244353;F=Field(P);BASE=Path(__file__).parent

def add(a,b,c=1):return [[(x+c*y)%P for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,v):return [[x*v%P for x in row] for row in a]
def diagonal(v):return [[x if i==j else 0 for j in range(len(v))] for i,x in enumerate(v)]
def successor(order):
    p=[0]*len(order)
    for i,j in enumerate(order):p[j]=order[(i+1)%len(order)]
    return p

def deficit(p,q):
    inv=[0]*len(p)
    for i,j in enumerate(p):inv[j]=i
    seen=set();count=0
    for v in range(len(p)):
        if v in seen:continue
        count+=1
        while v not in seen:seen.add(v);v=inv[q[v]]
    return len(p)-count

def cycle_orders(n,number,seed):
    rng=random.Random(seed+17*n);out=[];perms=[]
    while len(out)<number:
        order=list(range(n));rng.shuffle(order);p=successor(order)
        slope=(p[1]-p[0])%n
        if all(p[i]==(slope*i+p[0])%n for i in range(n)):continue
        if any(all(p[q[i]]==q[p[i]] for i in range(n)) for q in perms):continue
        out.append(order);perms.append(p)
    return out

def green(order,alpha):
    n=len(order);pos=[0]*n
    for i,j in enumerate(order):pos[j]=i
    den=F.inv(1-pow(alpha,n,P));powers=[pow(alpha,j,P)*den%P for j in range(n)]
    return [[powers[(pos[i]-pos[j])%n] for j in range(n)] for i in range(n)]

def denominator(order,alpha):
    n=len(order);out=F.eye(n)
    for j,i in enumerate(successor(order)):out[i][j]=(out[i][j]-alpha)%P
    return out

def stage(order,alpha,index,patched=False):
    n=len(order);a,b=1+index,n//2+1+index
    modified=[b if x==a else a if x==b else x for x in order]
    g0=green(order,alpha);g1=green(modified,alpha);delta=deficit(successor(order),successor(modified));assert delta==2
    assert F.mul(denominator(order,alpha),g0)==F.eye(n)
    if patched:
        l=[1]*n;r=[1]*n;l[(3+index)%n]=7+index;r[(7+index)%n]=11+index
        g1=[[x*l[i]*r[j]%P for j,x in enumerate(row)] for i,row in enumerate(g1)]
    s=add(g0,g1);si=F.inverse(s);core=scale(denominator(order,alpha),F.inv(2));rank=F.rank(add(si,core,-1))
    assert rank<=delta+2*patched
    if not patched:
        assert rank==delta
        assert F.rank(add(g1,g0,-1))==delta<n
    return si,core,rank

def nnz(a):return max(sum(bool(x) for x in row) for row in a)
def witness(core,k):
    n=len(core);m=n//(k+1);bad={j for row in core[:m] for j,x in enumerate(row) if x};columns=[j for j in range(n) if j not in bad][:m]
    assert len(columns)==m;z=root(n,P,3)
    if m:assert F.det([[pow(z,i*j,P) for j in columns] for i in range(m)])
    return columns

def reproduce():
    source=json.loads((BASE/'sources/phase34/audit.json').read_text());extra=json.loads((BASE/'sources/phase34/extra_audit.json').read_text());out=[]
    for expected in source['examples']:
        n=expected['N'];orders=cycle_orders(n,2,340034);terms=[stage(o,a,i) for i,(o,a) in enumerate(zip(orders,(3,5)))];rng=random.Random(340034+n);d=diagonal([F.inv(rng.randrange(1,P)) for _ in range(n)])
        actual=F.mul(F.mul(terms[0][0],d),terms[1][0]);core=F.mul(F.mul(terms[0][1],d),terms[1][1]);rank=F.rank(add(actual,core,-1))
        assert rank==expected['inverse_product_correction_rank'];assert nnz(core)==expected['inverse_sparse_core_max_row_nnz']
        assert witness(core,4)==expected['vandermonde_witness'];far=deficit(*map(successor,orders));assert far==expected['independent_cycle_difference_rank']
        out.append({'N':n,'product_correction_rank':rank,'reference_row_sparsity':nnz(core),'Fourier_required_rank':n//5,'far_cycle_deficit':far})
    orders=cycle_orders(64,2,341234);terms=[stage(o,a,i,True) for i,(o,a) in enumerate(zip(orders,(3,5)))];rng=random.Random(118);d=diagonal([F.inv(rng.randrange(1,P)) for _ in range(64)])
    actual=F.mul(F.mul(terms[0][0],d),terms[1][0]);core=F.mul(F.mul(terms[0][1],d),terms[1][1]);rank=F.rank(add(actual,core,-1));assert rank==extra['phase_patches']['inverse_correction_rank']==8;assert nnz(core)==4;witness(core,4)
    patch={'rank':rank,'required_rank':64//5,'stage_ranks':[t[2] for t in terms]}
    orders=cycle_orders(64,3,342234);terms=[stage(o,3+2*i,i) for i,o in enumerate(orders)]
    actual=terms[0][0];core=terms[0][1]
    for i,d in enumerate(([2+j for j in range(64)],[100+j for j in range(64)]),start=1):actual=F.mul(F.mul(actual,diagonal(d)),terms[i][0]);core=F.mul(F.mul(core,diagonal(d)),terms[i][1])
    rank=F.rank(add(actual,core,-1));assert rank==extra['three_stage']['correction_rank']==6;assert nnz(core)==8;witness(core,8)
    triple={'rank':rank,'required_rank':64//9,'stage_ranks':[t[2] for t in terms]}
    far_controls=[]
    for expected in extra['rank_distant_controls']:
        n=expected['N'];orders=cycle_orders(n,4,343334);greens=[green(o,3 if i<2 else 5) for i,o in enumerate(orders)];z=root(n,P,3);phase=[pow(z,i*i,P) for i in range(n)]
        def apply(v):
            mid=[sum((a+b)*x for a,b,x in zip(r,s,v))%P*phase[i]%P for i,(r,s) in enumerate(zip(greens[0],greens[1]))]
            return [sum((a+b)*x for a,b,x in zip(r,s,mid))%P for r,s in zip(greens[2],greens[3])]
        rng=random.Random(113+n);x=[rng.randrange(1,P) for _ in range(n)];mx=apply(x);mz=apply(x[-1:]+x[:-1]);md=apply([x[i]*pow(z,i,P)%P for i in range(n)])
        counts=[sum((mz[i]-pow(z,i,P)*mx[i])%P!=0 for i in range(n)),sum((md[i]-mx[(i+1)%n])%P!=0 for i in range(n))]
        ds=[deficit(successor(orders[2*i]),successor(orders[2*i+1])) for i in range(2)]
        assert ds==expected['independent_order_cycle_deficits'];assert counts==[expected['first_Weyl_defect_nonzero'],expected['second_Weyl_defect_nonzero']]
        far_controls.append({'N':n,'cycle_deficits':ds,'Weyl_nonzero_counts':counts})
    for row in source['uniform_bounds']:assert row['Fourier_minus_sparse_rank_floor']==row['N']//(2**row['stages']+1)>row['lowrank_budget']
    return {'near_products':out,'patched_product':patch,'three_stage_product':triple,'rank_distant_products':far_controls,'uniform_bounds':source['uniform_bounds']}

def general_sparse():
    rng=random.Random(3401);out=[]
    for n in (4,8,16,32,64):
        z=root(n,P,3)
        for k in range(min(n,7)):
            a=[[0]*n for _ in range(n)]
            for row in a:
                for j in rng.sample(range(n),k):row[j]=rng.randrange(1,P)
            cols=witness(a,k)
            for sign in (1,-1):
                fn=[[pow(z,sign*i*j,P) for j in range(n)] for i in range(n)]
                got=F.rank(add(fn,a,-1));assert got>=n//(k+1)
                out.append({'N':n,'row_sparsity':k,'orientation':sign,'actual_rank':got,'required_rank':n//(k+1),'witness_columns':cols})
    return out

if __name__=='__main__':
    result={'status':'PASS','field':P,'saved_experiments':reproduce(),'sparse_rigidity_controls':general_sparse()}
    (BASE/'PHASE34_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: saved phase34 matrix/rank controls reproduced; 64 arbitrary row-sparse Fourier controls')
