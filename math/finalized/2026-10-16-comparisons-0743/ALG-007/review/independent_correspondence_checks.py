"""Fresh finite algebra checks, not execution of any supplied research code."""
import itertools
import json
from pathlib import Path

def rank(a, p):
    a = [list(row) for row in a]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        k = next((k for k in range(pivot, len(a)) if a[k][col] % p), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        inv = pow(a[pivot][col], -1, p)
        a[pivot] = [v * inv % p for v in a[pivot]]
        for row in range(len(a)):
            if row != pivot:
                scale = a[row][col]
                a[row] = [(v-scale*w) % p for v,w in zip(a[row], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot

def root_of_order(p, q):
    return next(z for z in range(2,p) if pow(z,q,p)==1 and all(pow(z,d,p)!=1 for d in range(1,q) if q%d==0))

def polynomial_product_roots(roots,p):
    a=[1]
    for root in roots:
        nxt=[0]*(len(a)+1)
        for j,v in enumerate(a):
            nxt[j]=(nxt[j]-root*v)%p
            nxt[j+1]=(nxt[j+1]+v)%p
        a=nxt
    return a

records=[]
for p,q,k,m in [(17,16,4,4),(97,12,4,3),(97,24,6,4),(97,32,8,4)]:
    z=root_of_order(p,q)
    xi=pow(z,k,p)
    for support_size in range(m+1):
        for support in itertools.combinations(range(m), support_size):
            for mode in ['all_blocks','one_block_only','disjoint_blocks','late_only']:
                c=[[0]*m for _ in range(k)]
                for u in support:
                    for b in range(k):
                        if mode=='all_blocks' or (mode=='one_block_only' and b==0) or (mode=='disjoint_blocks' and b==u%k) or (mode=='late_only' and b==k-1):
                            c[b][u]=(b+u+1) % (p-1)+1
                y=[[sum(c[b][u]*pow(xi,(-u*t)%m,p) for u in range(m))%p for t in range(m)] for b in range(k)]
                slope=next(a for a in range(1,q) if all(a%d for d in range(2,q+1) if q%d==0))
                beta=3
                raw=[]
                for b in range(k):
                    for t in range(m):
                        chirp=pow(z,(slope*t*(t-1)//2+(slope*m*b+beta)*t)%q,p)
                        raw.append(y[b][t]*pow(chirp,-1,p)%p)
                recovered=[]
                for b in range(k):
                    row=[]
                    for u in range(m):
                        val=0
                        for t in range(m):
                            chirp=pow(z,(slope*t*(t-1)//2+(slope*m*b+beta)*t)%q,p)
                            val+=chirp*raw[b*m+t]*pow(xi,u*t,p)
                        row.append(val*pow(m,-1,p)%p)
                    recovered.append(row)
                assert recovered==c
                roots=[pow(xi,(-u)%m,p) for u in support]
                a=polynomial_product_roots(roots,p)
                assert all(sum(a[j]*y[b][(t+j)%m] for j in range(len(a)))%p==0 for b in range(k) for t in range(m))
                h=[[y[b][(t+j)%m] for j in range(support_size)] for b in range(k) for t in range(support_size)]
                observed=rank(h,p) if support_size else 0
                assert observed==support_size
                records.append({'p':p,'Q':q,'K':k,'M':m,'support':list(support),'coefficient_pattern':mode,'joint_rank':observed})

# A scalar projection can lose a mode that remains active in the vector sequence.
p,q,k,m=17,16,4,4
z=root_of_order(p,q); xi=pow(z,k,p)
c=[1,p-1,0,0]
assert any(c) and sum(c)%p==0
cancellation={'p':p,'Q':q,'K':k,'M':m,'mode':1,'coefficient_vector':c,'sum_projection':0}

result={'verdict':'PASS','cases':len(records),'checks':['exact dechirp/polynomial coefficient correspondence','forward annihilator on every coordinate, including periodic wrap','joint minimality rank with disjoint, late-only, or missing block supports','full-support endpoint','scalar projection cancellation control'],'cases_detail':records,'cancellation_control':cancellation,'limitations':'Finite controls only; no imported research program, optimization benchmark, new global complexity proof, production certification, or historical priority claim.'}
Path(__file__).with_name('INDEPENDENT_CORRESPONDENCE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':'PASS','cases':len(records)}))
