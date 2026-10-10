"""Galois-projected Fourier ranks for finite abelian groups.

A=C_{n1}x...xC_{nr} has exponent m=lcm(n_i). Identify each character
with an index tuple j and each input with tuple k. Fourier entry is
zeta_m^(sum_i (m/n_i)*j_i*k_i).

All projected entries are exact integers. Nonzero modular minors prove the
corresponding characteristic-zero lower bounds. Full theorems in THEOREM.md.
"""
from __future__ import annotations
import json,math,itertools
import numpy as np
from cyclotomic_rank_certificate import P,residues,rank_minor_mod,det_mod,ramanujan

def lcm(ns):
 r=1
 for n in ns:r=math.lcm(r,n)
 return r

def cyclic_subgroups(ns):
 elements=list(itertools.product(*(range(n) for n in ns)))
 groups=set()
 for a in elements:
  order=lcm([n//math.gcd(n,k) for n,k in zip(ns,a)])
  group=frozenset(tuple((t*k)%n for k,n in zip(a,ns)) for t in range(order))
  groups.add(group)
 return len(groups)

def group_matrix_samples(ns,samples):
 m=lcm(ns)
 elements=list(itertools.product(*(range(n) for n in ns)))
 z=len(elements)
 M=np.empty((z,z),dtype=np.int64)
 for i,a in enumerate(elements):
  for j,b in enumerate(elements):
   exponent=sum((m//n)*ai*bi for n,ai,bi in zip(ns,a,b))%m
   M[i,j]=samples[exponent]
 return M

def run(ns):
 ns=tuple(ns);N=math.prod(ns);m=lcm(ns)
 rs=residues(m);dim=len(rs[0]);c=cyclic_subgroups(ns)
 ls={"trace":None,"traceless":[0]+list(range(1,dim)),"unrestricted":[1]+list(range(1,dim))}
 records={}
 for mode,coeffs in ls.items():
  if mode=='trace':vals=[ramanujan(m,k)%P for k in range(m)]
  else:vals=[sum(a*b for a,b in zip(coeffs,v))%P for v in rs]
  M=group_matrix_samples(ns,vals)
  rank,rows,cols=rank_minor_mod(M)
  determinant=det_mod(M[np.ix_(rows,cols)]) if rank else 1
  assert determinant%P !=0
  target={'trace':c,'traceless':N-c,'unrestricted':N}[mode]
  assert rank==target,(ns,mode,rank,target)
  records[mode]={'rank_mod_p':rank,'target_rank':target,'nonzero_minor_mod_p':determinant}
 return {'group_factors':list(ns),'order':N,'exponent':m,'cyclotomic_degree':dim,
         'cyclic_subgroup_count':c,'witnesses':records}

if __name__=='__main__':
 groups=[[2,2],[3,3],[4,2],[4,4],[3,9],[5,5],[8,4],[8,8],
         [3,3,3],[4,2,3],[4,3,5],[8,2,3],[7,7],[2,2,2,2],[5,5,3]]
 data={'theorem':'trace rank=# cyclic subgroups; generic traceless rank=|A|-# cyclic subgroups',
       'prime':P,'results':[]}
 for a in groups:
  r=run(a)
  data['results'].append(r)
  print(a,'|A|',r['order'],'c(A)',r['cyclic_subgroup_count'],
        'ranks',tuple(r['witnesses'][m]['rank_mod_p'] for m in ('trace','traceless','unrestricted')),flush=True)
 with open('ABELIAN_RANK_CERTIFICATES.json','w') as f:json.dump(data,f,indent=2)
