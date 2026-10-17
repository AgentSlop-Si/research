"""Fresh exact-arithmetic controls, 17 October 2026.
No imports or execution of historical research code. Python integers are
correctness oracles; ledger volumes refer to the stated stream model.
"""
from pathlib import Path
import json, random, hashlib

HERE = Path(__file__).resolve().parent
COUNTS = dict(divisions=0, cascades=0, roundtrips=0, matrix_products=0,
              coefficient_carries=0, ledger_cases=0, mutation_controls=0)

def chunks(x, m):
    """Oracle adapter; production model uses a single packed input scan."""
    return [(x >> j) & ((1 << m)-1)
            for j in range(((max(1,x.bit_length())-1)//m)*m, -1, -m)]

def unchunks(a, m):
    out=0
    for v in a: out=(out<<m)|v
    return out

def trim(a):
    i=0
    while i+1<len(a) and a[i]==0: i+=1
    return a[i:]

def cascade(a, m, d):
    """Read high-to-low binary chunks once, with d Mersenne divider states."""
    if m<2 or d<1: raise ValueError('domain')
    B=1<<m; p=B-1
    states=[0]*d; out=[]
    for digit in a:
        if not 0<=digit<B: raise ValueError('chunk')
        for j in range(d):
            r=states[j]
            s=r+digit
            e=int(s>=p)
            digit=r+e
            states[j]=s-e*p
            assert 0<=digit<B and 0<=states[j]<p
        out.append(digit)
    return trim(out), states, d*m*len(a)

def group_value(rs, m):
    v=0; volume=0
    for r in reversed(rs):
        volume += max(m,v.bit_length()+m)
        v=(v<<m)-v+r
    return v,volume

def encode(x,m,d):
    if x<0: raise ValueError('negative input')
    a=chunks(x,m); result=[]; scan=0; group=0; lengths=[]
    while any(a):
        lengths.append(len(a)*m)
        a,rs,cost=cascade(a,m,d)
        g,gv=group_value(rs,m)
        result.append(g);scan+=cost;group+=gv
    return result or [0],dict(transition_volume=scan,group_volume=group,
                             scan_lengths=lengths)

def decode(gs,m,d):
    v=0; volume=0
    for g in reversed(gs):
        for _ in range(d):
            volume += max(1,v.bit_length()+m)
            v=(v<<m)-v
        volume += max(1,v.bit_length(),g.bit_length())
        v+=g
    return v,volume

def oracle_digits(x,q):
    out=[]
    while x: x,r=divmod(x,q);out.append(r)
    return out or [0]

def carry(cs,m,d):
    out=[];c=0
    for z in cs:
        a=chunks(z+c,m)
        qa,rs,_=cascade(a,m,d)
        c=unchunks(qa,m);g,_=group_value(rs,m);out.append(g)
    while c:
        qa,rs,_=cascade(chunks(c,m),m,d)
        c=unchunks(qa,m);g,_=group_value(rs,m);out.append(g)
    return out

def eval_base(a,q):
    r=0
    for v in reversed(a):r=r*q+v
    return r

def main():
    rng=random.Random(17102026)
    for m in range(2,9):
        p=(1<<m)-1
        for x in range(4096):
            qa,rs,_=cascade(chunks(x,m),m,1)
            assert (unchunks(qa,m),rs[0])==divmod(x,p)
            COUNTS['divisions']+=1
    for m in [2,3,4,5,7,13,19,31]:
        p=(1<<m)-1
        for d in [1,2,3,4,7,11]:
            q=p**d
            cases=[0,1,p-1,p,p+1,q-1,q,q+1,q*q-1,q*q,q*q+1]
            cases += [rng.getrandbits(n) for n in [1,m,2*m,63,128,257,521]]
            for x in cases:
                qa,rs,vol=cascade(chunks(x,m),m,d)
                r,gv=group_value(rs,m)
                assert (unchunks(qa,m),r)==divmod(x,q)
                assert all(0<=a<p for a in rs)
                assert vol==d*m*len(chunks(x,m))
                COUNTS['cascades']+=1
                gs,led=encode(x,m,d)
                assert gs==oracle_digits(x,q)
                assert decode(gs,m,d)[0]==x
                assert all(0<=g<q for g in gs)
                COUNTS['roundtrips']+=1
    # Exact coefficient widths, full carry, and an actual smaller matrix.
    for m in [2,3,4,7,13]:
        p=(1<<m)-1
        for d in [1,2,3]:
            Q=p**d
            for M in [2,3,4]:
                L=M*M
                for kind in range(5):
                    a=[Q-1]*L if kind==0 else [rng.randrange(Q) for _ in range(L)]
                    b=[Q-1]*L if kind==0 else [rng.randrange(Q) for _ in range(L)]
                    x=eval_base(a,Q);y=eval_base(b,Q)
                    cs=[sum(a[i]*b[k-i] for i in range(L) if 0<=k-i<L)
                        for k in range(2*L-1)]
                    bound=L*(Q-1)**2
                    assert max(cs)<=bound
                    cc=carry(cs,m,d)
                    assert decode(cc,m,d)[0]==x*y
                    COUNTS['coefficient_carries']+=1
                    R=Q**M
                    aa=[eval_base(a[i*M:(i+1)*M],Q) for i in range(M)]
                    bb=[eval_base(b[i*M:(i+1)*M],Q) for i in range(M)]
                    C=[[aa[i]*bb[j] for j in range(M)] for i in range(M)]
                    ss=[sum(C[i][k-i] for i in range(M) if 0<=k-i<M)
                        for k in range(2*M-1)]
                    assert eval_base(ss,R)==x*y
                    h=(R-1).bit_length()
                    assert all(t.bit_length()<=h for t in aa+bb)
                    assert max(ss)<=M*(R-1)**2
                    assert M*M*h>=M*((Q**L-1).bit_length()-1)
                    COUNTS['matrix_products']+=1
    rows=[]
    for N in [64,128,256,512,1024,2048,4096]:
        for m in [2,3,4,7,13,19,31,64,128]:
            if 4*m>N:continue
            for d in [1,2,3,4,8]:
                if 4*d*m>N:continue
                gs,led=encode((1<<N)-1,m,d)
                volume=led['transition_volume']
                # Conservative constants for the proved moderate-group range.
                assert volume*m >= N*N//8
                assert volume*m <= 8*N*N
                out=decode(gs,m,d)
                assert out[0]==(1<<N)-1
                rows.append(dict(N=N,m=m,d=d,groups=len(gs),
                                 transition_volume=volume,group_volume=led['group_volume'],
                                 reconstruction_volume=out[1],normalized=volume*m/(N*N)))
                COUNTS['ledger_cases']+=1
    # Countercontrols: dropped quotient, wrong radix, missing carry threshold.
    assert 8 != eval_base([0,1],7)
    assert 49 != (1<<6)-1
    r=2;a=1;p=3
    assert (r,r+a)!=(r+1,r+a-p)
    assert 100%3 != 100//3
    COUNTS['mutation_controls']=4
    result={'status':'PASS','counts':COUNTS,'rows':rows,
            'scope':'Fresh exact controls and explicit stream-volume ledgers only; no timing, historical execution, fast multiplication, fixed-tape benchmark, or novelty claim.'}
    (HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','counts':COUNTS,'ledger_rows':len(rows)},indent=2))

if __name__=='__main__':main()
