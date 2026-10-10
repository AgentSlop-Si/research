"""Independent audit controls, authored 2026-10-10. No uploaded module imports.

All arithmetic is exact modulo a specified prime. The completion uses the
explicit fixed-basis proof in PROOF_AUDIT.md, not the source's greedy code.
"""
import itertools
import json
import math
from pathlib import Path
import random

OUT = Path(__file__).resolve().parent

def tr(a):
    return list(map(list, zip(*a)))

def sub(a, rr, cc):
    return [[a[i][j] for j in cc] for i in rr]

def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def mm(a, b, p):
    return [[sum(x*y for x,y in zip(row,col)) % p for col in zip(*b)] for row in a]

def add(a,b,p,sgn=1):
    return [[(x+sgn*y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def rref(a,p):
    b=[list(map(lambda x:x%p,row)) for row in a]
    piv=[]
    if not b: return b,piv
    for c in range(len(b[0])):
        rs=[i for i in range(len(piv),len(b)) if b[i][c]]
        if not rs: continue
        r=len(piv); z=rs[0]
        b[r],b[z]=b[z],b[r]
        v=pow(b[r][c],-1,p)
        b[r]=[x*v%p for x in b[r]]
        for i in range(len(b)):
            if i != r:
                t=b[i][c]
                b[i]=[(x-t*y)%p for x,y in zip(b[i],b[r])]
        piv.append(c)
        if len(piv)==len(b): break
    return b,piv

def rank(a,p): return len(rref(a,p)[1])

def inv(a,p):
    n=len(a)
    b,piv=rref([row+e for row,e in zip(a,eye(n))],p)
    if piv[:n] != list(range(n)): raise ValueError('singular')
    return [row[n:] for row in b]

def det(a,p):
    b=[row[:] for row in a]; out=1
    for c in range(len(b)):
        rs=[i for i in range(c,len(b)) if b[i][c]%p]
        if not rs:return 0
        r=rs[0]
        if r!=c: b[c],b[r]=b[r],b[c];out=-out
        v=b[c][c]%p;out=out*v%p
        for i in range(c+1,len(b)):
            t=b[i][c]*pow(v,-1,p)%p
            b[i]=[(x-t*y)%p for x,y in zip(b[i],b[c])]
    return out%p

def fourier(n,p):
    w=next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n)))
    return [[pow(w,i*j,p) for j in range(n)] for i in range(n)],w

def cauchy(n,p):
    return [[pow(i-(n+j),-1,p) for j in range(n)] for i in range(n)]

def fixed_completion(m,p):
    n=len(m); h=n//2
    basis=[[m[k][j] if j>k else 0 for j in range(n)] for k in range(h)]
    weights=eye(h)
    for i in range(h,n):
        d=n-i-1
        if not d: co=[]
        else:
            b=sub(m,range(d),range(i+1,n))
            co=mm([m[i][i+1:]],inv(b,p),p)[0]
        weights.append(co+[0]*(h-d))
    r=mm(weights,basis,p) if h else [[0]*n for _ in range(n)]
    t=add(m,r,p,-1)
    assert all(t[i][j]==0 for i in range(n) for j in range(i+1,n))
    assert all(t[i][i]!=0 for i in range(n))
    assert rank(r,p)==h
    return r,t,weights,basis

def schur_from_factor(m,t,x,y,p):
    n=len(m);q=len(y);a=inv(t,p)
    u=mm(a,x,p);v=mm(y,a,p)
    b=add(eye(q),mm(y,mm(a,x,p),p),p)
    k=[ar+ur for ar,ur in zip(a,u)]+[vr+br for vr,br in zip(v,b)]
    ki=inv(k,p)
    assert sub(ki,range(n),range(n))==m
    assert add(b,mm(v,mm(t,u,p),p),p,-1)==eye(q)
    return {"n":n,"q":q,"baseline_diagonal":[t[i][i] for i in range(n)],
            "baseline_det":det(t,p),"nnz_u":sum(bool(z) for r in u for z in r),
            "nnz_v":sum(bool(z) for r in v for z in r),"nnz_b":sum(bool(z) for r in b for z in r)},k

def completion_minrank_formula(m,p):
    n=len(m)
    increments=[rank(sub(m,range(j+1),range(j+1,n)),p)-rank(sub(m,range(j),range(j+1,n)),p) for j in range(n)]
    return sum(increments),increments

def lis(seq):
    a=[]
    for i,x in enumerate(seq):a.append(1+max([a[j] for j in range(i) if seq[j]<x] or [0]))
    return max(a,default=0)

def main():
    result={"discipline":"Only this fresh script executed; uploaded programs and bytecode inert."}
    result['reverse_orders']=[]
    for n in range(2,9):
        good=[]
        for order in itertools.permutations(range(n)):
            pos={v:i for i,v in enumerate(order)}
            if all(pos[i]>pos[j] for i in range(n) for j in range(i+1,n)):good.append(order)
        assert good==[tuple(reversed(range(n)))]
        result['reverse_orders'].append({'n':n,'tested':math.factorial(n),'survivors':1})

    result['fullspark']=[]
    for n,p in [(5,11),(7,29)]:
        f,w=fourier(n,p);count=0
        for d in range(1,n+1):
            for rows in itertools.combinations(range(n),d):
                for cols in itertools.combinations(range(n),d):
                    assert det(sub(f,rows,cols),p)!=0
                    count+=1
        result['fullspark'].append({'n':n,'p':p,'omega':w,'all_minors':count})

    result['nonfullspark']=[]
    for n,p in [(9,19),(11,23),(13,53)]:
        f,w=fourier(n,p);bad=None;count=0
        for d in range(2,5):
            if bad:break
            for rows in itertools.combinations(range(n),d):
                if bad:break
                for cols in itertools.combinations(range(n),d):
                    count+=1
                    b=sub(f,rows,cols)
                    if det(b,p)==0:bad={'rows':rows,'cols':cols,'matrix':b,'det':0};break
        result['nonfullspark'].append({'n':n,'p':p,'omega':w,'searched_minors':count,'singular_minor':bad})

    result['fourier_sharp']=[]
    for n,p in [(5,11),(7,29),(9,19),(11,23),(13,53)]:
        f,w=fourier(n,p);r,t,x,y=fixed_completion(f,p)
        info,k=schur_from_factor(f,t,x,y,p);info.update({'p':p,'omega':w})
        result['fourier_sharp'].append(info)

    result['cauchy_sharp']=[]
    for n in range(2,41):
        p=1009;f=cauchy(n,p);r,t,x,y=fixed_completion(f,p)
        info,k=schur_from_factor(f,t,x,y,p);result['cauchy_sharp'].append(info)

    rng=random.Random(10301247)
    permuted=0
    for n,p in [(5,11),(7,29)]:
        f,w=fourier(n,p)
        for trial in range(40):
            rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
            rs=[rng.randrange(1,p) for _ in range(n)];cs=[rng.randrange(1,p) for _ in range(n)]
            m=[[f[rp[i]][cp[j]]*rs[i]*cs[j]%p for j in range(n)] for i in range(n)]
            r,t,x,y=fixed_completion(m,p);schur_from_factor(m,t,x,y,p);permuted+=1
    result['endpoint_gauges_verified']=permuted

    result['lis_masked_controls']=[]
    for n,p in [(5,11),(7,29)]:
        f,w=fourier(n,p);count=0;slack=n
        for order in itertools.permutations(range(n)):
            pos={v:i for i,v in enumerate(order)}
            ell=lis([pos[i] for i in range(n)])
            r=[[f[i][j] if i<j and pos[i]<pos[j] else 0 for j in range(n)] for i in range(n)]
            rr=rank(r,p);assert rr>=ell//2;slack=min(slack,rr-ell//2);count+=1
        result['lis_masked_controls'].append({'n':n,'p':p,'orders':count,'min_slack':slack})

    f,w=fourier(4,5);order=[0,2,1,3];m=sub(f,order,order)
    x=[[1],[4],[(-w)%5],[0]];y=[[0,1,1,1]];r=mm(x,y,5);t=add(m,r,5,-1)
    assert rank(r,5)==1 and all(t[i][j]==0 for i in range(4) for j in range(i+1,4))
    info,k=schur_from_factor(m,t,x,y,5)
    result['composite_counterexample']={'field':5,'omega':w,'order':order,'M':m,'R':r,'T':t,'K':k,'certificate':info}

    result['bit_reversal_completion_rank']=[]
    for n,p in [(4,5),(8,17),(16,97),(32,97),(64,193)]:
        f,w=fourier(n,p);bits=n.bit_length()-1
        order=[int(format(i,f'0{bits}b')[::-1],2) for i in range(n)]
        m=sub(f,order,order);q,steps=completion_minrank_formula(m,p)
        result['bit_reversal_completion_rank'].append({'n':n,'p':p,'omega':w,'min_rank_formula':q,'increments':steps})

    result['two_branch_schur']=[]
    for n in [3,5,7]:
        p=101
        for q in [1,2,n]:
            a=[[rng.randrange(p) if i>j else int(i==j) for j in range(n)] for i in range(n)]
            b=[[rng.randrange(p) if i<j else int(i==j) for j in range(n)] for i in range(n)]
            d=[row+[0]*n for row in a]+[[0]*n+row for row in b];di=inv(d,p)
            u=[[rng.randrange(p) for j in range(q)] for i in range(2*n)]
            v=[[rng.randrange(p) for j in range(2*n)] for i in range(q)]
            h=add(eye(q),mm(v,mm(di,u,p),p),p)
            k=[row+ur for row,ur in zip(d,u)]+[row+hr for row,hr in zip(v,h)]
            ki=inv(k,p);g=sub(ki,range(2*n),range(2*n));cor=add(g,di,p,-1)
            assert rank(cor,p)<=q
            off=sub(g,range(n),range(n,2*n));assert rank(off,p)<=q
            s=[[sum(g[i+ni][j+nj] for ni in [0,n] for nj in [0,n])%p for j in range(n)] for i in range(n)]
            sr=rank(add(s,add(inv(a,p),inv(b,p),p),p,-1),p);assert sr<=q
            result['two_branch_schur'].append({'n':n,'q':q,'correction_rank':rank(cor,p),'cross_rank':rank(off,p),'summed_correction_rank':sr})

    # General separator check without invertible principal branch blocks.
    sep_checked=0;singular_side=0
    for _ in range(1000):
        # Coordinates U=(0,1), S=(2), V=(3,4); zero both cross blocks.
        k=[[rng.randrange(5) for j in range(5)] for i in range(5)]
        for i in [0,1]:
            for j in [3,4]:k[i][j]=k[j][i]=0
        if det(k,5)==0:continue
        ki=inv(k,5);assert rank(sub(ki,[0,1],[3,4]),5)<=1
        sep_checked+=1
        singular_side+=int(det(sub(k,[0,1],[0,1]),5)==0 or det(sub(k,[3,4],[3,4]),5)==0)
    result['separator_without_principal_invertibility']={'invertible_whole_systems':sep_checked,'singular_principal_side_cases':singular_side}
    # Shared zero rectangles can be stronger than the LIS-chain certificate.
    n=8;p=101;m=cauchy(n,p);order=[3,2,1,0,7,6,5,4]
    pos={v:i for i,v in enumerate(order)}
    assert lis([pos[i] for i in range(n)])==2
    assert all(i<j and pos[i]<pos[j] for i in range(4) for j in range(4,8))
    assert rank(sub(m,range(4),range(4,8)),p)==4
    result['lis_not_sufficient']={'n':8,'sigma':order,'LIS':2,'LIS_lower_bound':1,'common_zero_rectangle_rank':4}

    # Same-branch bound also follows from one-sided zero cuts when A is singular.
    same_checked=0;same_singular=0
    for q in [1,2]:
        n=5;p=5;half=n//2
        for _ in range(500):
            a=[[rng.randrange(p) if i>=j else 0 for j in range(n)] for i in range(n)]
            u=[[rng.randrange(p) for j in range(q)] for i in range(n)]
            v=[[rng.randrange(p) for j in range(n)] for i in range(q)]
            b=[[rng.randrange(p) for j in range(q)] for i in range(q)]
            k=[ar+ur for ar,ur in zip(a,u)]+[vr+br for vr,br in zip(v,b)]
            if not det(k,p):continue
            ki=inv(k,p)
            assert rank(sub(ki,range(half),range(n-half,n)),p)<=q
            same_checked+=1;same_singular+=int(det(a,p)==0)
    result['same_branch_without_A_invertibility']={'invertible_whole_systems':same_checked,'singular_A_cases':same_singular}
    result['status']='PASS'
    (OUT/'fresh_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
