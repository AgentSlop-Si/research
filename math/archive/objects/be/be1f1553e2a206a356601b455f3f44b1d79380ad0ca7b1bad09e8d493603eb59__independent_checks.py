#!/usr/bin/env python3
"""Independent reviewer controls. Imports only Python stdlib, never uploaded code."""
import itertools, json, math, random
from pathlib import Path

BASE=Path(__file__).resolve().parent
RNG=random.Random(202610092201)

def prime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))

def field(n):
    p=n+1
    while not prime(p):p+=n
    divisors=[d for d in range(1,n) if n%d==0]
    for g in range(1,p):
        if pow(g,n,p)==1 and all(pow(g,d,p)!=1 for d in divisors):return p,g
    raise AssertionError('root')

def rank(a,p):
    a=[list(row) for row in a]
    if not a:return 0
    r=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]%p),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][c],-1,p)
        a[r]=[x*inv%p for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                z=a[i][c];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def dft(x,w,p):
    return [sum(v*pow(w,-k*t,p) for t,v in enumerate(x))%p for k in range(len(x))]

def kernel(q,z,p):return sum(pow(z,t,p) for t in range(q))%p

def routing_checks():
    out={'column_tests':0,'kernel_entries':0,'zero_denominator_entries':0,'routing_count_checks':0,
         'extremal_gcd_checks':0,'square_blocks':0,'square_basis_edges':0,'nonzero_mu_requirement':'Not needed: mu=0 is dense, K=all ones.'}
    configs=[(q,m) for q in range(2,8) for m in range(2,9)]+[(6,10),(8,12)]
    for q,m in configs:
        p,w=field(q*m);eta=pow(w,q,p);xi=pow(w,m,p)
        maxdiv=max(d for d in range(1,m+1) if m%d==0 and math.gcd(d,q)==1)
        assert max(math.gcd(a*q+1,m) for a in range(m))==maxdiv
        out['extremal_gcd_checks']+=1
        for a in range(m):
            for mu in range(p):
                matched=0;edges=0
                for h in range(m):
                    lam=mu*pow(eta,-a*h,p)%p
                    defect=(1-pow(eta,-h,p)*pow(lam,q,p))%p
                    vals=[]
                    for s in range(q):
                        z=pow(w,-h-s*m,p);v=kernel(q,z*lam%p,p)
                        assert (1-z*lam)*v%p==defect
                        if (1-z*lam)%p==0:
                            assert v==q%p and defect==0;out['zero_denominator_entries']+=1
                        elif defect==0:assert v==0
                        else:assert v==defect*pow((1-z*lam)%p,-1,p)%p and v!=0
                        vals.append(v)
                    nz=sum(bool(v) for v in vals)
                    assert nz==(1 if defect==0 else q)
                    matched+=defect==0;edges+=nz
                    out['column_tests']+=1;out['kernel_entries']+=q
                assert matched in (0,math.gcd(a*q+1,m))
                assert matched<=maxdiv
                assert edges==q*m-(q-1)*matched
                assert edges>=q*m-(q-1)*maxdiv
                out['routing_count_checks']+=1
    for m in range(2,14):
        p,w=field(m*m);eta=pow(w,m,p)
        edges=0
        for h in range(m):
            lam=[pow(w,(1-m*h)*j,p) for j in range(m)]
            assert len(set(lam))==m
            K=[[kernel(m,pow(w,-h-s*m,p)*x%p,p) for x in lam] for s in range(m)]
            assert rank(K,p)==m
            E=[[K[s][j]*(1-pow(w,-h-s*m,p)*lam[j])%p for j in range(m)] for s in range(m)]
            assert rank(E,p)==1
            assert sum(bool(v) for row in K for v in row)==m*m-m+1
            assert K[(-h*h)%m][h]==m%p
            edges+=sum(bool(v) for row in K for v in row)
            out['square_blocks']+=1
        assert edges==m**3-m*m+m;out['square_basis_edges']+=edges
    return out

def orbit_signature(x,p):
    pos=[i for i,v in enumerate(x) if v%p]
    if not pos:return pos,[]
    n=len(x)
    return pos,[((pos[(j+1)%len(pos)]-i)%n or n,x[pos[(j+1)%len(pos)]]%p,x[i]%p) for j,i in enumerate(pos)]

def find_shift(f,v,p):
    """Reviewer KMP on rational tokens; returns any certified cyclic shift."""
    fp,ft=orbit_signature(f,p);vp,vt=orbit_signature(v,p)
    if not vp:return 0 if not fp else None
    if len(fp)!=len(vp):return None
    def same(a,b):return a[0]==b[0] and (a[1]*b[2]-b[1]*a[2])%p==0
    pi=[0]*len(vt)
    for i in range(1,len(vt)):
        j=pi[i-1]
        while j and not same(vt[i],vt[j]):j=pi[j-1]
        if same(vt[i],vt[j]):j+=1
        pi[i]=j
    j=0
    for i in range(2*len(ft)-1):
        token=ft[i%len(ft)]
        while j and not same(token,vt[j]):j=pi[j-1]
        if same(token,vt[j]):j+=1
        if j==len(vt):
            shift=(fp[i-len(vt)+1]-vp[0])%len(f)
            a=vp[0];den=f[(a+shift)%len(f)]
            assert all((v[b]*den-v[a]*f[(b+shift)%len(f)])%p==0 for b in range(len(f)))
            return shift
    return None

def brute_shift(f,v,p):
    if not any(v):return 0 if not any(f) else None
    a=next(i for i,x in enumerate(v) if x)
    for s in range(len(f)):
        den=f[(a+s)%len(f)]
        if den and all((v[b]*den-v[a]*f[(b+s)%len(f)])%p==0 for b in range(len(f))):return s
    return None

def detector_checks():
    total=0
    for k,p in [(1,5),(2,3),(3,3),(4,3),(5,3),(6,2)]:
        vectors=list(itertools.product(range(p),repeat=k))
        for f in vectors:
            for v in vectors:
                assert (find_shift(f,v,p) is None)==(brute_shift(f,v,p) is None)
                total+=1
    return {'exhaustive_vector_pairs':total,'fields_and_lengths':[[1,5],[2,3],[3,3],[4,3],[5,3],[6,2]],'covers':'zero vectors, singleton supports, periodic patterns, false candidates'}

def fusion(U,H,g,a,beta,w,p):
    k=len(U);r=len(H);m=len(g);n=k*m
    G=[dft([U[b][i] for b in range(k)],pow(w,m,p),p) for i in range(r)]
    out=[0]*n
    for ell in range(k):
        z=[]
        for t in range(m):
            u=(ell+a*t)%k
            value=sum(H[i][t]*G[i][u] for i in range(r))%p
            exponent=-a*t*(t-1)//2-(beta+ell)*t+m*u*g[t]
            z.append(value*pow(w,exponent,p)%p)
        y=dft(z,pow(w,k,p),p)
        for j in range(m):out[ell+j*k]=y[j]
    return out

def phase7_checks():
    out={'factor_cases':0,'unknown_template_cases':0,'full_output_bins':0,'exact_witness':{}}
    for k,m in [(2,2),(4,2),(4,4),(8,2),(8,4),(8,8),(16,4),(16,8),(32,8)]:
        p,w=field(k*m);n=k*m
        for r in range(1,min(m,3)+1):
            for repeat in range(4):
                a=[v for v in range(1,n) if math.gcd(v,n)==1][repeat%len([v for v in range(1,n) if math.gcd(v,n)==1])]
                beta=repeat;g=[RNG.randrange(k) for _ in range(m)]
                U=[[RNG.randrange(p) for _ in range(r)] for _ in range(k)]
                H=[[RNG.randrange(p) for _ in range(m)] for _ in range(r)]
                x=[]
                for b in range(k):
                    for t in range(m):
                        V=sum(U[(b+g[t])%k][i]*H[i][t] for i in range(r))%p
                        x.append(V*pow(w,-a*t*(t-1)//2-(a*m*b+beta)*t,p)%p)
                assert fusion(U,H,g,a,beta,w,p)==dft(x,w,p)
                out['factor_cases']+=1;out['full_output_bins']+=n
                # Restrict to exactly one template per nonzero column, recover all shifts/templates independently.
                group=[t%r for t in range(m)];scale=[RNG.randrange(p) for _ in range(m)]
                V=[[scale[t]*U[(b+g[t])%k][group[t]]%p for t in range(m)] for b in range(k)]
                refs=[];recovered_g=[];recovered_scale=[];recovered_group=[]
                for t in range(m):
                    col=[V[b][t] for b in range(k)]
                    if not any(col):recovered_g.append(0);recovered_scale.append(0);recovered_group.append(-1);continue
                    for i,f in enumerate(refs):
                        s=find_shift(f,col,p)
                        if s is not None:break
                    else:i=len(refs);refs.append(col);s=0
                    anchor=next(b for b,z in enumerate(col) if z)
                    recovered_g.append(s);recovered_group.append(i)
                    recovered_scale.append(col[anchor]*pow(refs[i][(anchor+s)%k],-1,p)%p)
                assert len(refs)<=r
                RU=[[f[b] for f in refs] for b in range(k)];RH=[[recovered_scale[t] if recovered_group[t]==i else 0 for t in range(m)] for i in range(len(refs))]
                raw=[V[b][t]*pow(w,-a*t*(t-1)//2-(a*m*b+beta)*t,p)%p for b in range(k) for t in range(m)]
                assert fusion(RU,RH,recovered_g,a,beta,w,p)==dft(raw,w,p)
                out['unknown_template_cases']+=1;out['full_output_bins']+=n
    # Uploaded explicit parameters are inert data; recompute all assertions independently.
    p=2013265921;k=16;m=8;n=k*m;w=pow(31,(p-1)//n,p)
    assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
    f=[2]+[1]*(k-1);h=list(range(1,m+1));g=list(range(m))
    V=[[h[t]*f[(b+g[t])%k]%p for t in range(m)] for b in range(k)]
    raw=[V[b][t]*pow(w,-t*(t-1)//2-m*b*t,p)%p for b in range(k) for t in range(m)]
    D=[dft(row,pow(w,k,p),p) for row in V]
    hr=rank([[raw[i+j] for j in range(n//2)] for i in range(n//2)],p)
    witness={'nonzero_input':sum(bool(z) for z in raw),'block_rank':rank(V,p),'active_modes':sum(any(D[b][t] for b in range(k)) for t in range(m)),'hankel_rank':hr,'N':n,'p':p,'root':w}
    assert witness['nonzero_input']==n and witness['block_rank']==m and witness['active_modes']==m and hr==n//2
    assert fusion([[z] for z in f],[h],g,1,0,w,p)==dft(raw,w,p)
    out['exact_witness']=witness
    return out

def inverse_formula_checks():
    cases=0;nodes=0
    for m in range(2,23):
        p,w=field(m*m)
        for h in range(m):
            q=pow(w,1-m*h,p);F=[1];T=[pow(q,j*(j-1)//2,p) for j in range(m)]
            for j in range(1,m):F.append(F[-1]*(1-pow(q,j,p))%p)
            assert all(F)
            for rep in range(3):
                B=[RNG.randrange(p) for _ in range(m)]
                C=[sum(B[j]*pow(q,t*j,p) for j in range(m))%p for t in range(m)]
                d=[sum((-1)**t*C[t]*pow(F[t],-1,p)*T[r-t]*pow(F[r-t],-1,p) for t in range(r+1))%p for r in range(m)]
                a=[d[r]*pow(T[r],-1,p)%p for r in range(m)]
                rec=[pow(F[j],-1,p)*sum(a[r]*F[r]*(-1)**(r-j)*T[r-j]*pow(F[r-j],-1,p) for r in range(j,m))%p for j in range(m)]
                assert rec==B;cases+=1
            nodes+=m
    return {'exact_inverse_cases':cases,'nonzero_factorial_values':nodes,'M_range':[2,22],'check_style':'Direct independent triangular sums, no FFT and no constructor-code import'}

if __name__=='__main__':
    result={'routing':routing_checks(),'projective_detector':detector_checks(),'phase7':phase7_checks(),'peer_inverse':inverse_formula_checks(),'uploaded_code_executed':False}
    (BASE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
