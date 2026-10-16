"""Read-only independent native/readback and immutable report validation.
Usage: python check_terminal_native.py independent_directory publisher_private_directory
Raw remote captures and preimages are inputs, never included in this public script.
"""
import collections,copy,hashlib,json,pathlib,re,sys
root=pathlib.Path(sys.argv[1]);pub=pathlib.Path(sys.argv[2]);private=root/'private'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def cells(data):
 out={}
 for sheet in data['structuredContent']['sheets']:
  for grid in sheet.get('data',[]):
   for r,row in enumerate(grid.get('rowData',[]),grid.get('startRow',0)):
    for c,cell in enumerate(row.get('values',[]),grid.get('startColumn',0)):
     key=(sheet['properties']['title'],r,c)
     assert key not in out or out[key]==cell
     out[key]=cell
 return out
fields={'userEnteredValue','userEnteredFormat','note','textFormatRuns','chipRuns','dataValidation'}
selected=lambda cell:{k:v for k,v in cell.items() if k in fields}
def address(s):
 m=re.fullmatch('([A-Z]+)([0-9]+)',s);assert m;c=0
 for x in m[1]:c=c*26+ord(x)-64
 return int(m[2])-1,c-1
before={}
for file in ['BASELINE_OVERVIEW_NATIVE.json','BASELINE_TARGETS_NATIVE.json','BASELINE_PROGRESS_NATIVE.json']:
 for k,v in cells(load(private/file)).items():
  assert k not in before or selected(before[k])==selected(v)
  before[k]=v
post=cells(load(private/'TERMINAL_NATIVE_READBACK.json'))
assert set(post)==set(before)
accepted=load(pub/'ACCEPTED_NATIVE_PLAN.json');plan=load(pub/'NATIVE_PLAN.json')
assert sha(pub/'ACCEPTED_NATIVE_PLAN.json')=='8afb9986cfef04f0189b381de86525cc0ffc7bf15ac9f9c03ac0517d8519982b'
report_commit='a462b0f54fc0e05da1fe689b7d1de665bd147944'
expected_plan=json.loads(json.dumps(accepted).replace('0'*40,report_commit));expected_plan['commit_placeholder']=False
assert expected_plan==plan
expected=copy.deepcopy(before);seen=set()
for item in plan['plans']:
 key=(item['sheet'],*address(item['cell']));assert key not in seen;seen.add(key)
 assert selected(before[key])==selected(item['before_cell'])
 expected[key]['userEnteredValue']={'stringValue':item['after']}
 assert item['after']==item['prefix']+'\n\nEarlier dated history (preserved verbatim):\n'+item['before']
assert all(selected(post[k])==selected(expected[k]) for k in expected)
changed={k for k in before if selected(before[k])!=selected(post[k])};assert changed==seen
for k in set(before)-seen:assert post[k].get('hyperlink')==before[k].get('hyperlink') or k[0]!='Research overview'
value=lambda r,c:next(iter(post['Research overview',r,c].get('userEnteredValue',{}).values()),None)
assert len(set(value(r,1) for r in range(4,331)))==327
census=collections.Counter(value(r,4) for r in range(4,331));assert census=={'CLOSED':87,'TO RESEARCH':240}
for r in range(4,331):
 for c in (0,1,3,4,11,12):assert selected(post['Research overview',r,c])==selected(before['Research overview',r,c])
allow=load(pub/'PUBLICATION_ALLOWLIST.json');assert sha(pub/'PUBLICATION_ALLOWLIST.json')=='c17a2c9065702cfb2a17cd92a1a94bce93697f07e1026f096f58f24c7143eb67'
remote=load(private/'REPORT_REMOTE_ALL.json');assert remote['commit']==report_commit
entries={e['path']:e for e in allow['files']};assert set(entries)=={r['path'] for r in remote['files']}
for r in remote['files']:
 c=r['result']['structuredContent'];content=c['content'].encode();entry=entries[r['path']]
 assert len(content)==entry['bytes']
 assert hashlib.sha256(content).hexdigest()==entry['sha256']
 assert hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()==entry['git_blob_sha']==c['sha']
compare=load(private/'REPORT_COMMIT_COMPARE_REMOTE.json')['structuredContent']
assert compare['ahead_by']==compare['total_commits']==1 and compare['behind_by']==0
assert {f['filename'] for f in compare['files']}==set(entries)
assert all(f['status']=='added' and f['deletions']==0 for f in compare['files'])
print(json.dumps({'verdict':'PASS','report_commit':report_commit,'report_files_verified':len(entries),'report_bytes_verified':sum(e['bytes'] for e in entries.values()),'report_commit_added_allowlist_only':True,'mechanical_immutable_rebind_only':True,'bound_plan_sha256':sha(pub/'NATIVE_PLAN.json'),'independently_read_native_cells':len(post),'exact_authorized_cell_changes':len(changed),'untouched_native_cells':len(post)-len(changed),'all_captured_notes_formats_rich_runs_chips_validations_preserved':True,'all_target_old_suffixes_preserved':True,'all_overview_identities_statuses_priorities_unchanged':True,'census':dict(census),'unique_overview_ids':327,'no_parent_closures':True,'final_index_seal_commit_pending':True},indent=2))
