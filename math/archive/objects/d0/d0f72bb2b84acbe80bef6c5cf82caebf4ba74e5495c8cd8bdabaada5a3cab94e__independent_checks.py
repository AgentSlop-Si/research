#!/usr/bin/env python3
"""Independent integer/Fraction outer-only gate audit. No constructor code imported."""
from fractions import Fraction as F
from math import isqrt,lcm
from pathlib import Path
import json,hashlib,sys
BASE=Path(__file__).parent
sys.path.insert(0,str(BASE/'seed_audit'))
from independent_verifier import prescribed_orders,cproduct,normnum,shapecheck,as_fraction,fraction_record,cycles
LABELS=[(axis,c,s) for axis in ('H','V') for c in (0,1) for s in (-1,1)]
def cover(a,b,label):
 axis,c,s=label
 return [b*((x+s*(2*y+c))%a)+y if axis=='H' else b*x+(y+s*(2*x+c))%b for x in range(a) for y in range(b)]
def projection(v):
 x,y=divmod(v,8);return 4*(x%4)+y%4

def lifts():
 out=[]
 for label,small in zip(LABELS,prescribed_orders()):
  ts=cover(4,4,label);tl=cover(8,8,label);eta=[None]*16
  for v,w in enumerate(ts):eta[w]=small[v]
  pre=[]
  for w in tl:
   x,y=divmod(w,8);xx,yy=divmod(eta[4*(x%4)+y%4],4)
   pre.append(8*(xx+4*(x//4))+yy+4*(y//4))
  cc=cycles(pre);assert len(cc)==4 and all(len(c)==16 for c in cc)
  tails=sorted(next(v for v in c if projection(v)==0) for c in cc);assert tails==[0,4,32,36]
  p=pre[:]
  for j,v in enumerate(tails):p[v]=pre[tails[(j+1)%4]]
  assert len(cycles(p))==1 and sorted(p)==list(range(64))
  assert all(projection(p[v])==small[projection(v)] for v in range(64))
  out.append(p)
 return out

def verify():
 raw=(BASE/'seed_audit/sources/DYADIC_AFFINE_CHART.json').read_bytes();sha=hashlib.sha256(raw).hexdigest()
 assert sha=='904d7d24bf3aeee0a7c206eb8fd98ee11045fbc22cc97a105511b51907e1b188'
 chart=json.loads(raw);seed=json.loads((BASE/'seed_audit/INDEPENDENT_CERTIFICATE.json').read_text())
 assert seed['status']=='ACCEPTED_EXACT_N16_LOCAL_EXISTENCE' and seed['chart_sha256']==sha
 e=as_fraction(seed['bounds']['residual_upper_bound']);q=as_fraction(seed['bounds']['contraction_factor_bound'])
 root=e/(1-q);rho=F(2,10**12);assert 0<q<1 and root<rho<F(1,10**9)
 cr,ci=chart['center_real'],chart['center_imag'];vr,vi=chart['directions_real'],chart['directions_imag']
 for c in (cr,ci):shapecheck(c,[3,16,8])
 for v in (vr,vi):shapecheck(v,[3,16,8,256])
 assert chart['dyadic_exponent']==60
 S=1<<60;poles=[d**64-1 for d in range(2,10)];L=lcm(*poles);D=S*L
 orders=lifts();greens=[]
 for term,p in enumerate(orders):
  d=term+2;g=[[0]*64 for _ in range(64)]
  for col in range(64):
   row=col
   for power in range(64):g[row][col]=d**(64-power)*(L//poles[term]);row=p[row]
  inv=[None]*64
  for v,w in enumerate(p):inv[w]=v
  assert all(d*g[i][k]-g[inv[i]][k]==d*L*int(i==k) for i in range(64) for k in range(64))
  greens.append(g)
 hs=[];Ls=[]
 for ell in range(2):
  h=tuple([[sum(c[ell][projection(i)][j]*greens[j][i][k] for j in range(8)) for k in range(64)] for i in range(64)] for c in (cr,ci))
  hs.append(h);largest=0
  for i in range(64):
   v=projection(i);total=0
   for k in range(64):
    coeff=[greens[j][i][k] for j in range(8)]
    for t in range(256):
     total+=abs(sum(coeff[j]*vr[ell][v][j][t] for j in range(8)))+abs(sum(coeff[j]*vi[ell][v][j][t] for j in range(8)))
   largest=max(largest,total)
  Ls.append(F(largest,D))
  print('Rebuilt inner layer',ell,flush=True)
 hb=[F(normnum(h),D) for h in hs]
 Q=1<<160;s=isqrt(2*Q*Q);assert s*s<=2*Q*Q<(s+1)**2;BD=2*Q
 br=[[BD*int(i==j) for j in range(64)] for i in range(64)];bi=[[0]*64 for _ in range(64)]
 vals=[(BD,0),(s,s),(0,BD),(-s,s),(-BD,0),(-s,-s),(0,-BD),(s,-s)]
 for block in (0,1,4,5):
  for i in range(8):
   for j in range(8):br[8*block+i][8*block+j],bi[8*block+i][8*block+j]=vals[(i*j)%8]
 minor=json.loads((BASE/'sources/EXACT_MINOR_CHART.json').read_text())
 assert minor['row']==0 and minor['dyadic_exponent']==80
 cols=minor['columns'];assert cols==[27,31,11,28,47,10,30,59,51]
 rr,ri=minor['inverse_real'],minor['inverse_imag'];shapecheck(rr,[9,9]);shapecheck(ri,[9,9]);RS=1<<80
 # Form actual center augmented matrix M explicitly, then apply R.
 # This differs from the constructor's contraction-first multiplication order.
 h0cols=tuple([[row[k] for k in cols] for row in part] for part in hs[0])
 x=cproduct(hs[1],cproduct((br,bi),h0cols));XD=D*D*BD
 mr=[[sum(greens[j][0][v]*x[0][v][k] for v in range(64)) for k in range(9)] for j in range(8)]
 mi=[[sum(greens[j][0][v]*x[1][v][k] for v in range(64)) for k in range(9)] for j in range(8)]
 MD=L*XD;mr.append([MD]*9);mi.append([0]*9)
 prod=cproduct((rr,ri),(mr,mi));PD=RS*MD
 for i in range(9):prod[0][i][i]-=PD
 center=F(normnum(prod),PD)
 fr=[[sum(rr[r][j]*greens[j][0][k] for j in range(8)) for k in range(64)] for r in range(9)]
 fi=[[sum(ri[r][j]*greens[j][0][k] for j in range(8)) for k in range(64)] for r in range(9)]
 beta=F(normnum((fr,fi)),RS*L);bankerr=F(8,Q)
 delta=8*Ls[1]*rho*(hb[0]+Ls[0]*rho)+8*hb[1]*Ls[0]*rho+hb[1]*bankerr*hb[0]
 pert=9*beta*delta;total=center+pert;assert total<F(2659,10**9)<1
 expected=json.loads((BASE/'sources/OUTER_PREFIX_REJECTION_CERTIFICATE.json').read_text())
 bounds={'derived_seed_root_bound':root,'accepted_seed_root_radius_used':rho,'bank_enclosure_error_bound':bankerr,'preconditioned_Green_row_norm':beta,'center_preconditioned_minor_defect':center,'seed_and_bank_minor_perturbation':pert,'total_preconditioned_minor_defect':total}
 for key,value in bounds.items():assert value==as_fraction(expected[key]),key
 assert hb==list(map(as_fraction,expected['inner_layer_center_bounds'])) and Ls==list(map(as_fraction,expected['inner_layer_direction_bounds']))
 assert poles==expected['fixed_large_inverse_guards']
 result={'status':'ACCEPTED_OUTER_ONLY_REJECTION','source_fractions_match_exactly':True,'arithmetic':'stdlib Gaussian integers and Fractions','chart_sha256':sha,'orders':orders,'selected_row':0,'selected_columns':cols,'all_large_inverse_entries_checked':8*64*64,'bounds':{k:fraction_record(v) for k,v in bounds.items()},'inner_layer_center_bounds':list(map(fraction_record,hb)),'inner_layer_direction_bounds':list(map(fraction_record,Ls)),'prefix_variation_bound':fraction_record(delta),'sqrt2_enclosure':{'Q':str(Q),'s':str(s)},'frozen_inner_coefficients':1024,'free_outer_coefficients':512,'scope':'Two literal inner pullbacks of the accepted algebraic N16 seed cannot be corrected by any outer endpoints; full 1536-variable N64 family remains open.'}
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('ACCEPTED',json.dumps({k:float(v) for k,v in bounds.items()},sort_keys=True),flush=True)
if __name__=='__main__':verify()
