#!/usr/bin/env python3
"""Export two exact modular-component controls using newly authored local code."""
import json
from pathlib import Path
from fresh_modular_obstruction_test import Field,construct,guard,zgcd,zmod,divmodp,trim
s,p=63,5
factors=[[1,0,1,3,1,0,1],[1,1,2,0,2,1,1]]
out=[]
for f in factors:
 F=Field(p,f);U,delta=construct(F,s,F.q);V,delta_i=construct(F,s,F.power(F.q,s-1))
 checks={}
 for exponent in [25,125]:
  a=f[:];b=trim(list(F.sub(F.power(F.q,exponent),F.q)))
  while b:a,b=b,divmodp(a,b,p)[1]
  checks[str(exponent)]=len(a)-1
 assert checks=={'25':0,'125':0} and F.power(F.q,5**6)==F.q
 assert F.power(F.q,63)==F.one and F.power(F.q,21)!=F.one and F.power(F.q,9)!=F.one
 row={'irreducibility_gcd_degrees':checks,'q_to_5pow6_equals_q':True,'q_has_order_63':True,'s':s,'p':p,'factor_ascending':f,'U_ascending':U,'inverse_U_ascending':V,'delta':delta,'inverse_delta':delta_i,'guard_gcd_degrees':guard(F,s,U),'inverse_guard_gcd_degrees':guard(F,s,V)}
 for name,W in [('direct',U),('inverse',V)]:
  G=zgcd(F,W,[F.one]+[F.zero]*(s-1)+[F.one]);il=F.inv(G[-1]);G=[F.mul(c,il) for c in G]
  row[name+'_monic_resonance_gcd']=G
  assert zmod(F,W,G)==[] and zmod(F,[F.one]+[F.zero]*(s-1)+[F.one],G)==[]
 out.append(row)
Path(__file__).with_name('S63_P5_COMPONENT_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
for r in out:
 print(r['factor_ascending'],'delta',r['delta'],'degrees',r['guard_gcd_degrees'],'gcd',r['direct_monic_resonance_gcd'])
