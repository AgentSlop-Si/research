"""Exploratory necessary rank-cut checks, NOT an FFT complexity theorem.
Requires scipy and networkx, plus packaged prior checkpoint source.
"""
import json,random,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'fft_scan_network_gate_2026-10-09'))
from fast_mincut import ScanFlowOracle
from scan_flow import make_graph,mincut_bound
from research_gate import bitrev

def main():
    samples={8:2000,16:2000,32:2000,64:2000,128:1000}
    rng=random.Random(20261010)
    results={}
    for n,limit in samples.items():
        P=bitrev(n)
        oracle=ScanFlowOracle(n,[1,1,1],[P,P])
        small=0;vals=[]
        for i in range(limit):
            mode=i%5
            if mode==0:
                width=rng.randint(1,n)
                start=rng.randint(0,n-width)
                R=list(range(start,start+width))
                width=rng.randint(1,n)
                start=rng.randint(0,n-width)
                C=list(range(start,start+width))
            elif mode==1:
                k=rng.randint(1,n)
                R=rng.sample(range(n),k);C=rng.sample(range(n),k)
            elif mode==2:
                k=rng.randint(1,n)
                R=list(range(k));C=list(range(n-k,n))
            elif mode==3:
                k=rng.randint(1,n)
                R=list(range(n-k,n));C=list(range(k))
            else:
                k=rng.randint(1,n)
                R=rng.sample(range(n),k);C=rng.sample(range(n),rng.randint(1,n))
            bound=oracle.bound(R,C)
            if bound<min(len(R),len(C)):
                small+=1;vals.append([i,R,C,bound])
            if i<4 and n<=32:
                G,big=make_graph(n,[1,1,1],[P,P])
                other,_=mincut_bound(G,big,n,3,R,C)
                assert bound==other
        results[str(n)]={'queries':limit,'cut_below_full_rank_count':small,
                         'first_nonfull_queries':vals[:2]}
        print(n,limit,small,flush=True)
    out=root/'NETWORK_RESULTS.json'
    out.write_text(json.dumps(results,indent=2)+'\n')
    return results

if __name__=='__main__':main()
