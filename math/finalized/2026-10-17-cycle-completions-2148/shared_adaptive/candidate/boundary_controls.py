#!/usr/bin/env python3
"""Fresh exact primitive, stream, legality, and unequal-input boundary controls."""
import json,pathlib,random
from shared_dispatcher import Elementary,Dispatcher,native_plan,canonical,split_blocks,assemble,digest
HERE=pathlib.Path(__file__).resolve().parent
rng=random.Random(213017102026);E=Elementary();tests={}
for a in range(-32,33):
    for b in range(-32,33):assert E.mul(a,b)==a*b
tests['small_signed_multiplications']=65*65
for a in range(128):
    for b in range(1,33):assert E.divmod(a,b)==divmod(a,b)
tests['small_long_divisions']=128*32
for _ in range(100):
    a=rng.getrandbits(256);b=rng.getrandbits(128)|1
    assert E.mul(a,b)==a*b and E.divmod(a,b)==divmod(a,b)
    assert E.mod(-a,b)==(-a)%b
tests['large_primitive_pairs']=100
for s in range(1,66):
    for _ in range(4):
        a=rng.getrandbits(rng.randrange(1,2000));bs=split_blocks(a,s,E)
        assert all(0<=b<(1<<s) for b in bs)
        assert assemble(dict(enumerate(bs)),s,len(bs)-1,E)==a
tests['stream_round_trips']=65*4
for r in range(3,21):
    p=native_plan(r,E)
    for _ in range(6):
        a=rng.randrange(1<<p.block_bits);c=canonical(a,p,E)
        assert sum(x*w for x,w in zip(c,p.weights))==a
        assert all(0<=x<p.point for x in c)
tests['legal_canonical_blocks']=18*6
products=[]
for label,a,b,kwargs in [
    ('unequal-dense',rng.getrandbits(4096)|1,3,{}),
    ('negative-unbalanced',-(rng.getrandbits(2048)|1),-1,{}),
    ('all-ones',(1<<2048)-1,(1<<2047)-1,{}),
    ('independent-large-shifts',(rng.getrandbits(2048)|1)<<901,-((rng.getrandbits(2048)|1)<<577),{}),
    ('minimal-base-positive',511,477,{'base_bits':8}),
    ('minimal-base-signed',-1023,1001,{'base_bits':8}),
    ('support-one-fallback',65537,1048577,{'base_bits':8,'support_limit':1}),
]:
    d=Dispatcher(**kwargs);v=d.multiply(a,b);assert v==a*b
    products.append({'label':label,'output_sha256':digest(v),**d.summary()})
    print(label,d.summary()['dispatcher'],flush=True)
tests['additional_complete_products']=len(products)
(HERE/'BOUNDARY_RESULTS.json').write_text(json.dumps({'counts':tests,'products':products,'all_passed':True},indent=2)+'\n')
print(tests,flush=True)
