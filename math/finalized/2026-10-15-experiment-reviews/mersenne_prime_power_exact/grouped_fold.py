from math import comb

def div_group(x,m,d,ledger=None):
 p=(1<<m)-1;Q=p**d;shift=m*d;mask=(1<<shift)-1;q=0
 while x>>shift:
  A=x>>shift;B=x&mask
  if d==1:correction=A
  elif d==2:correction=(A<<(m+1))-A
  else:correction=sum((1 if j%2 else -1)*(A*comb(d,j)<<(m*(d-j))) for j in range(1,d+1))
  q+=A;x=B+correction
  if ledger is not None:ledger['folds']+=1
 while x>=Q:q+=1;x-=Q
 return q,x

def encode_group(x,m,d):
 out=[];ledger={'folds':0}
 while x:x,a=div_group(x,m,d,ledger);out.append(a)
 return out or [0],ledger
