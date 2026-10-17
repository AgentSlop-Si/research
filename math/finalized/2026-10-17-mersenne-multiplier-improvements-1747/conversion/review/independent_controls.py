import importlib.util, sys, random, math, json, pathlib, hashlib, zipfile, ast, time
root=pathlib.Path(__file__).resolve().parent.parent/'source'
out=pathlib.Path(__file__).resolve().parent
import os
external=pathlib.Path(os.environ.get('MERSENNE_EXTERNAL_INPUTS',str(out.parents[1]/'external-inputs')))
spec=importlib.util.spec_from_file_location('reviewed',out/'inspected_fresh_conversion.py')
f=importlib.util.module_from_spec(spec); sys.modules[spec.name]=f; spec.loader.exec_module(f)
# Original seals remain evidence; portable checks gate the current publication.
publication=json.loads((out.parents[1]/'PUBLICATION_MANIFEST.json').read_text())
manifest={'files': {entry['path'].split('/')[-1]:entry for entry in publication['files'] if entry['path'].startswith('conversion/source/')}}
checks={k: {'bytes_match':len((root/k).read_bytes())==v['bytes'], 'sha256_match':hashlib.sha256((root/k).read_bytes()).hexdigest()==v['sha256']} for k,v in manifest['files'].items()}
assert all(v['bytes_match'] and v['sha256_match'] for v in checks.values())
pins=json.loads((root/'SOURCE_PINS.json').read_text()); pins_checks={}
p=pins['archive']; pins_checks[p['path']]=hashlib.sha256((external/p['path']).read_bytes()).hexdigest()==p['sha256']
with zipfile.ZipFile(external/p['path']) as z:
    for v in pins['inspected_archive_texts']:
        b=z.read(v['member']); pins_checks[v['member']]=len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
for v in pins['prior_reports']:
    pins_checks[v['path']]=hashlib.sha256((external/v['path']).read_bytes()).hexdigest()==v['sha256']
assert all(pins_checks.values())
start=time.time(); saved=f.run_controls(); runtime=time.time()-start
original=json.loads((root/'CONTROL_RESULTS.json').read_text()); assert saved==original
r=random.Random(202610171742); ledger=f.Ledger(); counts={}
def add(k): counts[k]=counts.get(k,0)+1
for m in range(2,10):
    p=(1<<m)-1
    values=list(range(-1000,1001))+[s*((1<<k)+t) for k in [m,m+1,5*m+1,17*m] for s in [-1,1] for t in [-1,0,1]]
    for x in values:
        assert f.mersenne_divmod(x,m,ledger)==divmod(x,p); add('signed_divisions')
for n in [0,1,2,3,4,7,8,9,15,16,17,31,32,33]:
    for _ in range(6):
        aa=[r.randrange(-100,101) for j in range(n)]
        for sig in [-1,1]:
            exp=[sum(math.comb(i,j)*aa[i]*sig**(i-j) for i in range(j,n)) for j in range(n)]
            assert f.taylor_shift(aa,sig,ledger)==exp; add('signed_shifts')
        assert f.taylor_shift(f.taylor_shift(aa,1,ledger),-1,ledger)==aa; add('inverse_pairs')
for m in [2,4,6,8,11]:
    p=(1<<m)-1
    for n in [0,1,2,3,5,9]:
        for _ in range(5):
            aa=[r.randrange(-2*p,2*p) for j in range(n)]
            val=sum(x*p**j for j,x in enumerate(aa))
            try: result=f.p_to_binary(aa,m,ledger)
            except ValueError: assert val<0
            else: assert result==val and val>=0
            add('signed_raw_p')
    for d in [1,2,3,7,17]:
        for _ in range(6):
            aa=[r.randrange(-(p**d),p**d) for j in range(4)]
            val=sum(x*p**(j*d) for j,x in enumerate(aa))
            try: result=f.grouped_raw_to_binary(aa,m,d,ledger)
            except ValueError: assert val<0
            else: assert result==val and val>=0
            add('signed_raw_grouped')
        for value in [0,1,p**d-1,p**d,p**(d+1)-1]:
            gg=f.binary_to_grouped(value,m,d,ledger)
            assert f.grouped_to_binary(gg,m,d,ledger)==value; add('group_boundaries')
        try: f.grouped_to_binary([p**d],m,d,ledger)
        except ValueError: add('reject_noncanonical_group')
        else: raise AssertionError('accepted group equal to radix')
# Check packing at maximal residues and unequal operand lengths.
for width in [1,2,7,8,15,16,31,64]:
    for na,nb in [(1,1),(1,7),(3,4),(8,8),(17,13)]:
        aa=[(1<<width)-1]*na; bb=[(1<<width)-1]*nb
        got,cap=f.convolution_mod_power_two(aa,bb,width,ledger)
        exp=[sum(aa[j]*bb[k-j] for j in range(na) if 0<=k-j<nb)&((1<<width)-1) for k in range(na+nb-1)]
        assert got==exp; add('max_residue_packed_convolutions')
# Single-group d>L path must not allocate a d-position shift.
probe=f.Ledger(); assert f.grouped_to_binary([1],2,1000000,probe)==1
assert max(s['length'] for s in probe.shifts)==1
result={'verdict':'all independent checks passed', 'manifest':checks,'source_pins':pins_checks,'full_controls_reproduced_exactly':True,'full_control_seconds':runtime,'additional_counts':counts,'d_greater_than_L_probe_shift_lengths':[s['length'] for s in probe.shifts], 'reviewed_code_sha256':hashlib.sha256((out/'inspected_fresh_conversion.py').read_bytes()).hexdigest()}
(out/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
