import math
from functools import lru_cache
import numpy as np

@lru_cache(None)
def totient(n):
    return sum(math.gcd(i,n)==1 for i in range(n))
@lru_cache(None)
def mu(n):
    count=0
    p=2
    z=n
    while p*p<=z:
        if z%p==0:
            count+=1;z//=p
            if z%p==0:return 0
            while z%p==0:z//=p
        p+=1
    if z>1:count+=1
    return (-1)**count

def profile(n,m):
    dsets=[set(range(-t,m-t))-{0} for t in range(m)]
    cov=np.zeros((n,n),float)
    for i in range(n):
        for j in range(n):
            g=math.gcd(n,i-j)
            val=0.
            for d in dsets[i%m]&dsets[j%m]:
                h=math.gcd(n,d*(i-j))
                nf=n//h
                val+=mu(nf)/totient(nf)
            cov[i,j]=val/n
    evals=np.linalg.eigvalsh(cov)
    return {'n':n,'m':m,'max_eig':float(evals[-1]),'baseline':m/n,'ratio':float(evals[-1]/(m/n)),'trace':float(np.trace(cov))}

if __name__=='__main__':
    for n in [12,18,20,24,30,36,40,42,48,54,60,64,72,80,84,90,96,100,108,120,126,144,150,168,180,192,210,240]:
        for m in range(2,math.isqrt(n)+1):
            if n%m:continue
            if n>=60 and m<3: continue
            r=profile(n,m)
            print(n,m,f"{r['ratio']:.4f}")
