"""Independent 832-bit half-angle-root review. Author controls are not imported.
Inspected candidate production modules are imported only after manifest verification.
"""
from pathlib import Path
from math import isqrt
from collections import Counter
import hashlib,json,sys,time,copy,random
ROOT=Path(__file__).resolve().parent / '../candidate'
OUT=Path(__file__).resolve().parent
start=time.monotonic();checks=Counter()
def check(name,ok):
    if not ok:raise AssertionError(name)
    checks[name]+=1
manifest=json.loads((ROOT/'SAFE_MANIFEST.json').read_text())
for row in manifest['files']:
    data=(ROOT/row['path']).read_bytes()
    check('frozen manifest bytes/hash',len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'])
sys.path.insert(0,str(ROOT))
from sparse_adapter import SparseAdapter,Failure,canonical,strict_loads
from nonconstant_buckets import M,B,T,H,G,K,P,LIMIT,ELL,R
adapter=SparseAdapter();raw,state=adapter.producer.fixture()
fixture=adapter.execute(raw,state)
fpacket=fixture.packet();expected=json.loads((ROOT/'NONCONSTANT_FIXTURE_PACKET.json').read_text())
check('fresh full fixture matches frozen packet',canonical(fpacket)==canonical(expected))
check('live fixture original nonquarter input',fpacket['source']['entries']==[[1,1,0],[3,1,0]])
check('fixture genuine complex output',any(y for x,y in fixture.numerators))
check('fixture normalization exact half',fpacket['source']['normalized_norm_squared']=={'numerator':2,'denominator_power_two':2})
check('full fixture source pin',fpacket['producer_source_sha256']=='5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed')
print('Fresh theorem-size fixture reproduced, including all 131072 values.',flush=True)
# Widest admitted coefficients and full support, at unrelated arbitrary indices.
rng=random.Random(202610172144)
indices=sorted(rng.sample(range(M),16));rows=[]
for i,n in enumerate(indices):rows.append([n,(-1 if i%2 else 1)*((1<<1024)-1-i),(-1 if i%3 else 1)*((1<<1023)+i)])
large_raw={**raw,'entries':rows};large=adapter.execute(large_raw,state,sigma=M-3,tau=M-17)
large_packet=large.packet()
check('full sixteen-mode family at cap executes',len(large.numerators)==B and len(large_packet['source']['entries'])==16)
check('large coefficient normalization strict norm',large_packet['source']['normalized_norm_squared']['numerator']*4>1<<large_packet['source']['normalized_norm_squared']['denominator_power_two'])
# Include exact d=2T exclusion, d=0, and circular wraparound in a single run.
edge_raw={**raw,'entries':[[0,1,2],[T,-3,1],[2*T,1,-1],[M-1,-1,3]]}
edge=adapter.execute(edge_raw,state,sigma=1,tau=M-1);edge_packet=edge.packet()
coarse=adapter.execute(raw,state,query_bits=8)
check('exact descriptor independent of query radius',coarse.numerators==fixture.numerators)
coarse_src=adapter.producer.execute(raw,state,query_bits=8)
try:coarse_src.query(1,require_accepted_radius=True)
except ValueError as err:check('coarse finite query refuses accepted radius','PRECISION' in str(err))
else:raise AssertionError('coarse finite query accepted')
# Independent interval arithmetic, with no Machin pi, Taylor series, prefix sums,
# rounded binary powering, or production numerical primitive.
Q=832;S=1<<Q;ZERO=(0,0);ONE=(S,S)
def up(n,d):return -((-n)//d)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[1],-a[0])
def sub(a,b):return add(a,neg(b))
def scale(a,c):return tuple(sorted((a[0]*c,a[1]*c)))
def divide(a,d):return(a[0]//d,up(a[1],d))
def mul(a,b):
    p=[x*y for x in a for y in b];return(min(p)//S,up(max(p),S))
def quot(a,b):
    assert b[0]>0
    return(min(x*S//y for x in a for y in b),max(up(x*S,y) for x in a for y in b))
def square_root(a):
    assert 0<=a[0]<=a[1]
    lo=isqrt(a[0]*S);hi=isqrt(a[1]*S)
    if hi*hi<a[1]*S:hi+=1
    return(lo,hi)
def cmul(a,b):return(sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0])))
roots={1:(neg(ONE),ZERO),2:(ZERO,ONE)}
c=ZERO
for degree in range(3,30):
    cc=square_root(divide(add(ONE,c),2))
    ss=square_root(divide(sub(ONE,c),2))
    roots[degree]=(cc,ss);c=cc
root_cache={}
def root(k,m):
    k%=1<<m;key=(k,m)
    if key not in root_cache:
        value=(ONE,ZERO)
        for bit in range(m):
            if k>>bit&1:value=cmul(value,roots[m-bit])
        root_cache[key]=value
    return root_cache[key]
def absi(a):
    return(0 if a[0]<=0<=a[1] else min(abs(a[0]),abs(a[1])),max(abs(a[0]),abs(a[1])))
# Independent direct endpoint exponentiation, retaining exact wide intermediates.
phi=[];denpower=S**113
for d in range(LIMIT+1):
    if d==0:v=ONE
    elif d%256==0:v=ZERO
    else:
        num=absi(root(d,9)[1]);den=scale(root(d,29)[1],ELL)
        ratio=quot(num,den);ratio=(max(0,ratio[0]),min(S,ratio[1]))
        v=(ratio[0]**114//denpower,up(ratio[1]**114,denpower))
    phi.append(v)
C=(S+2*sum(v[0] for v in phi[1:G+1]),S+2*sum(v[1] for v in phi[1:G+1]))
scale_to_prod=1<<(Q-K)
check('independent root normalizer nested',adapter.engine.C.lo*scale_to_prod<=C[0]<=C[1]<=adapter.engine.C.hi*scale_to_prod)
windows={}
def window(d):
    if d not in windows:
        vals=[phi[abs(d-a)] for a in range(-H,H+1)]
        windows[d]=quot((sum(v[0] for v in vals),sum(v[1] for v in vals)),C)
    return windows[d]
max_component_width=0;max_radius_fraction=[0,1];run_summaries=[]
for label,run,packet in [('fixture',fixture,fpacket),('sixteen_max_width',large,large_packet),('circular_edges',edge,edge_packet)]:
    hdr=packet['downstream'];entries=packet['source']['entries'];h=packet['source']['h'];sg=hdr['sigma'];tau=hdr['tau']
    active=set(hdr['active_bins']);certs=hdr['certificates']
    check('all output coordinates explicit',len(run.numerators)==B)
    for j,(re,im) in enumerate(run.numerators):
        check('every output exact integer pair',type(re)is int and type(im)is int)
        if j not in active:check('every far-only output zero',(re,im)==(0,0))
    l1=sum(abs(re)+abs(im) for n,re,im in entries);energy=sum(re*re+im*im for n,re,im in entries)
    check('complex l1 bound squared',l1*l1<=2*len(entries)*energy and l1<6*(1<<h))
    tail=up(3073*l1*(1<<K),20**114*(1<<h))
    check('tail paid on exact complex component l1',tail==hdr['tail_grid_units'])
    all_retained=set()
    for n,re,im in entries:
        expected_bins={j for j in range(B) if min((j*T+sg*n)%M,(-j*T-sg*n)%M)<2*T}
        base=(-(sg*n%M))//T
        candidates={(base+o)%B for o in range(-2,3) if min((((base+o)%B)*T+sg*n)%M,(-((base+o)%B)*T-sg*n)%M)<2*T}
        check('retention exhaustive arbitrary modes',expected_bins==candidates and len(expected_bins)<=4)
        all_retained.update(expected_bins)
    check('union exact circular active set',all_retained==active)
    for row in certs:
        j,qr,qi,lr,hr,li,hi,er,ei=row
        real=imag=ZERO
        for n,re,im in entries:
            q=(j*T+sg*n)%M;d=min(q,M-q)
            if d>=2*T:continue
            z=root(-n*tau,28)
            cr=divide(sub(scale(z[0],re),scale(z[1],im)),1<<h)
            ci=divide(add(scale(z[1],re),scale(z[0],im)),1<<h)
            w=window(d);real=add(real,mul(w,cr));imag=add(imag,mul(w,ci))
        check('independent root complex enclosure nested',lr*scale_to_prod<=real[0]<=real[1]<=hr*scale_to_prod and li*scale_to_prod<=imag[0]<=imag[1]<=hi*scale_to_prod)
        U=1<<(K-P);OU=1<<(Q-P)
        check('actual exact retained radius inequality',er*er+ei*ei<=(U-tail)**2)
        dr=max(abs(qr*OU-real[0]),abs(qr*OU-real[1]));di=max(abs(qi*OU-imag[0]),abs(qi*OU-imag[1]))
        check('independent root Euclidean radius plus tail',dr*dr+di*di<=(OU-tail*scale_to_prod)**2)
        max_component_width=max(max_component_width,hr-lr,hi-li)
        frac=(dr*dr+di*di,OU*OU)
        if frac[0]*max_radius_fraction[1]>max_radius_fraction[0]*frac[1]:max_radius_fraction=list(frac)
    run_summaries.append({'label':label,'support':len(entries),'active_bins':len(active),'output_count':len(run.numerators),'h':h,'sigma':sg,'tau':tau,'max_coefficient_bits':max(max(abs(r).bit_length(),abs(i).bit_length()) for n,r,i in entries)})
print('Independent 832-bit algebraic-root oracle passed all three full-output runs.',flush=True)
# Independently check actual sine widths at all phases already evaluated by oracle.
for n in [0,1,M//4-1,M//4,M//2-1,M-1]+indices:
    for tau in [0,17,M-1]:
        actual=adapter.engine.sine.phase(n,tau);expected_root=root(-n*tau,28)
        for a,b in zip(actual,expected_root):
            check('phase sign and circular reduction at fresh roots',a.lo*scale_to_prod<=b[0]<=b[1]<=a.hi*scale_to_prod)
            check('uniform sine width claim observed',a.hi-a.lo<1<<14)
# Finite exact inequalities used by the universal (not empirical) proof.
check('strict omitted tail certificate',3073*(1<<480)<20**114)
check('window delta distinct',3073*M**4<=16**57)
check('uniform rounding reserve',2*((1<<95)+(1<<86))**2<(3*(1<<94))**2)
check('uniform tail reserve',up(6*(1<<560),1<<480)<1<<94)
check('uniform recorded arithmetic bound',(5631+129)*2048+20000+16*8192<1<<24<30000000)
check('uniform observed retained interval widths',max_component_width<1<<87)
# Recompute exact canonical replay and targeted semantic failures.
check('separate original context replay',adapter.verify(raw,state,16,464,fpacket)['bound_to_separately_supplied_original_input'])
def rejected(label,call,reason):
    try:call()
    except (ValueError,ArithmeticError) as e:check(label,reason in str(e))
    else:raise AssertionError('unexpected acceptance '+label)
bad=copy.deepcopy(fpacket);bad['bucket_numerators'][123456][1]=1
rejected('full distant-coordinate forgery rejected',lambda:adapter.verify(raw,state,16,464,bad),'SEMANTIC_MISMATCH')
changed=copy.deepcopy(raw);changed['entries'][0][0]=2
rejected('separately supplied arbitrary original binding',lambda:adapter.verify(changed,state,16,464,fpacket),'SEMANTIC_MISMATCH')
rejected('separately supplied tau binding',lambda:adapter.verify(raw,state,16,464,fpacket,tau=18),'SEMANTIC_MISMATCH')
rejected('separately supplied state binding',lambda:adapter.verify(raw,{**state,'a':3},16,464,fpacket),'SEMANTIC_MISMATCH')
for text in ['{"a":1,"a":2}','{"a":true,"b":1.2}','NaN']:
    rejected('canonical JSON rejection',lambda t=text:strict_loads(t),'GRAMMAR')
receipt=adapter.receipt(additional_packet_exports=3,additional_json_parses=1)
check('every successful call paid full outputs',receipt['numerical']['operations']['bucket_output']==receipt['successful_calls']*B)
check('all numerical resources under cumulative caps',receipt['numerical']['numeric_operations']<30000000 and receipt['numerical']['allocated_slots']<8000000 and receipt['numerical']['max_integer_bits']<20000)
check('no FFT claimed or paid as executed',receipt['actual_FFT_roots']==receipt['actual_FFT_butterflies']==0)
check('preparation actual scalar count',receipt['numerical']['operations']['phi_evaluation']==5631 and receipt['numerical']['operations']['numerator_root_preparation']==129)
# Direct signed-time identity at reduced scale; this is a diagnostic only.
import mpmath as mp
mp.mp.dps=180
mm=256;bb=8;tt=32;ell=8;rr=2;gg=8;hh=24
coef=[1]
for _ in range(2*rr):
    nxt=[0]*(len(coef)+ell-1)
    for j,c in enumerate(coef):
        for k in range(ell):nxt[j+k]+=c
    coef=nxt
rad=rr*(ell-1);den=ell**(2*rr)
ph=lambda q:sum(mp.mpf(c)*mp.exp(-2j*mp.pi*q*(t-rad)/mm)/den for t,c in enumerate(coef))
cc=sum(ph(a) for a in range(-gg,gg+1));modes=[(1,1,2),(3,-2,1),(127,1,-3),(255,-1,-1)]
for sig,tau in [(5,37),(253,255)]:
    for j in range(bb):
        value=0
        for off,c in enumerate(coef):
            t=off-rad
            D=sum(mp.exp(2j*mp.pi*a*t/mm) for a in range(-hh,hh+1))
            v=sum(mp.mpc(re,im)*mp.exp(-2j*mp.pi*n*(sig*t+tau)/mm) for n,re,im in modes)
            value+=mp.mpf(c)*D*v*mp.exp(-2j*mp.pi*j*t/bb)/(den*cc)
        freq=sum(mp.mpc(re,im)*mp.exp(-2j*mp.pi*n*tau/mm)*sum(ph(j*tt+sig*n-a) for a in range(-hh,hh+1))/cc for n,re,im in modes)
        check('independent signed-time reduced diagnostic',abs(value-freq)<mp.mpf('1e-165'))
# Re-verify frozen sources were not modified by review execution.
for row in manifest['files']:
    data=(ROOT/row['path']).read_bytes();check('manifest unchanged after independent review',hashlib.sha256(data).hexdigest()==row['sha256'])
report={'status':'PASS_INDEPENDENT_NONCONSTANT_BUCKETS_CONTROLS','assertions':sum(checks.values()),'checks':dict(checks),'elapsed_seconds':time.monotonic()-start,'oracle':{'bits':Q,'method':'independent integer-square-root half angles, complex root products, direct endpoint power and direct window sums; no production or author numerical primitives'},'runs':run_summaries,'maximum_retained_component_width_grid_units':max_component_width,'maximum_oracle_squared_radius_fraction':max_radius_fraction,'receipt':receipt,'source_manifest':manifest,'external_writes':False}
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:report[k] for k in ['status','assertions','elapsed_seconds']},indent=2),flush=True)
