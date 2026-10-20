"""Independent direct path-matchings reconstruction of the fixed P19 certificate.
Usage: python check_independent_certificate.py /path/to/author/THREE_CERTIFICATE.json
No author recurrence or control implementation is imported.
"""
from pathlib import Path
from math import comb
from fractions import Fraction as Q
import json, sys

def add(a,b,shift=0,scale=1):
 while len(a)<len(b)+shift:a.append(0)
 for i,c in enumerate(b):a[i+shift]+=scale*c

def mul(a,b):
 out=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:out[i+j]+=x*y
 return out

def matchings():
 # Edge i is the original recurrence edge 1-q^i.
 # Each matching contributes (-1)^k product(1-q^i)=product(q^i-1).
 B=[[0] for _ in range(10)];count=0
 def rec(next_edge,size,prod):
  nonlocal count
  add(B[9-size],prod);count+=1
  for i in range(next_edge,19):
   rec(i+2,size+1,mul(prod,[0]+[comb(i,j) for j in range(1,i+1)]))
 rec(1,0,[1])
 C=[[0] for _ in range(10)]
 for l,poly in enumerate(B):
  for j in range(l+1):add(C[j],poly,3*l,comb(l,j)*(-1)**(l-j))
 return count,[{i:c for i,c in enumerate(poly) if c} for poly in C]

def vp(c,p):
 n=0
 while c%p==0:n+=1;c//=p
 return n

if __name__=='__main__':
 source=Path(sys.argv[1]);count,C=matchings();author=json.loads(source.read_text())['coefficients'];rows=[]
 for j,c in enumerate(C):
  assert c=={int(k):v for k,v in author[j]['integer_coefficients'].items()}
  L=9+2*j;assert min(c)>=L
  units=[k for k,v in c.items() if v%3]
  m=min(units);u=c[m]%3
  vals={k:k+18*vp(v,3) for k,v in c.items()}
  low=min(vals.values());at=[k for k,v in vals.items() if v==low]
  row=dict(j=j,t_divisibility=L,first_mod3_degree=m,first_mod3_unit=u,e18_lowest_weight=low,e18_minimizers=at)
  if j<4:
   assert (m,u)==[(25,1),(28,2),(24,2),(21,1)][j]
   assert 18+L>m and at==[m]
   row['all_e_ge18_unique_dominance']=True
  rows.append(row)
 assert count==6765
 delta=Q(4,3);av=[4,7,3,0,1,0,0,0,0,0]
 dterms=[av[j]+18*vp(j,3)+(j-1)*delta for j in range(1,10)]
 assert min(dterms)==Q(13,3) and dterms.index(min(dterms))+1==2
 wrong_terms=[av[j]+(j-1)*delta for j in range(1,10)]
 assert min(wrong_terms)==Q(8,3) and min(wrong_terms)!=min(dterms)
 out={'method':'Direct sum over all path matchings, then exact binomial X^2=t^3(V-1) substitution','matchings':count,'all_ten_integer_polynomials_byte_data_equal':True,'certificate':rows,'ordinary_derivative_lower_bounds':[str(x) for x in dterms],'drop_integer_derivative_factors_mutant':{'minimum':str(min(wrong_terms)),'rejected':True}}
 Path(__file__).with_name('INDEPENDENT_FIXED_POLYNOMIAL_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
