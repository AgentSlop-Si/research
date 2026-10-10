"""Independent Phase25 checks. Never imports or executes submitted code."""
import hashlib
import json
from pathlib import Path
import random
import time
from fractions import Fraction
from frontier_solver import (factor, successor, two_run, four_track,
                             sparse_denominator, green_apply, TwistedInverse)

P = 998244353
ROOT = Path(__file__).resolve().parent

def cycles(p):
    seen = set(); sizes = []
    for i in range(len(p)):
        if i not in seen:
            j = i; count = 0
            while j not in seen:
                seen.add(j); count += 1; j = p[j]
            sizes.append(count)
    return sorted(sizes)

def compose(a,b): return [a[b[j]] for j in range(len(a))]
def invert(a):
    out=[0]*len(a)
    for j,i in enumerate(a): out[i]=j
    return out

def dense(rows, p):
    return [[row.get(j,0)%p for j in range(len(rows))] for row in rows]

def rank(a,p):
    a=[[x%p for x in row] for row in a]; n=len(a); m=len(a[0]) if n else 0; r=0
    for j in range(m):
        pivot=next((i for i in range(r,n) if a[i][j]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][j],-1,p)
        for i in range(r+1,n):
            c=a[i][j]*inv%p
            if c:
                for k in range(j,m): a[i][k]=(a[i][k]-c*a[r][k])%p
        r+=1
        if r==n: break
    return r

def determinant(a,p):
    a=[r[:] for r in a]; n=len(a); d=1
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]%p),None)
        if pivot is None: return 0
        if pivot!=j: a[j],a[pivot]=a[pivot],a[j]; d=-d
        v=a[j][j]%p; d=d*v%p; inv=pow(v,-1,p)
        for i in range(j+1,n):
            c=a[i][j]*inv%p
            for k in range(j,n): a[i][k]=(a[i][k]-c*a[j][k])%p
    return d%p

def first_zero_unpivoted(a,p):
    a=[r[:] for r in a]; n=len(a)
    for j in range(n):
        if not a[j][j]%p: return j
        inv=pow(a[j][j],-1,p)
        for i in range(j+1,n):
            c=a[i][j]*inv%p
            for k in range(j,n): a[i][k]=(a[i][k]-c*a[j][k])%p
    return None

def matmul(a,b,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]

def green_matrix(order,alpha,p):
    n=len(order); loc=invert(order); powers=[pow(alpha,t,p) for t in range(n)]
    den=pow((1-pow(alpha,n,p))%p,-1,p)
    return [[powers[(loc[i]-loc[j])%n]*den%p for j in range(n)] for i in range(n)]

def batch_inverse(xs,p):
    pref=[1]
    for x in xs: pref.append(pref[-1]*x%p)
    inv=pow(pref[-1],-1,p); out=[0]*len(xs)
    for j in range(len(xs)-1,-1,-1):
        out[j]=inv*pref[j]%p; inv=inv*xs[j]%p
    return out

def affine_dft(n,z,runs,p,w):
    out=[0]*n
    for t,l,b,a in runs:
        start=pow(z,t,p); zl=pow(z,l,p)
        step=pow(w,a%n,p); fs=pow(w,b%n,p); ns=pow(w,(a*l)%n,p)
        phase=numphase=front=1; den=[]; idx=[]; vals=[0]*n
        for k in range(n):
            q=z*phase%p
            if q==1: vals[k]=start*front*l%p
            else:
                vals[k]=start*front*(1-zl*numphase)%p; den.append((1-q)%p); idx.append(k)
            phase=phase*step%p; front=front*fs%p; numphase=numphase*ns%p
        for k,v in zip(idx,batch_inverse(den,p)): vals[k]=vals[k]*v%p
        out=[(u+v)%p for u,v in zip(out,vals)]
    return out

def dft(x,p,w):
    return [sum(v*pow(w,j*k,p) for j,v in enumerate(x))%p for k in range(len(x))]

def ntt(x,p,w):
    n=len(x); a=x[:]; j=0
    for i in range(1,n):
        b=n>>1
        while j&b: j^=b; b>>=1
        j^=b
        if i<j: a[i],a[j]=a[j],a[i]
    l=2
    while l<=n:
        step=pow(w,n//l,p)
        for base in range(0,n,l):
            z=1
            for k in range(l//2):
                u=a[base+k]; v=a[base+k+l//2]*z%p
                a[base+k]=(u+v)%p; a[base+k+l//2]=(u-v)%p; z=z*step%p
        l*=2
    return a

def run():
    start=time.time(); result={'status':'PASS','source_execution':'None; only independent audit code was run.'}
    source=json.loads((ROOT/'SOURCE_INPUTS.json').read_text()); archive=ROOT/source['source_zip']
    assert archive.stat().st_size==source['bytes'] and hashlib.sha256(archive.read_bytes()).hexdigest()==source['sha256']
    result['original_archive_verified']=True
    stride=0; comm=0
    for n in (8,16,32,64,128,256):
        for u in range(1,n//2,2):
            a=2*u; order=two_run(n,a); w=successor(order); z=[(j+1)%n for j in range(n)]
            ranks=[n-len(cycles([(w[j]-b)%n for j in range(n)])) for b in range(1,n)]
            assert min(ranks)==n//2-1
            assert ranks[(a%n)-1]==ranks[((-a)%n)-1]==n//2-1
            v=compose(invert(compose(z,w)),compose(w,z))
            assert cycles(v)==[n//4,3*n//4]
            for j in range(n):
                expected={ (a-2)%n:(-a)%n, a%n:(a-1)%n, (-a-1)%n:(-a-2)%n }.get(j,(j+(-2*a if j%2==0 else 2*a))%n)
                assert v[j]==expected
            stride+=n-1; comm+=1
    result['permutation_checks']={'stride_cases':stride,'all_slope_commutators':comm,'lengths':[8,16,32,64,128,256]}
    rankfields=0
    for n in (8,16,32):
        for a in range(2,n,4):
            w=successor(two_run(n,a)); z=[(j+1)%n for j in range(n)]
            wz=compose(w,z); zw=compose(z,w)
            for p in (2,3,97):
                arr=[[int(i==wz[j])-int(i==zw[j]) for j in range(n)] for i in range(n)]
                assert rank(arr,p)==n-2; rankfields+=1
    result['dense_permutation_rank_checks']=rankfields
    gr=0
    for n in (8,16,32):
        for a in range(2,n,4):
            ga=green_matrix(two_run(n,a),2,P); gz=green_matrix(list(range(n)),3,P)
            ab=matmul(ga,gz,P); ba=matmul(gz,ga,P)
            assert rank([[(x-y)%P for x,y in zip(u,v)] for u,v in zip(ab,ba)],P)==n-2; gr+=1
    result['dense_resolvent_commutators']=gr
    affine=0; large=0
    for n in (8,16,32,64):
        w=pow(3,(P-1)//n,P)
        specs=[]
        for a in range(2,n,4): specs.append([(0,n//2,0,a),(n//2,n//2,n-1,-a)])
        specs += [[(0,n,0,1)],[(0,n//2,0,1),(n//2,n//2,n-1,-1)],[(j,1,(5*j)%n,0) for j in range(n)]]
        for runs in specs:
            order=[0]*n
            for t,l,b,a in runs:
                for v in range(l): order[t+v]=(b+a*v)%n
            assert len(set(order))==n
            for z in [0,2,3]+[pow(w,k,P) for k in range(n)]:
                x=[0]*n
                for t,j in enumerate(order): x[j]=pow(z,t,P)
                assert affine_dft(n,z,runs,P,w)==dft(x,P,w); affine+=1
    for n in (256,1024,4096,16384):
        w=pow(3,(P-1)//n,P)
        for a in (2,n//2+2):
            runs=[(0,n//2,0,a),(n//2,n//2,n-1,-a)]; order=two_run(n,a)
            for z in (0,2,w):
                x=[0]*n; v=1
                for j in order: x[j]=v; v=v*z%P
                assert affine_dft(n,z,runs,P,w)==ntt(x,P,w); large+=1
    result['affine_dft_checks']={'dense':affine,'large_independent_ntt':large,'max_n':16384}
    cuts=[]
    for n in (16,32,64,128):
        q=n//4; i=list(range(q))+list(range(2*q,3*q)); j=list(range(q,2*q))+list(range(3*q,n)); si=set(i)
        w=successor(two_run(n,n//2+2)); z=[(k+1)%n for k in range(n)]
        assert [(k,w[k]) for k in j if w[k] in si]==[(q+1,3*q-1),(3*q+1,q-1),(n-2,2*q)]
        assert [(k,z[k]) for k in j if z[k] in si]==[(2*q-1,2*q),(n-1,0)]
        ga=green_matrix(two_run(n,n//2+2),2,P); gz=green_matrix(list(range(n)),3,P)
        s=[[(u+v)%P for u,v in zip(r1,r2)] for r1,r2 in zip(ga,gz)]
        hidden=rank([[s[r][c] for c in j] for r in i],P)
        nat=rank([row[n//2:] for row in s[:n//2]],P)
        assert hidden==5 and nat==n//2
        assert rank([[ga[r][c] for c in j] for r in i],P)==3
        assert rank([[gz[r][c] for c in j] for r in i],P)==2
        cuts.append({'n':n,'natural_rank':nat,'hidden_rank':hidden})
    result['cut_checks']=cuts
    for n in (16,32,64,256,1024,16384):
        order=four_track(n); loc=invert(order); w=successor(two_run(n,n//2+2))
        farw=[(j,w[j]) for j in range(n) if abs(loc[w[j]]-loc[j])>6]
        farz=[(j,(j+1)%n) for j in range(n) if abs(loc[(j+1)%n]-loc[j])>6]
        assert farw==[(1,n//2-1),(n-2,n//2)] and farz==[(n//2-1,n//2),(n-1,0)]
    result['four_track_checks']=[16,32,64,256,1024,16384]
    n=16; rows,_=sparse_denominator(n,2,2,P); c=dense(rows,P)
    band=[[v if abs(i-j)<=6 else 0 for j,v in enumerate(row)] for i,row in enumerate(c)]
    dc=determinant(c,P); db=determinant(band,P); zero=first_zero_unpivoted(band,P)
    assert dc and db and zero==5 and pow(2,n,P)!=1
    result['unpivoted_counterexample']={'p':P,'n':n,'alpha':2,'beta':2,'det_C':dc,'det_band':db,'zero_pivot_zero_based':zero,'resolvent_denominator':(1-pow(2,n,P))%P}
    alpha=Fraction(3,2); beta=Fraction(1,2)
    assert alpha**16!=1 and beta**16!=1 and 1/(1-alpha)+1/(1-beta)==0
    result['singular_sum_counterexample']={'n':16,'alpha':'3/2','beta':'1/2','ones_eigenvalue_of_S':'0','ones_eigenvalue_of_C':'0'}
    small={'n':16,'p':19,'nonsingular':0,'singular':0}; base_singular=None
    for alpha in range(19):
        if pow(alpha,16,19)==1: continue
        for beta in range(19):
            if pow(beta,16,19)==1: continue
            rows,order=sparse_denominator(16,alpha,beta,19); a=dense(rows,19); rr=rank(a,19)
            try: f=factor(rows,6,19)
            except ArithmeticError:
                assert rr<16; small['singular']+=1; continue
            assert rr==16; small['nonsingular']+=1
            x=[(k*k+3*k+7)%19 for k in range(16)]
            rhs=[sum(v*x[j] for j,v in row.items())%19 for row in rows]
            assert f.solve(rhs)==x
            inv=TwistedInverse.create(16,alpha,beta,19)
            sg=[(u+v)%19 for u,v in zip(green_apply(two_run(16,10),alpha,x,19),green_apply(list(range(16)),beta,x,19))]
            assert inv.apply(sg)==x
            band=[[v if abs(i-j)<=6 else 0 for j,v in enumerate(row)] for i,row in enumerate(a)]
            if base_singular is None and rank(band,19)<16:
                base_singular={'n':16,'p':19,'alpha':alpha,'beta':beta,'det_C':determinant(a,19),'rank_band':rank(band,19)}
    result['all_parameter_frontier_control']=small
    result['singular_band_counterexample']=base_singular
    solver=[]
    for n in (16,64,256,1024,4096,16384):
        for alpha,beta in ((2,3),(2,2),(pow(4,-1,P),pow(5,-1,P))):
            inv=TwistedInverse.create(n,alpha,beta,P); x=[(k*k+17*k+29)%P for k in range(n)]
            s=lambda v:[(a+b)%P for a,b in zip(green_apply(two_run(n,n//2+2),alpha,v,P),green_apply(list(range(n)),beta,v,P))]
            assert inv.apply(s(x))==x and s(inv.apply(x))==x
            f=inv.factors
            assert f.max_active<=11 and f.max_row_nonzeros<=25
            solver.append({'n':n,'alpha':alpha,'beta':beta,'max_active':f.max_active,'max_row_nonzeros':f.max_row_nonzeros,'elimination_updates':f.elimination_updates})
    result['large_solver_checks']=solver
    r=Fraction(1,4); s=Fraction(1,5)
    bound=(1/(1-r)+1/(1-s))/(1/(1+r)+1/(1+s))
    assert bound==Fraction(155,98)
    result['improved_complex_condition_bound']='155/98'
    result['elapsed_seconds']=round(time.time()-start,3)
    (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': run()
