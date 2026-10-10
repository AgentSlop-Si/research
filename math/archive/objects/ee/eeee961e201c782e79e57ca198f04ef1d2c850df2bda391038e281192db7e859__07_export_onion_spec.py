"""Export the exact rational residual system metadata and modular witness."""
import json,hashlib
from pathlib import Path
from general_onion import build
from dual_support import primitive_root,constraints,P8
from inverse_quartic import rankmod
n=8;p=12289;w=primitive_root(p,n)
x=[101,203,307,401,509,601,701,809]
C,B,aux=build(n,p,w,P8,x)
lo,up=constraints(B,p)
rem=[{'name':name,'value_mod_12289':int(value)} for name,value in lo+up if not (
    name in {f'lower_{i}_1' for i in range(2,7)} or
    name in {f'lower_{i}_2' for i in range(3,7)} or
    name in {f'upper_1_{j}' for j in range(2,7)} or
    name in {f'upper_2_{j}' for j in range(3,7)})]
assert len(rem)==12 and all(z['value_mod_12289']!=0 for z in rem)
obj={'title':'12 exact rational Fourier feasibility equations in eight coordinates',
  'scope':'Open chart ONLY; not solved; roots must satisfy det(C), B anchors, inverse A corner and nonzero denominators',
  'cyclotomic_field':'Q[z]/(Phi_8(z))=Q[z]/(z^4+1)',
  'variables':['t','h0','h1','h2','h6','beta','gamma1','gamma2'],
  'permutation':P8,
  'evaluator':'general_onion.py:build(8,p,omega,P8,variables)',
  'definitions':'See PROOF_CERTIFICATE.md sections 2..5; C from L,V,U,W; B=F8 C P^-1',
  'equation_formulae':{'lower':'B[i,j]*B[7,0]-B[i,0]*B[7,j]=0',
                       'upper':'B[i,j]*B[0,7]-B[i,7]*B[0,j]=0'},
  'remaining_equations':[r['name'] for r in rem],
  'reference_non_solution':{'prime':p,'primitive_root':w,'parameters':x,'stage_rank':rankmod(C,p),
                            'residuals':rem,'note':'Deliberate NONSOLUTION; validates 12 genuinely remaining equations'} }
raw=json.dumps(obj,indent=2,sort_keys=True)+'\n'
here=Path(__file__).resolve().parent
(here/'onion_twelve_system_spec.json').write_text(raw)
print('equations',len(rem),'sha256',hashlib.sha256(raw.encode()).hexdigest())
