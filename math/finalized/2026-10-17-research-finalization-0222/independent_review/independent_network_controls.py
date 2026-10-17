"""Independently authored formulas and analytic Jacobian, inert candidate JSON only."""
import json,itertools,math,hashlib
from pathlib import Path
PTH=Path(__file__).with_name('NETWORK_WITNESS.json')
doc=json.loads(PTH.read_text());n=doc['n'];p=doc['prime'];params=doc['parameters'];perm=doc['permutation']
assert p>2 and all(p%d for d in range(2,math.isqrt(p)+1))

def stage(v):
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            out[i][j]=v[i] if i==j else v[n+i]*v[2*n+j] if i>j else v[3*n+i]*v[4*n+j]
    return out

def dstage(v,q):
    out=[[0]*n for _ in range(n)];block,pos=divmod(q,n)
    for i in range(n):
        for j in range(n):
            if i==j: out[i][j]=int(block==0 and pos==i)
            elif i>j:
                out[i][j]=(v[2*n+j] if block==1 and pos==i else 0)+(v[n+i] if block==2 and pos==j else 0)
            else:
                out[i][j]=(v[4*n+j] if block==3 and pos==i else 0)+(v[3*n+i] if block==4 and pos==j else 0)
    return out

def mult(X,Y):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*Y)] for r in X]

def det(X):
    X=[[z%p for z in r] for r in X];ans=1
    for k in range(len(X)):
        q=next((i for i in range(k,len(X)) if X[i][k]),None)
        if q is None:return 0
        if k!=q: X[k],X[q]=X[q],X[k];ans=-ans
        z=X[k][k];ans=ans*z%p; inv=pow(z,p-2,p)
        # Normalize pivot row; row additions preserve determinant.
        X[k]=[z*inv%p for z in X[k]]
        for i in range(k+1,len(X)):
            factor=X[i][k];X[i]=[(a-factor*b)%p for a,b in zip(X[i],X[k])]
    return ans%p
A=stage(params[:5*n]);B=stage(params[5*n:]);BP=[[row[perm[k]] for k in range(n)] for row in B];W=mult(BP,A)
assert W==doc['integer_matrix']; assert det(A) and det(B)
minor_records=[]
for k in range(1,n+1):
    count=0;bad=0
    for rr in itertools.combinations(range(n),k):
        for cc in itertools.combinations(range(n),k):
            bad+=not bool(det([[W[i][j] for j in cc] for i in rr]));count+=1
    assert not bad;minor_records.append({'order':k,'count':count,'zero_count':bad})
derivs=[]
for q in range(10*n):
    if q<5*n:V=mult(BP,dstage(params[:5*n],q))
    else:
        D=dstage(params[5*n:],q-5*n);DP=[[row[perm[k]] for k in range(n)] for row in D];V=mult(DP,A)
    derivs.append([z for row in V for z in row])
J=list(map(list,zip(*derivs)))
rr=doc['jacobian_minor_rows'];cc=doc['jacobian_minor_columns'];assert len(rr)==len(cc)==60
v=det([[J[i][j] for j in cc] for i in rr]);assert v==doc['jacobian_minor_determinant_mod_prime']==696549753
res={'candidate_data_sha256':hashlib.sha256(PTH.read_bytes()).hexdigest(),'integer_product_reproduced':True,'stage_determinants_nonzero':True,'prime_verified_by_trial_division':p,'minors':minor_records,'total_square_minors':sum(x['count'] for x in minor_records),'analytic_jacobian_60_minor':v,'jacobian_rank_at_least':60,'dimension_upper_bound':'60 from 5n-6=34 dimensions per stage and n=8 intermediate diagonal gauges; established in written proof, not rank modulo p.'}
Path(__file__).with_name('INDEPENDENT_NETWORK_RESULTS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
