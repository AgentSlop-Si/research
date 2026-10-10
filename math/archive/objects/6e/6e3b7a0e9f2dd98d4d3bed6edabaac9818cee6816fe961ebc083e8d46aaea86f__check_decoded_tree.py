"""Exact recurrence-state subtree fusion checks; naive arithmetic, no speed claim."""
import random,json
from pathlib import Path
from check_cyclic_rational_fusion import P,root,mul

def denominator(zs):
    q=[1]
    for z in zs:q=mul(q,[1,-z%P])
    return q

def extend(v,q):
    L=len(v); prod=mul(q,v); R=(prod[L:]+[0]*L)[:L]
    h=[1]+[0]*(L-1)
    for j in range(1,L):h[j]=-sum(q[i]*h[j-i] for i in range(1,min(j,len(q)-1)+1))%P
    return [(-x)%P for x in mul(R,h)[:L]]

def main():
    rng=random.Random(9012026); cases=0;nodes=0;output_checks=0
    for period in [8,16,32]:
        zeta=root(period)
        for k in range(1,min(period,8)+1):
            L=1<<(k-1).bit_length()
            for depth in range(5):
                for _ in range(3):
                    zs=[pow(zeta,j,P) for j in rng.sample(range(period),k)]
                    a=[rng.randrange(1,P) for _ in zs]; N=L*(1<<depth)
                    direct=[sum(b*pow(z,m,P) for b,z in zip(a,zs))%P for m in range(N)]
                    states={0:direct[:L]}; ws=zs[:]
                    for d in range(depth):
                        q=denominator(ws); new={}
                        for r,v in states.items():
                            both=v+extend(v,q); nodes+=1
                            new[r]=both[::2];new[r+(1<<d)]=both[1::2]
                        states=new;ws=[w*w%P for w in ws]
                    out=[0]*N
                    for r,v in states.items():
                        for j,x in enumerate(v):out[r+(1<<depth)*j]=x
                    assert out==direct
                    cases+=1;output_checks+=N
    data=dict(status='passed',field_prime=P,cases=cases,branch_nodes=nodes,output_coefficients_checked=output_checks,
              limitation='Naive exact test of fused-state identity including root collisions; no fast-FFT benchmark.')
    Path(__file__).with_name('decoded_tree_checks.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
