import hashlib,json,math,sys
from pathlib import Path
from probe_constraints import rref,data
from probe_full_left import setup,probe,rempow
ROOT=Path(__file__).parent

def det(A,p):
 a=[r[:] for r in A];v=1;n=len(a)
 for j in range(n):
  k=next((k for k in range(j,n) if a[k][j]%p),None)
  if k is None:return 0
  if k!=j:a[j],a[k]=a[k],a[j];v=-v
  u=a[j][j]%p;v=v*u%p
  for k in range(j+1,n):
   t=a[k][j]*pow(u,-1,p)%p
   for l in range(j,n):a[k][l]=(a[k][l]-t*a[j][l])%p
 return v%p

def resultant(f,p):
 df=[j*f[j]%p for j in range(1,len(f))]
 n=len(f)-1;m=len(df)-1
 while m>=0 and not df[m]:m-=1
 df=df[:m+1]
 M=[]
 for s in range(m):M.append([0]*s+f[::-1]+[0]*(m-1-s))
 for s in range(n):M.append([0]*s+df[::-1]+[0]*(n-1-s))
 return det(M,p)

def solve(A,b,p):
 R,cols=rref([a+[v] for a,v in zip(A,b)],p)
 if len(A[0]) in cols:raise ValueError('inconsistent')
 x=[0]*len(A[0])
 for i,j in enumerate(cols):x[j]=R[i][-1]
 return x

def certify(n):
 d=probe(n);p=d['p'];q=d['q'];m=d['m'];gap=n-m
 seq,G,f=setup(n,p,q)
 rows=[];labels=[]
 for b,s in enumerate(seq,1):
  for r in range(len(s)-m):rows.append(s[r:r+m+1]);labels.append([b,r])
 rank=len(rref(rows,p)[1]);bound=min((gap-1)*(gap-2)//2,4*gap-11) if gap>=4 else len(rows)
 assert rank==bound,(n,rank,bound)
 eq_rows=rref([list(z) for z in zip(*rows)],p)[1]
 selected=[rows[i] for i in eq_rows];cols=rref(selected,p)[1]
 assert m not in cols
 J=cols;A=[[rows[i][j] for j in J] for i in eq_rows]
 c=d['witness']['coefficients'];free=[j for j in range(m) if j not in J]
 assert all(sum(a*b for a,b in zip(row,c))%p==0 for row in rows)
 P=rempow(n,c,p)
 row_cert=[]
 for b in range(n):
  M=[];t=[]
  for a in range(n):
   M.append([G(a,b,1,1)*v%p for v in P[a]]+[G(a,b,-1,1),G(a,b,1,-1)]+[G(a,b,-1,-1)*v%p for v in P[-a%n]])
   t.append(f(a,b))
  x=solve(M,t,p)
  assert all(sum(u*v for u,v in zip(row,x))%p==v for row,v in zip(M,t))
  row_cert.append({'b':b,'rank':len(rref(M,p)[1]),'solution':x})
 axis=[P[a]+[1]+P[-a%n] for a in range(n)]
 axiscols=rref(axis,p)[1]
 axisdet=det([[row[j] for j in axiscols] for row in axis],p)
 assert len(axiscols)==n and axisdet
 res=resultant(c,p);assert res and c[0]
 out={'N':n,'m':m,'gap':gap,'bank_count':2*m+2,'p':p,'q_residue':q,'primitive_order':n,'rank_bound':bound,'recurrence_rank':rank,'equations':labels,'recurrence_matrix':rows,'defining_equation_indices':eq_rows,'defining_equation_labels':[labels[i] for i in eq_rows],'solved_coefficient_indices':J,'fixed_coefficient_integer_values':{str(j):c[j] for j in free},'monic_coefficient':1,'defining_minor_residue':det(A,p),'annihilator_coefficients_residue':c,'constant_coefficient_residue':c[0],'resultant_residue':res,'axis_column_convention':'++ moments 0..m-1, singleton constant, -- moments 0..m-1','axis_columns':axiscols,'axis_minor_residue':axisdet,'all_rows_compatible_mod_p':True,'row_controls':row_cert}
 (ROOT/f'N{n}_LIFT_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
 return {k:out[k] for k in ['N','m','bank_count','p','q_residue','rank_bound','defining_minor_residue','constant_coefficient_residue','resultant_residue','axis_minor_residue']}

summary=[certify(n) for n in [13,17,35]]
n=11;p=23;q=2;s=data(n,p,q);A=[s[b-1][r:r+6] for b in [1,2] for r in range(len(s[b-1])-5)]
assert len(A)==6 and det(A,p)==4
(ROOT/'N11_FULL_QUINTIC_OBSTRUCTION.json').write_text(json.dumps({'N':11,'p':p,'q_residue':q,'moment_sequences':s[:2],'matrix':A,'determinant_residue':det(A,p),'scope':'At most five ++ nodes with one -+ singleton at alpha=1; no restriction on -- node count. Reflection gives the analogous -- obstruction.'},indent=2)+'\n')
(ROOT/'LIFT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
