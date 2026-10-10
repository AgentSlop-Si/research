"""Check archived rank certificates without trusting their recorded masks or cuts.
Rebuilds each permutation from its name and validates two exact field ranks.
"""
from pathlib import Path
import json
from moving_partition import *

HERE=Path(__file__).resolve().parent

def shuffles(k,name):
    t=transformations(k)
    if name=='rotations':return [t['rotl']]*3
    if name=='twisted_bitrev':return [t['bitrev_then_rotl']]*3
    if name=='middle_xor':return [t['bitrev'],t['bitrev_then_xor'],t['bitrev']]
    if name=='middle_rotate':return [t['bitrev'],t['bitrev_then_rotl'],t['bitrev']]
    if name=='mixed_twists':return [t['bitrev_then_rotl'],t['bitrev_then_xor'],t['bitrev_then_rotl']]
    raise ValueError(name)

def check():
    certs=json.loads((HERE/'EXACT_CERTIFICATES.json').read_text())['cases']
    assert len(certs)==13
    for item in certs:
        n=item['n'];k=n.bit_length()-1
        ps=shuffles(k,item['name'])
        assert item['permutations']==ps
        A=parity_set(n,item['initial_parity_mask'])
        budget,path,costs=moving_partition_budget(n,A,ps,item['orders'])
        assert costs==item['boundary_costs'] and budget==item['bound']
        assert budget<item['fourier_rank']==n//2
        assert [len(s) for s in path]==[n//2]*len(path)
        # independent propagation of the stated parity masks
        for j,group in enumerate(path):
            assert set(group)==set(parity_set(n,item['mask_path'][j]))
            brute=sum((i in set(group))!=((i+1) in set(group)) for i in range(n-1))
            assert brute==costs[j]
        R=[i for i in range(n) if i not in set(path[-1])]
        for field in item['modular']:
            p=field['prime']
            assert p in (12289,65537)
            assert field['primitive_root']==primitive_root_of_unity(n,p)
            assert fourier_block_rank(n,R,A,p)==n//2
        print('CERT PASS N',n,item['name'],'Fourier rank',n//2,'capacity',budget,flush=True)
    print('ALL 13 EXACT CERTIFICATES VERIFIED')

if __name__=='__main__':check()
