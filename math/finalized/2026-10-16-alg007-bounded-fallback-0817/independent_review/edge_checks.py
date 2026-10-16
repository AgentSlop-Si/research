import importlib.util,sys,json
from pathlib import Path
s=importlib.util.spec_from_file_location('new_adapter',sys.argv[1] if len(sys.argv)>1 else 'alg007_fallback_contract_0817/publication_safe/alg007_bounded_adapter.py'); a=importlib.util.module_from_spec(s);sys.modules[s.name]=a;s.loader.exec_module(a)
checks=0
for n in (4,8,16,32,64,128):
 y=a.transform(list(range(n)),2,0,attempt_budget=0)
 c=y['ledger']['phases']['fallback'];b=n*(n.bit_length()-1)//2
 assert c['ntt_butterfly']==b and c['field_mul']==b and c['field_add']==2*b
 assert c['ntt_started']==c['ntt_finished']==c['fallback_dispatch']==1
 assert y['ledger']['attempt_spent']==0
 checks+=1
invalid=[({'x':[0]*8,'m':1,'cap':0}),({'x':[0]*8,'m':4,'cap':0}),({'x':[0]*6,'m':2,'cap':0}),({'x':[0]*8,'m':2,'cap':3}),({'x':[0]*8,'m':2,'cap':0,'a':2}),({'x':[0]*8,'m':2,'cap':0,'root':1}),({'x':[0]*8,'m':2,'cap':0,'attempt_budget':-1}),({'x':[True]*8,'m':2,'cap':0}),({'x':[a.P]*8,'m':2,'cap':0})]
for kw in invalid:
 try:a.transform(**kw)
 except a.ContractError:checks+=1
 else:raise AssertionError(kw)
class Trap(list):
 def __len__(self):raise AssertionError('userhook')
try:a.transform(Trap([0]*8),2,0)
except a.ContractError:checks+=1
# Recognizer may finish but budget interrupt decoder: preserve charged prefix and full fallback.
x=[1]*8
full=a.transform(x,2,2,attempt_budget=10000000)
recognition=sum(full['ledger']['phases']['recognition'].values())
y=a.transform(x,2,2,attempt_budget=recognition)
assert y['route']=='FALLBACK_BUDGET' and y['ledger']['denied_reservation']['phase']=='decode'
assert y['ledger']['attempt_spent']==recognition and y['values']==full['values'];checks+=1
r={'pass':True,'checks':checks,'scope':'Independent exact fallback butterfly schedule, invalid-domain rejection, user-hook avoidance and decode-interruption retention'}
Path(__file__).resolve().parent.joinpath('EDGE_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
