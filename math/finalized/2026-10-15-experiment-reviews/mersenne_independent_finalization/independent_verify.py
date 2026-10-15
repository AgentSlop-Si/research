"""Independent audit, no writes outside this review directory."""
import sys, random, json, math, statistics, time, platform
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'source_snapshot'))
import check as C
import grouped_fold as G
import benchmark as B

def decode_oracle(digits,Q):
    return sum(a*Q**i for i,a in enumerate(digits))

def digits_oracle(x,Q):
    a=[]
    while x:
        x,r=divmod(x,Q);a.append(r)
    return a or [0]

rng=random.Random(0xA71D17)
counts={'exhaustive_divisions':0,'boundary_random_divisions':0,'encodings':0,'schoolbook_products':0,'ntt_coefficients':0,'full_products':0,'capacity_rejections':0}
for m in [2,3,4,5,7]:
    for d in [1,2,3,4,8]:
        Q=((1<<m)-1)**d
        for x in range(4096):
            assert G.div_group(x,m,d)==divmod(x,Q)
            counts['exhaustive_divisions']+=1
for m in [2,3,4,5,7,13,17,19]:
    p=(1<<m)-1
    for d in [1,2,3,4,8,12]:
        Q=p**d; S=1<<(m*d)
        xs={0,1,Q-1,Q,Q+1,S-1,S,S+1,Q*Q-1,Q*Q,Q*Q+1}
        for k in [2,3,5,17]:
            for delta in [-1,0,1]:xs.add(Q**k+delta)
        for n in [1,7,32,127,512,1024]:
            xs.add((1<<n)-1);xs.add(1<<n);xs.add(rng.getrandbits(n))
        for x in sorted(xs):
            assert C.div_p(x,m,{'folds':0,'scan_bit_upper':0})==divmod(x,p)
            assert G.div_group(x,m,d)==divmod(x,Q)
            counts['boundary_random_divisions']+=2
            a,_=G.encode_group(x,m,d); b,_=C.encode(x,m,d)
            assert a==b==digits_oracle(x,Q)
            assert C.decode(a,m,d)[0]==decode_oracle(a,Q)==x
            assert all(0<=v<Q for v in a)
            counts['encodings']+=2
        for n in [0,1,31,127]:
            x=rng.getrandbits(n);y=rng.getrandbits(n)
            a,_=G.encode_group(x,m,d);b,_=G.encode_group(y,m,d)
            c,_=C.multiply(a,b,m,d)
            assert decode_oracle(c,Q)==x*y
            assert all(0<=v<Q for v in c)
            counts['schoolbook_products']+=1
# Raw NTT+CRT coefficients versus independent schoolbook oracle.
for la,lb in [(1,1),(2,3),(7,5),(32,17),(65,64)]:
    for width in [0,1,9,19,38]:
        a=[rng.getrandbits(width) for _ in range(la)]
        b=[rng.getrandbits(width) for _ in range(lb)]
        actual,stats=B.conv(a,b)
        expected=[sum(a[i]*b[j] for i in range(la) for j in range(lb) if i+j==k) for k in range(la+lb-1)]
        assert actual==expected
        counts['ntt_coefficients']+=len(expected)
P=math.prod(q for q,g in B.PRIMES)
try:B.conv([P],[1])
except ValueError:counts['capacity_rejections']+=1
else:raise AssertionError('CRT capacity not rejected')
# Complete candidate pipelines on zero, asymmetry, carries and randomized pairs.
for m,d in [(2,1),(2,2),(3,3),(7,4),(19,2)]:
    for n in [0,1,31,127,511]:
        for x,y in [(0,rng.getrandbits(n)),(1,(1<<n)-1),((1<<n)-1,(1<<n)-1),(rng.getrandbits(n),rng.getrandbits(n))]:
            for enc in [C.encode,G.encode_group]:
                B.encode=enc;B.run(x,y,m,d,False);counts['full_products']+=1
# Independently validate the small unit-group controls and primality assumptions.
primes=[]
for m in [2,3,5,7,13,17,19]:
    p=(1<<m)-1
    assert all(p%t for t in range(2,math.isqrt(p)+1));primes.append(p)
root_controls=[]
for m,d in [(2,1),(2,2),(2,3),(3,1),(3,2),(5,1),(3,3)]:
    p=(1<<m)-1;Q=p**d
    roots=[a for a in range(Q) if math.gcd(a,Q)==1 and pow(a,4,Q)==1 and pow(a,2,Q)!=1]
    assert not roots
    root_controls.append({'m':m,'d':d,'Q':Q,'order4_units':len(roots)})
result={'status':'PASS','counts':counts,'primality_controls':primes,'root_controls':root_controls,'scope':'Nonnegative integers, m>=2, d>=1; randomized/exhaustive finite verification plus separately documented invariant proof. Composite p=15 also included to verify primality is unnecessary for conversion.'}
(HERE/'INDEPENDENT_CORRECTNESS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)

# Remove diagnostic work symmetrically, preserving the exact radix.
def encode_clean(x,m,d,kind):
    if kind=='binary':
        Q=1<<(m*d);mask=Q-1;out=[]
        while x:out.append(x&mask);x>>=m*d
        return out or [0]
    p=(1<<m)-1;Q=p**d;out=[]
    if kind=='p2_native_divmod':
        while x:x,r=divmod(x,Q);out.append(r)
    elif kind=='p2_grouped':
        shift=m*d;mask=(1<<shift)-1
        assert d==2
        while x:
            q=0
            while x>>shift:
                A=x>>shift;low=x&mask;q+=A;x=low+(A<<(m+1))-A
            if x>=Q:q+=1;x-=Q
            out.append(x);x=q
    elif kind=='p2_sequential':
        while x:
            digit=0;weight=1
            for j in range(d):
                q=0
                while x>>m:
                    A=x>>m;low=x&p;q+=A;x=A+low
                if x>=p:q+=1;x-=p
                digit+=x*weight;x=q;weight=(weight<<m)-weight
            out.append(digit)
    else:raise ValueError(kind)
    return out or [0]

def run_clean(x,y,m,d,kind):
    t=time.perf_counter_ns();Q=(1<<(m*d)) if kind=='binary' else ((1<<m)-1)**d
    a=encode_clean(x,m,d,kind);b=encode_clean(y,m,d,kind)
    t1=time.perf_counter_ns();c,stats=B.conv(a,b);t2=time.perf_counter_ns()
    carry=0
    for i in range(len(c)):carry,c[i]=divmod(c[i]+carry,Q)
    while carry:carry,v=divmod(carry,Q);c.append(v)
    z=0
    for v in reversed(c):
        if kind=='binary':z<<=m*d
        else:
            for j in range(d):z=(z<<m)-z
        z+=v
    t3=time.perf_counter_ns()
    assert z==x*y
    return {'total_ms':(t3-t)/1e6,'convert_ms':(t1-t)/1e6,'convolution_ms':(t2-t1)/1e6,'carry_reconstruct_ms':(t3-t2)/1e6,**stats,'digits':max(len(a),len(b))}

R=random.Random(90152);order=random.Random(742918);rows=[];raw=[]
methods=['p2_sequential','p2_grouped','p2_native_divmod','binary']
for N in [256,1024,2048,8192]:
    X=R.getrandbits(N)|(1<<(N-1));Y=R.getrandbits(N)|(1<<(N-1))
    for k in methods:run_clean(X,Y,19,2,k)
    trials={k:[] for k in methods}
    for rep in range(9):
        shuffled=methods[:];order.shuffle(shuffled)
        for k in shuffled:
            v=run_clean(X,Y,19,2,k);trials[k].append(v);raw.append({'N':N,'kind':k,'rep':rep,**v})
    for k in methods:
        row={'N':N,'kind':k,**trials[k][0]}
        for name in ['total_ms','convert_ms','convolution_ms','carry_reconstruct_ms']:row[name]=statistics.median(v[name] for v in trials[k])
        row['total_min_ms']=min(v['total_ms'] for v in trials[k]);row['total_max_ms']=max(v['total_ms'] for v in trials[k]);rows.append(row)
    print(N,[(k,round(statistics.median(v['total_ms'] for v in trials[k]),4)) for k in methods],flush=True)
(HERE/'UNINSTRUMENTED_BENCHMARK.json').write_text(json.dumps({'status':'PASS','python':sys.version,'platform':platform.platform(),'method':'Identical preselected input pair per size; original seed 90152; m=19,d=2; nine randomized-order measured trials after one warm-up; no ledger instrumentation; same original NTT/CRT backend; complete conversion+convolution+carry+reconstruction; oracle assertion outside timer; setup inside timer; native divmod radix Q is an additional control, not a bit-fold algorithm. Shared machine timings only.','rows':rows,'raw_trials':raw},indent=2)+'\n')
