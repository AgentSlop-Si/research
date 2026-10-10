from pathlib import Path
import struct,json,hashlib,itertools,random
from prepare_and_check import macaulay
from independent_utils import family,components,rank
root=Path(__file__).resolve().parent;src=root/'extracted/fft_green_phase30_four_parameter';cert=src/'certificates';out={}
for n,p in [(8,998244353),(16,998244353),(8,2013265921)]:
 data=list(map(int,(root/f'four_N{n}_p{p}.txt').read_text().split()));encoded=struct.pack('<II',p,n)+struct.pack('<'+'I'*(len(data)-2),*data[2:]);actual=(cert/f'four_green_input_N{n}_p{p}.bin').read_bytes();assert encoded==actual;out[f'input_N{n}_p{p}_byte_identical']=True
checks=0
for line in (src/'SHA256SUMS.txt').read_text().splitlines():
 h,name=line.split(None,1);p=src/name.lstrip('*');assert p.is_file()and hashlib.sha256(p.read_bytes()).hexdigest()==h;checks+=1
out['source_checksum_entries_pass']=checks
fifth=[]
for n in (4,8,16):
 T,G,spec=family(n);p=spec['p'];X,_=components(n,(2800+n)*3+7,p,spec['root'],[11]);Y,_=components(n,(2800+n)*3+11,p,spec['root'],[13]);G+=X+Y;hist={};maps=[]
 if n==4:maps=itertools.product(itertools.permutations(range(4)),repeat=2)
 else:
  rng=random.Random(55130+n);maps=[(rng.sample(range(n),4),rng.sample(range(n),4))for _ in range(100)]
 for r,c in maps:
  rk=rank(macaulay(T,G,r,c,p),p);hist[rk]=hist.get(rk,0)+1;assert rk==35
 fifth.append({'n':n,'histogram':hist,'scope':'exhaustive full permutations'if n==4 else '100 independent sampled 4x4 matchings'})
 print('five term',n,hist,flush=True)
out['five_term_4x4']=fifth;(root/'EXTRA_RESULTS.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
