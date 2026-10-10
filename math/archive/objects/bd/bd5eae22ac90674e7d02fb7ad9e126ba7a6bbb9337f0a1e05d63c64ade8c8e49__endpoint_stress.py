"""Reproducible stress test of the exact cut-rank lower bound after endpoint shuffles.
The test does NOT decide existence of low-channel factorizations.
"""
import json
from pathlib import Path
from cut_budget import endpoint_certificate,endpoint_patterns,fourier,permute

def run():
    results=[]
    for n in (16,32,64):
        f=fourier(n);orders=endpoint_patterns(n)
        for left,right in [('natural','natural'),('natural','bit_reversal'),
                           ('bit_reversal','natural'),('parity','parity'),
                           ('bit_reversal','bit_reversal')]:
            if n==64 and (left,right) != ('bit_reversal','bit_reversal'):
                continue
            c=endpoint_certificate(permute(f,orders[left],orders[right]),998244353)
            results.append({'n':n,'output_order':left,'input_order':right,**c})
            if left=='natural' or right=='natural':
                assert c['necessary_rank_sum']>=n//4
    Path(__file__).with_name('endpoint_stress_results.json').write_text(json.dumps(results,indent=2)+'\n')
    for x in results:
        print(x['n'], x['output_order'],x['input_order'],
              x['necessary_rank_sum'], x['surplus'])
    return results
if __name__=='__main__':run()
