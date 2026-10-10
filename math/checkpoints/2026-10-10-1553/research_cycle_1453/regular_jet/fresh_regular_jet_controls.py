#!/usr/bin/env python3
"""Fresh exact controls. No supplied research module is executed/imported.
All dense objects and exhaustive words below are small verification oracles.
"""
import json, math, random
from pathlib import Path

P=65537

def check(ok,msg):
    if not ok: raise AssertionError(msg)

def mul(a,b,p=P):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]=(out[i+j]+x*y)%p
    return out

def add(a,b,p=P):
    return [((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))]

def poly_eval(a,x,p=P):
    z=0
    for c in reversed(a):z=(z*x+c)%p
    return z

def shiftpoly(a,x,p=P):
    n=len(x);y=[0]*n
    for t,c in enumerate(a):
        for j,v in enumerate(x):y[(j+t)%n]=(y[(j+t)%n]+c*v)%p
    return y

def shiftpoly_transpose(a,x,p=P):
    n=len(x);y=[0]*n
    for t,c in enumerate(a):
        for j,v in enumerate(x):y[(j-t)%n]=(y[(j-t)%n]+c*v)%p
    return y

def green(a,x,p=P):
    n=len(x);an=pow(a,n,p);check(an!=1,'singular gain')
    # y0 = (x0+a*x[n-1]+...+a^(n-1)*x[1])/(1-a^n).
    y0=x[0];at=a
    for j in range(n-1,0,-1):y0=(y0+at*x[j])%p;at=at*a%p
    y=[y0*pow(1-an,-1,p)%p]
    for j in range(1,n):y.append((x[j]+a*y[-1])%p)
    return y

def pmul(gains,x,p=P):
    gs=[green(a,x,p) for a in gains]
    return [(gs[0][j]+gs[1][j])%p for j in range(len(x))]+[(gs[2][j]+gs[3][j])%p for j in range(len(x))]

def make_polys(gains,p=P):
    factors=[[1,-a%p] for a in gains];q=[1]
    for f in factors:q=mul(q,f,p)
    rs=[]
    for pair in [(0,1),(2,3)]:
        r=[0]
        for omitted in pair:
            term=[1]
            for j,f in enumerate(factors):
                if j!=omitted:term=mul(term,f,p)
            r=add(r,term,p)
        rs.append(r)
    return q,rs

def rmul(rs,x,p=P):return shiftpoly(rs[0],x,p)+shiftpoly(rs[1],x,p)

def rtmul(rs,x,p=P):
    n=len(x)//2;a=shiftpoly_transpose(rs[0],x[:n],p);b=shiftpoly_transpose(rs[1],x[n:],p)
    return [(u+v)%p for u,v in zip(a,b)]

def edge_word(word,n):
    k=len(word);s=0
    for t in range(-n,0):s=2*s+word[t%k]
    es=[];N=1<<n
    for bit in word:
        # Store edge blocks (all b=0, then all b=1), unlike interleaved source notation.
        es.append(s+N*bit);s=(2*s+bit)%N
    return es

def hessian(n,k,p=P):
    N=1<<n;w=pow(3,(p-1)//N,p);gamma=[1]*N+[pow(w,s,p) for s in range(N)]
    inv=[pow(v,-1,p) for v in gamma];H=[{} for _ in gamma]
    for code in range(1<<k):
        word=[(code>>t)&1 for t in range(k)];es=edge_word(word,n);v=1
        for e in es:v=v*gamma[e]%p
        for u,e in enumerate(es):
            for t,f in enumerate(es):
                if u!=t:H[e][f]=(H[e].get(f,0)+v*inv[e]*inv[f])%p
    H=[{j:v for j,v in row.items() if v} for row in H]
    return gamma,H

def hm(H,x,p=P):return [sum(v*x[j] for j,v in row.items())%p for row in H]

def fourier(x,w,p=P):
    return [sum(v*pow(w,i*j,p) for j,v in enumerate(x))%p for i in range(len(x))]

def mixed_word_jet(n,k,gamma,u,v,p=P):
    ans=0
    for code in range(1<<k):
        es=edge_word([(code>>t)&1 for t in range(k)],n)
        c,a,b,ab=1,0,0,0
        for e in es:
            c,a,b,ab=c*gamma[e]%p,(a*gamma[e]+c*u[e])%p,(b*gamma[e]+c*v[e])%p,(ab*gamma[e]+a*v[e]+b*u[e])%p
        ans=(ans+ab)%p
    return ans

def cleared_fourier_column(q,N,w,j,p=P):
    return [pow(w,i*j,p)*sum(c*pow(w,b*i,p)*poly_eval(q,pow(w,j+b,p),p) for b,c in enumerate(q))%p for i in range(N)]

def main():
    rng=random.Random(311453);gains=[pow(3,k,P) for k in [1,3,5,7]];q,rs=make_polys(gains)
    results={'field':P,'gains':gains,'groups':[],'scope':'Fresh finite falsification controls; all-N claims rest on proof, not these tests.'}
    small=[]
    for n in range(1,7):
        N=1<<n;k=n+2;w=pow(3,(P-1)//N,P);gamma,H=hessian(n,k);delta=k*2**max(0,k-n-1)
        check(max(map(len,H))<=delta,'locality')
        for _ in range(3):
            x=[rng.randrange(P) for _ in range(N)];y=[rng.randrange(P) for _ in range(N)]
            px=pmul(gains,x);py=pmul(gains,y)
            check(pmul(gains,shiftpoly(q,x))==rmul(rs,x),'PQ=R')
            check(sum(a*b for a,b in zip(px,hm(H,py)))%P==mixed_word_jet(n,k,gamma,px,py),'formal mixed Hessian')
            fqx=fourier(shiftpoly(q,x),w);cleared=shiftpoly_transpose(q,fqx)
            bycols=[sum(cleared_fourier_column(q,N,w,j)[i]*x[j] for j in range(N))%P for i in range(N)]
            check(cleared==bycols,'cleared target polynomial identity')
        for j in range(N):
            vals=cleared_fourier_column(q,N,w,j);check(sum(z==0 for z in vals)<=len(q)-1,'root support bound')
        small.append({'N':N,'hessian_max_row_nnz':max(map(len,H)),'locality_bound':delta,'formal_mixed_direction_cases':3,'all_cleared_fourier_columns':N})
    results['groups'].append({'name':'constructive_source_and_formal_identity','cases':small})
    large=[]
    for n in [8,9,10,11]:
        N=1<<n;k=n+2;w=pow(3,(P-1)//N,P);gamma,H=hessian(n,k);delta=2*k
        cases=[]
        for j in [0,1,N//3,N-1]:
            ej=[0]*N;ej[j]=1;b=rtmul(rs,hm(H,rmul(rs,ej)));f=cleared_fourier_column(q,N,w,j)
            bn=sum(v!=0 for v in b);fn=sum(v!=0 for v in f)
            check(bn<=32*delta,'cleared carrier support bound');check(fn>=N-4,'target support lower bound')
            if N-4>32*delta:check(b!=f,'excluded candidate unexpectedly Fourier')
            cases.append({'column':j,'carrier_nnz':bn,'target_nnz':fn,'different':b!=f})
        large.append({'N':N,'uniform_exclusion_test':N-4>32*delta,'lower':N-4,'upper':32*delta,'columns':cases})
    results['groups'].append({'name':'large_sparse_denominator_controls','cases':large})
    # Rank-deficiency trap for degree-d polynomial/Hermite pullback.
    # N=8, f uses only two linear moments. Full formal Hessian cannot have rank 8.
    N=8;w=pow(3,(P-1)//N,P);A=[[1]*N,list(range(N))];H2=[[2,3],[3,5]]
    pulled=[[sum(A[a][i]*H2[a][b]*A[b][j] for a in range(2) for b in range(2))%P for j in range(N)] for i in range(N)]
    v=[1,-2,1]+[0]*5
    check(all(sum(row[j]*v[j] for j in range(N))%P==0 for row in pulled),'moment null vector')
    check(any(fourier(v,w)),'Fourier unexpectedly annihilates nonzero input')
    results['groups'].append({'name':'bounded_moment_non_fourier_control','N':N,'moments':2,'null_vector':v})
    results['status']='PASS'
    out=Path(__file__).with_name('FRESH_RESULTS.json');out.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'status':'PASS','small_cases':len(small),'large_cases':len(large),'result':str(out)}))
if __name__=='__main__':main()
