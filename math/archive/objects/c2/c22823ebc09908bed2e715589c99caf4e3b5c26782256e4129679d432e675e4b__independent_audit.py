"""Independent randomized and operation-ledger audit for Phase18.

Checks an independently coded cyclic Green solver and separate dense elimination;
charges a direct K-branch reference without invoking the collapsed identity.
"""
import random,json,time,hashlib
from pathlib import Path
from phase18 import (Count,MagneticTwirlPlan,WeightedSectorPlan,primitive_nth_root,
                     independent_twirl)
from test_phase18 import direct_branches,rank,matrix_by_application,F,commutator

OUT=Path(__file__).parent


def reference_with_ledger(x,a,b,k,p,omega):
    """K direct Green solves with shared periodic diagonal inverses.
    Does not call the compressed operator or use its D = dI-cS^K formula.
    """
    n=len(x);m=n//k;c=Count()
    def pp(z,t):
        v=1;b=z%p
        while t:
            if t&1:v=c.mul(v,b,p)
            t>>=1
            if t:b=c.mul(b,b,p)
        return v
    q=pp(omega,m)
    phases=[1];
    for t in range(1,k):phases.append(c.mul(phases[-1],q,p))
    invd=[];r=[]
    for t in range(k):
        d=c.sub(1,c.mul(b,phases[t],p),p)
        dinv=c.inverse(d,p)
        invd.append(dinv)
        r.append(c.mul(a,dinv,p))
    prod=1
    for z in r:prod=c.mul(prod,z,p)
    A=pp(prod,m)
    inv_cycle=c.inverse(c.sub(1,A,p),p)
    acc=[0]*n
    for j in range(k):
        B=0;rhs=[0]*n
        for i in range(n):
            t=(i+j)%k
            rhs[i]=c.mul(x[i],invd[t],p)
            B=c.add(c.mul(r[t],B,p),rhs[i],p)
        z=c.mul(B,inv_cycle,p)
        for i in range(n):
            z=c.add(c.mul(r[(i+j)%k],z,p),rhs[i],p)
            acc[i]=c.add(acc[i],z,p)
    invK=c.inverse(k,p)
    result=[c.mul(val,invK,p) for val in acc]
    return result,c.report()


def direct_selected_bins(x,p,omega,ks):
    n=len(x);answer=[]
    for k in ks:
        wk=pow(omega,(-k)%n,p)
        step=1;v=0
        for xi in x:
            v=(v+xi*step)%p
            step=step*wk%p
        answer.append(v)
    return answer


def small_audit():
    rng=random.Random(20261010)
    total_full=0;entries=0;weighted=0;rankcases=0
    samples=[]
    for n,k,p in [(8,4,97),(12,3,97),(12,4,97),(15,5,241),(16,4,97),(24,6,97),(32,8,97)]:
        w=primitive_nth_root(n,p)
        passed=0
        for t in range(18):
            a=rng.randrange(p);b=rng.randrange(p)
            try:plan=MagneticTwirlPlan(n,k,p,a,b,w)
            except (ZeroDivisionError,ValueError):continue
            x=[rng.randrange(p) for _ in range(n)]
            independent=direct_branches(x,a,b,k,p,w)
            fused=plan.apply(x)
            assert independent==fused,(n,k,a,b)
            passed+=1;total_full+=1;entries+=n
            if t%3==0:
                for ell in range(min(k,4)):
                    wgot=WeightedSectorPlan(plan,ell).apply(x)
                    expected=direct_branches(x,a,b,k,p,w,ell)
                    assert wgot==expected
                    weighted+=1
        samples.append({'n':n,'k':k,'prime':p,'cases':passed})
        # Dense rank of averaged operator via basis images, independent elimination.
        a,b=2,3
        try:
            plan=MagneticTwirlPlan(n,k,p,a,b,w)
            actual=rank(matrix_by_application(plan,n),p)
            expect=n-k+1 if pow(a,n,p)==1 else n
            assert actual==expect
            rankcases+=1
        except ZeroDivisionError:pass
    return dict(full_vector_cases=total_full,checked_entries=entries,
                weighted_gaussian_cases=weighted,rank_cases=rankcases,
                cases=samples)


def large_audit():
    n=65536;k=64;p=65537;a=2;b=3
    w=primitive_nth_root(n,p)
    rng=random.Random(17)
    x=[rng.randrange(p) for _ in range(n)]
    t0=time.perf_counter(); plan=MagneticTwirlPlan(n,k,p,a,b,w)
    c=Count();actual=plan.apply(x,c)
    prep=plan.counter.report();online=c.report()
    t1=time.perf_counter()
    baseline,base_ops=reference_with_ledger(x,a,b,k,p,w)
    t2=time.perf_counter()
    assert actual==baseline
    # Independent direct DFT outputs: magnetic twirl is NOT a DFT.
    bins=[0,1,2,3,7,31,255,1024,8191,32768,65535]
    true_dft=direct_selected_bins(x,p,w,bins)
    discrepancies=sum(actual[i]!=v for i,v in zip(bins,true_dft))
    assert discrepancies>=8
    # output recurrence verification: D y = P_K(S) x; direct O(KN) would be too
    # expensive but we verify selected residuals with naive convolution.
    res_inds=[0,1,2,7,14,29,128,1023,4096,16384,65535]
    ak=pow(a,k,p);bk=pow(b,k,p);d=(1-bk)%p
    for i in res_inds:
        raw=sum(pow(a,j,p)*x[(i-j)%n] for j in range(k))%p
        assert (d*actual[i]-ak*actual[(i-k)%n]-raw)%p==0
    return dict(N=n,K=k,prime=p,alpha=a,beta=b,
                setup_field_ops=prep,online_field_ops=online,
                total_fused_field_ops=prep['total_field_ops']+online['total_field_ops'],
                reference_shared_prep_and_K_solves=base_ops,
                counted_op_ratio=round(base_ops['total_field_ops']/
                   (prep['total_field_ops']+online['total_field_ops']),4),
                full_outputs_independently_compared=n,
                direct_dft_bins=bins,dft_bin_mismatches=discrepancies,
                independently_directly_verified_residuals=len(res_inds),
                elapsed_fused_seconds=round(t1-t0,4),
                elapsed_reference_seconds=round(t2-t1,4))


def size_ledger():
    rows=[]
    for n,k,p in [(64,8,193),(256,16,257),(1024,32,12289),
                    (4096,64,12289),(16384,128,65537),
                    (65536,256,65537)]:
        w=primitive_nth_root(n,p)
        a,b=2,3
        try:plan=MagneticTwirlPlan(n,k,p,a,b,w)
        except ZeroDivisionError:continue
        x=[(77*i+13)%p for i in range(n)]
        c=Count();y=plan.apply(x,c)
        val=plan.counter.report()['total_field_ops']+c.report()['total_field_ops']
        rows.append(dict(N=n,K=k,ops=val,ops_per_N=round(val/n,4),checksum=sum(y)%p))
    return rows


def main():
    ts=time.time(); report={'phase':18,'model':'exact prime-field scalar arithmetic',
        'status':'structured Green-resolvent fusion, not FFT'}
    report['small']=small_audit()
    report['large']=large_audit()
    report['scaling']=size_ledger()
    report['audit_elapsed_seconds']=round(time.time()-ts,3)
    (OUT/'AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
