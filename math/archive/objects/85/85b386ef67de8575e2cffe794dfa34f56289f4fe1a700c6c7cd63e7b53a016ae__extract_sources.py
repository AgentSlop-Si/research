from pathlib import Path,PurePosixPath
import zipfile,hashlib,json,stat
root=Path(__file__).resolve().parent
master=Path('fft_research_master_20261009')
known={}
for p in master.rglob('*'):
 if p.is_file(): known.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(),[]).append(str(p.relative_to(master)))
manifest=[]
for archive in sorted((root/'original').glob('*.zip')):
 dest=root/'extracted'/archive.stem; dest.mkdir(parents=True,exist_ok=True)
 rows=[]; seen=set(); size=0
 with zipfile.ZipFile(archive) as z:
  for f in z.infolist():
   p=PurePosixPath(f.filename)
   assert not p.is_absolute() and '..' not in p.parts and '\\' not in f.filename
   assert not stat.S_ISLNK(f.external_attr>>16)
   if f.is_dir(): continue
   assert f.filename not in seen;seen.add(f.filename)
   size+=f.file_size; assert size<40_000_000 and f.file_size<20_000_000
   b=z.read(f);h=hashlib.sha256(b).hexdigest(); out=dest/f.filename;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b);out.chmod(0o444)
   rows.append({'path':f.filename,'bytes':len(b),'sha256':h,'master_matches':known.get(h,[])})
 archive.chmod(0o444)
 manifest.append({'archive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'members':rows})
(root/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
for a in manifest: print(a['archive'],a['sha256'],len(a['members']),'members',sum(not x['master_matches'] for x in a['members']),'byte new');print('\n'.join(x['path'] for x in a['members'] if x['path'].endswith('.md')))
