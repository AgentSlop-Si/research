#!/usr/bin/env python3
"""New independent final-review controls. No producer control program is imported.
Native integer arithmetic occurs only as a test oracle.
"""
import copy, hashlib, importlib.util, json, math, random, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
SRC=Path(__file__).resolve().parent.parent / 'candidate' / 'run_shared.py'
spec=importlib.util.spec_from_file_location('review_jump_candidate',SRC)
c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
rng=random.Random(818017226)
R={'plans':[],'canonical_boundaries':0,'complete_products':[],'source_node_identities':[],
   'coefficient_convolutions':0,'mutations':[],'budget_checks':[],'signed_leaf_targets':[],
   'canonical_division_bound':0}

def genbin(x,h):
    return math.prod(x-j for j in range(h))//math.factorial(h)

def plan_oracle(r):
    ell=math.lcm(*range(1,r+1));d=ell//r
    congr=[]
    for p in range(2,r+1):
        if any(p%q==0 for q in range(2,math.isqrt(p)+1)):continue
        qp=up=1
        while d%(qp*p)==0:qp*=p
        while ell%(up*p)==0:up*=p
        if qp>1:congr.append((qp,(-pow(ell//up,-1,qp))%qp))
    k=sum(a*(d//q)*pow(d//q,-1,q) for q,a in congr)%d if d>1 else 1
    P=1+k*ell;ww=tuple(math.comb(P+h-1,h) for h in range(r+1))
    s=(ww[-1]//d).bit_length()-1
    rows={x:tuple((-1)**h*genbin(x,h) for h in range(r)) for x in range(-(r-1),2*r-1)}
    norm=lambda x:sum(map(abs,rows[x]))
    off=min(range(r),key=lambda a:(max(norm(-a),norm(2*r-2-a)),a))
    nodes=tuple(range(-off,2*r-1-off))
    return P,s,ww[:-1],nodes,tuple(rows[x] for x in nodes),tuple(genbin(-P-nodes[0],h) for h in range(2*r-1))

plans={}
for r in range(2,35):
    p=c.base.native_plan(r,c.base.Elementary());o=plan_oracle(r)
    assert (p.point,p.block_bits,p.weights,p.nodes,p.rows,p.interpolation)==o
    plans[r]=p;R['plans'].append({'rank':r,'s':p.block_bits,'P_bits':p.point.bit_length()})
print('PASS independent plans',len(R['plans']),flush=True)

def digits(v,w):
    out=[]
    for z in w[::-1]:a,v=divmod(v,z);out.append(a)
    assert not v
    return tuple(out[::-1])

def blocks(v,s):
    v=abs(v);mask=(1<<s)-1;out=[]
    while v:out.append(v&mask);v>>=s
    return out or [0]

def integer(bs,s):return sum(v<<(s*i) for i,v in enumerate(bs))

def convolution(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

for r,p in plans.items():
    rho=1<<p.block_bits
    values={0,1,rho-1,rho//2}
    for w in p.weights:
        values.update(v for v in (w-1,w,w+1) if 0<=v<rho)
    values.update(rng.randrange(rho) for _ in range(5))
    for v in sorted(values):
        expected=digits(v,p.weights)
        assert c.base.canonical(v,p,c.base.Elementary())==expected
        assert all(0<=z<p.point for z in expected)
        rem=v
        for w in p.weights[::-1]:
            q,rem=divmod(rem,w)
            assert q<p.point
            # Long division loops at most bit_length(P)+1, including zero.
            assert max(0,max(1,(q*w+rem).bit_length())-max(1,w.bit_length()))+1 <= p.point.bit_length()+1
            R['canonical_division_bound']+=1
        R['canonical_boundaries']+=1
print('PASS canonical boundaries',R['canonical_boundaries'],flush=True)

def inspect_rows(a,b,answer,all_nodes=True):
    p=plans[answer.statistics['rank']];ab=blocks(a,p.block_bits);bb=blocks(b,p.block_bits)
    g,e=answer.graph,answer.execution
    xx=range(len(p.nodes)) if all_nodes else sorted({0,len(p.nodes)//2,len(p.nodes)-1})
    ds=[[digits(v,p.weights) for v in z] for z in (ab,bb)]
    leaf_target=[sum(v*w for v,w in zip(leaf,p.weights)) for leaf in g['leaves']]
    assert all(abs(v)<1<<p.block_bits for v in leaf_target)
    R['signed_leaf_targets'].append({'negative':sum(v<0 for v in leaf_target),'positive':sum(v>0 for v in leaf_target)})
    for xi in xx:
        row=p.rows[xi]
        ar,br=[[sum(u*v for u,v in zip(co,row)) for co in side] for side in ds]
        am,bm=max(map(abs,ar)),max(map(abs,br));bound=max(len(ar),len(br))*am*bm
        width=8*(((2*bound).bit_length()+7)//8) if bound else 0
        assert e['source_rows'][xi]==(p.nodes[xi],am,bm,width,bound)
        for original,terms in ((ar,g['sides'][0]),(br,g['sides'][1])):
            diff=[original[0]]+[y-x for x,y in zip(original,original[1:])]+[-original[-1]]
            expanded=[0]*len(diff)
            for pos,leaf,sg in terms:expanded[pos]+=sg*e['leaf_rows'][leaf][xi]
            assert diff==expanded
        event=[0]*(len(ar)+len(br)+1)
        for pos,pid,sg in g['events']:event[pos]+=sg*e['product_rows'][pid][xi]
        first=second=0;recovered=[]
        for val in event:first+=val;second+=first;recovered.append(second)
        assert first==second==0 and recovered[-2:]==[0,0]
        # Expand genuine original convolution only for bounded test sizes.
        if len(ar)*len(br)<10000:
            assert recovered[:-2]==convolution(ar,br)
            R['coefficient_convolutions']+=1
        if width:
            Q=1<<width
            pa=sum(v<<(width*i) for i,v in enumerate(ar));pb=sum(v<<(width*i) for i,v in enumerate(br))
            de=sum(v<<(width*i) for i,v in enumerate(event))
            assert de==(1-Q)**2*pa*pb and (1<<width)>2*bound
        else:assert not any(ar) or not any(br)
        R['source_node_identities'].append({'rank':p.rank,'x':p.nodes[xi],'width':width,'lengths':(len(ar),len(br))})
    if len(ab)*len(bb)<10000:
        co,peak=c.integrate_events(g,e['targets'],c.base.Elementary())
        assert co==convolution(ab,bb)
        R['coefficient_convolutions']+=1

def product(label,a,b,base_bits=64,budget=None,rows=False):
    t=time.perf_counter();res=c.multiply_runs(a,b,base_bits=base_bits,budget_factor=budget)
    assert res is not None and res.value==a*b,label
    record={'label':label,'elapsed':round(time.perf_counter()-t,6),**res.statistics}
    R['complete_products'].append(record)
    if rows and res.graph:inspect_rows(a,b,res,rows=='all')
    print('PASS product',label,record.get('root_bits'),record.get('jump_counts'),flush=True)
    return res

for a,b in [(0,0),(0,-1),(-33,0),(1,1),(-1,1),(1,-1),(-1,-1),(2**1024-1,-(2**1023+7)),(2**1025-1,1)]:
    product('signed_base_boundary',a,b,base_bits=1024)
for j in range(36):
    a=rng.getrandbits(rng.randint(65,2200)) or 1;b=rng.getrandbits(rng.randint(1,1700)) or 1
    product('random_%02d'%j,(-1 if j%2 else 1)*a,(-1 if j%3 else 1)*b,rows='all' if j in (0,9,20,35) else False)

saved=None
for r in (10,12,14,16,18,20,21):
    p=plans[r];s=p.block_bits;rho=1<<s;length=(1<<r)//s+2
    nr=1 if r==10 else max(2,3*math.isqrt(1<<r)//(r*r))
    va=[rng.randrange(1,rho) for _ in range(nr)];vb=[rng.randrange(1,rho) for _ in range(nr+1)]
    aa=[va[min(nr-1,i*nr//length)] for i in range(length)]
    bb=[vb[min(nr,i*(nr+1)//length)] for i in range(length-1)]
    # Force full top block so rank and unbounded occupied-support interpretation are unambiguous.
    aa[-1]=va[-1];bb[-1]=vb[-1]
    a,b=integer(aa,s),integer(bb,s)
    ans=product('growing_dense_%d'%r,-a,b,budget=64,rows='all' if r<=12 else 'sample')
    assert ans.statistics['rank']==r and ans.statistics['occupied'][0]>4
    if r==12:saved=(a,b,ans)

p=plans[12];s=p.block_bits;rho=1<<s;length=(1<<12)//s+2
families=[
 ('maximum_carry',[rho-1]*length,[rho-1]*(length-1)),
 ('shift_zero_gaps',[0]*3+[rho-1]*4+[0]*4+[p.point-1]*(length-11),[p.point+1]*5+[0]*5+[rho//2]*(length-10)),
 ('opposite_normalization',[p.point-1,p.point+1]*(length//2),[p.point+1,p.point-1]*(length//2)),
 ('partial_top',[rho-1]*(length-1)+[1],[p.point]*length),
 ('one_block_unbalanced',[rho-1]*length,[p.point-1]),
 ('run_repeated_values',[1]*3+[p.point]*4+[1]*5+[p.point]*(length-12),[p.point]*4+[1]*7+[p.point]*(length-11))]
for name,ab,bb in families:product(name,integer(ab,s),-integer(bb,s),rows='all')
# Exact nonlinear regression, including direction of normalization vs decoded integer sign.
for r in (6,10,12,18):
    p=plans[r];x,y=p.point-1,p.point+1
    d=tuple(v-u for u,v in zip(digits(x,p.weights),digits(y,p.weights)))
    assert d!=digits(y-x,p.weights) and sum(v*w for v,w in zip(d,p.weights))==2
    sg,norm=c.signed_normalize(d)
    assert sg==-1 and sum(v*w for v,w in zip(norm,p.weights))==-2

# Production threshold, verified on both sides, and reject-before-graph evidence.
p=plans[12];s=p.block_bits;rho=1<<s;length=18
A=integer([rho-3]*9+[rho-7]*9,s)
B=integer([rho-11]*6+[rho-13]*6+[rho-17]*6,s)
assert c.multiply_runs(A,B,budget_factor=64) is not None
orig=c.make_graph
called=[]
def forbidden(*args,**kw):called.append(True);raise AssertionError('graph built after failed budget')
c.make_graph=forbidden
try:
    D=integer([rho-19]*6+[rho-23]*6+[rho-29]*6,s)
    assert c.multiply_runs(B,D,budget_factor=64) is None
    assert not called
finally:c.make_graph=orig
R['budget_checks'].extend([{'case':'default_budget_accept_12_events','passed':True},{'case':'default_budget_reject_16_events_before_graph','passed':True}])
fa,fb=(1<<3072)+(1<<1500)+1,-((1<<3021)+7)
assert c.multiply(fa,fb,budget_factor=0)==fa*fb
R['budget_checks'].append({'case':'pinned_complete_fallback','passed':True})

# Input-bound certificate corruptions; use a multi-product graph.
a,b,answer=saved;p=plans[answer.statistics['rank']];ab=blocks(a,p.block_bits);bb=blocks(b,p.block_bits)
def mutate(label,gm=None,em=None,am=None):
    g,e=copy.deepcopy(answer.graph),copy.deepcopy(answer.execution);aa=ab[:]
    if gm:gm(g)
    if em:em(e)
    if am:am(aa)
    try:c.check_certificate(aa,bb,p,g,e,c.base.Elementary())
    except (ValueError,ArithmeticError,AssertionError,IndexError,TypeError):pass
    else:raise AssertionError('corruption accepted: '+label)
    R['mutations'].append({'case':label,'rejected':True})
mutate('input_dense_binding',am=lambda x:x.__setitem__(2,x[2]^1))
mutate('point_header',gm=lambda g:g.__setitem__('point',g['point']+1))
mutate('length_header',gm=lambda g:g.__setitem__('lengths',(g['lengths'][0]+1,g['lengths'][1])))
mutate('leaf_coefficient',gm=lambda g:g['leaves'].__setitem__(0,(g['leaves'][0][0]+1,*g['leaves'][0][1:])))
mutate('unused_leaf',gm=lambda g:g['leaves'].append((p.point-1,)*p.rank))
mutate('terminal_jump',gm=lambda g:g['sides'][0].pop())
mutate('initial_jump',gm=lambda g:g['sides'][0].pop(0))
mutate('term_sign',gm=lambda g:g['sides'][0].__setitem__(0,(*g['sides'][0][0][:2],-g['sides'][0][0][2])))
mutate('run_value',gm=lambda g:g['changes'][0].__setitem__(0,(g['changes'][0][0][0],g['changes'][0][0][1]^1)))
mutate('event_missing',gm=lambda g:g['events'].pop())
mutate('event_duplicate',gm=lambda g:g['events'].append(g['events'][0]))
mutate('event_sign',gm=lambda g:g['events'].__setitem__(0,(*g['events'][0][:2],-g['events'][0][2])))
mutate('event_offset',gm=lambda g:g['events'].__setitem__(0,(g['events'][0][0]+1,*g['events'][0][1:])))
mutate('product_missing',gm=lambda g:g['products'].pop())
mutate('product_duplicate',gm=lambda g:g['products'].append(g['products'][0]))
mutate('target_value',em=lambda e:e['targets'].__setitem__(0,e['targets'][0]+1))
mutate('target_missing',em=lambda e:e['targets'].pop())
mutate('leaf_row',em=lambda e:e['leaf_rows'].__setitem__(0,(e['leaf_rows'][0][0]+1,*e['leaf_rows'][0][1:])))
mutate('product_row',em=lambda e:e['product_rows'].__setitem__(0,(e['product_rows'][0][0]+1,*e['product_rows'][0][1:])))
mutate('source_width',em=lambda e:e['source_rows'].__setitem__(0,(*e['source_rows'][0][:3],e['source_rows'][0][3]+8,e['source_rows'][0][4])))
mutate('source_max',em=lambda e:e['source_rows'].__setitem__(0,(e['source_rows'][0][0],e['source_rows'][0][1]+1,*e['source_rows'][0][2:])))
mutate('source_bound',em=lambda e:e['source_rows'].__setitem__(0,(*e['source_rows'][0][:4],e['source_rows'][0][4]+1)))
print('PASS mutations',len(R['mutations']),flush=True)
R['summary']={'pass':True,'plans':len(R['plans']),'canonical_boundaries':R['canonical_boundaries'],
'complete_products':len(R['complete_products']),'source_node_identities':len(R['source_node_identities']),
'coefficient_convolutions':R['coefficient_convolutions'],'mutation_rejections':len(R['mutations']),
'budget_checks':len(R['budget_checks']),'canonical_division_checks':R['canonical_division_bound']}
R['source_hashes']={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in (SRC,SRC.with_name('REPORT.md'),c.BASE)}
(HERE/'RESULTS.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps(R['summary'],indent=2),flush=True)
