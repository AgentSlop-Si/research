#!/usr/bin/env python3
"""Independent exact review of the moving-partition source. Uploaded code is inert."""
import json,random
from pathlib import Path
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent

def boundary(a,n):return sum((j in a)!=((j+1) in a) for j in range(n-1))
def mask_set(n,m):return {j for j in range(n) if (j&m).bit_count()%2==0}
def bformula(k,m):return sum(2**(k-1-s) for s in range(k) if (m&((1<<(s+1))-1)).bit_count()%2)
def primitive(n,p):
    for a in range(2,p):
        w=pow(a,(p-1)//n,p)
        if pow(w,n,p)==1 and (n==1 or pow(w,n//2,p)!=1):return w
    raise AssertionError

def certificates():
    source=json.loads((BASE/'sources/moving/EXACT_CERTIFICATES.json').read_text());out=[]
    for case in source['cases']:
        n=case['n'];a=mask_set(n,case['initial_parity_mask']);initial=sorted(a);cost=[boundary(a,n)];sets=[a]
        for pi in case['permutations']:
            assert sorted(pi)==list(range(n));a={j for j in range(n) if pi[j] in a};sets.append(a);cost.append(boundary(a,n))
        assert cost==case['boundary_costs']
        assert all(mask_set(n,m)==aset for m,aset in zip(case['mask_path'],sets))
        bound=sum(r*d for r,d in zip(case['orders'],cost));assert bound==case['bound']<n//2
        rows=[i for i in range(n) if i not in a];checked=[]
        for witness in case['modular']:
            p=witness['prime'];w=witness['primitive_root'];assert prime_by_trial_division(p)
            assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
            mat=[[pow(w,i*j,p) for j in initial] for i in rows]
            det=Field(p).det(mat);assert det==witness['determinant']!=0
            checked.append({'prime':p,'determinant':det})
        out.append({'N':n,'name':case['name'],'boundary_costs':cost,'capacity':bound,'required_rank':n//2,'modular':checked})
    return out

def parity_and_twists():
    count=0;twisted=[]
    for k in range(1,11):
        n=1<<k
        for mask in range(1,n):assert boundary(mask_set(n,mask),n)==bformula(k,mask);count+=1
        reverse=lambda x:int(format(x,'0%db'%k)[::-1],2)
        rotate=lambda x:((x<<1)&(n-1))+(x>>(k-1))
        pi=[rotate(reverse(x)) for x in range(n)]
        assert all(pi[1<<j]==1<<((-j)%k) for j in range(k))
        m=k//2;mask=(1<<m) if k%2==0 else (1<<m)+(1<<(m+1))
        if k==1:mask=1
        a=mask_set(n,mask);assert {j for j in range(n) if pi[j] in a}==a
        d=boundary(a,n);assert d==((1<<m)-1 if k%2==0 else 1<<m)
        rank_controls=[]
        for p in (12289,65537):
            w=primitive(n,p);f=Field(p)
            if n<=256:
                col=sorted(a)
                # Both final signs, needed when a shuffle swaps the partition.
                for same in (False,True):
                    row=sorted(a if same else set(range(n))-a)
                    mat=[[pow(w,i*j,p) for j in col] for i in row]
                    assert f.rank(mat)==n//2
                rank_controls.append({'prime':p,'full_half_block_ranks':[n//2,n//2]})
            elif k%2==0:
                eta=pow(w,(1<<(m-1))**2,p)
                for rows in ([0,1],[2,3]):assert f.det([[pow(eta,i*j,p) for j in (0,1)] for i in rows])
                rank_controls.append({'prime':p,'proof_block_size':2,'both_partition_signs':'PASS'})
            else:
                eta=pow(w,(1<<(m-1))**2,p)
                for rows in ([0,1,6,7],[2,3,4,5]):assert f.det([[pow(eta,i*j,p) for j in (0,1,6,7)] for i in rows])
                rank_controls.append({'prime':p,'proof_block_size':4,'both_partition_signs':'PASS'})
        minimum=(n//2+d-1)//d;expected=((1<<(m-1))+1) if k%2==0 else 1<<m
        assert minimum==expected
        twisted.append({'k':k,'N':n,'invariant_mask':mask,'boundary':d,'necessary_depth':minimum,'rank_controls':rank_controls})
    return {'exhaustive_parity_masks':count,'twisted_controls':twisted}

def stage_products():
    p=65537;f=Field(p);rng=random.Random(70823);out=[]
    for trial in range(200):
        n=rng.randrange(2,13);t=rng.randrange(1,6);ranks=[rng.randrange(1,3) for _ in range(t)]
        a=set(rng.sample(range(n),rng.randrange(1,n)));initial=sorted(a);matrix=f.eye(n);bound=0
        for layer,r in enumerate(ranks):
            if layer:
                pi=rng.sample(range(n),n);matrix=[matrix[j] for j in pi];a={j for j in range(n) if pi[j] in a}
            factors=[[[rng.randrange(p) for _ in range(r)] for _ in range(n)] for _ in range(4)]
            stage=[[rng.randrange(p) if i==j else sum(factors[0 if i>j else 2][i][k]*factors[1 if i>j else 3][j][k] for k in range(r))%p for j in range(n)] for i in range(n)]
            matrix=f.mul(stage,matrix);bound+=r*boundary(a,n)
        cross=[[matrix[i][j] for j in initial] for i in range(n) if i not in a]
        actual=f.rank(cross);assert actual<=bound
        out.append({'N':n,'stages':t,'rank_orders':ranks,'cross_rank':actual,'moving_capacity':bound})
    return out

def survivor():
    k=8;n=1<<k;rng=random.Random(20261016+17*k);perms=[];columns=[]
    for stage in range(3):
        rows=[1<<i for i in range(k)]
        for _ in range(2*k*k):
            i,j=rng.sample(range(k),2)
            if rng.randrange(4)==0:rows[i],rows[j]=rows[j],rows[i]
            else:rows[i]^=rows[j]
        pi=[sum(((x&row).bit_count()%2)<<i for i,row in enumerate(rows)) for x in range(n)]
        assert sorted(pi)==list(range(n));perms.append(pi);columns.append([pi[1<<j] for j in range(k)])
    layout=list(range(n));edges=[]
    for stage in range(4):
        edges.extend(zip(layout[:-1],layout[1:]))
        if stage<3:layout=[layout[j] for j in perms[stage]]
    parity_caps=[]
    for m in range(1,n):
        cap=sum(((x&m).bit_count()%2)!=((y&m).bit_count()%2) for x,y in edges)
        assert cap>=n//2;parity_caps.append(cap)
    adj=[[] for _ in range(n)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    intervals=0;minimum_slack=n
    for lo in range(n):
        inside=set();cap=0
        for hi in range(lo,n):
            cap+=sum(-1 if v in inside else 1 for v in adj[hi]);inside.add(hi)
            if len(inside)==n:continue
            needed=min(len(inside),n-len(inside));assert cap>=needed
            minimum_slack=min(minimum_slack,cap-needed);intervals+=1
    assert intervals==32895
    return {'N':n,'seed':20261016,'shuffle_bit_columns':columns,'parity_masks':255,'minimum_parity_capacity':min(parity_caps),'consecutive_intervals':intervals,'minimum_interval_slack':minimum_slack,'scope':'Necessary moving-cut tests only; no coefficient fitting or network maxflow replication'}

if __name__=='__main__':
    result={'status':'PASS','certificates':certificates(),'parity_twist':parity_and_twists(),'stage_products':stage_products(),'survivor':survivor()}
    (BASE/'MOVING_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: 13 certificates, 26 saved determinants, 2036 masks, 10 twisted lengths, 200 stage products, 255 survivor masks and 32895 intervals')
