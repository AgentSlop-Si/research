"""Floating-point non-guarantee diagnostic, separate from exact field theorem."""
import math,json
rows=[]
for n in (128,384,1024,4096,16384):
    theta=math.pi/n
    # cond_2([[1,1],[1,exp(2*pi*i/n)]]) = cot(pi/(2N)).
    cond=1.0/math.tan(theta/2)
    rows.append({'N':n,'adjacent_two_root_vandermonde_cond2':cond,
                 'cond2_divided_by_N':cond/n})
o={'purpose':'Witness ill-conditioned complex Prony recovery even at s=2. This is NOT a forward-error proof or finite-field phenomenon.',
   'theorem':'cond_2([[1,1],[1,exp(2*pi*i/N)]])=cot(pi/(2N)) ~ 2N/pi',
   'rows':rows}
with open('PRECISION_GATE.json','w') as f:json.dump(o,f,indent=2)
print(json.dumps(o,indent=2))
