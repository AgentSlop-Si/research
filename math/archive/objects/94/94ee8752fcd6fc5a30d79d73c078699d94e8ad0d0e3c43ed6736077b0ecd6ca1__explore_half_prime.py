import sympy as s

def add(a,b,p):return ((a[0]+b[0])%p,(a[1]+b[1])%p)
def mul(a,b,p):return ((a[0]*b[0]-a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0]-a[1]*b[1])%p)
def sc(c,a,p):return (c*a[0]%p,c*a[1]%p)
for p in list(s.primerange(7,10000)):
 if p%4!=3:continue
 A=(p-1)//2; lam=(pow(2,-1,p),1); tau=(1,p-1)
 h0=(1,0);h1=(1,0)
 for k in range(2,A+1):
  h=add(mul(lam,h1,p) if k%2==0 else h1,sc(-(k-1),h0,p),p)
  h0,h1=h1,h
 val=add(mul(lam,h1,p),sc(-A,mul(tau,h0,p),p),p)
 if val==(0,0):print('BOTH BAD',p,flush=True)
 # norm zero means some component bad
 norm=(val[0]*val[0]-val[0]*val[1]+val[1]*val[1])%p
 if norm==0:print('SOME BAD',p,val,flush=True)
print('done')
