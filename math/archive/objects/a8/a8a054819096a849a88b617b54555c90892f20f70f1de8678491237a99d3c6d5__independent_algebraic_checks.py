"""Newly authored audit. Uploaded Python is never imported or executed.
All matrix arithmetic below is exact prime-field arithmetic; certificate JSON
is read solely as data. Formulae are rebuilt from the stated matrix model.
"""
import json, random, hashlib, argparse
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent / 'source_material' / 'algebraic'
OUT = Path(__file__).resolve().parent
P = 12289
PERM = [7,0,6,3,4,1,2,5]

def rr(A,p,with_transform=False):
    A=np.asarray(A,dtype=np.int64).copy()%p
    nr,nc=A.shape; T=np.eye(nr,dtype=np.int64); piv=[]; r=0
    for c in range(nc):
        if r==nr: break
        q=next((k for k in range(r,nr) if A[k,c]),None)
        if q is None: continue
        A[[r,q]]=A[[q,r]]; T[[r,q]]=T[[q,r]]
        z=pow(int(A[r,c]),-1,p); A[r]=A[r]*z%p; T[r]=T[r]*z%p
        for i in range(nr):
            if i!=r and A[i,c]:
                z=int(A[i,c]); A[i]=(A[i]-z*A[r])%p; T[i]=(T[i]-z*T[r])%p
        piv.append(c); r+=1
    return A,piv,T

def rank(A,p=P): return len(rr(A,p)[1])
def inv(A,p):
    R,cols,T=rr(A,p)
    assert cols==list(range(len(A)))
    return T

def det(A,p):
    a=np.asarray(A,dtype=np.int64).copy()%p; v=1
    for c in range(len(a)):
        k=next((i for i in range(c,len(a)) if a[i,c]),None)
        if k is None:return 0
        if k!=c: a[[c,k]]=a[[k,c]];v=-v
        z=int(a[c,c]);v=v*z%p
        a[c]=a[c]*pow(z,-1,p)%p
        for i in range(c+1,len(a)):
            a[i]=(a[i]-int(a[i,c])*a[c])%p
    return v%p

def seed_point(n,r,seed=1011,p=P):
    rng=random.Random(seed); pts=[]
    for _ in range(2):
        groups={k:np.array([[rng.randrange(1,p) for _ in range(r)] for _ in range(n)],dtype=np.int64) for k in ('L','V','U','W')}
        d=np.array([rng.randrange(1,p) for _ in range(n)],dtype=np.int64)
        pts.append(np.concatenate([d]+[groups[k].ravel() for k in ('L','V','U','W')]))
    return np.concatenate(pts)

def stage(x,n,r,p):
    d=x[:n]; off=n; g=[]
    for _ in range(4):g.append(x[off:off+n*r].reshape(n,r));off+=n*r
    L,V,U,W=g
    return (np.diag(d)+np.tril(L@V.T,-1)+np.triu(U@W.T,1))%p

def value(x,n=8,r=1,perm=PERM,p=P):
    k=n*(1+4*r)
    return stage(x[k:],n,r,p)@stage(x[:k],n,r,p)[perm]%p

def jacobian(x,n=8,r=1,perm=PERM,p=P):
    # Each scalar coordinate occurs at most linearly, so difference is exact.
    base=value(x,n,r,perm,p); cols=[]
    for k in range(len(x)):
        y=x.copy();y[k]+=1
        cols.append((value(y,n,r,perm,p)-base).ravel()%p)
    return np.array(cols,dtype=np.int64).T

def stage_derivative(x,u):
    d,L,V,U,W=x.reshape(5,8);dd,l,v,q,w=u.reshape(5,8)
    return (np.diag(dd)+np.tril(np.outer(l,V)+np.outer(L,v),-1)+np.triu(np.outer(q,W)+np.outer(U,w),1))%P

def stage_hessian(u,v):
    _,l1,v1,u1,w1=u.reshape(5,8);_,l2,v2,u2,w2=v.reshape(5,8)
    return (np.tril(np.outer(l1,v2)+np.outer(l2,v1),-1)+np.triu(np.outer(u1,w2)+np.outer(u2,w1),1))%P

def hessian(x,u,v):
    a,b=x[:40],x[40:]; ua,ub=u[:40],u[40:];va,vb=v[:40],v[40:]
    A=stage(a,8,1,P); B=stage(b,8,1,P)
    return (stage_hessian(ub,vb)@A[PERM]+stage_derivative(b,ub)@stage_derivative(a,va)[PERM]+stage_derivative(b,vb)@stage_derivative(a,ua)[PERM]+B@stage_hessian(ua,va)[PERM]).ravel()%P

def gauges(x):
    out=[]
    for offset in (0,40):
        for k in (8,23,31,32):
            g=np.zeros(80,dtype=np.int64);g[offset+k]=1;out.append(g)
        for lo,hi in ((8,16),(24,32)):
            g=np.zeros(80,dtype=np.int64);g[offset+lo:offset+lo+8]=x[offset+lo:offset+lo+8];g[offset+hi:offset+hi+8]=-x[offset+hi:offset+hi+8];out.append(g)
    for k in range(8):
        g=np.zeros(80,dtype=np.int64);q=PERM.index(k)
        for off in (0,8,24):g[off+k]=x[off+k]
        for off in (0,16,32):g[40+off+q]=-x[40+off+q]
        out.append(g)
    return np.array(out).T%P

def curvature_check():
    x=seed_point(8,1);J=jacobian(x);R,cols,T=rr(J,P);Q=T[len(cols):]
    E=np.zeros(64,dtype=np.int64);E[7]=1
    aug=np.column_stack((J,E));cert=json.loads((ROOT/'curvature_minor_certificate.json').read_text())
    cd=det(aug[np.ix_(cert['minor_rows'],cert['minor_columns'])],P)
    assert len(cols)==60 and rank(aug)==61 and cd==6913
    G=gauges(x);assert rank(G)==20 and not np.any(J@G%P)
    # Universally cover all first tangents v against all 20 gauge generators.
    eye=np.eye(80,dtype=np.int64)
    for i in range(80):
        for k in range(20):assert not np.any(Q@hessian(x,eye[i],G[:,k])%P)
    v=eye[7]+eye[40];assert np.array_equal(hessian(x,v,v)*pow(2,-1,P)%P,E)
    assert np.any(Q@E%P)
    def solve(y):
        z=T@y%P
        if np.any(z[60:]):return None
        u=np.zeros(80,dtype=np.int64);u[cols]=z[:60]
        assert np.array_equal(J@u%P,y%P)
        return u
    def accept(d1,d2):
        u=solve(d1)
        return u is not None and solve((d2-hessian(x,u,u)*pow(2,-1,P))%P) is not None
    assert not accept(J@v%P,np.zeros(64,dtype=np.int64)) and accept(J@v%P,E)
    rng=random.Random(910)
    VI=inv(np.array([[pow(t,k,P) for k in range(5)] for t in range(5)],dtype=np.int64),P)
    for _ in range(20):
        u=np.array([rng.randrange(P) for _ in x],dtype=np.int64);w=np.array([rng.randrange(P) for _ in x],dtype=np.int64)
        d1=J@u%P;d2=(J@w+hessian(x,u,u)*pow(2,-1,P))%P
        assert accept(d1,d2)
        ys=np.array([value((x+t*u)%P).ravel() for t in range(5)])
        coeff=VI@ys%P
        assert np.array_equal(coeff[1],d1)
        assert np.array_equal(coeff[2],hessian(x,u,u)*pow(2,-1,P)%P)
    return {'jacobian_rank':60,'augmented_rank':61,'saved_minor_determinant':cd,'independent_gauge_rank':20,'all_1600_coordinate_gauge_Hessian_conormal_pairings_zero':True,'realized_jets_accepted':20,'independent_degree_four_interpolations':20,'straight_line_rejected_corrected_curve_accepted':True,'nonzero_conormal_E':(Q@E%P).tolist(),'point_integer_coordinates_d_L_V_U_W':x.tolist()}

def identities(B,p):
    a=[(int(B[i,j])*int(B[7,0])-int(B[i,0])*int(B[7,j]))%p for i in range(2,7) for j in range(1,i)]
    b=[(int(B[i,j])*int(B[0,7])-int(B[i,7])*int(B[0,j]))%p for i in range(1,6) for j in range(i+1,7)]
    return np.array(a+b,dtype=np.int64)

def normalized_stage(rng,p,fix_diag):
    d=[1]*8 if fix_diag else [rng.randrange(1,p) for _ in range(8)]
    L=[0]+[rng.randrange(1,p) for _ in range(6)]+[1];V=[rng.randrange(1,p) for _ in range(7)]+[0]
    U=[1]+[rng.randrange(1,p) for _ in range(6)]+[0];W=[0]+[rng.randrange(1,p) for _ in range(7)]
    return stage(np.array(d+L+V+U+W,dtype=np.int64),8,1,p)

def root(n,p):
    for g in range(2,p):
        z=pow(g,(p-1)//n,p)
        if pow(z,n,p)==1 and pow(z,n//2,p)!=1:return z
    raise AssertionError

def elimination_checks():
    records=[]
    for p in (12289,65537):
        rng=random.Random(614122+p);passes=0;random_failures=0;breaks=0;z=root(8,p)
        F=np.array([[pow(z,i*j,p) for j in range(8)] for i in range(8)],dtype=np.int64)
        for _ in range(30):
            A=normalized_stage(rng,p,True);B=normalized_stage(rng,p,False);PA=A[PERM];d=det(PA,p)
            if not d:continue
            M=B@PA%p;I=inv(PA,p);rec=M@I%p
            assert np.array_equal(rec,B) and not np.any(identities(rec,p))
            G=M@(d*I%p)%p;assert np.array_equal(identities(G,p),identities(B,p)*(d*d%p)%p)
            L=rec[:,0]*pow(int(rec[7,0]),-1,p)%p;V=rec[7,:];U=rec[:,7]*pow(int(rec[0,7]),-1,p)%p;W=rec[0,:]
            got=(np.diag(np.diag(rec))+np.tril(np.outer(L,V),-1)+np.triu(np.outer(U,W),1))%p
            assert np.array_equal(got,rec);passes+=1
            for i,j in [(i,j) for i in range(2,7) for j in range(1,i)]+[(i,j) for i in range(1,6) for j in range(i+1,7)]:
                bad=B.copy();bad[i,j]=(bad[i,j]+1)%p
                assert np.count_nonzero(identities(bad,p))==1;breaks+=1
            if np.any(identities(F@I%p,p)):random_failures+=1
        records.append({'prime':p,'positive_products_and_exact_reconstructions':passes,'single_equation_mutation_checks':breaks,'random_A_failures_for_F8_not_nonexistence_evidence':random_failures})
    return records

def ct_checks():
    saved=json.loads((ROOT/'ct_control_results.json').read_text()); out=[]
    for row in saved['results']:
        a,b=row['radix_pair'];n=a*b;z=root(n,P)
        # Derive factors from input/output labels, independently of source loops.
        io=row['input_order'];oo=row['output_order'];pm=row['middle_shuffle']
        oa=[0,1] if a==2 else [0,2,1,3]
        ob=[0,2,1,3] if b==4 else list(range(b))
        A=np.zeros((n,n),dtype=np.int64);B=np.zeros_like(A)
        for rowi in range(n):
            block,v=divmod(rowi,b)
            for coli,j in enumerate(io):
                if j%a==block:A[rowi,coli]=pow(z,a*ob[v]*(j//a),P)
        for rowi,k in enumerate(oo):
            k2=k%b;k1=k//b
            for coli in range(n):
                cb,u=divmod(coli,a)
                if cb==k2:B[rowi,coli]=pow(z,oa[u]*(k2+b*k1),P)
        F=np.array([[pow(z,k*j,P) for j in io] for k in oo],dtype=np.int64)
        assert np.array_equal(B@A[pm]%P,F)
        def order(S):return max(rank(S[:k,k:]) for k in range(1,n)),max(rank(S[k:,:k]) for k in range(1,n))
        ao,bo=order(A),order(B)
        assert max(ao)==row['rank_stage_1'] and max(bo)==row['rank_stage_2']
        if n==16:assert A[1,0]==A[5,4]==1 and A[5,0]==0
        out.append({'n':n,'all_entries_equal':True,'A_upper_lower_orders':ao,'B_upper_lower_orders':bo})
    # Exact characteristic-zero F4 cut-2 blocks under [0,2,1,3]:
    # [[1,1],[-1,-1]] and [[1,-1],[1,-1]], both rank one.
    return out

def large_checks():
    saved=json.loads((ROOT/'large_curvature_results.json').read_text());out=[]
    for row in saved:
        pm=row['perm'];J=jacobian(seed_point(16,2),16,2,pm);R,cols,T=rr(J,P);rk=len(cols);Q=T[rk:]
        assert rk==row['jacobian_rank'];assert all(np.any(Q[:,i*16+pm[i]]) for i in range(16))
        out.append({'n':16,'r':2,'rank':rk,'all_16_diagonal_quadratic_terms_transverse_mod_p':True,'permutation':pm})
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir','--source',dest='source',type=Path,default=ROOT,help='Directory containing the three certificate JSON files; read only')
    parser.add_argument('--output',type=Path,default=OUT,help='Directory for independent results JSON')
    args=parser.parse_args();ROOT=args.source.resolve();OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
    result={}
    for name,f in [('curvature',curvature_check),('elimination',elimination_checks),('ct_controls',ct_checks),('larger_pointwise_checks',large_checks)]:
        result[name]=f();print(name, 'PASS',flush=True)
    (OUT/'independent_algebraic_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='curvature'},indent=2))
