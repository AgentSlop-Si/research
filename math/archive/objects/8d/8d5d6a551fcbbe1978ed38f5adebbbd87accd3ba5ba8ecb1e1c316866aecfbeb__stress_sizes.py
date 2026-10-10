"""Deterministic power-of-two gauge-pencil stress tests over GF(65537)."""
import json,random
from pathlib import Path
import verify as V

def run():
    V.rng=random.Random(2026101002)
    output=[]
    for n in (4,8,16,32):
        root=V.omega_root(n); assert V.is_primitive(root,n)
        success=0;zero=0;bad=[]
        for t in range(10):
            A=V.two_green_stage(n)
            B=V.two_green_stage(n)
            K=[[A[k][i]*(B[i][1]-pow(root,k,V.P)*B[i][0])%V.P for i in range(n)] for k in range(n)]
            r=V.rank(K)
            if r==n:success+=1
            else:zero+=1;bad.append((t,r))
        output.append({'N':n,'field':V.P,'trials':10,'full_rank_two_column_pencil':success,'rank_deficient':zero,'details':bad})
    Path(__file__).with_name('STRESS_RESULTS.json').write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2))
if __name__=='__main__':run()
