"""Independent review oracle, written after inspection of the frozen candidate.
No imports of author tests or numerical helpers. Local-only writes.
"""
import sys, json, time, math, copy, hashlib
from pathlib import Path
from fractions import Fraction
HERE=Path(__file__).resolve().parent
SRC=Path(__file__).resolve().parent.parent/'candidate'
EXPECT={'constant_buckets.py':'951da991cf6cc795e2faf4cf14a7aae75639e0be79e4ce09af7363c0dd5b6359','scale_adapter.py':'24506f440d70f6008ff59c333a89b237457251ebd58313cfa49e79ba679667c7','checks.py':'2b5e4b864d5c18587c8fd0e491da7542bed2ce8a2b9d9d0c95ffb8f1035f6b54'}
checks={}; errors=[]; start=time.monotonic()
def check(name,ok):
    if not ok: raise AssertionError(name)
    checks[name]=checks.get(name,0)+1

def rejected(name,fn):
    try: fn()
    except (ValueError,ArithmeticError,TypeError) as e:
        checks[name]=checks.get(name,0)+1; return str(e)
    raise AssertionError('Not rejected: '+name)

for f,h in EXPECT.items(): check('frozen source '+f,hashlib.sha256((SRC/f).read_bytes()).hexdigest()==h)
# Independently certified higher-resolution interval library. All recurrence
# angles remain intervals, unlike the candidate's midpoint-plus-Lipschitz path.
K=704; S=1<<K
ceil=lambda a,b:-((-a)//b)
def arctan_recip(q):
    n=220; lo=hi=0
    for j in range(n):
        d=(2*j+1)*q**(2*j+1); a=S//d; b=ceil(S,d)
        if j%2: lo-=b;hi-=a
        else:lo+=a;hi+=b
    tail=ceil(S,(2*n+1)*q**(2*n+1))
    # n even means next term is positive; this interval is exact.
    return lo,hi+tail
p5=arctan_recip(5);p239=arctan_recip(239)
PI=(16*p5[0]-4*p239[1],16*p5[1]-4*p239[0])
check('independent pi interval domain',3*S<PI[0]<PI[1]<4*S)
TERMS=160;TAIL=ceil(S*2**(2*TERMS+1),math.factorial(2*TERMS+1))
check('independent finite Taylor tail',TAIL==1)
def sine(p,q):
    p=p%(2*q);sign=1
    if p>q:p=2*q-p;sign=-1
    if 2*p>q:p=q-p
    if p==0:return(0,0)
    if 2*p==q:return(sign*S,sign*S)
    xlo=PI[0]*p//q;xhi=ceil(PI[1]*p,q)
    lo=tl=xlo;hi=th=xhi
    for j in range(1,TERMS):
        d=S*S*(2*j)*(2*j+1)
        tl=tl*xlo*xlo//d;th=ceil(th*xhi*xhi,d)
        if j%2:lo-=th;hi-=tl
        else:lo+=tl;hi+=th
    lo=max(-S,lo-TAIL);hi=min(S,hi+TAIL)
    return (lo,hi) if sign==1 else(-hi,-lo)
def divpos(a,b):
    assert b[0]>0
    return(a[0]*S//b[1],ceil(a[1]*S,b[0]))
def phi(a):
    if a==0:return(S,S)
    n=sine(a,256)
    if n==(0,0):return n
    if n[1]<0:n=(-n[1],-n[0])
    n=(max(0,n[0]),max(0,n[1]))
    d=sine(a,1<<28);d=(d[0]*(1<<20),d[1]*(1<<20))
    r=divpos(n,d);r=(max(0,r[0]),min(S,r[1]))
    den=S**113
    return(r[0]**114//den,ceil(r[1]**114,den))
C=[S,S];N0=[S,S];N1=[0,0]
for a in range(1,3585):
    v=phi(a)
    if a<=512:C[0]+=2*v[0];C[1]+=2*v[1]
    if a<=1536:N0[0]+=2*v[0];N0[1]+=2*v[1]
    if a>=512:N1[0]+=v[0];N1[1]+=v[1]
ORACLE=[divpos(N0,C),divpos(N1,C)]
print('Independent 704-bit interval oracle finished',time.monotonic()-start,flush=True)
# Actual live, frozen producer -> adapter execution.
sys.path.insert(0,str(SRC))
from scale_adapter import ScaleAdapter,canonical,strict_loads
adapter=ScaleAdapter();raw,state=adapter.producer.fixture()
run=adapter.execute(raw,state);packet=run.packet();engine=adapter.engine
print('Fresh actual engine finished',time.monotonic()-start,flush=True)
check('actual complete immutable output',len(run.numerators)==131072 and type(run.numerators)is tuple and run.bits==464)
for idx,oracle in zip((0,1,131071),(ORACLE[0],ORACLE[1],ORACLE[1])):
    val=run.numerators[idx];unit=1<<(K-464)
    check('higher-grid independent error certificate',max(abs(val[0]*unit-oracle[0]),abs(val[0]*unit-oracle[1]))<=unit and val[1]==0)
    cert=next(c for c in engine.certificates if c.bin_index==idx)
    check('independent oracle strictly within candidate enclosure',cert.enclosure_low*(1<<(K-560))<=oracle[0]<=oracle[1]<=cert.enclosure_high*(1<<(K-560)))
check('normalizer independent enclosure',engine.normalizer.lo*(1<<(K-560))<=C[0]<=C[1]<=engine.normalizer.hi*(1<<(K-560)))
# Exhaustively inspect every actual output and all B circular distance classes.
for j,v in enumerate(run.numerators):
    check('all output exact type',type(v)is tuple and len(v)==2 and all(type(x)is int for x in v))
    if j not in (0,1,131071):
        check('far output zero',v==(0,0))
        check('exhaustive circular distance guard',min(j,131072-j)*2048-1536>=2560)
check('exact far-bin rho comparison',3073*(1<<464)<20**114)
check('separate exact window delta comparison',3073*(1<<112)<=16**57)
check('independent theorem dimensions',(1<<17)==4096*32 and Fraction(5,56)*28==Fraction(5,2) and 2*57*((1<<20)-1)+1<(1<<28))
check('exact norm',Fraction(1<<28,1<<28)==1 and packet['source']['value_exponent']==-14)
check('live producer binding',packet['producer']['context']['raw']==raw and packet['producer']['context']['state']==state)
check('fresh semantic replay',adapter.verify(raw,state,16,464,packet)['bound_to_separately_supplied_original_context'])
# Same numeric result is not sufficient: retained original scale, phase, t,q,p,
# schedule, status, all output entries, and flags must bind exactly.
mutations=[('source sign',lambda p:p['source']['period'][0].__setitem__(0,-1)),('full recovery claim',lambda p:p['downstream'].__setitem__('full_recovery_executed',True)),('forged target',lambda p:p['downstream'].__setitem__('target','Ux')),('changed final bin',lambda p:p['bucket_numerators'][-1].__setitem__(1,1)),('removed middle bin',lambda p:p['bucket_numerators'].pop(65536)),('changed original phase',lambda p:p['producer']['context']['state'].__setitem__('a',3)),('formal radius',lambda p:p['source']['formal_policy_radius_over_alpha'].__setitem__('scale',-465)),('changed producer hash',lambda p:p['producer']['policy'].__setitem__('raw_input_sha256','0'*64))]
for name,mut in mutations:
    bad=copy.deepcopy(packet);mut(bad)
    rejected('packet rejection '+name,lambda:adapter.verify(raw,state,16,464,bad))
for name,arg in [('scaled original',{'raw':{**raw,'F':1}}),('different legal phase',{'state':{**state,'beta':1}}),('different t',{'t':17}),('different q',{'q':465}),('different p',{'p':268436014}),('different legal sigma',{'sigma':3}),('different legal tau',{'tau':1})]:
    args={'raw':raw,'state':state,'t':16,'q':464,'packet':packet};args.update(arg)
    rejected('separate original replay rejection '+name,lambda:adapter.verify(**args))
for entries in ([[0,-1,0]],[[0,0,1]],[[1<<26,1,0]],[[0,1,0],[1<<26,1,0]],[]):
    bad={**raw,'entries':entries}
    rejected('unsupported input rejection',lambda:adapter.execute(bad,state))
for F in (-(1<<126),(1<<126)-1,-131,131):
    rr={**raw,'F':F};ss={**state,'a':(1<<28)-1,'beta':(1<<28)-1}
    other=adapter.execute(rr,ss,sigma=(1<<28)-1,tau=(1<<28)-1)
    check('large signed exact scale invariant',other.numerators is run.numerators and json.loads(other.header_bytes)['source']['alpha_exponent']==-F)
for x in ('{"x": true, "x": false}','{"x":1e0}','{"x":Infinity}', '[[[[[[[[[[[[[[[[[[0]]]]]]]]]]]]]]]]]]'):
    rejected('strict intake control',lambda:strict_loads(x))
class Trap:
    def __eq__(self,other):raise AssertionError('equality hook ran')
    def __iter__(self):raise AssertionError('iterator hook ran')
for obj in (Trap(),[Trap()],{'x':Trap()}):rejected('untrusted canonical type',lambda:canonical(obj))
# A distinct original signed-window oracle: tiny exact box convolution,
# explicit signed taps, and complex exponentials; no ratio-based window code.
import mpmath as mp
mp.mp.dps=100
M=256;B=4;r=1;ell=32;g=16;H=48;T=64
coeff=[1]
for _ in range(2*r):
    nxt=[0]*(len(coeff)+ell-1)
    for i,x in enumerate(coeff):
        for j in range(ell):nxt[i+j]+=x
    coeff=nxt
rad=r*(ell-1);den=ell**(2*r)
Phi=lambda a:sum(mp.mpf(c)/den*mp.exp(-2j*mp.pi*a*(i-rad)/M) for i,c in enumerate(coeff))
CN=sum(Phi(a) for a in range(-g,g+1))
for j in range(B):
    # Two factors 1/sqrt(M) give exactly 1/M in constant-source BUCKETS.
    original=sum(mp.mpf(c)/den*sum(mp.exp(2j*mp.pi*a*(i-rad)/M) for a in range(-H,H+1))*mp.exp(-2j*mp.pi*j*(i-rad)/B)/CN for i,c in enumerate(coeff))
    dual=sum(Phi(j*T-a) for a in range(-H,H+1))/CN
    check('independent signed-window identity diagnostic',abs(original-dual)<mp.mpf('1e-90'))
# Final integrity verifies no author file changed during execution.
for f,h in EXPECT.items():check('postexecution frozen source '+f,hashlib.sha256((SRC/f).read_bytes()).hexdigest()==h)
receipt=adapter.receipt(additional_packet_exports=1,additional_json_parses=4)
check('paid resource controls',receipt['total_bit_work_upper']>receipt['producer_bit_work_upper']+receipt['numerical']['total_bit_work_upper'] and receipt['cumulative_storage_upper_bits']>0)
check('actual preparation not phantom',receipt['numerical']['operations']['phi_evaluation']==3584 and receipt['numerical']['operations']['bucket_output']==131072 and receipt['actual_FFT_roots']==0 and receipt['actual_FFT_butterflies']==0)
check('recorded numerical caps',receipt['numerical']['numeric_operations']<=30000000 and receipt['numerical']['max_observed_integer_bits']<=70000 and receipt['numerical']['allocated_slots']<=4000000)
result={'status':'ACCEPT_RESTRICTED_THEOREM_SCALE_INTEGRATION','assertions':sum(checks.values()),'checks':checks,'elapsed_seconds':time.monotonic()-start,'source_hashes':EXPECT,'oracle_grid_bits':K,'oracle_angle_method':'full positive interval recurrence, no candidate numerical primitive','oracle_pi_interval':[str(x) for x in PI],'oracle_bucket_intervals':[[str(x) for x in b] for b in ORACLE],'receipt':receipt,'scope':'x=2^-F delta_0 at N=2^28 -> original ideal BUCKETS; no full recovery/outer transfer/general input/serial rounded equivalence'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ('status','assertions','elapsed_seconds')}),flush=True)
