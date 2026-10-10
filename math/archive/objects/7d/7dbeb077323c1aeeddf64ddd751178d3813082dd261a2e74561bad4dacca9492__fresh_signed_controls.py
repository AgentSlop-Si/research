"""Fresh exact modular controls, self-contained except Python standard library.
No existing research implementation, import, compile, or AST inspection is used.
"""
import itertools, json
from pathlib import Path
OUT=Path(__file__).resolve().parent

def inv(a,p): return pow(a%p,-1,p)
def root(N,p):
    for q in range(2,p):
        if pow(q,N,p)==1 and all(pow(q,d,p)!=1 for d in range(1,N) if N%d==0): return q
    raise ValueError((N,p))
def gbin(r,l,q,p):
    z=1
    for j in range(1,l+1): z=z*(1-pow(q,r+j,p))*inv(1-pow(q,j,p),p)%p
    return z

def solve(A,b,p):
    C=[[(v%p) for v in row]+[t%p] for row,t in zip(A,b)]; M=len(A);L=len(A[0]);piv=[];i=0
    for j in range(L):
        k=next((k for k in range(i,M) if C[k][j]),None)
        if k is None: continue
        C[i],C[k]=C[k],C[i];u=inv(C[i][j],p);C[i]=[v*u%p for v in C[i]]
        for k in range(M):
            if k!=i and C[k][j]:
                u=C[k][j];C[k]=[(a-u*b)%p for a,b in zip(C[k],C[i])]
        piv.append(j);i+=1
        if i==M:break
    if any(all(v==0 for v in row[:L]) and row[L] for row in C):return None,len(piv)
    x=[0]*L
    for i,j in enumerate(piv):x[j]=C[i][L]
    return x,len(piv)

def matinv(A,p):
    n=len(A);I=[[int(i==j) for j in range(n)] for i in range(n)];C=[a[:]+b for a,b in zip(A,I)]
    for j in range(n):
        k=next(k for k in range(j,n) if C[k][j]);C[j],C[k]=C[k],C[j];u=inv(C[j][j],p);C[j]=[v*u%p for v in C[j]]
        for k in range(n):
            if k!=j:
                u=C[k][j];C[k]=[(a-u*b)%p for a,b in zip(C[k],C[j])]
    return [r[n:] for r in C]

def sector(N,p,q,e,d,alpha,l):
    v=[0]*(N*N);zeta=pow(q,(e*d)%N,p)
    for r in range(N-l):v[((e*r)%N)*N+(d*l)%N]=pow(alpha,r,p)*gbin(r,l,zeta,p)%p
    return v

def fcoeff(N,p,q):
    C=sum(pow(q,(-j*j)%N,p) for j in range(N))*inv(N,p)%p
    assert C
    return [C*pow(q,((a+b)**2*pow(4,-1,N))%N,p)%p for a in range(N) for b in range(N)]

def row_pairs(N,p,q,d):
    f=fcoeff(N,p,q);out=[]
    for x,y in itertools.product(range(1,p),repeat=2):
        vx=sector(N,p,q,1,d,x,1);vy=sector(N,p,q,-1,d,y,1);b=d%N
        hx=f[N+b]*inv(vx[N+b],p)%p;hy=f[(N-1)*N+b]*inv(vy[(N-1)*N+b],p)%p
        if all((hx*vx[a*N+b]+hy*vy[a*N+b]-f[a*N+b])%p==0 for a in range(1,N)):
            out.append((x,y))
    return out

def original_matrix(N,p,q,e,d,alpha,beta,weights):
    R=[[0]*N for _ in range(N)];z=pow(q,e*d%N,p)
    for j,w in enumerate(weights):
        Q=[[int(k==i) for i in range(N)] for k in range(N)]
        for i in range(N):
            Q[(i+e)%N][i]=(Q[(i+e)%N][i]-alpha)%p
            Q[i][i]=(Q[i][i]-beta*pow(z,j,p)*pow(q,d*i%N,p))%p
        Qinv=matinv(Q,p)
        for k in range(N):
            for i in range(N):R[k][i]=(R[k][i]+w*Qinv[k][i]*inv(N,p))%p
    return R

def realizations(N,p,search_all=False):
    q=root(N,p);cp=row_pairs(N,p,q,1);cm=row_pairs(N,p,q,-1);target=fcoeff(N,p,q);tried=0;found=[]
    for (xp,yp),(xm,ym) in itertools.product(cp,cm):
        ors=[(1,1,xp),(-1,1,yp),(1,-1,xm),(-1,-1,ym)]
        cols=[sector(N,p,q,e,d,alpha,l) for e,d,alpha in ors for l in range(N)]
        hs,rank=solve(list(map(list,zip(*cols))),target,p);tried+=1
        if hs is None: continue
        data={'orientations':[],'coefficient_rank':rank};R=[[0]*N for _ in range(N)]
        for idx,(e,d,alpha) in enumerate(ors):
            beta=next(b for b in range(1,p) if (1-pow(alpha,N,p)-pow(b,N,p))%p)
            Delta=(1-pow(alpha,N,p)-pow(beta,N,p))%p;z=pow(q,e*d%N,p);h=hs[idx*N:(idx+1)*N]
            gamma=[v*Delta*pow(inv(beta,p),l,p)%p for l,v in enumerate(h)]
            weights=[sum(gamma[l]*pow(z,(-j*l)%N,p) for l in range(N))%p for j in range(N)]
            B=original_matrix(N,p,q,e,d,alpha,beta,weights)
            for k in range(N):
                for i in range(N):R[k][i]=(R[k][i]+B[k][i])%p
            data['orientations'].append({'epsilon':e,'delta':d,'alpha':alpha,'beta':beta,'Delta':Delta,'h':h,'branch_weights':weights})
        assert R==[[pow(q,(-k*i)%N,p) for i in range(N)] for k in range(N)]
        data['direct_original_branch_matrix_equal_fourier']=True;found.append(data)
        if not search_all:break
    return {'N':N,'p':p,'q':q,'positive_row_candidate_pairs':len(cp),'negative_row_candidate_pairs':len(cm),'parameter_quadruples_checked':tried,'solutions':found,'scope':'Exact finite-field control only; no extrapolation to other fields or lengths.'}

support=[]
for N in range(3,32,2):
    orientations=list(itertools.product([1,-1],repeat=2))
    sets=[{(a,b) for a in range(N) for b in range(N) if (e*a)%N+(d*b)%N<=N-1} for e,d in orientations]
    assert set.union(*sets)==set(itertools.product(range(N),repeat=2))
    holes=[]
    for i in range(4):
        missing=set(itertools.product(range(N),repeat=2))-set.union(*(sets[j] for j in range(4) if j!=i))
        assert len(missing)==(N-1)//2;holes.append(len(missing))
    support.append({'N':N,'four_cover':True,'triple_hole_counts':holes})

cases=[realizations(3,7),realizations(5,11,True),realizations(7,29,True)]
for v in cases:print(json.dumps(v),flush=True)

# Directly reconstruct arbitrary signed averages from branch inverses and compare
# their Weyl expansions, including alpha=0 and nontrivial weights.
checks=[]
for N,p in [(3,7),(5,11),(7,29),(9,19),(11,23)]:
    q=root(N,p)
    for e,d in itertools.product([1,-1],repeat=2):
        for alpha in [0,1,2]:
            beta=next(b for b in range(1,p) if (1-pow(alpha,N,p)-pow(b,N,p))%p)
            Delta=(1-pow(alpha,N,p)-pow(beta,N,p))%p;z=pow(q,e*d%N,p);w=[(3*j*j+2*j+1)%p for j in range(N)]
            gamma=[sum(w[j]*pow(z,j*l%N,p) for j in range(N))*inv(N,p)%p for l in range(N)]
            coeff=[0]*(N*N)
            for l in range(N):
                h=gamma[l]*pow(beta,l,p)*inv(Delta,p)%p
                coeff=[(a+h*b)%p for a,b in zip(coeff,sector(N,p,q,e,d,alpha,l))]
            C=[[0]*N for _ in range(N)]
            for a,b in itertools.product(range(N),repeat=2):
                for i in range(N):C[(i+a)%N][i]=(C[(i+a)%N][i]+coeff[a*N+b]*pow(q,b*i%N,p))%p
            assert C==original_matrix(N,p,q,e,d,alpha,beta,w)
            checks.append({'N':N,'p':p,'epsilon':e,'delta':d,'alpha':alpha,'beta':beta,'equal':True})
n3_constructions=[]
for p in [7,13,19,31]:
    N=3;q=root(N,p);f=fcoeff(N,p,q)
    alphas={(1,1):1,(1,-1):q,(-1,1):q,(-1,-1):1}
    hs={key:[0,0,0] for key in alphas}
    for key,k in [((1,1),0),((1,-1),1),((-1,1),-1)]:
        hs[key][0]=sum(f[a*N]*pow(q,(-k*a)%N,p) for a in range(N))*inv(N,p)%p
    for (e,d),alpha in alphas.items():
        hs[e,d][1]=f[(e%N)*N+d%N]*inv(alpha*(1+pow(q,(e*d)%N,p)),p)%p
    for d in [1,-1]:
        hs[1,-d][2]=(f[d%N]-hs[1,d][1]-hs[-1,d][1])%p
    R=[[0]*N for _ in range(N)]
    for (e,d),alpha in alphas.items():
        z=pow(q,e*d%N,p);w=[-sum(hs[e,d][l]*pow(z,(-j*l)%N,p) for l in range(N))%p for j in range(N)]
        B=original_matrix(N,p,q,e,d,alpha,1,w)
        for k in range(N):
            for i in range(N):R[k][i]=(R[k][i]+B[k][i])%p
    assert R==[[pow(q,(-k*i)%N,p) for i in range(N)] for k in range(N)]
    n3_constructions.append({'N':N,'p':p,'q':q,'explicit_construction_equal_original_fourier':True})
interpolation_controls=[]
for N,p in [(3,7),(5,11),(7,29),(9,19)]:
    q=root(N,p);ors=list(itertools.product([1,-1],repeat=2))
    for target_kind in ['fourier','arbitrary_weyl_coefficients']:
        target=fcoeff(N,p,q) if target_kind=='fourier' else [(7*a*a+3*b+2*a*b+1)%p for a in range(N) for b in range(N)]
        assigned={o:[0]*(N*N) for o in ors}
        for a,b in itertools.product(range(N),repeat=2):
            o=next((e,d) for e,d in ors if (e*a)%N+(d*b)%N<=N-1)
            assigned[o][a*N+b]=target[a*N+b]
        reconstructed=[[0]*N for _ in range(N)]
        for e,d in ors:
            z=pow(q,e*d%N,p);H=[[0]*N for _ in range(N)]
            for l in range(N):
                t=[assigned[e,d][((e*r)%N)*N+(d*l)%N]*inv(gbin(r,l,z,p),p)%p if r<N-l else 0 for r in range(N)]
                for j in range(N):H[j][l]=sum(t[r]*pow(q,(-j*r)%N,p) for r in range(N))*inv(N,p)%p
            for j in range(N):
                w=[-sum(H[j][l]*pow(z,(-k*l)%N,p) for l in range(N))%p for k in range(N)]
                B=original_matrix(N,p,q,e,d,pow(q,j,p),1,w)
                for a in range(N):
                    for b in range(N):reconstructed[a][b]=(reconstructed[a][b]+B[a][b])%p
        desired=[[sum(target[((k-i)%N)*N+b]*pow(q,b*i%N,p) for b in range(N))%p for i in range(N)] for k in range(N)]
        assert reconstructed==desired
        interpolation_controls.append({'N':N,'p':p,'q':q,'target':target_kind,'banks':4*N,'original_inverse_sum_matches':True})
cyclic_solve_controls=[]
for N,p in [(3,7),(5,11),(7,29),(9,19),(11,23)]:
    q=root(N,p);powers=[pow(q,i,p) for i in range(N)];count=0
    for e,d in itertools.product([1,-1],repeat=2):
        for j,k in itertools.product(range(N),repeat=2):
            alpha=powers[j];ai=inv(alpha,p);x=[(i*i+3*i+j+2*k+1)%p for i in range(N)]
            i0=(-e*k)%N;y=[None]*N;y[(i0-e)%N]=-x[i0]*ai%p
            for t in range(1,N):
                i=(i0-e*t)%N;di=(1-powers[(e*d*k+d*i)%N])%p
                y[(i-e)%N]=(di*y[i]-x[i])*ai%p
            assert all(((1-powers[(e*d*k+d*i)%N])*y[i]-alpha*y[(i-e)%N]-x[i])%p==0 for i in range(N))
            count+=1
    cyclic_solve_controls.append({'N':N,'p':p,'q':q,'known_zero_diagonal_solves_checked':count,'all_original_equations_match':True})
result={'cyclic_solve_controls':cyclic_solve_controls,'interpolation_upper_bound_controls':interpolation_controls,'support_controls':support,'small_realization_controls':cases,'original_branch_matrix_checks':checks,'n3_explicit_constructions':n3_constructions,'counts':{'support_lengths':len(support),'direct_signed_average_checks':len(checks),'explicit_n3_constructions':len(n3_constructions),'interpolation_upper_bound_controls':len(interpolation_controls),'known_zero_diagonal_solves':sum(c['known_zero_diagonal_solves_checked'] for c in cyclic_solve_controls)}}
(OUT/'fresh_signed_controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['counts']),flush=True)
