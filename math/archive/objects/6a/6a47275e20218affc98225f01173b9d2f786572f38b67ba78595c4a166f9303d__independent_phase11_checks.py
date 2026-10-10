import sys, random, json
sys.path.insert(0, 'two_research_updates_2247/unpacked/fft_phase11_fresh_factor')
from fresh_factor import convolve,sparse_product_and_recover,find_recurrence,PRIMES,multiply_near_power,multiply_int

def reference(a,b,p=None):
    ans=[sum(a[j]*b[k-j] for j in range(max(0,k-len(b)+1),min(len(a)-1,k)+1)) for k in range(len(a)+len(b)-1)]
    return ans if p is None else [x%p for x in ans]

rng=random.Random(202610082249)
cases=0
for p in [None]+[q[0] for q in PRIMES]:
    for trial in range(90):
        n=rng.randrange(1,42);m=rng.randrange(1,42)
        bits=rng.choice([0,1,4,30,100,600]) if p is None else 35
        a=[rng.randrange(-(1<<bits),1+(1<<bits)) for _ in range(n)]
        b=[rng.randrange(-(1<<bits),1+(1<<bits)) for _ in range(m)]
        truth=reference(a,b,p)
        for mode in ['auto','ntt','structured']:
            got,plan=convolve(a,b,mod=p,mode=mode)
            assert got==truth,(p,trial,mode)
            cases+=1
        qa=[1]+[rng.randrange(-4,5) for _ in range(rng.randrange(7))]
        qb=[1]+[rng.randrange(-4,5) for _ in range(rng.randrange(7))]
        assert sparse_product_and_recover(a,b,qa,qb,p)==truth,(p,trial,qa,qb)
        cases+=1

recurrence_cases=0
for p,_,_ in PRIMES:
    for d in range(1,8):
        for trial in range(10):
            q=[1]+[rng.randrange(p) for _ in range(d)]
            a=[rng.randrange(p) for _ in range(d)]
            for i in range(d,100):a.append((-sum(q[j]*a[i-j] for j in range(1,d+1)))%p)
            found=find_recurrence(a,max_degree=d,p=p)
            assert found is not None
            assert all(sum(found[j]*a[i-j] for j in range(len(found)))%p==0 for i in range(len(found)-1,len(a)))
            b=[rng.randrange(p) for _ in range(37)]
            assert convolve(a,b,mod=p,max_degree=d)[0]==reference(a,b,p)
            recurrence_cases+=1

integer_cases=0
for bits in [0,1,5,64,512,2048]:
    for _ in range(20):
        a=rng.getrandbits(bits);b=rng.getrandbits(bits+7)
        assert multiply_near_power(a,b)[0]==a*b
        if bits<=512:
            assert multiply_int(a,b)[0]==a*b
        integer_cases+=1

p=PRIMES[0][0]
constant=[7]*400;arbitrary=[rng.randrange(p) for _ in range(400)]
_,forced_ntt_plan=convolve(constant,arbitrary,mod=p,mode='ntt')
_,forced_structured_plan=convolve(arbitrary,arbitrary,mod=p,mode='structured')
res=dict(random_convolution_checks=cases,recurrence_cases=recurrence_cases,integer_cases=integer_cases,
         forced_ntt_returned_method=forced_ntt_plan.method,forced_structured_returned_method=forced_structured_plan.method)
print(json.dumps(res,indent=2))
