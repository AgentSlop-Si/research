import tarfile,zipfile,lzma,hashlib,json,time
from pathlib import Path
src=Path('master_v25_integration_20261010/fft_research_master_v25_20261010.zip')
out=Path('v25_delivery/fft_research_master_checkpoint25_20261010.tar.xz')
records={}; start=time.time()
with zipfile.ZipFile(src) as z, lzma.open(out,'wb',preset=8) as compressed, tarfile.open(fileobj=compressed,mode='w|') as tar:
 for i,entry in enumerate(z.infolist()):
  if entry.is_dir(): continue
  info=tarfile.TarInfo(entry.filename);info.size=entry.file_size;info.mode=0o644;info.mtime=0
  with z.open(entry) as f: tar.addfile(info,f)
  records[entry.filename]=hashlib.sha256(z.read(entry)).hexdigest()
  if i%1000==0:print(i,round(time.time()-start,1),flush=True)
seen={}
with tarfile.open(out,'r:xz') as t:
 for entry in t:
  assert entry.isfile(); f=t.extractfile(entry);seen[entry.name]=hashlib.sha256(f.read()).hexdigest()
assert seen==records
result=dict(path=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),files=len(seen),all_member_paths_and_bytes_match_verified_zip=True,original_zip_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),elapsed_seconds=time.time()-start)
(out.parent/'SOLID_ARCHIVE_VERIFICATION.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
