#!/usr/bin/env python3
"""Rigorous algebraic-seed rejection of an outer-only N64 correction law."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm,isqrt
import json,sys,hashlib,time
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'seed_compatibility_gate'))
from check_n16_outer_gate import LABELS
from check_lift_defects import cover_and_splice,project
from check_hierarchical_lift import lift
def cm(a,b):
 ar,ai=a;br,bi=b
 return ar@br-ai@bi,ar@bi+ai@br
def bounds(a,den):return [F(int(sum(abs(r)+abs(i) for r,i in zip(rr,ii))),den) for rr,ii in zip(*a)]
def frac(d):return F(int(d['numerator']),int(d['denominator']))
def show(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator),'decimal':float(x)}
def input_path(name):
 p=HERE/name
 return p if p.exists() else ROOT/'n16_existence_milestone'/name
def propose():
 data=np.load(HERE/'PROPOSED_MINOR.npz');r=data['inverse'];p=80
 obj={'row':int(data['row']),'columns':data['columns'].tolist(),'dyadic_exponent':p,
      'inverse_real':[[int(round(float(v)*2**p)) for v in row] for row in r.real],
      'inverse_imag':[[int(round(float(v)*2**p)) for v in row] for row in r.imag]}
 (HERE/'EXACT_MINOR_CHART.json').write_text(json.dumps(obj,indent=2)+'\n')
def certify():
 started=time.monotonic()
 seed_path=input_path('DYADIC_AFFINE_CHART.json')
 assert hashlib.sha256(seed_path.read_bytes()).hexdigest()=='904d7d24bf3aeee0a7c206eb8fd98ee11045fbc22cc97a105511b51907e1b188'
 seed=json.loads(seed_path.read_text());old=json.loads(input_path('EXACT_CONTRACTION_CERTIFICATE.json').read_text())
 e,q=frac(old['residual_upper_bound']),frac(old['contraction_factor_bound'])
 rho=F(2,10**12)
 assert q<1 and e/(1-q)<rho
 # The accepted Banach proof gives ||y*|| <= e/(1-q), not just its original
 # radius 10^-9. This strictly smaller algebraic-root enclosure is derived,
 # never obtained by specializing the dyadic center modulo a prime.
 center=tuple(np.asarray(seed['center_'+part],dtype=object) for part in ('real','imag'))
 directions=tuple(np.asarray(seed['directions_'+part],dtype=object) for part in ('real','imag'))
 scale=1<<seed['dyadic_exponent'];poles=[(j+2)**64-1 for j in range(8)]
 assert all(d>0 for d in poles)
 L=lcm(*poles);D=L*scale;greens=np.zeros((8,64,64),dtype=object)
 for j,label in enumerate(LABELS):
  ts,ps,_=cover_and_splice(4,4,label);_,pl,_=lift(ts,ps,4,4,label);d=j+2
  for col in range(64):
   row=col
   for power in range(64):greens[j,row,col]=d**(64-power)*(L//poles[j]);row=pl[row]
 hs=[];ls=[]
 for layer in range(2):
  h=tuple(np.empty((64,64),dtype=object) for _ in range(2));largest=0
  for row in range(64):
   v=project(row,4,4)
   for part in range(2):h[part][row]=center[part][layer,v]@greens[:,row,:]
   # Stream the 256 chart-direction columns to avoid storing a large tensor.
   dparts=tuple(greens[:,row,:].T@directions[part][layer,v] for part in range(2))
   row_bound=int(sum(abs(r)+abs(i) for r,i in zip(dparts[0].ravel(),dparts[1].ravel())))
   largest=max(largest,row_bound)
  hs.append(h);ls.append(F(largest,D))
 hb=[max(bounds(h,D)) for h in hs]
 # Only the first Fourier row is tested, so its nine selected entries are
 # exactly 1. The only new algebraic enclosure needed is sqrt(2) in F8.
 Q=1<<160;s=isqrt(2*Q*Q);BD=2*Q
 b=(np.eye(64,dtype=object)*BD,np.zeros((64,64),dtype=object))
 values=[(BD,0),(s,s),(0,BD),(-s,s),(-BD,0),(-s,-s),(0,-BD),(s,-s)]
 for x in (0,1,4,5):
  for y in range(8):
   for z in range(8):b[0][8*x+y,8*x+z],b[1][8*x+y,8*x+z]=values[y*z%8]
 bank_error=F(8,Q)
 minor=json.loads((HERE/'EXACT_MINOR_CHART.json').read_text());assert minor['row']==0
 columns=minor['columns'];assert len(columns)==len(set(columns))==9 and all(0<=c<64 for c in columns)
 R=tuple(np.asarray(minor['inverse_'+part],dtype=object) for part in ('real','imag'))
 RS=1<<minor['dyadic_exponent']
 fg=tuple(part[:,:8]@greens[:,0,:] for part in R);FD=RS*L
 fbound=max(bounds(fg,FD))
 h0cols=tuple(part[:,columns] for part in hs[0])
 prefix=cm(cm(hs[1],b),h0cols)
 rm=cm(fg,prefix);den=FD*D*D*BD
 # The last augmented row is exactly all ones. Add R[:,8] times this row.
 for part in range(2):
  for i in range(9):
   for j in range(9):rm[part][i,j]+=R[part][i,8]*L*D*D*BD
 for i in range(9):rm[0][i,i]-=den
 center_defect=max(bounds(rm,den))
 # Exact matrix-infinity perturbation of H1(y*) B_true H0(y*) relative to
 # the dyadic-center product with B_approx. True bank norm is exactly 8.
 prefix_error=8*ls[1]*rho*(hb[0]+ls[0]*rho)+8*hb[1]*ls[0]*rho+hb[1]*bank_error*hb[0]
 # There are nine selected columns. Bound each output entry by the induced
 # row functional norm, then sum all nine for an infinity-norm bound.
 perturbation=9*fbound*prefix_error
 total=center_defect+perturbation
 assert total<1
 result={'status':'PASS_RIGOROUS_OUTER_ONLY_REJECTION','target_row':0,'minor_columns':columns,
         'accepted_seed_root_radius_used':show(rho),'derived_seed_root_bound':show(e/(1-q)),
         'inner_layer_center_bounds':[show(x) for x in hb],
         'inner_layer_direction_bounds':[show(x) for x in ls],
         'bank_enclosure_error_bound':show(bank_error),'preconditioned_Green_row_norm':show(fbound),
         'center_preconditioned_minor_defect':show(center_defect),'seed_and_bank_minor_perturbation':show(perturbation),
         'total_preconditioned_minor_defect':show(total),'fixed_large_inverse_guards':poles,
         'free_outer_physical_coefficients':512,'frozen_inner_physical_coefficients':1024,
         'exact_arithmetic':'Gaussian integers and rational fractions after reading proposed dyadic preconditioner',
         'scope':'No outer endpoint choice can correct the two literal inner pullbacks of the accepted N16 seed. Full N64 family remains open.',
         'elapsed_seconds':time.monotonic()-started}
 (HERE/'OUTER_PREFIX_REJECTION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k in ('status','elapsed_seconds','minor_columns') or isinstance(v,dict) and 'decimal' in v},indent=2),flush=True)
if __name__=='__main__':
 if '--propose' in sys.argv:propose()
 certify()
