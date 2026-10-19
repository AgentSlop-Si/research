#!/usr/bin/env python3
"""Independent integer CRT-basis corroboration, not an exhaustive mask search."""
from pathlib import Path
from itertools import product, combinations
from collections import Counter
import hashlib,json
B=Path(__file__).resolve().parent
C=Path('/workspace/shared/fiveprime_q7_boundary_20261019_1430')
def dump(p,o): (B/p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def families(n):
    if n==1:
        yield from ((m,) for m in range(32));return
    def rec(prefix,lo):
        if len(prefix)==n:
            yield tuple(prefix);return
        for m in range(lo,32):
            if all((m&s).bit_count()==1 for s in prefix):
                yield from rec(prefix+[m],m)
    yield from rec([],1)
types={}; nonstars=set(); local={}
for n in range(1,8):
    tt=set(); count=ns=0
    for ff in families(n):
        count+=1;union=0;common=31
        for s in ff:union|=s;common&=s
        k=union.bit_count();inc=sum(s.bit_count() for s in ff)
        tt.add((k,inc))
        if n>1 and not common:
            ns+=1;nonstars.add((n,k,inc));assert n<=k<=5
        if n>1 and common:assert inc==n+k-1
        assert sum(sum(bool(s&(1<<j)) for s in ff)>=4 for j in range(5))<=1
    types[n]=sorted(tt);local[n]={'families':count,'nonstars':ns,'types':types[n]}
assert nonstars=={(3,3,6),(3,4,7),(3,5,8),(4,4,9),(4,5,10),(5,5,12)}
def partitions(n,lo=1):
    if n==0:yield ();return
    for x in range(lo,n+1):
        for rest in partitions(n-x,x):yield (x,)+rest
partitions_data=[]
for p in partitions(7):
    if len(p)>4:continue
    feasible=[z for z in product(*(types[n] for n in p)) if sum(k for k,i in z)<=5]
    maximum=max(sum(i for k,i in z) for z in feasible)
    extremizers=sorted(set(tuple(i for k,i in z) for z in feasible if sum(i for k,i in z)==maximum))
    if p==(1,1,5):assert max(7*(z[0][1]+z[1][1])+4*z[2][1] for z in feasible)==48
    partitions_data.append({'partition':p,'max':maximum,'extremizing_incidences':extremizers})
actual={tuple(x['partition']):x['max'] for x in partitions_data}
assert actual=={(7,):11,(1,6):10,(2,5):10,(3,4):12,(1,1,5):12,(1,2,4):11,(1,3,3):10,(2,2,3):10,(1,1,1,4):10,(1,1,2,3):9,(1,2,2,2):8}
dump('LOCAL_CONTROLS.json',{'families':local,'partitions':partitions_data,'exhaustively_checked_component_sizes':list(range(1,8))})

# zeta=alpha*beta with alpha=zeta^21, beta=zeta^15. Each alpha^4
# and beta^6 is reduced using its own prime cyclotomic relation.
def prime_basis(e,p):
    e%=p
    return [-1]*(p-1) if e==p-1 else [int(i==e) for i in range(p-1)]
def tensor_power(e):return tuple(x*y for x in prime_basis(e,5) for y in prime_basis(e,7))
P=[tensor_power(e) for e in range(35)];Z=(0,)*24

def residue(exponents):
    hist=Counter(e%35 for e in exponents)
    return tuple(sum(v*P[e][j] for e,v in hist.items()) for j in range(24))
def grams(R,ids=None):
    ids=list(range(len(R))) if ids is None else ids
    row=[[residue((ids[i]-ids[j])*c for c in range(35) if R[i][c] and R[j][c]) for j in range(len(R))] for i in range(len(R))]
    col=[[residue(ids[r]*(e-c) for r in range(len(R)) if R[r][c] and R[r][e]) for e in range(35)] for c in range(35)]
    return row,col

def classify(G,d):
    failures=[];orders=Counter()
    for i,row in enumerate(G):
        for j,v in enumerate(row):
            expected=(d,)+(0,)*23 if i==j else Z
            good=v==expected
            o=1 if i==j else 7 if (i-j)%5==0 else 5 if (i-j)%7==0 else 35
            orders[str(o)+('_pass' if good else '_fail')]+=1
            if not good:failures.append({'i':i,'j':j,'residue':v})
    return {'counts':dict(orders),'failures':failures}

crt=0
for a,b,u,v in product(range(5),range(7),range(5),range(7)):
    r=(21*a+15*b)%35;c=(21*u+15*v)%35
    assert (r*c-21*a*u-15*b*v)%35==0;crt+=1

fresh=[]
for d in [1,5,7,35]+list(range(8,14)):
    pos=d in [1,5,7,35]
    R=[[int((r-c)%(35//d)==0) if pos else int((c-r)%35<d) for c in range(35)] for r in range(35)]
    assert set(map(sum,R))=={d};assert {sum(R[r][c] for r in range(35)) for c in range(35)}=={d}
    gg=grams(R);summaries=[]
    for G in gg:
        s=classify(G,d);assert (not s['failures'])==pos
        summaries.append({'counts':s['counts'],'first_failure':s['failures'][:1]})
    fresh.append({'name':('divisor_' if pos else 'fresh_cyclic_')+str(d),'degree':d,'positive':pos,'row':summaries[0],'column':summaries[1]})

# Re-evaluate the author's masks, without calling/importing their checker.
submitted=json.loads((C/'ORIGINAL_PHASE_CONTROLS.json').read_text())
submitted_checks=[]
for control in submitted['controls']:
    R=control['mask'];d=control['degree'];gg=grams(R)
    for side,G in zip(['row','column'],gg):
        s=classify(G,d)
        assert s['counts']==control['gram_counts_by_character_order'][side]
        bypair={(x['i'],x['j']):tuple(x['residue']) for x in s['failures']}
        assert len(bypair)==len(control['all_failures'][side])
        for f in control['all_failures'][side]:
            converted=tuple(sum(coeff*P[e][j] for e,coeff in enumerate(f['residue'])) for j in range(24))
            assert converted==bypair[(f['i'],f['j'])]
    submitted_checks.append({'name':control['name'],'row_and_column_recomputed':True})

units=[k for k in range(35) if k%5 and k%7]
zero_sets=set()
for m in range(1<<7):zero_sets.add(tuple(c for c in range(35) if m&(1<<(c%7))))
for m in range(1<<5):zero_sets.add(tuple(c for c in range(35) if m&(1<<(c%5))))
assert len(zero_sets)==158
for h in units:
    for S in zero_sets:assert residue(h*c for c in S)==Z
    for c in range(35):assert residue([h*c])!=Z
# Nonprimitive characters: constant counts cancel; one count imbalance does not.
for p,mult in [(5,7),(7,5)]:
    for k in range(1,p):
        for t in range(1,6):
            assert residue(mult*k*j for j in range(p) for _ in range(t))==Z
            assert residue([mult*k*j for j in range(p) for _ in range(t)]+[0])!=Z

dump('ORIGINAL_PHASE_CONTROLS.json',{'basis':'alpha^i beta^j, 0<=i<4, 0<=j<6; alpha=zeta^21,beta=zeta^15','crt_congruences':crt,'fresh_controls':fresh,'author_masks_independently_recomputed':submitted_checks,'primitive_union_controls':len(zero_sets)*len(units),'primitive_singleton_negative_controls':35*len(units),'fresh_complete_gram_entries':len(fresh)*2*35*35,'submitted_complete_gram_entries':len(submitted_checks)*2*35*35})

old=Path('/workspace/shared/sparse_fiveq_first_interior_20261019_1344/Q7_ROW_GROUP_COUNTERCONTROL.json')
block=json.loads(old.read_text());R=block['R_block'];ids=block['row_indices'];rg,cg=grams(R,ids)
assert ids==[0,15,30,10,25,5,20]
assert all(rg[i][j]==((11,)+(0,)*23 if i==j else Z) for i,j in product(range(7),repeat=2))
details=[]
for row,r in zip(R,ids):
    lines=[u for u in range(5) if all(row[c] for c in range(35) if c%5==u)]
    fibers=[v for v in range(7) if all(row[c] for c in range(35) if c%7==v)]
    details.append({'row':r,'support':[c for c in range(35) if row[c]],'full_lines':lines,'full_fibers':fibers})
assert all(not x['full_fibers'] for x in details)
assert [x['full_lines'] for x in details]==[[],[],[],[],[],[3],[]]
m=sum(row[5] for row in R);assert R[0][5] and m==2
coldegrees=[sum(row[c] for row in R) for c in range(35)]
assert cg[5][5]==(2,)+(0,)*23
out={'original_source_sha256':sha(old),'row_indices':ids,'shape':[7,35],'row_gram':'11 I_7','column_degrees':coldegrees,'column_gram_is_not_11I35':True,'rows':details,'extension_certificate':{'row':0,'column':5,'own_group_multiplicity':m,'max_other_groups':4,'max_square_column_degree':6,'required_square_degree':11},'scope':'A valid rectangular row Gram, with exact obstruction to completing this block to a 35x35 degree-11 fixed-phase mask.'}
dump('RECTANGULAR_CHECK.json',out)
print(json.dumps({'status':'PASS','component_sizes_checked':7,'partitions':len(partitions_data),'crt_congruences':crt,'fresh_full_gram_entries':len(fresh)*2450,'author_full_gram_entries':len(submitted_checks)*2450,'rectangular_row_gram_entries':49,'primitive_positive_controls':len(zero_sets)*len(units)},indent=2))
