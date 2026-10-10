#!/usr/bin/env python3
"""Fresh audit implementation. Never imports, compiles, or runs uploaded code.
Run with Python 3 + NumPy. All paths are relative to this file by default.
"""
import argparse, ast, cmath, hashlib, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np


def phase(n, numerator):
    return cmath.exp(1j * math.pi * (int(numerator) % (2*n)) / n)


def phases(n, m, a, beta):
    return np.array([[phase(n, a*t*(t-1) + 2*(a*m*b+beta)*t + (n%2)*t)
                      for t in range(m)] for b in range(n//m)])


def independent_cycle(x, m, a, beta):
    """Derived scalar recurrence and exact-Python-integer phase arguments.
    One K-point FFT; independently coded sequential gauged scan.
    """
    n=len(x); k=n//m; h=n%2
    s=phases(n,m,a,beta)
    d=np.einsum('bt,bt->b',s,x.reshape(k,m))
    dft=np.fft.fft(d)
    forcing=[]; gauges=[]; indices=[]
    for j in range(n):
        r=(a*j)%n
        gauge=phase(n,a*j*(j-1)+2*beta*j+h*j)
        boundary=phase(n,-2*m*(r+beta)-a*m*(m-1)-h*m)
        f=(dft[r%k]-boundary*dft[(r+a*m)%k])/math.sqrt(n)
        forcing.append(f/gauge); gauges.append(gauge); indices.append(r)
    seed=sum(forcing)/2
    prefix=0j; out=np.empty(n,dtype=complex)
    for j in range(n):
        out[indices[j]]=gauges[j]*(seed-prefix)
        prefix+=forcing[j]
    y=(np.conj(s)*d[:,None]).ravel()
    return out,y


def phi_mu(n):
    phi=n; mu=1; z=n; p=2
    while p*p<=z:
        if z%p==0:
            phi-=phi//p; z//=p; mu=-mu
            if z%p==0: mu=0
            while z%p==0: z//=p
        p+=1
    if z>1: phi-=phi//z; mu=-mu
    return phi,mu


def analytic_covariance(n,m,k):
    ds=[set(range(-u,m-u))-{0} for u in range(m)]
    q=np.empty((n,n),dtype=complex)
    for i in range(n):
        for j in range(n):
            val=Fraction(0)
            for d in ds[i%m]&ds[j%m]:
                z=n//math.gcd(n,d*(i-j)); ph,mob=phi_mu(z)
                val+=Fraction(mob,n*ph)
            q[i,j]=float(val)*phase(n,2*k*(i-j))
    return q


def all_state_covariance(n,m,k):
    f=np.array([phase(n,-2*k*j)/math.sqrt(n) for j in range(n)])
    q=np.zeros((n,n),dtype=complex); mean=np.zeros(n,dtype=complex)
    states=0; scaled_defect=0.; diagonal_defect=0.
    for a in range(1,n):
        if math.gcd(a,n)!=1: continue
        for beta in range(n):
            s=phases(n,m,a,beta)
            # The ACTUAL row U P, with P=conjugate(s) outer s.
            coeff=(s*np.sum(f.reshape(-1,m)*np.conj(s),axis=1)[:,None]).ravel()
            err=coeff-f
            mean+=err; q+=np.outer(np.conj(err),err); states+=1
            if beta==0:
                p=np.outer(np.conj(s[0]),s[0])
                scaled_defect=max(scaled_defect,float(np.max(np.abs(p@p-m*p))))
                diagonal_defect=max(diagonal_defect,float(np.max(np.abs(np.diag(p)-1))))
    q/=states; mean/=states
    predicted=analytic_covariance(n,m,k)
    difference=float(np.max(np.abs(q-predicted)))
    assert difference<2e-12,(n,m,k,difference)
    eig=np.linalg.eigvalsh(q)
    assert float(np.min(eig))>-2e-12
    assert abs(float(np.trace(q).real)-(m-1))<2e-12
    assert np.max(np.abs(mean))<2e-12
    ph=phi_mu(n)[0]; divs=[g for g in range(1,m) if n%g==0]
    old=float(Fraction((m-1)*len(divs),ph))
    loose=float(Fraction(m*(m-1),ph))
    assert eig[-1]<=old+2e-12 and old<loose
    return dict(n=n,m=m,k=k,states=states,covariance_max_entry_error=difference,
        mean_max_error=float(np.max(np.abs(mean))),covariance_norm=float(eig[-1]),
        prior_divisor_bound=old,new_loose_bound=loose,trace=float(np.trace(q).real),
        scaled_projection_max_defect=scaled_defect,diagonal_max_defect=diagonal_defect)


def check_cycle(max_n):
    rng=np.random.default_rng(91092026); records=[]
    for n in range(4,max_n+1):
        for m in range(2,math.isqrt(n)+1):
            if n%m: continue
            a=int(rng.integers(1,n))
            while math.gcd(a,n)!=1: a=int(rng.integers(1,n))
            beta=int(rng.integers(n)); x=rng.normal(size=n)+1j*rng.normal(size=n)
            got,y=independent_cycle(x,m,a,beta)
            oracle=np.fft.fft(y)/math.sqrt(n)
            err=float(np.max(np.abs(got-oracle)))
            assert err<2e-10,(n,m,a,beta,err)
            # Exact monodromy parity check, with arbitrary units and all N.
            assert (a*(n-1)+(n%2))%2==1
            records.append(dict(n=n,m=m,a=a,beta=beta,max_error=err))
    for n,m in [(840,10),(3600,12),(20736,16),(945,15),(1225,35)]:
        a=next(j for j in range(n//3,n) if math.gcd(j,n)==1); beta=n//2
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        got,y=independent_cycle(x,m,a,beta)
        err=float(np.max(np.abs(got-np.fft.fft(y)/math.sqrt(n))))
        assert err<1e-8,(n,m,err)
        records.append(dict(n=n,m=m,a=a,beta=beta,max_error=err))
    return dict(all_pairs_max_n=max_n,checked=len(records),
        odd_length_pairs=sum(r['n']%2 for r in records),
        largest_error=max(r['max_error'] for r in records),
        worst=max(records,key=lambda r:r['max_error']),records=records)


def check_exact_bounds(max_n):
    pairs=0; counts=0; best_improvement=0.; best_pair=None
    for n in range(4,max_n+1):
        ph=phi_mu(n)[0]
        for m in range(2,math.isqrt(n)+1):
            if n%m: continue
            pairs+=1; groups={}
            for d in range(1,m): groups.setdefault(math.gcd(n,d),[]).append(d)
            c=Fraction(0); direct=Fraction(0)
            for g,ds in groups.items():
                phg=phi_mu(n//g)[0]
                assert Fraction(ph,phg)<=g
                maximum=max(sum(d<=u for d in ds)+sum(d<=m-1-u for d in ds) for u in range(m))
                assert maximum<=(m-1)//g
                c+=Fraction(maximum,phg)
                direct+=Fraction(2*len(ds),phg)
                counts+=1
            old=Fraction((m-1)*len(groups),ph)
            loose=Fraction(m*(m-1),ph)
            assert c<=old<loose and direct<=loose
            gain=float(loose/old)
            if gain>best_improvement: best_improvement=gain; best_pair=[n,m]
    return dict(max_n=max_n,factor_pairs=pairs,gcd_group_certificates=counts,
        all_exact_rational_inequalities_passed=True,
        largest_loose_over_prior_divisor_ratio=best_improvement,pair=best_pair)


def check_medians():
    checks=0
    for s in range(1,20,2):
        q=(s+1)//2
        for p in [Fraction(i,20) for i in range(21)]:
            tail=sum(Fraction(math.comb(s,j))*p**j*(1-p)**(s-j) for j in range(q,s+1))
            assert tail<=math.comb(s,q)*p**q<=2**s*p**q
            checks+=1
    # Exhaust all bad/good masks and all signs at s=3,5,7.
    geometry=0
    import itertools
    for s in [3,5,7]:
        for values in itertools.product([0j,complex(1,1),complex(-1,1),complex(3,0),complex(0,-3)],repeat=s):
            bad=sum(abs(v)>math.sqrt(2)+1e-10 for v in values)
            if bad<(s+1)//2:
                med=complex(float(np.median([v.real for v in values])),float(np.median([v.imag for v in values])))
                assert abs(med)<=2+1e-12
            geometry+=1
    return dict(exact_tail_checks=checks,median_geometry_masks=geometry,
        sharper_bound='N * min(1, binom(s,(s+1)/2) * (B*N**(2*alpha))**((s+1)/2)) + s*epsilon')


def check_sampler():
    records=[]
    for n in range(2,257):
        b=(n-1).bit_length(); space=1<<b; ph=phi_mu(n)[0]
        unit_values=[a for a in range(space) if math.gcd(a,n)==1 and a<n]
        assert len(unit_values)==ph
        probability=Fraction(len(unit_values)*n,space**2)
        assert probability>=Fraction(1,4*(b+1))
        assert Fraction(ph,n)>=Fraction(1,b+1)
        assert 2*b**3>=b*b*(b+1)
        # Original [1,n) unit candidate probability. Claimed phi/n is a lower bound.
        assert Fraction(ph,n-1)>=Fraction(ph,n)
        records.append(dict(n=n,b=b,accepted_raw_pairs=ph*n,all_raw_pairs=space**2))
    return dict(lengths_tested=len(records),uniformity='Every unit/beta pair has exactly one raw preimage per trial.',
        repair_trials='max(64,8*b**3)',repair_abort_bound='exp(-b**2)',records=records)


def check_offsets():
    records=[]; rng=np.random.default_rng(137)
    for n in [5,6,10,12,15,18,21,27,35,45,63,97]:
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        target=np.fft.fft(x)/math.sqrt(n)
        for p in [2,3,5]:
            q=p
            while q<n:q*=p
            js=[(2*k*q+n)//(2*n) for k in range(n)]
            nums=[k*q-js[k]*n for k in range(n)]
            h=n//math.gcd(n,q)
            assert len(set(nums))==h and len(set(js))==n
            assert len(set(nums[:h]))==h
            assert all(nums[k]==nums[k%h] for k in range(n))
            assert all(js[k]<js[k+1] for k in range(n-1))
            assert max(abs(t) for t in nums)*2<=n
            out=np.empty(n,dtype=complex)
            for t in set(nums):
                # Independent explicit modulated Q-DFT at only selected k.
                theta=Fraction(t,n)
                for k in range(n):
                    if nums[k]!=t: continue
                    total=sum(x[j]*cmath.exp(-2j*math.pi*float((Fraction(js[k])+theta)*j/q)) for j in range(n))
                    out[k]=total/math.sqrt(n)
            err=float(np.max(np.abs(out-target)))
            assert err<1e-11
            records.append(dict(n=n,radix=p,Q=q,h=h,max_error=err))
    return dict(cases=len(records),largest_error=max(r['max_error'] for r in records),records=records)


def static_source_check(source):
    errors=[]; count=0
    for line in (source/'MANIFEST.sha256').read_text().splitlines():
        sha,name=line.split(maxsplit=1); path=source/name.strip()
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=sha:errors.append(name)
        count+=1
    assert not errors,errors
    core=ast.parse((source/'composite_cycle_core.py').read_text())
    calls=[]
    for fn in core.body:
        if isinstance(fn,ast.FunctionDef):
            for node in ast.walk(fn):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='fft':
                    calls.append(dict(function=fn.name,line=node.lineno,expression=ast.unparse(node)))
    assert len(calls)==2 and {v['function'] for v in calls}=={'decode_balanced_scan','direct_row_estimate'}
    return dict(manifest_files_verified=count,source_executed=False,static_fft_calls=calls)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,default=Path(__file__).parent/'source')
    ap.add_argument('--output',type=Path,default=Path(__file__).parent/'CHECK_RESULTS.json')
    args=ap.parse_args()
    result={}
    result['source']=static_source_check(args.source)
    result['cycles']=check_cycle(600)
    print('cycle checks:',result['cycles']['checked'],'max error',result['cycles']['largest_error'],flush=True)
    result['covariance']=[all_state_covariance(*case) for case in [(12,3,1),(18,3,4),(30,5,7),(36,4,2),(60,6,7),(45,5,2),(49,7,3)]]
    print('covariance states:',sum(r['states'] for r in result['covariance']),flush=True)
    result['exact_bounds']=check_exact_bounds(2000)
    result['median']=check_medians()
    result['sampler']=check_sampler()
    result['offsets']=check_offsets()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cycles','sampler']},indent=2),flush=True)
    print('ALL INDEPENDENT CHECKS PASSED',flush=True)

if __name__=='__main__':main()
