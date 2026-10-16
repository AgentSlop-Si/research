import importlib.util,sys,json
from pathlib import Path
s=importlib.util.spec_from_file_location('new_adapter',sys.argv[1] if len(sys.argv)>1 else 'alg007_fallback_contract_0817/publication_safe/alg007_bounded_adapter.py');a=importlib.util.module_from_spec(s);sys.modules[s.name]=a;s.loader.exec_module(a)
def E(e):return e.bit_count()+2*e.bit_length()-1
checks=0
for q in (4,8,16,32,64,128):
 for supplied in (False,True):
  root=pow(31,(a.P-1)//q,a.P) if supplied else None
  H=sum(E(e) for e in [a.P-1,(a.P-1)//2,(a.P-1)//3,(a.P-1)//5,q,q//2,a.P-2,a.P-2])+ (0 if supplied else E((a.P-1)//q))
  ell=q.bit_length()-1;T=13*q*ell//2+9*q+ell+1
  for budget in (0,1,13,113,1000000):
   y=a.transform(list(range(q)),2,0,root=root,attempt_budget=budget);l=y['ledger'];ph=l['phases']
   assert sum(ph['input'].values())+sum(ph['setup'].values())==15*q+11+H
   assert sum(ph['fallback'].values())==T+1
   assert l['total_units']==15*q+11+H+l['attempt_spent']+T+1+4*q
   checks+=1
r={'pass':True,'checks':checks,'scope':'Exact independently derived cold and fallback event totals across both root branches'}
Path(__file__).resolve().parent.joinpath('COST_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
