#!/usr/bin/env python3
"""Verify accepted archives or reconstruct one by exact binary concatenation.
Python standard library only. No extraction, research execution, or network.
"""
import argparse,hashlib,json,os,sys,tempfile
from pathlib import Path,PurePosixPath
MANIFEST_SHA256='340403d90179326603d8d9dfa1088f26762eff290431565c541c1e8042050c2e'
def need(c,m):
 if not c:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
 d={}
 for k,v in ps:need(k not in d,'Duplicate JSON key');d[k]=v
 return d
def regular(root,rel):
 p=PurePosixPath(rel)
 need(isinstance(rel,str) and p.as_posix()==rel and not p.is_absolute() and '..' not in p.parts and '\\' not in rel,'Unsafe input path')
 q=root
 for part in p.parts:
  q=q/part;need(not q.is_symlink(),'Symlink input')
 need(q.is_file(),'Missing regular input');return q

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');ap.add_argument('--archive',help='Exact archive id listed in ARCHIVES.json');ap.add_argument('--output',type=Path);a=ap.parse_args()
 need(a.check or a.archive,'Use --check or select --archive')
 need(not(a.check and a.output),'--check cannot write output')
 need(a.archive or a.output is None,'Output requires one selected archive')
 root=Path(__file__).resolve().parent;b=regular(root,'ARCHIVES.json').read_bytes();need(H(b)==MANIFEST_SHA256,'Archive manifest differs from pinned bytes')
 m=json.loads(b,object_pairs_hook=pairs);need(m['schema']=='f020-exact-archive-delivery-v1','Wrong manifest schema')
 selected=[r for r in m['archives'] if a.archive is None or r['id']==a.archive]
 need(len(selected)>0 and (a.archive is None or len(selected)==1),'Unknown or duplicate archive id')
 for row in selected:
  chunks=[];offset=0
  for i,p in enumerate(row['parts'],1):
   need(type(p['bytes'])is int and 0<p['bytes']<=8388608 and type(p['offset'])is int and p['offset']==offset and type(p['index'])is int and p['index']==i,'Part layout')
   part=regular(root,p['path']).read_bytes();need(len(part)==p['bytes'] and H(part)==p['sha256'],'Part bytes/hash mismatch')
   need(i==len(row['parts']) or len(part)==8388608,'Nonfinal part size')
   chunks.append(part);offset+=len(part)
  data=b''.join(chunks);need(type(row['bytes'])is int and len(data)==row['bytes'] and H(data)==row['sha256'],'Reassembled archive mismatch')
  print('Verified '+row['id']+': '+str(len(data))+' bytes, SHA256 '+row['sha256'])
  if not a.check:
   output=a.output if a.output is not None else root/row['output_filename']
   need(not output.is_symlink(),'Refusing symlink output')
   if output.exists():
    need(output.is_file() and output.read_bytes()==data,'Refusing to overwrite existing output')
    print('Existing exact output verified: '+str(output));continue
   fd,tmp=tempfile.mkstemp(prefix='.f020-verified-',dir=output.parent)
   try:
    with os.fdopen(fd,'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.link(tmp,output)
   finally:os.unlink(tmp)
   print('Created exact archive: '+str(output))
if __name__=='__main__':
 try:main()
 except (OSError,ValueError,KeyError,TypeError)as e:print('Verification failed: '+str(e),file=sys.stderr);sys.exit(1)
