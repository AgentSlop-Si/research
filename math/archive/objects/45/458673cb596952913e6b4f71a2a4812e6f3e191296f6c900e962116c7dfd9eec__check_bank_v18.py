"""Fresh independent Green-bank separation and modular certificate replay.
Reads source JSON results only; no uploaded Python is imported or executed.
"""
from pathlib import Path
from itertools import permutations
import random,json,math
import sympy as sy
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'bank_v18/fft_green_bank_separation_v18'
saved=json.loads((SRC/'results.json').read_text())

def separate(positions,universe=None):
    U=list(range(len(positions[0])))if universe is None else list(universe)
    U.sort(key=positions[0].__getitem__);m=len(U)//2;A=U[:m];B=U[-m:]if m else[]
    for order in positions[1:]:
        cut=set(sorted(A+B,key=order.__getitem__)[:len(A)])
        al=[x for x in A if x in cut];ah=[x for x in A if x not in cut]
        bl=[x for x in B if x in cut];bh=[x for x in B if x not in cut]
        assert len(al)==len(bh) and len(bl)==len(ah)
        A,B=(al,bh)if len(al)>=len(bl)else(bl,ah)
    assert len(A)==len(B) and not set(A)&set(B)
    assert len(A)>=len(U)//2**len(positions)
    signs=[]
    for order in positions:
        if A:
            assert max(order[x]for x in A)<min(order[x]for x in B)or max(order[x]for x in B)<min(order[x]for x in A)
            signs.append(1 if order[A[0]]<order[B[0]]else-1)
    return A,B,signs
def cycle(n,rng):
    order=list(range(n));rng.shuffle(order);start=order.index(0);order=order[start:]+order[:start]
    pos=[0]*n
    for i,v in enumerate(order):pos[v]=i
    return pos
def elimination(A,p):
    A=[row.copy()for row in A];m=len(A);n=len(A[0]);row=0;det=1
    for col in range(n):
        pivot=next((i for i in range(row,m)if A[i][col]),None)
        if pivot is None:continue
        if pivot!=row:A[row],A[pivot]=A[pivot],A[row];det=-det%p
        lead=A[row][col];det=det*lead%p;inv=pow(lead,-1,p)
        for i in range(row+1,m):
            v=A[i][col]*inv%p
            for j in range(col,n):A[i][j]=(A[i][j]-v*A[row][j])%p
        row+=1
        if row==m:break
    return row,det if m==n and row==n else 0
def root(p,n):
    factors=list(sy.factorint(p-1))
    g=next(g for g in range(2,p)if all(pow(g,(p-1)//q,p)!=1 for q in factors))
    z=pow(g,(p-1)//n,p);assert pow(z,n,p)==1 and z!=1
    return z

certs=[]
for old in saved['exact_hamiltonian_certificates']:
    n,t,p=old['n'],old['t'],old['field_modulus'];assert sy.isprime(n)and sy.isprime(p)and(p-1)%n==0
    rng=random.Random(1800+1009*t+n)
    orders=[cycle(n,rng)for j in range(t)];A,B,signs=separate(orders);size=len(A)
    total=[[0]*size for i in range(size)];ranks=[]
    for pos in orders:
        while True:
            alpha=rng.randrange(0,p)
            if pow(alpha,n,p)!=1:break
        left=[rng.randrange(1,p)for i in range(n)];right=[rng.randrange(1,p)for j in range(n)]
        inv=pow(1-pow(alpha,n,p),-1,p)
        block=[[left[i]*right[j]*pow(alpha,(pos[i]-pos[j])%n,p)*inv%p for j in B]for i in A]
        rk,_=elimination(block,p);assert rk<=1;ranks.append(rk)
        total=[[(x+y)%p for x,y in zip(ar,br)]for ar,br in zip(total,block)]
    omega=root(p,n);fourier=[[pow(omega,i*j,p)for j in B]for i in A]
    bankrank,_=elimination(total,p);frank,fdet=elimination(fourier,p)
    actual={'n':n,'t':t,'field_modulus':p,'separated_size':size,'term_ranks':ranks,'sum_rank':bankrank,'fourier_rank':frank,'fourier_det':fdet,'orientations':signs,'threshold':2**t*(t+1)}
    assert actual==old,(actual,old)
    assert bankrank<=t<size==frank and fdet
    certs.append(actual)

hist={}
for perm in permutations(range(8)):
    pos=[0]*8
    for i,x in enumerate(perm):pos[x]=i
    A,B,_=separate([list(range(8)),pos]);hist[len(A)]=hist.get(len(A),0)+1
assert sum(hist.values())==40320 and min(hist)==2
assert {str(k):v for k,v in hist.items()}==saved['exhaustive_two_order']['histogram']

bounded=[]
for old in saved['bounded_cycle_certificates']:
    n,t,count=old['n'],old['t'],old['cycles_each'];rng=random.Random(2818+n+31*t+101*count)
    metadata=[]
    for z in range(t):
        shuffled=list(range(n));rng.shuffle(shuffled);cuts=sorted(rng.sample(range(1,n),count-1));bounds=[0]+cuts+[n]
        parts=[shuffled[bounds[j]:bounds[j+1]]for j in range(count)];parts.sort(key=min)
        cid=[0]*n;pos=[0]*n
        for label,part in enumerate(parts):
            r=part.index(min(part));part=part[r:]+part[:r]
            for j,v in enumerate(part):cid[v]=label;pos[v]=j
        metadata.append((cid,pos))
    cells={}
    for x in range(n):cells.setdefault(tuple(cid[x]for cid,pos in metadata),[]).append(x)
    cell=max(cells.values(),key=lambda v:(len(v),[-x for x in v]));A,B,signs=separate([pos for cid,pos in metadata],cell)
    actual={'n':n,'t':t,'cycles_each':count,'cycle_product_bound':count**t,'largest_common_cycle_cell':len(cell),'separated_size':len(A),'guaranteed_floor':n//(2**t*count**t),'orientations':signs}
    assert actual==old
    bounded.append(actual)

out={'passed':True,'uploaded_code_executed':False,'hamiltonian_certificates_reproduced':certs,'exhaustive_two_order':{'count':40320,'minimum':2,'histogram':hist},'bounded_cycle_controls_reproduced':bounded,'proof_scope':'All-prime complex theorem uses prime Fourier full-spark, not a finite-field extrapolation. The theorem is for sums of resolvents, not products.','required_bounded_cycle_guards':'Prime Fourier length and every individual cycle denominator 1-alpha^L nonzero.'}
(ROOT/'BANK_V18_INDEPENDENT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print('Bank-v18: all seven exact certificates, all 40320 two-order tests, and three bounded-cycle controls reproduced.')
