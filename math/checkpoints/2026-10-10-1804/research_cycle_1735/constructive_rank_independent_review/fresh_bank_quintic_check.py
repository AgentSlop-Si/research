"""Fresh independent N=11 recurrence obstruction; no author code imports."""
import json
from pathlib import Path
P=23; N=11; Q=2

def inv(x):
    assert x%P
    return pow(x%P,P-2,P)
def gb(n,k,q):
    # Pascal construction, avoiding product quotients.
    if k<0 or k>n:return 0
    row=[1]
    for r in range(1,n+1):
        row=[1]+[(row[j-1]+pow(q,j,P)*row[j])%P for j in range(1,r)]+[1]
    return row[k]
def G(e,d,a,b):
    r=(e*a)%N;l=(d*b)%N
    return gb(r+l,l,pow(Q,(e*d)%N,P)) if r+l<N else 0

def det(A):
    A=[r[:] for r in A];out=1
    for j in range(len(A)):
        k=next((k for k in range(j,len(A)) if A[k][j]),None)
        if k is None:return 0
        if k!=j:A[k],A[j]=A[j],A[k];out=-out
        pivot=A[j][j];out=out*pivot%P
        for k in range(j+1,len(A)):
            fac=A[k][j]*inv(pivot)%P
            A[k]=[(a-fac*b)%P for a,b in zip(A[k],A[j])]
    return out%P
assert pow(Q,N,P)==1 and Q!=1
h=pow(4,-1,N)
rows=[]; sequences={};denominators=[]
for b in [1,2]:
    denom=G(-1,1,N-b,b);denominators.append(denom)
    T=inv(denom)
    seq=[]
    for a in range(b,N-b):
        denominator=G(1,1,a,b);denominators.append(denominator)
        f=pow(Q,(h*(a+b)**2)%N,P)
        seq.append((f-T*G(-1,1,a,b))*inv(denominator)%P)
    sequences[b]=seq
    for j in range(len(seq)-5):rows.append(seq[j:j+6])
assert len(rows)==6 and all(len(r)==6 for r in rows)
D=det(rows);assert D
out={'N':N,'modulus':P,'primitive_root':Q,'moment_sequences':sequences,'matrix':rows,'determinant':D,'all_required_denominators_nonzero':all(denominators),'denominators':denominators,'verdict':'No common degree-at-most-five annihilator for this fixed-singleton central-moment architecture.'}
Path(__file__).with_name('FRESH_BANK_QUINTIC_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
