#!/usr/bin/env python3
"""Auditor-authored exact controls. No source imports or source execution."""
import json, math, random, hashlib
from fractions import Fraction
from pathlib import Path

def root(n,p):
    for g in range(2,p):
        w=pow(g,(p-1)//n,p)
        if pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n)):
            return w
    raise ValueError('no primitive root')
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(A,B,p):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def mv(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]
def inv(A,p):
    n=len(A);R=[row[:]+e for row,e in zip(A,eye(n))]
    for j in range(n):
        k=next((k for k in range(j,n) if R[k][j]%p),None)
        if k is None:raise ValueError('singular')
        R[j],R[k]=R[k],R[j];z=pow(R[j][j],-1,p);R[j]=[x*z%p for x in R[j]]
        for k in range(n):
            if k!=j:
                z=R[k][j];R[k]=[(x-z*y)%p for x,y in zip(R[k],R[j])]
    return [r[n:] for r in R]
def rank(A,p):
    R=[r[:] for r in A];k=0
    for j in range(len(R[0])):
        h=next((h for h in range(k,len(R)) if R[h][j]%p),None)
        if h is None:continue
        R[k],R[h]=R[h],R[k];z=pow(R[k][j],-1,p);R[k]=[x*z%p for x in R[k]]
        for h in range(k+1,len(R)):
            z=R[h][j];R[h]=[(x-z*y)%p for x,y in zip(R[h],R[k])]
        k+=1
        if k==len(R):break
    return k
def mon(n,w,p,a,b):return [[pow(w,b*j,p) if i==(j+a)%n else 0 for j in range(n)] for i in range(n)]
def coeff(A,w,p):
    n=len(A);ni=pow(n,-1,p)
    return [[sum(pow(w,(-b*t)%n,p)*A[(t+a)%n][t] for t in range(n))*ni%p for b in range(n)] for a in range(n)]
def synth(C,w,p):
    n=len(C)
    return [[sum(C[(i-j)%n][b]*pow(w,b*j,p) for b in range(n))%p for j in range(n)] for i in range(n)]
def green(X,a,p):
    n=len(X);return inv([[(int(i==j)-a*X[i][j])%p for j in range(n)] for i in range(n)],p)
def gs(x,a,p,c=None):
    n=len(x);power=a;z=x[0]
    for k in range(n-1,0,-1):z=(z+power*x[k])%p;power=power*a%p
    y=[z*pow(1-power,-1,p)%p]
    for k in range(1,n):y.append((x[k]+a*y[-1])%p)
    if c is not None:c[0]+=2*n-1;c[1]+=3*n-2;c[2]+=1
    return y
def prepare(n,b,w,p,c=None):
    ds=[];pre=[1];t=1
    for _ in range(n):
        d=(1-b*t)%p
        if not d:raise ValueError('pole')
        ds.append(d);pre.append(pre[-1]*d%p);t=t*w%p
    z=pow(pre[-1],-1,p);out=[0]*n
    for j in range(n-1,-1,-1):out[j]=z*pre[j]%p;z=z*ds[j]%p
    if c is not None:c[0]+=n;c[1]+=5*n;c[2]+=1
    return out

def main():
    out={'policy':'Only this independently authored checker was executed; uploaded programs remain inert.'}
    cases=[(3,31),(5,101),(7,113),(9,109),(11,353),(15,241),(17,443)]
    checks=[];rotated=0;entries=0;endpoint=0;basis_ops=0;witnesses=[];composite=[]
    for n,p in cases:
        w=root(n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
        C=coeff(F,w,p);G=sum(pow(w,j*j,p) for j in range(n))%p;gam=G*pow(n,-1,p)%p;i2=pow(2,-1,n);i4=pow(4,-1,n)
        assert G*sum(pow(w,-j*j,p) for j in range(n))%p==n%p
        formula=[[gam*pow(w,-(a-b)**2*i4,p)%p for b in range(n)] for a in range(n)]
        assert C==formula and synth(C,w,p)==F and rank(C,p)==n and all(all(r) for r in C)
        S=mon(n,w,p,1,0);T=mon(n,w,p,0,1)
        params=[a for a in range(2,p) if pow(a,n,p)!=1][:3];a,b,g=params
        A=green(S,a,p);B=green(T,b,p);E=green(S,g,p);fwd=mul(A,B,p);rev=mul(B,A,p);triple=mul(mul(A,B,p),E,p)
        den=pow((1-pow(a,n,p))*(1-pow(b,n,p)),-1,p)
        assert coeff(fwd,w,p)==[[den*pow(a,i,p)*pow(b,j,p)%p for j in range(n)] for i in range(n)]
        assert coeff(rev,w,p)==[[den*pow(a,i,p)*pow(b,j,p)*pow(w,i*j,p)%p for j in range(n)] for i in range(n)]
        assert [rank(coeff(X,w,p),p) for X in [fwd,rev,triple]]==[1,n,n]
        for l1,l2,r1,r2 in [(1,2,3,4),(0,1,2,0),(4,2,0,3)]:
            M=mul(mul(mon(n,w,p,l1,l2),fwd,p),mon(n,w,p,r1,r2),p)
            assert rank(coeff(M,w,p),p)==1;endpoint+=1
        diag=prepare(n,b,w,p)
        for j in range(n):
            x=[int(k==j) for k in range(n)]
            tests=[gs([v*d%p for v,d in zip(x,diag)],a,p),[v*d%p for v,d in zip(gs(x,a,p),diag)],gs([v*d%p for v,d in zip(gs(x,g,p),diag)],a,p)]
            for y,M in zip(tests,[fwd,rev,triple]):assert y==mv(M,x,p);basis_ops+=1
        assert all(X!=F for X in [fwd,rev,triple])
        for u,v,r,s in [(1,0,0,1),(1,0,1,1),(0,1,1,1),(1,1,0,1),(1,2,1,3),(1,0,1,7),(1,0,1,11),(2,1,1,1),(2,3,3,2)]:
            D=(u*s-v*r)%n
            if math.gcd(D,n)!=1:continue
            de=(D-u*r-v*s)*i2%n;q=u*u+v*v;t=r*r+s*s
            CR=[[gam*pow(w,(-q*i*i*i4+u*v*i*i2-t*j*j*i4+r*s*j*i2+de*i*j)%n,p)%p for j in range(n)] for i in range(n)]
            # Actual matrix powers and products, not the rotated phase formula, synthesize.
            U=mon(n,w,p,u,v);V=mon(n,w,p,r,s);up=eye(n);R=[[0]*n for _ in range(n)]
            for i in range(n):
                vp=eye(n)
                for j in range(n):
                    term=mul(up,vp,p)
                    R=[[(x+CR[i][j]*y)%p for x,y in zip(row,trow)] for row,trow in zip(R,term)]
                    vp=mul(vp,V,p)
                up=mul(up,U,p)
            assert R==F;actual=rank(CR,p);assert actual==n//math.gcd(n,de)
            if n in (9,15) and actual not in (1,n):composite.append({'n':n,'basis':[u,v,r,s],'delta':de,'rank':actual})
            if de==0:
                m=(n+1)//2;assert rank([[CR[i+j][0] for j in range(m)] for i in range(m)],p)==m
            rotated+=1;entries+=n*n
        # A bounded witness search is evidence, not a uniform parameter-generation algorithm.
        witness=None
        for aa in range(2,min(p,12)):
            if pow(aa,n,p)==1:continue
            GA=green(S,aa,p)
            for bb in range(2,min(p,12)):
                if pow(bb,n,p)==1:continue
                GB=green(T,bb,p);H=[[(x+y)%p for x,y in zip(ra,rb)] for ra,rb in zip(GA,GB)]
                try:HI=inv(H,p)
                except ValueError:continue
                if all(all(row) for row in HI):
                    assert mul(H,HI,p)==eye(n) and H!=F and mul(GA,GB,p)!=mul(GB,GA,p)
                    witness={'n':n,'field':p,'alpha':aa,'beta':bb,'inverse_support':n*n};break
            if witness:break
        assert witness;witnesses.append(witness);checks.append({'n':n,'field':p,'omega':w,'forward_rank':1,'reverse_triple_ranks':[n,n]})
    out.update(cases=checks,rotated_actual_matrix_reconstructions=rotated,rotated_entries=entries,canonical_endpoint_controls=endpoint,all_basis_operator_checks=basis_ops,composite_intermediate_ranks=composite,dense_inverse_witnesses=witnesses)
    enumerated=[]
    for n,p in cases:
        if n not in (3,5,7,11):continue
        w=root(n,p);i2=pow(2,-1,n);i4=pow(4,-1,n);count=0;zero=0;rank_checks=0;hankel=0
        for u in range(n):
          for v in range(n):
           for r in range(n):
            for s in range(n):
                D=(u*s-v*r)%n
                if not D:continue
                de=(D-u*r-v*s)*i2%n;A=(u*u+v*v)%n;B=(r*r+s*s)%n;h=(u*r+v*s)%n
                assert (A*B-h*h-D*D)%n==0
                core=[[pow(w,de*i*j,p) for j in range(n)] for i in range(n)]
                assert rank(core,p)==(n if de else 1);rank_checks+=1
                if not de:
                    assert A and B and (A*B-2*D*D)%n==0
                    m=(n+1)//2;seq=[pow(w,(-A*i*i*i4+u*v*i*i2)%n,p) for i in range(n)]
                    assert rank([[seq[i+j] for j in range(m)] for i in range(m)],p)==m
                    zero+=1;hankel+=1
                count+=1
        enumerated.append({'n':n,'GL2_pairs':count,'actual_core_ranks':rank_checks,'rank_one_hankel_checks':hankel})
    out['all_generating_prime_pairs']=enumerated
    # Endpoints invalidate the geometric nonwrapping rank-one premise.
    n=5;p=101;seq=[pow(2,(i-1)%n,p) for i in range(n)];hr=rank([[seq[i+j] for j in range(3)] for i in range(3)],p)
    assert hr==2;out['endpoint_hankel_countercontrol']={'n':n,'field':p,'shifted_geometric_sequence':seq,'rank':hr}
    # Characteristic-zero dense inverse specialization using exact rationals.
    rat=[]
    for n in range(2,18):
        a=Fraction(1,2);cs=[-a**k/(2**(k+1)*(1-(a/2)**n)) for k in range(n)];cs[0]+=1
        assert all(cs);rat.append(n)
    out['rational_beta_zero_dense_inverse_lengths']=rat
    # Explicit singular guards and zero-parameter rank-one cases.
    try:gs([1,2,3],1,31);raise AssertionError('pole missed')
    except ValueError:pass
    try:prepare(3,1,root(3,31),31);raise AssertionError('pole missed')
    except ValueError:pass
    assert gs([1,2,3],0,31)==[1,2,3]
    out['pole_and_zero_parameter_guards']=3
    n=65536;p=998244353;w=pow(3,(p-1)//n,p);assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
    rng=random.Random(2601013);x=[rng.randrange(p) for _ in range(n)];prep=[0,0,0];online=[0,0,0]
    diag=prepare(n,3,w,p,prep);y=gs(x,2,p,online);h=[(a+b*c)%p for a,b,c in zip(y,x,diag)];online[0]+=n;online[1]+=n
    assert all((y[j]-2*y[j-1]-x[j])%p==0 for j in range(n))
    assert prep==[n,5*n,1] and online==[3*n-1,4*n-2,1] and sum(prep)+sum(online)==13*n-1
    rows=[0,1,7,123,n//3,n//2,n-1];den=pow(1-pow(2,n,p),-1,p);mismatch=0
    for j in rows:
        ref=sum(pow(2,(j-k)%n,p)*x[k] for k in range(n))*den%p
        assert h[j]==(ref+x[j]*pow(1-3*pow(w,j,p),-1,p))%p
        fj=sum(pow(w,j*k,p)*x[k] for k in range(n))%p;mismatch+=int(h[j]!=fj)
    assert mismatch==len(rows)
    out['large_fresh_input']={'n':n,'field':p,'recurrence_equations':n,'direct_kernel_rows':len(rows),'DFT_mismatches':mismatch,'preparation_add_mul_inv':prep,'online_add_mul_inv':online,'total_field_operations':sum(prep)+sum(online),'output_sha256':hashlib.sha256(json.dumps(h).encode()).hexdigest()}
    out['result']='PASS'
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'result':'PASS','rotated':rotated,'GL2':sum(r['GL2_pairs'] for r in enumerated),'basis_operator_checks':basis_ops,'large_work':sum(prep)+sum(online)}))
if __name__=='__main__':main()
