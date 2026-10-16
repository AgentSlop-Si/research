"""Self-authored inert-data native-readback verifier; never executes source code.
Arguments: expected-cells.json before-native.json after-native.json before-metadata.json after-metadata.json result.json
"""
from pathlib import Path
import json,sys,copy,collections,hashlib

def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def flat(x):
    out={}
    for s in x['structuredContent']['sheets']:
        for g in s.get('data',[]):
            for r,row in enumerate(g.get('rowData',[]),g.get('startRow',0)):
                for c,v in enumerate(row.get('values',[]),g.get('startColumn',0)):
                    k=(s['properties']['title'],r,c)
                    assert k not in out or out[k]==v
                    out[k]=v
    return out
def norm(v):
    out=copy.deepcopy(v)
    for run in out.get('textFormatRuns',[]):
        run.setdefault('startIndex',0)
        run.setdefault('format',{})
    return out
e,b,a,bm,am,o=sys.argv[1:]
expected={(x['sheet'],x['row_index'],x['column_index']):x for x in load(e)}
before,after=flat(load(b)),flat(load(a))
assert set(before)==set(after)==set(expected)
diff=[];changed=[]
for k,v in before.items():
    assert norm(v)==norm(expected[k]['before'])
    if norm(after[k])!=norm(expected[k]['after']):diff.append(list(k))
    if norm(v)!=norm(after[k]):changed.append(k)
assert not diff,diff
assert len(changed)==34
assert load(bm)['structuredContent']==load(am)['structuredContent']
ids=[after['Research overview',r,1]['userEnteredValue']['stringValue'] for r in range(4,331)]
census=collections.Counter(after['Research overview',r,4]['userEnteredValue']['stringValue'] for r in range(4,331))
assert len(set(ids))==327 and dict(census)=={'CLOSED':87,'TO RESEARCH':240}
status=[]
for r in range(4,331):
    assert before['Research overview',r,1]==after['Research overview',r,1]
    assert before['Research overview',r,11]==after['Research overview',r,11]
    if before['Research overview',r,4]!=after['Research overview',r,4]:
        status.append(after['Research overview',r,1]['userEnteredValue']['stringValue'])
assert set(status)=={'ALG-050','STRUCTURED-RESIDUAL-EXECUTOR-20261012'}
result={'decision':'PASS_NATIVE_POSTWRITE','guard_cells':len(before),'changed_cells':len(changed),'unchanged_guard_cells':len(before)-len(changed),'census':dict(census),'unique_ids':len(set(ids)),'only_status_changes':status,'all_numeric_priorities_unchanged':True,'full_sheet_metadata_unchanged':True,'all_expected_cells_match':True,'normalization':'Only protobuf-default rich-run startIndex=0 and format={} omissions normalized. All other requested CellData compared exactly.','before_native_sha256':sha(b),'after_native_sha256':sha(a),'expected_cells_sha256':sha(e),'before_metadata_sha256':sha(bm),'after_metadata_sha256':sha(am),'source_programs_executed':False}
Path(o).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
