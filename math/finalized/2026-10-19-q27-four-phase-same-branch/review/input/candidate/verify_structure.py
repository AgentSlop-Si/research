"""Fresh exact source, coefficient-ring, support and coverage verification."""
import hashlib, itertools, json, pathlib, math
from fractions import Fraction as Q
root=pathlib.Path(__file__).resolve().parent
sources={
 'CHART.json':('d0a7a859b27574b0fd327587ba9e831984a98714','5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98',3138),
 'PROOF.md':('794d745dab580b4ba2c335a25231f4018b24654e','dbc5794d7680b91102e41d2bfcdcd5ad92e488fc75460ea540fad7fe159edde8',13770),
 'REVIEW.md':('635e2a53bebbcdf9f703b7ab60b42e7ffefb982d','79adf45b1526f71728240f40c8fd2b7d3a019cda161a0b308b01b630dc307df2',15730)}
bindings={}
for name,(blob,sha,size) in sources.items():
 data=(root/'sources'/name).read_bytes()
 assert len(data)==size and hashlib.sha256(data).hexdigest()==sha
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
 bindings[name]={'git_blob':blob,'sha256':sha,'bytes':size,'commit':'7769fb444edb0b63ebbce7e31dc52966ba08f4f0'}
c=json.loads((root/'sources/CHART.json').read_text())
assert c['N']==8 and c['product_order']=='M=S2*S1' and c['sum_coefficients']==[1,1,1]
assert c['free_phase_indices']==list(range(7,24))
assert [s['seed'] for s in c['stages']]==[42420,42520]
def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def norm(z):return z[0]*z[0]+z[1]*z[1]
def serial(z):return [str(v) for v in z]
def variation(e):return sum(abs(e[k]-e[(k+1)%4]) for k in range(4))
p=1000000009
assert p>2 and all(p%d for d in range(2,math.isqrt(p)+1))
ii=[569522298,430477711]
assert all(i*i%p==p-1 for i in ii) and sum(ii)==p
holonomies=[];denom_checks=[];guards=[]
for s,st in enumerate(c['stages']):
 assert len(st['cycles'])==3 and all(sorted(cy)==list(range(8)) for cy in st['cycles'])
 assert len(st['gaussian_pairs'])==17
 gains=[(Q(1),Q(0))]*7
 for a,b in st['gaussian_pairs']:
  gains.append((Q(a*a-b*b,a*a+b*b),Q(2*a*b,a*a+b*b)))
  for i in ii:
   for sign in [-1,1]:
    residue=(a+sign*i*b)%p
    assert residue
    denom_checks.append({'stage':s,'pair':[a,b],'i_image':i,'sign':sign,'residue':residue})
 assert len(gains)==24 and all(norm(g)==1 for g in gains)
 for branch in range(3):
  h=(Q(1),Q(0))
  for g in gains[8*branch:8*branch+8]:h=mul(h,g)
  assert norm(h)==1 and h!=(Q(1),Q(0))
  hrow={'stage':s,'branch':branch,'exact':serial(h),'images':[]}
  grow={'stage':s,'branch':branch,'exact':serial((1-h[0],-h[1])),'images':[]}
  for i in ii:
   def reduce(q):assert q.denominator%p;return q.numerator*pow(q.denominator,-1,p)%p
   hm=(reduce(h[0])+i*reduce(h[1]))%p
   assert hm and (1-hm)%p
   hrow['images'].append(hm);grow['images'].append((1-hm)%p)
  holonomies.append(hrow);guards.append(grow)
V146=[e for e in itertools.product(range(4),repeat=4) if max(e)-min(e)<=2]
V126=[e for e in V146 if variation(e)<=4]
H27=[e for e in itertools.product(range(3),repeat=4) if max(e)-min(e)<=1 and variation(e)<=2]
removed=[e for e in V146 if e not in V126]
assert (len(V146),len(V126),len(H27),len(removed))==(146,126,27,20)
assert (0,0,0,0) in V126
# Finite support-set checks supplement, not replace, the written universal proof.
for e in H27:
 assert tuple(2-v for v in e) in H27
 for f in H27:
  g=tuple(a+b for a,b in zip(e,f))
  assert max(g)-min(g)<=2 and variation(g)<=4
indices=[sum(e[k]*4**(3-k) for k in range(4)) for e in V126]
labels=[(s,b,tuple(8*b+j for j in edges)) for s in range(2) for b in [1,2] for edges in itertools.combinations(range(8),4)]
assert len(labels)==280 and len(set(labels))==280
coverage=[]
for fn,i in [('COVERAGE_PRIMARY.jsonl',ii[0]),('COVERAGE_CONJUGATE.jsonl',ii[1])]:
 rows=[json.loads(line) for line in (root/fn).read_text().splitlines()]
 assert len(rows)==280
 for number,(r,label) in enumerate(zip(rows,labels)):
  s,b,edges=label
  assert r['label']==number and (r['stage'],r['branch'],tuple(r['edges']))==label
  assert r['encoded']==[24*s+e for e in edges]
  assert r['rank']==126 and r['columns']==indices
  assert len(r['windows'])==len(set(r['windows']))==126
  assert all(0<=w<784 for w in r['windows'])
  assert r['prime']==p and r['i_image']==i and 0<r['determinant']<p
 coverage.append({'file':fn,'sha256':hashlib.sha256((root/fn).read_bytes()).hexdigest(),'labels':len(rows),'rank':126,'nonzero_fixed_minor_records':280,'full_windows_per_label':784})
result={'source_bindings':bindings,'prime':p,'primality_method':'complete trial division through floor(sqrt(p))','gaussian_images':ii,'denominator_checks':denom_checks,'holonomies':holonomies,'fixed_guards':guards,'support_counts':{'proposed':146,'actual_sharper':126,'entrywise_H':27,'removed':20},'removed_exponents':removed,'support126_columns':indices,'label_count':280,'coverage':coverage,'replay_costs_both_embeddings':{'labels':560,'matrix_numerator_builds':1120,'path_gain_multiplications':1120*6*8*7,'original_window_quotient_multiplybacks':560*784,'all_5power4_coefficients_per_multiplyback':625,'H_polynomial_coefficient_locations_checked':560*64*81,'Q_polynomial_coefficient_locations_checked':560*784*256,'minor_order':126,'selected_minor_count':560,'minor_input_coefficients':560*126*126,'P_convolution_scalar_multiplications':560*784*2*81*81}}
(root/'STRUCTURE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','labels':280,'embeddings':2,'support_dimensions':[146,126,27],'source_bytes_verified':sum(v[2] for v in sources.values()),'nonzero_minor_records':560,'full_polynomial_quotient_checks':560*784}))
