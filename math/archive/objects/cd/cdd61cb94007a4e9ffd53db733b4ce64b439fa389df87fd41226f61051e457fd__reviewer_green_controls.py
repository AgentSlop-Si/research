"""Independent C01 geometric certificate reconstruction; supplied code is not imported."""
import itertools,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
p=241
def add(x,y):return (x%p+y%p)%p+p*((x//p+y//p)%p)
def neg(x):return (-(x%p))%p+p*((-(x//p))%p)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    a,b=x%p,x//p;c,d=y%p,y//p
    return (a*c+7*b*d)%p+p*((a*d+b*c)%p)
def inverse(x):
    assert x
    a,b=x%p,x//p;t=pow((a*a-7*b*b)%p,-1,p)
    return a*t%p+p*((-b*t)%p)
def div(x,y):return mul(x,inverse(y))
def norm(x):return ((x%p)**2-7*(x//p)**2)%p
def sm(xs):
    z=0
    for x in xs:z=add(z,x)
    return z
def dot(a,b):return sm(mul(x,y) for x,y in zip(a,b))
def mat(A,B):return [[dot(r,c) for c in zip(*B)] for r in A]
def tr(A):return list(map(list,zip(*A)))
def mv(A,v):return [dot(r,v) for r in A]
def canonical(v):
    assert any(v)
    return [1,div(v[1],v[0])] if v[0] else [0,1]
def rankdet(A):
    a=[list(r) for r in A];h=len(a);w=len(a[0]);r=0;det=1
    for c in range(w):
        q=next((i for i in range(r,h) if a[i][c]),None)
        if q is None:continue
        if q!=r:a[r],a[q]=a[q],a[r];det=neg(det)
        v=a[r][c];det=mul(det,v);iv=inverse(v)
        for i in range(r+1,h):
            f=mul(a[i][c],iv)
            if f:
                for j in range(c,w):a[i][j]=sub(a[i][j],mul(f,a[r][j]))
        r+=1
        if r==h:break
    return r,det
def invmat(A):
    n=len(A);a=[r[:]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
    for c in range(n):
        q=next(i for i in range(c,n) if a[i][c]);a[c],a[q]=a[q],a[c];iv=inverse(a[c][c]);a[c]=[mul(iv,x) for x in a[c]]
        for i in range(n):
            if i!=c:
                f=a[i][c];a[i]=[sub(x,mul(f,y)) for x,y in zip(a[i],a[c])]
    return [r[n:] for r in a]
def poly(q,v):return add(add(mul(q[0],mul(v[0],v[0])),mul(q[1],mul(v[0],v[1]))),mul(q[2],mul(v[1],v[1])))
sq={a*a%p:a for a in range(p)}
def roots(q):
    # All roots of a homogeneous base-field quadratic in P1(F_p^2).
    A,B,C=q;out=[]
    if not C:out.append([0,1])
    if C:
        disc=(B*B-4*A*C)%p
        r=sq[disc] if disc in sq else p*sq[disc*pow(7,-1,p)%p]
        for rr in {r,neg(r)}:out.append([1,div(sub(rr,B),(2*C)%p)])
    elif B:out.append([1,(-A*pow(B,-1,p))%p])
    elif not A:raise AssertionError('unconstrained polynomial supplied')
    return out

def lower():
    packet=json.loads((ROOT/'inherited_reaudit/final_v1/GREEN_FRESH_CERTIFICATE.json').read_text())
    B=packet['summary']['target'];F=[[pow(91,i*j,p) for j in range(5)] for i in range(5)]
    Fi=invmat(F);Q=[[add(Fi[i][j],pow(91,3*i*i,p) if i==j else 0) for j in range(5)] for i in range(5)]
    assert invmat(Q)==B
    cycles=[]
    for tail in itertools.permutations(range(1,5)):
        walk=(0,)+tail;pi=[0]*5
        for u,v in zip(walk,walk[1:]+walk[:1]):pi[u]=v
        cycles.append(pi)
    assert cycles==packet['cycles']
    expected={}
    for r in packet['branches']:
        key=(tuple(r['cycles']),tuple(map(tuple,r['u'])),tuple(map(tuple,r['v'])))
        assert key not in expected;expected[key]=r
    seen=set();transitions=0;empty=0;branches=0;rankone=0;zero_u=0;zero_v=0;neither=0;shapes={};J=[[0,1],[240,0]]
    for ip,pi in enumerate(cycles):
      for it,tau in enumerate(cycles):
        ti=[tau.index(j) for j in range(5)]
        M={(i,j):[[B[i][j],B[i][ti[j]]],[B[pi[i]][j],B[pi[i]][ti[j]]]] for i in range(5) for j in range(5)}
        eligible={j:[i for i in range(5) if j not in [i,pi[i],tau[i]]] for j in range(5)}
        edges=[];adj={i:[] for i in range(5)}
        for j in range(5):
          for i,k in itertools.combinations(eligible[j],2):
            C=mat(mat(M[i,j],J),tr(M[k,j]));assert sub(mul(C[0][0],C[1][1]),mul(C[0][1],C[1][0]))
            transitions+=1;edges.append((i,k,C));adj[i].append((k,mat(J,tr(C))));adj[k].append((i,mat(J,C)))
        transforms={};components=[]
        for root in range(5):
            if root in transforms:continue
            transforms[root]=[[1,0],[0,1]];todo=[root];vs=[]
            while todo:
                i=todo.pop(0);vs.append(i)
                for k,T in adj[i]:
                    if k not in transforms:transforms[k]=mat(T,transforms[i]);todo.append(k)
            components.append(sorted(vs))
        domains=[]
        for vs in components:
            quadratics=[]
            for i,k,C in edges:
                if i not in vs:continue
                H=mat(mat(tr(transforms[i]),C),transforms[k]);q=[H[0][0],add(H[0][1],H[1][0]),H[1][1]]
                assert all(x<p for x in q)
                if any(q):quadratics.append(q)
            assert quadratics
            domain=[v for v in roots(quadratics[0]) if all(poly(q,v)==0 for q in quadratics)]
            domains.append(domain)
        if any(not d for d in domains):empty+=1;continue
        shape=str(sorted(map(len,domains)));shapes[shape]=shapes.get(shape,0)+1
        for chosen in itertools.product(*domains):
            u=[None]*5
            for vs,root in zip(components,chosen):
                for i in vs:u[i]=canonical(mv(transforms[i],root))
            v=[]
            for j in range(5):
                rows=[mv(tr(M[i,j]),u[i]) for i in eligible[j]]
                assert rankdet(rows)[0]==1;rankone+=1
                r=next(r for r in rows if any(r));vj=canonical([neg(r[1]),r[0]])
                assert all(dot(r,vj)==0 for r in rows);v.append(vj)
            U=[[0]*5 for _ in range(5)];V=[[0]*5 for _ in range(5)]
            for i in range(5):U[i][i],U[i][pi[i]]=u[i]
            for j in range(5):V[j][j]=v[j][0];V[ti[j]][j]=v[j][1]
            UBV=mat(mat(U,B),V);A=[]
            for i in range(5):
                for j in range(5):
                    row=[0]*11;row[i]=V[i][j];row[5+j]=U[i][j];row[-1]=UBV[i][j];A.append(row)
            assert rankdet([r[:-1] for r in A])[0]==10 and rankdet(A)[0]==11
            key=((ip,it),tuple(map(tuple,u)),tuple(map(tuple,v)));assert key in expected and key not in seen;seen.add(key)
            rec=expected[key];chosenrows=rec['equation_rows'];rr,dd=rankdet([A[i] for i in chosenrows]);assert rr==11 and dd==rec['determinant']
            ri=[sum(t//5==i for t in chosenrows)-1 for i in range(5)];ci=[sum(t%5==j for t in chosenrows)-1 for j in range(5)]
            assert min(ri+ci)>=0 and ri==rec['row_multidegrees'] and ci==rec['column_multidegrees']
            branches+=1;zu=any(x[0]==0 for x in u);zv=any(x[0]==0 for x in v);zero_u+=zu;zero_v+=zv;neither+=not(zu or zv)
    assert seen==set(expected);assert (transitions,empty,branches,rankone,zero_u,zero_v,neither)==(4320,384,624,3120,240,240,144)
    return dict(target_directly_verified=True,cycle_pairs=576,transitions=transitions,empty_pairs=empty,branches=branches,rank_one_columns=rankone,all_stored_minors_match=True,independent_forest_shapes=shapes,zero_row_base=zero_u,zero_column_base=zero_v,neither_zero=neither)

def upper():
    src=json.loads((ROOT/'inherited_reaudit/final_v1/GREEN_FRESH_CERTIFICATE.json').read_text());B=src['summary']['target']
    a,b,c,e,f,h=B[0][1],B[0][2],B[1][2],B[1][3],B[1][4],B[2][3]
    alpha=div(c,mul(a,b));beta=div(e,mul(a,b));gamma=div(f,mul(a,a));eps=div(h,mul(b,b))
    L=sub(mul(beta,beta),mul(gamma,eps));M=sm([neg(mul(2,mul(alpha,beta))),mul(alpha,gamma),mul(alpha,eps),mul(beta,gamma),mul(beta,eps),neg(mul(2,mul(gamma,eps)))]);J=mul(sub(beta,gamma),sub(beta,gamma))
    guard=[a,b,gamma,sub(beta,gamma),L,sub(mul(div(M,L),div(M,L)),mul(4,div(J,L)))];assert guard==[20,102,234,89,163,163]
    ds=[v[1] for v in roots([div(J,L),div(M,L),1])];assert len(ds)==2
    records=[]
    for d in ds:
        T=sub(mul(gamma,add(d,2)),add(alpha,beta));t=div(add(mul(gamma,d),mul(add(alpha,beta),mul(d,d))),T)
        kap=div(add(t,mul(d,d)),gamma);x=div(sub(t,d),kap);rs=[x,div(sub(alpha,x),d),div(sub(beta,x),d),div(sub(gamma,x),d)]
        z=div(kap,add(1,t));u=[1]+[mul(B[0][i],rs[i-1]) for i in range(1,5)];v=[div(z,t)]+[sub(B[0][i],mul(z,u[i])) for i in range(1,5)]
        delta=[sub(B[i][i],mul(add(1,t),mul(u[i],v[i]))) for i in range(5)]
        for i in range(5):
            for j in range(i+1,5):assert add(mul(u[i],v[j]),mul(t,mul(v[i],u[j])))==B[i][j]
        assert [norm(v) for v in [d,T,kap,t,add(1,t),sub(1,t)]]==[124,139,53,1,160,85]
        assert list(map(norm,u))==[1,44,153,153,44] and list(map(norm,v))==[41,117,7,7,117] and list(map(norm,delta))==[72,113,64,64,113]
        records.append({'d':d,'t':t,'all_guards_nonzero':True,'off_diagonal_identities':20})
    assert mul(records[0]['t'],records[1]['t'])==1
    return {'records':records,'guard_count':27,'reciprocal_holonomies':True}

if __name__=='__main__':
    r={'lower':lower(),'upper':upper(),'source_programs_executed':False}
    (OUT/'reviewer_green_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
