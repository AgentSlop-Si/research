import json

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1;b>>=1
 return c

def divmodp(a,b):
 assert b
 q=0
 while a and a.bit_length()>=b.bit_length():
  s=a.bit_length()-b.bit_length();q^=1<<s;a^=b<<s
 return q,a

def quo(a,b):
 q,r=divmodp(a,b);assert not r;return q

def val(a,p=3):
 if not a:return None
 i=0
 while True:
  q,r=divmodp(a,p)
  if r:return i
  i+=1;a=q

def add(a,b):
 c=list(a)+[0]*max(0,len(b)-len(a))
 for i,v in enumerate(b):c[i]^=v
 while c and not c[-1]:c.pop()
 return c

def scale(a,b):return [mul(x,b) for x in a]

def trace(n):
 p0=[1];p1=[6,1]
 if n==0:return p0
 if n==1:return p1
 for j in range(2,n+1):
  aj=(1<<(2*j-1))^(1<<(2*j));cj=mul(1^(1<<(2*j-1)),1^(1<<(2*j-2)))
  p=add(add([0]+p1,scale(p1,aj)),scale(p0,cj));p0,p1=p1,p
 return p1

def det(A):
 n=len(A)
 if n==0:return 1
 if n==1:return A[0][0]
 old=1
 for k in range(n-1):
  if not A[k][k]:
   r=next((r for r in range(k+1,n) if A[r][k]),None)
   if r is None:return 0
   A[k],A[r]=A[r],A[k]
  p=A[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):A[i][j]=quo(mul(p,A[i][j])^mul(A[i][k],A[k][j]),old)
   A[i][k]=0
  old=p
 return A[-1][-1]

def resultant(a,b):
 while a and not a[-1]:a.pop()
 while b and not b[-1]:b.pop()
 if not a or not b:return 0
 r=len(a)-1;s=len(b)-1;n=r+s
 A=[]
 for i in range(s):A.append([0]*i+list(reversed(a))+[0]*(s-1-i))
 for i in range(r):A.append([0]*i+list(reversed(b))+[0]*(r-1-i))
 return det(A)

if __name__=='__main__':
 rows=[]
 for m in [1,2,3,4,5,6,7,8,12,16]:
  p=trace(m);r=resultant(p[::2],p[1::2]);row={'m':m,'E_val':val(p[0]),'R_val':val(r),'Q_val':val(p[0])+val(r),'R_degree':r.bit_length()-1};rows.append(row);print(row,flush=True)
 print(json.dumps(rows))
