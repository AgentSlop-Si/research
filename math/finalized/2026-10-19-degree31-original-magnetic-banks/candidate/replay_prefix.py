"""Cold compile and exact complete-prefix/first-hit replay; no historical witness executed."""
from pathlib import Path
import json,subprocess,tempfile,hashlib,time,resource
R=Path(__file__).resolve().parent;v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text());start=time.time();runs=[]
with tempfile.TemporaryDirectory(prefix='degree31_prefix_') as tmp:
 T=Path(tmp);(T/'search_degree31.cpp').write_bytes((R/'search_degree31.cpp').read_bytes())
 subprocess.run(['g++','-O3','-std=c++17','search_degree31.cpp','-lgmpxx','-lgmp','-o','search_degree31'],cwd=T,check=True)
 # A run ending immediately before the known first hit must exhaust without emitting a candidate.
 for n,expect in [(v['trial'],1),(v['trial']+1,0)]:
  p=subprocess.run(['./search_degree31',str(n)],cwd=T,text=True,capture_output=True);assert p.returncode==expect
  if expect:
   assert p.stdout=='';orig=(R/'PREFIX_LEDGER.jsonl').read_bytes().splitlines(keepends=True);assert (T/'PREFIX_LEDGER.jsonl').read_bytes()==b''.join(orig[:-1])
  else:
   assert p.stdout==(R/'NONSTABLE_CANDIDATE.json').read_text();assert (T/'PREFIX_LEDGER.jsonl').read_bytes()==(R/'PREFIX_LEDGER.jsonl').read_bytes()
  (R/f'REPLAY_{n}.log').write_text(p.stderr)
  runs.append({'nonzero_node_limit':n,'exit_code':p.returncode,'prefix_sha256':hashlib.sha256((T/'PREFIX_LEDGER.jsonl').read_bytes()).hexdigest(),'candidate_output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()})
u=resource.getrusage(resource.RUSAGE_CHILDREN)
out={'verdict':'PASS','fresh_compile':True,'full_failed_prefix_and_first_hit_reexecuted':True,'runs':runs,'wall_seconds':time.time()-start,'child_user_cpu_seconds':u.ru_utime,'child_system_cpu_seconds':u.ru_stime,'peak_rss_KiB':u.ru_maxrss}
(R/'FIRST_HIT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
