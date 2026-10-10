"""Separate all-basis verification against the closed-form Fourier matrix."""
import json,random
from math import gcd,lcm
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
from crt15_engine import make_plan,transform,predicted

def audit():
    entries=0;identities=0;max_n=0
    for p,g in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
        for n in (15,30,60,120,240,480):
            if (p-1)%n:continue
            G=n//15;w=n_root(n,p,g)
            GT=make_plan(n,p,g,mode='gt');CT=make_plan(n,p,g,mode='ct')
            for j in range(n):
                basis=[0]*n;basis[j]=1
                expected=[pow(w,j*k%n,p) for k in range(n)]
                for plan,inner in ((GT,'gt'),(CT,'gt'),(CT,'ct')):
                    result,c=transform(basis,plan,inner=inner)
                    assert result==expected,(n,j,inner)
                    assert c.total()==predicted(G,inner=inner,outer='gt' if plan is GT else 'ct')[2]
                    identities+=n
                entries+=n;max_n=max(max_n,n)
        print('finished exact basis field',p)
    controls=0
    for a,b in ((2,2),(4,4),(4,8),(3,3),(3,5),(3,8),(5,8),(3,10)):
        n=a*b
        if (P-1)%n:continue
        w=n_root(n,P,GENERATOR)
        if gcd(a,b)>1:
            assert pow(w,lcm(a,b),P)!=1
            controls+=1
        else:
            ea=b*pow(b,-1,a);eb=a*pow(a,-1,b)
            wa=pow(w,b,P);wb=pow(w,a,P)
            for u in range(a):
              for v in range(b):
                for r in range(a):
                  for s in range(b):
                    left=pow(w,((ea*u+eb*v)%n)*((b*r+a*s)%n)%n,P)
                    right=pow(wa,u*r,P)*pow(wb,v*s,P)%P
                    assert left==right
                    controls+=1
    output=dict(status='PASS',prime_fields=[P,ALT_P],sizes=[15,30,60,120,240,480],
      max_size=max_n,independent_matrix_entries_per_implementation=entries,
      exact_matrix_equality_checks=identities,
      CRT_permutation_and_obstruction_checks=controls,
      correct_for_all_inputs_by_linearity=True,
      scope='transform lengths 15*2^t in suitable exact prime fields; NOT complex bit complexity')
    with open('AUDIT_PHASE27.json','w') as f:json.dump(output,f,indent=2)
    print(output)
if __name__=='__main__':audit()
