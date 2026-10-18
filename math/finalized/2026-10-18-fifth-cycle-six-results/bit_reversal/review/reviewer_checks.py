#!/usr/bin/env python3
"""Independent review controls. No candidate or archived code imported.
Exact rational local/source-chart checks; direct stage-product derivatives;
a fresh-prime selected-minor test; exact structural identities.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parent
CANDIDATE=ROOT.parent/'candidate'

def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def mul(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def neg(a):return [[-x for x in r] for r in a]
def inv(a):
    n=len(a);b=[[F(x) for x in row]+eye(n)[i] for i,row in enumerate(a)]
    for j in range(n):
        q=next(i for i in range(j,n) if b[i][j]);b[j],b[q]=b[q],b[j]
        d=b[j][j];b[j]=[x/d for x in b[j]]
        for i in range(n):
            if i!=j:
                d=b[i][j];b[i]=[x-d*y for x,y in zip(b[i],b[j])]
    return [r[n:] for r in b]
def rational_rank(cols):
    basis={}
    for col in cols:
        v=list(col)
        for i,w in sorted(basis.items()):
            d=v[i]
            if d:v=[x-d*y for x,y in zip(v,w)]
        i=next((i for i,x in enumerate(v) if x),None)
        if i is not None:
            d=v[i];basis[i]=[x/d for x in v]
    return len(basis)
def raw(S):
    n=len(S)
    return [[F(0)]+[S[i][0] for i in range(1,n)],
            [S[-1][j]/S[-1][0] for j in range(n-1)]+[F(0)],
            [S[i][-1] for i in range(n-1)]+[F(0)],
            [F(0)]+[S[0][j]/S[0][-1] for j in range(1,n)],
            [S[i][i] for i in range(n)]]
def chart(v):
    a,b,c,e,d=v;n=len(a)
    return [[a[i]*b[j] if i>j else c[i]*e[j] if i<j else d[i] for j in range(n)] for i in range(n)]
def raw_derivative(v,typ,q):
    n=len(v[0]);u=[r.copy() for r in v];u[typ][q]+=1
    a=chart(u);b=chart(v)
    return [[a[i][j]-b[i][j] for j in range(n)] for i in range(n)]
def tri(n,variant=0):
    return [[F(20+i+variant if i==j else i+2 if i==j+1 else j+1 if j==i+1 else 0) for j in range(n)] for i in range(n)]
def reverse_bits(i,m):
    r=0
    for _ in range(m):r=(r<<1)|(i&1);i>>=1
    return r
def perm(n):
    m=n.bit_length()-1;assert 1<<m==n
    return [[F(i==reverse_bits(j,m)) for j in range(n)] for i in range(n)]
def product(stages,P):
    a=stages[0]
    for b in stages[1:]:a=mul(mul(a,P),b)
    return a

def local_checks():
    out=[]
    for n in (4,5,8):
        T=tri(n);S=inv(T);v=raw(S);assert chart(v)==S
        ds=[raw_derivative(v,a,q) for a in range(5) for q in range(n)]
        xs=[neg(mul(mul(T,d),T)) for d in ds]
        assert all(x[i][j]==0 for x in xs for i in range(n) for j in range(n) if abs(i-j)>2)
        rk=rational_rank([[z for r in x for z in r] for x in xs]);assert rk==5*n-6
        out.append({'N':n,'nonsymmetric_tridiagonal':True,'exact_raw_tangent_rank':rk,'all_inverted_raw_directions_pentadiagonal':True})
    n=4;t=3;P=perm(n);Ts=[tri(n,k) for k in range(t)];Ss=[inv(T) for T in Ts]
    K=product(Ts,P);M=product(list(reversed(Ss)),P);assert mul(K,M)==eye(n)
    count=0
    for k in range(t):
        v=raw(Ss[k])
        for typ in range(5):
            for q in range(n):
                d=raw_derivative(v,typ,q);X=neg(mul(mul(Ts[k],d),Ts[k]));ts=Ts.copy();ts[k]=X
                ss=list(reversed(Ss));ss[t-1-k]=d
                assert product(ts,P)==neg(mul(mul(K,product(ss,P)),K));count+=1
    out.append({'N':n,'stages':t,'distinct_nonsymmetric_anchors':True,'exact_raw_product_derivative_transport_columns':count})
    return out

def determinant_by_column_operations(a,p):
    a=np.array(a,dtype=np.int64)%p;n=a.shape[0];assert a.shape==(n,n);d=1
    # Column pivoting and column elimination, independent of candidate row algorithm.
    for i in range(n):
        matches=np.flatnonzero(a[i,i:])
        if not len(matches):return 0
        j=i+int(matches[0])
        if j!=i:a[:,[i,j]]=a[:,[j,i]];d=-d
        v=int(a[i,i]);d=d*v%p
        if i+1<n:
            scales=a[i,i+1:]*pow(v,-1,p)%p
            a[i+1:,i+1:]=(a[i+1:,i+1:]-a[i+1:,i,None]*scales[None,:])%p
            a[i,i+1:]=0
    return int(d%p)
def fresh_minor_checks():
    p=104729;res=json.loads((CANDIDATE/'RESULTS.json').read_text());out=[]
    for case in res['cases']:
        n=case['N'];t=case['t'];T=np.array([[4 if i==j==0 else 3 if i==j else int(abs(i-j)==1) for j in range(n)] for i in range(n)],dtype=np.int64);P=np.array(perm(n),dtype=np.int64)
        # Prefix/suffix products, with deliberately independent recursion order.
        prefix=[np.eye(n,dtype=np.int64)]
        for _ in range(t-1):prefix.append((prefix[-1]@T@P)%p)
        suffix=[None]*t;suffix[-1]=np.eye(n,dtype=np.int64)
        for k in range(t-2,-1,-1):suffix[k]=(P@T@suffix[k+1])%p
        selected=[]
        for k,i,j in case['column_labels']:
            selected.append((prefix[k][:,i,None]*suffix[k][j,None,:]%p).reshape(-1))
        a=np.array(selected,dtype=np.int64).T;det=determinant_by_column_operations(a,p);assert det
        out.append({'N':n,'t':t,'p':p,'candidate_selected_minor_determinant':det,'row_rank':n*n})
    return out

def exact_structure_checks():
    distances=[]
    for m in (3,4,5,7,9,11,13,15):
        n=1<<m;distance=min(abs(i-(n-1-reverse_bits(i,m))) for i in range(n))
        if m>=5 and m%2:assert distance==3
        distances.append({'bits':m,'min_RP_displacement':distance})
    interleavers=[]
    for n in (4,8,16):
        N=2*n;P=np.array(perm(N),dtype=np.int64);Pn=np.array(perm(n),dtype=np.int64);Q=np.zeros((N,N),dtype=np.int64)
        for b in (0,1):
            for j in range(n):Q[2*j+b,b*n+j]=1
        diag=np.zeros((N,N),dtype=np.int64);diag[:n,:n]=Pn;diag[n:,n:]=Pn;assert np.array_equal(P,Q@diag)
        T=np.diag([4]+[3]*(N-1))+np.diag([1]*(N-1),1)+np.diag([1]*(N-1),-1)
        B=Q.T@T@Q;I=np.eye(n,dtype=np.int64);L=np.diag([1]*(n-1),-1)
        upper=3*I.copy();upper[0,0]+=1
        assert np.array_equal(B,np.block([[upper,I+L],[I+L.T,3*I]]));interleavers.append(N)
    # Exact integer intertwiner for a NON-Toeplitz centrosymmetric anchor.
    n=32;P=np.array(perm(n),dtype=object);R=np.fliplr(np.eye(n,dtype=object));B=R@P
    diagonal=[10+min(i,n-1-i) for i in range(n)];off=[1+(min(i,n-2-i)%3) for i in range(n-1)]
    T=np.diag(diagonal).astype(object)+np.diag(off,1)+np.diag(off,-1)
    assert np.array_equal(R@T,T@R);assert np.array_equal((P@T)@B,B@(T@P))
    assert all(B[i,j]==0 for i in range(n) for j in range(n) if abs(i-j)<=2)
    # Check an explicit all-depth functional over an independent field, without rank inference.
    p=104729
    def mod_inv(a):
        a=[[int(x)%p for x in r] for r in a];b=[r+[int(i==j) for j in range(n)] for i,r in enumerate(a)]
        for j in range(n):
            q=next(i for i in range(j,n) if b[i][j]);b[j],b[q]=b[q],b[j];v=pow(b[j][j],-1,p);b[j]=[x*v%p for x in b[j]]
            for i in range(n):
                if i!=j:
                    v=b[i][j];b[i]=[(x-v*y)%p for x,y in zip(b[i],b[j])]
        return np.array([r[n:] for r in b],dtype=np.int64)
    A=np.asarray(T@P,dtype=np.int64)%p;C=np.asarray(P@T,dtype=np.int64)%p;Ci=mod_inv(C);B=np.asarray(B,dtype=np.int64)
    depths=[]
    for t in (1,2,3,9,17):
        Ctinv=np.eye(n,dtype=np.int64)
        for _ in range(t-1):Ctinv=Ctinv@Ci%p
        Zt=Ctinv@B%p
        left=np.eye(n,dtype=np.int64);right=np.eye(n,dtype=np.int64)
        for _ in range(t-1):left=left@C%p
        for k in range(t):
            observation=left@Zt%p@right%p
            assert np.array_equal(observation,B)
            left=left@Ci%p;right=right@A%p
        depths.append(t)
    return {'RP_distances':distances,'exact_interleaver_sizes':interleavers,'non_Toeplitz_centrosymmetric_intertwiner_N':n,'annihilator_modular_depths':depths,'annihilator_prime':p}

def replay_checks():
    original=json.loads((CANDIDATE/'RESULTS.json').read_text());replay=json.loads((ROOT/'replay/RESULTS.json').read_text())
    original.pop('elapsed_seconds');replay.pop('elapsed_seconds');assert original==replay
    assert (CANDIDATE/'INDEPENDENT_RESULTS.json').read_bytes()==(ROOT/'replay/INDEPENDENT_RESULTS.json').read_bytes()
    m=json.loads((CANDIDATE/'MANIFEST.json').read_text())
    for item in m['files']:
        b=(CANDIDATE/item['path']).read_bytes();assert len(b)==item['bytes'];assert hashlib.sha256(b).hexdigest()==item['sha256']
    return {'candidate_manifest_entries_verified':len(m['files']),'author_control_replay':'identical except elapsed_seconds','author_second_control_replay':'byte-identical','candidate_REPORT_sha256':hashlib.sha256((CANDIDATE/'REPORT.md').read_bytes()).hexdigest(),'candidate_MANIFEST_sha256':hashlib.sha256((CANDIDATE/'MANIFEST.json').read_bytes()).hexdigest()}

if __name__=='__main__':
    out={'all_passed':True,'scope':'Finite implementation controls and pinned-input integrity; not a uniform rank proof.','bindings_and_replays':replay_checks(),'rational_source_chart_checks':local_checks(),'fresh_prime_minor_checks':fresh_minor_checks(),'structural_checks':exact_structure_checks(),'reviewer_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'REVIEWER_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
