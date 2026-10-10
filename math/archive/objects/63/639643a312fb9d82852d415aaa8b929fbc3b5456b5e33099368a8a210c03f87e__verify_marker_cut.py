#!/usr/bin/env python3
"""Fresh standard-library-only exact controls. No predecessor code is imported."""
from fractions import Fraction
from pathlib import Path
import hashlib, json
P=65537
ROOT=Path(__file__).resolve().parent

def gamma(k):
    ans=0
    while k:
        if k&1: ans+=k//2
        k//=2
    return ans

def step(v, root):
    N=len(v); y=[0]*N
    for s,x in enumerate(v):
        a=2*s%N
        y[a]=(y[a]+x)%P
        y[a+1]=(y[a+1]+pow(root,s,P)*x)%P
    return y

def add(a,b):
    for i,x in enumerate(b): a[i]=(a[i]+x)%P

def prepared(n,b):
    N=1<<n; d=n-b; r=1<<d
    omega=pow(3,(P-1)//N,P)
    assert pow(omega,N,P)==1 and pow(omega,N//2,P)!=1
    R=list(range(0,N,1<<b)); A=[]; layers=[[] for _ in range(d+1)]
    for s in range(N):
        w=format(s,f'0{n}b'); pos=w.rfind('0'*b)
        if pos<0: A.append(s)
        else:
            h=n-pos-b
            if h: layers[h].append(s)
    T=set(R+A); E=set(range(N))-T
    assert sum(map(len,layers))==len(E)
    for h in range(1,d+1):
        words=[w for w in range(1<<(h-1),1<<h) if '0'*b not in format(w,f'0{h}b')]
        expected={((j<<(b+h))+w) for j in range(1<<(d-h)) for w in words}
        assert expected==set(layers[h])
        for s in layers[h]:
            for bit in (0,1):
                q=(2*s+bit)%N
                if q in E:
                    assert h<d and q in layers[h+1]
                if q in A: assert h==d
    for s in A:
        assert all((2*s+bit)%N not in E for bit in (0,1))
    return dict(n=n,b=b,N=N,d=d,r=r,omega=omega,R=R,A=A,T=T,E=E,layers=layers)

def oracle_source(z,x):
    N=z['N']; n=z['n']; T=z['T']; E=z['E']
    f=[[0]*N for _ in range(n+1)]; f[0]=[x[s] if s in T else 0 for s in range(N)]
    e=[x[s] if s in E else 0 for s in range(N)]
    for L in range(1,n+1):
        e=step(e,z['omega'])
        f[L]=[e[s] if s in T else 0 for s in range(N)]
        e=[e[s] if s in E else 0 for s in range(N)]
    assert not any(e)
    return f

def layered_source(z,x):
    N=z['N']; n=z['n']; d=z['d']; T=z['T']; E=z['E']
    f=[[0]*N for _ in range(n+1)]
    for s in T: f[0][s]=x[s]
    polys={s:[x[s]]+[0]*(h-1) for h in range(1,d+1) for s in z['layers'][h]}
    for h in range(1,d+1):
        for s in z['layers'][h]:
            for bit in (0,1):
                q=(2*s+bit)%N; wt=pow(z['omega'],s,P) if bit else 1
                for k,val in enumerate(polys[s]):
                    if q in T: f[k+1][q]=(f[k+1][q]+wt*val)%P
                    else: polys[q][k+1]=(polys[q][k+1]+wt*val)%P
    return f

def oracle_feedback(z,u):
    N=z['N']; n=z['n']; T=z['T']; E=z['E']
    out=[[0]*N for _ in range(n+1)]; e=u[:]
    for L in range(1,n+1):
        e=step(e,z['omega'])
        out[L]=[e[s] if s in T else 0 for s in range(N)]
        e=[e[s] if s in E else 0 for s in range(N)]
    return out

def compressed_feedback(z,u,limit=None,top_recovery=False):
    n=z['n']; b=z['b']; d=z['d']; r=z['r']; N=z['N']; omega=z['omega']; eta=pow(omega,1<<b,P)
    if limit is None: limit=n
    out=[[0]*N for _ in range(limit+1)]; recover=[0]*N
    if limit==0:return out,recover
    direct=step(u,omega)
    out[1]=[direct[s] if s in z['T'] else 0 for s in range(N)]
    q=[u[s] for s in z['R']]
    rrmax=max(0,min(d+1-b,limit-b))
    hneeded=(d+1<=limit)
    mx=max(rrmax,d if hneeded else 0,min(d,limit) if top_recovery else 0)
    zeta=omega*pow(eta,-1,P)%P
    for t in range(1,mx+1):
        q=step(q,eta)
        for a in range(r):
            w=a% (1<<t)
            if not (w>=1<<(t-1) and '0'*b not in format(w,f'0{t}b')): q[a]=0
        if t<=rrmax:
            for a,val in enumerate(q):
                w=a%(1<<t)
                if not w&1:continue
                y=((1<<b)*(a-w)+w)%r
                out[b+t][(1<<b)*y]=(out[b+t][(1<<b)*y]+pow(zeta,gamma(w),P)*val)%P
        if t==d and hneeded:
            for a,val in enumerate(q):
                for bit in (0,1):
                    w=2*a+bit
                    if w>=1<<d and '0'*b not in format(w,f'0{d+1}b'):
                        assert w in z['A']
                        factor=pow(omega,gamma(w),P)*pow(pow(eta,gamma(a),P),-1,P)%P
                        out[d+1][w]=(out[d+1][w]+factor*val)%P
        if top_recovery and t==limit:
            for a,val in enumerate(q):
                w=a%(1<<t); y=((1<<b)*(a-w)+w)%N
                if y in z['E']: recover[y]=(recover[y]+pow(zeta,gamma(w),P)*val)%P
    return out,recover

def compressed_inverse(z,f):
    n=z['n']; N=z['N']; rho=[v[:] for v in f]; v=[]; yE=[0]*N
    for j in range(n+1):
        v.append(rho[j][:])
        feedback,rec=compressed_feedback(z,v[j],n-j,True)
        add(yE,rec)
        for L in range(1,n-j+1): add(rho[j+L],feedback[L])
    return v,yE

def oracle_inverse(z,f):
    state=[0]*z['N']; v=[]
    for j in range(z['n']+1):
        if j:state=step(state,z['omega'])
        add(state,f[j]); v.append([state[s] if s in z['T'] else 0 for s in range(z['N'])])
    return v,[state[s] if s in z['E'] else 0 for s in range(z['N'])]

def rank(rows):
    rows=[r[:] for r in rows]; pivot=0
    for col in range(len(rows[0]) if rows else 0):
        hit=next((j for j in range(pivot,len(rows)) if rows[j][col]),None)
        if hit is None:continue
        rows[pivot],rows[hit]=rows[hit],rows[pivot]
        inv=pow(rows[pivot][col],-1,P); rows[pivot]=[v*inv%P for v in rows[pivot]]
        for j in range(pivot+1,len(rows)):
            a=rows[j][col]
            if a:rows[j]=[(v-a*w)%P for v,w in zip(rows[j],rows[pivot])]
        pivot+=1
        if pivot==len(rows):break
    return pivot

counts=dict(parameters=0,global_source_basis=0,retained_feedback_basis=0,polynomial_inverses=0,fresh_recoveries=0,source_rank_cases=0,moment_controls=0)
records=[]
for n in range(2,8):
    for b in range(1,n):
        z=prepared(n,b); N=z['N']; d=z['d']; counts['parameters']+=1
        columns=[]
        for s in range(N):
            x=[0]*N; x[s]=1
            a=layered_source(z,x); c=oracle_source(z,x); assert a==c
            if N<=32:columns.append([a[L][q] for L in range(d+1) for q in sorted(z['T'])])
            counts['global_source_basis']+=1
        if columns:
            assert rank(list(map(list,zip(*columns))))==N; counts['source_rank_cases']+=1
        for s in sorted(z['T']):
            u=[0]*N;u[s]=1
            assert compressed_feedback(z,u)[0]==oracle_feedback(z,u)
            counts['retained_feedback_basis']+=1
        f=[[(j*17+s*13+7)%P if s in z['T'] else 0 for s in range(N)] for j in range(n+1)]
        assert compressed_inverse(z,f)==oracle_inverse(z,f); counts['polynomial_inverses']+=1
        x=[(s*s+7*s+19)%P for s in range(N)]
        v,ye=compressed_inverse(z,layered_source(z,x)); y=x
        for _ in range(n):y=step(y,z['omega'])
        assert [(v[n][s]+ye[s])%P for s in range(N)]==y;counts['fresh_recoveries']+=1
        sizes=[len(z['layers'][h]) for h in range(1,d+1)]
        S=sum((h+1)*e for h,e in enumerate(sizes))
        assert S<=N*((1<<(b+1))-b-2)
        vinv=sum(e*max(b,d-h) for h,e in enumerate(sizes))
        vjoint=sum(e*(n-h) for h,e in enumerate(sizes))
        brute_inv=0;brute_joint=0
        for j in range(n+1):
            mx=max(max(0,min(d+1-b,n-j-b)),d if j+d+1<=n else 0)
            brute_inv+=sum(sizes[:mx]); brute_joint+=sum(sizes[:min(d,n-j)])
        assert vinv==brute_inv and vjoint==brute_joint
        records.append(dict(n=n,b=b,E=len(z['E']),Rstar=len(z['T']),layer_sizes=sizes,source_moment=S,inverse_visits=vinv,joint_visits=vjoint))
# Exact rational infinite-moment identity via the avoiding-word generating function.
for b in range(1,65):
    z=Fraction(1,2)
    U=sum(z**j for j in range(b)); Up=sum(j*z**(j-1) for j in range(1,b))
    V=1-sum(z**j for j in range(1,b+1)); Vp=-sum(j*z**(j-1) for j in range(1,b+1))
    A=U/V; Ap=(Up*V-U*Vp)/(V*V)
    assert (A+z*Ap)/2**(b+1)==2**(b+1)-b-2
    counts['moment_controls']+=1
# Explicit changed-language counterexample: old suffix-only K_4 e_0 != new one.
z=prepared(4,2); u=[0]*16;u[0]=1
old=u[:];oldout=None
for L in range(1,5):
    old=step(old,z['omega'])
    oldout=[old[s] if s in z['R'] else 0 for s in range(16)]
    old=[old[s] if s not in z['R'] else 0 for s in range(16)]
new=oracle_feedback(z,u)[4]
assert oldout[12]==64 and not any(new)
result=dict(field=P,counts=counts,parameters=records,counterexample=dict(n=4,b=2,omega=64,input_index=0,old_degree4_output_index=12,old_value=64,new_degree4_value=0))
(ROOT/'MARKER_CUT_CONTROLS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
lines=['Exact marker-cut controls passed.']+[f'{k}: {v}' for k,v in counts.items()]+['Counterexample: N=16, b=2, old K_4 e_0 has value 64 at state 12; new K_4 e_0 is zero.']
(ROOT/'EXACT_RUN.log').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
