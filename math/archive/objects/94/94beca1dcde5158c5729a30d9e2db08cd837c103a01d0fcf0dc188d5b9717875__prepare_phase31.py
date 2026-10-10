"""Reconstruct Phase31 from previously sealed explicit cycle/gauge data.
No uploaded program is imported. The fifth component was independently
specified during the earlier Phase30 five-generator dimension controls.
"""
from pathlib import Path
import json,hashlib,struct,random,itertools
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'phase31/fft_green_phase31_rectangular'
SPECS=ROOT/'PRIOR_REVIEW_FAMILY_SPECIFICATIONS.json'
P=998244353
def mm(A,B):return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*B)]for row in A]
def inv(A):
    n=len(A);M=[[v%P for v in row]+[int(i==j)for j in range(n)]for i,row in enumerate(A)]
    for j in range(n):
        k=next(i for i in range(j,n)if M[i][j]);M[j],M[k]=M[k],M[j]
        v=pow(M[j][j],-1,P);M[j]=[x*v%P for x in M[j]]
        for i in range(n):
            if i!=j:
                v=M[i][j];M[i]=[(x-v*y)%P for x,y in zip(M[i],M[j])]
    return [row[n:]for row in M]
def component(spec,n,w):
    order=spec['order'];assert sorted(order)==list(range(n))
    pos={v:k for k,v in enumerate(order)};alpha=pow(spec['coupling_denominator'],-1,P)
    den=(1-pow(alpha,n,P))%P;assert den
    return [[pow(w,spec['left_exponents'][i]+spec['right_exponents'][j],P)*pow(alpha,(pos[i]-pos[j])%n,P)*pow(den,-1,P)%P for j in range(n)]for i in range(n)]
def decode(path):
    z=struct.unpack('<'+'I'*(path.stat().st_size//4),path.read_bytes());p,n=z[:2];assert p==P and len(z)==2+6*n*n
    return n,[[list(z[2+h*n*n+i*n:2+h*n*n+(i+1)*n])for i in range(n)]for h in range(6)]
records=[]
for spec in json.loads(SPECS.read_text()):
    if spec['p']!=P:continue
    n=spec['n'];w=spec['root'];assert pow(w,n,P)==1 and pow(w,n//2,P)!=1
    A0,A1=[component(x,n,w)for x in spec['A']]
    C0,C1=[component(x,n,w)for x in spec['C']]
    coeff=3*pow(2,-1,P)%P
    A=[[(A0[i][j]+coeff*A1[i][j])%P for j in range(n)]for i in range(n)]
    C=[[(C0[i][j]+coeff*C1[i][j])%P for j in range(n)]for i in range(n)]
    F=[[pow(w,i*j,P)for j in range(n)]for i in range(n)]
    T=mm(mm(inv(A),F),inv(C));assert all(x for row in T for x in row)
    G=[component(x,n,w)for x in spec['B']+spec['G3']+spec['G4_custom_control']]
    expected=[T]+G;nn,stored=decode(SRC/f'certificates/input_N{n}.bin');assert nn==n and stored==expected
    out=ROOT/f'REBUILT_INPUT_N{n}.bin';out.write_bytes(struct.pack('<II',P,n)+b''.join(struct.pack('<'+'I'*(n*n),*(x for row in M for x in row))for M in expected))
    records.append({'N':n,'all_six_matrices_reconstructed':True,'target_nonzero_and_outers_invertible':True,'input_bytes_match':out.read_bytes()==(SRC/f'certificates/input_N{n}.bin').read_bytes(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
    if n==8:
        rng=random.Random(310031+n);rs=list(range(n));cs=list(range(n));rng.shuffle(rs);rng.shuffle(cs)
        L=[rng.randrange(1,P)for _ in range(n)];R=[rng.randrange(1,P)for _ in range(n)]
        B=[[sum((h+1)*G[h][i][j]for h in range(5))%P for j in range(n)]for i in range(n)]
        target=[[L[i]*B[rs[i]][cs[j]]*R[j]%P for j in range(n)]for i in range(n)]
        _,saved=decode(SRC/'certificates/input_planted_N8.bin');assert saved==[target]+G
        rowlist=list(itertools.permutations(range(n),3));collist=list(itertools.permutations(range(n),4))
        case=rowlist.index(tuple(rs[:3]))*len(collist)+collist.index(tuple(cs[:4]));assert case==9682
        (ROOT/'PLANTED_CASE_ID.bin').write_bytes(struct.pack('<Q',case))
        records.append({'planted_N':n,'all_entries_reconstructed':True,'case_id':case,'coefficients':[1,2,3,4,5]})
ids=(SRC/'certificates/indices_N16_100000.bin').read_bytes();values=list(struct.unpack('<'+'Q'*(len(ids)//8),ids))
expected=random.Random(310031).sample(range(146764800),100000)
assert values==expected and len(set(values))==100000
records.append({'N16_sample_count':len(values),'distinct':True,'seed_sequence_matched':True,'exhaustive':False})
(ROOT/'PHASE31_PREPARATION_REVIEW.json').write_text(json.dumps(records,indent=2)+'\n')
print('All Phase31 matrices, planted instance, and sampled case IDs independently reconstructed.')
