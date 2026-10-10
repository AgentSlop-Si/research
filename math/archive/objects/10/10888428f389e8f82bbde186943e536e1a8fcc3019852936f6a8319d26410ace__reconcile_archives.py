"""Fresh reviewer utility: reads ZIP/JSON/checksum data only, never source execution."""
import pathlib,json,hashlib,zipfile,re,posixpath
P=pathlib.Path(__file__).parent;rs=json.loads((P/'SOURCE_MANIFEST.json').read_text());roots=json.loads((P/'provenance/ARCHIVE_ROOTS.json').read_text());out=P/'provenance/archive_data';out.mkdir(exist_ok=True)
graph={a['sha256']:a for a in json.loads(pathlib.Path('code_coverage_audit_0228/ARCHIVE_GRAPH.json').read_text())};byhash={r['sha256']:r for r in rs};ars=sorted({o['archive_sha256'] for r in rs for o in r['occurrences'] if o['kind']=='archive_member'});records=[];results=[];checksum_checks=[];reference_checks=[]
for ah in ars:
 candidates=[pathlib.Path(r['path']) if pathlib.Path(r['path']).is_absolute() else pathlib.Path('fft_research_master_20261009')/r['path'] for r in roots if r['sha256']==ah]
 ap=next((p for p in candidates if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==ah),None)
 if ap is None:records.append({'archive_sha256':ah,'status':'archive_unavailable','candidate_paths':[str(p) for p in candidates]});continue
 with zipfile.ZipFile(ap) as z:
  infos=z.infolist();members={i.filename:(j,i) for j,i in enumerate(infos) if not i.is_dir()};hashes={};occ=[];dirs=set()
  for r in rs:
   for o in r['occurrences']:
    if o.get('archive_sha256')!=ah:continue
    info=infos[o['member_index']];assert info.filename==o['name'];raw=z.read(info);actual=hashlib.sha256(raw).hexdigest();assert actual==r['sha256'] and len(raw)==r['size_bytes'];occ.append({'source_sha256':r['sha256'],'member_index':o['member_index'],'member_name':info.filename,'bytes':len(raw),'match':True});dirs.add(posixpath.dirname(info.filename))
  def digest(name):
   if name not in hashes:hashes[name]=hashlib.sha256(z.read(members[name][1])).hexdigest()
   return hashes[name]
  for name,(ix,info) in members.items():
   parent=posixpath.dirname(name);base=posixpath.basename(name)
   if parent in dirs and re.search(r'(SHA256SUMS|MANIFEST|CHECKSUM)',base,re.I) and info.file_size<2000000:
    raw=z.read(info)
    try:txt=raw.decode()
    except UnicodeDecodeError:continue
    loc=out/(ah[:12]+'__'+name.replace('/','__'));loc.write_bytes(raw)
    for lno,line in enumerate(txt.splitlines(),1):
     m=re.match(r'^([a-fA-F0-9]{64})\s+\*?(.+?)\s*$',line)
     if not m:continue
     want,rel=m.groups();target=posixpath.normpath(posixpath.join(parent,rel));found=target if target in members else rel if rel in members else None
     checksum_checks.append({'archive_sha256':ah,'manifest_member':name,'line':lno,'target':target,'expected_sha256':want.lower(),'actual_sha256':digest(found) if found else None,'match':digest(found)==want.lower() if found else None})
   eligible=(parent in dirs or posixpath.basename(parent)=='results' and posixpath.dirname(parent) in dirs) and info.file_size<2000000 and base.lower().endswith('.json') and re.search(r'(result|audit|certificat|benchmark|verification)',base,re.I)
   if not eligible:continue
   raw=z.read(info)
   try:obj=json.loads(raw)
   except Exception:continue
   loc=out/(ah[:12]+'__'+name.replace('/','__'));loc.write_bytes(raw)
   top={k:v for k,v in obj.items() if not isinstance(v,(list,dict))} if isinstance(obj,dict) else {'list_length':len(obj) if isinstance(obj,list) else None}
   results.append({'archive_sha256':ah,'archive_path':str(ap),'member_index':ix,'member_name':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'snapshot':str(loc.relative_to(P)),'stored_status_only':top,'current_review_execution':'none'})
   def walk(x,path):
    if isinstance(x,dict):
     for k,v in x.items():
      if isinstance(v,str) and re.fullmatch('[a-f0-9]{64}',v):
       candidate_names=[]
       for cand in (posixpath.normpath(posixpath.join(parent,k)),posixpath.normpath(posixpath.join(name.split('/')[0],k)),k):
        if cand in members and cand not in candidate_names:candidate_names.append(cand)
       if not candidate_names and re.search(r'\.(py|cpp|md|zip)$',k):candidate_names=[q for q in members if q.endswith('/'+k)]
       if not candidate_names:
        candidate_names=[m['name'] for m in graph.get(ah,{}).get('members',[]) if m.get('sha256')==v and m['name'] in members]
       matches=[q for q in candidate_names if digest(q)==v]
       reference_checks.append({'archive_sha256':ah,'result_member':name,'json_path':path+[k],'declared_sha256':v,'in_assigned_sources':v in byhash,'candidate_members':candidate_names,'matching_members':matches,'resolution':'exact_member_match' if matches else 'member_hash_mismatch' if candidate_names else 'no_unambiguous_member_path','assigned_source_path':byhash[v]['representative_path'] if v in byhash else None})
      else:walk(v,path+[k])
    elif isinstance(x,list):
     for j,v in enumerate(x):walk(v,path+[j])
   walk(obj,[])
  records.append({'archive_sha256':ah,'archive_path':str(ap),'archive_size_bytes':ap.stat().st_size,'status':'opened_and_hash_verified','source_occurrences':occ,'all_selected_source_occurrences_rehashed':True})
for name,obj in [('ARCHIVE_RECONCILIATION.json',records),('STORED_RESULTS.json',results),('ARCHIVE_CHECKSUM_RECONCILIATION.json',checksum_checks),('STORED_HASH_REFERENCES.json',reference_checks)]: (P/name).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'archives':len(records),'opened':sum(x['status']=='opened_and_hash_verified' for x in records),'source_occurrences':sum(len(x.get('source_occurrences',[])) for x in records),'stored_results':len(results),'checksums':len(checksum_checks),'checksum_match':sum(x['match'] is True for x in checksum_checks),'checksum_mismatch':sum(x['match'] is False for x in checksum_checks),'hash_references':len(reference_checks),'reference_match':sum(x['resolution']=='exact_member_match' for x in reference_checks),'reference_mismatch':sum(x['resolution']=='member_hash_mismatch' for x in reference_checks)},indent=2))
print('MISMATCHES',json.dumps([x for x in reference_checks if x['resolution']=='member_hash_mismatch'],indent=2)[:20000])
