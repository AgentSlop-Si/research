#!/usr/bin/env python3
"""Bounded retained-carrier-anchor experiment; no upstream file is edited."""
from pathlib import Path
from hashlib import sha256
import argparse, gzip, importlib.util, inspect, json, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
UP=ROOT/'upstream'
sys.path.insert(0,str(UP/'scripts/experiments'))
import binary_frame_compiler as compiler
from binary_frame_replay import replay
from binary_frame_profile_prepare import prepare

def main():
 p=argparse.ArgumentParser();p.add_argument('h',type=int,choices=[23,25]);p.add_argument('mode',choices=['baseline','carrier']);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('pinned_pair_graph',UP/'research/pair-assembly/pair_graph.py')
 graph=importlib.util.module_from_spec(spec);spec.loader.exec_module(graph);compiler.graph=graph.graph
 source=inspect.getsource(compiler.compile_)
 if a.mode=='carrier':
  replacements={
   "def acquire(g,anchors):":"def acquire(g,anchors):\n  stats['acquire_calls']+=1;stats['acquire_with_carriers']+=bool(carrier_anchors);stats['carrier_anchor_occurrences']+=len(carrier_anchors)",
   "b=blocks[g];outuses=":"carrier_anchors=[];b=blocks[g];outuses=",
   "elif kind=='carry':assign[key]=s;assert slots[s]==signal[uses[key][0]]":"elif kind=='carry':assign[key]=s;carrier_anchors.append(s);assert slots[s]==signal[uses[key][0]]",
   "acquire(g,list(value_slots.values()))":"acquire(g,list(value_slots.values())+carrier_anchors)",
  }
  for old,new in replacements.items():
   assert source.count(old)==(2 if old.startswith('acquire(') else 1),(old,source.count(old))
   source=source.replace(old,new)
  exec(compile(source,'<carrier_anchor_variant>','exec'),compiler.__dict__)
 out=ROOT/'results'/f'{a.mode}-{a.h}';out.mkdir(parents=True,exist_ok=True)
 (out/'compile_function.py').write_text(source)
 started=time.time();result,word=compiler.compile_(a.h,matching=True,reclaim=True,dirty=True)
 raw=(json.dumps(word,separators=(',',':'))+'\n').encode();path=out/'word.json.gz'
 with path.open('wb') as f:
  with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as g:g.write(raw)
 receipt=replay(path)
 prepared=prepare(path,out/'transitions.bin')
 profiler=ROOT/'profiles'
 subprocess.run([str(profiler),str(out/'transitions.bin')],check=True)
 profile=json.loads((out/'transitions.bin.profiles.json').read_text())
 if a.mode=='baseline':
  expected=json.loads((UP/'research/pair-assembly/frame'/f'frame-profiles-{a.h}.json').read_text())
  assert profile==expected,('baseline fixed profile mismatch',profile,expected)
  record=json.loads((UP/'research/pair-assembly/frame/frame-compiler.json').read_text())['axes'][str(a.h)]
  assert sha256(raw).hexdigest()==record['word_sha256'],'baseline exact serialized word mismatch'
 assert result['roles']==receipt['roles']==profile['R']
 assert result['rank_mass']==receipt['rank_mass']==profile['rank_sum']
 data=dict(mode=a.mode,h=a.h,compiled=result,replay=receipt,prepared=prepared,profile=profile,word_sha256=sha256(raw).hexdigest(),elapsed=time.time()-started)
 (out/'receipt.json').write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps(data),flush=True)
if __name__=='__main__':main()
