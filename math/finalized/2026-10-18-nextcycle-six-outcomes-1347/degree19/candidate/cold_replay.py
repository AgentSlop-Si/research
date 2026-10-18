#!/usr/bin/env python3
"""Cold-reconstruct and independently verify in a disposable folder."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,sys
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=sha(R/'DEGREE19_LITERAL_CERTIFICATE.json')
steps=[];log=[]
with tempfile.TemporaryDirectory(prefix='degree19-cold-') as td:
 p=Path(td)
 for n in ['search_degree19.cpp','verify_literal.cpp','candidate_data.h','independent_literal_check.py','field_verify.py','DEGREE19_LITERAL_CERTIFICATE.json']:
  shutil.copy2(R/n,p/n)
 def run(name,args,code=0):
  r=subprocess.run(args,cwd=p,text=True,capture_output=True)
  log.append(name+'\n'+r.stdout+r.stderr)
  assert r.returncode==code,(name,r.returncode,r.stdout,r.stderr)
  steps.append({'step':name,'exit_code':r.returncode})
  return r
 run('prime_polynomial_irreducibility',[sys.executable,'-I','field_verify.py'])
 run('isolated_inert_certificate_check',[sys.executable,'-I','independent_literal_check.py'])
 assert sha(p/'DEGREE19_LITERAL_CERTIFICATE.json')==expected
 assert sha(p/'FIELD_IRREDUCIBILITY.json')==sha(R/'FIELD_IRREDUCIBILITY.json')
 run('fresh_cpp_compile',['g++','-O3','-std=c++17','verify_literal.cpp','-o','verify_literal'])
 run('fresh_cpp_reconstruction',['./verify_literal'])
 assert sha(p/'DEGREE19_LITERAL_CERTIFICATE.json')==expected
 run('reconstructed_certificate_check',[sys.executable,'-I','independent_literal_check.py'])
 run('fresh_search_compile',['g++','-O3','-std=c++17','search_degree19.cpp','-o','search_degree19'])
 prefix=run('exact_failed_prefix',['./search_degree19','3411'],1)
 assert prefix.stdout=='' and 'NO_SPLIT declared trials=3411' in prefix.stderr
 (R/'FAILED_PREFIX.log').write_text(prefix.stderr)
 (R/'FAILED_PREFIX.stdout').write_text(prefix.stdout)
 discovered=run('exact_first_candidate',['./search_degree19','3412'])
 assert discovered.stdout==(R/'NONSTABLE_CANDIDATE.json').read_text()
 (R/'COLD_RUN.log').write_text('\n'.join(log))
 receipt={'verdict':'PASS','certificate_sha256':expected,'field_receipt_byte_identical':True,'reconstructed_certificate_byte_identical':True,'discovery_candidate_byte_identical':True,'isolated_python_checks':2,'fresh_cpp_reconstructions':1,'failed_prefix_cap':3411,'first_hit_cap':3412,'steps':steps}
 (R/'COLD_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
