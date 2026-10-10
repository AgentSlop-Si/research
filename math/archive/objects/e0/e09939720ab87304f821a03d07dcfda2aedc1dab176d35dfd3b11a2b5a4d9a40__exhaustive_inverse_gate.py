"""Exhaustive GF(17)^4 sparse-circular-inverse classification by independent DFT."""
import itertools,json
from types import SimpleNamespace
from blind_inverse import discover_sparse_circular_inverse

p,n=17,4
omega=pow(3,4,p)
assert pow(omega,n,p)==1 and pow(omega,2,p)!=1
engine=SimpleNamespace(n=n,p=p,omega=omega,powers=[pow(omega,k,p) for k in range(n)],primitive_gen=3)
forward=[[pow(omega,(j*k)%n,p) for j in range(n)] for k in range(n)]
inverse=[[pow(omega,(-j*k)%n,p) for k in range(n)] for j in range(n)]
invn=pow(n,-1,p)
inv=[0]+[pow(a,-1,p) for a in range(1,p)]
all_vectors=invertible=eligible=accepted=misses=false=0
counts={}
for r in itertools.product(range(p),repeat=n):
    all_vectors+=1
    R=[sum(r[j]*forward[k][j] for j in range(n))%p for k in range(n)]
    if all(R):
        invertible+=1
        I=[inv[v] for v in R]
        C=[sum(I[k]*inverse[j][k] for k in range(n))*invn%p for j in range(n)]
        support={j:a for j,a in enumerate(C) if a}
        success=len(support)<=2
    else:
        success=False;support={}
    found,meta=discover_sparse_circular_inverse(r,engine,2)
    got=found is not None
    if success:eligible+=1
    if got:accepted+=1
    if success and not got:misses+=1
    if got and not success:false+=1
    if got and found !=support:
        raise AssertionError(('wrong inverse recovered',r,support,found))
    if misses or false:
        raise AssertionError(('oracle disagrees',r,success,found))
result={'field':'GF(17)','N':4,'all_vectors':all_vectors,
        'invertible_circular_convolution_vectors':invertible,
        'inverse_support_le2':eligible,'detector_accepted':accepted,
        'missed_structured_vectors':misses,'false_acceptances':false,
        'oracle':'Compute all 4 direct Fourier bins, invert nonzero bins independently, inverse DFT, count actual inverse support.'}
with open('EXHAUSTIVE_INVERSE_GATE.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
