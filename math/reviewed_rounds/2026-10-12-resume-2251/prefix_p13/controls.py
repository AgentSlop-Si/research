#!/usr/bin/env python3
"""Exact small group, endpoint and artifact replay controls for the finite candidate."""
import itertools,json,math,subprocess,tempfile,sys,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent

def mul(a,b):return (a%4+(-1 if a//4 else 1)*(b%4))%4+4*((a//4)^(b//4))
stabs=[]
for mask in range(256):
 T={i for i in range(8) if mask>>i&1}
 stabs.append(sum(1<<g for g in range(8) if {mul(g,x) for x in T}==T))
closures=[]
for mask in range(256):
 B={0};stack=[0]
 while stack:
  a=stack.pop()
  for g in range(8):
   if mask>>g&1:
    b=mul(a,g)
    if b not in B:B.add(b);stack.append(b)
 closures.append(len(B))
maximum=-1;maximum_count=0;escape_max=-1;escape_count=0
for perm in itertools.permutations(range(8)):
 mask=0;gen=0;score=0
 for j,g in enumerate(perm,1):
  mask|=1<<g;score+=stabs[mask].bit_count()-1
  if j<8:gen|=stabs[mask]
 if score>maximum:maximum=score;maximum_count=1
 elif score==maximum:maximum_count+=1
 if closures[gen]==8:
  if score>escape_max:escape_max=score;escape_count=1
  elif score==escape_max:escape_count+=1
assert (maximum,maximum_count,escape_max)==(12,2432,10)
# Concrete rejected wrong-encoding witness: correct score alone is insufficient.
mask=0;gen=0;wrong_score=0
for j,g in enumerate(range(8),1):
 mask|=1<<g;wrong_score+=stabs[mask].bit_count()-1
 if j<8:gen|=stabs[mask]
assert wrong_score==10 and closures[gen]==4

def conflict(i,d,j,e):
 if i==j:return True
 L=math.lcm(d,e)
 return not any((m>i or L==d) and (m<j or L==e) for m in range(i,j+1) if m%L==0)
assert conflict(104,8,208,52) # exact-period low conflict must survive
assert conflict(26,2,26,13) # competing exact stabilizers at one prefix
assert not conflict(13,13,26,13) # eligible equal-type endpoints
assert conflict(13,13,26,2) # upper endpoint cannot hide larger stabilizer
assert not conflict(26,13,52,26) # upper endpoint may realize its own order

source=BASE/'check_prefix_slice.py';before=hashlib.sha256(source.read_bytes()).hexdigest()
replay=[]
with tempfile.TemporaryDirectory(prefix='prefix_p13_cold_') as td:
 td=Path(td);copy=td/source.name;copy.write_bytes(source.read_bytes())
 for p,r,name,extra in [(11,13,'p11_r13_calibration.json',['--no-group']),(13,17,'p13_r17_check.json',[])]:
  subprocess.run([sys.executable,str(copy),'--p',str(p),'--r',str(r),'--out',str(td/name),*extra],cwd=td,check=True,capture_output=True,text=True)
  old=json.loads((BASE/name).read_text());new=json.loads((td/name).read_text());old.pop('elapsed_seconds');new.pop('elapsed_seconds');assert old==new
  replay.append({'p':p,'r':r,'semantic_match':True})
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
result={'D8':{'permutations':math.factorial(8),'maximum':maximum,'maximum_count':maximum_count,'escape_maximum':escape_max,'escape_maximum_count':escape_count},'rejected_wrong_encoding':{'score':wrong_score,'B_order':closures[gen]},'endpoint_controls_passed':5,'cold_replay':replay,'checker_sha256':before,'source_unchanged':True}
(BASE/'CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
