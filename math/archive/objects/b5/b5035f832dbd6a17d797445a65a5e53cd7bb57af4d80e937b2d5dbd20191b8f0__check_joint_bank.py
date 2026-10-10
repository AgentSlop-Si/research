#!/usr/bin/env python3
"""Independent standard-library certificate; no predecessor code is executed."""
import json, hashlib, pathlib, math, time
OUT = pathlib.Path(__file__).resolve().parent
SOURCE_DIRS = [pathlib.Path('research_round_2156/construct_global_chirp_lift'), pathlib.Path('research_round_2156/extend_three_green_family')]

def snapshot():
    return {str(f):hashlib.sha256(f.read_bytes()).hexdigest() for d in SOURCE_DIRS for f in sorted(d.rglob('*')) if f.is_file()}

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def add(a,b,p):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return trim([x%p for x in c])

def scale(a,c,p): return trim([x*c%p for x in a])
def sub(a,b,p): return add(a,scale(b,-1,p),p)
def mul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%p
    return trim(c)

def divmodp(a,b,p):
    a=trim(a); b=trim(b)
    assert b != [0]
    if len(a)<len(b): return [0],a
    q=[0]*(len(a)-len(b)+1); ib=pow(b[-1],-1,p)
    while a != [0] and len(a)>=len(b):
        k=len(a)-len(b); c=a[-1]*ib%p; q[k]=c
        for j,x in enumerate(b): a[j+k]=(a[j+k]-c*x)%p
        a=trim(a)
    return trim(q),a

def rem(a,b,p): return divmodp(a,b,p)[1]
def gcd(a,b,p):
    while b != [0]: a,b=b,rem(a,b,p)
    return scale(a,pow(a[-1],-1,p),p)
def invmod(a,m,p):
    r0,r1=m,rem(a,m,p); s0,s1=[0],[1]
    while r1 != [0]:
        q,r=divmodp(r0,r1,p)
        r0,r1=r1,r; s0,s1=s1,sub(s0,mul(q,s1,p),p)
    assert len(r0)==1 and r0[0]
    return rem(scale(s0,pow(r0[0],-1,p),p),m,p)
def mmul(a,b,m,p): return rem(mul(a,b,p),m,p)
def xmul(a,m,p):
    r=len(m)-1; a=a+[0]*(r-len(a)); c=a[-1]
    return [( (a[i-1] if i else 0)-c*m[i])%p for i in range(r)]

def solve(M,b,p):
    n=len(b); a=[[x%p for x in M[i]]+[b[i]%p] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]); a[j],a[k]=a[k],a[j]
        inv=pow(a[j][j],-1,p); a[j]=[x*inv%p for x in a[j]]
        for i in range(j+1,n):
            t=a[i][j]
            if t:
                for k in range(j,n+1): a[i][k]=(a[i][k]-t*a[j][k])%p
    x=[0]*n
    for i in range(n-1,-1,-1): x[i]=(a[i][n]-sum(a[i][j]*x[j] for j in range(i+1,n)))%p
    return x

def orthopoly(j,f,p):
    if j==0: return [1]
    return solve([[f[i+k] for k in range(j)] for i in range(j)],[-f[i+j] for i in range(j)],p)+[1]

def trace_powers(m,p):
    r=len(m)-1; s=[r%p]
    for k in range(1,r):
        s.append((-k*m[r-k]-sum(m[r-j]*s[k-j] for j in range(1,k)))%p)
    return s

def trace(v,s,p): return sum(x*y for x,y in zip(v,s))%p

def make_bank(N,w,p,sign):
    r=(N+1)//2; h=pow(2,-1,N)
    f=[pow(w,(sign*h*k*k)%N,p) for k in range(N+1)]
    P=orthopoly(r,f,p); R=orthopoly(r-1,f,p)
    def explicit_polynomial(j):
        v=[1]; root=1; step=pow(w,sign%N,p)
        for _ in range(j):
            v=mul(v,[-root%p,1],p); root=root*step%p
        return [f[j]*v[l]*pow(f[l],-1,p)%p for l in range(j+1)]
    assert P==explicit_polynomial(r) and R==explicit_polynomial(r-1)
    assert gcd(P,R,p)==[1]
    XN=[p-1]+[0]*(N-1)+[1]
    bad=[]
    for tau in range(2*N+1):
        m=add(P,scale(R,tau,p),p)
        dm=[(i*m[i])%p for i in range(1,len(m))]
        if m[0] and gcd(m,dm,p)==[1] and gcd(m,XN,p)==[1]: break
        bad.append(tau)
    else: raise AssertionError('No legal moment polynomial')
    for k in range(r-1): assert sum(m[j]*f[k+j] for j in range(r+1))%p==0
    Q=[sum(m[j+1+l]*f[l] for l in range(r-j))%p for j in range(r)]
    b=mmul(Q,invmod(dm,m,p),m,p)
    assert gcd(b,m,p)==[1]
    zN=[1]
    for _ in range(N): zN=xmul(zN,m,p)
    closure=sub([1],zN,p); iclosure=invmod(closure,m,p)
    a=mmul(closure,b,m,p); assert gcd(a,m,p)==[1]
    traces=trace_powers(m,p)
    zkb=b; moments=[]
    for k in range(N):
        moments.append(trace(zkb,traces,p)); zkb=xmul(zkb,m,p)
    assert moments==f[:N]
    ell=[]; zka=a
    for k in range(r): ell.append(trace(zka,traces,p)); zka=xmul(zka,m,p)
    bank={'N':N,'p':p,'omega':w,'sign':sign,'r':r,'tau':tau,'rejected_tau':bad,'polynomial':m,'numerator':Q,'weight':a,'trace_functional':ell,'inverse_closure':iclosure,'moments':moments}
    return bank

def apply_bank(bank,x):
    p=bank['p']; m=bank['polynomial']; r=bank['r']; N=bank['N']; ell=bank['trace_functional']
    h=[0]*r
    for v in reversed(x): h=xmul(h,m,p); h[0]=(h[0]+v)%p
    y0=mmul(bank['inverse_closure'],h,m,p); y0+= [0]*(r-len(y0))
    out=[trace(y0,ell,p)]; yi=y0
    tail=[]
    for i in range(N-1,0,-1):
        yi=xmul(yi,m,p); yi[0]=(yi[0]+x[i])%p
        tail.append(trace(yi,ell,p))
    return out+list(reversed(tail))

def matmul(A,B,p):
    cols=list(zip(*B))
    return [[sum(x*y for x,y in zip(row,col))%p for col in cols] for row in A]
def mv(A,x,p): return [sum(a*b for a,b in zip(row,x))%p for row in A]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def rank(A,p):
    a=[row[:] for row in A]; n=len(a); nc=len(a[0]) if n else 0; k=0
    for j in range(nc):
        pos=next((i for i in range(k,n) if a[i][j]),None)
        if pos is None: continue
        a[k],a[pos]=a[pos],a[k]; iv=pow(a[k][j],-1,p); a[k]=[v*iv%p for v in a[k]]
        for i in range(k+1,n):
            t=a[i][j]
            if t: a[i]=[(v-t*w)%p for v,w in zip(a[i],a[k])]
        k+=1
        if k==n: break
    return k

def root_of_unity(N,p):
    for g in range(2,p):
        w=pow(g,(p-1)//N,p)
        if pow(w,N,p)==1 and all(pow(w,k,p)!=1 for k in range(1,N) if N%k==0): return w
    raise AssertionError('No root')

def full_control(N,p):
    w=root_of_unity(N,p); h=pow(2,-1,N); G=sum(pow(w,h*k*k%N,p) for k in range(N))%p; c=N*G%p
    assert (1+c)%p
    den=pow(1+c,-1,p)
    F=[[pow(w,i*j%N,p) for j in range(N)] for i in range(N)]
    A=[pow(w,h*i*i%N,p) for i in range(N)]; D=[pow(a,-1,p) for a in A]; D2=[d*d%p for d in D]
    H=[[pow(w,(-h*(i+j)**2)%N,p) for j in range(N)] for i in range(N)]
    B=[[(F[i][j]-G*H[i][j]+(c*D[i] if i==j else 0))*den%p for j in range(N)] for i in range(N)]
    banks=[make_bank(N,w,p,s) for s in [-1,1]]
    for i in range(N):
        for j in range(N):
            assert B[i][j]==(A[i]*banks[0]['moments'][(j-i)%N]*A[j]-G*D2[i]*banks[1]['moments'][(j-i)%N]*D2[j]+(c*D[i] if i==j else 0))*den%p
    # Test actual quotient-algebra Green solve, not only moment interpolation.
    test_vectors=[[((i+1)**3+7*i+11)%p for i in range(N)], [int(i==0) for i in range(N)], [int(i==N-1) for i in range(N)]]
    for x in test_vectors:
        zs=[apply_bank(banks[0],[A[i]*x[i]%p for i in range(N)]),apply_bank(banks[1],[D2[i]*x[i]%p for i in range(N)])]
        y=[(A[i]*zs[0][i]-G*D2[i]*zs[1][i]+c*D[i]*x[i])*den%p for i in range(N)]
        assert y==mv(B,x,p)
    cubic_inverse_checked=N<=65
    if cubic_inverse_checked:
        FA=[[F[i][j]*A[j]%p for j in range(N)] for i in range(N)]
        cube=matmul(matmul(FA,FA,p),FA,p)
        assert cube==[[c*int(i==j)%p for j in range(N)] for i in range(N)]
        Finv=[[pow(N,-1,p)*pow(w,(-i*j)%N,p)%p for j in range(N)] for i in range(N)]
        M=[[(Finv[i][j]+(A[i] if i==j else 0))%p for j in range(N)] for i in range(N)]
        assert matmul(M,B,p)==eye(N) and matmul(B,M,p)==eye(N)
        BA=[[B[i][j]*A[j]%p for j in range(N)] for i in range(N)]
        BAB=matmul(BA,B,p); BABAB=matmul(BA,BAB,p)
        recovered=[[( (1+c)*B[i][j]+(1-2*c)*BAB[i][j]+(1+c)*BABAB[i][j])%p for j in range(N)] for i in range(N)]
        assert recovered==F
    crt_checked=False; square_checked=False
    if N%5==0 and math.gcd(5,N//5)==1:
        m=N//5; e5=m*pow(m,-1,5); em=5*pow(5,-1,m) if m>1 else 0
        eta=pow(w,e5,p); theta=pow(w,em,p); h5=3; hm=pow(2,-1,m) if m>1 else 0
        for aa in range(5):
            for b in range(m):
                i=(e5*aa+em*b)%N
                for cc in range(5):
                    for d in range(m):
                        j=(e5*cc+em*d)%N
                        assert F[i][j]==pow(eta,aa*cc%5,p)*pow(theta,b*d%m,p)%p
                        assert H[i][j]==pow(eta,-h5*(aa+cc)**2%5,p)*pow(theta,-hm*(b+d)**2%m,p)%p
        crt_checked=True
        q=math.isqrt(m)
        if q*q==m:
            assert sum(pow(theta,hm*k*k%m,p) for k in range(m))%p==q%p
            zeta=pow(theta,q,p)
            for s in range(q):
                for t in range(q):
                    for r in range(q):
                        for u in range(q):
                            b=s+q*r; d=t+q*u
                            assert pow(theta,b*d%m,p)==pow(theta,s*t%m,p)*pow(zeta,(r*t+s*u)%q,p)%p
                            assert pow(theta,-hm*(b+d)**2%m,p)==pow(theta,-hm*(s+t)**2%m,p)*pow(zeta,-(s+t)*(r+u)%q,p)%p
            square_checked=True
    k=N//2; natural_rank=rank([row[k:] for row in B[:k]],p)
    assert natural_rank==k
    return {'N':N,'p':p,'omega':w,'r_each_chirp':(N+1)//2,'nontrivial_full_branches':N+1,'all_entry_bank_checks':N*N,'scan_output_checks':len(test_vectors)*N,'cubic_two_sided_inverse_and_Fourier_recovery':cubic_inverse_checked,'CRT_all_entries':crt_checked,'square_residue_identity':square_checked,'natural_cut_rank':natural_rank,'bank_polynomials':banks}

def restricted_control():
    p=241; eta=91; q=483; g=(1+2*(pow(eta,2,p)+pow(eta,3,p)))%p
    den=pow((1+5*q**3*g)%p,-1,p)
    C=[[(pow(eta,i*j%5,p)-q*g*pow(eta,-3*(i+j)**2%5,p)+(5*q**3*g*pow(eta,-3*i*i%5,p) if i==j else 0))*den%p for j in range(5)] for i in range(5)]
    a,b,cc,e,f,hh=C[0][1],C[0][2],C[1][2],C[1][3],C[1][4],C[2][3]
    alpha=cc*pow(a*b,-1,p)%p; beta=e*pow(a*b,-1,p)%p; gamma=f*pow(a*a,-1,p)%p; eps=hh*pow(b*b,-1,p)%p
    L=(beta*beta-gamma*eps)%p
    M=(-2*alpha*beta+alpha*gamma+alpha*eps+beta*gamma+beta*eps-2*gamma*eps)%p; J=(beta-gamma)**2%p
    modulus=[J*pow(L,-1,p)%p,M*pow(L,-1,p)%p,1]; assert modulus==[124,30,1]
    def plus(x,y): return add(x,y,p)
    def minus(x,y): return sub(x,y,p)
    def times(x,y): return mmul(x,y,modulus,p)
    def div(x,y): return times(x,invmod(y,modulus,p))
    d=[0,1]; d2=times(d,d)
    T=minus(scale(plus(d,[2]),gamma,p),[alpha+beta])
    pole=div(plus(scale(d,gamma,p),scale(d2,alpha+beta,p)),T)
    kap=scale(plus(pole,d2),pow(gamma,-1,p),p)
    x=div(minus(pole,d),kap)
    rr=[x,div(minus([alpha],x),d),div(minus([beta],x),d),div(minus([gamma],x),d)]
    z=div(kap,plus([1],pole)); uu=[[1]]+[scale(rr[i-1],C[0][i],p) for i in range(1,5)]
    vv=[div(z,pole)]+[minus([C[0][i]],times(z,uu[i])) for i in range(1,5)]
    for i in range(5):
        for j in range(i+1,5): assert plus(times(uu[i],vv[j]),times(pole,times(vv[i],uu[j])))==[C[i][j]]
    delta=[minus([C[i][i]],times(plus([1],pole),times(uu[i],vv[i]))) for i in range(5)]
    def norm(y):
        y=y+[0]*(2-len(y)); aa,bb=y
        return (aa*aa-modulus[1]*aa*bb+modulus[0]*bb*bb)%p
    endpoint_norms={'u':[norm(y) for y in uu],'v':[norm(y) for y in vv],'delta':[norm(y) for y in delta]}
    assert endpoint_norms=={'u':[1,44,153,153,44],'v':[41,117,7,7,117],'delta':[72,113,64,64,113]}
    assert norm(pole)==1 and norm(plus([1],pole))==160 and norm(minus([1],pole))==85
    for i in range(5):
        for j in range(5):
            first=times(uu[i],vv[j]); second=times(vv[i],uu[j])
            if i>j: first=times(pole,first)
            else: second=times(pole,second)
            full=plus(first,second)
            if i==j: full=plus(full,delta[i])
            assert full==[C[i][j]]
    tr=plus(pole,invmod(pole,modulus,p)); assert len(tr)==1
    # Independently evaluate predecessor rational n(rho)/d(rho).
    nn=[(7,10,10,0),(7,8,8,2),(3,8,10,4),(-5,-8,-4,2),(-1,-8,-6,0),(-3,-10,-10,0)]
    dd=[(1,0,0,0),(1,-1,-1,1),(-1,-1,0,2),(0,1,3,1),(2,1,2,0),(1,0,0,0)]
    def evalcoeff(v): return sum(c*pow(eta,j,p) for j,c in enumerate(v))%p
    rho=-q*g%p
    num=sum(evalcoeff(v)*pow(rho,k,p) for k,v in enumerate(nn))%p; denom=sum(evalcoeff(v)*pow(rho,k,p) for k,v in enumerate(dd))%p
    assert tr[0]==num*pow(denom,-1,p)%p
    return {'q':q,'p':p,'eta':eta,'target':C,'quadratic':modulus,'all_25_three_Green_entries':True,'all_endpoint_norms':endpoint_norms,'pole_trace':tr[0],'rational_trace_agrees':True,'scope':'Exact finite-field sanity check only; not independent recertification of every characteristic-zero guard.'}

def main():
    before=snapshot(); (OUT/'SOURCE_HASHES_BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
    t=time.time(); controls=[]
    for N,p in [(5,241),(15,31),(45,181),(65,131),(245,491)]:
        control=full_control(N,p); controls.append(control)
        print('PASS',N,p,'rank',control['natural_cut_rank'],'branches',control['nontrivial_full_branches'],flush=True)
    restricted=restricted_control(); after=snapshot(); assert before==after
    result={'status':'PASS','source_files_unchanged':len(before),'seconds':time.time()-t,'controls':controls,'restricted_predecessor_sanity_check':restricted,'scope':'New standard-library code. Exact modular controls supplement uniform characteristic-zero proofs; uploaded and predecessor code were not executed.'}
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n'); (OUT/'SOURCE_HASHES_AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
    print('ALL PASS',result['seconds'],flush=True)
if __name__=='__main__': main()
