"""Independent row-first retained-target check, not production traversal."""
from pathlib import Path
import json,time,resource
from fractions import Fraction as F
import retained_oracle as oracle
HERE=Path(__file__).resolve().parent

def scale(interval,v):
    pair=[x*v for x in interval];return min(pair),max(pair)
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a,b):return a[0]-b[1],a[1]-b[0]
def main():
    start=time.monotonic();data=json.loads((HERE/'OUTPUT.json').read_text());src=data['source'];out=data['output']
    N=src['N'];M=4*N;m=src['m'];P=data['estimates']['bits'];D=5;h=16*D*m+1
    op=oracle.Oracle(N,M,D);grid=oracle.BITS+P
    rows=[];count=0;largest=F(0)
    for ell,pair in enumerate(out['pairs']):
        real=(0,0);imag=(0,0);l1=0;terms=0
        for k,(a,b) in data['estimates']['pairs']:
            # Independent row-first geometric predicate, no outer iterator,
            # endpoint tables, coefficient engine or production source helpers.
            delta=(ell*M//N-k+M//2)%M-M//2
            if not -h-1<=delta<h+1:continue
            cr,ci=op.coefficient(ell,k)
            real=plus(real,minus(scale(cr,a),scale(ci,b)))
            imag=plus(imag,plus(scale(cr,b),scale(ci,a)))
            l1+=abs(a)+abs(b);terms+=1;count+=1
        normalized_bits=out['bits']+src['scale']
        lifted=[a << (grid-normalized_bits) for a in pair]
        radii=[max(abs(a-x[0]),abs(a-x[1])) for a,x in zip(lifted,(real,imag))]
        error_grid=(l1 << (oracle.BITS-8*m))+(1 << (grid-out['normalized_bits']))
        squared=radii[0]**2+radii[1]**2
        assert squared<=error_grid**2,(ell,'all-output retained-target bound failed')
        ratio=F(squared,error_grid**2);largest=max(largest,ratio)
        rows.append({'ell':ell,'terms':terms,'real_interval':real,'imag_interval':imag,
                     'squared_endpoint_error':squared,'squared_allowed_error':error_grid**2})
    assert count==op.calls==out['incidences']
    result={'all_rows_checked':len(rows),'independent_coefficient_calls':op.calls,
            'retained_count_matches_production':True,'target_grid':grid,
            'max_squared_error_to_squared_bound_ratio':{'numerator':largest.numerator,'denominator':largest.denominator},
            'oracle_sources':'Byte-identical accepted independent Horner oracle with different pi identity, root and traversal; source preserved.',
            'seconds':time.monotonic()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'rows':rows}
    (HERE/'RETAINED_TARGET_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('all_rows_checked','independent_coefficient_calls','retained_count_matches_production','seconds')}))
if __name__=='__main__':main()
