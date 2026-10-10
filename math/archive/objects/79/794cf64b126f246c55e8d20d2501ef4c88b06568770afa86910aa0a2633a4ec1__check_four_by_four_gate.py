"""New exact coefficient-gate controls. No uploaded program is executed."""
import json,runpy
from pathlib import Path
hh=runpy.run_path('research_round_2156/feedback_involution/check_two_cayley.py')
ident,add,sub,scale,mul,inv=[hh[k]for k in ('ident','add','sub','scale','mul','inv')]
p=65521;N=13;I=ident(N)
for fn in (ident,add,sub,scale,mul,inv):fn.__globals__['p']=p
pi=[(i+6)%N for i in range(N)];sigma=list(range(N));sigma[0],sigma[1]=1,0
tau=[sigma[(sigma[i]+6)%N]for i in range(N)]
def P(perm):return [[int(j==perm[i])for j in range(N)]for i in range(N)]
def diag(v):return [[v[i]if i==j else 0 for j in range(N)]for i in range(N)]
def det(M):
    M=[r[:]for r in M];d=1
    for j in range(len(M)):
        k=next((k for k in range(j,len(M))if M[k][j]%p),None)
        if k is None:return 0
        if k!=j:M[k],M[j]=M[j],M[k];d=-d%p
        z=M[j][j]%p;d=d*z%p;zi=pow(z,-1,p);M[j]=[v*zi%p for v in M[j]]
        for k in range(j+1,len(M)):
            z=M[k][j];M[k]=[(a-z*b)%p for a,b in zip(M[k],M[j])]
    return d

def gate(B,r0,r1,s0,s1,cols=None):
    i,k=0,1;forbidden={f[t]for f in (r0,r1,s0,s1)for t in (i,k)}
    eligible=[j for j in range(N)if j not in forbidden]
    cols=eligible[:4]if cols is None else cols
    assert len(cols)==4 and all(j in eligible for j in cols)
    c0=[s0.index(j)for j in range(N)];c1=[s1.index(j)for j in range(N)];rows=[]
    for j in cols:
        A,C=B[r0[i]][c0[j]],B[r0[i]][c1[j]];Bb,D=B[r1[i]][c0[j]],B[r1[i]][c1[j]]
        E,G=B[r0[k]][c0[j]],B[r0[k]][c1[j]];F,H=B[r1[k]][c0[j]],B[r1[k]][c1[j]]
        rows.append([(A*G-C*E)%p,(Bb*G-D*E)%p,(A*H-C*F)%p,(Bb*H-D*F)%p])
    return rows,det(rows),cols,sorted(forbidden)
omega=pow(17,(p-1)//N,p);assert omega==56909 and pow(omega,N,p)==1 and omega!=1
roots=[pow(omega,j,p)for j in range(N)];av=[roots[(7*j*j)%N]for j in range(N)]
G=sum(av)%p;c=N*G%p;den=pow(1+c,-1,p);assert G==63693 and c==41757
B=[[((roots[(i*j)%N]-G*roots[(-7*(i+j)**2)%N]+(c*roots[(-7*i*i)%N]if i==j else 0))*den)%p for j in range(N)]for i in range(N)]
F=[[roots[(i*j)%N]for j in range(N)]for i in range(N)]
assert B==inv(add(inv(F),diag(av)))
idp=list(range(N));R,d,cols,forbidden=gate(B,idp,pi,idp,tau,[2,3,4,5])
expected=[[30388,12950,52923,20728],[30191,50630,14717,481],[27205,30796,53578,20728],[20815,59325,15216,39038]]
assert R==expected and d==60131 and forbidden==[0,1,6,7]
assert mul(P(pi),P(tau))!=mul(P(tau),P(pi))
crossings=[]
for t in range(N):
    left={(t+j)%N for j in range(N//2)}
    ee=[sum(perm[i]not in left for i in left)for perm in (pi,tau)]
    assert ee[0]==6 and sum(ee)>=6;crossings.append(ee)
controls=[]
shift2=[(i+2)%N for i in range(N)];rev=[(-i)%N for i in range(N)]
swap34=idp[:];swap34[3],swap34[4]=4,3
swap56=idp[:];swap56[5],swap56[6]=6,5
for monomial in (False,True):
    ep=(shift2,swap34,swap56,rev)if monomial else (idp,idp,idp,idp)
    lp0,rp0,lp1,rp1=map(P,ep)
    patterns=[]
    for lp,rp,cyc in ((lp0,rp0,pi),(lp1,rp1,tau)):
        base=mul(inv(rp),inv(lp));edge=mul(inv(rp),mul(P(cyc),inv(lp)))
        patterns += [[row.index(1)for row in base],[row.index(1)for row in edge]]
    r0,r1,s0,s1=patterns
    for zeros in (False,True):
        w0=[2]*N;w1=[3]*N
        if zeros:w0[3]=0;w1[7]=0
        D0=sub(I,mul(diag(w0),P(pi)));D1=sub(I,mul(diag(w1),P(tau)))
        for mask in ('none','left','right','both'):
            l0=[i+1 for i in range(N)];rr0=[i+2 for i in range(N)];l1=[i+3 for i in range(N)];rr1=[i+4 for i in range(N)]
            if mask in ('left','both'):
                for i in range(0,N,3):l0[i]=0
            if mask in ('right','both'):
                for i in range(0,N,4):rr1[i]=0
            T0=mul(mul(diag(l0),lp0),mul(inv(D0),mul(diag(rr0),rp0)))
            T1=mul(mul(diag(l1),lp1),mul(inv(D1),mul(diag(rr1),rp1)))
            testB=add(T0,T1);_,dd,cc,_=gate(testB,r0,r1,s0,s1);assert dd==0
            if mask=='none':
                Q0,Q1=inv(T0),inv(T1);assert mul(Q0,mul(testB,Q1))==add(Q0,Q1)
                assert all(Q0[i][j]==0 for i in range(N)for j in range(N)if j not in (r0[i],r1[i]))
                assert all(Q1[i][j]==0 for i in range(N)for j in range(N)if j not in (s0[i],s1[i]))
            controls.append(dict(monomial_endpoints=monomial,zero_edges=zeros,endpoint_mask=mask,gate_determinant=dd,columns=cc))
result=dict(status='PASS',N=N,prime=p,omega=omega,G=G,c=c,guard_1_plus_c=1+c,pi=pi,tau=tau,rows=[0,1],columns=cols,rhs_forbidden_columns=forbidden,coefficient_matrix=R,determinant=d,target_entries_verified=N*N,half_cut_checks=N,crossings=crossings,genuine_two_Green_gate_controls=len(controls),singular_endpoint_controls=sum(v['endpoint_mask']!='none'for v in controls),zero_edge_controls=sum(v['zero_edges']for v in controls),monomial_endpoint_controls=sum(v['monomial_endpoints']for v in controls),controls=controls)
Path(__file__).with_name('FOUR_BY_FOUR_GATE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k not in ('controls','crossings')},indent=2))
