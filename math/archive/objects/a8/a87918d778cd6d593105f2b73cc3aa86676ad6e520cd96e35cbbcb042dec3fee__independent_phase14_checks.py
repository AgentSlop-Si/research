"""Independent audit checks. No uploaded module is imported or executed."""
import ast, hashlib, json, math, pathlib, zipfile, io
import numpy as np
BASE=pathlib.Path(__file__).parent
SOURCE=BASE/'extracted/fft_hero1_phase14'

def mm(A,B,p):
    return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]

def inv(A,p):
    n=len(A);T=[list(row)+[int(j==i) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(k for k in range(j,n) if T[k][j]%p)
        T[j],T[k]=T[k],T[j]
        t=pow(T[j][j],-1,p);T[j]=[v*t%p for v in T[j]]
        for k in range(n):
            if k==j:continue
            t=T[k][j];T[k]=[(x-t*y)%p for x,y in zip(T[k],T[j])]
    return [r[n:] for r in T]

def root(order,p):
    for r in range(2,p):
        if pow(r,order,p)==1 and all(pow(r,order//d,p)!=1 for d in range(2,order+1) if order%d==0):return r
    raise ValueError('No root')

def recur_kernel(G,M,a,beta,z,p):
    """Derive each coefficient impulse response by the signed cyclic recurrence."""
    K=G//M;out=[[0]*K for _ in range(G)];normal=pow(2,-1,p)
    for r in range(K):
        force=[];phase=[]
        for j in range(G):
            k=a*j%G
            ph=pow(z,(a*j*(j-1)//2+beta*j)%G,p)
            # Fourier of one coefficient impulse, before and after block-edge shift.
            h=(pow(z,(-M*k*r)%G,p)-pow(z,(-M*(k+beta)-a*M*(M-1)//2-M*(k+a*M)*r)%G,p))%p
            force.append(h*pow(ph,-1,p)%p);phase.append(ph)
        state=sum(force)*normal%p
        for j in range(G):
            out[a*j%G][r]=phase[j]*state%p
            state=(state-force[j])%p
    return out

def verify_full(N,M,p):
    G=N&-N;m=N//G;K=G//M;zN=root(N,p);z=pow(zN,m,p)
    E=[(K*u*(u+1)//2+u)%G for u in range(M)]
    W=[[pow(z,-i*e%G,p) for i in range(M)] for e in E]
    Ws=[[pow(z,i*e%G,p) for e in E] for i in range(M)]
    Gamma=mm(Ws,W,p);C=mm(inv(Gamma,p),Ws,p)
    badW=[[pow(z,(-i*(e-u))%G,p) for i in range(M)] for u,e in enumerate(E)]
    badC=inv(badW,p)
    assert mm(W,C,p)==[[int(i==j) for j in range(M)] for i in range(M)]
    assert all(Gamma[i][j]==Gamma[i+1][j+1] for i in range(M-1) for j in range(M-1))
    mismatches=0;direct_decoder_entries=0;mutation_mismatches=0;chart_mutation_mismatches=0
    for s in range(m):
        kernels=[]
        for i in range(M):
            a=1+i*K;beta=3*s+i*(K+1)
            T=recur_kernel(G,M,a,beta,z,p);kernels.append(T)
            for k in range(G):
                for r in range(K):
                    direct=sum(pow(z,(-a*u*(u-1)//2-(a*M*r+beta)*u-k*(r*M+u))%G,p) for u in range(M))%p
                    assert T[k][r]==direct
                    direct_decoder_entries+=1
        for r in range(K):
            for u in range(M):
                coeff=[C[i][u]*pow(z,(u*(u-1)//2+(M*r+3*s)*u)%G,p)%p for i in range(M)]
                badcoeff=[badC[i][u]*pow(z,(u*(u-1)//2+(M*r+3*s)*u)%G,p)%p for i in range(M)]
                n=m*(r*M+u)+s
                for k1 in range(G):
                    y=sum(coeff[i]*kernels[i][k1][r] for i in range(M))%p
                    for k2 in range(m):
                        k=k1+G*k2
                        actual=y*pow(zN,(-k*s)%N,p)%p
                        expected=pow(zN,(-k*n)%N,p)
                        bady=sum(badcoeff[i]*kernels[i][k1][r] for i in range(M))%p
                        chart_mutation_mismatches+=(bady*pow(zN,(-k*s)%N,p)%p)!=expected
                        mismatches+=actual!=expected
                        # A necessary genuine output mutation check, not just changed inverses.
                        mutant=y*pow(zN,(-k*s+1)%N,p)%p
                        mutation_mismatches+=mutant!=expected
    assert mismatches==0 and mutation_mismatches>0 and chart_mutation_mismatches>0
    return {'N':N,'G':G,'M':M,'prime':p,'full_fourier_entries':N*N,'decoder_entries':direct_decoder_entries,'mismatches':mismatches,'output_phase_mutation_mismatches':mutation_mismatches,'wrong_chart_phase_mismatches':chart_mutation_mismatches}

def numerical_projections():
    rows=[];rng=np.random.default_rng(10314)
    for M,K,q in ((4,4,2),(8,16,2),(8,32,5),(16,128,4)):
        G=K*M;u=np.arange(M);i=np.arange(q);E=K*u*(u+1)//2+u
        W=np.exp(-2j*np.pi*np.outer(E/G,i));P=W@np.linalg.solve(W.conj().T@W,W.conj().T)
        x=rng.normal(size=M)+1j*rng.normal(size=M);c=np.linalg.solve(W.conj().T@W,W.conj().T@x)
        captured=np.vdot(W.conj().T@x,c).real
        lhs=np.linalg.norm(x-W@c)**2;rhs=np.vdot(x,x).real-captured
        # A proper fixed projection has worst-case error exactly 1, not sqrt(1-q/M).
        _,_,vh=np.linalg.svd(W.conj().T,full_matrices=True);h=vh[-1].conj();null_error=np.linalg.norm((np.eye(M)-P)@h)/np.linalg.norm(h)
        rows.append({'M':M,'K':K,'q':q,'projection_defect':float(np.linalg.norm(P@P-P)),'energy_identity_defect':float(abs(lhs-rhs)),'kernel_witness_relative_error':float(null_error),'maximum_coordinate_residual_squared':float(1-np.min(np.diag(P).real))})
        assert abs(null_error-1)<1e-12 and abs(lhs-rhs)<1e-10
    return rows

def conditioning():
    rows=[]
    for M in (2,4,8,16,32,64,128,256):
        T=[u*(u+1)//2%M for u in range(M)];assert len(set(T))==M
        for ratio in (1,2,4,8,16):
            K=M*ratio;G=K*M;u=np.arange(M,dtype=np.int64);E=(K*u*(u+1)//2+u)%G
            W=np.exp(-2j*np.pi*np.outer(E/G,np.arange(M)))
            sv=np.linalg.svd(W/math.sqrt(M),compute_uv=False)
            delta=math.expm1(math.pi*(M-1)**2/(2*K*M))
            if delta<1:assert sv[0]<=1+delta+1e-10 and sv[-1]>=1-delta-1e-10
            rows.append({'M':M,'K':K,'sigma_min_normalized':float(sv[-1]),'sigma_max_normalized':float(sv[0]),'delta_bound':delta,'gram_condition_estimate':float((sv[0]/sv[-1])**2),'gram_condition_bound':((1+delta)/(1-delta))**2 if delta<1 else None})
    return rows

def orbit_counts():
    rows=[]
    for M in (2,4,8,16,32):
        for K in (M,2*M,4*M):
            G=K*M;actual=sum(len({(1+i*K)*j%G for i in range(M)}) for j in range(G));formula=K*(2*M*M+1)//3
            assert actual==formula
            rows.append({'M':M,'K':K,'destinations':actual,'raw':M*G})
    return rows

def integrity():
    entries=[]
    for line in (SOURCE/'MANIFEST.sha256').read_text().splitlines():
        h,name=line.split(None,1);name=name.strip().lstrip('*');actual=hashlib.sha256((SOURCE/name).read_bytes()).hexdigest();entries.append({'name':name,'match':h==actual});assert h==actual
    syntax=[]
    for f in sorted(SOURCE.glob('*.py')):ast.parse(f.read_text(),filename=f.name);syntax.append(f.name)
    pred=zipfile.ZipFile(SOURCE/'PRIOR_v13_COMPLETE.zip');preserved=json.loads((SOURCE/'SOURCE_INTEGRITY.json').read_text())['preserved_source_modules']
    for name,d in preserved.items():
        path=next(n for n in pred.namelist() if n.endswith('/'+name));assert pred.read(path)==(SOURCE/name).read_bytes()
    return {'top_manifest_entries':len(entries),'all_manifest_entries_pass':True,'parsed_python_files':len(syntax),'preserved_v13_modules':len(preserved)}

result={'scope':'Independently authored mathematical checks; no uploaded code run','integrity':integrity(),'exact_full_rank':[verify_full(*case) for case in [(4,2,17),(48,4,97),(96,4,97),(128,8,257),(192,8,193),(384,8,769)]],'projection_checks':numerical_projections(),'conditioning_checks':conditioning(),'orbit_checks':orbit_counts()}
result['independent_full_fourier_entries']=sum(r['full_fourier_entries'] for r in result['exact_full_rank'])
result['independent_decoder_entries']=sum(r['decoder_entries'] for r in result['exact_full_rank'])
(BASE/'independent_phase14_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('conditioning_checks','orbit_checks')},indent=2))
