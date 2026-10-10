"""Auditor-authored checks. Standard library only. No source imports or execution."""
import itertools as it, json, math, random
from pathlib import Path

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b,p): return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def mv(a,x,p): return [sum(u*v for u,v in zip(r,x))%p for r in a]
def plus(a,b,p,sgn=1): return [[(x+sgn*y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,t,p): return [[x*t%p for x in r] for r in a]
def rank(a,p):
    a=[r[:] for r in a];k=0
    for j in range(len(a[0]) if a else 0):
        u=next((i for i in range(k,len(a)) if a[i][j]%p),None)
        if u is None:continue
        a[k],a[u]=a[u],a[k];d=pow(a[k][j],-1,p)
        for i in range(k+1,len(a)):
            t=a[i][j]*d%p
            a[i]=[(x-t*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def inv(a,p):
    n=len(a);a=[r[:]+e for r,e in zip(a,ident(n))]
    for j in range(n):
        u=next((i for i in range(j,n) if a[i][j]),None)
        if u is None:raise ValueError('singular')
        a[j],a[u]=a[u],a[j];a[j]=[x*pow(a[j][j],-1,p)%p for x in a[j]]
        for i in range(n):
            if i!=j:
                t=a[i][j];a[i]=[(x-t*y)%p for x,y in zip(a[i],a[j])]
    return [r[n:] for r in a]

def root(n,p):
    # Finite check setup only, explicitly searched; not a free algorithm oracle.
    return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0))
def ft(n,p):
    w=root(n,p);return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def support(a):return max(sum(bool(x) for x in c) for c in zip(*a))
def binomial(n,t,a,p):
    z=ident(n)
    for j in range(n):z[(j+t)%n][j]=(z[(j+t)%n][j]-a)%p
    return z

def cycle_solve(x,a,t,p):
    # Solve by affine propagation from the final coordinate in each cycle.
    n=len(x);d=math.gcd(n,t);m=n//d;den=(1-pow(a,m,p))%p
    if den==0:raise ValueError('singular')
    den=pow(den,-1,p);out=[0]*n
    for offset in range(d):
        lane=[(offset+k*t)%n for k in range(m)];b=0
        for i in lane:b=(a*b+x[i])%p
        prev=b*den%p
        for i in lane:prev=(a*prev+x[i])%p;out[i]=prev
    return out

def gauge(n,p,rng):
    rows=rng.sample(range(n),n);v=[[0]*n for _ in range(n)]
    for j,i in enumerate(rows):v[i][j]=rng.randrange(1,p)
    return v

def minors():
    out=[]
    for n,p in [(3,7),(5,11),(7,29)]:
        f=ft(n,p);count=0
        for k in range(1,n+1):
            for rr in it.combinations(range(n),k):
                for cc in it.combinations(range(n),k):
                    assert rank([[f[i][j] for j in cc] for i in rr],p)==k;count+=1
        out.append({'N':n,'p':p,'nonzero_minors':count})
    return out

def uncertainty():
    out=[]
    for n,p in [(5,11),(7,29),(8,17)]:
        f=ft(n,p)
        for k in [1,2]:
            count=0;minimum=n
            for ix in it.combinations(range(n),k):
                for cs in it.product(range(1,p),repeat=k):
                    y=[sum(c*f[i][j] for j,c in zip(ix,cs))%p for i in range(n)];b=sum(bool(t) for t in y)
                    assert k*b>=n
                    if n in [5,7]:assert k+b>=n+1
                    count+=1;minimum=min(minimum,b)
            out.append({'N':n,'p':p,'k':k,'vectors':count,'minimum_output_support':minimum})
    # Composite length: prime additive rule really fails, product rule is sharp.
    assert sum(bool(t) for t in mv(ft(8,17),[1,0,0,0,1,0,0,0],17))==4
    # GF(8)=GF(2)[u]/(u^3+u+1), primitive seventh root u.
    def mul(x,y):
        z=0
        while y:
            if y&1:z^=x
            y>>=1;x<<=1
            if x&8:x^=11
        return z
    def power(x,e):
        y=1
        for _ in range(e):y=mul(y,x)
        return y
    vals=[1^power(2,k)^power(2,3*k) for k in range(7)]
    assert sum(bool(v) for v in vals)==4
    return {'exhaustive':out,'composite_sharp':{'N':8,'input_support':2,'output_support':4},'prime_finite_field_additive_counterexample':{'N':7,'field':'GF(8), u^3+u+1','input':[1,1,0,1,0,0,0],'output':vals,'support_sum':7,'required_complex_bound':8}}

def networks():
    rng=random.Random(123512);rows=[]
    for n,p in [(3,7),(5,11),(8,97),(12,97),(16,97)]:
        for L in [1,2,3,4]:
            for r0 in [0,1,2]:
                for rep in range(2):
                    G=ident(n);H=ident(n);budget=0
                    for stage in range(L):
                        while True:
                            t=rng.randrange(1,n);a=rng.randrange(p)
                            if pow(a,n//math.gcd(n,t),p)==1:continue
                            B=binomial(n,t,a,p)
                            g=mm(mm(gauge(n,p,rng),inv(B,p),p),gauge(n,p,rng),p)
                            uv=mm([[rng.randrange(p) for _ in range(r0)] for i in range(n)],[[rng.randrange(p) for j in range(n)] for _ in range(r0)],p) if r0 else [[0]*n for _ in range(n)]
                            h=plus(g,uv,p)
                            if rank(h,p)==n:break
                        gi=inv(g,p);hi=inv(h,p)
                        delta=plus(hi,gi,p,-1)
                        assert delta==scale(mm(mm(hi,uv,p),gi,p),-1,p)
                        assert rank(delta,p)==rank(uv,p)<=r0
                        G=mm(g,G,p);H=mm(h,H,p);budget+=rank(uv,p)
                    gi=inv(G,p);hi=inv(H,p);r=rank(plus(hi,gi,p,-1),p);s=support(gi)
                    assert r<=budget and s<=2**L
                    rows.append({'N':n,'L':L,'r_each':r0,'rank_budget':budget,'actual_inverse_rank':r,'actual_inverse_col_support':s})
    # Positive full Fourier stages with sufficient correction rank must be allowed.
    pos=[]
    for n,p in [(3,7),(5,11),(7,29),(8,17),(12,97)]:
        f=ft(n,p);R=plus(f,ident(n),p,-1);r=rank(R,p)
        assert (r+1)**2>=n
        if n in [3,5,7]:assert 2*(r+1)>=n+1
        pos.append({'N':n,'H_equals_F':True,'G_equals_I':True,'correction_rank':r})
    return {'cases':rows,'positive_F_controls':pos}

def green_checks():
    rng=random.Random(140512);count=0;singular=0;fusion=0;comm=[];chirps=[]
    for n in [1,2,3,4,5,6,8,10,12,15,16]:
        p=241;w=root(n,p)
        admissible=[a for a in range(p) if pow(a,n,p)!=1][:3]
        for t in range(n):
            for a in [0,1,2,3,7]:
                b=binomial(n,t,a,p);d=math.gcd(n,t)
                if pow(a,n//d,p)==1:
                    assert rank(b,p)<n
                    try:cycle_solve([1]*n,a,t,p)
                    except ValueError:singular+=1
                    else:raise AssertionError('singular accepted')
                else:
                    bi=inv(b,p)
                    for j in range(n):
                        x=[int(i==j) for i in range(n)];assert cycle_solve(x,a,t,p)==[r[j] for r in bi]
                    count+=1
        for K in range(1,n+1):
            if n%K:continue
            z=pow(w,n//K,p)
            for a in admissible:
                mean=[[0]*n for _ in range(n)];base=inv(binomial(n,1,a,p),p)
                for j in range(K):
                    conjugate=[[base[r][c]*pow(z,j*(r-c)%(p-1),p)%p for c in range(n)] for r in range(n)]
                    assert conjugate==inv(binomial(n,1,a*pow(z,j,p)%p,p),p)
                    mean=plus(mean,conjugate,p)
                mean=scale(mean,pow(K,-1,p),p)
                target=inv(binomial(n,K,pow(a,K,p),p),p)
                assert mean==target;fusion+=1
        if n>1:
            a=next(a for a in range(1,p) if pow(a,n,p)!=1)
            A=binomial(n,1,a,p);B=[[(1-a*pow(w,i,p))%p if i==j else 0 for j in range(n)] for i in range(n)]
            ai=inv(A,p);bi=inv(B,p);C=plus(mm(ai,bi,p),mm(bi,ai,p),p,-1)
            rhs=mm(mm(mm(mm(ai,bi,p),plus(mm(A,B,p),mm(B,A,p),p,-1),p),bi,p),ai,p)
            assert C==rhs and rank(C,p)==n and support(mm(B,A,p))<=2
            comm.append({'N':n,'rank':n})
        if n%2:
            h=pow(2,-1,n) if n>1 else 0
            C=[[pow(w,(-h*(i-j)**2)%n,p) for j in range(n)] for i in range(n)];D=[pow(w,h*i*i%n,p) for i in range(n)]
            assert [[D[i]*C[i][j]*D[j]%p for j in range(n)] for i in range(n)]==ft(n,p)
            ci=inv(C,p);assert all(all(r) for r in ci);chirps.append({'N':n,'inverse_support':support(ci)})
    # N=1 commutator has rank zero, not one.
    return {'stride_operator_basis_cases':count,'singular_guards':singular,'full_orbit_matrix_identities':fusion,'commutator_cases':comm,'odd_chirp_cases':chirps,'N1_commutator_rank':0}

def large():
    n=65536;p=786433;a=2;K=16;w=pow(10,(p-1)//n,p)
    assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
    x=[(j*j+31*j+19)%p for j in range(n)]
    z=cycle_solve(x,pow(a,K,p),K,p);phase=pow(w,n//K,p)
    average=[0]*n;c=a
    for j in range(K):
        y=cycle_solve(x,c,1,p)
        average=[(u+v)%p for u,v in zip(average,y)];c=c*phase%p
    average=[v*pow(K,-1,p)%p for v in average]
    assert z==average
    assert all((z[j]-pow(a,K,p)*z[(j-K)%n]-x[j])%p==0 for j in range(n))
    # Corrected modulation plan: shared powers plus one batch inversion.
    powers=[1]*n
    for j in range(1,n):powers[j]=powers[j-1]*w%p
    den=[(1-2*t)%p for t in powers];pref=[1]
    for t in den:pref.append(pref[-1]*t%p)
    tmp=pow(pref[-1],-1,p);iz=[0]*n
    for j in range(n-1,-1,-1):iz[j]=tmp*pref[j]%p;tmp=tmp*den[j]%p
    v=[u*t%p for u,t in zip(x,iz)];y=cycle_solve(v,a,1,p)
    assert all(den[j]*v[j]%p==x[j] and (y[j]-a*y[j-1])%p==v[j] for j in range(n))
    diffs=[]
    for k in [0,1,2,17]:
        value=sum(xj*powers[k*j%n] for j,xj in enumerate(x))%p
        if value!=y[k]:diffs.append(k)
    assert len(diffs)>0
    # Standard left-to-right binary ladder counts, initial leading bit uncharged.
    binary=sum(j.bit_length()-1+j.bit_count()-1 for j in range(1,n))
    assert binary==21*n+3
    return {'N':n,'p':p,'omega':w,'K':K,'full_fusion_outputs':n,'full_pair_stage_residuals':2*n,'DFT_disagreement_bins':diffs,'independent_pow_binary_ladder_multiplications':binary,'shared_root_recurrence_multiplications':n-1,'corrected_modulation_multiplications':6*n-1,'corrected_modulation_subtractions':n,'corrected_modulation_inversions':1,'counts_exclude_root_order_verification_and_modular_inversion_implementation':True}

def bounds():
    out=[]
    for n,prime in [(127,True),(257,True),(1024,False),(65536,False),(1048576,False)]:
        for L in range(1,5):
            s=2**L;r=0
            while ((s+1)*(r+1)<n+1 if prime else s*(r+1)**2<n):r+=1
            out.append({'N':n,'L':L,'prime':prime,'minimum_total_rank':r})
    return out

if __name__=='__main__':
    result={'status':'passed','independent':True,'uploaded_code_executed':False,'minors':minors(),'uncertainty':uncertainty(),'networks':networks(),'green':green_checks(),'large':large(),'rank_bounds':bounds()}
    Path('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'minors':sum(x['nonzero_minors'] for x in result['minors']),'networks':len(result['networks']['cases']),'green':result['green'],'large':result['large']},sort_keys=True))
