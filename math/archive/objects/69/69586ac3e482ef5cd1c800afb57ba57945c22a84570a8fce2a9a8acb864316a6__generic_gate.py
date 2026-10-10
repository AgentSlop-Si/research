"""Exhaustive tiny-field exploratory check of short-annihilator noncoverage.

This finite-field enumeration is a diagnostic; the characteristic-zero
algebraic dimension theorem is proved separately in THEOREM.md.
"""
import itertools,json,time

def main():
    p=17;n=4;start=time.perf_counter()
    histogram=[0]*(n+1)
    examples={}
    for r in itertools.product(range(p), repeat=n):
        best=n
        for c in range(p):
            k=0
            for j in range(n):
                if (r[j]+c*r[(j-1)%n])%p:k+=1
                if k>=best:break
            if k<best:best=k
            if best==0:break
        histogram[best]+=1
        if str(best) not in examples:examples[str(best)]=list(r)
    count=sum(histogram)
    assert count==p**n
    # Every finite vector is covered at K=N with q(z)=1. But K=1,
    # d=1 is a tiny union of lower-dimensional algebraic families.
    assert sum(histogram[:2])<count
    result={'prime':p,'N':n,'degree_max':1,'polynomials_scanned':p,
            'vectors_checked':count,'minimal_defect_support_histogram':histogram,
            'fraction_with_K_le_1':sum(histogram[:2])/count,
            'fraction_with_K_le_2':sum(histogram[:3])/count,
            'witnesses':examples,'seconds':round(time.perf_counter()-start,3)}
    with open('GENERIC_GATE.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__':main()
