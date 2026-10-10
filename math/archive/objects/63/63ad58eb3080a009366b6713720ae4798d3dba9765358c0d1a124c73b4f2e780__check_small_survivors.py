"""New exact research controls. Does not import or execute uploaded programs."""
import json
from pathlib import Path
import sympy as sy
p=241

def I(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def diag(v):return [[v[i]if i==j else 0 for j in range(len(v))]for i in range(len(v))]
def add(A,B):return [[(a+b)%p for a,b in zip(ar,br)]for ar,br in zip(A,B)]
def scale(c,A):return [[c*a%p for a in row]for row in A]
def sub(A,B):return add(A,scale(-1,B))
def mul(A,B):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)]for row in A]
def mv(A,v):return [sum(a*b for a,b in zip(row,v))%p for row in A]
def inv(A):
    n=len(A);M=[row[:]+eye for row,eye in zip(A,I(n))]
    for j in range(n):
        k=next(k for k in range(j,n)if M[k][j]%p)
        M[j],M[k]=M[k],M[j];z=pow(M[j][j]%p,-1,p);M[j]=[a*z%p for a in M[j]]
        for k in range(n):
            if k!=j:
                z=M[k][j];M[k]=[(a-z*b)%p for a,b in zip(M[k],M[j])]
    return [row[n:]for row in M]
def rank(A):
    if not A:return 0
    M=[row[:]for row in A];r=0
    for j in range(len(M[0])):
        k=next((k for k in range(r,len(M))if M[k][j]%p),None)
        if k is None:continue
        M[r],M[k]=M[k],M[r];z=pow(M[r][j]%p,-1,p);M[r]=[a*z%p for a in M[r]]
        for k in range(len(M)):
            if k!=r:
                z=M[k][j];M[k]=[(a-z*b)%p for a,b in zip(M[k],M[r])]
        r+=1
        if r==len(M):break
    return r

def det2(M):return (M[0][0]*M[1][1]-M[0][1]*M[1][0])%p
def perm(perm):return [[int(j==perm[i])for j in range(len(perm))]for i in range(len(perm))]
def green_apply(t,cycle,x):
    pref=1;total=0
    for i in cycle:total=(total+pref*x[i])%p;pref=pref*t%p
    y=[0]*len(x);y[cycle[0]]=total*pow((1-pref)%p,-1,p)%p
    for k in range(len(cycle)-1,0,-1):
        i=cycle[k];nxt=cycle[(k+1)%len(cycle)];y[i]=(x[i]+t*y[nxt])%p
    return y

def target(n,w):
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n))
    h=(n+1)//2;roots=[pow(w,j,p)for j in range(n)];av=[roots[h*j*j%n]for j in range(n)]
    F=[[roots[i*j%n]for j in range(n)]for i in range(n)];A=diag(av)
    G=sum(av)%p;c=n*G%p;guard=(1+c)%p;assert guard
    B=[[(roots[i*j%n]-G*roots[-h*(i+j)**2%n]+(c*roots[-h*i*i%n]if i==j else 0))*pow(guard,-1,p)%p for j in range(n)]for i in range(n)]
    assert B==inv(add(inv(F),A))
    assert mul(sub(I(n),mul(B,A)),F)==B
    return F,A,B,G,c

def symbolic_three():
    w=sy.Symbol('w');phi=w*w+w+1
    def red(v):
        num,den=sy.fraction(sy.cancel(v));num=sy.rem(num,phi,w);den=sy.rem(den,phi,w)
        return sy.rem(num*sy.invert(den,phi,w),phi,w)
    F=sy.Matrix(3,3,lambda i,j:w**(i*j));A=sy.diag(1,w*w,w*w)
    X=(F.inv()+A).applyfunc(red);B=X.inv().applyfunc(red)
    a=(w+10)/14;b=(1-2*w)/14;d=(9*w-1)/14;e=-(w+3)/14
    wanted=sy.Matrix([[a,b,b],[b,d,e],[b,e,d]]).applyfunc(red)
    assert B==wanted
    assert red(b-w*e)==0 and red(a-w*w*d)==0
    assert red(d-(-17-16*w)/(4+26*w))==0
    assert red(e-(1-4*w)/(4+26*w))==0
    r=red(2*e/d);assert r==(6+8*w)/13
    assert red(1+4*r-(37+32*w)/13)==0
    assert all(red(z)!=0 for z in (d,e,r,r-2,r+1,1+4*r,4+26*w))
    D=sy.diag(w,1,1);P=sy.Matrix([[0,1,0],[0,0,1],[1,0,0]])
    built=(d/2*D*(2*sy.eye(3)+r*(P+P.T))*D).applyfunc(red)
    assert built==B
    M=(F*A).applyfunc(red); K=(B*A).applyfunc(red)
    zero=sy.zeros(3)
    assert (M*M-(2+w)*M+(3+3*w)*sy.eye(3)).applyfunc(red)==zero
    assert ((6+4*w)*K*K-(8+7*w)*K+(3+3*w)*sy.eye(3)).applyfunc(red)==zero
    assert ((-2-3*w)*B+(6+4*w)*B*A*B-F).applyfunc(red)==zero
    assert red(K[0,1])!=0 and red(6+4*w)!=0
    return dict(complex_minimal_polynomial_coefficients_ascending=['3+3w','-8-7w','6+4w'],complex_mu_at_one=1,complex_feedback_coefficients=['-2-3w','6+4w'],field='Q(w), w^2+w+1=0',target_entries_checked=9,constructed_entries_checked=9,parameter_equation='t^2+t=(6+8w)/13',complex_root_guard='r != 0,2,-1; both quadratic roots have t != 0 and t^3 != 1',additional_root='sqrt((37+32w)/13)',exact_checks='PASS')

def finite_three():
    F,A,B,G,c=target(3,15);dvec=[15,1,1];D=diag(dvec);t=207;kappa=2
    assert B==[[19,84,84],[84,44,102],[84,102,44]]
    assert G==210 and c==148 and (1-pow(t,3,p))%p==22
    assert (t*t+t)%p==158==2*B[1][2]*pow(B[1][1],-1,p)%p
    assert kappa==B[1][1]*(1-pow(t,3,p))*pow(2,-1,p)%p
    P=perm([1,2,0]);Pinv=perm([2,0,1])
    terms=[scale(kappa,mul(D,mul(inv(sub(I(3),scale(t,PP))),D)))for PP in (P,Pinv)]
    assert add(*terms)==B
    Q0,Q1=map(inv,terms);assert mul(Q0,mul(B,Q1))==add(Q0,Q1)
    K=mul(B,A);mu=add(add(scale(66,mul(K,K)),scale(128,K)),scale(48,I(3)))
    assert mu==[[0]*3 for _ in range(3)] and (66+128+48)%p==1
    assert rank([[v for row in X for v in row]for X in (I(3),K)])==2
    assert inv(sub(I(3),K))==add(scale(194,I(3)),scale(66,K))
    assert F==add(scale(194,B),scale(66,mul(B,mul(A,B))))
    def appB(x):
        y=[d*z%p for d,z in zip(dvec,x)]
        z0=green_apply(t,[0,1,2],y);z1=green_apply(t,[0,2,1],y)
        return [kappa*d*(z+zz)%p for d,z,zz in zip(dvec,z0,z1)]
    for j in range(3):
        x=[int(i==j)for i in range(3)];u=appB(x);assert u==mv(B,x)
        v=appB(mv(A,u));out=[(194*a+66*b)%p for a,b in zip(u,v)]
        assert out==mv(F,x)
    return dict(N=3,prime=p,omega=15,G=G,c=c,guard_1_plus_c=(1+c)%p,t=t,kappa=kappa,green_guard=22,B=B,target_entries_checked=9,Green_sum_entries_checked=9,scan_B_entries_checked=9,feedback_basis_vectors_checked=3,feedback_output_entries_checked=9,minimal_polynomial_coefficients_ascending=[48,128,66],mu_at_one=1,exact_minimal_degree=2,online_Green_scan_calls_per_vector=4,independent_guard_inversions=1)

def coefficients(B,pi,tau,i,k):
    n=len(B);ti=[tau.index(j)for j in range(n)];forbidden={i,k,pi[i],pi[k],tau[i],tau[k]}
    out=[]
    for j in range(n):
        if j in forbidden:continue
        aa,cc=B[i][j],B[i][ti[j]];bb,dd=B[pi[i]][j],B[pi[i]][ti[j]]
        ee,gg=B[k][j],B[k][ti[j]];ff,hh=B[pi[k]][j],B[pi[k]][ti[j]]
        out.append((j,[(aa*gg-cc*ee)%p,(bb*gg-dd*ee)%p,(aa*hh-cc*ff)%p,(bb*hh-dd*ff)%p]))
    return out

def homography(c):return [[c[2],c[3]],[(-c[0])%p,(-c[1])%p]]
def return_maps(H):
    C1=mul(inv(H[0,2]),mul(H[1,2],H[0,1]))
    C3=mul(inv(mul(H[2,4],H[0,2])),mul(H[3,4],H[0,3]))
    return C1,C3,sub(mul(C1,C3),mul(C3,C1))

def finite_five():
    n=5;F,A,B,G,c=target(n,91);pi=[2,3,4,0,1];tau=[3,2,4,1,0]
    assert G==103 and c==33 and mul(perm(pi),perm(tau))!=mul(perm(tau),perm(pi))
    budgets=[]
    for s in range(n):
        left={(s+j)%n for j in range(n//2)};right=set(range(n))-left
        cuts=[sum(pp[i]not in left for i in left)for pp in (pi,tau)]
        assert cuts[0]==2 and sum(cuts)>=2
        assert rank([[B[i][j]for j in sorted(right)]for i in sorted(left)])==2
        budgets.append(cuts)
    expected={(0,1):(4,[50,144,20,74]),(0,2):(1,[20,0,50,63]),(0,3):(4,[20,74,0,101]),(1,2):(0,[53,184,113,213]),(1,3):(4,[178,0,191,221]),(2,4):(3,[20,0,77,238]),(3,4):(2,[213,188,110,213])}
    H={};rows=[]
    for i in range(n):
        for k in range(i+1,n):
            cc=coefficients(B,pi,tau,i,k)
            if (i,k)not in expected:assert not cc;rows.append(dict(pair=[i,k],rank=0));continue
            assert cc==[expected[i,k]];j,co=cc[0];HH=homography(co);assert det2(HH);H[i,k]=HH
            # Exhibit a separate local projective witness with both base coefficients nonzero.
            witnesses=[]
            for b in (0,1):
                u=[1,b];v=mv(HH,u)
                if v[0]:
                    z=[u[0]*v[0],u[1]*v[0],u[0]*v[1],u[1]*v[1]]
                    assert sum(a*b for a,b in zip(co,z))%p==0
                    assert (z[0]*z[3]-z[1]*z[2])%p==0
                    witnesses.append([u,v])
            assert witnesses
            rows.append(dict(pair=[i,k],column=j,coefficients=co,rank=1,homography=HH,homography_determinant=det2(HH),local_witness=witnesses[0]))
    assert [det2(H[ik])for ik in expected]==[97,55,92,137,55,181,107]
    C1,C3,comm=return_maps(H)
    assert C1==[[75,4],[33,140]] and C3==[[106,125],[20,52]]
    assert comm==[[52,94],[190,189]] and det2(comm)==162
    controls=[]
    for zero_edges in (False,True):
        ww0=[2]*n;ww1=[3]*n
        if zero_edges:ww0[1]=0;ww1[3]=0
        G0=inv(sub(I(n),mul(diag(ww0),perm(pi))));G1=inv(sub(I(n),mul(diag(ww1),perm(tau))))
        for masked in (False,True):
            ll=[i+1 for i in range(n)];rr=[i+7 for i in range(n)]
            if masked:ll[2]=0;rr[1]=0
            T0=mul(diag(ll),mul(G0,diag([i+2 for i in range(n)])))
            T1=mul(diag([i+4 for i in range(n)]),mul(G1,diag(rr)))
            test=add(T0,T1)
            if not masked:
                Q0,Q1=inv(T0),inv(T1)
                assert mul(Q0,mul(test,Q1))==add(Q0,Q1)
                for ik in expected:
                    i,k=ik;co=coefficients(test,pi,tau,i,k)[0][1]
                    ui=[Q0[i][i],Q0[i][pi[i]]];uk=[Q0[k][k],Q0[k][pi[k]]]
                    z=[ui[0]*uk[0],ui[1]*uk[0],ui[0]*uk[1],ui[1]*uk[1]]
                    assert sum(a*b for a,b in zip(co,z))%p==0
            HH={ik:homography(coefficients(test,pi,tau,*ik)[0][1])for ik in expected}
            guards=[det2(HH[ik])for ik in expected]
            dd=None
            if all(guards):dd=det2(return_maps(HH)[2]);assert dd==0
            controls.append(dict(zero_edges=zero_edges,singular_endpoint_mask=masked,homography_determinants=guards,commutator_determinant_when_defined=dd))
    return dict(N=n,prime=p,omega=91,G=G,c=c,guard_1_plus_c=(1+c)%p,pi=pi,tau=tau,target_entries_checked=25,half_cut_checks=5,crossings=budgets,local_pairs_checked=10,rank_one_pairs=7,rank_zero_pairs=3,local_projective_witnesses=7,local_gates=rows,C1=C1,C3=C3,commutator=comm,commutator_determinant=162,global_compatibility='REJECT',genuine_Green_controls=controls)

result=dict(status='PASS',symbolic_three=symbolic_three(),finite_three=finite_three(),finite_five=finite_five(),scope='Exact finite N3 construction; fixed N5 cycle-order exclusion. No growing-size FFT claim.')
Path(__file__).with_name('SMALL_SURVIVOR_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
