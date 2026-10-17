"""Fresh reviewer controls. Standard library only; no historical/source programs loaded."""
from fractions import Fraction
from itertools import product, combinations
import cmath, hashlib, json, math
from pathlib import Path


def rank(A,p):
    a=[row[:] for row in A]
    nr=len(a); nc=len(a[0]) if nr else 0; h=0
    for j in range(nc):
        pivot=next((i for i in range(h,nr) if a[i][j]%p),None)
        if pivot is None: continue
        a[h],a[pivot]=a[pivot],a[h]
        inv=pow(a[h][j]%p,-1,p)
        a[h]=[(v*inv)%p for v in a[h]]
        for i in range(nr):
            if i!=h and a[i][j]%p:
                c=a[i][j]%p
                a[i]=[(x-c*y)%p for x,y in zip(a[i],a[h])]
        h+=1
        if h==nr: break
    return h


def finite_root(q,p):
    for a in range(2,p):
        if pow(a,q,p)==1 and all(pow(a,q//d,p)!=1 for d in range(2,q+1) if q%d==0):
            return a
    raise ValueError((q,p))


def ramanujan_controls():
    p=257; cases=[]
    for q in [2,4,8,16,32,64,128,256]:
        m=q//2; z=finite_root(q,p)
        P=[[0]*m for _ in range(m)]
        for j in range(m):
            dest=(5*j)%m; sign=(-1)**((5*j)//m)
            P[dest][j]=sign%p
        V=[[pow(z,k*j,p) for j in range(m)] for k in range(1,q,2)]
        # Signed z->z^5 agrees with permuting odd evaluations.
        for ki,k in enumerate(range(1,q,2)):
            target=((5*k)%q-1)//2
            for j in range(m):
                lhs=sum(V[ki][a]*P[a][j] for a in range(m))%p
                assert lhs==V[target][j]
        A=[[(P[i][j]-(i==j))%p for j in range(m)] for i in range(m)]
        nullity=m-rank(A,p)
        assert nullity==(1 if q==2 else 2)
        assert rank(V,p)==m
        # Ramanujan c_q is m at 0, -m at m; shifts give m[I;-I].
        for j in range(m):
            for k in range(q):
                Eeval=(pow(z,k*j,p)-pow(z,k*(j+m),p))*pow(2,-1,p)%p
                assert Eeval==(0 if k%2==0 else pow(z,k*j,p))
        supports=[()] + [(j,) for j in range(m)]
        if m<=8: supports += list(combinations(range(m),2))
        else: supports += [(0,m-1),(1,m//2)]
        for support in supports:
            reduced=[A[i] for i in range(m) if i not in support]
            dim=m-rank(reduced,p)
            assert dim<=min(m,len(support)+nullity)
        cases.append({'q':q,'coefficient_dimension':m,'kernel_dimension':nullity,'fixed_support_checks':len(supports)})
    # Ambient-N Ramanujan coefficient map beta=r/N, checked on fresh input.
    embedding_checks=[]
    for N in [2,4,8,16,32,64,128]:
        zN=finite_root(N,p)
        x=[(j*j+3*j+7)%p for j in range(N)]
        X=[sum(x[j]*pow(zN,k*j,p) for j in range(N))%p for k in range(N)]
        for q in [2**j for j in range(1,N.bit_length())]:
            m=q//2
            v=[sum(x[j+t*q] for t in range(N//q))%p for j in range(q)]
            r=[(v[j]-v[j+m])%p for j in range(m)]
            beta=[a*pow(N,-1,p)%p for a in r]
            h=[sum(beta[j]*(m if (n-j)%q==0 else -m if (n-j)%q==m else 0) for j in range(m))%p for n in range(N)]
            target={k*N//q for k in range(1,q,2)}
            for k in range(N):
                H=sum(h[j]*pow(zN,k*j,p) for j in range(N))%p
                assert H==(X[k] if k in target else 0)
            embedding_checks.append({'N':N,'q':q,'dimension':m})
    # Derive all-output conductor writes and algebraic ledger independently.
    ledgers=[]
    for d in range(1,11):
        N=2**d
        conductors=[2**j for j in range(1,d+1)]
        outputs=[0]+[k*N//q for q in conductors for k in range(1,q,2)]
        assert sorted(outputs)==list(range(N))
        T=sum((q//2)*((q//2)%3) for q in conductors if q>=4)
        nu=N//3
        assert (N+2*d)+(3*N-4+nu)+(5*N-8-2*d+2*T)==9*N-12+2*T+nu
        fft_emission=sum(q//2+3*(q//2)*((q//2).bit_length()-1)//2 for q in conductors if q>=4)
        all_local_fft=N+2*d+3*N-4+nu+fft_emission
        full_radix=N+2*d+3*N*d//2
        assert all_local_fft-full_radix==N-3+nu
        ledgers.append({'N':N,'writes':len(outputs),'T':T,'nu':nu,'hybrid_overhead_bound':N-3+nu})
    return {'exact_modular_cases':cases,'ambient_N_embedding':embedding_checks,'ledger_and_coverage':ledgers,'limit':'Finite controls corroborate algebra only; not an attribution or complexity proof.'}


def weyl_controls():
    cases=[]; scalar_errors=[]
    for q,p in [(3,7),(5,11),(7,29),(11,23)]:
        z=finite_root(q,p); inv2=pow(2,-1,q); inv4=pow(4,-1,q)
        gamma=sum(pow(z,j*j,p) for j in range(q))*pow(q,-1,p)%p
        assert gamma
        coeff={}
        for a,b in product(range(q),repeat=2):
            trace=sum(pow(z,(j*j+(a-b)*j-a*b*inv2)%q,p) for j in range(q))*pow(q,-1,p)%p
            formula=gamma*pow(z,(-(a*a+b*b)*inv4)%q,p)%p
            assert trace==formula
            coeff[a,b]=trace
        counts={1:0,q:0}; orientations=0
        directions=[u for u in product(range(q),repeat=2) if u!=(0,0)]
        for a,b in directions:
            for c,d in directions:
                if (a*d-b*c)%q==0: continue
                sigma=(b*c-a*d)%q; kap=(a*c+b*d+sigma)%q
                tensor=[]
                for m in range(q):
                    row=[]
                    for n in range(q):
                        pair=((m*a+n*c)%q,(m*b+n*d)%q)
                        actual=coeff[pair]*pow(z,(-sigma*m*n*inv2)%q,p)%p
                        phase=(-(a*a+b*b)*m*m*inv4-(c*c+d*d)*n*n*inv4-kap*m*n*inv2)%q
                        expected=gamma*pow(z,phase,p)%p
                        assert actual==expected
                        row.append(actual)
                    tensor.append(row)
                r=rank(tensor,p); assert r==(1 if kap==0 else q)
                counts[r]+=1
                if kap==0:
                    assert (a*c+b*d-sigma)%q != 0
                    orientations+=1
        # Complex source scalar, not finite-field reduction of i/sqrt(q).
        G=sum(cmath.exp(2j*math.pi*j*j/q) for j in range(q))
        legendre2=1 if pow(2,(q-1)//2,q)==1 else -1
        nu=G*G*legendre2/(q*q)
        C=(1j)**((q-1)//2)*math.sqrt(q)
        error=abs(C*nu-G/q)
        assert error<1e-12
        scalar_errors.append({'q':q,'absolute_error':error})
        cases.append({'q':q,'field':p,'rank_counts':counts,'reversal_controls':orientations})
    return {'exact_modular_cases':cases,'complex_normalization':scalar_errors,'limit':'Finite controls corroborate stated prime-length formulas, not arbitrary-field representation theory.'}


def precision_interface_controls():
    # Composite contract alone does not identify a summary decoder.
    C=Fraction(1); D=Fraction(1); C_hat=Fraction(1001,1000); D_hat=1/C_hat
    assert D_hat*C_hat==D*C
    assert D_hat!=D
    return {'composite_error':str(D_hat*C_hat-D*C),'summary_decoder_error_at_one':str(D_hat-D),'interpretation':'Abstract countermodel to an inference from composite accuracy alone; not a model of the supplied implementation.'}

result={'status':'PASS','ramanujan':ramanujan_controls(),'weyl':weyl_controls(),'precision_interface':precision_interface_controls()}
p=Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','result_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
