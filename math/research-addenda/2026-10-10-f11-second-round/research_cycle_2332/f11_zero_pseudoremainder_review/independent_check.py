#!/usr/bin/env python3
"""Fresh independent exact verifier; reads inert JSON only, never imports author code."""
import json, hashlib, math, time
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
OUT=Path('research_cycle_2332/f11_zero_pseudoremainder_review')
CAND=Path('research_cycle_2325/f11_zero_resultant')
BASE=Path('research_cycle_2303/regular_hzero_analysis/CERTIFICATE.json')
ATLAS=Path('research_cycle_2014/fused_chart_atlas/CERTIFICATE.json')
BR=Path('research_cycle_2308/hzero_continuation_review/RECEIPT.json')
started=time.time(); checks={}; pins={}; negative={}
def read(p):
 p=Path(p); raw=p.read_bytes(); pins[str(p)]=hashlib.sha256(raw).hexdigest(); return json.loads(raw)
def write(n,d): (OUT/n).write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
def ck(n,b):
 if not b: raise AssertionError(n)
 checks[n]=True;print('PASS',n,round(time.time()-started,2),flush=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
A=read(BASE); T=read(ATLAS); BReceipt=read(BR); D=read(CAND/'DERIVATION.json'); E=read(CAND/'ELIMINATION.json')
ck('accepted_base_receipt_pin',pins[str(BR)]=='8d9767ba65f61fce39676dadd7b187d520ceb3f770b8f8b4401bfaf6c6b34127')
ck('accepted_base_certificate_pin',pins[str(BASE)]==BReceipt['candidate_sha256']=='779b560d09cdf9dc6cae1afe5cd568f267bbf1db545c0639dcc937b4b00f4c2b')
ck('accepted_atlas_pin',pins[str(ATLAS)]==BReceipt['accepted_atlas_sha256'])
for path,h in D['source_pins'].items(): ck('source_file_'+path,sha(path)==h);pins[path]=h
ck('source_pin_coverage',all(D['source_pins'].get(p)==h for p,h in A['source_pins'].items()))
# K coefficients are a length-10 integer vector and a positive common denominator.
# Multiplication reduces with zeta^11=1 followed by zeta^10=-sum(zeta^0,...,zeta^9).
Z=((0,)*10,1); I=((1,)+(0,)*9,1)
ops={'coefficient_products':0,'double_product_checks':0}
def norm(a,d=1):
 assert len(a)==10 and d!=0
 if d<0:a=tuple(-x for x in a);d=-d
 g=math.gcd(d,*a)
 return (tuple(x//g for x in a),d//g)
def ka(a,b):
 if a==Z:return b
 if b==Z:return a
 av,ad=a;bv,bd=b;g=math.gcd(ad,bd);u=bd//g;v=ad//g
 return norm(tuple(x*u+y*v for x,y in zip(av,bv)),ad*u)
def kn(a):return (tuple(-x for x in a[0]),a[1])
@lru_cache(maxsize=250000)
def km(a,b):
 if a==Z or b==Z:return Z
 if a==I:return b
 if b==I:return a
 av,ad=a;bv,bd=b
 r=[0]*11
 for i,x in enumerate(av):
  if x:
   for j,y in enumerate(bv):
    if y:r[(i+j)%11]+=x*y
 c=norm(tuple(r[i]-r[10] for i in range(10)),ad*bd)
 ops['coefficient_products']+=1
 # A second independent reduction on the first 250 and regular later products.
 if ops['coefficient_products']<=250 or ops['coefficient_products']%997==0:
  t=[0]*19
  for i,x in enumerate(av):
   for j,y in enumerate(bv):t[i+j]+=x*y
  for i in range(18,9,-1):
   v=t[i]
   for j in range(11):t[i-10+j]-=v
  assert norm(tuple(t[:10]),ad*bd)==c
  ops['double_product_checks']+=1
 return c
def ki(a):
 # Invert one nonzero element of K by exact rational Gaussian elimination.
 cols=[km(a,(tuple(1 if i==j else 0 for i in range(10)),1)) for j in range(10)]
 mat=[[Fraction(cols[j][0][i],cols[j][1]) for j in range(10)]+[Fraction(i==0)] for i in range(10)]
 for j in range(10):
  p=next(i for i in range(j,10) if mat[i][j]);mat[j],mat[p]=mat[p],mat[j]
  lead=mat[j][j];mat[j]=[v/lead for v in mat[j]]
  for i in range(10):
   if i!=j and mat[i][j]:
    f=mat[i][j];mat[i]=[v-f*w for v,w in zip(mat[i],mat[j])]
 values=[mat[i][-1] for i in range(10)];dd=math.lcm(*(v.denominator for v in values))
 out=norm(tuple(int(v*dd) for v in values),dd);assert km(a,out)==I;return out
# Multivariate polynomials are sparse dictionaries from exponent tuples to K.
def load(data,n=None):
 p={}
 for m,v,d in data:
  if n is None:n=len(m)
  assert len(m)==n and all(type(x)==int and x>=0 for x in m)
  assert len(v)==10 and all(type(x)==int for x in v) and type(d)==int and d>0
  k=norm(tuple(v),d);assert k!=Z and k==(tuple(v),d) and tuple(m) not in p
  p[tuple(m)]=k
 return p
def enc(p):return [[list(m),list(v),d] for m,(v,d) in sorted(p.items())]
def pc(a,n):return {} if a==Z else {(0,)*n:a}
def pv(i,n):return {tuple(int(i==j) for j in range(n)):I}
def pa(a,b):
 r=dict(a)
 for m,k in b.items():
  v=ka(r.get(m,Z),k)
  if v==Z:r.pop(m,None)
  else:r[m]=v
 return r
def pn(a):return {m:kn(k) for m,k in a.items()}
def ps(a,b):return pa(a,pn(b))
def pm(a,b):
 r={}
 for u,k in a.items():
  for v,l in b.items():
   m=tuple(x+y for x,y in zip(u,v));w=ka(r.get(m,Z),km(k,l))
   if w==Z:r.pop(m,None)
   else:r[m]=w
 return r
def pp(a,k,n=None):
 if n is None:n=len(next(iter(a)))
 r=pc(I,n)
 while k:
  if k&1:r=pm(r,a)
  k//=2
  if k:a=pm(a,a)
 return r
def scalar(a,k):return {m:km(v,k) for m,v in a.items() if km(v,k)!=Z}
def shift(a,i,k):return {tuple(v+(k if j==i else 0) for j,v in enumerate(m)):w for m,w in a.items()}
def coef(a,i,j):return {tuple(0 if h==i else x for h,x in enumerate(m)):v for m,v in a.items() if m[i]==j}
def deg(a,i):return max((m[i] for m in a),default=-1)
def substitute(p,srcvars,mapping,n):
 r={};cache={}
 for m,k in p.items():
  t=pc(k,n)
  for v,powr in zip(srcvars,m):
   if powr:
    assert v in mapping,('missing coordinate',v)
    key=(v,powr)
    if key not in cache:cache[key]=pp(mapping[v],powr,n)
    t=pm(t,cache[key])
  r=pa(r,t)
 return r
# Validate canonical content-addressed original source polynomials, including all 50+19.
source_cache={};source_data={};count=0
for ref,path in A['source_polynomial_refs'].items():
 if path not in source_cache:source_cache[path]=read(path)
 src=source_cache[path]; raw=src['polynomials'][ref]
 assert hashlib.sha256(json.dumps(raw,separators=(',',':')).encode()).hexdigest()==ref
 p=load(raw,len(src['variables']));source_data[ref]=(p,src['variables']);count+=len(p)
ck('all_80_original_polynomial_hashes_and_canonical_terms',len(source_data)==80 and count==A['source_term_count'])
chart=D['preserved_chart']; ck('verbatim_full_chart_preservation',chart==A['preserved_chart'])
ck('all_50_original_residuals_retained',len(chart['retained_equations'])==50)
ck('all_19_original_guards_retained',len(chart['retained_guards'])==19)
ck('all_original_reference_bindings_present',all(r in source_data for r in list(chart['retained_equations'].values())+list(chart['retained_guards'].values())))
ck('optional_zero_and_branch_predicates_preserved',chart['additional_guards']==['b!=0','Q_a!=0','F_A!=0','F_B!=0'] and chart['conditions']==['Q_H=0','d!=0','F_M!=0'])
# Bind accepted atlas expressions without importing its programs.
b,c,q,e=[pv(i,4) for i in range(4)];one=pc(I,4);z=pc(((0,1)+(0,)*8,1),4)
map4={11:b,34:c,41:q,83:e,22:one,49:ps(z,c)}
def at4(k):return substitute(load(T['polynomials'][k]),T['variables'],map4,4)
def orig4(ref):
 p,vs=source_data[ref];return substitute(p,vs,map4,4)
AP={k:load(v,4) for k,v in A['polynomials'].items() if k in ['N25_cleared_numerator','N25_cleared_denominator']}
N25,D25clear=AP['N25_cleared_numerator'],AP['N25_cleared_denominator']
Nd,Dd=at4('Q_d_num'),at4('Q_d_den');N39,D39=at4('F_N39'),at4('F_D39');AA,BB,a=at4('F_A'),at4('F_B'),at4('Q_a')
d25=orig4(chart['retained_guards']['D25'])
x39def=next(v for v in chart['definitions'] if v['variable']==39)
ck('original_N39_rebind',orig4(x39def['numerator'])==N39)
ck('original_D39_rebind',orig4(x39def['denominator'])==D39)
ck('original_D25_rebind',d25==at4('Q_D25'))
ck('accepted_d_denominator_factorization',Dd==pm(pm(pm(pm(pp(z,4),b),q),e),d25))
ck('accepted_x25_denominator_factorization',D25clear==pm(pm(pm(pm(AA,q),a),Dd),d25))
ck('source_E25_binding',D['selected_original_residual']=='25' and D['selected_original_residual_ref']==chart['retained_equations']['25'])
source,vs=source_data[D['selected_original_residual_ref']]
ck('original_E25_55_terms',len(source)==55)
num={25:N25,39:N39,65:Nd,88:pn(BB)};den={25:D25clear,39:D39,65:Dd,88:AA}
for v in den:ck('clearing_power_'+str(v),max(m[vs.index(v)] for m in source)==D['clearing_powers'][str(v)]==1)
clear={};used=set()
for powers,k in source.items():
 t=pc(k,4)
 for v,power in zip(vs,powers):
  if v in den:
   t=pm(t,pp(num[v],power,4));t=pm(t,pp(den[v],1-power,4))
  elif power:
   assert v in map4;t=pm(t,pp(map4[v],power,4));used.add(v)
 clear=pa(clear,t)
ck('original_E25_termwise_clearing',clear==load(D['E25_clear'],4))
ck('cleared_E25_size_degrees',len(clear)==882 and [deg(clear,i) for i in range(4)]==[10,4,8,6])
factor=pm(pm(pm(pm(pm(pp(q,2),b),e),pp(d25,2)),pp(a,2)),D39)
reduced=load(D['E25_reduced'],4)
ck('guarded_cancellation_factor',factor==load(D['E25_cancel'],4))
ck('guarded_cancellation_ledger',D['E25_cancel_ledger']==[['q',2],['b',1],['e',1],['D25',2],['a',2],['D39',1]])
ck('exact_clear_factor_reduced_identity',clear==pm(factor,reduced))
ck('reduced_E25_size_degrees',len(reduced)==204 and [deg(reduced,i) for i in range(4)]==[6,4,3,3])
# Coefficient order now (e,c,q); H reduction only inverts its fixed K leading coefficient.
ee,cc,qq=[pv(i,3) for i in range(3)];map3={83:ee,34:cc,41:qq}
def at3(k):return substitute(load(T['polynomials'][k]),T['variables'],map3,3)
H=load(D['H'],3);C0=at3('Q_C0');C1=at3('Q_C1')
ck('H_bound_to_accepted_atlas',H==at3('Q_H') and deg(H,0)==3)
def accepted_univariate(k):return substitute(load(A['polynomials'][k],4),['b','c','q','e'],{'e':ee},3)
ck('accepted_C1_inverse_rechecked',pa(pm(C1,accepted_univariate('C1_inverse')),pm(H,accepted_univariate('C1_inverse_H_multiplier')))==pc(I,3))
ck('accepted_polynomial_b_relation_rechecked',pa(pm(C1,accepted_univariate('new_b_polynomial')),C0)==pm(H,accepted_univariate('b_relation_quotient')))
hlc=H[(3,0,0)];inv_hlc=ki(hlc)
def divH(p):
 r=dict(p);quot={}
 while any(m[0]>=3 for m in r):
  m=max(m for m in r if m[0]>=3);k=km(r[m],inv_hlc);v=(m[0]-3,m[1],m[2]);term={v:k}
  quot=pa(quot,term);r=ps(r,pm(term,H))
 return quot,r
def red(p):return divH(p)[1]
def rm(a,b):return red(pm(a,b))
T25={};c0powers=[pp(pn(C0),i,3) for i in range(7)];c1powers=[pp(C1,i,3) for i in range(7)]
for (bp,cp,qp,ep),k in reduced.items():
 term=pm(c0powers[bp],c1powers[6-bp]);term=shift(shift(shift(scalar(term,k),0,ep),1,cp),2,qp);T25=pa(T25,term)
HQ,S=divH(T25)
ck('fresh_E25_H_division_quotient',HQ==load(D['E25_H_quotient'],3))
ck('fresh_E25_H_division_remainder',S==load(D['E25_H_remainder'],3))
ck('E25_remainder_54_terms_degrees_2_4_3',len(S)==54 and [deg(S,i) for i in range(3)]==[2,4,3])
P=load(A['E41_H_reduction']['remainder'],3)
ck('E41_accepted_remainder_unchanged',P==load(D['E41_H_remainder'],3))
p=[coef(P,2,i) for i in range(3)];s=[coef(S,2,i) for i in range(4)]
ck('P_q_coefficient_arrays',p==[load(v,3) for v in E['P_coefficients_ascending_q']])
ck('S_q_coefficient_arrays',s==[load(v,3) for v in E['S_coefficients_ascending_q']])
# Determinant computed division-free by exterior-product row accumulation.
cols=[shift(P,2,2),shift(P,2,1),P,shift(S,2,1),S]
matrix=[[coef(f,2,r) for f in cols] for r in range(4,-1,-1)]
def determinant(mat):
 n=len(mat);acc={0:pc(I,3)}
 for row in mat:
  new={}
  for mask,value in acc.items():
   for j,x in enumerate(row):
    if mask>>j&1:continue
    term=rm(value,x)
    if (mask>>(j+1)).bit_count()%2:term=pn(term)
    mask2=mask|1<<j;new[mask2]=pa(new.get(mask2,{}),term)
  acc=new
 return acc[(1<<n)-1]
ck('fixed_sylvester_layout',E['sylvester_rows']==['q^4','q^3','q^2','q','1'] and E['sylvester_column_polynomials']==['q^2*P','q*P','P','q*S','S'])
det=determinant(matrix)
ck('division_free_Sylvester_determinant_zero',not det and not load(E['resultant_mod_H'],3))
one3=pc(I,3)
identity5=[[one3 if i==j else {} for j in range(5)] for i in range(5)]
ck('determinant_identity_matrix_control',determinant(identity5)==one3)
identity5[0],identity5[1]=identity5[1],identity5[0]
ck('determinant_sign_control',determinant(identity5)==pn(one3))
controlP=pa(pp(qq,2),one3);controlS=pa(pa(pp(qq,3),qq),one3)
controlcols=[shift(controlP,2,2),shift(controlP,2,1),controlP,shift(controlS,2,1),controlS]
controlmatrix=[[coef(f,2,r) for f in controlcols] for r in range(4,-1,-1)]
ck('nonzero_Sylvester_resultant_control',determinant(controlmatrix)==one3)
U,V,QB=[load(E[k],3) for k in ['Bezout_U','Bezout_V','Bezout_H_quotient']]
syzygy_vector=[coef(U,2,2),coef(U,2,1),coef(U,2,0),coef(V,2,1),coef(V,2,0)]
cofactor_row=None
for r in range(5):
 vector=[]
 for col in range(5):
  submatrix=[[x for j,x in enumerate(row) if j!=col] for i,row in enumerate(matrix) if i!=r]
  value=determinant(submatrix)
  vector.append(pn(value) if (r+col)%2 else value)
 if vector==syzygy_vector:cofactor_row=r;break
ck('syzygy_is_Sylvester_cofactor_vector',cofactor_row is not None)
ck('nonzero_syzygy_multipliers',bool(U) and bool(V) and len(U)==120 and len(V)==75 and deg(U,2)<=2 and deg(V,2)<=1)
ck('full_polynomial_syzygy_identity',pa(pm(U,P),pm(V,S))==pm(H,QB))
# Fresh pseudo-division, with no division by ell or any parameter polynomial.
ell=p[2];prem=dict(S);pq={};mult=pc(I,3)
for step in range(2):
 d=deg(prem,2);lc=coef(prem,2,d)
 ck('pseudo_step_degree_'+str(step),d==3-step and E['pseudo_steps'][step]['q_degree']==d-1)
 ck('pseudo_step_leading_coefficient_'+str(step),load(E['pseudo_steps'][step]['lc'],3)==lc)
 fac=shift(lc,2,d-2);pq=pa(rm(ell,pq),fac);prem=ps(rm(ell,prem),rm(fac,P));mult=rm(ell,mult)
L=load(E['pseudo_remainder'],3);QP=load(E['pseudo_quotient'],3);M=load(E['pseudo_multiplier'],3);QH=load(E['pseudo_H_quotient'],3)
ck('fresh_pseudo_quotient',pq==QP)
ck('fresh_pseudo_multiplier',mult==M==rm(ell,ell))
ck('fresh_pseudo_remainder',prem==L)
ck('full_polynomial_pseudo_identity',ps(ps(pm(M,S),pm(QP,P)),L)==pm(H,QH))
L0,L1=coef(L,2,0),coef(L,2,1)
ck('linear_pseudoremainder_term_degrees',len(L)==60 and len(L0)==len(L1)==30 and [deg(L,i) for i in range(3)]==[2,9,1])
f1=red(ps(ps(pa(pm(pm(ell,ell),s[1]),pm(pm(s[3],p[1]),p[1])),pm(pm(ell,s[3]),p[0])),pm(pm(ell,s[2]),p[1])))
f0=red(pa(ps(pm(pm(ell,ell),s[0]),pm(pm(ell,s[2]),p[0])),pm(pm(s[3],p[1]),p[0])))
ck('displayed_L1_formula',f1==L1);ck('displayed_L0_formula',f0==L0)
# Mutation controls on independently computed invariants.
unit4=pc(I,4);unit3=pc(I,3)
negative['changed_original_E25_coefficient']=pa(clear,pm(pm(pm(D25clear,D39),Dd),AA))!=load(D['E25_clear'],4)
negative['changed_cancellation_factor']=pm(pa(factor,unit4),reduced)!=clear
negative['changed_remainder']=pa(S,unit3)!=red(T25)
negative['changed_syzygy_coefficient']=pa(pm(pa(U,unit3),P),pm(V,S))!=pm(H,QB)
negative['changed_pseudoremainder']=ps(ps(pm(M,S),pm(QP,P)),pa(L,unit3))!=pm(H,QH)
for k in chart['retained_equations']:
 changed=json.loads(json.dumps(chart));del changed['retained_equations'][k];negative['dropped_E'+k]=changed!=A['preserved_chart']
for k in chart['retained_guards']:
 changed=json.loads(json.dumps(chart));del changed['retained_guards'][k];negative['dropped_guard_'+k]=changed!=A['preserved_chart']
for guard in ['L1!=0','ell!=0','s3!=0','c!=0','x0!=0','x49!=0']:
 changed=json.loads(json.dumps(chart));changed['additional_guards'].append(guard);negative['added_unproved_'+guard]=changed!=A['preserved_chart']
# The textbook leading-degree warning is checked independently with integer polynomials.
wP=pa(qq,unit3);wS=pa(qq,pc(((2,)+(0,)*9,1),3));wcols=[shift(wP,2,1),wP,shift(wS,2,1),wS]
wmat=[[coef(f,2,j) for f in wcols] for j in range(3,-1,-1)]
ck('degree_drop_zero_determinant_counterexample',not determinant(wmat) and ps(wS,wP)==unit3)
ck('all_negative_controls_rejected',all(negative.values()))
ck('claim_limits',E['claims']=={'dimension_claimed':False,'feasibility_decided':False,'no_new_nonzero_assumptions':True,'novelty_claimed':False,'q_eliminated_as_necessary_constraint':False,'resultant_identically_zero_mod_H':True})
ck('all_inputs_still_match_pins',all(sha(p)==h for p,h in pins.items()))
write('INPUT_PINS.json',pins);write('EXACT_CHECKS.json',checks);write('NEGATIVE_CONTROLS.json',negative)
write('INDEPENDENT_LINEAR_COEFFICIENTS.json',{'variables':['e','c','q'],'L0':enc(L0),'L1':enc(L1),'H':enc(H),'conditional_cover':['L1 != 0: q = -L0/L1, retain and test the entire original chart','L1 = 0: retain q and impose L0 = 0 together with the entire original chart'],'new_nonzero_restrictions':[]})
write('ARITHMETIC_RESULT.json',{'status':'PASS','method':'Fresh standard-library exact rational cyclotomic sparse arithmetic; inert JSON only; division-free exterior-product determinant; fresh pseudo-division. Selected coefficient products cross-checked by descending Phi11 reduction.','counts':{'E25_source':len(source),'E25_clear':len(clear),'E25_reduced':len(reduced),'S':len(S),'P':len(P),'L0':len(L0),'L1':len(L1),'residuals':50,'guards':19,'original_polynomials':len(source_data),'original_source_terms':count},'ops':ops,'elapsed_seconds':time.time()-started,'negative_control_count':len(negative),'author_program_execution':False,'historical_program_execution':False,'new_optional_zero_exclusions':[],'parameter_polynomial_inversions':[]})
print('ARITHMETIC REVIEW COMPLETE',round(time.time()-started,2),flush=True)
