"""Independent aggregate controls. No research-program imports."""
from pathlib import Path
import json
import sympy as s
from sympy import QQ

OUT=Path(__file__).parent

def factors(n):
    fs=[];d=2
    while d*d<=n:
        while n%d==0:fs.append(d);n//=d
        d+=1
    if n>1:fs.append(n)
    return fs

def center_order(p):
    k=(p-1)//2
    return [n for r in range(k) for n in (k-1-r,k+r)]

def hierarchy_order(p, fs=None):
    N=p-1;fs=fs or factors(N);g=int(s.primitive_root(p));exponents=[0];d=1
    for q in fs:
        d*=q;shift=N//d
        exponents=[(a+j*shift)%N for j in range(q) for a in exponents]
    return [pow(g,a,p)-1 for a in exponents]

def expected_hierarchy(p,fs):
    return sum((p-1)*(q-1)//q for q in fs)

def stabilizers(p,order):
    T=set();sizes=[]
    for n in order:
        T.add(n+1)
        sizes.append(sum({a*x%p for x in T}==T for a in range(1,p)))
    return sizes

def exact_control(p,kind):
    field=QQ.cyclotomic_field(p);z=field.unit;zero=field.zero;one=field.one
    zp=[z**i for i in range(p)]
    order=center_order(p) if kind=='center' else hierarchy_order(p)
    assert len(set(order))==p-1 and set(order)==set(range(p-1))
    beta=[zp[(n+1)%p]-zp[-(n+1)%p] for n in range(p-1)]
    assert all(beta)
    C=[[zero for _ in range(p)] for _ in range(p)]
    for i in range(p):C[i][i]=one
    for j in range(1,p-1):
        prev,cur=order[j-1:j+1];C[cur][prev]=-beta[prev]/beta[cur]
    F=[[zp[i*t%p] for t in range(p)] for i in range(p)]
    R=[row[:] for row in F]
    prefixes=[]
    for j,cur in enumerate(order):
        if j:
            prev=order[j-1]
            R[cur]=[F[cur][t]-C[cur][prev]*R[prev][t] for t in range(p)]
        prefixes.append([t for t in range(p) if not R[cur][t]])
    assert all(sum((C[i][j]*R[j][t] for j in range(p)),zero)==F[i][t] for i in range(p) for t in range(p))
    st=stabilizers(p,order)
    assert [len(a) for a in prefixes]==[a-1 for a in st]
    if kind=='center':
        expected=[0 if L%2 else (1 if L<p-1 else p-2) for L in range(1,p)]
        assert [len(a) for a in prefixes]==expected
        predicted_Z=(3*p-7)//2
    else:predicted_Z=expected_hierarchy(p,factors(p-1))
    nnzC=sum(bool(a) for row in C for a in row)
    nnzR=sum(bool(a) for row in R for a in row)
    assert nnzC==2*p-2 and p*p-nnzR==predicted_Z
    # Literal inverse and both products, using independently forward-solved columns.
    V=[[zero for _ in range(p)] for _ in range(p)]
    for col in range(p):
        V[p-1][col]=one if col==p-1 else zero
        for j,cur in enumerate(order):
            V[cur][col]=(one if cur==col else zero)-(C[cur][order[j-1]]*V[order[j-1]][col] if j else zero)
    assert sum(bool(a) for row in V for a in row)==p*(p-1)//2+1
    for X,Y in [(C,V),(V,C)]:
        assert all(sum((X[i][k]*Y[k][j] for k in range(p)),zero)==(one if i==j else zero) for i in range(p) for j in range(p))
    # Each separately colored B_t has one charged column. CR=F verifies every slice,
    # but the full Gauss-scaled transfer is also multiplied in the literal matrices.
    twoinv=pow(2,-1,p);gamma=[zp[-twoinv*t*t%p] for t in range(p)]
    G=sum(gamma,zero);assert G
    B=[[R[u][t]*gamma[t] for t in range(p)] for u in range(p)]
    BA=[[sum((B[u][t]*F[t][v] for t in range(p)),zero) for v in range(p)] for u in range(p)]
    CBA=[[sum((C[i][u]*BA[u][v] for u in range(p)),zero) for v in range(p)] for i in range(p)]
    assert all(CBA[i][j]*zp[-twoinv*(i*i+j*j)%p]/G==F[i][j] for i in range(p) for j in range(p))
    columns=[sum(bool(R[u][t]) for u in range(p)) for t in range(p)]
    return {'p':p,'kind':kind,'order':order,'prefix_zero_locations':prefixes,'stabilizer_sizes':st,'nnz_C':nnzC,'nnz_C_inverse':p*(p-1)//2+1,'nnz_R':nnzR,'colored_column_counts':columns,'Z':predicted_Z,'edges':p*p+nnzC+nnzR,'literal_transfer':'passed','both_inverse_products':'passed','all_coefficients_nonzero':True}

small=[]
for p in [5,7,11,13,17]:
    for kind in ['center','hierarchy']:
        row=exact_control(p,kind);small.append(row)
        print(p,kind,row['Z'],row['edges'],flush=True)
        (OUT/'FRESH_AGGREGATE_EXACT_RESULTS.json').write_text(json.dumps(small,indent=2)+'\n')

bounded=[]
for p in list(s.primerange(5,128)):
    fs=factors(p-1)
    for f in [fs,list(reversed(fs))]:
        order=hierarchy_order(p,f);st=stabilizers(p,order)
        ds=[1]
        for q in f:ds.append(ds[-1]*q)
        expected=[max(d for d in ds if L%d==0) for L in range(1,p)]
        assert st==expected
        assert sum(v-1 for v in st)==expected_hierarchy(p,f)
    bounded.append({'p':p,'prime_factors':fs,'Z':expected_hierarchy(p,fs),'both_factor_orders_passed':True})
(OUT/'FRESH_AGGREGATE_STABILIZER_RESULTS.json').write_text(json.dumps(bounded,indent=2)+'\n')
print('All exact and bounded controls passed.',flush=True)
