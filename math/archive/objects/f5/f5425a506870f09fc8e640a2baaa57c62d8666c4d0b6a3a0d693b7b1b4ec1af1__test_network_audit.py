"""Optional exact integer maxflow checks. Requires SciPy + NetworkX + NumPy.
The maxflow answers are only necessary rank capacities, never Fourier fits.
"""
import random
from fast_mincut import ScanFlowOracle
from moving_partition import *
from mixing_survivor import make

def run():
    total=0
    for k in (7,8):
        n=1<<k;tr=transformations(k)
        patterns={
            'rotations':[tr['rotl']]*3,
            'middle_xor':[tr['bitrev'],tr['bitrev_then_xor'],tr['bitrev']],
            'twisted':[tr['bitrev_then_rotl']]*3,
        }
        for name,ps in patterns.items():
            winners,num=search_parity(k,ps,[1]*4)
            assert winners
            C=parity_set(n,winners[0]['mask'])
            cap,path,costs=moving_partition_budget(n,C,ps,[1]*4)
            R=[j for j in range(n) if j not in set(path[-1])]
            oracle=ScanFlowOracle(n,[1]*4,ps)
            graph_capacity=oracle.bound(R,C)
            assert graph_capacity==cap<n//2,(k,name,graph_capacity,cap)
            total+=1
            print('MAXFLOW',n,name,graph_capacity,'<',n//2,flush=True)
    for k in (6,7,8):
        n=1<<k;ps,cols=make(k,20261016)
        rng=random.Random(k)
        oracle=ScanFlowOracle(n,[1]*4,ps)
        probes=[(list(range(n//2)),list(range(n//2,n))),
                (list(range(0,n,2)),list(range(1,n,2))),
                (parity_set(n,1<<(k//2)),parity_set(n,1<<(k//2),1))]
        for _ in range(5):
            c=sorted(rng.sample(range(n),n//2))
            r=sorted(rng.sample(range(n),n//2))
            probes.append((c,r))
        vals=[oracle.bound(r,c) for c,r in probes]
        assert vals==[n//2]*8,(n,vals)
        print('SURVIVOR',n,'8 sampled full-rank network capacities',vals,flush=True)
    print('PASS: 6 tight moving cuts and 24 full-capacity controls')

if __name__=='__main__':run()
