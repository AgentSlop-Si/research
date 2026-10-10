#!/usr/bin/env python3
"""Exact nonsingularity guards for both frozen N64 inner pullbacks."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import json,sys
import numpy as np
import scipy.linalg as la
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'seed_compatibility_gate'))
from check_n16_outer_gate import LABELS
from check_lift_defects import cover_and_splice,project
from check_hierarchical_lift import lift
def cm(a,b):
 ar,ai=a;br,bi=b
 return ar@br-ai@bi,ar@bi+ai@br
def norm(a,d):return F(max(int(sum(abs(r)+abs(i) for r,i in zip(rr,ii))) for rr,ii in zip(*a)),d)
def show(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator),'decimal':float(x)}
def source(name):
 p=HERE/name
 return p if p.exists() else ROOT/'n16_existence_milestone'/name
def main():
 data=json.loads(source('DYADIC_AFFINE_CHART.json').read_text())
 a=tuple(np.asarray(data['center_'+part],dtype=object) for part in ('real','imag'))
 v=tuple(np.asarray(data['directions_'+part],dtype=object) for part in ('real','imag'))
 scale=1<<data['dyadic_exponent'];denoms=[(j+2)**64-1 for j in range(8)];L=lcm(*denoms);D=scale*L
 gs=np.zeros((8,64,64),dtype=object)
 for j,label in enumerate(LABELS):
  t,p,_=cover_and_splice(4,4,label);_,pl,_=lift(t,p,4,4,label);d=j+2
  for col in range(64):
   row=col
   for power in range(64):gs[j,row,col]=d**(64-power)*(L//denoms[j]);row=pl[row]
 rho=F(2,10**12);p=80;RS=1<<p;results=[];inputs=[]
 seedcert=json.loads(source('EXACT_CONTRACTION_CERTIFICATE.json').read_text())
 def readfrac(x):return F(int(x['numerator']),int(x['denominator']))
 assert readfrac(seedcert['residual_upper_bound'])/(1-readfrac(seedcert['contraction_factor_bound']))<rho
 saved=None if '--propose' in sys.argv else json.loads((HERE/'FIXED_INNER_PRECONDITIONERS.json').read_text())
 for ell in range(2):
  h=tuple(np.empty((64,64),dtype=object) for _ in range(2));largest=0
  for row in range(64):
   small=project(row,4,4)
   for part in range(2):h[part][row]=a[part][ell,small]@gs[:,row,:]
   dv=tuple(gs[:,row,:].T@v[part][ell,small] for part in range(2))
   largest=max(largest,int(sum(abs(r)+abs(i) for r,i in zip(dv[0].ravel(),dv[1].ravel()))))
  derivative=F(largest,D)
  if saved is None:
   floating=np.asarray([[complex(float(F(int(r),D)),float(F(int(i),D))) for r,i in zip(rr,ii)] for rr,ii in zip(*h)])
   approx=la.inv(floating)
   R=tuple(np.asarray([[int(round(float(x)*RS)) for x in row] for row in part],dtype=object) for part in (approx.real,approx.imag))
  else:
   assert saved[ell]['layer']==ell and saved[ell]['denominator_exponent']==p
   R=tuple(np.asarray(saved[ell][part],dtype=object) for part in ('real','imag'))
  product=cm(R,h)
  for i in range(64):product[0][i,i]-=RS*D
  defect=norm(product,RS*D);inverse_bound=norm(R,RS)
  total=defect+inverse_bound*derivative*rho
  assert total<1
  inputs.append({'layer':ell,'denominator_exponent':p,'real':R[0].tolist(),'imag':R[1].tolist()})
  results.append({'layer':ell,'center_inverse_defect':show(defect),'preconditioner_norm':show(inverse_bound),
                  'seed_direction_bound':show(derivative),'root_radius':show(rho),'total_nonsingularity_bound':show(total)})
 (HERE/'FIXED_INNER_PRECONDITIONERS.json').write_text(json.dumps(inputs,separators=(',',':'))+'\n')
 (HERE/'FIXED_INNER_GUARDS.json').write_text(json.dumps({'status':'PASS','results':results,
      'scope':'Both literal N64 inner pullbacks are nonsingular at the accepted N16 root; no one-inner coefficient solution is asserted.'},indent=2)+'\n')
 print(json.dumps({'status':'PASS','bounds':[r['total_nonsingularity_bound']['decimal'] for r in results]}))
if __name__=='__main__':main()
