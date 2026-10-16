"""Independent exact prewrite checker. No network access or external writes.

Usage: python check_native_plan.py plan.json baseline_native.json [...]
Produces a compact JSON verdict on stdout. Native captures stay outside this file.
"""
import collections,copy,hashlib,json,re,sys

def native_cells(snapshot):
    cells={}
    for sheet in snapshot['structuredContent']['sheets']:
        for grid in sheet.get('data',[]):
            for row,line in enumerate(grid.get('rowData',[]),grid.get('startRow',0)):
                for col,value in enumerate(line.get('values',[]),grid.get('startColumn',0)):
                    cells[sheet['properties']['title'],row,col]=value
    return cells

def selected(value):
    return {key:val for key,val in value.items() if key in {
        'userEnteredValue','userEnteredFormat','note','textFormatRuns','chipRuns','dataValidation'}}

def position(address):
    match=re.fullmatch(r'([A-Z]+)([0-9]+)',address)
    assert match
    col=0
    for ch in match[1]:col=26*col+ord(ch)-64
    return int(match[2])-1,col-1

plan=json.load(open(sys.argv[1]));baseline={}
for path in sys.argv[2:]:
    for key,value in native_cells(json.load(open(path))).items():
        if key in baseline:assert selected(baseline[key])==selected(value)
        baseline[key]=value
assert len(plan['plans'])==len(plan['requests'])==79
assert plan['baseline_commit']=='0339a31eb6109f0b96074ab8321f8653641e7530'
allowed_owners={'F020','ALG-048','ALG-036','ALG-042','ALG-052','M-NILPOTENT-FOLD','M-SYMMETRY'}
separator='\n\nEarlier dated history (preserved verbatim):\n'
seen=set();notes=0;guards=copy.deepcopy(baseline)
for item,request in zip(plan['plans'],plan['requests']):
    key=(item['sheet'],*position(item['cell']))
    assert key not in seen;seen.add(key)
    old=selected(baseline[key]);assert old==selected(item['before_cell'])
    assert set(old['userEnteredValue'])=={'stringValue'}
    assert item['operation']=='prepend_preserving_history'
    assert item['after']==item['prefix']+separator+item['before']
    assert item['before']==old['userEnteredValue']['stringValue']
    expected=copy.deepcopy(old);expected['userEnteredValue']={'stringValue':item['after']}
    assert expected==selected(item['expected_after_cell'])
    assert len(item['after'].encode('utf-16-le'))//2 < 50000
    notes+=bool(old.get('note'))
    assert not old.get('textFormatRuns') and not old.get('chipRuns')
    mutation=request['updateCells'];r,c=key[1:]
    assert mutation['range']=={'sheetId':item['sheet_id'],'startRowIndex':r,
        'endRowIndex':r+1,'startColumnIndex':c,'endColumnIndex':c+1}
    assert mutation['fields']=='userEnteredValue'
    assert mutation['rows']==[{'values':[{'userEnteredValue':expected['userEnteredValue']}]}]
    if key[0]=='Progress':assert item['cell']=='C7'
    else:
        owner=item['stable_id'];assert owner in allowed_owners
        idcol={'Catalogue':0,'novelity breakthough':2,'Research overview':1}.get(key[0])
        if idcol is not None:
            assert baseline[key[0],r,idcol]['userEnteredValue']['stringValue']==owner
        else:assert key[0]=='Theorem register' and r==21 and owner=='F020'
    guards[key]=expected

value=lambda cells,row,col:next(iter(cells['Research overview',row,col].get('userEnteredValue',{}).values()),None)
ids=[value(baseline,r,1) for r in range(4,331)]
assert len(ids)==len(set(ids))==327
assert collections.Counter(value(baseline,r,4) for r in range(4,331))=={'CLOSED':87,'TO RESEARCH':240}
for row in range(4,331):
    for col in (0,1,3,4,11,12):
        assert selected(baseline['Research overview',row,col])==selected(guards['Research overview',row,col])
assert notes==8
print(json.dumps({'verdict':'PASS','targets':len(seen),'target_notes_preserved':notes,
 'target_rich_runs':0,'native_preimage_cells':len(baseline),'complete_old_text_preserved':True,
 'value_only_masks':True,'unique_overview_ids':327,'census':{'closed':87,'open':240},
 'all_overview_identity_status_priority_cells_unchanged':True,
 'placeholder_commit':plan['commit_placeholder'],
 'plan_sha256':hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()},indent=2))
