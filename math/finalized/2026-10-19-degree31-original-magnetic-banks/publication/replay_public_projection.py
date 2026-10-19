from pathlib import Path
import json,hashlib,subprocess,tempfile,shutil,time,concurrent.futures
P=Path(__file__).resolve().parent.parent
start=time.time();commands=[('source_rebuild','candidate',['python','-I','source_binding_check.py']),('candidate_standalone','candidate',['python','-I','independent_literal_check.py']),('review_standalone','review',['python','-I','literal_review.py','inputs/DEGREE31_LITERAL_CERTIFICATE.json','--quiet']),('review_arithmetic','review',['python','-I','arithmetic_review.py','../candidate']),('review_provenance','review',['python','-I','provenance_review.py','../candidate'])]
with tempfile.TemporaryDirectory(prefix='degree31_public_') as tmp:
 T=Path(tmp)/'packet';shutil.copytree(P,T)
 def run(c):
  name,wd,args=c;t=time.time();p=subprocess.run(args,cwd=T/wd,text=True,capture_output=True);assert p.returncode==0,(name,p.stderr)
  return {'check':name,'working_directory':wd,'command':args,'exit_code':p.returncode,'wall_seconds':time.time()-t}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,commands))
 # The pure independently authored literal receipt is deterministic and unchanged.
 assert (T/'review/LITERAL_REVIEW.json').read_bytes()==(P/'review/LITERAL_REVIEW.json').read_bytes()
 # The arithmetic replay changes only its SOURCE_PINS file-hash binding after location metadata projection.
 fresh=json.loads((T/'review/ARITHMETIC_REVIEW.json').read_text());published=json.loads((P/'review/ARITHMETIC_REVIEW.json').read_text())
 original_pin_hash=published['source_hashes']['SOURCE_PINS.json'];fresh_pin_hash=fresh['source_hashes']['SOURCE_PINS.json'];fresh['source_hashes']['SOURCE_PINS.json']=original_pin_hash
 assert fresh==published
 assert (T/'review/PROVENANCE_REVIEW.json').read_bytes()==(P/'review/PROVENANCE_REVIEW.json').read_bytes()
out={'verdict':'PASS','isolated_portable_copy':True,'no_original_local_source_paths_needed':True,'checks':results,'independent_literal_receipt_byte_identical':True,'independent_provenance_receipt_byte_identical':True,'independent_arithmetic_only_source_pin_container_hash_differs':True,'original_source_pins_container_sha256':original_pin_hash,'public_source_pins_container_sha256':fresh_pin_hash,'wall_seconds':time.time()-start}
(P/'publication/PORTABLE_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
