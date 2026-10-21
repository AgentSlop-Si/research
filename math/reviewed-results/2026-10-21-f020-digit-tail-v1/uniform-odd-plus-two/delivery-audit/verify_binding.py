#!/usr/bin/env python3
"""Verify this detached audit and, optionally, its exact bound main archive."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,stat,struct,zipfile,zlib
ROOT=Path(__file__).resolve().parent
MAIN='f020-uniform-odd-plus-two-public-20261021_v3'
MAIN_SHA='8513904de5d101d40170bd05ed7b9070a1f658611b8d007c2457da82a90dc501'
MANIFEST_SHA='29fe6496e20c1e2d5f14e34bf335a07e99232803d1f7dd2205816c34137c180a'
SEAL_SHA='c1e28c5ae7734d2e4a55b9e4e2ce30389bc2d5ad181b28bc582e03d6c0e55239'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def pairs(ps):
 d={}
 for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in()).throw(ValueError('nonfinite JSON')))
def safe(n):
 p=PurePosixPath(n);need(n==str(p)and not p.is_absolute()and '..'not in p.parts and '\\'not in n and ':'not in n and all(ord(c)>=32 for c in n),'unsafe path')
def manifest(files,pin):
 need(H(files['MANIFEST.json'])==pin,'manifest pin');m=parse(files['MANIFEST.json']);need(parse(files['SEAL.json'])['manifest_sha256']==pin,'manifest seal');seen={'MANIFEST.json','SEAL.json'}
 for row in m['files']:
  n=row['path'];safe(n);need(n not in seen,'duplicate manifest path');seen.add(n);b=files[n];need(type(row['bytes'])is int and row['bytes']>=0 and len(b)==row['bytes']and H(b)==row['sha256'],'file identity')
 need(seen==set(files),'exact inventory');return len(files)
def audit():
 need(not ROOT.is_symlink(),'root symlink');files={};dirs=set()
 for p in ROOT.rglob('*'):
  need(not p.is_symlink(),'audit symlink')
  if p.is_file():files[p.relative_to(ROOT).as_posix()]=p.read_bytes()
  elif p.is_dir():dirs.add(p.relative_to(ROOT).as_posix())
  else:raise ValueError('special file')
 expected={str(p)for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need(dirs==expected,'extra directory');s=parse(files['SEAL.json']);count=manifest(files,s['manifest_sha256']);v=parse(files['VERDICT.json']);need(v['status']=='ACCEPTED_PUBLIC_PACKAGE_WITHIN_STATED_SCOPE'and v['main_archive_sha256']==MAIN_SHA and v['main_manifest_sha256']==MANIFEST_SHA and v['main_seal_sha256']==SEAL_SHA,'audit verdict binding');return count
def archive(path):
 raw=path.read_bytes();need(H(raw)==MAIN_SHA and len(raw)==18647129,'main archive identity');members={};locals=[];centrals=[];offset=0
 with zipfile.ZipFile(io.BytesIO(raw))as z:
  for i in z.infolist():
   n=i.filename;safe(n);need(n==i.orig_filename and n not in members and not i.is_dir()and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG,'archive member safety');members[n]=z.read(i)
  need(z.namelist()==sorted(members),'canonical member order')
 names=sorted(members);need(len({n.casefold()for n in names})==len(names),'case collision')
 for n in names:
  b=members[n];nb=n.encode('ascii');crc=zlib.crc32(b)&0xffffffff;size=len(b);local=struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,33,crc,size,size,len(nb),0)+nb+b;central=struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,788,20,0,0,0,33,crc,size,size,len(nb),0,0,0,0,0o100644<<16,offset)+nb;locals.append(local);centrals.append(central);offset+=len(local)
 central=b''.join(centrals);canonical=b''.join(locals)+central+struct.pack('<IHHHHIIH',0x06054b50,0,0,len(names),len(names),len(central),offset,0);need(raw==canonical,'full canonical ZIP bytes');need({n.split('/')[0]for n in names}=={MAIN},'archive root');files={n[len(MAIN)+1:]:b for n,b in members.items()};need(H(files['SEAL.json'])==SEAL_SHA,'main seal identity');count=manifest(files,MANIFEST_SHA);need(count==571,'main file count');return count
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);a=p.parse_args();result={'status':'PASS','detached_audit_files':audit(),'main_archive_sha256':MAIN_SHA,'main_archive_checked':False}
 if a.archive:result.update(main_archive_checked=True,main_archive_files=archive(a.archive),full_canonical_archive_verified=True)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
