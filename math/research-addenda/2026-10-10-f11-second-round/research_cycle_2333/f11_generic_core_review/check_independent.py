#!/usr/bin/env python3
"""Fresh bounded E25 review. Imports only Python's standard library.
Historical files are read as inert JSON or byte-hashed, never imported/executed.
"""
from pathlib import Path
from math import gcd
from functools import lru_cache
from copy import deepcopy
import hashlib,json,time

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
AUTHOR=ROOT/'research_cycle_2325/f11_generic_residual'
CERT_SHA='3db49646d9e36a1e979a31dccd49e6f4e5c4dd1484412cb7b602aa1b1511a0d9'
SEAL_SHA='2edc8f9a9c46a54d5d01e6a98c9fce55dbdcceb7b83a0a8113c2732af5354273'
PINS={
'research_cycle_1805/guarded_fourier_reduction/CERTIFICATE.json':'8a7f612c361540d427fd33aea8dc6c9710ae969a66ce15e000c9b1e3467859b4',
'research_cycle_2014/fused_chart_atlas/CERTIFICATE.json':'3fd7382a6207024853f7cf466b05a1f7aba9d9ef7e1b737353711a0394d49024',
'research_cycle_2304/regular_hnonzero_analysis/CANDIDATE.json':'6f10377ef9be102175f559e20e67c928eb88ca1f1868baafe62c4678ce3da8fa',
'research_cycle_2310/hnonzero_continuation_review/RECEIPT.json':'22e0babbd1d637a38a355bed333317fb1f38c98057403715374fcdd066880d9e'}
checks=[]

def ensure(ok,label):
    if not ok:raise AssertionError(label)

def check(ok,label):
    ensure(ok,label);checks.append(label);print('PASS',label,flush=True)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def content_sha(rows):return hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
def read(path):return json.loads(Path(path).read_text())

# A field element is a reduced integral vector of length 10 and one positive denominator.
def knorm(nums,den=1):
    ensure(len(nums)==10 and type(den) is int and den!=0,'valid scalar')
    if den<0:nums=[-v for v in nums];den=-den
    g=den
    for v in nums:g=gcd(g,v)
    return tuple(v//g for v in nums),den//g

ZERO=knorm([0]*10);ONE=knorm([1]+[0]*9);NEG=knorm([-1]+[0]*9)

def kadd(a,b):
    if a==ZERO:return b
    if b==ZERO:return a
    u,v=a;x,y=b;g=gcd(v,y);d=v//g*y
    return knorm([u[i]*(y//g)+x[i]*(v//g) for i in range(10)],d)

def kneg(a):return tuple(-x for x in a[0]),a[1]

@lru_cache(maxsize=300000)
def kmul(a,b):
    if a==ZERO or b==ZERO:return ZERO
    if a==ONE:return b
    if b==ONE:return a
    u,v=a;x,y=b
    # Independent representations: ordinary convolution + monic long division,
    # and cyclic convolution mod z^11-1 followed by z^10=-(1+...+z^9).
    long=[0]*19;cyclic=[0]*11
    for i in range(10):
        for j in range(10):
            term=u[i]*x[j];long[i+j]+=term;cyclic[(i+j)%11]+=term
    for degree in range(18,9,-1):
        q=long[degree]
        for j in range(11):long[degree-10+j]-=q
    cyc=[cyclic[i]-cyclic[10] for i in range(10)]
    ensure(long[:10]==cyc and not any(long[10:]),'dual field multiplication')
    return knorm(long[:10],v*y)

E0=(0,0,0,0)
def constant(a):return {} if a==ZERO else {E0:a}
UNIT=constant(ONE)
def var(i):return {tuple(int(j==i) for j in range(4)):ONE}

def padd(a,b):
    out=dict(a)
    for m,c in b.items():
        t=kadd(out.get(m,ZERO),c)
        if t==ZERO:out.pop(m,None)
        else:out[m]=t
    return out

def pneg(a):return {m:kneg(c) for m,c in a.items()}
def pmul(a,b):
    out={}
    for m,c in a.items():
        for n,d in b.items():
            exp=tuple(m[i]+n[i] for i in range(4));term=kmul(c,d)
            val=kadd(out.get(exp,ZERO),term)
            if val==ZERO:out.pop(exp,None)
            else:out[exp]=val
    return out

def powers(p,n):
    out=[UNIT]
    for _ in range(n):out.append(pmul(out[-1],p))
    return out

def ppow(p,n):return powers(p,n)[-1]
def degree(p,i):return max((m[i] for m in p),default=-1)
def stat(p):return {'terms':len(p),'degrees':[degree(p,i) for i in range(4)]}

def parse(rows,n=4):
    ensure(isinstance(rows,list),'polynomial rows')
    out={};prev=None
    for row in rows:
        ensure(isinstance(row,list) and len(row)==3,'polynomial triple')
        m,nums,den=row
        ensure(len(m)==n and all(type(i) is int and i>=0 for i in m),'nonnegative exponent vector')
        ensure(len(nums)==10 and all(type(i) is int for i in nums) and type(den) is int and den>0,'rational coefficient row')
        key=tuple(m);val=knorm(nums,den)
        ensure(val!=ZERO and val==(tuple(nums),den),'canonical nonzero coefficient')
        ensure(key not in out and (prev is None or prev<key),'unique sorted monomials')
        out[key]=val;prev=key
    return out

def project(rows,variables):
    p=parse(rows,len(variables));idx={v:i for i,v in enumerate(variables)};out={}
    for mon,coef in p.items():
        ensure(all(ex==0 or variables[j] in [11,34,41,83] for j,ex in enumerate(mon)),'projected polynomial support')
        out[tuple(mon[idx[v]] for v in [11,34,41,83])]=coef
    return out

def clear_variable(poly,index,num,den,exponent):
    ensure(degree(poly,index)<=exponent,'clearing degree bound')
    np=powers(num,exponent);dp=powers(den,exponent);mix=[pmul(np[i],dp[exponent-i]) for i in range(exponent+1)]
    groups={}
    for mon,coef in poly.items():
        power=mon[index];m=list(mon);m[index]=0
        groups.setdefault(power,{})[tuple(m)]=coef
    result={}
    for power,group in groups.items():result=padd(result,pmul(group,mix[power]))
    return result

def substitute_raw(poly,variables,coordinates):
    maxima=[max((m[i] for m in poly),default=0) for i in range(len(variables))]
    active=[i for i,m in enumerate(maxima) if m]
    prep={};den=UNIT
    for i in active:
        n,d=coordinates[variables[i]];np=powers(n,maxima[i]);dp=powers(d,maxima[i])
        prep[i]=[pmul(np[k],dp[maxima[i]-k]) for k in range(maxima[i]+1)]
        den=pmul(den,dp[maxima[i]])
    num={}
    for mon,coef in poly.items():
        term=constant(coef)
        for i in active:term=pmul(term,prep[i][mon[i]])
        num=padd(num,term)
    return num,den,{str(variables[i]):maxima[i] for i in active}

start=time.monotonic()
check(sha(AUTHOR/'CERTIFICATE.json')==CERT_SHA,'requested certificate pin')
check(sha(AUTHOR/'SEAL.json')==SEAL_SHA,'requested author seal pin')
candidate=read(AUTHOR/'CERTIFICATE.json');seal=read(AUTHOR/'SEAL.json')
check(seal['certificate_sha256']==CERT_SHA,'seal certificate binding')
check(sha(AUTHOR/'SHA256SUMS.txt')==seal['manifest_sha256'],'author manifest pin')
manifest={}
for line in (AUTHOR/'SHA256SUMS.txt').read_text().splitlines():
    h,name=line.split('  ',1);ensure('/' not in name and '..' not in name,'flat author manifest');manifest[name]=h
check(manifest==seal['artifacts'],'author seal manifest equality')
for name,h in manifest.items():check(sha(AUTHOR/name)==h,'author artifact hash '+name)
for path,h in PINS.items():check(sha(ROOT/path)==h,'source pin '+path)
source=read(ROOT/list(PINS)[0]);atlas=read(ROOT/list(PINS)[1]);base=read(ROOT/list(PINS)[2]);prior=read(ROOT/list(PINS)[3])
check(prior['candidate_sha256']==PINS[list(PINS)[2]],'prior independent receipt accepts exact base')
check(prior['status'].startswith('PASS:'),'prior receipt passes')
for key in ['all_19_original_guards_retained_per_piece','all_50_original_residuals_retained_per_piece','all_canceled_denominators_protected','original_q_nonzero_guard_retained','five_coordinate_and_E41_cancellation_pairs_exact']:
    check(prior['claims'][key] is True,'accepted prerequisite '+key)
check(prior['source_hashes'][list(PINS)[0]]==PINS[list(PINS)[0]] and prior['source_hashes'][list(PINS)[1]]==PINS[list(PINS)[1]],'prior source bindings')

ref='ce2413e7d1b9e31c5372467e1d12115510d1385a73052fbb0e9c005b1d7ca841'
check(source['final']['equations']['25']==atlas['equations']['25']==ref,'retained source E25 binding')
source_rows=source['polynomials'][ref];source_poly=parse(source_rows,len(source['variables']))
check(content_sha(source_rows)==ref,'E25 actual coefficient content address')
support=[v for i,v in enumerate(source['variables']) if any(m[i] for m in source_poly)]
check(len(source_rows)==55 and support==[11,22,25,34,39,41,49,65,83,88],'55-term exact source support without x0 or x92')
source_polynomials_verified=0
for h in set(atlas['equations'].values())|set(atlas['guards'].values()):
    if h in source['polynomials']:
        ensure(content_sha(source['polynomials'][h])==h,'retained source content hash '+h);source_polynomials_verified+=1
check(source_polynomials_verified==64,'64 available retained equation/guard content addresses')
check(len(atlas['equations'])==50 and len(atlas['guards'])==19,'accepted original predicate counts')
branch=next(b for b in atlas['branches'] if b['name']=='H_nonzero__regular')
check(base['branches'][0]['retained_branch']==base['branches'][1]['retained_branch']==branch,'both accepted wrappers retain complete regular branch')
check(branch['retained_equations']==atlas['equations'] and branch['retained_guards']==atlas['guards'],'all original predicate mappings retained')
check(branch['conditions']==['Q_H!=0','d!=0','F_M!=0'],'regular conditions')
check(branch['additional_guards']==['b!=0','Q_a!=0','F_A!=0','F_B!=0'],'additional guards')
check('x41' in branch['retained_guards'] and 'x83' in branch['retained_guards'],'original q and e guards')
check(base['branches'][0]['added_conditions']==['A!=0'] and base['branches'][0]['q_reconstruction']=={'numerator':'-B','denominator':'A'},'generic A pivot only')
check(base['branches'][1]['added_conditions']==['A=0'] and base['branches'][1]['added_equations']==['B=0'] and base['branches'][1]['inputs']==[11,41,83],'explicit A=B=0 exception')

zeta=constant(knorm([0,1]+[0]*8));b,c,q,e=[var(i) for i in range(4)]
coordinates={11:(b,UNIT),34:(c,UNIT),41:(q,UNIT),83:(e,UNIT),22:(UNIT,UNIT),49:(padd(zeta,pneg(c)),UNIT)}
check(project(atlas['polynomials']['bind22'],atlas['variables'])==UNIT,'binding x22=1')
check(project(atlas['polynomials']['bind49'],atlas['variables'])==coordinates[49][0],'binding x49=zeta-c')
for item in base['coordinate_ledger']:
    if item['variable'] in [25,39,65,88]:
        coordinates[item['variable']]=(parse(item['num']),parse(item['den']))
        check(bool(coordinates[item['variable']][1]),'nonzero polynomial coordinate denominator '+str(item['variable']))
check(sorted(coordinates)==support,'complete E25 coordinate coverage')
check(project(source['polynomials'][atlas['guards']['x41']],source['variables'])==q,'original x41 guard is q')
check(project(source['polynomials'][atlas['guards']['x83']],source['variables'])==e,'original x83 guard is e')
check(coordinates[65]==(project(atlas['polynomials']['Q_d_num'],atlas['variables']),project(atlas['polynomials']['Q_d_den'],atlas['variables'])),'x65 coordinate exact atlas binding')
check(coordinates[88]==(pneg(project(atlas['polynomials']['F_B'],atlas['variables'])),project(atlas['polynomials']['F_A'],atlas['variables'])),'x88 coordinate exact guarded E35 binding')
# Values in this ledger, including canceled denominator protection, are accepted
# prerequisites through the pinned independent receipt, not inferred here.
raw_num,raw_den,maxima=substitute_raw(source_poly,source['variables'],coordinates)
check(raw_num==parse(candidate['raw_num']),'fresh source coordinate substitution numerator')
check(raw_den==parse(candidate['raw_den']),'fresh source coordinate substitution denominator')
N4=parse(candidate['N4']);D4=parse(candidate['D4']);T=parse(candidate['quotient4'])
check(pmul(N4,T)==raw_num,'N_raw=N4*T exact coefficient identity')
check(pmul(D4,T)==raw_den,'D_raw=D4*T exact coefficient identity')
cn=parse(base['c_num']);cd=parse(base['c_den']);A=parse(base['A']);B=parse(base['B'])
H=project(atlas['polynomials']['Q_H'],atlas['variables'])
check(cn==project(atlas['polynomials']['Q_c_num'],atlas['variables']),'c numerator exact accepted atlas binding')
check(cd==project(atlas['polynomials']['Q_c_den'],atlas['variables']),'c denominator exact accepted atlas binding')
check(cd==pmul(b,H),'c denominator b*H identity')
check(degree(N4,1)==4,'exact c-degree four')
N3=clear_variable(N4,1,cn,cd,4)
check(N3==parse(candidate['N3']),'N3=cd^4*N4(b,cn/cd,q,e) exact identity')
check(degree(N3,2)==2,'exact q-degree two')
check(all(m[1]==m[2]==0 for m in A) and all(m[1]==m[2]==0 for m in B),'A and B depend only on b,e')
N2=clear_variable(N3,2,pneg(B),A,2)
check(N2==parse(candidate['N2']),'N2=A^2*N3(b,-B/A,e) exact identity')
strip_product=pmul(pmul(ppow(b,10),ppow(e,3)),H);core=parse(candidate['core'])
check(strip_product==parse(candidate['stripped_product']),'stripped product is exactly b^10*e^3*H')
check(pmul(strip_product,core)==N2,'N2=b^10*e^3*H*core exact identity')
check(all(m[1]==m[2]==0 for m in N2) and all(m[1]==m[2]==0 for m in core),'N2 and core use only b,e')
check(stat(N2)=={'terms':370,'degrees':[19,0,0,39]},'N2 exact 370 terms and (19,39) multidegree')
check(stat(core)=={'terms':340,'degrees':[9,0,0,33]},'core exact 340 terms and (9,33) multidegree')
check(degree(core,0)>1 and degree(core,3)>1,'direct core is nonaffine in both inputs')
expected_polys={'raw_num':raw_num,'raw_den':raw_den,'N4':N4,'D4':D4,'quotient4':T,'N3':N3,'N2':N2,'core':core,'stripped_product':strip_product}
expected_stats={k:stat(v) for k,v in expected_polys.items() if k in ['raw_num','raw_den','N4','D4','quotient4','N3','N2']}
expected_factors=[{'exponent':10,'label':'b','polynomial':[[[1,0,0,0],[1,0,0,0,0,0,0,0,0,0],1]]},{'exponent':3,'label':'e','polynomial':[[[0,0,0,1],[1,0,0,0,0,0,0,0,0,0],1]]},{'exponent':1,'label':'H','polynomial':candidate['stripped_factors'][2]['polynomial']}]
check(parse(expected_factors[2]['polynomial'])==H,'stripped H is pinned atlas H')
expected_claims={'A_zero_exception_eliminated':False,'dimension':False,'feasibility':False,'full_Fourier_factorization':False,'global_two_input':False,'guarded_equivalence_to_E25':True,'infeasibility':False,'necessary_two_variable_polynomial':True,'new_linear_elimination':False,'nonzero_constant_obstruction':False,'novelty':False}
expected_preservation={'H_nonzero_regular_conditions':True,'all_19_original_guards':True,'all_50_original_residuals':True,'all_prior_cancellation_exclusions':True,'original_q_nonzero':True}

def validate(cand):
    # Deliberately no candidate or seal hash gate: the negative controls exercise
    # arithmetic results and structural predicates checked from inert sources.
    ensure(cand['source_hashes']==PINS,'source binding map')
    ensure(cand['original_residual']=='25' and cand['original_reference']==ref,'source selection')
    ensure(cand['variables']==[11,34,41,83] and cand['field']==base['field'],'field and variable convention')
    ensure(cand['retained_generic_branch']==base['branches'][0],'complete generic predicate retention')
    ensure(cand['unchanged_A_zero_exception']==base['branches'][1],'complete exceptional predicate retention')
    ensure(cand['preservation']==expected_preservation,'preservation claims')
    ensure(cand['claims']==expected_claims,'bounded claims only')
    ensure(cand['new_divisions']==[],'no new divisions')
    ensure(cand['new_necessary_conditions']==['N2(b,e)=0','core(b,e)=0'],'necessary conditions only')
    ensure(cand['c_power']==4 and cand['q_power']==2,'exact clearing exponents')
    for name,poly in expected_polys.items():ensure(parse(cand[name])==poly,'exact polynomial '+name)
    ensure(cand['stats']==expected_stats,'exact polynomial statistics')
    ensure(cand['stripped_factors']==expected_factors,'only approved stripped factors')
    ensure(cand['guarded_strip']=={'identity':'N2=b^10*e^3*H*core','nonzero_basis':{'H':'explicit Q_H!=0 condition','b':'accepted additional b!=0 guard','e':'original x83!=0 guard'}},'guarded cancellation basis')
    ensure(cand['bounded_attempt']['direct_core_terms']==340 and cand['bounded_attempt']['direct_core_multidegree']==[9,33],'bounded direct-core observation')
    return True

check(validate(candidate),'complete mathematical certificate validation without hash gate')
for name in ['DERIVATION.json','STRIPPED.json']:
    sibling=read(AUTHOR/name)
    check(all(candidate[k]==v for k,v in sibling.items()),'inert companion agreement '+name)

negative=[]
def reject(label,edit):
    changed=deepcopy(candidate);edit(changed)
    try:validate(changed)
    except (AssertionError,KeyError,TypeError,ValueError) as exc:
        negative.append({'name':label,'rejected_by':str(exc)});return
    raise AssertionError('negative control unexpectedly accepted: '+label)

def set_path(obj,path,value):
    for k in path[:-1]:obj=obj[k]
    obj[path[-1]]=value

def mutate_coefficient(obj,name):obj[name][0][1][0]+=obj[name][0][2]
for name in expected_polys:reject('coefficient corruption '+name,lambda x,name=name:mutate_coefficient(x,name))
for key,val in [('c_power',3),('q_power',1),('original_residual',41),('original_reference',base['original_E41']),('new_divisions',['B']),('new_necessary_conditions',['core(b,e)=0 is sufficient'])]:reject('alter '+key,lambda x,key=key,val=val:x.__setitem__(key,val))
for label,path,val in [
('drop A nonzero',['retained_generic_branch','added_conditions'],[]),
('change q solve sign',['retained_generic_branch','q_reconstruction','numerator'],'B'),
('drop H nonzero',['retained_generic_branch','retained_branch','conditions'],['d!=0','F_M!=0']),
('drop b guard',['retained_generic_branch','retained_branch','additional_guards'],['Q_a!=0','F_A!=0','F_B!=0']),
('drop exception',['unchanged_A_zero_exception'],{}),
('drop B=0 exception condition',['unchanged_A_zero_exception','added_equations'],[]),
('discard q exception input',['unchanged_A_zero_exception','inputs'],[11,83]),
('change strip exponent',['stripped_factors',0,'exponent'],9),
('strip B instead of H',['stripped_factors',2,'label'],'B'),
('deny original q guard',['preservation','original_q_nonzero'],False),
('false stats',['stats','N2','terms'],369),
('claim sufficiency',['claims','feasibility'],True),
('claim infeasibility',['claims','infeasibility'],True),
('claim global two input',['claims','global_two_input'],True),
('claim removed exception',['claims','A_zero_exception_eliminated'],True),
('claim new linear solve',['claims','new_linear_elimination'],True),
('claim novelty',['claims','novelty'],True),
('source-map corruption',['source_hashes',list(PINS)[0]],'0'*64),
]:reject(label,lambda x,path=path,val=val:set_path(x,path,val))
for guard in ['x41','x83','D25']:
    reject('remove original guard '+guard,lambda x,guard=guard:x['retained_generic_branch']['retained_branch']['retained_guards'].pop(guard))
reject('remove original E25',lambda x:x['retained_generic_branch']['retained_branch']['retained_equations'].pop('25'))
reject('remove inherited denominator rule',lambda x:x['retained_generic_branch']['retained_branch']['definitions'].pop())
check(len(negative)==38,'38 independent mutation controls rejected')
for path,h in PINS.items():check(sha(ROOT/path)==h,'final source pin '+path)
check(sha(AUTHOR/'CERTIFICATE.json')==CERT_SHA and sha(AUTHOR/'SEAL.json')==SEAL_SHA,'candidate and seal unchanged at completion')
receipt={
'status':'PASS: independent exact E25 generic-core review',
'accepted_scope':'On the accepted fixed-F11 regular H!=0, A!=0 piece, retained E25=0 is equivalent to N2(b,e)=0 and to core(b,e)=0, with N2=b^10*e^3*H*core. These are necessary conditions for the full retained circuit only.',
'candidate_path':str((AUTHOR/'CERTIFICATE.json').relative_to(ROOT)),'candidate_sha256':CERT_SHA,'author_seal_sha256':SEAL_SHA,
'source_hashes':PINS,'original_E25_content_address':ref,'source_E25_terms':55,'source_E25_support':support,'source_maximal_powers':maxima,
'exact_check_count':len(checks),'checks':checks,'negative_controls_rejected':len(negative),
'field_multiplication':'Integer convolution followed by monic Phi11 long division; every nontrivial distinct multiplication dual-checked using cyclic convolution modulo z^11-1 and Phi11 reduction.',
'distinct_coefficient_products_computed':kmul.cache_info().misses,'source_polynomials_content_verified':source_polynomials_verified,
'polynomial_statistics':dict(expected_stats,core=stat(core)),
'guarded_identity':'E25=N2/[A^2*cd^4*D4(b,cn/cd,-B/A,e)], cd=b*H, on the retained admissible domain.',
'cancellation_reason':'Every coordinate denominator in D_raw is nonzero by the pinned accepted ledger. D_raw=D4*T forces D4 and T nonzero in a field. cd=b*H and A are nonzero by retained guards. b^10*e^3*H is nonzero by b, x83 and H guards. No division by B is made.',
'claims':dict(expected_claims,all_50_residuals_retained=True,all_19_guards_retained=True,original_q_nonzero_retained=True,all_accepted_denominator_exclusions_retained=True,A_B_zero_exception_retained=True),
'nonaffinity_limit':'The stored core has degrees 9 and 33; this establishes only failure of a direct affine solve in those coordinates, not absence of other pivots, factors, or solutions.',
'author_program_execution':False,'historical_program_execution':False,'author_program_source_inspection':False,'historical_program_source_inspection':False,'external_writes':False,'ranking_changes':False,
'input_policy':'Inert JSON and byte hashes only; no author or inherited program is executed or imported.',
'trust_boundary':'The pinned independent 2310 receipt supplies the accepted base chart, rational-coordinate ledger, nonvanishing of its coordinate denominators, and historical projection/reconstruction theorem. This review independently binds E25 to source rows, substitutes that accepted ledger, checks both new cancellation identities, both clearings, guarded stripping, and complete predicate retention. It does not re-prove the accepted historical chart.',
'elapsed_seconds':round(time.monotonic()-start,3)}
(OUT/'ARITHMETIC_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
(OUT/'NEGATIVE_CONTROLS.json').write_text(json.dumps({'count':len(negative),'candidate_hash_gate_used':False,'controls':negative},indent=2,sort_keys=True)+'\n')
print('REVIEW PASS',receipt['exact_check_count'],'checks;',len(negative),'negative controls;',receipt['elapsed_seconds'],'seconds',flush=True)
