#!/usr/bin/env python3
"""Fresh independent Phase 21 auditor. Does not import or execute submitted code.
Builds each Green matrix by dense inversion of I-diag(w)Q, not cycle application.
Only external data read: source JSON results, hashes, and selected minor indices.
"""
from pathlib import Path
import json, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
SRC=ROOT/"inputs"

def inv(a,p):
    n=len(a)
    aug=np.column_stack((np.array(a,dtype=np.int64)%p,np.eye(n,dtype=np.int64)))
    for c in range(n):
        choices=np.flatnonzero(aug[c:,c])
        if not len(choices): raise ValueError("singular")
        r=c+int(choices[0])
        aug[[c,r]]=aug[[r,c]]
        aug[c]=(aug[c]*pow(int(aug[c,c]),-1,p))%p
        factors=aug[:,c].copy(); factors[c]=0
        aug=(aug-factors[:,None]*aug[c])%p
    answer=aug[:,n:]
    assert np.array_equal((a@answer)%p,np.eye(n,dtype=np.int64))
    return answer

def rank_and_det(a,p):
    a=np.array(a,dtype=np.int64,copy=True)%p
    m,n=a.shape
    r=0;det=1
    for c in range(n):
        ix=np.flatnonzero(a[r:,c])
        if len(ix)==0: continue
        k=r+int(ix[0])
        if k!=r: a[[k,r]]=a[[r,k]];det=-det
        v=int(a[r,c]);det=det*v%p
        a[r,c:]=a[r,c:]*pow(v,-1,p)%p
        if r+1<m:
            f=a[r+1:,c].copy()
            a[r+1:,c:]=(a[r+1:,c:]-f[:,None]*a[r,c:])%p
        r+=1
        if r==m:break
    return r, (int(det) if m==n and r==n else 0)

def permutations(s):
    x=np.repeat(np.arange(s),s);y=np.tile(np.arange(s),s)
    return [((x+2*y)%s)*s+y,((x+2*y+1)%s)*s+y,x*s+(y+2*x)%s,x*s+(y+2*x+1)%s]

def green(q,w,p):
    a=np.eye(len(q),dtype=np.int64)
    a[np.arange(len(q)),q]-=w
    return inv(a%p,p)

def valid(q,w,p):
    unseen=set(range(len(q)))
    while unseen:
        start=min(unseen);t=start;prod=1
        while t in unseen:
            unseen.remove(t);prod=prod*int(w[t])%p;t=int(q[t])
        assert t==start
        if prod==1:return False
    return True

def baseline(s,seed=19,p=65537):
    qs=permutations(s);rng=np.random.default_rng(seed);ws=[];gs=[]
    for layer in range(2):
        wl=[];gl=[]
        for q in qs:
            while True:
                w=rng.integers(2,1024,size=s*s,dtype=np.int64)
                if valid(q,w,p):break
            wl.append(w);gl.append(green(q,w,p))
        ws.append(wl);gs.append(gl)
    alpha=pow(4,-1,p)
    ls=[sum(layer)*alpha%p for layer in gs]
    return qs,ws,gs,ls

def bridge_data(s,seed=19,p=65537):
    qs,ws,gs,ls=baseline(s,seed,p)
    H=gs[0][1];V=gs[1][3];B=H[qs[1]];C=(V@H%p)[qs[3]]
    return qs,ws,gs,ls,H,V,B,C

def normalize(e,V,B,C,p):
    z=(inv(V,p)@e)%p;z=(z@inv(B,p))%p
    keys=np.array([pow(int(c),-1,p) for c in C.flat],dtype=np.int64).reshape(C.shape)
    return ((z*16)%p)*keys%p

def hessian(s,seed=19,p=65537,explicit=False):
    qs,ws,gs,ls,H,V,B,C=bridge_data(s,seed,p)
    n=s*s;a=pow(16,-1,p)
    rv,dv=rank_and_det(V,p);rb,db=rank_and_det(B,p)
    d=pow(dv,n,p)*pow(db,n,p)%p
    for c in C.flat:d=d*(a*int(c)%p)%p
    result={"N":n,"p":p,"seed":seed,"bridge_nonzero":bool(np.all(C)),"formula_det":int(d)}
    assert d!=0 and np.all(C)
    if explicit:
        columns=[]
        for i in range(n):
            di=np.zeros((n,n),dtype=np.int64);di[i,qs[3][i]]=1
            dV=V@di%p@V%p
            for j in range(n):
                dj=np.zeros((n,n),dtype=np.int64);dj[j,qs[1][j]]=1
                dH=H@dj%p@H%p
                columns.append(((dV@dH%p)*a%p).ravel())
        K=np.column_stack(columns)
        rk,dk=rank_and_det(K,p)
        result.update(direct_rank=rk,direct_det=dk)
        assert dk==d and rk==n*n
    if p==65537:
        omega=pow(3,(p-1)//n,p)
        assert pow(omega,n,p)==1 and pow(omega,n//2,p)!=1
        F=np.array([[pow(omega,i*j,p) for j in range(n)]for i in range(n)],dtype=np.int64)
        E=(F-ls[1]@ls[0]%p)%p
        z=normalize(E,V,B,C,p)
        r,de=rank_and_det(z,p)
        result.update(normalized_fourier_error_rank=r,normalized_fourier_error_det=de)
        assert r==n
    return result

def finite(s,seed=29,dense=True,zero_horizontal=False):
    p=65537;n=s*s
    qs,ws,gs,ls,H,V,B,C=bridge_data(s,seed,p)
    a=pow(4,-1,p);aa=a*a%p
    rng=np.random.default_rng(211+s)
    dv=rng.integers(1,101,size=n,dtype=np.int64)
    dh=rng.integers(1,101,size=n,dtype=np.int64)
    if not dense:
        dv[:]=0;dh[:]=0;dv[3]=121;dv[9]=7;dh[5]=3;dh[10]=10
    if zero_horizontal:dh=(-ws[0][1])%p
    Hn=green(qs[1],(ws[0][1]+dh)%p,p)
    Vn=green(qs[3],(ws[1][3]+dv)%p,p)
    Lhn=(gs[0][0]+Hn+gs[0][2]+gs[0][3])*a%p
    Lvn=(gs[1][0]+gs[1][1]+gs[1][2]+Vn)*a%p
    T0=ls[1]@ls[0]%p
    Th=ls[1]@Lhn%p;Tv=Lvn@ls[0]%p;Tboth=Lvn@Lhn%p
    four=(Tboth-Th-Tv+T0)%p
    deltaH=(Hn-H)%p;deltaV=(Vn-V)%p
    mixed=(deltaV@deltaH%p)*aa%p
    assert np.array_equal(four,mixed)
    oneh=ls[1]@deltaH%p*a%p
    onev=deltaV@ls[0]%p*a%p
    assert np.array_equal((Tboth-T0)%p,(oneh+onev+mixed)%p)
    # Compute Q_H^{-1} via the explicitly built permutation matrix.
    Qh=np.eye(n,dtype=np.int64)[qs[1]]
    Qv=np.eye(n,dtype=np.int64)[qs[3]]
    core=inv(Vn,p)@(four*pow(aa,-1,p)%p)%p
    core=core@inv(H,p)%p@Qh.T%p
    Cp=Qv@V%p@Hn%p
    factorized=dv[:,None]*Cp%p*dh[None,:]%p
    assert np.array_equal(core,factorized)
    result={"N":n,"seed":seed,"four_point_identity":True,"full_edit_decomposition":True,
            "division_free_identity":True,"ordinary_mixed_rank":rank_and_det(mixed,p)[0],"C_prime_zero_entries":int(np.count_nonzero(Cp==0)),
            "edited_horizontal_all_zero":zero_horizontal}
    if np.all(Cp):
        reciprocals=np.array([pow(int(c),-1,p) for c in Cp.flat],dtype=np.int64).reshape(Cp.shape)
        z=core*reciprocals%p
        assert np.array_equal(z,dv[:,None]*dh[None,:]%p)
        result["normalized_mixed_rank"]=rank_and_det(z,p)[0]
    if not zero_horizontal:
        result["full_edit_rank_in_original_normalization"]=rank_and_det(normalize((Tboth-T0)%p,V,B,C,p),p)[0]
    return result

def jacobian():
    p=65537;s=8;n=64
    qs,ws,gs,ls=baseline(s,19,p)
    alpha=pow(4,-1,p)
    columns=[]
    for stage in range(2):
        for k in range(4):
            G=gs[stage][k]
            if stage==0:left=ls[1]@G%p;right=G
            else:left=G;right=G@ls[0]%p
            for i in range(n):
                columns.append(((left[:,i,None]*right[qs[k][i],None,:])%p*alpha%p).ravel())
    J=np.column_stack(columns)
    cert=json.loads((SRC/"N64_JACOBIAN_CERTIFICATE.json").read_text())
    rows=cert["selected_rows"];cols=cert["selected_columns"]
    assert len(rows)==len(set(rows))==504 and all(0<=r<n*n for r in rows)
    assert len(cols)==len(set(cols))==504 and all(0<=c<8*n for c in cols)
    rr,dd=rank_and_det(J[np.ix_(rows,cols)],p)
    assert rr==504 and dd==8439==cert["minor_det_mod_p"]
    groups=[]
    for stage in range(2):
        for i in range(n):
            fixed=[k for k,q in enumerate(qs) if q[i]==i]
            if len(fixed)>=2:
                assert len(fixed)==2
                a,b=fixed
                da=alpha*pow((1-int(ws[stage][a][i]))%p,-2,p)%p
                db=alpha*pow((1-int(ws[stage][b][i]))%p,-2,p)%p
                ca=(stage*4+a)*n+i;cb=(stage*4+b)*n+i
                assert np.all((J[:,ca]*db-J[:,cb]*da)%p==0)
                groups.append({"stage":stage,"vertex":i,"terms":fixed,"columns":[ca,cb]})
    assert len(groups)==8
    assert len({c for g in groups for c in g["columns"]})==16
    return {"N":64,"minor_rank":rr,"minor_det_mod_p":dd,"independent_null_directions":8,
            "exact_jacobian_rank":504,"null_groups":groups,"saved_minor_support_verified":True}

def main():
    output={"method":"Portable mathematical checker; original package integrity checks are recorded separately.",
            "hessian_and_fourier":[],"finite_edits":[]}
    for s in [2,4,8,16]:
        item=hessian(s,explicit=s<=4);output["hessian_and_fourier"].append(item);print(json.dumps(item),flush=True)
    output["second_field"]=hessian(4,seed=26,p=786433,explicit=True);print(json.dumps(output["second_field"]),flush=True)
    for s in [2,4,8]:
        item=finite(s);output["finite_edits"].append(item);print(json.dumps(item),flush=True)
    output["sparse_finite_edit"]=finite(4,seed=47,dense=False);print(json.dumps(output["sparse_finite_edit"]),flush=True)
    output["zero_weight_counterexample"]=finite(4,zero_horizontal=True);print(json.dumps(output["zero_weight_counterexample"]),flush=True)
    output["jacobian"]=jacobian();print(json.dumps(output["jacobian"]),flush=True)
    (ROOT/"independent_results.json").write_text(json.dumps(output,indent=2)+"\n")

if __name__=="__main__":main()
