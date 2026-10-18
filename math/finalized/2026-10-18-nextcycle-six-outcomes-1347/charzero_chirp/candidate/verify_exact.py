#!/usr/bin/env python3
"""Self-contained exact arithmetic verification; no search, floats, network or supplied historical code."""
import copy,hashlib,itertools,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
P=17

def poly(raw):return {tuple(e):c%P for e,c in raw if c%P}
def add(a,b):
 r=dict(a)
 for e,c in b.items():
  r[e]=(r.get(e,0)+c)%P
  if not r[e]:del r[e]
 return r
def mul(a,b):
 r={}
 for e,c in a.items():
  for f,d in b.items():
   z=tuple(x+y for x,y in zip(e,f));r[z]=(r.get(z,0)+c*d)%P
 return {e:c for e,c in r.items() if c}
def valid_certificate(c):
 r={}
 for h,f in zip(c['multipliers'],c['inputs']):r=add(r,mul(poly(h),poly(f)))
 return r==poly(c['target'])

def cyc_pow(k):
 k%=16;r=[0]*8;r[k%8]=1 if k<8 else -1;return tuple(r)
def cadd(a,b):return tuple(x+y for x,y in zip(a,b))
def cmul(a,b):
 r=[0]*8
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   t=i+j;r[t%8]+=x*y*(1 if t<8 else -1)
 return tuple(r)
ZERO=(0,)*8

def convolution(a,b):return [sumc(cmul(a[j],b[(t-j)%8]) for j in range(8)) for t in range(8)]
def sumc(values):
 r=ZERO
 for v in values:r=cadd(r,v)
 return r

def main():
 cs=json.loads((BASE/'CERTIFICATES.json').read_text())
 assert cs['modulus']==17 and cs['root_zeta']==3 and cs['a']==6 and cs['b']==4
 assert pow(3,16,17)==1 and pow(3,8,17)==16 and pow(6,4,17)==4
 results={}
 for name in ['330','312','510','420','411']:
  c=cs[name];assert valid_certificate(c),name
  bad=copy.deepcopy(c);bad['target'][0][1]=(bad['target'][0][1]+1)%17
  assert not valid_certificate(bad),name+' corruption escaped'
  results[name]={'identity_verified':True,'multiplier_term_counts':[len(h) for h in c['multipliers']],'corrupted_target_rejected':True}
 # Integral cyclotomic arithmetic proves all 64 entries of C Q = 8 I.
 q=[cyc_pow(t*t) for t in range(8)];ck=[cyc_pow(-t*t) for t in range(8)]
 got=convolution(ck,q);expected=[tuple([8]+[0]*7)]+[ZERO]*7
 assert got==expected
 bad=list(q);bad[1]=cyc_pow(0);assert convolution(ck,bad)!=expected
 # Gauge-shift and stride-3 symmetry identities for all eight coefficients.
 for r in range(8):
  for t in range(8):
   assert q[(t-r)%8]==cmul(cyc_pow(r*r-2*r*t),q[t])
 for t in range(8):assert q[(3*t)%8]==cmul(cyc_pow(8*t),q[t])
 # The exact parity identity Q(-x)=x^4 Q(x).
 for t in range(8):assert q[(t-4)%8]==tuple(((-1)**t)*v for v in q[t])
 # The only length-six cases left after the hand parity classes.
 counts=[]
 for n1 in range(7):
  for n2 in range(7-n1):
   for n3 in range(7-n1-n2):
    n4=6-n1-n2-n3
    if n1>=n3 and n1+n3>=4:counts.append((n1,n2,n3,n4))
 arithmetic={(3,1,2,0):'312',(4,1,1,0):'411',(3,0,3,0):'330',(4,0,2,0):'420',(5,0,1,0):'510'}
 classes={}
 for c in counts:
  r=c[0]+c[2]
  if r==4:kind='four_odd_parity_class'
  elif r==5 and c[3]==1:kind='five_odd_stride4_hand_exclusion'
  elif r==5 and c[0]==5:kind='five_stride1_even_ratio_conflict'
  elif r==6 and c[0]==6:kind='degree_six_missing_coefficient'
  else:kind=arithmetic[c]
  classes[str(c)]=kind
 for c in arithmetic:assert c[0]+2*c[1]+c[2]+4*c[3]<8
 # Exceptional denominator/field tests used in the hand proof at the fixed prime.
 a,b=6,4
 assert a*a%17 != (2*(-3+4*b)*pow(9,-1,17))%17
 assert (1+3*b)%17!=0 and (a**4-a*a+1)%17!=0
 result={'status':'PASS','claim':'N=8 exact legal pure-shift-resolvent minimum is 7 over C and a splitting field of Q over Q(zeta16).','proof_type':'Symbolic parity classification, guarded algebraic specialization, explicit ideal identities and splitting construction.','arithmetic_certificates':results,'integral_cyclotomic_inverse_all_64_entries':True,'gauge_shift_cases':64,'stride_symmetry_coefficients':8,'six_stage_pattern_count':len(counts),'six_stage_pattern_coverage':classes,'mutation_controls':6,'historical_F17_search_not_executed':True,'no_status_score_or_census_changes':True}
 (BASE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
