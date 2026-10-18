#!/usr/bin/env python3
"""Reproducible ordered preflight, then bounded deterministic support discovery."""
from pathlib import Path
import subprocess,json,hashlib,sys,datetime
R=Path(__file__).resolve().parent;steps=[]
def run(name,args,stdout=None,stderr=None):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 a=subprocess.run(args,cwd=R,text=True,capture_output=True)
 end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 if stdout:(R/stdout).write_text(a.stdout)
 if stderr:(R/stderr).write_text(a.stderr)
 assert a.returncode==0,(name,a.returncode,a.stderr)
 steps.append({'step':name,'start_utc':start,'end_utc':end,'exit_code':a.returncode})
 print(name,'PASS',flush=True)
run('field_irreducibility',[sys.executable,'-I','field_verify.py'])
run('convolution_boundary_preflight',[sys.executable,'-I','check_convolution_boundary.py'],'CONVOLUTION_BOUNDARY_CHECK.stdout')
run('unbounded_GMP_preflight',[sys.executable,'-I','check_arithmetic.py'],'ARITHMETIC_CHECK.stdout')
run('compile_search',['g++','-O3','-std=c++17','search_degree29.cpp','-lgmpxx','-lgmp','-o','search_degree29'])
run('search_cap_100000',['./search_degree29','100000'],'NONSTABLE_CANDIDATE.json','SEARCH_PROGRESS.log')
(R/'DISCOVERY_CHRONOLOGY.json').write_text(json.dumps({'verdict':'PASS','steps':steps},indent=2)+'\n')
v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text());f=lambda x:'{'+','.join(map(str,x))+'}'
(R/'candidate_data.h').write_text('static const int INPUT_Y[D]='+f(v['y'])+';\nstatic const int INPUT_H[8][D]={'+','.join(f(x) for x in v['H'])+'};\n')
print('FOUND',v['trial'],v['candidates'],flush=True)
