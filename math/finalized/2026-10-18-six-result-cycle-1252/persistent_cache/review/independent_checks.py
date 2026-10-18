#!/usr/bin/env python3
"""Independent exact checks. Does not import or invoke candidate source."""
from fractions import Fraction
from itertools import product, combinations
from functools import lru_cache
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def lru(seq,k):
    stack=[]; loads=0
    for x in seq:
        if x in stack: stack.remove(x)
        else: loads+=1
        stack.insert(0,x)
        del stack[k:]
    return loads

def optimum_demand(seq,h,weights=None):
    weights=weights or {x:1 for x in seq}
    @lru_cache(None)
    def solve(t,cache):
        if t==len(seq): return 0
        x=seq[t]; old=set(cache)
        if x in old: return solve(t+1,cache)
        if len(old)<h: return weights[x]+solve(t+1,tuple(sorted(old|{x})))
        return weights[x]+min(solve(t+1,tuple(sorted(old-{y}|{x}))) for y in old)
    return solve(0,())

def optimum_prefetch(seq,h,u):
    masks=[m for m in range(1<<u) if m.bit_count()<=h]
    dp={0:0}
    for x in seq:
        dp={n:min(cost+(n&~m).bit_count() for m,cost in dp.items())
            for n in masks if (n>>x)&1}
    return min(dp.values())

def phase_witness(seq,k):
    if not seq:return 0,[]
    sets=[]; cur=set()
    for x in seq:
        if x not in cur and len(cur)==k:
            sets.append(cur);cur=set()
        cur.add(x)
    sets.append(cur)
    filled=[]
    for s in sets:
        z=set(s)
        for x in range(k+1):
            if len(z)==k:break
            z.add(x)
        filled.append(z)
    return k+sum(len(b-a) for a,b in zip(filled,filled[1:])),[sorted(s) for s in filled]

def potential_checks():
    requests=loads=mins=0
    for k in range(1,9):
        order=tuple(range(k)); universe=range(k+4)
        def rank(x):return x+1 if x<k else k+1
        for h in range(1,k+1):
            for O in combinations(universe,h):
                p=sum(map(rank,O));assert p>=h*(h+1)//2;mins+=1
                for x in O:
                    new=(x,)+tuple(y for y in order if y!=x)
                    new=new[:k]
                    newrank={y:i+1 for i,y in enumerate(new)}
                    delta=sum(newrank.get(y,k+1) for y in O)-p
                    assert delta<= (0 if x<k else -(k-h+1));requests+=1
                for x in O:
                    for y in universe:
                        if y not in O:
                            assert rank(y)-rank(x)<=k;loads+=1
    return dict(K_range=[1,8],universe='K+4; up to four distinct absent views',
                request_transitions=requests,offline_load_transitions=loads,potential_minima=mins,
                symmetry='Canonical LRU order suffices by relabeling')

def exhaustive_checks():
    seqs=ineq=phase=oracle=0
    maxrat=Fraction(0);wit=None
    for u,maxlen in [(2,9),(3,7),(4,6)]:
        for n in range(maxlen+1):
            for seq in product(range(u),repeat=n):
                opts={h:optimum_demand(seq,h) for h in range(1,u+1)}
                for k in range(1,u+1):
                    a=lru(seq,k)
                    for h in range(1,k+1):
                        assert (k-h+1)*a<=k*opts[h];ineq+=1
                    if opts[k] and Fraction(a,opts[k])>maxrat:
                        maxrat=Fraction(a,opts[k]);wit=dict(K=k,sequence=seq,online=a,offline=opts[k])
                if n:
                    k=u-1;loads,_=phase_witness(seq,k)
                    assert opts[k]<=loads<=k+(n-1)//k;phase+=1
                # Separate arbitrary-subset/preload oracle, not just demand.
                if n<=4:
                    for h in range(1,u+1):
                        assert optimum_prefetch(seq,h,u)==opts[h];oracle+=1
                seqs+=1
    return dict(sequences=seqs,competitive_inequalities=ineq,phase_certificates=phase,
                independent_prefetch_oracle_comparisons=oracle,
                max_observed_equal_capacity_ratio=str(maxrat),max_witness=wit)

def conv(a,b):
    n=len(a);r=[0]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[(i+j)%n]+=x*y
    return tuple(r)

def det(matrix):
    a=[[Fraction(x) for x in r] for r in matrix];d=Fraction(1);n=len(a)
    for c in range(n):
        p=next((i for i in range(c,n) if a[i][c]),None)
        if p is None:return Fraction(0)
        if p!=c:a[p],a[c]=a[c],a[p];d=-d
        q=a[c][c];d*=q
        for j in range(c,n):a[c][j]/=q
        for i in range(c+1,n):
            q=a[i][c]
            for j in range(c,n):a[i][j]-=q*a[c][j]
    return d

def realizations():
    instances=answers=distinct=0;examples=[]
    for n in range(2,10):
        a=(n,)+(1,)*(n-1);b=(1,)+(0,)*(n-1)
        matrix=[[a[(r-c)%n] for c in range(n)] for r in range(n)]
        D=det(matrix);assert D==Fraction((n-1)**(n-1)*(2*n-1))
        assert conv(a,b)==a
        for k in range(1,9):
            kernels=[tuple(1+(i+1)**(j+1) for j in range(n)) for i in range(k+1)]
            vals=[conv(conv(a,b),H) for H in kernels]
            assert all(all(H) for H in kernels)
            assert len(set(vals))==k+1;distinct+=1
            for H,v in zip(kernels,vals):
                # Independent direct-coordinate oracle and a cheap algebraic shortcut.
                assert v==tuple(sum(a[j]*H[(t-j)%n] for j in range(n)) for t in range(n))
                assert v==tuple(sum(H)+(n-1)*H[t] for t in range(n));answers+=n
            if n==4 and k==2:examples.append(dict(N=n,K=k,A=a,B=b,H=kernels,views=vals,determinant=str(D)))
            instances+=1
    return dict(rational_integer_instances=instances,exact_coordinates=answers,
                pairwise_distinct_view_checks=distinct,explicit_examples=examples,
                shortcut='For A=(N,1,...,1), V[t]=sum(H)+(N-1)H[t]; excluded by mandatory-build grammar')

def adversarial_checks():
    rows=[]
    for k in range(1,9):
        for policy in ['LRU','MRU','discard_all','prefetch_lowest']:
            state=[];seq=[];builds=0
            for t in range(120):
                x=next(v for v in range(k+1) if v not in state)
                seq.append(x);builds+=1
                if policy=='discard_all':state=[]
                elif policy=='prefetch_lowest':
                    # Serve x, then pay any new loads to restore a fixed k-view cache.
                    before=set(state)
                    if len(state)==k:state.pop()
                    state.append(x)
                    target=set(range(k));builds+=len(target-set(state));state=sorted(target)
                else:
                    if len(state)==k:state.pop(0 if policy=='LRU' else -1)
                    state.append(x)
            cert,_=phase_witness(seq,k)
            assert builds>=len(seq) and cert<=k+(len(seq)-1)//k
            rows.append(dict(K=k,policy=policy,T=len(seq),online_loads=builds,offline_phase_upper=cert))
    return rows

def escape_counterexamples():
    # Allowing cheaper builds by handle invalidates the claimed unweighted ratio.
    seq=(0,1,2,1)*20;weights={0:1000,1:1,2:1}
    stack=[];weighted_lru=0
    for x in seq:
        if x in stack:stack.remove(x)
        else:weighted_lru+=weights[x]
        stack.insert(0,x);del stack[2:]
    weighted_opt=optimum_demand(seq,2,weights)
    assert weighted_lru>2*weighted_opt
    # Omitting compulsory reads/outputs makes the K full-work assertion false.
    k=4;F=4;g=100;diluted=Fraction(F+g,Fraction(F,k)+g)
    assert diluted==Fraction(104,101) and diluted<k
    # Algebraic/partial caching escape under explicit simple arithmetic tariff.
    k=2;n=4;T=300;seq=tuple(t%3 for t in range(T))
    fullF=2*n*n # N^2 products, N(N-1) sums, N writes
    scalarF=2*n # N products, N-1 sums, one write
    full=lru(seq,k)*fullF+T;partial=3*scalarF+T
    assert 3<=k*n and full>k*partial
    # Free extra complete slot prevents the adversarial always-miss implication.
    extra=lru(seq,k+1);assert extra==3
    # Distinct full views need not differ on a chosen coordinate.
    a=(2,1);hs=[(2,1),(1,3)]
    vs=[conv(a,h) for h in hs];assert vs[0]!=vs[1] and vs[0][0]==vs[1][0]
    return dict(
        weighted_prices=dict(K=2,sequence=[0,1,2,1],repetitions=20,
                             prices=weights,LRU=weighted_lru,OPT=weighted_opt,ratio=str(Fraction(weighted_lru,weighted_opt))),
        common_output=dict(K=4,F=F,g=g,asymptotic_lower=str(diluted)),
        partial_coordinate_storage=dict(K=k,N=n,T=T,LRU_full_cost=full,partial_allowed_cost=partial,
                                      persistent_scalar_answers=3,available_scalar_slots=k*n,ratio=str(Fraction(full,partial))),
        hidden_extra_slot=dict(declared_K=k,actual_K=k+1,T=T,actual_loads=extra),
        free_initial_comparator=dict(K=2,request=[0],online_empty_loads=1,offline_warm_loads=0),
        coordinate_alias=dict(A=a,H=hs,views=vs,coordinate=0,equal_answer=vs[0][0]),
        conclusion='All are excluded by the stated grammar; they reject extension to broader solvers or unqualified runtime ratios.')

def version_controls():
    reg={}; stored=[]; paid_comparisons=0; raw_scalars=0
    def register(key):
        nonlocal paid_comparisons,raw_scalars
        # Deliberately exact linear registry, with comparison work charged.
        for i,old in enumerate(stored):
            paid_comparisons+=1
            if old==key:return i
        stored.append(key);raw_scalars+=sum(len(a) for a in key)
        return len(stored)-1
    checks=outputs=0
    for n in range(1,7):
        A=tuple(range(1,n+1));B=tuple(2*j+1 for j in range(n));H=tuple(3*j+2 for j in range(n))
        original=(A,B,H);base=register(original)
        for which in range(3):
            for pos in range(n):
                arrays=[list(x) for x in original]
                arrays[which][pos]+=7
                change=register(tuple(map(tuple,arrays)));assert change!=base
                arrays[which][pos]-=7
                restore=register(tuple(map(tuple,arrays)));assert restore==base
                stream=[(base,[0]),(change,[]),(restore,[0]),(change,[0]),(base,[])]
                active=[v for v,coords in stream if coords]
                assert active==[base,base,change] and lru(active,2)==2
                for v,coords in stream:
                    a,b,h=stored[v]
                    answer=conv(conv(a,b),h)
                    for t in coords:
                        oracle=sum(a[i]*b[j]*h[(t-i-j)%n] for i in range(n) for j in range(n))
                        assert answer[t]==oracle;outputs+=1
                checks+=1
    return dict(cancel_restore_controls=checks,exact_requested_answers=outputs,
                paid_version_comparisons=paid_comparisons,paid_raw_scalar_slots=raw_scalars,
                zero_output_queries='Ingested but omitted from active cache-request sequence')


def main():
    result=dict(verdict='PASS_RESTRICTED_SCOPE',potential=potential_checks(),
                exhaustive=exhaustive_checks(),realization=realizations(),
                adaptive_adversaries=adversarial_checks(),version_controls=version_controls(),scope_escape_counterexamples=escape_counterexamples(),
                failures=0,uses_candidate_code=False)
    (HERE/'INDEPENDENT_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['verdict','potential','exhaustive','realization','version_controls','scope_escape_counterexamples','failures']},indent=2))
if __name__=='__main__':main()
