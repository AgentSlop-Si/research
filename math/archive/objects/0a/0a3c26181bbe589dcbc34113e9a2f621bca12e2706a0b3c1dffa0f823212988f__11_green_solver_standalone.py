"""Independent O(N) tridiagonal solve in a prime field for T=tridiag(-1,3,-1)."""
MOD=998244353

def tri_solve(b,p=MOD):
    n=len(b)
    c=[0]*n
    d=[0]*n
    if not n: return []
    inv=pow(3,-1,p)
    if n>1: c[0]=-inv %p
    d[0]=b[0]*inv%p
    for i in range(1,n):
        denominator=(3+c[i-1])%p
        z=pow(denominator,-1,p)
        if i+1<n: c[i]=-z%p
        d[i]=(b[i]+d[i-1])*z%p
    x=[0]*n
    x[-1]=d[-1]
    for i in range(n-2,-1,-1): x[i]=(d[i]-c[i]*x[i+1])%p
    return x
