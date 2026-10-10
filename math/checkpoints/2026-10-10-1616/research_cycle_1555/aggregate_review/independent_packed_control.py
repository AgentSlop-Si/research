"""Fresh exact check of packed disjoint four-vertex chains; reviewer code only."""
from reviewer_prime_ring import PrimeRing
from pathlib import Path
import json

def verify(p):
    K=PrimeRing(p);z=K.z;mul=K.mul;add=K.add;sub=K.sub;Z=K.zero;O=K.one
    a=K.sum((O,z(1),z(-1)));m=p//4
    assert a!=Z and a!=O
    F=[[z(i*t) for t in range(p)] for i in range(p)]
    C=[[O if i==j else Z for j in range(p)] for i in range(p)]
    R=[list(row) for row in F]
    expected_zeros=[]
    for k in range(m):
        q=4*k
        C[q+2][q+1]=O; C[q+3][q+2]=a; C[q][q+3]=O
        for t in range(p):
            R[q+2][t]=sub(F[q+2][t],R[q+1][t])
            R[q+3][t]=sub(F[q+3][t],mul(a,R[q+2][t]))
            R[q][t]=sub(F[q][t],R[q+3][t])
        expected_zeros += [[q+2,0],[q,0],[q,1],[q,p-1]]
    zeros=[[i,t] for i in range(p) for t in range(p) if R[i][t]==Z]
    assert zeros==sorted(expected_zeros)
    r=[sum(R[i][t]!=Z for i in range(p)) for t in range(p)]
    assert r==[p-2*m]+[p-m]+[p]*(p-3)+[p-m]
    Crows=[[(j,x) for j,x in enumerate(row) if x!=Z] for row in C]
    for i in range(p):
        for t in range(p):assert K.sum(mul(c,R[v][t]) for v,c in Crows[i])==F[i][t]
    # Exact inverse by finite nilpotent series I-N+N²-N³.
    N=[[sub(C[i][j],O if i==j else Z) for j in range(p)] for i in range(p)]
    def mm(A,B):return [[K.sum(mul(x,y) for x,y in zip(row,col)) for col in zip(*B)] for row in A]
    N2=mm(N,N);N3=mm(N2,N);N4=mm(N3,N)
    assert all(x==Z for row in N4 for x in row)
    Ci=[[K.sum((O if i==j else Z,K.neg(N[i][j]),N2[i][j],K.neg(N3[i][j]))) for j in range(p)] for i in range(p)]
    assert sum(x!=Z for row in Ci for x in row)==p+6*m
    assert mm(C,Ci)==[[O if i==j else Z for j in range(p)] for i in range(p)]
    inv2=(p+1)//2
    raw=[[Z for j in range(p)] for i in range(p)]
    colored_count=0
    for t in range(p):
        # B_t has only column t; every entry is a separately charged t-edge.
        col=[mul(z(-inv2*t*t),R[v][t]) for v in range(p)]
        colored_count+=sum(x!=Z for x in col)
        for i in range(p):
            cb=K.sum(mul(c,col[v]) for v,c in Crows[i])
            for j in range(p):
                actual=mul(cb,F[t][j]);assert actual==z(-inv2*t*t+(i+j)*t)
                raw[i][j]=add(raw[i][j],actual)
    G=K.sum(z(-inv2*t*t) for t in range(p));assert mul(G,K.conj(G))==K.scalar(O,p)
    for i in range(p):
        for j in range(p):assert mul(z(-inv2*(i*i+j*j)),raw[i][j])==mul(G,F[i][j])
    nC=sum(x!=Z for row in C for x in row)
    assert nC==p+3*m and colored_count==p*p-4*m
    # Pointwise no-gauge witness: first chain's column1 reaches outputs1,2
    # with ratio1 and has a nonzero middle entry for both labels0 and1.
    assert C[1][1]==C[2][1]==O and R[1][0]!=Z and R[1][1]!=Z and z(1)!=O
    return {'p':p,'blocks':m,'A':p*p,'C':nC,'middle':colored_count,'E':p*p+nC+colored_count,'strict_fiber_baseline':2*p*p+p,'saving':m,'inverse_C':p+6*m,'delta_C':3*m,'r':r,'R_zero_positions':zeros,'fiber_entries_checked':p**3,'corrected_entries_checked':p*p,'pointwise_gauge_obstruction_verified':True}
results=[verify(p) for p in (5,7,11,13,17,19)]
out={'status':'passed_exact','source_programs_executed_or_imported':False,'cases':results,'fiber_entries_total':sum(x['fiber_entries_checked'] for x in results),'corrected_entries_total':sum(x['corrected_entries_checked'] for x in results)}
Path(__file__).with_name('INDEPENDENT_PACKED_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
