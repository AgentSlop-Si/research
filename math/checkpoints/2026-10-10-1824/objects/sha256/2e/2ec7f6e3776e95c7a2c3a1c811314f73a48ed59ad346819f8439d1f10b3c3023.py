"""Fresh independent finite exact controls; no inherited programs imported/executed."""
from pathlib import Path
from math import gcd
import hashlib, json
import sympy as sp

OUT=Path(__file__).resolve().parent

def trim(f,p):
    f=[x%p for x in f]
    while len(f)>1 and f[-1]==0: f.pop()
    return f

def rem(f,g,p):
    f=trim(f,p); g=trim(g,p); ig=pow(g[-1],-1,p)
    while len(f)>=len(g) and f!=[0]:
        j=len(f)-len(g); c=f[-1]*ig%p
        for i,v in enumerate(g): f[j+i]=(f[j+i]-c*v)%p
        f=trim(f,p)
    return f

def pgcd(f,g,p):
    f=trim(f,p); g=trim(g,p)
    while g!=[0]: f,g=g,rem(f,g,p)
    return [(x*pow(f[-1],-1,p))%p for x in f] if f!=[0] else [0]

def padd(f,g,p,sign=1):
    return trim([(f[i] if i<len(f) else 0)+sign*(g[i] if i<len(g) else 0)
                 for i in range(max(len(f),len(g)))],p)

def pmul(f,g,p):
    z=[0]*(len(f)+len(g)-1)
    for i,x in enumerate(f):
        for j,y in enumerate(g): z[i+j]=(z[i+j]+x*y)%p
    return trim(z,p)

def pdiv(f,g,p):
    f=trim(f,p); g=trim(g,p); inv=pow(g[-1],-1,p)
    q=[0]*max(1,len(f)-len(g)+1)
    while len(f)>=len(g) and f!=[0]:
        j=len(f)-len(g); c=f[-1]*inv%p; q[j]=c
        for i,v in enumerate(g): f[j+i]=(f[j+i]-c*v)%p
        f=trim(f,p)
    return trim(q,p),f

def pinv(f,g,p):
    # Extended Euclid, independently compared to full axis-matrix elimination.
    r0,r1=g[:],rem(f,g,p); s0,s1=[0],[1]
    while r1!=[0]:
        q,r=pdiv(r0,r1,p)
        r0,r1=r1,r; s0,s1=s1,padd(s0,pmul(q,s1,p),p,-1)
    assert len(r0)==1 and r0[0]
    return rem([x*pow(r0[0],-1,p)%p for x in s0],g,p)

def corrected_test(g,N,p):
    h=g[:]; removed_one=False
    if sum(h)%p==0:
        h,r=pdiv(h,[-1,1],p); assert r==[0]
        removed_one=True
        if sum(h)%p==0: return {'applicable':False,'reason':'root one is repeated'}
    m=len(h)-1; d=N-m
    if 2*m<=N-1 or h[0]==0 or pgcd(h,h[::-1],p)!=[1]:
        return {'applicable':False,'reason':'residual degree, constant, or reciprocal guard fails'}
    R=rem(pmul([h[0]]*N,pinv(h[::-1],h,p),p),h,p)
    failed_axis=R[0]==0 and len(R)-1<=d-1
    return {'applicable':True,'removed_simple_root_one':removed_one,'residual_degree':m,
            'inverse_residue':R,'predicted_axis_rank':N-int(failed_axis)}

def rref(mat,p):
    a=[[x%p for x in row] for row in mat]; nr=len(a); nc=len(a[0]) if nr else 0
    piv=[]; row=0; labels=list(range(nr)); selected=[]
    for col in range(nc):
        j=next((j for j in range(row,nr) if a[j][col]),None)
        if j is None: continue
        a[row],a[j]=a[j],a[row]; labels[row],labels[j]=labels[j],labels[row]
        selected.append(labels[row]); s=pow(a[row][col],-1,p)
        a[row]=[s*x%p for x in a[row]]
        for k in range(nr):
            if k!=row and a[k][col]:
                s=a[k][col]; a[k]=[(x-s*y)%p for x,y in zip(a[k],a[row])]
        piv.append(col); row+=1
        if row==nr: break
    return a,piv,selected

def kernel(mat,p):
    a,piv,selected=rref(mat,p); n=len(a[0]); frees=[j for j in range(n) if j not in piv]
    basis=[]
    for col in frees:
        v=[0]*n; v[col]=1
        for i,j in enumerate(piv): v[j]=-a[i][col]%p
        basis.append(v)
    return basis,piv,selected

def rank(mat,p): return len(rref(mat,p)[1])

def det(mat,p):
    a=[row[:] for row in mat]; d=1
    for i in range(len(a)):
        k=next((k for k in range(i,len(a)) if a[k][i]%p),None)
        if k is None: return 0
        if k!=i: a[i],a[k]=a[k],a[i]; d=-d
        z=a[i][i]%p; d=d*z%p; zi=pow(z,-1,p)
        for k in range(i+1,len(a)):
            c=a[k][i]*zi%p
            for j in range(i,len(a)): a[k][j]=(a[k][j]-c*a[i][j])%p
    return d%p

def prime_and_q(N):
    # Explicit bounded arithmetic search; every chosen q has exact order N.
    p=next((k*N+1 for k in range(1,201) if sp.isprime(k*N+1)),None)
    assert p is not None
    q=pow(int(sp.primitive_root(p)),(p-1)//N,p)
    assert pow(q,N,p)==1 and all(pow(q,N//ell,p)!=1 for ell in sp.factorint(N))
    return p,q

def gaussian(n,b,q,p):
    if b<0 or b>n: return 0
    z=1
    for j in range(1,b+1): z=z*(1-pow(q,n-b+j,p))*pow((1-pow(q,j,p))%p,-1,p)%p
    return z

def recurrence(N,d,p,q):
    m=N-d; h=pow(4,-1,N); qi=pow(q,-1,p); rows=[]; labs=[]
    for b in range(1,d-1):
        T=pow(gaussian(2*b,b,qi,p),-1,p)
        seq=[]
        for j in range(1,N-b):
            F=pow(q,h*(j+b)**2%N,p)
            Gminus=gaussian(N-j+b,b,qi,p) if N-j+b<=N-1 else 0
            Gplus=gaussian(j+b,b,q,p)
            seq.append((F-T*Gminus)*pow(Gplus,-1,p)%p)
        for a in range(1,d-b):
            row=seq[a-1:a+m]; assert len(row)==m+1
            rows.append(row); labs.append([a,b])
    return rows,labs

def axis(g,N,p):
    m=len(g)-1; powers=[]; v=[1]+[0]*(m-1)
    for j in range(N):
        powers.append(v)
        v=rem([0]+v,g,p); v=v+[0]*(m-len(v))
    return [powers[a]+[1]+powers[-a%N] for a in range(N)]

def degree_gcd_basis(basis,p):
    z=[0]
    for b in basis: z=pgcd(z,b,p)
    return z

def monic_trials(basis,p):
    pivot=next((i for i,v in enumerate(basis) if v[-1]),None)
    if pivot is None: return []
    base=[x*pow(basis[pivot][-1],-1,p)%p for x in basis[pivot]]
    dirs=[]
    for i,v in enumerate(basis):
        if i!=pivot: dirs.append([(a-v[-1]*b)%p for a,b in zip(v,base)])
    trials=[]
    # Fixed budget: baseline plus six deterministic coefficient assignments.
    for k in range(7):
        co=[0 if k==0 else (j+1)**k%p for j in range(len(dirs))]
        g=[(base[a]+sum(co[j]*v[a] for j,v in enumerate(dirs)))%p for a in range(len(base))]
        trials.append((co,g))
    return trials

def run_case(N,d):
    p,q=prime_and_q(N); m=N-d; A,labs=recurrence(N,d,p,q); basis,piv,rs=kernel(A,p)
    bound=min((d-1)*(d-2)//2,4*d-11)
    assert len(piv)<=bound
    fixed=degree_gcd_basis(basis,p)
    samples=[]
    for co,g in monic_trials(basis,p):
        deriv=[j*g[j]%p for j in range(1,len(g))]
        recg=pgcd(g,g[::-1],p)
        ax=axis(g,N,p); axrank=rank(ax,p)
        criterion=corrected_test(g,N,p)
        if criterion['applicable']: assert criterion['predicted_axis_rank']==axrank
        axpiv=rref(ax,p)[1]
        axminor=det([[row[j] for j in axpiv] for row in ax],p) if axrank==N else None
        samples.append({'free_coefficients':co,'g':g,'constant':g[0],'g_at_one':sum(g)%p,
                        'derivative_gcd':pgcd(g,deriv,p),'reciprocal_gcd':recg,'axis_rank':axrank,
                        'axis_pivot_columns':axpiv,'axis_minor':axminor,'corrected_criterion':criterion,
                        'all_recurrences_zero':all(sum(a*b for a,b in zip(row,g))%p==0 for row in A)})
    return {'N':N,'d':d,'m':m,'p':p,'q':q,'matrix_rank':len(piv),'rank_bound':bound,
            'rank_saturates_analytic_bound':len(piv)==bound,'kernel_dimension':len(basis),
            'kernel_fixed_gcd_mod_p':fixed,'all_basis_vanish_at_one':all(sum(v)%p==0 for v in basis),
            'matrix':A,'row_labels':labs,'pivot_columns':piv,'selected_rows':rs,
            'defining_minor':det([[A[i][j] for j in piv] for i in rs],p),
            'basis':basis,'samples':samples}

def exact_counterexamples():
    t=sp.symbols('t'); results=[]
    for N,r in [(5,1),(7,1),(9,1),(15,3),(25,5),(35,7)]:
        n=N//r; g=2+sum(t**(j*r) for j in range(1,n-1)); m=sp.degree(g,t)
        H=sp.Poly(g,t).all_coeffs()[::-1]; H=sum(co*t**(m-j) for j,co in enumerate(H))
        A=t**(N-r)+t**r-2; J=sp.expand(t**N*A.subs(t,1/t)+A.subs(t,0)*(1-t**N))
        assert sp.gcd(g,H)==1 and sp.gcd(g,sp.diff(g,t))==1
        assert sp.rem(A,g,t)==0 and J==A and A.subs(t,1)==0 and m>(N-1)/2
        M=[]
        for a in range(N):
            v=sp.Poly(sp.rem(t**a,g,t),t); w=sp.Poly(sp.rem(t**((-a)%N),g,t),t)
            M.append([v.nth(i) for i in range(m)]+[1]+[w.nth(i) for i in range(m)])
        rankQ=sp.Matrix(M).rank()
        assert rankQ==N-1
        invR=sp.rem(2*sum(t**j for j in range(N))*sp.invert(H,g,t),g,t)
        assert invR.subs(t,0)==0 and sp.degree(invR,t)<=N-m-1
        results.append({'N':N,'m':int(m),'d':int(N-m),'r':r,'g':str(g),'H':str(H),'A':str(A),
                        'gcd_g_H':1,'squarefree':True,'g_divides_A':True,'J_A_equals_A':True,
                        'A_at_one':0,'axis_rank_Q':rankQ,'inverse_residue':str(invR)})
    return results

if __name__=='__main__':
    cases=[(13,5),(17,6),(21,4),(27,4),(35,5),(35,9),(45,7),(45,11),(51,7),(51,12),(55,8),(55,13),(65,9),(65,15),(75,10),(75,17)]
    out={'status':'PASS','independent_fresh_code':True,'inherited_code_imported_or_executed':False,
         'bounded_cases':cases,'exact_counterexamples':exact_counterexamples(),'recurrence_cases':[]}
    for N,d in cases:
        c=run_case(N,d); out['recurrence_cases'].append(c)
        print(N,d,c['matrix_rank'],c['kernel_dimension'],c['kernel_fixed_gcd_mod_p'],
              [(s['reciprocal_gcd'],s['axis_rank']) for s in c['samples'][:2]],flush=True)
    f=OUT/'FRESH_AXIS_CONTROLS.json'; f.write_text(json.dumps(out,indent=2)+'\n')
    print(f)
