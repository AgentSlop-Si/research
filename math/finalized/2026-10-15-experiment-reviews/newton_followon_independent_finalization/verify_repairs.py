import importlib.util,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
old=load('original_block',ROOT/'rerun/block_carried_newton_tree/producer.py')
new=load('repaired_block',ROOT/'corrected_block_carried/producer.py')
pc=load('repaired_precision',ROOT/'corrected_precision_channels/producer.py')
r=random.Random(202610151908);counts={}
for i in range(600):
 a=r.getrandbits(r.randrange(300));b=r.getrandbits(r.randrange(300))
 p=r.randrange(3,80);g=r.randrange(1,30);period=r.randrange(1,15);h=r.randrange(1,60)
 x,L=old.multiply_integer(a,b,p,g,period,h);y,M=new.multiply_integer(a,b,p,g,period,h)
 assert x==y==a*b and L==M
counts['block_schedule_exact_products_and_ledgers']=600
for i in range(3000):
 a=r.getrandbits(r.randrange(0,1500))*r.choice([-1,1]);b=r.getrandbits(r.randrange(0,800))+1
 ar=pc.Arithmetic()
 assert ar.divmod(a,b)==divmod(a,b)
 assert ar.mul(a,b)==a*b
 assert ar.mul(b,a)==a*b
counts['signed_repaired_arithmetic_comparisons']=9000
A=json.loads((ROOT/'rerun/precision_adaptive_channels/RESULTS.json').read_text())
B=json.loads((ROOT/'corrected_precision_channels/RESULTS.json').read_text())
for x,y in zip(A['representative_ledgers'],B['representative_ledgers']):
 for key in set(x)-{'counts'}:assert x[key]==y[key],key
counts['unchanged_precision_representative_ledgers_except_primitive_counters']=len(A['representative_ledgers'])
out={'status':'PASS','seed':202610151908,'counts':counts}
(ROOT/'REPAIR_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
