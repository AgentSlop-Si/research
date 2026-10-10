import pathlib,json,zipfile,hashlib,collections,io
R=pathlib.Path('materials_1954');M=pathlib.Path('fft_research_master_20261009');ix=collections.defaultdict(list);seen=set();counts={'archive_containers_opened':0,'member_occurrences':0,'uncompressed_bytes_read':0}
def scan(blob,path,depth=0):
 h=hashlib.sha256(blob).hexdigest()
 if h in seen:return
 seen.add(h)
 if depth>20:raise ValueError('Archive depth exceeds limit')
 try:z=zipfile.ZipFile(io.BytesIO(blob))
 except zipfile.BadZipFile:return
 counts['archive_containers_opened']+=1
 with z:
  for zi in z.infolist():
   if zi.is_dir():continue
   if zi.file_size>150_000_000:raise ValueError('Oversize member')
   b=z.read(zi);hh=hashlib.sha256(b).hexdigest();where=path+'::'+zi.filename;ix[hh].append(where);counts['member_occurrences']+=1;counts['uncompressed_bytes_read']+=len(b)
   if counts['uncompressed_bytes_read']>1_000_000_000:raise ValueError('Total read budget')
   if zi.filename.lower().endswith('.zip'):scan(b,where,depth+1)
for p in M.rglob('*.zip'):scan(p.read_bytes(),str(p.relative_to(M)))
A=json.loads((R/'content_inventory.json').read_text())
for a in A:
 for f in a['files']:f['master_recursive_archive_matches']=ix.get(f['sha256'],[])
 a['novel_content_count']=sum(not f['master_matches'] and not f['master_recursive_archive_matches'] for f in a['files'])
 print(a['archive'],a['novel_content_count'])
(R/'content_inventory.json').write_text(json.dumps(A,indent=2));counts['comparison_scope']='All regular master files plus recursively read unique master ZIP containers, without executing code';counts['master_manifest_sha256']=hashlib.sha256((M/'SHA256SUMS').read_bytes()).hexdigest();(R/'COMPARISON_SCOPE.json').write_text(json.dumps(counts,indent=2));print(counts)
