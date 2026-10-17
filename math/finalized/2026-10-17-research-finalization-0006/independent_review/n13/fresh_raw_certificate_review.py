"""Fresh 2026-10-17 independent raw-bank verifier. Original cyclic equations, no candidate code."""
import json,hashlib,sys,time
from pathlib import Path
P,N,Q=53,13,16

def check(path):
    started=time.monotonic();raw=path.read_bytes();cert=json.loads(raw);m=cert['degree'];mod=cert['modulus_ascending']
    assert m in (2,3) and len(mod)==m+1 and mod[-1]==1
    def canonical(v):
        assert isinstance(v,list) and len(v)==m and all(type(x) is int and 0<=x<P for x in v)
        return tuple(v)
    z=(0,)*m;o=(1,)+(0,)*(m-1)
    def embed(n):return (n%P,)+(0,)*(m-1)
    def add(x,y):return tuple((a+b)%P for a,b in zip(x,y))
    def neg(x):return tuple(-a%P for a in x)
    def sub(x,y):return add(x,neg(y))
    def mul(x,y):
        c=[0]*(2*m-1)
        for i,a in enumerate(x):
            for j,b in enumerate(y):c[i+j]+=a*b
        for k in range(2*m-2,m-1,-1):
            q=c[k]%P
            for j in range(m):c[k-m+j]-=q*mod[j]
        return tuple(c[i]%P for i in range(m))
    def power(x,k):
        v=o
        while k:
            if k&1:v=mul(v,x)
            x=mul(x,x);k//=2
        return v
    def inv(x):
        assert x!=z
        y=power(x,P**m-2);assert mul(x,y)==o;return y
    def ev(p,x):
        v=z
        for a in reversed(p):v=add(mul(v,x),embed(a))
        return v
    def dot(a,b):
        v=z
        for x,y in zip(a,b):v=add(v,mul(x,y))
        return v
    assert all(P%d for d in range(2,8)) and pow(Q,N,P)==1 and Q!=1
    # A degree-two or degree-three polynomial is irreducible iff it has no base-field root.
    assert all(sum(c*pow(x,i,P) for i,c in enumerate(mod))%P for x in range(P))
    H,K=cert['positive_H'],cert['negative_H'];rp=list(map(canonical,cert['positive_roots']));rn=list(map(canonical,cert['negative_roots']))
    assert len(H)==len(K)==8 and H[-1]==K[-1]==1
    assert len(rp)==len(set(rp))==len(rn)==len(set(rn))==7 and z not in rp+rn
    assert all(ev(H,x)==z for x in rp) and all(ev(K,x)==z for x in rn)
    banks=cert['banks'];assert len(banks)==16
    actual_support={s:[] for s in [(1,1),(-1,1),(1,-1),(-1,-1)]}
    G={}
    for e,d in actual_support:
        omega=pow(Q,e*d%N,P);D={(0,0):1}
        for total in range(1,N):
            for r in range(total+1):
                ell=total-r;D[r,ell]=(D.get((r-1,ell),0)+pow(omega,r,P)*D.get((r,ell-1),0))%P
        for a in range(N):
            for b in range(N):G[e,d,a,b]=embed(D.get(((e*a)%N,(d*b)%N),0))
    invN=embed(pow(N,-1,P));gamma=embed(sum(pow(Q,(-t*t)%N,P) for t in range(N))*pow(N,-1,P)%P)
    aggregate=[[z]*N for _ in range(N)];physical=[];coefficient_count=0;inverses=0;first_inverse=None
    for bank in banks:
        e,d=bank['epsilon'],bank['delta_sign'];assert (e,d) in actual_support
        alpha=canonical(bank['alpha']);beta=canonical(bank['beta']);actual_support[e,d].append(alpha)
        weights=list(map(canonical,bank['raw_weights']));amps=list(map(canonical,bank['sector_amplitudes']));assert len(weights)==len(amps)==N
        Delta=sub(sub(o,power(alpha,N)),power(beta,N));assert Delta!=z and Delta==canonical(bank['inverse_guard'])
        assert alpha!=z and any(a!=z for a in amps)
        ai=inv(alpha);B=[[z]*N for _ in range(N)]
        for j,w in enumerate(weights):
            diagonal=[sub(o,mul(beta,embed(pow(Q,(e*d*j+d*t)%N,P)))) for t in range(N)]
            rseq=[(-e*s)%N for s in range(N)];mults=[mul(diagonal[r],ai) for r in rseq]
            whole=o
            for a in mults:whole=mul(a,whole)
            closure=inv(sub(o,whole));R=[[z]*N for _ in range(N)]
            for t in range(N):
                constant=z
                for r,a in zip(rseq,mults):constant=sub(mul(a,constant),ai if r==t else z)
                x=mul(constant,closure);R[0][t]=x
                for r,a in zip(rseq[:-1],mults[:-1]):
                    x=sub(mul(a,x),ai if r==t else z);R[(r-e)%N][t]=x
            for r in range(N):
                for t in range(N):
                    want=o if r==t else z
                    assert sub(mul(diagonal[r],R[r][t]),mul(alpha,R[(r-e)%N][t]))==want
                    assert sub(mul(R[r][t],diagonal[t]),mul(alpha,R[r][(t+e)%N]))==want
            inverses+=1
            if first_inverse is None:first_inverse=R
            scale=mul(invN,w)
            for r in range(N):
                for t in range(N):B[r][t]=add(B[r][t],mul(scale,R[r][t]))
        assert any(x!=z for row in B for x in row)
        for b in range(N):
            normalized=mul(mul(power(beta,(d*b)%N),inv(mul(mul(embed(N),Delta),gamma))),dot(weights,[embed(pow(Q,(e*b*j)%N,P)) for j in range(N)]))
            assert normalized==amps[b]
        for a in range(N):
            for b in range(N):
                extracted=mul(invN,dot([B[(t+a)%N][t] for t in range(N)],[embed(pow(Q,(-b*t)%N,P)) for t in range(N)]))
                expected=mul(gamma,mul(mul(G[e,d,a,b],power(alpha,(e*a)%N)),amps[b]))
                assert extracted==expected;coefficient_count+=1
        physical.append(B)
        for r in range(N):
            for t in range(N):aggregate[r][t]=add(aggregate[r][t],B[r][t])
    assert set(actual_support[1,1])==set(rp) and len(actual_support[1,1])==7
    assert set(actual_support[-1,-1])==set(rn) and len(actual_support[-1,-1])==7
    assert actual_support[-1,1]==[embed(cert['y'])] and actual_support[1,-1]==[embed(cert['z'])]
    target=[[embed(pow(Q,(-r*t)%N,P)) for t in range(N)] for r in range(N)]
    assert aggregate==target and aggregate==[list(map(canonical,row)) for row in cert['aggregate']]
    controls={'omit_normalization':sum(mul(embed(N),aggregate[r][t])!=target[r][t] for r in range(N) for t in range(N)),'opposite_Fourier_sign':sum(aggregate[r][t]!=embed(pow(Q,(r*t)%N,P)) for r in range(N) for t in range(N)),'change_first_weight':sum(mul(invN,x)!=z for row in first_inverse for x in row),'delete_each_bank':[sum(x!=z for row in B for x in row) for B in physical]}
    assert all(controls[x]>0 for x in ['omit_normalization','opposite_Fourier_sign','change_first_weight']) and all(controls['delete_each_bank'])
    assert path.read_bytes()==raw
    result={'verdict':'ACCEPT_LITERAL_ORIGINAL_BANK_IDENTITY','candidate_sha256':hashlib.sha256(raw).hexdigest(),'degree':m,'field_modulus_ascending':mod,'allocation':[7,1,1,7],'inverses':inverses,'two_sided_inverse_products':2*inverses,'Weyl_coefficients':coefficient_count,'target_entries':169,'controls':controls,'method':'Fresh finite-field arithmetic and cyclic affine branch solves from original sparse matrices; inert candidate weights only; no candidate or historical code executed.','elapsed_seconds':time.monotonic()-started}
    out=Path(__file__).parent/(cert['name']+'_AUTHOR_CERTIFICATE_RECEIPT.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':check(Path(sys.argv[1]))
