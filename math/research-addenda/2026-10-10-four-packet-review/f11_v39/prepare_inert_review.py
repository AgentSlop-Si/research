# Publication adaptation of reviewer-authored checker.
# Original SHA-256: b7c5faffa05c196decb54859efd6bac64f7f1377b1cb2f4d16290cecca1fe606
# Changes: Replaced archive/baseline/provider metadata blocks with bundled inert-input hash verification. Topology, paths and both complete sample preparations unchanged.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
import pathlib,json,hashlib,collections,math
ROOT=pathlib.Path(__file__).resolve().parent
PACK=ROOT/'inert_packet/fft_transfer_quartic_circuit_v39'
def sha(b):return hashlib.sha256(b).hexdigest()
_publication_inputs=json.loads((ROOT/'PUBLICATION_INPUT_HASHES.json').read_text())
for _name,_hash in _publication_inputs.items():
 assert hashlib.sha256((ROOT/_name).read_bytes()).hexdigest()==_hash, _name
topbytes=(PACK/'topology_11.json').read_bytes()
assert sha(topbytes)=='4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a9a1ba59fd79a76a9b'
L=json.loads(topbytes)['layers'];assert len(L)==3 and all(len(x)==33 and len(set(map(tuple,x)))==33 for x in L)
assert list(map(tuple,[e for layer in L for e in layer]))==[tuple(map(int,x.split())) for x in (PACK/'topology_edges.txt').read_text().splitlines()]
for layer in L:
 assert collections.Counter(x[0] for x in layer)==collections.Counter({i:3 for i in range(11)})
 assert collections.Counter(x[1] for x in layer)==collections.Counter({i:3 for i in range(11)})
# Sparse propagation keeps path-edge labels in chronological order.
paths=[]
for source in range(11):
 states=[[] for _ in range(11)];states[source]=[()]
 for lev,layer in enumerate(L):
  nxt=[[] for _ in range(11)]
  for eid,(dst,src) in enumerate(layer):nxt[dst].extend(p+(33*lev+eid,) for p in states[src])
  states=nxt
 paths.append(states)
P=[paths[j][i] for i in range(11) for j in range(11)]
assert sum(map(len,P))==297
(ROOT/'paths.json').write_text(json.dumps(P))
mask=(1<<64)-1
sample_results=[]
for prime,seed,kind,expected in [(1000003,20261011,'xorshift',6774884542161267937),(1000033,972524161,'lcg',11690676381034439803)]:
 assert all(prime%d for d in range(2,math.isqrt(prime)+1))
 state=seed;H=[];weights=[]
 for s in range(24):
  w=[]
  for e in range(99):
   if kind=='xorshift':
    state^=(state<<13)&mask;state^=state>>7;state^=(state<<17)&mask;state&=mask
   else:state=(6364136223846793005*state+1442695040888963407)&mask
   w.append(1+state%(prime-1))
  weights.append(w)
  # Transfer via input-basis propagation, using no saved evaluated values.
  matrix=[]
  for j in range(11):
   vec=[int(i==j) for i in range(11)]
   for lev,layer in enumerate(L):
    out=[0]*11
    for eid,(dst,src) in enumerate(layer):out[dst]=(out[dst]+w[33*lev+eid]*vec[src])%prime
    vec=out
   matrix.append(vec)
  h=[matrix[j][i] for i in range(11) for j in range(11)]
  assert h==[sum(math.prod(w[e] for e in path) for path in ps)%prime for ps in P]
  H.append(h)
 fnv=14695981039346656037
 for x in sum(H,[]):fnv=((fnv^x)*1099511628211)&mask
 assert fnv==expected
 name=f'samples_{prime}.txt';(ROOT/name).write_text('\n'.join(' '.join(map(str,row)) for row in H)+'\n')
 sample_results.append({'prime':prime,'prime_trial_division_verified':True,'seed':seed,'generator':kind,'samples':24,'entries':2904,'fnv64':str(fnv),'sample_text_sha256':sha((ROOT/name).read_bytes()),'two_independent_transfer_methods_agree':True})
result={'topology_sha256':sha(topbytes),'path_histogram':dict(sorted(collections.Counter(map(len,P)).items())),'samples':sample_results,'historical_archive_and_baseline_replay':'not performed; excluded from publication payload'}
(ROOT/'publication_preparation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
