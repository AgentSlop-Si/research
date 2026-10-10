"""Fresh exact controls. Imports only the newly authored candidate helper."""
from pathlib import Path
import hashlib,itertools,json,random
from chirp_candidates import eligible_chirps,planned_seed_bound

def costs(n):
    result=[]
    for s in range(n):
        j=s%n;order=1
        while j: j=(j+s)%n;order+=1
        result.append(2 if s==4 else min(4 if s<4 else s,n-s+4 if s>4 else n,order))
    return result

def fixture(n,p,e,s,mu):
    phi=1;q=pow(e,8,p);a=[]
    for t in range(n):
        if t: phi=phi*(1-pow(q,t,p))%p
        a.append(pow(mu,t,p)*pow(e,s*t*t,p)*pow(phi,-1,p)%p)
    return a

def gate(a,p,e,allowed):
    if not any(a):return 'zero'
    if any(a[t]==0 for t in range(3)):return None
    n=len(a);q=pow(e,8,p);w=e*e%p
    r=(1-q)*a[1]*pow(a[0],-1,p)%p
    delta=(1-q*q)*a[2]*pow(a[1],-1,p)*pow(r,-1,p)%p
    s=next((s for s in allowed if pow(w,s,p)==delta),None)
    if s is None:return None
    for t in range(1,n):
        if ((1-pow(q,t,p))*a[t]-r*pow(w,s*(t-1),p)*a[t-1])%p:return None
    return s,r

def direct(a,p,e):
    return [sum(x*pow(e,2*j*t,p) for t,x in enumerate(a))%p for j in range(len(a))]

def fallback(a,p,e):
    out=[]
    for j in range(len(a)):
        z=pow(e,2*j,p);v=0
        for x in reversed(a):v=(v*z+x)%p
        out.append(v)
    return out

def onepole(a,p,e,r):
    n=len(a);w=e*e%p;b=a[-1]*r*pow(w,-4,p)%p
    y=[None]*n;y[0]=sum(a)%p;j=0;seeds=1
    for _ in range(n-1):
        k=(j+4)%n;den=(1+r*pow(w,j,p))%p
        if den:y[k]=(y[j]+b)*pow(den,-1,p)%p
        else:y[k]=sum(x*pow(w,k*t,p) for t,x in enumerate(a))%p;seeds+=1
        j=k
    return y,seeds

def run():
    r={'scope':'Candidate-generation engineering correction only. No original program run, imported or modified.','oracle':'Additive order by repeated addition, independent of helper gcd/divisor enumeration.'}
    pairs=decisions=0
    for n in range(3,512,2):
        expected_cost=costs(n)
        assert [planned_seed_bound(n,s) for s in range(n)]==expected_cost
        previous=set()
        for b in range(n+5):
            expected=tuple(s for s,c in enumerate(expected_cost) if c<=b)
            actual=eligible_chirps(n,b)
            assert actual==expected,(n,b)
            assert previous<=set(actual);previous=set(actual)
            if b>=2 and n>=5:assert 4 in actual
            pairs+=1;decisions+=n
    r['exhaustive_planner']={'N':'every odd 3 through 511','B':'every integer 0 through N+4','lengths':255,'N_budget_pairs':pairs,'chirp_membership_decisions':decisions,'exact':True}
    rng=random.Random(17623002);restrictions=0
    for n in range(3,100,2):
        expected_cost=costs(n)
        for b in range(n+3):
            sup=[s for s in range(n) if rng.randrange(2)];sup+=sup[:3]
            assert eligible_chirps(n,b,(s for s in sup))==tuple(s for s,c in enumerate(expected_cost) if c<=b and s in sup)
            restrictions+=1
    r['restriction_checks']=restrictions
    invalid=0
    for args in [(2,3),(1,3),(4,2),(9,-1),(True,2),(9,True),(9,2.0),(9,'2'),(9,2,[-1]),(9,2,[9]),(9,2,[4.0]),(9,2,[True])]:
        try:eligible_chirps(*args)
        except (TypeError,ValueError):invalid+=1
        else:raise AssertionError(args)
    r['invalid_argument_rejections']=invalid
    huge=[]
    for n in [3**100,3**100+2,10**100+1,177147]:
        for b in [0,1,2,3,4,12]:
            v=eligible_chirps(n,b);assert all(planned_seed_bound(n,s)<=b for s in v)
            assert (4 in v)==(b>=2);huge.append({'N':str(n),'B':b,'candidate_count':len(v)})
    assert eligible_chirps(9,10**100)==tuple(range(9))
    r['large_integer_checks']=huge
    print('Planner controls passed',flush=True)
    polecases=offgrid=singular=0;fields=[]
    for n,p in [(5,31),(9,37),(15,61),(27,109)]:
        e=next(e for e in range(2,p) if pow(e,2*n,p)==1 and all(pow(e,k,p)!=1 for k in range(1,2*n)))
        assert all(p%d for d in range(2,int(p**.5)+1));fields.append({'N':n,'p':p,'eta':e})
        for mu in range(1,p):
            a=fixture(n,p,e,4,mu)
            for b in (2,3):
                params=gate(a,p,e,eligible_chirps(n,b));assert params is not None and params[0]==4
                y,seeds=onepole(a,p,e,params[1]);assert y==direct(a,p,e) and seeds<=2
                polecases+=1;offgrid+=pow(mu,2*n,p)!=1;singular+=seeds==2
    r['s4_controls']={'fields':fields,'budgets':[2,3],'cases':polecases,'off_grid_phase_cases':offgrid,'two_seed_singular_cases':singular,'all_exact':True}
    raw=[]
    for n,p,e,budgets in [(3,7,3,[0,1,2,3,4]),(5,11,2,[2,3])]:
        c=costs(n);state={}
        for b in budgets:
            family={(0,)*n}
            for s,cost in enumerate(c):
                if cost>b:continue
                for mu in range(1,p):
                    a=fixture(n,p,e,s,mu)
                    for gamma in range(1,p):family.add(tuple(gamma*x%p for x in a))
            state[b]=[eligible_chirps(n,b),family,0,0]
        for a in itertools.product(range(p),repeat=n):
            for b in budgets:
                allowed,family,accepted,rejected=state[b];params=gate(a,p,e,allowed)
                assert (params is not None)==(a in family),(n,b,a)
                if params is None:
                    assert fallback(a,p,e)==direct(a,p,e);state[b][3]+=1
                else:
                    state[b][2]+=1
                    if params!='zero' and params[0]==4:
                        y,seeds=onepole(a,p,e,params[1]);assert y==direct(a,p,e)
        for b in budgets:raw.append({'N':n,'p':p,'eta':e,'B':b,'vectors':p**n,'accepted':state[b][2],'fallback':state[b][3]})
        print('Raw gate/fallback N='+str(n)+' passed',flush=True)
    r['exhaustive_raw_gate_fallback']=raw
    unsupported=forged=0;n,p,e=9,37,4
    for b in (2,3):
        allowed=eligible_chirps(n,b)
        for s in range(n):
            a=fixture(n,p,e,s,2)
            if s not in allowed:
                assert gate(a,p,e,allowed) is None and fallback(a,p,e)==direct(a,p,e);unsupported+=1
        a=fixture(n,p,e,4,2)
        for i in range(n):
            bad=a[:];bad[i]=(bad[i]+1)%p
            assert gate(bad,p,e,allowed) is None and fallback(bad,p,e)==direct(bad,p,e);forged+=1
    r['unsupported_chirp_fallbacks']=unsupported;r['all_position_mutation_fallbacks']=forged
    r['fallback_limit']='Fresh exact Horner fallback stand-in checked against power sums; original NTT not rerun.'
    for name in ('chirp_candidates.py','test_chirp_candidates.py'):r[name+'_sha256']=hashlib.sha256(Path(name).read_bytes()).hexdigest()
    Path('TEST_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['exhaustive_planner','s4_controls','exhaustive_raw_gate_fallback']},indent=2))
if __name__=='__main__':run()
