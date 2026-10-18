#!/usr/bin/env python3
"""Cold rebuild, multiprecision preflight, literal proof, and exact search replay."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,sys
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=sha(R/'DEGREE29_LITERAL_CERTIFICATE.json');v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text())
steps=[];log=[]
with tempfile.TemporaryDirectory(prefix='degree29-cold-') as td:
 p=Path(td)
 for n in ['search_degree29.cpp','verify_literal.cpp','candidate_data.h','independent_literal_check.py','field_verify.py','DEGREE29_LITERAL_CERTIFICATE.json','arithmetic_probe.cpp','check_arithmetic.py','check_convolution_boundary.py']:
  shutil.copy2(R/n,p/n)
 def run(name,args,code=0):
  r=subprocess.run(args,cwd=p,text=True,capture_output=True)
  log.append(name+'\n'+r.stdout+r.stderr)
  assert r.returncode==code,(name,r.returncode,r.stdout,r.stderr)
  steps.append({'step':name,'exit_code':r.returncode});return r
 def compile(src,out,extra=[]):return ['g++','-O3','-std=c++17',*extra,src,'-lgmpxx','-lgmp','-o',out]
 run('prime_polynomial_irreducibility',[sys.executable,'-I','field_verify.py'])
 run('convolution_boundary_controls_before_search',[sys.executable,'-I','check_convolution_boundary.py'])
 assert sha(p/'CONVOLUTION_BOUNDARY_CHECK.json')==sha(R/'CONVOLUTION_BOUNDARY_CHECK.json')
 run('fresh_arithmetic_probe_compile',compile('arithmetic_probe.cpp','arithmetic_probe',['-fsanitize=undefined','-fno-sanitize-recover=all']))
 probe=run('cpp_unbounded_arithmetic_probe',['./arithmetic_probe']);(p/'ARITHMETIC_PROBE.json').write_text(probe.stdout)
 assert sha(p/'ARITHMETIC_PROBE.json')==sha(R/'ARITHMETIC_PROBE.json')
 run('independent_arithmetic_preflight_before_search',[sys.executable,'-I','check_arithmetic.py'])
 assert sha(p/'ARITHMETIC_CHECK.json')==sha(R/'ARITHMETIC_CHECK.json')
 run('isolated_inert_certificate_check',[sys.executable,'-I','independent_literal_check.py'])
 assert sha(p/'DEGREE29_LITERAL_CERTIFICATE.json')==expected
 assert sha(p/'FIELD_IRREDUCIBILITY.json')==sha(R/'FIELD_IRREDUCIBILITY.json')
 run('fresh_cpp_compile',compile('verify_literal.cpp','verify_literal'))
 run('fresh_cpp_reconstruction',['./verify_literal'])
 assert sha(p/'DEGREE29_LITERAL_CERTIFICATE.json')==expected
 run('reconstructed_certificate_check',[sys.executable,'-I','independent_literal_check.py'])
 run('undefined_behavior_sanitizer_compile',compile('verify_literal.cpp','verify_ubsan',['-fsanitize=undefined','-fno-sanitize-recover=all']))
 run('undefined_behavior_sanitizer_literal_check',['./verify_ubsan'])
 assert sha(p/'DEGREE29_LITERAL_CERTIFICATE.json')==expected
 run('fresh_search_compile',compile('search_degree29.cpp','search_degree29'))
 prefix=run('exact_failed_prefix',['./search_degree29',str(v['trial'])],1)
 assert prefix.stdout=='' and f"NO_SPLIT declared trials={v['trial']}" in prefix.stderr
 (R/'FAILED_PREFIX.log').write_text(prefix.stderr);(R/'FAILED_PREFIX.stdout').write_text(prefix.stdout)
 discovered=run('exact_first_candidate',['./search_degree29',str(v['trial']+1)])
 assert discovered.stdout==(R/'NONSTABLE_CANDIDATE.json').read_text()
 (R/'COLD_RUN.log').write_text('\n'.join(log))
 receipt={'verdict':'PASS','certificate_sha256':expected,'field_receipt_byte_identical':True,'arithmetic_probe_and_check_byte_identical':True,'boundary_and_truncation_tests_completed_before_search':True,'convolution_boundary_receipt_byte_identical':True,'radix16_negative_controls_before_search':True,'reconstructed_certificate_byte_identical':True,'discovery_candidate_byte_identical':True,'isolated_python_checks':2,'fresh_cpp_reconstructions':2,'undefined_behavior_sanitizer':'PASS','failed_prefix_cap':v['trial'],'first_hit_cap':v['trial']+1,'steps':steps}
 (R/'COLD_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
