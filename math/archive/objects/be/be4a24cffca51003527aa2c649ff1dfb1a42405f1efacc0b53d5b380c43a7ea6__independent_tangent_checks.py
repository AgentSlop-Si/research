"""Own exact reconstruction of the N16 finite-field tangent proof object.
Only JSON data and our independently authored flow routines are read.
"""
from pathlib import Path
import json, random
import numpy as np
from independent_nonlinear_checks import Flow, network

ROOT=Path(__file__).resolve().parent
SOURCE = ROOT / 'nonlinear_tangent_certificate_N16.json'
cert=json.loads(SOURCE.read_text())
n,r,p=cert['n'],cert['rank_per_stage'],cert['modulus']
perm=cert['shuffle']

def reduce(a):
    a=np.array(a,dtype=np.int64,copy=True)%p
    pivots=[]; row=0
    for c in range(a.shape[1]):
        if row==len(a): break
        nz=np.flatnonzero(a[row:,c])
        if not len(nz): continue
        k=row+int(nz[0]); a[[row,k]]=a[[k,row]]
        a[row]=(a[row]*pow(int(a[row,c]),-1,p))%p
        ids=np.flatnonzero(a[:,c]); ids=ids[ids!=row]
        if len(ids): a[ids]=(a[ids]-a[ids,c,None]*a[row])%p
        pivots.append(c); row+=1
    return a,pivots

def kernel(a):
    red,piv=reduce(a)
    out=[]
    for j in range(red.shape[1]):
        if j in piv: continue
        v=np.zeros(red.shape[1],dtype=np.int64);v[j]=1
        for row,c in enumerate(piv): v[c]=-red[row,j]%p
        assert not np.any(a@v%p)
        out.append(v)
    return out

rng=random.Random(cert['generator_seed'])
def params():
    arrays=[np.array([[rng.randrange(1,p) for a in range(r)] for i in range(n)],dtype=np.int64) for z in range(4)]
    arrays.append(np.array([rng.randrange(1,p) for i in range(n)],dtype=np.int64))
    return arrays

def matrix(q):
    l,v,u,w,d=q
    return (np.tril(l@v.T,-1)+np.triu(u@w.T,1)+np.diag(d))%p

def derivs(q):
    for i in range(n):
        a=np.zeros((n,n),dtype=np.int64);a[i,i]=1;yield a
    for typ in range(4):
        for i in range(n):
            for lane in range(r):
                a=np.zeros((n,n),dtype=np.int64)
                if typ==0: a[i,:i]=q[1][:i,lane]
                if typ==1: a[i+1:,i]=q[0][i+1:,lane]
                if typ==2: a[i,i+1:]=q[3][i+1:,lane]
                if typ==3: a[:i,i]=q[2][:i,lane]
                yield a

aa,bb=params(),params();a,b=matrix(aa),matrix(bb)
pa=a[perm,:];m=b@pa%p
columns=[(b@da[perm,:]%p).ravel() for da in derivs(aa)]
columns += [(db@pa%p).ravel() for db in derivs(bb)]
j=np.stack(columns,axis=1)
rank_j=len(reduce(j)[1]); assert rank_j==232

edges,ids,src,sink=network(n,r,perm)
tangent=[]
for entry in cert['unique_nontrivial_cut_rectangles']:
    rows,cols=entry['R'],entry['C']
    e=edges+[(src,ids[0,'x',c,0],n+1) for c in cols]+[(ids[1,'y',rr,1],sink,n+1) for rr in rows]
    bound=Flow(len(ids),e).value(src,sink)
    block=m[np.ix_(rows,cols)]
    assert bound==entry['bound']==len(reduce(block)[1])
    for left in kernel(block.T):
        for right in kernel(block):
            g=np.zeros((n,n),dtype=np.int64)
            g[np.ix_(rows,cols)]=np.outer(left,right)%p
            tangent.append(g.ravel())
g=np.stack(tangent)
delta=np.zeros(n*n,dtype=np.int64)
for k,v in cert['delta_sparse_flattened'].items(): delta[int(k)]=v
q=np.array(cert['normal_vector_flattened'],dtype=np.int64)
rank_g=len(reduce(g)[1]); assert rank_g==14
assert not np.any(g@j%p)
assert not np.any(g@delta%p)
assert not np.any(q@j%p)
pairing=int(q@delta%p);assert pairing==4599
result={'uploaded_code_executed':False,'field_prime':p,'jacobian_shape':list(j.shape),'jacobian_rank':rank_j,'saved_rectangles_recomputed':len(cert['unique_nontrivial_cut_rectangles']),'cut_tangent_rows':len(g),'cut_tangent_rank':rank_g,'q_dot_delta':pairing,'delta_support':cert['delta_sparse_flattened'],'checks':['all saved graph capacities','all saved block ranks','G J = 0','G delta = 0','q J = 0','q delta = 4599'],'scope':'35 saved rectangles; the original 20000-query sampling sequence was not rerun; finite-field first-order statement only'}
(ROOT/'independent_tangent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
