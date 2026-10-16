"""Self-authored bounded controls. Never imports or runs supplied research code."""
from pathlib import Path
from math import comb
from itertools import product
from fractions import Fraction
import random, json, hashlib

ROOT = Path(__file__).resolve().parent
counts = {}
def check(ok, category):
    assert ok, category
    counts[category] = counts.get(category, 0) + 1

def blocks(N, B):
    q, r = divmod(N, B)
    lengths = [q + (b < r) for b in range(B)]
    s = 0
    for ell in lengths:
        yield s, ell
        s += ell

def summaries(N, B, a, beta, rows):
    """Direct signed reduction with i = zeta^(N/4)."""
    D = N // 2
    out = []
    for s, ell in blocks(N, B):
        c = [0] * D
        for t in range(ell):
            exponent = (a*t*(t-1)//2 + (a*s+beta)*t) % N
            for coeff, shift in ((rows[s+t][0],0),(rows[s+t][1],N//4)):
                q, j = divmod((exponent+shift) % N, D)
                c[j] += (-1 if q else 1)*coeff
        out.append(c)
    return out

def oracle_summaries(N, B, a, beta, rows):
    """Separate integer polynomial construction and long division."""
    D = N//2
    out = []
    for s, ell in blocks(N,B):
        p = [0] * (2*N)
        for t in range(ell):
            # Sum the stepwise chirp phase, instead of the closed formula.
            e = sum(a*(s+j)+beta for j in range(t)) % N
            re, im = rows[s+t]
            p[e] += re
            p[e+N//4] += im
        for k in range(len(p)-1,D-1,-1):
            p[k-D] -= p[k]
            p[k] = 0
        out.append(p[:D])
    return out

def det_bareiss(A):
    A = [r[:] for r in A]
    n = len(A); sign = 1; prev = 1
    for k in range(n-1):
        pivot = next((i for i in range(k,n) if A[i][k]), None)
        if pivot is None: return 0
        if pivot != k:
            A[pivot],A[k] = A[k],A[pivot]; sign = -sign
        v = A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = A[i][j]*v-A[i][k]*A[k][j]
                assert numerator % prev == 0
                A[i][j] = numerator//prev
            A[i][k] = 0
        prev = v
    return sign*A[-1][-1]

def norm_integer(c):
    D = len(c)
    matrix = [[0]*D for _ in range(D)]
    for j in range(D):
        for i, v in enumerate(c):
            q,k=divmod(i+j,D)
            matrix[k][j] += (-1 if q else 1)*v
    return det_bareiss(matrix)

def ceil_log2(n):
    assert n >= 1
    return (n-1).bit_length()

def plan(N,B,W,A,t=0):
    m=N.bit_length()-1; D=N//2
    H=min(comb(N+B-1,B), 1<<(N-B))
    C=64*H*B*(1<<B)*N*N
    c=ceil_log2(C); K=ceil_log2(A); G=W+(D-1)*K
    Pq=16*m+16; I=B+2*m+10
    p=max(W,c+t+1,c+Pq+G+2)
    return dict(N=N,B=B,W=W,A=A,t=t,H=H,C=C,c=c,K=K,G=G,
                Pq=Pq,I=I,p=p,width_bound=p+I,
                sufficient_wrapper_width=p+I<=65536)

def run():
    # Exhaustive small exact input algebra, with all valid states.
    N=4
    for flat in product((-1,0,1),repeat=8):
        rows=list(zip(flat[::2],flat[1::2]))
        for B in (3,4):
            for a in (1,3):
                for beta in range(4):
                    z=summaries(N,B,a,beta,rows)
                    check(z==oracle_summaries(N,B,a,beta,rows),'exhaustive_reduction')
    rng=random.Random(340016)
    for N in (8,16,32,64):
        for _ in range(100):
            B=rng.randrange(3,N+1);a=rng.randrange(N//2)*2+1;beta=rng.randrange(N)
            rows=[(rng.randrange(-17,18),rng.randrange(-17,18)) for j in range(N)]
            z=summaries(N,B,a,beta,rows)
            check(z==oracle_summaries(N,B,a,beta,rows),'larger_reduction')
            raw_bound=sum(abs(v) for r in rows for v in r)
            for c in z:
                check(sum(map(abs,c))<=raw_bound,'coefficient_l1_bound')
                if N<=32:
                    norm=norm_integer(c)
                    check((norm==0)==(not any(c)),'integer_norm_zero_equivalence')
                    if any(c): check(abs(norm)>=1,'integer_norm_separation')
    # All-zero and nonzero-input projected-zero are different facts.
    zero=[(0,0)]*64
    kernel=zero[:];kernel[0]=(1,0);kernel[1]=(-1,0)
    check(not any(v for c in summaries(64,3,1,0,zero) for v in c),'zero_input')
    check(any(v for r in kernel for v in r) and
          not any(v for c in summaries(64,3,1,0,kernel) for v in c),'nonzero_input_kernel')
    near=[]
    for k in (1,2,8,32,128,1000,65000):
        rows=zero[:];rows[0]=(1<<k,0);rows[1]=(-(1<<k)+1,0)
        z=summaries(64,3,1,0,rows)
        check(z[0]==[1]+[0]*31 and all(not any(c) for c in z[1:]),'near_kernel_exact')
        p=plan(64,3,k+1,1)
        check(p['K']==0 and p['G']==k+1,'near_kernel_width_paid')
        near.append({key:p[key] for key in ('N','B','W','K','G','p','width_bound','sufficient_wrapper_width')})
    # Exact symbolic planning inequalities, independent of producer outputs.
    params=[]
    for N in (4,8,16,32,64,128,256,512,1024,2048,4096):
        bs=range(3,N+1) if N<=64 else sorted({3,4,N//4,N//2,3*N//4,N-1,N})
        for B in bs:
            ell=(N+B-1)//B
            for W in (1,16,53,2098,65536):
                for A in (1,3,1<<(W+ceil_log2(2*ell))):
                    for t in (0,17,100):
                        z=plan(N,B,W,A,t)
                        p,C,Pq,G=z['p'],z['C'],z['Pq'],z['G']
                        check(p>=W,'exact_loading')
                        check(2*C<=(1<<(p-t)),'upstream_precision')
                        check(C<=(1<<(p-Pq-G-2)),'delta_signal_allowance')
                        # sqrt(N)*rho < 1, checked by squaring.
                        check(N<(1<<(2*Pq)),'sqrt_N_rho_guard')
                        check(z['c']>=0 and C<=(1<<z['c']),'ceil_constant')
                        check(z['width_bound']==p+B+2*(N.bit_length()-1)+10,'paid_width')
                        if A==1 and t==0 and W in (1,53):
                            params.append({key:z[key] for key in ('N','B','W','p','width_bound','sufficient_wrapper_width')})
    # Concrete semantic mutation controls. They are not wrapper replays.
    mutations={}
    mutations['projected_zero_mislabeled_as_zero_input']=any(v for row in kernel for v in row)
    # Neglecting i's shift would wrongly call 1+i*i = 0 nonzero.
    rows=[(0,0)]*8;rows[0]=(1,0);rows[1]=(0,1)
    correct=summaries(8,3,1,2,rows)
    mutations['missing_imaginary_exponent']=not any(correct[0])
    # zeta^(N/2) = -1 rather than +1.
    rows=[(0,0)]*8;rows[0]=(1,0);rows[1]=(1,0)
    correct=summaries(8,3,1,4,rows)
    mutations['wrong_cyclotomic_sign']=not any(correct[0])
    # Ignoring W gives a precision independent of exact near-kernel width.
    low=plan(64,3,2,1); high=plan(64,3,1001,1)
    mutations['ignoring_common_grid_width']=high['p']>low['p']
    # A failed width upper certificate does not certify actual overwidth.
    z=plan(4096,3,65536,1)
    mutations['cap_failure_not_actual_overwidth']=not z['sufficient_wrapper_width'] and (1).bit_length()<=65536
    for name, detected in mutations.items():check(detected,'mutation_'+name)
    return {'status':'PASS','scope':'Self-authored bounded exact algebra/planning only; no producer, wrapper, or downstream execution',
            'counts':counts,'near_kernel_plans':near,'selected_plans':params,'mutations':mutations,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    result=run()
    (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counts':counts,'mutations':result['mutations']},indent=2))
