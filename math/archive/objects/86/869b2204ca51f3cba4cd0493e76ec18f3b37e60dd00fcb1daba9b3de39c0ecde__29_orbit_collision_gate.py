"""Exact collision counting for the stationary Toeplitz chirp Green scans.

a_i = 1+iK, G=K M. For a fixed scan-clock j:
   idx_i(j) = a_i*j mod G = j + K*(i*j mod M).
The number of distinct destinations across all i=0..M-1 equals
   M/gcd(j,M).
For M=2^h the number of distinct (j mod M, destination-in-fiber) pairs
across all j-residues is exactly (2*M*M+1)/3. Repeating each residue K
times gives K*(2*M*M+1)/3 distinct (j,destination) pairs across G clocks.
The naive M*G per-channel output visits can therefore be compressed by
*destination collisions alone* by only a ~3/2 factor. This is NOT a lower
bound on general algebraic sharing or on FFT complexity.
"""
import json
import math
from pathlib import Path


def predicted_unique_pairs(G,M):
    if G%M or M<1 or (M&(M-1)):
        raise ValueError('M power of two dividing G required')
    return (G//M)*(2*M*M+1)//3


def exact_unique_pairs(G,M):
    K=G//M
    return sum(len({((1+i*K)*j)%G for i in range(M)}) for j in range(G))


def run():
    rows=[]
    for M in (1,2,4,8,16,32,64,128):
        for K in (max(1,M),max(1,2*M)):
            G=K*M
            if K==1 and M==1:continue
            predicted=predicted_unique_pairs(G,M)
            explicit=exact_unique_pairs(G,M)
            analytic=sum(M//math.gcd(j,M) for j in range(G))
            assert predicted==explicit==analytic,(G,M,predicted,explicit,analytic)
            rows.append({'G':G,'M':M,'K':K,'naive_channel_visits':M*G,
                         'unique_clock_destination_pairs':explicit,
                         'ratio_to_naive':explicit/(M*G)})
    obj={'scope':'Exact same-clock destination-collision counts only: NO general algebraic circuit lower bound',
         'formula':'K*(2*M*M+1)/3 for G=KM and M a power of two',
         'verified':rows}
    (Path(__file__).parent/'ORBIT_COLLISION_RESULTS.json').write_text(json.dumps(obj,indent=2)+'\n')
    print(f'{len(rows)} orbit-collision controls passed; last ratio {rows[-1]["ratio_to_naive"]:.6f}; limit 2/3')

if __name__=='__main__':run()
