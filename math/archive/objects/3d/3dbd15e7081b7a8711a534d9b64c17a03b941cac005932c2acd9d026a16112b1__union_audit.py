"""Independent exact full-basis audit for the known two-filter graph union."""
import json, time
from annihilator_engine import RecurrenceGreen,decode_factor_union,far_coprime_shift

CASES=[(2013265921,31,[15,30,60,128,256,384]),
       (998244353,3,[7,17,119,128,256])]

def main():
    records=[];total=0
    start=time.perf_counter()
    for p,g,ns in CASES:
        for n in ns:
            engine=RecurrenceGreen(n,p,g)
            factors=[(far_coprime_shift(n),2),(n-1,3)]
            checks=0
            for j in range(n):
                impulse=[0]*n;impulse[j]=1
                got,meta=decode_factor_union(impulse,factors,engine)
                expected=[pow(engine.omega,j*k,p) for k in range(n)]
                if got!=expected:raise AssertionError(('graph union matrix basis failed',n,p,j))
                checks+=n
            total+=checks
            records.append({'p':p,'N':n,'factors':factors,'matrix_entries_checked':checks})
            print('UNION BASIS PASS',p,n,checks,flush=True)
    output={'exact_union_matrix_entries':total,'cases':records,
            'seconds':round(time.perf_counter()-start,3)}
    with open('UNION_BASIS.json','w') as f:json.dump(output,f,indent=2)
    print('TOTAL',total)
if __name__=='__main__':main()
