"""Independently authored checks. No supplied module is imported or executed."""
import json, math, random
from pathlib import Path
import numpy as np

OUT=Path(__file__).parent
P=998244353
IROOT=pow(3,(P-1)//4,P)
Z8=pow(3,(P-1)//8,P)
ROOT2=(Z8+pow(Z8,-1,P))%P

def mm(a,b):
    # Eight products below P^2 sum to less than int64 maximum.
    out=np.zeros((a.shape[0],b.shape[1]),dtype=np.int64)
    for j in range(0,a.shape[1],8):
        out=(out+(a[:,j:j+8]@b[j:j+8,:])%P)%P
    return out

def inverse(a):
    n=len(a); w=np.concatenate([a.copy()%P,np.eye(n,dtype=np.int64)],axis=1)
    for j in range(n):
        piv=next(k for k in range(j,n) if w[k,j])
        w[[j,piv]]=w[[piv,j]]
        w[j]=(w[j]*pow(int(w[j,j]),-1,P))%P
        factors=w[:,j].copy();factors[j]=0
        w=(w-factors[:,None]*w[j:j+1,:])%P
    return w[:,n:]

def rank(a):
    w=a.copy()%P;r=0
    for j in range(w.shape[1]):
        inds=np.flatnonzero(w[r:,j])
        if not len(inds):continue
        q=r+int(inds[0]);w[[r,q]]=w[[q,r]]
        w[r]=(w[r]*pow(int(w[r,j]),-1,P))%P
        f=w[r+1:,j].copy()
        w[r+1:]=(w[r+1:]-f[:,None]*w[r:r+1])%P
        r+=1
        if r==len(w):break
    return r

def cayley(adj,alpha):
    n=len(adj);eye=np.eye(n,dtype=np.int64)
    return (2*inverse((eye-IROOT*alpha%P*adj)%P)-eye)%P

def haar_mod(m):
    h=np.zeros((m,m),dtype=np.int64)
    def scale(w):
        e=w.bit_length()-1
        return pow((pow(2,e//2,P)*(ROOT2 if e%2 else 1))%P,-1,P)
    h[:,0]=scale(m)
    width=m;start=1
    while width>1:
        for b in range(m//width):
            lo=b*width;mid=lo+width//2
            h[lo:mid,start+b]=scale(width)
            h[mid:lo+width,start+b]=(-scale(width))%P
        start+=m//width;width//=2
    return h

def modular_stage(n,variant,seed):
    order=list(range(n));random.Random(seed).shuffle(order)
    invorder=np.argsort(order).tolist()
    path=np.zeros((n,n),dtype=np.int64)
    path2=np.zeros_like(path)
    for j in range(n-1):
        path[j,j+1]=path[j+1,j]=1
        u,v=invorder[j:j+2];path2[u,v]=path2[v,u]=1
    alpha=pow(2 if variant=='strong_haar' else 32,-1,P)
    eps=pow(2 if variant=='strong_haar' else 512,-1,P)
    m=n//2
    if variant=='green_tree':
        size=(1<<((m+1).bit_length()-1))-1
        adj=np.zeros((m,m),dtype=np.int64)
        for k in range(1,size):adj[k,(k-1)//2]=adj[(k-1)//2,k]=1
        h=cayley(adj,2);hinv=inverse(h)
    else:
        h=haar_mod(m);hinv=h.T.copy()
    r=np.zeros((n,n),dtype=np.int64);r[:m,m:]=h;r[m:,:m]=hinv
    q=(np.eye(n,dtype=np.int64)+(IROOT*eps%P)*r)%P
    return mm(q,mm(cayley(path,alpha),cayley(path2,alpha)))

def run_modular():
    cov=[];pairs=[]
    for n in [8,16,32,64,128]:
        omega=pow(3,(P-1)//n,P)
        d=np.array([pow(omega,k,P) for k in range(n)],dtype=np.int64)
        for v in ['green_tree','haar_adapter']:
            a=modular_stage(n,v,5031+n)
            defect=(a[:,np.roll(np.arange(n),-1)]-d[:,None]*a)%P
            cov.append(dict(n=n,variant=v,rank=rank(defect)))
        stages={}
        for role,seed in [('first',2609+n),('second',2609+10*n)]:
            for v in ['green_tree','haar_adapter','strong_haar']:
                a=modular_stage(n,v,seed);ai=inverse(a)
                assert np.array_equal(mm(a,ai),np.eye(n,dtype=np.int64))
                if role=='first':
                    diag=np.diag(mm(a[:,np.roll(np.arange(n),-1)],ai))
                else:diag=np.diag(mm(ai,d[:,None]*a%P))
                stages[role,v]=sorted(int(x) for x in diag)
        for v,w in [('green_tree','green_tree'),('green_tree','haar_adapter'),
                    ('haar_adapter','green_tree'),('haar_adapter','haar_adapter'),
                    ('strong_haar','strong_haar'),('strong_haar','haar_adapter')]:
            x,y=stages['first',v],stages['second',w]
            idx=next((j for j,(a,b) in enumerate(zip(x,y)) if a!=b),None)
            pairs.append(dict(n=n,first=v,second=w,match=x==y,
                              mismatch_index=idx,first_mismatch=None if idx is None else [x[idx],y[idx]]))
    expected=json.loads((OUT/'phase13_source_certificate.json').read_text())
    for a,b in zip(pairs,expected):
        assert a['n']==b['n'] and a['first_mismatch']==b['first_mismatch']
    assert len(expected)==len(pairs)==30
    assert all(a['rank']==a['n'] for a in cov)
    return dict(covariance=cov,two_stage=pairs,all_uploaded_mismatches_reproduced=True)

def givens_qr(a):
    n=len(a);r=a.copy();q=np.eye(n,dtype=complex);count=0
    for k in range(n-1):
        x,y=r[k,k],r[k+1,k]
        if abs(y)==0:continue
        rho=math.sqrt(abs(x)**2+abs(y)**2)
        g=np.array([[x.conjugate(),y.conjugate()],[-y,x]])/rho
        r[k:k+2]=g@r[k:k+2]
        q[:,k:k+2]=q[:,k:k+2]@g.conj().T
        count+=1
    phases=np.diag(r)/abs(np.diag(r))
    r=phases.conjugate()[:,None]*r;q=q*phases[None,:]
    return q,r,count

def haar_gates(m):
    h=np.eye(m);count=0;leaves=[]
    def rec(slot,node,width):
        nonlocal count
        if width==1:leaves.append(slot);return
        a=h[slot].copy();b=h[node].copy()
        h[slot]=(a+b)/math.sqrt(2);h[node]=(a-b)/math.sqrt(2)
        count+=1
        rec(slot,2*node,width//2);rec(node,2*node+1,width//2)
    rec(0,1,m)
    return h[leaves,:],count

def run_numeric():
    rng=np.random.default_rng(140413);rows=[]
    for n in [4,8,16,32,64]:
        for strength in [1/32,1/2,2,100]:
            a=np.diag(rng.normal(size=n))
            off=rng.normal(size=n-1)
            a+=np.diag(off,1)+np.diag(off,-1)
            t=np.eye(n)-1j*strength*a
            qm,rm,cm=givens_qr(t);qp,rp,cp=givens_qr(t.conj().T)
            cay=t.conj().T@np.linalg.inv(t)
            m=n//2;h,hcount=haar_gates(m)
            root=h[:,0]
            assert np.linalg.norm(root-np.ones(m)/math.sqrt(m))<1e-12
            eps=strength;c=1/math.sqrt(1+eps**2);s=eps*c
            z=np.zeros((m,m));ii=np.eye(m)
            invol=np.block([[z,h],[h.T,z]])
            v=c*np.eye(n)+1j*s*invol
            dh=np.block([[h,z],[z,ii]])
            rot=np.block([[c*ii,1j*s*ii],[1j*s*ii,c*ii]])
            gatev=dh@rot@dh.conj().T
            record=dict(n=n,strength=strength,cayley_gates=cm+cp,
                        haar_gates=hcount,rotation_gates=2*hcount+m,
                        common_R_error=float(np.linalg.norm(rm-rp)),
                        qr_error=float(np.linalg.norm(t-qm@rm)),
                        cayley_error=float(np.linalg.norm(cay-qp@qm.conj().T)),
                        normalized_rotation_error=float(np.linalg.norm(v-gatev)),
                        normalized_rotation_unitarity=float(np.linalg.norm(v@v.conj().T-np.eye(n))))
            assert max(record[k] for k in ['common_R_error','qr_error','cayley_error','normalized_rotation_error','normalized_rotation_unitarity'])<1e-9
            assert cm+cp<=2*(n-1) and hcount==m-1
            rows.append(record)
    return rows

if __name__=='__main__':
    result=dict(numeric_gate_reconstruction=run_numeric(),exact_modular=run_modular())
    (OUT/'independent_phase13_results.json').write_text(json.dumps(result,indent=2))
    print('PASS: 20 QR/Haar normalized reconstruction cases; 10 full-rank covariance defects; all 30 uploaded two-stage mismatch certificates reproduced.')
