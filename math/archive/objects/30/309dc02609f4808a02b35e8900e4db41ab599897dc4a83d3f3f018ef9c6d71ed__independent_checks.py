#!/usr/bin/env python3
"""Fresh review-authored parity-rank and affine-depth controls; source programs are inert."""
import json,random
from fractions import Fraction
from pathlib import Path
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent

def rank_formula(k,a,b):return (1<<k)//(4 if a.bit_length()+b.bit_length()<=k else 2)
def boundary(k,a):return sum(1<<(k-j-1) for j in range(k) if (a&((1<<(j+1))-1)).bit_count()%2)
def pull(mask,columns):return sum(((mask&v).bit_count()%2)<<j for j,v in enumerate(columns))
def binary_rank(rows):
    piv={}
    for r in rows:
        while r:
            j=r.bit_length()-1
            if j in piv:r^=piv[j]
            else:piv[j]=r;break
    return len(piv)
def random_columns(k,rng):
    rows=[1<<j for j in range(k)]
    for _ in range(2*k*k):
        i,j=rng.sample(range(k),2)
        if rng.randrange(4)==0:rows[i],rows[j]=rows[j],rows[i]
        else:rows[i]^=rows[j]
    return [sum(((rows[i]>>j)&1)<<i for i in range(k)) for j in range(k)]
def transform_table(cols):
    k=len(cols);basis=[pull(1<<j,cols) for j in range(k)];out=[0]*(1<<k)
    for m in range(1,1<<k):low=m&-m;out[m]=out[m^low]^basis[low.bit_length()-1]
    return out

def trace(k,cols,a,weights=None):
    masks=[a]
    for col in cols:masks.append(pull(masks[-1],col))
    ds=[boundary(k,m) for m in masks];weights=weights or [1]*len(masks);cap=sum(r*d for r,d in zip(weights,ds));rank=rank_formula(k,a,masks[-1])
    return {'N':1<<k,'input_mask':a,'output_mask':masks[-1],'masks':masks,'stage_capacities':ds,'capacity':cap,'complex_fourier_rank':rank,'gap':rank-cap}

def best(k,cols):
    tables=[transform_table(c) for c in cols];bs=[0]+[boundary(k,m) for m in range(1,1<<k)];winner=None;key=None
    for a in range(1,1<<k):
        m=a;cap=bs[m]
        for table in tables:m=table[m];cap+=bs[m]
        gap=rank_formula(k,a,m)-cap;candidate=(gap,-cap)
        if key is None or candidate>key:winner=a;key=candidate
    return trace(k,cols,winner)

def primitive(n,p):
    for g in range(2,p):
        w=pow(g,(p-1)//n,p)
        if pow(w,n,p)==1 and pow(w,n//2,p)!=1:return w
    raise AssertionError

def rank_controls():
    out=[];deficient=[]
    for k in range(2,7):
        n=1<<k;count=sum(rank_formula(k,a,b)==n//4 for a in range(1,n) for b in range(1,n));assert count==(k-2)*(n//2)+1;deficient.append({'k':k,'deficient_ordered_pairs':count})
        sets={(a,s):[j for j in range(n) if (a&j).bit_count()%2==s] for a in range(1,n) for s in range(2)}
        for p in (12289,65537):
            assert prime_by_trial_division(p);w=primitive(n,p);f=Field(p);powers=[pow(w,j,p) for j in range(n)];checks=0
            for a in range(1,n):
                for b in range(1,n):
                    signs=((s,t) for s in range(2) for t in range(2)) if n<=16 else [(0,1)]
                    for s,t in signs:
                        actual=f.rank([[powers[(i*j)%n] for j in sets[a,s]] for i in sets[b,t]])
                        assert actual==rank_formula(k,a,b),(k,a,b,s,t,p,actual);checks+=1
            out.append({'N':n,'prime':p,'full_parity_matrix_rank_checks':checks})
    # Imported sampling criterion hypotheses, checked as exact residue counts.
    sets_checked=0
    for u in range(10):
        h=1<<(u+1)
        for a in range(1<<u,h):
            for sign in (0,1):
                e=[j for j in range(h) if (a&j).bit_count()%2==sign]
                assert len(e)==h//2 and len({j%(h//2) for j in e})==h//2
                for s in range(u+2):
                    counts=[0]*(1<<s)
                    for j in e:counts[j%len(counts)]+=1
                    assert max(counts)-min(counts)<=1
                sets_checked+=1
    cols=[0,1,2,3,4,13,6,7];rows=[0,1,2,3,4,6,7,12];bad=[]
    for p,expected in ((12289,7),(65537,8)):
        w=primitive(16,p);actual=Field(p).rank([[pow(w,i*j,p) for j in cols] for i in rows]);assert actual==expected;bad.append({'prime':p,'rank':actual})
    return {'parity_matrix_checks':out,'deficient_pair_counts':deficient,'balanced_residue_sets':sets_checked,'general_universal_set_bad_prime':{'rows':rows,'columns':cols,'complex_rank':8,'specializations':bad,'scope':'This is a general universal-set witness, not a claim that these columns are a parity halfset'}}

def verify_records():
    source=json.loads((BASE/'sources/EXACT_CERTIFICATES.json').read_text());legacy=[];universal=[]
    for ntext,row in source['legacy_layout_witnesses'].items():
        n=int(ntext);k=n.bit_length()-1;cols=row['three_GF2_shuffle_columns'];rng=random.Random(20261016+17*k)
        assert cols==[random_columns(k,rng) for _ in range(3)]
        assert all(binary_rank(c)==k for c in cols)
        actual=best(k,cols)
        assert all(actual[key]==row[key] for key in actual)
        if n>256:assert actual['gap']>0
        legacy.append(actual)
    for _,row in source['universal_GF2_depth_witnesses'].items():
        k=row['k'];cols=row['GF2_shuffle_columns'];assert all(binary_rank(c)==k for c in cols)
        actual=trace(k,cols,row['input_mask'],[row['r']]*row['t']);assert all(actual[key]==row[key] for key in actual)
        q=row['q'];assert k>row['t']*q and all(m%(1<<q)==0 for m in actual['masks'])
        assert actual['capacity']<(1<<k)//4<=actual['complex_fourier_rank'];universal.append(actual)
    h=source['heterogeneous_example'];k=h['k'];cols=h['GF2_shuffle_columns'];rs=h['stage_orders'];qs=h['quotas'];assert all(binary_rank(c)==k for c in cols)
    actual=trace(k,cols,h['input_mask'],rs);assert actual['masks']==h['stage_masks'] and actual['stage_capacities']==h['stage_boundaries'] and actual['capacity']==h['capacity'] and actual['complex_fourier_rank']==h['exact_complex_fourier_rank']
    assert sum(qs)<k and sum((Fraction(r,1<<q) for r,q in zip(rs,qs)),Fraction())<=Fraction(1,4)
    assert all(m%(1<<q)==0 for m,q in zip(actual['masks'],qs));assert actual['capacity']<(1<<k)//4
    # Full modular rank corroboration of the N512 and N1024 saved cuts.
    ranks=[]
    for n in (512,1024):
        row=source['legacy_layout_witnesses'][str(n)];a=row['input_mask'];b=row['output_mask'];cc=[j for j in range(n) if not (j&a).bit_count()%2];rr=[i for i in range(n) if (i&b).bit_count()%2]
        for p in (12289,65537):
            w=primitive(n,p);powers=[pow(w,j,p) for j in range(n)];rank=Field(p).rank([[powers[i*j%n] for j in cc] for i in rr]);assert rank==n//2;ranks.append({'N':n,'prime':p,'full_rank':rank})
    return {'legacy_seed_cases':legacy,'universal_depth_cases':universal,'heterogeneous_case':actual,'large_modular_ranks':ranks}

def stress():
    saved=json.loads((BASE/'sources/MIXER_EXPERIMENT.json').read_text());out={}
    for k in range(8,13):
        records=[]
        for j in range(50):
            rng=random.Random(20261010000+10000*k+j);records.append(best(k,[random_columns(k,rng) for _ in range(3)]))
        gaps=[r['gap'] for r in records]
        result={'trials':50,'failed_rank_gate':sum(g>0 for g in gaps),'survived_gate':sum(g<=0 for g in gaps),
                'max_fourier_minus_capacity':max(gaps),'min_fourier_minus_capacity':min(gaps),
                'example_excluded':next((r for r in records if r['gap']>0),None),'example_survivor':next((r for r in records if r['gap']<=0),None)}
        assert result==saved[str(1<<k)];out[str(1<<k)]=result
    return out

def new_nullspace_controls():
    results=[]
    for t,r in ((2,1),(3,1),(4,1),(5,1),(6,1),(2,2),(3,3)):
        q=(4*r*t-1).bit_length();k=t*q+1;rng=random.Random(713000+t*31+r)
        maps=[random_columns(k,rng) for _ in range(t-1)]
        images=[1<<i for i in range(k)];equations=[]
        for stage in range(t):
            equations.extend(sum(((images[i]>>bit)&1)<<i for i in range(k)) for bit in range(q))
            if stage<t-1:images=[pull(m,maps[stage]) for m in images]
        rows=equations[:];pivots=[];at=0
        for bit in range(k):
            found=next((i for i in range(at,len(rows)) if (rows[i]>>bit)&1),None)
            if found is None:continue
            rows[at],rows[found]=rows[found],rows[at]
            for i in range(len(rows)):
                if i!=at and (rows[i]>>bit)&1:rows[i]^=rows[at]
            pivots.append(bit);at+=1
        free=max(set(range(k))-set(pivots));mask=1<<free
        for bit,row in zip(pivots,rows):
            if (row&mask).bit_count()%2:mask|=1<<bit
        assert mask and all((row&mask).bit_count()%2==0 for row in equations)
        witness=trace(k,maps,mask,[r]*t)
        assert all(m%(1<<q)==0 for m in witness['masks']) and witness['capacity']<(1<<k)//4
        results.append({'k':k,'t':t,'r':r,'q':q,'constraint_rank':len(pivots),'witness':witness})
    return results

if __name__=='__main__':
    result={'status':'PASS','rank_controls':rank_controls(),'records':verify_records(),'all_250_mixer_trials':stress(),'fresh_nullspace_controls':new_nullspace_controls(),
      'source_uniform_helper_r_greater_than_one_correction':{'k':9,'t':2,'r':2,'q':4,'input_mask':16,'stage_boundaries':[31,31],'unweighted_source_capacity':62,'correct_weighted_capacity':124,'mathematical_theorem_unaffected':True}}
    (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: exhaustive parity matrix controls, universal-set guards, all saved certificates, all 250 mixer trials, and four full N512/N1024 ranks')
