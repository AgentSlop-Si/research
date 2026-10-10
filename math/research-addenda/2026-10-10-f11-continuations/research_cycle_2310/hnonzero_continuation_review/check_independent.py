#!/usr/bin/env python3
"""Independent regular-H-nonzero continuation verifier.
Only inert JSON and byte hashes are read. No author or inherited code is
inspected, imported, or run. Sparse polynomials are constructed afresh.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json, hashlib, time, copy, sys
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
TARGET=ROOT/'research_cycle_2304/regular_hnonzero_analysis'
V=(0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92)
IDX={v:i for i,v in enumerate(V)}
ZERO=(0,)*len(V)
CZ=(F(0),)*10
CO=(F(1),)+(F(0),)*9
checks=[]
source_hashes={}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def bind(p,h):
    assert sha(ROOT/p)==h,('hash mismatch',p)
    source_hashes[p]=h

def require(x,label):
    assert x,label
    checks.append(label)

@lru_cache(None)
def cmul(a,b):
    # First route: cyclic convolution using zeta^11=1, then remove zeta^10.
    t=[F(0)]*11
    for i,x in enumerate(a):
      if x:
       for j,y in enumerate(b):
        if y:t[(i+j)%11]+=x*y
    out=tuple(t[i]-t[10] for i in range(10))
    # Independent second route: long reduction by monic Phi11.
    u=[F(0)]*19
    for i,x in enumerate(a):
      if x:
       for j,y in enumerate(b):
        if y:u[i+j]+=x*y
    for k in range(18,9,-1):
      z=u[k]
      if z:
       for j in range(11):u[k-10+j]-=z
    assert tuple(u[:10])==out,'coefficient arithmetic disagreement'
    return out

def cadd(a,b):return tuple(x+y for x,y in zip(a,b))
def clean(p):return {m:c for m,c in p.items() if any(c)}
def const(c):
    if isinstance(c,int):c=(F(c),)+(F(0),)*9
    return {} if not any(c) else {ZERO:c}
ONE=const(1)

def var(v):
    m=list(ZERO);m[IDX[v]]=1;return {tuple(m):CO}
X={v:var(v) for v in V}
def add(a,b):
    z=dict(a)
    for m,c in b.items():z[m]=cadd(z.get(m,CZ),c)
    return clean(z)
def neg(a):return {m:tuple(-t for t in c) for m,c in a.items()}
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    z={}
    for m,c in a.items():
      for n,d in b.items():
        t=tuple(x+y for x,y in zip(m,n));z[t]=cadd(z.get(t,CZ),cmul(c,d))
    return clean(z)
def power(a,k):
    r=ONE
    while k:
      if k&1:r=mul(r,a)
      k//=2
      if k:a=mul(a,a)
    return r

def decode(rows,variables):
    result={};seen=set()
    for mon,vec,den in rows:
      assert len(mon)==len(variables) and len(vec)==10
      assert isinstance(den,int) and den>0
      assert all(isinstance(x,int) and x>=0 for x in mon)
      assert all(isinstance(x,int) for x in vec)
      m=[0]*len(V)
      for v,k in zip(variables,mon):m[IDX[v]]=k
      m=tuple(m);assert m not in seen;seen.add(m)
      c=tuple(F(x,den) for x in vec);assert any(c)
      result[m]=c
    return result

def support(p):return {v for v in V if any(m[IDX[v]] for m in p)}
def degree(p,v):return max([0]+[m[IDX[v]] for m in p])

def evaluate(p,coordinates):
    """Return a raw denominator-cleared pair, with no gcd or division."""
    used={v:degree(p,v) for v in V if degree(p,v)}
    cache={}
    den=ONE
    for v,k in used.items():
      n,d=coordinates.get(v,(X[v],ONE))
      np=[ONE];dp=[ONE]
      for i in range(k):np.append(mul(np[-1],n));dp.append(mul(dp[-1],d))
      cache[v]=(np,dp)
      den=mul(den,dp[k])
    num={}
    for m,c in p.items():
      term=const(c)
      for v,k in used.items():
        np,dp=cache[v];j=m[IDX[v]]
        term=mul(term,mul(np[j],dp[k-j]))
      num=add(num,term)
    return num,den

def raw_ratio(n,d,coords):
    nn,nd=evaluate(n,coords);dn,dd=evaluate(d,coords)
    return mul(nn,dd),mul(nd,dn)

def poly_equal(a,b,label):require(a==b,label)
def content_sha(rows):return hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()

atlas=read('research_cycle_2014/fused_chart_atlas/CERTIFICATE.json')
base=next(b for b in atlas['branches'] if b['name']=='H_nonzero__regular')
upstream=read('research_cycle_1805/guarded_fourier_reduction/CERTIFICATE.json')
pinned=read('research_cycle_1917/zero_pivot_branch/PINNED_INPUT.json')
AT={k:decode(v,atlas['variables']) for k,v in atlas['polynomials'].items()}
POOL={}
for d in [upstream,pinned]:POOL.update(d.get('polynomials',{}))
# Fill original reference definitions from the pinned, inert source collection.
for path,h in atlas['source_hashes'].items():
    bind(path,h)
    if path.endswith('.json'):
      obj=read(path)
      if isinstance(obj,dict):
        for k,v in obj.get('polynomials',{}).items():
          if len(k)!=64 or any(c not in '0123456789abcdef' for c in k):continue
          if k in POOL:assert POOL[k]==v,('conflicting content',k)
          POOL[k]=v
ORIG={}
def original(ref):
    if ref not in ORIG:
      rows=POOL[ref]
      assert content_sha(rows)==ref,('polynomial hash mismatch',ref)
      ORIG[ref]=decode(rows,V)
    return ORIG[ref]

# Fixed exact source-level facts, independent of candidate payloads.
zeta=const((F(0),F(1))+(F(0),)*8)
b,c,q,e,d,x,r=[X[v] for v in (11,34,41,83,65,0,88)]
require(sum((1 for k in atlas['equations']),0)==50,'baseline has 50 retained residuals')
require(len(atlas['guards'])==19,'baseline has 19 retained guards')
for ref in list(atlas['equations'].values())+list(atlas['guards'].values()):original(ref)
for f in atlas['inherited_definitions']:
    original(f['numerator']);original(f['denominator'])
original(atlas['x91_restoration']['numerator']);original(atlas['x91_restoration']['denominator'])
poly_equal(original(atlas['guards']['x41']),q,'original x41 guard is exactly q')
poly_equal(AT['Q_c_den'],mul(b,AT['Q_H']),'accepted c denominator is b*H')
poly_equal(AT['Q_c_num'],add(mul(b,AT['Q_C1']),AT['Q_C0']),'accepted c numerator is b*C1+C0')
poly_equal(AT['Q_d_den'],mul(mul(mul(mul(power(zeta,4),b),q),e),original(atlas['guards']['D25'])),'D65 = zeta^4*b*q*e*D25')
poly_equal(AT['F_D88'],add(mul(mul(mul(mul(q,AT['F_M']),d),x),ONE),AT['F_K0']),'D88 = q*M*d*x+K0')
poly_equal(AT['F_J'],add(mul(AT['F_A'],AT['F_N88']),mul(AT['F_B'],AT['F_K0'])),'J = A35*N88+B35*K0')
poly_equal(AT['x0_num'],neg(AT['F_J']),'regular x0 numerator is -J')
poly_equal(AT['x0_den'],mul(mul(mul(AT['F_B'],q),AT['F_M']),d),'regular x0 denominator is B35*q*M*d')
poly_equal(AT['F_N88'],neg(power(zeta,10)),'N88 = -zeta^10, a nonzero constant')
original_r=next(j for j in base['definitions'] if j['variable']==88)
for atlas_name,role in [('F_D88','denominator'),('F_N88','numerator')]:
    original_reduced,original_den=evaluate(original(original_r[role]),{22:(ONE,ONE),49:(sub(zeta,c),ONE)})
    poly_equal(original_den,ONE,'original r '+role+' normalization is polynomial')
    poly_equal(original_reduced,AT[atlas_name],'original r '+role+' source equals '+atlas_name)
require(len(base['definitions'])==13 and {j['variable'] for j in base['definitions']}==set(V)-{11,41,83},'accepted definitions reconstruct all other coordinates without overwriting inputs')
# Original regular reconstruction gives D88=-A35*N88/B35.
dn,dd=evaluate(AT['F_D88'],{0:(AT['x0_num'],AT['x0_den'])})
poly_equal(mul(dn,AT['F_B']),neg(mul(mul(dd,AT['F_A']),AT['F_N88'])),'regular original D88 rational identity')
poly_equal(AT['Q_x92_den'],mul(q,AT['Q_a']),'x92 denominator = q*a')
yzero,_=evaluate(AT['Q_x92_num'],{0:({},ONE)})
poly_equal(AT['Q_x92_num'],sub(yzero,mul(mul(x,d),AT['Q_x92_den'])),'x92 numerator affine-shift identity')
# Verify N25(x,d,x92) = N25(0,d,x92+x*d) directly, without a gauge assumption.
n25_ref=next(j['numerator'] for j in base['definitions'] if j['variable']==25)
n25=original(n25_ref)
n25_zero,_=evaluate(n25,{0:({},ONE)})
n25_shift,_=evaluate(n25_zero,{92:(add(X[92],mul(x,d)),ONE)})
poly_equal(n25,n25_shift,'original N25 depends on x0,x92 only through x92+x0*d')
e41=original(atlas['equations']['41'])
require(support(e41)=={11,25,34,39,41,49,83},'original E41 support excludes x0,d,x92')
require(len(e41)==22,'original E41 has 22 exact source terms')


def validate(candidate,record=True):
    global checks
    saved_checks=checks
    if not record:checks=[]
    try:
      require(candidate['variables']==[11,34,41,83],'candidate variable order')
      require(candidate['original_E41']==atlas['equations']['41'],'original E41 reference unchanged')
      require(candidate['scope']=='Refinement only of fixed-F11 regular H!=0 chart','bounded target scope')
      require(candidate['field']==atlas['field'],'exact field and extension scope')
      required_claims={'generic_q_elimination':True,'zero_pivot_infeasibility':False,'chart_feasibility':False,'dimension':False,'novelty':False,'full_fourier_factorization':False}
      require(candidate['claims']==required_claims,'claims do not exceed generic branch refinement')
      branches=candidate['branches']
      require(len(branches)==2,'both coefficient cases retained')
      generic,exceptional=branches
      require(generic['name']=='E41_A_nonzero' and exceptional['name']=='E41_A_zero','branch names and order')
      for branch in branches:
        require(branch['retained_branch']==base,'full accepted branch exactly retained: '+branch['name'])
        require(branch['retained_branch']['retained_equations']==atlas['equations'],'50 exact residual references preserved: '+branch['name'])
        require(branch['retained_branch']['retained_guards']==atlas['guards'],'19 exact guards preserved: '+branch['name'])
      require(generic['inputs']==[11,83] and generic['added_conditions']==['A!=0'],'generic inputs and nonzero coefficient predicate')
      require(generic['q_reconstruction']=={'numerator':'-B','denominator':'A'},'generic signed q reconstruction')
      require(generic['evaluation_order']=='Bind q=-B/A first; then execute the accepted branch definitions unchanged.','generic q-first evaluation order')
      require(generic['reverse_map']=={'type':'projection','coordinates':[11,83]},'generic inverse projection')
      require(exceptional['inputs']==[11,41,83] and exceptional['added_conditions']==['A=0'] and exceptional['added_equations']==['B=0'],'exceptional A=B=0 keeps three inputs')
      require(exceptional['q_reconstruction']=='q remains a retained input','exceptional q is not divided away')
      require(exceptional['reverse_map']=={'type':'projection','coordinates':[11,41,83]},'exceptional inverse projection')
      require(exceptional['evaluation_order']=='Execute the accepted branch definitions unchanged.','exceptional evaluation order')
      # Numerically named representations are shifted only in this proof circuit.
      coords={0:({},ONE),22:(ONE,ONE),49:(sub(zeta,c),ONE)}
      nums={};dens={}
      rows=candidate['coordinate_ledger']
      require([u['variable'] for u in rows]==[65,92,88,25,39],'coordinate ledger order')
      expected_sources=[('atlas','Q_d_num','Q_d_den'),('atlas','Q_x92_num','Q_x92_den'),('E35 consequence','-F_B','F_A')]
      for i,row in enumerate(rows):
        v=row['variable'];spec=row['basis']
        if i<3:
          kind,nref,dref=expected_sources[i]
          require(spec=={'kind':kind,'numerator':nref,'denominator':dref},'coordinate source binding '+str(v))
          n=neg(AT['F_B']) if nref=='-F_B' else AT[nref]
          denominator=AT[dref]
        else:
          definition=next(a for a in base['definitions'] if a['variable']==v)
          require(spec=={'kind':'original','numerator':definition['numerator'],'denominator':definition['denominator']},'original coordinate source binding '+str(v))
          n=original(spec['numerator']);denominator=original(spec['denominator'])
        raw_n,raw_d=raw_ratio(n,denominator,coords)
        reduced_n=decode(row['num'],candidate['variables'])
        reduced_d=decode(row['den'],candidate['variables'])
        quotient=decode(row['raw_denominator_over_reduced_denominator'],candidate['variables'])
        require(bool(raw_d) and bool(reduced_d) and bool(quotient),'nonzero formal denominator polynomials '+str(v))
        poly_equal(raw_n,mul(reduced_n,quotient),'raw numerator cancellation identity '+str(v))
        poly_equal(raw_d,mul(reduced_d,quotient),'raw denominator cancellation identity '+str(v))
        coords[v]=(reduced_n,reduced_d);nums[v]=reduced_n;dens[v]=reduced_d
      N=decode(candidate['E41_num'],candidate['variables']);D=decode(candidate['E41_den'],candidate['variables'])
      raw_n,raw_d=evaluate(e41,coords)
      T=decode(candidate['E41_denominator_quotient'],candidate['variables'])
      poly_equal(raw_n,mul(N,T),'original E41 raw numerator exact cancellation')
      poly_equal(raw_d,mul(D,T),'original E41 raw denominator exact cancellation')
      require(bool(raw_d) and bool(D) and bool(T),'E41 cancellation factors formally nonzero')
      cn=decode(candidate['c_num'],candidate['variables']);cd=decode(candidate['c_den'],candidate['variables'])
      poly_equal(cn,AT['Q_c_num'],'c numerator exact accepted source')
      poly_equal(cd,AT['Q_c_den'],'c denominator exact accepted source')
      require(support(cn)<= {11,83} and support(cd)<= {11,83},'c reconstruction depends only on b,e')
      require(candidate['c_clearing_exponent']==3 and degree(N,34)==3,'exact c clearing exponent is three')
      cleared_n,cleared_d=evaluate(N,{34:(cn,cd)})
      poly_equal(cleared_d,power(cd,3),'c substitution raw denominator is cd^3')
      P=decode(candidate['P'],candidate['variables']);A=decode(candidate['A'],candidate['variables']);B=decode(candidate['B'],candidate['variables'])
      poly_equal(cleared_n,P,'all exact cleared E41 coefficients')
      poly_equal(P,add(mul(A,q),B),'P = A*q+B exactly')
      require(support(A)<= {11,83} and support(B)<= {11,83},'new coefficients A,B depend only on b,e')
      require(bool(A) and bool(B),'A,B formally nonzero without a feasibility inference')
      stats={'E41_terms':len(N),'P_terms':len(P),'A_terms':len(A),'B_terms':len(B),'A_degrees':[degree(A,v) for v in candidate['variables']],'B_degrees':[degree(B,v) for v in candidate['variables']]}
      require(candidate['stats']==stats,'reported term counts and multidegrees exact')
      # q=-B/A satisfies the affine equation identically; no division by B.
      p_n,p_d=evaluate(P,{41:(neg(B),A)})
      require(not p_n,'generic q substitution annihilates P exactly')
      poly_equal(p_d,A,'new q substitution denominator is A only')
      return {'stats':stats,'coordinate_order':[u['variable'] for u in rows]}
    finally:
      if not record:checks=saved_checks


def mutated(c,change):
    x=copy.deepcopy(c);change(x);return x

def bump_row(row):row[1][0]+=row[2]
def controls(candidate):
    cases=[]
    def test(name,change):
      try:validate(mutated(candidate,change),False)
      except (AssertionError,KeyError,ValueError):cases.append(name)
      else:raise AssertionError('negative control accepted: '+name)
    test('delete three-input exception',lambda x:x['branches'].pop())
    test('delete exceptional B=0',lambda x:x['branches'][1].__setitem__('added_equations',[]))
    test('delete original q nonzero guard',lambda x:x['branches'][0]['retained_branch']['retained_guards'].pop('x41'))
    test('delete original E41',lambda x:x['branches'][1]['retained_branch']['retained_equations'].pop('41'))
    test('q solve wrong sign',lambda x:x['branches'][0]['q_reconstruction'].__setitem__('numerator','B'))
    test('wrong generic projection',lambda x:x['branches'][0]['reverse_map'].__setitem__('coordinates',[11,41]))
    test('generic q binding scheduled too late',lambda x:x['branches'][0].__setitem__('evaluation_order','Execute definitions before q.'))
    test('replace exceptional input q',lambda x:x['branches'][1].__setitem__('inputs',[11,34,83]))
    test('unsupported feasibility claim',lambda x:x['claims'].__setitem__('chart_feasibility',True))
    for k in ['E41_num','E41_den','E41_denominator_quotient','c_num','c_den','P','A','B']:
      test('corrupt '+k,lambda x,k=k:bump_row(x[k][0]))
    test('change c clearing exponent',lambda x:x.__setitem__('c_clearing_exponent',2))
    for i,row in enumerate(candidate['coordinate_ledger']):
      for key in ['num','den','raw_denominator_over_reduced_denominator']:
        test('corrupt coordinate '+str(row['variable'])+' '+key,lambda x,i=i,key=key:bump_row(x['coordinate_ledger'][i][key][0]))
    # Full coefficient mutation checks for the new asserted A and B, no hash gate.
    for k in ['A','B']:
      for i in range(len(candidate[k])):
        test('coefficient '+k+' term '+str(i),lambda x,k=k,i=i:bump_row(x[k][i]))
    return cases


def main():
    start=time.monotonic()
    seal=read(str((TARGET/'SEAL.json').relative_to(ROOT)))
    assert sha(TARGET/'SEAL.json')=='b7b0b311515d5e35675566fa5ddb6c0af05dca645b9b13e89fed976442d74ca0'
    for path,h in seal['artifact_hashes'].items():assert sha(TARGET/path)==h,('candidate artifact changed',path)
    assert sha(TARGET/'SHA256SUMS.txt')==seal['manifest_sha256']
    candidate=read(str((TARGET/'CANDIDATE.json').relative_to(ROOT)))
    for p,h in candidate['source_hashes'].items():bind(p,h)
    for p,h in atlas['prerequisite_receipts'].items():bind(p,h)
    receipt=read('research_cycle_2016/three_input_atlas_review/RECEIPT.json')
    require(receipt['candidate_sha256']==sha(ROOT/'research_cycle_2014/fused_chart_atlas/CERTIFICATE.json'),'accepted atlas receipt binds baseline bytes')
    dispatch=read('research_review_dispatch_2056/ACCEPTED_F11_CONTINUATIONS.json')
    for p in dispatch['accepted']:bind(p['receipt'],p['sha256'])
    result=validate(candidate)
    diagnostic=read(str((TARGET/'E41_FOUR_VARIABLES.json').relative_to(ROOT)))
    require(diagnostic['E41_numerator']==candidate['E41_num'] and diagnostic['E41_denominator']==candidate['E41_den'],'diagnostic E41 coefficients exactly match authoritative candidate')
    require(diagnostic['variables']==['b','c','q','e'],'diagnostic four-variable coordinate order')
    NN=decode(candidate['E41_num'],candidate['variables']);DD=decode(candidate['E41_den'],candidate['variables'])
    require(diagnostic['stats']=={'num_terms':len(NN),'den_terms':len(DD),'degrees':[degree(NN,v) for v in candidate['variables']],'den_degrees':[degree(DD,v) for v in candidate['variables']]},'diagnostic multidegrees and counts exact')
    print('Independent exact positive checks PASS',len(checks),flush=True)
    negative=controls(candidate)
    print('Independent semantic negative controls rejected',len(negative),flush=True)
    # Recheck every seal and source after all calculations.
    for p,h in source_hashes.items():assert sha(ROOT/p)==h
    for p,h in seal['artifact_hashes'].items():assert sha(TARGET/p)==h
    assert sha(TARGET/'SEAL.json')=='b7b0b311515d5e35675566fa5ddb6c0af05dca645b9b13e89fed976442d74ca0'
    summary={'status':'PASS: independent exact bounded H!=0 continuation arithmetic and structure','candidate_sha256':sha(TARGET/'CANDIDATE.json'),'seal_sha256':sha(TARGET/'SEAL.json'),'checks':checks,'check_count':len(checks),'negative_controls_rejected':negative,'negative_control_count':len(negative),'source_hashes':source_hashes,'source_polynomials_content_verified':len(ORIG),'distinct_cyclotomic_products_dual_checked':cmul.cache_info().currsize,'coefficient_arithmetic':'fractions.Fraction; every coefficient product cross-checked by cyclic convolution and long Phi11 reduction','historical_program_execution':False,'historical_program_source_inspection':False,'author_program_execution':False,'author_program_source_inspection':False,'checker_sha256':sha(Path(__file__)),'result':result,'elapsed_seconds':round(time.monotonic()-start,3)}
    (OUT/'ARITHMETIC_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['status','check_count','negative_control_count','distinct_cyclotomic_products_dual_checked','elapsed_seconds']},indent=2))
if __name__=='__main__':main()
