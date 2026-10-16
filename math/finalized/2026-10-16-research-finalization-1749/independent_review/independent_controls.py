#!/usr/bin/env python3
"""Fresh bounded mathematical controls; no source research program imported/executed."""
from collections import Counter
from itertools import product
import hashlib, json, random
from pathlib import Path
OUT=Path(__file__).resolve().parent

def v2(s):
    assert s>0
    return (s&-s).bit_length()-1

def exact_gauss_norm(M,a,s):
    # Literal pair expansion, independently reduced in Z[z]/(z^(M/2)+1).
    # For M a power of two this is the exact cyclotomic defining polynomial.
    if M==1: return [1]
    H=M//2
    counts=Counter((a*(t*t-u*u)+s*(t-u))%M for t in range(M) for u in range(M))
    return [counts[j]-counts[j+H] for j in range(H)]

def affine():
    checked=dc=odd=0
    for M in (2,4,8,16,32,64):
        for a in range(1,M,2):
            for s in range(M):
                got=exact_gauss_norm(M,a,s)
                want=M*(1+((-1 if M==2 else 1)*(-1)**s))
                assert got==[want]+[0]*(M//2-1),(M,a,s,got,want)
                checked+=1
        # DC follows from exact sum of individual norm values, with K unrestricted.
        for K in (1,2,3,5,M-1,M,M+1,2*M+3):
            for b,d in product(range(M),repeat=2):
                numer=sum(M*(1+((-1 if M==2 else 1)*(-1)**(b+d*r))) for r in range(K))
                if d%2==0:
                    assert abs(numer-K*M)==K*M
                    if M>=4 and b%2==0: assert numer==2*K*M
                    dc+=1
                else:
                    target=M*(K+((-1 if M==2 else 1)*(-1)**b)*(K%2))
                    assert numer==target
                    odd+=1
    assert exact_gauss_norm(4,0,0)==[16,0] # even-a formula fails
    # M=1 is exactly the input; no flat-input failure.
    assert exact_gauss_norm(1,13,18)==[1]
    return {'exact_cyclotomic_pair_checks':checked,'even_step_DC_controls':dc,'odd_step_counter_controls':odd,
            'guards_checked':['M=2 parity reversal','M=1 exact exception','a=0 counterexample','odd d/even K exact DC'],
            'status':'PASS'}

def add_vec(out, src, shift=0, p=None):
    for j,x in enumerate(src):
        out[j+shift]+=x
        if p: out[j+shift]%=p

def jet_rec(N,d,x,p=None):
    n=N.bit_length()-1
    out=[[0]*(d+n)]+[[0]*(d+v2(s)+1) for s in range(1,N)]
    for s in range(1,N): add_vec(out[s],x[s],0,p)
    edge=0
    for s in sorted(range(1,N),key=v2):
        par=2*s%N
        if par:
            add_vec(out[par],out[s],1,p); edge+=len(out[s])
    root=0
    for s in range(1,N):
        add_vec(out[0],[-a for a in out[s]],0,p);root+=len(out[s])
    return out,edge,root

def jet_direct(N,d,x,p=None):
    # Definition sum z^t(A0^t-E)x, with E applied independently per coefficient.
    n=N.bit_length()-1
    out=[[0]*(d+n) for _ in range(N)]
    for t in range(n):
        for j in range(d+1):
            for s in range(N):
                out[(s*(1<<t))%N][j+t]+=x[s][j]
                out[0][j+t]-=x[s][j]
    if p: out=[[a%p for a in row] for row in out]
    return out

def jet():
    rng=random.Random(921007)
    cases=dense=cmaps=markers=0
    for n in range(1,9):
        N=1<<n
        for d in sorted(set((0,1,2,n,2*n))):
            caps=d*N+2*N-2
            noncaps=d*(N-1)+2*N-n-2
            edgecap=d*(N-2)+2*N-2*n-2
            for p in (None,3,97):
                for trial in range(3):
                    x=[[rng.randrange(-4,5) for _ in range(d+1)] for _ in range(N)]
                    y,e,r=jet_rec(N,d,x,p)
                    z=jet_direct(N,d,x,p)
                    assert sum(map(len,y))==caps and sum(map(len,y[1:]))==noncaps
                    assert e==edgecap and r==noncaps
                    for row,flat in zip(y,z): assert row+[0]*(len(flat)-len(row))==flat
                    assert all(sum(row[j] if j<len(row) else 0 for row in y)%(p or 10**100)==0 for j in range(d+n))
                    # Root-coordinate input is annihilated, including polynomial x0.
                    x2=[r[:] for r in x];x2[0]=[1000+q for q in range(d+1)]
                    assert jet_rec(N,d,x2,p)[0]==y
                    # C is a difference plus supplied nonzero row scalars; scalar 1
                    # suffices to check degree capacity, since scalars cannot raise it.
                    ccaps=0
                    for s in range(N//2):
                        cap=d+n if s==0 else d+v2(s)+1
                        ccaps+=cap
                        for j in range(cap,d+n):
                            aa=(y[s][j] if j<len(y[s]) else 0)-(y[s+N//2][j] if j<len(y[s+N//2]) else 0)
                            assert aa%(p or 10**100)==0
                    assert ccaps==d*N//2+N-1;cmaps+=1
                    h=[rng.randrange(-5,6) for _ in range(N)]
                    for j in range(d+n):
                        a=sum(h[s]*(y[s][j] if j<len(y[s]) else 0) for s in range(N))
                        b=sum((h[s]-h[0])*(y[s][j] if j<len(y[s]) else 0) for s in range(1,N))
                        assert (a-b)%(p or 10**100)==0
                    markers+=1;cases+=1
            # Integer input showing every claimed coefficient slot can be nonzero.
            xx=[[1]*(d+1) for _ in range(N)]
            yy,_,_=jet_rec(N,d,xx)
            assert all(a!=0 for row in yy for a in row)
            dense+=1
    return {'definition_vs_recurrence_cases':cases,'exact_operation_and_slot_cases':cases,
            'root_input_annihilation_cases':cases,'dense_output_witnesses':dense,
            'C_capacity_cases':cmaps,'constant_marker_contraction_cases':markers,
            'max_N':256,'input_degree_cases':'0,1,2,n,2n (deduplicated)','coefficient_domains':'integers, GF(3), GF(97)',
            'status':'PASS'}

def actual_C_twiddles():
    # Independent source-model check with a genuine primitive Nth root.
    p=257; primitive=3; rng=random.Random(1336); count=0
    assert pow(primitive,256,p)==1 and pow(primitive,128,p)!=1
    for n in range(1,9):
        N=1<<n; omega=pow(primitive,256//N,p)
        assert pow(omega,N,p)==1 and pow(omega,N//2,p)!=1
        for d in sorted(set((0,1,2,n,2*n))):
            x=[[rng.randrange(p) for _ in range(d+1)] for _ in range(N)]
            y,_,_=jet_rec(N,d,x,p); direct=jet_direct(N,d,x,p)
            got=[]
            for r in range(N//2):
                cap=d+n if r==0 else d+v2(r)+1
                row=[pow(omega,r,p)*((y[r][j] if j<len(y[r]) else 0)-(y[r+N//2][j] if j<len(y[r+N//2]) else 0))%p for j in range(cap)]
                ref=[pow(omega,r,p)*(direct[r][j]-direct[r+N//2][j])%p for j in range(d+n)]
                assert row+[0]*(d+n-cap)==ref;got.append(row)
            assert sum(map(len,got))==d*N//2+N-1
            count+=1
    return {'status':'PASS','actual_primitive_root_C_map_cases':count,'field':257,'max_N':256}

if __name__=='__main__':
    result={'ALG032':affine(),'ALG039':jet(),'ALG039_source_field_C_map':actual_C_twiddles(),'method':'Independent fresh standard-library implementation; bounded checks supplement proofs, not unbounded theorem proof.'}
    (OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
