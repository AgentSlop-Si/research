import ast, pathlib, json, re, hashlib, zipfile
R=pathlib.Path('materials_1954'); inv=json.loads((R/'content_inventory.json').read_text());res={'source_code_executed':False,'source_code_imported':False,'source_code_compiled':False,'archives':[]}
for a in inv:
 item={'archive':a['archive'],'sha256':a['sha256'],'crc_ok':True,'manifest_entries':[],'python_syntax':[],'json_parse':[]}
 with zipfile.ZipFile(R/'originals'/a['archive']) as z:item['crc_ok']=z.testzip() is None
 for f in a['files']:
  p=R/f['path']
  if p.suffix=='.py':
   try:ast.parse(p.read_text(),filename=str(p));item['python_syntax'].append({'member':f['member'],'ok':True})
   except Exception as e:item['python_syntax'].append({'member':f['member'],'ok':False,'error':str(e)})
  if p.suffix=='.json':
   try:json.loads(p.read_text());item['json_parse'].append({'member':f['member'],'ok':True})
   except Exception as e:item['json_parse'].append({'member':f['member'],'ok':False,'error':str(e)})
  entries=[]
  if p.name in ('MANIFEST.sha256','SHA256SUMS.txt'):
   for line in p.read_text().splitlines():
    ma=re.match(r'^([0-9a-fA-F]{64})\s+\*?(.+)$',line)
    if ma:entries.append((ma.group(2),ma.group(1),None))
  if p.name=='MANIFEST.json':
   d=json.loads(p.read_text())
   entries=[(n,v['sha256'],v.get('bytes')) for n,v in d.get('files',{}).items()]
  for name,h,size in entries:
   q=p.parent/name
   ok=q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==h and (size is None or q.stat().st_size==size)
   item['manifest_entries'].append({'manifest':f['member'],'member_relative':name,'sha256':h,'verified':ok})
 res['archives'].append(item)
res['counts']={'archives':len(inv),'first_level_members':sum(a['file_count'] for a in inv),'first_level_unique_contents':len({f['sha256'] for a in inv for f in a['files']}),'byte_new_occurrences':sum(a['novel_content_count'] for a in inv),'byte_new_unique_contents':len({f['sha256'] for a in inv for f in a['files'] if not f['master_matches'] and not f['master_archive_member_matches']}),'verified_manifest_entries':sum(sum(x['verified'] for x in a['manifest_entries']) for a in res['archives']),'manifest_entries':sum(len(a['manifest_entries']) for a in res['archives']),'syntax_parsed_python':sum(len(a['python_syntax']) for a in res['archives']),'json_parsed':sum(len(a['json_parse']) for a in res['archives'])}
(R/'STATIC_VALIDATION.json').write_text(json.dumps(res,indent=2));print(json.dumps(res['counts'],indent=2));print('FAILURES',[a['archive'] for a in res['archives'] if not a['crc_ok'] or any(not x['verified'] for x in a['manifest_entries']) or any(not x['ok'] for x in a['python_syntax']+a['json_parse'])])
for a in inv:
 print('\n',a['archive'])
 for f in a['files']:
  if a['novel_content_count'] and (f['master_matches'] or f['master_archive_member_matches']):print(f['member'],(f['master_matches']+f['master_archive_member_matches'])[:4])
