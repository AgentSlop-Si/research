"""Empirical structure diagnostic, explicitly NOT a universal symbolic proof."""
import random,json
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects,Work,direct_one_frequency
from resultant_gate import D,resultant_at,interp_newton,strip_trivial_factors

def main():
 p,n=2013265921,128;e=RecurrenceGreen(n,p,31)
 rng=random.Random(960210)
 records={}
 for family in ('generic','dense-K2','one-character','input-sparse'):
  for t in range(100):
   if family=='generic':r=[rng.randrange(p) for _ in range(n)]
   elif family=='dense-K2':
    h=[0]*n
    j,k=rng.sample(range(n),2);h[j],h[k]=rng.randrange(1,p),rng.randrange(1,p)
    r=dense_from_shift_defects(h,rng.randrange(1,n),rng.randrange(2,p),p)
   elif family=='one-character':
    w=e.powers[rng.randrange(n)];r=[pow(w,j,p) for j in range(n)]
   else:
    r=[0]*n
    j,k=rng.sample(range(n),2);r[j],r[k]=rng.randrange(1,p),rng.randrange(1,p)
   R=[direct_one_frequency(r,e.powers[k],p) for k in range(8)]
   coeff=interp_newton([resultant_at(R,w,p,Work()) for w in range(D+1)],p,Work())
   if not coeff:key='zero-resultant'
   else:
    reduced,z,o=strip_trivial_factors(coeff,p,Work())
    pal=reduced==reduced[::-1]
    key=f'Tdegree{len(coeff)-1}:w^{z}:(w-1)^{o}:Udegree{len(reduced)-1}:pal{pal}'
   records[(family,key)]=records.get((family,key),0)+1
 out={'N':n,'p':p,'samples_per_family':100,
      'counts':[{'family':f,'pattern':k,'count':v} for (f,k),v in sorted(records.items())],
      'caveat':'Finite-field numerical pattern evidence, NOT symbolic proof; Phase20 uses degree<=45 and per-input exact factor divisions only.'}
 with open('RESULTANT_PATTERN_AUDIT.json','w') as f:json.dump(out,f,indent=2)
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
