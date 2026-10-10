"""New exact fixed-direction recovery controls. Imports only our own prior verifier."""
import importlib.util,json
from pathlib import Path
from itertools import product
spec=importlib.util.spec_from_file_location('own_projective_helpers','research_round_2156/projective_row_gate/check_projective_gate.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
h.p=241

def cycles(pp):
    n=len(pp);assert sorted(pp)==list(range(n));seen=set();cc=[]
    for i in range(n):
        if i in seen:continue
        cyc=[];j=i
        while j not in seen:seen.add(j);cyc.append(j);j=pp[j]
        assert j==i;cc.append(cyc)
    return cc

def structural(U,V,r0,r1,s0,s1):
    n=len(U);p=h.p
    for pp in (r0,r1,s0,s1):assert sorted(pp)==list(range(n))
    assert all(r0[i]!=r1[i]and s0[i]!=s1[i]for i in range(n))
    assert all(U[i][j]==0 for i in range(n)for j in range(n)if j not in (r0[i],r1[i]))
    assert all(V[i][j]==0 for i in range(n)for j in range(n)if j not in (s0[i],s1[i]))
    c0,c1=h.pinv(s0),h.pinv(s1);a=[U[i][r0[i]]for i in range(n)];b=[U[i][r1[i]]for i in range(n)]
    d=[V[c0[j]][j]for j in range(n)];e=[V[c1[j]][j]for j in range(n)]
    if not all(a)or not all(d):return dict(status='REJECT',reason='zero_base_coordinate',a=a,d=d)
    R0=[h.pinv(r0)[r1[i]]for i in range(n)];R1=[s1[c0[i]]for i in range(n)]
    cc0,cc1=cycles(R0),cycles(R1)
    if len(cc0)!=1 or len(cc1)!=1:return dict(status='REJECT',reason='non_Hamiltonian_relative_permutation',cycles0=cc0,cycles1=cc1)
    w0=[-bb*pow(aa,-1,p)%p for aa,bb in zip(a,b)]
    w1=[-e[R1[i]]*pow(d[R1[i]],-1,p)%p for i in range(n)]
    guards=[]
    for w,cc in ((w0,cc0),(w1,cc1)):
        gg=[]
        for cyc in cc:
            val=1
            for i in cyc:val=val*w[i]%p
            gg.append((1-val)%p)
        guards.append(gg)
    if not all(x for gg in guards for x in gg):return dict(status='REJECT',reason='singular_Green_denominator',guards=guards)
    W0=h.mul(h.diag(w0),h.perm(R0));W1=h.mul(h.diag(w1),h.perm(R1))
    assert U==h.mul(h.diag(a),h.mul(h.sub(h.eye(n),W0),h.perm(r0)))
    assert V==h.mul(h.perm(s0),h.mul(h.sub(h.eye(n),W1),h.diag(d)))
    return dict(status='PASS',a=a,d=d,w0=w0,w1=w1,R0=R0,R1=R1,cycles0=cc0,cycles1=cc1,guards=guards)

def sparse_sandwich(U,B,V):
    n=len(B);p=h.p
    rows=[[(j,v)for j,v in enumerate(row)if v]for row in U]
    cols=[[(i,V[i][j])for i in range(n)if V[i][j]]for j in range(n)]
    assert all(len(x)<=2 for x in rows+cols)
    K=[[sum(a*B[k][ell]*b for k,a in rows[i]for ell,b in cols[j])%p for j in range(n)]for i in range(n)]
    assert K==h.mul(U,h.mul(B,V))
    queries=sum(len(rows[i])*len(cols[j])for i in range(n)for j in range(n))
    return K,queries

def scale_solve(U,V,K):
    n=len(U);p=h.p;adj=[[]for _ in range(2*n)];equations=[]
    for i in range(n):
        for j in range(n):
            aa,bb,k=V[i][j],U[i][j],K[i][j]
            if not aa and not bb:
                if k:return dict(status='REJECT',reason='off_support_entry',position=[i,j],value=k)
                continue
            coeff=([(i,aa)]if aa else[])+([(n+j,bb)]if bb else[])
            e=len(equations);equations.append(dict(position=[i,j],coefficients=coeff,rhs=k))
            if aa and bb:
                adj[i].append((n+j,-aa*pow(bb,-1,p)%p,k*pow(bb,-1,p)%p,e))
                adj[n+j].append((i,-bb*pow(aa,-1,p)%p,k*pow(aa,-1,p)%p,e))
    components=[];belong=[None]*(2*n);alpha=[None]*(2*n);beta=[None]*(2*n);tree=[]
    for root in range(2*n):
        if belong[root]is not None:continue
        c=len(components);members=[];queue=[root];belong[root]=c;alpha[root]=1;beta[root]=0
        for v in queue:
            members.append(v)
            for w,a,b,e in adj[v]:
                if belong[w]is None:
                    belong[w]=c;alpha[w]=a*alpha[v]%p;beta[w]=(a*beta[v]+b)%p;tree.append((v,w,e));queue.append(w)
        components.append(members)
    imposed=[[]for _ in components]
    for e,eq in enumerate(equations):
        coeff=eq['coefficients'];c=belong[coeff[0][0]];assert all(belong[v]==c for v,a in coeff)
        aa=sum(a*alpha[v]for v,a in coeff)%p;bb=(sum(a*beta[v]for v,a in coeff)-eq['rhs'])%p
        if aa:imposed[c].append(((-bb*pow(aa,-1,p))%p,e))
        elif bb:return dict(status='REJECT',reason='linear_cycle_contradiction',equation=e,residual=bb,equations=equations,tree=tree,alpha=alpha,beta=beta)
    values=[None]*(2*n);choices=[]
    for c,members in enumerate(components):
        assert all(alpha[v]for v in members)
        forbid=sorted({-beta[v]*pow(alpha[v],-1,p)%p for v in members})
        fixed=imposed[c]
        if fixed:
            t,first=fixed[0]
            for tt,e in fixed[1:]:
                if tt!=t:return dict(status='REJECT',reason='conflicting_linear_pins',component=c,pins=[[t,first],[tt,e]],equations=equations,tree=tree,alpha=alpha,beta=beta)
            if t in forbid:return dict(status='REJECT',reason='forced_zero_scale',component=c,parameter=t,forbidden=forbid,equations=equations)
        else:
            t=next((t for t in range(min(p,len(forbid)+1))if t not in forbid),None)
            if t is None:return dict(status='REJECT',reason='no_nonzero_parameter',component=c,variables=members,forbidden=forbid,field_size=p,equations=equations)
        for v in members:values[v]=(alpha[v]*t+beta[v])%p;assert values[v]
        choices.append(dict(variables=members,parameter=t,fixed=bool(fixed),forbidden=forbid))
    assert all(sum(a*values[v]for v,a in eq['coefficients'])%p==eq['rhs']for eq in equations)
    return dict(status='PASS',x=values[:n],y=values[n:],equation_count=len(equations),components=len(components),choices=choices)

def green_apply(w,cyc,v):
    p=h.p;pref=1;total=0
    for i in cyc:total=(total+pref*v[i])%p;pref=pref*w[i]%p
    out=[0]*len(v);out[cyc[0]]=total*pow((1-pref)%p,-1,p)%p
    for k in range(len(cyc)-1,0,-1):
        i=cyc[k];out[i]=(v[i]+w[i]*out[cyc[(k+1)%len(cyc)]])%p
    return out

def recover(B,U,V,patterns,check_scans=True):
    n=len(U);p=h.p;r0,r1,s0,s1=patterns
    st=structural(U,V,*patterns)
    if st['status']!='PASS':return st
    K,queries=sparse_sandwich(U,B,V);answer=scale_solve(U,V,K)
    if answer['status']!='PASS':return dict(answer,structural_guards=st['guards'],target_entry_queries=queries)
    x,y=answer['x'],answer['y'];dx=[xx*pow(aa,-1,p)%p for xx,aa in zip(x,st['a'])];dy=[yy*pow(dd,-1,p)%p for yy,dd in zip(y,st['d'])]
    W0=h.mul(h.diag(st['w0']),h.perm(st['R0']));W1=h.mul(h.diag(st['w1']),h.perm(st['R1']))
    T0=h.mul(h.perm(h.pinv(r0)),h.mul(h.inv(h.sub(h.eye(n),W0)),h.diag(dx)))
    T1=h.mul(h.diag(dy),h.mul(h.inv(h.sub(h.eye(n),W1)),h.perm(h.pinv(s0))))
    Q0=h.mul(h.diag([pow(v,-1,p)for v in x]),U);Q1=h.mul(V,h.diag([pow(v,-1,p)for v in y]))
    assert h.add(T0,T1)==B and h.inv(T0)==Q0 and h.inv(T1)==Q1
    assert h.mul(Q0,h.mul(B,Q1))==h.add(Q0,Q1)
    # Retain separately prescribed endpoint permutations, not just their combined base support.
    original_permutation_controls=[]
    for branch,(Q,T,base,edge)in enumerate(((Q0,T0,r0,r1),(Q1,T1,s0,s1))):
        lp=[(i+2)%n for i in range(n)]if branch==0 else([1,0]+list(range(2,n)))
        PL=h.perm(lp)
        PR=h.mul(h.inv(PL),h.perm(h.pinv(base)))
        cycle_matrix=h.mul(PR,h.mul(h.perm(edge),PL))
        pp=[row.index(1)for row in cycle_matrix];assert len(cycles(pp))==1
        assert h.mul(h.inv(PR),h.inv(PL))==h.perm(base)
        assert h.mul(h.inv(PR),h.mul(h.perm(pp),h.inv(PL)))==h.perm(edge)
        Qprime=h.mul(PR,h.mul(Q,PL));gg=[Qprime[i][i]for i in range(n)];assert all(gg)
        ww=[-Qprime[i][pp[i]]*pow(gg[i],-1,p)%p for i in range(n)]
        denominator=h.sub(h.eye(n),h.mul(h.diag(ww),h.perm(pp)))
        assert Qprime==h.mul(h.diag(gg),denominator)
        reconstructed=h.mul(PL,h.mul(h.inv(denominator),h.mul(h.diag([pow(g,-1,p)for g in gg]),PR)))
        assert reconstructed==T
        original_permutation_controls.append(dict(left_permutation=lp,right_permutation=[row.index(1)for row in PR],cycle=pp))
    checked=0
    if check_scans:
        for j in range(n):
            v=[int(i==j)for i in range(n)]
            z=green_apply(st['w0'],st['cycles0'][0],[a*b%p for a,b in zip(dx,v)])
            out0=[z[i]for i in h.pinv(r0)]
            z=green_apply(st['w1'],st['cycles1'][0],[v[i]for i in h.pinv(s0)])
            out1=[a*b%p for a,b in zip(dy,z)]
            assert out0==h.mv(T0,v)and out1==h.mv(T1,v)
            assert [(a+b)%p for a,b in zip(out0,out1)]==h.mv(B,v);checked+=1
    return dict(answer,original_endpoint_permutation_controls=original_permutation_controls,structural_guards=st['guards'],target_entry_queries=queries,target_entries_verified=n*n,basis_vectors_checked=checked,recovered_weights0=st['w0'],recovered_weights1=st['w1'])

def directional_checks(B,U,V,patterns):
    n=len(B);r0,r1,s0,s1=patterns;c0,c1=h.pinv(s0),h.pinv(s1)
    K,_=sparse_sandwich(U,B,V);UB=h.mul(U,B);column_ranks=[]
    for j in range(n):
        rows=[];v=[V[c0[j]][j],V[c1[j]][j]]
        for i in range(n):
            if j in(r0[i],r1[i],s0[i],s1[i]):continue
            row=[UB[i][c0[j]],UB[i][c1[j]]];assert sum(a*b for a,b in zip(row,v))%h.p==0;assert K[i][j]==0;rows.append(row)
        nz=[row for row in rows if any(row)];rank=int(bool(nz))
        if nz and any(h.det([nz[0],row])for row in nz[1:]):rank=2
        assert rank<=1;column_ranks.append(rank)
    rel=h.extract(B,*patterns);u=[[U[i][r0[i]],U[i][r1[i]]]for i in range(n)]
    assert all(h.bilinear(L,u[i],u[k])==0 for i,k,L in rel)
    gate=h.solve_rows(n,rel,finite=True);assert gate['status']=='PASS'
    return dict(row_gate='PASS',selected_relations=len(rel),column_nullspace_ranks=column_ranks,joint_off_support='PASS')

def positives():
    out=[];p=h.p
    for n in(5,8,9):
        ident=list(range(n));R0=[(i+1)%n for i in ident];sig=ident[:];sig[0],sig[1]=1,0;R1=[sig[R0[sig[i]]]for i in ident]
        assert h.mul(h.perm(R0),h.perm(R1))!=h.mul(h.perm(R1),h.perm(R0))
        for monomial,zeros in product((False,True),repeat=2):
            r0=sig if monomial else ident;s0=[(-i)%n for i in ident]if monomial else ident
            r1=[r0[R0[i]]for i in ident];s1=[R1[s0[i]]for i in ident]
            w0=[2]*n;w1=[3]*n
            if zeros:w0[1]=0;w1[-1]=0
            aa=[i+2 for i in ident];dd=[i+5 for i in ident];xx=[i+11 for i in ident];yy=[2*i+13 for i in ident]
            G0=h.sub(h.eye(n),h.mul(h.diag(w0),h.perm(R0)));G1=h.sub(h.eye(n),h.mul(h.diag(w1),h.perm(R1)))
            U=h.mul(h.diag(aa),h.mul(G0,h.perm(r0)));V=h.mul(h.perm(s0),h.mul(G1,h.diag(dd)))
            T0=h.mul(h.perm(h.pinv(r0)),h.mul(h.inv(G0),h.diag([x*pow(a,-1,p)%p for x,a in zip(xx,aa)])))
            T1=h.mul(h.diag([y*pow(d,-1,p)%p for y,d in zip(yy,dd)]),h.mul(h.inv(G1),h.perm(h.pinv(s0))))
            B=h.add(T0,T1);patterns=(r0,r1,s0,s1)
            direct=directional_checks(B,U,V,patterns);answer=recover(B,U,V,patterns);assert answer['status']=='PASS'
            # Gauge normalization must preserve recovered plan validity.
            lam=[i+2 for i in ident];mu=[i+4 for i in ident]
            Ug=h.mul(h.diag(lam),U);Vg=h.mul(V,h.diag(mu))
            Kg,_=sparse_sandwich(Ug,B,Vg)
            xg=[a*b%p for a,b in zip(lam,answer['x'])];yg=[a*b%p for a,b in zip(mu,answer['y'])]
            assert Kg==h.add(h.mul(Ug,h.diag(yg)),h.mul(h.diag(xg),Vg))
            out.append(dict(N=n,monomial_endpoints=monomial,zero_edges=zeros,directions=direct,recovery=answer))
    return out

def negative_controls():
    p=h.p;n=5;ident=list(range(n));pi=[1,2,3,4,0];tau=[2,0,3,4,1]
    U=h.sub(h.eye(n),h.scale(2,h.perm(pi)));V=h.sub(h.eye(n),h.scale(3,h.perm(tau)))
    K=h.add(U,V);K[0][0]=(K[0][0]+1)%p;B=h.mul(h.inv(U),h.mul(K,h.inv(V)))
    patterns=(ident,pi,ident,tau);direct=directional_checks(B,U,V,patterns);answer=recover(B,U,V,patterns)
    assert answer['status']=='REJECT'and answer['reason']in('conflicting_linear_pins','linear_cycle_contradiction')
    # Three exact equations already form a standalone inconsistency certificate.
    assert (U[0][2],V[0][2],K[0][2])==(0,p-3,p-3)
    assert (U[4][0],V[4][0],K[4][0])==(p-2,0,p-2)
    assert (U[0][0],V[0][0],K[0][0])==(1,1,3)
    h.inv(B) # Additional diagnostic: this synthetic target is invertible too.
    out=[dict(name='joint_direction_pass_scale_failure',prime=p,N=n,pi=pi,tau=tau,B=B,directions=direct,result=answer,short_certificate=['x0=1','y0=1','x0+y0=3','0=1'])]
    n=3;ident=list(range(n));pi=[1,2,0];tau=[2,0,1];patterns=(ident,pi,ident,tau)
    U=h.perm(pi);V=h.eye(n);B=h.add(h.inv(U),V)
    answer=recover(B,U,V,patterns);assert answer['reason']=='zero_base_coordinate'
    out.append(dict(name='invertible_but_zero_base_coordinate',result=answer))
    U=h.sub(h.eye(n),h.perm(pi));V=U;B=[[0]*n for _ in range(n)]
    patterns=(ident,pi,ident,pi);assert h.add(h.scale(-1,U),V)==B
    answer=recover(B,U,V,patterns);assert answer['reason']=='singular_Green_denominator'
    out.append(dict(name='linear_solution_but_singular_Green_direction',result=answer))
    h.p=2;n=3;ident=list(range(n));pi=[1,2,0];tau=[2,0,1];patterns=(ident,pi,ident,tau)
    U=V=B=h.eye(n);answer=recover(B,U,V,patterns);assert answer['reason']=='no_nonzero_parameter'and answer['forbidden']==[0,1]
    out.append(dict(name='finite_field_forbidden_values_exhausted',prime=2,result=answer))
    h.p=5;U=V=B=h.eye(n);answer=recover(B,U,V,patterns);assert answer['status']=='PASS'
    out.append(dict(name='same_identity_directions_larger_field',prime=5,result=answer))
    h.p=p
    return out

def main():
    pos=positives();neg=negative_controls()
    result=dict(status='PASS',prime=241,constructed_positive_targets=len(pos),noncommuting_positive_targets=len(pos),monomial_positive_targets=sum(x['monomial_endpoints']for x in pos),zero_edge_positive_targets=sum(x['zero_edges']for x in pos),basis_vectors_checked=sum(x['recovery']['basis_vectors_checked']for x in pos),target_entries_verified=sum(x['recovery']['target_entries_verified']for x in pos),positive_controls=pos,other_controls=neg,scope='Complete fixed-direction invertible-endpoint certificate; no unrestricted direction search.')
    Path(__file__).with_name('FIXED_DIRECTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
