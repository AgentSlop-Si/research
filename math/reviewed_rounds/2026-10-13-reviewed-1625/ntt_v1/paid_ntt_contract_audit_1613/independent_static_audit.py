"""Independent static/byte/integer checks only. Does not import/compile/run NTT or its generator."""
from pathlib import Path
from functools import lru_cache
from hashlib import sha256
from math import isqrt
from collections import Counter
import csv, json, struct
ROOT=Path('/workspace/scratch/928904ebc9b0')
BASE=ROOT/'paid_ntt_contract_1546'
OUT=ROOT/'paid_ntt_contract_audit_1613'
P=998244353
checks={}
files=json.loads((BASE/'FILES_SHA256.json').read_text())
checks['artifact_hashes']=[{'file':r['file'],'bytes_match':len((d:=(BASE/r['file']).read_bytes()))==r['bytes'],'hash_match':sha256(d).hexdigest()==r['sha256']} for r in files]
sources=json.loads((BASE/'SOURCE_IDENTITIES.json').read_text())['sources']
checks['source_hashes']=[{'path':r['path'],'bytes_match':len((d:=Path(r['path']).read_bytes()))==r['bytes'],'hash_match':sha256(d).hexdigest()==r['sha256'],'lines':len(d.splitlines())} for r in sources]
@lru_cache(None)
def split(n):
    if n==1:return 0,0
    if n==2:return 2,0
    a,b=split(n//2);c,d=split(n//4)
    return 6*(n//4)+a+2*c, n//4+2*(n//4-1)+b+2*d
counts=[]
for e in range(1,24):
    n=2**e;expected=(n*e,n*e//2-n+1)
    r2=(0,0)
    for l in range(1,e+1):
        L=2**l;blocks=n//L;r2=(r2[0]+blocks*(L//2)*2,r2[1]+blocks*(L//2-1))
    f4=(n if e%2 else 0,0);m=2 if e%2 else 1
    while m<n:
        blocks=n//(4*m);f4=(f4[0]+blocks*8*m,f4[1]+blocks*(m+3*(m-1)));m*=4
    dif=(0,0);L=n
    while L>=4:
        q=L//4;blocks=n//L;dif=(dif[0]+blocks*8*q,dif[1]+blocks*(q+3*(q-1)));L//=4
    if L==2:dif=(dif[0]+n,dif[1])
    exponent=(P-1)//n; pow_calls=exponent.bit_length()+exponent.bit_count()
    actual={'radix2':r2,'fused4':f4,'splitradix':split(n),'dif4':dif}
    assert all(x==expected for x in actual.values())
    assert pow_calls+n-1==n+35-e
    counts.append({'e':e,'n':n,'add_sub':expected[0],'mul':expected[1],'root_generation_mul':pow_calls+n-1,'all_four_loop_counts_match':True})
checks['source_loop_counts']=counts
static=list(csv.DictReader((BASE/'STATIC_COUNTS.csv').open()))
assert len(static)==92
for r in static:
    n=int(r['n']);e=n.bit_length()-1
    assert int(r['add_sub_calls_per_transform'])==n*e
    assert int(r['mul_mod_calls_per_transform'])==n*e//2-n+1
checks['static_count_rows_match']=len(static)
old=list(csv.DictReader(Path(sources[1]['path']).open()))
for r in old:
    n=int(r['n']);e=n.bit_length()-1
    assert int(r['adds'])==n*e and int(r['muls'])==n*e//2-n+1
checks['historical_csv_count_rows_match']=len(old)
assert all(P%d for d in range(2,isqrt(P)+1))
assert (2**23)*7*17==P-1
certificate=json.loads((BASE/'MODULUS_ROOT_CERTIFICATE.json').read_text())
for q in (2,7,17):assert pow(3,(P-1)//q,P)==certificate['primitive_order_checks'][str(q)]!=1
for r in certificate['length_root_checks']:
    n=r['n'];w=pow(3,(P-1)//n,P)
    assert w==r['omega'] and pow(w,n,P)==r['omega_to_n']==1
    assert pow(w,n//2,P)==r['omega_to_half_n']==P-1
    if n>=4:assert pow(pow(w,n//4,P),2,P)==P-1
checks['modulus_root_integer_checks']={'prime':True,'primitive':True,'lengths':len(certificate['length_root_checks']),'addition_upper_bound':2*(P-1),'product_upper_bound':(P-1)**2}
manifest=json.loads((BASE/'CORPUS_MANIFEST.json').read_text());data=(BASE/'corpus_inputs.bin').read_bytes()
assert len(data)==manifest['bytes']==33554304
assert sha256(data).hexdigest()==manifest['sha256']
limit=2**32//P*P
assert limit==manifest['rejection_limit']==3992977412
cursor=0;seen=[];dense=0;rejections=0
for r in manifest['vectors']:
    n=r['n'];case=r['case'];assert r['offset_bytes']==cursor and r['length_bytes']==4*n
    chunk=data[cursor:cursor+4*n];cursor+=4*n
    assert sha256(chunk).hexdigest()==r['sha256']
    observed=[x[0] for x in struct.iter_unpack('<I',chunk)]
    assert all(0<=v<P for v in observed)
    if case.startswith('dense_'):
        expected=[];counter=0
        while len(expected)<n:
            msg='paid-ntt-v1|2026-10-13|p=998244353|n=%d|case=%s|block=%d'%(n,case,counter)
            digest=sha256(msg.encode('ascii')).digest();counter+=1
            for i in range(0,32,4):
                z=int.from_bytes(digest[i:i+4],'little')
                if z>=limit:rejections+=1;continue
                expected.append(z%P)
                if len(expected)==n:break
        dense+=1
    elif case=='zero':expected=[0]*n
    elif case=='ones':expected=[1]*n
    elif case=='minus_ones':expected=[P-1]*n
    elif case=='ramp':expected=list(range(n))
    elif case=='alternating':expected=[1,P-1]*(n//2)
    else:
        j={'impulse_0':0,'impulse_1':1,'impulse_floor_n3':n//3}[case]
        expected=[int(i==j) for i in range(n)]
    assert observed==expected
    seen.append((n,case))
assert cursor==len(data) and len(seen)==288 and len(set(seen))==288
assert seen==[(n,c) for n in manifest['lengths'] for c in manifest['case_ids']]
checks['corpus_independent_reconstruction']={'vectors':len(seen),'dense_vectors':dense,'rejected_digest_words':rejections,'all_bytes_match':True,'all_coordinates_canonical':True,'global_sha256':sha256(data).hexdigest()}
order=json.loads((BASE/'PAIRED_ORDER.json').read_text())['orders']
assert len(order)==48 and [r['block'] for r in order]==list(range(48))
for s in (0,1):
    rows=order[s*24:(s+1)*24]
    assert len({tuple(r['algorithm_order']) for r in rows})==24
    assert all(r['session']==s for r in rows)
    tally=Counter((a,i) for r in rows for i,a in enumerate(r['algorithm_order']))
    assert len(tally)==16 and set(tally.values())=={6}
assert [r['algorithm_order'] for r in order[24:]]==[r['algorithm_order'] for r in order[:24]][::-1]
checks['paired_order']={'blocks':48,'all_24_permutations_per_session':True,'per_algorithm_position_per_session':6,'session_1_reverse_of_session_0':True,'first_order':order[0]['algorithm_order'],'string_lexicographic_first':sorted(order[0]['algorithm_order'])}
checks['pilot_design_counts']={'batches':48*2*2*4,'useful_transform_calls':48*4*2*(1+64),'discarded_warmup_transform_calls':48*4*2*4,'total_transform_calls_excluding_correctness_and_diagnostics':48*4*2*(1+64)+48*4*2*4,'k1_timed_cases':['dense_0'],'k64_useful_calls_per_dense_case_per_trial':8}
checks['execution_status']={'recovered_cpp_compiled':False,'recovered_cpp_run':False,'original_artifact_generator_run':False,'reference_transform_run':False,'new_performance_measurements':False}
(OUT/'INDEPENDENT_STATIC_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ('source_loop_counts','artifact_hashes')},indent=2))
