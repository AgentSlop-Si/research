#!/usr/bin/env python3
"""Independent review controls written after source inspection.
Only the candidate under review is imported; reference arithmetic and test inputs
are newly written. Native products/divisions are endpoint oracles, not production.
"""
import ast, copy, hashlib, importlib.util, json, math, pathlib, random, time
HERE=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path(__file__).resolve().parent / '../candidate'
EXPECTED='a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06'
assert hashlib.sha256((SRC/'shared_dispatcher.py').read_bytes()).hexdigest()==EXPECTED
import sys
sys.path.insert(0,str(SRC))
import shared_dispatcher as M
rng=random.Random(20261017214709)
R={'seed':20261017214709,'counts':{},'products':[],'candidate_source_sha256':EXPECTED}

def count(name,n=1): R['counts'][name]=R['counts'].get(name,0)+n

def choose(x,j):
    if j==0:return 1
    if x>=0:return math.comb(x,j) if j<=x else 0
    return (-1)**j*math.comb(j-x-1,j)

def ref_plan(r):
    L=math.lcm(*range(1,r+1));d=L//r
    moduli=[];residues=[]
    for p in range(2,r+1):
        if any(p%h==0 for h in range(2,math.isqrt(p)+1)):continue
        q=1;u=1
        while d%(q*p)==0:q*=p
        if q==1:continue
        while L%(u*p)==0:u*=p
        moduli.append(q);residues.append((-pow(L//u,-1,q))%q)
    k=1 if d==1 else sum(a*(d//q)*pow(d//q,-1,q) for a,q in zip(residues,moduli))%d
    P=1+k*L
    W=[math.comb(P+j-1,j) for j in range(r+1)]
    assert W[r]%d==0
    s=(W[r]//d).bit_length()-1
    rows={x:tuple((-1)**j*choose(x,j) for j in range(r)) for x in range(1-r,2*r-1)}
    shift=min(range(r),key=lambda a:(max(sum(map(abs,rows[-a])),sum(map(abs,rows[2*r-2-a]))),a))
    nodes=tuple(range(-shift,2*r-1-shift))
    return P,s,tuple(W[:-1]),nodes,tuple(rows[x] for x in nodes),tuple(choose(-P-nodes[0],j) for j in range(2*r-1))

for name,meta in json.loads((SRC/'MANIFEST.json').read_text())['files'].items():
    data=(SRC/name).read_bytes();assert len(data)==meta['bytes'];assert hashlib.sha256(data).hexdigest()==meta['sha256'];count('manifest_entries')

for r in range(2,41):
    p=M.native_plan(r,M.Elementary());ref=ref_plan(r)
    assert (p.point,p.block_bits,p.weights,p.nodes,p.rows,p.interpolation)==ref
    count('independent_native_plans')
    vals={0,1,(1<<p.block_bits)-1,p.point-1,p.point,p.point+1}
    vals.update(w+delta for w in p.weights for delta in [-1,0,1] if 0<=w+delta<1<<p.block_bits)
    vals.update(rng.randrange(1<<p.block_bits) for _ in range(8))
    for a in vals:
        c=M.canonical(a,p,M.Elementary())
        rem=a;oracle=[0]*r
        for j in reversed(range(r)):oracle[j],rem=divmod(rem,p.weights[j])
        assert tuple(oracle)==c and rem==0
        assert all(0<=v<p.point for v in c)
        assert sum(v*w for v,w in zip(c,p.weights))==a
        assert sum(v*(-1)**j*choose(-p.point,j) for j,v in enumerate(c))==a
        count('canonical_boundary_cases')

# Independently convolve signed rows, including negative packed operands and
# maximal centered coefficients. No candidate interpolation is used as oracle.
for L in [1,2,3,7,16,31]:
    for z in range(30):
        ar=[rng.randrange(-500,501) for _ in range(L)]
        br=[rng.randrange(-500,501) for _ in range(L)]
        if z%3==0:ar[-1]=-abs(ar[-1])-1
        if z%4==0:br[-1]=-abs(br[-1])-1
        A=max(map(abs,ar));B=max(map(abs,br));E=M.Elementary()
        w,bound=M.slot_width(L,A,B,E);Q=1<<w
        assert w==8*((2*L*A*B).bit_length()+7>>3) and Q>2*L*A*B
        U=sum(a*Q**i for i,a in enumerate(ar));V=sum(a*Q**i for i,a in enumerate(br))
        assert M.pack(ar,w,E)==U and M.pack(br,w,E)==V
        conv=[sum(ar[i]*br[k-i] for i in range(L) if 0<=k-i<L) for k in range(2*L-1)]
        assert M.unpack(U*V,w,2*L-1,bound,E)==conv
        count('signed_stream_convolutions')
        if U*V<0:count('negative_packed_products')
for q in range(1,65):
    for delta in [-2,-1,0,1,2]:
        B=(1<<(8*q-1))+delta
        w,b=M.slot_width(1,1,B,M.Elementary())
        assert w==8*((2*B).bit_length()+7>>3) and (1<<w)>2*b
        count('strict_width_boundaries')

# Byte boundaries, long carries, zero gaps and nonzero outer shifts.
for s in [1,2,3,7,8,9,15,16,17,31,32,33,63,64,65,127,128,129]:
    for length in [1,2,3,19]:
        coeff={i:rng.randrange(1<<(2*s+7)) for i in range(length) if i%3==0 or i==length-1}
        v=sum(c<<(s*i) for i,c in coeff.items())
        assert M.assemble(coeff,s,length-1,M.Elementary())==v
        bs=M.split_blocks(v,s,M.Elementary())
        assert sum(c<<(s*i) for i,c in enumerate(bs))==v
        count('carrying_stream_roundtrips')

def product(label,a,b,**kwargs):
    d=M.Dispatcher(**kwargs);v=d.multiply(a,b)
    assert v==a*b,label
    R['products'].append({'label':label,'input_bits':[abs(a).bit_length(),abs(b).bit_length()],**d.summary()})
    print(label,d.summary()['dispatcher'],flush=True)
    return d

for j in range(32):
    n=rng.randrange(9,193);m=rng.randrange(1,193)
    a=(rng.getrandbits(n)|1)*(-1 if j&1 else 1)
    b=(rng.getrandbits(m)|1)*(-1 if j&2 else 1)
    product('low-threshold-'+str(j),a<<rng.randrange(15),b<<rng.randrange(15),base_bits=8,support_limit=1+(j%4))
for n in [1025,1537,2049,4097,6001]:
    product('dense-random-'+str(n),-(rng.getrandbits(n)|(1<<(n-1))|1),rng.getrandbits(n-31)|1)
product('unequal-one-bit',-1,(1<<8193)-1)
product('zero-high-input',0,1<<200000)
product('huge-shift-small-core',-(17<<190003),31<<8027)

for r in [10,12,15]:
    P,s,_,_,_,_=ref_plan(r);K=((1<<r)+s-1)//s
    sets=[([0,K],[0,K-1]),([0,1,2,K],[0,1,K-1,K])]
    for q,(apos,bpos) in enumerate(sets):
        a=sum(((1<<s)-1)<<(s*k) for k in apos)
        b=sum((rng.randrange(1,1<<s)|1)<<(s*k) for k in bpos)
        assert max(a.bit_length(),b.bit_length()).bit_length()-1==r
        d=product('max-block-carry-r%d-%d'%(r,q),-a,b)
        assert d.stats['calls']==1 and d.stats['sparse_shared']==1
        c=d.certificates[0]['certificate'];ex=d.certificates[0]['execution']
        # Independent direct polynomial oracle for every exposed row.
        p=d.plans[r];bs=(M.split_blocks(a,s,M.Elementary()),M.split_blocks(b,s,M.Elementary()))
        for row in ex['rows']:
            x=row['node'];refrows=[]
            for side in bs:
                rr=[]
                for k,v in enumerate(side):
                    if not v:continue
                    rem=v;digits=[0]*r
                    for j in reversed(range(r)):digits[j],rem=divmod(rem,p.weights[j])
                    rr.append([k,sum(digits[j]*(-1)**j*choose(x,j) for j in range(r))])
                refrows.append(rr)
            assert refrows==row['input_terms']
            conv={}
            for i,aa in refrows[0]:
                for j,bb in refrows[1]:conv[i+j]=conv.get(i+j,0)+aa*bb
            assert row['product_terms']==[[k,v] for k,v in sorted(conv.items())]
            count('independent_shared_rows')
        actualconv={}
        for i,aa in enumerate(bs[0]):
            if not aa:continue
            for j,bb in enumerate(bs[1]):
                if bb:actualconv[i+j]=actualconv.get(i+j,0)+aa*bb
        assert ex['output_terms']==[[k,v] for k,v in sorted(actualconv.items())]
        count('independent_block_convolutions')

# Five supports are rejected even when the final added block is far into a gap.
r=12;P,s,_,_,_,_=ref_plan(r);K=((1<<r)+s-1)//s
A=sum((P+2)<<(s*k) for k in [0,1,2,3,K]);B=(P+3)+(7<<(s*(K-1)))
d=product('fifth-support-gap',A,-B)
assert d.stats['dense_fallback']>=1

# Repeated nonconstant leaf, colliding convolution positions, scaled contents,
# and direct compiler outer shifts. All node widths checked against actual rows.
p=M.native_plan(13,M.Elementary());F=p.point+2
blocks=([0,0,3*F,9*F,15*F],[0,5*F,15*F,25*F])
c=M.compile_sparse(*blocks,p,M.Elementary(),4)
assert M.check_structure(c,blocks,p,M.Elementary(),4)
out,ex=M.evaluate_shared(c,blocks,p,M.Elementary())
assert M.check_execution(c,ex,blocks,p,M.Elementary())
assert len(c['leaves'])==1 and len(c['product_nodes'])==1
assert ex['edge_count_before_combining']==9 and ex['edge_count_after_combining']==5
assert [v['common_content'] for v in c['sides']]==[3,5]
assert [v['outer_shift'] for v in c['sides']]==[2,1]
assert out=={k:sum(a*b for i,a in enumerate(blocks[0]) for j,b in enumerate(blocks[1]) if i+j==k) for k in range(3,8)}
R['merge_control']={'before':9,'after':5,'memo_hits':ex['memo_hits'],'memo_misses':ex['memo_misses']}
# Fresh mutations beyond the producer suite.
mutations={
 'negative-position':lambda z:z['sides'][0]['terms'][0].__setitem__(0,-1),
 'duplicate-position':lambda z:z['sides'][0]['terms'][1].__setitem__(0,z['sides'][0]['terms'][0][0]),
 'missing-side':lambda z:z['sides'].pop(),
 'extra-side':lambda z:z['sides'].append(copy.deepcopy(z['sides'][0])),
 'negative-leaf':lambda z:z['leaves'][0].__setitem__(0,-1),
 'nonprimitive-leaf':lambda z:z['leaves'].__setitem__(0,[2*v for v in z['leaves'][0]]),
 'invalid-product-index':lambda z:z['product_nodes'][0].__setitem__(0,99),
 'missing-edge':lambda z:z['edges'].pop(),
 'duplicate-product':lambda z:z['product_nodes'].append(copy.deepcopy(z['product_nodes'][0])),
 'shift-content-pair':lambda z:z['sides'][1].__setitem__('common_content',1),
}
for label,mutate in mutations.items():
    bad=copy.deepcopy(c);mutate(bad)
    assert not M.check_structure(bad,blocks,p,M.Elementary(),4),label
    count('fresh_structure_rejections')
for label,mutate in {
 'missing-node':lambda z:z['rows'].pop(),
 'changed-row-term':lambda z:z['rows'][0]['input_terms'][0][0].__setitem__(1,42),
 'deleted-zero-column':lambda z:z['rows'][0]['product_terms'].pop(),
 'changed-output-position':lambda z:z['output_terms'][0].__setitem__(0,999),
}.items():
    bad=copy.deepcopy(ex);mutate(bad)
    assert not M.check_execution(c,bad,blocks,p,M.Elementary()),label
    count('fresh_execution_rejections')

# Reproduce the distinct odd witness independently, including exact ordinary
# source child products. Child products here use the oracle only for checking.
r=17;P,s,_,nodes,_,_=ref_plan(r);K=((1<<r)+s-1)//s;C=2049;A=(C<<(s*K))+P
D=product('independent-distinct-odd-witness',A,-A)
cert=D.certificates[0];ex=cert['execution'];pairs=[]
for x,row in zip(nodes,ex['rows']):
    w=row['slot_bits'];Q=1<<w;U=(C<<(K*w))-x
    pairs.append((U,U))
    h=sum(v*Q**k for k,v in row['product_terms'])
    assert h==U*U
    assert row['bound']==(K+1)*C*C
    assert w==8*((2*(K+1)*C*C).bit_length()+7>>3)
    count('distinct_witness_source_products')
assert len(set(pairs))==33 and sum(U&1 for U,V in pairs)==16
assert set(abs(U).bit_length() for U,V in pairs)=={6380}
assert D.stats['calls']==1 and D.E.max_mul_bits<6380
R['distinct_odd_witness']={'pairs':33,'odd':16,'child_bits':6380,'largest_elementary_operand_bits':D.E.max_mul_bits,'input_bits':A.bit_length()}

# Independently rerun the finite diagnostic ledger, without claiming timing.
r=14;P,s,_,_,_,_=ref_plan(r);K=((1<<r)+s-1)//s;x=(513<<(s*K))+P
S=product('ledger-shared',x,x);T=product('ledger-forced-dense',x,x,force_dense=True)
a=S.E.summary()['charged_bit_work'];b=T.E.summary()['charged_bit_work']
old=json.loads((SRC/'CONTROL_RESULTS.json').read_text())['cost_comparison']
assert a==old['shared']['backend']['charged_bit_work'] and b==old['dense']['backend']['charged_bit_work']
R['primitive_charge_comparison']={'shared':a,'dense':b,'ratio':b/a,'not_wall_clock':True}
R['all_passed']=True
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps({'counts':R['counts'],'complete_products':len(R['products']),'comparison':R['primitive_charge_comparison'],'all_passed':True},indent=2),flush=True)
