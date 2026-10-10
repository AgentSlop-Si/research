import pathlib,json,hashlib,itertools
p=pathlib.Path('research_cycle_1635/v34_independent_audit')
tp=p/'source/extracted/fft_cyclotomic_zero_forcing_v34/topology_11.json'
t=json.loads(tp.read_text());L=t['layers'];N=t['n']; paths={}
for a,(u,j) in enumerate(L[0]):
 for b,(v,u2) in enumerate(L[1]):
  if u2!=u:continue
  for c,(i,v2) in enumerate(L[2]):
   if v2==v:paths.setdefault((i,j),[]).append((a,b,c))
forced=[0,0,0];unique=[]
for ij,ps in paths.items():
 if len(ps)==1:
  unique.append(ij)
  for layer,e in enumerate(ps[0]):forced[layer]|=1<<e
seen=[set(),set(),set()];full=(1<<N)-1
for line in (p/'restricted_seed_certificates.txt').read_text().splitlines():
 layer,deleted,seed=map(int,line.split()); assert 0<=layer<3 and 0<=deleted<1<<len(L[layer]);assert seed.bit_count()==3 and seed&~full==0
 assert not deleted&forced[layer] and deleted not in seen[layer];seen[layer].add(deleted)
 rows=[0]*N
 for e,(r,c) in enumerate(L[layer]):
  if not deleted>>e&1:rows[r]|=1<<c
 known=seed;used=set()
 while known!=full:
  found=False
  for r,mask in enumerate(rows):
   unknown=mask&~known
   if unknown and unknown&(unknown-1)==0:
    assert r not in used
    used.add(r);known|=unknown;found=True;break
  assert found
 assert len(used)==N-3
for l in range(3):assert len(seen[l])==1<<(len(L[l])-forced[l].bit_count())
out={'status':'PASS','independent_root_verifier':True,'unique_paths':len(unique),'forced_unit_counts':[x.bit_count() for x in forced],'masks_per_layer':list(map(len,seen)),'total_certificates':sum(map(len,seen)),'guaranteed_layer_rank':N-3,'guaranteed_product_rank':3*(N-3)-2*N,'topology_sha256':hashlib.sha256(tp.read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256((p/'restricted_seed_certificates.txt').read_bytes()).hexdigest(),'scope':'Integral matrices on the fixed support with all output entries units, residue Fourier rank one; not poles or arbitrary complex weights.'}
(p/'ROOT_INDEPENDENT_CERTIFICATE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
