"""Independent controls: fresh polynomial oracles and instrumented copied code."""
import sys, json, hashlib, itertools, math, random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'candidate'))
import restricted_guards as rg
import dependencies.guarded_sharing as gs
rng=random.Random(0x202610181759)
records=[]
def rec(kind,data): records.append((kind,data))
def conv(a,b):
    return [sum(a[i]*b[k-i] for i in range(max(0,k-len(b)+1),min(len(a)-1,k)+1)) for k in range(len(a)+len(b)-1)]
def ev(c,x): return sum(v*pow(x,i) for i,v in enumerate(c))
def shift(c,s): return [sum(math.comb(i,j)*c[i]*pow(s,i-j) for i in range(j,len(c))) for j in range(len(c))]
def vp(x):
    if x==0: return None
    n=0
    while x%2==0: x//=2; n+=1
    return n
def factval(j): return sum(j//(1<<k) for k in range(1,j.bit_length()+1))
def gamma(n): return factval(n-1)
def box(m,L): return [sum(1 for i in range(L) if 0<=j-i<L)*((1<<m)-1)**2 for j in range(2*L-1)]
def prec(bounds): return max(factval(j)+max(1,b.bit_length()) for j,b in enumerate(bounds))

# Formula established without calling candidate product bounds or factorial guard.
for L in list(range(1,385))+[511,512,513,1023,1024,1025]:
    for m in [2,3,5,16,129,513]:
        bs=[min(j+1,2*L-1-j,L)*((1<<m)-1)**2 for j in range(2*L-1)]
        W=prec(bs); delta=int(L>=4 and L%2==0 and m>=3)
        assert W==2*m+factval(2*L-2)+delta
        assert rg.product_bounds(m,L)==bs
        assert rg.envelope_precision(bs)==W
        H=2*m+(L-1).bit_length()
        assert H+factval(2*L-2)-W==(L-1).bit_length()-delta
        rec('precision',[L,m,W])

# Arbitrary, nontriangular boxes, including n even, trailing zero, all zero.
for n in [1,2,3,4,5,8,9,16,25,40,65,98]:
    for mode in ['all_zero','spikes','random','trailing_zero']:
        bs=[0 if mode=='all_zero' else (1<<rng.randrange(1,80))-1 for j in range(n)]
        if mode=='spikes': bs=[v if j%3==0 else 0 for j,v in enumerate(bs)]
        if mode=='trailing_zero': bs[-1]=0
        for case in ['zero','max','random']:
            cs=[0 if case=='zero' else v if case=='max' else rng.randrange(v+1) for v in bs]
            for extra in [0,1,17]:
                W=prec(bs)+extra
                vals=[ev(cs,x)%(1<<W) for x in range(n)]
                st={}; out=rg.height_decode(vals,bs,W,st)
                assert out==cs
                assert st['low_bits']==W-gamma(n)
                assert st['residual_horner_small_actions']==n*n
                rec('arbitrary_box',[n,mode,case,extra,W])

# Tail solve instrumentation: every multiplication/division gets checked.
original_mul, original_div = rg.mul_small, rg.odd_divide_bits
for L in [1,2,3,4,5,8,13,24,49]:
    for m in [1,2,3,11,97,521]:
        bs=box(m,L); W=prec(bs); g=gamma(2*L-1); b=W-g
        tailbs=[v>>b for v in bs]; cs=[rng.randrange(v+1) for v in tailbs]
        vals=[ev(cs,x)%(1<<g) for x in range(len(cs))]
        mults=[]; divs=[]
        def counted_mul(v,s,w):
            out=original_mul(v,s,w)
            assert out==(v*s)% (1<<w)
            mults.append((v,s,w)); return out
        def counted_div(v,u,w):
            out=original_div(v,u,w)
            assert (out*u-v)%(1<<w)==0
            divs.append((u,w)); return out
        rg.mul_small,rg.odd_divide_bits=counted_mul,counted_div
        st={}; out=rg.short_tail_decode(vals,tailbs,g,st)
        rg.mul_small,rg.odd_divide_bits=original_mul,original_div
        assert out==cs and max(tailbs)<L
        n=len(cs)
        if g:
            assert len(mults)==(n-1)+n*(n-1)//2+n*(n+1)//2
            assert all(s<L and w==g for _,s,w in mults[(n-1)+n*(n-1)//2:])
            assert st['tail_odd_division_steps']==sum(g-factval(j) for j in range(n))
            assert len(divs)==sum(g>factval(j) for j in range(n))
            assert all(u==math.factorial(j)//(1<<factval(j)) for (u,w),j in zip(divs,[j for j in range(n-1,-1,-1) if g>factval(j)]))
        else:
            assert not mults and not divs and not any(cs)
        rec('instrumented_tail',[L,m,g,len(mults),len(divs)])

# Full route, with an independent exact shift oracle and phase product ledger.
orig_shift=rg.shift_mod
for L in [1,2,3,4,6,9,15,26]:
    for m in [2,3,7,32,129,513]:
        for mode in ['zero','max','edge','random']:
            a=[0 if mode=='zero' else (1<<m)-1 if mode=='max' else ((1<<m)-1 if i in [0,L-1] else 0) if mode=='edge' else rng.randrange(1<<m) for i in range(L)]
            bb=[rng.randrange(1<<m) if mode=='random' else x for x in a]
            phases=[]; calls=[]; current=['samples']; W=prec(box(m,L))
            def backend(x,y):
                calls.append((current[0],x.bit_length(),y.bit_length()))
                z=rg.karatsuba(x,y); assert z==x*y; return z
            def check_shift(v,s,w,p):
                current[0]='forward'+str(len(phases))
                out=orig_shift(v,s,w,p)
                assert out==[x%(1<<w) for x in shift(v,s)]
                phases.append((s,w)); current[0]='samples'; return out
            rg.shift_mod=check_shift
            x=sum(v<<(m*i) for i,v in enumerate(a)); y=sum(v<<(m*i) for i,v in enumerate(bb))
            st={}; out=rg.multiply_restricted(x,y,m,L,backend,st)
            rg.shift_mod=orig_shift
            assert out==x*y and st['final_coefficients']==conv(a,bb)
            assert phases==[(1,W),(1,W)]
            samplecalls=[r for r in calls if r[0]=='samples']
            assert len(samplecalls)==2*L-1
            h=m if L==1 else min(W,m+(L-1).bit_length()+(L-1)*(2*L-3).bit_length())
            assert max(max(x,y) for _,x,y in samplecalls)<=h
            assert rg.restricted_convolution(a,bb,m)==st['final_coefficients']
            rec('full_route',[L,m,mode,W,h,len(calls)])

# Fresh witness generation by repeated multiplication, independent of binomial sums.
for a in range(1,11):
    for b in range(a+1):
        R=[1]
        for i in range(a): R=conv(R,[-1,1])
        for i in range(b): R=conv(R,[1,1])
        C=max(map(abs,R)); t=C.bit_length(); A=3*a+b; D=5*a+3*b
        L=max((D+1)//2+1,2*(a+b)+1)
        for m in [t,t+1,t+19]:
            F=[0]*L; P=[0]*L; M=[0]*L
            s=min(A,L-1); F[s]=1<<(m-1)
            for j,c in enumerate(R):
                P[A-s+2*j]=max(c,0)<<(m-t)
                M[A-s+2*j]=max(-c,0)<<(m-t)
            assert all(0<=c<(1<<m) for c in F+P+M)
            pp,mm=conv(F,P),conv(F,M); diff=[v-w for v,w in zip(pp,mm)]
            e=2*m-1-t; collision=e+A; H=2*m+(L-1).bit_length()
            assert diff[D]==1<<e and any(v%(1<<H) for v in diff)
            for x in [-10003,-257,-19,-3,-2,-1,0,1,2,3,17,256,10007]:
                expected=(1<<e)*pow(x,A)*pow(x*x-1,a)*pow(x*x+1,b)
                assert ev(diff,x)==expected and expected%(1<<collision)==0
            assert all(vp(ev(diff,x))==collision for x in [-3,-2,2,3])
            for tr in [-7,-1,1,4]:
                tt=shift(diff,tr)
                assert any(v%(1<<H) for v in tt)
                for z in [-11,-2,0,3,12]: assert ev(tt,z)%(1<<collision)==0
            assert max(0,collision-H+1)==max(0,3*a+b-t-(L-1).bit_length())
            rec('bounded_witness',[L,a,b,m,t,collision,H])

# Improved asymptotic constant: integer norm bound and explicit finite inequality.
const=(16-math.log2(200*math.sqrt(5)/27))/14
assert abs(const-0.8535762332)<1e-10
for s in [1,2,3,5,7,11,19,31,53]:
    R=[1]
    for j in range(5*s): R=conv(R,[-1,1])
    for j in range(s): R=conv(R,[1,1])
    C=max(map(abs,R)); t=C.bit_length()
    assert C*C*729**s<=200000**s
    assert t<=s*math.log2(200*math.sqrt(5)/27)+1
    for L in [14*s+1,14*s+7,14*s+14]:
        assert (L-1)//14==s
        lower=16*s-t-(L-1).bit_length()
        bound=(16-math.log2(200*math.sqrt(5)/27))*s-1-(L-1).bit_length()
        assert lower+1e-10>=bound
        rec('improved_constant',[s,L,t,lower])

# All residue nodes, rather than only n consecutive, establish tiny minima.
for m,L in [(1,1),(1,2),(1,3),(1,4),(1,5),(2,2),(2,3),(3,2)]:
    arrays=list(itertools.product(range(1<<m),repeat=L))
    ps=set(tuple(conv(a,b)) for i,a in enumerate(arrays) for b in arrays[i:])
    minimum=None; last=None
    for W in range(0,prec(box(m,L))+1):
        seen={}; collision=None
        for p in ps:
            sig=tuple(ev(p,x)%(1<<W) for x in range(1<<W))
            if sig in seen and seen[sig]!=p: collision=(seen[sig],p); break
            seen[sig]=p
        if collision is None: minimum=W; break
        last=collision
    assert minimum is not None and minimum>=1
    # Each consecutive signature agrees exactly with the full-node equivalence.
    W=minimum-1
    grouped={}
    for p in ps:
        sig=tuple(ev(p,x)%(1<<W) for x in range(2*L-1))
        full=tuple(ev(p,x)%(1<<W) for x in range(1<<W))
        if sig in grouped: assert grouped[sig]==full
        grouped[sig]=full
    rec('full_residue_minimum',[m,L,len(ps),minimum])

counts={}
for k,v in records: counts[k]=counts.get(k,0)+1
out={'status':'PASS','counts':counts,'constant':const,'digest':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),'tiny_minima':[v for k,v in records if k=='full_residue_minimum']}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
