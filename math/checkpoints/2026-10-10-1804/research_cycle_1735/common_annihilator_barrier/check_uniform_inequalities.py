"""Fresh finite sanity checks; the Markdown files carry the all-N proof."""
from math import isqrt

def check(N,d,variant):
 m=N-d;r=2*(d-1)
 E=d-3+(d-1)//2;O=d-3+(d-2)//2
 assert d>=4
 if variant==13:assert (13*d-17)**2<N
 else:assert N>=64*d*d
 assert N>=7*d
 assert m+1>=3*(d-1)
 assert m>=4*(d-1)
 assert N-5*d+12>=(N+1)//2
 assert m>=(N-1)//2
 assert E+r<(N+1)//2
 assert (N+1)//2+O+r<N
 assert E+O+2+2*r==7*d-10
 assert d+2*r-1==5*d-5
 assert (7*d-10)+(d-1)+(5*d-5)==13*d-16

for N in range(1025,100000,2):
 check(N,isqrt(N)//8,8)
 if N>=1297:check(N,(isqrt(N)+16)//13,13)
for N in [100001,1000001,10000001,100000001]:
 check(N,isqrt(N)//8,8)
 check(N,(isqrt(N)+16)//13,13)
print('PASS: both uniform inequality ranges and exact atom counts')
