"""Independent v4 arithmetic/data audit. Never imports uploaded programs."""
from pathlib import Path
import cmath
import hashlib
import json
import math
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
rng = random.Random(472106)

def packed_sums(rows, U, word_bits=64):
    G, B = len(rows), len(rows[0])
    q = (2*U*G).bit_length()
    lanes = word_bits//q
    assert lanes >= 1
    accum = [0]*((B+lanes-1)//lanes)
    for row in rows:
        for base in range(0, B, lanes):
            word = sum((row[t]+U) << (q*(t-base))
                       for t in range(base, min(base+lanes, B)))
            assert 0 <= word < 1 << word_bits
            accum[base//lanes] += word
            assert accum[base//lanes] < 1 << word_bits
    got = [((accum[t//lanes] >> (q*(t%lanes))) & ((1<<q)-1))-G*U
           for t in range(B)]
    want = [sum(row[t] for row in rows) for t in range(B)]
    assert got == want
    return got

guard_cases = guard_lanes = 0
for U in [1, 2, 7, 32, 127]:
    for G in [1, 2, 3, 8, 17, 64, 257]:
        for B in [1, 2, 7, 16, 65, 129, 257]:
            for kind in range(4):
                rows = [[(-U if kind == 0 else U if kind == 1 else
                          (-U if (a+b)%2 else U) if kind == 2 else
                          rng.randint(-U,U)) for b in range(B)] for a in range(G)]
                packed_sums(rows,U)
                guard_cases += 1
                guard_lanes += B

phase_cases = 0
for N in [1,2,3,5,8,17,31,64,127]:
    for Q in [2,4,8,16,32,128,1024]:
        for r in range(N):
            q = ((2*Q*r+N)//(2*N))%Q
            # Exact circular numerator distance; no floating-point decisions.
            distance = min(abs(Q*r-N*q), abs(Q*r-N*q-N*Q), abs(Q*r-N*q+N*Q))
            assert 2*distance <= N
            phase_cases += 1

decoder_cases = 0
max_error = max_ratio = 0.0
phases = [1,-1,1j,-1j]
for N in [1,2,3,5,8,17,31,64,127]:
    for B in [1,3,8,17,64,129]:
        for g,G in [(1,1),(2,3),(3,5),(4,8)]:
            h1,h2 = 1/32,1/64
            Q0 = 256
            Q1 = 1 << math.ceil(math.log2(256*B))
            U = 33
            atoms = [(rng.randrange(N),rng.randrange(4)) for _ in range(g*G)]
            bound = math.pi/Q0 + math.pi*(B-1)/Q1 + (h1+h2)/math.sqrt(2)
            for m0 in range(0,N,B):
                count=min(B,N-m0)
                real_rows,imag_rows=[],[]
                for group in range(G):
                    vals=[]
                    for t in range(count):
                        val=0j
                        for j,s in atoms[group*g:(group+1)*g]:
                            qa=((2*Q0*((j*m0)%N)+N)//(2*N))%Q0
                            qb=((2*Q1*j+N)//(2*N))%Q1
                            val += phases[s]*cmath.exp(-2j*math.pi*(qa/Q0+t*qb/Q1))
                        vals.append(val/g)
                    real_rows.append([round(v.real/h1) for v in vals])
                    imag_rows.append([round(v.imag/h1) for v in vals])
                sr=packed_sums(real_rows,U)
                si=packed_sums(imag_rows,U)
                for t in range(count):
                    approx=complex(round((h1*sr[t]/G)/h2)*h2,
                                   round((h1*si[t]/G)/h2)*h2)
                    exact=sum(phases[s]*cmath.exp(-2j*math.pi*j*(m0+t)/N)
                              for j,s in atoms)/(g*G)
                    error=abs(approx-exact)
                    assert error <= bound+1e-12,(N,B,g,G,error,bound)
                    max_error=max(max_error,error)
                    max_ratio=max(max_ratio,error/bound)
            decoder_cases += 1

source_data=HERE/'source_v4_results.json'
if not source_data.exists():
    source_data=ROOT/'extracted_0/results.json'
saved=json.loads(source_data.read_text())
rows=saved['packed_correctness']
slopes={}
for case in ['flat','random_phase','gaussian','spike_noise']:
    vals=[r for r in saved['sampling_scaling'] if r['case']==case]
    xs=[math.log(r['k']) for r in vals]
    ys=[math.log(r['median_normalized_sampling_error']) for r in vals]
    xm,ym=sum(xs)/len(xs),sum(ys)/len(ys)
    slopes[case]=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/sum((x-xm)**2 for x in xs)
saved_summary={
    'rows':len(rows),
    'max_decoder_error':max(r['decoder_error_normalized'] for r in rows),
    'violations':sum(r['decoder_error_normalized']>r['decoder_bound_normalized']+1e-12 for r in rows),
    'one_word_key_violations':sum(r['params']['descriptor_bits']*r['params']['g_used']>r['params']['word_bits'] for r in rows),
    'table_exponent_budget_violations':sum(r['params']['descriptor_bits']*r['params']['g_used']>r['params']['gamma']*math.log2(r['N']) for r in rows),
    'all_lookup_miss_rows':sum(r['table_entries']==r['lookup_count'] for r in rows),
    'total_cache_misses':sum(r['table_entries'] for r in rows),
    'total_lookups':sum(r['lookup_count'] for r in rows),
    'sampling_loglog_slopes':slopes,
    'clipped_budget_violations':[
        {'mode':kind,'log2N':r['log2N'],'stated_total':r['eta_total_budget'],
         'sampling_plus_decoder':r['eta_sample']+r['eta_total_budget']/2}
        for kind in ['cost_model_linear','cost_model_subfft'] for r in saved[kind]
        if r['eta_sample']+r['eta_total_budget']/2>r['eta_total_budget']+1e-12
    ]
}
manifest=ROOT/'extracted_2/fft_macro_wordram_checkpoint_20261009/MANIFEST.json'
manifest_count=None
if manifest.exists():
    obj=json.loads(manifest.read_text())
    for rel,digest in obj['files'].items():
        path=manifest.parent/rel
        assert path.is_relative_to(manifest.parent)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    manifest_count=len(obj['files'])

result={'independent_guard_cases':guard_cases,'independent_guard_lanes':guard_lanes,
        'independent_phase_rounding_cases':phase_cases,
        'independent_decoder_cases':decoder_cases,'max_decoder_error':max_error,
        'max_fraction_of_bound':max_ratio,'saved_data_audit':saved_summary,
        'macro_manifest_verified_files':manifest_count}
(HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
