#!/usr/bin/env python3
"""Fresh transcription controls; supplied research programs are not imported.
All matrix arithmetic in rank checks is exact over explicitly named prime fields.
"""
import hashlib, json, pathlib, time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
PRIMES=(12289,65537)

def rev(n):
    m=(n-1).bit_length();assert n==1<<m
    return [int(format(i,f'0{m}b')[::-1],2) for i in range(n)]
def permutation(p): return np.eye(len(p),dtype=np.int64)[:,p]
def anchor(n,endpoint=1):
    T=np.diag(np.full(n,3,dtype=np.int64))+np.diag(np.ones(n-1,dtype=np.int64),1)+np.diag(np.ones(n-1,dtype=np.int64),-1)
    T[0,0]+=endpoint;return T

def echelon(A,p):
    A=A.copy()%p;m,n=A.shape;r=0;piv=[];det=1
    for j in range(n):
        inds=np.flatnonzero(A[r:,j])
        if not len(inds):continue
        i=r+int(inds[0])
        if i!=r:A[[r,i]]=A[[i,r]];det=-det
        q=int(A[r,j]);det=det*q%p;A[r]=A[r]*pow(q,-1,p)%p
        ids=np.flatnonzero(A[r+1:,j])+r+1
        A[ids]=(A[ids]-A[ids,j,None]*A[r,None,:])%p
        piv.append(j);r+=1
        if r==m:break
    return r,piv,int(det%p)
def inverse(A,p):
    n=len(A);B=np.hstack([A.copy()%p,np.eye(n,dtype=np.int64)])
    for j in range(n):
        ids=np.flatnonzero(B[j:,j]);assert len(ids)
        i=j+int(ids[0]);B[[j,i]]=B[[i,j]];B[j]=B[j]*pow(int(B[j,j]),-1,p)%p
        ids=[i for i in range(n) if i!=j and B[i,j]]
        B[ids]=(B[ids]-B[ids,j,None]*B[j,None,:])%p
    return B[:,n:]
def build_chart(S,p):
    n=len(S);a=np.zeros(n,dtype=np.int64);b=a.copy();c=a.copy();e=a.copy()
    a[1:]=S[1:,0];b[:-1]=S[-1,:-1]*pow(int(S[-1,0]),-1,p)%p
    c[:-1]=S[:-1,-1];e[1:]=S[0,1:]*pow(int(S[0,-1]),-1,p)%p
    d=np.diag(S).copy();return a,b,c,e,d
def chart_matrix(params,p):
    a,b,c,e,d=params
    return (np.tril(np.outer(a,b),-1)+np.triu(np.outer(c,e),1)+np.diag(d))%p
def raw_derivatives(params,p):
    a,b,c,e,d=params;n=len(a);out=[]
    for typ in range(5):
        for q in range(n):
            X=np.zeros((n,n),dtype=np.int64)
            if typ==0:X[q,:q]=b[:q]
            if typ==1:X[q+1:,q]=a[q+1:]
            if typ==2:X[q,q+1:]=e[q+1:]
            if typ==3:X[:q,q]=c[:q]
            if typ==4:X[q,q]=1
            out.append(X)
    return out

def sparse_jac(T,P,t,p):
    n=len(T);A=T@P%p;AT=P@T%p
    L=[np.eye(n,dtype=np.int64)];R=[np.eye(n,dtype=np.int64)]
    for k in range(1,t):L.append(L[-1]@A%p);R.append(AT@R[-1]%p)
    labels=[(k,i,j) for k in range(t) for i in range(n) for j in range(max(0,i-2),min(n,i+3))]
    J=np.array([np.outer(L[k][:,i],R[t-1-k][j,:]).ravel()%p for k,i,j in labels],dtype=np.int64).T
    return J,labels

def raw_jac(S,P,t,p):
    ds=raw_derivatives(build_chart(S,p),p);A=S@P%p;B=P@S%p
    L=[np.eye(len(S),dtype=np.int64)];R=[np.eye(len(S),dtype=np.int64)]
    for k in range(1,t):L.append(L[-1]@A%p);R.append(B@R[-1]%p)
    return np.array([(L[k]@X%p@R[t-1-k]%p).ravel() for k in range(t) for X in ds],dtype=np.int64).T

def tangent_transport(S,p):
    n=len(S);a,b,c,e,d=build_chart(S,p);count=0
    for i in range(n):
        for j in range(max(0,i-2),min(n,i+3)):
            U=-np.outer(S[:,i],S[j,:])%p
            da=np.zeros(n,dtype=np.int64);db=da.copy();dc=da.copy();de=da.copy()
            da[1:]=U[1:,0];db[:-1]=(U[-1,:-1]-b[:-1]*U[-1,0])*pow(int(S[-1,0]),-1,p)%p
            dc[:-1]=U[:-1,-1];de[1:]=(U[0,1:]-e[1:]*U[0,-1])*pow(int(S[0,-1]),-1,p)%p
            V=(np.tril(np.outer(da,b)+np.outer(a,db),-1)+np.triu(np.outer(dc,e)+np.outer(c,de),1)+np.diag(np.diag(U)))%p
            assert np.array_equal(U,V);count+=1
    return count

def run():
    start=time.time();result={'purpose':'transcription controls only; no all-size saturation claim','prime_fields':list(PRIMES),'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'cases':[],'uniform_obstruction_controls':[]}
    for n in (8,16,32):
        t=n//4+1;T=anchor(n);P=permutation(rev(n));case={'N':n,'t':t,'anchor':'diag(4,3,...,3), both adjacent diagonals 1','fields':[]};selected=None
        for p in PRIMES:
            S=inverse(T,p);assert np.array_equal(chart_matrix(build_chart(S,p),p),S)
            checks=tangent_transport(S,p);J,labels=sparse_jac(T,P,t,p);rank,piv,det=echelon(J,p);assert rank==n*n
            if selected is None:selected=piv;case['minor_columns']=piv;case['column_labels']=[list(labels[q]) for q in piv]
            mr,_,md=echelon(J[:,selected],p);assert mr==n*n
            R=raw_jac(S,P,t,p);rr,_,_=echelon(R,p);assert rr==n*n
            # Mutation: identity boundaries must not attain threshold dominance.
            I=np.eye(n,dtype=np.int64);JI,_=sparse_jac(T,I,t,p);ir,_,_=echelon(JI,p);assert ir<n*n
            case['fields'].append({'p':p,'sparse_rank':rank,'raw_5Nt_rank':rr,'minor_det':md,'invertible_T_det':echelon(T,p)[2],'pentadiagonal_transport_columns':checks,'identity_boundary_rank':ir})
        result['cases'].append(case)
    # Integer identity checks, no modular inference: B=RP, PTB=BTP.
    for m in (3,4,5,7,9):
        n=1<<m;rv=rev(n);q=[n-1-rv[i] for i in range(n)];distance=min(abs(i-q[i]) for i in range(n))
        # Verify the intertwining relation using sparsity, without dense cubic work.
        T=anchor(n,0);P=permutation(rv);B=permutation(q)
        lhs=P@(T@B);rhs=B@(T@P);assert np.array_equal(lhs,rhs)
        if m>=5 and m%2:assert distance==3
        result['uniform_obstruction_controls'].append({'m':m,'N':n,'min_B_distance':distance,'exact_integer_PTB_equals_BTP':True,'annihilator_applies':distance>2})
    # Endpoint perturbation really breaks the particular annihilator.
    n=32;P=permutation(rev(n));B=permutation([n-1-i for i in rev(n)]);T=anchor(n)
    assert np.any(P@T@B-B@T@P)
    result['endpoint_perturbation_breaks_old_intertwiner']=True
    result['elapsed_seconds']=time.time()-start
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    for c in result['cases']:print(json.dumps({k:v for k,v in c.items() if k not in ('minor_columns','column_labels')}))
if __name__=='__main__':run()
