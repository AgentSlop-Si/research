"""Fresh independent reduction of the forced-two-root N11 family."""
from pathlib import Path
import json
p=23
A=[[1,17,2,0],[17,2,0,5],[2,0,5,11],[9,11,11,20]]
s=[1,17,2,0,5,11,18,10,14]
u=[9,11,11,20,12,15,19]
def solve(A,b):
 M=[r[:]+[v%p] for r,v in zip(A,b)]
 for i in range(len(A)):
  j=next(j for j in range(i,len(A)) if M[j][i]);M[i],M[j]=M[j],M[i]
  v=pow(M[i][i],-1,p);M[i]=[x*v%p for x in M[i]]
  for j in range(len(A)):
   if j!=i:
    v=M[j][i];M[j]=[(a-v*b)%p for a,b in zip(M[j],M[i])]
 return [r[-1] for r in M]
cl=solve(A,[-s[4],-s[5],-s[6],-u[4]])+[1,0,0]
cm=solve(A,[-s[5],-s[6],-s[7],-u[5]])+[0,1,0]
c0=solve(A,[-s[6],-s[7],-s[8],-u[6]])+[0,0,1]
def ev(c,x):return sum(v*pow(x,j,p) for j,v in enumerate(c))%p
B=[[ev(cl,x),ev(cm,x)] for x in [7,8]]
det=(B[0][0]*B[1][1]-B[0][1]*B[1][0])%p
assert c0==[12,21,2,4,0,0,1]
assert cl==[11,22,12,16,1,0,0] and cm==[5,2,21,20,0,1,0]
assert B==[[17,13],[18,6]] and det==6
assert ev(c0,7)==ev(c0,8)==0
parameters=solve(B,[-ev(c0,7),-ev(c0,8)]);assert parameters==[0,0]
quartic=[15,20,8,15,1]
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c
assert mul(mul([16,1],[15,1]),quartic)==c0
assert all(ev(quartic,x) for x in range(p))
def mod(a,b):
 a=a[:]
 while len(a)>=len(b):
  v=a[-1]*pow(b[-1],-1,p)%p;offset=len(a)-len(b)
  for i,x in enumerate(b):a[i+offset]=(a[i+offset]-v*x)%p
  while a and not a[-1]:a.pop()
 return a
assert all(mod(quartic,[b,a,1]) for a in range(p) for b in range(p))
report={'status':'PASS','field':'F23','q':2,'base_sextic_ascending':c0,'lambda_derivative_ascending':cl,'mu_derivative_ascending':cm,'forced_K_roots':[7,8],'root_constraint_matrix':B,'root_constraint_determinant':det,'parameter_residues':parameters,'remaining_quartic_ascending':quartic,'quartic_irreducible':True,'original_exceptional_product':12*6*5*3*18*8%23,'interpretation':'Unique exact K solution to the two root constraints reduces to the accepted good family point. All guards/minors persist, and the remaining exact quartic is irreducible over K. Its splitting field degree is at least 4 and at most 24; no exact splitting-field degree is claimed.'}
assert report['original_exceptional_product']==17
Path(__file__).with_name('INDEPENDENT_MODULAR_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
