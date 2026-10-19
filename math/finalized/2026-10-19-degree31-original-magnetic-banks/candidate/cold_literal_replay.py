"""Fresh isolated reexecution of degree-31 proof and literal checks, plus UBSan."""
from pathlib import Path
import tempfile,subprocess,json,time,hashlib,resource
R=Path(__file__).resolve().parent;start=time.time();steps=[]
with tempfile.TemporaryDirectory(prefix='degree31_cold_') as tmp:
 T=Path(tmp)
 names=['field_preflight.py','search_degree31.cpp','verify_literal.cpp','candidate_data.h','arithmetic_probe.cpp','check_arithmetic.py','check_convolution_boundary.py','independent_literal_check.py','DEGREE31_LITERAL_CERTIFICATE.json']
 for n in names:(T/n).write_bytes((R/n).read_bytes())
 def run(label,cmd,out=None):
  t=time.time();p=subprocess.run(cmd,cwd=T,text=True,capture_output=True);assert p.returncode==0,(label,p.stderr)
  if out:(T/out).write_text(p.stdout)
  steps.append({'step':label,'exit_code':p.returncode,'wall_seconds':time.time()-t});(R/'COLD_LITERAL_RUN.log').open('a').write(label+'\n'+p.stdout+p.stderr+'\n')
 run('prime_polynomial_irreducibility_before_inversions',['python','-I','field_preflight.py'])
 run('ordinary_convolution_boundary',['python','-I','check_convolution_boundary.py'])
 run('compile_ubsan_arithmetic',['g++','-O1','-g','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all','arithmetic_probe.cpp','-lgmpxx','-lgmp','-o','arithmetic_probe'])
 run('ubsan_arithmetic_probe',['./arithmetic_probe'],'ARITHMETIC_PROBE.json')
 assert (T/'ARITHMETIC_PROBE.json').read_bytes()==(R/'ARITHMETIC_PROBE.json').read_bytes()
 run('unbounded_integer_probe_check',['python','-I','check_arithmetic.py'])
 run('compile_ubsan_literal',['g++','-O1','-g','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all','verify_literal.cpp','-lgmpxx','-lgmp','-o','verify_literal'])
 run('ubsan_literal_reconstruction',['./verify_literal'])
 assert (T/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes()==(R/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes()
 run('isolated_standalone_python_literal',['python','-I','independent_literal_check.py'])
 results=json.loads((T/'INDEPENDENT_LITERAL_RESULT.json').read_text());assert results['verdict']=='PASS' and results['full_sector_equalities']==169
u=resource.getrusage(resource.RUSAGE_CHILDREN)
out={'verdict':'PASS','fresh_directory':True,'certificate_byte_identical':True,'arithmetic_probe_byte_identical':True,'undefined_behavior_sanitizer_passed':True,'steps':steps,'wall_seconds':time.time()-start,'child_user_cpu_seconds':u.ru_utime,'child_system_cpu_seconds':u.ru_stime,'peak_rss_KiB':u.ru_maxrss,'certificate_sha256':hashlib.sha256((R/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest()}
(R/'COLD_LITERAL_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
