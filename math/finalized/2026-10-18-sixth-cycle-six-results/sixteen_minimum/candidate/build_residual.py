"""Exact finite indexing and generator for every length <=14 chirp candidate.
Standard library only. This file does not import or execute historical code.
"""
from itertools import product
import json, pathlib, time
ROOT=pathlib.Path(__file__).resolve().parent

def compositions(n,k,p=()):
    if k==1:
        yield p+(n,)
    else:
        for z in range(n+1):
            yield from compositions(n-z,k-1,p+(z,))

def rotate(n):
    ans=[0]*8
    for s,c in enumerate(n,1):
        q=3*s%16
        q=min(q,16-q)
        ans[q-1]+=c
    return tuple(ans)

def orbit(n):
    out=[]
    for _ in range(4):
        out.append(n); n=rotate(n)
    assert n==out[0]
    return tuple(sorted(set(out)))

def grouped_terms(n):
    """Return c_i as sparse integer polynomials; monomial has sum(n) entries."""
    offsets=[]; acc=0
    for z in n:
        offsets.append(acc); acc+=z
    coeffs=[{} for _ in range(16)]
    for degrees in product(*(range(z+1) for z in n)):
        exponent=[0]*acc
        for j,d in enumerate(degrees):
            if d: exponent[offsets[j]+d-1]=1
        residue=sum((s+1)*d for s,d in enumerate(degrees))%16
        e=tuple(exponent)
        coeffs[residue][e]=coeffs[residue].get(e,0)+1
    return coeffs

def variable_names(n):
    return [f'b{s}_{j}' for s,z in enumerate(n,1) for j in range(1,z+1)]

def encode_system(n):
    cs=grouped_terms(n)
    return {
        'counts':list(n), 'strides':list(range(1,9)),
        'field':{'symbol':'a','minimal_polynomial':'a^16+1','characteristic':0},
        'variables':variable_names(n)+['u'],
        'cyclic_coefficients':[[[list(e),v] for e,v in sorted(c.items())] for c in cs],
        'equations': [{'i':i,'form':'c_i - a^(i*i mod 32) c_0'} for i in range(1,16)]
                     + [{'form':'u*c_0 - 1'}],
        'interpretation':'Every c_i is explicitly stored. a^16=-1; each equation is over Q(a).',
        'legality':'Saturation by c_0 is exactly equivalent to saturation by all grouped factor resultants.',
    }

def main():
    start=time.monotonic()
    all_patterns=[n for n in compositions(14,8) if sum(n[s-1] for s in (1,3,5,7))>=8]
    cover={}
    for n in all_patterns:
        o=orbit(n); rep=o[0]
        cover.setdefault(rep,set()).add(n)
    rows=[]
    for rep, members in sorted(cover.items()):
        assert set(orbit(rep))==members
        rows.append({'representative':list(rep),'orbit':[list(x) for x in sorted(members)],
                     'status':'EXCLUDED_PURE_ODD_STRIDE' if sum(c>0 for c in rep)==1 else 'RESIDUAL_UNSOLVED'})
    assert len(all_patterns)==50940 and len(rows)==12922
    lengths={r:sum(1 for n in compositions(r,8) if sum(n[s-1] for s in (1,3,5,7))>=8)
             for r in range(8,15)}
    # Every shorter accepted candidate pads to length 14 with zero stride-one parameters.
    short_count=0
    aset=set(all_patterns)
    for r in range(8,15):
        for n in compositions(r,8):
            if sum(n[s-1] for s in (1,3,5,7))<8: continue
            padded=list(n); padded[0]+=14-r
            assert tuple(padded) in aset
            short_count+=1
    layers=[]
    for r in range(8,15):
        patterns=[n for n in compositions(r,8) if sum(n[s-1] for s in (1,3,5,7))>=8]
        reps=sorted({orbit(n)[0] for n in patterns})
        layers.append({'length':r, 'patterns':len(patterns), 'orbits':len(reps),
            'representatives':[list(n) for n in reps],
            'excluded_pure_odd_representatives':[list(n) for n in reps if sum(c>0 for c in n)==1]})
    (ROOT/'ALL_LENGTHS_INDEX.json').write_text(json.dumps({'field':'Q[a]/(a^16+1)',
        'status':'No legal attainment below 15 or complete exclusion is claimed.',
        'generator':'build_residual.encode_system(counts)', 'layers':layers},indent=2)+'\n')
    (ROOT/'RESIDUAL_INDEX.json').write_text(json.dumps({'padded_length':14,
        'patterns_before_symmetry':len(all_patterns), 'representatives':len(rows),
        'counts_by_literal_length':lengths, 'total_literal_patterns':short_count,
        'symmetry':'multiply strides by 3 mod 16, reverse signs, and Galois-conjugate the target root',
        'systems':rows},indent=2)+'\n')
    sample=(2,2,2,2,2,1,2,1)
    system=encode_system(sample)
    (ROOT/'BENCHMARK_SYSTEM.json').write_text(json.dumps(system,separators=(',',':'))+'\n')
    result={'patterns':len(all_patterns),'orbits':len(rows),'lengths':lengths,
            'total_literal_patterns':short_count,'orbits_by_length':{z['length']:z['orbits'] for z in layers},'benchmark_counts':sample,
            'benchmark_coefficient_terms':sum(map(len,grouped_terms(sample))),
            'benchmark_variables':len(variable_names(sample))+1,
            'elapsed_seconds':time.monotonic()-start}
    (ROOT/'INDEX_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
