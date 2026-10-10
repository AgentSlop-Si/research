from pathlib import Path,PurePosixPath
from zipfile import ZipFile
import hashlib,json,stat
base=Path('materials_2115/multistage')
master=Path('fft_research_master_20261009')
known={}
for p in master.rglob('*'):
 if p.is_file(): known.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(),[]).append(str(p.relative_to(master)))
records=[]
for zpath in sorted((base/'sources').glob('*.zip')):
 root=base/'extracted'/zpath.stem
 root.mkdir()
 with ZipFile(zpath) as z:
  infos=z.infolist(); assert sum(x.file_size for x in infos)<100_000_000
  for i in infos:
   p=PurePosixPath(i.filename)
   assert not p.is_absolute() and '..' not in p.parts and not stat.S_ISLNK(i.external_attr>>16)
   if i.is_dir(): continue
   out=root.joinpath(*p.parts); out.parent.mkdir(parents=True,exist_ok=True)
   assert not out.exists()
   data=z.read(i); out.write_bytes(data); out.chmod(0o444)
   h=hashlib.sha256(data).hexdigest()
   records.append({'archive':zpath.name,'member':i.filename,'size':len(data),'sha256':h,'master_matches':known.get(h,[])})
  zpath.chmod(0o444)
checks=[]
for p in (base/'extracted').rglob('SHA256SUMS*'):
 for line in p.read_text().splitlines():
  if not line.strip(): continue
  h,name=line.split(maxsplit=1); name=name.lstrip('* ')
  q=p.parent/name
  checks.append({'manifest':str(p.relative_to(base)),'member':name,'ok':q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==h})
summary={'source_archives':[{'name':p.name,'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((base/'sources').glob('*.zip'))], 'member_count':len(records),'byte_new_member_count':sum(not r['master_matches'] for r in records),'all_embedded_checks_pass':all(c['ok'] for c in checks),'embedded_check_count':len(checks),'records':records,'checks':checks}
(base/'research/SOURCE_COMPARISON.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('records','checks')},indent=2))
