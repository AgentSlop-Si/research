"""Fresh inert checker for archived manifests and source-digest declarations."""
import json,pathlib,zipfile,hashlib,posixpath,re,collections
P=pathlib.Path(__file__).parent;index=json.loads((P/'STORED_OUTPUTS_INDEX.json').read_text())
HEX=re.compile(r'^[0-9a-f]{64}$');records=[];archives={}
for x in json.loads((P/'ARCHIVE_PROVENANCE.json').read_text()):
 archives[x['sha256']]=zipfile.ZipFile(P/x['snapshot'])
def entries(obj,prefix=''):
 if isinstance(obj,list):
  for i,x in enumerate(obj):yield from entries(x,prefix+f'/{i}')
 elif isinstance(obj,dict):
  path=obj.get('path',obj.get('filename',obj.get('name')))
  h=obj.get('sha256')
  if path and isinstance(h,str) and HEX.fullmatch(h):yield path,h,prefix
  for k,v in obj.items():
   if isinstance(v,str) and HEX.fullmatch(v) and ('.' in k or '/' in k):yield k,v,prefix
   elif isinstance(v,dict) and isinstance(v.get('sha256'),str) and HEX.fullmatch(v['sha256']) and ('.' in k or '/' in k):yield k,v['sha256'],prefix
   elif isinstance(v,(dict,list)):yield from entries(v,prefix+'/'+k)
for row in index:
 name=row['member_name'];ext=posixpath.splitext(name)[1]
 refs=[]
 if ext=='.json':
  try:refs=list(entries(json.loads((P/row['snapshot']).read_bytes())))
  except Exception:pass
 elif posixpath.basename(name)=='SHA256SUMS.txt':
  for line in (P/row['snapshot']).read_text().splitlines():
   m=re.match(r'^([0-9a-f]{64})\s+\*?(.+)$',line)
   if m:refs.append((m[2],m[1],'text_manifest'))
 if not refs:continue
 z=archives[row['archive_sha256']];names=z.namelist();base=posixpath.dirname(name)
 for fn,h,where in refs:
  exact=posixpath.normpath(posixpath.join(base,fn))
  alternatives=[exact] if exact in names else [n for n in names if n==fn or n.endswith('/'+fn)]
  candidates=[]
  for n in alternatives:
   digest=hashlib.sha256(z.read(n)).hexdigest();candidates.append({'member_name':n,'actual_sha256':digest,'matches':digest==h})
  if exact in names:status='MATCH' if candidates[0]['matches'] else 'MISMATCH'
  elif any(c['matches'] for c in candidates):status='MATCH_OTHER_ARCHIVE_LOCATION'
  elif candidates:status='UNRESOLVED_NONLOCAL_REFERENCE' # same basename is not enough to assert mutation
  else:status='NOT_PRESENT_IN_THIS_CONTAINER'
  records.append({'archive_sha256':row['archive_sha256'],'declaration_member':name,'json_context':where,'declared_path':fn,'declared_sha256':h,'resolution_status':status,'candidates':candidates})
(P/'STORED_INTEGRITY_RECONCILIATION.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(collections.Counter(x['resolution_status'] for x in records)))
for r in records:
 if r['resolution_status']=='MISMATCH':print(json.dumps(r))
