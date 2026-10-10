#!/usr/bin/env python3
"""Independently authored audit. Uploaded programs are NEVER imported or run.
Finite-field checks use only displayed equations and fresh schoolbook products.
Numerical covariance checks are diagnostics alongside the report's proofs.
"""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json, math, random
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RNG=random.Random(94117)

def factors(n):
    f={};p=2
    while p*p<=n:
        while n%p==0:f[p]=f.get(p,0)+1;n//=p
        p+=1
    if n>1:f[n]=1
    return f

def phi(n):
    t=n
    for p in factors(n):t=t//p*(p-1)
    return t

def mu(n):
    f=factors(n)
    return 0 if any(e>1 for e in f.values()) else (-1)**len(f)

def isprime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))

def field(n):
    p=2*n+1
    while not isprime(p):p+=2*n
    for eta in range(2,p):
        if pow(eta,2*n,p)==1 and all(pow(eta,2*n//q,p)!=1 for q in factors(2*n)):
            return p,eta
    raise AssertionError('root absent')

def partition(n,b):
    q,r=divmod(n,b)
    return [q+1]*r+[q]*(b-r)

def starts(lens):
    s=[];z=0
    for m in lens:s.append(z);z+=m
    return s

def conv(x,y,p):
    z=[0]*(len(x)+len(y)-1)
    for i,a in enumerate(x):
        for j,b in enumerate(y):z[i+j]=(z[i+j]+a*b)%p
    return z

def seq(nodes,w,n,p):
    b=len(nodes);q=[1]
    for z in nodes:q=conv(q,[1,-z%p],p)
    inv=[1]+[0]*(b-1)
    for i in range(1,b):inv[i]=-sum(q[j]*inv[i-j] for j in range(1,i+1))%p
    power=[1]*b;out=[]
    for k in range(min(b,n)):
        out.append(sum(a*t for a,t in zip(w,power))%p)
        power=[a*t%p for a,t in zip(nodes,power)]
    while len(out)<n:
        cursor=len(out);take=min(b,n-cursor)
        rhs=[-v%p for v in conv(out[-b:],q,p)[b:b+take]]
        out+=conv(rhs,inv,p)[:take]
    direct=[sum(w[j]*pow(nodes[j],k,p) for j in range(b))%p for k in range(n)]
    assert out==direct
    return out

def projected(x,lens,a,beta,p,eta):
    n=len(x);ss=starts(lens);h=n%2;ds=[];ys=[]
    for s,m in zip(ss,lens):
        ph=[pow(eta,(a*t*(t-1)+2*(a*s+beta)*t+h*t)%(2*n),p) for t in range(m)]
        d=sum(ph[t]*x[s+t] for t in range(m))%p;ds.append(d)
        ys.extend(d*pow(v,-1,p)%p for v in ph)
    return ds,ys

def green_case(n,lens,a,beta,p,eta,x):
    ss=starts(lens);b=len(lens);ds,y=projected(x,lens,a,beta,p,eta)
    nodes=[pow(eta,-2*s%(2*n),p) for s in ss];end=[0]*b
    for j,(s,m) in enumerate(zip(ss,lens)):
        c=pow(eta,(-a*m*(m-1)-2*(a*s+beta)*m-(n%2)*m)%(2*n),p)
        end[(j+1)%b]=c*ds[j]%p
    dseq=seq(nodes,ds,n,p);eseq=seq(nodes,end,n,p)
    force=seq(nodes,[(u-v)%p for u,v in zip(ds,end)],n,p)
    assert force==[(u-v)%p for u,v in zip(dseq,eseq)]
    gg=[pow(eta,(a*j*(j-1)+2*beta*j+(n%2)*j)%(2*n),p) for j in range(n+1)]
    assert gg[n]==p-1
    terms=[force[a*j%n]*pow(gg[j],-1,p)%p for j in range(n)]
    seed=sum(terms)*pow(2,-1,p)%p;pref=0;ans=[0]*n
    for j in range(n):
        ans[a*j%n]=gg[j]*(seed-pref)%p;pref=(pref+terms[j])%p
    direct=[sum(y[t]*pow(eta,-2*k*t%(2*n),p) for t in range(n))%p for k in range(n)]
    assert ans==direct
    return n

def masks(lens):
    n=sum(lens);out={}
    for d in range(-max(lens)+1,max(lens)):
        if not d:continue
        out[d]=[int(0<=t+d<m) for m in lens for t in range(m)]
    return out

def cert(n,lens):
    mm=masks(lens)
    vals=[sum((F(mm[d][i],phi(n//math.gcd(n,d))) for d in mm),F(0)) for i in range(n)]
    grouped=sum((F(max(sum(mm[d][i] for d in mm if math.gcd(n,d)==g) for i in range(n)),phi(n//g)) for g in set(math.gcd(n,d) for d in mm)),F(0))
    old=sum((F(1,phi(n//math.gcd(n,d))) for d in mm),F(0))
    return max(vals,default=F(0)),grouped,old

def covariance(n,lens):
    mm=masks(lens);den=n*phi(n)
    def ram(t):
        g=math.gcd(n,t)
        return sum(r*mu(n//r) for r in range(1,g+1) if g%r==0)
    return [[F(sum(mm[d][i]*mm[d][j]*ram(d*(i-j)) for d in mm),den) for j in range(n)] for i in range(n)]

def provenance():
    v=ROOT/'source_extracted/fft_rough_length_green_v14';h=ROOT/'hero0/source_extracted/fft_hero0_phase4_coprime_green'
    checks=[]
    for line in (v/'MANIFEST.sha256').read_text().splitlines():
        digest,path=line.split(None,1);path=path.strip()
        assert hashlib.sha256((v/path).read_bytes()).hexdigest()==digest
        checks.append(path)
    hv=json.loads((h/'SHA256SUMS.json').read_text())
    for path,z in hv.items():
        data=(h/path).read_bytes();assert len(data)==z['bytes'];assert hashlib.sha256(data).hexdigest()==z['sha256']
    static={}
    for base in [v,h]:
        for p in base.glob('*.py'):
            tree=ast.parse(p.read_text())
            static[str(p.relative_to(ROOT))]={'imports':[ast.unparse(x) for x in ast.walk(tree) if isinstance(x,(ast.Import,ast.ImportFrom))],'calls':sorted(set(ast.unparse(x.func) for x in ast.walk(tree) if isinstance(x,ast.Call)))}
    return {'v14_manifest_entries_verified':len(checks),'hero0_manifest_entries_verified':len(hv),'source_static_ast':static}

def exact_checks():
    cases=outputs=averages=frames=kernel_cases=0;primes=set()
    for n in range(3,66):
        p,eta=field(n);primes.add(p);unit=[a for a in range(1,n) if math.gcd(a,n)==1]
        bs=sorted({3,min(4,n),min(7,n),max(3,n//2),n-1,n})
        ls=[partition(n,b) for b in bs]
        if n>=9:
            # Include unbalanced contiguous partitions within the no-alias guard.
            q=n//3;ls.append([q]+[1]*(n-q))
        for lens in ls:
            assert sum(lens)==n and min(lens)>0 and 2*(max(lens)-1)<n
            x=[RNG.randrange(p) for _ in range(n)]
            for a in sorted({unit[0],unit[-1],unit[len(unit)//2]}):
                outputs+=green_case(n,lens,a,RNG.randrange(n),p,eta,x);cases+=1
            if n<=23:
                a=unit[-1];s=[0]*n
                for beta in range(n):
                    _,y=projected(x,lens,a,beta,p,eta)
                    s=[(t+z)%p for t,z in zip(s,y)]
                assert s==[n*t%p for t in x];averages+=1
    for q in range(4,85):
        p,eta=field(q)
        for m in range(2,math.isqrt(q)+1):
            if q%m:continue
            k=q//m;lens=[m]*k;x=[RNG.randrange(p) for _ in range(q)];total=[0]*q
            for r in range(m):
                _,y=projected(x,lens,1,(2+r*k)%q,p,eta)
                total=[(u+v)%p for u,v in zip(total,y)]
            assert total==[m*v%p for v in x];frames+=1
            # Exact nonzero null vector for one row: x0=S1, x1=-S0.
            xx=[0]*q;xx[0]=pow(eta,(4+(q%2))%(2*q),p);xx[1]=p-1
            _,yy=projected(xx,lens,1,2,p,eta);assert not any(yy);assert any(xx);kernel_cases+=1
    return {'green_cases':cases,'all_output_equalities':outputs,'exact_beta_average_cases':averages,'finite_field_primes':sorted(primes),'complete_frame_cases':frames,'one_row_exact_kernel_cases':kernel_cases,'fused_single_forcing_matches_two_streams':True}

def covariance_checks():
    count=0;max_ratio=0;prime_tight=0;unique_long=0;strict=[];small_checks=[]
    for n in range(3,55):
        for b in sorted({3,min(4,n),min(7,n),max(3,n//2),n-1,n}):
            lens=partition(n,b);v,c,t=cert(n,lens);assert v<=c<=t
            q=covariance(n,lens);ar=np.array(q,dtype=float)
            assert sum(q[i][i] for i in range(n))==F(sum(m*(m-1) for m in lens),n)
            eig=float(np.linalg.eigvalsh(ar)[-1]);assert eig<=float(v)+2e-12
            if v:max_ratio=max(max_ratio,eig/float(v))
            if isprime(n):
                assert v==F(max(lens)-1,n-1)
                mm=masks(lens);raw=np.diag([(m-1)/(n-1) for m in lens for _ in range(m)])
                for mask in mm.values():raw-=np.outer(mask,mask)/(n*(n-1))
                assert np.max(abs(raw-ar))<1e-14
                longs=lens.count(max(lens))
                if max(lens)>1:
                    if longs>=2:assert abs(eig-float(v))<1e-12;prime_tight+=1
                    else:assert eig<float(v)-1e-14;unique_long+=1
            if v<c and len(strict)<8:strict.append({'n':n,'blocks':b,'overlap':str(v),'prior_group_max':str(c)})
            count+=1
    # Independent full state averaging, using direct projection matrix rather than shell formula.
    for n,b in [(7,3),(9,4),(10,3),(11,4),(12,5),(15,4),(17,5)]:
        lens=partition(n,b);ss=starts(lens);z=np.exp(2j*np.pi/n);eta=np.exp(1j*np.pi/n)
        qs=np.zeros((n,n),complex);states=0
        for a in range(1,n):
            if math.gcd(a,n)>1:continue
            for beta in range(n):
                P=np.zeros((n,n),complex)
                for s,m in zip(ss,lens):
                    ph=np.array([z**((a*t*(t-1)//2+(a*s+beta)*t)%n)*eta**((n%2)*t) for t in range(m)])
                    P[s:s+m,s:s+m]=np.outer(ph.conjugate(),ph)
                coeff=(np.ones(n)@(P-np.eye(n)))/math.sqrt(n)
                qs+=np.outer(coeff.conjugate(),coeff);states+=1
        qs/=states;ref=np.array(covariance(n,lens),float);err=float(np.max(abs(qs-ref)))
        assert err<2e-13;small_checks.append({'n':n,'blocks':b,'states':states,'max_entry_discrepancy':err})
    return {'covariance_cases':count,'max_numeric_operator_ratio':max_ratio,'prime_sharp_cases':prime_tight,'prime_unique_long_strict_cases':unique_long,'strict_improvements_over_prior_group_max':strict,'direct_state_covariance_comparisons':small_checks}

def amplification():
    rows=[]
    for n in [101,1009,10007,100003]:
        candidates=sorted({min(n,max(3,round(n**a))) for a in [.1,.2,.3,.4,.5,.6]}|{8,16,32})
        candidate=[]
        for b in candidates:
            if b>n:continue
            v=F((n+b-1)//b-1,n-1);p=2*v
            if p>F(1,8):continue
            for r in range(1,1001,2):
                h=(r+1)//2;bound=n*math.comb(r,h)*p**h
                if bound<=F(1,n):break
            else:raise AssertionError('row bound not reached')
            cost=r*(n*math.log2(b)+b*b)
            candidate.append({'b':b,'rows':r,'variance':str(v),'exact_subset_failure_bound':str(bound),'cost_proxy':cost,'ratio_NlogN':cost/(n*math.log2(n))})
        rows.append({'n':n,'target_tolerance':1,'failure_target':str(F(1,n)),'best_sampled_proxy':min(candidate,key=lambda z:z['cost_proxy']),'candidates':candidate})
    return rows

def hero_weighted_covariance():
    rows=[]
    for n,q,m,sigma2,xi in [(7,35,5,4,2.3),(11,55,5,8,15),(11,60,5,8,15),(13,60,4,6,3.75),(17,85,5,8,25)]:
        center=(n-1)//2;src=(np.arange(n)-center)%q;tall=np.where(np.arange(q)<q/2,np.arange(q),np.arange(q)-q)/q
        ga=np.exp(np.pi*sigma2*tall*tall)/math.sqrt(sigma2);units=[a for a in range(1,q) if math.gcd(a,q)==1]
        cov=np.zeros((n,n),complex);diagonal=np.zeros(n)
        for d in range(-m+1,m):
            if not d:continue
            dest=src+d;valid=(dest>=0)&(dest<q)&(dest//m==src//m)
            ids=np.flatnonzero(valid)
            ratio=ga[src[ids]]/ga[dest[ids]]
            diagonal[ids]+=q/n*ratio**2/phi(q//math.gcd(q,d))
            for a in units:
                v=np.zeros(n,complex)
                v[ids]=ratio*np.exp(-2j*np.pi*xi*tall[dest[ids]])*np.exp(-2j*np.pi*a*d*src[ids]/q)
                cov+=np.outer(v.conjugate(),v)/(n*len(units))
        bound=float(max(diagonal));eig=float(np.linalg.eigvalsh(cov)[-1]);assert eig<=bound+2e-12
        tau=max(abs(tall[src]));R=math.exp(math.pi*sigma2*(2*tau*m/q+(m/q)**2))
        ov=cert(q,[m]*(q//m))[0];coarse=q/n*R*R*float(ov);assert bound<=coarse+2e-12
        # Exhaustive independent projector covariance for one fixed input.
        x=np.array([complex(RNG.random(),RNG.random()) for _ in range(n)]);z=np.zeros(q,complex);z[src]=x*ga[src]
        target=np.sum(x*np.exp(-2j*np.pi*xi*tall[src]))/math.sqrt(n);ave=0.;mean=0j
        for a in units:
            for beta in range(q):
                y=np.zeros(q,complex)
                for start in range(0,q,m):
                    tt=np.arange(m);ph=np.exp(2j*np.pi*((a*tt*(tt-1)//2+(a*start+beta)*tt)%q)/q)*np.exp(1j*np.pi*(q%2)*tt/q)
                    y[start:start+m]=ph.conjugate()*np.dot(ph,z[start:start+m])
                er=np.sum(y/ga*np.exp(-2j*np.pi*xi*tall))/math.sqrt(n)-target
                ave+=abs(er)**2;mean+=er
        states=q*len(units);ave/=states;mean/=states;formula=float(np.vdot(x,cov@x).real)
        assert abs(ave-formula)<2e-11;assert abs(mean)<2e-12
        rows.append({'n':n,'q':q,'m':m,'all_short_displacements_units':all(math.gcd(q,d)==1 for d in range(1,m)),'states':states,'operator_norm_numeric':eig,'weighted_overlap_bound':bound,'coarse_R_squared_overlap_bound':coarse,'direct_average_vs_formula_error':abs(ave-formula),'mean_error':abs(mean)})
    return rows

def static_corrections():
    n=17;v=F(3,16);prob=2*v
    assert prob==F(3,8)
    for h in range(1,101):
        assert 2*n*2**(2*h-1)*prob**h==n*F(3,2)**h>1
    src=(ROOT/'source_extracted/fft_rough_length_green_v14/arbitrary_block_core.py').read_text()
    assert 'vandermonde = lam[None, :] ** exponents' in src
    c=(ROOT/'source_extracted/fft_rough_length_green_v14/covariance.py').read_text()
    assert 'p >= 0.5' in c and '(2.0**rows)' in c
    return {'median_helper':{'n':17,'blocks':5,'variance':'3/16','tolerance':1,'p':'3/8','bound_at_R_2h_minus_1':'17*(3/2)^h','exact_checks':100,'source_executed':False},'memory':{'source':'arbitrary_block_core.py','lines':[226,230],'allocation':'B by B Vandermonde','general_space':'O(N+B^2)','streaming_repair_described':True}}

def main():
    results={}
    for name,fn in [('provenance',provenance),('exact_algebra',exact_checks),('covariance',covariance_checks),('amplification',amplification),('weighted_gaussian_fusion',hero_weighted_covariance),('static_counterexamples',static_corrections)]:
        results[name]=fn();print('PASS',name,flush=True)
    (Path(__file__).parent/'CHECK_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:({a:b for a,b in v.items() if a!='source_static_ast'} if isinstance(v,dict) else {'cases':len(v)}) for k,v in results.items()},indent=2))
if __name__=='__main__':main()
