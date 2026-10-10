"""Fresh controls for Phase33. No uploaded module is imported or executed.

Uses direct DFT matrices, explicitly enumerated subgroup orbits, independently
enumerated character bases, and exact rational cyclotomic quotient arithmetic.
Run from any directory with Python 3; only the standard library is required.
"""
from fractions import Fraction as Q
from math import gcd, isqrt
from pathlib import Path
import hashlib, json, random, zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source_inert' / 'fft_hero1_phase33'
if not SOURCE.exists():
    SOURCE = HERE / 'source_data'

def isprime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))

def generator(p):
    factors = [d for d in range(2,p) if (p-1)%d == 0 and isprime(d)]
    return next(g for g in range(2,p) if all(pow(g,(p-1)//d,p)!=1 for d in factors))

def orbits(n,C):
    H = list(range(1,n,2**C))
    unseen = set(range(n)); result=[]
    while unseen:
        a=min(unseen); group=sorted({a*h%n for h in H})
        result.append(group); unseen.difference_update(group)
    return result

def project(x,groups,p):
    y=[0]*len(x)
    for group in groups:
        a=sum(x[k] for k in group)*pow(len(group),-1,p)%p
        for k in group:y[k]=a
    return y

def dft(x,w,p):
    n=len(x)
    roots=[pow(w,k,p) for k in range(n)]
    return [sum(v*roots[k*j%n] for j,v in enumerate(x))%p for k in range(n)]

def short_fft(x,w,p):
    """Independent textbook radix-2 recursion for the comparison construction."""
    n=len(x)
    if n==1:return x[:]
    even=short_fft(x[::2],w*w%p,p);odd=short_fft(x[1::2],w*w%p,p)
    z=1;left=[];right=[]
    for a,b in zip(even,odd):
        v=z*b%p;left.append((a+v)%p);right.append((a-v)%p);z=z*w%p
    return left+right

def by_additive_quotients(x,C,wC,p):
    """Geometric-sum comparator: only a primitive 2^C-th root is needed.
    Shell buckets, additive short FFTs, prefix sums, short shell synthesis.
    O(N + (t-C+1)*C*2^C), bounded in this implementation by ordinary radix-2
    work; no claim that the construction is historically new.
    """
    n=len(x);t=n.bit_length()-1
    buckets={j:[0]*2**min(j,C) for j in range(1,t+1)}
    for k in range(1,n):
        v=(k&-k).bit_length()-1;j=t-v
        r=(k>>v)%len(buckets[j]);buckets[j][r]=(buckets[j][r]+x[k])%p
    spectra={j:short_fft(b,pow(wC,2**C//len(b),p),p) for j,b in buckets.items()}
    prefix=[x[0]%p]
    for j in range(1,t+1):prefix.append((prefix[-1]+spectra[j][0])%p)
    out=[0]*n;out[0]=prefix[-1]
    for ell in range(1,t+1):
        vals={}
        for r in range(1,2**min(ell,C),2):
            val=prefix[t-ell]
            for s in range(1,min(ell,C)+1):
                j=t-ell+s;m=min(j,C)
                val=(val+spectra[j][2**(m-s)*r%(2**m)])%p
            vals[r]=val
        for u in range(1,2**ell,2):out[2**(t-ell)*u]=vals[u%2**min(ell,C)]
    return out

def all_characters(q,j,p,g):
    mod=q**j; units=[u for u in range(mod) if gcd(u,q)==1]
    if q==2 and j==1:return [{1:1}]
    if q==2:
        length=2**(j-2); eta=pow(g,(p-1)//length,p)
        return [{((-1)**e*pow(5,a,mod))%mod:(pow(-1,e*s,p)*pow(eta,a*b,p))%p
                 for e in range(2) for a in range(length)}
                for s in range(2) for b in range(length)]
    length=len(units)
    ugen=next(v for v in units if len({pow(v,k,mod) for k in range(length)})==length)
    eta=pow(g,(p-1)//length,p)
    return [{pow(ugen,a,mod):pow(eta,a*b,p) for a in range(length)} for b in range(length)]

def conductor_from_values(chi,q,j):
    if all(v==1 for v in chi.values()):return 0
    for c in range(1,j+1):
        classes={}
        for u,v in chi.items():classes.setdefault(u%(q**c),set()).add(v)
        if all(len(s)==1 for s in classes.values()):return c
    raise AssertionError('conductor not found')

def physical_modes(q,t,p,g):
    n=q**t; modes=[(0,0,{0:1},[1]+[0]*(n-1))]
    for j in range(1,t+1):
        for chi in all_characters(q,j,p,g):
            v=[0]*n
            for u,value in chi.items():v[u*(n//q**j)]=value
            modes.append((j,conductor_from_values(chi,q,j),chi,v))
    assert len(modes)==n
    return modes

def by_mellin_theorem(x,q,t,C,p,g,w):
    """Independent direct sums of full-shell character expansions.
    Deliberately unoptimized: validates formulas, not implementation timings.
    """
    n=q**t; y=[x[0]%p]*n
    for j,c,chi,v in physical_modes(q,t,p,g)[1:]:
        if c>C:continue
        X=sum(x[k]*pow(value,-1,p) for k,value in enumerate(v) if value)%p
        if c==0:
            for k in range(n):
                kernel=sum(pow(w,k*u*(n//q**j),p) for u in chi)%p
                y[k]=(y[k]+X*kernel*pow(len(chi),-1,p))%p
        else:
            ell=t+c-j
            primitive={u%(q**c):value for u,value in chi.items()}
            tau=sum(value*pow(w,(n//q**c)*u,p) for u,value in primitive.items())%p
            coeff=X*tau*pow(len(primitive),-1,p)%p
            for u in range(q**ell):
                if u%q:y[u*(n//q**ell)]=(y[u*(n//q**ell)]+coeff*pow(primitive[u%(q**c)],-1,p))%p
    return y

def modal_test(q,t,p):
    n=q**t;g=generator(p);w=pow(g,(p-1)//n,p)
    modes=physical_modes(q,t,p,g); nonzero=0; columns=[]
    for j,c,chi,v in modes:
        y=dft(v,w,p); coords=[]
        for ell,d,chout,out in modes:
            value=sum(yy*pow(zz,-1,p) for yy,zz in zip(y,out) if zz)%p
            value=value*pow(sum(zz!=0 for zz in out),-1,p)%p
            coords.append(value)
            if value:
                nonzero+=1
                if c:
                    assert ell==t+c-j and d==c
                    for u,z in chout.items():assert z*chi[u%(q**j)]%p==1
        if c:assert sum(z!=0 for z in coords)==1
        columns.append(coords)
    assert nonzero==n+t*(t+3)//2
    return {'q':q,'t':t,'n':n,'prime':p,'nonzeros':nonzero,'entries':n*n,
            'matrix_sha256':hashlib.sha256(json.dumps(columns).encode()).hexdigest()}

class Cyclo:
    """Q[z]/(z^(M/2)+1) for power-of-two M; M is set once per case."""
    M=4
    def __init__(self,a=0):
        self.a=tuple(a) if isinstance(a,(list,tuple)) else (Q(a),)+(Q(0),)*(self.M//2-1)
    @classmethod
    def root(cls,e):
        e%=cls.M; d=cls.M//2; a=[Q(0)]*d;a[e%d]=Q(1 if e<d else -1);return cls(a)
    def __add__(self,b):
        if not isinstance(b,Cyclo):b=Cyclo(b)
        return Cyclo([u+v for u,v in zip(self.a,b.a)])
    __radd__=__add__
    def __neg__(self):return Cyclo([-u for u in self.a])
    def __sub__(self,b):return self+-b
    def __mul__(self,b):
        if not isinstance(b,Cyclo):return Cyclo([u*b for u in self.a])
        d=self.M//2;a=[Q(0)]*d
        for i,u in enumerate(self.a):
            if u:
                for j,v in enumerate(b.a):
                    if v:a[(i+j)%d]+=u*v*(1 if i+j<d else -1)
        return Cyclo(a)
    __rmul__=__mul__
    def conj(self):return sum((self.root(-i)*v for i,v in enumerate(self.a)),Cyclo())
    def __eq__(self,b):
        if not isinstance(b,Cyclo):b=Cyclo(b)
        return self.a==b.a

def exact_case(n,C):
    Cyclo.M=max(n,4); stride=Cyclo.M//n
    x=[Cyclo(Q((j*j+3*j+1)%13-6,3))+Cyclo.root(Cyclo.M//4)*Q((7*j+2)%11-5,5) for j in range(n)]
    groups=orbits(n,C)
    def pr(v):
        y=[None]*n
        for group in groups:
            avg=sum((v[k] for k in group),Cyclo())*Q(1,len(group))
            for k in group:y[k]=avg
        return y
    def ft(v):return [sum((a*Cyclo.root(stride*k*j) for j,a in enumerate(v)),Cyclo()) for k in range(n)]
    fx=ft(x); px=pr(x); projected=pr(fx)
    assert projected==ft(px) and pr(px)==px
    r=[a-b for a,b in zip(x,px)];e=[a-b for a,b in zip(fx,projected)]
    lhs=sum((a*a.conj() for a in e),Cyclo())
    rhs=n*sum((a*a.conj() for a in r),Cyclo())
    assert lhs==rhs and all(v==0 for v in lhs.a[1:])
    energy=sum((a*a.conj() for a in x),Cyclo())
    means=sum(((sum((x[k] for k in group),Cyclo())*sum((x[k] for k in group),Cyclo()).conj())*Q(1,len(group)) for group in groups),Cyclo())
    assert rhs==n*(energy-means)
    return {'n':n,'C':C,'rank':len(groups),'error_squared':str(lhs.a[0]),'exact_cyclotomic_check':True}

def cost_counts(t,C):
    n=2**t
    online=n+t-1+sum((2**(min(j,C)-1)-1)*(5*2**(min(j,C)-1)-1) for j in range(1,t+1))
    setup=0 if C==1 else t-1+sum(2**c+2**(c-2)-1+(1 if c==2 else 2**(c-2))*2**c for c in range(2,C+1))
    signs=0 if C==1 else (4**(C-1)+2)//3
    return online,setup,signs

def main():
    results={'scope':'fresh independent mathematics and analytic cost controls; uploaded programs never executed', 'modular_cases':[], 'modal_matrices':[], 'exact_complex_cases':[], 'ledger_rows':[]}
    output_entries=0; basis_entries=0
    for p in [12289,65537]:
        assert isprime(p); g=generator(p)
        for t in range(1,8):
            n=2**t;w=pow(g,(p-1)//n,p)
            assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
            x=[random.Random(p*100000+n*100+j).randrange(p) for j in range(n)]
            full=dft(x,w,p)
            for C in range(1,t+1):
                groups=orbits(n,C);rank=2**C+(t-C)*2**(C-1)
                assert len(groups)==rank
                px=project(x,groups,p); pf=project(full,groups,p)
                assert project(px,groups,p)==px
                assert pf==dft(px,w,p)==by_mellin_theorem(x,2,t,C,p,g,w)
                assert pf==by_additive_quotients(x,C,pow(w,n//2**C,p),p)
                error=[(a-b)%p for a,b in zip(full,pf)]; residual=[(a-b)%p for a,b in zip(x,px)]
                assert sum(error[k]*error[-k%n] for k in range(n))%p==n*sum(v*v for v in residual)%p
                if C<t:
                    group=next(v for v in groups if len(v)>1);z=[0]*n;z[group[0]]=1;z[group[1]]=p-1
                    assert project(z,groups,p)==[0]*n and any(dft(z,w,p))
                output_entries+=n
                results['modular_cases'].append({'n':n,'C':C,'prime':p,'rank':rank})
                if n<=32:
                    for col in range(n):
                        e=[0]*n;e[col]=1
                        assert by_mellin_theorem(e,2,t,C,p,g,w)==project([pow(w,k*col,p) for k in range(n)],groups,p)
                        basis_entries+=n
    for q,t,p in [(2,t,12289) for t in range(1,6)]+[(3,1,37),(3,2,73),(3,3,163),(5,1,41),(5,2,401),(7,1,127),(7,2,1471)]:
        results['modal_matrices'].append(modal_test(q,t,p))
    for t in range(1,6):
        for C in range(1,t+1):results['exact_complex_cases'].append(exact_case(2**t,C))
    for row in json.loads((SOURCE/'PROJECTION_BENCHMARK.json').read_text()):
        n=row['n'];t=n.bit_length()-1
        for lev in row['levels']:
            C=lev['cutoff'];online,setup,signs=cost_counts(t,C)
            assert online==lev['online_field_ops'] and setup==lev['prepared_setup_field_ops']
            results['ledger_rows'].append({'n':n,'C':C,'published_online_reproduced':online,'published_setup_reproduced':setup,'unlogged_literal_setup_negations':signs})
    for row in json.loads((SOURCE/'BENCHMARK_PHASE33.json').read_text())['dyadic']:
        n=row['n'];t=row['t'];assert row['warm_modal']==(3*t-7)*n+6*t+4
        assert row['setup_modal']==3*(t-2)*n//2+2*t+2
    for row in json.loads((SOURCE/'BENCHMARK_PHASE33.json').read_text())['crt_phase29']:
        n=row['n'];h=n//120;t=(n//15).bit_length()-1
        assert row['crt_mellin']==15*((3*t-7)*(n//15)+6*t+4)+98*(n//15)
        assert row['optimized_phase29']==180*h*(h.bit_length()-1)+1163*h+15
    isotropic=[0,1,0,4,0,16,0,13];p=17;w=pow(3,2,p)
    assert project(isotropic,orbits(8,1),p)==[0]*8 and sum(v*v for v in isotropic)%p==0
    err=dft(isotropic,w,p);assert any(err) and sum(err[k]*err[-k%8] for k in range(8))%p==0
    results['finite_field_zero_certificate_nonzero_error']={'p':17,'N':8,'C':1,'input':isotropic,'error':err}
    # Valid root with Gauss core coefficient equal to 1: exact operation formula
    # requires the stated tested-field convention rather than all prime fields.
    tau=(pow(3,1,5)-pow(3,3,5))%5;assert tau==1
    results['identity_gauss_multiplier']={'p':5,'N':4,'root':3,'tau':tau,'formula_warm':12,'source_branch_warm':11}
    # A projected transform still exists over a field that has the low root
    # but no primitive N-th root. Compare after extending to a root-rich field
    # is unnecessary: use the explicit geometric-sum coefficient formula.
    n=64;C=2;p=5;x=[(j*j+2*j+3)%p for j in range(n)]
    low=by_additive_quotients(x,C,2,p);reference=[]
    for k in range(n):
        val=x[0]
        for j in range(1,7):
            m=min(j,C);L=2**(j-m)
            if k%L==0:
                for u in range(1,2**j,2):
                    val+=x[2**(6-j)*u]*pow(2,((k//L)*u*2**(C-m))%(2**C),p)
        reference.append(val%p)
    assert low==reference
    results['low_root_only_case']={'N':64,'C':2,'prime':5,'primitive_low_root':2,'field_has_primitive_N_root':False,'all_entries_verified':64}
    results['summary']={'dense_projected_output_entries':output_entries,'basis_projected_output_entries':basis_entries,'modular_cases':len(results['modular_cases']),'modal_matrix_entries':sum(r['entries'] for r in results['modal_matrices']),'exact_complex_cases':len(results['exact_complex_cases']),'projection_ledger_rows':len(results['ledger_rows']),'all_passed':True}
    (HERE/'independent_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results['summary'],indent=2))

if __name__=='__main__':main()
