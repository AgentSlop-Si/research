# Newly authored modular probe; final checker independently reconstructs this.
from math import gcd

def prime(n):return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def divisors(n):return [d for d in range(2,n+1) if n%d==0 and prime(d)]
def primitive(n,p):
 for a in range(2,p):
  w=pow(a,(p-1)//n,p)
  if pow(w,n,p)==1 and all(pow(w,n//d,p)!=1 for d in divisors(n)):return w

def coeff(r,z,p):
 a=(1+r*pow(z,2,p))%p;b=(1+r*pow(z,3,p))%p;c=(pow(z,2,p)+r*pow(z,3,p))%p;e=(pow(z,3,p)+r*pow(z,2,p))%p;f=(pow(z,4,p)+r)%p;h=(z+r)%p
 A=c*a*b%p;B=e*a*b%p;C=f*b*b%p;E=h*a*a%p;S=(A+B)%p;U=(2*C-S)%p;L=(B*B-C*E)%p;M=(-2*A*B+A*C+A*E+B*C+B*E-2*C*E)%p;J=(B-C)**2%p
 R=(L*U*U-M*U*C+J*C*C)%p
 guard=a*b*C*(A-B)*(B-C)*(C-S)*L*R%p
 if not guard:return None
 num=(-2*S*J*U*L-M*(-S*J*C+(C*L-S*M)*U)+2*J*(C*L-S*M)*C)%p;den=L*R%p
 return num*pow(den,-1,p)%p
for N in [15,35,45,65,245]:
 for p in range(N+1,50000,N):
  if not prime(p):continue
  w=primitive(N,p);h=(N+1)//2;G=sum(pow(w,h*j*j,p) for j in range(N))%p
  if (1+N*G)%p==0:continue
  m=N//5;e5=m*pow(m,-1,5);em=5*pow(5,-1,m);z=pow(w,e5,p);theta=pow(w,em,p);hm=(m+1)//2
  rows=[]
  for b in range(m):
   for d in range(m):
    rho=-G*pow(theta,(-hm*(b+d)**2-b*d)%m,p)%p;t=coeff(rho,z,p)
    if t is not None:rows.append((b,d,rho,t))
  ts=sorted(set(t for b,d,r,t in rows));rs=sorted(set(r for b,d,r,t in rows))
  if len(ts)>1:
   print(N,p,w,G,'ratios',len(rs),'traces',len(ts),'controls',rows[:5]);break
