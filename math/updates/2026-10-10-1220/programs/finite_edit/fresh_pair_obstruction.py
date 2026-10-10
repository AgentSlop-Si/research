#!/usr/bin/env python3
"""Fresh finite-edit compatibility controls. No submitted module is imported/run."""
import json
from pathlib import Path
import numpy as np

P = 65537
OUT = Path(__file__).resolve().parent

def mm(a,b):
    return (np.asarray(a,dtype=np.int64) @ np.asarray(b,dtype=np.int64)) % P

def inverse(a):
    n=len(a); m=np.column_stack((a.copy()%P,np.eye(n,dtype=np.int64)))
    for j in range(n):
        ii=np.flatnonzero(m[j:,j])
        if not len(ii): raise ValueError('Singular inverse pencil')
        k=j+int(ii[0]); m[[j,k]]=m[[k,j]]
        m[j]=(m[j]*pow(int(m[j,j]),-1,P))%P
        factors=m[:,j].copy(); factors[j]=0
        m=(m-factors[:,None]*m[j])%P
    g=m[:,n:]
    assert np.array_equal(mm(a,g),np.eye(n,dtype=np.int64))
    return g

def rank_det(a):
    m=np.asarray(a,dtype=np.int64).copy()%P; nr,nc=m.shape
    r=0; det=1
    for c in range(nc):
        rows=np.flatnonzero(m[r:,c])
        if not len(rows): continue
        k=r+int(rows[0])
        if k!=r: m[[k,r]]=m[[r,k]]; det=-det
        pivot=int(m[r,c]); det=det*pivot%P
        m[r]=(m[r]*pow(pivot,-1,P))%P
        if r+1<nr: m[r+1:]=(m[r+1:]-m[r+1:,c,None]*m[r])%P
        r+=1
        if r==nr: break
    return r, (int(det%P) if nr==nc and r==nr else 0)

def cycle_ok(q,w):
    seen=set()
    for start in range(len(q)):
        if start in seen: continue
        j=start; z=1
        while j not in seen:
            seen.add(j); z=z*int(w[j])%P; j=int(q[j])
        if z==1:return False
    return True

def green(q,w):
    pencil=np.eye(len(q),dtype=np.int64)
    pencil[np.arange(len(q)),q]-=w
    return inverse(pencil%P)

def pinned(n,seed=19):
    s=int(n**0.5); assert s*s==n
    x=np.repeat(np.arange(s),s);y=np.tile(np.arange(s),s)
    qs=[((x+2*y)%s)*s+y,((x+2*y+1)%s)*s+y,
        x*s+(y+2*x)%s,x*s+(y+2*x+1)%s]
    rng=np.random.default_rng(seed); weights=[]; greens=[]
    for layer in range(2):
        ws=[]; gs=[]
        for q in qs:
            while True:
                w=rng.integers(2,1024,size=n,dtype=np.int64)
                if cycle_ok(q,w):break
            ws.append(w);gs.append(green(q,w))
        weights.append(ws);greens.append(gs)
    a=pow(4,-1,P); b=a
    A=(sum(greens[1][:3])*b)%P
    B=((greens[0][0]+greens[0][2]+greens[0][3])*a)%P
    Qh=np.eye(n,dtype=np.int64)[qs[1]]
    Qv=np.eye(n,dtype=np.int64)[qs[3]]
    return qs,weights,greens,A,B,a,b,Qh,Qv

def coefficient_matrices(F,A,B,a,b,Qh,Qv):
    n=len(F); I=np.eye(n,dtype=np.int64)
    X=(F-mm(A,B))%P
    R=mm((X-a*A-b*B-(a*b%P)*I)%P,Qh.T)
    U=mm(mm(Qv,(X-a*A)%P),Qh.T)
    W=(X-b*B)%P
    Z=mm(Qv,X)
    return R,U,W,Z

def pair_matrix(c,i,k):
    R,U,W,Z=c
    return np.column_stack((
        -R[i]*W[k]+R[k]*W[i],
        U[i]*W[k]-R[k]*Z[i],
        R[i]*Z[k]-U[k]*W[i],
        -U[i]*Z[k]+U[k]*Z[i]))%P

def row_minor(m):
    selected=[];r=0
    for j in range(len(m)):
        rr,_=rank_det(m[selected+[j]])
        if rr>r:selected.append(j);r=rr
        if r==4: return selected,m[selected],rank_det(m[selected])[1]
    return None

def find_certificate(c):
    n=len(c[0])
    for i in range(n):
        for k in range(i+1,n):
            found=row_minor(pair_matrix(c,i,k))
            if found:
                js,minor,det=found
                return {'row_pair':[i,k],'target_columns':js,'minor_matrix':minor.tolist(),
                        'determinant_mod_p':det,'rank':4}
    return None

def reachable_control(n,zero_h=False):
    qs,ws,gs,A,B,a,b,Qh,Qv=pinned(n)
    rng=np.random.default_rng(211+n)
    h=np.zeros(n,dtype=np.int64) if zero_h else rng.integers(2,200,size=n,dtype=np.int64)
    v=rng.integers(2,200,size=n,dtype=np.int64)
    H=green(qs[1],h);V=green(qs[3],v)
    F=mm((A+b*V)%P,(B+a*H)%P)
    c=coefficient_matrices(F,A,B,a,b,Qh,Qv)
    R,U,W,Z=c
    residual=(R-v[:,None]*U-h[None,:]*W+(v[:,None]*h[None,:]%P)*Z)%P
    assert not np.any(residual)
    I=np.eye(n,dtype=np.int64);Sv=(I-v[:,None]*Qv)%P;Sh=(I-h[:,None]*Qh)%P
    pencil_lhs=mm(mm(Sv,F),Sh)
    pencil_rhs=mm((mm(Sv,A)+b*I)%P,(mm(B,Sh)+a*I)%P)
    assert np.array_equal(pencil_lhs,pencil_rhs)
    maxrank=0
    for i in range(n):
        for k in range(i+1,n):
            M=pair_matrix(c,i,k)
            vec=np.array([1,v[i],v[k],v[i]*v[k]%P],dtype=np.int64)
            assert not np.any(mm(M,vec))
            rank,_=rank_det(M);assert rank<=3;maxrank=max(maxrank,rank)
    # Baseline chart rank is a separate negative control, never the new test.
    H0=gs[0][1];V0=gs[1][3];B0=mm(Qh,H0);C0=mm(mm(Qv,V0),H0)
    T0=mm((A+b*V0)%P,(B+a*H0)%P)
    E=(F-T0)%P
    raw=mm(mm(inverse(V0),E),inverse(B0))*pow(a*b%P,-1,P)%P
    recips=np.array([pow(int(c),-1,P) for c in C0.flat],dtype=np.int64).reshape(n,n)
    baseline_rank=rank_det(raw*recips%P)[0]
    return {'N':n,'modified_horizontal_all_zero':zero_h,'all_bilinear_equations_zero':True,
            'two_sided_pencil_identity':True,'all_row_pairs_checked':n*(n-1)//2,
            'max_row_pair_rank':maxrank,'complete_edit_baseline_normalized_rank':baseline_rank}

def main():
    results={'field_prime':P,'seed':19,'construction':'Fresh dense inverses and direct matrix products; no submitted programs imported or executed.',
             'fourier_certificates':[],'reachable_controls':[]}
    for n in [4,16,64,256]:
        qs,ws,gs,A,B,a,b,Qh,Qv=pinned(n)
        omega=pow(3,(P-1)//n,P)
        assert pow(omega,n,P)==1 and pow(omega,n//2,P)!=1
        F=np.array([[pow(omega,i*j,P) for j in range(n)] for i in range(n)],dtype=np.int64)
        certificate=find_certificate(coefficient_matrices(F,A,B,a,b,Qh,Qv))
        assert certificate is not None
        item={'N':n,'omega':omega,'coefficient_each_term_mod_p':a,'certificate':certificate,
              'integer_weight_arrays':[[w.tolist() for w in stage] for stage in ws]}
        results['fourier_certificates'].append(item)
        print(json.dumps({key:val for key,val in item.items() if key!='integer_weight_arrays'}),flush=True)
    for n,z in [(4,False),(16,False),(16,True),(64,False)]:
        item=reachable_control(n,z);results['reachable_controls'].append(item);print(json.dumps(item),flush=True)
    (OUT/'FRESH_PAIR_OBSTRUCTION_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
