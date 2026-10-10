"""Fresh independent arithmetic/data controls. No supplied source is executed, imported, compiled, or parsed."""
from pathlib import Path
from fractions import Fraction
import json,math,hashlib
O=Path(__file__).parent;E=json.load(open(O/'EVIDENCE_INDEX.json'));P=json.load(open(O/'PROVENANCE.json'))
checks=[]
def add(name,ok,details):
 assert ok,name
 checks.append({'name':name,'pass':bool(ok),'details':details})
def evidence(index,basename):
 prefix=P[index]['member'].rsplit('/',1)[0]+'/'
 exact=[e for e in E if e['member']==prefix+basename]
 if not exact:
  exact=[e for e in E if e['sha256'] in P[index]['stored_evidence_hashes'] and Path(e['member']).name==basename]
 assert len(exact)==1,(index,basename)
 return json.loads((O/exact[0]['local']).read_text())
def det_integer(a):
 # Exact integer Bareiss elimination; modular evidence is independently checked by reduction at end.
 a=[r[:] for r in a];sign=1;prev=1;n=len(a)
 for c in range(n-1):
  piv=next((i for i in range(c,n) if a[i][c]),None)
  if piv is None:return 0
  if piv!=c:a[c],a[piv]=a[piv],a[c];sign=-sign
  v=a[c][c]
  for i in range(c+1,n):
   for j in range(c+1,n):
    numerator=v*a[i][j]-a[i][c]*a[c][j]
    assert numerator%prev==0
    a[i][j]=numerator//prev
   a[i][c]=0
  prev=v
 return sign*a[-1][-1]
# The two Weyl equations leave a scalar degree of freedom, so a seed is essential.
for n,omega in [(4,22),(16,8)]:
 p=97;f=[[pow(omega,-i*j,p) for j in range(n)] for i in range(n)]
 left=all(f[i][(j+1)%n]==pow(omega,-i,p)*f[i][j]%p for i in range(n) for j in range(n))
 right=all(f[i][j]*pow(omega,-j,p)%p==f[(i+1)%n][j] for i in range(n) for j in range(n))
 add('negative Fourier Weyl pairs',left and right,{'N':n,'p':p,'root':omega,'entries':n*n})
 add('scale ambiguity remains',all((2*f[i][0])%p==2 for i in range(n)),{'N':n,'twice_Fourier_first_column':2,'required_seed':1})
# Scalar spectral partial fractions are a different control from archived matrix computations.
for b in (2,4,8):
 p=97;xi=pow(5,96//b,p);count=0
 for t in range(p):
  if pow(t,b,p)==1:continue
  for s in range(b):
   lhs=sum(pow(xi,-r*s,p)*pow((1-t*pow(xi,r,p))%p,-1,p) for r in range(b))*pow(b,-1,p)%p
   rhs=pow(t,s,p)*pow((1-pow(t,b,p))%p,-1,p)%p
   assert lhs==rhs;count+=1
 add('character packet scalar identity',True,{'p':p,'packet_width':b,'pairs_checked':count})
# Repeated profiles cannot create cross-block identity entries.
for m in (2,4,8):
 k=2*m;p=65537;w=pow(3,65536//m,p)
 gram=[[sum(pow(w,(a-b)*i,p) for i in range(m))*pow(m,-1,p)%p for b in range(k)] for a in range(k)]
 projected=[[gram[a][b] if a==b else 0 for b in range(k)] for a in range(k)]
 add('physical identity projection differs from repeated Gram',gram[0][m]==1 and projected[0][m]==0 and all(projected[a][b]==int(a==b) for a in range(k) for b in range(k)),{'m':m,'k':k})
# Stored minors are proof objects, not execution receipts.
seed=evidence(7,'VERIFIED_RESULTS.json')['seed'];seed_rows=seed['fixed_prefix_rejection_rows'];p=998244353
add('N16 archived 9x9 obstruction determinants',all(det_integer(row['augmented_minor'])%p==row['augmented_determinant']!=0 for row in seed_rows),{'rows':len(seed_rows),'first_determinant':seed_rows[0]['augmented_determinant'],'method':'new integer Bareiss then field reduction; stored matrices only'})
phase=evidence(11,'PHASE33_RESULTS.json')['two_term_certificates']
add('archived Phase33 6x6 determinants',all(det_integer(r['minor'])%r['prime']==r['determinant']!=0 for r in phase),{'certificates':len(phase),'method':'new integer Bareiss then field reduction; stored matrices only'})
scan=evidence(21,'scan_certificate.json')
for f in scan['finite_fields']:
 p,z=f['p'],f['root'];rows=scan['nonzero_17_minor_physical_rows'];cols=scan['nonzero_17_minor_physical_cols'];m=[[pow(z,i*j,p) for j in cols] for i in rows]
 add('N64 Fourier 17x17 determinant reconstructed',det_integer(m)%p==f['shared_minor_det']!=0,{'prime':p,'root':z,'determinant':f['shared_minor_det'],'method':'new integer Bareiss over independently built powers; no graph reexecution'})
t=evidence(17,'nonlinear_tangent_certificate_N16.json');p=t['modulus'];q=t['normal_vector_flattened'];dot=sum(q[int(k)]*v for k,v in t['delta_sparse_flattened'].items())%p
add('saved tangent normal separates delta',dot==4599,{'field':p,'q_dot_delta':dot,'does_not_recompute_J_or_G':True})
add('tangent certificate field is prime',p>=2 and all(p%d for d in range(2,math.isqrt(p)+1)),{'p':p})
add('tangent NumPy int64 safety bound for fixed certificate',288*(p-1)**2<2**63,{'largest_conservative_dot_terms':288,'bound':288*(p-1)**2,'limit':2**63-1,'all_reduced_entries_at_most':p-1})
p=998244353;add('Phase13 block-8 modular matmul safety',8*(p-1)**2<2**63,{'bound':8*(p-1)**2,'limit':2**63-1,'note':'requires reduced inputs, as supplied callers provide'})
sumexp=sum(Fraction(7,4)**k/math.factorial(k) for k in range(6));lens=Fraction(2,3)*Fraction(7,125)+Fraction(2,15)*Fraction(49,3125)/(1-Fraction(7,25))
add('area-separator tail exact constants',sumexp==Fraction(700667,122880)>Fraction(50,9) and lens==Fraction(679,16875) and lens*Fraction(8,3)<Fraction(27,250),{'exp_lower':str(sumexp),'lens_coefficient':str(lens),'not_full_analytic_theorem_recheck':True})
add('area tail polynomial is positive and increasing from 256',17*256**2-4216*256-1108==33708 and 34*256-4216>0,{'positive_scaled_gap':33708,'positive_derivative':34*256-4216,'coefficient_of_M_squared':17})
add('Haar fixed-width exponent comparison',31**200<32**199,{'inequality':'31^200 < 32^199','no_short_word_constructed':True})
# Exact arithmetic on certificate dimensions and preserved results.
c=evidence(16,'superconcentrator_N8_certificate.json');counts={str(k):math.comb(8,k)**2 for k in range(1,9)}
add('N8 cut cardinalities',c['flow_counts_by_size']==counts and sum(counts.values())==12869,{'nonempty_pairs':sum(counts.values()),'no_maxflow_run_in_this_control':True})
old=evidence(16,'independent_nonlinear_results.json');portable=evidence(16,'portable_verification.json')['results']['independent_nonlinear_results.json'];a={k:v for k,v in old.items() if k!='seconds'};b={k:v for k,v in portable.items() if k!='seconds'}
add('N8 stored replay semantic equality except elapsed time',a==b,{'original_seconds':old['seconds'],'replay_seconds':portable['seconds'],'byte_identical':old==portable})
(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'source_execution':'none','method':'new reviewer arithmetic and stored-data reconstruction only','checks':checks,'all_pass':True},indent=2))
print('Fresh reviewer controls:',len(checks),'all pass')
