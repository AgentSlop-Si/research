"""Fresh data-only circuit continuation; no inherited executable is imported."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'research_cycle_1805/guarded_fourier_reduction'
C=json.loads((SOURCE/'CERTIFICATE.json').read_text())
B=json.loads((SOURCE/'COMPACT_BRANCH.json').read_text())
V=C['variables']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
polys={}
def put(p):
    p=sorted(p,key=lambda t:t[0])
    key=hashlib.sha256(json.dumps(p,separators=(',',':')).encode()).hexdigest()
    polys[key]=p
    return key
new=[]
for variable,equation,guard in [(22,'58',None),(88,'36',None),(52,'4','x83')]:
    p=C['polynomials'][B['equations'][equation]]
    j=V.index(variable)
    denominator=[]; numerator=[]
    for m,c,d in p:
        assert m[j]<=1
        if m[j]:
            mm=m[:]; mm[j]=0; denominator.append([mm,c,d])
        else: numerator.append([m,[-x for x in c],d])
    assert len(numerator)==1
    unit=numerator[0][1:]
    if guard: assert numerator[0][0][V.index(int(guard[1:]))]==1 and sum(numerator[0][0])==1
    else: assert not any(numerator[0][0])
    deps=sorted({V[i] for poly in [numerator,denominator] for m,c,d in poly for i,power in enumerate(m) if power})
    nr,dr=put(numerator),put(denominator)
    new.append({'variable':variable,'source_equation':equation,'source_label':C['initial']['labels'][equation],
                'source':B['equations'][equation],'numerator':nr,'denominator':dr,'dependencies':deps,
                'denominator_nonzero':{'method':'forced by source equation and nonzero numerator',
                    'identity':'source = variable * denominator - numerator',
                    'numerator_nonzero':{'constant':unit,'guard_factors':[] if guard is None else [guard]},
                    'zero_branch':'denominator=0 forces nonzero numerator=0, impossible'},
                'retained_denominator_guard':f'D{variable}'})
# The three inherited solve definitions stay identical and are replayed by the checker.
all_defs=new+B['definitions']
removed={d['source_equation'] for d in new}
eq={k:r for k,r in B['equations'].items() if k not in removed}
guards=dict(B['guards'])
for d in new:guards[d['retained_denominator_guard']]=d['denominator']
result={'format':'guarded triangular rational circuit v2; forced-numerator pivots',
 'status':'AUTHOR-PENDING: newly authored checker has not been independently reviewed',
 'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'CERTIFICATE.json',SOURCE/'COMPACT_BRANCH.json',ROOT/'research_cycle_1819/guarded_reduction_review/RECEIPT.json']},
 'variables':V,'coefficient_basis':'1,zeta,...,zeta^9; Phi11(zeta)=0',
 'free_variables':[v for v in B['free_variables'] if v not in {22,88,52}],
 'reconstruction_order':[d['variable'] for d in all_defs], 'new_eliminations':[22,88,52],
 'definitions':all_defs,'equations':eq,'guards':guards,'polynomials':polys,
 'inherited_polynomial_sources':['research_cycle_1805/guarded_fourier_reduction/CERTIFICATE.json','research_cycle_1805/guarded_fourier_reduction/COMPACT_BRANCH.json'],
 'equation_count':len(eq),'guard_count':len(guards),'original_guard_count':len(B['guards']),
 'semantics':'Assign the free coordinates. Evaluate each definition in reconstruction order; its denominator must be nonzero, and set the coordinate to numerator/denominator. Evaluate all residual equation references as zero and all guard references as nonzero at the resulting 15-coordinate point. Reconstruct x91 by the accepted parent certificate. All fourteen old guards are retained, plus the three newly proved denominator guards. No parent residual polynomial is expanded after substitution.',
 'equivalence':'Bijection with the accepted guarded 12-coordinate necessary circuit system, via unique rational reconstruction. This is not yet sufficiency for original Fourier factorization.',
 'limits':{'max_sparse_product_pairs':1000000,'max_output_terms':50000,'no_full_residual_expansion':True},
 'factorization_claimed':False,'contradiction_claimed':False}
(OUT/'CONSEQUENCE_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print('Wrote',OUT/'CONSEQUENCE_CERTIFICATE.json')
