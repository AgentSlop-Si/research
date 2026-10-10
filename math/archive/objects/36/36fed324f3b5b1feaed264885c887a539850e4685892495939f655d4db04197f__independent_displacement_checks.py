#!/usr/bin/env python3
"""Fresh auditor implementation. Constructor and uploaded code are never imported."""
import json,random
from pathlib import Path

def zeros(a,b=None):return [[0]*(a if b is None else b) for _ in range(a)]
def I(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(A,B,p,k=1):return [[(a+k*b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def scale(A,k,p):return [[k*x%p for x in row] for row in A]
def mm(A,B,p):
    R=zeros(len(A),len(B[0]))
    for i,row in enumerate(A):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(B[k]):
                    if y:R[i][j]=(R[i][j]+x*y)%p
    return R
def mv(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]
def vv(x,y,p,k=1):return [(a+k*b)%p for a,b in zip(x,y)]
def dot(x,y,p):return sum(a*b for a,b in zip(x,y))%p
def inv(A,p):
    n=len(A);R=[r[:]+s for r,s in zip(A,I(n))]
    for j in range(n):
        k=next((k for k in range(j,n) if R[k][j]),None)
        if k is None:return None
        R[j],R[k]=R[k],R[j];a=pow(R[j][j],-1,p);R[j]=[x*a%p for x in R[j]]
        for k in range(n):
            if k!=j:
                a=R[k][j];R[k]=[(x-a*y)%p for x,y in zip(R[k],R[j])]
    return [r[n:] for r in R]
def det(A,p):
    R=[r[:] for r in A];d=1
    for j in range(len(R)):
        k=next((k for k in range(j,len(R)) if R[k][j]),None)
        if k is None:return 0
        if k!=j:R[j],R[k]=R[k],R[j];d=-d
        d=d*R[j][j]%p;a=pow(R[j][j],-1,p)
        for k in range(j+1,len(R)):
            z=R[k][j]*a%p;R[k]=[(x-z*y)%p for x,y in zip(R[k],R[j])]
    return d%p
def rank(A,p):
    R=[r[:] for r in A];h=0
    for j in range(len(R[0])):
        k=next((k for k in range(h,len(R)) if R[k][j]),None)
        if k is None:continue
        R[h],R[k]=R[k],R[h];a=pow(R[h][j],-1,p);R[h]=[x*a%p for x in R[h]]
        for k in range(h+1,len(R)):
            a=R[k][j];R[k]=[(x-a*y)%p for x,y in zip(R[k],R[h])]
        h+=1
        if h==len(R):break
    return h
def sub(A,rows,cols):return [[A[i][j] for j in cols] for i in rows]
def tr(A):return [list(r) for r in zip(*A)]
def function(n,m,f,weights):
    A=zeros(n,m)
    for j in range(m):A[f(j)%n][j]=weights[j]
    return A
def border(A,a,b,c):return [r+[a[i]] for i,r in enumerate(A)]+[b+[c]]
def disp(X,A,Y,p):return add(mm(X,A,p),mm(A,Y,p),p,-1)
def poly_eval(Cs,z,p):
    A=zeros(len(Cs[0]),len(Cs[0][0]));t=1
    for C in Cs:A=add(A,C,p,t);t=t*z%p
    return A

def setup(N,p,w):
    n=N.bit_length()-1;m=N//2;l=N//4
    A0=function(N,N,lambda j:2*j,[1]*N);A1=function(N,N,lambda j:2*j+1,[pow(w,j,p) for j in range(N)]);Q=add(A0,A1,p)
    E0=zeros(N);E0[0]=[1]*N;C=zeros(m,N)
    for j in range(m):C[j][j]=pow(w,j,p);C[j][j+m]=-pow(w,j,p)%p
    J=function(N,m,lambda j:2*j+1,[1]*m)
    K=[];H=[];power=I(N)
    for a in range(n):
        k=add(power,E0,p,-1);K.append(k);H.append(mm(mm(C,k,p),J,p));power=mm(A0,power,p)
    ev=list(range(0,m,2));od=list(range(1,m,2));F=[sub(A,ev,ev) for A in H];G=[sub(A,ev,od) for A in H];R=sub(H[0],od,ev);T=sub(H[0],od,od)
    assert all(sub(A,od,ev)==zeros(l) and sub(A,od,od)==zeros(l) for A in H[1:])
    E=zeros(l);E[0]=[1]*l
    V=function(l,l,lambda j:4*j+1,[pow(w,8*j+2,p) for j in range(l)])
    assert F[0]==G[0]==scale(E,-1,p) and F[1]==add(V,E,p,-1)
    assert R==function(l,l,lambda j:2*j,[pow(w,4*j+1,p) for j in range(l)])
    assert T==function(l,l,lambda j:2*j+1,[pow(w,4*j+3,p) for j in range(l)])
    Ws=[I(l)]
    for _ in range(n):Ws.append(mm(T,Ws[-1],p))
    Ms=[]
    for d in range(n+1):
        S=I(l) if d==0 else scale(F[d-1] if d-1<n else zeros(l),-1,p)
        if d>=2:
            for a in range(d-1):S=add(S,mm(mm(G[a],Ws[d-2-a],p),R,p),p,-1)
        beta=[0]*l
        if d==1:beta=[p-1]*l
        if d>=2:beta=scale(mm(mm([[1]*l],Ws[d-2],p),R,p),-1,p)[0]
        Ms.append(border(S,[-int(d==0 and i==0)%p for i in range(l)],beta,(int(d==0)-int(d==1))%p))
    assert sub(Ms[1],range(l),range(l))==E
    assert sub(Ms[2],range(l),range(l))==add(add(scale(V,-1,p),E,p),mm(E,R,p),p)
    return n,m,l,Q,C,J,K,F,G,R,T,Ws,Ms

def main():
    rng=random.Random(12102026);out={'policy':'Only auditor-authored code executed','minors':[],'scalar_identities':[],'marked_recoveries':[],'kernel_controls':[],'formal_recurrences':[],'guard_countercontrols':[]}
    for p,base in [(65537,3),(257,3)]:
      for N in [8,16,32,64,128]:
        w=pow(base,(p-1)//N,p);assert pow(w,N//2,p)==p-1
        n,m,l,Q,C,J,K,Fc,Gc,R,T,Ws,Ms=setup(N,p,w)
        sco=[sub(A,range(l),range(l)) for A in Ms[:3]];charts=[]
        for style in range(2):
            weights=[1 if style==0 else rng.randrange(1,p) for j in range(l)]
            for left,right in [(0,0),(0,1),(7,19)]:
                L=function(l,l,lambda j:j+1,weights[:-1]+[left]);B=function(l,l,lambda j:j+1,weights[:-1]+[right]);charts.append(('shift',L,B))
                if l>=4:
                    rows=[4*i+2 for i in range(l//4)];cols=list(range(l//4));mats=[sub(disp(L,A,B,p),rows,cols) for A in sco]
                    assert mats[:2]==[zeros(l//4)]*2
                    expected=[[(-pow(w,8*j+2,p)*weights[4*j+1])%p if i==j else 0 for j in cols] for i in cols]
                    assert mats[2]==expected and det(expected,p)!=0
                    out['minors'].append({'N':N,'field':p,'chart':'shift','style':style,'wraps':[left,right],'size':l//4,'leading_det':det(expected,p)})
        for b in [0,1]:
            weights=[rng.randrange(1,p) for j in range(l)];X=function(l,l,lambda j:2*j+b,weights);charts.append(('tree',X,X))
            if l>=8:
                rows=[8*i+2+b for i in range(l//8)];cols=list(range(l//8));mats=[sub(disp(X,A,X,p),rows,cols) for A in sco]
                assert mats[:2]==[zeros(l//8)]*2
                expected=[[(-pow(w,8*j+2,p)*weights[4*j+1])%p if i==j else 0 for j in cols] for i in cols]
                assert mats[2]==expected and det(expected,p)
                out['minors'].append({'N':N,'field':p,'chart':'doubling','b':b,'size':l//8,'leading_det':det(expected,p)})
            u=[0]*l;u[0]=pow(weights[0],-1,p);u[l//2]=-pow(weights[l//2],-1,p)%p;v=[int(j==1-b) for j in range(l)];A=[[x*y%p for y in v] for x in u]
            assert rank(A,p)==1 and mm(X,A,p)==mm(A,X,p)==zeros(l) and A[0][1-b]!=0
            out['kernel_controls'].append({'N':N,'field':p,'b':b,'dimension_at_least':l*l//4})
        # An arbitrary noncommuting dense intermediary, not a reused tree choice.
        Y=[[rng.randrange(p) for j in range(l)] for i in range(l)]
        for z in [0,1,2,5,w]:
            D=add(I(l),T,p,-z);W=inv(D,p);q=(1-z*pow(w,-1,p))%p;assert det(D,p)==q
            if W is None:
                if N<=32:out['guard_countercontrols'].append({'N':N,'field':p,'z':z,'q':q,'full_det':det(add(I(N),Q,p,-z),p)})
                continue
            F=poly_eval(Fc,z,p);G=poly_eval(Gc,z,p);S=add(add(I(l),F,p,-z),mm(mm(G,W,p),R,p),p,-z*z)
            beta=vv([-z%p]*l,mm(mm([[1]*l],W,p),R,p)[0],p,-z*z);M=border(S,[-int(i==0)%p for i in range(l)],beta,(1-z)%p);Si=inv(S,p);Mi=inv(M,p)
            assert add(mm(Y,W,p),mm(W,Y,p),p,-1)==scale(mm(mm(W,disp(Y,T,Y,p),p),W,p),z,p)
            for name,L,B in charts:
                dF=disp(L,F,B,p);dG=add(mm(L,G,p),mm(G,Y,p),p,-1);dR=add(mm(Y,R,p),mm(R,B,p),p,-1);dT=disp(Y,T,Y,p)
                inn=add(mm(mm(dG,W,p),R,p),mm(mm(G,W,p),dR,p),p)
                inn=add(inn,mm(mm(mm(mm(G,W,p),dT,p),W,p),R,p),p,z)
                res=add(add(add(L,B,p,-1),dF,p,-z),inn,p,-z*z);assert disp(L,S,B,p)==res
                bl=border(L,[0]*l,[0]*l,9);br=border(B,[0]*l,[0]*l,9)
                explicit=border(res,[(-L[i][0]+9*int(i==0))%p for i in range(l)],vv([9*x%p for x in beta],mv(tr(B),beta,p),p,-1),0)
                assert disp(bl,M,br,p)==explicit
                if Si is not None:assert disp(B,Si,L,p)==scale(mm(mm(Si,res,p),Si,p),-1,p) and rank(disp(B,Si,L,p),p)==rank(res,p)
                if Mi is not None:assert disp(br,Mi,bl,p)==scale(mm(mm(Mi,explicit,p),Mi,p),-1,p)
                if name=='tree' and Si is not None:assert rank(add(S,mm(mm(L,S,p),Y,p),p,-1),p)>=l//2
                out['scalar_identities'].append({'N':N,'field':p,'z':z,'chart':name,'rank':rank(res,p),'S_invertible':Si is not None,'M_invertible':Mi is not None})
            if N<=64 and Mi is not None:
                x=[rng.randrange(p) for _ in range(N)];h=[rng.randrange(p) for _ in range(N)];Kz=poly_eval(K,z,p);kx=mv(Kz,x,p);f=mv(C,kx,p);fE=f[::2];fO=f[1::2];wf=mv(W,fO,p)
                g=vv(fE,mv(G,wf,p),p,z);sigma=(sum(x)+z*sum(wf))%p;et=mv(Mi,g+[sigma],p);e=et[:-1];t=et[-1];o=mv(W,vv(fO,mv(R,e,p),p,z),p);u=[0]*m;u[::2]=e;u[1::2]=o
                y=vv(kx,mv(Kz,mv(J,u,p),p),p,z);y[0]=(y[0]+t)%p
                assert mv(add(I(N),Q,p,-z),y,p)==x
                aa=scale(mm([h],mm(Kz,J,p),p),z,p)[0];aE=aa[::2];aO=aa[1::2];pm=vv(aE,mm(mm([aO],W,p),R,p)[0],p,z);c=(dot(h,kx,p)+dot(aO,wf,p))%p
                assert (c+dot(pm,e,p)+h[0]*t)%p==dot(h,y,p)
                out['marked_recoveries'].append({'N':N,'field':p,'z':z,'full_equations':N,'marker_checked':True})
        # Formal recurrence: arbitrary polynomial RHS and independently full recovered constant-input jet.
        if N<=32:
            rhs=[[rng.randrange(p) for _ in range(l+1)] for d in range(n+1)];sol=[];M0inv=inv(Ms[0],p)
            for d in range(n+1):
                v=rhs[d][:]
                for k in range(1,d+1):v=vv(v,mv(Ms[k],sol[d-k],p),p,-1)
                sol.append(mv(M0inv,v,p))
            for d in range(n+1):
                got=[0]*(l+1)
                for k in range(d+1):got=vv(got,mv(Ms[k],sol[d-k],p),p)
                assert got==rhs[d]
            x=[rng.randrange(p) for _ in range(N)];kx=[mv(A,x,p) for A in K]+[[0]*N];fs=[mv(C,a,p) for a in kx];rhs=[]
            for d in range(n+1):
                gd=fs[d][::2][:];sd=sum(x)%p if d==0 else 0
                if d>=1:
                    for a in range(d):
                        sd=(sd+sum(mv(Ws[a],fs[d-1-a][1::2],p)))%p
                        for b in range(d-a):
                            if b<len(Gc):gd=vv(gd,mv(Gc[b],mv(Ws[a],fs[d-1-a-b][1::2],p),p),p)
                rhs.append(gd+[sd])
            sol=[]
            for d in range(n+1):
                v=rhs[d][:]
                for k in range(1,d+1):v=vv(v,mv(Ms[k],sol[d-k],p),p,-1)
                sol.append(mv(M0inv,v,p))
            us=[]
            for d in range(n+1):
                od=[0]*l
                for a in range(d+1):
                    inner=fs[d-a][1::2][:]
                    if d-a>=1:inner=vv(inner,mv(R,sol[d-a-1][:-1],p),p)
                    od=vv(od,mv(Ws[a],inner,p),p)
                u=[0]*m;u[::2]=sol[d][:-1];u[1::2]=od;us.append(u)
            qx=x[:]
            for d in range(n+1):
                yd=kx[d][:]
                for a in range(d):
                    if a<len(K):yd=vv(yd,mv(K[a],mv(J,us[d-1-a],p),p),p)
                yd[0]=(yd[0]+sol[d][-1])%p;assert yd==qx;qx=mv(Q,qx,p)
            out['formal_recurrences'].append({'N':N,'field':p,'degree':n,'arbitrary_polynomial_source':True,'full_constant_input_recovery_coefficients':N*(n+1)})
    out['result']='PASS';Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:len(v) for k,v in out.items() if isinstance(v,list)}|{'result':'PASS'}))
if __name__=='__main__':main()
