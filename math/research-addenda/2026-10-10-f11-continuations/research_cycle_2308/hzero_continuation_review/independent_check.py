"""Independent exact review. Standard-library sparse arithmetic; inert input JSON only.
No author/reviewer module is imported or executed. The author code was inspected
only for navigating data; all evidence below comes from the actual certificates.
"""
from pathlib import Path
import json, hashlib, math, functools, time
ROOT=Path.cwd(); OUT=Path(__file__).resolve().parent
AUTHOR=Path('research_cycle_2303/regular_hzero_analysis')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
checks=[]; pins={}; coeff_products=0; max_terms=0; pair_count=0

def pin(path,want=None):
    actual=sha(path)
    if want is not None: assert actual==want,(str(path),actual,want)
    if str(path) in pins: assert pins[str(path)]==actual
    pins[str(path)]=actual
    return actual

def norm(v,d=1):
    assert d and len(v)==10
    if d<0:v=[-x for x in v];d=-d
    g=math.gcd(d,*v)
    return tuple(x//g for x in v)+(d//g,)
ZERO=norm([0]*10); ONE=norm([1]+[0]*9)
def ca(a,b):
    g=math.gcd(a[10],b[10]);s=b[10]//g;t=a[10]//g
    return norm([a[i]*s+b[i]*t for i in range(10)],a[10]*s)
def cn(a):return tuple(-x for x in a[:10])+(a[10],)
@functools.lru_cache(maxsize=180000)
def cm(a,b):
    global coeff_products
    coeff_products+=1
    v=[0]*19; cyc=[0]*11
    for i in range(10):
        for j in range(10):
            t=a[i]*b[j];v[i+j]+=t;cyc[(i+j)%11]+=t
    for k in range(18,9,-1):
        t=v[k]
        for j in range(11):v[k-10+j]-=t
    other=[cyc[i]-cyc[10] for i in range(10)]
    assert v[:10]==other and not any(v[10:]),'Independent cyclotomic products differ'
    return norm(other,a[10]*b[10])
VARS=[0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92]
N=len(VARS); E0=(0,)*N
class P(dict):
    def __add__(a,b):
        if not isinstance(b,P): b=constant(b)
        r=P(a)
        for m,v in b.items():
            w=ca(r.get(m,ZERO),v)
            if w==ZERO:r.pop(m,None)
            else:r[m]=w
        return r
    __radd__=__add__
    def __neg__(a):return P((m,cn(v)) for m,v in a.items())
    def __sub__(a,b):return a+-b
    def __mul__(a,b):
        global max_terms,pair_count
        if not isinstance(b,P):b=constant(b)
        r=P();pair_count+=len(a)*len(b)
        for m,v in a.items():
            for n,w in b.items():
                mn=tuple(x+y for x,y in zip(m,n));co=ca(r.get(mn,ZERO),cm(v,w))
                if co==ZERO:r.pop(mn,None)
                else:r[mn]=co
        max_terms=max(max_terms,len(r));return r
    __rmul__=__mul__
    def __pow__(a,n):
        assert type(n) is int and n>=0
        r=constant(1)
        while n:
            if n&1:r=r*a
            n//=2
            if n:a=a*a
        return r

def constant(n):
    if not n:return P()
    return P({E0:norm([n]+[0]*9)})
def variable(v):
    m=[0]*N;m[VARS.index(v)]=1;return P({tuple(m):ONE})
x={v:variable(v) for v in VARS};z=P({E0:norm([0,1]+[0]*8)});one=constant(1)

def decode(rows,variables):
    r=P();last=None
    for m,v,d in rows:
        assert len(m)==len(variables) and len(v)==10 and type(d) is int and d>0
        assert all(type(k)is int and k>=0 for k in m)
        assert all(type(k)is int for k in v)
        assert last is None or tuple(m)>last
        last=tuple(m);co=norm(v,d);assert co!=ZERO
        ex=[0]*N
        for vi,k in zip(variables,m):ex[VARS.index(vi)]=k
        assert tuple(ex) not in r;r[tuple(ex)]=co
    return r

def degree(p,vi):return max((m[VARS.index(vi)] for m in p),default=-1)
def support(p):return {v for i,v in enumerate(VARS) if any(m[i] for m in p)}
def subst(p,env):
    cache={};ans=P()
    for m,v in p.items():
        t=P({E0:v})
        for i,k in enumerate(m):
            if k:
                vi=VARS[i]
                if (vi,k) not in cache:cache[vi,k]=env.get(vi,x[vi])**k
                t=t*cache[vi,k]
        ans=ans+t
    return ans

def eq(name,lhs,rhs):
    if not isinstance(rhs,P):rhs=constant(rhs)
    diff=lhs-rhs
    assert not diff,(name,len(diff),list(diff.items())[:1])
    assert lhs!=(rhs+one),name+' negative control'
    checks.append({'name':name,'left_terms':len(lhs),'right_terms':len(rhs),'zero_difference':True,'unit_perturbation_rejected':True})
    print('PASS',name,flush=True)

A=load('research_cycle_2014/fused_chart_atlas/CERTIFICATE.json')
AR=load('research_cycle_2016/three_input_atlas_review/RECEIPT.json')
pin('research_cycle_2014/fused_chart_atlas/CERTIFICATE.json',AR['candidate_sha256'])
pin('research_cycle_2016/three_input_atlas_review/RECEIPT.json')
assert AR['status'].startswith('PASS')
for rel,h in AR['artifacts'].items():pin(Path('research_cycle_2016/three_input_atlas_review')/rel,h)
for path,h in A['source_hashes'].items():pin(path,h)
for path,h in A['prerequisite_receipts'].items():pin(path,h)
S=load('research_cycle_1854/residual_gauge/SIX_COORDINATE_CIRCUIT.json')
assert S['variables']==VARS
pool={};locations={}
for path in S['polynomial_sources']:
    D=load(path);assert D['variables']==VARS
    for ref,p in D['polynomials'].items():
        if ref in pool:assert pool[ref]==p
        pool[ref]=p;locations[ref]=path
C=load(AUTHOR/'CERTIFICATE.json');pin(AUTHOR/'CERTIFICATE.json')
for path,h in C['source_pins'].items():pin(path,h)
assert load(AUTHOR/'SOURCE_PINS.json')==C['source_pins'];pin(AUTHOR/'SOURCE_PINS.json')
for accepted in load('research_review_dispatch_2056/ACCEPTED_F11_CONTINUATIONS.json')['accepted']:
    pin(accepted['receipt'],accepted['sha256']);assert load(accepted['receipt'])['status'].startswith('PASS')
B=next(b for b in A['branches'] if b['name']=='H_zero__regular')
CB=C['preserved_chart']
assert CB['retained_equations']==A['equations']==B['retained_equations']==S['equations']
assert CB['retained_guards']==A['guards']==B['retained_guards']==S['guards']
assert len(A['equations'])==50 and len(A['guards'])==19
expect=json.loads(json.dumps(B));expect['name']='H_zero__regular__polynomial_b'
old_def=next(d for d in expect['definitions'] if d['variable']==11)
new_def=next(d for d in CB['definitions'] if d['variable']==11)
assert new_def['numerator']=='new_b_polynomial' and new_def['denominator']=='one'
old_def.update(new_def);assert CB==expect
refs=set(A['equations'].values())|set(A['guards'].values())
for d in CB['definitions']:
    for side in ('numerator','denominator'):
        if d[side] not in A['polynomials'] and d[side]!='new_b_polynomial':refs.add(d[side])
assert set(C['source_polynomial_refs'])==refs
source_terms=0
for ref in sorted(refs):
    rows=pool[ref];assert hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==ref
    assert locations[ref]==C['source_polynomial_refs'][ref]
    decode(rows,VARS);source_terms+=len(rows)
assert C['source_polynomial_count']==len(refs) and C['source_term_count']==source_terms
# Irreducibility over Q: Phi11(t+1) is Eisenstein at 11.
coeff=[sum(math.comb(i,j) for i in range(j,11)) for j in range(11)]
assert coeff[-1]==1 and all(k%11==0 for k in coeff[:-1]) and coeff[0]%121!=0
assert sum((z**i for i in range(11)),P())==P() and z**11==one
ap={name:decode(p,A['variables']) for name,p in A['polynomials'].items()}
cp={name:decode(p,[11,34,41,83]) for name,p in C['polynomials'].items()}
get=lambda name:ap[name]
H,C0,C1=(get(n) for n in ('Q_H','Q_C0','Q_C1'))
b,c,q,e=x[11],x[34],x[41],x[83]
assert support(H)=={83} and degree(H,83)==3
bp=cp['new_b_polynomial'];assert support(bp)<={83} and degree(bp,83)==2
for name in ('C1_inverse','C1_inverse_H_multiplier','b_relation_quotient'):assert support(cp[name])<={83}
eq('C1 inverse modulo H',C1*cp['C1_inverse']+H*cp['C1_inverse_H_multiplier'],one)
eq('polynomial b exact quotient',C1*bp+C0,H*cp['b_relation_quotient'])
eq('old b numerator',get('Q_exception_b_num'),-C0)
eq('old b denominator',get('Q_exception_b_den'),C1)
eq('compatibility original relation',get('compat'),b*C1+C0-b*H*c)
for name in ('x83','D25','g98'):
    G=C['guard_Bezout'][name]
    gp=decode(G['guard_polynomial'],[83]);sm=decode(G['guard_multiplier'],[83]);tm=decode(G['H_multiplier'],[83])
    source=decode(pool[A['guards'][name]],VARS)
    sliced=subst(source,{22:one,49:z-c})
    if name=='g98':eq('g98 sliced source',sliced,cp['g98_after_slice'])
    eq(name+' actual guard binding',gp,subst(sliced,{11:bp}))
    eq(name+' Bezout nonvanishing',gp*sm+H*tm,one)
# Check each formula used to clear E41 against pinned source data.
D25=get('Q_D25');aa=get('Q_a');tt=get('Q_t');CC=get('Q_C')
Nd=get('Q_d_num');Dd=get('Q_d_den');AA=get('F_A');BB=get('F_B')
Ynum=cp['Y_numerator'];Yden=cp['Y_denominator']
eq('d denominator factorization',Dd,z**4*b*q*e*D25)
eq('Y denominator',Yden,q*aa*Dd)
eq('Y numerator',Ynum,-(q*b*tt*Nd+CC*Dd))
eq('x92 numerator binding',get('Q_x92_num'),-(q*aa*x[0]*x[65]+q*b*tt*x[65]+CC))
eq('x92 denominator binding',get('Q_x92_den'),q*aa)
eq('Y cancellation after d reconstruction',subst(get('Q_x92_num')+x[0]*x[65]*get('Q_x92_den'),{65:Nd})-CC*(Dd-one),Ynum)
# The previous identity keeps the q*b*t factor and applies denominator Dd to C.
N88=get('F_N88');D88=get('F_D88');M=get('F_M');K0=get('F_K0');J=get('F_J')
eq('D88 accepted affine binding',D88,x[0]*x[65]*q*M+K0)
eq('J accepted relation',J,AA*N88+BB*K0)
eq('regular x0 numerator',get('x0_num'),-J)
eq('regular x0 denominator',get('x0_den'),BB*x[65]*q*M)
eq('r=-B/A clear identity',BB*D88+AA*N88,x[0]*get('x0_den')-get('x0_num'))
for vi,nameN,nameD in ((88,'F_N88','F_D88'),(39,'F_N39','F_D39')):
    definition=next(d for d in A['inherited_definitions'] if d['variable']==vi)
    for side,name in (('numerator',nameN),('denominator',nameD)):
        eq(str(vi)+' '+side+' original-source binding',get(name),subst(decode(pool[definition[side]],VARS),{22:one,49:z-c}))
alpha=cp['alpha25'];beta=cp['beta25'];assert support(alpha)<= {83} and support(beta)<={83}
def25=next(d for d in A['inherited_definitions'] if d['variable']==25)
eq('N25 original factor structure',decode(pool[def25['numerator']],VARS),alpha+beta*x[88]*(one-x[92]-x[0]*x[65]))
eq('D25 source binding',decode(pool[def25['denominator']],VARS),D25)
N25n=cp['N25_cleared_numerator'];N25d=cp['N25_cleared_denominator']
eq('N25 new cleared numerator',N25n,alpha*AA*Yden-beta*BB*(Yden-Ynum))
eq('N25 new cleared denominator',N25d,AA*Yden*D25)
Esource=decode(pool[A['equations']['41']],VARS)
assert degree(Esource,25)==degree(Esource,39)==1
assert support(Esource)<={11,22,25,34,39,41,49,83}
Esource=subst(Esource,{22:one,49:z-c})
Eclear=P();N39=get('F_N39');D39=get('F_D39')
for m,v in Esource.items():
    ex=list(m);n25=ex[VARS.index(25)];n39=ex[VARS.index(39)]
    ex[VARS.index(25)]=ex[VARS.index(39)]=0
    Eclear=Eclear+P({tuple(ex):v})*N25n**n25*N25d**(1-n25)*N39**n39*D39**(1-n39)
eq('E41 direct original numerator clearing',cp['E41_clear'],Eclear)
Fac=cp['E41_cancel_factor'];Ered=cp['E41_reduced']
eq('E41 canceled factor',Fac,q**2*b*D25*aa*D39)
eq('E41 exact cancellation',Ered*Fac,Eclear)
k=C['E41_H_reduction']['b_degree'];assert degree(Ered,11)==k
hom=P()
for m,v in Ered.items():
    ex=list(m);ib=ex[VARS.index(11)];ex[VARS.index(11)]=0
    hom=hom+P({tuple(ex):v})*(-C0)**ib*C1**(k-ib)
HQ=decode(C['E41_H_reduction']['H_quotient'],[83,34,41]);REM=decode(C['E41_H_reduction']['remainder'],[83,34,41])
eq('E41 exact H quotient and remainder',hom,H*HQ+REM)
assert REM and degree(REM,83)<degree(H,83)
assert {n:degree(REM,v) for n,v in [('e',83),('c',34),('q',41)]}==C['E41_H_reduction']['remainder_degrees']=={'e':2,'c':3,'q':2}
assert len(REM)==C['E41_H_reduction']['remainder_terms']==33
# Independently check dependence ordering. Full original denominators remain mandatory.
bound=set(CB['inputs'])
for d in CB['definitions']:
    assert d['variable'] not in bound
    for side in ('numerator','denominator'):
        ref=d[side];pol=cp[ref] if ref in cp else ap[ref] if ref in ap else decode(pool[ref],VARS)
        assert support(pol)<=bound,(d['variable'],side,sorted(support(pol)-bound))
    bound.add(d['variable'])
assert bound==set(VARS)
assert C['claims']=={'polynomial_b_reconstruction':True,'redundant_original_guards':['x83','D25','g98'],'every_original_residual_retained':True,'every_original_guard_retained':True,'new_nonzero_coordinate_exclusions':[],'E41_necessary_polynomial':True,'further_input_elimination':False,'feasibility_decided':False,'infeasibility_claimed':False,'unrestricted_parameters_claimed':False,'dimension_claimed':False,'FFT_claimed':False}
# Recompute the author's bounded mutation set with this independent engine.
negative={}
negative['alter_b_constant']=bool(C1*(bp+one)+C0-H*cp['b_relation_quotient'])
negative['alter_E41_reduced_constant']=bool((Ered+one)*Fac-Eclear)
negative['alter_H_remainder_constant']=bool(hom-H*HQ-(REM+one))
for name in ('x83','D25','g98'):
    G=C['guard_Bezout'][name];gp=decode(G['guard_polynomial'],[83]);sm=decode(G['guard_multiplier'],[83]);tm=decode(G['H_multiplier'],[83])
    negative['alter_'+name+'_guard_multiplier']=bool(gp*(sm+one)+H*tm-one)
    negative['alter_'+name+'_H_multiplier']=bool(gp*sm+H*(tm+one)-one)
for label,field in [('residual','retained_equations'),('guard','retained_guards')]:
    for name in CB[field]:
        altered=dict(CB[field]);del altered[name]
        negative['omit_'+label+'_'+name]=altered!=B[field]
negative['add_optional_c_nonzero']=(CB['additional_guards']+['c!=0'])!=B['additional_guards']
assert len(negative)==79 and all(negative.values())
author_neg=load(AUTHOR/'NEGATIVE_CONTROLS.json');assert author_neg['tests']==negative and author_neg['rejected']==79
assert len(Ered)==105 and [degree(Ered,vi) for vi in [11,34,41,83]]==[4,3,2,3]
assert len(pool[A['equations']['41']])==22
(OUT/'NEGATIVE_CONTROLS.json').write_text(json.dumps({'independently_recomputed_author_mutations':negative,'identity_unit_perturbations_rejected':len(checks),'total_rejected':len(negative)+len(checks)},indent=2,sort_keys=True)+'\n')
for path,h in pins.items():assert sha(path)==h,(path,'changed during check')
result={'status':'PASS: exact bounded H=0 continuation','candidate':str(AUTHOR/'CERTIFICATE.json'),'candidate_sha256':pins[str(AUTHOR/'CERTIFICATE.json')],'source_files_pinned':len(pins),'source_polynomials_verified':len(refs),'source_terms_verified':source_terms,'equations_retained':50,'guards_retained':19,'polynomial_b_degree':2,'E41_remainder_degrees':{'e':2,'c':3,'q':2},'E41_remainder_terms':33,'exact_identity_count':len(checks),'negative_controls_rejected':len(checks)+len(negative),'distinct_coeff_products_double_checked':coeff_products,'total_sparse_term_products':pair_count,'peak_polynomial_terms':max_terms,'new_optional_zero_exclusions':[],'new_division_by_parameter':False,'algebraic_roots_discarded':False,'dimension_claimed':False,'full_feasibility_claimed':False,'historical_program_execution':False,'method':'Fresh standard-library integer-vector rational cyclotomic sparse arithmetic; every coefficient product cross-checked by descending Phi11 reduction and cyclic convolution; inert certificates only.'}
(OUT/'EXACT_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n')
(OUT/'ARITHMETIC_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2),flush=True)
