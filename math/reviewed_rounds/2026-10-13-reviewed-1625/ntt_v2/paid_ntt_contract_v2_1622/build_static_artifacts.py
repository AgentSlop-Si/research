"""New artifact generator. Does not load, import, compile, or execute the NTT source."""
import csv, hashlib, itertools, json, math, pathlib, struct
BASE=pathlib.Path(__file__).resolve().parent
SOURCE=BASE.parent/'top_unknown_sources_1148/downloads/FFT'
p=998244353
nlist=[1<<e for e in range(1,19)]
caseids=['zero','ones','minus_ones','impulse_0','impulse_1','impulse_floor_n3','alternating','ramp']+[f'dense_{r}' for r in range(8)]
limit=((1<<32)//p)*p

def vals(n,c):
    if c=='zero': return [0]*n
    if c=='ones': return [1]*n
    if c=='minus_ones': return [p-1]*n
    if c.startswith('impulse_'):
        j={'impulse_0':0,'impulse_1':1,'impulse_floor_n3':n//3}[c]
        a=[0]*n;a[j]=1;return a
    if c=='alternating': return [1 if j%2==0 else p-1 for j in range(n)]
    if c=='ramp': return list(range(n))
    a=[]; block=0
    while len(a)<n:
        s=f'paid-ntt-v1|2026-10-13|p=998244353|n={n}|case={c}|block={block}'.encode('ascii')
        for z in struct.unpack('<8I',hashlib.sha256(s).digest()):
            if z<limit:
                a.append(z%p)
                if len(a)==n: break
        block+=1
    return a
rows=[];offset=0;globalhash=hashlib.sha256()
with (BASE/'corpus_inputs.bin').open('wb') as out:
    for n in nlist:
        for c in caseids:
            data=struct.pack('<'+'I'*n,*vals(n,c));h=hashlib.sha256(data).hexdigest()
            out.write(data);globalhash.update(data)
            rows.append({'n':n,'case':c,'offset_bytes':offset,'length_bytes':len(data),'sha256':h})
            offset+=len(data)
manifest={'format':'little-endian uint32, no header; ascending n then case_ids order','modulus':p,'lengths':nlist,'case_ids':caseids,'generator':'build_static_artifacts.py','dense_definition':'SHA256 ASCII counter stream; eight little-endian uint32 words per block; reject z >= floor(2^32/p)*p, then z mod p; block starts at 0','rejection_limit':limit,'seed_template':'paid-ntt-v1|2026-10-13|p=998244353|n={n}|case={case}|block={block}','corpus_file':'corpus_inputs.bin','bytes':offset,'sha256':globalhash.hexdigest(),'vectors':rows}
(BASE/'CORPUS_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
prime=all(p%d for d in range(2,math.isqrt(p)+1))
root={'type':'fresh integer arithmetic certificate, not NTT execution','p':p,'primality_method':'trial division by every integer 2..floor(sqrt(p))','is_prime':prime,'primitive':3,'p_minus_1_factorization':{'2':23,'7':1,'17':1},'primitive_order_checks':{str(q):pow(3,(p-1)//q,p) for q in [2,7,17]},'length_root_checks':[]}
for e in range(1,24):
    n=1<<e;w=pow(3,(p-1)//n,p)
    root['length_root_checks'].append({'n':n,'omega':w,'omega_to_n':pow(w,n,p),'omega_to_half_n':pow(w,n//2,p)})
assert prime and all(v!=1 for v in root['primitive_order_checks'].values())
assert all(x['omega_to_n']==1 and x['omega_to_half_n']==p-1 for x in root['length_root_checks'])
(BASE/'MODULUS_ROOT_CERTIFICATE.json').write_text(json.dumps(root,indent=2)+'\n')
with (BASE/'STATIC_COUNTS.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['n','log2_n','algorithm','add_sub_calls_per_transform','mul_mod_calls_per_transform','status'])
    for e in range(1,24):
        n=1<<e
        for a in ['radix2','fused4','splitradix','dif4']:
            writer.writerow([n,e,a,n*e,n*e//2-n+1,'source-derived; not timing'])
perms=list(itertools.permutations(['radix2','fused4','splitradix','dif4']))
order=[]
for b in range(48):
    # One frozen algorithm-index permutation cycle and its reverse give exact position balance.
    order.append({'block':b,'session':b//24,'algorithm_order':list(perms[b%24 if b<24 else 23-(b%24)])})
(BASE/'PAIRED_ORDER.json').write_text(json.dumps({'blocks':48,'definition':'Two sessions of 24 blocks: permutations in frozen algorithm-index order [radix2,fused4,splitradix,dif4], then the reverse order','orders':order},indent=2)+'\n')
src=[]
for name in ['fft_engine.cpp','benchmark_final_ntt.csv']:
    data=(SOURCE/name).read_bytes();src.append({'path':str(SOURCE/name),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(BASE/'SOURCE_IDENTITIES.json').write_text(json.dumps({'sources':src,'missing_later_review_sha256':'32b9e8e7c33b69633e1616188b59e0f9ad643677680bbb5b6175ee5900ddf4d8','missing_review_not_rebound':True,'inherited_code_execution':False},indent=2)+'\n')
print(json.dumps({'corpus_bytes':offset,'corpus_sha256':manifest['sha256'],'vectors':len(rows),'prime':prime,'primitive_order_checks':root['primitive_order_checks']}))
