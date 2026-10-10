"""Fresh sparse reconstruction and full projective equal-outer exclusion checks.
Only generated certificate JSON is read; no uploaded program is imported.
"""
from pathlib import Path
import sympy as s,json,itertools
root=Path(__file__).resolve().parent;a,c,t=s.symbols('a c t');I=s.I;QQ=s.QQ_I;N=4
Z=s.zeros(4);R=s.zeros(4)
for j in range(4):Z[(j+1)%4,j]=1
for j,k in enumerate([0,2,1,3]):R[k,j]=1
G0=(s.eye(4)-Z/4).inv();G1=(s.eye(4)-R*Z*R.T/5).inv();F=s.Matrix([[I**(j*k)for k in range(4)]for j in range(4)])
# Each adjugate entry has degree at most 3, so four exact values determine it.
Acoef=[s.zeros(4)for _ in range(4)]
for v in range(4):
 adj=(G0+v*G1).adjugate();lag=s.Poly(s.prod((t-w)/s.Integer(v-w)for w in range(4)if w!=v),t)
 for deg in range(4):Acoef[deg]+=lag.nth(deg)*adj
# Independent polynomial identity guard for the reconstructed adjugate.
H=G0+t*G1;AP=sum((t**j*Acoef[j]for j in range(4)),s.zeros(4));d=s.factor(H.det());assert all(s.expand(x)==0 for x in H*AP-d*s.eye(4))
coeff={(u,v):Acoef[u]*F*Acoef[v]for u in range(4)for v in range(4)}
K={(i,j):s.Poly.from_dict({uv:s.expand(M[i,j])for uv,M in coeff.items()},(a,c),domain=QQ)for i in range(4)for j in range(4)}
# Check all middle entry-zero branches, without assuming outside regularity.
bs=sorted(set(-G0[i,j]/G1[i,j]for i in range(4)for j in range(4)),key=float);zeroresults=[]
for bv in bs:
 B=G0+bv*G1;positions=[(i,j)for i in range(4)for j in range(4)if B[i,j]==0];polys=[K[x]for x in positions];count=0
 for i,k in itertools.combinations(range(4),2):
  for j,l in itertools.combinations(range(4),2):
   if all(B[u,v]for u,v in [(i,j),(i,l),(k,j),(k,l)]):polys.append(K[i,j]*K[k,l]*B[i,l]*B[k,j]-K[i,l]*K[k,j]*B[i,j]*B[k,l]);count+=1
 gb=s.groebner(polys,c,a,domain=QQ,order='grevlex');assert len(gb)==1 and s.Poly(list(gb)[0]).total_degree()==0
 zeroresults.append({'b':str(bv),'zero_positions':positions,'supported_rectangles':count,'groebner_basis':['1']});print('zero branch passes',str(bv),flush=True)
# Equal-outer specialization and the b-coefficient rank minors.
Kt={}
for ij,P in K.items():
 dic={}
 for (u,v),co in P.terms():dic[(u+v,)]=dic.get((u+v,),0)+co
 Kt[ij]=s.Poly.from_dict(dic,t,domain=QQ)
rows=[]
for i in range(1,4):
 for j in range(1,4):
  X=Kt[i,j]*Kt[0,0];Y=Kt[i,0]*Kt[0,j]
  aa=[G0[i,0]*G0[0,j],G0[i,0]*G1[0,j]+G1[i,0]*G0[0,j],G1[i,0]*G1[0,j]];bb=[G0[i,j]*G0[0,0],G0[i,j]*G1[0,0]+G1[i,j]*G0[0,0],G1[i,j]*G1[0,0]]
  rows.append([X*aa[z]-Y*bb[z]for z in range(3)])
cert=json.loads((root/'N4_EQUAL_OUTER_RANK_CERTIFICATE.json').read_text());qs=[];records=[]
for rec in cert['records']:
 M=[rows[i]for i in rec['rows']];det=s.Poly(0,t,domain=QQ)
 for perm in itertools.permutations(range(3)):
  sg=(-1)**sum(perm[i]>perm[j]for i in range(3)for j in range(i+1,3));det+=sg*M[0][perm[0]]*M[1][perm[1]]*M[2][perm[2]]
 q,rem=det.div(Kt[0,0]);assert rem.is_zero;q=q.monic();assert q==s.Poly.from_list([s.sympify(v)for v in rec['quotient_coefficients']],t,domain=QQ);qs.append(q)
 records.append({'rows':rec['rows'],'raw_degree':det.degree(),'K00_degree':Kt[0,0].degree(),'quotient_degree':q.degree(),'coefficient_match':True})
assert qs[0].gcd(qs[1]).degree()==0
# Exact modular Bezout with all reduction guards checked.
bez=json.loads((root/'N4_EQUAL_OUTER_MODULAR_BEZOUT.json').read_text());p=bez['p'];ii=bez['image_i'];assert s.isprime(p)and ii*ii%p==p-1
for name,q in zip(('P','Q'),qs):
 co=[]
 for v in q.all_coeffs():
  re,im=s.expand(v).as_real_imag();rn,rd=re.as_numer_denom();jn,jd=im.as_numer_denom();assert int(rd)%p and int(jd)%p;co.append((int(rn)*pow(int(rd),-1,p)+ii*int(jn)*pow(int(jd),-1,p))%p)
 assert co==bez[name]and co[0]==1 and len(co)==31
val=[0]*60
for P,Q in [(bez['P'],bez['U']),(bez['Q'],bez['V'])]:
 for i,x in enumerate(P):
  for j,y in enumerate(Q):val[i+j]=(val[i+j]+x*y)%p
assert val==[0]*59+[1]
# At common outer infinity, the leading row-coefficient minor remains nonzero.
infrows=[[x.nth(12)for x in row]for row in rows];infdet=s.expand(s.Matrix(infrows[:3]).det());assert infdet!=0
out={'source_code_executed':False,'adjugate_reconstruction_identity_verified':True,'field':'Q(i)','middle_zero_branches':zeroresults,'equal_outer_rank_minors':records,'exact_gcd':'1','modular_bezout':{'p':p,'i_image':ii,'denominators_survive':True,'degree_preserved':True,'identity_verified':True},'common_outer_infinity':{'K00':str(Kt[0,0].nth(6)),'first_rank_minor_nonzero':str(infdet)},'middle_infinity':'Covered by the same nonzero Veronese coefficient vector (0,0,1) in the finite outer regular argument.','conclusion':'No projective equal-outer N4 factorization H_[u:v] L H_[r:s] M H_[u:v] equals F4 for nonzero coefficient pairs and invertible diagonal masks, with identity internal permutations. Unequal outer ratios are not covered.'}
(root/'VERIFIED_RESULTS.json').write_text(json.dumps(out,indent=2));print('FULL PROJECTIVE EQUAL-OUTER EXCLUSION VERIFIED',flush=True)
