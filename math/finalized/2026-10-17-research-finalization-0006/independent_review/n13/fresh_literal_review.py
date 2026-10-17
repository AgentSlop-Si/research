"""Fresh 17 Oct 2026 independent literal-bank check. Uses no previous code."""
from pathlib import Path
import json,hashlib,time
P,N,Q=53,13,16
ZERO,ONE=0,1

def add(x,y):
    a,b=x%P,x//P;c,d=y%P,y//P
    return (a+c)%P+P*((b+d)%P)
def neg(x):return (-x%P)+P*((-(x//P))%P)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    a,b=x%P,x//P;c,d=y%P,y//P
    return (a*c+2*b*d)%P+P*((a*d+b*c)%P)
def power(x,k):
    v=1
    while k:
        if k&1:v=mul(v,x)
        x=mul(x,x);k>>=1
    return v
def inv(x):
    assert x
    a,b=x%P,x//P;ni=pow((a*a-2*b*b)%P,-1,P)
    return (a*ni)%P+P*((-b*ni)%P)
def dot(a,b):
    t=0
    for x,y in zip(a,b):t=add(t,mul(x,y))
    return t
def encode(x):return [x%P,x//P]
def poly_eval(p,x):
    t=0
    for c in p[::-1]:t=add(mul(t,x),c)
    return t
def solve(A,b):
    a=[r[:]+[v] for r,v in zip(A,b)]; rows,cols=len(a),len(A[0]);piv=[];k=0
    for c in range(cols):
        hit=next((i for i in range(k,rows) if a[i][c]),None)
        if hit is None:continue
        a[k],a[hit]=a[hit],a[k];u=inv(a[k][c]);a[k]=[mul(u,x) for x in a[k]]
        for i in range(rows):
            if i!=k and a[i][c]:
                u=a[i][c];a[i]=[sub(x,mul(u,y)) for x,y in zip(a[i],a[k])]
        piv.append(c);k+=1
        if k==rows:break
    assert not any(not any(r[:cols]) and r[-1] for r in a)
    x=[0]*cols
    for i,c in enumerate(piv):x[c]=a[i][-1]
    assert [dot(r,x) for r in A]==b
    return x,len(piv)
def inverse(A):
    a=[r[:]+[int(i==j) for j in range(N)] for i,r in enumerate(A)]
    for c in range(N):
        hit=next(i for i in range(c,N) if a[i][c]);a[c],a[hit]=a[hit],a[c]
        u=inv(a[c][c]);a[c]=[mul(u,x) for x in a[c]]
        for i in range(N):
            if i!=c and a[i][c]:
                u=a[i][c];a[i]=[sub(x,mul(u,y)) for x,y in zip(a[i],a[c])]
    assert [r[:N] for r in a]==[[int(i==j) for j in range(N)] for i in range(N)]
    return [r[N:] for r in a]
def mm(A,B):
    bt=list(zip(*B));return [[dot(r,c) for c in bt] for r in A]
def matrices_sum(mats):
    out=[[0]*N for _ in range(N)]
    for mat in mats:
        for i in range(N):
            for j in range(N):out[i][j]=add(out[i][j],mat[i][j])
    return out
def mismatch(A,B):return sum(x!=y for a,b in zip(A,B) for x,y in zip(a,b))

def main():
    started=time.monotonic()
    assert all(P%d for d in range(2,8)) and pow(Q,N,P)==1 and Q!=1
    assert 2 not in {x*x%P for x in range(P)}
    assert all(mul(x,inv(x))==1 for x in range(1,P*P))
    # H/K are read only as inert, explicit candidate coefficient data.
    H=[36,25,12,17,34,9,51,1];K=[17,25,35,42,4,3,25,1]
    rootsH=[x for x in range(1,P*P) if poly_eval(H,x)==0]
    rootsK=[x for x in range(1,P*P) if poly_eval(K,x)==0]
    assert len(rootsH)==len(rootsK)==7
    banks=[(1,1,x) for x in rootsH]+[(-1,1,14),(1,-1,43)]+[(-1,-1,x) for x in rootsK]
    # G is independently generated from left multiplication in the Weyl algebra.
    G={}
    for e,d in [(1,1),(-1,1),(1,-1),(-1,-1)]:
        omega=pow(Q,(e*d)%N,P);D={(0,0):1}
        for total in range(1,N):
            for r in range(total+1):
                ell=total-r
                D[r,ell]=(D.get((r-1,ell),0)+pow(omega,r,P)*D.get((r,ell-1),0))%P
        for a in range(N):
            for b in range(N):G[e,d,a,b]=D.get(((e*a)%N,(d*b)%N),0)
    amplitudes=[[0]*N for _ in banks];ranks=[]
    for b in range(N):
        A=[[mul(G[e,d,a,b],power(x,(e*a)%N)) for e,d,x in banks] for a in range(N)]
        target=[pow(Q,(10*(a+b)**2)%N,P) for a in range(N)]
        values,rank=solve(A,target);ranks.append(rank)
        for i,v in enumerate(values):amplitudes[i][b]=v
    invN=pow(N,-1,P);gamma=sum(pow(Q,(-t*t)%N,P) for t in range(N))*invN%P
    assert gamma==7
    target=[[pow(Q,(-i*j)%N,P) for j in range(N)] for i in range(N)]
    identity=[[int(i==j) for j in range(N)] for i in range(N)]
    physical=[];witness=[];inverse_count=0;weyl_count=0;first_inverse=None
    for ix,((e,d,alpha),A) in enumerate(zip(banks,amplitudes)):
        Delta=neg(power(alpha,N));assert Delta and any(A)
        weights=[mul(mul(Delta,gamma),dot(A,[pow(Q,(-e*b*j)%N,P) for b in range(N)])) for j in range(N)]
        recovered=[mul(inv(mul(mul(N,Delta),gamma)),dot(weights,[pow(Q,(e*b*j)%N,P) for j in range(N)])) for b in range(N)]
        assert recovered==A
        bank=[[0]*N for _ in range(N)]
        for j,w in enumerate(weights):
            literal=[[0]*N for _ in range(N)]
            for t in range(N):
                literal[t][t]=(1-pow(Q,(e*d*j+d*t)%N,P))%P
                literal[(t+e)%N][t]=sub(literal[(t+e)%N][t],alpha)
            imat=inverse(literal);inverse_count+=1
            assert mm(literal,imat)==identity and mm(imat,literal)==identity
            if first_inverse is None:first_inverse=imat
            scale=mul(invN,w)
            for r in range(N):
                for t in range(N):bank[r][t]=add(bank[r][t],mul(scale,imat[r][t]))
        assert any(x for r in bank for x in r)
        for a in range(N):
            for b in range(N):
                extracted=mul(invN,dot([bank[(t+a)%N][t] for t in range(N)],[pow(Q,(-b*t)%N,P) for t in range(N)]))
                expected=mul(gamma,mul(mul(G[e,d,a,b],power(alpha,(e*a)%N)),A[b]))
                assert extracted==expected;weyl_count+=1
        physical.append(bank)
        witness.append({'epsilon':e,'delta':d,'alpha':encode(alpha),'beta':[1,0],'Delta':encode(Delta),'weights':[encode(w) for w in weights],'amplitudes':[encode(v) for v in A]})
    aggregate=matrices_sum(physical);assert aggregate==target
    controls={}
    controls['omit_normalization']=mismatch([[mul(N,x) for x in row] for row in aggregate],target)
    controls['opposite_Fourier_sign']=mismatch(aggregate,[[pow(Q,(i*j)%N,P) for j in range(N)] for i in range(N)])
    controls['change_first_weight']=mismatch([[add(aggregate[r][t],mul(invN,first_inverse[r][t])) for t in range(N)] for r in range(N)],target)
    controls['delete_each_bank']=[sum(bool(x) for row in B for x in row) for B in physical]
    assert all(controls[k]>0 for k in ['omit_normalization','opposite_Fourier_sign','change_first_weight']) and all(controls['delete_each_bank'])
    receipt={'verdict':'LITERAL_UPPER_ACCEPT','field':'F53[u]/(u^2-2)','encoding':'[a,b] means a+b*u','H':H,'K':K,'positive_roots':[encode(x) for x in rootsH],'negative_roots':[encode(x) for x in rootsK],'cross_y':[14,0],'cross_z':[43,0],'allocation':[7,1,1,7],'sector_ranks':ranks,'literal_inverses_checked':inverse_count,'two_sided_inverse_products_checked':2*inverse_count,'bank_Weyl_coefficients_checked':weyl_count,'aggregate_entries_checked':N*N,'all_nonzero_field_inverse_controls':P*P-1,'controls':controls,'elapsed_seconds':time.monotonic()-started,'scope':'Exact original bank identity on all K^13; lower16 and base-field exact18 are matching accepted dependencies, not replayed here; no speed result.'}
    out=Path(__file__).parent
    (out/'INDEPENDENT_WITNESS.json').write_text(json.dumps({'field_modulus':[51,0,1],'banks':witness},indent=2)+'\n')
    (out/'LITERAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
