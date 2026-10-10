#!/usr/bin/env python3
"""Independent Phase21 exact review controls. No uploaded code imported.
Polynomial and determinant primitives reused from our independent Phase20 audit.
"""
import argparse,json,math,random,itertools
from pathlib import Path
def trim(q):
    q=list(q)
    while q and q[-1]==0:q.pop()
    return q

def pmul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c)
def padd(a,b,p):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a):c[i]=v
    for i,v in enumerate(b):c[i]=(c[i]+v)%p
    return trim(c)
def peval(q,x,p):
    v=0
    for c in reversed(q):v=(v*x+c)%p
    return v

def premainder(a,b,p):
    a=trim(a);b=trim(b);iv=pow(b[-1],-1,p)
    while len(a)>=len(b):
        q=a[-1]*iv%p;shift=len(a)-len(b)
        for i,c in enumerate(b):a[shift+i]=(a[shift+i]-q*c)%p
        a=trim(a)
    return a

def pgcd(a,b,p):
    a,b=trim(a),trim(b)
    while b:a,b=b,premainder(a,b,p)
    return [v*pow(a[-1],-1,p)%p for v in a] if a else []

def determinant(M,p):
    A=[row[:] for row in M];value=1
    for k in range(len(A)):
        j=next((j for j in range(k,len(A)) if A[j][k]%p),None)
        if j is None:return 0
        if j!=k:A[k],A[j]=A[j],A[k];value=-value
        pivot=A[k][k];value=value*pivot%p;iv=pow(pivot,-1,p)
        for i in range(k+1,len(A)):
            q=A[i][k]*iv%p
            for j in range(k,len(A)):A[i][j]=(A[i][j]-q*A[k][j])%p
    return value%p

def dft(r,w,p,count=None):
    n=len(r)
    return [sum(v*pow(w,j*k%n,p) for j,v in enumerate(r))%p for k in range(n if count is None else count)]
def idft(R,w,p):return [v*pow(len(R),-1,p)%p for v in dft(R,pow(w,-1,p),p)]
def interp(xs,ys,p):
    master=[1]
    for x in xs:master=pmul(master,[-x%p,1],p)
    out=[0]*len(xs)
    for x,y in zip(xs,ys):
        q=[0]*len(xs);q[-1]=master[-1]
        for j in range(len(q)-2,-1,-1):q[j]=(master[j+1]+x*q[j+1])%p
        assert (master[0]+x*q[0])%p==0
        denominator=peval(q,x,p);assert denominator
        factor=y*pow(denominator,-1,p)%p
        for j,c in enumerate(q):out[j]=(out[j]+factor*c)%p
    return trim(out)

def pencil(T,w,e,s,p):
    m=s+1;nodes=list(range(m+1));values=[]
    for a in nodes:values.append(determinant([[T[e+i+j]*(1-a*pow(w,e+i+j,p))%p for j in range(m)] for i in range(m)],p))
    return interp(nodes,values,p)

def res(T,w,s,p):
    m=s+1;P=pencil(T,w,0,s,p);Q=pencil(T,w,1,s,p)
    P=(P+[0]*(m+1-len(P)))[::-1];Q=(Q+[0]*(m+1-len(Q)))[::-1]
    A=[]
    for f in [P,Q]:
        for j in range(m):A.append([0]*j+f+[0]*(m-1-j))
    return determinant(A,p)

def compress(T,s,p):
    b=s*(s+1)*(2*s+1)//6;v=s*(s+1)*(4*s+5)//6;q=(s+1)**2
    xs=[];ws=[];vals=[];seen=set()
    for w in range(2,p):
        x=(w+pow(w,-1,p))%p
        if x in seen:continue
        seen.add(x);xs.append(x);ws.append(w)
        val=res(T,w,s,p)*pow(pow(w,v+b,p)*pow(w-1,q,p)%p,-1,p)%p;vals.append(val)
        if len(xs)==b+4:break
    assert len(xs)==b+4
    V=interp(xs[:b+1],vals[:b+1],p)
    assert all(peval(V,x,p)==y for x,y in zip(xs[b+1:],vals[b+1:]))
    U=[0]*(2*b+1)
    for j,c in enumerate(V):
        for k in range(j+1):U[b+j-2*k]=(U[b+j-2*k]+c*math.comb(j,k))%p
    assert U==U[::-1]
    return U

def factor_at_one(f,p):
    f=f[:];out=[0]*(len(f)-1)
    out[-1]=f[-1]
    for j in range(len(out)-2,-1,-1):out[j]=(f[j+1]+out[j+1])%p
    assert (f[0]+out[0])%p==0
    return trim(out)

def algebra_tests():
    rng=random.Random(21010);out=[]
    for p,orders in [(65537,range(1,7)),(12289,range(1,5))]:
        for s in orders:
            T=[rng.randrange(1,p) for _ in range(4*s)];D=(s+1)**2*(2*s+1)
            f=interp(list(range(D+1)),[res(T,w,s,p) for w in range(D+1)],p)
            v=s*(s+1)*(4*s+5)//6;q=(s+1)**2;b=s*(s+1)*(2*s+1)//6
            grade=f+[0]*(D+1-len(f));sign=(-1)**q
            assert all(grade[j]==sign*grade[D-j]%p for j in range(D+1))
            assert not any(f[:v]);U=f[v:]
            for _ in range(q):U=factor_at_one(U,p)
            U+= [0]*(2*b+1-len(U));assert U==U[::-1] and U==compress(T,s,p)
            for w in [D+1,D+2,D+13,p-1]:assert res(T,w,s,p)==pow(w,v,p)*pow(w-1,q,p)*peval(U,w,p)%p
            out.append({'s':s,'field':p,'grade_D':D,'v':v,'one_factor':q,'b':b,'resultant_degree':len(f)-1,'compressed_degree':len(trim(U))-1,'core_samples':b+1,'witness_samples':3})
    degenerates=0
    for s in [1,2,4,8]:
        for T in [[0]*(4*s),[1]*(4*s)]:assert not any(compress(T,s,65537));degenerates+=1
    for s in range(1,65):
        D=(s+1)**2*(2*s+1);v=s*(s+1)*(4*s+5)//6;b=s*(s+1)*(2*s+1)//6
        assert D-sum(max(2*i,2*j+1) for i in range(s+1) for j in range(s+1))==v
        assert D-2*v-(s+1)**2==2*b
    return {'full_reconstructions':out,'degenerate_compressions':degenerates,'symbolic_integer_identity_orders':64}

def solve(A,b,p):
    n=len(b);M=[row[:]+[v] for row,v in zip(A,b)]
    for j in range(n):
        z=next((z for z in range(j,n) if M[z][j]%p),None)
        if z is None:return None
        M[z],M[j]=M[j],M[z];iv=pow(M[j][j],-1,p);M[j]=[x*iv%p for x in M[j]]
        for i in range(n):
            if i!=j:
                q=M[i][j];M[i]=[(x-q*y)%p for x,y in zip(M[i],M[j])]
    return [row[-1] for row in M]

def prony(Y,s,powers,p):
    for d in range(1,s+1):
        c=solve([[Y[i+j] for j in range(d)] for i in range(d)],[-Y[i+d]%p for i in range(d)],p)
        if c is None:continue
        c+=[1]
        if any(sum(c[j]*Y[i+j] for j in range(d+1))%p for i in range(len(Y)-d)):continue
        exps=[e for e,z in enumerate(powers) if peval(c,z,p)==0]
        if len(exps)!=d:continue
        a=solve([[pow(powers[e],k,p) for e in exps] for k in range(d)],Y[:d],p)
        if a is None:continue
        A={e:v for e,v in zip(exps,a) if v}
        if all(sum(v*pow(powers[e],k,p) for e,v in A.items())%p==y for k,y in enumerate(Y)):return A
    return None

def gate(r,w,p,s):
    n=len(r);R=dft(r,w,p,4*s);meta={'full_checks':0,'candidate_roots':0}
    if not all(R):return None,{**meta,'reason':'zero-probe'}
    T=[pow(x,-1,p) for x in R];U=compress(T,s,p)
    if not any(U):return None,{**meta,'reason':'zero-resultant'}
    powers=[pow(w,k,p) for k in range(n)];roots=[d for d in range(1,n) if peval(U,powers[d],p)==0]
    assert len(roots)<=s*(s+1)*(2*s+1)//3;meta['candidate_roots']=len(roots)
    for delta in roots:
        z=powers[delta];g=pgcd(pencil(T,z,0,s,p),pencil(T,z,1,s,p),p)
        if len(g)!=2:continue
        alpha=-g[0]%p
        if not alpha:continue
        Y=[T[k]*(1-alpha*pow(z,k,p))%p for k in range(4*s)];A=prony(Y,s,powers,p)
        if not A:continue
        Ahat=[sum(v*pow(z,e,p) for e,v in A.items())%p for z in powers]
        if not all(Ahat):continue
        meta['full_checks']+=1
        rhs=[(int(j==0)-alpha*int(j==delta))%p for j in range(n)]
        lhs=[sum(v*r[(j-e)%n] for e,v in A.items())%p for j in range(n)]
        if lhs!=rhs:return None,{**meta,'reason':'full-certificate-failed'}
        out=[(1-alpha*pow(w,k*delta,p))*pow(Ahat[k],-1,p)%p for k in range(n)]
        assert out==dft(r,w,p)
        return (A,delta,alpha,out),{**meta,'reason':'accepted'}
    return None,{**meta,'reason':'no-candidate'}

def prime(x):return x>=2 and all(x%d for d in range(2,math.isqrt(x)+1))
def field(n):
    k=100
    while not prime(n*k+1):k+=1
    p=n*k+1;fac=[d for d in range(2,n+1) if n%d==0 and prime(d)]
    for a in range(2,p):
        w=pow(a,k,p)
        if all(pow(w,n//d,p)!=1 for d in fac):return p,w

def sparse_eval(A,w,n,p):return [sum(a*pow(w,k*e,p) for e,a in A.items())%p for k in range(n)]
def sparse_product(A,B,n,p):
    R={}
    for i,a in A.items():
        for j,b in B.items():R[(i+j)%n]=(R.get((i+j)%n,0)+a*b)%p
    return {i:v for i,v in R.items() if v}

def application_tests():
    rng=random.Random(781121);out=[];adversaries=[]
    for n,t,reps in [(30,2,3),(32,1,2),(32,2,3),(64,2,3),(128,2,2),(64,3,1)]:
        p,w=field(n);s=2**t
        for rep in range(reps):
            while True:
                Q={0:1};ds=rng.sample(range(1,n),t);aa=[rng.randrange(2,p) for _ in range(t)]
                for d,a in zip(ds,aa):Q=sparse_product(Q,{0:1,d:-a%p},n,p)
                Qhat=sparse_eval(Q,w,n,p)
                if all(Qhat):break
            u,v=rng.sample(range(n),2);H={u:7,v:11};Hhat=sparse_eval(H,w,n,p)
            R=[a*pow(b,-1,p)%p for a,b in zip(Hhat,Qhat)];r=idft(R,w,p)
            found,meta=gate(r,w,p,s)
            if found:
                assert found[-1]==R
                if n>4*s:
                    k=4*s;corrupt=[(r[j]+pow(w,-k*j%(n),p))%p for j in range(n)]
                    assert dft(corrupt,w,p,4*s)==dft(r,w,p,4*s)
                    f,m=gate(corrupt,w,p,s);assert f is None and m['reason']=='full-certificate-failed';adversaries.append({'N':n,'s':s,'full_checks':m['full_checks']})
            out.append({'N':n,'field':p,'s':s,'actual_Q_terms':len(Q),'meta':meta})
    # Exact Phase20 counterexample is declined here because its second Fourier probe is zero.
    r=[1,50,64,96,22,33,50,75];f,m=gate(r,64,97,2);assert f is None and m["reason"]=="zero-probe"
    out.append({'N':8,'field':97,'s':2,'inherited_guard_counterexample_new_path':m})
    # Probe zero and identically-zero-resultant exclusions.
    p,w=field(32);f,z=gate([0]*32,w,p,4);assert f is None and z['reason']=='zero-probe'
    negatives=[]
    for n in [16,32,64]:
        p,w=field(n)
        for _ in range(3):
            r=[rng.randrange(p) for _ in range(n)];f,m=gate(r,w,p,2)
            assert f is None or f[-1]==dft(r,w,p);negatives.append(m['reason'])
    return {'structured':out,'probe_preserving_adversaries':adversaries,'generic_controls':negatives,'zero_vector_reason':z['reason']}

def inherited_solver_control():
    p=1201;n=8;w=(-7)%p;g=29
    assert pow(g,150,p)==w and all(pow(g,1200//q,p)!=1 for q in [2,3,5])
    assert prime(p) and pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n)) and (p-1)%(2*n)==0
    L=[[(7+pow(w,i,p))*int(i==j)+2*int(j==(i-1)%n) for j in range(n)] for i in range(n)]
    P=[[(7+2*pow(w,-i%n,p))*int(i==j)+int(j==(i-1)%n) for j in range(n)] for i in range(n)]
    assert L[1][1]%p==0 and determinant(L,p)==945 and determinant(P,p)!=0
    x=[1]+[0]*(n-1);r=[sum(a*b for a,b in zip(row,x))%p for row in P];R=dft(r,w,p)
    y=solve(L,R,p);assert y==dft(x,w,p)
    return {'N':n,'field':p,'omega':w,'primitive_generator':g,'L_zero_diagonal_index':1,'L_determinant':945,'P_determinant':determinant(P,p),'roots_for_Bluestein_exist':True,'mathematical_Green_identity_pass':True,'source_CyclicSolver_requires_inverse_of_zero':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='INDEPENDENT_RESULTS.json');args=ap.parse_args()
    r={'status':'PASS','uploaded_code_executed':False,'algebra':algebra_tests(),'applications':application_tests(),'inherited_solver_control':inherited_solver_control()}
    Path(args.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print('PASS Phase21 independent controls',len(r['algebra']['full_reconstructions']),'full resultant reconstructions',len(r['applications']['structured']),'structured cases',len(r['applications']['probe_preserving_adversaries']),'adversaries')
if __name__=='__main__':main()
