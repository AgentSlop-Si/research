#!/usr/bin/env python3
"""Fresh exact auditor. Never imports or executes another research program.
Input files are JSON data only; all polynomial and field operations are local.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd, comb
from copy import deepcopy
import hashlib, json, time

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
AUTHOR=ROOT/'research_cycle_1825/guarded_consequences'
PARENT=ROOT/'research_cycle_1805/guarded_fourier_reduction'
PRIOR=ROOT/'research_cycle_1819/guarded_reduction_review/RECEIPT.json'
PRIOR_SHA='51f6adcf4c160cc5b83ae44d99f77544067f91ec915db1fcc234ae83d4f48c39'
FROZEN_AUTHOR={
 'CONSEQUENCE_CERTIFICATE.json':'44ace9f92adb7784f862705c29974fe4eb3faadf6ab38131934da950cf636a2b',
 'REPORT.md':'1cc0969a6b5003a9ca5502d6e8b09d30ea1ee58a216eaaa63f8a58ae4b3f4a82',
 'CHECK_RECEIPT.json':'e0397f7f174e87134e53778b272a83fd4ab843db5fdebb5b77ff6aecaf2ddc94',
 'REVIEW_ENTRY.json':'9e691093a9cd9ff23218d5f44b107e4cc2d1d16ea5589185fda2fb9736674a22',
 'SHA256SUMS.txt':'fbe86931affc82934fb485463a31bfa6beaabd5d076dddbbffd9564c3aafd62f'}
V=[0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92]
I={v:i for i,v in enumerate(V)}
E=(0,)*16
ZERO=(Q(0),)*10
ONE=(Q(1),)+(Q(0),)*9
Z=(Q(0),Q(1))+(Q(0),)*8

class Invalid(Exception): pass
def need(condition,message):
    if not condition: raise Invalid(message)
def digest(b): return hashlib.sha256(b).hexdigest()
def sha(p): return digest(Path(p).read_bytes())
def load(p): return json.loads(Path(p).read_text())
def packed(x): return json.dumps(x,separators=(',',':')).encode()
def fadd(a,b): return tuple(x+y for x,y in zip(a,b))
def fneg(a): return tuple(-x for x in a)
@lru_cache(maxsize=50000)
def fmul(a,b):
    # Direct convolution and reduction by z^10+...+z+1.
    r=[Q(0)]*19
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: r[i+j]+=x*y
    for k in range(18,9,-1):
        t=r[k]
        if t:
            for j in range(k-10,k): r[j]-=t
    return tuple(r[:10])
def fpow(a,n):
    result=ONE
    while n:
        if n&1: result=fmul(result,a)
        a=fmul(a,a); n//=2
    return result
def fc(pair):
    a,d=pair
    need(len(a)==10 and type(d) is int and d>0 and all(type(t) is int for t in a),'field serialization')
    return tuple(Q(t,d) for t in a)
def cp(c): return {} if c==ZERO else {E:c}
def xp(v):
    e=list(E); e[I[v]]=1
    return {tuple(e):ONE}
def padd(a,b):
    result=dict(a)
    for e,c in b.items():
        v=fadd(result.get(e,ZERO),c)
        if v==ZERO: result.pop(e,None)
        else: result[e]=v
    return result
def pneg(a): return {e:fneg(c) for e,c in a.items()}
def pmul(a,b):
    result={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f))
            h=fadd(result.get(g,ZERO),fmul(c,d))
            if h==ZERO: result.pop(g,None)
            else: result[g]=h
    return result
def support(p): return {V[i] for e in p for i,n in enumerate(e) if n}
def raw_support(raw): return {V[i] for e,a,d in raw for i,n in enumerate(e) if n}
def poly(raw): return {tuple(e):tuple(Q(x,d) for x in a) for e,a,d in raw}
def validate_raw(key,raw):
    need(digest(packed(raw))==key,'polynomial content address')
    last=None
    for term in raw:
        need(isinstance(term,list) and len(term)==3,'term format')
        e,a,d=term
        need(len(e)==16 and all(type(x) is int and x>=0 for x in e),'monomial format')
        need(last is None or tuple(e)>last,'strict monomial ordering')
        last=tuple(e)
        fc([a,d]); need(any(a),'stored zero coefficient')
        need(gcd(d,*a)==1,'noncanonical coefficient fraction')

def validate_certificate(c,parent,old):
    need(c['variables']==V==parent['variables']==old['variables'],'coordinate basis')
    need(c['coefficient_basis']==parent['coefficient_basis']==old['coefficient_basis'],'coefficient basis')
    need(c['source_hashes']==EXPECTED_SOURCES,'source hashes')
    need(c['inherited_polynomial_sources']==[str(PARENT.relative_to(ROOT)/'CERTIFICATE.json'),str(PARENT.relative_to(ROOT)/'COMPACT_BRANCH.json')],'inherited data sources')
    need(c['new_eliminations']==[22,88,52],'new pivot selection')
    need(c['definitions'][3:]==old['definitions'],'inherited definitions preserved')
    need(c['reconstruction_order']==[d['variable'] for d in c['definitions']],'declared reconstruction order')
    need(c['reconstruction_order']==[22,88,52,39,44,55],'acyclic recorded order')
    need(c['free_variables']==[v for v in old['free_variables'] if v not in [22,88,52]],'free-coordinate partition')
    need(len(c['free_variables'])==9,'nine free coordinates')
    need(set(c['free_variables'])|set(c['reconstruction_order'])==set(V)-{91},'complete fifteen-coordinate reconstruction')
    need(not(set(c['free_variables'])&set(c['reconstruction_order'])),'disjoint reconstruction')
    rawpool=dict(BASE_POOL)
    for h,r in c['polynomials'].items():
        validate_raw(h,r)
        need(h not in rawpool or rawpool[h]==r,'content-address collision')
        rawpool[h]=r
    @lru_cache(None)
    def p(h):
        need(h in rawpool,'missing polynomial reference')
        return poly(rawpool[h])
    known=set(c['free_variables']); removed=[]; checks=[]
    expected_n={22:cp(Z),88:cp(fneg(fpow(Z,10))),52:pmul(cp(fneg(fpow(Z,4))),xp(83))}
    expected_sources={22:'58',88:'36',52:'4'}
    # Encode the report's two grouped denominator formulas independently.
    def add(*args):
        r={}
        for t in args: r=padd(r,t)
        return r
    def mul(*args):
        r=cp(ONE)
        for t in args: r=pmul(r,t)
        return r
    def z(k): return cp(fpow(Z,k))
    a=mul(xp(11),xp(34)); w=mul(xp(0),xp(65))
    D88=add(pneg(z(7)),mul(xp(41),add(z(1),pneg(z(10)),mul(a,add(z(7),pneg(z(9)),mul(add(z(2),pneg(cp(ONE))),xp(83)))),mul(w,add(z(10),mul(a,add(xp(83),pneg(z(7)))))))))
    D52=add(pneg(xp(83)),mul(w,add(pneg(z(7)),mul(z(6),xp(83)))),mul(xp(0),xp(49),add(z(3),mul(add(z(5),pneg(z(2))),xp(83)),mul(xp(25),add(pneg(z(2)),mul(z(1),xp(83)))),mul(add(pneg(z(8)),mul(z(7),xp(83))),xp(88),add(cp(ONE),pneg(xp(92)),pneg(w))))))
    expected_d={22:add(xp(34),xp(49)),88:D88,52:D52}
    for d in c['definitions']:
        v=d['variable']; source=d['source_equation']; removed.append(source)
        need(d['source']==parent['final']['equations'][source],'source equation reference')
        need(d['source_label']==parent['initial']['labels'][source],'source equation label')
        if v in expected_sources:
            need(source==expected_sources[v] and source in old['equations'],'new pivot from retained predecessor residual')
        n=p(d['numerator']); den=p(d['denominator']); src=p(d['source'])
        deps=support(n)|support(den)
        need(sorted(deps)==d['dependencies'],'complete dependencies')
        need(deps<=known,'dependency not previously reconstructed')
        need(v not in deps,'self-dependent pivot')
        need(src==padd(pmul(xp(v),den),pneg(n)),'exact source = variable*denominator-numerator')
        nz=d['denominator_nonzero']
        if v in expected_n:
            need(n==expected_n[v],'claimed forced numerator')
            need(nz['method']=='forced by source equation and nonzero numerator','forced denominator method')
            need(nz['identity']=='source = variable * denominator - numerator','forced denominator identity')
            nn=nz['numerator_nonzero']; constant=fc(nn['constant'])
            need(constant!=ZERO,'nonzero numerator scalar')
            product=cp(constant)
            for g in nn['guard_factors']:
                need(g in old['guards'],'numerator uses original guard')
                need(g in c['guards'] and c['guards'][g]==old['guards'][g],'numerator guard retained')
                factor=p(old['guards'][g]); need(support(factor)<=known,'acyclic numerator proof')
                product=pmul(product,factor)
            need(product==n,'exact numerator nonzero-factor certificate')
            need(d['retained_denominator_guard']=='D'+str(v),'derived denominator guard name')
            need(c['guards'].get('D'+str(v))==d['denominator'],'derived denominator guard retained')
            need(den==expected_d[v],'grouped D'+str(v)+' exact formula')
            mode='forced by source equation and nonzero numerator'
        else:
            constant=fc(nz['constant']); need(constant!=ZERO,'nonzero inherited pivot scalar')
            product=cp(constant)
            for g in nz['guard_factors']:
                need(g in old['guards'] and c['guards'].get(g)==old['guards'][g],'inherited denominator original guard retained')
                factor=p(old['guards'][g]); need(support(factor)<=known,'acyclic inherited guard proof')
                product=pmul(product,factor)
            need(product==den,'exact inherited denominator guard-product identity')
            mode='product of available retained guards and nonzero field constant'
        known.add(v)
        checks.append({'variable':v,'source_equation':source,'source_label':d['source_label'],'dependencies':sorted(deps),'numerator_terms':len(n),'denominator_terms':len(den),'nonzero_proof':mode})
    need(len(set(removed))==6,'distinct source removals')
    need(c['equations']=={k:h for k,h in old['equations'].items() if k not in ['58','36','4']},'complete residual reference dictionary')
    need(c['equations']=={k:h for k,h in parent['final']['equations'].items() if k not in removed},'complete fifteen-coordinate source partition')
    guards=dict(old['guards']); guards.update({'D'+str(d['variable']):d['denominator'] for d in c['definitions'][:3]})
    need(c['guards']==guards,'all fourteen original guards plus exactly three derived guards')
    need(c['equation_count']==len(c['equations'])==52,'residual equation count')
    need(c['guard_count']==len(c['guards'])==17 and c['original_guard_count']==len(old['guards'])==14,'guard counts')
    for h in list(c['equations'].values())+list(c['guards'].values()):
        need(h in rawpool,'residual/guard reference defined')
        need(raw_support(rawpool[h])<=known,'residual/guard evaluation dependency')
    need(poly(rawpool[old['guards']['x83']])==xp(83),'original x83 guard is exact coordinate')
    need(c['factorization_claimed'] is False and c['contradiction_claimed'] is False,'bounded claim flags')
    # Inherited x91 restoration is a field-unit solve after all fifteen coordinates.
    d=parent['events'][0]
    need(d['kind']=='linear_elimination' and d['variable']==91,'inherited x91 reconstruction record')
    n=p(d['numerator']); den=p(d['denominator']); src=p(d['source'])
    need(support(n)<=known and not support(den),'x91 final reconstruction dependencies')
    need(den==cp(fadd(fpow(Z,7),fneg(fpow(Z,6)))) and den,'x91 nonzero field denominator')
    need(src==padd(pmul(xp(91),den),pneg(n)),'x91 source identity')
    return {'pivots':checks,'free_variables':c['free_variables'],'residual_equations':52,'original_guards':14,'derived_guards':3,'total_guards':17,'x91_reconstruction_rechecked':True,'unique_polynomials':len(rawpool)}

def mutate_polynomial(c,which):
    d=c['definitions'][0]; old=d[which]; raw=deepcopy(c['polynomials'][old])
    raw[0][1][0]+=1
    new=digest(packed(raw)); c['polynomials'][new]=raw; d[which]=new
    if which=='denominator': c['guards']['D22']=new

def controls(c,parent,old):
    cases=[]
    def case(name,change,match):
        m=deepcopy(c); change(m)
        try: validate_certificate(m,parent,old)
        except Invalid as err:
            need(match in str(err),'mutation rejected for unexpected reason: '+name+' / '+str(err))
            cases.append({'name':name,'result':'REJECTED','reason':str(err),'hash_pin_bypassed_to_exercise_semantic_check':True})
        else: raise Invalid('mutation escaped: '+name)
    case('rehashed numerator coefficient altered',lambda m:mutate_polynomial(m,'numerator'),'exact source')
    case('rehashed denominator coefficient altered',lambda m:mutate_polynomial(m,'denominator'),'exact source')
    case('nonzero numerator guard factor omitted',lambda m:m['definitions'][2]['denominator_nonzero']['numerator_nonzero'].update(guard_factors=[]),'exact numerator nonzero-factor')
    case('nonzero numerator scalar set to zero',lambda m:m['definitions'][1]['denominator_nonzero']['numerator_nonzero'].update(constant=[[0]*10,1]),'nonzero numerator scalar')
    case('required x83 original guard dropped',lambda m:m['guards'].pop('x83'),'numerator guard retained')
    case('derived D88 guard dropped',lambda m:m['guards'].pop('D88'),'derived denominator guard retained')
    case('derived D52 points to D22',lambda m:m['guards'].update(D52=m['guards']['D22']),'derived denominator guard retained')
    case('source label changed',lambda m:m['definitions'][0].update(source_label=['entry',10,9]),'source equation label')
    case('source reference changed',lambda m:m['definitions'][0].update(source=m['definitions'][1]['source']),'source equation reference')
    case('dependency x88 suppressed for x52',lambda m:m['definitions'][2].update(dependencies=[0,25,49,65,83,92]),'complete dependencies')
    case('x52 placed before x88',lambda m:(m['definitions'].__setitem__(slice(1,3),list(reversed(m['definitions'][1:3]))),m.update(reconstruction_order=[22,52,88,39,44,55])),'acyclic recorded order')
    case('one residual dropped',lambda m:m['equations'].pop('1'),'complete residual reference dictionary')
    case('one residual replaced',lambda m:m['equations'].update({'1':m['equations']['3']}),'complete residual reference dictionary')
    case('additional original g98 guard dropped',lambda m:m['guards'].pop('g98'),'all fourteen original guards')
    case('free-coordinate list incomplete',lambda m:m['free_variables'].remove(83),'free-coordinate partition')
    case('inherited pivot numerator replaced',lambda m:m['definitions'][3].update(numerator=m['definitions'][0]['numerator']),'inherited definitions preserved')
    case('source hash claim changed',lambda m:m['source_hashes'].update({next(iter(m['source_hashes'])):'0'*64}),'source hashes')
    def bad_raw(m): next(iter(m['polynomials'].values()))[0][1][0]+=1
    case('unrehashed content tampered',bad_raw,'polynomial content address')
    return cases

if __name__=='__main__':
    start=time.monotonic(); hashes={}
    for name,h in FROZEN_AUTHOR.items(): need(sha(AUTHOR/name)==h,'author freeze pin '+name)
    need(sha(PRIOR)==PRIOR_SHA,'accepted predecessor receipt pin')
    prior=load(PRIOR)
    for path,h in prior['source_hashes'].items():
        need(sha(ROOT/path)==h,'accepted source file hash: '+path); hashes[path]=h
    EXPECTED_SOURCES={str((PARENT/'CERTIFICATE.json').relative_to(ROOT)):sha(PARENT/'CERTIFICATE.json'),str((PARENT/'COMPACT_BRANCH.json').relative_to(ROOT)):sha(PARENT/'COMPACT_BRANCH.json'),str(PRIOR.relative_to(ROOT)):PRIOR_SHA}
    hashes.update(EXPECTED_SOURCES)
    parent=load(PARENT/'CERTIFICATE.json'); old=load(PARENT/'COMPACT_BRANCH.json'); c=load(AUTHOR/'CONSEQUENCE_CERTIFICATE.json')
    need(old['parent_certificate_sha256']==EXPECTED_SOURCES[str((PARENT/'CERTIFICATE.json').relative_to(ROOT))],'accepted compact parent hash')
    need(prior['compact']['free_variables']==old['free_variables'] and prior['compact']['equations']==len(old['equations']) and prior['compact']['guards']==len(old['guards']),'accepted receipt endpoint binding')
    need(old['guards']==parent['final']['guards'],'accepted inherited guards')
    BASE_POOL={}; total_terms=0
    for obj in [parent,old]:
        for h,r in obj['polynomials'].items():
            validate_raw(h,r)
            need(h not in BASE_POOL or BASE_POOL[h]==r,'inherited content collision')
            if h not in BASE_POOL: total_terms+=len(r)
            BASE_POOL[h]=r
    need(fpow(Z,11)==ONE and fadd(ONE,tuple(sum(fpow(Z,k)[i] for k in range(1,11)) for i in range(10)))==ZERO,'cyclotomic arithmetic self-test')
    need(all(comb(11,k)%11==0 for k in range(1,11)) and comb(11,1)%121!=0,'Phi11(z+1) Eisenstein certificate')
    result=validate_certificate(c,parent,old)
    result['mutation_controls']=controls(c,parent,old)
    # Frozen author entry is required for final review, not inferred from a live draft.
    entry=load(AUTHOR/'REVIEW_ENTRY.json')
    need(entry['free_variables']==c['free_variables'] and entry['residual_equations']==52 and entry['retained_original_guards']==14 and entry['total_guards']==17,'frozen entry endpoint claims')
    need(entry['new_mandatory_coordinate']==22,'frozen entry x22 nonzero claim')
    for item in entry['files']:
        path=item['path']; h=item['sha256']; p=ROOT/path
        need(p.exists() and sha(p)==h and p.stat().st_size==item['bytes'],'frozen author manifest file '+path)
        hashes[path]=h
    manifest_paths=set()
    for line in (AUTHOR/'SHA256SUMS.txt').read_text().splitlines():
        h,name=line.split('  ',1)
        need('/' not in name and sha(AUTHOR/name)==h,'frozen author SHA256SUMS '+name)
        manifest_paths.add(name)
        hashes[str((AUTHOR/name).relative_to(ROOT))]=h
    need(manifest_paths=={Path(d['path']).name for d in entry['files']}|{'REVIEW_ENTRY.json'},'author manifest coverage')
    # Verify author receipt metadata; do not treat author PASS as independent proof.
    ar=load(AUTHOR/'CHECK_RECEIPT.json')
    need(ar['certificate_sha256']==sha(AUTHOR/'CONSEQUENCE_CERTIFICATE.json'),'author receipt certificate binding')
    need(ar['checker_sha256']==sha(AUTHOR/'check_consequence.py'),'author receipt checker binding')
    need(ar['source_hashes']==EXPECTED_SOURCES,'author receipt source binding')
    for path in AUTHOR.iterdir():
        if path.is_file(): hashes[str(path.relative_to(ROOT))]=sha(path)
    for path,h in hashes.items(): need(sha(ROOT/path)==h,'final frozen-source recheck '+path)
    receipt={'status':'PASS: independent exact guarded 12-to-9 circuit equivalence; no factorization or impossibility conclusion','accepted_predecessor_receipt_sha256':PRIOR_SHA,'author_entry_sha256':sha(AUTHOR/'REVIEW_ENTRY.json'),'certificate_sha256':sha(AUTHOR/'CONSEQUENCE_CERTIFICATE.json'),'method':'Fresh standard-library exact cyclotomic polynomial checker; no author or inherited program executed or imported','coefficient_field':'Q[zeta]/(1+zeta+...+zeta^10)','inherited_pool_polynomials':len(BASE_POOL),'inherited_pool_terms':total_terms,**result,'source_hashes':hashes,'checker_sha256':sha(__file__),'runtime_seconds':round(time.monotonic()-start,6),'scope':'Bijection with the accepted guarded necessary circuit checkpoint, not a sufficiency theorem for original Fourier factorization. Counts denote stored constraints, not algebraic independence. No full nine-variable residual expansion or new search was attempted.'}
    (OUT/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    (OUT/'MUTATION_CONTROLS.json').write_text(json.dumps(result['mutation_controls'],indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['source_hashes','mutation_controls']},indent=2))
