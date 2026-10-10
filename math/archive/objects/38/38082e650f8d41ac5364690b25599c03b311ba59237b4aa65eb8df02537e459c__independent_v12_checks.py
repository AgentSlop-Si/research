"""Independent v12 audit. Never imports or executes uploaded programs.

Python, NumPy, mpmath only. Source data is read as inert JSON for comparisons.
The mathematical proofs are in V12_AUDIT_AND_EXTENSION.md.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
import hashlib, json, math
import mpmath as mp
import numpy as np

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'extracted'/'fft_hero1_centered_v12'
mp.mp.dps=65

def dyadic(n): return 1 << (n-1).bit_length()
def grid(n):
    q=dyadic(n)
    j=[(2*k*q+n)//(2*n) for k in range(n)]
    return q,j,[Fraction(k*q-j[k]*n,n) for k in range(n)]
def block_size(q):
    if q<=4:return 1
    m=1 << ((q.bit_length()-1).bit_length()-1)
    while m*m>q:m//=2
    return m
def tail(r,z):
    a=mp.mpf(z)/2
    if a>=r+1:return mp.inf
    return 2*mp.exp(a*a/(r+1))*a**r/mp.factorial(r)/(1-a/(r+1))
def envelope(z):return 1+2*mp.exp(z*z/8)*mp.expm1(z/2)
def sharp_envelope(z):return 1+z-z**3/12+z**5/320
def alt_tail(r,z):
    a=z/2
    return 2*a**r/mp.factorial(r)/(1-a/(r+1))
def proxy(n,r,m,h):
    q=dyadic(n);k=q//m;d=2*h+1
    return d*q+d*r*k+r*(q+k*math.log2(max(k,2))+n)+n
def bound(n,r,m,h,version):
    q=dyadic(n);z=mp.pi*(n-1)/(2*q);delta=mp.pi*(m-1)/q
    if version=='v11':return tail(r,mp.pi)+(2*r-1)*tail(h+1,delta)
    if version=='v12':return tail(r,z)+envelope(z)*tail(h+1,delta)
    if version=='sharp':return tail(r,z)+sharp_envelope(z)*tail(h+1,delta)
    if version=='midpoint':return tail(r,z)+sharp_envelope(z)*tail(h+1,delta/2)
    raise ValueError(version)
def choose(n,target,version):
    m=block_size(dyadic(n));out=[]
    for r in range(1,50):
        for h in range(12):
            e=bound(n,r,m,h,version)
            if e<=target:out.append((proxy(n,r,m,h),r,h,e))
    p,r,h,e=min(out)
    return {'rank':r,'halfwidth':h,'proxy':p,'bound':float(e),'block':m}

@lru_cache(None)
def bessel(order,z):return mp.besselj(order,z)
def chebyshev_weights(r,w):
    ts=[mp.mpf(1)]
    if r>1:ts.append(w)
    for j in range(2,r):ts.append(2*w*ts[-1]-ts[-2])
    return [ts[0]]+[2*(-mp.j)**j*ts[j] for j in range(1,r)]
def fused(z,d,w,r,h):
    return sum(a*sum(bessel(j-v,z)*bessel(v,d) for v in range(-h,h+1))
               for j,a in enumerate(chebyshev_weights(r,w)))
def truncated(z,w,r):return sum(a*bessel(j,z) for j,a in enumerate(chebyshev_weights(r,w)))

def exact_grids():
    count=0
    for n in list(range(1,257))+[511,513,1001,10007]:
        q,j,theta=grid(n);c=Fraction(n-1,2*q)
        assert len(set(j))==n and j[0]==0 and j[-1]<q
        assert all(abs(t)<=Fraction(1,2) for t in theta)
        assert all(j[k+1]-j[k] in (1,2) for k in range(n-1))
        assert max(abs(c),abs(Fraction(n-1,q)-c))==c
        accumulated=Fraction(0)
        for k in range(n):
            assert accumulated==c*theta[k]
            if k<n-1:accumulated+=c*(Fraction(q,n)-(j[k+1]-j[k]))
            count+=1
    return {'lengths':260,'exact_phase_exponent_checks':count}

def bessel_checks():
    records=[];err=mp.mpf(0)
    for iz in range(33):
        z=mp.pi*iz/64
        terms=[bessel(r,z) for r in range(90)]
        assert all(v>=0 for v in terms)
        total=terms[0]+2*sum(terms[1:])
        integral=1+mp.quad(lambda t:mp.besselj(0,t),[0,z])
        err=max(err,abs(total-integral))
        assert total<=sharp_envelope(z)+mp.mpf('1e-60')
        for r in [1,2,3,7,12,20]:
            t=2*sum(terms[r:])
            assert t<=alt_tail(r,z)+mp.mpf('1e-60')
        records.append({'z':float(z),'l1':float(total),'polynomial_bound':float(sharp_envelope(z))})
    # Exact-rational constant certificate via Machin's identity, not host pi.
    def atan_interval(q,terms):
        a=sum((Fraction((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(terms)),Fraction(0))
        e=Fraction(1,(2*terms+1)*q**(2*terms+1))
        return a-e,a+e
    a,b=atan_interval(5,20),atan_interval(239,20)
    pi_upper=16*a[1]-4*b[0]
    z=pi_upper/2
    poly=1+z-z**3/12+z**5/320
    assert poly<Fraction(1139,500)
    return {'samples':records,'max_identity_residual':str(err),
            'exact_rational_endpoint_bound_below_2_278':True,
            'old_endpoint_envelope':float(envelope(mp.pi/2)),
            'new_endpoint_envelope':float(sharp_envelope(mp.pi/2))}

def kernel_checks():
    totals={};records=[]
    for mode in ['left','midpoint']:
        worst_fusion=mp.mpf(0);worst_total=mp.mpf(0);worst_h0=mp.mpf(0);count=0
        for n in [3,7,10,17,37,93,127,511]:
            q,j,theta=grid(n);m=block_size(q);c=mp.mpf(n-1)/(2*q);zmax=mp.pi*c
            positions=sorted(set([0,n-1,m-1,min(m,n-1),n//2,(n//m)*m if n%m else n-m]))
            for ix in positions:
                if not 0<=ix<n:continue
                start=ix//m*m;occ=min(m,n-start)
                anchor=mp.mpf(start)+(mp.mpf(occ-1)/2 if mode=='midpoint' else 0)
                z=mp.pi*(anchor/q-c);d=mp.pi*(ix-anchor)/q
                for w in [mp.mpf(-1),mp.mpf('-0.63'),mp.mpf(0),mp.mpf('0.27'),mp.mpf(1)]:
                    for r in [1,3,7,12]:
                        ref=truncated(z+d,w,r)
                        for h in [0,1,2,3]:
                            approx=fused(z,d,w,r,h)
                            fusion_bound=sharp_envelope(zmax)*tail(h+1,abs(d))
                            fusion_error=abs(approx-ref)
                            if fusion_bound:
                                ratio=fusion_error/fusion_bound;worst_fusion=max(worst_fusion,ratio)
                                assert ratio<=1+mp.mpf('1e-40')
                            else:assert fusion_error<mp.mpf('1e-60')
                            total_bound=tail(r,zmax)+fusion_bound
                            ratio=abs(approx-mp.exp(-mp.j*(z+d)*w))/total_bound
                            assert ratio<=1+mp.mpf('1e-40');worst_total=max(worst_total,ratio)
                            if h==0:
                                sharp=tail(r,abs(z))+abs(d)
                                if sharp:
                                    rh=abs(approx-mp.exp(-mp.j*(z+d)*w))/sharp
                                    assert rh<=1+mp.mpf('1e-40');worst_h0=max(worst_h0,rh)
                            count+=1
        records.append({'mode':mode,'kernels':count,'max_fusion_ratio':float(worst_fusion),
                        'max_total_ratio':float(worst_total),'max_h0_ratio':float(worst_h0)})
    return records

def covariance_checks():
    rows=[]
    for n,r,h,mode in [(3,3,0,'left'),(7,5,1,'left'),(10,3,1,'midpoint'),(17,5,0,'midpoint'),(23,5,1,'midpoint')]:
        q,ids,thetas=grid(n);m=block_size(q);k=q//m;c=mp.mpf(n-1)/(2*q)
        U=np.exp(-2j*np.pi*np.outer(np.arange(q),np.arange(q))/q)/math.sqrt(q)
        weights=np.zeros((n,n),complex)
        for out in range(n):
            w=2*mp.mpf(thetas[out].numerator)/thetas[out].denominator
            carrier=mp.exp(-mp.j*mp.pi*c*w)
            for ix in range(n):
                start=ix//m*m;occ=min(m,n-start)
                anchor=mp.mpf(start)+(mp.mpf(occ-1)/2 if mode=='midpoint' else 0)
                weights[out,ix]=complex(carrier*fused(mp.pi*(anchor/q-c),mp.pi*(ix-anchor)/q,w,r,h))
        target=math.sqrt(q/n)*U[ids,:n]*weights
        mean=np.zeros_like(target);cov=[np.zeros((n,n),complex) for _ in range(n)];states=0
        for a in range(1,q,2):
            for beta in range(q):
                C=np.zeros((k,q),complex)
                for b in range(k):
                    for t in range(m):
                        exponent=(a*t*(t-1)//2+(a*m*b+beta)*t)%q
                        C[b,b*m+t]=np.exp(2j*np.pi*exponent/q)
                P=C.conj().T@C
                result=math.sqrt(q/n)*(U@P)[ids,:n]*weights
                mean+=result;dif=result-target
                for out in range(n):cov[out]+=np.outer(dif[out].conj(),dif[out])
                states+=1
        mean/=states
        ratio=0.0
        for out in range(n):
            cap=m/n*max(abs(weights[out]))**2
            ratio=max(ratio,float(np.linalg.eigvalsh(cov[out]/states)[-1]/cap))
        assert np.max(abs(mean-target))<1e-12 and ratio<=1+1e-11
        rows.append({'N':n,'Q':q,'M':m,'R':r,'H':h,'mode':mode,'states':states,
                     'mean_matrix_error':float(np.max(abs(mean-target))),'max_covariance_ratio':ratio})
    return rows

def finite_rank_gate():
    n=8;p=97;w=pow(5,12,p);full=set(range(n))
    assert pow(w,8,p)==1 and pow(w,4,p)!=1
    subsets=[frozenset(i for i in range(n) if mask>>i&1) for mask in range(1,255)]
    def runs(s):return sum(i==0 or i-1 not in s for i in s)
    def cut(s):
        count=0
        for i in s:
            if i==0 or i-1 not in s:
                j=i
                while j+1 in s:j+=1
                count+=any(v<i for v in full-s)+any(v>j for v in full-s)
        return count
    def rank(rs,cs):
        matrix=[[pow(w,i*j,p) for j in sorted(cs)] for i in sorted(rs)]
        piv=0
        for col in range(len(cs)):
            ix=next((i for i in range(piv,len(matrix)) if matrix[i][col]),None)
            if ix is None:continue
            matrix[piv],matrix[ix]=matrix[ix],matrix[piv]
            inv=pow(matrix[piv][col],-1,p)
            matrix[piv]=[v*inv%p for v in matrix[piv]]
            for row in range(piv+1,len(matrix)):
                mult=matrix[row][col]
                matrix[row]=[(a-mult*b)%p for a,b in zip(matrix[row],matrix[piv])]
            piv+=1
            if piv==len(matrix):break
        return piv
    banks=[]
    for maxruns in [1,2]:
        allowed=[s for s in subsets if runs(s)<=maxruns];bad=set()
        for I in allowed:
            for H in allowed:
                if len(H)<len(I):continue
                if len(I)-len(H)+rank(full-I,H)>cut(I)+cut(H):
                    for J in subsets:
                        if len(J)==len(I) and J<=H:bad.add((I,J))
        banks.append(bad)
    outcomes={};allI=sorted(set(I for bank in banks for I,J in bank),key=lambda s:tuple(s))
    for perm in permutations(range(n)):
        ok=[True,True]
        for I in allI:
            J=frozenset(perm[i] for i in I)
            for b in range(2):
                if (I,J) in banks[b]:ok[b]=False
            if not any(ok):break
        key=str(tuple(ok));outcomes[key]=outcomes.get(key,0)+1
    assert [len(b) for b in banks]==[72,84]
    assert outcomes=={'(False, False)':24592,'(True, True)':15728}
    return {'field':97,'constraints':[len(b) for b in banks],'outcomes':outcomes}

def parameter_checks():
    data=json.loads((SOURCE/'RESULT_SUMMARY.json').read_text());checked=0;extensions=[]
    for rec in data['parameter_choices']:
        n=rec['N'];target=mp.mpf(str(rec['target_deterministic_rel_error']))
        vals={v:choose(n,target,v) for v in ['v11','v12','sharp','midpoint']}
        for v in ['v11','v12']:
            old=rec[v];new=vals[v]
            assert (new['rank'],new['halfwidth'],new['proxy'])==(old['rank'],old['halfwidth'],old['work_proxy'])
            assert abs(new['bound']-old['deterministic_error_bound'])<=2e-14*max(1e-30,new['bound'])
            checked+=1
        extensions.append({'N':n,'target':float(target),**vals})
    for rec in data['rank_table']:
        z=mp.pi*(rec['N']-1)/dyadic(rec['N']);tol=mp.mpf(str(rec['target_tail']))
        for label,factor in [('uncentered_rank',1),('centered_rank',mp.mpf('0.5'))]:
            r=next(r for r in range(1,100) if tail(r,z*factor)<=tol)
            assert rec[label]==r
    return {'compared_parameter_records':checked,'compared_rank_rows':len(data['rank_table']),
            'extension_table':extensions}

def main():
    out={'scope':'Independent checks only; no uploaded module imports or execution.'}
    for name,fn in [('exact_grids',exact_grids),('bessel_envelopes',bessel_checks),
                    ('kernels',kernel_checks),('covariance',covariance_checks),
                    ('finite_rank_gate',finite_rank_gate),('parameters',parameter_checks)]:
        out[name]=fn();print(name+': PASS',flush=True)
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('ALL INDEPENDENT CHECKS PASSED',flush=True)

if __name__=='__main__':main()
