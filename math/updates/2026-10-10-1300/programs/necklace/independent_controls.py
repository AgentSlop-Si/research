"""Fresh audit controls. Does not import, execute, or copy uploaded programs.

Uses exhaustive rotation grouping and elementary path-jet propagation as
deliberately slow verification oracles. Not an algorithm-performance test.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import json, random

ROOT = Path(__file__).resolve().parent
RNG = random.Random(202610101251)

def orbits(n, k):
    seen = set()
    rows = []
    for bits in product((0, 1), repeat=k):
        if bits in seen:
            continue
        rotations = {bits[t:] + bits[:t] for t in range(k)}
        seen.update(rotations)
        states = []
        for t in range(k):
            s = sum(bits[(t-n+j) % k] << (n-1-j) for j in range(n))
            states.append(2*s+bits[t])
        rows.append((len(rotations), states))
    return rows

def scalar_product(xs, p):
    r = 1
    for x in xs:
        r = r*x % p
    return r

def orbit_value(rows, base, p):
    return sum(c*scalar_product([base[e] for e in edges], p) for c, edges in rows) % p

def positional_mixed(rows, base, u, v, p):
    total = 0
    for c, edges in rows:
        for i, e in enumerate(edges):
            for j, f in enumerate(edges):
                if i != j:
                    total += c*u[e]*v[f]*scalar_product([base[g] for q,g in enumerate(edges) if q not in (i,j)],p)
    return total % p

def path_jet(n, k, base, u, v, p):
    """Propagate (constant,t,s,ts) path coefficients from each vertex."""
    N = 1 << n
    out = [0]*4
    for start in range(N):
        values = [[0]*4 for _ in range(N)]
        values[start][0] = 1
        for _ in range(k):
            nxt = [[0]*4 for _ in range(N)]
            for s, (a,b,c,d) in enumerate(values):
                for bit in (0,1):
                    e=2*s+bit; dest=e%N; w=base[e]
                    add=(a*w,b*w+a*u[e],c*w+a*v[e],d*w+b*v[e]+c*u[e])
                    for q in range(4):
                        nxt[dest][q]=(nxt[dest][q]+add[q])%p
            values=nxt
        out=[(a+b)%p for a,b in zip(out,values[start])]
    return out

def gram_matrix(rows, base, p):
    E=len(base); H=[[0]*E for _ in range(E)]
    for coeff,edges in rows:
        mult=Counter(edges)
        lam=coeff*scalar_product([base[e] for e in edges],p)%p
        for e,m in mult.items():
            for f,r in mult.items():
                value=lam*m*(r-int(e==f))*pow(base[e],-1,p)*pow(base[f],-1,p)
                H[e][f]=(H[e][f]+value)%p
    return H

def matrix_rank(A,p):
    A=[row[:] for row in A]; i=0
    for j in range(len(A[0])):
        piv=next((h for h in range(i,len(A)) if A[h][j]),None)
        if piv is None: continue
        A[i],A[piv]=A[piv],A[i]
        z=pow(A[i][j],-1,p); A[i]=[a*z%p for a in A[i]]
        for h in range(i+1,len(A)):
            c=A[h][j]
            if c:A[h]=[(a-c*b)%p for a,b in zip(A[h],A[i])]
        i+=1
        if i==len(A):break
    return i

def matvec(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]

def closed_green(cycle,gains,x,p):
    N=len(x); den=(1-scalar_product(gains,p))%p
    if not den:raise ZeroDivisionError('singular cycle')
    y=[0]*N
    for t,j in enumerate(cycle):
        acc=0; w=1
        for d in range(N):
            acc+=w*x[cycle[(t-d)%N]]
            w=w*gains[cycle[(t-d)%N]]%p
        y[j]=acc*pow(den,-1,p)%p
    return y

def run():
    report={'seed':202610101251,'uploaded_programs_executed':False,'scope':'Fresh independent finite controls, not proof by testing or fast-algorithm benchmark','groups':{}}
    # Original archive integrity is recorded separately in SOURCE_MANIFEST.json.
    count=0
    for p in (17,97):
        for n in range(1,6):
            E=2<<n
            for k in range(1,n+4):
                rows=orbits(n,k)
                assert sum(c for c,_ in rows)==1<<k
                for typ in range(3):
                    w=[RNG.randrange(p) for _ in range(E)]
                    if typ==1:w=[0 if j%3==0 else z for j,z in enumerate(w)]
                    if typ==2:w=[0]*E
                    assert orbit_value(rows,w,p)==path_jet(n,k,w,[0]*E,[0]*E,p)[0]
                    count+=1
    report['groups']['weighted_trace']={'comparisons':count,'n_range':[1,5],'k_range':'1 through n+3','fields':[17,97],'includes_zero_weights':True}
    count=0; gramchecks=0
    for p in (17,97):
        for n in range(1,5):
            E=2<<n
            for k in (n,n+1,n+2):
                rows=orbits(n,k)
                for typ in range(3):
                    base=[RNG.randrange(1,p) for _ in range(E)]
                    if typ==1:base=[0 if j%4==0 else z for j,z in enumerate(base)]
                    if typ==2:base=[0]*E
                    u=[RNG.randrange(p) for _ in range(E)];v=[RNG.randrange(p) for _ in range(E)]
                    truth=positional_mixed(rows,base,u,v,p)
                    assert truth==path_jet(n,k,base,u,v,p)[3]
                    if typ==0:
                        H=gram_matrix(rows,base,p)
                        assert truth==sum(a*b for a,b in zip(u,matvec(H,v,p)))%p
                        gramchecks+=1
                    count+=1
    report['groups']['hessian']={'independent_mixed_comparisons':count,'gram_comparisons':gramchecks,'includes_zero_baselines':True}
    cases=[]
    for n in range(1,9):
        for k in range(1,n+4):
            sets=[set() for _ in range(2<<n)]
            for _,edges in orbits(n,k):
                for i,e in enumerate(edges):
                    for j,f in enumerate(edges):
                        if i!=j:sets[e].add(f)
            bound=k*(1<<max(0,k-n-1));actual=max(map(len,sets))
            assert actual<=bound
            cases.append({'N':1<<n,'k':k,'max_support':actual,'bound':bound})
    report['groups']['structural_locality']={'plans':len(cases),'rows':cases,'N16_k6_sparse_marking_impossibility':16>6*2}
    count=0
    for p in (17,97):
        for N in (2,4,8,16):
            for _ in range(3):
                cycle=list(range(N));RNG.shuffle(cycle)
                while True:
                    a=[RNG.randrange(p) for _ in range(N)]
                    if scalar_product(a,p)!=1:break
                x=[RNG.randrange(p) for _ in range(N)]
                y=closed_green(cycle,a,x,p)
                assert all((y[j]-a[j]*y[cycle[(t-1)%N]]-x[j])%p==0 for t,j in enumerate(cycle))
                count+=1
    singular=False
    try:closed_green([0,1],[1,1],[1,2],17)
    except ZeroDivisionError:singular=True
    assert singular
    report['groups']['green_recurrence']={'equation_checks':count,'singular_cycle_control':singular}
    ranks=[]
    for p in (257,65537):
        for n in range(1,7):
            N=1<<n;k=n+2;omega=pow(3,(p-1)//N,p)
            assert pow(omega,N,p)==1 and pow(omega,N//2,p)!=1
            base=[v for s in range(N) for v in (1,pow(omega,s,p))]
            H=gram_matrix(orbits(n,k),base,p)
            ranks.append({'p':p,'N':N,'k':k,'rank':matrix_rank(H,p),'dimension':2*N})
    report['groups']['canonical_carrier_finite_ranks']={'cases':len(ranks),'rows':ranks,'all_size_rank_claim':False}
    H=gram_matrix(orbits(1,3),[1,1,1,2],3)
    assert H==[[0]*4 for _ in range(4)]
    report['groups']['characteristic_counterexample']={'p':3,'N':2,'k':3,'omega':2,'canonical_H':H,'rank':0,'Fourier_rank':2,'interpretation':'p divides k makes the ordinary trace carrier Hessian identically zero; not a counterexample over C'}
    assert orbit_value(orbits(2,2),[1,0,0,0,0,0,0,0],17)==1
    report['groups']['multiplicity_negative_control']={'N':4,'k':2,'only_loop0_weight':1,'correct_trace':1,'incorrect_k_instead_of_least_period':2}
    f4=[]
    for p in (17,97):
        omega=pow(3,(p-1)//4,p) if p==17 else 22
        assert pow(omega,2,p)==p-1
        A=[1,0,1,0];B=[1,0,-1,0];C=[0,1,0,1];D=[0,1,0,-1]
        H=[[(A[i]*A[j]+B[i]*C[j]+C[i]*B[j]+omega*D[i]*D[j])%p for j in range(4)] for i in range(4)]
        assert H==[[pow(omega,i*j,p) for j in range(4)] for i in range(4)]
        f4.append({'p':p,'omega':omega,'entries':16})
    report['groups']['F4_algebraic_control']={'rows':f4,'four_Green_factorization':False}
    report['passed_groups']=len(report['groups'])
    return report

if __name__=='__main__':
    report=run()
    (ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed_groups':report['passed_groups'],'groups':{k:{a:b for a,b in v.items() if isinstance(b,(int,bool,str))} for k,v in report['groups'].items()}},indent=2))
