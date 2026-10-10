"""Independent controls authored from cyclotomic and character definitions.
No supplied program is loaded, executed, imported, compiled, or AST-parsed.
Supplied JSON witness vectors are data only. Standard-library implementation.
"""
from pathlib import Path
from itertools import product
from math import gcd, lcm, prod
from functools import lru_cache
from fractions import Fraction
import hashlib, json, time

HERE = Path(__file__).resolve().parent
PRIMES = [998244353, 1000000007]

def trim(a):
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def quotient(a,b):
    a=a[:]; q=[0]*max(1,(len(a)-len(b)+1))
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b); assert a[-1] % b[-1] == 0
        t=a[-1]//b[-1]; q[k]=t
        for j,v in enumerate(b): a[j+k]-=t*v
        trim(a)
    assert a==[0]
    return trim(q)

@lru_cache(None)
def phi(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0: a=quotient(a,list(phi(d)))
    return tuple(a)

@lru_cache(None)
def roots(n):
    p=phi(n); d=len(p)-1; v=[1]+[0]*(d-1); result=[]
    for k in range(n):
        result.append(tuple(v)); high=v[-1]
        v=[0]+v[:-1]
        for j in range(d): v[j]-=high*p[j]
    assert tuple(v)==result[0]
    return tuple(result)

def data(factors):
    m=lcm(*factors); points=list(product(*(range(n) for n in factors)))
    exps=[[sum(a*b*(m//n) for a,b,n in zip(x,y,factors))%m for y in points] for x in points]
    units=[u for u in range(m) if gcd(u,m)==1]
    if m==1: units=[0]
    seen=set(); orbits=[]
    for x in points:
        if x in seen: continue
        orbit={tuple((u*a)%n for a,n in zip(x,factors)) for u in units}
        seen |= orbit; orbits.append(sorted(points.index(y) for y in orbit))
    return m,points,exps,orbits

def trace_coeffs(m):
    R=roots(m); d=len(R[0]); units=[u for u in range(m) if gcd(u,m)==1]
    if m==1: units=[0]
    out=[]
    for k in range(d):
        z=[sum(R[(k*u)%m][j] for u in units) for j in range(d)]
        assert all(t==0 for t in z[1:]);out.append(z[0])
    return out

def project(m,exps,coeffs):
    vals=[sum(a*b for a,b in zip(coeffs,r)) for r in roots(m)]
    return [[vals[e] for e in row] for row in exps]

def rank_mod(A,p):
    B=[[x%p for x in row] for row in A]; nr=len(B); nc=len(B[0]) if B else 0
    labels=list(range(nr)); rr=[];cc=[];rank=0
    for c in range(nc):
        pivot=next((j for j in range(rank,nr) if B[j][c]),None)
        if pivot is None: continue
        B[rank],B[pivot]=B[pivot],B[rank];labels[rank],labels[pivot]=labels[pivot],labels[rank]
        rr.append(labels[rank]);cc.append(c)
        inv=pow(B[rank][c],-1,p); prow=B[rank]
        for j in range(rank+1,nr):
            if B[j][c]:
                f=B[j][c]*inv%p; row=B[j]
                for k in range(c+1,nc): row[k]=(row[k]-f*prow[k])%p
                row[c]=0
        rank+=1
        if rank==nr: break
    # Independently recompute the selected square minor in original row order.
    minor=[[A[i][j]%p for j in cc] for i in rr];det=1
    for k in range(rank):
        j=next(j for j in range(k,rank) if minor[j][k])
        if j!=k: minor[k],minor[j]=minor[j],minor[k];det=-det
        pivot=minor[k][k];det=det*pivot%p; inv=pow(pivot,-1,p)
        for j in range(k+1,rank):
            f=minor[j][k]*inv%p
            for c in range(k+1,rank):minor[j][c]=(minor[j][c]-f*minor[k][c])%p
            minor[j][k]=0
    assert det%p!=0
    return {'prime':p,'rank':rank,'pivot_rows':rr,'pivot_columns':cc,'minor_determinant':det%p}

def rank_exact(A):
    B=[[Fraction(x) for x in row] for row in A];rank=0
    for c in range(len(B[0]) if B else 0):
        j=next((j for j in range(rank,len(B)) if B[j][c]),None)
        if j is None:continue
        B[rank],B[j]=B[j],B[rank]
        for j in range(rank+1,len(B)):
            if B[j][c]:
                t=B[j][c]/B[rank][c]
                for k in range(c,len(B[0])):B[j][k]-=t*B[rank][k]
        rank+=1
        if rank==len(B):break
    return rank

def run_group(factors):
    m,points,exps,orbits=data(factors);N=len(points);d=len(phi(m))-1
    record={'factors':factors,'N':N,'exponent':m,'cyclotomic_degree':d,'cyclic_subgroups':len(orbits),'modes':{}}
    for mode,target in [('trace',len(orbits)),('traceless',N-len(orbits)),('unrestricted',N)]:
        for t in range(1,N+3):
            coeffs=trace_coeffs(m) if mode=='trace' else [t**j for j in range(d)]
            if mode=='traceless':coeffs[0]=0
            M=project(m,exps,coeffs); witnesses=[rank_mod(M,p) for p in PRIMES]
            if all(w['rank']==target for w in witnesses):break
            if mode=='trace': raise AssertionError('trace mismatch')
        else:raise AssertionError('fresh generic witness search exhausted')
        if mode=='traceless':
            assert all(sum(row[j] for j in orb)==0 for row in M for orb in orbits)
        result={'basis_functional':coeffs,'target_rank':target,'matrix_sha256':hashlib.sha256(json.dumps(M,separators=(',',':')).encode()).hexdigest(),'certificates':witnesses}
        if N<=16:
            result['rank_over_Q_exact']=rank_exact(M);assert result['rank_over_Q_exact']==target
        record['modes'][mode]=result
    return record

def main():
    start=time.time(); source=json.loads((HERE/'source_text/RANK_CERTIFICATES.json').read_text())
    abelian=json.loads((HERE/'source_text/ABELIAN_RANK_CERTIFICATES.json').read_text())
    cases=[[r['n']] for r in source['results']]+[r['group_factors'] for r in abelian['results']]
    results=[]
    for factors in cases:
        result=run_group(factors);results.append(result)
        print('fresh',factors,result['N'],result['cyclic_subgroups'],flush=True)
    source_checks=[]
    for row in source['results']:
        n=row['n'];m,pts,exp,orb=data([n])
        for mode in ['traceless','unrestricted']:
            coeff=row['witnesses'][mode]['basis_functional'];M=project(m,exp,coeff)
            expected=row['witnesses'][mode]['rank_mod_p'];got=[rank_mod(M,p) for p in PRIMES]
            assert all(w['rank']==expected for w in got)
            source_checks.append({'n':n,'mode':mode,'rank':expected,'certificates':got})
    # Nonzero exceptional functional, composition cancellation, tensor mismatch.
    m,pts,exp,orb=data([5]);M=project(m,exp,[0,1,0,0]);assert rank_exact(M)==2
    degeneracies={'nonzero_exceptional_L_C5':{'basis_functional':[0,1,0,0],'rank_Q':2,'generic_rank':3},'C3_tensor_C3':{'individual_generic_rank':1,'product_of_ranks':1,'tensor_generic_rank':4,'cyclic_subgroups':5},'C2_fourth_tensor':{'N':16,'generic_traceless_rank':0},'F4_squared':{'exact_product':'4 times inversion permutation','product_projection_rank':0,'factor_projection_rank':1},'unitary_F2':{'base_field':'Q','generic_traceless_rank':2,'unnormalized_rank':0}}
    twiddles=[]
    for t in range(9):
        h=2**t;g=8*h;nonrat=sum(1 for u in range(8) for q in range(h) if (2*u*q)%g!=0)
        assert nonrat==7*(h-1);twiddles.append({'h':h,'nonrational_entries':nonrat,'fifteen_copies':15*nonrat})
    report={'status':'PASS','fresh_group_cases':len(results),'fresh_projected_matrices':3*len(results),'fresh_modular_rank_certificates':6*len(results),'reconstructed_supplied_cyclic_witnesses':len(source_checks),'primes':PRIMES,'fresh_results':results,'source_witness_rechecks':source_checks,'degeneracies':degeneracies,'twiddle_counts':twiddles,'runtime_seconds':time.time()-start,'scope':'Controls corroborate proved rank statements; not program equivalence or runtime claims.'}
    (HERE/'FRESH_RANK_RESULTS.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['fresh_results','source_witness_rechecks']},indent=2))

if __name__=='__main__':main()
