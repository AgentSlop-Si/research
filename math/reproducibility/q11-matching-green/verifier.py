#!/usr/bin/env python3
"""Q11 repository reproducibility supplement; Python standard library only.

Public-safe derivative of the accepted independently generated reviewer checker.
See NOTICE.md for attribution, provenance, licensing status and limitations.
It reads only its optional local expected-results/manifest files and writes JSON
to standard output. No private archive, network, or external package is needed.
"""
import argparse, json, hashlib, math, pathlib, random, sys
ROOT=pathlib.Path(__file__).resolve().parent

def factors(n):
    ans=[]; d=2
    while d*d<=n:
        if n%d==0:
            ans.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:ans.append(n)
    return ans

def prime(n):
    """Deterministic trial-division certification for these bounded test primes."""
    if not 2 <= n < 2**32:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))

def validate_root(n, p, w):
    if not prime(p):
        raise ValueError('The test modulus must be a certified prime below 2**32.')
    if pow(w, n, p) != 1 or any(pow(w, n // d, p) == 1 for d in factors(n)):
        raise ValueError('The supplied root must have exact order N.')

def validate_branch(sigma, weights, p):
    n = len(weights)
    if len(sigma) != n or n == 0 or sorted(sigma) != list(range(n)):
        raise ValueError('The successor must be a permutation of all coordinates.')
    visited = set()
    j = 0
    for _ in range(n):
        visited.add(j)
        j = sigma[j]
    if j != 0 or len(visited) != n:
        raise ValueError('The structural permutation must be one Hamiltonian cycle.')
    holonomy = 1
    for w in weights:
        holonomy = holonomy * w % p
    if holonomy == 1:
        raise ValueError('Unit holonomy makes the Green inverse singular.')
    return holonomy

def root_for(n):
    k=2
    while True:
        p=k*n+1
        if p >= 2**32:
            raise ValueError('The bounded test-prime search is exhausted.')
        if prime(p):
            for a in range(2,1000):
                w=pow(a,k,p)
                if pow(w,n,p)==1 and all(pow(w,n//d,p)!=1 for d in factors(n)):
                    return p,w
        k+=2

def setup(q,rootpower=1):
    if not isinstance(q, int) or q <= 0 or q % 2 == 0 or q % 5 == 0:
        raise ValueError('Control q must be positive, odd, and coprime to 5.')
    n=5*q*q;s=5*q;h=(n+1)//2;p,w=root_for(n);w=pow(w,rootpower,p)
    assert math.gcd(rootpower,n)==1
    validate_root(n,p,w)
    preparation = {'multiplications': 0, 'additions': 0}
    def pmul(a,b):
        preparation['multiplications'] += 1
        return a*b%p
    def psub(a,b):
        preparation['additions'] += 1
        return (a-b)%p
    P=[1]*n
    for i in range(1,n):P[i]=pmul(P[i-1],w)
    e=P[pow(q,4,n)];g=(1+2*e*e+2*pow(e,3,p))%p;G=q*g%p;c=n*G%p
    assert g*g%p==5%p and G*G%p==n%p
    if (1+c)%p==0:
        raise ValueError('Resonant finite-field target guard; select another prime/root.')
    rho=pow(1+c,-1,p)
    assert rho==(1-c)*pow((1-125*pow(q,6))%p,-1,p)%p
    directG=sum(P[(h*i*i)%n] for i in range(n))%p
    assert directG==G
    def target(i,j):
        v=(P[(i*j)%n]-G*P[(-h*(i+j)**2)%n])%p
        if i==j:v=(v+c*P[(-h*i*i)%n])%p
        return rho*v%p
    # Literal four-table preparation. Scalar setup and root/Gauss certification
    # above are separate. Endpoint access below performs no field arithmetic.
    minus_rho_G = -rho*G%p  # scalar setup, outside the four-table ledger
    U = [pmul(rho,z) for z in P]
    V = [pmul(minus_rho_G,z) for z in P]
    D = [psub(psub(pmul(c,U[-h*i*i%n]), U[i*i%n]), V[-4*h*i*i%n])
         for i in range(n)]
    assert preparation == {'multiplications':4*n-1, 'additions':2*n}
    def u(mode,a,b,i):
        return U[i*b%n] if mode==0 else V[(-h*i*i-i*b)%n]
    def v(mode,a,b,j):
        return P[(a*(j-b))%n] if mode==0 else P[(-h*j*j-a*(j-b))%n]
    return n,s,h,p,w,P,G,c,rho,target,u,v,D,preparation

def round_paths(s,q,t):
    paths=[]
    for d in range(1,(s+1)//2):
        a=(t+d)%s;b=(t-d)%s
        paths.append(([a+s*k for k in range(q)]+[b+s*k for k in range(q)],a,b))
    paths.append(([t+s*k for k in range(q)],t,t))
    return paths

def branch(n,s,q,t,mode,direction,u,v):
    paths=round_paths(s,q,t)
    flat=[z for path,a,b in paths for z in path]
    if direction<0:flat=list(reversed(flat))
    assert len(flat)==n and set(flat)==set(range(n))
    sigma=[0]*n
    for i,j in zip(flat,flat[1:]+flat[:1]):sigma[i]=j
    W=[1]*n; L=[0]*n;R=[0]*n
    for path,a,b in paths:
        W[path[-1] if direction>0 else path[0]]=0
        if a==b:
            for i in path:L[i]=u(mode,a,a,i);R[i]=v(mode,a,a,i)
        else:
            aa,bb=(a,b) if direction>0 else (b,a)
            for k in range(q):
                i=aa+s*k;j=bb+s*k
                L[i]=u(mode,aa,bb,i);R[j]=v(mode,aa,bb,j)
    return sigma,W,L,R

def add_inverse_to_matrix(M,sigma,W,L,R,p):
    # Literal finite weighted-walk inverse. Does not use the rank-one factorization.
    n=len(W); entries=0
    assert validate_branch(sigma,W,p)==0
    visited=set();j=0
    for _ in range(n):visited.add(j);j=sigma[j]
    assert j==0 and len(visited)==n
    for i in range(n):
        j=i;weight=1
        for _ in range(n):
            M[i][j]=(M[i][j]+L[i]*weight*R[j])%p;entries+=1
            weight=weight*W[j]%p;j=sigma[j]
            if not weight:break
        assert not weight
    return entries

def inverse_apply(sigma,W,R,x,p):
    n=len(W);z=[0]*n
    assert validate_branch(sigma,W,p)==0
    for i in range(n):
        j=i;weight=1
        for _ in range(n):
            z[i]=(z[i]+weight*R[j]*x[j])%p
            weight=weight*W[j]%p;j=sigma[j]
            if not weight:break
        assert not weight
    assert all((z[i]-W[i]*z[sigma[i]]-R[i]*x[i])%p==0 for i in range(n))
    return z

def optimized(q,data,x):
    n,s,h,p,w,P,G,c,rho,target,u,v,D,preparation=data
    y=[D[i]*x[i]%p for i in range(n)];mul=n;add=0
    for t in range(s):
        for mode in (0,1):
            for direction in (1,-1):
                for path,a,b in round_paths(s,q,t):
                    if a==b:
                        directed=path if direction>0 else list(reversed(path))
                        accum=None
                        for i in reversed(directed):
                            val=v(mode,a,a,i)*x[i]%p;mul+=1
                            if accum is None:accum=val
                            else:accum=(accum+val)%p;add+=1
                            out=u(mode,a,a,i)*accum%p;mul+=1
                            y[i]=(y[i]+out)%p;add+=1
                    else:
                        aa,bb=(a,b) if direction>0 else (b,a)
                        accum=None
                        for k in range(q):
                            j=bb+s*k;val=v(mode,aa,bb,j)*x[j]%p;mul+=1
                            if accum is None:accum=val
                            else:accum=(accum+val)%p;add+=1
                        for k in range(q):
                            i=aa+s*k;out=u(mode,aa,bb,i)*accum%p;mul+=1
                            y[i]=(y[i]+out)%p;add+=1
    assert mul==n*(4*s+5)
    assert add==2*(s+1)*(2*n-s)
    return y,mul,add

def matvec(M,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in M]

def full_control(q,rootpower=1):
    data=setup(q,rootpower);n,s,h,p,w,P,G,c,rho,target,u,v,D,preparation=data
    B=[[target(i,j) for j in range(n)] for i in range(n)]
    M=[[0]*n for _ in range(n)]
    rng=random.Random(8497+q+rootpower)
    x=[rng.randrange(p) for _ in range(n)]
    yg=[D[i]*x[i]%p for i in range(n)]
    walk_entries=0
    for t in range(s):
        for mode in (0,1):
            for direction in (1,-1):
                sig,W,L,R=branch(n,s,q,t,mode,direction,u,v)
                walk_entries+=add_inverse_to_matrix(M,sig,W,L,R,p)
                z=inverse_apply(sig,W,R,x,p)
                for i in range(n):yg[i]=(yg[i]+L[i]*z[i])%p
    before=[M[i][i] for i in range(n)]
    for i in range(n):M[i][i]=(M[i][i]+D[i])%p
    assert M==B
    assert any(before[i]!=B[i][i] for i in range(n)), 'Calibration omission must fail.'
    # Full two-sided defining inverse, freshly from F^(-1)+A.
    invn=pow(n,-1,p)
    C=[[invn*P[-i*j%n]%p for j in range(n)] for i in range(n)]
    for i in range(n):C[i][i]=(C[i][i]+P[h*i*i%n])%p
    tested=0
    if n<=245:
        BT=list(zip(*B));CT=list(zip(*C))
        for i in range(n):
            for j in range(n):
                assert sum(a*b for a,b in zip(B[i],CT[j]))%p==(i==j)
                assert sum(a*b for a,b in zip(C[i],BT[j]))%p==(i==j)
                tested+=2
    allvectors=[[0]*n,x,[(i*i+3*i+1)%p for i in range(n)],[(p-1) for _ in range(n)]]
    if n<=45:allvectors.extend([[int(i==j) for i in range(n)] for j in range(n)])
    mult=add=0
    for xx in allvectors:
        y,mult,add=optimized(q,data,xx)
        assert y==matvec(B,xx,p)
        assert matvec(C,y,p)==xx
    assert yg==matvec(B,x,p)
    # Endpoint mutation: one live endpoint changes a nonzero target entry.
    sig,W,L,R=branch(n,s,q,0,0,1,u,v)
    # General coefficient-level mutation has nonzero response on a supported basis.
    i=next(i for i in range(n) if L[i]);j=i
    while not R[j]:
        assert W[j];j=sig[j]
    assert R[j]!=0
    assert (L[i]+1)*R[j]%p!=L[i]*R[j]%p
    return dict(q=q,N=n,prime=p,omega=w,root_power=rootpower,branches=4*s+1,
      full_matrix_entries=n*n,full_two_sided_inverse_entries=tested,
      generic_inverse_walk_entries=walk_entries,generic_branch_recurrences=4*s*n,
      optimized_vectors=len(allvectors),optimized_multiplications=mult,optimized_additions=add,
      preparation_counts=preparation,
      negative_controls=['omitted calibration','mutated live endpoint'])

def match_control(s):
    inv2=pow(2,-1,s);count=0;digest=hashlib.sha256()
    for a in range(s):
        for b in range(a+1,s):
            t=(a+b)*inv2%s;d=(a-t)%s;d=min(d,s-d)
            assert 1<=d<=(s-1)//2
            assert {(t+d)%s,(t-d)%s}=={a,b}
            digest.update(f'{a},{b},{t},{d};'.encode());count+=1
    return dict(classes=s,unordered_pairs=count,assignment_sha256=digest.hexdigest())

def actual_family_control():
    q=483;data=setup(q);n,s,h,p,w,P,G,c,rho,target,u,v,D,preparation=data
    # Every actual-family diagonal, independently using direct original (i+i)^2 exponent.
    for i in range(n):
        diag=0
        for mode in (0,1):diag+=2*u(mode,i%s,i%s,i)*v(mode,i%s,i%s,i)
        assert (diag+D[i])%p==target(i,i)
    rng=random.Random(926017)
    pairs=[(0,n-1),(n-1,0),(0,1),(n-1,n-2)]
    pairs += [(rng.randrange(n),rng.randrange(n)) for _ in range(4096)]
    sameclass=0
    # Include same class off-diagonal explicitly, then random directed block entries.
    pairs += [(a,a+s*(q-1)) for a in range(s)]
    for i,j in pairs:
        a=i%s;b=j%s
        expected=target(i,j)
        if a==b:
            sameclass+=1;value=sum(u(mode,a,a,i)*v(mode,a,a,j) for mode in (0,1))
            if i==j:value=2*value+D[i]
        else:
            t=(a+b)*pow(2,-1,s)%s;d=(a-t)%s;d=min(d,s-d)
            assert {a,b}=={(t+d)%s,(t-d)%s}
            value=sum(u(mode,a,b,i)*v(mode,a,b,j) for mode in (0,1))
        assert value%p==expected
    # Boundary toggles have a concrete forbidden cross-component path.
    # Select distinct paired components in t=0, their forward active L/R supports.
    paths=round_paths(s,q,0)
    i=paths[0][0][0];j=paths[1][0][q]
    original=0;mutated=u(0,paths[0][1],paths[0][2],i)*v(0,paths[1][1],paths[1][2],j)%p
    assert mutated!=original
    try:
        validate_root(n,p,1)
    except ValueError:
        pass
    else:
        raise AssertionError('An imprimitive root was accepted.')
    try:
        validate_branch([1,2,0],[1,1,1],p)
    except ValueError:
        pass
    else:
        raise AssertionError('Unit holonomy was accepted.')
    return dict(q=q,N=n,prime=p,omega=w,all_diagonal_entries=n,
      sampled_offdiagonal_and_diagonal_entries=len(pairs),sameclass_samples=sameclass,
      full_Gauss_sum_terms=n,terms=4*s+1,
      application_multiplications=n*(4*s+5),application_additions=2*(s+1)*(2*n-s),
      preparation_counts=preparation,
      full_transform_executed=False,negative_controls=['removed zero boundary creates crossblock','imprimitive root rejected','unit holonomy rejected'])

def verify_manifest():
    manifest = json.loads((ROOT/'FILE_MANIFEST.json').read_text())
    paths = [item['path'] for item in manifest['files']]
    if len(set(paths)) != len(paths):
        raise ValueError('Duplicate manifest paths.')
    for item in manifest['files']:
        path = pathlib.PurePosixPath(item['path'])
        if path.is_absolute() or len(path.parts) != 1 or path.name in ('.','..'):
            raise ValueError('Manifest paths must be plain filenames.')
        b = (ROOT/path.name).read_bytes()
        if len(b) != item['bytes'] or hashlib.sha256(b).hexdigest() != item['sha256']:
            raise ValueError('A manifest payload failed its exact-byte check: '+path.name)

def run_controls(include_large=False):
    result={'checker':'public-safe derivative of independently generated reviewer code',
      'small_controls_outside_frozen_family':[]}
    for q,rp in [(1,1),(1,2),(3,1),(3,2),(7,1),(11,1)]:
        result['small_controls_outside_frozen_family'].append(full_control(q,rp))
        print('Small control passed',q,rp,file=sys.stderr,flush=True)
    sizes = (5,15,35,55,2415) if include_large else (5,15,35,55)
    result['matchings']=[match_control(s) for s in sizes]
    if include_large:
        result['actual_m1']=actual_family_control()
    result['uniform_proof']='See the linked accepted report; finite-field controls are not the infinite-family proof.'
    result['status']='ALL_ASSERTIONS_PASS'
    return result

def main():
    if not __debug__:
        raise SystemExit('Run without -O or PYTHONOPTIMIZE; checks use assertions.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--large',action='store_true',
                        help='Add all q=483 diagonals, full Gauss sum, matching pairs and sampled coefficients; not a full transform.')
    parser.add_argument('--check',type=pathlib.Path,
                        help='Compare deterministic results with this JSON certificate.')
    parser.add_argument('--verify-manifest',action='store_true',
                        help='First verify all listed local payload SHA-256 values and byte sizes.')
    args=parser.parse_args()
    if args.verify_manifest:
        verify_manifest()
    result=run_controls(args.large)
    if args.check:
        expected=json.loads(args.check.read_text())
        if not args.large:
            expected.pop('actual_m1',None)
            expected['matchings']=[x for x in expected['matchings'] if x['classes']<=55]
        if result != expected:
            raise SystemExit('FAIL: results differ from the supplied certificate.')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
