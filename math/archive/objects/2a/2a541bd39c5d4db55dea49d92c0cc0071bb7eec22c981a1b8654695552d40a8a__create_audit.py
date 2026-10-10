"""Reproduce the breadth/provenance audit. No user-supplied program execution."""
import zipfile,hashlib,json,glob,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
files=sorted(Path('fft_audit').glob('*.zip'))
files+=sorted(x for x in Path('/mnt/data').glob('FFT_*.zip') if x.name not in {'FFT_PROJECTIVE_GAUGE_RIGIDITY_2026-10-10.zip'})
archive=[]
seen_txt={}
for p in files:
 try:z=zipfile.ZipFile(p)
 except zipfile.BadZipFile:continue
 with z:
  z.bad=z.testzip()
  text_items=0
  for member in z.infolist():
   if member.is_dir():continue
   if member.filename.lower().endswith(('.md','.txt','.json','.py','.csv')) and member.file_size<500000:
    try:
     b=z.read(member.filename)
     seen_txt[hashlib.sha256(b).hexdigest()]=seen_txt.get(hashlib.sha256(b).hexdigest(),0)+1
     text_items+=1
    except Exception:pass
  entry={'archive':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
         'members':len(z.infolist()),'text_like_occurrences':text_items,'crc_ok':z.bad is None}
  archive.append(entry)
res={'date':'2026-10-10','method':'Container archive indexing, CRC and SHA256, targeted mathematical reviews; not line-by-line verification of every proof.',
     'archive_count':len(archive),'member_occurrences':sum(x['members'] for x in archive),
     'text_like_occurrences':sum(x['text_like_occurrences'] for x in archive),
     'unique_text_like_sha256':len(seen_txt),'archives':archive}
(HERE/'AUDIT_MANIFEST.json').write_text(json.dumps(res,indent=2))
print('archives:',len(archive),'members:',res['member_occurrences'],'unique text:',res['unique_text_like_sha256'])
for x in archive:print(x['archive'],x['members'])
