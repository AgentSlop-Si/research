#!/usr/bin/env python3
"""Independent ALG-043 controls. The submitted constructor is only a target under test.
No historical implementation or submitted checker is imported/executed.
"""
import hashlib, importlib.util, json, math, random, sys
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode = True
SRC=Path(__file__).resolve().parent.parent/'candidate'
HERE=Path(__file__).resolve().parent

def hashes(path):
    return {str(f.relative_to(path)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(path.rglob('*')) if f.is_file()}

before=hashes(SRC)
(HERE/'SOURCE_BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('submitted_constructor',SRC/'prepare_cores.py')
submitted=importlib.util.module_from_spec(spec); spec.loader.exec_module(submitted)

def permutation(n):
    # Sorting by distance from either end, lower bit before higher bit on a tie.
    return sorted(range(n),key=lambda b:(min(b,n-1-b), b))

def g(t,w,N,p): return pow(w,(-(t*(t+1)//2))%N,p)

def partial(mask,bits): return sum((1<<b) for i,b in enumerate(bits) if (mask>>i)&1)

def matrix_rank(A,p):
    # Full Gauss-Jordan elimination, independently built on direct chirp entries.
    A=[row[:] for row in A]; row=0
    for col in range(len(A[0])):
        pivot=next((i for i in range(row,len(A)) if A[i][col]),None)
        if pivot is None: continue
        A[row],A[pivot]=A[pivot],A[row]
        inv=pow(A[row][col],p-2,p)
        A[row]=[v*inv%p for v in A[row]]
        for i in range(len(A)):
            if i==row: continue
            f=A[i][col]
            A[i]=[(a-f*b)%p for a,b in zip(A[i],A[row])]
        row+=1
        if row==len(A): break
    return row

def primitive_root_of_order(N,p):
    # Direct search, rather than the submitted checker's fixed generator 3.
    assert (p-1)%N==0
    for base in range(2,p):
        w=pow(base,(p-1)//N,p)
        if pow(w,N,p)==1 and pow(w,N//2,p)!=1: return w
    raise AssertionError((N,p))

def full_contraction(t,cores,pi,p):
    states={0:1}
    for bit,core in zip(pi,cores):
        nxt={}; x=(t>>bit)&1
        for (left,b,right),v in core.items():
            if b==x and left in states:
                nxt[right]=(nxt.get(right,0)+states[left]*v)%p
        states=nxt
    assert set(states)=={0}
    return states[0]

def unique_path(t,cores,pi,s,p):
    left=0; value=1
    for k,(bit,core) in enumerate(zip(pi,cores),1):
        x=(t>>bit)&1
        if k<s:
            right=t% (1<<((k+1)//2))
        else:
            right=sum(((t>>b)&1)<<i for i,b in enumerate(pi[k:]))
        value=value*core[(left,x,right)]%p; left=right
    assert left==0
    return value

counts={k:0 for k in ('constructor_instances','core_coefficients','direct_entry_reconstructions',
                      'full_contractions','unfolding_ranks','factorization_entries','window_antiperiodicity',
                      'exact_cost_ledgers','integer_profiles','negative_controls')}
evidence=[]
# Multiple characteristics and odd embeddings, including inverses and noncanonical roots.
for p,maxn in ((3,1),(5,2),(17,4),(97,5),(257,8),(12289,12),(65537,16)):
    for n in range(1,maxn+1):
        N=1<<n; pi=permutation(n); base=primitive_root_of_order(N,p)
        for u in sorted({1,3%N,7%N,N-1}):
            w=pow(base,u,p)
            assert u%2 and pow(w,N,p)==1 and pow(w,N//2,p)==p-1
            cores,ledger=submitted.prepare(n,w,p)
            s=next(k for k in range(1,n+1) if (k+1)//2>=n-k)
            ranks=[1]+[1<<min((k+1)//2,n-k) for k in range(1,n)]+[1]
            P=2*sum(ranks[k-1] for k in range(1,s)); B=2*ranks[s-1]*ranks[s]
            S=sum(ranks[k-1] for k in range(s+1,n+1)); W=max(ranks)
            assert ledger['field_multiplications']==7*n+P+B+6*ranks[s]
            assert ledger['root_guard_multiplications']==2*n+3
            assert ledger['scalar_core_slots']==P+B+S
            assert ledger['explicit_bridge_map_slots']==3*ranks[s]
            assert ledger['power_and_onebit_slots']==2*n
            assert ledger['width']==W==1<<((n+1)//3)
            counts['exact_cost_ledgers']+=1
            for k,(bit,core) in enumerate(zip(pi,cores),1):
                assert set(a for a,x,b in core)==set(range(ranks[k-1]))
                assert set(b for a,x,b in core)==set(range(ranks[k]))
                expected_slots=2*ranks[k-1] if k<s else (B if k==s else ranks[k-1])
                assert len(core)==expected_slots
                for (a,x,b),v in core.items():
                    if k<s:
                        assert b==(a+(x<<bit) if k%2 else a)
                        expected=g(x<<bit,w,N,p)*pow(w,(-a*(x<<bit))%N,p)%p
                    elif k==s:
                        rest=partial(b,pi[k:]); vbits=(x<<bit)+rest
                        expected=g(vbits,w,N,p)*pow(w,(-a*vbits)%N,p)%p
                    else:
                        assert (x,b)==(a%2,a//2); expected=1
                    assert v==expected and v!=0
                    counts['core_coefficients']+=1
            # Exhaustive n<=12, deterministic samples for larger n.
            ts=range(N) if n<=12 else sorted({0,1,N-1,N//2,*(random.Random(1009*n+u).sample(range(N),1024))})
            for t in ts:
                assert unique_path(t,cores,pi,s,p)==g(t,w,N,p)
                counts['direct_entry_reconstructions']+=1
                if n<=8:
                    assert full_contraction(t,cores,pi,p)==g(t,w,N,p)
                    counts['full_contractions']+=1
                assert g(t-N,w,N,p)==(-g(t,w,N,p))%p
                counts['window_antiperiodicity']+=1
            # Full unfolded matrices, in more than one characteristic.
            if n<=9 and p in (17,257,12289) and u in {1,N-1}:
                for k in range(1,n):
                    rows=[partial(a,pi[:k]) for a in range(1<<k)]
                    cols=[partial(b,pi[k:]) for b in range(1<<(n-k))]
                    A=[[g(a+b,w,N,p) for b in cols] for a in rows]
                    assert matrix_rank(A,p)==ranks[k]
                    counts['unfolding_ranks']+=1
                    j=(k+1)//2
                    for a,row in zip(rows,A):
                        low=a% (1<<j)
                        for b,value in zip(cols,row):
                            assert value==g(a,w,N,p)*g(b,w,N,p)*pow(w,(-low*b)%N,p)%p
                            counts['factorization_entries']+=1
            counts['constructor_instances']+=1
            evidence.append({'prime':p,'n':n,'embedding':u,'width':W,'bridge_stage':s,
                             'multiplications':ledger['field_multiplications'],'scalar_slots':P+B+S})

for n in range(1,1001):
    ranks=[1]+[1<<min((k+1)//2,n-k) for k in range(1,n)]+[1]
    s=next(k for k in range(1,n+1) if (k+1)//2>=n-k); W=max(ranks)
    P=2*sum(ranks[:s-1]); B=2*ranks[s-1]*ranks[s]; S=sum(ranks[s:n])
    assert W==1<<((n+1)//3)
    assert P<6*W and S<2*W and B<=2*W*W
    assert P+B+S<=2*W*W+8*W
    # Dense fallback storage also avoids reliance on expected-time dictionary access.
    dense=sum(2*ranks[k-1]*ranks[k] for k in range(1,n+1))
    assert dense<=12*W*W
    counts['integer_profiles']+=1

# Detect nonprimitive-root admission, cross-factor omission, and ordinary-order transfer.
for n in (1,2,5,12):
    p=12289; N=1<<n; w=primitive_root_of_order(N,p)
    try: submitted.prepare(n,pow(w,2,p),p)
    except ValueError: pass
    else: raise AssertionError('nonprimitive root passed')
    counts['negative_controls']+=1
p=257; n=8; N=1<<n; w=primitive_root_of_order(N,p)
assert g(3,w,N,p)!=g(1,w,N,p)*g(2,w,N,p)%p; counts['negative_controls']+=1
A=[[g(a+16*b,w,N,p) for b in range(16)] for a in range(16)]
assert matrix_rank(A,p)==16>1<<((n+1)//3);counts['negative_controls']+=1

certificates=[]
for n,claim in ((18,46),(30,46),(64,46),(128,46),(1024,47)):
    eps=Fraction(1,10**6); c=Fraction(88,7)
    assert (n-1)*c**(2*claim)<=eps**2*math.factorial(claim)**2
    assert (n-1)*c**(2*(claim-1))>eps**2*math.factorial(claim-1)**2
    certificates.append({'n':n,'epsilon':'1/1000000','first_passing_R':claim})

# Independent source blob and report seals.
bindings=json.loads((SRC/'SOURCE_BINDINGS.json').read_text())
source_validation={}
for filename,binding in bindings['sources'].items():
    raw=(SRC/'sources'/filename).read_bytes()
    sha=hashlib.sha256(raw).hexdigest(); assert sha==binding['sha256']
    row={'sha256':sha}
    if 'git_blob' in binding:
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if blob!=binding['git_blob']:
            assert raw.endswith(b'\n')
            upstream=raw[:-1]
            upstream_blob=hashlib.sha1(b'blob '+str(len(upstream)).encode()+b'\0'+upstream).hexdigest()
            assert upstream_blob==binding['git_blob']
            row['git_blob']=upstream_blob
            row['retained_copy_normalization']='one additional terminal LF'
            row['retained_copy_git_blob']=blob
        else:
            row['git_blob']=blob
    source_validation[filename]=row

after=hashes(SRC); assert after==before
(HERE/'SOURCE_AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
result={'verdict':'PASS','counts':counts,'instances':evidence,'rational_certificates':certificates,
        'source_validation':source_validation,'source_preservation':'all original regular-file hashes identical',
        'scope':'Exact modular controls only; all-size and complex statements are checked by proofs in the independent review.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(counts,sort_keys=True));print('PASS')
