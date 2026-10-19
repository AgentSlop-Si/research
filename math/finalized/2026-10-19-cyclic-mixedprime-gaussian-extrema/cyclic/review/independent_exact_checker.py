#!/usr/bin/env python3
"""Fresh independent characteristic-zero audit; does not import or run author/history code."""
import hashlib, json, time
from pathlib import Path
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parent
CANDIDATE=Path('/workspace/shared/phase_cyclic_family_20261019_1001/PROOF.md')

def verify(n, full=False):
    start=time.monotonic()
    m=n//4; h=n//2; order=4*n
    K=sp.QQ.cyclotomic_field(order)
    zero,one,w=K.zero,K.one,K.unit
    p=[one]
    for j in range(1,order): p.append(p[-1]*w)
    assert p[-1]*w==one
    def z(j): return p[j%order]
    def rat(a,b=1): return K.convert(sp.Rational(a,b))
    cache={}
    def conj(x):
        if x in cache:return cache[x]
        cs=x.to_list(); result=zero
        for k,c in enumerate(cs):result+=K.convert(c)*z(-(len(cs)-1-k))
        cache[x]=result
        return result
    def mat(rows):return DomainMatrix(rows,(len(rows),len(rows[0])),K)
    def rows(M):return M.to_list()
    def conjugate(M):return mat([[conj(v) for v in row] for row in rows(M)])
    def equal(A,B):return A.to_dense()==B.to_dense()
    def zero_matrix(nr,nc):return mat([[zero]*nc for _ in range(nr)])
    I=DomainMatrix.eye(n,K).to_dense()
    q=[0 if j%2==0 else m*n-2+4*j for j in range(n)]
    b=[2*v%order for v in q]
    # Direct Fourier sums, using only the sum-index symmetry to avoid repeated sums.
    sums=[]
    for s in range(n):
        v=zero
        for l in range(n):v+=z(b[l]-4*s*l)
        sums.append(v*rat(1,n))
    C=[[sums[(j+k)%n] for k in range(n)] for j in range(n)]
    predicted=[[zero]*n for _ in range(n)]
    t=z(m*2*n-4)
    for k in range(n):
        for shift,weight in [(0,rat(1,2)),(h,rat(1,2)),(2,t*rat(1,2)),(h+2,-t*rat(1,2))]:
            predicted[(shift-k)%n][k]+=weight
    assert C==predicted,('Fourier support',n)
    MM=[[z(2)*C[j][k]*z(b[k]) for k in range(n)] for j in range(n)]
    M=mat(MM)
    assert equal(M*conjugate(M).transpose(),I),('M unitary',n)
    traces=[]; block_dims=[]
    specs=[(0,1,0,lambda j:one,2),(1,1,0,lambda j:z(m*2*n+8*j),-2),
           (0,-1,2,lambda j:z(m*2*n),-2),(1,-1,2,lambda j:z(8*j-8),2)]
    for epsilon,eta,shift,weight,phase in specs:
        inds=list(range(epsilon,h,2)); loc={j:k for k,j in enumerate(inds)}
        JJ=[[zero]*m for _ in range(m)]
        for col,j in enumerate(inds):
            target=(shift-j)%n
            coeff=weight(j)*(one if target<h else rat(eta))
            JJ[loc[target%h]][col]=coeff
        J=mat(JJ); Ib=DomainMatrix.eye(m,K).to_dense()
        assert equal(J*J,Ib),('involution',n,epsilon,eta)
        assert equal(conjugate(J).transpose(),J),('Hermitian',n,epsilon,eta)
        actual=[[MM[k][j]+rat(eta)*MM[k][j+h] for j in inds] for k in inds]
        assert equal(mat(actual),J*z(phase)),('block match',n,epsilon,eta)
        tr=sum((JJ[j][j] for j in range(m)),zero)
        expected=(1+int(m%2==0)) if len(traces) in (0,3) else int(m%2==1)
        assert tr==rat(expected),('trace',n,len(traces))
        traces.append(expected);block_dims.append(m)
    assert sum(traces)==4
    mult=[m+1+int(m%2==0),m+int(m%2==1),m-1-int(m%2==0),m-int(m%2==1)]
    assert min(mult)>=0 and sum(mult)==n
    assert sum(mult[:2])==h+2 and sum(mult[2:])==h-2
    gamma=z(sum(b[j] for j in range(0,n,2))-sum(b[j] for j in range(1,n,2)))
    assert gamma==-one
    # Check each weighted two-step cycle product independently.
    for parity in (0,1):
        j=parity; product=one; visited=[]
        while j not in visited:
            visited.append(j);product*=z(b[j]-b[(j-1)%n]);j=(j-2)%n
        assert j==parity and len(visited)==h and product==-one
    result={'N':n,'m':m,'field_order':order,'field_degree':K.mod.degree(),
            'direct_fourier_support':True,'four_block_involutions_and_matches':True,
            'block_traces':traces,'W_spectrum_multiplicities_in_order_plus_plus_minus_minus':mult,
            'two_cycle_products':[-1,-1]}
    if full:
        # Work with U=sqrt(N)V to keep all entries in a cyclotomic number field.
        UU=[[z(1+q[j]+q[k]-4*j*k) for k in range(n)] for j in range(n)]
        U=mat(UU)
        assert equal(conjugate(U).transpose()*U,I*rat(n)),('unitarity U',n)
        W=(U.transpose()*U)*rat(1,n)
        WfromM=mat([[z(q[j]-q[k])*MM[j][k] for k in range(n)] for j in range(n)])
        assert equal(W,WfromM),('W similarity',n)
        G=(U-conjugate(U))*(z(-n)*rat(1,2))
        assert equal(G,conjugate(G)),('G real',n)
        A=(G.transpose()*G)*rat(1,n)
        assert equal(A,(I-(W+conjugate(W))*rat(1,2))*rat(1,2)),('Gram identity',n)
        ss=(rat(2)-z(2)-z(-2))*rat(1,4)
        cc=one-ss
        R=(A-I*ss)*(one/(cc-ss))
        assert equal(R*R,R) and equal(R.transpose(),R) and equal(R,conjugate(R))
        rr,pivots=R.rref()
        d=h-2
        assert len(pivots)==d
        assert sum((rows(R)[j][j] for j in range(n)),zero)==rat(d)
        T=G*R
        if d:
            _,tpiv=T.rref();assert len(tpiv)==d
            AA=T.extract(list(range(n)),list(tpiv))
            BB=(AA.transpose()*AA).inv()*AA.transpose()*T
            assert equal(AA*BB,T)
            a,brows=rows(AA),rows(BB)
            EE=[[sum(((a[j][2*l]+z(n)*a[j][2*l+1])*(brows[2*l+1][k]+z(n)*brows[2*l][k]) for l in range(d//2)),zero) for k in range(n)] for j in range(n)]
            E=mat(EE)
        else:E=zero_matrix(n,n)
        assert E.rank()<=m-1
        assert equal((E-conjugate(E))*(z(-n)*rat(1,2)),T),('legal correction imaginary part',n)
        B=(U+conjugate(U)-E-conjugate(E))*rat(1,2)
        assert equal(B,conjugate(B)),('real core',n)
        residual=U-B-E
        assert equal(residual,(G-T)*z(n)),('residual identity',n)
        gram=conjugate(residual).transpose()*residual*rat(1,n)
        assert equal(gram,(I-R)*ss),('exact residual Gram and norm',n)
        result.update({'direct_unitary_and_Gram_checks':True,'projector_exact_rank':d,
                       'independent_rank_factor_correction':True,'complex_correction_rank':E.rank(),
                       'real_core_and_exact_residual_Gram':True})
    result['elapsed_seconds']=round(time.monotonic()-start,4)
    print(json.dumps(result),flush=True)
    return result

def main():
    initial=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    results=[]
    for n in [4,8,12,16,20,24,28,32,36,40,44,48,64]:
        results.append(verify(n,full=n<=20))
    final=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    output={'status':'PASS','candidate_proof_sha256_before':initial,'candidate_proof_sha256_after':final,
            'candidate_unchanged':initial==final,'arithmetic':'Exact rational cyclotomic fields; no floating-point matrix arithmetic',
            'author_or_historical_code_executed':False,'independent_checker':str(Path(__file__).resolve()),
            'checks':results,'scope':'Finite checks support the identities; the universal theorem requires the separately audited analytic proof.'}
    (ROOT/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print('PASS',flush=True)
if __name__=='__main__': main()
