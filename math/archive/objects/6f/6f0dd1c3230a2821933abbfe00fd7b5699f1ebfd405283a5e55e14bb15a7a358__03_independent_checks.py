"""Independent checks authored for this report. No uploaded modules are imported."""
import json, math
from pathlib import Path
import numpy as np

P=257

def mul(A,B): return (A @ B) % P

def rank(A):
    A=np.array(A,dtype=np.int64).copy()%P
    m,n=A.shape; r=0
    for j in range(n):
        inds=np.flatnonzero(A[r:,j])
        if len(inds)==0: continue
        k=r+int(inds[0]); A[[r,k]]=A[[k,r]]
        A[r]=(A[r]*pow(int(A[r,j]),-1,P))%P
        factors=A[:,j].copy(); factors[r]=0
        A=(A-factors[:,None]*A[r:r+1])%P
        r+=1
        if r==m: break
    return r

def inv(A):
    n=len(A); W=np.concatenate((A.copy()%P,np.eye(n,dtype=np.int64)),axis=1)
    for j in range(n):
        inds=np.flatnonzero(W[j:,j])
        if len(inds)==0: raise ValueError('singular')
        k=j+int(inds[0]); W[[j,k]]=W[[k,j]]
        W[j]=(W[j]*pow(int(W[j,j]),-1,P))%P
        factors=W[:,j].copy(); factors[j]=0
        W=(W-factors[:,None]*W[j:j+1])%P
    return W[:,n:]

def root(n):
    w=pow(3,-256//n,P)
    assert pow(w,n,P)==1 and pow(w,n//2,P)!=1
    return w

def diag_pow(w,n,a): return np.diag([pow(w,(a*j)%n,P) for j in range(n)]).astype(np.int64)

def shift(n):
    Z=np.zeros((n,n),dtype=np.int64)
    for j in range(n):Z[(j+1)%n,j]=1
    return Z

def T(A): return np.roll(np.roll(A,-1,axis=0),-1,axis=1)

def poly_roots(roots):
    c=[1]
    for z in roots:
        out=[0]*(len(c)+1)
        for j,v in enumerate(c):out[j]=(out[j]-z*v)%P;out[j+1]=(out[j+1]+v)%P
        c=out
    return c

def poly_T(A,c):
    result=np.zeros_like(A); cur=A.copy()
    for coeff in c:
        result=(result+coeff*cur)%P;cur=T(cur)
    return result

def fourier_mod(n):
    w=root(n);return np.array([[pow(w,j*k,P) for k in range(n)]for j in range(n)],dtype=np.int64)

out={'sharp_inverse_rows':[],'all_rows_half_support':[],'projector_completion':[],'twisted_spectrum':[],'linear_phase_products':[]}
for n in [2,4,8,16,32]:
    F=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)/np.sqrt(n)
    for s in sorted(set([1,n//2,n-1])):
        i=n//3;u=F.conj().T[i] # row e_i^T F*; F is symmetric
        v=np.zeros(n,dtype=complex);v[:s]=u[:s]/np.sqrt(s/n)
        a=np.sqrt(s/n)
        E=np.outer(v.conj(),a*np.eye(n)[i]-v@F)
        M=F+E;B=np.linalg.inv(M)
        distance=np.linalg.norm(E,2);tail=np.linalg.norm(B[i,s:])
        assert abs(distance-np.sqrt(1-s/n))<1e-12 and tail<1e-11
        out['sharp_inverse_rows'].append({'N':n,'s':s,'error':float(distance),'expected':float(np.sqrt(1-s/n)),'inverse_row_tail':float(tail)})
    h=n//2
    # Columns are reordered even first, then odd. M retains the diagonal blocks.
    cols=list(range(0,n,2))+list(range(1,n,2))
    H=F[:,cols];Md=np.zeros_like(F);Md[:h,:h]=H[:h,:h];Md[h:,h:]=H[h:,h:]
    M=np.zeros_like(F);M[:,cols]=Md
    B=np.linalg.inv(M);maxsupport=max(np.count_nonzero(abs(row)>1e-10) for row in B)
    err=np.linalg.norm(M-F,2)
    assert maxsupport==h and abs(err-1/np.sqrt(2))<1e-12
    out['all_rows_half_support'].append({'N':n,'row_support':int(maxsupport),'error':float(err)})

for n,m in [(8,2),(16,4),(32,4),(64,8)]:
    k=n//m; z=pow(root(n),-1,P);a=3;beta0=1;Ps=[]
    for h in range(m):
        beta=(beta0+h*k)%n;A=np.zeros((n,n),dtype=np.int64)
        for r in range(k):
            s=[pow(z,(a*t*(t-1)//2+(a*m*r+beta)*t)%n,P)for t in range(m)]
            for t in range(m):
                for u in range(m):A[r*m+t,r*m+u]=(pow(s[t],-1,P)*s[u])%P
        Ps.append(A)
    total=sum(Ps)%P
    assert np.array_equal(total,(m*np.eye(n,dtype=np.int64))%P)
    for h in range(m):
        for ell in range(m):
            expected=(m*Ps[h])%P if h==ell else np.zeros((n,n),dtype=np.int64)
            assert np.array_equal(mul(Ps[h],Ps[ell]),expected)
    ranks=[rank(sum(Ps[:ell])%P)for ell in range(1,m+1)]
    assert ranks==[ell*k for ell in range(1,m+1)]
    F=fourier_mod(n)
    assert np.array_equal((sum(mul(F,A)for A in Ps)*pow(m,-1,P))%P,F)
    out['projector_completion'].append({'N':n,'M':m,'K':k,'partial_sum_ranks':ranks,'exact_completion':True})

for n in [4,8,16,32,64]:
    w=np.exp(-2j*np.pi/n);F=np.array([[w**(j*k)for k in range(n)]for j in range(n)])/np.sqrt(n)
    Z=shift(n).astype(complex)
    for a in [0,1,n//2]:
        defect=F@Z-w**a*Z@F
        sv=np.linalg.svd(defect,compute_uv=False)
        expected=np.array([2*np.cos(np.pi*(2*(r//2)+1)/(2*n))for r in range(n)])
        discrepancy=float(max(abs(sv-expected)))
        assert discrepancy<1e-11
        out['twisted_spectrum'].append({'N':n,'phase_exponent':a,'max_discrepancy':discrepancy})

for n,affine in [(16,False),(32,True),(128,False),(256,True)]:
    w=root(n);Z=shift(n);I=np.eye(n,dtype=np.int64);F=fourier_mod(n)
    factors=[];phase_lists=[]
    for j in range(2):
        terms=[];exps=[]
        for ell in range(2):
            B=np.zeros((n,n),dtype=np.int64)
            for i in range(n-1):B[i+1,i]=1+j;B[i,i+1]=2+ell
            for diagonal in range(6,60):
                try:G=inv((B+diagonal*I)%P);break
                except ValueError:continue
            else:raise RuntimeError('no denominator')
            u=2*(j+ell)+1 if affine else 1;c=j+ell if affine else 0
            order=np.array([(c+u*i)%n for i in range(n)])
            GG=np.zeros_like(G);GG[np.ix_(order,order)]=G
            aa=1+j+2*ell;bb=2+j+3*ell;net=(aa+bb)%n
            term=mul(mul(diag_pow(w,n,aa),GG),diag_pow(w,n,bb))
            rho=rank((T(term)-pow(w,net,P)*term)%P)
            assert rho<=(4 if affine else 2)
            terms.append(term);exps.append(net)
        factors.append(terms);phase_lists.append(exps)
    S0=sum(factors[0])%P;S1=sum(factors[1])%P;M=mul(S1,S0)
    branches=[mul(B,A)for B in factors[1]for A in factors[0]]
    exps=[(b+a)%n for b in phase_lists[1]for a in phase_lists[0]]
    distinct=sorted(set(exps));d=len(distinct);c=poly_roots([pow(w,e,P)for e in distinct])
    branch_ranks=[rank((T(A)-pow(w,e,P)*A)%P)for A,e in zip(branches,exps)]
    projected_rank=rank(poly_T(M,c));fourier_rank=rank(poly_T(F,c))
    bound=d*sum(branch_ranks)
    assert projected_rank<=bound and fourier_rank>=n-d
    W=mul(Z.T,diag_pow(w,n,1));cur=I.copy();qW=np.zeros_like(I)
    for k,ck in enumerate(c):
        qW=(qW+(ck*pow(w,k*(k-1)//2,P)%P)*cur)%P;cur=mul(cur,W)
    assert np.array_equal(poly_T(F,c),mul(qW,F))
    out['linear_phase_products'].append({'N':n,'affine_orders':affine,'branches':4,'distinct_total_phases':d,'branch_defect_ranks':branch_ranks,'annihilated_candidate_rank':projected_rank,'rank_upper_bound':bound,'annihilated_Fourier_rank':fourier_rank,'Fourier_rank_lower_bound':n-d,'excluded_by_rank_gap':projected_rank<fourier_rank})

path=Path(__file__).with_name('CHECK_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'all independent checks passed','results':str(path),'sections':{k:len(v)for k,v in out.items()}},indent=2))
