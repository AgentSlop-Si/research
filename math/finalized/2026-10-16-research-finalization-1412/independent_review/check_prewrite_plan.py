"""Reviewer-authored structural check; accepts private plan inputs, emits safe summary only."""
import json, hashlib, collections, copy, sys
from pathlib import Path
base=Path(sys.argv[1])
out=Path(sys.argv[2])
load=lambda n:json.loads((base/n).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
p=load('NATIVE_PLAN.json'); s=load('NATIVE_PLAN_SAFE.json'); guards=load('NATIVE_EXPECTED_ALL_CELLS.json')
plans=p['plans']; assert p['target_count']==len(plans)==len(p['requests'])==len(s['targets'])==50
key=lambda x:(x['sheet'],x['row_index'],x['column_index'])
ps={key(x):x for x in plans}; gs={key(x):x for x in guards}
assert len(ps)==50 and len(gs)==len(guards)==1955
assert p['requests']==[x['request'] for x in plans]
separator='\n\nEarlier dated history (preserved verbatim):\n'
rich=notes=prefixes=0
protected={'Catalogue':{26,28,29},'novelity breakthough':{20,22,23},'Research overview':{11,13,14}}
for x, sx in zip(plans,s['targets']):
    k=key(x); assert k in gs
    assert x['before_cell']==gs[k]['before'] and x['expected_after_cell']==gs[k]['after']
    assert x['before_cell']['userEnteredValue']=={'stringValue':x['before']}
    assert x['expected_after_cell']['userEnteredValue']=={'stringValue':x['after']}
    assert x['column_index'] not in protected.get(x['sheet'],set())
    before=x['before_cell']; after=x['expected_after_cell']; masked=x['fields'].split(',')
    assert masked in [['userEnteredValue'],['userEnteredValue','textFormatRuns']]
    assert {a:v for a,v in before.items() if a not in masked}=={a:v for a,v in after.items() if a not in masked}
    rq=x['request']; assert set(rq)=={'updateCells'}; u=rq['updateCells']
    assert set(u)=={'start','rows','fields'}
    assert u['start']=={'sheetId':x['sheet_id'],'rowIndex':x['row_index'],'columnIndex':x['column_index']}
    assert u['fields']==x['fields'] and len(u['rows'])==len(u['rows'][0]['values'])==1
    v=u['rows'][0]['values'][0]
    assert set(v)==set(masked) and all(v[a]==after[a] for a in masked)
    if x['operation']=='prepend_preserving_history':
        prefixes+=1; prefix=x['prefix']+separator
        assert x['after']==prefix+x['before']
        offset=len(prefix.encode('utf-16-le'))//2
        assert x['prefix_utf16_length']==offset
        if before.get('textFormatRuns'):
            old=before['textFormatRuns']; rich+=len(old)
            expected=[{'startIndex':0,'format':{}}]
            for run in old:
                new=copy.deepcopy(run);new['startIndex']=new.get('startIndex',0)+offset;expected.append(new)
            assert after['textFormatRuns']==expected
    else:assert x['operation']=='replace_current_summary_or_status'
    if 'note' in before:notes+=1;assert before['note']==after['note']
    assert sx['sheet']==x['sheet'] and sx['cell']==x['cell'] and sx['operation']==x['operation']
    assert sx['prefix']==x['prefix']
    assert sx['before_text_sha256']==sha(x['before'].encode()) and sx['after_text_sha256']==sha(x['after'].encode())
assert prefixes==47 and rich==60 and notes==5
changed={key(g) for g in guards if g['before']!=g['after']};assert changed==set(ps)
for g in guards:
    if key(g) not in ps:assert g['before']==g['after']
status=[]; before_counts=collections.Counter(); after_counts=collections.Counter();ids=[]
for g in guards:
    if g['sheet']=='Research overview' and g['column_index']==4:
        bv=g['before'].get('userEnteredValue',{}).get('stringValue');av=g['after'].get('userEnteredValue',{}).get('stringValue')
        if bv in ['TO RESEARCH','CLOSED']:
            before_counts[bv]+=1;after_counts[av]+=1
            identifier=gs[(g['sheet'],g['row_index'],1)]['before']['userEnteredValue']['stringValue'];ids.append(identifier)
            if bv!=av:status.append({'stable_id':identifier,'cell':'E'+str(g['row_index']+1),'before':bv,'after':av})
assert len(ids)==len(set(ids))==327
assert dict(before_counts)=={'TO RESEARCH':244,'CLOSED':83}
assert dict(after_counts)=={'TO RESEARCH':242,'CLOSED':85}
assert status==[{'stable_id':'Q32','cell':'E45','before':'TO RESEARCH','after':'CLOSED'},{'stable_id':'ALG-057','cell':'E210','before':'TO RESEARCH','after':'CLOSED'}]
assert ps[('Research overview',2,0)]['after']=='327 overview records: 242 TO RESEARCH + 85 CLOSED'
for x in plans:
    if x['stable_id']=='ALG-053' and x['cell'] in ['AE148','Y139','P208']:
        assert 'dyadic K' in x['prefix'] and 'supplied primitive Nth root' in x['prefix'] and 'fixed d' in x['prefix']
report_names=['algebra','algorithms','low_value','source_blocked']
assert len(sys.argv)==7, 'Provide plan directory, output file, then four report files.'
reports={name:Path(path) for name,path in zip(report_names,sys.argv[3:])}
r={'verdict':'ACCEPT_SCOPED_PREWRITE_PLAN_CONDITIONAL_ON_VERIFIED_IMMUTABLE_LINK_REBIND',
'baseline_commit':p['baseline_commit'],'plan_safe_sha256':sha((base/'NATIVE_PLAN_SAFE.json').read_bytes()),
'private_plan_sha256':sha((base/'NATIVE_PLAN.json').read_bytes()),'guard_snapshot_sha256':sha((base/'NATIVE_EXPECTED_ALL_CELLS.json').read_bytes()),
'report_commit':p['report_commit'],'commit_placeholder':p['commit_placeholder'],
'exact_target_count':50,'history_preserving_prepends':47,'current_census_replacement':1,'activity_status_changes':status,
'masks':dict(collections.Counter(x['fields'] for x in plans)),
'historical_rich_runs_preserved_by_utf16_offset':rich,'notes_unchanged':notes,'guard_cells':1955,'non_target_guard_cells_unchanged':1905,
'overview_unique_ids':327,'baseline_census':dict(before_counts),'expected_census':dict(after_counts),
'numeric_priority_proof_novelty_columns_untouched':True,'external_writes_performed_by_reviewer':False,
'worker_report_sha256':{n:sha(f.read_bytes()) for n,f in reports.items()},
'release_conditions':['Replace only the 40-zero report-commit placeholders with a verified immutable publication commit; all other strings, targets and masks must remain equal.','Immediately before mutation, compare all guarded live CellData with captured preimages; stop on drift.','After mutation, read back the exact targets, preserved metadata, untouched guards and full 327-ID census.','This acceptance covers administrative activity archival for Q32/ALG-057, not completion of their deferred obligations.'],
'exact_targets':[{'sheet':x['sheet'],'cell':x['cell'],'stable_id':x['stable_id'],'operation':x['operation'],'fields':x['fields']} for x in plans]}
out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['exact_targets','worker_report_sha256','release_conditions']},indent=2))
