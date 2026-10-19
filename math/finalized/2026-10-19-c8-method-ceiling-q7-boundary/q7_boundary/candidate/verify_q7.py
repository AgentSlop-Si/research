#!/usr/bin/env python3
"""Exact standard-library corroboration of REPORT.md; not a square-mask census."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

BASE=Path(__file__).resolve().parent
N=35

def write(name,obj):
    (BASE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def family_data(ss):
    union=0; common=31
    for s in ss: union|=s; common&=s
    mult=[sum((s>>u)&1 for s in ss) for u in range(5)]
    return union.bit_count(),sum(s.bit_count() for s in ss),common,mult

# All repeated restrictions are allowed. Nonstar rank reduces the remaining n>5
# possibilities symbolically to stars; no hidden distinct-row assumption is used.
types={1:[(k,k) for k in range(6)]}
local_counts={}
nonstar_expected={(3,3,6),(3,4,7),(3,5,8),(4,4,9),(4,5,10),(5,5,12)}
nonstar_seen=set()
scanned=valid=0
for n in range(2,6):
    tt=set(); count=nonstars=0
    for ss in combinations_with_replacement(range(1,32),n):
        scanned+=1
        if any((a&b).bit_count()!=1 for a,b in combinations(ss,2)):continue
        valid+=1;count+=1
        k,I,common,mult=family_data(ss)
        tt.add((k,I))
        if common:
            assert common.bit_count()==1 and I==n+k-1
            assert sum(m>=4 for m in mult)<=1
        else:
            nonstars+=1
            assert min(s.bit_count() for s in ss)>=2
            assert n<=k<=5
            assert (n,k,I) in nonstar_expected
            nonstar_seen.add((n,k,I))
            assert sum(m>=4 for m in mult)<=1
    types[n]=sorted(tt)
    local_counts[n]={'valid_multisets':count,'nonstars':nonstars,'types':types[n]}
assert nonstar_seen==nonstar_expected
for n in [6,7]:types[n]=[(k,n+k-1) for k in range(1,6)]
write('LOCAL_FAMILIES.json',{'scanned_multisets':scanned,'valid_multisets':valid,
                           'by_component_size':local_counts,
                           'rank_reduction_for_sizes_6_7':'symbolic, REPORT section 2'})

expected_max={
 (7,):11,(1,6):10,(2,5):10,(3,4):12,(1,1,5):12,(1,2,4):11,
 (1,3,3):10,(2,2,3):10,(1,1,1,4):10,(1,1,2,3):9,(1,2,2,2):8}
partition_results=[]
for part,maximum in expected_max.items():
    pats=sorted(set(tuple(p[1] for p in pp) for pp in product(*(types[n] for n in part))
                    if sum(p[0] for p in pp)<=5))
    assert max(map(sum,pats))==maximum
    if part==(3,4):assert all(p==(3,9) for p in pats if sum(p)==12)
    if part==(1,1,5):
        assert all(p==(0,0,12) for p in pats if sum(p)==12)
        assert all(7*(p[0]+p[1])+4*p[2]<=48 for p in pats)
        assert 34*10>7*48
    if part==(1,2,4):assert all(p==(0,2,9) for p in pats if sum(p)==11)
    partition_results.append({'partition':part,'max_fiber_incidence':maximum,
                              'component_incidence_vectors':pats,
                              'maximizers':[p for p in pats if sum(p)==maximum]})
write('PARTITION_CERTIFICATES.json',partition_results)

# Exact local baseline checks, retaining each local support as a 5-bit mask.
def partitions(n,lo=1):
    if n==0:yield ()
    for k in range(lo,n+1):
        for p in partitions(n-k,k):yield (k,)+p

def baseline_patterns(labels):
    choices=[[m for m in range(1,32) if m>>l&1] for l in labels]
    comps=[0]*3+[1]*4
    out=[]
    def rec(ss):
        j=len(ss)
        if j==7:out.append(tuple(ss));return
        for m in choices[j]:
            if all((m&s).bit_count()==int(comps[i]==comps[j]) for i,s in enumerate(ss)):
                rec(ss+[m])
    rec([])
    return out

baseline_results=[]
for aa in partitions(3):
    for bb in partitions(4):
        if len(aa)+len(bb)>5:continue
        labels=[]
        for i,n in enumerate(aa+bb):labels.extend([i]*n)
        pp=baseline_patterns(labels)
        if not pp: cert={'kind':'no_local_pattern'}
        else:
            cert=None
            for start,end in [(0,3),(3,7)]:
                ll=labels[start:end];freq=Counter(ll);n=end-start
                if len(freq)==1:continue
                repeated=next((l for l,k in freq.items() if k>=2),None)
                if repeated is not None:
                    outside=next(i for i in range(start,end) if labels[i]!=repeated)
                    assert all(p[outside].bit_count()>=2 for p in pp)
                    cert={'kind':'fixed_row_at_least_two_per_fiber','row':outside,
                          'minimum_degree':14,'repeated_label':repeated}
                else:
                    assert all(sum(p[i].bit_count() for i in range(start,end))>=2*n-1 for p in pp)
                    assert n*11<7*(2*n-1)
                    cert={'kind':'component_incidence_lower_bound','row_range':[start,end],
                          'required_at_degree_11':n*11,'lower_bound':7*(2*n-1)}
                break
            if cert is None:
                assert all(sum(m.bit_count() for m in p)<=10 for p in pp)
                cert={'kind':'two_stars_upper_bound','max_fiber_incidence':10,
                      'required_average_incidence':11}
        baseline_results.append({'class_sizes_3':aa,'class_sizes_4':bb,'labels':labels,
                                 'local_pattern_count':len(pp),'certificate':cert,
                                 'local_patterns':pp})
assert len(baseline_results)==12
write('SPLIT_LINE_CERTIFICATES.json',baseline_results)

# Phi_35=Phi_5(x^7)/Phi_5(x), exact monic division, low-to-high coefficients.
num=[0]*29
for i in range(5):num[7*i]=1
den=[1]*5
rem=num[:];phi=[0]*25
for k in range(24,-1,-1):
    c=rem[k+4];phi[k]=c
    for j in range(5):rem[k+j]-=c*den[j]
assert not any(rem) and phi[-1]==1

def reduce_poly(p):
    p=p[:]
    if len(p)<25:p +=[0]*(25-len(p))
    for k in range(len(p)-1,23,-1):
        z=p[k]
        if z:
            for j,c in enumerate(phi):p[k-24+j]-=z*c
    return p[:24]

powers=[]
for e in range(35):
    p=[0]*(e+1);p[e]=1;powers.append(reduce_poly(p))
zero=[0]*24

def residue(exponents):
    out=[0]*24
    for e in exponents:
        for j,c in enumerate(powers[e%35]):out[j]+=c
    return out

def grams(R,row_ids=None):
    if row_ids is None:row_ids=list(range(len(R)))
    rr=[]
    for i,r in enumerate(row_ids):
        row=[]
        for j,s in enumerate(row_ids):
            row.append(residue((r-s)*c for c in range(35) if R[i][c] and R[j][c]))
        rr.append(row)
    cc=None
    if len(R)==35:
        cc=[]
        for c in range(35):
            row=[]
            for e in range(35):
                row.append(residue(r*(e-c) for r in range(35) if R[r][c] and R[r][e]))
            cc.append(row)
    return rr,cc

def audit_control(name,R,d,positive):
    assert all(sum(row)==d for row in R)
    assert all(sum(R[r][c] for r in range(35))==d for c in range(35))
    gg=grams(R);orders={};failures={}
    for side,G in zip(['row','column'],gg):
        count=Counter();ff=[]
        for i in range(35):
            for j in range(35):
                want=[d]+[0]*23 if i==j else zero
                good=G[i][j]==want
                if i==j:order=1
                elif (i-j)%5==0:order=7
                elif (i-j)%7==0:order=5
                else:order=35
                count[str(order)+('_pass' if good else '_fail')]+=1
                if not good:ff.append({'i':i,'j':j,'residue':G[i][j]})
        if positive:assert not ff
        else:assert ff
        orders[side]=dict(count);failures[side]=ff
    return {'name':name,'degree':d,'positive':positive,'mask':R,
            'gram_counts_by_character_order':orders,'all_failures':failures}

crt_checks=0
for a,b,u,v in product(range(5),range(7),range(5),range(7)):
    r=(21*a+15*b)%35;c=(21*u+15*v)%35
    assert (r*c-21*a*u-15*b*v)%35==0
    crt_checks+=1
controls=[]
for d in [1,5,7,35]:
    if d==1:R=[[int(r==c) for c in range(35)] for r in range(35)]
    elif d==5:R=[[int(r%7==c%7) for c in range(35)] for r in range(35)]
    elif d==7:R=[[int(r%5==c%5) for c in range(35)] for r in range(35)]
    else:R=[[1]*35 for _ in range(35)]
    controls.append(audit_control('divisor_'+str(d),R,d,True))
R=[[int(r%5==c%5 or r%7==c%7) for c in range(35)] for r in range(35)]
controls.append(audit_control('cross_shape_11',R,11,False))
for t in [1,2,3]:
    R=[]
    for r in range(35):
        a,b=r%5,r%7;base=a if b else (a+1)%5
        R.append([int(c%5==base or (c%7==b and c%5 in [(a+j)%5 for j in range(2,t+2)])) for c in range(35)])
    controls.append(audit_control('all_split_'+str(7+t),R,7+t,False))
write('ORIGINAL_PHASE_CONTROLS.json',{'cyclotomic_polynomial':phi,'crt_checks':crt_checks,
                                    'full_square_gram_entries':len(controls)*2*35*35,'controls':controls})

block=json.loads((BASE/'sources'/'Q7_ROW_GROUP_COUNTERCONTROL.json').read_text())
R=block['R_block'];row_ids=block['row_indices']
assert row_ids==[0,15,30,10,25,5,20]
assert all(sum(row)==11 for row in R)
G,_=grams(R,row_ids)
for i,j in product(range(7),repeat=2):assert G[i][j]==([11]+[0]*23 if i==j else zero)
row_details=[]
for i,r in enumerate(row_ids):
    lines=[u for u in range(5) if all(R[i][c] for c in range(35) if c%5==u)]
    fibers=[v for v in range(7) if all(R[i][c] for c in range(35) if c%7==v)]
    row_details.append({'row':r,'full_lines':lines,'full_fibers':fibers})
assert not row_details[0]['full_lines'] and not row_details[0]['full_fibers']
assert R[0][5]==1
m=sum(row[5] for row in R)
assert m==2 and m+4==6<11
write('RECTANGULAR_EXTENSION_OBSTRUCTION.json',{'row_indices':row_ids,'row_details':row_details,
       'all_49_original_row_gram_residues':G,'certificate':{'row':0,'supported_column':5,
       'own_group_column_multiplicity':m,'max_other_groups_contribution':4,
       'max_square_column_degree':m+4,'required_degree':11}})

bindings=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())
for entry in bindings:
    assert digest(BASE/entry['frozen_path'])==entry['sha256']
    assert digest(Path(entry['original_path']))==entry['sha256']
results={'status':'PASS','theorem_degrees':[8,9,10,11,12,13],
         'scope':'Exact finite controls corroborate the symbolic theorem; no square-mask census.',
         'local_multisets_scanned':scanned,'local_multisets_valid':valid,
         'component_partitions_checked':len(partition_results),
         'split_baseline_cases_checked':len(baseline_results),
         'split_local_patterns_checked':sum(x['local_pattern_count'] for x in baseline_results),
         'original_crt_congruences_checked':crt_checks,
         'complete_square_gram_entries_checked':len(controls)*2*35*35,
         'rectangular_gram_entries_checked':49,
         'source_bindings_verified':len(bindings),
         'external_actions':[],'floating_arithmetic_used':False}
write('RESULTS.json',results)
print(json.dumps(results,indent=2))
