"""Newly authored exact comparison controls. Does not import research programs."""
from pathlib import Path
import hashlib
import itertools
import json

def rank(a, p):
    a = [list(r) for r in a]
    if not a or not a[0]: return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(row, len(a)) if a[j][col] % p), None)
        if pivot is None: continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, p)
        a[row] = [(v*inv) % p for v in a[row]]
        for j in range(len(a)):
            if j != row:
                q = a[j][col]
                a[j] = [(u-q*v) % p for u,v in zip(a[j],a[row])]
        row += 1
        if row == len(a): break
    return row

def product_roots(roots,p):
    a=[1]
    for z in roots:
        b=[0]*(len(a)+1)
        for j,v in enumerate(a):
            b[j]=(b[j]-z*v)%p
            b[j+1]=(b[j+1]+v)%p
        a=b
    return a

def evaluate(a,z,p):
    q=0
    for v in a[::-1]: q=(q*z+v)%p
    return q

configs=[(5,4,2),(97,12,3),(17,16,4),(97,24,4),(193,32,4),(97,48,6),(193,64,8)]
checks=0; recurrence_coordinates=0; raw_coordinates=0; rank_checks=0
families=[]
for p,Q,M in configs:
    K=Q//M
    zeta=next(z for z in range(1,p) if pow(z,Q,p)==1 and all(pow(z,k,p)!=1 for k in range(1,Q)))
    xi=pow(zeta,K,p)
    a=1; beta=1
    for r in sorted({0,1,min(2,M),M}):
        S=list(range(r))
        for mode in ['dense','disjoint','late']:
            D=[[0]*M for _ in range(K)]
            for j in S:
                if mode=='dense':
                    for b in range(K): D[b][j]=(1+b+j)%p or 1
                elif mode=='disjoint': D[j%K][j]=j+1
                else: D[K-1][j]=j+1
            x=[]; y=[]
            invM=pow(M,-1,p)
            for b in range(K):
                row=[]
                for t in range(M):
                    v=sum(D[b][j]*pow(xi,(-j*t)%M,p) for j in S)*invM%p
                    s=pow(zeta,(a*t*(t-1)//2+(a*M*b+beta)*t)%Q,p)
                    x.append(v*pow(s,-1,p)%p)
                    row.append(v)
                y.append(row)
            recovered=[]
            for b in range(K):
                row=[]
                for j in range(M):
                    row.append(sum(y[b][t]*pow(xi,j*t,p) for t in range(M))%p)
                recovered.append(row)
            assert recovered==D
            union=[j for j in range(M) if any(D[b][j] for b in range(K))]
            assert union==S
            nodes=[pow(xi,(-j)%M,p) for j in S]
            A=product_roots(nodes,p)
            assert [j for j in range(M) if evaluate(A,pow(xi,(-j)%M,p),p)==0]==S
            for b in range(K):
                for t in range(2*M):
                    assert sum(A[j]*y[b][(t+j)%M] for j in range(len(A)))%p==0
                    recurrence_coordinates+=1
            H=[[y[b][(i+j)%M] for j in range(r)] for b in range(K) for i in range(r)]
            assert rank(H,p)==r
            rank_checks+=1
            for b in range(K):
                for t in range(M):
                    s=pow(zeta,(a*t*(t-1)//2+(a*M*b+beta)*t)%Q,p)
                    assert s*x[b*M+t]%p==y[b][t]
                    raw_coordinates+=1
            families.append({'p':p,'Q':Q,'K':K,'M':M,'r':r,'coefficient_layout':mode})
            checks+=1

# A scalar projection may annihilate a nonzero common-support vector.
p=17; M=4; K=4; xi=4; active=1
D=[[0]*M for _ in range(K)]; D[0][active]=1; D[1][active]=p-1
assert any(D[b][active] for b in range(K))
assert all(sum(D[b][active]*pow(xi,(-active*t)%M,p) for b in range(K))%p==0 for t in range(M))
# Reverse-polynomial roots must be inverted, not silently copied.
z=pow(xi,-1,p); A=[-z%p,1]; q=[1,-z%p]
assert evaluate(A,z,p)==0 and evaluate(q,pow(z,-1,p),p)==0
assert evaluate(q,z,p)!=0
result={'status':'PASS','purpose':'new common-support comparison identities only; no rerun of accepted Green/recognition gates','cases':checks,'joint_rank_checks':rank_checks,'recurrence_coordinate_checks':recurrence_coordinates,'dechirped_raw_coordinate_checks':raw_coordinates,'scalar_projection_cancellation_control':'PASS','forward_reciprocal_root_orientation_control':'PASS','full_support_periodic_extension_control':'PASS','zero_and_late_and_disjoint_support_controls':'PASS','configurations':configs,'families':families,'historical_programs_executed':False,'production_or_runtime_certificate':False}
root=Path(__file__).resolve().parent
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('families',)},indent=2))
