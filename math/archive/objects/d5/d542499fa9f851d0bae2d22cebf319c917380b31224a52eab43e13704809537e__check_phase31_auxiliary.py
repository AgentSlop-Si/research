"""Independent q6/q7 controls and five-term cyclic-executor checks."""
from pathlib import Path
from itertools import combinations,combinations_with_replacement,permutations
import json,random,struct
ROOT=Path(__file__).resolve().parent;P=998244353
def load(n):
    raw=(ROOT/f'REBUILT_INPUT_N{n}.bin').read_bytes();v=struct.unpack('<'+'I'*(len(raw)//4),raw);assert v[:2]==(P,n)
    mats=[[list(v[2+h*n*n+i*n:2+h*n*n+(i+1)*n])for i in range(n)]for h in range(6)]
    return mats[0],mats[1:]
def extra(n,seed,den):
    rng=random.Random(seed);order=list(range(n));rng.shuffle(order);pos={x:i for i,x in enumerate(order)}
    left=[rng.randrange(n)for i in range(n)];right=[rng.randrange(n)for i in range(n)]
    w=pow(3,-((P-1)//n),P);a=pow(den,-1,P);b=pow(1-pow(a,n,P),-1,P)
    return [[pow(w,left[i]+right[j],P)*pow(a,(pos[i]-pos[j])%n,P)*b%P for j in range(n)]for i in range(n)]
def rank(M):
    n=len(M[0]);basis={}
    for old in M:
        v=old.copy()
        for col in sorted(basis):
            if v[col]:
                t=v[col];row=basis[col]
                v[col:]=[(x-t*y)%P for x,y in zip(v[col:],row[col:])]
        col=next((j for j,x in enumerate(v)if x),None)
        if col is not None:
            inv=pow(v[col],-1,P);basis[col]=[x*inv%P for x in v]
            if len(basis)==n:return n
    return len(basis)
def macaulay(T,G,rs,cs):
    q=len(G);pairs=list(combinations_with_replacement(range(q),2));triples=list(combinations_with_replacement(range(q),3));index={v:i for i,v in enumerate(triples)}
    ans=[]
    for i,h in combinations(range(len(rs)),2):
        for j,l in combinations(range(len(cs)),2):
            x=T[i][l]*T[h][j]%P;y=T[i][j]*T[h][l]%P;co=[]
            for a,b in pairs:
                u=G[a][rs[i]][cs[j]]*G[b][rs[h]][cs[l]];v=G[a][rs[i]][cs[l]]*G[b][rs[h]][cs[j]]
                if a!=b:u+=G[b][rs[i]][cs[j]]*G[a][rs[h]][cs[l]];v+=G[b][rs[i]][cs[l]]*G[a][rs[h]][cs[j]]
                co.append((x*u-y*v)%P)
            for var in range(q):
                row=[0]*len(triples)
                for pair,z in zip(pairs,co):row[index[tuple(sorted(pair+(var,)))]]=z
                ans.append(row)
    return ans
results=[]
for n in [4,8,16]:
    T,G=load(n);seed=2800+n;G6=G+[extra(n,seed*7+29,17)]
    if n==4:mappings=((rs,cs)for rs in permutations(range(n),3)for cs in permutations(range(n),4))
    else:
        rng=random.Random(619000+n);mappings=[(rng.sample(range(n),3),rng.sample(range(n),4))for j in range(24)]
    hist={}
    for rs,cs in mappings:
        r=rank(macaulay(T,G6,rs,cs));assert r==56;hist[r]=hist.get(r,0)+1
    results.append({'q':6,'N':n,'exhaustive':n==4,'histogram':hist});print('q6',n,hist,flush=True)
    if n>4:
        G7=G6+[extra(n,seed*7+31,19)];rng=random.Random(3300+n);hist={}
        for z in range(3):
            rs=rng.sample(range(n),3);cs=rng.sample(range(n),5);r=rank(macaulay(T,G7,rs,cs));assert r==84;hist[r]=hist.get(r,0)+1
        results.append({'q':7,'N':n,'exhaustive':False,'histogram':hist});print('q7',n,hist,flush=True)

executors=[]
for spec in json.loads((ROOT/'PRIOR_REVIEW_FAMILY_SPECIFICATIONS.json').read_text()):
    if spec['p']!=P:continue
    n=spec['n'];_,G=load(n);w=spec['root'];components=spec['B']+spec['G3']+spec['G4_custom_control'];coeff=[1,2,3,4,5]
    for trial in range(n+2):
        x=[int(j==trial)for j in range(n)]if trial<n else[(j+1)**(trial-n+1)%P for j in range(n)]
        answer=[0]*n
        for h,item in enumerate(components):
            order=item['order'];a=pow(item['coupling_denominator'],-1,P);inv=pow(1-pow(a,n,P),-1,P)
            y=[x[j]*pow(w,item['right_exponents'][j],P)%P for j in range(n)]
            tail=y[order[1]]
            for j in range(2,n):tail=(y[order[j]]+a*tail)%P
            z=[0]*n;z[order[0]]=(y[order[0]]+a*tail)*inv%P
            for j in range(1,n):z[order[j]]=(y[order[j]]+a*z[order[j-1]])%P
            answer=[(answer[j]+coeff[h]*pow(w,item['left_exponents'][j],P)*z[j])%P for j in range(n)]
        expected=[sum(coeff[h]*G[h][i][j]*x[j]for h in range(5)for j in range(n))%P for i in range(n)]
        assert answer==expected
    executors.append({'N':n,'basis_and_extra_vectors':n+2,'all_match_dense':True,'scope':'Linear-work candidate middle pencil, not Fourier identity.'})
(ROOT/'PHASE31_AUXILIARY_REVIEW.json').write_text(json.dumps({'passed':True,'controls':results,'executors':executors,'uploaded_code_executed':False},indent=2)+'\n')
