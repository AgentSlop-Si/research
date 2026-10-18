"""Independent audit controls. Oracle arithmetic is explicitly separate."""
from pathlib import Path
import sys, json, random, hashlib, math, itertools, operator
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'candidate'))
import kernel_stream as C
rng = random.Random(202610181249)
counts = {}
digest = hashlib.sha256()
def encode(x):
    if isinstance(x, int): return ('-' if x < 0 else '') + hex(abs(x))
    if isinstance(x, (tuple,list)): return '[' + ','.join(map(encode,x)) + ']'
    return str(x)
def record(k,x=True):
    counts[k] = counts.get(k,0)+1
    digest.update((k+':'+encode(x)+'\n').encode())
def horner_shift(a,sign):
    out=[]
    for v in reversed(a):
        nxt=[0]*(len(out)+1)
        for i,c in enumerate(out):
            nxt[i]+=sign*c
            nxt[i+1]+=c
        nxt[0]+=v
        out=nxt
    return out

def convolution(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

# Test the explicit backend, with adversarial differences and unequal lengths.
for w in (0,1,7,15,16,17,18,31,32,33,63,64,65,127,129,257,1025):
    for r in range(32):
        x=rng.getrandbits(w); y=rng.getrandbits(w if r%2 else max(0,w-9))
        if r%4==0: x=(1<<w)-1
        if r%5==0: y=(1<<w)-1
        x*=(-1 if r%2 else 1); y*=(-1 if r%3 else 1)
        assert C.karatsuba(x,y)==x*y
        record('explicit_karatsuba', (w,x,y))

# Newton precision and exact count; separate native oracle callbacks.
for t in list(range(1,66))+[127,128,129,255,256,257,513,1024]:
    for case in range(3):
        u=rng.getrandbits(t)|1
        precision=1; widths=[]
        while precision<t:
            precision=min(2*precision,t); widths.extend([precision,precision])
        calls=[]
        def checked(x,y):
            cap=widths[len(calls)]; assert x.bit_length()<=cap and y.bit_length()<=cap
            calls.append((x.bit_length(),y.bit_length())); return C.karatsuba(x,y)
        inv=C.odd_inverse(u,t,checked)
        assert inv==pow(u,-1,1<<t)
        assert len(calls)==2*(t-1).bit_length()
        record('precision_bounded_inverse',(t,u,inv))

# Exhaust every legal 8-bit odd-division carry transition, independent of code.
R=256
for u in range(1,R,2):
    inv=pow(u,-1,R)
    for carry in range(u):
        for a in range(R):
            b=((a-carry)*inv)%R
            v=u*b+carry-a
            assert v%R==0 and 0<=v//R<u
            counts['exhaustive_division_transitions']=counts.get('exhaustive_division_transitions',0)+1
record('exhaustive_division_transition_completed',counts['exhaustive_division_transitions'])

for t in (8,16,24,40,72):
    for W in (1,t-1,t,t+1,2*t-1,2*t,2*t+1,257,4099,16385):
        for case in range(4):
            u=[1,(1<<t)-1,rng.getrandbits(t)|1,rng.getrandbits(t)|1][case]
            x=[0,(1<<W)-1,rng.getrandbits(W),rng.getrandbits(W)][case]
            calls=[]; prefix_x=prefix_y=0; position=0
            def prod(a,b):
                assert a.bit_length()<=t and b.bit_length()<=t
                calls.append(1); return C.karatsuba(a,b)
            def trace(a,b,c,next_carry,numerator):
                global prefix_x,prefix_y,position
                assert 0<=c<u and 0<=next_carry<u
                assert numerator==u*b+c-a==next_carry*(1<<t)
                prefix_x+=a<<(t*position);prefix_y+=b<<(t*position);position+=1
                assert u*prefix_y==prefix_x+(next_carry<<(t*position))
            q=C.limb_divide(x,u,W,t,pow(u,-1,1<<t),prod,trace)
            assert q==(x*pow(u,-1,1<<W))%(1<<W)
            assert len(calls)==2*((W+t-1)//t)
            calls.clear()
            z=C.limb_product(x,u,W,t,prod)
            assert z==x*u%(1<<W) and len(calls)==(W+t-1)//t
            record('streamed_division_and_product',(t,W,x,u,q,z))

# Check factorial/cofactor/inverse preparation and all local widths/counts.
for n in list(range(2,42))+[63,64,65,95,127,129]:
    p=C.parameters(n,1);t=p['t'];s=8*((p['g']+7)//8);q=(t+s-1)//s
    calls=[]
    def prod(a,b): calls.append((a.bit_length(),b.bit_length())); return C.karatsuba(a,b)
    us,fs,vs,ks=C.prepare(n,t,prod)
    before=2*(n-1)*q; invcount=2*(t-1).bit_length()
    assert len(calls)==3*(n-1)*q+invcount
    for a,b in calls[:before]+calls[before+invcount:]: assert max(a,b)<=s
    for a,b in calls[before:before+invcount]: assert max(a,b)<=t
    U=math.factorial(n-1)>>((n-1)-(n-1).bit_count())
    for i in range(n):
        ui=math.factorial(i)>>(i-i.bit_count())
        assert us[i]==ui and fs[i]*ui==U and vs[i]*ui%(1<<t)==1
        assert ks[i]==fs[i]<<i.bit_count() and 0<ks[i]<(1<<t)
    record('preparation_and_exact_schedule',(n,t,U,ks))

# Coefficient-slot no-spill and inter-slab carry checks with maximal inputs.
for n in (1,2,3,4,5,7,8,9,17,33):
    for t in (8,16,24):
        for W in (1,t-1,t,t+1,2*t-1,2*t+1,7*t+3):
            for mode in range(3):
                a=[(1<<W)-1 if mode==0 else rng.getrandbits(W) for _ in range(n)]
                k=[(1<<t)-1 if mode<2 else rng.getrandbits(t) for _ in range(n)]
                calls=[];prefixes=[0]*n;written=[0]*n;R=1<<t
                def prod(x,y): calls.append((x.bit_length(),y.bit_length()));return C.karatsuba(x,y)
                def trace(s,j,digits,c,carry,next_carry):
                    assert c==sum(digits[i]*k[j-i] for i in range(j+1))
                    assert c<=n*(R-1)**2 and 0<=carry<=n*(R-1) and 0<=next_carry<=n*(R-1)
                    prefixes[j]+=c<<(s*t);written[j]+=((c+carry)%R)<<(s*t)
                    assert prefixes[j]==written[j]+(next_carry<<((s+1)*t))
                out=C.narrow_convolution(a,k,W,t,prod,trace)
                expect=[v% (1<<W) for v in convolution(a,k)[:n]]
                assert out==expect
                b=8*((2*t+(n-1).bit_length()+7)//8)
                assert len(calls)==(W+t-1)//t and all(max(x,y)<=n*b for x,y in calls)
                record('maximal_random_slab_convolution',(n,t,W,mode,out))

# Independent polynomial-Horner shift oracle, not factorial or binomial code.
assert C.shift([])==[];record('empty_shift')
for n in range(1,6):
    for a in itertools.product((-1,0,1),repeat=n):
        for sign in (-1,1):
            out=C.shift(a,sign)
            assert out==horner_shift(a,sign) and C.shift(out,-sign)==list(a)
            record('exhaustive_horner_shift_inverse',(a,sign,out))
for n in (2,3,5,8,9,17,33):
    p0=C.parameters(n,0)
    for h in sorted(set([0,1,max(0,p0['t']-n-1-p0['g']),p0['t'],2*p0['t']+1,1025])):
        for sign in (-1,1):
            a=[rng.getrandbits(h)*rng.choice((-1,1)) for _ in range(n)]
            if h: a[0]=(1<<h)-1;a[-1]=-((1<<h)-1)
            p=C.parameters(n,h); local=[];packed=[]
            def lp(x,y): assert max(x.bit_length(),y.bit_length())<=p['t'];local.append(1);return C.karatsuba(x,y)
            def cp(x,y): assert max(x.bit_length(),y.bit_length())<=p['S'];packed.append(1);return C.karatsuba(x,y)
            out=C.shift(a,sign,h,lp,cp)
            assert out==horner_shift(a,sign)
            s0=8*((p['g']+7)//8)
            setup=3*(n-1)*((p['t']+s0-1)//s0)+2*(p['t']-1).bit_length()
            assert len(local)==setup+5*n*p['q'] and len(packed)==p['q']
            assert C.shift(out,-sign)==a
            record('signed_shift_full_schedule',(n,h,sign,out))

# Reconstruct full interfaces with an independently implemented linear divider.
def local_div_p(x,m):
    neg=x<0;x=abs(x);B=1<<m;p=B-1;digits=[]
    while x: digits.append(x&(B-1));x>>=m
    rem=0;quot=[]
    for a in reversed(digits):
        sm=rem+a;delta=int(sm>=p);quot.append(rem+delta);rem=sm-delta*p
    q=0
    for a in quot:q=(q<<m)+a
    if neg:return (-q,0) if rem==0 else (-q-1,p-rem)
    return q,rem

def normalize(a,m,base_p):
    carry=0;out=[];B=(1<<m)-int(base_p)
    for c in a:
        carry,d=local_div_p(c+carry,m) if base_p else divmod(c+carry,B)
        out.append(d)
    assert carry>=0
    while carry:
        carry,d=local_div_p(carry,m) if base_p else divmod(carry,B);out.append(d)
    while out and out[-1]==0:out.pop()
    return out

def val(a,B):
    z=0
    for x in reversed(a):z=z*B+x
    return z

def to_p(x,m):
    a=[]
    while x:a.append(x&((1<<m)-1));x>>=m
    return normalize(C.shift(a,1,m),m,True)

for m,L in ((2,1),(2,5),(3,8),(5,7),(8,9),(16,11),(31,7),(127,8),(521,9)):
    B=1<<m;p=B-1
    for mode in range(4):
        a=[B-1 if mode==0 else rng.randrange(B) for _ in range(L)]
        b=[B-1 if mode==1 else rng.randrange(B) for _ in range(L)]
        X=val(a,B);Y=val(b,B)
        ap=C.shift(a,1,m);bp=C.shift(b,1,m)
        assert val(ap,p)==X and val(bp,p)==Y
        canonical=normalize(ap,m,True)
        recovered=normalize(C.shift(canonical,-1,m),m,False)
        assert val(recovered,B)==X
        raw=convolution(ap,bp)
        binary=C.shift(raw,-1)
        assert binary==convolution(a,b) and val(normalize(binary,m,False),B)==X*Y
        record('full_roundtrip_lazy_raw_product',(m,L,mode,X,Y))
        for d in (1,2,3,L,L+3,1000000):
            # No large p**d is formed: evaluate actual chunks only.
            groups=[val(canonical[i:i+d],p) for i in range(0,len(canonical),d)]
            restored=[]
            for idx,g in enumerate(groups):
                pp=to_p(g,m)
                assert len(pp)<=d
                restored+=pp
                if idx+1<len(groups):restored+=[0]*(d-len(pp))
            assert val(restored,p)==X
            for g in groups:
                pp=to_p(g,m)
                assert val(normalize(C.shift(pp,-1,m),m,False),B)==g
            record('grouped_actual_width_roundtrip',(m,L,mode,d,groups))
        for d in (1,2,3):
            ac=normalize(ap,m,True);bc=normalize(bp,m,True)
            ga=[val(ac[i:i+d],p) for i in range(0,len(ac),d)]
            gb=[val(bc[i:i+d],p) for i in range(0,len(bc),d)]
            gc=convolution(ga,gb);expanded=[];hits=[]
            for j,c in enumerate(gc):
                digits=to_p(abs(c),m)
                while len(expanded)<j*d+len(digits):expanded.append(0);hits.append(0)
                for i,z in enumerate(digits):expanded[j*d+i]+=z;hits[j*d+i]+=1
            assert val(normalize(C.shift(expanded,-1),m,False),B)==X*Y
            # Bounded-overlap guarantee is asserted only when m>=L.
            if m>=L:assert max(hits,default=0)<=4
            record('raw_grouped_readout',(m,L,mode,d,gc))

# Signed floor division and raw signed p / p^d representations.
for m in range(2,10):
    for x in range(-1024,1025):
        assert local_div_p(x,m)==divmod(x,(1<<m)-1)
        record('signed_floor_division_oracle',(m,x,local_div_p(x,m)))
for m,L in ((3,5),(7,8),(31,9),(127,8),(521,6)):
    B=1<<m;p=B-1
    for trial in range(8):
        a=[rng.randrange(B) for _ in range(L)];X=val(a,B)
        raw=C.shift(a,1,m)
        for j in range(L-1):
            delta=rng.randrange(-p,p)
            raw[j]+=p*delta;raw[j+1]-=delta
        assert val(raw,p)==X
        out=normalize(C.shift(raw,-1),m,False)
        assert val(out,B)==X
        record('signed_raw_p_readout',(m,L,trial,raw))
        for d in (1,2,3):
            canonical=normalize(C.shift(a,1,m),m,True)
            grouped=[val(canonical[i:i+d],p) for i in range(0,len(canonical),d)]
            P=p**d  # Independent oracle perturbation only; no cost claim.
            for j in range(len(grouped)-1):
                delta=(-1 if j%2 else 1)*(P-1)
                grouped[j]+=P*delta;grouped[j+1]-=delta
            expanded=[]
            for j,c in enumerate(grouped):
                digits=to_p(abs(c),m)
                while len(expanded)<j*d+len(digits):expanded.append(0)
                for i,z in enumerate(digits):expanded[j*d+i]+=(-z if c<0 else z)
            assert val(normalize(C.shift(expanded,-1),m,False),B)==X
            record('signed_raw_grouped_readout',(m,L,trial,d,grouped))

# Explicit missing-carry / missing-denominator / missing-guard failures.
R=256;a=[65535,65535];k=[255,255]
good=C.narrow_convolution(a,k,16,8)
wrong=[sum((a[i]&255)*k[j-i] for i in range(j+1))&255 for j in range(2)]
wrong=[x+(x<<8) for x in wrong]
assert wrong!=good;record('negative_missing_slab_carry',(wrong,good))
a=[3,-7,11,-15,31,-63,127]
p=C.parameters(len(a),7);u,f,v,k=C.prepare(len(a),p['t']);M=1<<p['W']
A=[((u[i]*a[i])<<(p['g']-i.bit_count()))%M for i in range(len(a))]
D=convolution(A[::-1],k)
missing=[]
for j in range(len(a)):
    r=((D[len(a)-1-j]*pow(u[j],-1,M))<<j.bit_count())%M
    r>>=p['g']
    if r>=(1<<(p['H']-1)):r-=1<<p['H']
    missing.append(r)
assert missing!=horner_shift(a,1);record('negative_missing_denominator',(missing,horner_shift(a,1)))
# Guard omission destroys high reconstruction bits for some maximal-height data.
found=False
for n in range(2,15):
    h=5;pp=C.parameters(n,h);aa=[31]*n;truth=horner_shift(aa,1)
    for z in truth:
        truncated=((z<<pp['g'])% (1<<pp['H']))>>pp['g']
        if truncated!=z: found=True
assert found;record('negative_missing_guard')

# Cost ratios and actual-width counterexample independently checked as metadata.
examples=[]
for L,m in ((8,8192),(16,32768),(32,131072),(64,524288)):
    p=C.parameters(L,m);assert p['S']<L*m and p['t']<m
    small=C.parameters(L,0)
    examples.append({'L':L,'m':m,'N':L*m,'t':p['t'],'S':p['S'],'q':p['q'],'zero_actual_W':small['W'],'zero_actual_t':small['t']})
assert any(e['zero_actual_W']<e['zero_actual_t'] for e in examples)
record('capacity_and_width_boundary',examples)
result={'status':'PASS','counts':counts,'sha256':digest.hexdigest(),'examples':examples,
        'scope':'Independent correctness and operation/width controls; no timing inference. All tested production products use the explicit Karatsuba core. Native multiplication is confined to separate oracle and carry-identity calculations.','external_writes':False}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
