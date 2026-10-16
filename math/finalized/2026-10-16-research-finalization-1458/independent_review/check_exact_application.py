"""Independently authored, data-only checker. Never imports supplied programs.

Usage: python check_exact_application.py PLAN BASELINE EXPECTED STAGE ALLOWLIST OUTPUT
All inputs are inert JSON or text. OUTPUT contains hashes/counts, never raw cells.
"""
import sys, json, hashlib, re, copy, collections
from pathlib import Path

def read(p):
    return json.loads(Path(p).read_text())

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def flatten(obj):
    result = {}
    for sheet in obj['structuredContent']['sheets']:
        for grid in sheet.get('data', []):
            for r, row in enumerate(grid.get('rowData', []), grid.get('startRow', 0)):
                for c, cell in enumerate(row.get('values', []), grid.get('startColumn', 0)):
                    key = (sheet['properties']['title'], r, c)
                    assert key not in result or result[key] == cell
                    result[key] = cell
    return result

def u16(s):
    return len(s.encode('utf-16-le')) // 2

def colnum(s):
    n = 0
    for c in s:
        n = 26*n + ord(c)-64
    return n-1

planfile, baselinefile, expectedfile, stagedir, allowfile, outputfile = sys.argv[1:]
plan, baseline, expected, allow = read(planfile), flatten(read(baselinefile)), read(expectedfile), read(allowfile)
stage = Path(stagedir)
prefixroot = 'math/finalized/2026-10-16-research-finalization-1458/'
allowed = {
    'Catalogue': ['AE84','AF84','AE19','AF19','X174','Y174','Z174','AE174','AF174'],
    'novelity breakthough': ['Y45','Z45','Y20','Z20','Y212','Z212'],
    'Incoming queue': ['F40','K40','L40'],
    'Research overview': ['E62','F62','P62','Q62','C17','E17','F17','P17','Q17','P30','Q30','P300','Q300','E3','A3'],
    'Progress': ['A1']}
allowcells = {(s,a) for s, cells in allowed.items() for a in cells}
assert len(allowcells) == 34
assert {(x['sheet'],x['cell']) for x in plan['plans']} == allowcells
assert len(plan['plans']) == len(plan['requests']) == 34
assert plan['baseline_commit'] == '35d9dcdc3f3869de75b33b2b09705222e8d09e8d'
commit = plan['report_commit']
assert re.fullmatch('[0-9a-f]{40}',commit)
assert plan['commit_placeholder'] == (commit == '0'*40)
changes, oldruns, notes = {}, 0, 0
separator = '\n\nEarlier dated history (preserved verbatim):\n'
replacements = {('Research overview','E62'):'CLOSED',('Research overview','E17'):'CLOSED',('Research overview','A3'):'327 overview records: 240 TO RESEARCH + 87 CLOSED'}
for p, request in zip(plan['plans'],plan['requests']):
    match = re.fullmatch(r'([A-Z]+)(\d+)',p['cell'])
    key = p['sheet'],int(match[2])-1,colnum(match[1])
    assert key == (p['sheet'],p['row_index'],p['column_index'])
    assert key not in changes
    before = baseline[key]
    assert before == p['before_cell']
    assert before['userEnteredValue'] == {'stringValue':p['before']}
    after = copy.deepcopy(before)
    after['userEnteredValue'] = {'stringValue':p['after']}
    fields = ['userEnteredValue']
    if (p['sheet'],p['cell']) in replacements:
        assert p['after'] == replacements[p['sheet'],p['cell']]
        assert p['prefix'] is None and p['prefix_utf16_length'] == 0
        assert not before.get('textFormatRuns') and not before.get('chipRuns')
    else:
        assert p['after'] == p['prefix'] + separator + p['before']
        assert p['prefix'].endswith('/independent_review/INDEPENDENT_REVIEW.md')
        assert p['prefix'].count('https://github.com/AgentSlop-Si/research/blob/'+commit+'/') == 2
        shift = u16(p['prefix']+separator)
        assert shift == p['prefix_utf16_length']
        runs = before.get('textFormatRuns',[])
        oldruns += len(runs)
        if runs:
            newruns = [{'startIndex':0,'format':{}}]
            if runs[0].get('startIndex',0)>0:
                newruns.append({'startIndex':shift,'format':{}})
            for r in runs:
                q = copy.deepcopy(r); q['startIndex']=q.get('startIndex',0)+shift
                newruns.append(q)
            after['textFormatRuns']=newruns; fields.append('textFormatRuns')
        assert not before.get('chipRuns'), 'New chip scope needs independent review'
    notes += bool(before.get('note'))
    assert u16(p['after']) < 50000
    assert after == p['expected_after_cell']
    assert p['fields'].split(',') == fields
    payload = {f:after[f] for f in fields}
    want = {'updateCells':{'start':{'sheetId':p['sheet_id'],'rowIndex':key[1],'columnIndex':key[2]},'rows':[{'values':[payload]}],'fields':','.join(fields)}}
    assert request == p['request'] == want
    changes[key] = after
expectedmap = {(x['sheet'],x['row_index'],x['column_index']):x for x in expected}
assert set(expectedmap) == set(baseline)
for key, cell in baseline.items():
    assert expectedmap[key]['before'] == cell
    assert expectedmap[key]['after'] == changes.get(key,cell)
assert len(baseline)==1747
census=collections.Counter(expectedmap['Research overview',r,4]['after']['userEnteredValue']['stringValue'] for r in range(4,331))
ids=[expectedmap['Research overview',r,1]['after']['userEnteredValue']['stringValue'] for r in range(4,331)]
assert dict(census)=={'CLOSED':87,'TO RESEARCH':240} and len(set(ids))==327
for r in range(4,331):
    assert expectedmap['Research overview',r,11]['after']==baseline['Research overview',r,11]
paths=[x['repository_path'] for x in allow]
assert len(paths)==len(set(paths)) and all(x.startswith(prefixroot) for x in paths)
actual={p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file()}
assert actual==set(paths)
for x in allow:
    assert not any(part in ('private','.git') for part in Path(x['repository_path']).parts)
    dest=stage/x['repository_path']
    if x['source_path']!='publisher-authored':
        assert dest.read_bytes()==Path(x['source_path']).read_bytes()
    text=dest.read_text()
    assert ('/work'+'space/') not in text and ('sediment'+':/')+'/' not in text
    assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY',text)
result={'decision':'PASS_EXACT_PREWRITE','plan_sha256':sha(planfile),'allowlist_sha256':sha(allowfile),'report_commit':commit,'commit_placeholder':plan['commit_placeholder'],'target_count':34,'prefix_count':31,'replacement_count':3,'guard_cells':len(baseline),'preserved_historical_rich_runs':oldruns,'preserved_target_notes':notes,'census':dict(census),'unique_ids':len(set(ids)),'stage_file_count':len(actual),'all_stage_files_match_allowlist':True,'no_source_program_execution':True}
Path(outputfile).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
