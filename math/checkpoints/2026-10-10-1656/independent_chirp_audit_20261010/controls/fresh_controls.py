"""Independent audit controls. Does not import, compile, or execute supplied source.
Theoretical algorithm is reconstructed from the displayed equations; the comparison
NTT is an independently written generic Cooley-Tukey with direct small butterflies.
All arithmetic is integer modular arithmetic. No floating-point Fourier oracle.
"""
from pathlib import Path
import hashlib, itertools, json, math, random, time
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source'/'extracted'
RNG=random.Random(87103426)

def factors(v):
    out=[]; t=2
    while t*t<=v:
        if v%t==0:
            out.append(t)
            while v%t==0: v//=t
        t+=1
    if v>1: out.append(v)
    return out

def is_prime(p):
    return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))

def field(n,p=None):
    if p is None:
        p=2*n+1
        while not is_prime(p): p+=2*n
    assert is_prime(p) and (p-1)%(2*n)==0
    for a in range(2,p):
        eta=pow(a,(p-1)//(2*n),p)
        if pow(eta,2*n,p)==1 and all(pow(eta,2*n//f,p)!=1 for f in factors(2*n)):
            return p,eta
    raise AssertionError('root not found')

def fixture(n,p,eta,s,gamma,mu):
    """Closed coefficient formula, not the adjacent recognition recurrence."""
    q=pow(eta,8,p); phi=1; a=[]
    for t in range(n):
        if t: phi=phi*(1-pow(q,t,p))%p
        a.append(gamma*pow(mu,t,p)*pow(eta,(s*t*t)%(2*n),p)*pow(phi,-1,p)%p)
    return a

def budget_cost(n,s):
    if s==4:return 2
    return min(max(4,s), n-s+4 if s>4 else n, n//math.gcd(n,s))

def source_gate_model(n,budget):
    """Literal set logic under audit, implemented here without source execution."""
    candidates={s for s in range(n) if s<=budget}
    candidates|={n-t for t in range(1,min(n,budget-4)+1)}
    candidates|={k*(n//d) for d in range(1,budget+1) if n%d==0 for k in range(d)}
    return {s for s in candidates if 0<=s<n and budget_cost(n,s)<=budget}

def recognize(a,p,eta,eligible):
    """Cross-product detector, deliberately avoids original ratio division chain."""
    n=len(a); a=[v%p for v in a]
    if all(v==0 for v in a):return 'zero'
    if any(a[k]==0 for k in (0,1,2)):return None
    q=pow(eta,8,p); w=eta*eta%p
    u=(1-q)*a[1]%p; v=(1-q*q)*a[2]%p
    match=[s for s in eligible if v*a[0]%p==u*a[1]*pow(w,s,p)%p]
    if not match:return None
    assert len(match)==1
    s=match[0]; rho=u*pow(a[0],-1,p)%p
    for t in range(1,n):
        if ((1-pow(q,t,p))*a[t]-rho*pow(w,s*(t-1),p)*a[t-1])%p:return None
    return s,rho,rho*pow(eta,-s,p)%p

def direct(a,p,w,indices=None):
    if indices is None:indices=range(len(a))
    out=[]
    for j in indices:
        z=pow(w,j,p); term=1; value=0
        for x in a:
            value=(value+x*term)%p; term=term*z%p
        out.append(value)
    return out

def ntt(a,p,w):
    """Independent ordinary-length positive-sign NTT, generic direct butterflies."""
    n=len(a)
    if n==1:return a[:]
    radix=next((d for d in range(2,math.isqrt(n)+1) if n%d==0),n)
    size=n//radix
    chunks=[ntt(a[t::radix],p,pow(w,radix,p)) for t in range(radix)]
    y=[0]*n
    # The same N requested bins. No padding or 2N transform.
    z=1
    for k in range(n):
        power=1; value=0
        for t in range(radix):
            value=(value+chunks[t][k%size]*power)%p; power=power*z%p
        y[k]=value; z=z*w%p
    return y

def evaluate(a,p,eta,s,rho):
    """Fresh graph evaluator from the theorem, with independent direct-sum seeds."""
    n=len(a); w=eta*eta%p; boundary=a[-1]*rho*pow(w,-s,p)%p
    omega=[pow(w,j,p) for j in range(n)]
    y=[None]*n
    def seed(j):y[j]=direct(a,p,w,[j])[0]
    if s==4:
        seed(0); j=0; seeds=1; singular=[]
        for _ in range(n-1):
            nxt=(j+4)%n; den=(1+rho*omega[j])%p
            if den:y[nxt]=(y[j]+boundary)*pow(den,-1,p)%p
            else:seed(nxt); seeds+=1; singular.append(j)
            j=nxt
        mode='one-pole'
    else:
        d=n//math.gcd(n,s); fwd=max(4,s); back=n-s+4 if s>4 else n
        if d<=min(fwd,back):
            mode='coset'; seeds=d
            subgroup=[h*s%n for h in range(d)]
            for h in subgroup:seed(h)
            visited=set(subgroup)
            for r in range(1,math.gcd(n,s)):
                current={(h+4*(r-1))%n for h in subgroup}
                successor={(h+4*r)%n for h in subgroup}
                assert not (visited&successor)
                for j in current:
                    assert y[j] is not None and y[(j+s)%n] is not None
                    y[(j+4)%n]=(y[j]-rho*omega[j]*y[(j+s)%n]+boundary)%p
                visited|=successor
            assert visited==set(range(n))
        elif back<fwd:
            mode='backward'; seeds=back
            for j in range(back):seed(j)
            for k in range(back,n):
                j=k-4; y[k]=(y[j]-rho*omega[j]*y[j-(n-s)]+boundary)%p
        else:
            mode='forward'; seeds=fwd
            for j in range(fwd):seed(j)
            if s<4:
                for k in range(4,n):
                    j=k-4; y[k]=(y[j]-rho*omega[j]*y[j+s]+boundary)%p
            else:
                for k in range(s,n):
                    j=k-s; y[k]=(y[j]-y[j+4]+boundary)*pow(rho*omega[j],-1,p)%p
    assert all(v is not None for v in y)
    return y,mode,seeds

def rank_mod(A,p):
    A=[r[:] for r in A]; rank=0
    for col in range(len(A[0])):
        found=next((i for i in range(rank,len(A)) if A[i][col]%p),None)
        if found is None:continue
        A[rank],A[found]=A[found],A[rank]
        inv=pow(A[rank][col],-1,p)
        A[rank]=[v*inv%p for v in A[rank]]
        for i in range(rank+1,len(A)):
            v=A[i][col]; A[i]=[(x-v*y)%p for x,y in zip(A[i],A[rank])]
        rank+=1
    return rank

def power_cost(k):return k.bit_count()+k.bit_length()-1

def run():
    receipt={'scope':'Exact ordinary N-point positive-sign DFT over verified prime fields. Source programs never executed or imported.','source_files':{},'manifest_errors':[], 'external_audit_equals_zip_audit':False,'controls':{}}
    for path in sorted(SRC.iterdir()):
        if path.is_file():receipt['source_files'][path.name]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    for line in (SRC/'SHA256SUMS.txt').read_text().splitlines():
        claimed,name=line.split(None,1)
        if receipt['source_files'][name]['sha256']!=claimed:receipt['manifest_errors'].append(name)
    receipt['external_audit_equals_zip_audit']=(ROOT/'source'/'COSET_AUDIT_RESULTS.json').read_bytes()==(SRC/'COSET_AUDIT_RESULTS.json').read_bytes()
    assert not receipt['manifest_errors'] and receipt['external_audit_equals_zip_audit']
    controls=receipt['controls']; controls['exhaustive_raw']=[]
    for n,p in [(3,7),(5,11)]:
        p,eta=field(n,p); eligible=source_gate_model(n,12)
        family={tuple(fixture(n,p,eta,s,gamma,mu)) for s in eligible for gamma in range(1,p) for mu in range(1,p)}
        family.add((0,)*n); accepted=0; fallback=0
        for a in itertools.product(range(p),repeat=n):
            params=recognize(a,p,eta,eligible)
            assert (params is not None)==(a in family)
            if params is not None:
                accepted+=1
                if params!='zero':
                    y,_,_=evaluate(a,p,eta,*params[:2]);assert y==direct(a,p,eta*eta%p)
            else:
                fallback+=1
                assert ntt(list(a),p,eta*eta%p)==direct(a,p,eta*eta%p)
        controls['exhaustive_raw'].append({'N':n,'p':p,'eta':eta,'raw_vectors':p**n,'accepted':accepted,'fallback':fallback})
    print('Exhaustive raw-input tests complete',flush=True)
    small=[]; checked=0; altered=0
    for n in [7,9,11,15,21,25,27,35,49,63,81,99,105]:
        p,eta=field(n); w=eta*eta%p; allowed=source_gate_model(n,12)
        for s in range(n):
            for mu in list(dict.fromkeys([1,eta,p-1,next((u for u in range(2,p) if pow(u,2*n,p)!=1),1)])):
                gamma=RNG.randrange(1,p); a=fixture(n,p,eta,s,gamma,mu)
                params=recognize(a,p,eta,allowed)
                assert (params is not None)==(s in allowed)
                reference=direct(a,p,w)
                assert ntt(a,p,w)==reference
                if params is not None:
                    assert params[0]==s and params[2]==mu
                    y,mode,seeds=evaluate(a,p,eta,*params[:2]);assert y==reference
                    boundary=a[-1]*params[1]*pow(w,-s,p)%p
                    assert all((y[(j+4)%n]-y[j]+params[1]*pow(w,j,p)*y[(j+s)%n]-boundary)%p==0 for j in range(n))
                checked+=n
            # Every single coefficient mutation must reject unless it accidentally is a different member.
            # n>=7 makes family ratios overdetermined; exact rejection expected.
            if s in allowed:
                for index in [0,1,2,n//2,n-1]:
                    forged=a[:]; forged[index]=(forged[index]+1)%p
                    assert recognize(forged,p,eta,allowed) is None
                    assert ntt(forged,p,w)==direct(forged,p,w);altered+=1
        small.append({'N':n,'p':p,'eta':eta,'chirps_checked':n,'eligible_chirps':len(allowed)})
    controls['small_all_chirps']=small;controls['small_full_coefficients']=checked;controls['single_sample_forgery_rejections']=altered
    print('All-residue and mutation controls complete',flush=True)
    resonances=[]
    for n in [5,9,15,27,49,81]:
        p,eta=field(n);w=eta*eta%p
        for pole in range(n):
            rho=-pow(w,-pole,p)%p;mu=rho*pow(eta,-4,p)%p
            a=fixture(n,p,eta,4,3,mu);params=recognize(a,p,eta,source_gate_model(n,12))
            y,mode,seeds=evaluate(a,p,eta,*params[:2]);assert y==direct(a,p,w)
            assert seeds==(1 if pole==(-4)%n else 2)
        resonances.append({'N':n,'all_pole_positions':n,'closing_edge_pole_needs_second_seed':False})
    controls['resonances']=resonances
    gate_bugs=[]
    for n in range(5,100,2):
        for b in range(0,15):
            actual=source_gate_model(n,b);expected={s for s in range(n) if budget_cost(n,s)<=b}
            missing=sorted(expected-actual)
            if missing:gate_bugs.append({'N':n,'budget':b,'missing':missing})
            assert not(actual-expected)
    assert all(c['budget'] in (2,3) and c['missing']==[4] for c in gate_bugs)
    controls['gate_completeness_counterexamples']=gate_bugs
    p,eta=field(9);a=fixture(9,p,eta,4,1,2)
    controls['gate_bug_witness']={'N':9,'p':p,'eta':eta,'s':4,'gamma':1,'mu':2,'input':a,'declared_seed_cost':2,'accepted_budget_2':recognize(a,p,eta,source_gate_model(9,2)) is not None,'accepted_budget_4':recognize(a,p,eta,source_gate_model(9,4)) is not None}
    # Primitive-root order checks do not constitute primality validation.
    composite=None
    for p in range(7,500,6):
        if is_prime(p):continue
        for eta in range(2,p):
            if pow(eta,6,p)==1 and pow(eta,3,p)!=1 and pow(eta,2,p)!=1:
                q=pow(eta,8,p)
                if math.gcd((1-q)%p,p)>1:
                    composite={'N':3,'p':p,'eta':eta,'q':q,'gcd_1_minus_q_p':math.gcd((1-q)%p,p)};break
        if composite:break
    controls['composite_modulus_out_of_domain_witness']=composite
    # Noncyclic coefficient chirp signs absorbed by the unrestricted geometric phase.
    aliases=0
    for n in [9,15,27]:
        p,eta=field(n)
        for s in range(n):
            assert fixture(n,p,eta,s+n,3,2)==fixture(n,p,eta,s,3,(-2)%p);aliases+=1
    controls['chirp_alias_wrap_checks']=aliases
    hankel=[]
    for n in [9,27,81]:
        p,eta=field(n);s=n//3;r=(n+1)//2
        b=[pow(2,t,p)*pow(eta,(s-2)*t*t,p)%p for t in range(n)]
        rank=rank_mod([[b[i+j] for j in range(r)] for i in range(r)],p)
        assert rank==r;hankel.append({'N':n,'s':s,'rank':rank})
    controls['hankel']=hankel
    print('Resonance, gate, wrap, and Hankel controls complete',flush=True)
    # Match the supplied audit parameters for count reconstruction, but calculate roots independently.
    old=json.loads((SRC/'AUDIT_RESULTS.json').read_text());prime_map={v['N']:v['p'] for v in old['cases']}
    audit=json.loads((SRC/'COSET_AUDIT_RESULTS.json').read_text());large=[];full=0;direct_count=0
    for n in [81,243,729,2187,6561,19683,59049,177147]:
        p,eta=field(n,prime_map[n]);w=eta*eta%p
        mu=next(u for u in range(2,p) if pow(u,2*n,p)!=1)
        for name,s in [('fixed',7),('near-n',n-2),('coset-3',n//3),('coset-9',n//9)]:
            a=fixture(n,p,eta,s,17,mu);params=recognize(a,p,eta,source_gate_model(n,12));assert params[0]==s
            y,mode,seeds=evaluate(a,p,eta,*params[:2]);ref=ntt(a,p,w);assert y==ref
            indices=sorted(set([0,1,2,n//2,n-1]+[RNG.randrange(n) for _ in range(8)]))
            assert [y[j] for j in indices]==direct(a,p,w,indices)
            prep=2*n-1+sum(power_cost(k) for k in [2*n]+[2*n//f for f in factors(2*n)])
            recognition=5*n+5
            seed_ops=2*seeds*(n-1)
            if mode=='coset':propagation=2+4*(n-seeds)
            elif mode=='backward':propagation=2+4*(n-seeds)+max(0,n-seeds-1)
            elif mode=='forward' and s>4:propagation=2+1+3*(n-s)+max(0,n-s-1)
            else:raise AssertionError(mode)
            fast=prep+recognition+seed_ops+propagation
            m=0;temp=n
            while temp>1:assert temp%3==0;temp//=3;m+=1
            baseline=prep+3+10*(n//3)*m
            claimed=next(c for c in audit['cases'] if c['N']==n and c['family']==name)
            assert fast==claimed['new_total'] and baseline==claimed['ntt_total']
            large.append({'N':n,'p':p,'eta':eta,'mu':mu,'mu_off_2N_root_grid':pow(mu,2*n,p)!=1,'family':name,'s':s,'strategy':mode,'seed_count':seeds,'all_outputs_exact':True,'direct_bins':len(indices),'rederived_prep':prep,'rederived_recognition':recognition,'rederived_seed_operations':seed_ops,'rederived_propagation':propagation,'rederived_fast_total':fast,'rederived_same_N_reference_total':baseline,'spectrum_sha256':hashlib.sha256(json.dumps(y,separators=(',',':')).encode()).hexdigest()})
            full+=n;direct_count+=len(indices)
        print('Large control N='+str(n)+' complete',flush=True)
    controls['large_same_N']=large;controls['large_complete_coefficients']=full;controls['large_selected_direct_bins']=direct_count
    receipt['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    (ROOT/'results'/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'full_large_coefficients':full,'selected_large_direct_bins':direct_count,'exhaustive_raw':controls['exhaustive_raw'],'gate_witness':controls['gate_bug_witness'],'composite_witness':composite},indent=2))
if __name__=='__main__':run()
