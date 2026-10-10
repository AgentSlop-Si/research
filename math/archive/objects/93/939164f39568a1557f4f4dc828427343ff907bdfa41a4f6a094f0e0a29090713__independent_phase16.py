"""Independent Phase16 mathematical audit. Never imports or runs supplied files.
Dense arithmetic is an oracle/checker, not an algorithmic complexity claim.
"""
import json
import math
from pathlib import Path
import numpy as np

SEED = 2026100916
rng = np.random.default_rng(SEED)

def entropy(A):
    p = abs(A)**2
    z = p > 0
    return float(-(p[z]*np.log2(p[z])).sum())

def fourier(n):
    # Reduce the integer exponent modulo n before evaluating the complex root.
    j = np.arange(n)
    return np.exp((2j*np.pi/n)*((j[:,None]*j[None,:]) % n))/np.sqrt(n)

def cycles(n,b):
    unused=set(range(n)); out=[]
    while unused:
        start=min(unused); c=[]; k=start
        while k in unused:
            unused.remove(k); c.append(k); k=k*(1+b)%n
        assert k==start
        out.append(c)
    return out

def direct_factor_audit(n,b):
    """Build R from direct stream regrouping, without a folding executor."""
    L=n//b; orb=cycles(n,b)
    R=np.zeros((n,n),complex); O=np.zeros((n,n),complex)
    phase=np.ones(n,complex); degrees=[]; frequencies=[]; cursor=0
    for c in orb:
        d=len(c); g=L//d; u=c[0]//g
        O[cursor:cursor+d,cursor:cursor+d]=fourier(d)
        for e in range(d):
            a=(e*pow(u,-1,d))%d if d>1 else 0
            carry=(u*a-e)//d
            for r in range(g):
                col=(a+d*r)*b+(u*g)%b
                R[cursor+e,col]=np.exp(2j*np.pi*((carry+u*r)%b)/b)/np.sqrt(g)
            phase[cursor+e]=np.exp(2j*np.pi*(e*g)/n)
            degrees.append(g)
        frequencies += c; cursor += d
    B=np.kron(np.eye(L),fourier(b))
    inp=[a+L*h for a in range(L) for h in range(b)]
    P=np.eye(n)[inp,:]
    assembled=(O@(phase[:,None]*R)@B@P)[np.argsort(frequencies)]
    err=float(abs(assembled-fourier(n)).max())
    gram=float(abs(R@R.conj().T-np.eye(n)).max())
    support=(abs(R)>1e-12).sum(axis=1)
    assert list(support)==degrees
    assert err<1e-11 and gram<1e-11
    E=[entropy(B),entropy(R),entropy(O)]
    expected=[n*math.log2(b),n-b,b+n*(math.log2(L)-1)]
    assert max(abs(x-y) for x,y in zip(E,expected))<1e-8
    return dict(N=n,B=b,entropies=E,expected=expected,
                full_DFT_error=err,residual_gram_error=gram,
                total_gate_optimum=n*int(math.log2(n))//2)

def circuit_audit(n,b):
    """Recursive even/odd FFT wiring, independent of supplied iterative schedule."""
    L=n//b; A=np.eye(n,dtype=complex)[[a+L*h for a in range(L) for h in range(b)]]
    counts={"base":0,"fold":0,"orbit":0}; gains=[]; max_overlap=0.
    def gate(i,j,w,kind):
        nonlocal max_overlap
        rows=A[[i,j]].copy(); old=entropy(rows)
        max_overlap=max(max_overlap,float(np.minimum(abs(rows[0])**2,abs(rows[1])**2).sum()))
        A[i]=(rows[0]+w*rows[1])/np.sqrt(2)
        A[j]=(rows[0]-w*rows[1])/np.sqrt(2)
        gains.append(entropy(A[[i,j]])-old); counts[kind]+=1
    def fft(wires,kind):
        if len(wires)==1: return wires
        even=fft(wires[::2],kind); odd=fft(wires[1::2],kind)
        for k,(i,j) in enumerate(zip(even,odd)):
            gate(i,j,np.exp(2j*np.pi*k/len(wires)),kind)
        return even+odd
    registers={}
    for a in range(L):
        order=fft(list(range(a*b,(a+1)*b)),"base")
        for q,w in enumerate(order): registers[L,a,q]=w
    d=L
    while d>1:
        for a in range(d//2):
            for q in range(b//2):
                i=registers.pop((d,a,2*q)); j=registers.pop((d,a+d//2,2*q))
                gate(i,j,np.exp(2j*np.pi*q/b),"fold")
                registers[d//2,a,q]=i; registers[d//2,a,q+b//2]=j
        d//=2
    out=np.empty_like(A)
    for c in cycles(n,b):
        d=len(c); g=L//d; u=c[0]//g; wires=[]
        for e in range(d):
            a=(e*pow(u,-1,d))%d if d>1 else 0
            carry=(u*a-e)//d
            w=registers[d,a,u]
            A[w]*=np.exp(2j*np.pi*(carry/b+e*g/n)); wires.append(w)
        ordered=fft(wires,"orbit")
        out[c]=A[ordered]
    error=float(abs(out-fourier(n)).max())
    assert error<1e-11 and max(abs(x-2) for x in gains)<1e-10
    assert max_overlap<1e-24
    assert len(gains)==n*int(math.log2(n))//2
    return dict(N=n,B=b,counts=counts,gate_count=len(gains),
                min_entropy_gain=min(gains),max_entropy_gain=max(gains),
                max_input_support_overlap=max_overlap,DFT_error=error)

def givens(a,b):
    r=np.hypot(abs(a),abs(b))
    if r==0: return np.eye(2,dtype=complex)
    return np.array([[a.conjugate(),b.conjugate()],[-b,a]],complex)/r

def compile_rankone(U,pivot="adaptive"):
    """Two sweeps; robust prefix pivot handles zero-generator degeneracies."""
    A=U.copy(); n=len(A); operations=[]
    def eliminate(i,j,col):
        G=givens(A[i,col],A[j,col]); A[[i,j]]=G@A[[i,j]]
        operations.append((i,j,G))
    for k in range(n-1,1,-1):
        if pivot=="nearest": col=k-2
        else:
            mass=abs(A[k-1,:k-1])**2+abs(A[k,:k-1])**2
            col=int(np.argmax(mass))
        eliminate(k-1,k,col)
    hess=float(abs(np.tril(A,-2)).max())
    for j in range(n-1): eliminate(j,j+1,j)
    diagonal=np.diag(A).copy()
    off=float(abs(A-np.diag(diagonal)).max())
    assembled=np.diag(diagonal)
    for i,j,G in operations[::-1]: assembled[[i,j]]=G.conj().T@assembled[[i,j]]
    return assembled,dict(gates=len(operations),hessenberg_error=hess,
        diagonal_error=off,reconstruction_error=float(abs(assembled-U).max()),
        phase_modulus_error=float(abs(abs(diagonal)-1).max()))

def cayley(A,alpha):
    I=np.eye(len(A),dtype=complex)
    # Solve, rather than explicitly forming an inverse.
    return 2*np.linalg.solve(I-1j*alpha*A,I)-I

def path_audits():
    cases=[]
    for n in [2,3,4,8,16,32,64,128]:
        for mode in ["real_signed","split","hermitian_diagonal"]:
            weights=rng.uniform(.25,1.75,n-1)*rng.choice([-1,1],n-1)
            if mode=="split" and n>3: weights[n//2-1]=0
            if mode=="hermitian_diagonal":
                weights=weights*np.exp(1j*rng.uniform(-np.pi,np.pi,n-1))
            A=np.diag(weights,1)+np.diag(np.conj(weights),-1)
            if mode=="hermitian_diagonal": A += np.diag(rng.uniform(-1,1,n))
            for alpha in [0.,-2.,1/32,.5,2.,float(n),float(n*n),1e-9]:
                U=cayley(A,alpha); unit=float(abs(U@U.conj().T-np.eye(n)).max())
                rebuilt,stats=compile_rankone(U)
                stats.update(N=n,mode=mode,alpha=alpha,unitarity_error=unit)
                # Solves at larger strengths may accumulate ordinary floating-point error.
                assert unit<1e-8 and stats['reconstruction_error']<1e-8
                assert stats['diagonal_error']<1e-8 and stats['gates']==2*n-3
                if mode!="hermitian_diagonal":
                    stats['determinant_one_error']=float(abs(np.linalg.det(U)-1))
                    assert stats['determinant_one_error']<1e-8
                cases.append(stats)
    # Exact signed permutation: global strict-lower generator exists, nearest-pivot fails.
    U=np.eye(4,dtype=complex); U[[0,3]]=U[[3,0]]
    _,nearest=compile_rankone(U,pivot="nearest")
    _,adaptive=compile_rankone(U,pivot="adaptive")
    assert nearest['hessenberg_error']==1 and adaptive['reconstruction_error']==0
    return cases,dict(matrix=U.real.tolist(),nearest=nearest,adaptive=adaptive)

def haar(m):
    # Explicit orthonormal basis functions, independent of recursion executor.
    H=np.empty((m,m)); H[:,0]=1/np.sqrt(m)
    for level in range(int(math.log2(m))):
        length=m//(2**level)
        for node in range(2**level):
            column=2**level+node; lo=node*length
            H[:,column]=0
            H[lo:lo+length//2,column]=1/np.sqrt(length)
            H[lo+length//2:lo+length,column]=-1/np.sqrt(length)
    return H

def haar_circuit(m):
    A=np.eye(m,dtype=complex); active=[0]; wavelet=1; gates=0
    while len(active)<m:
        next_active=[]
        for current in active:
            first=A[current].copy(); second=A[wavelet].copy()
            A[current]=(first+second)/np.sqrt(2)
            A[wavelet]=(first-second)/np.sqrt(2)
            next_active.extend([current,wavelet]); wavelet+=1; gates+=1
        active=next_active
    return A[active],gates

def binary_entropy(p):
    return sum(-x*math.log2(x) for x in [p,1-p] if x>0)

def stage_audits():
    records=[]
    for n in [4,8,16,32,64,128]:
        m=n//2; H=haar(m); Hc,ng=haar_circuit(m)
        assert ng==m-1 and abs(Hc-H).max()<1e-12
        for eps in [0.,1/512,-.5,1.,float(n),float(n*n)]:
            p=eps*eps/(1+eps*eps)
            I=np.eye(m); R=np.block([[np.zeros((m,m)),H],[H.T,np.zeros((m,m))]])
            V=(np.eye(n)+1j*eps*R)/np.hypot(1.,eps)
            W=np.block([[Hc,np.zeros((m,m))],[np.zeros((m,m)),I]])
            J=np.block([[I,1j*eps*I],[1j*eps*I,I]])/np.hypot(1.,eps)
            Vc=W@J@W.conj().T
            components=[]
            for alpha in [-n,n*n]:
                edge=rng.uniform(.5,1.5,n-1)*rng.choice([-1,1],n-1)
                A=np.diag(edge,1)+np.diag(edge,-1)
                permutation=rng.permutation(n)
                C=cayley(A,float(alpha)); Cc,info=compile_rankone(C)
                components.append((C[np.ix_(permutation,permutation)],Cc[np.ix_(permutation,permutation)],info))
            S=V@components[0][0]@components[1][0]
            Sc=Vc@components[0][1]@components[1][1]
            err=float(abs(S-Sc).max())
            E=entropy(V); predicted=n*binary_entropy(p)+2*p*(n-2)
            gates=sum(c[2]['gates'] for c in components)+2*ng+m
            assert err<1e-9 and gates==11*n//2-8
            assert abs(E-predicted)<1e-8 and abs(entropy(H)-2*(m-1))<1e-9
            assert abs(np.linalg.det(S)-1)<1e-8
            records.append(dict(N=n,epsilon=eps,alphas=[-n,n*n],gates=gates,
                                full_matrix_error=err,inverse_matrix_error=float(abs(S.conj().T-Sc.conj().T).max()),
                                V_entropy=E,predicted_V_entropy=predicted,
                                determinant_one_error=float(abs(np.linalg.det(S)-1))))
    return records

def random_gate_checks():
    records=[]
    for n in [4,8,16,32]:
        A=np.eye(n,dtype=complex); lo=2.; hi=-2.
        for step in range(10*n):
            i,j=rng.choice(n,2,replace=False)
            X=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            Q,_=np.linalg.qr(X)
            old=entropy(A[[i,j]])
            A[[i,j]]=Q@A[[i,j]]
            gain=entropy(A[[i,j]])-old; lo=min(lo,gain); hi=max(hi,gain)
            assert abs(gain)<=2+1e-10
        records.append(dict(N=n,gates_tested=10*n,min_gain=lo,max_gain=hi))
    return records

def workspace_checks():
    records=[]
    for n in [4,8,16]:
        m=3*n
        A=np.vstack([np.eye(n,dtype=complex),np.zeros((m-n,n),complex)])
        maximum=-2.; minimum=2.
        for step in range(20*m):
            i,j=rng.choice(m,2,replace=False)
            X=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            Q,_=np.linalg.qr(X)
            mass=float((abs(A[[i,j]])**2).sum())
            before=entropy(A[[i,j]])
            A[[i,j]]=Q@A[[i,j]]
            gain=entropy(A[[i,j]])-before
            assert abs(gain)<=mass+1e-10 and mass<=2+1e-10
            maximum=max(maximum,gain); minimum=min(minimum,gain)
        assert abs(A.conj().T@A-np.eye(n)).max()<1e-10
        records.append(dict(inputs=n,workspace_dimension=m,gates=20*m,min_gain=minimum,max_gain=maximum))
    return records

def determinant_checks():
    records=[]
    for n in [2,4,8,16,32,64,128]:
        actual=np.linalg.det(fourier(n))
        exponent=((n-1)*(3*n-2))%8
        expected=np.exp(1j*np.pi*exponent/4)
        error=float(abs(actual-expected))
        assert error<1e-10
        records.append(dict(N=n,actual=[actual.real,actual.imag],expected=[expected.real,expected.imag],error=error))
    return records

def approximate_checks():
    records=[]
    for n in [8,16,32,64]:
        F=fourier(n)
        for theta in [.01,.1,.3]:
            Q=np.eye(n,dtype=complex); c=math.cos(theta); s=math.sin(theta)
            Q[:2,:2]=[[c,s],[-s,c]]
            U=Q@F; err=float(np.linalg.norm(U-F,2))
            lower=n*(math.log2(n)-binary_entropy(err)-err*math.log2(n-1))
            assert entropy(U)+1e-10>=lower
            records.append(dict(N=n,operator_error=err,actual_entropy=entropy(U),
                                conservative_entropy_lower_bound=lower))
    return records

if __name__=='__main__':
    paths,degenerate=path_audits()
    sizes=[(16,8),(32,8),(64,8),(128,16),(256,16),(256,128),(512,32)]
    result=dict(audit_date='2026-10-09',seed=SEED,uploaded_code_executed=False,
                direct_factors=[direct_factor_audit(n,b) for n,b in sizes],
                gate_circuits=[circuit_audit(n,b) for n,b in sizes],
                path_cases=paths,degenerate_pivot_counterexample=degenerate,
                stage_cases=stage_audits(),random_gates=random_gate_checks(),
                approximate_cases=approximate_checks(),workspace_cases=workspace_checks(),determinant_cases=determinant_checks())
    result['summary']=dict(status='PASS',path_cases=len(paths),stage_cases=len(result['stage_cases']),
        max_path_reconstruction_error=max(x['reconstruction_error'] for x in paths),
        max_stage_error=max(x['full_matrix_error'] for x in result['stage_cases']),
        max_DFT_error=max(x['DFT_error'] for x in result['gate_circuits']),
        max_two_bit_deviation=max(max(abs(x['min_entropy_gain']-2),abs(x['max_entropy_gain']-2)) for x in result['gate_circuits']))
    Path(__file__).with_name('independent_phase16_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],indent=2))
    print('Nearest shared column is not a valid generic zero-case pivot:',json.dumps(degenerate))
