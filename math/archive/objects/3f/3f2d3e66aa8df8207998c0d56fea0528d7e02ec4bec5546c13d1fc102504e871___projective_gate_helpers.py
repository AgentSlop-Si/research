"""New projective-consistency verifier; no uploaded executable code is used.
Finite-field enumeration appears only in tiny validation controls, not in the theorem's cost claim.
"""
from itertools import product
from collections import deque
from pathlib import Path
import json
p=241

def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def add(A,B):return [[(a+b)%p for a,b in zip(ar,br)]for ar,br in zip(A,B)]
def scale(c,A):return [[c*a%p for a in row]for row in A]
def sub(A,B):return add(A,scale(-1,B))
def mul(A,B):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)]for row in A]
def tr(A):return [list(x)for x in zip(*A)]
def mv(A,v):return [sum(a*b for a,b in zip(row,v))%p for row in A]
def inv(A):
    n=len(A);M=[row[:]+er for row,er in zip(A,eye(n))]
    for j in range(n):
        k=next(k for k in range(j,n)if M[k][j]%p)
        M[j],M[k]=M[k],M[j];t=pow(M[j][j]%p,-1,p);M[j]=[x*t%p for x in M[j]]
        for k in range(n):
            if k!=j:
                t=M[k][j];M[k]=[(x-t*y)%p for x,y in zip(M[k],M[j])]
    return [row[n:]for row in M]
def det(A):return (A[0][0]*A[1][1]-A[0][1]*A[1][0])%p
def diag(v):return [[v[i]if i==j else 0 for j in range(len(v))]for i in range(len(v))]
def perm(pp):return [[int(j==pp[i])for j in range(len(pp))]for i in range(len(pp))]
def pinv(pp):return [pp.index(j)for j in range(len(pp))]
def canon(v):
    assert any(v);t=pow(next(x%p for x in v if x%p),-1,p)
    return tuple(x*t%p for x in v)
def points():return [(1,t)for t in range(p)]+[(0,1)]
def qeval(q,z):return (q[0]*z[0]**2+q[1]*z[0]*z[1]+q[2]*z[1]**2)%p
def bilinear(L,u,v):return sum(a*b for a,b in zip(v,mv(L,u)))%p
def H(L):return [[L[1][0],L[1][1]],[(-L[0][0])%p,(-L[0][1])%p]]
def LfromH(HH):return [[(-HH[1][0])%p,(-HH[1][1])%p],HH[0][:]]
def outer(a,b):return [[x*y%p for y in b]for x in a]
def kernel(row):return canon([row[1]%p,(-row[0])%p])

def trim(a):
    a=[x%p for x in a]
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def prem(a,b):
    a=trim(a);b=trim(b);assert b!=[0]
    while a!=[0]and len(a)>=len(b):
        k=len(a)-len(b);t=a[-1]*pow(b[-1],-1,p)%p
        for j,v in enumerate(b):a[k+j]=(a[k+j]-t*v)%p
        a=trim(a)
    return a

def pgcd(a,b):
    a,b=trim(a),trim(b)
    while b!=[0]:a,b=b,prem(a,b)
    return [(x*pow(a[-1],-1,p))%p for x in a]if a!=[0]else a

def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c)

def domain(qs,finite):
    nz=[(idx,q)for idx,q in qs if any(q)]
    if not nz:return dict(unrestricted=True,nonempty=True,qs=[],g=[0],infinity=True,finite_points=points()if finite else None,witness=[])
    g=[0];infinity=True;certificate=[]
    for idx,q in nz:
        gg=pgcd(g,q);ii=infinity and q[2]==0
        if not certificate or len(gg)<len(g)or (infinity and not ii):certificate.append(idx)
        g,infinity=gg,ii
    closure_nonempty=len(g)>1 or infinity
    allowed=[z for z in points()if all(qeval(q,z)==0 for _,q in nz)]if finite else None
    if not closure_nonempty:assert len(certificate)<=3
    if finite and not allowed:
        possible=set(points());certificate=[]
        for idx,q in nz:
            new={z for z in possible if qeval(q,z)==0}
            if not certificate or new!=possible:certificate.append(idx)
            possible=new
            if not possible:break
        assert len(certificate)<=3
    return dict(unrestricted=False,nonempty=bool(allowed)if finite else closure_nonempty,qs=nz,g=g,infinity=infinity,finite_points=allowed,witness=certificate)

def permits(D,z):
    if D['unrestricted']:return True
    if z[0]==0:return D['infinity']
    t=z[1]*pow(z[0],-1,p)%p
    return sum(a*pow(t,j,p)for j,a in enumerate(D['g']))%p==0
def exhausted(D,labels,finite):
    if D['unrestricted']:return False
    permitted=[z for z in labels if permits(D,z)]
    assert len(permitted)<=2
    if finite:return set(D['finite_points']).issubset(permitted)
    f=[1]
    for z in permitted:
        if z[0]:f=pmul(f,pmul([(-z[1])%p,1],[(-z[1])%p,1]))
    return prem(f,D['g'])==[0]and(not D['infinity']or(0,1)in permitted)

def sat_solve(nvar,clauses):
    def node(lit):return 2*(abs(lit)-1)+(lit<0)
    def lit(k):return -(k//2+1)if k%2 else k//2+1
    adj=[[]for _ in range(2*nvar)];rev=[[]for _ in adj]
    for a,b in clauses:
        for x,y in ((node(-a),node(b)),(node(-b),node(a))):adj[x].append(y);rev[y].append(x)
    seen=set();order=[]
    def dfs(x):
        seen.add(x)
        for y in adj[x]:
            if y not in seen:dfs(y)
        order.append(x)
    for x in range(len(adj)):
        if x not in seen:dfs(x)
    comp=[-1]*len(adj)
    def assign(x,c):
        comp[x]=c
        for y in rev[x]:
            if comp[y]<0:assign(y,c)
    for x in reversed(order):
        if comp[x]<0:assign(x,max(comp,default=-1)+1)
    for v in range(nvar):
        if comp[2*v]==comp[2*v+1]:
            def path(a,b):
                parent={a:None};queue=deque([a])
                while b not in parent:
                    x=queue.popleft()
                    for y in adj[x]:
                        if y not in parent:parent[y]=x;queue.append(y)
                rr=[b]
                while rr[-1]!=a:rr.append(parent[rr[-1]])
                rr=rr[::-1];assert all(y in adj[x]for x,y in zip(rr,rr[1:]))
                return [lit(x)for x in rr]
            return dict(satisfiable=False,contradiction_variable=v+1,paths=[path(2*v,2*v+1),path(2*v+1,2*v)])
    values=[comp[2*v]>comp[2*v+1]for v in range(nvar)]
    def value(lit):return values[abs(lit)-1]if lit>0 else not values[abs(lit)-1]
    assert all(value(a)or value(b)for a,b in clauses)
    return dict(satisfiable=True,assignment=values)

def solve_rows(n,relations,finite=False):
    adj=[[]for _ in range(n)];rank_counts=[0,0,0]
    for e,(i,k,L)in enumerate(relations):
        rr=2 if det(L)else int(any(any(row)for row in L));rank_counts[rr]+=1
        if rr==2 and i!=k:
            HH=H(L);adj[i].append((k,HH,e));adj[k].append((i,inv(HH),e))
    component=[None]*n;T=[None]*n;tree=[];components=[]
    for root in range(n):
        if component[root]is not None:continue
        c=len(components);members=[];component[root]=c;T[root]=eye(2);queue=deque([root])
        while queue:
            i=queue.popleft();members.append(i)
            for k,HH,e in adj[i]:
                if component[k]is None:component[k]=c;T[k]=mul(HH,T[i]);tree.append((i,k,e));queue.append(k)
        components.append(members)
    qs=[[]for _ in components];cross=[]
    for e,(i,k,L)in enumerate(relations):
        ci,ck=component[i],component[k]
        if ci==ck:
            R=mul(tr(T[k]),mul(L,T[i]));q=[R[0][0],(R[0][1]+R[1][0])%p,R[1][1]];qs[ci].append((e,q))
        elif any(any(row)for row in L):
            assert det(L)==0
            r,s=next((r,s)for r in range(2)for s in range(2)if L[r][s])
            pp=[L[t][s]for t in range(2)];qq=[v*pow(L[r][s],-1,p)%p for v in L[r]]
            assert outer(pp,qq)==L
            alpha=kernel(mul([qq],T[i])[0]);beta=kernel(mul([pp],T[k])[0])
            cross.append((ci,alpha,ck,beta,e))
    domains=[domain(q,finite)for q in qs]
    base=dict(vertices=n,selected_relations=len(relations),rank_counts=rank_counts,components=len(components),tree_edges=len(tree),cross_rank_one_edges=len(cross))
    for c,D in enumerate(domains):
        if not D['nonempty']:
            return dict(base,status='REJECT',reason='empty_internal_domain',domain='base_field'if finite else'algebraic_closure',component=c,quadratic_certificate=[dict(relation=e,coefficients=q)for e,q in qs[c]if e in D['witness']],tree=tree,transforms=T)
    labels=[{}for _ in components];var_to_label=[]
    for ci,a,ck,b,e in cross:
        for c,z in ((ci,a),(ck,b)):
            if z not in labels[c]:labels[c][z]=len(var_to_label)+1;var_to_label.append((c,z))
    clauses=[];origins=[]
    def clause(a,b,origin):clauses.append((a,b));origins.append(origin)
    for ci,a,ck,b,e in cross:clause(labels[ci][a],labels[ck][b],dict(kind='rank_one_edge',relation=e))
    for c,dd in enumerate(labels):
        items=list(dd.items())
        for j,(z,x)in enumerate(items):
            if not permits(domains[c],z):clause(-x,-x,dict(kind='forbidden_line',component=c,point=z))
            for zz,xx in items[j+1:]:clause(-x,-xx,dict(kind='at_most_one',component=c,points=[z,zz]))
        if exhausted(domains[c],dd,finite):
            allowed=[x for z,x in items if permits(domains[c],z)];assert 1<=len(allowed)<=2
            clause(allowed[0],allowed[-1],dict(kind='finite_domain',component=c))
    answer=sat_solve(len(var_to_label),clauses)
    if not answer['satisfiable']:
        return dict(base,status='REJECT',reason='two_sat_contradiction',boolean_variables=len(var_to_label),clause_count=len(clauses),clauses=clauses,clause_origins=origins,variable_labels=var_to_label,certificate=answer)
    if finite:
        roots=[]
        for c,dd in enumerate(labels):
            chosen=[z for z,x in dd.items()if answer['assignment'][x-1]];assert len(chosen)<=1
            roots.append(chosen[0]if chosen else domains[c]['finite_points'][0])
        directions=[canon(mv(T[i],roots[component[i]]))for i in range(n)]
        assert all(bilinear(L,directions[i],directions[k])==0 for i,k,L in relations)
    else:directions=None
    return dict(base,status='PASS',domain='base_field'if finite else'algebraic_closure',boolean_variables=len(var_to_label),clause_count=len(clauses),directions=directions)

def extract(B,r0,r1,s0,s1):
    n=len(B);c0=pinv(s0);c1=pinv(s1);relations=[]
    for i in range(n):
        for k in range(i+1,n):
            forbidden={ff[t]for ff in (r0,r1,s0,s1)for t in (i,k)}
            for j in range(n):
                if j in forbidden:continue
                Mi=[[B[r0[i]][c0[j]],B[r0[i]][c1[j]]],[B[r1[i]][c0[j]],B[r1[i]][c1[j]]]]
                Mk=[[B[r0[k]][c0[j]],B[r0[k]][c1[j]]],[B[r1[k]][c0[j]],B[r1[k]][c1[j]]]]
                aa,cc=Mi[0];bb,dd=Mi[1];ee,gg=Mk[0];ff,hh=Mk[1]
                L=[[(aa*gg-cc*ee)%p,(bb*gg-dd*ee)%p],[(aa*hh-cc*ff)%p,(bb*hh-dd*ff)%p]]
                assert det(L)==det(Mi)*det(Mk)%p
                relations.append((i,k,L))
    return relations

def target(n,w):
    roots=[pow(w,j,p)for j in range(n)];h=(n+1)//2;av=[roots[h*j*j%n]for j in range(n)]
    F=[[roots[i*j%n]for j in range(n)]for i in range(n)]
    return inv(add(inv(F),diag(av)))

def positive_controls():
    details=[]
    for n in (3,5,7,9):
        ident=list(range(n));pi=[(i+1)%n for i in ident];sigma=ident[:];sigma[0],sigma[1]=1,0;tau=[sigma[pi[sigma[i]]]for i in ident]
        for monomial,zero_edges,masked in product((False,True),repeat=3):
            lp0=[(i+1)%n for i in ident]if monomial else ident;rp0=[(-i)%n for i in ident]if monomial else ident
            lp1=sigma if monomial else ident;rp1=[(i+2)%n for i in ident]if monomial else ident
            ww0=[2]*n;ww1=[3]*n
            if zero_edges:ww0[1]=0;ww1[-1]=0
            G0=inv(sub(eye(n),mul(diag(ww0),perm(pi))));G1=inv(sub(eye(n),mul(diag(ww1),perm(tau))))
            ll0=[i+1 for i in ident];rr0=[i+3 for i in ident];ll1=[i+5 for i in ident];rr1=[i+7 for i in ident]
            if masked:ll0[1]=0;ll0[-1]=0;rr0[2]=0;ll1[0]=0;rr1[-1]=0
            T0=mul(diag(ll0),mul(perm(lp0),mul(G0,mul(diag(rr0),perm(rp0)))))
            T1=mul(diag(ll1),mul(perm(lp1),mul(G1,mul(diag(rr1),perm(rp1)))))
            B=add(T0,T1);patterns=[]
            for lp,rp,cyc in ((lp0,rp0,pi),(lp1,rp1,tau)):
                li,ri=pinv(lp),pinv(rp);patterns.extend([[li[ri[i]]for i in ident],[li[cyc[ri[i]]]for i in ident]])
            r0,r1,s0,s1=patterns;relations=extract(B,*patterns)
            # Exact normalized epsilon-limit directions of Q0 rows; right endpoint zeros cancel projectively.
            directions=[];rpi=pinv(rp0)
            for i in ident:
                terms=[]
                for j,c in ((r1[i],1),(r0[i],-ww0[rpi[i]])):
                    terms.append((1,c%p)if ll0[j]==0 else(0,c*ll0[j]%p))
                valuation=min(e for e,c in terms if c)
                directions.append(canon([c if e==valuation else 0 for e,c in terms]))
            assert all(bilinear(L,directions[i],directions[k])==0 for i,k,L in relations)
            if not masked:
                Q0,Q1=inv(T0),inv(T1);assert mul(Q0,mul(B,Q1))==add(Q0,Q1)
                assert directions==[canon([Q0[i][r0[i]],Q0[i][r1[i]]])for i in ident]
            out=solve_rows(n,relations,finite=True);assert out['status']=='PASS'
            details.append(dict(N=n,monomial_endpoints=monomial,zero_edges=zero_edges,singular_endpoint_masks=masked,selected_relations=len(relations),rank_counts=out['rank_counts'],components=out['components'],boolean_variables=out['boolean_variables'],clause_count=out['clause_count']))
    return details

def brute(n,relations):
    for zz in product(points(),repeat=n):
        if all(bilinear(L,zz[i],zz[k])==0 for i,k,L in relations):return True
    return False

def abstract_controls():
    global p
    result=[];old=p;p=5
    e1=(1,0);e2=(0,1);same=outer([0,1],[0,1]);different=outer([1,0],[0,1]);zero=[[0,0],[0,0]]
    identity=LfromH(eye(2));swap=LfromH([[0,1],[1,0]])
    q_xy=[[0,1],[0,0]]
    cases=[('vacuous',2,[(0,1,zero)]),('infinity_transition',2,[(0,1,swap)]),('rank_one_free_branch',2,[(0,1,same)]),('coincident_root',1,[(0,0,[[0,0],[0,1]])]),('identity_cycle',3,[(0,1,identity),(1,2,identity),(0,2,identity)]),('singular_internal',2,[(0,1,identity),(0,1,different)])]
    rank_one_unsat=[(0,0,q_xy),(1,1,q_xy)]
    for x,y in product(([0,1],[1,0]),repeat=2):rank_one_unsat.append((0,1,outer(y,x)))
    cases.append(('two_sat_unsat',2,rank_one_unsat))
    returns=[[[1,0],[0,2]],[[1,1],[0,2]],[[2,0],[1,1]]]
    assert all(det(sub(mul(a,b),mul(b,a)))==0 for a,b in product(returns,repeat=2))
    cases.append(('three_quadratics_needed',1,[(0,0,LfromH(r))for r in returns]))
    # Add a common eigenline case, a rank-zero duplicate, and finite-domain coverage cases.
    cases.extend([('common_eigenline',1,[(0,0,LfromH(r))for r in returns[:2]]),('rank_zero_with_transition',2,[(0,1,identity),(0,1,zero)]),('finite_two_point_domain',2,[(0,0,q_xy),(0,1,same)]),('unrestricted_all_named',2,[(0,1,outer([0,1],kernel(z)))for z in points()])])
    for name,n,relations in cases:
        answer=solve_rows(n,relations,finite=True);expected=brute(n,relations)
        assert (answer['status']=='PASS')==expected
        result.append(dict(name=name,prime=p,brute_assignments_budget=(p+1)**n,status=answer['status'],reason=answer.get('reason'),certificate=answer.get('certificate'),quadratic_certificate=answer.get('quadratic_certificate')))
    p=2
    for name,L in [('characteristic_two_repeated_root',[[1,0],[0,1]]),('characteristic_two_extension_roots',[[1,1],[0,1]])]:
        rel=[(0,0,L)];finite_answer=solve_rows(1,rel,finite=True);closure_answer=solve_rows(1,rel,finite=False)
        assert (finite_answer['status']=='PASS')==brute(1,rel)
        assert closure_answer['status']=='PASS'
        result.append(dict(name=name,prime=2,brute_assignments_budget=3,finite=finite_answer['status'],closure=closure_answer['status']))
    p=old
    no_root=[(0,0,[[(-7)%p,0],[0,1]])]
    closure=solve_rows(1,no_root,finite=False);finite=solve_rows(1,no_root,finite=True)
    assert closure['status']=='PASS'and finite['status']=='REJECT'
    result.append(dict(name='closure_versus_F241',prime=p,closure=closure['status'],finite=finite['status'],polynomial='t^2-7',Legendre_7=pow(7,(p-1)//2,p)))
    return result

def main():
    positives=positive_controls();abstract=abstract_controls()
    B3=target(3,15);id3=list(range(3));r3=extract(B3,id3,[1,2,0],id3,[2,0,1]);n3=solve_rows(3,r3,finite=True);assert n3['status']=='PASS'
    B5=target(5,91);id5=list(range(5));r5=extract(B5,id5,[2,3,4,0,1],id5,[3,2,4,1,0]);n5=solve_rows(5,r5,finite=False);assert n5['status']=='REJECT'and n5['reason']=='empty_internal_domain'
    qc=n5['quadratic_certificate'];qa,qb=[x['coefficients']for x in qc]
    mat=[[qa[0],0,qb[0],0],[qa[1],qa[0],qb[1],qb[0]],[qa[2],qa[1],qb[2],qb[1]],[0,qa[2],0,qb[2]]]
    bezout=mv(inv(mat),[1,0,0,0]);assert mv(mat,bezout)==[1,0,0,0]
    n5['affine_Bezout_coefficients_u_then_v']=bezout;n5['infinity_excluded']=all(q['coefficients'][2]for q in qc)
    result=dict(status='PASS',genuine_two_Green_controls=len(positives),singular_endpoint_controls=sum(x['singular_endpoint_masks']for x in positives),zero_edge_controls=sum(x['zero_edges']for x in positives),monomial_endpoint_controls=sum(x['monomial_endpoints']for x in positives),genuine_selected_relations=sum(x['selected_relations']for x in positives),abstract_controls=len(abstract),N3=n3,N5=n5,positive_controls=positives,abstract_details=abstract,scope='Exact selected-row subsystem gate; acceptance is not a Green factorization certificate.')
    Path(__file__).with_name('PROJECTIVE_GATE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
