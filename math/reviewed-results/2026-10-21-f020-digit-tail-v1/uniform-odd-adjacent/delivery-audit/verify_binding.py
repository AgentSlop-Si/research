#!/usr/bin/env python3
"""Verify this detached audit and, optionally, its exact bound main archive."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,stat,struct,zipfile,zlib
ROOT=Path(__file__).resolve().parent
MAIN='f020-uniform-odd-adjacent-public-20261021_v2'
MAIN_SHA='666c6ea4e537d2e3df1a4a634e7d6dc9e5a82d6f984bced77b25a880af9ce617'
MANIFEST_SHA='50c50ea59450797ba581008517247850ca8afcb740c37351437aa766c6c8e323'
SEAL_SHA='f95c2c70d5b8b190f3e70eb96c3d5bc8c50a583a2863152ab22d11cbc22a6839'
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
 expected={str(p)for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need(dirs==expected,'extra directory');s=parse(files['SEAL.json']);count=manifest(files,s['manifest_sha256']);v=parse(files['VERDICT.json']);need(v['status']=='ACCEPTED_PUBLIC_PACKAGE_WITHIN_STATED_SCOPE'and v['main_archive_sha256']==MAIN_SHA and v['main_manifest_sha256']==MANIFEST_SHA and v['main_seal_sha256']==SEAL_SHA,'audit verdict binding')
 need(v.get('detached_audit_version')==2 and v.get('main_scientific_and_delivery_bytes_unchanged')is True,'corrected audit version')
 correction=parse(files['CORRECTION_PROVENANCE.json']);formulas=parse(files['SUMMARY_FORMULA_CHECK.json'])
 need(correction['old_detached_audit']['sha256']=='c5431da051bb7bf585a1003dd8467c0c9f5f4616ff05634ffe10e63ef1125ede' and correction['main_archive']['sha256']==MAIN_SHA,'correction provenance binding')
 need(correction['accepted_author_report']['sha256']==formulas['accepted_proof_sha256']=='57ed78b499b62abe3b440ba8875736ebe12e1be2b29f35d1effce8e041b2fbec','accepted proof binding')
 need(formulas['status']=='PASS' and formulas['all_summary_mathematical_formulas_checked']is True and formulas['scientific_source_or_theorem_changed']is False,'summary checks')
 report=files['REPORT.md'].decode('utf8')
 need('h=floor(r/2), beta=p^h, L=N/beta=p^(ceil(r/2))'in report and 'For r=2, when p divides R_c(-1)'in report and 'L=p^(r-1)'not in report,'corrected formula and scope')
 for row in correction['carried_evidence_files']:need(H(files[row['path']])==row['sha256'] and len(files[row['path']])==row['bytes'],'unchanged carried evidence')
 return count
def archive(path):
 raw=path.read_bytes();need(H(raw)==MAIN_SHA and len(raw)==16497819,'main archive identity');members={};locals=[];centrals=[];offset=0
 with zipfile.ZipFile(io.BytesIO(raw))as z:
  for i in z.infolist():
   n=i.filename;safe(n);need(n==i.orig_filename and n not in members and not i.is_dir()and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG,'archive member safety');members[n]=z.read(i)
  need(z.namelist()==sorted(members),'canonical member order')
 names=sorted(members);need(len({n.casefold()for n in names})==len(names),'case collision')
 for n in names:
  b=members[n];nb=n.encode('ascii');crc=zlib.crc32(b)&0xffffffff;size=len(b);local=struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,33,crc,size,size,len(nb),0)+nb+b;central=struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,788,20,0,0,0,33,crc,size,size,len(nb),0,0,0,0,0o100644<<16,offset)+nb;locals.append(local);centrals.append(central);offset+=len(local)
 central=b''.join(centrals);canonical=b''.join(locals)+central+struct.pack('<IHHHHIIH',0x06054b50,0,0,len(names),len(names),len(central),offset,0);need(raw==canonical,'full canonical ZIP bytes');need({n.split('/')[0]for n in names}=={MAIN},'archive root');files={n[len(MAIN)+1:]:b for n,b in members.items()};need(H(files['SEAL.json'])==SEAL_SHA,'main seal identity');count=manifest(files,MANIFEST_SHA);need(count==513,'main file count');return count
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);a=p.parse_args();result={'status':'PASS','detached_audit_files':audit(),'main_archive_sha256':MAIN_SHA,'main_archive_checked':False}
 if a.archive:result.update(main_archive_checked=True,main_archive_files=archive(a.archive),full_canonical_archive_verified=True)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
