"""Fresh exact Q[z]/Phi_5 control; no uploaded programs imported."""
import json
from pathlib import Path
from math import comb

def red(a):
    a=list(a)+[0]*max(0,5-len(a))
    for k in range(len(a)-1,3,-1):
        q=a[k];a[k]=0
        for j in range(4): a[k-4+j]-=q
    return tuple(a[:4])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):
    c=[0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return red(c)
one=(1,0,0,0);z=(0,1,0,0)
roots=[one]
for i in range(1,5):roots.append(mul(roots[-1],z))
phi=add(add(one,z),roots[4])
assert add(mul(phi,phi),tuple(-x for x in add(phi,one)))==(0,0,0,0)
assert mul(phi,add(one,roots[2]))==z
assert mul(phi,add(one,roots[3]))==roots[4]
edges=[]
for i in range(5):
    for j in range(5):
        k=i*j%5
        labels=(0,2) if k==1 else ((0,3) if k==4 else (k,))
        amp=phi if k in (1,4) else one
        actual=(0,0,0,0)
        for label in labels:
            edges.append({'source':j,'target':i,'label':label,'amplitude':'phi' if k in (1,4) else '1'})
            actual=add(actual,mul(amp,roots[label]))
        assert actual==roots[k]
assert len(edges)==33
assert set(e['label'] for e in edges)=={0,2,3}
assert comb(1+3,3)==4<5
result={'status':'PASS','field':'Q[z]/(1+z+z^2+z^3+z^4)','embedding':'z=exp(-2*pi*i/5)','positive_amplitude':'phi=1+2*cos(2*pi/5)>0','entries_verified':25,'edges':33,'depth':1,'distinct_phase_labels':3,'binomial_label_bound':4,'p':5,'scope':'Counterexample only to extending the positive-rational phase-alphabet exclusion to arbitrary positive real amplitudes; no contradiction to pure-root/rational theorem and no FFT speedup.','edge_certificate':edges}
Path(__file__).with_name('POSITIVE_REAL_PALETTE_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if k!='edge_certificate'})
