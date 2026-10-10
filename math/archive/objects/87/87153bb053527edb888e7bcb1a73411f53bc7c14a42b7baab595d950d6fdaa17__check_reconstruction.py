import own_base_check as k
import json
from pathlib import Path
E=k.E;n=5;z=k.Z;c=E(5*k.G)
F=[[E(z**(i*j)) for j in range(n)] for i in range(n)]
B=[[E(x) for x in r] for r in k.B]
A=[E(z**(3*j*j)) for j in range(n)]
M=[[A[i]*F[i][j] for j in range(n)] for i in range(n)]
K=[[A[i]*B[i][j] for j in range(n)] for i in range(n)]
K2=k.mm(K,K);K3=k.mm(K2,K);M3=k.mm(k.mm(M,M),M)
Q=[[(1+c)*K2[i][j]+(1-2*c)*K[i][j]+E((1+c) if i==j else 0) for j in range(n)] for i in range(n)]
assert all(M3[i][j]==(c if i==j else 0) for i in range(n) for j in range(n))
assert all((1+c)*K3[i][j]-3*c*K2[i][j]+3*c*K[i][j]-E(c if i==j else 0)==0 for i in range(n) for j in range(n))
IK=[[E(i==j)-K[i][j] for j in range(n)] for i in range(n)]
assert k.isid(k.mm(IK,Q)) and k.isid(k.mm(Q,IK))
assert k.mm(B,Q)==F
counts={'B_calls':0,'green_solves':0,'diagonal_corrections':0,'A_calls':0,'scan_equations':0,'outputs':0}
def scan(x,pole):
 w=[E(1)]*4+[pole];aa=E(1);bb=E(0)
 for i in range(4,0,-1):aa=w[i]*aa;bb=x[i]+w[i]*bb
 y0=(x[0]+w[0]*bb)/(1-w[0]*aa)
 y=[y0]+[E(0)]*4
 for i in range(4,0,-1):y[i]=x[i]+w[i]*y[(i+1)%5]
 assert all(y[i]-w[i]*y[(i+1)%5]==x[i] for i in range(5))
 counts['green_solves']+=1;counts['scan_equations']+=5
 return y
def bapply(x):
 one=scan([k.v[i]*x[i] for i in range(5)],k.t)
 two=scan([k.u[i]*x[i] for i in range(5)],1/k.t)
 counts['B_calls']+=1;counts['diagonal_corrections']+=1
 return [(1-k.t)*k.u[i]*one[i]+(k.t-1)*k.v[i]*two[i]+k.di[i]*x[i] for i in range(5)]
inputs=[[E(i==j) for i in range(5)] for j in range(5)]+[[E(i+1) for i in range(5)],[E(z**i)+k.d for i in range(5)]]
for x in inputs:
 y0=bapply(x);y1=bapply([A[i]*y0[i] for i in range(5)]);y2=bapply([A[i]*y1[i] for i in range(5)]);counts['A_calls']+=2
 y=[(1+c)*y0[i]+(1-2*c)*y1[i]+(1+c)*y2[i] for i in range(5)]
 assert y==[sum(F[i][j]*x[j] for j in range(5)) for i in range(5)]
 counts['outputs']+=5
assert counts['green_solves']==42 and counts['B_calls']==21
Path('RECONSTRUCTION_RESULTS.json').write_text(json.dumps({'status':'PASS','matrix_identity_entries':125,'counts':counts,'per_transform':{'nontrivial_Green_solves':6,'B_calls':3,'A_calls':2,'diagonal_corrections':3},'setup':'Root, quadratic extension, endpoints and all inverse constants charged separately; fixed-size only.'},sort_keys=True,indent=2)+'\n')
print(counts)
