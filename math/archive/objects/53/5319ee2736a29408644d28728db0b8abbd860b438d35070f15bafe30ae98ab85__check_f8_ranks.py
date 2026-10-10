# Independently written audit code. Never imports or executes supplied package.
from itertools import combinations
from pathlib import Path
import hashlib,json

def rank(a,p):
    a=[list(row) for row in a]; r=0
    if not a:return 0
    for j in range(len(a[0])):
        piv=next((i for i in range(r,len(a)) if a[i][j]%p),None)
        if piv is None:continue
        a[r],a[piv]=a[piv],a[r]
        c=pow(a[r][j]%p,-1,p)
        a[r]=[x*c%p for x in a[r]]
        for i in range(r+1,len(a)):
            c=a[i][j]%p
            a[i]=[(x-c*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
out={'hashes':{},'fields':[]}
for p,g in ((998244353,3),(2013265921,31)):
    w=pow(g,(p-1)//8,p);assert pow(w,4,p)==p-1
    F=[[pow(w,i*j,p) for j in range(8)] for i in range(8)]
    counts={}
    for rr in combinations(range(8),3):
        for cc in combinations(range(8),5):
            r=rank([[F[i][j] for j in cc] for i in rr],p)
            counts[r]=counts.get(r,0)+1
    assert counts=={3:3136}
    rec={'p':p,'rank_3x5_inventory':counts,'orders':{}}
    for name,rr,cc in [('natural',list(range(8)),list(range(8))),('parity',[0,2,4,6,1,3,5,7],[0,2,4,6,1,3,5,7]),('package_dp',[0,1,2,4,3,5,6,7],[0,1,4,5,2,3,6,7])]:
        M=[[F[i][j] for j in cc] for i in rr]
        ranks=[[rank([row[s:] for row in M[:s]],p),rank([row[:s] for row in M[s:]],p)] for s in range(1,8)]
        overlaps=[rank([row[:s] for row in M[s+1:]],p) for s in range(1,7)]
        rec['orders'][name]={'ranks':ranks,'lower_overlap_ranks':overlaps}
    out['fields'].append(rec)
Path(__file__).with_name('f8_rank_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
