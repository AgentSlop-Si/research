"""Optimized support suppression gate for two quasiseparable stages.
S can be ANY coordinate subset containing J=pi(I), not just interval hull.
Do not claim pass implies existence.
"""
from subset_gate import modrank,fourier_matrix,apply_perm_mask
from itertools import combinations,permutations
from collections import Counter


def gamma(S,J,n,cup=1,cdown=1):
    assert J & S == J
    g=0;i=0
    while i<n:
        if (S>>i)&1: i+=1;continue
        lo=i
        while i<n and not((S>>i)&1):i+=1
        hi=i-1
        if any((J>>j)&1 for j in range(lo)):g+=cdown
        if any((J>>j)&1 for j in range(hi+1,n)):g+=cup
    return g


def bc_window(u,v,n,bup=1,bdown=1):
    return (u>0)*bup+(v<n-1)*bdown


def all_m_rank(n,p=12289,M=None):
    M=fourier_matrix(n,p) if M is None else M
    mask_cols = [tuple(k for k in range(n) if j>>k&1) for j in range(1<<n)]
    mask_rows = [tuple(k for k in range(n) if not(i>>k&1)) for i in range(1<<n)]
    # m rank where I represents missing row window, S retained C support
    mr={}
    for I in range(1,1<<n):
        rowset=mask_rows[I]
        for S in range(1<<n):
            colset=mask_cols[S]
            mr[I,S]=modrank([[M[k][j] for j in colset] for k in rowset],p) if rowset and colset else 0
    return mr


def best_scores(n,mr,cup=1,cdown=1):
    # window I only; all J size t, optimize S superset J
    ans={};arg={}
    ALL=(1<<n)-1
    for u in range(n):
        for v in range(u,n):
            t=v-u+1
            I=sum(1<<k for k in range(u,v+1))
            bcost=bc_window(u,v,n)
            for J in range(1<<n):
                if J.bit_count()!=t:continue
                gaps=ALL^J
                sub=gaps
                best=-10**6; support=None; best_rank=None
                while True:
                    S=J|sub
                    r=mr[I,S]
                    score=t-S.bit_count()+r-gamma(S,J,n,cup,cdown)
                    if score>best: best=score;support=S;best_rank=r
                    if sub==0:break
                    sub=(sub-1)&gaps
                ans[I,J]=(best,bcost)
                arg[I,J]=(support,best_rank)
    return ans,arg


def screen(n,ans):
    stats=Counter(); ex=None;oldw=None
    from prior_window_gate import check_windows
    for pi in permutations(range(n)):
        old=not check_windows(pi)
        new=True;bad=None
        for u in range(n):
            I=0;J=0
            for v in range(u,n):
                I|=1<<v;J|=1<<pi[v]
                required,budget=ans[I,J]
                if required>budget:
                    new=False;bad=(I,J,required,budget);break
            if not new:break
        stats[old,new]+=1
        if old and not new and ex is None:ex=(pi,bad)
        if not old and new and oldw is None:oldw=(pi,bad)
    return dict(stats),ex,oldw

if __name__=='__main__':
    import time,json
    start=time.monotonic()
    n=8;mr=all_m_rank(n)
    print('ranks:',len(mr),'seconds',round(time.monotonic()-start,2),flush=True)
    scores,arg=best_scores(n,mr)
    print('scores:',len(scores),'seconds',round(time.monotonic()-start,2),flush=True)
    st,ex,oldw=screen(n,scores)
    print('counts',st,'new w',ex,'old w',oldw,'seconds',round(time.monotonic()-start,2),flush=True)
    if ex:
        pi,(I,J,v,b)=ex
        print('witness supporting set',arg[I,J])
