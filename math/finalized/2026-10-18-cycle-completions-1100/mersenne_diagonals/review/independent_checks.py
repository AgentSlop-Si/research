"""Fresh, separately seeded mathematical review controls; oracle arithmetic is explicit."""
import collections, hashlib, itertools, json, math, pathlib, random, sys
ROOT=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'reviewed_candidate'))
import diagonal_core as core
SEED=202610181052
rng=random.Random(SEED)
counts=collections.Counter(); digest=hashlib.sha256(); coverage={}
def serial(x):
    if isinstance(x,int): return hex(x)
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x
def record(key,*values):
    counts[key]+=1; digest.update((key+':'+repr(serial(values))+'\n').encode())
def direct_shift(a,s):
    out=[]
    for x in reversed(a):
        z=[0]+out
        for j,v in enumerate(out): z[j]+=s*v
        z[0]+=x; out=z
    return out

# Karatsuba signs, odd split boundaries, and sparse/high/low halves.
for b in [0,1,7,15,16,17,18,31,32,33,63,64,65,127,128,129,255,257,513,1023,2049,4097]:
    vals=[0,1,(1<<b)-1,1<<b,rng.getrandbits(b),rng.getrandbits(b)]
    for x,y in itertools.product(vals,repeat=2):
        if rng.randrange(2): x=-x
        if rng.randrange(2): y=-y
        assert core.kmul(x,y)==x*y
        record('signed_karatsuba',b,x,y)

# All admissible one-limb states, independent of the implementation's initial carry.
R=256
for u in range(1,R,2):
    v=pow(u,-1,R)
    for c in range(u):
        for a in range(R):
            b=((a-c)*v)%R
            z=u*b+c-a
            assert z%R==0 and 0<=z//R<u
            assert 0<=b<R and z<(1<<16)
            counts['exhaustive_carry_transitions']+=1
record('exhaustive_carry_summary',counts['exhaustive_carry_transitions'])

# Newton inversion at non-power-of-two precisions and every small target width.
original_kmul=core.kmul
for t in list(range(1,42))+[47,63,64,65,127,129,257,511,1025]:
    for u in [1,(1<<t)-1,(1<<(t-1))|1,rng.getrandbits(t)|1]:
        calls=[]
        # Use native multiplication as an explicit oracle/counting backend for this trace.
        def traced(x,y):
            calls.append((x.bit_length(),y.bit_length())); return x*y
        core.kmul=traced
        v=core.inverse_odd(u,t)
        core.kmul=original_kmul
        p=1; precisions=[]
        while p<t: p=min(2*p,t); precisions.extend([p,p])
        assert len(calls)==len(precisions)
        assert all(max(a,b)<=p for (a,b),p in zip(calls,precisions))
        assert v==pow(u,-1,1<<t)
        assert core.inverse_odd(u,t)==v
        record('newton_width_trace',t,u,calls)

# Full production stream: one partial final limb, W<t, extremal divisors, and long carries.
widths=[1,2,7,8,9,15,16,17,31,32,33,63,64,65,127,128,129,255,257,1025,8193,32769,65537]
for W in widths:
    for t in [8,16,24,40,72,136]:
        mask=(1<<W)-1; R=1<<t
        for u in [1,3,R-1,(1<<(t-1))+1,rng.getrandbits(t)|1]:
            x=[0,1,mask,rng.getrandbits(W)][rng.randrange(4)]
            v=core.inverse_odd(u,t); calls=[]
            def counted(x,y):
                calls.append((x.bit_length(),y.bit_length())); return original_kmul(x,y)
            got=core.stream_div_odd(x,u,W,t,v,counted)
            q=(W+t-1)//t
            assert len(calls)==2*q and all(max(a,b)<=t for a,b in calls)
            assert got==(x*pow(u,-1,1<<W))&mask
            assert core.stream_mul(x,u,W,t)==(x*u)&mask
            c=X=Y=0
            for j in range(q):
                a=(x>>(j*t))&(R-1); b=((a-c)*v)%R
                z=u*b+c-a; assert z%R==0
                c=z//R; X+=a<<(j*t); Y+=b<<(j*t)
                assert 0<=c<u and u*Y==X+(c<<((j+1)*t))
            assert got==Y&mask
            record('streamed_division_width_count_prefix',W,t,u,x)
coverage['largest_stream_input_bits']=max(widths)

# Branches at exact factorial cap and all seven byte-padding widths.
orig_inv=core.inverse_odd; orig_div=core.stream_div_odd
for n in [1,2,3,5,8,9,16,17,31,32,33,63,65,96,129]:
    Bn=max(1,(n-1)*(n-1).bit_length())
    minW=n+1+(n-1).bit_length()
    Ws=sorted(set([minW,max(minW,Bn-1),max(minW,Bn),max(minW,Bn+1),8*((Bn+7)//8)+1,8*((Bn+7)//8)+7,max(minW,8193)]))
    for W in Ws:
        if W<minW: continue
        h=W-minW
        H,g,W2,Bn2,B,t=core.parameters(n,h)
        assert W==W2 and Bn==Bn2 and B<=W and B<=t<B+8
        invs=[]; divs=[]
        def capture_inverse(u,t): invs.append((u,t)); return orig_inv(u,t)
        def capture_division(x,u,W,t,v=None,product=original_kmul):
            divs.append((x,u,W,t)); return orig_div(x,u,W,t,v,product)
        core.inverse_odd=capture_inverse; core.stream_div_odd=capture_division
        U,v,V=core.tables(n,W,t)
        core.inverse_odd=orig_inv; core.stream_div_odd=orig_div
        assert len(invs)==1 and invs[0][1]==t
        assert len(divs)==(1 if W>t else 0)
        fact=1
        for i in range(n):
            if i: fact*=i
            u=fact>>(i-i.bit_count())
            assert 0<u<(1<<Bn)
            assert U[i]==u%(1<<t) and U[i]%(1<<W)==u%(1<<W)
            assert v[i]==pow(u,-1,1<<t) and V[i]==pow(u,-1,1<<W)
            if W>t: assert U[i]==u
        record('factorial_cap_tables_and_shared_inverse',n,h,W,Bn,B,t,len(divs))

# Direct diagonal entries, exact convolution orientation, guards and centered extraction.
for n in [2,3,4,7,8,9,15,16,17,31,33,65]:
    for h in [0,1,7,n,16*n]:
        a=[rng.randrange(-(1<<h)+1,1<<h) for _ in range(n)]
        for sigma in [-1,1]:
            H,g,W,Bn,B,t=core.parameters(n,h); mask=(1<<W)-1
            U,v,V=core.tables(n,W,t)
            true_u=[math.factorial(i)>>(i-i.bit_count()) for i in range(n)]
            A=[(core.stream_mul(x&mask,U[i],W,t)<<(g-i.bit_count()))&mask for i,x in enumerate(a)]
            assert A==[((true_u[i]*x)<<(g-i.bit_count()))&mask for i,x in enumerate(a)]
            J=[(sigma**i*(V[i]<<i.bit_count()))&mask for i in range(n)]
            D=core.packed_convolution(A[::-1],J,W,lambda x,y:x*y)
            for k in range(2*n-1):
                expected=sum(A[n-1-i]*J[k-i] for i in range(n) if 0<=k-i<n)&mask
                assert D[k]==expected
            out=direct_shift(a,sigma)
            reconstructed=[]
            for j in range(n):
                d=D[n-1-j]
                z=core.stream_div_odd(d,U[j],W,t,v[j])
                assert z==(d*pow(true_u[j],-1,1<<W))&mask
                residue=(z<<j.bit_count())&mask
                assert residue% (1<<g)==0 and residue==((out[j]<<g)&mask)
                y=residue>>g
                if y>=(1<<(H-1)): y-=1<<H
                reconstructed.append(y)
            assert reconstructed==out
            assert core.shift(a,sigma,h,convolution_product=lambda x,y:x*y)==out
            assert core.shift(out,-sigma,convolution_product=lambda x,y:x*y)==a
            record('both_diagonals_kernel_guard_reconstruction',n,h,sigma,a)

# End-to-end original explicit Karatsuba convolution, exhaustive low-height tuples.
for n in range(1,6):
    for a in itertools.product([-1,0,1],repeat=n):
        for sigma in [-1,1]:
            got=core.shift(a,sigma)
            assert got==direct_shift(a,sigma)
            assert core.shift(got,-sigma)==list(a)
            record('explicit_backend_exhaustive_signed_shift',a,sigma)
assert core.shift([])==[]
record('empty_shift')

# Full positional oracle boundaries, maximum binary input, signed carries and lazy products.
for m in [2,3,5,8,13,31,67,127]:
    radix=1<<m; p=radix-1
    for L in [1,2,3,7,13]:
        a=[radix-1]*L
        b=[rng.randrange(radix) for _ in range(L)]
        X=sum(x<<(m*i) for i,x in enumerate(a)); Y=sum(y<<(m*i) for i,y in enumerate(b))
        A=core.shift(a,1,convolution_product=lambda x,y:x*y)
        B=core.shift(b,1,convolution_product=lambda x,y:x*y)
        C=[sum(A[i]*B[k-i] for i in range(L) if 0<=k-i<L) for k in range(2*L-1)]
        raw=core.shift(C,-1,convolution_product=lambda x,y:x*y)
        assert sum(c<<(m*i) for i,c in enumerate(raw))==X*Y
        carry=0; bits=[]
        for c in raw:
            carry,z=divmod(c+carry,radix); bits.append(z)
        assert carry>=0
        while carry: carry,z=divmod(carry,radix); bits.append(z)
        assert sum(c<<(m*i) for i,c in enumerate(bits))==X*Y
        digits=[]; q=X
        while q: q,z=divmod(q,p); digits.append(z)
        assert len(digits)>=L
        back=core.shift(digits,-1,convolution_product=lambda x,y:x*y)
        assert sum(c<<(m*i) for i,c in enumerate(back))==X
        for d in [1,2,3,L,L+5]:
            grouped=[]
            for start in range(0,len(digits),d):
                g=digits[start:start+d]
                rawg=core.shift(g,-1,convolution_product=lambda x,y:x*y)
                grouped.append(sum(c<<(m*i) for i,c in enumerate(rawg)))
            assert sum(c*p**(d*i) for i,c in enumerate(grouped))==X
            record('grouped_actual_length_identity',m,L,d)
        record('lazy_product_and_maximum_digit_roundtrip',m,L,X,Y)

# Check exact packing capacity, parameter regimes and sufficient asymptotic thresholds.
for L in [1,2,3,7,16,31,64,127,257]:
    for m in [max(2,(L+3)//4),max(2,L),max(2,L*L),max(2,8*L*L)]:
        H,g,W,Bn,B,t=core.parameters(L,m)
        b=8*((2*W+g+7)//8); N=L*m
        Bstar=max(1,min(m,L*(L).bit_length()))
        assert W<=9*m+16 and B<=10*Bstar+16
        if L>1: assert L*b>2*N
        record('conversion_parameter_capacity',L,m,N,W,B,Bstar,L*b)

result={'status':'PASS','seed':SEED,'counts':dict(counts),'coverage':coverage,'digest':digest.hexdigest(),
 'scope':'Finite independent controls of the new arithmetic; complexity follows from the separately inspected proof. Native backend calls in large correctness cases are explicitly paid, not claimed Karatsuba runs.',
 'timing_claim':False}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
