"""Independent modular verification of exact-definition lifting certificates.
Reads author JSON as inert data; no author code is imported or executed.
"""
import json, math
from pathlib import Path
from functools import lru_cache
import sympy as sy
BASE=Path(__file__).parent
SRC=BASE.parent/'common_annihilator_barrier'

def mat_det(A,p):
    a=[[x%p for x in row] for row in A];ans=1
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]),None)
        if j is None:return 0
        if i!=j:a[i],a[j]=a[j],a[i];ans=-ans
        v=a[i][i];ans=ans*v%p
        for j in range(i+1,len(a)):
            scale=a[j][i]*pow(v,-1,p)%p
            for k in range(i,len(a)):a[j][k]=(a[j][k]-scale*a[i][k])%p
    return ans%p

def reduce_matrix(A,p):
    a=[[x%p for x in row] for row in A];r=0;piv=[]
    for c in range(len(a[0])):
        j=next((j for j in range(r,len(a)) if a[j][c]),None)
        if j is None:continue
        a[r],a[j]=a[j],a[r]
        a[r]=[x*pow(a[r][c],-1,p)%p for x in a[r]]
        for j in range(len(a)):
            if j!=r:
                t=a[j][c]
                a[j]=[(x-t*y)%p for x,y in zip(a[j],a[r])]
        piv.append(c);r+=1
        if r==len(a):break
    return a,piv

def solve_square(A,b,p):
    r,piv=reduce_matrix([x+[y] for x,y in zip(A,b)],p)
    assert piv==list(range(len(A)))
    return [row[-1] for row in r]

def pmul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return c

def peval(a,z,p):
    v=0
    for x in a[::-1]:v=(v*z+x)%p
    return v

def product(factors,p):
    out=[1]
    for f in factors:out=pmul(out,f,p)
    return out

def verify(N):
    data=json.loads((SRC/f'N{N}_LIFT_CERTIFICATE.json').read_text())
    p=data['p'];q=data['q_residue'];m=data['m'];d=N-m;h=pow(4,-1,N);e=pow(2,-1,N)
    assert sy.isprime(p) and pow(q,N,p)==1
    assert all(pow(q,N//r,p)!=1 for r in sy.factorint(N))
    @lru_cache(None)
    def gauss(n,k,z):
        rows=[[1]]
        for t in range(1,n+1):
            old=rows[-1]
            rows.append([1]+[(old[j-1]+pow(z,j,p)*old[j])%p for j in range(1,t)]+[1])
        return rows[n][k]
    def G(a,b,E,D):
        u=(E*a)%N;v=(D*b)%N
        return gauss(u+v,v,pow(q,E*D%N,p)) if u+v<N else 0
    def target(a,b):return pow(q,h*(a+b)**2%N,p)
    seq={};denoms=[]
    for b in range(1,(N+1)//2):
        z=G(N-b,b,-1,1);denoms.append(z);T=pow(z,-1,p)
        seq[b]=[]
        for a in range(1,N-b):
            z=G(a,b,1,1);denoms.append(z)
            seq[b].append((target(a,b)-T*G(a,b,-1,1))*pow(z,-1,p)%p)
    labels=[];rows=[]
    for b in range(1,(N+1)//2):
        for r in range(len(seq[b])-m):labels.append([b,r]);rows.append(seq[b][r:r+m+1])
    assert labels==data['equations'] and rows==data['recurrence_matrix']
    rank=len(reduce_matrix(rows,p)[1]);assert rank==data['recurrence_rank']
    I=data['defining_equation_indices'];J=data['solved_coefficient_indices']
    A=[[rows[i][j] for j in J] for i in I]
    assert len(I)==len(J)==rank
    defining_det=mat_det(A,p);assert defining_det==data['defining_minor_residue']!=0
    c=[0]*(m+1);c[m]=1
    free=set(range(m))-set(J)
    assert free==set(map(int,data['fixed_coefficient_integer_values']))
    for j,v in data['fixed_coefficient_integer_values'].items():c[int(j)]=v%p
    rhs=[-sum(rows[i][j]*c[j] for j in free|{m})%p for i in I]
    for j,v in zip(J,solve_square(A,rhs,p)):c[j]=v
    assert c==data['annihilator_coefficients_residue']
    assert all(sum(x*y for x,y in zip(row,c))%p==0 for row in rows)
    assert c[0]==data['constant_coefficient_residue']!=0
    t=sy.Symbol('t');g=sy.Poly(sum(v*t**j for j,v in enumerate(c)),t,modulus=p)
    resultant=int(g.resultant(g.diff()))%p
    assert resultant==data['resultant_residue']!=0
    # Construct powers in the monic quotient by repeated multiplication by t.
    P=[];v=[1]+[0]*(m-1)
    for a in range(N):
        P.append(v[:]);lead=v[-1]
        v=[0]+v[:-1]
        v=[(v[j]-lead*c[j])%p for j in range(m)]
    axis=[P[a]+[1]+P[-a%N] for a in range(N)]
    cols=data['axis_columns'];axisdet=mat_det([[r[j] for j in cols] for r in axis],p)
    assert len(cols)==N and len(set(cols))==N and axisdet==data['axis_minor_residue']!=0
    assert len(data['row_controls'])==N
    for rec in data['row_controls']:
        b=rec['b'];sol=rec['solution'];M=[]
        for a in range(N):
            row=[G(a,b,1,1)*x%p for x in P[a]]+[G(a,b,-1,1),G(a,b,1,-1)]+[G(a,b,-1,-1)*x%p for x in P[-a%N]]
            M.append(row)
            assert len(sol)==2*m+2 and sum(x*y for x,y in zip(row,sol))%p==target(a,b)
        assert len(reduce_matrix(M,p)[1])==rec['rank']
    # Independently check the polynomial row envelope and omitted-endpoint relation.
    D=product([[1,-pow(q,j,p)%p] for j in range(2,d)],p)
    assert all(peval(D,pow(q,k,p),p) for k in range(m+1))
    Emax=d-3+(d-1)//2;Omax=d-3+(d-2)//2
    triple_vectors=[];endpoint=m+1;zstar=pow(q,endpoint,p)
    for (b,r),row in zip(labels,rows):
        a=r+1;tval=a+b
        F=product([[1,-pow(q,j,p)%p] for j in range(2,d) if not a+1<=j<=a+b],p)
        Rpoly=product([[1,-pow(q,a-j,p)%p] for j in range(1,b+1)],p)
        Qb=math.prod((1-pow(q,j,p))%p for j in range(1,b+1))%p
        Tb=pow(G(N-b,b,-1,1),-1,p)
        B=Tb*((-1)**b)*pow(q,b*(b+1)//2,p)%p
        poly=[0]*(tval//2)+[(Qb*pow(q,h*tval*tval%N,p)*x)%p for x in F]
        E=poly if tval%2==0 else [0]
        O=poly if tval%2 else [0]
        R=[-B*x%p for x in pmul(Rpoly,F,p)]
        assert len(E)-1<=Emax and len(O)-1<=Omax and len(R)-1<=d-2
        assert E[0]==O[0]==0
        if d%2==0:assert peval(E,zstar,p)==0
        else:assert peval(O,zstar,p)==0
        for k,w in enumerate(row):
            z=pow(q,k,p);C=pow(q,h*k*k%N,p);rho=pow(q,e*k%N,p)
            val=(C*peval(E,z,p)+C*rho*peval(O,z,p)+peval(R,z,p))%p
            assert val==peval(D,z,p)*w%p
        C=pow(q,h*endpoint*endpoint%N,p);rho=pow(q,e*endpoint%N,p)
        assert (C*peval(E,zstar,p)+C*rho*peval(O,zstar,p)+peval(R,zstar,p))%p==0
        triple_vectors.append(E+[0]*(Emax+1-len(E))+O+[0]*(Omax+1-len(O))+R+[0]*(d-1-len(R)))
    triple_rank=len(reduce_matrix(triple_vectors,p)[1]);assert triple_rank<=4*d-11
    return {'N':N,'m':m,'gap':d,'banks':2*m+2,'modulus':p,'q':q,'all_denominators_nonzero':all(denoms),'recurrence_rows':len(rows),'recurrence_rank':rank,'rank_upper_bound':min((d-1)*(d-2)//2,4*d-11),'defining_minor':defining_det,'constant':c[0],'resultant':resultant,'axis_minor':axisdet,'physical_rows_verified':N,'physical_entries_verified':N*N,'polynomial_envelope_verified':True,'polynomial_triple_rank':triple_rank,'omitted_endpoint_relation_verified':True,'status':'PASS'}

out=[]
for N in [13,17,35]:
    row=verify(N);out.append(row);print(json.dumps(row),flush=True)
(BASE/'FRESH_BANK_LIFT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
