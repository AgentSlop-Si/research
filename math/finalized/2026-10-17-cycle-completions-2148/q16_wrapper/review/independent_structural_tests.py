"""Fresh independent tests; historical sources are never imported/executed."""
import ast, hashlib, json, random, sys
from dataclasses import asdict, replace, FrozenInstanceError
from pathlib import Path
ROOT=Path(__file__).resolve().parent / '../candidate'
OUT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from outer_wrapper import Header, Outer, ReceiptLedger, Incidence
from sparse_output import produce_medians, verify_produced

checks=[]; negatives=[]
def ok(name): checks.append(name)
def reject(name, fn, fragment=None):
    try: fn()
    except (ValueError,ArithmeticError,FrozenInstanceError) as e:
        if fragment is not None: assert fragment in str(e),(name,str(e))
        negatives.append({'name':name,'exception':type(e).__name__,'message':str(e)})
    else: raise AssertionError('unexpected acceptance: '+name)

# Pin the reviewed bytes before importing/using their behavior.
expected_manifest='234149beef4953463b73724c526e10c0b5bb9701e3bf9abbb13c334def2e6b34'
assert hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest()==expected_manifest
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for name,pin in manifest['files'].items():
    blob=(ROOT/name).read_bytes()
    assert len(blob)==pin['bytes'] and hashlib.sha256(blob).hexdigest()==pin['sha256']
ok('all public candidate manifest entries match')

# Independent high-level median oracle: ordinary built-in sort, no source port.
rng=random.Random(202610172143)
median_cases=0
for R in (1,3,5,7,9,15,17,31):
    for S in (0,1,2,3,7,16):
        for rep in range(8):
            M=128;P=8+rep
            candidates=tuple(sorted(rng.sample(range(M),S)))
            rows=tuple(tuple((rng.randint(-10000,10000),rng.randint(-10000,10000)) for _ in range(S)) for _ in range(R))
            L=ReceiptLedger();run=produce_medians(M,P,candidates,rows,L)
            expected=tuple((k,(sorted(row[j][0] for row in rows)[R//2],sorted(row[j][1] for row in rows)[R//2])) for j,k in enumerate(candidates))
            assert run.output.pairs==expected and run.output.bits==P
            assert run._origin.candidates is candidates and run._origin.rows is rows
            before=L.events; assert verify_produced(run,L,replay=True) is run.output
            assert L.events>before
            median_cases+=1
ok(f'{median_cases} independent Cartesian-median cases, including odd partial merge runs and empty support')

L=ReceiptLedger()
for name,M,P,C,R in [
 ('boolean M',True,8,(0,),(((1,2),),)),
 ('boolean P',4,True,(0,),(((1,2),),)),
 ('non-dyadic M',6,8,(0,),(((1,2),),)),
 ('too-small P',4,7,(0,),(((1,2),),)),
 ('mutable candidates',4,8,[0],(((1,2),),)),
 ('descending candidates',4,8,(1,0),(((1,2),(3,4)),)),
 ('duplicate candidates',4,8,(0,0),(((1,2),(3,4)),)),
 ('negative candidate',4,8,(-1,),(((1,2),),)),
 ('candidate equal M',4,8,(4,),(((1,2),),)),
 ('boolean candidate',4,8,(False,),(((1,2),),)),
 ('mutable rounds',4,8,(0,),[ ((1,2),) ]),
 ('zero rounds',4,8,(0,),()),
 ('even rounds',4,8,(0,),(((1,2),),((3,4),))),
 ('mutable row',4,8,(0,),([(1,2)],)),
 ('row too long',4,8,(0,),(((1,2),(3,4)),)),
 ('mutable pair',4,8,(0,),(([1,2],),)),
 ('short pair',4,8,(0,),(((1,),),)),
 ('long pair',4,8,(0,),(((1,2,3),),)),
 ('boolean real',4,8,(0,),(((True,2),),)),
 ('floating imag',4,8,(0,),(((1,2.0),),))]:
    reject(name,lambda M=M,P=P,C=C,R=R:produce_medians(M,P,C,R,L))
ok('malformed median inputs rejected')

# Direct row-first oracle over modest finite N, not inverse endpoint construction.
geometry_cases=0
for N in (1,2,127,256,257,258,300,511,512,513,777,1023,1024,1025):
    M=1<<(4*N-1).bit_length()
    for D in (5,6,9):
        support=tuple(sorted(set((0,1,M//3,M//2,M-2,M-1))))
        LL=ReceiptLedger();run=produce_medians(M,16,support,(tuple((k,-k) for k in support),),LL)
        out=Outer(Header(N,M,D,16),run,LL);g=out.binding.geometry
        got=list(out.incidences())
        if g.t>=M:
            assert not got and out.last_failure=='OUTER_DENSE_REQUIRED' and out.kernel is None
        else:
            expected={(ell,k) for ell in range(N) for k in support
                      if (k-ell*M//N)%M<=g.h+1 or (k-ell*M//N)%M>=M-g.h}
            assert {(r.ell,r.k) for r in got}==expected
            assert len(got)==len(expected)
            for ordinal,r in enumerate(got):
                assert r.ordinal==ordinal
                out._validate_incidence(r)
            assert out.kernel is None
        geometry_cases+=1
ok(f'{geometry_cases} independent direct row-first incidence/guard cases')

N=(1<<55)-1;M=1<<57;D=5;P=928
support=(0,1710,(1<<55)+1,M-1);U=1<<P
rows=(((U,0),(0,0),(-U,U//2),(U//4,-U//4)),
      ((U+1,1),(1,-1),(-U+1,U//2+1),(U//4+1,-U//4+1)),
      ((U-1,-1),(-1,1),(-U-1,U//2-1),(U//4-1,-U//4-1)))
L=ReceiptLedger();run=produce_medians(M,P,support,rows,L);producer=L.report()
before=L.events;out=Outer(Header(N,M,D,P),run,L);assert L.events>before
g=out.binding.geometry
assert (g.m,g.s,g.h,g.t,g.J,g.K,g.p)==(57,285,4561,9124,587,623,459)
records=list(out.incidences());assert out.kernel is None
assert len(records)==9123
assert [sum(r.k==k for r in records) for k in support]==[2281,2280,2281,2281]
assert [[r.ordinal,r.k,r.ell,r.lifted] for r in records]==json.loads((ROOT/'INCIDENCES.json').read_text())
# Independent centered-offset incidence set with modular row inverses.
expected=set()
for k in support:
    for delta in range(-g.h,g.h+2):
        center=(k-delta)%M
        ell=(center*N+M-1)//M
        if ell<N and ell*M//N==center: expected.add((ell,k))
assert {(r.ell,r.k) for r in records}==expected and len(expected)==9123
for ordinal,r in enumerate(records):
    assert r.ordinal==ordinal
    out._validate_incidence(r)
ok('all 9,123 requested incidences, per-support counts, order and source evidence verified')

selected=[]
for ell,k in ((0,0),(1<<53,(1<<55)+1),(0,1710)):
    r=next(r for r in records if r.ell==ell and r.k==k)
    c=out.coefficient(r)
    assert c.incidence is r and c.incidence.binding is out.binding
    assert c._origin.incidence is r and c._origin.result is c.certificate
    assert c.real==c.certificate.real_integer and c.imag==c.certificate.imag_integer and c.p==c.certificate.p
    assert c.real_enclosure is c.certificate.real_enclosure and c.imag_enclosure is c.certificate.imag_enclosure
    assert out.validate_coefficient(c) is c
    selected.append(c)
assert [asdict(c.certificate) for c in selected]==json.loads((ROOT/'RESULTS.json').read_text())['selected_coefficients']
assert out.kernel.paid.operations['pi_setup']==out.kernel.paid.operations['sqrt_setup']==1
assert selected[0].certificate.residue==0 and selected[0].certificate.denominator is None
assert selected[1].certificate.residue==1 and selected[1].certificate.denominator.lo>0
assert selected[2].certificate.F.hi<0 and selected[2].certificate.R.hi<0
ok('three exact selected coefficient certificate records and their source bindings reproduced')

other=Outer(Header(N,M,D,P),produce_medians(M,P,support,rows,L),L)
reject('foreign binding',lambda:out.validate_binding(other.binding))
reject('cloned binding',lambda:out.validate_binding(replace(out.binding)))
reject('frozen original input context',lambda:setattr(run._origin,'rows',()))
reject('substituted output only',lambda:Outer(Header(N,M,D,P),replace(run,output=replace(run.output)),L))
changed=replace(run.output,pairs=((0,(U+20,0)),)+run.output.pairs[1:])
forged=replace(run,output=changed,_origin=replace(run._origin,output=changed))
before=L.events
reject('changed output and origin with old immutable context',lambda:Outer(Header(N,M,D,P),forged,L),'semantic replay mismatch')
assert L.events>before
# If a coherent replacement context is presented, it is a new run and the replay
# recomputes it. No claim of externally authenticated historical source exists.
for field,value in [('N',0),('D',4),('estimate_bits',7),('N',True),('M',float(M)),('D',False),('estimate_bits',False),('M',M//2),('estimate_bits',P+1)]:
    reject('header '+field+' '+str(value),lambda field=field,value=value:Outer(replace(Header(N,M,D,P),**{field:value}),run,L))
for field,value in [('ordinal',1),('ordinal',False),('support_ordinal',1),('support_ordinal',-1),('k',1),('ell',1),('lifted',records[0].lifted+N),('binding',other.binding)]:
    reject('incidence '+field,lambda field=field,value=value:out.coefficient(replace(records[0],**{field:value})))
c=selected[0]
for field,value in [('real',c.real+1),('imag',c.imag+1),('p',c.p+1),('p',True),('incidence',records[1]),('certificate',replace(c.certificate)),('real_enclosure',replace(c.real_enclosure)),('imag_enclosure',replace(c.imag_enclosure))]:
    reject('coefficient '+field,lambda field=field,value=value:out.validate_coefficient(replace(c,**{field:value})))
reject('foreign coefficient origin',lambda:other.validate_coefficient(c))
ok('binding, original-context replay, header, incidence and coefficient substitution controls')

LL=ReceiptLedger();before=LL.report()
reject('16385-bit consumed malformed prefix',lambda:produce_medians(M,P,(0,),(((1<<16384,False),),),LL),'exact built-in integer')
assert LL.max_bits>=16385 and LL.bit_work>before['bit_work'] and LL.fields==4
before=L.report();out.validate_binding(out.binding);after=L.report()
assert all(after[k]>=before[k] for k in before) and after['events']>before['events']
be=out.kernel.paid.events;out.kernel.prepare();assert out.kernel.paid.events>be
assert out.kernel.paid.operations['pi_setup']==out.kernel.paid.operations['sqrt_setup']==1
emptyL=ReceiptLedger();empty=Outer(Header(N,M,D,P),produce_medians(M,P,(),((),),emptyL),emptyL)
assert list(empty.incidences())==[] and empty.kernel is None and emptyL.bit_work>0
ok('malformed-prefix actual-width charging, cumulative reuse, empty lazy setup')

# AST loop inventory: production iteration occurs only over sparse input data,
# per-column median rows, merge-sort runs or retained endpoint intervals.
loops=[]
for filename in ('outer_wrapper.py','sparse_output.py'):
    module=ast.parse((ROOT/filename).read_text())
    for node in ast.walk(module):
        if isinstance(node,(ast.For,ast.While,ast.comprehension)):
            expression=node.test if isinstance(node,ast.While) else node.iter
            loops.append({'file':filename,'line':getattr(node,'lineno',None),'type':type(node).__name__,'iteration':ast.unparse(expression)})
            assert ast.unparse(expression) not in ('range(N)','range(M)','range(G.N)','range(G.M)')
assert not any('phase_medians' in name or 'compact_window' in name for name in sys.modules)
ok('production loop inventory contains no dense N/M traversal; no historical module imported')

result={'status':'PASS_LOCAL_MEDIAN_REFINEMENT_BINDING_AND_OUTER_ITERATOR_STRUCTURAL_SUBGATE',
 'pinned_manifest_sha256':expected_manifest,'checks':checks,'median_cases':median_cases,'small_geometry_cases':geometry_cases,
 'incidence_count':len(records),'per_support_counts':[2281,2280,2281,2281],
 'selected_coefficients':[asdict(c.certificate) for c in selected],
 'negative_controls':negatives,'negative_control_count':len(negatives),
 'producer_ledger':producer,'final_outer_ledger':L.report(),'malformed_prefix_ledger':LL.report(),
 'fresh_module_paths':{name:str(Path(sys.modules[name].__file__).resolve()) for name in ('outer_wrapper','sparse_output','production_scalar')},
 'production_loop_inventory':loops,'historical_source_executed':False,
 'independent_transcendental_oracle':'separate scalar reviewer; not claimed by this test',
 'full_sparse_pipeline_provenance':False,'full_outer_transform':False}
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'median_cases':median_cases,'geometry_cases':geometry_cases,'incidences':len(records),'coefficients':3,'negative_controls':len(negatives)}))
