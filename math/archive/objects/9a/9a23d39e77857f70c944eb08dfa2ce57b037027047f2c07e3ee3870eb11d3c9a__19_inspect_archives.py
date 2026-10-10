import os,json,zipfile,hashlib,pathlib,stat,collections
R=pathlib.Path('materials_1954'); M=pathlib.Path('fft_research_master_20261009')
sha=lambda b:hashlib.sha256(b).hexdigest()
index=collections.defaultdict(list)
for p in M.rglob('*'):
 if p.is_file() and not p.is_symlink():
  index[sha(p.read_bytes())].append(str(p.relative_to(M)))
archives=[]
for p in sorted((R/'originals').glob('*.zip')):
 info={'archive':p.name,'sha256':sha(p.read_bytes()),'master_archive_matches':index.get(sha(p.read_bytes()),[]),'files':[]}; dest=R/'extracted'/p.stem
 with zipfile.ZipFile(p) as z:
  if sum(x.file_size for x in z.infolist())>150_000_000:raise ValueError('Oversized archive')
  for zi in z.infolist():
   rel=pathlib.PurePosixPath(zi.filename)
   if rel.is_absolute() or '..' in rel.parts or stat.S_ISLNK(zi.external_attr >>16):raise ValueError('Unsafe ZIP entry')
   if zi.is_dir():continue
   b=z.read(zi); q=dest/pathlib.Path(*rel.parts);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
   h=sha(b);info['files'].append({'path':str(q.relative_to(R)),'member':zi.filename,'bytes':len(b),'sha256':h,'master_matches':index.get(h,[])})
 info['file_count']=len(info['files']);info['novel_file_count']=sum(not f['master_matches'] for f in info['files']);archives.append(info)
(R/'content_inventory.json').write_text(json.dumps(archives,indent=2))
for a in archives:
 print('\nARCHIVE',a['archive'],'files',a['file_count'],'novel',a['novel_file_count'],'archive_match',a['master_archive_matches'])
 for f in a['files']:
  if not f['master_matches']:print(' NEW',f['member'],f['bytes'])
