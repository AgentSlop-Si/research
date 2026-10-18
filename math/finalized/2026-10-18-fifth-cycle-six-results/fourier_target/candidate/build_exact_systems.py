"""Fresh, deterministic, exact target systems. Standard library only."""
from itertools import combinations, permutations
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
P=[7,0,6,3,4,1,2,5]; N=8
names=[f'{s}_{g}{i}' for s in 'AB' for g in ['d','l','m','u','v'] for i in range(N)]
unused=[f'{s}_{g}{i}' for s in 'AB' for g,i in [('l',0),('m',7),('u',7),('v',0)]]
def factor(s,i,j):
 return [f'{s}_d{i}'] if i==j else ([f'{s}_l{i}',f'{s}_m{j}'] if i>j else [f'{s}_u{i}',f'{s}_v{j}'])
def zpower(k):
 k%=8;return [(-1 if k>=4 else 1) if r==k%4 else 0 for r in range(4)]
def neg(a):return [-v for v in a]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def scalar(c):return [c,0,0,0]
original=[]
for i in range(N):
 for j in range(N):
  terms=[dict(coefficient=scalar(1),monomial=sorted(factor('B',i,P[k])+factor('A',k,j))) for k in range(N)]
  terms.append(dict(coefficient=neg(zpower(i*j)),monomial=[]))
  original.append(dict(row=i,column=j,terms=terms))
obj=dict(field='Q[z]/(z^4+1)',variables=names,unobservable_variables=unused,permutation=P,convention='P e_j=e_{p[j]}; (B P A)[i,j]=sum_k B[i,p[k]] A[k,j]',equations=original)
(ROOT/'ORIGINAL_IDEAL.json').write_text(json.dumps(obj,indent=2)+'\n')
# Minor equations for C and F*C*P^-1; C column indices stay fixed.
quad=[]
for a,b in combinations(range(N),2):
 for r,s in combinations(range(N),2):
  if (s<a or r>b):
   quad.append(dict(stage='C',columns=[a,b],rows=[r,s],terms=[dict(coefficient=scalar(1),monomial=[f'c{r}_{a}',f'c{s}_{b}']),dict(coefficient=scalar(-1),monomial=[f'c{s}_{a}',f'c{r}_{b}'])]))
  lo,hi=sorted([P[a],P[b]])
  if s<lo or r>hi:
   terms=[]
   for u,v in combinations(range(N),2):
    coeff=sub(zpower(r*u+s*v),zpower(r*v+s*u))
    if any(coeff):
     terms.append(dict(coefficient=coeff,monomial=[f'c{u}_{a}',f'c{v}_{b}']))
     terms.append(dict(coefficient=neg(coeff),monomial=[f'c{v}_{a}',f'c{u}_{b}']))
   # Choosing columns [a,b] rather than sorted P-order changes a minor sign only.
   quad.append(dict(stage='F*C*P^-1',columns_in_C=[a,b],columns_in_B=[P[a],P[b]],rows=[r,s],terms=terms))
assert len(quad)==280
relaxed=dict(field=obj['field'],variables=[f'c{i}_{j}' for i in range(N) for j in range(N)]+['t'],equations=quad,invertibility_equation='t*det(C)-1',status='necessary relaxation; membership still requires exact original-chart lifting of C^-1 and F*C*P^-1')
(ROOT/'RELAXED_QUADRICS.json').write_text(json.dumps(relaxed,indent=2)+'\n')
def coeffstr(v):
 return '('+'+'.join(f'({c})'+('' if k==0 else f'*z^{k}') for k,c in enumerate(v) if c)+')'
def polystr(eq):
 return '+'.join(coeffstr(t['coefficient'])+(' * '+'*'.join(t['monomial']) if t['monomial'] else '') for t in eq['terms'])
active=[x for x in names if x not in unused]
s=['// Fresh exact original ideal; no saturation or nonzero chart assumptions.','ring R = (0,z),('+','.join(active)+'),dp;','minpoly = z^4+1;','ideal I =\n'+',\n'.join(polystr(e) for e in original)+';','// Run std(I) with a characteristic-zero engine and preserve its proof/certificate.','// A reported basis [1] alone must be independently verified through a lifted identity.']
(ROOT/'ORIGINAL_IDEAL.sing').write_text('\n'.join(s)+'\n')
s=['// Necessary inverse relaxation. Infeasibility implies original infeasibility.','ring R = (0,z),('+','.join(relaxed['variables'])+'),dp;','minpoly = z^4+1;','matrix C[8][8] = '+','.join(f'c{i}_{j}' for i in range(N) for j in range(N))+';','ideal J =\n'+',\n'.join(polystr(e) for e in quad)+',\nt*det(C)-1;','// Run std(J) and lift(ideal(J),ideal(1)) only with retained exact output.']
(ROOT/'RELAXED_IDEAL.sing').write_text('\n'.join(s)+'\n')
print(json.dumps(dict(original_variables=80,observable_variables=72,original_equations=64,relaxed_variables=65,quadrics=280,relaxed_quadratic_terms=sum(len(e['terms']) for e in quad),max_original_degree=max(len(t['monomial']) for e in original for t in e['terms']))))
