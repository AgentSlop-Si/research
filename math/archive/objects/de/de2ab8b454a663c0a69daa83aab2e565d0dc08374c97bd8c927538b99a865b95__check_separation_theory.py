"""Independent paired-order weighted-Green separation controls.
The all-N norm theorem is proved analytically in the review, not inferred
from these modular computations. No uploaded program is executed.
"""
from pathlib import Path
import random,itertools,json
ROOT=Path(__file__).resolve().parent;P=998244353
SRC=ROOT/'separation_theory/FFT_SEPARATION_RANK_THEORY'
expected=json.loads((SRC/'VERIFY_RESULTS.json').read_text())
def rank(A):
    if not A:return 0
    A=[row.copy()for row in A];row=0
    for col in range(len(A[0])):
        pivot=next((i for i in range(row,len(A))if A[i][col]),None)
        if pivot is None:continue
        A[row],A[pivot]=A[pivot],A[row];inv=pow(A[row][col],-1,P)
        for i in range(row+1,len(A)):
            q=A[i][col]*inv%P
            A[i][col:]=[(x-q*y)%P for x,y in zip(A[i][col:],A[row][col:])]
        row+=1
        if row==len(A):break
    return row
def pos(order):
    out=[0]*len(order)
    for j,x in enumerate(order):out[x]=j
    return out
def branch(n,rng):
    cycle=list(range(n));rng.shuffle(cycle);at=pos(cycle)
    rr=list(range(n));cc=list(range(n));rng.shuffle(rr);rng.shuffle(cc)
    weights=[rng.randint(2,1000000)for j in range(n)]
    def prefixes():
        out=[1]
        for j in cycle:out.append(out[-1]*weights[j]%P)
        return out
    pref=prefixes()
    while pref[-1]==1:weights[cycle[-1]]=rng.randint(2,1000000);pref=prefixes()
    left=[rng.randint(1,1000000)for j in range(n)];right=[rng.randint(1,1000000)for j in range(n)]
    return {'n':n,'cycle':cycle,'row':[at[x]for x in rr],'col':[at[x]for x in cc],'pref':pref,'inverse_pref':[pow(x,-1,P)for x in pref[:-1]],'den_inverse':pow(1-pref[-1],-1,P),'left':left,'right':right,'weights':weights}
def half(R,C,r,c):
    m=len(R)//2
    if not m:return [],[],'empty'
    rr=sorted(R,key=r.__getitem__);cc=sorted(C,key=c.__getitem__)
    if r[rr[m-1]]<c[cc[-m]]:return rr[:m],cc[-m:],'row-before-col'
    assert c[cc[m-1]]<r[rr[-m]]
    return rr[-m:],cc[:m],'col-before-row'
def entry(b,i,j):
    a,d=b['row'][i],b['col'][j]
    value=b['pref'][d]*b['inverse_pref'][a]%P
    if a>d:value=value*b['pref'][-1]%P
    return value*b['den_inverse']*b['left'][i]*b['right'][j]%P
def direct_arc(b,i,j):
    a,d=b['row'][i],b['col'][j];value=1
    while a!=d:value=value*b['weights'][b['cycle'][a]]%P;a=(a+1)%b['n']
    return value*b['den_inverse']*b['left'][i]*b['right'][j]%P

rng=random.Random(20261010);records=[];direct_count=0
for n in [16,32,64,128,256]:
    for q in [1,2,3,4,5]:
        m=n//2**q
        if m<2:continue
        for trial in range(4 if n<128 else 10):
            bank=[branch(n,rng)for z in range(q)];R=C=list(range(n));orient=[]
            for b in bank:R,C,o=half(R,C,b['row'],b['col']);orient.append(o)
            assert len(R)==len(C)==m
            matrices=[]
            for b in bank:
                assert max(b['row'][i]for i in R)<min(b['col'][j]for j in C)or max(b['col'][j]for j in C)<min(b['row'][i]for i in R)
                assert entry(b,R[0],C[-1])==direct_arc(b,R[0],C[-1]);direct_count+=1
                matrices.append([[entry(b,i,j)for j in C]for i in R])
            ranks=[rank(M)for M in matrices];assert max(ranks)<=1
            total=[[sum(M[i][j]for M in matrices)%P for j in range(m)]for i in range(m)];rnk=rank(total);assert rnk<=q
            root=pow(3,(P-1)//n,P);frank=rank([[pow(root,i*j,P)for j in C]for i in R])
            records.append({'n':n,'q':q,'m':m,'orientations':orient,'branch_ranks':ranks,'sum_rank':rnk,'fourier_sub_rank':frank})
assert records==expected['tests']

zero=[]
for trial in range(30):
    n=rng.choice([16,32,64]);cyc=list(range(n));rng.shuffle(cyc);rr=list(range(n));cc=list(range(n));rng.shuffle(rr);rng.shuffle(cc);at=pos(cyc)
    rp=[at[x]for x in rr];cp=[at[x]for x in cc]
    weights=[0 if rng.random()<.2 else rng.randrange(1,10000)for j in range(n)];weights[cyc[rng.randrange(n)]]=0
    R,C,o=half(list(range(n)),list(range(n)),rp,cp)
    def value(i,j):
        a,d=rp[i],cp[j];z=1
        while a!=d:z=z*weights[cyc[a]]%P;a=(a+1)%n
        return z
    r=rank([[value(i,j)for j in C]for i in R]);assert r<=1
    zero.append({'N':n,'rank':r})

shared=[]
for trial in range(20):
    n=64;first=branch(n,rng);bank=[first]
    for z in range(3):
        b=branch(n,rng);b['cycle']=first['cycle'];b['row']=first['row'];b['col']=first['col'];weights=[rng.randint(1,100000)for j in range(n)];pref=[1]
        for j in b['cycle']:pref.append(pref[-1]*weights[j]%P)
        assert pref[-1]!=1;b['weights']=weights;b['pref']=pref;b['inverse_pref']=[pow(x,-1,P)for x in pref[:-1]];b['den_inverse']=pow(1-pref[-1],-1,P);bank.append(b)
    R,C,o=half(list(range(n)),list(range(n)),first['row'],first['col']);assert len(R)==32
    r=rank([[sum(entry(b,i,j)for b in bank)%P for j in C]for i in R]);assert r<=4;shared.append(r)

cyclotomic=[]
for n,q in [(5,1),(13,2),(37,3),(83,4)]:
    for trial in range(12):
        bank=[branch(n,rng)for j in range(q)];R=C=list(range(n))
        for b in bank:R,C,o=half(R,C,b['row'],b['col'])
        assert len(R)==len(C)==n//2**q
        R=R[:q+1];C=C[:q+1];coeff=[0]*n
        for perm in itertools.permutations(range(q+1)):
            sign=(-1)**sum(perm[i]>perm[j]for i in range(q+1)for j in range(i+1,q+1))
            coeff[sum(R[i]*C[perm[i]]for i in range(q+1))%n]+=sign
        assert len(set(coeff))!=1
        cyclotomic.append({'prime_length':n,'branch_count':q,'rows':R,'columns':C,'cyclotomic_remainder_coefficients':coeff,'nonzero_over_C':True})
out={'passed':True,'uploaded_code_executed':False,'all_148_stored_rank_records_match':True,'rank_records':records,'direct_weighted_arc_spot_checks':direct_count,'zero_edge_trials':zero,'shared_order_ranks':shared,'exact_complex_cyclotomic_checks':cyclotomic,'scope':'The general exact/approximate all-length theorem is the analytic separation-and-norm proof. Finite-field ranks do not substitute for it.'}
(ROOT/'SEPARATION_THEORY_INDEPENDENT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print('Separation theory:',len(records),'stored records match; 30 zero-edge, 20 shared-order, and 48 exact complex cyclotomic controls pass.')
