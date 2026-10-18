#!/usr/bin/env python3
"""New review controls. Execute inspected new definitions, never historical modules.

The fresh adapter uses host arithmetic solely as an independent test oracle. It
does not claim to rerun the inherited production backend or its cost ledger.
"""
import ast
import copy
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import sys
from types import ModuleType, SimpleNamespace

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent / 'candidate'
EXPECTED = '47101aabdb3789846e3822226c0ff1089b150ff5af0419b61fb036a169a154df'
COUNTS = dict(canonical_convexity=0, endpoint_runs=0, endpoint_accepts=0,
              graph_products=0, source_nodes=0, convolution_checks=0,
              rejected_mutations=0, strict_family=0, signed_products=0,
              negative_decoded_normalized_leaves=0, recovery_tail_rejections=0)
RNG = random.Random(202610181055)


class Arithmetic:
    def __init__(self): self.multiplications = 0; self.max_operand = 0
    def add(self, a, b): return a+b
    def mul(self, a, b):
        self.multiplications += 1
        self.max_operand = max(self.max_operand, abs(a).bit_length(), abs(b).bit_length())
        return a*b
    def tick(self, *args): pass
    def summary(self): return {'oracle_multiplications': self.multiplications,
                              'max_oracle_operand_bits': self.max_operand}


def binomial(x, k):
    if x >= 0: return math.comb(x, k) if k <= x else 0
    return (-1)**k * math.comb(k-x-1, k)


PLANS = {}
def fresh_plan(r, E=None):
    if r in PLANS: return PLANS[r]
    H = math.lcm(*range(1, r+1)); d = H//r
    moduli, residues = [], []
    for p in range(2, r+1):
        if any(p % q == 0 for q in range(2, math.isqrt(p)+1)): continue
        q = 1
        while d % (q*p) == 0: q *= p
        if q == 1: continue
        u = 1
        while H % (u*p) == 0: u *= p
        moduli.append(q); residues.append((-pow(H//u, -1, q)) % q)
    if d == 1: k = 1
    else:
        k = sum(a*(d//m)*pow(d//m, -1, m) for a, m in zip(residues, moduli)) % d
    assert math.prod(moduli) == d and 1 <= k <= max(1, d-1)
    P = 1+k*H
    W = tuple(math.comb(P+j-1, j) for j in range(r+1))
    assert W[-1] % d == 0
    s = (W[-1]//d).bit_length()-1
    # Determine the minimax translation by evaluating every node norm, rather
    # than inheriting the endpoint optimization or production plan builder.
    row = lambda x: tuple((-1)**j*binomial(x, j) for j in range(r))
    left = min(range(r), key=lambda a: (max(sum(map(abs, row(x)))
                        for x in range(-a, 2*r-1-a)), a))
    xs = tuple(range(-left, 2*r-1-left))
    lagrange = []
    for x in xs:
        v = Fraction(1)
        for y in xs:
            if x != y: v *= Fraction(-P-y, x-y)
        assert v.denominator == 1
        lagrange.append(v.numerator)
    plan = SimpleNamespace(rank=r, point=P, block_bits=s, weights=W[:-1],
                           nodes=xs, rows=tuple(map(row, xs)), lagrange=lagrange)
    PLANS[r] = plan
    return plan


def canonical(a, plan, E=None):
    out = [0]*plan.rank
    for j in reversed(range(plan.rank)):
        out[j], a = divmod(a, math.comb(plan.point+j-1, j))
    assert a == 0
    return tuple(out)


def evaluate(v, row, E=None): return sum(a*b for a, b in zip(v, row))
def polynomial(v, x): return sum(c*(-1)**j*binomial(x, j) for j, c in enumerate(v))
def interpolate(values, plan, E=None): return sum(a*b for a,b in zip(values,plan.lagrange))
def slot_width(L, A, B, E=None):
    bound=L*A*B
    return 8*(((2*bound).bit_length()+7)//8), bound
def split(a, s, E=None): return [(a >> (i*s)) & ((1 << s)-1) for i in range(max(1,(a.bit_length()+s-1)//s))]
def integer(v, s): return sum(a << (s*i) for i,a in enumerate(v))
def assemble(c, s, last, E=None): return integer(c[:last+1], s)
def normalize(v):
    sign = 1 if next(c for c in v if c) > 0 else -1
    return sign, tuple(sign*c for c in v)
FALLBACK_CALLS=[]
def fallback(a,b,**kwargs):
    FALLBACK_CALLS.append((a.bit_length(),b.bit_length(),kwargs))
    return a*b


def load_new_definitions():
    raw=(CANDIDATE/'affine_shared.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    parsed=ast.parse(raw, filename=str(CANDIDATE/'affine_shared.py'))
    body=[n for n in parsed.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
    assert len(body)==12
    module=ModuleType('fresh_affine_review_candidate')
    sys.modules[module.__name__]=module
    module.__dict__.update(dataclass=dataclass,
        base=SimpleNamespace(Elementary=Arithmetic, native_plan=fresh_plan,
            canonical=canonical,evaluate=evaluate,interpolate=interpolate,
            slot_width=slot_width,split_blocks=split,assemble=assemble,
            bits=lambda a:max(1,abs(a).bit_length())),
        accepted=SimpleNamespace(signed_normalize=normalize,multiply=fallback))
    exec(compile(ast.Module(body=body,type_ignores=[]),str(CANDIDATE/'affine_shared.py'),'exec'),module.__dict__)
    return module


def conv(a,b):
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): z[i+j]+=x*y
    return z
def diff(a): return [a[0]]+[a[i]-a[i-1] for i in range(1,len(a))]+[-a[-1]]
def dn(a,n):
    for _ in range(n): a=diff(a)
    return a


prod=load_new_definitions()


def check_run(bs,p):
    rs=prod.certify_runs(bs,[(0,len(bs))],p,Arithmetic())
    actual=[canonical(a,p) for a in bs]
    slope=tuple(b-a for a,b in zip(actual[0],actual[1])) if len(bs)>1 else (0,)*p.rank
    oracle=all(v==tuple(a+i*b for a,b in zip(actual[0],slope)) for i,v in enumerate(actual))
    assert (rs is not None)==oracle
    COUNTS['endpoint_runs']+=1
    COUNTS['endpoint_accepts']+=int(oracle)


def check_graph(a,b,p):
    parts=tuple(prod.affine_partition(bs) for bs in (a,b))
    rs=tuple(prod.certify_runs(bs,part,p,Arithmetic()) for bs,part in zip((a,b),parts))
    if any(v is None for v in rs): return None
    g=prod.make_graph(rs,(len(a),len(b)),p,Arithmetic())
    e=prod.evaluate_graph(g,p,Arithmetic())
    COUNTS['negative_decoded_normalized_leaves']+=sum(
        sum(c*w for c,w in zip(v,p.weights))<0 for v in g['leaves'])
    assert prod.check_certificate((a,b),g,e,p,Arithmetic())
    recovered,peak=prod.integrate_events(g,e['targets'],Arithmetic())
    assert recovered==conv(a,b)
    COUNTS['convolution_checks']+=1
    assert integer(recovered,p.block_bits)==integer(a,p.block_bits)*integer(b,p.block_bits)
    vectors=([canonical(v,p) for v in a],[canonical(v,p) for v in b])
    for side,bs in enumerate((a,b)):
        assert len(g['sides'][side])<=4*len(rs[side])
        for j in range(p.rank):
            expected=dn([v[j] for v in vectors[side]],2)
            actual=[0]*len(expected)
            for pos,leaf,sg in g['sides'][side]: actual[pos]=sg*g['leaves'][leaf][j]
            assert actual==expected
            assert all(abs(v)<2*p.point for v in actual)
    for xi,x in enumerate(p.nodes):
        ar=[polynomial(v,x) for v in vectors[0]]
        br=[polynomial(v,x) for v in vectors[1]]
        event=[0]*(len(a)+len(b)+3)
        for pos,product,sign in g['events']: event[pos]+=sign*e['product_rows'][product][xi]
        assert event==dn(conv(ar,br),4)==conv(dn(ar,2),dn(br,2))
        ma,mb=max(map(abs,ar)),max(map(abs,br)); bound=max(len(a),len(b))*ma*mb
        width=8*(((2*bound).bit_length()+7)//8) if bound else 0
        assert e['source_rows'][xi]==(x,ma,mb,width,bound)
        if bound:
            assert (1<<width)>2*bound and width%8==0
            # Literal packed source identities at their original node width.
            y=1<<width
            pa=sum(v*pow(y,i) for i,v in enumerate(ar))
            pb=sum(v*pow(y,i) for i,v in enumerate(br))
            pe=sum(v*pow(y,i) for i,v in enumerate(event))
            assert pe==(1-y)**4*pa*pb
        COUNTS['source_nodes']+=1; COUNTS['convolution_checks']+=2
    COUNTS['graph_products']+=1
    return g,e


def main():
    manifest=json.loads((CANDIDATE/'MANIFEST.json').read_text())
    for f in manifest['files']:
        raw=(CANDIDATE/f['path']).read_bytes()
        assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256']

    # Generic greedy-canonical convexity, including non-divisibility weights.
    for weights in ((1,3,7),(1,2,5,13),(1,4,9),(1,5,6)):
        for c in itertools.product(range(6),repeat=len(weights)):
            a=sum(x*w for x,w in zip(c,weights)); rem=a; got=[]
            for w in reversed(weights): q,rem=divmod(rem,w);got.append(q)
            criterion=all(sum(c[j]*weights[j] for j in range(h))<weights[h] for h in range(1,len(weights)))
            assert (tuple(reversed(got))==c)==criterion
            COUNTS['canonical_convexity']+=1

    for r in range(2,31):
        p=fresh_plan(r);H=math.lcm(*range(1,r+1))
        assert p.point>H and all(H%math.comb(r,j)==0 for j in range(r+1))
        assert H>=math.comb(r,r//2)>=Fraction(2**r,r+1)
    for r in (2,3):
        p=fresh_plan(r); cap=1<<p.block_bits
        for length in range(1,10):
            for start in range(cap):
                for d in range(-cap,cap+1):
                    if length==1 and d: continue
                    if all(0<=start+i*d<cap for i in range(length)):
                        check_run([start+i*d for i in range(length)],p)
    for r in (4,6,9,12,16,20):
        p=fresh_plan(r);cap=1<<p.block_bits
        for _ in range(350):
            length=RNG.randrange(2,35)
            a,b=sorted((RNG.randrange(cap),RNG.randrange(cap)))
            step=(b-a)//(length-1)
            bs=[a+i*step for i in range(length)]
            if RNG.randrange(2): bs.reverse()
            check_run(bs,p)
        # Long guaranteed passes exercise the convexity certificate strongly.
        for length in (3,17,81):
            offset=p.weights[-1]
            if offset+length<cap: check_run([offset+i for i in range(length)],p)

    for r in (2,3,4,6,9,12):
        p=fresh_plan(r);cap=1<<p.block_bits
        for _ in range(35):
            a=[RNG.randrange(cap) for _ in range(RNG.randrange(1,13))]
            b=[RNG.randrange(cap) for _ in range(RNG.randrange(1,13))]
            check_graph(a,b,p)
        for a,b in (([0],[0]),([0,0,1,0],[1,0,0]),([1],[1]),
                    ([1,2,3,0,0,0,2,1],[3,2,1,2,2]),
                    (list(range(1,18)),list(range(17,0,-1)))):
            if max(a+b)<cap: check_graph(a,b,p)
    for r in (6,10,16):
        p=fresh_plan(r)
        check_graph([p.point-1,p.point+1],[p.point+1,p.point-1],p)
    assert COUNTS['negative_decoded_normalized_leaves']>0

    # Strict-family and full new front-end checks under the fresh oracle shim.
    families=[]
    for r in (10,12,14,16,18,20):
        p=fresh_plan(r);L=(2**r+p.block_bits-1)//p.block_bits+1
        assert L<p.point
        a=integer(list(range(1,L+1)),p.block_bits)
        b=integer(list(range(L,0,-1)),p.block_bits)
        N=max(a.bit_length(),b.bit_length())
        assert N.bit_length()-1==r
        old_cost=(L+1)**2*r**4; new_cost=r**4
        result=prod.multiply_affine(-a,b,budget_factor=64)
        assert result and result.value==-a*b
        assert result.statistics['run_counts']==(1,1)
        assert result.statistics['difference_counts']==(3,3)
        assert result.statistics['pair_events']==9
        assert new_cost<=64*N
        COUNTS['strict_family']+=int(old_cost>64*N)
        COUNTS['signed_products']+=1
        families.append(dict(rank=r,bits=N,length=L,block_bits=p.block_bits,
                             old_budget_rejected=old_cost>64*N,events=9,
                             shared_products=result.statistics['shared_products']))
        if r in (12,16,20):
            top=(((1<<p.block_bits)-1)//p.weights[-1]-1)*p.weights[-1]
            aa=integer([top+i+1 for i in range(L)],p.block_bits)
            bb=integer([top+L-i for i in range(L-2)],p.block_bits)
            result=prod.multiply_affine(aa,-bb,budget_factor=64)
            assert result and result.value==-aa*bb
            assert result.statistics['largest_prefix_bits']>p.block_bits
            COUNTS['signed_products']+=1
    for a,b in ((0,9),(-7,4),(1,-1),((1<<1023)-1,(1<<1022)+1)):
        assert prod.multiply(a,b)==a*b;COUNTS['signed_products']+=1

    p=fresh_plan(12); L=(2**12+p.block_bits-1)//p.block_bits+1
    a=integer(list(range(1,L+1)),p.block_bits)
    saved=prod.certify_runs
    def forbidden(*args,**kwargs):raise AssertionError('forbidden late stage executed')
    prod.certify_runs=forbidden
    assert prod.multiply_affine(a,a,budget_factor=0) is None
    prod.certify_runs=saved
    before=len(FALLBACK_CALLS); assert prod.multiply(a,-a,affine_budget=0)==-a*a
    assert len(FALLBACK_CALLS)==before+1
    p=fresh_plan(10);L=(2**10+p.block_bits-1)//p.block_bits+1
    a=integer([p.point-1+i for i in range(L)],p.block_bits)
    saved=prod.make_graph;prod.make_graph=forbidden
    assert prod.multiply_affine(a,a,budget_factor=64) is None
    prod.make_graph=saved

    # Dense carry and higher-order obstructions, independently reconstructed.
    obstructions=[]
    for r in (6,10,16):
        p=fresh_plan(r);bs=[(i+1)*((p.point+1)//2) for i in range(90)]
        assert max(bs)<1<<p.block_bits
        assert prod.affine_partition(bs)==[(0,len(bs))]
        assert prod.certify_runs(bs,[(0,len(bs))],p,Arithmetic()) is None
        support=sum(x!=0 for x in dn([canonical(v,p)[0] for v in bs],2))
        assert support>=len(bs)-2
        obstructions.append({'rank':r,'blocks':len(bs),'low_coordinate_support':support})
    p=fresh_plan(10);q=(p.point+23)//24;bs=[q*t*(10-t) for t in range(11)]
    assert all(canonical(bs[t],p)==(bs[t],)+(0,)*(p.rank-1) for t in (0,1,2,10))
    assert canonical(bs[5],p)!=(bs[5],)+(0,)*(p.rank-1)

    # Reject certificate and dense binding mutations; all mutations are fresh.
    bs=([1,2,3,4,5,8,10,12],[4,3,2,1,7,7,7]);p=fresh_plan(10)
    goodg,goode=check_graph(*bs,p)
    mutations=[]
    for key in ('version','order','rank','point','block_bits'):
        mutations.append((key,lambda g,e,key=key:g.__setitem__(key,g[key]+1)))
    mutations += [
        ('lengths',lambda g,e:g.__setitem__('lengths',(1,2))),
        ('nodes',lambda g,e:g.__setitem__('nodes',tuple(x+1 for x in g['nodes']))),
        ('run_side',lambda g,e:g.__setitem__('runs',(g['runs'][0],))),
        ('run_tail',lambda g,e:g['runs'][0].pop()),
        ('term_side',lambda g,e:g['sides'].pop()),
        ('term',lambda g,e:g['sides'][0].pop()),
        ('leaf',lambda g,e:g['leaves'].__setitem__(0,tuple(x+1 for x in g['leaves'][0]))),
        ('product',lambda g,e:g['products'].pop()),
        ('event',lambda g,e:g['events'].pop()),
        ('extra_event',lambda g,e:g['events'].append(g['events'][0])),
        ('target',lambda g,e:e['targets'].__setitem__(0,e['targets'][0]+1)),
        ('leaf_row',lambda g,e:e['leaf_rows'].__setitem__(0,tuple(x+1 for x in e['leaf_rows'][0]))),
        ('product_row',lambda g,e:e['product_rows'].__setitem__(0,tuple(x+1 for x in e['product_rows'][0])))]
    for column in (1,2,3,4):
        mutations.append(('source_'+str(column),lambda g,e,c=column:e['source_rows'].__setitem__(0,tuple(v+1 if i==c else v for i,v in enumerate(e['source_rows'][0])))))
    for name,change in mutations:
        g,e=copy.deepcopy(goodg),copy.deepcopy(goode);change(g,e)
        try:prod.check_certificate(bs,g,e,p,Arithmetic())
        except (ValueError,IndexError,TypeError,StopIteration):COUNTS['rejected_mutations']+=1
        else:raise AssertionError('accepted mutation '+name)
    changed=(bs[0][:],bs[1][:]);changed[0][2]+=1
    try:prod.check_certificate(changed,goodg,goode,p,Arithmetic())
    except ValueError:COUNTS['rejected_mutations']+=1
    else:raise AssertionError('accepted changed interior')
    bad=copy.deepcopy(goodg);bad['events'].pop()
    try:prod.integrate_events(bad,goode['targets'],Arithmetic())
    except ArithmeticError:COUNTS['recovery_tail_rejections']+=1
    else:raise AssertionError('missing terminal event escaped recovery tail check')

    output={'status':'PASS','candidate_source_sha256':EXPECTED,
            'execution_scope':'Only fresh candidate function/class bodies with independent new adapter; no historical module import or execution.',
            'manifest_entries_verified':len(manifest['files']),'native_formula_plans':29,
            'counts':COUNTS,'strict_families':families,'obstructions':obstructions,
            'guards':['budget before canonical conversion','endpoint rejection before graph allocation'],
            'fallback_scope':'Routing observed with a fresh oracle sentinel; historical fallback not executed.'}
    (HERE/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
