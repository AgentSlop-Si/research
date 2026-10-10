"""Fresh 2026-10-10 reconstruction from displayed mathematics, not source code.
Standard-library only. No supplied program imported, parsed or executed.
Field encoding: integer a+241*b denotes a+b*theta, theta^2=7.
"""
from itertools import permutations, combinations, product
from pathlib import Path
import json, hashlib

P = 241
def add(x,y): return ((x%P+y%P)%P)+P*((x//P+y//P)%P)
def neg(x): return (-x%P)+P*((- (x//P))%P)
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    a,b=x%P,x//P; c,d=y%P,y//P
    return ((a*c+7*b*d)%P)+P*((a*d+b*c)%P)
def inv(x):
    a,b=x%P,x//P; z=pow((a*a-7*b*b)%P,-1,P)
    return a*z%P+P*((-b*z)%P)
def div(x,y): return mul(x,inv(y))
def sm(xs):
    s=0
    for x in xs: s=add(s,x)
    return s
def tr(A): return [list(x) for x in zip(*A)]
def mm(A,B): return [[sm(mul(x,y) for x,y in zip(r,c)) for c in tr(B)] for r in A]
def det2(A): return sub(mul(A[0][0],A[1][1]),mul(A[0][1],A[1][0]))
def inverse(A):
    n=len(A); T=[r[:]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
    for j in range(n):
        i=next(i for i in range(j,n) if T[i][j]); T[j],T[i]=T[i],T[j]
        v=inv(T[j][j]); T[j]=[mul(v,x) for x in T[j]]
        for i in range(n):
            if i!=j and T[i][j]:
                v=T[i][j]; T[i]=[sub(x,mul(v,y)) for x,y in zip(T[i],T[j])]
    return [r[n:] for r in T]
def rank_rows(A):
    T=[r[:] for r in A]; ids=list(range(len(A))); piv=[]; k=0
    for j in range(len(T[0])):
        ii=next((i for i in range(k,len(T)) if T[i][j]),None)
        if ii is None: continue
        T[k],T[ii]=T[ii],T[k]; ids[k],ids[ii]=ids[ii],ids[k]
        piv.append(ids[k]); v=inv(T[k][j]); T[k]=[mul(v,x) for x in T[k]]
        for i in range(k+1,len(T)):
            if T[i][j]:
                v=T[i][j]; T[i]=[sub(x,mul(v,y)) for x,y in zip(T[i],T[k])]
        k+=1
        if k==len(T):break
    return k,piv
def det(A):
    T=[r[:] for r in A]; d=1
    for j in range(len(T)):
        ii=next((i for i in range(j,len(T)) if T[i][j]),None)
        if ii is None:return 0
        if ii!=j:T[j],T[ii]=T[ii],T[j]; d=neg(d)
        v=T[j][j]; d=mul(d,v); iv=inv(v)
        for i in range(j+1,len(T)):
            a=mul(T[i][j],iv)
            T[i]=[sub(x,mul(a,y)) for x,y in zip(T[i],T[j])]
    return d
def normpair(v):
    i=next(i for i,z in enumerate(v) if z)
    return tuple(div(x,v[i]) for x in v)
SQ={i*i%P:i for i in range(P)}
def sqrt_base(a):
    a%=P
    if a in SQ: return SQ[a]
    return P*SQ[a*pow(7,-1,P)%P]
def roots(q):
    # q=(A,B,C) means A*x^2+B*x*y+C*y^2, over the base field.
    a,b,c=q; ans=[]
    if c:
        z=sqrt_base((b*b-4*a*c)%P)
        ans=[(1,div(add((-b)%P,z),2*c%P)),(1,div(sub((-b)%P,z),2*c%P))]
    elif b: ans=[(1,(-a*pow(b,-1,P))%P),(0,1)]
    elif a: ans=[(0,1)]
    else: raise ValueError('Unrestricted quadratic must be omitted')
    return sorted(set(ans))
def qeval(q,v): return sm([mul(q[0],mul(v[0],v[0])),mul(q[1],mul(v[0],v[1])),mul(q[2],mul(v[1],v[1]))])
I=[[1,0],[0,1]]; J=[[0,1],[P-1,0]]
def action(T,v): return normpair([sm(mul(a,b) for a,b in zip(row,v)) for row in T])

def main():
    assert pow(7,120,P)==P-1 and pow(91,5,P)==1 and 91!=1
    z=91; g=(1+2*(pow(z,2,P)+pow(z,3,P)))%P; c=5*g%P
    B=[[(pow(z,i*j%5,P)-g*pow(z,-3*(i+j)**2%5,P)+(c*pow(z,-3*i*i%5,P) if i==j else 0))*pow(1+c,-1,P)%P for j in range(5)] for i in range(5)]
    F=[[pow(z,i*j%5,P) for j in range(5)] for i in range(5)]
    A=inverse(F)
    for i in range(5):A[i][i]=add(A[i][i],pow(z,3*i*i%5,P))
    assert inverse(A)==B and g*g%P==5
    cycles=[]
    for t in permutations(range(1,5)):
        v=(0,)+t; pi=[0]*5
        for i in range(5):pi[v[i]]=v[(i+1)%5]
        cycles.append(pi)
    rows=[]; branches=[]; total_edges=0; empty=0; topology={}; base_counts=[0,0,0]
    for ip,pi in enumerate(cycles):
      for it,tau in enumerate(cycles):
        tinv=[tau.index(j) for j in range(5)]
        matrices={}; eligible={}
        for j in range(5):
            eligible[j]=[i for i in range(5) if j not in (i,pi[i],tau[i])]
            for i in eligible[j]: matrices[i,j]=[[B[i][j],B[i][tinv[j]]],[B[pi[i]][j],B[pi[i]][tinv[j]]]]
        edges=[]; adj=[[] for _ in range(5)]
        for j in range(5):
          for i,k in combinations(eligible[j],2):
            C=mm(mm(matrices[i,j],J),tr(matrices[k,j]))
            assert det2(C) and det2(C)==mul(det2(matrices[i,j]),det2(matrices[k,j]))
            e=len(edges); edges.append((i,k,j,C)); adj[i].append((k,e,mm(J,tr(C)))); adj[k].append((i,e,mm(J,C)))
        total_edges+=len(edges)
        transforms={}; components=[]; component_of={}; forest=[]
        for root in range(5):
            if root in transforms:continue
            todo=[root]; transforms[root]=I; component=[]
            while todo:
                i=todo.pop(); component.append(i);component_of[i]=len(components)
                for k,e,T in adj[i]:
                    if k not in transforms:
                        transforms[k]=mm(T,transforms[i]);todo.append(k);forest.append(e)
            components.append(sorted(component))
        quads=[[] for _ in components]
        for i,k,j,C in edges:
            R=mm(mm(tr(transforms[i]),C),transforms[k])
            q=(R[0][0],add(R[0][1],R[1][0]),R[1][1])
            if any(q):quads[component_of[i]].append(q)
        domains=[]
        for qs in quads:
            assert qs, 'A continuous row component would need a new proof'
            cand=roots(qs[0]);domains.append([v for v in cand if all(qeval(q,v)==0 for q in qs)])
        record={'cycles':[ip,it],'components':components,'forest_edges':forest,'quadratics':quads,'domains':domains}
        rows.append(record)
        if any(not d for d in domains):empty+=1;continue
        key=str([len(d) for d in domains]);topology[key]=topology.get(key,0)+1
        for root_values in product(*domains):
            us=[action(transforms[i],root_values[component_of[i]]) for i in range(5)]
            vs=[]
            for j in range(5):
                cs=[[sm(mul(us[i][k],matrices[i,j][k][h]) for k in range(2)) for h in range(2)] for i in eligible[j]]
                assert rank_rows(cs)[0]==1
                u=next(v for v in cs if any(v)); v=normpair((neg(u[1]),u[0]));vs.append(v)
                assert all(sm(mul(x,y) for x,y in zip(v,a))==0 for a in cs)
            U=[[0]*5 for _ in range(5)];V=[[0]*5 for _ in range(5)]
            for i in range(5):U[i][i],U[i][pi[i]]=us[i]
            for j in range(5):V[j][j],V[tinv[j]][j]=vs[j]
            K=mm(mm(U,B),V); aug=[]
            for i in range(5):
              for j in range(5):
                r=[0]*11;r[i]=V[i][j];r[5+j]=U[i][j];r[10]=K[i][j];aug.append(r)
                if i in eligible[j]:assert K[i][j]==0
            rc,_=rank_rows([r[:10] for r in aug]);ra,piv=rank_rows(aug)
            assert (rc,ra)==(10,11)
            delta=det([aug[r] for r in piv]);assert delta
            nr=[sum(r//5==i for r in piv)-1 for i in range(5)]
            nc=[sum(r%5==j for r in piv)-1 for j in range(5)]
            assert min(nr+nc)>=0 and sum(nr)==sum(nc)==6
            zr=any(v[0]==0 for v in us);zc=any(v[0]==0 for v in vs)
            base_counts[0]+=zr;base_counts[1]+=zc;base_counts[2]+=not(zr or zc)
            branches.append({'cycles':[ip,it],'u':us,'v':vs,'equation_rows':piv,'determinant':delta,'row_multidegrees':nr,'column_multidegrees':nc})
    assert len(rows)==576 and empty==384 and len(branches)==624
    assert total_edges==4320 and topology=={'[2]':72,'[2, 2]':120}
    assert base_counts==[240,240,144]
    controls=[]
    def branch(pi,weights,left,right):
        T=[[int(i==j) for j in range(5)] for i in range(5)]
        for i in range(5):T[i][pi[i]]=neg(weights[i])
        G=inverse(T)
        return [[mul(mul(left[i],G[i][j]),right[j]) for j in range(5)] for i in range(5)]
    def leading_pair(coeffs,endpoints):
        # Endpoint zero is epsilon. Keep lowest-valuation nonzero coefficients.
        vv=[(-1 if e==0 else 0, c if e==0 else div(c,e)) for c,e in zip(coeffs,endpoints)]
        valuation=min(v for v,c in vv if c)
        return normpair([c if v==valuation else 0 for v,c in vv])
    for seed in range(12):
        pi=cycles[seed];tau=cycles[(7*seed+5)%24];tinv=[tau.index(j) for j in range(5)]
        w1=[2+i+seed for i in range(5)];w2=[11+2*i+seed for i in range(5)]
        w1[seed%5]=0;w2[(seed+2)%5]=0
        if seed==0:w1=[0]*5
        l1=[3+i+seed for i in range(5)];r1=[17+i+seed for i in range(5)]
        l2=[31+i+seed for i in range(5)];r2=[43+i+seed for i in range(5)]
        if seed<8:l1[seed%5]=0;r1[(seed+1)%5]=0;l2[(seed+2)%5]=0;r2[(seed+3)%5]=0
        G1=branch(pi,w1,l1,r1);G2=branch(tau,w2,l2,r2)
        target=[[add(G1[i][j],G2[i][j]) for j in range(5)] for i in range(5)]
        us=[leading_pair([1,neg(w1[i])],[l1[i],l1[pi[i]]]) for i in range(5)]
        vs=[leading_pair([1,neg(w2[tinv[j]])],[r2[j],r2[tinv[j]]]) for j in range(5)]
        U=[[0]*5 for _ in range(5)];V=[[0]*5 for _ in range(5)]
        for i in range(5):U[i][i],U[i][pi[i]]=us[i]
        for j in range(5):V[j][j],V[tinv[j]][j]=vs[j]
        K=mm(mm(U,target),V);aug=[]
        for i in range(5):
          for j in range(5):
            if j not in (i,pi[i],tau[i]):assert K[i][j]==0
            r=[0]*11;r[i]=V[i][j];r[5+j]=U[i][j];r[10]=K[i][j];aug.append(r)
        rank,_=rank_rows(aug);assert rank<=10
        controls.append({'seed':seed,'singular_endpoint_masks':seed<8,'zero_edges':True,'augmented_rank':rank})
    summary={'fresh_reconstruction':True,'supplied_programs_executed':False,'field':'GF(241)[theta]/(theta^2-7)','encoding':'a+241*b means a+b*theta','target':B,'ordered_cycle_pairs':len(rows),'nonsingular_transition_equations':total_edges,'empty_row_domains':empty,'surviving_topologies':topology,'surviving_row_branches':len(branches),'rank_one_columns':5*len(branches),'coefficient_rank':10,'augmented_rank':11,'zero_row_base_branches':base_counts[0],'zero_column_base_branches':base_counts[1],'neither_zero_base_branches':base_counts[2],'fresh_positive_controls':controls}
    out=Path(__file__).resolve().parent
    (out/'GREEN_FRESH_CERTIFICATE.json').write_text(json.dumps({'summary':summary,'cycles':cycles,'rows':rows,'branches':branches},indent=2)+'\n')
    (out/'GREEN_FRESH_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
