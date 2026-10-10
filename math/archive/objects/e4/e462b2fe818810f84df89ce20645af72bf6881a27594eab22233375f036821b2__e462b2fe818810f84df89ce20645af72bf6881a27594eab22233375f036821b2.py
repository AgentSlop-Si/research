"""Numerical warning gate: denominator coefficients can grow exponentially in K.
This is not a rigorous floating-point error upper bound; the exact limiting
argument and binomial coefficient formula are documented in THEOREM.md.
"""
import cmath,math,json,random
from pathlib import Path
from rational_forcing import AllLengthGreen,P0,G0


def dense_denominator(n,support):
    omega=cmath.exp(-2j*math.pi/n)
    den=[1+0j]
    for j in support:
        lam=omega**j
        new=[0j]*(len(den)+1)
        for i,v in enumerate(den):
            new[i]+=v
            new[i+1]-=lam*v
        den=new
    return den


def run():
    n=1<<17
    r=[]
    for k in (4,8,16,32):
        clustered=dense_denominator(n,range(k))
        dispersed=dense_denominator(n,[j*(n//k) for j in range(k)])
        item={'N':n,'K':k,'clustered_max_abs_coef':max(abs(z) for z in clustered),
              'dispersed_max_abs_coef':max(abs(z) for z in dispersed),
              'central_binomial_comparison':math.comb(k,k//2),
              'clustered_to_output_upper_amplification':max(abs(z) for z in clustered)/k}
        r.append(item)
    e=AllLengthGreen(512,P0,G0)
    random.seed(20261010)
    ks=[]
    for trial in range(16):
        x=[random.randrange(P0) for _ in range(e.n)]
        ks.append(sum(bool(z) for z in e.sparse_residual(x)))
    out={'denominator_coefficient_warnings':r,'uniform_random_input_residual_supports':ks,
         'generic_input_predicted_support':512*(1-1/P0),
         'interpretation':'Finite-field correctness does not imply bounded complex bit precision; dense generic inputs do not sparsify.'}
    Path(__file__).with_name('PRECISION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':run()
