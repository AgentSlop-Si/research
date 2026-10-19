"""Run the standalone JSON checker on deliberately corrupted inert certificates."""
from pathlib import Path
import json,subprocess,tempfile,copy,time,hashlib,concurrent.futures
R=Path(__file__).resolve().parent;data=json.loads((R/'DEGREE31_LITERAL_CERTIFICATE.json').read_text());cases=[]
def case(name,change):
 x=copy.deepcopy(data);change(x);cases.append((name,x))
def bump(a):a[0]=(a[0]+1)%53
case('noncanonical_coefficient',lambda x:x['banks'][0]['alpha'].__setitem__(0,53))
case('zero_alpha',lambda x:x['banks'][0].__setitem__('alpha',[0]*31))
case('wrong_pole_guard',lambda x:bump(x['banks'][0]['guard']))
case('duplicate_support_root',lambda x:x['roots'].__setitem__(1,x['roots'][0][:]))
case('annihilator_coefficient_changed',lambda x:bump(x['H'][0]))
case('one_raw_weight_changed',lambda x:bump(x['banks'][0]['weights'][0]))
case('one_amplitude_changed',lambda x:bump(x['banks'][0]['amplitudes'][0]))
case('missing_physical_bank',lambda x:x['banks'].pop())
case('wrong_degree_metadata',lambda x:x.__setitem__('degree',29))
case('positive_fourier_target',lambda x:x.__setitem__('matrix',[[[pow(16,r*c%13,53)]+[0]*30 for c in range(13)] for r in range(13)]))
case('omitted_1_over_13_target',lambda x:x.__setitem__('matrix',[[[(13*a[0])%53]+a[1:] for a in row] for row in x['matrix']]))
def run(row):
 name,x=row;start=time.time()
 with tempfile.TemporaryDirectory(prefix='degree31_mutation_') as tmp:
  T=Path(tmp);(T/'independent_literal_check.py').write_bytes((R/'independent_literal_check.py').read_bytes());(T/'DEGREE31_LITERAL_CERTIFICATE.json').write_text(json.dumps(x))
  p=subprocess.run(['python','-I','independent_literal_check.py'],cwd=T,text=True,capture_output=True)
  assert p.returncode!=0 and 'AssertionError' in p.stderr,(name,p.returncode,p.stderr)
  return {'mutation':name,'rejected':True,'exit_code':p.returncode,'wall_seconds':time.time()-start,'last_stderr_line':p.stderr.strip().splitlines()[-1]}
start=time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,cases))
out={'verdict':'PASS','positive_control_receipt':json.loads((R/'INDEPENDENT_LITERAL_RESULT.json').read_text())['verdict'],'checker_sha256':hashlib.sha256((R/'independent_literal_check.py').read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256((R/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest(),'mutations':results,'wall_seconds':time.time()-start}
(R/'MUTATION_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
