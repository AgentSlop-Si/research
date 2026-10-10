"""New exact controls; no imported or executed uploaded code."""
import json
from pathlib import Path
p=65537

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def add(A,B): return [[(a+b)%p for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def scale(c,A): return [[c*a%p for a in row] for row in A]
def sub(A,B): return add(A,scale(-1,B))
def mul(A,B):
    Bt=list(zip(*B)); return [[sum(a*b for a,b in zip(row,col))%p for col in Bt] for row in A]
def mv(A,v): return [sum(a*b for a,b in zip(row,v))%p for row in A]
def inv(A):
    n=len(A); M=[row[:]+eye for row,eye in zip(A,ident(n))]
    for j in range(n):
        k=next(k for k in range(j,n) if M[k][j])
        M[j],M[k]=M[k],M[j]; z=pow(M[j][j],-1,p); M[j]=[a*z%p for a in M[j]]
        for i in range(n):
            if i!=j and M[i][j]:
                z=M[i][j]; M[i]=[(a-z*b)%p for a,b in zip(M[i],M[j])]
    return [row[n:] for row in M]
def nonzero(A): return any(any(row) for row in A)
def rowsupp(A): return max(sum(a!=0 for a in row) for row in A)
def green_apply(c,w,cycle,x):
    n=len(w); pref=1; total=0
    for i in cycle:
        total=(total+pref*x[i])%p
        pref=pref*c*w[i]%p
    z=[0]*n; z[cycle[0]]=total*pow((1-pref)%p,-1,p)%p
    for k in range(n-1,0,-1):
        i=cycle[k]; nxt=cycle[(k+1)%n]
        z[i]=(x[i]+c*w[i]*z[nxt])%p
    return z

def make_case(n,cycle,w,a,b,lam,seed_control=False):
    I=ident(n); W=[[0]*n for _ in range(n)]; e=[0]*n
    for k,i in enumerate(cycle): W[i][cycle[(k+1)%n]]=w[i]; e[i]=1 if k%2==0 else p-1
    E=[[e[i] if i==j else 0 for j in range(n)] for i in range(n)]
    rho=1
    for wi in w: rho=rho*wi%p
    assert all((1-pow(c,n,p)*rho)%p for c in (a,b))
    Ca=sub(scale(2,inv(sub(I,scale(a,W)))),I)
    Cb=sub(scale(2,inv(sub(I,scale(b,W)))),I)
    A=Ca; B=scale(lam,mul(Cb,E)); K=mul(B,A)
    assert mul(E,mul(W,E))==scale(-1,W)
    assert mul(K,K)==scale(lam*lam,I)
    assert any(K[i][j] != (K[0][0] if i==j else 0) for i in range(n) for j in range(n))
    H=sub(I,K); Jfb=sub(I,mul(A,B)); qden=pow((1-lam*lam)%p,-1,p)
    T=mul(inv(H),B)
    Tformula=scale(qden,add(scale(lam,mul(Cb,E)),scale(lam*lam,inv(Ca))))
    assert T==Tformula
    assert T==scale(qden,add(B,mul(K,B)))
    P=mul(sub(I,scale(b,W)),add(I,scale(a,W)))
    PT=mul(P,T)
    expected=scale(qden,add(scale(lam,mul(mul(add(I,scale(a,W)),add(I,scale(b,W))),E)),scale(lam*lam,mul(sub(I,scale(b,W)),sub(I,scale(a,W))))))
    assert PT==expected and rowsupp(P)<=3 and rowsupp(PT)<=3
    om=pow(3,(p-1)//n,p); F=[[pow(om,i*j,p) for j in range(n)] for i in range(n)]
    D=[[pow(om,i,p) if i==j else 0 for j in range(n)] for i in range(n)]
    S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
    cov=sub(mul(D,T),mul(T,S))
    c1=sub(mul(H,mul(D,B)),mul(B,mul(S,Jfb)))
    assert c1==mul(H,mul(cov,Jfb))
    if n>9 or (a==0 and n>4): assert nonzero(cov)
    ones=[1]*n; e0=[int(i==0) for i in range(n)]
    seed=(mv(T,e0)==ones)
    assert seed == (mv(H,ones)==mv(B,e0))
    if seed_control: assert seed
    checked_vectors=0
    for j in range(n):
        x=[int(i==j) for i in range(n)]
        def appA(v): return [(2*u-z)%p for u,z in zip(green_apply(a,w,cycle,v),v)]
        def appB(v):
            ev=[s*z%p for s,z in zip(e,v)]
            return [lam*(2*u-z)%p for u,z in zip(green_apply(b,w,cycle,ev),ev)]
        ax=appA(x); bx=appB(x)
        assert ax==mv(A,x) and bx==mv(B,x)
        horner=[qden*(u+v)%p for u,v in zip(bx,appB(appA(bx)))]
        assert horner==mv(T,x)
        checked_vectors+=1
    return dict(N=n,a=a,b=b,lambda_=lam,seed_control=seed_control,seed_pass=seed,covariance_pass=not nonzero(cov),exact_minimal_degree=2,max_P_rowsupp=rowsupp(P),max_PT_rowsupp=rowsupp(PT),basis_vectors=checked_vectors)

def main():
    result=[]
    for n in (2,4,8,16,32,64):
        for reverse in (False,True):
            cycle=list(range(n)) if not reverse else [0]+list(range(n-1,0,-1))
            w=[i+2 for i in range(n)]
            result.append(make_case(n,cycle,w,3,5,2))
        w=[1]*n; w[0]=3; w[-1]=3*pow(5,-1,p)%p
        result.append(make_case(n,list(range(n)),w,0,1,2,True))
    summary={'status':'PASS','prime':p,'cases':len(result),'dense_two_cayley_cases':sum(not x['seed_control'] for x in result),'seed_passing_controls':sum(x['seed_control'] for x in result),'basis_vectors_checked':sum(x['basis_vectors'] for x in result),'operator_output_entries_checked':sum(3*x['N']*x['basis_vectors'] for x in result),'non_scalar_quadratic_checks':len(result),'sparse_multiplied_identities':len(result),'cubic_residual_identities':len(result),'cases_detail':result}
    out=Path(__file__).with_name('TWO_CAYLEY_RESULTS.json'); out.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases_detail'},indent=2))
if __name__=='__main__': main()
