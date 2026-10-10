#!/usr/bin/env python3
"""Independent v15 audit. Reads uploaded archives as bytes only; never imports them.

Run: OPENBLAS_NUM_THREADS=1 python3 audit/independent_checks.py
Only the standard library and installed NumPy are imported. All paths are relative
to this script, and no original master tree is needed to reproduce the results.
"""
from pathlib import Path, PurePosixPath
import hashlib, io, json, math, stat, zipfile
import numpy as np

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'audit' / 'INDEPENDENT_RESULTS.json'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def inventory_zip(data):
    """Bounded inert reader, including nested ZIPs and source checksum records."""
    z = zipfile.ZipFile(io.BytesIO(data))
    infos = z.infolist()
    assert len(infos) < 10000 and sum(i.file_size for i in infos) < 100_000_000
    files = {}; seen = set()
    for i in infos:
        p = PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
        assert p not in seen and not stat.S_ISLNK(i.external_attr >> 16)
        assert not i.flag_bits & 1
        seen.add(p)
        if not i.is_dir():
            files[str(p)] = z.read(i)
    checked = 0; nested = []
    for name, b in files.items():
        if name.endswith('.zip'):
            nested.append({'path': name, 'sha256': sha(b), 'inventory': inventory_zip(b)})
        if name.rsplit('/', 1)[-1] == 'SHA256SUMS.json':
            prefix = str(PurePosixPath(name).parent)
            for rel, rec in json.loads(b).items():
                data = files[str(PurePosixPath(prefix) / rel)]
                assert sha(data) == rec['sha256'] and len(data) == rec['bytes']
                checked += 1
        if name.rsplit('/', 1)[-1] in ('MANIFEST.sha256', 'SHA256SUMS', 'SHA256SUMS.txt'):
            prefix = str(PurePosixPath(name).parent)
            for line in b.decode().splitlines():
                if not line.strip(): continue
                h, rel = line.split(maxsplit=1)
                rel = rel.lstrip('*')
                p = str(PurePosixPath(prefix) / rel)
                assert p in files, (name, rel)
                assert sha(files[p]) == h, (name, rel)
                checked += 1
    return {'files': len(files), 'manifest_entries_checked': checked, 'nested': nested}

def archive_checks():
    records = []
    for p in sorted((BASE / 'originals').rglob('*.zip')):
        b = p.read_bytes()
        records.append({'path': str(p.relative_to(BASE)), 'bytes': len(b),
                        'sha256': sha(b), 'inventory': inventory_zip(b)})
    assert records[1]['sha256'] == records[2]['sha256']
    assert records[0]['sha256'] == '7547bd349f84ac7256fe7fdf612011cf8148adc53873db8abd5a53a0b9bd952d'
    assert records[1]['sha256'] == 'd14e9f44365af9ed3141f3a0325b5523a5a48201ecbb7253e6978ac322a08992'
    return records

def prime_factors(n):
    out=[]; d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def exact_checks():
    """Finite-field factor-chain checks; Python integers prevent overflow.

    These are independently built linear maps, with every basis vector checked
    at the small sizes, plus dense controls at the source's four test sizes.
    Modular inverse replaces conjugation; no complex positivity is inferred.
    """
    p=998244353
    for prime,gen0 in [(13,2),(998244353,3)]:
        assert all(prime % d for d in range(2,math.isqrt(prime)+1))
        for d in prime_factors(prime-1): assert pow(gen0,(prime-1)//d,prime)!=1
    inv=lambda a:pow(a,p-2,p)
    def mat(w,n): return [[pow(w,-i*j,p) for j in range(n)] for i in range(n)]
    def mv(A,x): return [sum(a*b for a,b in zip(row,x))%p for row in A]
    cases=[(1,1),(4,1),(4,4),(6,3),(7,7),(8,2),(8,4),(14,7),(16,4),(28,4),
           (56,7),(119,7),(136,8),(238,14)]
    rows=[]; outputs=0; phase_relations=0; frame_entries=0
    for q,m in cases:
        p = 13 if q == 6 else 998244353
        gen = 2 if q == 6 else 3
        k=q//m; assert q%m==0 and (p-1)%(2*q)==0
        z=pow(gen,(p-1)//q,p); eta=pow(gen,(p-1)//(2*q),p)
        for d in prime_factors(q):assert pow(z,q//d,p)!=1
        FK=mat(pow(z,m,p),k); FM=mat(pow(z,k,p),m); FQ=mat(z,q)
        slopes=sorted(set([0,1,2,q-1]))
        total_vectors=0
        for a in slopes:
            beta=3%q if q>1 else 0
            c=[pow(z,a*t*(t-1)//2+beta*t,p)*pow(eta,(q%2)*t,p)%p for t in range(m)]
            w=pow(z,k,p)
            s=[[c[t]*pow(z,a*m*b*t,p)%p for t in range(m)] for b in range(k)]
            for b in range(k):
                for t in range(m):
                    for r in range(m):
                        lhs=pow(z,a*t*(t-1)//2+(a*m*b+beta+r*k)*t,p)*pow(eta,(q%2)*t,p)%p
                        assert lhs==s[b][t]*pow(w,r*t,p)%p
                        phase_relations+=1
            # Complete frame on one block, using inverses rather than conjugates.
            for u in range(m):
                for t in range(m):
                    v=sum(inv(s[0][u]*pow(w,r*u,p)%p)*s[0][t]*pow(w,r*t,p) for r in range(m))*inv(m)%p
                    assert v==int(u==t)
                    frame_entries+=1
            vectors=[]
            if q<=28:
                vectors += [[int(i==j) for i in range(q)] for j in range(q)]
            else:
                vectors += [[int(i==j) for i in range(q)] for j in sorted(set([0,1,q//2,q-1]))]
            vectors += [[(i*i*17+(i+1)*seed+5)%p for i in range(q)] for seed in (3,11)]
            for x in vectors:
                # Raw summary map, directly expressed from phase characters.
                D=[[sum(s[b][t]*x[b*m+t]*pow(w,r*t,p) for t in range(m))%p for b in range(k)] for r in range(m)]
                F=[mv(FK,d) for d in D]
                # Invert local Fourier mixing after commuting past block Fourier.
                G=[[sum(F[r][j]*pow(w,-r*t,p) for r in range(m))*inv(m)%p for j in range(k)] for t in range(m)]
                H=[[G[t][(j+a*t)%k]*inv(c[t])%p for j in range(k)] for t in range(m)]
                direct_H=[mv(FK,x[t::m]) for t in range(m)]
                assert H==direct_H
                y=[0]*q
                for j in range(k):
                    v=mv(FM,[H[t][j]*pow(z,-j*t,p)%p for t in range(m)])
                    for r in range(m):y[j+k*r]=v[r]
                assert y==mv(FQ,x)
                outputs+=q; total_vectors+=1
        rows.append({'Q':q,'M':m,'K':k,'field':p,'generator':gen,'slopes':slopes,'vectors':total_vectors})
    return {'fields':[13,998244353],'cases':rows,'exact_output_entries':outputs,
            'exact_phase_relations':phase_relations,'exact_frame_entries':frame_entries}

def normalization_checks():
    rec=[]
    for q,m in [(6,3),(12,3),(15,5),(20,4),(24,4),(28,7)]:
        k=q//m; a=2; beta=3
        i=np.arange(q); U=np.exp(-2j*np.pi*np.outer(i,i)/q)/math.sqrt(q)
        A=np.zeros((q,q),complex)
        for b in range(k):
            for r in range(m):
                for t in range(m):
                    exponent=a*t*(t-1)/2+(a*m*b+beta)*t+(q%2)*t/2+r*k*t
                    A[b*m+r,b*m+t]=np.exp(2j*np.pi*exponent/q)
        normalized=A/math.sqrt(m)
        gram=float(np.max(abs(normalized.conj().T@normalized-np.eye(q))))
        synthesis=U@A.conj().T/m
        sv=np.linalg.svd(synthesis,compute_uv=False)
        singular=float(np.max(abs(sv-1/math.sqrt(m))))
        # Raw single block to selected frequencies ell+s*K.
        selected=U[np.arange(m)*k+1 if k>1 else np.arange(m), :m]
        physical=float(np.max(abs(np.linalg.svd(selected,compute_uv=False)-1/math.sqrt(k))))
        assert max(gram,singular,physical)<1e-11
        rec.append({'Q':q,'M':m,'analysis_unitarity_residual':gram,'summary_synthesis_sv_residual':singular,'physical_block_sv_residual':physical})
    return rec

def covariance_checks():
    """Full enumeration for the actual unnormalized Green projector.

    At every fixed input coordinate the diagonal has been subtracted. Compares
    the directly averaged quadratic-form matrix to an independently grouped
    character Gram matrix, retaining Gaussian weights and fractional frequency.
    """
    rec=[]
    for n,q,m in [(3,14,2),(4,20,2),(5,21,3),(7,35,5),(7,28,4)]:
        c=(n-1)//2; idx=(np.arange(n)-c)%q
        ti=np.where(np.arange(q)<q/2,np.arange(q)/q,np.arange(q)/q-1)
        tau=float(np.max(abs(ti[idx]))); sig2=3.; xi=1.375
        gg=np.exp(np.pi*sig2*ti*ti)/math.sqrt(sig2)
        units=[a for a in range(1,q) if math.gcd(a,q)==1]
        cov=np.zeros((n,n),complex); mean=np.zeros(n,complex)
        for a in units:
            for beta in range(q):
                coeff=np.zeros(n,complex)
                for jn,j in enumerate(idx):
                    b,t=divmod(int(j),m)
                    st=np.exp(2j*np.pi*(a*t*(t-1)/2+(a*m*b+beta)*t+(q%2)*t/2)/q)
                    for u in range(m):
                        l=b*m+u
                        if l==j:continue
                        su=np.exp(2j*np.pi*(a*u*(u-1)/2+(a*m*b+beta)*u+(q%2)*u/2)/q)
                        coeff[jn]+=gg[j]/gg[l]*np.exp(-2j*np.pi*xi*ti[l])*st*np.conj(su)/math.sqrt(n)
                cov+=np.outer(np.conj(coeff),coeff)
                mean+=coeff
        cov/=q*len(units); mean/=q*len(units)
        grouped=np.zeros((n,n),complex)
        for d in range(1-m,m):
            if d==0:continue
            v=[]
            for j in idx:
                l=int(j)+d
                valid=0<=l<q and int(j)//m==l//m
                v.append(gg[j]/gg[l]*np.exp(-2j*np.pi*xi*ti[l]) if valid else 0)
            v=np.array(v)
            for a in units:
                w=v*np.exp(-2j*np.pi*a*d*idx/q)/math.sqrt(n)
                grouped+=np.outer(np.conj(w),w)/len(units)
        residual=float(np.max(abs(cov-grouped))); eig=float(np.linalg.eigvalsh(cov)[-1])
        R=math.exp(math.pi*sig2*(2*tau*m/q+(m/q)**2))
        rough=all(math.gcd(q,d)==1 for d in range(1,m))
        bound=q/n*R*R*(m-1)/len(units) if rough else q/n*R*R*m*(m-1)/len(units)
        assert residual<1e-11 and eig<=bound+1e-11 and np.max(abs(mean))<1e-11
        rec.append({'N':n,'Q':q,'M':m,'states':q*len(units),'rough':rough,'grouped_residual':residual,'mean_residual':float(np.max(abs(mean))),'top_eigenvalue':eig,'analytic_bound':bound})
    return rec

def sampler_checks():
    rec=[]
    for q in (14,21,35,55,77):
        bits=(q-1).bit_length(); accepted=[]
        for a in range(1<<bits):
            for b in range(1<<bits):
                if 1<=a<q and math.gcd(a,q)==1 and b<q:accepted.append((a,b))
        phi=sum(math.gcd(a,q)==1 for a in range(1,q))
        assert len(accepted)==phi*q and len(set(accepted))==len(accepted)
        slope_counts={a:sum(aa==a for aa,_ in accepted) for a in range(1,q) if math.gcd(a,q)==1}
        beta_counts={b:sum(bb==b for _,bb in accepted) for b in range(q)}
        assert set(slope_counts.values())=={q} and set(beta_counts.values())=={phi}
        rec.append({'Q':q,'bits_per_pair':2*bits,'accepted_pairs':len(accepted),'possible_pairs':1<<(2*bits)})
    return rec

def main():
    result={'source_policy':'Uploaded Python, bytecode and logs are data only; no source imports or execution.',
            'archives':archive_checks(),'exact_factorization':exact_checks(),
            'normalization':normalization_checks(),'covariance':covariance_checks(),
            'bounded_fair_bit_sampler':sampler_checks()}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'exact_outputs':result['exact_factorization']['exact_output_entries'],
                      'phase_relations':result['exact_factorization']['exact_phase_relations'],
                      'frame_entries':result['exact_factorization']['exact_frame_entries'],
                      'covariance_states':sum(x['states'] for x in result['covariance']),
                      'all_passed':True},indent=2))

if __name__=='__main__':main()
