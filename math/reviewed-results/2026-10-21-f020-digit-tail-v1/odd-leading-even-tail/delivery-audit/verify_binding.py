#!/usr/bin/env python3
"""Read-only exhaustive detached-audit and optional exact public-archive verifier."""
import argparse,hashlib,io,json,stat,struct,zipfile,zlib
from pathlib import Path,PurePosixPath

def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(rows):
 d={}
 for k,v in rows:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in()).throw(ValueError('nonfinite JSON')))
def safe(n):
 p=PurePosixPath(n);need(type(n)is str and n==str(p) and not p.is_absolute() and '..'not in p.parts and '\\'not in n and ':'not in n and all(ord(c)>=32 for c in n),'unsafe name');return n
def inventory(root):
 out={}
 need(root.is_dir() and not root.is_symlink(),'bad root')
 for p in root.rglob('*'):
  need(not p.is_symlink(),'symlink')
  n=safe(p.relative_to(root).as_posix())
  if p.is_file():out[n]=p.read_bytes()
  else:need(p.is_dir(),'special file')
 return out
def members_exact(data,manifest):
 expected={'MANIFEST.json','SEAL.json'}
 for row in manifest['files']:
  n=safe(row['path']);need(n not in expected,'duplicate manifest member');expected.add(n)
  need(type(row['bytes'])is int and row['bytes']>=0 and n in data and len(data[n])==row['bytes'] and sha(data[n])==row['sha256'],'member identity')
 need(set(data)==expected,'inventory mismatch')
def audit(root):
 data=inventory(root);m=parse(data['MANIFEST.json']);s=parse(data['SEAL.json']);need(sha(data['MANIFEST.json'])==s['manifest_sha256'],'audit manifest seal');members_exact(data,m)
 for field,name in [('report_sha256','REPORT.md'),('verdict_sha256','VERDICT.json')]:need(s[field]==sha(data[name]),'audit content seal')
 need(type(s['file_count'])is int and s['file_count']==len(data),'audit file count')
 expected_dirs={str(p)for n in data for p in PurePosixPath(n).parents if str(p)!='.'};need({p.relative_to(root).as_posix()for p in root.rglob('*')if p.is_dir()}==expected_dirs,'extra directory')
 return parse(data['VERDICT.json']),{'status':'PASS','audit_manifest_sha256':sha(data['MANIFEST.json']),'audit_files':len(data)}
def canonical(data):
 local=[];central=[];offset=0
 for n,b in sorted(data.items()):
  name=n.encode('ascii');crc=zlib.crc32(b)&0xffffffff;length=len(b)
  part=struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,33,crc,length,length,len(name),0)+name+b
  c=struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,788,20,0,0,0,33,crc,length,length,len(name),0,0,0,0,0o100644<<16,offset)+name
  local.append(part);central.append(c);offset+=len(part)
 c=b''.join(central);return b''.join(local)+c+struct.pack('<IHHHHIIH',0x06054b50,0,0,len(data),len(data),len(c),offset,0)
def archive(path,v):
 raw=path.read_bytes();need(len(raw)==v['package_archive']['bytes'] and sha(raw)==v['package_archive']['sha256'],'exact trusted public ZIP required');files={}
 with zipfile.ZipFile(io.BytesIO(raw))as z:
  for i in z.infolist():
   name=safe(i.filename);need(name==i.orig_filename and name not in files and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG,'archive member type/duplicate');files[name]=z.read(i)
 need(raw==canonical(files),'noncanonical archive bytes');prefix=v['package_name']+'/'
 need(all(n.startswith(prefix)for n in files),'wrong public archive root');data={n[len(prefix):]:b for n,b in files.items()};need(sha(data['MANIFEST.json'])==v['package_manifest_sha256'] and sha(data['SEAL.json'])==v['package_seal_sha256'],'public manifest/seal pins');m=parse(data['MANIFEST.json']);s=parse(data['SEAL.json']);need(s['manifest_sha256']==v['package_manifest_sha256']and s['file_count']==len(data),'public seal');members_exact(data,m)
 return {'status':'PASS','package_archive_sha256':sha(raw),'package_files':len(data),'canonical_archive_bytes':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--package-zip',type=Path);a=p.parse_args();v,result=audit(a.root)
 if a.package_zip:result['public_archive']=archive(a.package_zip,v)
 print(json.dumps(result,sort_keys=True,indent=2))
