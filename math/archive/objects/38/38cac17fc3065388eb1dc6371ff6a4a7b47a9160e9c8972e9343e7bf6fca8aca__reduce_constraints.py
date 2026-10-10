import sympy as S
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
zsym=S.Symbol('z');z=S.CRootOf(zsym**4+1,3);K=QQ.algebraic_field(z)
R,*v=ring('t0,t1,t2,t3,w,q',K);t=v[:4];w,q=v[4:];Z=R.ground_new(K.unit);print('z',z,Z,flush=True)
pows=[Z**j for j in range(8)];sig=[2,7,5,0,6,1,3,4]
M=[[pows[(r*(j-j%2))%8]+(-1)**j*t[j//2]*pows[(r*(j-j%2+1))%8] for j in range(8)]for r in range(8)]
B=[M[0][j]+w*M[7][j] for j in range(8)]
rows={}
for r in range(1,8):
 row=[]
 for j in [1,2,4,5,6]:
  if r in [j,(j+1)%8,sig[j]]:continue
  c=B[sig[j]]*M[(r-1)%8][j]-B[j]*M[(r-1)%8][sig[j]]
  b=B[sig[j]]*M[r][j]-B[j]*M[r][sig[j]]
  row.append((j,b,c))
 rows[r]=row
 print('row',r,'cols',[j for j,b,c in row],flush=True)
 for j,b,c in row:print(' equation',j,':',b+q*c,flush=True)
 for ii in range(1,len(row)):
  j,b,c=row[0];jj,bb,cc=row[ii];e=b*cc-bb*c
  print(' RESULTANT',j,jj,'terms',len(e), 'factor:',e.factor_list(),flush=True)
