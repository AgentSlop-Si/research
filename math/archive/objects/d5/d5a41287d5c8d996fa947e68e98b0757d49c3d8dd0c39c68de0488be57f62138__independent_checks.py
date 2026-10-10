#!/usr/bin/env python3
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,hashlib
import sympy as s
HERE=Path(__file__).resolve().parent
SRC=HERE.parent.parent/'joint_orbit/iteration_7_balanced_routes/BALANCED_SUPPORT.json'

def counted_route(M):
    # Explicit O(N) stable integer counting sort; no comparison sorting.
    N=M*M;areas=[(i//M+1)*(i%M+1) for i in range(N)]
    count=[0]*(N+1)
    for a in areas:count[a]+=1
    start=[0]*(N+1);total=0
    for a in range(1,N+1):start[a]=total;total+=count[a]
    pos=start[:];order=[0]*N
    for i,a in enumerate(areas):order[pos[a]]=i;pos[a]+=1
    sigma=[0]*N
    for r,i in enumerate(order):sigma[i]=order[N-1-r]
    assert all(sigma[sigma[i]]==i for i in range(N))
    return areas,sigma

source=json.loads(SRC.read_text());controls=[]
for orig in source:
    M=orig['M'];N=M*M;area,sigma=counted_route(M)
    rows=[]
    for i,j in enumerate(sigma):
        x,y=i//M+1,i%M+1;u,v=j//M+1,j%M+1
        A=area[i];B=area[j];I=max(0,x+u-M)*max(0,y+v-M)
        union=A+B-I;diff=A+B-2*I
        assert I*N<=A*B
        if M>=4:assert max(A,B)*8>=N and min(A,B)*2<=N and diff*8>=N
        rows.append((union,diff,A,B,i,j))
    assert min(r[0] for r in rows)==orig['min_union']
    assert min(r[1] for r in rows)==orig['min_symmetric_difference']
    assert list(min(rows,key=lambda r:r[1]))==orig['minimum_symmetric_difference_witness']
    if orig['rowmap'] is not None:assert sigma==orig['rowmap']
    controls.append({'M':M,'N':N,'min_union':min(r[0] for r in rows),
                     'min_symmetric_difference':min(r[1] for r in rows),
                     'counting_sort_matches_source':True,'route_is_involution':True})

# Exact complete coupling/cancellation audit at M=4 over Q(zeta16).
z=s.symbols('z');phi=s.Poly(z**8+1,z,domain=s.QQ)
def reduce(e):return s.Poly(e,z,domain=s.QQ).rem(phi).as_expr()
def path(i,j,sign):
    t,u=divmod(i,4);tt,uu=divmod(j,4);dt=t-tt;du=u-uu
    if min(dt,du)<0:return s.Integer(0)
    out=0
    for vertical in combinations(range(dt+du),dt):
        vv=set(vertical);x=uu;exp=0
        for k in range(dt+du):
            if k in vv:exp+=x
            else:x+=1
        out+=z**((sign*exp)%16)
    return reduce(out)
Gp=[[path(i,j,1) for j in range(16)] for i in range(16)]
Gm=[[path(i,j,-1) for j in range(16)] for i in range(16)]
areas,sigma=counted_route(4)
J=[[Gm[sigma[i]][15-j] for j in range(16)] for i in range(16)]
rows=[]
for i in range(16):
    onlyG=[j for j in range(16) if Gp[i][j]!=0 and J[i][j]==0]
    onlyJ=[j for j in range(16) if J[i][j]!=0 and Gp[i][j]==0]
    both=[j for j in range(16) if Gp[i][j]!=0 and J[i][j]!=0]
    cancellation=Counter()
    for j in both:
        ratio=reduce(-Gp[i][j]*s.invert(J[i][j],phi.as_expr(),z))
        assert ratio!=0 and reduce(Gp[i][j]+ratio*J[i][j])==0
        cancellation[tuple(str(s.Poly(ratio,z).nth(k)) for k in range(8))]+=1
    largest=max(cancellation.values(),default=0)
    union=len(onlyG)+len(onlyJ)+len(both)
    minimum=union-largest
    assert minimum>=len(onlyG)+len(onlyJ)>=2
    rows.append({'row':i,'G_only':len(onlyG),'J_only':len(onlyJ),'overlap':len(both),
                 'maximum_simultaneous_cancellations':largest,'minimum_support_nonzero_couplings':minimum,
                 'support_alpha_zero':len(onlyJ)+len(both),'support_beta_zero':len(onlyG)+len(both),
                 'cancellation_ratio_multiplicities':[{'ratio_coefficients':list(k),'multiplicity':v} for k,v in cancellation.items()]})
result={'source':str(SRC.relative_to(HERE.parent.parent)),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'geometry_controls':controls,'N16_exact_coupling_rows':rows,
        'N16_minimum_support_alpha_beta_nonzero':min(r['minimum_support_nonzero_couplings'] for r in rows),
        'N16_minimum_support_alpha_zero':min(r['support_alpha_zero'] for r in rows),
        'N16_minimum_support_beta_zero':min(r['support_beta_zero'] for r in rows),
        'zero_pair_rank':0,
        'scope':'Uniform support for specified phase masks and alpha beta nonzero, not arbitrary independently changed masks and not Fourier compatibility.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='N16_exact_coupling_rows'},indent=2))
