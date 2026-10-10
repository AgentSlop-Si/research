"""Independent Phase22 audit; imports no submitted modules and executes no source programs."""
from pathlib import Path
import json, math
from fractions import Fraction
import numpy as np
BASE=Path(__file__).resolve().parent
SRC=BASE/'data'
P=65537

def inverse(A,p):
    n=len(A); R=np.concatenate((A.copy()%p,np.eye(n,dtype=np.int64)),axis=1)
    for c in range(n):
        nz=np.flatnonzero(R[c:,c]); assert len(nz),'singular pencil'
        k=c+int(nz[0]); R[[c,k]]=R[[k,c]]
        R[c]=(R[c]*pow(int(R[c,c]),-1,p))%p
        fac=R[:,c].copy();fac[c]=0
        R=(R-fac[:,None]*R[c])%p
    out=R[:,n:];assert np.array_equal(A@out%p,np.eye(n,dtype=np.int64))
    return out

def rank(A,p):
    R=A.copy()%p;m,n=R.shape;k=0
    for c in range(n):
        ii=np.flatnonzero(R[k:,c])
        if not len(ii):continue
        i=k+int(ii[0]);R[[i,k]]=R[[k,i]]
        R[k]=R[k]*pow(int(R[k,c]),-1,p)%p
        R[k+1:]=(R[k+1:]-R[k+1:,c,None]*R[k])%p
        k+=1
        if k==m:break
    return k

def maps(s):
    return [np.array([(((x+2*y+(t==1))%s)*s+y if t<2 else x*s+(y+2*x+(t==3))%s) for x in range(s) for y in range(s)],dtype=np.int64) for t in range(4)]

def cycles(perm):
    unseen=set(range(len(perm)));ret=[]
    while unseen:
        start=min(unseen);C=[];i=start
        while i in unseen:
            unseen.remove(i);C.append(i);i=int(perm[i])
        assert i==start;ret.append(C)
    return ret

def seed_arrays(s,p):
    rng=np.random.default_rng(19);out=[]
    for stage in range(2):
        layer=[]
        for perm in maps(s):
            while True:
                row=rng.integers(2,1024,size=s*s,dtype=np.int64)
                if all(math.prod(map(int,row[C]))%p!=1 for C in cycles(perm)):break
            layer.append(row.tolist())
        out.append(layer)
    return out

def greens(s,weights,p):
    n=s*s;out=[]
    for stage in range(2):
        row=[]
        for perm,vals in zip(maps(s),weights[stage]):
            A=np.eye(n,dtype=np.int64);A[np.arange(n),perm]-=np.array(vals)
            row.append(inverse(A,p))
        out.append(row)
    return out

def block(T,A,B,s,orientation,r,c):
    if orientation=='H':
        rows=[r*s+y for y in range(s) if y!=c];cols=[a*s+c for a in range(s) if a!=r]
        other=lambda i,j:(j//s)*s+i%s
        fixed=r*s+c
    else:
        rows=[x*s+r for x in range(s) if x!=c];cols=[c*s+b for b in range(s) if b!=r]
        other=lambda i,j:(i//s)*s+j%s
        fixed=c*s+r
    Q=np.array([[B[i,other(i,j)]*A[other(i,j),j] for j in cols] for i in rows])
    return T[np.ix_(rows,cols)]-Q,rows,cols,fixed

def det2(M,p):return (int(M[0,0])*int(M[1,1])-int(M[0,1])*int(M[1,0]))%p

def rational_entry(perm,vals,i,j):
    C=next(c for c in cycles(perm) if i in c)
    if j not in C:return Fraction(0)
    den=1-math.prod(vals[q] for q in C)
    pos=C.index(i);steps=(C.index(j)-pos)%len(C)
    return Fraction(math.prod(vals[C[(pos+t)%len(C)]] for t in range(steps)),den)

def poly_multiply(A,B,n):
    out={}
    for a,v in A.items():
        for b,w in B.items():
            c=(a+b)%n; sign=1 if c<n//2 else -1;c%=n//2
            out[c]=out.get(c,Fraction(0))+sign*v*w
    return {i:v for i,v in out.items() if v}

def exact_minor(s,weights,orientation):
    n=s*s;perms=maps(s);fixedin=(2,3) if orientation=='H' else (0,1);fixedout=(0,1) if orientation=='H' else (2,3)
    D=[]
    for u in (1,2):
        row=[]
        for v in (1,2):
            i,j,k=(u,v*s,v*s+u) if orientation=='H' else (u*s,v,u*s+v)
            A=sum((rational_entry(perms[t],weights[0][t],k,j)/4 for t in fixedin),Fraction(0))
            B=sum((rational_entry(perms[t],weights[1][t],i,k)/4 for t in fixedout),Fraction(0))
            exponent=i*j%n;term={exponent%(n//2):Fraction(1 if exponent<n//2 else -1)}
            term[0]=term.get(0,Fraction(0))-A*B;row.append(term)
        D.append(row)
    one=poly_multiply(D[0][0],D[1][1],n);two=poly_multiply(D[0][1],D[1][0],n)
    ans={i:one.get(i,Fraction(0))-two.get(i,Fraction(0)) for i in one.keys()|two.keys()}
    return {i:v for i,v in ans.items() if v}

def run():
    expected=json.loads((SRC/'EXACT_CERTIFICATES.json').read_text())
    accepted=json.loads((SRC/'INTEGER_BACKGROUNDS.json').read_text())
    pinned={d['N']:d['integer_weight_arrays'] for d in accepted['fourier_certificates']}
    results={'method':'Fresh dense modular inverses, independent products, independently reconstructed rational cycle entries and sparse cyclotomic algebra. Submitted programs neither imported nor executed.','pinned':[],'reachable_controls':[],'spectra':[],'uniform_bounds':[]}
    for s,p in [(3,109),(4,P),(8,P),(16,P)]:
        n=s*s;ww=seed_arrays(s,p)
        if n in pinned:assert ww==pinned[n]
        G=greens(s,ww,p);alpha=pow(4,-1,p)
        stages=[sum(layer)*alpha%p for layer in G];T=stages[1]@stages[0]%p
        omega=pow(3,(p-1)//n,p);F=np.array([[pow(omega,i*j,p) for j in range(n)] for i in range(n)],dtype=np.int64)
        for ori in ('H','V'):
            ai=(2,3) if ori=='H' else (0,1);bi=(0,1) if ori=='H' else (2,3)
            A=(G[0][ai[0]]+G[0][ai[1]])*alpha%p;B=(G[1][bi[0]]+G[1][bi[1]])*alpha%p
            ranks=[];reachable=[]
            for r in range(s):
                for c in range(s):
                    W,rows,cols,k=block(F,A,B,s,ori,r,c);ranks.append(rank(W%p,p))
                    V,rows,cols,k=block(T,A,B,s,ori,r,c)
                    assert np.array_equal(V%p,np.outer(stages[1][rows,k],stages[0][k,cols])%p)
                    reachable.append(rank(V%p,p))
            assert set(ranks)=={s-1};assert set(reachable)=={1}
            W=block(F,A,B,s,ori,0,0)[0]%p;det=det2(W,p)
            ref=next(x for x in expected['certificates'] if x['N']==n and x['input_orientation']==ori)
            assert det==ref['minor_det_mod_p'];assert W[:2,:2].tolist()==ref['minor_matrix']
            record={'N':n,'p':p,'orientation':ori,'first_minor_matrix':W[:2,:2].tolist(),'first_minor':det,'all_fourier_block_ranks':sorted(set(ranks)),'all_original_network_block_ranks':sorted(set(reachable))}
            if s>3:
                poly=exact_minor(s,ww,ori)
                exactref=next(x for x in expected['cyclotomic'] if x['N']==n and x['orientation']==ori)
                refpoly={x['power']:Fraction(int(x['numerator']),int(x['denominator'])) for x in exactref['coefficient_vector_sparse']}
                assert poly==refpoly and poly
                value=sum((v.numerator%p)*pow(v.denominator%p,-1,p)*pow(omega,k,p) for k,v in poly.items())%p
                assert value==det
                record.update(exact_cyclotomic_matches=True,exact_nonzero_coefficient_count=len(poly),exact_coefficients=[{'power':k,'numerator':str(v.numerator),'denominator':str(v.denominator)} for k,v in sorted(poly.items())])
            results['pinned'].append(record)
            # All four adjustable Green weights zero: each new resolvent is I,
            # both selected axis sums are I/2, so all off-rook variable bridges vanish.
            X=(A+2*alpha*np.eye(n,dtype=np.int64))%p
            Y=(B+2*alpha*np.eye(n,dtype=np.int64))%p
            Tzero=Y@X%p
            for r in range(s):
                for c in range(s):
                    assert not np.any(block(Tzero,A,B,s,ori,r,c)[0]%p)
            results['reachable_controls'].append({'N':n,'orientation':ori,'mode':'all_four_editable_Green_weight_arrays_zero','all_block_ranks':[0],'Green_inverse_domain':'all four pencils equal I'})
        print('pinned',n,'passed',flush=True)
    # Independent exact arbitrary-supported and zero-bridge controls, both orientations.
    p=P;rng=np.random.default_rng(20261010)
    for s in (3,4,7):
        n=s*s;x=np.arange(n)//s;y=np.arange(n)%s
        hmask=y[:,None]==y[None,:];vmask=x[:,None]==x[None,:]
        for ori in ('H','V'):
            hin,vout=(hmask,vmask) if ori=='H' else (vmask,hmask)
            # Fixed A,B deliberately general rook-supported, including both axes.
            rook=hmask|vmask;A=rng.integers(0,p,size=(n,n),dtype=np.int64)*rook;B=rng.integers(0,p,size=(n,n),dtype=np.int64)*rook
            for mode in ('arbitrary','zero_unknown_bridge','zero_fixed_bridge'):
                H=rng.integers(0,p,size=(n,n),dtype=np.int64)*hin;V=rng.integers(0,p,size=(n,n),dtype=np.int64)*vout
                AA=A.copy();BB=B.copy()
                if mode=='zero_unknown_bridge':V=(-BB*vout)%p
                if mode=='zero_fixed_bridge':AA=np.diag(np.diag(AA))
                X=(AA+H)%p;Y=(BB+V)%p;T=Y@X%p;rs=[]
                for r in range(s):
                    for c in range(s):
                        W,rows,cols,k=block(T,AA,BB,s,ori,r,c)
                        assert np.array_equal(W%p,np.outer(Y[rows,k],X[k,cols])%p)
                        rs.append(rank(W%p,p))
                assert max(rs)<=1
                if mode=='zero_unknown_bridge':assert set(rs)=={0}
                results['reachable_controls'].append({'s':s,'orientation':ori,'mode':mode,'all_block_ranks':sorted(set(rs))})
    # Sine Gram matrices and singular-tail diagnostics. These support, not replace, the exact proofs.
    for s in range(3,34):
        a=np.arange(1,s);J=np.sin(2*np.pi*a[:,None]*a[None,:]/s);Pmat=np.eye(s-1)[np.array([s-int(i)-1 for i in a])]
        err=float(np.max(abs(J@J.T-s/2*(np.eye(s-1)-Pmat))))
        sv=np.linalg.svd(J,compute_uv=False);r=(s-1)//2 if s%2 else (s-2)//2
        assert err<1e-9 and np.count_nonzero(sv>1e-8)==r
        assert np.max(abs(sv[:r]-math.sqrt(s)))<1e-9
        results['spectra'].append({'s':s,'rank':r,'gram_max_error':err})
    for s in (3,4,5,6,7,8,11,16,32):
        total=0.;diagtail=0.;margins=[]
        for x in range(s):
            for b in range(s):
                y=np.array([i for i in range(s) if i!=b]);a=np.array([i for i in range(s) if i!=x])
                C=np.exp(2j*np.pi*(x*b/s+y[:,None]*a[None,:]/s+y[:,None]*b/s**2))
                sv=np.linalg.svd(C.imag,compute_uv=False);tail=float(np.sum(sv[2:]**2));total+=tail
                margins.append(tail-max(0.,s*s/2-5*s))
                z=np.linalg.svd(C,compute_uv=False);diagtail+=float(np.sum(z[1:]**2))
                assert np.max(abs(z-np.array([math.sqrt(s)]*(s-2)+[1.])))<1e-9
        assert min(margins)>-1e-9
        diagonal=math.sqrt(diagtail)/s**2;assert abs(diagonal-math.sqrt(1-3/s+1/s**2))<1e-10
        results['uniform_bounds'].append({'s':s,'certified_simple_formula':math.sqrt(max(0.,.5-5/s)),'numerical_imaginary_rank_two_tail':math.sqrt(total)/s**2,'diagonal_formula_control':diagonal,'minimum_per_block_tail_margin':min(margins)})
    # Compare the preserved mathematical diagnostics; source provenance is separate.
    advertised=json.loads((SRC/'NUMERICAL_COMPARISON.json').read_text())
    for row in advertised['numerical_global_real_phase_rank2_bounds']:
        s=row['side'];fresh=next(x for x in results['uniform_bounds'] if x['s']==s)
        assert abs(row['uniform_real_background_rank2_SVD_lower_bound_numeric']-fresh['numerical_imaginary_rank_two_tail'])<1e-10
    results['all_assertions_passed']=True
    (BASE/'FRESH_PHASE22_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print('all independent assertions passed',flush=True)

if __name__=='__main__':run()
