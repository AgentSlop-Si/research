#!/usr/bin/env python3
import argparse,hashlib,json,random,resource,runpy,shutil,subprocess,tempfile,time
from pathlib import Path
R=Path(__file__).resolve().parent
m=runpy.run_path(str(R/'literal_review.py'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);args=ap.parse_args()
 f=m['Field']([11,2]+[0]*29+[1]);D=m['D'];P=m['P'];Q=m['ORDER']
 basis=[tuple(int(i==j) for i in range(D)) for j in range(D)]
 rng=random.Random(202610193011)
 pairs=[(a,b) for a in basis for b in basis]
 pairs += [(tuple(rng.randrange(P) for _ in range(D)),tuple(rng.randrange(P) for _ in range(D))) for _ in range(100)]
 pairs.append(((52,)*D,(52,)*D))
 commands=[];expected=[]
 for a,b in pairs:commands.append('mul '+' '.join(map(str,a+b)));expected.append(f.mul(a,b))
 a=basis[1];exps=[2**127-1,2**127,2**128-1,2**128,2**128+1,Q-2,Q-1,Q,(Q+3)//8,(Q-1)//2,2**256+20261019]
 for e in exps:commands.append('pow '+' '.join(map(str,a))+' '+str(e));expected.append(f.power(a,e))
 commands.append('inv '+' '.join(map(str,a)));expected.append(f.inverse(a))
 start=time.perf_counter()
 with tempfile.TemporaryDirectory(prefix='degree31-implementation-probe-') as tmp:
  t=Path(tmp)
  shutil.copy2(args.candidate/'search_degree31.cpp',t/'search_degree31.cpp')
  shutil.copy2(R/'implementation_probe.cpp',t/'implementation_probe.cpp')
  cmd=['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all','implementation_probe.cpp','-lgmpxx','-lgmp','-o','probe']
  build=subprocess.run(cmd,cwd=t,capture_output=True,text=True)
  (R/'IMPLEMENTATION_BUILD.log').write_text(build.stdout+build.stderr)
  if build.returncode:raise RuntimeError('implementation compile failed')
  run=subprocess.run([str(t/'probe')],input='\n'.join(commands)+'\n',cwd=t,capture_output=True,text=True)
  (R/'IMPLEMENTATION_RUN.stderr').write_text(run.stderr)
  if run.returncode or run.stderr:raise RuntimeError('implementation probe error or UBSan diagnostic')
  actual=[tuple(json.loads(line)) for line in run.stdout.splitlines()]
  if actual!=expected:raise RuntimeError('C++ field implementation differs from independent arithmetic')
  (R/'IMPLEMENTATION_VALUES.json').write_text(json.dumps(actual,separators=(',',':'))+'\n')
 out={'verdict':'PASS','candidate_field_source_sha256':sha(args.candidate/'search_degree31.cpp'),
      'driver_sha256':sha(R/'implementation_probe.cpp'),'field_product_cases':len(pairs),'power_cases':len(exps),'euclidean_inverse_comparisons':1,
      'exponents':list(map(str,exps)),'undefined_behavior_sanitizer':'no diagnostics','fresh_temporary_compilation':True,
      'candidate_discovery_main_executed':False,'expected_math':'fresh Python ordinary convolution, generic reduction, Euclidean inversion',
      'values_sha256':sha(R/'IMPLEMENTATION_VALUES.json'),'compile_command':cmd,'elapsed_seconds':time.perf_counter()-start,
      'child_cpu_seconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,
      'peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
 (R/'IMPLEMENTATION_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
