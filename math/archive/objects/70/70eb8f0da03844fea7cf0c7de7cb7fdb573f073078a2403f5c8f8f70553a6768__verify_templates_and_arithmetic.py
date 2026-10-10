#!/usr/bin/env python3
"""Fresh independent static/text/exact-arithmetic audit; never evaluates input code.
Only standard-library data readers/hash/regex operations are used. No solver,
supplied module import, execution, compilation, AST or SMT expression parser.
"""
from pathlib import Path
import collections, hashlib, json, re, zipfile

ROOT = Path('generated_solver_review_0520')
INVENTORY = Path('code_coverage_audit_0228')
ARCHIVE = Path('fft_inventory/account_library/downloads/cancellation_transform_reproducibility.zip')
ARCHIVE_HASH = 'cd152b676bae0a9f955b13f20e25d131bd90a57f55fa04cc77098dfbf68acdad'
PREFIX = 'cancellation_transform_reproducibility/'
M = [
 [1,0,1,0,1,0,1,0], [0,1,0,1,0,1,0,1],
 [1,0,-1,0,1,0,-1,0], [0,1,0,-1,0,1,0,-1],
 [1,0,0,1,-1,0,0,-1], [0,1,-1,0,0,-1,1,0],
 [1,0,0,-1,-1,0,0,1], [0,1,1,0,0,-1,-1,0],
]
# Independently transcribed staged sum/difference circuit, not loaded as code.
PIN = [(0,4,1),(1,5,1),(2,6,1),(3,7,1),
       (0,4,-1),(1,5,-1),(2,6,-1),(3,7,-1),
       (8,10,1),(9,11,1),(8,10,-1),(9,11,-1),
       (12,15,1),(13,14,-1),(12,15,-1),(13,14,1)]

def sha(b): return hashlib.sha256(b).hexdigest()
def save_json(path, obj): path.write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n')
def F(operator, *operands): return '(' + ' '.join((operator, *operands)) + ')'
def C(n): return F('_', 'bv'+str(n % 32), '5')
def eq(a,b): return F('=',a,b)
def node(k,j): return C(2 if k==j else 0) if k<8 else f'v_{k}_{j}'

def lookup(selector, gate, coordinate):
    # Left-to-right textual arms, final fallback is exactly gate-1.
    # This function constructs expected text; it does not parse source text.
    arms = [f'(ite {eq(selector,C(k))} {node(k,coordinate)} ' for k in range(gate-1)]
    return ''.join(arms) + node(gate-1,coordinate) + ')'*(gate-1)

def expected_document(budget, timeout, pinned):
    lines=[]; tags=[]
    def put(text, category, **detail): lines.append(text+'\n'); tags.append({'category':category,**detail})
    def assertion(text, category, **detail): put(F('assert',text),category,**detail)
    put(F('set-option',':timeout',str(timeout)), 'solver_setting')
    put(F('set-option',':produce-models','true'),'solver_setting')
    put(F('set-logic','QF_BV'),'logic')
    for g in range(8,8+budget):
        for prefix in ['a','b','op','sa','sb']:
            put(F('declare-const',f'{prefix}_{g}','Bool' if prefix in ['sa','sb'] else F('_','BitVec','5')),'gate_declaration',gate=g)
        for prefix in ['a','b']:
            assertion(F('bvult',f'{prefix}_{g}',C(g)),'predecessor_bound',gate=g)
        assertion(F('bvule',f'op_{g}',C(2)),'operation_bound',gate=g)
        assertion(F('=>',eq(f'op_{g}',C(0)),F('bvule',f'a_{g}',f'b_{g}')),'sum_order_symmetry',gate=g)
        for j in range(8):
            v=node(g,j)
            put(F('declare-const',v,F('_','BitVec','5')),'coordinate_declaration',gate=g,coordinate=j)
            assertion(F('and',F('bvsge',v,C(-4)),F('bvsle',v,C(4))),'signed_coefficient_bound',gate=g,coordinate=j)
            a,b=lookup(f'a_{g}',g,j),lookup(f'b_{g}',g,j)
            a=F('ite',f'sa_{g}',F('bvneg',a),a)
            b=F('ite',f'sb_{g}',F('bvneg',b),b)
            addition=eq(v,F('bvadd',a,b))
            doubling=eq(v,F('bvmul',C(2),a))
            halving=eq(F('bvmul',C(2),v),a)
            assertion(F('ite',eq(f'op_{g}',C(0)),addition,F('ite',eq(f'op_{g}',C(1)),doubling,halving)),'gate_equation',gate=g,coordinate=j)
    for r,row in enumerate(M):
        choices=[]
        for g in range(8,8+budget):
            for sign in [1,-1]:
                choices.append(F('and',*[eq(node(g,j),C(sign*2*x)) for j,x in enumerate(row)]))
        assertion(F('or',*choices),'target_row',target_row=r)
    if pinned:
        for g,(a,b,sgn) in enumerate(PIN,8):
            for prefix,val in [('a',C(a)),('b',C(b)),('op',C(0)),('sa','false'),('sb','true' if sgn==-1 else 'false')]:
                assertion(eq(f'{prefix}_{g}',val),'pinned_control',gate=g)
    put(F('check-sat'),'query')
    put(F('get-info',':reason-unknown'),'query')
    return ''.join(lines).encode('ascii'), tags

# Preserve exact queue and archive metadata, and revalidate actual archive bytes.
assert sha(ARCHIVE.read_bytes()) == ARCHIVE_HASH
archive_graph = json.loads((INVENTORY/'ARCHIVE_GRAPH.json').read_text())
archive_row = next(r for r in archive_graph if r['sha256']==ARCHIVE_HASH)
source_rows=[]
for number in ['06','07']:
    src=Path('remaining_source_queue_0502')/('batch_'+number+'.json')
    (ROOT/'input_manifests'/src.name).write_bytes(src.read_bytes())
    source_rows.extend(json.loads(src.read_text())['rows'])
save_json(ROOT/'input_manifests/archive_record.json',archive_row)
save_json(ROOT/'input_manifests/archive_root_records.json',[r for r in json.loads((INVENTORY/'ARCHIVE_ROOTS.json').read_text()) if r['sha256'] in [ARCHIVE_HASH,*source_rows[0]['root_archive_sha256s']]])
selected_names=['README.md','audit.md','smt_run.log','smt_run_30s.log','smt_search.py','verify_smt_control.py',
 'results/positive_control.smt2','results/slp_15.smt2','results/positive_control.log','results/slp_15.log',
 'results/positive_control.json','results/slp_15.json','results/synthetic_staged_baseline_certificate.json']
provenance=[]; data={}
with zipfile.ZipFile(ARCHIVE) as z:
    infos=z.infolist()
    for name in selected_names:
        record=next(r for r in archive_row['members'] if r['name']==PREFIX+name)
        info=infos[record['member_index']]
        assert info.filename==PREFIX+name
        content=z.read(info)
        assert sha(content)==record['sha256'] and len(content)==record['size_bytes']
        dest=ROOT/'source_snapshots'/name.replace('/','__')
        dest.write_bytes(content)
        data[name]=content
        provenance.append({**record,'archive_sha256':ARCHIVE_HASH,'archive_local_path':str(ARCHIVE),'snapshot':str(dest.relative_to(ROOT))})

coverage=[]
for row,budget,timeout,pinned in [(source_rows[0],16,5000,True),(source_rows[1],15,30000,False)]:
    name=row['names'][0]; actual=data['results/'+name]
    assert Path(row['local_content']).read_bytes()==actual
    expected,tags=expected_document(budget,timeout,pinned)
    if actual != expected:
        # Give first discrepancy without accepting any unmatched tail or line.
        j=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),min(len(actual),len(expected)))
        raise AssertionError((name,'mismatch',j,actual[max(0,j-100):j+100],expected[max(0,j-100):j+100]))
    lines=actual.splitlines(keepends=True)
    assert len(lines)==len(tags)
    lexical_tokens=re.findall(rb'\(|\)|[^()\s]+',actual)
    assert b''.join(re.findall(rb'\(|\)|[^()\s]+|\s+',actual))==actual
    depth=0;maximum=0
    for token in lexical_tokens:
        if token==b'(': depth+=1;maximum=max(maximum,depth)
        elif token==b')': depth-=1;assert depth>=0
    assert depth==0
    symbols=set();all_declarations=[];line_evidence=[];offset=0
    for i,(line,tag) in enumerate(zip(lines,tags),1):
        s=line.decode('ascii')
        declaration=re.fullmatch(r'\(declare-const ([a-z]+_\d+(?:_\d+)?) (Bool|\(_ BitVec 5\))\)\n',s)
        if declaration:
            symbol=declaration.group(1);assert symbol not in symbols
            symbols.add(symbol);all_declarations.append({'name':symbol,'type':declaration.group(2)})
        else:
            used=re.findall(r'\b(?:a|b|op|sa|sb)_\d+\b|\bv_\d+_\d+\b',s)
            assert set(used)<=symbols
        line_evidence.append({'line':i,'start_byte_zero_based':offset,'end_byte_exclusive':offset+len(line),'bytes':len(line),'sha256':sha(line),'matched_expected_exactly':True,**tag})
        offset+=len(line)
    assert offset==len(actual)
    counts=dict(collections.Counter(t['category'] for t in tags))
    evidence={'sha256':sha(actual),'name':name,'size_bytes':len(actual),'line_count':len(lines),'budget':budget,'timeout_ms':timeout,
      'method':'Independent text reconstruction from reviewed mathematical specification; every byte, including whitespace and final LF, compared exactly. Full lexical identifier/declaration-order and parenthesis scan. No source AST parsing.',
      'coverage_class':'complete_static_semantic_template_verification','static_inspection_complete':True,'complete_static_semantic_template_verification':True,'literal_first_to_last_model_read':False,'spot_check_only':False,
      'expected_sha256':sha(expected),'complete_byte_equality':True,'unmatched_bytes':0,'unmatched_lines':0,
      'all_declarations_unique_and_uses_declared':True,'declarations':all_declarations,'category_counts':counts,'lexical_token_count':len(lexical_tokens),'maximum_parenthesis_depth':maximum,
      'execution':'No supplied code or SMT run; no solver, source import, compilation or AST parsing.',
      'original_queue_provenance':row,'line_evidence':line_evidence}
    save_json(ROOT/'per_source'/(row['sha256']+'.json'),evidence)
    coverage.append({k:v for k,v in evidence.items() if k not in ['declarations','line_evidence','original_queue_provenance']})

# All 9 signed encoded coefficient values; equality is residue equality mod 32.
allowed=[r for r in range(32) if -4 <= (r if r<16 else r-32)<=4]
assert allowed==[0,1,2,3,4,28,29,30,31]
no_wrap={'signed_5bit_range':[-16,15],'stored_coefficient_range':[-4,4],'actual_coefficient_range':['-2','2'],
 'allowed_residues':allowed,'modulus':32,'sum_cases':0,'double_cases':0,'half_cases':0,'false_modular_solutions':0}
for a in range(-4,5):
    for sign in [-1,1]:
        x=sign*a
        assert -4<=x<=4
        for b in range(-4,5):
            for s2 in [-1,1]:
                y=s2*b;assert -8<=x+y<=8
                for v in range(-4,5):
                    assert ((v-(x+y))%32==0)==(v==x+y)
                    no_wrap['sum_cases']+=1
        assert -8<=2*x<=8
        for v in range(-4,5):
            assert ((v-2*x)%32==0)==(v==2*x)
            no_wrap['double_cases']+=1
            assert ((2*v-x)%32==0)==(2*v==x)
            no_wrap['half_cases']+=1
# Complete actual 5-bit selector domains, including all invalid encodings.
index_checks=[]
for g in range(8,24):
    valid=[x for x in range(32) if x<g]
    assert valid==list(range(g))
    for x in valid:
        # First matching equality arm or the default exactly matches chosen index.
        selected=next((k for k in range(g-1) if x==k),g-1)
        assert selected==x and selected<g
    index_checks.append({'gate':g,'all_32_residues_checked':True,'valid_count':len(valid),'valid_min':0,'valid_max':g-1,'fallback':g-1})
assert [x for x in range(32) if x<=2]==[0,1,2]
# Symmetry does not remove any possible signed addition, for all scalar cases.
symmetry_cases=0
for a in range(24):
    for b in range(24):
        for sa in [-1,1]:
            for sb in [-1,1]:
                ordered=sorted([(a,sa),(b,sb)])
                for x in range(-4,5):
                    for y in range(-4,5):
                        if a==b and x!=y: continue
                        values={a:x,b:y}
                        before=sa*values[a]+sb*values[b]
                        after=sum(sgn*values[index] for index,sgn in ordered)
                        assert ordered[0][0]<=ordered[1][0] and after==before
                        symmetry_cases+=1

# Fresh arithmetic replay of the transcribed circuit, checked against all data gates.
cert=json.loads(data['results/synthetic_staged_baseline_certificate.json'])
assert set(cert)=={'name','n_inputs','gates','outputs','target','normalization'}
assert cert['name']=='synthetic_staged_baseline' and cert['n_inputs']==8 and cert['normalization']=='1/4'
assert cert['target']==M and cert['outputs']==[[i,1] for i in range(16,24)]
assert len(cert['gates'])==16
vectors=[[2 if i==j else 0 for j in range(8)] for i in range(8)]
model_expected={};replay=[]
for g,((a,b,sign),gate) in enumerate(zip(PIN,cert['gates']),8):
    assert gate=={'op':'add','terms':[[a,1],[b,sign]]}
    assert 0<=a<=b<g
    v=[x+sign*y for x,y in zip(vectors[a],vectors[b])]
    assert all(-4<=x<=4 for x in v)
    vectors.append(v)
    model_expected.update({f'a_{g}':a,f'b_{g}':b,f'op_{g}':0,f'sa_{g}':False,f'sb_{g}':sign==-1})
    model_expected.update({f'v_{g}_{j}':x%32 for j,x in enumerate(v)})
    replay.append({'gate':g,'a':a,'b':b,'sign_b':sign,'stored_vector':v,'actual_vector':[x//2 for x in v]})
assert vectors[16:24]==[[2*x for x in row] for row in M]
assert all(any(v==[sign*2*x for x in row] for v in vectors[8:] for sign in [-1,1]) for row in M)
# Model reading is a flat lexical format check, not SMT parsing or evaluation.
model_text=data['results/positive_control.log'].decode('ascii')
assert model_text.startswith('sat\n(:reason-unknown "")\n(\n') and model_text.endswith(')\n')
body=model_text[len('sat\n(:reason-unknown "")\n(\n'):-2]
pattern=re.compile(r'  \(define-fun ([a-z]+_\d+(?:_\d+)?) \(\) (Bool|\(_ BitVec 5\))\n    (true|false|#b[01]{5})\)\n')
model={};cursor=0
for match in pattern.finditer(body):
    assert match.start()==cursor
    cursor=match.end();name,typ,val=match.groups();assert name not in model
    assert (typ=='Bool')==(val in ['true','false'])
    model[name]=(val=='true') if typ=='Bool' else int(val[2:],2)
assert cursor==len(body) and len(model)==208 and model==model_expected
# Every archived model declaration agrees with every literal declaration.
control_decl=json.loads((ROOT/'per_source'/(source_rows[0]['sha256']+'.json')).read_text())['declarations']
assert set(model)=={x['name'] for x in control_decl}
for d in control_decl: assert (type(model[d['name']]) is bool)==(d['type']=='Bool')
assert data['results/slp_15.log']==b'unknown\n(:reason-unknown "timeout")\n'
control_summary=json.loads(data['results/positive_control.json'])
search_summary=json.loads(data['results/slp_15.json'])
assert control_summary['status']=='sat' and control_summary['gates']==16 and control_summary['pinned_baseline'] is True
assert search_summary['status']=='unknown' and search_summary['budget']==15 and search_summary['timeout_ms']==30000
gram=[[sum(x*y for x,y in zip(a,b)) for b in M] for a in M]
assert gram==[[4 if i==j else 0 for j in range(8)] for i in range(8)]
assert all(sum(x!=0 for x in row)==4 for row in M)
results={'target_gram_matrix':gram,'target_rows_all_four_nonzero_coordinates':True,'all_checks_passed':True,'source_coverage':coverage,'no_wrap_exhaustive_arithmetic':no_wrap,'index_checks':index_checks,
 'operation_selector_valid_residues':[0,1,2],'commutative_symmetry_scalar_cases':symmetry_cases,
 'control_replay':replay,'control_model_definitions_verified':len(model),'control_model_fully_consumed_lexically':True,
 'control_model_matches_fresh_exact_arithmetic':True,'targets':M,'target_output_nodes':list(range(16,24)),
 'source_target':'unnormalized M; each stored target row is +/-2M; physical coefficient row is +/-M',
 'normalization':'certificate records 1/4; no quarter-scaling constraint or cost appears in either SMT source',
 'archived_control_summary':control_summary,'archived_search_summary':search_summary,
 'archived_search_log':data['results/slp_15.log'].decode('ascii'),
 'initial_run_log':data['smt_run.log'].decode('ascii'),'corrected_run_log':data['smt_run_30s.log'].decode('ascii'),
 'execution_attribution':'Only this freshly written checker was run. Archived SAT/unknown logs are historic data, not fresh solver execution. Fresh control satisfaction is established by template proof and exact arithmetic, not a solver.'}
save_json(ROOT/'checks/CHECK_RESULTS.json',results)
save_json(ROOT/'COVERAGE.json',coverage)
save_json(ROOT/'PROVENANCE.json',{'archive_sha256':ARCHIVE_HASH,'archive_size_bytes':ARCHIVE.stat().st_size,'archive_rehashed':True,'inputs':provenance,
 'authorship':'Queue origin_unresolved retained: generating-program linkage and archive provenance do not establish original-versus-reviewer authorship.',
 'root_chain':'Current archive bytes match both Library root entry and nested archive graph record; outer historical bundle is recorded provenance, not freshly rehashed by this checker.'})
preservation=[]
for row in source_rows:
    b=Path(row['local_content']).read_bytes();assert sha(b)==row['sha256'] and len(b)==row['size_bytes']
    preservation.append({'path':row['local_content'],'sha256_before_and_after':sha(b),'size_bytes':len(b),'unchanged':True})
assert sha(ARCHIVE.read_bytes())==ARCHIVE_HASH
save_json(ROOT/'PRESERVATION.json',{'source_inputs':preservation,'archive_unchanged':True,'central_registry_modified':False})
print(json.dumps({'pass':True,'files':[(c['name'],c['size_bytes'],c['line_count'],c['unmatched_bytes']) for c in coverage],
 'model_assignments_verified':len(model),'no_wrap':no_wrap,'pinned_control_exact':True,'slp_15_status':'archived unknown/timeout'},indent=2))
